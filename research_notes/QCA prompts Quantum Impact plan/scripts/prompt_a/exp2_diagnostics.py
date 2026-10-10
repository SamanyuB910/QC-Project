"""Experiment 2: does quantum similarity capture structure a classical kernel misses?  Kernel diagnostics on WDBC.

Diagnostics use a label-free global StandardScaler+PCA (all 569 rows); they are reported, never used for model
selection.  Labels enter only in s_K (model complexity), KTA and task-model alignment.

(a) per n in {4, 8, 12} and kernel family/bandwidth: geometric difference g(K_RBF || K_Q) (Huang et al. 2021),
    model complexity s_K on the true labels, centred KTA, participation ratio, task-model alignment.
(b) exponential concentration: off-diagonal mean/variance vs n = 2..16 (fixed bw=1, bw=0.2, MinMax[0,1] and [0,pi] 'plain').
(c) bandwidth scaling: 5-fold CV accuracy (C tuned inside) vs bandwidth c for n = 4, 8, 12, 16.
"""
import os
os.environ.setdefault("OMP_NUM_THREADS", "2"); os.environ.setdefault("OPENBLAS_NUM_THREADS", "2")
import json, time
import numpy as np
from sklearn.model_selection import StratifiedKFold
from sklearn.svm import SVC
import qk_core as qc

X, y = qc.load_wdbc()
ypm = 2 * y - 1
ALL = np.arange(len(y))
out = {"a": {}, "b": {}, "c": {}}
t0 = time.time()

# ------------------------------------------------------------------ (a) diagnostics table
for n in [4, 8, 12]:
    Z = qc.fold_features(X, ALL, n)
    KR = {g: qc.rbf_kernel_z(Z, g) for g in [0.01, 0.03, 0.1, 0.3, 1.0]}
    KL = Z @ Z.T + 1.0  # linear kernel (with bias) as an extra classical reference
    fams = {}
    for g, K in KR.items():
        fams[f"RBF g={g}"] = K
    fams["Linear"] = KL
    for c in [0.05, 0.1, 0.2, 0.5, 1.0]:
        S = qc.zz_states(Z * c, 2, "full")
        fams[f"FQK-full c={c}"] = qc.fid_kernel(S)
        fams[f"PQK c={c} g=1"] = qc.pqk_from_bloch(qc.bloch(S, n), 1.0)
        fams[f"FQK-linear c={c}"] = qc.fid_kernel(qc.zz_states(Z * c, 2, "linear"))
        fams[f"SEP c={c}"] = qc.fid_kernel(qc.zz_states(Z * c, 2, "none"))
    mm = (Z - Z.min(0)) / (Z.max(0) - Z.min(0))
    fams["QSVC-plain minmax01"] = qc.fid_kernel(qc.zz_states(mm, 2, "full"))
    fams["QSVC-plain minmax0pi"] = qc.fid_kernel(qc.zz_states(mm * np.pi, 2, "full"))
    # classical reference for g: the RBF that is best by 5-fold CV here (diagnostic only) -> we report vs several
    rows = {}
    refs = {"RBF g=0.03": KR[0.03], "RBF g=0.3": KR[0.3]}
    for name, K in fams.items():
        r = {"offdiag_mean": float(qc.offdiag(K).mean()), "offdiag_var": float(qc.offdiag(K).var()),
             "kta": qc.kta(K, ypm), "s_K(lam=0.1)": qc.model_complexity(K, ypm, 0.1),
             "s_K(lam=0.01)": qc.model_complexity(K, ypm, 0.01)}
        for rn, KC in refs.items():
            r[f"g_vs_{rn}(lam=0.01)"] = qc.geo_diff(KC, K, 0.01)
            r[f"g_vs_{rn}(lam=0.1)"] = qc.geo_diff(KC, K, 0.1)
        r["g_vs_Linear(lam=0.01)"] = qc.geo_diff(KL, K, 0.01)
        r.update(qc.spectrum_stats(K, ypm))
        r.pop("eigs_top20")
        rows[name] = r
    out["a"][n] = rows
    print(f"(a) n={n} done {time.time()-t0:.0f}s", flush=True)

# ------------------------------------------------------------------ (b) concentration vs n
rng = np.random.default_rng(0)
sub = np.sort(rng.choice(len(y), 200, replace=False))
for n in [2, 4, 6, 8, 10, 12, 14, 16]:
    Z = qc.fold_features(X, ALL, n)[sub]
    mm = (Z - Z.min(0)) / (Z.max(0) - Z.min(0))
    row = {}
    for label, A, ent in [("full bw=1", Z, "full"), ("linear bw=1", Z, "linear"), ("full bw=0.2", Z * 0.2, "full"),
                          ("linear bw=0.2", Z * 0.2, "linear"), ("full bw=1/sqrt(n)", Z / np.sqrt(n), "full"),
                          ("plain minmax01 full", mm, "full"), ("plain minmax0pi full", mm * np.pi, "full")]:
        S = qc.zz_states(A, 2, ent)
        K = qc.fid_kernel(S)
        od = qc.offdiag(K)
        row[label] = {"mean": float(od.mean()), "var": float(od.var())}
        if label in ("full bw=1", "full bw=0.2"):
            P = qc.pqk_from_bloch(qc.bloch(S, n), 1.0)
            # PQK with FIXED gamma (not median-normalised) to expose concentration of the projected features
            R = qc.bloch(S, n).reshape(len(sub), -1)
            d = 0.5 * qc.sqdist(R)
            Pf = np.exp(-(1.0 / n) * d)
            row["PQK " + label + " (gamma=1/n fixed)"] = {"mean": float(qc.offdiag(Pf).mean()), "var": float(qc.offdiag(Pf).var())}
            row["Bloch length mean " + label] = float(np.linalg.norm(qc.bloch(S, n), axis=2).mean())
        del S
    out["b"][n] = row
    print(f"(b) n={n} done {time.time()-t0:.0f}s", flush=True)

# ------------------------------------------------------------------ (c) bandwidth scaling (non-nested, diagnostic)
def cv_acc_C(K, seed=0):
    sk = StratifiedKFold(5, shuffle=True, random_state=seed)
    best = 0
    for C in qc.CS:
        a = []
        for tr, te in sk.split(np.zeros(len(y)), y):
            m = SVC(kernel="precomputed", C=C).fit(K[np.ix_(tr, tr)], y[tr])
            a.append(m.score(K[np.ix_(te, tr)], y[te]))
        best = max(best, np.mean(a))
    return float(best)

for n in [4, 8, 12, 16]:
    Z = qc.fold_features(X, ALL, n)
    row = {}
    for c in [0.02, 0.05, 0.1, 0.2, 0.35, 0.5, 0.75, 1.0, 1.5]:
        S = qc.zz_states(Z * c, 2, "full")
        K = qc.fid_kernel(S)
        row[c] = {"acc_bestC": cv_acc_C(K), "offdiag_mean": float(qc.offdiag(K).mean())}
        del S
    out["c"][n] = row
    print(f"(c) n={n}", {c: round(v['acc_bestC'], 3) for c, v in row.items()}, f"{time.time()-t0:.0f}s", flush=True)

json.dump(out, open("results/exp2_diagnostics.json", "w"), indent=1, default=str)
print("saved")
