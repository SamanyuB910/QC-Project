"""Experiment 1: rigorous nested-CV replication on WDBC (569 x 30), positive class = malignant.

Outer: 5 repeats x stratified 5-fold (seeds 1000..1004).  Inner: stratified 3-fold on the outer-train rows.
Scaler + PCA are fit on the outer-train rows only.  Every model's hyperparameters are chosen in the inner loop.
A deployable decision threshold targeting 98% sensitivity is calibrated on inner out-of-fold scores (never on the test fold).

Models at n = 4, 8, 12 PCA components (= qubits):
  LR-PCA, RBF-PCA (tuned C, gamma)
  QSVC-plain   : MinMax[0,1] PCA features, zz_feature_map(full, reps=2), C=1 (the tutorial-level default, untuned)
  FQK-full     : zz_feature_map full entanglement, bandwidth c * z, tuned (c, C)
  FQK-linear   : linear entanglement (chain), tuned (c, C)
  SEP          : no entanglers (separable product-state kernel), tuned (c, C)  [Bowles et al. ablation]
  PQK          : projected (1-RDM) kernel on the full-entanglement states, tuned (c, gamma, C)
  QKA-scale    : per-feature bandwidths learned by SPSA on centred kernel-target alignment, init at CV bandwidth
  QKA-RY       : tutorial-08 style trainable RY layer (n params), SVCLoss(C=1), SPSA, init 0, at CV bandwidth
  ARD-RBF      : classical control for QKA: per-feature RBF length-scales learned by the same SPSA/KTA
At n = 30 (all features, standardised): LR-30, RBF-30, HGB-30.
"""
import os
os.environ.setdefault("OMP_NUM_THREADS", "1"); os.environ.setdefault("OPENBLAS_NUM_THREADS", "1"); os.environ.setdefault("MKL_NUM_THREADS", "1")
import sys, time, pickle
import numpy as np
from multiprocessing import Pool
from sklearn.model_selection import StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.svm import SVC
import qk_core as qc

BW = [0.02, 0.05, 0.1, 0.2, 0.35, 0.5, 0.75, 1.0]
PQK_G = [0.1, 0.3, 1.0, 3.0]
RBF_G = [0.003, 0.01, 0.03, 0.1, 0.3, 1.0, 3.0]
TARGET_SENS = 0.98
SPSA_ITERS = 50
QKA_SUB = 250


def fit_eval_feat(make, grid, F, y, tr, te, splits):
    best, best_sc = None, (-1, -1)
    from sklearn.metrics import roc_auc_score
    for p in grid:
        accs, aucs = [], []
        for a, b in splits:
            m = make(**p).fit(F[tr][a], y[tr][a])
            d = m.decision_function(F[tr][b])
            accs.append(((d > 0).astype(int) == y[tr][b]).mean()); aucs.append(roc_auc_score(y[tr][b], d))
        sc = (round(np.mean(accs), 6), np.mean(aucs))
        if sc > best_sc:
            best_sc, best = sc, p
    m = make(**best).fit(F[tr], y[tr])
    s = m.decision_function(F[te])
    oof = np.empty(len(tr))
    for a, b in splits:
        oof[b] = make(**best).fit(F[tr][a], y[tr][a]).decision_function(F[tr][b])
    t = qc.calib_threshold(y[tr], oof, TARGET_SENS)
    return {"key": str(best), "C": None, "inner_acc": best_sc[0], "n_sv": None,
            "scores": s, "pred": (s > 0).astype(int), "pred_cal": (s >= t).astype(int), "thr": t}


def svc_loss(K, y):
    m = SVC(kernel="precomputed", C=1.0).fit(K, y)
    dc = m.dual_coef_[0]; sv = m.support_
    return float(np.abs(dc).sum() - 0.5 * dc @ K[np.ix_(sv, sv)] @ dc)


def run_task(args):
    n, rep = args
    t0 = time.time()
    X, y = qc.load_wdbc()
    ypm = 2 * y - 1
    outer = StratifiedKFold(5, shuffle=True, random_state=1000 + rep)
    res = {}
    def put(name, fold_te, r):
        d = res.setdefault(name, {"scores": np.full(len(y), np.nan), "pred": np.full(len(y), -1), "pred_cal": np.full(len(y), -1), "folds": []})
        d["scores"][fold_te] = r["scores"]; d["pred"][fold_te] = r["pred"]; d["pred_cal"][fold_te] = r["pred_cal"]
        d["folds"].append({k: r[k] for k in ("key", "C", "inner_acc", "n_sv", "thr")} | {k: r[k] for k in r if k.startswith("x_")})
    for f, (tr, te) in enumerate(outer.split(X, y)):
        seed = 10 * rep + f
        inner = __import__("sklearn.model_selection", fromlist=["StratifiedKFold"]).StratifiedKFold(3, shuffle=True, random_state=seed)
        splits = list(inner.split(np.zeros(len(tr)), y[tr]))
        Z = qc.fold_features(X, tr, n, seed=0)
        if n == 30:
            put("LR-30", te, fit_eval_feat(lambda C: LogisticRegression(C=C, max_iter=5000), [{"C": c} for c in [0.01, 0.1, 1, 10, 100]], Z, y, tr, te, splits))
            put("RBF-30", te, qc.fit_eval_kernel({g: qc.rbf_kernel_z(Z, g) for g in RBF_G}, y, tr, te, seed, TARGET_SENS))
            grid = [{"learning_rate": lr, "max_leaf_nodes": ml, "l2_regularization": l2} for lr in [0.05, 0.1] for ml in [7, 15] for l2 in [0.0, 1.0]]
            put("HGB-30", te, fit_eval_feat(lambda **p: HistGradientBoostingClassifier(max_iter=300, early_stopping=False, random_state=0, **p), grid, Z, y, tr, te, splits))
            continue
        # ---- classical on PCA-n
        put("LR-PCA", te, fit_eval_feat(lambda C: LogisticRegression(C=C, max_iter=5000), [{"C": c} for c in [0.01, 0.1, 1, 10, 100]], Z, y, tr, te, splits))
        rbfK = {g: qc.rbf_kernel_z(Z, g) for g in RBF_G}
        r_rbf = qc.fit_eval_kernel(rbfK, y, tr, te, seed, TARGET_SENS)
        put("RBF-PCA", te, r_rbf)
        # ---- plain tutorial-level QSVC: MinMax[0,1] on train, full ZZ, reps 2, C=1, no tuning
        mn, mx = Z[tr].min(0), Z[tr].max(0)
        Zmm = (Z - mn) / (mx - mn)
        Kp = qc.fid_kernel(qc.zz_states(Zmm, 2, "full"))
        m = SVC(kernel="precomputed", C=1.0).fit(Kp[np.ix_(tr, tr)], y[tr])
        s = m.decision_function(Kp[np.ix_(te, tr)])
        oof = qc.oof_scores_kernel(Kp, y, tr, 1.0, splits)
        t = qc.calib_threshold(y[tr], oof, TARGET_SENS)
        put("QSVC-plain", te, {"key": "minmax01", "C": 1.0, "inner_acc": None, "n_sv": int(m.n_support_.sum()), "scores": s,
                               "pred": (s > 0).astype(int), "pred_cal": (s >= t).astype(int), "thr": t,
                               "x_offdiag_mean": float(qc.offdiag(Kp[np.ix_(tr, tr)]).mean())})
        # ---- quantum kernels with bandwidth
        Sfull = {c: qc.zz_states(Z * c, 2, "full") for c in BW}
        fidF = {c: qc.fid_kernel(S) for c, S in Sfull.items()}
        r = qc.fit_eval_kernel(fidF, y, tr, te, seed, TARGET_SENS); put("FQK-full", te, r)
        c_star = r["key"]
        fidL = {c: qc.fid_kernel(qc.zz_states(Z * c, 2, "linear")) for c in BW}
        put("FQK-linear", te, qc.fit_eval_kernel(fidL, y, tr, te, seed, TARGET_SENS))
        del fidL
        sep = {c: qc.fid_kernel(qc.zz_states(Z * c, 2, "none")) for c in BW}
        put("SEP", te, qc.fit_eval_kernel(sep, y, tr, te, seed, TARGET_SENS))
        del sep
        pq = {}
        for c, S in Sfull.items():
            R = qc.bloch(S, n)
            for g in PQK_G:
                pq[(c, g)] = qc.pqk_from_bloch(R, g, ref_idx=tr)
        put("PQK", te, qc.fit_eval_kernel(pq, y, tr, te, seed, TARGET_SENS))
        del pq, Sfull
        # ---- kernel training (SPSA) on a stratified subsample of outer-train
        rng = np.random.default_rng(seed)
        sub = tr if len(tr) <= QKA_SUB else np.sort(rng.choice(tr, QKA_SUB, replace=False))
        Zs, ys = Z[sub], ypm[sub]
        # QKA-scale: per-feature bandwidth (log-param), KTA objective
        f_scale = lambda th: qc.kta(qc.fid_kernel(qc.zz_states(Zs * (c_star * np.exp(th)), 2, "full")), ys)
        th, fbest, hist = qc.spsa_maximize(f_scale, np.zeros(n), iters=SPSA_ITERS, seed=seed)
        Kq = qc.fid_kernel(qc.zz_states(Z * (c_star * np.exp(th)), 2, "full"))
        r = qc.fit_eval_kernel({"qka": Kq}, y, tr, te, seed, TARGET_SENS)
        r["x_kta_init"] = hist[0]; r["x_kta_final"] = fbest; r["x_scales"] = (c_star * np.exp(th)).tolist()
        put("QKA-scale", te, r)
        # QKA-RY: tutorial-08 style trainable RY layer, SVCLoss(C=1) (minimise), init 0
        f_ry = lambda th: -svc_loss(qc.fid_kernel(qc.zz_states(Zs * c_star, 2, "full", pre_ry=th)), y[sub])
        th, fbest, hist = qc.spsa_maximize(f_ry, np.zeros(n), iters=SPSA_ITERS, seed=seed)
        Kq = qc.fid_kernel(qc.zz_states(Z * c_star, 2, "full", pre_ry=th))
        r = qc.fit_eval_kernel({"qkary": Kq}, y, tr, te, seed, TARGET_SENS)
        r["x_loss_init"] = -hist[0]; r["x_loss_final"] = -fbest
        put("QKA-RY", te, r)
        # ARD-RBF classical control: same SPSA/KTA on per-feature RBF length-scales, init at CV RBF gamma
        g_star = r_rbf["key"]
        f_ard = lambda th: qc.kta(qc.ard_rbf(Zs, (g_star / n) * np.exp(th)), ys)
        th, fbest, hist = qc.spsa_maximize(f_ard, np.zeros(n), iters=SPSA_ITERS, seed=seed)
        Ka = qc.ard_rbf(Z, (g_star / n) * np.exp(th))
        r = qc.fit_eval_kernel({"ard": Ka}, y, tr, te, seed, TARGET_SENS)
        r["x_kta_init"] = hist[0]; r["x_kta_final"] = fbest
        put("ARD-RBF", te, r)
        print(f"n={n} rep={rep} fold={f} done {time.time()-t0:.0f}s", flush=True)
    return (n, rep, res, time.time() - t0)


if __name__ == "__main__":
    tasks = [(n, r) for n in [12, 8, 4] for r in range(5)] + [(30, r) for r in range(5)]
    with Pool(min(len(tasks), 18)) as pool:
        out = pool.map(run_task, tasks, chunksize=1)
    allres = {}
    for n, rep, res, dt in out:
        for name, d in res.items():
            allres[(name, n, rep)] = d
        print(f"task n={n} rep={rep}: {dt:.0f}s")
    pickle.dump(allres, open("results/exp1_raw.pkl", "wb"))
    print("saved results/exp1_raw.pkl")
