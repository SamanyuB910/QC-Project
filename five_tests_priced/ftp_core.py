"""Five Tests, Priced -- core model (data, prices, objective, exact search, exact QAOA reference).

Everything here is plain NumPy so it runs the same in Qollab's in-browser Python and on a laptop.

Bit convention: a panel is a 13-bit integer s; test i is in the panel iff (s >> i) & 1.
This is Qiskit's little-endian convention, so int(bitstring, 2) of a measured key IS the panel.

Ported from the research scripts in research_notes/QCA prompts Quantum Impact plan/scripts/prompt_b/
(common.py, s06_helpers.py, qsim.py, s10_pareto_onejob.py), with file-path and import side effects removed.
"""
import math

import numpy as np

# ----------------------------------------------------------------------------------------------- constants
FEATURES = ["age", "sex", "cp", "trestbps", "chol", "fbs", "restecg",
            "thalach", "exang", "oldpeak", "slope", "ca", "thal"]
LABELS = {
    "age": "age", "sex": "sex", "cp": "chest-pain type", "trestbps": "resting blood pressure",
    "chol": "cholesterol", "fbs": "fasting blood sugar", "restecg": "resting ECG",
    "thalach": "max heart rate (thallium test)", "exang": "exercise angina (treadmill)",
    "oldpeak": "ST depression (treadmill)", "slope": "ST slope (treadmill)",
    "ca": "vessels on fluoroscopy", "thal": "thallium scan result",
}
N = len(FEATURES)          # 13 qubits, one per test
K = 5                      # the clinic can afford five tests
LAM = 0.1                  # redundancy weight lambda
MU_GRID = [0.0, 0.02, 0.05, 0.1, 0.2]   # price weights: 0 = ignore price ... 0.2 = price matters a lot

# Relevance r_i: kNN mutual information with the diagnosis (k = 10 neighbours, mean of 20 seeds, discrete-feature
# mask), computed on all 297 patients. Shipped as constants because two optima are nearly tied (margins ~1e-4),
# so re-estimating r live could flip them. Source: prompt_b/results/s07_robustness.json ["kNN-MI k=10"]["r"].
R_K10 = np.array([0.02809099244605955, 0.04011519336902181, 0.13669130599364226, 0.02024255183378254,
                  0.009050224611943514, 5.01278870687627e-06, 0.016270742304905654, 0.09439720938402159,
                  0.09169989289124486, 0.10784624302560919, 0.07539719598659554, 0.12797945853741322,
                  0.14572276699853198])

# Frozen QAOA schedule (p = 1). Tuned offline on 12 random 80% subsamples x 5 price weights; never on the answer.
# Source: prompt_b/results/s10_pareto_onejob.json
GAMMA = 1.7181724313553923
BETA = 0.16760994251739314

# Turney (1995) test costs, Ontario fee schedule Oct 1992, CAD: (full price, price when its group is already paid).
EXPENSE = {"age": (1.00, 1.00), "sex": (1.00, 1.00), "cp": (1.00, 1.00), "trestbps": (1.00, 1.00),
           "chol": (7.27, 5.17), "fbs": (5.20, 3.10), "restecg": (15.50, 15.50),
           "thalach": (102.90, 1.00), "exang": (87.30, 1.00), "oldpeak": (87.30, 1.00),
           "slope": (87.30, 1.00), "ca": (100.90, 100.90), "thal": (102.90, 1.00)}
GROUPS = {"blood draw": ["chol", "fbs"],
          "thallium stress test": ["thalach", "thal"],
          "treadmill ECG": ["exang", "oldpeak", "slope"]}

ALL = np.arange(2 ** N)
BITS = ((ALL[:, None] >> np.arange(N)) & 1).astype(np.int8)     # (8192, 13)
HW = BITS.sum(1)
FEAS_IDX = np.flatnonzero(HW == K)                                 # the 1,287 five-test panels
POS_IN_FEAS = -np.ones(2 ** N, dtype=np.int64)
POS_IN_FEAS[FEAS_IDX] = np.arange(len(FEAS_IDX))
P_HW5 = math.comb(N, K) * (K / N) ** K * (1 - K / N) ** (N - K)   # chance a raw shot has exactly five 1s = 0.22278


# ----------------------------------------------------------------------------------------------- data + prices
def load_data():
    """297 Cleveland patients (6 rows with missing values already dropped). Returns X (297x13), y (0/1)."""
    arr = np.loadtxt("data/heart_cleveland_297.csv", delimiter=",", skiprows=1)
    return arr[:, :N], arr[:, 14].astype(int)


def redundancy(X):
    """c_ij = |Pearson correlation| between tests i and j (zero diagonal)."""
    C = np.abs(np.corrcoef(X, rowvar=False))
    np.fill_diagonal(C, 0.0)
    return C


def shared_costs():
    """Cost of each shared procedure, paid once if any test in the group is chosen: 2.10, 101.90, 86.30."""
    return {g: EXPENSE[mem[0]][0] - EXPENSE[mem[0]][1] for g, mem in GROUPS.items()}


def cost_vector():
    """Exact panel price for all 2^13 subsets: sum of discounted prices + each touched group's shared cost once.
    The OR over a group becomes polynomial terms; the 3-test treadmill group gives the one cubic term."""
    B = BITS.astype(float)
    c = B @ np.array([EXPENSE[f][1] for f in FEATURES])
    fi = {f: i for i, f in enumerate(FEATURES)}
    for g, shared in shared_costs().items():
        idx = [fi[f] for f in GROUPS[g]]
        c = c + shared * (1.0 - np.prod(1.0 - B[:, idx], axis=1))
    return c


def panel_cost(state):
    """Same price computed the obvious way, from the table (used to self-test cost_vector)."""
    names = state_to_names(state)
    cost = sum(EXPENSE[f][1] for f in names)
    for g, shared in shared_costs().items():
        if any(f in names for f in GROUPS[g]):
            cost += shared
    return cost


# ----------------------------------------------------------------------------------------------- objective
def objective(r, C, cost, mu, lam=LAM):
    """f_mu(x) = -sum r_i x_i + lam * sum_{i<j} c_ij x_i x_j + mu * cost(x) / 100, for all 2^13 subsets.
    Lower is better. The QCA prompt's penalty term is not needed: the circuit only ever produces five-test panels."""
    B = BITS.astype(float)
    return -(B @ r) + lam * 0.5 * np.einsum("si,ij,sj->s", B, C, B) + mu * cost / 100.0


def procedures(state):
    """Plain-language summary of what a panel costs the clinic, e.g. 'history + treadmill ECG + fluoroscopy'."""
    names = set(state_to_names(state))
    out = []
    if names & {"exang", "oldpeak", "slope"}:
        out.append("treadmill ECG")
    if names & {"thalach", "thal"}:
        out.append("thallium scan")
    if "ca" in names:
        out.append("fluoroscopy")
    if names & {"chol", "fbs"}:
        out.append("blood test")
    if "restecg" in names:
        out.append("resting ECG")
    return " + ".join(["history"] + out) if out else "history + vitals only"


def state_to_names(state):
    return [FEATURES[i] for i in range(N) if (int(state) >> i) & 1]


def names_to_state(names):
    return sum(1 << FEATURES.index(n) for n in names)


def exact_optimum(f):
    """Best five-test panel by brute force over all 1,287 (milliseconds)."""
    ff = f[FEAS_IDX]
    return int(FEAS_IDX[int(np.argmin(ff))])


def rank_of(f, state):
    """1-based rank of a five-test panel among all 1,287 by objective."""
    ff = f[FEAS_IDX]
    return int((ff < f[int(state)] - 1e-15).sum()) + 1


def score_pareto(score, cost):
    """Panels not beaten on both score (lower better) and price: the exact cost-vs-score Pareto set (13 panels)."""
    s5, c5 = score[FEAS_IDX], cost[FEAS_IDX]
    out, best = [], np.inf
    for i in np.lexsort((s5, c5)):
        if s5[i] < best - 1e-12:
            out.append(int(FEAS_IDX[i]))
            best = s5[i]
    return out


def auc_front(auc_map, cost, size=K):
    """Cheapest-first staircase of panels whose cross-validated AUC beats every cheaper panel of the same size."""
    states = [s for s in auc_map if bin(s).count("1") == size]
    states.sort(key=lambda s: (cost[s], -auc_map[s]))
    out, best = [], -1.0
    for s in states:
        if auc_map[s] > best + 1e-12:
            out.append(s)
            best = auc_map[s]
    return out


# ----------------------------------------------------------------------------------------------- exact QAOA reference
def complete_pairs(n=N):
    """All 78 test pairs in round-robin order (13 rounds of 6 disjoint pairs). The circuit uses the same order."""
    m = n + 1 if n % 2 else n
    players = list(range(m))
    out = []
    for _ in range(m - 1):
        for i in range(m // 2):
            a, b = players[i], players[m - 1 - i]
            if a < n and b < n:
                out.append((min(a, b), max(a, b)))
        players = [players[0]] + [players[-1]] + players[1:-1]
    return out


def pair_maps(pairs):
    """For each pair (a, b): positions (within the 1,287 five-test panels) of panels with a in, b out, and partners."""
    maps = []
    for a, b in pairs:
        sel = FEAS_IDX[(BITS[FEAS_IDX, a] == 1) & (BITS[FEAS_IDX, b] == 0)]
        maps.append((POS_IN_FEAS[sel], POS_IN_FEAS[sel ^ (1 << a) ^ (1 << b)]))
    return maps


def qaoa_xy_probs(f, gamma=GAMMA, beta=BETA, maps=None):
    """Exact p=1 XY-mixer QAOA restricted to the five-test sector (1,287 amplitudes).
    cost layer exp(-i gamma E_norm), mixer exp(+i beta (XX+YY)/2) per pair == XXPlusYYGate(-2 beta).
    Starts from the uniform superposition of five-test panels (what post-selecting the RY start gives).
    Returns probabilities over FEAS_IDX order (they sum to 1)."""
    maps = pair_maps(complete_pairs()) if maps is None else maps
    ff = f[FEAS_IDX]
    e = (ff - ff.mean()) / ff.std()
    phi = np.full(len(FEAS_IDX), 1 / math.sqrt(len(FEAS_IDX)), dtype=complex) * np.exp(-1j * gamma * e)
    c, s = math.cos(beta), 1j * math.sin(beta)
    for i10, i01 in maps:
        a, b = phi[i10].copy(), phi[i01].copy()
        phi[i10] = c * a + s * b
        phi[i01] = s * a + c * b
    p = np.abs(phi) ** 2
    return p / p.sum()


def independent_choice(p_feas):
    """The 'independent-choice' sampler: same per-test probabilities as the QAOA output, tests drawn independently,
    then conditioned on exactly five tests. Isolates what correlations between qubits add."""
    full = np.zeros(2 ** N)
    full[FEAS_IDX] = p_feas
    m = np.clip(full @ BITS, 1e-12, 1 - 1e-12)
    prod = np.exp(BITS @ np.log(m) + (1 - BITS) @ np.log(1 - m))[FEAS_IDX]
    return prod / prod.sum()


def closed_form_all_found(dists, targets, shots):
    """Exact probability that ONE job (len(dists) circuits x `shots` raw shots each) samples every target panel
    at least once. dists: list of probability vectors over FEAS_IDX (one per circuit); targets: distinct panels.
    Inclusion-exclusion over missed subsets; each raw shot is a five-test sample with probability P_HW5."""
    from itertools import combinations
    pos = [int(POS_IN_FEAS[t]) for t in targets]
    total = 0.0
    for k in range(len(pos) + 1):
        for T in combinations(pos, k):
            term = 1.0
            for p in dists:
                term *= (1.0 - P_HW5 * float(sum(p[i] for i in T))) ** shots
            total += (-1) ** k * term
    return max(0.0, min(1.0, total))


def llr_stats(counts_feas, p_ideal, p_null):
    """Log-likelihood ratio of observed five-test samples under the ideal circuit vs the independent-choice
    sampler, plus the expected mean +- sd of that statistic if the samples came from either model."""
    w = np.log(np.clip(p_ideal, 1e-300, None)) - np.log(np.clip(p_null, 1e-300, None))
    n = int(counts_feas.sum())
    obs = float(counts_feas @ w)
    def moments(p):
        m1 = float(p @ w)
        return n * m1, math.sqrt(max(n * (float(p @ w ** 2) - m1 ** 2), 0.0))
    return obs, moments(p_ideal), moments(p_null), n


def wilson(k, n, z=1.96):
    if n == 0:
        return (float("nan"), float("nan"))
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - h), min(1.0, c + h))
