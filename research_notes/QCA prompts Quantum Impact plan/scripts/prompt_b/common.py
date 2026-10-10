"""Shared helpers for the Prompt B (heart-disease feature selection) experiments.

Bit convention: state integer s, feature i is kept iff (s >> i) & 1 == 1.
This matches Qiskit's little-endian convention (qubit i = bit i of int(bitstring, 2)).
"""
import os, json, itertools, warnings
warnings.filterwarnings("ignore")
import numpy as np
import pandas as pd
from sklearn.feature_selection import mutual_info_classif

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "data_raw")
OUT = os.path.join(HERE, "results")
os.makedirs(OUT, exist_ok=True)

FEATURES = ["age", "sex", "cp", "trestbps", "chol", "fbs", "restecg",
            "thalach", "exang", "oldpeak", "slope", "ca", "thal"]
N = len(FEATURES)
K = 5
# discrete (categorical / small-integer) features for the MI estimator
DISCRETE = np.array([f in {"sex", "cp", "fbs", "restecg", "exang", "slope", "ca", "thal"} for f in FEATURES])

# Turney (1995) test costs, Canadian dollars, Ontario Ministry of Health fee schedule (Oct 1992).
# costs/heart-disease.expense: (full cost, discount cost); group file: A={chol,fbs}, B={thalach,thal}, C={exang,oldpeak,slope}
EXPENSE = {"age": (1.00, 1.00), "sex": (1.00, 1.00), "cp": (1.00, 1.00), "trestbps": (1.00, 1.00),
           "chol": (7.27, 5.17), "fbs": (5.20, 3.10), "restecg": (15.50, 15.50),
           "thalach": (102.90, 1.00), "exang": (87.30, 1.00), "oldpeak": (87.30, 1.00),
           "slope": (87.30, 1.00), "ca": (100.90, 100.90), "thal": (102.90, 1.00)}
GROUPS = {"A": ["chol", "fbs"], "B": ["thalach", "thal"], "C": ["exang", "oldpeak", "slope"]}


def load_data(path=None):
    """Cleveland processed file -> 297 complete rows, binary target (0 vs 1-4)."""
    path = path or os.path.join(RAW, "processed.cleveland.data")
    df = pd.read_csv(path, header=None, names=FEATURES + ["num"], na_values="?")
    df = df.dropna().reset_index(drop=True)
    X = df[FEATURES].to_numpy(float)
    y = (df["num"].to_numpy() > 0).astype(int)
    return X, y, df


def relevance(X, y, seeds=range(20), n_neighbors=3):
    """r_i = mutual information (nats) with the label; sklearn kNN (Kraskov/Ross) estimator for
    continuous features, contingency MI for discrete ones; averaged over seeds (seed only affects the
    tiny jitter sklearn adds to continuous features)."""
    R = np.array([mutual_info_classif(X, y, discrete_features=DISCRETE, n_neighbors=n_neighbors,
                                      random_state=s) for s in seeds])
    return R.mean(0), R.std(0)


def redundancy(X):
    C = np.abs(np.corrcoef(X, rowvar=False))
    np.fill_diagonal(C, 0.0)
    return C


ALL = np.arange(2 ** N)
BITS = ((ALL[:, None] >> np.arange(N)) & 1).astype(np.int8)  # (8192, 13)
HW = BITS.sum(1)
FEAS = HW == K
FEAS_IDX = np.where(FEAS)[0]  # 1287 states


def objective_terms(r, C):
    """Return per-state relevance sum and redundancy sum (i<j) for all 2^13 states."""
    Xb = BITS.astype(float)
    rel = Xb @ r
    red = 0.5 * np.einsum("si,ij,sj->s", Xb, C, Xb)
    return rel, red


def qubo_energy(r, C, lam, P, k=K):
    rel, red = objective_terms(r, C)
    return -rel + lam * red + P * (HW - k) ** 2


def subset_to_state(idx):
    s = 0
    for i in idx:
        s |= 1 << int(i)
    return s


def state_to_names(s):
    return [FEATURES[i] for i in range(N) if (s >> i) & 1]


def panel_cost(state_or_names):
    """Exact Turney cost with group discounts: sum of discount costs + shared cost once per touched group."""
    names = state_to_names(state_or_names) if isinstance(state_or_names, (int, np.integer)) else list(state_or_names)
    cost = sum(EXPENSE[f][1] for f in names)
    for g, mem in GROUPS.items():
        if any(f in names for f in mem):
            cost += EXPENSE[mem[0]][0] - EXPENSE[mem[0]][1]
    return cost


def all_costs():
    return np.array([panel_cost(int(s)) for s in ALL])


def wilson(k, n, z=1.96):
    if n == 0:
        return (np.nan, np.nan)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - h), min(1.0, c + h))


def save_json(name, obj):
    def conv(o):
        if isinstance(o, (np.bool_,)):
            return bool(o)
        if isinstance(o, (np.integer,)):
            return int(o)
        if isinstance(o, (np.floating,)):
            return float(o)
        if isinstance(o, np.ndarray):
            return o.tolist()
        raise TypeError(type(o))
    with open(os.path.join(OUT, name), "w") as f:
        json.dump(obj, f, indent=1, default=conv)
