"""Experiment 3: POSITIVE CONTROL for the 'does quantum similarity capture structure a classical kernel misses?' auditor.

Same WDBC inputs (label-free global scaler + PCA to n=8, unit variance), but labels engineered so that a
quantum kernel SHOULD win.  If the auditor (g_CQ, s_C/s_Q, KTA, nested-CV paired difference) flags these and
does NOT flag the real labels, it can detect an advantage when one exists.

Label sets:
  REAL          : true malignant/benign labels (negative control)
  HUANG(c_q)    : Huang et al. 2021 construction: y = sign(sqrt(K_Q) v - median), v = top eigvec of
                  sqrt(K_Q)(K_C + lam I)^-1 sqrt(K_Q)   (K_Q = FQK-full at bandwidth c_q, K_C = RBF g=0.3)
  OBS-k(c_q)    : y = sign(<psi_cq(x)| P |psi_cq(x)> - median) for a weight-k Pauli-Z string P (k = 1, 3)
                  (a 'label defined by a quantum measurement of the patient's encoding')
  + 10% label noise variants of HUANG and OBS-3.
Models (nested CV, 3 repeats x 5 outer, 3 inner; features fixed): LR, RBF (tuned g, C), HGB (tuned), FQK-full (tuned c, C),
FQK-linear, PQK (tuned c, gamma, C).
"""
import os
os.environ.setdefault("OMP_NUM_THREADS", "2"); os.environ.setdefault("OPENBLAS_NUM_THREADS", "2")
import json, time
import numpy as np
from sklearn.model_selection import StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import roc_auc_score
import qk_core as qc
from exp1_nested_cv import fit_eval_feat

from multiprocessing import Pool
t0 = time.time()
X, yreal = qc.load_wdbc()
N = len(yreal)
n = 8
Z = qc.fold_features(X, np.arange(N), n)
BW = [0.02, 0.05, 0.1, 0.35, 0.75]
RBF_G = [0.003, 0.01, 0.03, 0.1, 0.3, 1.0, 3.0, 10.0]
states = {c: qc.zz_states(Z * c, 2, "full") for c in BW}
FQK = {c: qc.fid_kernel(S) for c, S in states.items()}
RBF = {g: qc.rbf_kernel_z(Z, g) for g in RBF_G}
_EXTRA = {}
def extra():
    if not _EXTRA:
        _EXTRA["FQKL"] = {c: qc.fid_kernel(qc.zz_states(Z * c, 2, "linear")) for c in BW}
        P = {}
        for c, S in states.items():
            R = qc.bloch(S, n)
            for g in [0.3, 3.0]:
                P[(c, g)] = qc.pqk_from_bloch(R, g)
        _EXTRA["PQK"] = P
    return _EXTRA["FQKL"], _EXTRA["PQK"]

rng = np.random.default_rng(7)
labels = {"REAL": yreal}
for c_q in [0.35, 0.75]:
    g, v, sQ = qc.geo_diff_vec(RBF[0.3], FQK[c_q], lam=0.1)
    f = sQ @ v
    labels[f"HUANG(c={c_q})"] = (f > np.median(f)).astype(int)
    if __name__ == "__main__": print(f"HUANG c={c_q}: g={g:.2f}")
def zstring_expect(S, qubits):
    B = qc.bits_matrix(n)
    sign = (-1.0) ** B[:, qubits].sum(1)
    return (np.abs(S) ** 2) @ sign
for c_q in [0.35, 0.75]:
    for k, qs in [(1, [0]), (3, [0, 3, 6])]:
        f = zstring_expect(states[c_q], qs)
        labels[f"OBS-{k}(c={c_q})"] = (f > np.median(f)).astype(int)
for name in ["HUANG(c=0.75)", "OBS-3(c=0.75)"]:
    yy = labels[name].copy()
    flip = rng.choice(N, int(0.1 * N), replace=False)
    yy[flip] = 1 - yy[flip]
    labels[name + "+10%noise"] = yy


def audit_diag(y):
    ypm = 2 * y - 1
    # classical reference = best RBF by KTA (label-aware but cheap; diagnostic only)
    kc_key = max(RBF, key=lambda g: qc.kta(RBF[g], ypm))
    kq_key = max(FQK, key=lambda c: qc.kta(FQK[c], ypm))
    KC, KQ = RBF[kc_key], FQK[kq_key]
    sC, sQ = qc.model_complexity(KC, ypm, 0.1), qc.model_complexity(KQ, ypm, 0.1)
    return {"rbf_g_by_kta": kc_key, "fqk_c_by_kta": kq_key, "g_CQ(lam=0.1)": qc.geo_diff(KC, KQ, 0.1),
            "sqrtN": float(np.sqrt(N)), "s_C": sC, "s_Q": sQ, "s_C/s_Q": sC / sQ,
            "kta_C": qc.kta(KC, ypm), "kta_Q": qc.kta(KQ, ypm)}


def run_label(item):
    lname, y = item
    FQKL, PQK = extra()
    folds = {m: [] for m in ["LR", "RBF", "HGB", "FQK-full", "FQK-linear", "PQK"]}
    for rep in range(1):
        outer = StratifiedKFold(5, shuffle=True, random_state=2000 + rep)
        for f, (tr, te) in enumerate(outer.split(Z, y)):
            seed = 10 * rep + f
            splits = list(StratifiedKFold(3, shuffle=True, random_state=seed).split(np.zeros(len(tr)), y[tr]))
            r = fit_eval_feat(lambda C: LogisticRegression(C=C, max_iter=5000), [{"C": c} for c in [0.01, 0.1, 1, 10, 100]], Z, y, tr, te, splits)
            folds["LR"].append(((r["pred"] == y[te]).mean(), roc_auc_score(y[te], r["scores"])))
            grid = [{"learning_rate": lr, "max_leaf_nodes": 15} for lr in [0.05, 0.1]]
            r = fit_eval_feat(lambda **p: HistGradientBoostingClassifier(max_iter=300, early_stopping=False, random_state=0, **p), grid, Z, y, tr, te, splits)
            folds["HGB"].append(((r["pred"] == y[te]).mean(), roc_auc_score(y[te], r["scores"])))
            for mname, Ks in [("RBF", RBF), ("FQK-full", FQK), ("FQK-linear", FQKL), ("PQK", PQK)]:
                r = qc.fit_eval_kernel(Ks, y, tr, te, seed, Cs=(1.0, 10.0, 100.0, 1000.0))
                folds[mname].append(((r["pred"] == y[te]).mean(), roc_auc_score(y[te], r["scores"])))
    summ = {}
    for m, v in folds.items():
        a = np.array(v)
        summ[m] = {"acc": float(a[:, 0].mean()), "acc_sd_folds": float(a[:, 0].std()), "auc": float(a[:, 1].mean()),
                   "fold_accs": a[:, 0].tolist()}
    best_c = max(["LR", "RBF", "HGB"], key=lambda m: summ[m]["acc"])
    best_q = max(["FQK-full", "FQK-linear", "PQK"], key=lambda m: summ[m]["acc"])
    d = np.array(summ[best_q]["fold_accs"]) - np.array(summ[best_c]["fold_accs"])
    # Nadeau-Bengio corrected resampled t interval (k=5 folds, test/train ratio = 1/4)
    k = len(d); var = d.var(ddof=1) * (1 / k + 0.25)
    half = 2.776 * np.sqrt(var)  # t_{0.975, 4}
    res = {"models": summ, "best_classical": best_c, "best_quantum": best_q,
                      "diff_q_minus_c": float(d.mean()), "diff_CI95_NB": [float(d.mean() - half), float(d.mean() + half)],
                      "diag": audit_diag(y), "pos_rate": float(y.mean())}
    print(lname, {m: round(s["acc"], 3) for m, s in summ.items()}, "diff", round(d.mean(), 3),
          "diag", {k2: (round(v2, 3) if isinstance(v2, float) else v2) for k2, v2 in res["diag"].items()},
          f"{time.time()-t0:.0f}s", flush=True)
    return lname, res


if __name__ == "__main__":
    keep = ["REAL", "HUANG(c=0.35)", "HUANG(c=0.75)", "OBS-1(c=0.75)", "OBS-3(c=0.35)", "OBS-3(c=0.75)",
            "HUANG(c=0.75)+10%noise", "OBS-3(c=0.75)+10%noise"]
    keep = ["REAL", "HUANG(c=0.75)", "OBS-3(c=0.75)", "OBS-1(c=0.75)", "HUANG(c=0.35)", "HUANG(c=0.75)+10%noise", "OBS-3(c=0.35)", "OBS-3(c=0.75)+10%noise"]
    results = {}
    for k in keep:
        name, r = run_label((k, labels[k]))
        results[name] = r
        json.dump(results, open("results/exp3_positive_control.json", "w"), indent=1, default=float)
    print("saved")
