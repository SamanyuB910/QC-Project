"""Prompt C, step 4: noisy Grover with Aer depolarizing noise at IonQ forte-1 rates
(1q 2.67e-4 on rx, 2q 4.95e-3 on rzz; rz virtual). Exact noisy probabilities via density matrix.

Regime A ("needle", M=1): one matching event in a real slice -> k_opt ~ (pi/4) sqrt(N).
Regime B ("real rate"): the real 2024 rate of shallow&M>=6 (~4.8%) -> k_opt ~ 3 regardless of N.
Metrics per n: P_noisy(k) for k=0..K; random-guess M/N; classical success with the same budget
(k oracle calls + 1 verification check -> k+1 random checks without replacement);
expected cost to first verified success with restarts: E = (k+1)/P(k), minimised over k (noise-aware k).
Also: global-depolarizing analytic model P ~ F*P_ideal + (1-F)*M/N, F=(1-15/16 p2)^G2 (1-3/4 p1)^G1, validated vs DM.
"""
import json, os, math, time, warnings
import numpy as np
warnings.filterwarnings("ignore")
from math import comb
from qiskit_aer import AerSimulator
import gs_core as G

rows = G.load_catalog()
nm = G.ionq_noise_model()
sim_dm = AerSimulator(method="density_matrix", noise_model=nm)
sim_id = AerSimulator(method="statevector")

def probs_marked(tqc, n, marked, sim):
    qc = tqc.copy(); qc.save_probabilities(qubits=list(range(n)))
    p = sim.run(qc).result().data()["probabilities"]
    return float(sum(p[i] for i in marked))

def p_classical(N, M, q):
    q = min(q, N)
    return 1.0 - comb(N - M, q) / comb(N, q) if M > 0 else 0.0

def analytic(N, M, k, G1, G2, p1=G.P1, p2=G.P2):
    F = (1 - 15 / 16 * p2) ** G2 * (1 - 3 / 4 * p1) ** G1
    return F * G.p_success_theory(N, M, k) + (1 - F) * M / N, F

def pick_slice(n, rng, want_M, pred):
    for _ in range(20000):
        sl = G.slice_events(rows, n, rng); mk = G.marked_indices(sl, pred)
        if len(mk) == want_M: return sl, mk
    return None, None

out = {}
for regime in ("A_needle_M1", "B_real_rate"):
    out[regime] = []
    rng = np.random.default_rng(11)
    for n in range(3, 11):
        N = 2**n
        if n > 10: break
        if regime == "A_needle_M1":
            # rarest sensible condition per size: shallow & M>=6 for small N, shallow & M>=7 for N>=128
            thr = 6.0 if n <= 6 else 7.0
            pred = lambda r, t=thr: G.predicate(r, mag_thr=t)
            sl, mk = pick_slice(n, rng, 1, pred)
            if sl is None:
                print(f"n={n}: no window with exactly 1 match for M>={thr}"); continue
        else:
            if N > len(rows): break
            sl = G.slice_events(rows, n, rng); mk = G.marked_indices(sl)
            thr = 6.0
            if len(mk) == 0: continue
        M = len(mk); kopt = G.k_opt(N, M)
        K = min(max(kopt + 3, 4), 2 * kopt + 2)
        O = G.list_oracle(n, mk)
        t0 = time.time(); rec = dict(method=('density_matrix' if n <= (8 if regime=='A_needle_M1' else 7) else 'analytic_global_depolarizing'), n=n, N=N, M=M, mag_thr=thr, k_opt=kopt, ks=[], p_ideal=[], p_noisy=[], p_analytic=[], F=[], G2=[], G1=[], p_classical_k1=[])
        for k in range(0, K + 1):
            qc = G.grover_circuit(n, O, k, measure=False)
            tq = G.to_ionq(qc)
            g2 = G.twoq(tq); g1 = sum(1 for i in tq.data if i.operation.name == "rx")
            pa, F = analytic(N, M, k, g1, g2)
            dm_max = 8 if regime == "A_needle_M1" else 7
            pn = probs_marked(tq, n, mk, sim_dm) if n <= dm_max else pa   # DM exact up to dm_max, validated analytic beyond
            rec["ks"].append(k); rec["p_ideal"].append(G.p_success_theory(N, M, k)); rec["p_noisy"].append(pn)
            rec["p_analytic"].append(pa); rec["F"].append(F); rec["G2"].append(g2); rec["G1"].append(g1)
            rec["p_classical_k1"].append(p_classical(N, M, k + 1))
        pn = np.array(rec["p_noisy"]); ks = np.array(rec["ks"])
        cost = (ks + 1) / np.maximum(pn, 1e-12)
        kb = int(np.argmin(cost))
        rec.update(rand_guess=M / N, classical_expected_checks=(N + 1) / (M + 1),
                   best_k_noise_aware=kb, best_expected_cost_noisy=float(cost[kb]),
                   ideal_expected_cost=float(min((k + 1) / G.p_success_theory(N, M, k) for k in range(K + 1))),
                   p_noisy_at_kopt=float(pn[kopt]), p_classical_same_budget=p_classical(N, M, kopt + 1),
                   sec=time.time() - t0)
        out[regime].append(rec)
        print(f"[{regime}] n={n:2d} N={N:5d} M={M:2d} k_opt={kopt:2d} 2Q@kopt={rec['G2'][kopt]:6d} "
              f"P_ideal={rec['p_ideal'][kopt]:.3f} P_noisy={pn[kopt]:.3f} (analytic {rec['p_analytic'][kopt]:.3f}) "
              f"M/N={M/N:.4f} P_cl(k+1 checks)={rec['p_classical_same_budget']:.3f} | "
              f"[{rec['method'][:3]}] noise-aware k={kb}: E[calls+checks]={cost[kb]:.1f} vs classical {(N+1)/(M+1):.1f} [{rec['sec']:.0f}s]", flush=True)

json.dump(out, open(os.path.join(G.HERE, "results_c04_noise.json"), "w"), indent=1)

import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
fig, axs = plt.subplots(1, 2, figsize=(11, 4.2))
for ax, regime in zip(axs, out):
    for rec in out[regime]:
        l, = ax.plot(rec["ks"], rec["p_noisy"], "o-", ms=3, label=f"n={rec['n']} M={rec['M']}")
        ax.plot(rec["ks"], rec["p_ideal"], ":", color=l.get_color(), lw=1)
        ax.axhline(rec["rand_guess"], color=l.get_color(), lw=.6, ls="--")
    ax.set_title(f"{regime}: noisy (solid) vs ideal (dotted); dashed = M/N")
    ax.set_xlabel("k"); ax.set_ylabel("P(success)"); ax.legend(fontsize=7); ax.grid(alpha=.3)
fig.tight_layout(); fig.savefig(os.path.join(G.HERE, "fig_c04_noise.png"), dpi=130)
print("saved fig_c04_noise.png")
