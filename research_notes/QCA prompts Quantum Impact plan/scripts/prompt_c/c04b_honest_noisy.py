"""Prompt C, step 4b: the HONEST QROM+comparator oracle under IonQ forte-1-rate noise (n=3, 18 qubits),
Aer statevector trajectories (shots), vs the list oracle and vs classical with the same budget."""
import json, os, math, time, warnings
import numpy as np
warnings.filterwarnings("ignore")
from qiskit_aer import AerSimulator
import gs_core as G

rows = G.load_catalog(); rng = np.random.default_rng(7)
n = 3; N = 8
while True:
    sl = G.slice_events(rows, n, rng); mk = G.marked_indices(sl)
    if 1 <= len(mk) <= 1: break
M = len(mk)
sim = AerSimulator(method="statevector", noise_model=G.ionq_noise_model())
out = []
for k in (0, 1, 2):
    qc = G.grover_circuit(n, G.honest_oracle(n, sl), k)
    tq = G.to_ionq(qc)
    t0 = time.time()
    shots = 2000
    counts = sim.run(tq, shots=shots, seed_simulator=17).result().get_counts()
    hits = sum(c for bs, c in counts.items() if int(bs, 2) in mk)
    p = hits / shots; se = math.sqrt(p * (1 - p) / shots)
    F = (1 - 15 / 16 * G.P2) ** G.twoq(tq)
    pa = F * G.p_success_theory(N, M, k) + (1 - F) * M / N
    pcl = 1 - math.comb(N - M, k + 1) / math.comb(N, k + 1)
    rec = dict(k=k, twoq=G.twoq(tq), p_noisy=p, se=se, p_analytic=pa, p_ideal=G.p_success_theory(N, M, k), p_classical_k_plus_1=pcl, sec=time.time() - t0)
    out.append(rec)
    print(f"honest oracle n=3 M={M} k={k}: 2Q={rec['twoq']:4d} P_noisy={p:.3f}+-{se:.3f} (analytic {pa:.3f}, ideal {rec['p_ideal']:.3f}) "
          f"| classical with k+1={k+1} checks {pcl:.3f} | {rec['sec']:.0f}s", flush=True)
json.dump(out, open(os.path.join(G.HERE, "results_c04b_honest_noisy.json"), "w"), indent=1)
