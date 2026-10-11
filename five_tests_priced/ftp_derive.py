"""Five Tests, Priced -- where every number in the model comes from.

The model uses a few fixed numbers (in ftp_core.py). None of them is typed in by hand or taken on trust: this file
computes each one from the project's own data, so any Run (or tools/precompute.py) can check it.

  test prices       read from Turney's original cost files, shipped in data/      -> ftp_core.EXPENSE, GROUPS
  relevance r_i     how much each test tells us about the diagnosis: mutual information with the label,
                    scikit-learn's k-nearest-neighbour estimator (k = 10), mean of 20 random seeds -> ftp_core.R_K10
  circuit angles    tuned on 12 random 80% subsets of the patients x 5 price weights, to maximise the average
                    chance of sampling each subset's own best panel; the full-data answer is never used
                                                                                    -> ftp_core.GAMMA, BETA
  AUC table         cross-validated accuracy of every panel of 1-5 tests (ftp_classical.cv_auc)
                                                                                    -> results/precomputed.json

scikit-learn and SciPy are imported only inside the functions that need them.
"""
import numpy as np

import ftp_core as core

# Tests whose values are categories or yes/no, not measurements on a scale. The mutual-information estimator
# treats these as discrete.
DISCRETE_TESTS = {"sex", "cp", "fbs", "restecg", "exang", "slope", "ca", "thal"}

# Turney's files label the shared procedures A, B, C; these are the procedures they stand for.
TURNEY_GROUP_NAMES = {"A": "blood draw", "B": "thallium stress test", "C": "treadmill ECG"}


# =================================================================================================================
# Prices
# =================================================================================================================
def read_turney_prices():
    """Parse Turney's (1995) original cost files.

    data/heart-disease.expense: one line per test, "<test>: <full price>, <price once its group is paid>"
    data/heart-disease.group:   one line per test in a shared procedure, "<test>: <group letter>."
    Returns (expense {test: (full, discounted)}, groups {procedure name: [tests]}).
    """
    expense = {}
    with open("data/heart-disease.expense") as fh:
        for line in fh:
            if ":" in line:
                test, prices = line.split(":", 1)
                full, discounted = (float(p) for p in prices.split(","))
                expense[test.strip()] = (full, discounted)
    groups = {}
    with open("data/heart-disease.group") as fh:
        for line in fh:
            if ":" in line:
                test, letter = line.split(":", 1)
                name = TURNEY_GROUP_NAMES[letter.strip().rstrip(".")]
                groups.setdefault(name, []).append(test.strip())
    return expense, groups


def prices_match_turney():
    """True if ftp_core's price table and shared procedures are exactly Turney's files."""
    expense, groups = read_turney_prices()
    same_groups = {name: sorted(tests) for name, tests in groups.items()} == \
        {name: sorted(tests) for name, tests in core.GROUPS.items()}
    return expense == core.EXPENSE and same_groups


# =================================================================================================================
# Relevance of each test
# =================================================================================================================
def relevance(X, y, seeds=range(20), k=10):
    """Mutual information (in nats) between each test and the diagnosis, averaged over random seeds.

    scikit-learn's estimator counts nearest neighbours (k of them) for measured tests and uses exact counting for
    categorical ones. The seed only changes a tiny random jitter it adds to break ties, so averaging over seeds
    gives a stable value.
    """
    from sklearn.feature_selection import mutual_info_classif
    discrete = np.array([f in DISCRETE_TESTS for f in core.FEATURES])
    return np.mean([mutual_info_classif(X, y, discrete_features=discrete, n_neighbors=k, random_state=s)
                    for s in seeds], axis=0)


# =================================================================================================================
# Circuit angles
# =================================================================================================================
def tune_angles(X, y):
    """Re-run the tuning that produced ftp_core.GAMMA and ftp_core.BETA. Takes about a minute on a laptop.

    1. Draw 12 random subsets of 80% of the patients (seed 4242).
    2. On each subset, recompute relevance (5 seeds) and redundancy, and build the objective for all 5 price weights:
       60 training problems, each with its own exact best panel.
    3. Find the (gamma, beta) that maximise the average chance that the circuit samples each problem's own best
       panel (Nelder-Mead from 16 starting points). The full-data answer is never used.
    Returns (gamma, beta, the average chance at those angles).
    """
    from scipy.optimize import minimize
    rng = np.random.default_rng(4242)
    subsets = [rng.choice(len(y), int(0.8 * len(y)), replace=False) for _ in range(12)]
    price = core.cost_vector()
    mixer_pairs = core.pair_maps(core.complete_pairs())
    training = []                                   # (objective, position of its best panel)
    for rows in subsets:
        r = relevance(X[rows], y[rows], seeds=range(5))
        C = core.redundancy(X[rows])
        for mu in core.MU_GRID:
            f = core.objective(r, C, price, mu)
            training.append((f, core.POS_IN_FEAS[core.exact_optimum(f)]))

    def minus_average_chance(angles):
        return -np.mean([core.qaoa_xy_probs(f, angles[0], angles[1], mixer_pairs)[best] for f, best in training])

    best_fit = None
    for gamma_start in (0.3, 0.6, 1.0, 1.5):
        for beta_start in (0.05, 0.1, 0.2, 0.4):
            fit = minimize(minus_average_chance, [gamma_start, beta_start], method="Nelder-Mead",
                           options={"maxiter": 200})
            if best_fit is None or fit.fun < best_fit.fun:
                best_fit = fit
    return float(best_fit.x[0]), float(best_fit.x[1]), float(-best_fit.fun)


# =================================================================================================================
# Accuracy of every panel
# =================================================================================================================
def auc_table(X, y, sizes=(1, 2, 3, 4, 5)):
    """Cross-validated AUC of every panel with 1-5 tests (2,379 panels; several minutes). Returns {panel: AUC}."""
    from sklearn.model_selection import RepeatedStratifiedKFold

    import ftp_classical as classical
    folds = list(RepeatedStratifiedKFold(n_splits=5, n_repeats=3, random_state=7).split(X, y))
    panels = [int(s) for s in core.ALL if bin(int(s)).count("1") in sizes]
    return {s: classical.cv_auc(X, y, s, folds) for s in panels}
