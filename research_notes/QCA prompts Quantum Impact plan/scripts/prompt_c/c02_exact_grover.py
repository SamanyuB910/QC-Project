"""Prompt C, step 2: exact-M Grover on real 2024 USGS slices (n=3..6), overshoot,
and verification that the HONEST QROM+comparator oracle marks exactly the same events
as the tutorial list oracle (which needs the answer list).
"""
import math, json, time, os, warnings
import numpy as np
warnings.filterwarnings("ignore")
from qiskit import transpile
from qiskit.quantum_info import Statevector
from qiskit_aer import AerSimulator
import gs_core as G

rows = G.load_catalog()
# 1. encoding validation over the whole catalog
bad = sum(1 for r in rows if G.predicate(r) != (G.mag_code(r["mag"]) >= G.mag_code(6.0) and G.depth_code(r["depth"]) < 7))
print(f"[encode] catalog N={len(rows)}; bit-level predicate disagreements with float predicate: {bad}")
print(f"[encode] mag code range used {min(G.mag_code(r['mag']) for r in rows)}..{max(G.mag_code(r['mag']) for r in rows)}, "
      f"events clipped at mag code 31: {sum(1 for r in rows if (r['mag']-5)*10>=31.999)}")

rng = np.random.default_rng(2026)
out = {"slices": {}, "curves": {}, "honest_check": {}}
# 2. distribution of M over random contiguous windows
for n in range(3, 7):
    N = 2**n
    Ms = [len(G.marked_indices(G.slice_events(rows, n, rng))) for _ in range(5000)]
    Ms = np.array(Ms)
    out["slices"][n] = dict(N=N, mean_M=float(Ms.mean()), frac_M0=float((Ms == 0).mean()),
                            hist={int(k): int((Ms == k).sum()) for k in range(0, Ms.max() + 1)})
    print(f"[slices] n={n} N={N}: mean M={Ms.mean():.2f}, P(M=0)={np.mean(Ms==0):.3f}, P(M=1)={np.mean(Ms==1):.3f}, P(M>=2)={np.mean(Ms>=2):.3f}")

# 3. pick one representative slice per n with M>=1 (fixed seed), success vs k
sim = AerSimulator(method="statevector")
rng = np.random.default_rng(7)
for n in range(3, 7):
    N = 2**n
    while True:
        sl = G.slice_events(rows, n, rng)
        mk = G.marked_indices(sl)
        if 1 <= len(mk) <= max(1, N // 8): break
    M = len(mk)
    K = max(2 * G.k_opt(N, M) + 3, 6)
    O = G.list_oracle(n, mk)
    curve = []
    for k in range(K + 1):
        sv = Statevector(G.grover_circuit(n, O, k, measure=False))
        p = float(sum(abs(sv.data[i])**2 for i in mk))
        curve.append(p)
    th = [G.p_success_theory(N, M, k) for k in range(K + 1)]
    out["curves"][n] = dict(N=N, M=M, marked=mk, k_opt=G.k_opt(N, M), p_sim=curve, p_theory=th,
                            events=[f"M{sl[i]['mag']:.1f} {sl[i]['depth']:.0f}km {sl[i]['place']}" for i in mk],
                            window=[sl[0]['time'], sl[-1]['time']])
    print(f"\n[grover] n={n} N={N} M={M} k_opt={G.k_opt(N,M)} marked={mk}")
    for i in mk: print(f"   match: M{sl[i]['mag']:.1f} depth {sl[i]['depth']:.0f} km  {sl[i]['place']}")
    print("   k : " + " ".join(f"{k:5d}" for k in range(K + 1)))
    print("   P : " + " ".join(f"{p:5.3f}" for p in curve))
    print("   th: " + " ".join(f"{p:5.3f}" for p in th))
    assert max(abs(a - b) for a, b in zip(curve, th)) < 1e-9

    # 4. honest oracle equivalence (same slice): marginal on index register must match
    t0 = time.time()
    OH = G.honest_oracle(n, sl)
    kk = G.k_opt(N, M)
    qc = G.grover_circuit(n, OH, kk, measure=False)
    qc.save_statevector()
    tq = transpile(qc, sim, optimization_level=0)
    sv = np.asarray(sim.run(tq).result().get_statevector())
    nq = OH.num_qubits
    probs = np.abs(sv)**2
    idx_marg = np.zeros(N); anc_nonzero = 0.0
    for b, p in enumerate(probs):
        if p < 1e-14: continue
        i = b & (N - 1)
        if b >> n: anc_nonzero += p
        idx_marg[i] += p
    p_honest = float(sum(idx_marg[i] for i in mk))
    out["honest_check"][n] = dict(qubits=nq, k=kk, p_success_honest=p_honest, p_success_list=curve[kk],
                                  ancilla_garbage_prob=anc_nonzero, sim_seconds=time.time() - t0)
    print(f"   honest oracle: {nq} qubits, k={kk}: P(success)={p_honest:.6f} vs list {curve[kk]:.6f}; "
          f"prob mass with dirty ancillas={anc_nonzero:.2e}; sim {time.time()-t0:.1f}s")

json.dump(out, open(os.path.join(G.HERE, "results_c02_exact_grover.json"), "w"), indent=1)

# plot
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(7.5, 4.2))
for n, c in out["curves"].items():
    ax.plot(range(len(c["p_sim"])), c["p_sim"], "o-", ms=3, label=f"n={n}, N={c['N']}, M={c['M']}")
ax.set_xlabel("Grover iterations k (= oracle calls)"); ax.set_ylabel("P(measure a matching event)")
ax.set_title("Exact-M Grover on real 2024 USGS slices (shallow & M>=6): overshoot")
ax.legend(fontsize=8); ax.grid(alpha=.3)
fig.tight_layout(); fig.savefig(os.path.join(G.HERE, "fig_c02_overshoot.png"), dpi=130)
print("saved fig_c02_overshoot.png")
