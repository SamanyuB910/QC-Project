"""Step 1: data facts, r_i, c_ij, exact enumeration, lambda/P sweeps, classical baselines."""
import time, itertools
import numpy as np
from sklearn.feature_selection import SelectKBest, mutual_info_classif, f_classif, chi2
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from common import *

X, y, df = load_data()
print("rows", len(y), "positives", y.sum(), "negatives", (1 - y).sum())
raw = pd.read_csv(os.path.join(RAW, "processed.cleveland.data"), header=None, names=FEATURES + ["num"], na_values="?")
print("raw rows", len(raw), "rows with missing", raw.isna().any(axis=1).sum(), "missing by col", raw.isna().sum()[raw.isna().sum() > 0].to_dict())
print("num distribution", raw["num"].value_counts().sort_index().to_dict())

# ship a small CSV for Qollab
ship = df.copy(); ship["target"] = y
ship.to_csv(os.path.join(HERE, "heart_cleveland_297.csv"), index=False)
print("shipped csv bytes", os.path.getsize(os.path.join(HERE, "heart_cleveland_297.csv")))

r, r_sd = relevance(X, y)
C = redundancy(X)
order = np.argsort(-r)
print("\nRelevance r_i (MI nats, mean+-sd over 20 seeds):")
for i in order:
    print(f"  {FEATURES[i]:9s} {r[i]:.4f} +- {r_sd[i]:.4f}   cost ${EXPENSE[FEATURES[i]][0]:.2f}")
iu = np.triu_indices(N, 1)
print("c_ij stats: mean %.3f max %.3f (pair %s)" % (C[iu].mean(), C[iu].max(),
      [FEATURES[a] for a in np.unravel_index(np.argmax(C), C.shape)]))
top_pairs = sorted([(C[a, b], FEATURES[a], FEATURES[b]) for a, b in zip(*iu)], reverse=True)[:8]
print("top redundant pairs", [(round(v, 3), a, b) for v, a, b in top_pairs])
# seed sensitivity: does top-5 by r change across seeds?
R = np.array([mutual_info_classif(X, y, discrete_features=DISCRETE, n_neighbors=3, random_state=s) for s in range(20)])
tops = {tuple(sorted(np.argsort(-row)[:5])) for row in R}
print("distinct top-5-by-MI sets across 20 seeds:", [[FEATURES[i] for i in t] for t in tops])

rel, red = objective_terms(r, C)
res = {"n_rows": len(y), "n_pos": int(y.sum()), "r": r, "r_sd": r_sd, "C": C, "features": FEATURES}


def best_feasible(lam):
    f = -rel[FEAS_IDX] + lam * red[FEAS_IDX]
    o = np.argsort(f)
    return FEAS_IDX[o], f[o]


# ---- lambda sweep (feasible optimum, exact over 1287) ----
print("\nLambda sweep: exact optimum over C(13,5)=1287")
lam_grid = [0, 0.02, 0.05, 0.1, 0.15, 0.2, 0.3, 0.5, 0.75, 1.0, 1.5, 2.0, 5.0]
sweep = []
for lam in lam_grid:
    st, f = best_feasible(lam)
    gap = f[1] - f[0]
    spread = f[-1] - f[0]
    sweep.append({"lam": lam, "opt": state_to_names(int(st[0])), "f_opt": f[0], "gap_to_2nd": gap, "spread": spread,
                  "opt_rel": rel[st[0]], "opt_red": red[st[0]], "cost": panel_cost(int(st[0]))})
    print(f"  lam={lam:5.2f} opt={state_to_names(int(st[0]))} f*={f[0]:.4f} gap2={gap:.4f} spread={spread:.3f} rel={rel[st[0]]:.3f} red={red[st[0]]:.3f} cost=${panel_cost(int(st[0])):.2f}")
res["lambda_sweep"] = sweep

# ---- P sweep for a few lambdas: critical penalty over all 2^13 states ----
print("\nPenalty sweep: P* = smallest P that makes the global min over 2^13 feasible")
pcrit = {}
for lam in [0.1, 0.2, 0.3, 0.5, 1.0]:
    f0 = -rel + lam * red
    fk = f0[FEAS].min()
    best_w = {w: f0[HW == w].min() for w in range(N + 1)}
    Pstar = max((fk - best_w[w]) / (w - K) ** 2 for w in range(N + 1) if w != K)
    pcrit[lam] = Pstar
    # fraction of feasible states in the lowest-energy 1% and P(feasible) under Boltzmann-free uniform
    rows = []
    for P in [0.01, 0.05, 0.1, 0.2, 0.5, 1, 2, 5, 10, 100, 1e5]:
        E = f0 + P * (HW - K) ** 2
        gmin = np.argmin(E)
        # normalized position of the feasible optimum in the full spectrum
        Emin, Emax = E.min(), E.max()
        feas_opt = fk
        rows.append({"P": P, "global_min_feasible": bool(FEAS[gmin]), "global_min_hw": int(HW[gmin]),
                     "E_range": Emax - Emin, "objective_spread_over_E_range": (f0[FEAS].max() - fk) / (Emax - Emin)})
    print(f"  lam={lam}: P*={Pstar:.4f}  feasible-opt-only-if P>P*;  rows:")
    for rw in rows:
        print(f"     P={rw['P']:<8} globalmin feasible={rw['global_min_feasible']!s:5s} hw={rw['global_min_hw']:2d}  E_range={rw['E_range']:.3g}  (feasible objective spread / E_range)={rw['objective_spread_over_E_range']:.2e}")
    res.setdefault("penalty_sweep", {})[str(lam)] = {"Pstar": Pstar, "rows": rows}

# ---- classical baselines at a reference lambda ----
LAMS = [0.1, 0.2, 0.5, 1.0]
base = {}
rng = np.random.default_rng(0)


def f_of(state, lam):
    return -rel[state] + lam * red[state]


def greedy_mrmr(lam):
    sel = []
    for _ in range(K):
        best, bi = None, None
        for i in range(N):
            if i in sel:
                continue
            gain = -r[i] + lam * sum(C[i, j] for j in sel)
            if best is None or gain < best:
                best, bi = gain, i
        sel.append(bi)
    return subset_to_state(sel)


def sa_kswap(lam, n_eval, rng, T0=None, T1=None):
    """Simulated annealing over k-subsets with swap moves; returns best state, evaluations used."""
    cur = list(rng.choice(N, K, replace=False))
    s = subset_to_state(cur); fc = f_of(s, lam); best = (fc, s)
    T0 = T0 or 0.1; T1 = T1 or 1e-4
    for t in range(n_eval - 1):
        T = T0 * (T1 / T0) ** (t / max(1, n_eval - 2))
        out_i = rng.integers(K); cand_in = rng.choice([i for i in range(N) if i not in cur])
        new = cur.copy(); new[out_i] = cand_in
        s2 = subset_to_state(new); f2 = f_of(s2, lam)
        if f2 <= fc or rng.random() < np.exp(-(f2 - fc) / T):
            cur, fc = new, f2
            if fc < best[0]:
                best = (fc, s2)
    return best[1]


Xs = StandardScaler().fit_transform(X)
# L1 logistic path: smallest C giving >=5 nonzero, take top-5 by |coef|
l1_state = None
for Cc in np.logspace(-3, 1, 400):
    m = LogisticRegression(penalty="l1", solver="liblinear", C=Cc, max_iter=5000).fit(Xs, y)
    nz = np.flatnonzero(np.abs(m.coef_[0]) > 1e-8)
    if len(nz) >= 5:
        l1_state = subset_to_state(np.argsort(-np.abs(m.coef_[0]))[:5]); l1_C = Cc; l1_nz = len(nz)
        break
skb_mi = subset_to_state(np.argsort(-r)[:5])
skb_f = subset_to_state(np.argsort(-f_classif(X, y)[0])[:5])
skb_chi2 = subset_to_state(np.argsort(-chi2(X - X.min(0), y)[0])[:5])
print("\nL1-logistic first 5-feature model at C=%.4f (nonzero=%d): %s" % (l1_C, l1_nz, state_to_names(l1_state)))
print("SelectKBest MI:", state_to_names(skb_mi), " F-test:", state_to_names(skb_f), " chi2:", state_to_names(skb_chi2))

for lam in LAMS:
    st, f = best_feasible(lam)
    fopt = f[0]; fworst = f[-1]
    rank = {int(s): i for i, s in enumerate(st)}
    def ar(s):
        return f_of(s, lam) / fopt if fopt < 0 else np.nan
    def nar(s):
        return (fworst - f_of(s, lam)) / (fworst - fopt)
    g = greedy_mrmr(lam)
    entries = {"exact": int(st[0]), "greedy_mrmr": g, "selectkbest_MI": skb_mi, "selectkbest_F": skb_f,
               "selectkbest_chi2": skb_chi2, "l1_logistic": l1_state}
    print(f"\n lam={lam}: f*={fopt:.4f} (worst feasible {fworst:.4f})")
    out = {}
    for k_, s in entries.items():
        out[k_] = {"panel": state_to_names(s), "f": f_of(s, lam), "AR": ar(s), "normAR": nar(s), "rank": rank[s] + 1, "cost": panel_cost(s)}
        print(f"   {k_:17s} rank={rank[s]+1:4d}/1287 AR={ar(s):.4f} normAR={nar(s):.4f} cost=${panel_cost(s):7.2f} {state_to_names(s)}")
    # SA at matched evaluation budgets: P(SA best == optimum), 200 restarts
    for budget in [10, 25, 50, 100, 200, 1000]:
        hits = 0; ars = []
        for rep in range(300):
            sb = sa_kswap(lam, budget, rng)
            hits += sb == st[0]; ars.append(nar(sb))
        lo, hi = wilson(hits, 300)
        out[f"SA_{budget}"] = {"P_hit_opt": hits / 300, "ci": (lo, hi), "mean_normAR": float(np.mean(ars))}
        print(f"   SA budget={budget:5d} evals: P(found opt)={hits/300:.3f} [{lo:.3f},{hi:.3f}]  mean normAR={np.mean(ars):.4f}")
    # uniform random k-subset with N draws: P(opt in N draws) = 1-(1-1/1287)^N
    for nd in [10, 100, 1000]:
        out[f"uniform_{nd}"] = 1 - (1 - 1 / 1287) ** nd
    out["uniform_mean_normAR"] = float(np.mean([(fworst - v) / (fworst - fopt) for v in f]))
    print(f"   uniform k-subset: P(opt)/draw = {1/1287:.5f}; mean normAR={out['uniform_mean_normAR']:.4f}")
    # number of near-optimal states
    out["n_within_1pct"] = int((f <= fopt + 0.01 * abs(fopt)).sum()); out["n_within_5pct"] = int((f <= fopt + 0.05 * abs(fopt)).sum())
    print(f"   states within 1% of f*: {out['n_within_1pct']}, within 5%: {out['n_within_5pct']}")
    base[str(lam)] = out
res["baselines"] = base
res["l1_C"] = l1_C
t = time.time(); _ = [best_feasible(0.5) for _ in range(100)]
print("\nexact enumeration time (1287 feasible, vectorized): %.2f ms" % ((time.time() - t) * 10))
save_json("s01_data_qubo.json", res)
