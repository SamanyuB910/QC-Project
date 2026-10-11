"""Five Tests, Priced -- the core model: data, prices, the objective, exact search, and an exact model of the circuit.

Everything here is plain NumPy, so it runs the same in Qollab's in-browser Python and on a laptop.

HOW A PANEL IS STORED
  A "panel" is a choice of tests. It is stored as one 13-bit integer: bit i is 1 when test i (FEATURES[i]) is in
  the panel. Example: 47 = 0b0000000101111 has bits 0, 1, 2, 3 and 5 set, so it is the panel
  {age, sex, cp, trestbps, fbs}. Qiskit numbers qubits the same way (qubit i = bit i), so the integer value of a
  measured bitstring IS the panel. There are 2^13 = 8,192 possible panels; 1,287 of them have exactly five tests.

WHAT IS IN THIS FILE
  1. Constants          the 13 tests, the price weights, the shipped relevance values and circuit angles, prices
  2. Panel tables       every possible panel as a row of 0/1 bits, and which ones have exactly five tests
  3. Data and prices    load the patients, measure redundancy, compute the price of every panel
  4. The objective      the score the clinic wants to minimise, and exact search over all panels
  5. Exact circuit model  what the QAOA circuit should output, computed with NumPy instead of Qiskit
  6. Statistics         the closed-form prediction, the likelihood-ratio test and confidence intervals

Ported from the research scripts in research_notes/QCA prompts Quantum Impact plan/scripts/prompt_b/
(common.py, s06_helpers.py, qsim.py, s10_pareto_onejob.py), with file-path and import side effects removed.
"""
import math

import numpy as np

# =================================================================================================================
# 1. Constants
# =================================================================================================================

# The 13 measurements in the UCI Cleveland data, in column order. Test i is qubit i.
FEATURES = ["age", "sex", "cp", "trestbps", "chol", "fbs", "restecg",
            "thalach", "exang", "oldpeak", "slope", "ca", "thal"]

# Plain-English names for the column codes above.
LABELS = {
    "age": "age", "sex": "sex", "cp": "chest-pain type", "trestbps": "resting blood pressure",
    "chol": "cholesterol", "fbs": "fasting blood sugar", "restecg": "resting ECG",
    "thalach": "max heart rate (thallium test)", "exang": "exercise angina (treadmill)",
    "oldpeak": "ST depression (treadmill)", "slope": "ST slope (treadmill)",
    "ca": "vessels on fluoroscopy", "thal": "thallium scan result",
}

N = len(FEATURES)          # 13 tests = 13 qubits
K = 5                      # the clinic can afford five tests
LAM = 0.1                  # lambda: how much redundancy between chosen tests is penalised
MU_GRID = [0.0, 0.02, 0.05, 0.1, 0.2]   # price weights mu: 0 = ignore price ... 0.2 = price matters a lot

# Relevance r_i of each test: how much it tells us about the diagnosis (mutual information, estimated with
# k = 10 nearest neighbours, averaged over 20 random seeds, on all 297 patients).
# Computed by ftp_derive.relevance(X, y); every Run recomputes it and prints the difference (0 on our machines).
# Written out as fixed numbers so a different scikit-learn version cannot silently change the answer: two optimal
# panels are nearly tied (margins about 1e-4).
R_K10 = np.array([0.02809099244605955, 0.04011519336902181, 0.13669130599364226, 0.02024255183378254,
                  0.009050224611943514, 5.01278870687627e-06, 0.016270742304905654, 0.09439720938402159,
                  0.09169989289124486, 0.10784624302560919, 0.07539719598659554, 0.12797945853741322,
                  0.14572276699853198])

# The two angles of the one-layer (p = 1) QAOA circuit: gamma for the cost layer, beta for the mixer.
# Tuned on 12 random 80% subsets of the patients x 5 price weights, never on the answer, then frozen.
# Computed by ftp_derive.tune_angles(X, y) (about a minute; Run setting retune_angles = true repeats it).
GAMMA = 1.7181724313553923
BETA = 0.16760994251739314

# Test prices from Turney (1995): Ontario fee schedule, Oct 1992, Canadian dollars.
# Each test has two prices: (full price, price when its shared procedure is already paid for).
# These are exactly Turney's files data/heart-disease.expense and data/heart-disease.group; every Run checks this
# (ftp_derive.prices_match_turney).
EXPENSE = {"age": (1.00, 1.00), "sex": (1.00, 1.00), "cp": (1.00, 1.00), "trestbps": (1.00, 1.00),
           "chol": (7.27, 5.17), "fbs": (5.20, 3.10), "restecg": (15.50, 15.50),
           "thalach": (102.90, 1.00), "exang": (87.30, 1.00), "oldpeak": (87.30, 1.00),
           "slope": (87.30, 1.00), "ca": (100.90, 100.90), "thal": (102.90, 1.00)}

# Tests that come from one shared procedure: the procedure is paid once, whichever of its tests are chosen.
GROUPS = {"blood draw": ["chol", "fbs"],
          "thallium stress test": ["thalach", "thal"],
          "treadmill ECG": ["exang", "oldpeak", "slope"]}

# The procedure each test comes from, for the printed tables.
PROCEDURE_OF = {"age": "history", "sex": "history", "cp": "history", "trestbps": "vital signs",
                "chol": "blood draw", "fbs": "blood draw", "restecg": "resting ECG",
                "thalach": "thallium stress test", "thal": "thallium stress test",
                "exang": "treadmill ECG", "oldpeak": "treadmill ECG", "slope": "treadmill ECG",
                "ca": "fluoroscopy"}

# =================================================================================================================
# 2. Panel tables (computed once, used everywhere)
# =================================================================================================================

ALL = np.arange(2 ** N)                                            # every panel number 0 .. 8191
BITS = ((ALL[:, None] >> np.arange(N)) & 1).astype(np.int8)        # BITS[panel, i] = 1 if test i is in it; 8192 x 13
HW = BITS.sum(1)                                                   # number of tests in each panel ("Hamming weight")
FEAS_IDX = np.flatnonzero(HW == K)                                 # the 1,287 panels with exactly five tests

# POS_IN_FEAS[panel] = position of a five-test panel in FEAS_IDX (-1 for panels without exactly five tests).
# Probability vectors over "the 1,287 valid panels" use this order.
POS_IN_FEAS = -np.ones(2 ** N, dtype=np.int64)
POS_IN_FEAS[FEAS_IDX] = np.arange(len(FEAS_IDX))

# The circuit starts with every test "in" with probability 5/13, independently. The chance that a measured shot
# has exactly five tests is then the binomial probability C(13,5) (5/13)^5 (8/13)^8 = 0.22278.
P_HW5 = math.comb(N, K) * (K / N) ** K * (1 - K / N) ** (N - K)


# =================================================================================================================
# 3. Data and prices
# =================================================================================================================
def load_data():
    """The 297 Cleveland patients (the 6 rows with missing values are already removed).

    Returns X (297 x 13: one row per patient, one column per test) and y (1 = heart disease, 0 = none).
    The path must be a plain string literal: Qollab only ships data files it can see in the code.
    """
    table = np.loadtxt("data/heart_cleveland_297.csv", delimiter=",", skiprows=1)
    # Columns 0-12 are the tests, column 13 is the original 0-4 severity score, column 14 the 0/1 diagnosis.
    return table[:, :N], table[:, 14].astype(int)


def redundancy(X):
    """c_ij = |correlation| between tests i and j across patients (0 on the diagonal).

    Two highly correlated tests mostly repeat each other, so choosing both is penalised.
    """
    C = np.abs(np.corrcoef(X, rowvar=False))
    np.fill_diagonal(C, 0.0)
    return C


def shared_costs():
    """Price of each shared procedure, paid once if any of its tests is chosen: {name: 2.10 / 101.90 / 86.30}.

    It is the difference between a test's full price and its price once the procedure is paid for.
    """
    return {group: EXPENSE[tests[0]][0] - EXPENSE[tests[0]][1] for group, tests in GROUPS.items()}


def cost_vector():
    """Exact price of every one of the 8,192 panels, as a vector indexed by panel number.

    price = (sum of the discounted prices of the chosen tests)
          + (each shared procedure's price, once, if at least one of its tests is chosen)

    "At least one of a, b, c is chosen" is written as 1 - (1 - x_a)(1 - x_b)(1 - x_c). Multiplied out, this is a
    polynomial in the test choices x, which is what lets the circuit represent price. The 3-test treadmill group
    gives the one cubic term x_exang * x_oldpeak * x_slope.
    """
    bits = BITS.astype(float)
    price = bits @ np.array([EXPENSE[f][1] for f in FEATURES])
    column_of = {f: i for i, f in enumerate(FEATURES)}
    for group, shared_price in shared_costs().items():
        columns = [column_of[f] for f in GROUPS[group]]
        any_test_of_group_chosen = 1.0 - np.prod(1.0 - bits[:, columns], axis=1)
        price = price + shared_price * any_test_of_group_chosen
    return price


def panel_cost(state):
    """Price of one panel computed the obvious way, test by test. Used to self-test cost_vector()."""
    names = state_to_names(state)
    cost = sum(EXPENSE[f][1] for f in names)
    for group, shared_price in shared_costs().items():
        if any(f in names for f in GROUPS[group]):
            cost += shared_price
    return cost


# =================================================================================================================
# 4. The objective and exact search
# =================================================================================================================
def objective(r, C, cost, mu, lam=LAM):
    """Score of every one of the 8,192 panels for one price weight mu. LOWER IS BETTER.

        f_mu(x) = - sum_i r_i x_i                  reward informative tests (relevance)
                  + lam * sum_{i<j} c_ij x_i x_j   penalise pairs of tests that repeat each other (redundancy)
                  + mu * price(x) / 100            penalise price, more strongly for larger mu

    x_i = 1 if test i is in the panel. QCA's prompt also adds a penalty term to force exactly five tests; we do not
    need it, because the circuit's mixer only ever produces five-test panels.
    (The 0.5 below is because the double sum over all i, j counts every pair twice.)
    """
    bits = BITS.astype(float)
    return -(bits @ r) + lam * 0.5 * np.einsum("si,ij,sj->s", bits, C, bits) + mu * cost / 100.0


def procedures(state):
    """Plain-language summary of what a panel costs the clinic, e.g. 'history + treadmill ECG + fluoroscopy'."""
    names = set(state_to_names(state))
    steps = []
    if names & {"exang", "oldpeak", "slope"}:
        steps.append("treadmill ECG")
    if names & {"thalach", "thal"}:
        steps.append("thallium scan")
    if "ca" in names:
        steps.append("fluoroscopy")
    if names & {"chol", "fbs"}:
        steps.append("blood test")
    if "restecg" in names:
        steps.append("resting ECG")
    return " + ".join(["history"] + steps) if steps else "history + vitals only"


def state_to_names(state):
    """Panel number -> list of test names, e.g. 47 -> ['age', 'sex', 'cp', 'trestbps', 'fbs']."""
    return [FEATURES[i] for i in range(N) if (int(state) >> i) & 1]


def names_to_state(names):
    """List of test names -> panel number (the inverse of state_to_names)."""
    return sum(1 << FEATURES.index(n) for n in names)


def exact_optimum(f):
    """The best five-test panel for objective f, found by checking all 1,287 of them (takes milliseconds)."""
    scores_of_five_test_panels = f[FEAS_IDX]
    return int(FEAS_IDX[int(np.argmin(scores_of_five_test_panels))])


def rank_of(f, state):
    """Rank of a five-test panel among all 1,287 by objective f (1 = the best)."""
    scores_of_five_test_panels = f[FEAS_IDX]
    return int((scores_of_five_test_panels < f[int(state)] - 1e-15).sum()) + 1


def score_pareto(score, cost):
    """Five-test panels that no other panel beats on BOTH score (lower is better) and price.

    Walk through the panels from cheapest to most expensive and keep each one that scores better than everything
    cheaper. Result: the exact cost-vs-score Pareto set (13 panels).
    """
    scores, prices = score[FEAS_IDX], cost[FEAS_IDX]
    keep, best_so_far = [], np.inf
    for i in np.lexsort((scores, prices)):          # sort by price, ties broken by score
        if scores[i] < best_so_far - 1e-12:
            keep.append(int(FEAS_IDX[i]))
            best_so_far = scores[i]
    return keep


def auc_front(auc_map, cost, size=K):
    """The price ladder: cheapest-first list of panels whose cross-validated AUC beats every cheaper panel.

    auc_map: {panel: AUC}. Only panels with `size` tests are considered.
    """
    panels = [s for s in auc_map if bin(s).count("1") == size]
    panels.sort(key=lambda s: (cost[s], -auc_map[s]))   # cheapest first; at equal price, best AUC first
    ladder, best_so_far = [], -1.0
    for s in panels:
        if auc_map[s] > best_so_far + 1e-12:
            ladder.append(s)
            best_so_far = auc_map[s]
    return ladder


# =================================================================================================================
# 5. Exact model of the circuit (NumPy, no Qiskit)
# =================================================================================================================
def complete_pairs(n=N):
    """All 78 pairs of tests, in "round-robin tournament" order: 13 rounds of 6 pairs that share no test.

    The circuit's mixer applies one gate per pair in exactly this order, so this model must use it too.
    (With 13 tests, one "player" sits out each round; that is the dummy player n added below.)
    """
    players_count = n + 1 if n % 2 else n
    players = list(range(players_count))
    pairs = []
    for _ in range(players_count - 1):
        for i in range(players_count // 2):
            a, b = players[i], players[players_count - 1 - i]
            if a < n and b < n:
                pairs.append((min(a, b), max(a, b)))
        players = [players[0]] + [players[-1]] + players[1:-1]   # rotate everyone except the first player
    return pairs


def pair_maps(pairs):
    """For each pair of tests (a, b): which five-test panels the mixer gate on (a, b) mixes together.

    The gate swaps "a in, b out" with "a out, b in", so it pairs every panel that contains a but not b with the
    same panel with a replaced by b. Returns, per pair, the positions (in FEAS_IDX order) of both sides.
    """
    maps = []
    for a, b in pairs:
        a_in_b_out = FEAS_IDX[(BITS[FEAS_IDX, a] == 1) & (BITS[FEAS_IDX, b] == 0)]
        a_out_b_in = a_in_b_out ^ (1 << a) ^ (1 << b)      # flip bits a and b
        maps.append((POS_IN_FEAS[a_in_b_out], POS_IN_FEAS[a_out_b_in]))
    return maps


def qaoa_xy_probs(f, gamma=GAMMA, beta=BETA, maps=None):
    """Exact output of the one-layer circuit, restricted to five-test panels (1,287 numbers that sum to 1).

    Because the mixer never changes the number of tests, the circuit can be simulated on just the 1,287
    five-test panels instead of all 8,192 basis states:
      1. start:      equal amplitude on every five-test panel (what keeping only five-test shots of the
                     RY start gives)
      2. cost layer: multiply each panel's amplitude by exp(-i * gamma * its normalised score)
      3. mixer:      for each pair (a, b), mix the amplitudes of "a in, b out" and "a out, b in" panels:
                     exp(+i beta (XX+YY)/2), which is Qiskit's XXPlusYYGate(-2 beta)
      4. read out:   probability = |amplitude|^2
    Returns probabilities in FEAS_IDX order.
    """
    maps = pair_maps(complete_pairs()) if maps is None else maps
    scores = f[FEAS_IDX]
    normalised_score = (scores - scores.mean()) / scores.std()
    amplitude = np.full(len(FEAS_IDX), 1 / math.sqrt(len(FEAS_IDX)), dtype=complex)
    amplitude = amplitude * np.exp(-1j * gamma * normalised_score)
    cos_beta, i_sin_beta = math.cos(beta), 1j * math.sin(beta)
    for in_out, out_in in maps:
        a, b = amplitude[in_out].copy(), amplitude[out_in].copy()
        amplitude[in_out] = cos_beta * a + i_sin_beta * b
        amplitude[out_in] = i_sin_beta * a + cos_beta * b
    probability = np.abs(amplitude) ** 2
    return probability / probability.sum()


def independent_choice(p_feas):
    """The comparison sampler with NO correlations between tests.

    It gives every test the same probability of being chosen as the circuit does, but picks each test
    independently, then keeps only five-test panels. If the circuit beats this sampler, the circuit's
    correlations between qubits are doing useful work, not just its per-test odds.
    p_feas: the circuit's probabilities in FEAS_IDX order. Returns this sampler's probabilities, same order.
    """
    full = np.zeros(2 ** N)
    full[FEAS_IDX] = p_feas
    per_test = np.clip(full @ BITS, 1e-12, 1 - 1e-12)          # P(test i is in the panel), from the circuit
    # P(panel) = product over tests of P(in) or P(out); computed with logs for accuracy
    product = np.exp(BITS @ np.log(per_test) + (1 - BITS) @ np.log(1 - per_test))[FEAS_IDX]
    return product / product.sum()


# =================================================================================================================
# 6. Statistics
# =================================================================================================================
def closed_form_all_found(dists, targets, shots, p_hw5=None):
    """Exact chance that ONE job samples every target panel at least once.

    dists:   one probability vector (FEAS_IDX order) per circuit in the job
    targets: the distinct panels we hope to see (e.g. the optimum of each price weight)
    shots:   raw shots per circuit; each one is a five-test sample with probability p_hw5 (P_HW5 = 0.2228 for the
             ideal circuit, or a per-circuit list for noisy reference data)

    Inclusion-exclusion: P(see all) = sum over every subset T of the targets of (-1)^|T| * P(miss everything in T),
    and P(miss everything in T) = product over circuits of (1 - P(one shot lands in T))^shots.
    """
    from itertools import combinations
    hw5 = [P_HW5] * len(dists) if p_hw5 is None else list(p_hw5)
    positions = [int(POS_IN_FEAS[t]) for t in targets]
    total = 0.0
    for k in range(len(positions) + 1):
        for missed in combinations(positions, k):
            p_miss_all = 1.0
            for p, h in zip(dists, hw5):
                p_miss_all *= (1.0 - h * float(sum(p[i] for i in missed))) ** shots
            total += (-1) ** k * p_miss_all
    return max(0.0, min(1.0, total))


def llr_stats(counts_feas, p_ideal, p_null):
    """Does a run's samples look like the ideal circuit or like the independent-choice sampler?

    Each sampled panel adds log(P_ideal(panel) / P_null(panel)) to a running total, the log-likelihood ratio.
    A large positive total means "looks like the ideal circuit"; a large negative one "looks like the sampler
    without correlations". Also returns the mean and standard deviation the total would have if the samples
    really came from each model, so the observed value can be compared with both.

    counts_feas: sample counts in FEAS_IDX order. Returns (observed, (mean, sd) if ideal, (mean, sd) if null, n).
    """
    weight = np.log(np.clip(p_ideal, 1e-300, None)) - np.log(np.clip(p_null, 1e-300, None))
    n = int(counts_feas.sum())
    observed = float(counts_feas @ weight)

    def mean_and_sd_if_drawn_from(p):
        mean_per_sample = float(p @ weight)
        variance_per_sample = float(p @ weight ** 2) - mean_per_sample ** 2
        return n * mean_per_sample, math.sqrt(max(n * variance_per_sample, 0.0))

    return observed, mean_and_sd_if_drawn_from(p_ideal), mean_and_sd_if_drawn_from(p_null), n


def wilson(k, n, z=1.96):
    """95% confidence interval (Wilson score) for a proportion k/n. Well behaved even when k = 0."""
    if n == 0:
        return (float("nan"), float("nan"))
    p = k / n
    d = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / d
    half_width = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, centre - half_width), min(1.0, centre + half_width))
