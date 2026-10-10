"""Experiment 3b: the 'Will a quantum kernel help?' auditor applied to the exp3 label sets (real + engineered).
For each label set and each kernel family (classical: RBF grid + linear; quantum: FQK-full grid, PQK grid) we compute
Huang et al.'s label-specific model complexity s_K = y^T (K + lam I)^-1 y (Tr K = N, lam = 0.1) and take the family
minimum (the best-aligned member); then
  ratio  = s_C* / s_Q*   (>1: quantum kernel's generalisation bound sqrt(s/N) is better)
  g_min  = min over classical members of g(K_C || K_Q*)   (small => classical can match on ANY labels)
  learnable = s*/(N/lam) (fraction of the trivial upper bound N/lam; near 1 => nothing learns it)
Pre-registered verdict (written before looking at exp3 accuracies is NOT possible here, so we report it as a
post-hoc rule to be frozen for the build): 'quantum-favourable' iff ratio > 2 and min-family s_Q*/(N/lam) < 0.5.
"""
import os
os.environ.setdefault("OMP_NUM_THREADS", "4")
import json
import numpy as np
import qk_core as qc
import exp3_positive_control as e3   # module-level code builds Z, states, FQK, RBF and the label sets (deterministic)

N, lam = len(e3.yreal), 0.1
Z = e3.Z
KL = Z @ Z.T + 1.0
classical = {f"RBF g={g}": K for g, K in e3.RBF.items()}
classical["Linear"] = KL
FQKL, PQK = e3.extra()
quantum = {f"FQK c={c}": K for c, K in e3.FQK.items()}
quantum.update({f"PQK c={c} g={g}": K for (c, g), K in PQK.items()})
out = {}
for name in ["REAL", "HUANG(c=0.75)", "HUANG(c=0.35)", "OBS-1(c=0.75)", "OBS-3(c=0.75)", "OBS-3(c=0.35)",
             "HUANG(c=0.75)+10%noise", "OBS-3(c=0.75)+10%noise"]:
    y = e3.labels[name]
    ypm = 2 * y - 1
    sc = {k: qc.model_complexity(K, ypm, lam) for k, K in classical.items()}
    sq = {k: qc.model_complexity(K, ypm, lam) for k, K in quantum.items()}
    kc, kq = min(sc, key=sc.get), min(sq, key=sq.get)
    g_min = min(qc.geo_diff(K, quantum[kq], lam) for K in classical.values())
    ratio = sc[kc] / sq[kq]
    verdict = "quantum-favourable" if (ratio > 2 and sq[kq] / (N / lam) < 0.5) else ("unlearnable" if min(sc[kc], sq[kq]) / (N / lam) > 0.5 else "no quantum edge")
    out[name] = {"best_classical": kc, "s_C*": sc[kc], "best_quantum": kq, "s_Q*": sq[kq], "ratio_sC/sQ": ratio,
                 "g_min(lam=0.1)": g_min, "sqrtN": float(np.sqrt(N)), "s_C*/(N/lam)": sc[kc] / (N / lam),
                 "s_Q*/(N/lam)": sq[kq] / (N / lam), "verdict": verdict,
                 "kta_best_C": max(qc.kta(K, ypm) for K in classical.values()),
                 "kta_best_Q": max(qc.kta(K, ypm) for K in quantum.values())}
    print(name, {k: (round(v, 3) if isinstance(v, float) else v) for k, v in out[name].items()}, flush=True)
json.dump(out, open("results/exp3b_auditor.json", "w"), indent=1)

# ---- spectral task-model alignment (fraction of centred-label power in the top-k kernel eigenvectors), family max
def cum_align(K, ypm, ks=(10, 30, 100)):
    w, V = np.linalg.eigh((K + K.T) / 2)
    V = V[:, ::-1]
    yc = ypm - ypm.mean()
    p = np.cumsum((V.T @ yc) ** 2) / (yc @ yc)
    return {k: float(p[k - 1]) for k in ks}

eig_cache = {}
def fam_align(fam, ypm):
    best = {}
    for k, K in fam.items():
        if k not in eig_cache:
            w, V = np.linalg.eigh((K + K.T) / 2)
            eig_cache[k] = V[:, ::-1]
        V = eig_cache[k]
        yc = ypm - ypm.mean()
        p = np.cumsum((V.T @ yc) ** 2) / (yc @ yc)
        for kk in (10, 30, 100):
            if p[kk - 1] > best.get(kk, (-1, None))[0]:
                best[kk] = (float(p[kk - 1]), k)
    return best

classical_all = dict(classical)
quantum_all = dict(quantum)
quantum_all.update({f"FQK-linear c={c}": K for c, K in FQKL.items()})
for name in out:
    ypm = 2 * e3.labels[name] - 1
    ac, aq = fam_align(classical_all, ypm), fam_align(quantum_all, ypm)
    out[name]["align_top10_C"], out[name]["align_top10_Q"] = ac[10], aq[10]
    out[name]["align_top30_C"], out[name]["align_top30_Q"] = ac[30], aq[30]
    out[name]["align_top100_C"], out[name]["align_top100_Q"] = ac[100], aq[100]
    print(name, "top10 C/Q", ac[10], aq[10], "| top30", ac[30][0], aq[30][0], "| top100", ac[100][0], aq[100][0], flush=True)
json.dump(out, open("results/exp3b_auditor.json", "w"), indent=1)
