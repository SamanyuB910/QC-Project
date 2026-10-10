"""Prompt C, step 10: (a) ONE-job packaging for IonQ (list of circuits in one backend.run; or packed registers),
(b) judge-run timing with pure-Qiskit primitives (what Pyodide would run; expect ~2-5x slower in browser).
"""
import math, time, json, os, warnings
import numpy as np
warnings.filterwarnings("ignore")
from qiskit import QuantumCircuit, transpile
from qiskit.primitives import StatevectorSampler
from qiskit.providers.basic_provider import BasicSimulator
from qiskit.quantum_info import Statevector
import gs_core as G

rows = G.load_catalog(); rng = np.random.default_rng(7)
out = {}
# --- (a1) list-of-circuits job: k = 0..K Grover sweep + pre-drawn BBHT schedule + FPAA, for one real slice (n=5)
n = 5; N = 32
while True:
    sl = G.slice_events(rows, n, rng); mk = G.marked_indices(sl)
    if 1 <= len(mk) <= 3: break
M = len(mk); O = G.list_oracle(n, mk)
sweep = [G.grover_circuit(n, O, k) for k in range(0, 9)]
# pre-drawn (non-adaptive) BBHT schedule: j_r ~ U[0, ceil(m_r)), m_{r+1} = min(6/5 m_r, sqrt N); stop rule applied in post-processing
m, js = 1.0, []
for r in range(12):
    js.append(int(rng.integers(0, max(1, math.ceil(m))))); m = min(1.2 * m, math.sqrt(N))
bbht = [G.grover_circuit(n, O, j) for j in js]
batch = sweep + bbht
t0 = time.time(); tb = [G.to_ionq(c) for c in batch]; t_tr = time.time() - t0
twoq = [G.twoq(c) for c in tb]
print(f"(a1) one job = {len(batch)} circuits (Grover sweep k=0..8 + {len(js)} pre-drawn BBHT rounds j={js}); n={n}, M={M}")
print(f"     2Q per circuit (IonQ-like): {twoq}; total 2Q in job {sum(twoq)}; transpile {t_tr:.1f}s")
for shots in (256, 1024):
    t0 = time.time(); res = StatevectorSampler(seed=5).run(batch, shots=shots).result(); t_sv = time.time() - t0
    t0 = time.time(); bres = BasicSimulator().run(transpile(batch, BasicSimulator()), shots=shots, seed_simulator=5).result(); t_bs = time.time() - t0
    print(f"     shots={shots}: StatevectorSampler {t_sv:.2f}s, BasicSimulator {t_bs:.2f}s (local CPython; browser Pyodide slower)")
# post-process BBHT: walk rounds in order until the measured index (one shot per round) is a match
pub = StatevectorSampler(seed=9).run(bbht, shots=1).result()
calls = 0
for r, (j, pr) in enumerate(zip(js, pub)):
    calls += j
    idx = int(list(pr.data.c.get_counts().keys())[0], 2) if hasattr(pr.data, "c") else int(list(pr.data[list(pr.data.keys())[0]].get_counts().keys())[0], 2)
    if idx in mk:
        print(f"     BBHT post-processed: success at round {r+1}, oracle calls {calls}, verification checks {r+1}"); break
out["a1"] = dict(n=n, M=M, js=js, twoq=twoq)

# --- (a2) packed registers: 4 independent n=6 Grover circuits (k=0..3) side by side on 24 qubits, one circuit
n6 = 6
while True:
    sl6 = G.slice_events(rows, n6, rng); mk6 = G.marked_indices(sl6)
    if 1 <= len(mk6) <= 3: break
O6 = G.list_oracle(n6, mk6)
packed = QuantumCircuit(4 * n6, 4 * n6)
for r, k in enumerate(range(4)):
    sub = G.grover_circuit(n6, O6, k, measure=False)
    packed.compose(sub, qubits=list(range(r * n6, (r + 1) * n6)), inplace=True)
packed.measure(range(4 * n6), range(4 * n6))
from qiskit_aer import AerSimulator
t0 = time.time()
cnt = AerSimulator(method="matrix_product_state").run(transpile(packed, AerSimulator(method="matrix_product_state")), shots=4000, seed_simulator=3).result().get_counts()
tp = time.time() - t0
succ = [0] * 4
for bs, c in cnt.items():
    v = int(bs, 2)
    for r in range(4):
        if ((v >> (r * n6)) & (2**n6 - 1)) in mk6: succ[r] += c
print(f"(a2) packed 4x(n=6) Grover k=0..3 on 24 qubits, M={len(mk6)}: decoded P(success) per register = "
      f"{[round(s/4000,3) for s in succ]} vs theory {[round(G.p_success_theory(64,len(mk6),k),3) for k in range(4)]} ({tp:.1f}s Aer MPS)")
out["a2"] = dict(M=len(mk6), p=[s / 4000 for s in succ], theory=[G.p_success_theory(64, len(mk6), k) for k in range(4)])

# --- (b) honest oracle in-browser feasibility: qiskit.quantum_info.Statevector (pure numpy) on 18-21 qubits
for nn in (3, 4):
    rng2 = np.random.default_rng(7)
    while True:
        s2 = G.slice_events(rows, nn, rng2); m2 = G.marked_indices(s2)
        if 1 <= len(m2) <= max(1, 2**nn // 8): break
    qc = G.grover_circuit(nn, G.honest_oracle(nn, s2), G.k_opt(2**nn, len(m2)), measure=False)
    tq = transpile(qc, basis_gates=["u", "cx"], optimization_level=1)
    t0 = time.time(); sv = Statevector(tq); dt = time.time() - t0
    probs = sv.probabilities(list(range(nn)))
    print(f"(b) honest oracle n={nn}: {qc.num_qubits} qubits, {len(tq.data)} u/cx gates; quantum_info.Statevector {dt:.1f}s; "
          f"P(success)={sum(probs[i] for i in m2):.4f}")
    out[f"b_honest_n{nn}"] = dict(qubits=qc.num_qubits, gates=len(tq.data), seconds=dt)
json.dump(out, open(os.path.join(G.HERE, "results_c10_one_job.json"), "w"), indent=1, default=str)
