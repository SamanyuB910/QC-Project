"""Step 7: how fragile is 'the optimal panel'?
(1) relevance-estimator sensitivity (kNN MI with k=3/5/10, quantile-binned MI, permutation-debiased MI, |AUC-0.5|);
(2) bootstrap stability of the QUBO optimum (200 resamples): panel frequencies, per-feature selection frequency;
(3) same for the cost-aware objective at mu=0.05."""
import numpy as np
from collections import Counter
from sklearn.metrics import mutual_info_score, roc_auc_score
from sklearn.feature_selection import mutual_info_classif
from common import *
from qsim import Inst

X, y, _ = load_data()
LAM = 0.2
C = redundancy(X)


def binned_mi(X, y, bins=5):
    out = []
    for i in range(N):
        x = X[:, i]
        if DISCRETE[i] or len(np.unique(x)) <= bins:
            xb = x
        else:
            xb = np.searchsorted(np.quantile(x, np.linspace(0, 1, bins + 1)[1:-1]), x, side="right")
        out.append(mutual_info_score(xb, y))
    return np.array(out)


def perm_debiased(X, y, est, nperm=30, seed=0):
    rng = np.random.default_rng(seed)
    base = est(X, y)
    null = np.mean([est(X, rng.permutation(y)) for _ in range(nperm)], axis=0)
    return base - null, null


if __name__ == "__main__":
    ests = {
        "kNN-MI k=3 (prompt default, 20 seeds)": lambda X, y: relevance(X, y, n_neighbors=3)[0],
        "kNN-MI k=5": lambda X, y: relevance(X, y, n_neighbors=5)[0],
        "kNN-MI k=10": lambda X, y: relevance(X, y, n_neighbors=10)[0],
        "quantile-binned MI (5 bins)": lambda X, y: binned_mi(X, y, 5),
        "quantile-binned MI (10 bins)": lambda X, y: binned_mi(X, y, 10),
    }
    res = {"estimators": {}}
    print("Relevance estimator sensitivity (lambda=0.2, k=5):")
    for name, est in ests.items():
        r = est(X, y)
        I = Inst(r, C, LAM)
        print(f"  {name:38s} top-5={[FEATURES[i] for i in np.argsort(-r)[:5]]}  QUBO opt={state_to_names(int(I.opt))}  r_chol={r[4]:.3f} r_fbs={r[5]:.3f}")
        res["estimators"][name] = {"r": r, "opt": state_to_names(int(I.opt))}
    rb, nullb = perm_debiased(X, y, lambda X, y: binned_mi(X, y, 5))
    I = Inst(np.clip(rb, 0, None), C, LAM)
    print(f"  {'binned MI (5) minus permutation null':38s} top-5={[FEATURES[i] for i in np.argsort(-rb)[:5]]}  QUBO opt={state_to_names(int(I.opt))}  "
          f"null MI per feature mean={nullb.mean():.3f} (chol null {nullb[4]:.3f})")
    rk, nullk = perm_debiased(X, y, lambda X, y: mutual_info_classif(X, y, discrete_features=DISCRETE, n_neighbors=3, random_state=0), nperm=30)
    I = Inst(np.clip(rk, 0, None), C, LAM)
    print(f"  {'kNN MI k=3 minus permutation null':38s} top-5={[FEATURES[i] for i in np.argsort(-rk)[:5]]}  QUBO opt={state_to_names(int(I.opt))}  "
          f"null mean={nullk.mean():.3f}")
    res["estimators"]["perm-debiased binned"] = {"r": rb, "opt": state_to_names(int(I.opt))}
    auc = np.array([abs(roc_auc_score(y, X[:, i]) - 0.5) for i in range(N)])
    print("  univariate |AUC-0.5|:", {FEATURES[i]: round(auc[i], 3) for i in np.argsort(-auc)})
    res["univariate_auc_dev"] = dict(zip(FEATURES, auc))

    # stability under resampling. NOTE: bootstrap (with replacement) duplicates rows, which inflates kNN-MI for continuous
    # features (zero-distance neighbours); so we report both bootstrap and 80% subsampling WITHOUT replacement, and both
    # the prompt's kNN k=3 estimator and k=10.
    from s06_helpers import cost_vector
    COST = cost_vector()
    for scheme in ["bootstrap", "subsample80"]:
        for kn in [3, 10]:
            B = 200
            rng = np.random.default_rng(31)
            panels = Counter(); feat = np.zeros(N); panels_cost = Counter(); feat_cost = np.zeros(N)
            for b in range(B):
                idx = rng.integers(0, len(y), len(y)) if scheme == "bootstrap" else rng.choice(len(y), int(0.8 * len(y)), replace=False)
                r = relevance(X[idx], y[idx], seeds=range(3), n_neighbors=kn)[0]
                Cb = redundancy(X[idx])
                I = Inst(r, Cb, LAM)
                panels[int(I.opt)] += 1; feat += BITS[I.opt]
                I2 = Inst(r, Cb, LAM, extra=0.05 * COST / 100)
                panels_cost[int(I2.opt)] += 1; feat_cost += BITS[I2.opt]
            full_opt = int(Inst(relevance(X, y, n_neighbors=kn)[0], C, LAM).opt)
            print()
            print(f"[{scheme}, kNN k={kn}] QUBO optimum (lambda={LAM}) over {B} resamples: {len(panels)} distinct; "
                  f"full-data optimum {state_to_names(full_opt)} recovered in {panels[full_opt]/B:.1%}")
            for s_, c in panels.most_common(4):
                print(f"   {c/B:5.1%}  {state_to_names(s_)}  ${panel_cost(s_):.2f}")
            print("   per-feature selection frequency:", {FEATURES[i]: round(feat[i] / B, 2) for i in np.argsort(-feat)})
            print(f"   cost-aware mu=0.05: {len(panels_cost)} distinct; top:", [(state_to_names(s_), round(c / B, 3), round(panel_cost(s_), 2)) for s_, c in panels_cost.most_common(3)])
            res[f"{scheme}_k{kn}"] = {"distinct": len(panels), "full_opt_freq": panels[full_opt] / B,
                                      "top": [(state_to_names(s_), c / B) for s_, c in panels.most_common(6)],
                                      "feature_freq": dict(zip(FEATURES, feat / B)), "cost_distinct": len(panels_cost),
                                      "cost_top": [(state_to_names(s_), c / B) for s_, c in panels_cost.most_common(6)],
                                      "cost_feature_freq": dict(zip(FEATURES, feat_cost / B))}
    save_json("s07_robustness.json", res)
