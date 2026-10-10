"""Step 5: downstream value of the panels.
(A) Fixed panels (chosen on the full data) -> repeated nested CV (outer 5x5 stratified, inner 5-fold grid search)
    for logistic regression, RBF-SVM, gradient boosting. 95% CIs by patient bootstrap of repeat-averaged OOF scores.
(B) Honest pipelines: the selection step is re-run INSIDE each outer training fold (QUBO exact at lambda, greedy mRMR,
    SelectKBest-MI, L1-logistic, all 13), logistic regression downstream.
(C) All 1287 five-feature panels: repeated-CV AUC of logistic regression vs QUBO objective (Spearman), rank of the
    QUBO optimum, and all subsets of size 1..5 for the cost/AUC Pareto analysis (saved for s06).
"""
import sys, time
import numpy as np
from itertools import combinations
from joblib import Parallel, delayed
from scipy.stats import spearmanr
from sklearn.model_selection import RepeatedStratifiedKFold, StratifiedKFold, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import roc_auc_score
from common import *

X, y, df = load_data()
CAT = {"cp", "restecg", "slope", "thal"}
PART = (sys.argv[1] if len(sys.argv) > 1 else "ABC") if __name__ == "__main__" else ""


def prep(cols):
    names = [FEATURES[i] for i in cols]
    cat = [j for j, f in enumerate(names) if f in CAT]
    num = [j for j, f in enumerate(names) if f not in CAT]
    tr = []
    if num:
        tr.append(("num", StandardScaler(), num))
    if cat:
        tr.append(("cat", OneHotEncoder(handle_unknown="ignore"), cat))
    return ColumnTransformer(tr)


MODELS = {
    "LR": (lambda: LogisticRegression(max_iter=2000), {"m__C": [0.01, 0.1, 1, 10]}),
    "SVM": (lambda: SVC(kernel="rbf"), {"m__C": [0.1, 1, 10], "m__gamma": ["scale", 0.01, 0.1]}),
    "GB": (lambda: GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, random_state=0), {"m__max_depth": [1, 2]}),
}


def score_of(est, Xt):
    return est.predict_proba(Xt)[:, 1] if hasattr(est, "predict_proba") else est.decision_function(Xt)


def thr(model):
    return 0.0 if model == "SVM" else 0.5


def metrics(yt, s, t):
    pred = (s > t).astype(int)
    return roc_auc_score(yt, s), (pred == yt).mean(), pred[yt == 1].mean(), 1 - pred[yt == 0].mean()


def boot_ci(yt, s, t, B=2000, seed=0):
    rng = np.random.default_rng(seed); vals = []
    n = len(yt)
    for _ in range(B):
        i = rng.integers(0, n, n)
        if yt[i].min() == yt[i].max():
            continue
        vals.append(metrics(yt[i], s[i], t))
    v = np.array(vals)
    return np.percentile(v, 2.5, axis=0), np.percentile(v, 97.5, axis=0)


OUTER = RepeatedStratifiedKFold(n_splits=5, n_repeats=5, random_state=2026)
SPLITS = list(OUTER.split(X, y))


def nested_fixed(cols, model):
    mk, grid = MODELS[model]
    oof = np.zeros((5, len(y)))
    for f, (tr, te) in enumerate(SPLITS):
        rep = f // 5
        pipe = Pipeline([("p", prep(cols)), ("m", mk())])
        gs = GridSearchCV(pipe, grid, cv=StratifiedKFold(5, shuffle=True, random_state=f), scoring="roc_auc")
        gs.fit(X[tr][:, cols], y[tr])
        oof[rep, te] = score_of(gs.best_estimator_, X[te][:, cols])
    per_rep = np.array([metrics(y, oof[k_], thr(model)) for k_ in range(5)])
    avg = oof.mean(0)
    lo, hi = boot_ci(y, avg, thr(model))
    point = np.array(metrics(y, avg, thr(model)))
    return point, lo, hi, per_rep.mean(0)


def greedy_sel(r, C, lam):
    sel = []
    for _ in range(K):
        sel.append(min((-r[i] + lam * sum(C[i, j] for j in sel), i) for i in range(N) if i not in sel)[1])
    return sorted(sel)


def qubo_sel(r, C, lam):
    rel, red = objective_terms(r, C)
    f = -rel[FEAS_IDX] + lam * red[FEAS_IDX]
    s = FEAS_IDX[np.argmin(f)]
    return [i for i in range(N) if (s >> i) & 1]


def l1_sel(Xt, yt):
    Xs = StandardScaler().fit_transform(Xt)
    for Cc in np.logspace(-3, 1, 200):
        m = LogisticRegression(penalty="l1", solver="liblinear", C=Cc, max_iter=5000).fit(Xs, yt)
        if (np.abs(m.coef_[0]) > 1e-8).sum() >= K:
            return sorted(np.argsort(-np.abs(m.coef_[0]))[:K])


res = {}
r_full, _ = relevance(X, y); C_full = redundancy(X)
PANELS = {
    "QUBO_opt_lam0.1": qubo_sel(r_full, C_full, 0.1),
    "QUBO_opt_lam0.2": qubo_sel(r_full, C_full, 0.2),
    "QUBO_opt_lam0.5": qubo_sel(r_full, C_full, 0.5),
    "QUBO_opt_lam0 (=SelectKBest MI)": qubo_sel(r_full, C_full, 0.0),
    "greedy_mRMR_lam0.5": greedy_sel(r_full, C_full, 0.5),
    "L1_logistic_5": l1_sel(X, y),
    "routine_cheap (age,sex,trestbps,chol,fbs)": [FEATURES.index(f) for f in ["age", "sex", "trestbps", "chol", "fbs"]],
    "no_imaging_best? (age,sex,cp,thalach,exang)": [FEATURES.index(f) for f in ["age", "sex", "cp", "thalach", "exang"]],
    "all_13": list(range(N)),
}
if "A" in PART:
    print("(A) fixed panels, nested CV (outer 5x5, inner 5-fold grid)")
    resA = {}
    jobs = [(name, cols, model) for name, cols in PANELS.items() for model in ["LR", "SVM", "GB"]]
    outs = Parallel(n_jobs=6)(delayed(nested_fixed)(cols, model) for name, cols, model in jobs)
    for (name, cols, model), (mean, lo, hi, per_rep) in zip(jobs, outs):
        if True:
            t = time.time()
            resA[f"{name}|{model}"] = {"panel": [FEATURES[i] for i in cols], "cost": panel_cost([FEATURES[i] for i in cols]),
                                       "AUC": mean[0], "AUC_ci": (lo[0], hi[0]), "acc": mean[1], "acc_ci": (lo[1], hi[1]),
                                       "sens": mean[2], "sens_ci": (lo[2], hi[2]), "spec": mean[3], "per_repeat_mean_AUC_acc_sens_spec": per_rep}
            print(f"  {name:42s} {model:3s} cost=${panel_cost([FEATURES[i] for i in cols]):6.2f} AUC={mean[0]:.3f} [{lo[0]:.3f},{hi[0]:.3f}] "
                  f"acc={mean[1]:.3f} [{lo[1]:.3f},{hi[1]:.3f}] sens={mean[2]:.3f} [{lo[2]:.3f},{hi[2]:.3f}] spec={mean[3]:.3f} | per-repeat mean AUC={per_rep[0]:.3f} acc={per_rep[1]:.3f}  ({time.time()-t:.0f}s)", flush=True)
    res["A"] = resA

if "B" in PART:
    print("\n(B) honest pipelines: selection inside each outer training fold; LR downstream (inner C grid)")
    sel_fns = {
        "QUBO_exact_lam0.1": lambda Xt, yt: qubo_sel(relevance(Xt, yt, seeds=range(5))[0], redundancy(Xt), 0.1),
        "QUBO_exact_lam0.2": lambda Xt, yt: qubo_sel(relevance(Xt, yt, seeds=range(5))[0], redundancy(Xt), 0.2),
        "QUBO_exact_lam0.5": lambda Xt, yt: qubo_sel(relevance(Xt, yt, seeds=range(5))[0], redundancy(Xt), 0.5),
        "greedy_mRMR_lam0.5": lambda Xt, yt: greedy_sel(relevance(Xt, yt, seeds=range(5))[0], redundancy(Xt), 0.5),
        "SelectKBest_MI": lambda Xt, yt: sorted(np.argsort(-relevance(Xt, yt, seeds=range(5))[0])[:K]),
        "L1_logistic_5": l1_sel,
        "all_13": lambda Xt, yt: list(range(N)),
    }
    resB = {}
    for name, fn in sel_fns.items():
        oof = np.zeros((5, len(y))); chosen = []
        for f, (tr, te) in enumerate(SPLITS):
            cols = fn(X[tr], y[tr]); chosen.append(tuple(cols))
            pipe = Pipeline([("p", prep(cols)), ("m", LogisticRegression(max_iter=2000))])
            gs = GridSearchCV(pipe, {"m__C": [0.01, 0.1, 1, 10]}, cv=StratifiedKFold(5, shuffle=True, random_state=f), scoring="roc_auc")
            gs.fit(X[tr][:, cols], y[tr])
            oof[f // 5, te] = score_of(gs.best_estimator_, X[te][:, cols])
        per_rep = np.array([metrics(y, oof[k_], 0.5) for k_ in range(5)]).mean(0)
        per = np.array(metrics(y, oof.mean(0), 0.5))
        lo, hi = boot_ci(y, oof.mean(0), 0.5)
        from collections import Counter
        cc = Counter(chosen).most_common(3)
        resB[name] = {"AUC": per[0], "AUC_ci": (lo[0], hi[0]), "acc": per[1], "acc_ci": (lo[1], hi[1]), "sens": per[2],
                      "sens_ci": (lo[2], hi[2]), "per_repeat_mean": per_rep, "n_distinct_panels_over_25_folds": len(set(chosen)),
                      "top_panels": [([FEATURES[i] for i in c], n) for c, n in cc]}
        print(f"  {name:20s} AUC={per[0]:.3f} [{lo[0]:.3f},{hi[0]:.3f}] acc={per[1]:.3f} [{lo[1]:.3f},{hi[1]:.3f}] sens={per[2]:.3f} (per-repeat mean AUC {per_rep[0]:.3f}) "
              f"| distinct panels across 25 folds={len(set(chosen))}; most common {[([FEATURES[i] for i in c], n) for c, n in cc[:2]]}", flush=True)
    res["B"] = resB

if "C" in PART:
    print("\n(C) all subsets of size 1..5: repeated-CV AUC of logistic regression (C=1), fixed 5x3 folds")
    folds = list(RepeatedStratifiedKFold(n_splits=5, n_repeats=3, random_state=7).split(X, y))

    def cv_auc(cols):
        aucs = []
        for tr, te in folds:
            pipe = Pipeline([("p", prep(list(cols))), ("m", LogisticRegression(max_iter=2000))]).fit(X[tr][:, list(cols)], y[tr])
            aucs.append(roc_auc_score(y[te], pipe.predict_proba(X[te][:, list(cols)])[:, 1]))
        return float(np.mean(aucs))
    subsets = [c for m in range(1, K + 1) for c in combinations(range(N), m)]
    t = time.time()
    aucs = Parallel(n_jobs=4)(delayed(cv_auc)(c) for c in subsets)
    print(f"  {len(subsets)} subsets in {time.time()-t:.0f}s")
    states = np.array([subset_to_state(c) for c in subsets]); aucs = np.array(aucs)
    costs = np.array([panel_cost(int(s)) for s in states])
    np.savez(os.path.join(OUT, "s05_all_subsets.npz"), states=states, aucs=aucs, costs=costs)
    m5 = np.array([len(c) == K for c in subsets])
    st5, au5 = states[m5], aucs[m5]
    rel, red = objective_terms(r_full, C_full)
    resC = {"best5": (state_to_names(int(st5[np.argmax(au5)])), au5.max()), "median5": float(np.median(au5))}
    print(f"  best 5-panel by CV AUC: {state_to_names(int(st5[np.argmax(au5)]))} AUC={au5.max():.3f}; median 5-panel AUC={np.median(au5):.3f}")
    for lam in [0.0, 0.05, 0.1, 0.2, 0.3, 0.5, 1.0]:
        f = -rel[st5] + lam * red[st5]
        rho = spearmanr(f, -au5).correlation
        iopt = np.argmin(f)
        rank_auc = int((au5 > au5[iopt]).sum()) + 1
        # top-10 QUBO panels: mean AUC
        top10 = np.argsort(f)[:10]
        resC[f"lam{lam}"] = {"spearman_f_vs_negAUC": rho, "qubo_opt": state_to_names(int(st5[iopt])), "qubo_opt_auc": au5[iopt],
                             "qubo_opt_auc_rank": rank_auc, "top10_qubo_mean_auc": float(au5[top10].mean())}
        print(f"  lam={lam:4.2f}: Spearman(QUBO f, -AUC)={rho:+.3f}; QUBO optimum {state_to_names(int(st5[iopt]))} AUC={au5[iopt]:.3f} "
              f"(rank {rank_auc}/1287); mean AUC of QUBO top-10={au5[top10].mean():.3f}")
    rho_rel = spearmanr(rel[st5], au5).correlation
    print(f"  Spearman(relevance sum, AUC) = {rho_rel:+.3f}")
    resC["spearman_relsum_auc"] = rho_rel
    res["C"] = resC
save_json(f"s05_downstream_{PART}.json", res)
