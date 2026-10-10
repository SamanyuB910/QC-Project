"""Step 1b: (i) how much of the cost-Hamiltonian scale the objective keeps under each penalty choice;
(ii) native single-thread timings of each live pipeline step (for the judge-run estimate)."""
import time, json
import numpy as np
from common import *
from qsim import *
from s06_helpers import cost_vector

d = json.load(open(os.path.join(OUT, "s01_data_qubo.json"))); r = np.array(d["r"]); C = np.array(d["C"])
print("(i) penalty scale: spread of the 1287 feasible energies and the opt-to-2nd gap, in std units of the full cost Hamiltonian")
for lam in [0.1, 0.2, 0.5]:
    ps = float(np.max(np.abs(r) + lam * C.sum(1)))
    f0 = Inst(r, C, lam, 0).f0
    Pstar = max((f0[FEAS].min() - f0[HW == w].min()) / (w - K) ** 2 for w in range(N + 1) if w != K)
    for P, name in [(Pstar, "P*"), (0.3 * ps, "0.3xP_safe"), (ps, "P_safe"), (4.349349, "qiskit auto (lam=0.2 value)"), (1e5, "1e5 fallback")]:
        En = normalise(f0 + P * (HW - K) ** 2)
        s = np.sort(En[FEAS_IDX])
        print(f"  lam={lam} {name:28s} P={P:9.4f}  feasible spread={s[-1]-s[0]:.4f} std  opt-to-2nd gap={s[1]-s[0]:.2e} std")

print("\n(ii) native single-thread timings")
X, y, _ = load_data()
t = time.time(); rr = relevance(X, y, n_neighbors=10)[0]; print(f"  relevance kNN k=10, 20 seeds: {time.time()-t:.2f}s")
COST = cost_vector()
t = time.time(); I = Inst(rr, redundancy(X), 0.1, extra=0.1 * COST / 100); print(f"  enumerate 8192 + sort 1287: {time.time()-t:.3f}s")
t = time.time(); qaoa_xy(normalise(I.ff), [1.7], [0.17], COMPLETE_MAPS, dicke_init()); print(f"  numpy XY-complete p=1: {time.time()-t:.4f}s")
from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import Statevector
from qiskit.circuit.library import XXPlusYYGate
from qiskit_aer import AerSimulator
qc = QuantumCircuit(N)
for q in range(N):
    qc.ry(1.3, q)
for i in range(N):
    for j in range(i + 1, N):
        qc.rzz(0.1, i, j)
for (i, j) in complete_pairs():
    qc.append(XXPlusYYGate(-0.34), [i, j])
t = time.time(); tq = transpile(qc, basis_gates=["rzz", "rx", "rz"], optimization_level=2); print(f"  transpile: {time.time()-t:.2f}s ({tq.count_ops().get('rzz')} rzz)")
t = time.time(); Statevector(tq).probabilities(); print(f"  Statevector 13q: {time.time()-t:.2f}s")
tq.measure_all()
t = time.time(); AerSimulator().run([tq] * 5, shots=1000).result(); print(f"  Aer ideal 5 circuits x 1000 shots: {time.time()-t:.2f}s")
