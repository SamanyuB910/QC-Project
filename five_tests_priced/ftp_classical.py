"""Five Tests, Priced -- classical baselines (ported from prompt_b/s10d_localsearch_matched.py and
s10f_pooled_matched.py; the random generator is now passed in explicitly so results are reproducible)."""
import math

from ftp_core import K, N


def _state(sel):
    s = 0
    for i in sel:
        s |= 1 << int(i)
    return s


def greedy(f):
    """Greedy mRMR-style selection: add the test that most improves the objective, five times (55 evaluations)."""
    sel, evals = [], 0
    for _ in range(K):
        best = None
        for i in range(N):
            if i in sel:
                continue
            s = _state(sel + [i])
            evals += 1
            if best is None or f[s] < best[0]:
                best = (f[s], i)
        sel.append(best[1])
    return _state(sel), evals


def local_search(f, start_state, budget=10 ** 6):
    """Best-improvement 1-swap local search from a five-test panel (swap one test in for one test out)."""
    cur = [i for i in range(N) if (start_state >> i) & 1]
    fc, evals = f[_state(cur)], 1
    while evals < budget:
        best = None
        for a in range(K):
            for j in range(N):
                if j in cur:
                    continue
                new = cur.copy()
                new[a] = j
                s = _state(new)
                evals += 1
                if best is None or f[s] < best[0]:
                    best = (f[s], new)
                if evals >= budget:
                    break
            if evals >= budget:
                break
        if best is None or best[0] >= fc:
            break
        cur, fc = best[1], best[0]
    return _state(cur), evals


def sa_pool(f, n_eval, rng, T0=0.1, T1=1e-4):
    """Simulated annealing over five-test panels (1-swap moves, geometric cooling). Returns every panel evaluated."""
    cur = [int(v) for v in rng.choice(N, K, replace=False)]
    s = _state(cur)
    fc, pool = f[s], {s}
    for t in range(n_eval - 1):
        T = T0 * (T1 / T0) ** (t / max(1, n_eval - 2))
        i = int(rng.integers(K))
        j = int(rng.choice([q for q in range(N) if q not in cur]))
        new = cur.copy()
        new[i] = j
        s2 = _state(new)
        pool.add(s2)
        if f[s2] <= fc or rng.random() < math.exp(-(f[s2] - fc) / T):
            cur, fc = new, f[s2]
    return pool


CATEGORICAL = {"cp", "restecg", "slope", "thal"}


def cv_auc(X, y, state, folds=None):
    """Cross-validated AUC of logistic regression on one panel: standardise numeric tests, one-hot the categorical
    ones, 5x3 repeated stratified folds (random_state=7) on all patients. Same protocol as the precomputed table
    (prompt_b/s05_downstream.py part C). Imports scikit-learn only when called."""
    from sklearn.compose import ColumnTransformer
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import roc_auc_score
    from sklearn.model_selection import RepeatedStratifiedKFold
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import OneHotEncoder, StandardScaler

    from ftp_core import FEATURES
    cols = [i for i in range(N) if (state >> i) & 1]
    names = [FEATURES[i] for i in cols]
    cat = [j for j, f in enumerate(names) if f in CATEGORICAL]
    num = [j for j, f in enumerate(names) if f not in CATEGORICAL]
    tr = ([("num", StandardScaler(), num)] if num else []) + \
         ([("cat", OneHotEncoder(handle_unknown="ignore"), cat)] if cat else [])
    if folds is None:
        folds = list(RepeatedStratifiedKFold(n_splits=5, n_repeats=3, random_state=7).split(X, y))
    aucs = []
    for tr_i, te_i in folds:
        pipe = Pipeline([("p", ColumnTransformer(tr)), ("m", LogisticRegression(max_iter=2000))])
        pipe.fit(X[tr_i][:, cols], y[tr_i])
        aucs.append(roc_auc_score(y[te_i], pipe.predict_proba(X[te_i][:, cols])[:, 1]))
    return sum(aucs) / len(aucs)


def rrls_pool(f, budget, rng):
    """Random-restart 1-swap local search with a fixed evaluation budget. Returns every panel evaluated."""
    pool, used = set(), 0
    while used < budget:
        cur = [int(v) for v in rng.choice(N, K, replace=False)]
        fc = f[_state(cur)]
        pool.add(_state(cur))
        used += 1
        improved = True
        while improved and used < budget:
            improved, best = False, None
            for a in range(K):
                for j in range(N):
                    if j in cur or used >= budget:
                        continue
                    new = cur.copy()
                    new[a] = j
                    s = _state(new)
                    pool.add(s)
                    used += 1
                    if best is None or f[s] < best[0]:
                        best = (f[s], new)
            if best is not None and best[0] < fc:
                cur, fc, improved = best[1], best[0], True
    return pool
