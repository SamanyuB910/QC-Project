"""Diagnose why the plain MinimumEigenOptimizer(QAOA(StatevectorSampler)) path is slow / memory-hungry at 13 qubits,
and time the fix (decompose the PauliEvolutionGate into rz/rzz before sampling)."""
import json, os, time, tracemalloc, warnings
import numpy as np
warnings.filterwarnings("ignore")
from qiskit_optimization import QuadraticProgram
from qiskit_optimization.converters import QuadraticProgramToQubo
from qiskit.circuit.library import QAOAAnsatz
from qiskit.quantum_info import Statevector
from qiskit.primitives import StatevectorSampler
from qiskit import transpile

HERE = os.path.dirname(os.path.abspath(__file__))
d = json.load(open(os.path.join(HERE, "results", "s01_data_qubo.json")))
r = np.array(d["r"]); C = np.array(d["C"]); F = d["features"]; n = 13; lam = 0.2
qp = QuadraticProgram()
for f in F:
    qp.binary_var(f)
qp.minimize(linear={F[i]: -r[i] for i in range(n)}, quadratic={(F[i], F[j]): lam * C[i, j] for i in range(n) for j in range(i + 1, n)})
qp.linear_constraint(linear={f: 1 for f in F}, sense="==", rhs=5)
qubo = QuadraticProgramToQubo().convert(qp)
op, offset = qubo.to_ising()
print("Ising terms:", len(op), flush=True)
for n_small in [9, 11, 13]:
    # same structure on the first n_small variables to see scaling of the naive path
    pass
ans = QAOAAnsatz(op, reps=1)
bound = ans.assign_parameters(np.array([0.3, 0.7]))
bound_m = bound.copy(); bound_m.measure_all()
print("ansatz top-level ops:", bound.count_ops(), flush=True)
# fixed path: decompose to rz/rzz/rx/h first
dec = transpile(bound_m, basis_gates=["rz", "rzz", "rx", "h", "sx", "x", "cx"], optimization_level=0)
t = time.time(); tracemalloc.start()
res = StatevectorSampler(seed=1).run([dec], shots=1024).result()
cur, peak = tracemalloc.get_traced_memory(); tracemalloc.stop()
print(f"decomposed circuit -> StatevectorSampler: {time.time()-t:.2f}s, python peak alloc {peak/1e6:.1f} MB", flush=True)
# naive path: sample the undecomposed ansatz (what QAOA(sampler=StatevectorSampler()) does)
for nq in [9, 11]:
    sub = QuadraticProgram()
    for f in F[:nq]:
        sub.binary_var(f)
    sub.minimize(linear={F[i]: -r[i] for i in range(nq)}, quadratic={(F[i], F[j]): lam * C[i, j] for i in range(nq) for j in range(i + 1, nq)})
    sub.linear_constraint(linear={f: 1 for f in F[:nq]}, sense="==", rhs=4)
    o2, _ = QuadraticProgramToQubo().convert(sub).to_ising()
    a2 = QAOAAnsatz(o2, reps=1).assign_parameters(np.array([0.3, 0.7])); a2.measure_all()
    t = time.time(); tracemalloc.start()
    StatevectorSampler(seed=1).run([a2], shots=1024).result()
    cur, peak = tracemalloc.get_traced_memory(); tracemalloc.stop()
    print(f"naive undecomposed ansatz, {nq} qubits: {time.time()-t:.2f}s per sampler call, python peak alloc {peak/1e6:.1f} MB", flush=True)
