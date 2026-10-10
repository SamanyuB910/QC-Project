"""Step 9: honest (selection-inside-fold) cost-aware pipelines.
For each outer training fold: estimate r (kNN-MI, k=3 prompt default vs k=10) and C, solve the cost-aware QUBO/HUBO
exactly (1287 panels) at (lam, mu), fit logistic regression (inner C grid), score the outer test fold.
Reports AUC (+ bootstrap CI on repeat-averaged OOF scores) and mean panel cost per patient (Turney CAD 1992)."""
import numpy as np
from collections import Counter
from sklearn.model_selection import RepeatedStratifiedKFold, StratifiedKFold, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from joblib import Parallel, delayed
from common import *
from qsim import Inst
from s06_helpers import cost_vector
from s05_downstream import prep, boot_ci, metrics  # noqa (import-only; s05 main code is guarded by PART)

X, y, _ = load_data()
COST = cost_vector()
SPLITS = list(RepeatedStratifiedKFold(n_splits=5, n_repeats=5, random_state=2026).split(X, y))


def run(kn, lam, mu):
    oof = np.zeros((5, len(y))); costs = []; panels = []
    for f, (tr, te) in enumerate(SPLITS):
        r = relevance(X[tr], y[tr], seeds=range(5), n_neighbors=kn)[0]
        I = Inst(r, redundancy(X[tr]), lam, extra=mu * COST / 100)
        cols = [i for i in range(N) if (int(I.opt) >> i) & 1]
        costs.append(COST[I.opt]); panels.append(tuple(cols))
        pipe = Pipeline([("p", prep(cols)), ("m", LogisticRegression(max_iter=2000))])
        gs = GridSearchCV(pipe, {"m__C": [0.01, 0.1, 1, 10]}, cv=StratifiedKFold(5, shuffle=True, random_state=f), scoring="roc_auc")
        gs.fit(X[tr][:, cols], y[tr])
        oof[f // 5, te] = gs.best_estimator_.predict_proba(X[te][:, cols])[:, 1]
    avg = oof.mean(0)
    point = metrics(y, avg, 0.5); lo, hi = boot_ci(y, avg, 0.5)
    per_rep = np.mean([roc_auc_score(y, oof[k_]) for k_ in range(5)])
    top = Counter(panels).most_common(2)
    return {"kn": kn, "lam": lam, "mu": mu, "AUC": point[0], "AUC_ci": (lo[0], hi[0]), "sens": point[2], "sens_ci": (lo[2], hi[2]),
            "per_repeat_AUC": per_rep, "mean_cost": float(np.mean(costs)), "distinct_panels": len(set(panels)),
            "top_panels": [([FEATURES[i] for i in c], n) for c, n in top]}


if __name__ == "__main__":
    grid = [(3, 0.2, 0.0), (3, 0.2, 0.05), (3, 0.2, 0.1), (10, 0.1, 0.0), (10, 0.1, 0.02), (10, 0.1, 0.1), (10, 0.1, 0.2), (10, 0.2, 0.0)]
    outs = Parallel(n_jobs=8)(delayed(run)(*g) for g in grid)
    for o in outs:
        print(f"kNN k={o['kn']:2d} lam={o['lam']} mu={o['mu']:4.2f}: AUC={o['AUC']:.3f} [{o['AUC_ci'][0]:.3f},{o['AUC_ci'][1]:.3f}] "
              f"(per-repeat {o['per_repeat_AUC']:.3f}) sens={o['sens']:.3f} mean cost=${o['mean_cost']:.2f} distinct panels={o['distinct_panels']} top={o['top_panels']}")
    save_json("s09_honest_cost_pipelines.json", outs)
