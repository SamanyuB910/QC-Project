"""Five Tests, Priced -- classical comparison methods and the accuracy (AUC) of a panel.

Every method works on the same objective f (a vector giving the score of every panel; lower is better) and
counts how many panels it "evaluates" (looks up a score for), so it can be compared with the quantum job at an
equal number of evaluated panels.

  greedy         add the single best test, five times
  local_search   keep swapping one test for another while that improves the score
  sa_pool        simulated annealing: random swaps, sometimes accepting worse panels early on
  rrls_pool      local search restarted from random panels until the evaluation budget runs out
  cv_auc         how well a panel predicts heart disease (cross-validated logistic regression)

Ported from prompt_b/s10d_localsearch_matched.py and s10f_pooled_matched.py; the random number generator is
passed in explicitly so results are reproducible.
"""
import math

from ftp_core import K, N


def _state(tests):
    """List of test indices -> panel number (bit i set for each test i)."""
    panel = 0
    for i in tests:
        panel |= 1 << int(i)
    return panel


def greedy(f):
    """Start with no tests; five times, add the test that gives the best score so far.

    Returns (panel, number of panels evaluated). It needs only 55 evaluations, but can miss the true optimum
    because it never revisits an earlier choice.
    """
    chosen, evaluations = [], 0
    for _ in range(K):
        best = None                                   # (score, test) of the best addition this round
        for test in range(N):
            if test in chosen:
                continue
            score = f[_state(chosen + [test])]
            evaluations += 1
            if best is None or score < best[0]:
                best = (score, test)
        chosen.append(best[1])
    return _state(chosen), evaluations


def local_search(f, start_state, budget=10 ** 6):
    """Improve a five-test panel by "1-swaps": replace one chosen test with one unchosen test.

    Each round tries every possible swap and makes the best one; it stops when no swap improves the score.
    Returns (panel, number of panels evaluated).
    """
    current = [i for i in range(N) if (start_state >> i) & 1]
    current_score, evaluations = f[_state(current)], 1
    while evaluations < budget:
        best = None                                   # (score, panel as a list) of the best swap this round
        for slot in range(K):
            for test in range(N):
                if test in current:
                    continue
                candidate = current.copy()
                candidate[slot] = test
                score = f[_state(candidate)]
                evaluations += 1
                if best is None or score < best[0]:
                    best = (score, candidate)
                if evaluations >= budget:
                    break
            if evaluations >= budget:
                break
        if best is None or best[0] >= current_score:  # no swap helps: a local optimum
            break
        current, current_score = best[1], best[0]
    return _state(current), evaluations


def sa_pool(f, n_eval, rng, T0=0.1, T1=1e-4):
    """Simulated annealing over five-test panels, with exactly n_eval evaluations. Returns every panel evaluated.

    Each step proposes a random 1-swap. Better panels are always accepted; worse ones are accepted with
    probability exp(-(increase in score) / T). The "temperature" T falls geometrically from T0 to T1, so the
    search wanders early on and settles down later.
    """
    current = [int(v) for v in rng.choice(N, K, replace=False)]
    panel = _state(current)
    current_score, evaluated = f[panel], {panel}
    for step in range(n_eval - 1):
        temperature = T0 * (T1 / T0) ** (step / max(1, n_eval - 2))
        slot = int(rng.integers(K))
        new_test = int(rng.choice([q for q in range(N) if q not in current]))
        candidate = current.copy()
        candidate[slot] = new_test
        candidate_panel = _state(candidate)
        evaluated.add(candidate_panel)
        if f[candidate_panel] <= current_score or \
                rng.random() < math.exp(-(f[candidate_panel] - current_score) / temperature):
            current, current_score = candidate, f[candidate_panel]
    return evaluated


# Tests whose values are categories (e.g. chest-pain type 1-4), not measurements on a scale.
CATEGORICAL = {"cp", "restecg", "slope", "thal"}


def cv_auc(X, y, state, folds=None):
    """How well one panel predicts heart disease: the cross-validated AUC of logistic regression.

    Numeric tests are standardised and categorical ones one-hot encoded. 5-fold cross-validation is repeated 3
    times (random_state = 7) on all patients, the same protocol as the precomputed table
    (prompt_b/s05_downstream.py part C). AUC = 0.5 is guessing, 1.0 is perfect.
    scikit-learn is imported only here, so a default Run does not load it.
    """
    from sklearn.compose import ColumnTransformer
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import roc_auc_score
    from sklearn.model_selection import RepeatedStratifiedKFold
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import OneHotEncoder, StandardScaler

    from ftp_core import FEATURES
    columns = [i for i in range(N) if (state >> i) & 1]
    names = [FEATURES[i] for i in columns]
    categorical = [j for j, name in enumerate(names) if name in CATEGORICAL]
    numeric = [j for j, name in enumerate(names) if name not in CATEGORICAL]
    preprocessing = ([("num", StandardScaler(), numeric)] if numeric else []) + \
                    ([("cat", OneHotEncoder(handle_unknown="ignore"), categorical)] if categorical else [])
    if folds is None:
        folds = list(RepeatedStratifiedKFold(n_splits=5, n_repeats=3, random_state=7).split(X, y))
    aucs = []
    for train, test in folds:
        model = Pipeline([("p", ColumnTransformer(preprocessing)), ("m", LogisticRegression(max_iter=2000))])
        model.fit(X[train][:, columns], y[train])
        aucs.append(roc_auc_score(y[test], model.predict_proba(X[test][:, columns])[:, 1]))
    return sum(aucs) / len(aucs)


def rrls_pool(f, budget, rng):
    """Random-restart local search with exactly `budget` evaluations. Returns every panel evaluated.

    Start from a random five-test panel, improve it by best 1-swaps until stuck, then start again from a new
    random panel, until the budget is used up.
    """
    evaluated, used = set(), 0
    while used < budget:
        current = [int(v) for v in rng.choice(N, K, replace=False)]
        current_score = f[_state(current)]
        evaluated.add(_state(current))
        used += 1
        improved = True
        while improved and used < budget:
            improved, best = False, None
            for slot in range(K):
                for test in range(N):
                    if test in current or used >= budget:
                        continue
                    candidate = current.copy()
                    candidate[slot] = test
                    panel = _state(candidate)
                    evaluated.add(panel)
                    used += 1
                    if best is None or f[panel] < best[0]:
                        best = (f[panel], candidate)
            if best is not None and best[0] < current_score:
                current, current_score, improved = best[1], best[0], True
    return evaluated
