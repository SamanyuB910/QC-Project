"""Five Tests, Priced -- the quantum side: build the circuits, send the ONE job, read the measured counts.

THE CIRCUIT (one layer of QAOA, ported from prompt_b/s10_pareto_onejob.py). One qubit per test; 1 = "order it".
  1. Start:      RY(2 asin sqrt(5/13)) on every qubit, so each test is "in" with probability 5/13. Keeping only
                 the shots that have exactly five 1s leaves an equal mix of all 1,287 five-test panels.
  2. Cost layer: turns the objective into phases, so better panels pick up phases that the mixer converts into
                 higher probability. The objective is rewritten exactly as a sum of Z terms (its "Walsh" or
                 "Ising" expansion): single-qubit terms become RZ gates, pair terms become RZZ gates, and the one
                 three-qubit term (pay for the treadmill once) becomes a CX-RZ-CX ladder.
  3. XY mixer:   XXPlusYYGate on all 78 pairs. Each gate swaps a test in for a test out, so the number of tests
                 never changes: the "exactly five" rule is built into the circuit instead of a penalty term.
  4. Measure all 13 qubits.

WHAT IS IN THIS FILE
  1. Settings per simulator   default shots, and whether a simulator accepts several circuits in one job
  2. Circuits                 the QAOA circuit, the bit-order check circuit, the gate-convention probe
  3. Checks                   compile to simple gates, compare with the exact NumPy model, count gates
  4. Simulators               recognise which simulator Qollab passed in, and send exactly one job
  5. Reading counts           measured bitstrings -> panel numbers -> counts per five-test panel
"""
import math
import time
from itertools import combinations

import numpy as np

from ftp_core import FEAS_IDX, K, N, complete_pairs

# =================================================================================================================
# 1. Settings per simulator
# =================================================================================================================

# The bit-order check circuit always reads this panel: age, sex, cp, trestbps, fbs (bits 0, 1, 2, 3 and 5).
# If a simulator reversed the bit order, it would read a different panel (thal, ca, slope, oldpeak, restecg).
SENTINEL_STATE = 0b0000000101111

# Default shots per circuit for each kind of simulator. Simulators that add noise shot by shot inside the
# browser are slow, so they get fewer shots.
SHOT_POLICY = {"basic": 1000, "braket": 1000, "aer": 1000, "ionq": 1000, "ibm_fake": 8, "aer_noise": 100,
               "unknown": 100}

# Whether a list of circuits can be sent as ONE job. IonQ through Qollab cannot: tested on Qollab on
# Oct 10 2026, the IonQ API answered "Only job type ionq.circuit.v1 is supported" to a multi-circuit job.
# So on IonQ the program sends a single circuit.
LIST_JOBS_OK = {"basic": True, "braket": True, "aer": True, "aer_noise": True, "ibm_fake": True, "ionq": False,
                "unknown": True}


# =================================================================================================================
# 2. Circuits
# =================================================================================================================
def walsh_terms(f, tol=1e-10):
    """Rewrite the objective as a sum of products of Z values: f(x) = const + sum_S c_S * prod_{i in S} z_i.

    Here z_i = 1 - 2 x_i is +1 when test i is out and -1 when it is in (the eigenvalue of a Z gate). Because the
    objective is a polynomial of degree at most 3 in x, terms with 1, 2 and 3 tests are enough, and each
    coefficient c_S is simply the average of f(x) * prod z_i over all 8,192 panels.
    Returns {tuple of test indices: coefficient}. Asserts that the expansion reproduces f exactly.
    """
    from ftp_core import BITS
    Z = 1.0 - 2.0 * BITS.astype(float)
    const = float(f.mean())
    terms = {}
    rebuilt = np.full(len(f), const)
    for order in (1, 2, 3):
        for S in combinations(range(N), order):
            product_of_z = np.prod(Z[:, list(S)], axis=1)
            coefficient = float((f * product_of_z).mean())
            if abs(coefficient) > tol:
                terms[S] = coefficient
                rebuilt += coefficient * product_of_z
    error = float(np.max(np.abs(rebuilt - f)))
    assert error < 1e-9, f"Walsh expansion does not reproduce the objective (max error {error:.2e})"
    return terms


def build_circuit(f, name, gamma, beta):
    """The one-layer QAOA circuit for one price weight. f: objective over all 8,192 panels.

    Returns (circuit, Walsh terms). See the top of this file for what each layer does.
    """
    from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister
    from qiskit.circuit.library import XXPlusYYGate

    # The objective is divided by its spread over five-test panels, so one gamma works for every price weight.
    spread = float(f[FEAS_IDX].std())
    terms = walsh_terms(f)
    qubits, bits = QuantumRegister(N, "q"), ClassicalRegister(N, "c")
    qc = QuantumCircuit(qubits, bits, name=name)

    # 1. Start: every test "in" with probability 5/13.
    start_angle = 2 * math.asin(math.sqrt(K / N))
    for i in range(N):
        qc.ry(start_angle, i)

    # 2. Cost layer: one rotation per Walsh term, angle proportional to its coefficient.
    for S, coefficient in terms.items():
        angle = 2 * gamma * coefficient / spread
        if len(S) == 1:
            qc.rz(angle, S[0])
        elif len(S) == 2:
            qc.rzz(angle, S[0], S[1])
        else:
            # Three-test term Z_a Z_b Z_t: copy the parity of a and b onto t with two CX gates, rotate t, undo.
            a, b, t = S
            qc.cx(a, t)
            qc.cx(b, t)
            qc.rz(angle, t)
            qc.cx(b, t)
            qc.cx(a, t)

    # 3. XY mixer: swap a test in for a test out, on every pair, in the same order as the NumPy model.
    for (i, j) in complete_pairs():
        qc.append(XXPlusYYGate(-2 * beta), [i, j])

    # 4. Measure: classical bit i = qubit i = test i.
    qc.measure(qubits, bits)
    return qc, terms


def sentinel_circuit():
    """Bit-order check: X gates only, so it always reads the panel {age, sex, cp, trestbps, fbs}.

    Sent alongside the QAOA circuits; if the simulator reads it back correctly, the bit order is right.
    """
    from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister
    qubits, bits = QuantumRegister(N, "q"), ClassicalRegister(N, "c")
    qc = QuantumCircuit(qubits, bits, name="ftp_sentinel")
    for i in range(N):
        if (SENTINEL_STATE >> i) & 1:
            qc.x(i)
    qc.measure(qubits, bits)
    return qc


# The gate-convention probe (Run setting circuits = "probe"): one row per gate type the project submits.
# Each row: (what is measured, which qubits, the exact expected probability, how to read it from the qubits).
PROBE_TESTS = [
    ("RZZ(pi/3) between H layers: P(both qubits 1)", (0, 1), 0.25, "both"),
    ("RZZ(pi/2) between H layers: P(both qubits 1)", (2, 3), 0.50, "both"),
    ("RY(pi/3): P(1)", (4,), 0.25, "one"),
    ("RX(pi/3): P(1)", (5,), 0.25, "one"),
    ("RZ(pi/3) between H gates: P(1)", (6,), 0.25, "one"),
    ("X: P(1)", (7,), 1.00, "one"),
    ("idle qubits 8-12: P(1) (readout error)", (8, 9, 10, 11, 12), 0.00, "mean"),
]


def probe_circuit():
    """One shallow 13-qubit circuit with known answers for every gate type we submit (rz, ry, rx, rzz, x).

    If a simulator interpreted an angle differently (for example RZZ(theta) as exp(-i theta ZZ) instead of
    exp(-i theta/2 ZZ)), these probabilities would move far from the expected values; noise only nudges them.
    """
    from math import pi

    from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister
    qubits, bits = QuantumRegister(N, "q"), ClassicalRegister(N, "c")
    qc = QuantumCircuit(qubits, bits, name="ftp_probe")
    for (a, b), theta in (((0, 1), pi / 3), ((2, 3), pi / 2)):
        qc.h([a, b])
        qc.rzz(theta, a, b)
        qc.h([a, b])
    qc.ry(pi / 3, 4)
    qc.rx(pi / 3, 5)
    qc.h(6)
    qc.rz(pi / 3, 6)
    qc.h(6)
    qc.x(7)
    qc.measure(qubits, bits)
    return qc


def probe_readout(counts):
    """Measured probability for each PROBE_TESTS row, from raw counts {bitstring: count}. Returns (values, shots)."""
    shots, totals = 0, [0.0] * len(PROBE_TESTS)
    for key, count in counts.items():
        panel, _ = key_to_state(key)
        shots += count
        for row, (_, qubits, _, how) in enumerate(PROBE_TESTS):
            values = [(panel >> q) & 1 for q in qubits]
            if how == "both":
                totals[row] += count * (values[0] & values[1])
            elif how == "one":
                totals[row] += count * values[0]
            else:                                       # "mean": average over the listed qubits
                totals[row] += count * sum(values) / len(values)
    return [t / max(shots, 1) for t in totals], shots


# =================================================================================================================
# 3. Checks
# =================================================================================================================
def portable(circuits, seed):
    """Compile once, without a target device, to five simple gate types every simulator here accepts.

    The same compiled circuits go to the built-in simulator, IonQ, Braket and Aer, and the exactness check runs
    on exactly what is submitted.
    """
    from qiskit import transpile
    return transpile(circuits, basis_gates=["rz", "ry", "rx", "rzz", "x"], optimization_level=1,
                     seed_transpiler=seed)


def submitted_vs_reference_tvd(tqc, p_ref):
    """Simulate the compiled circuit exactly with Qiskit and compare it with the NumPy model.

    Returns (total-variation distance between the two five-test distributions, P(a shot has five tests)).
    A distance near 1e-15 means the circuit and the model agree to rounding error.
    """
    from qiskit.quantum_info import Statevector
    p_all = Statevector(tqc.remove_final_measurements(inplace=False)).probabilities()
    p_five = p_all[FEAS_IDX]
    return 0.5 * float(np.abs(p_five / p_five.sum() - p_ref).sum()), float(p_five.sum())


def two_qubit_count(qc):
    """Number of two-qubit gates in a circuit (the expensive, noisy gates on real hardware)."""
    ops = qc.count_ops()
    return int(sum(v for k, v in ops.items() if k in ("rzz", "cx", "cz", "ecr", "rxx", "ryy", "xx_plus_yy", "swap")))


# =================================================================================================================
# 4. Simulators
# =================================================================================================================
def classify_backend(be):
    """Recognise the simulator Qollab passed in. Returns (kind, description).

    kind is one of: basic (Qollab's built-in) | ionq | braket | ibm_fake (IBM noise models) |
                    aer_noise (Aer with noise) | aer (ideal Aer) | unknown
    """
    module = type(be).__module__.lower()
    name = str(getattr(be, "name", "") or "").lower()
    description = f"{type(be).__module__}.{type(be).__name__} name={getattr(be, 'name', '?')!r}"
    if "basic_provider" in module or name == "basic_simulator":
        return "basic", description
    if "ionq" in module or "ionq" in name:
        return "ionq", description
    if "braket" in module or "braket" in name:
        return "braket", description
    if "fake" in module or name.startswith("fake") or "ibm" in module:
        return "ibm_fake", description
    if "aer" in module:
        try:
            noisy = getattr(be.options, "noise_model", None) is not None
        except Exception:  # noqa: BLE001
            noisy = False
        try:
            method = str(getattr(be.options, "method", ""))
        except Exception:  # noqa: BLE001
            method = ""
        if "density" in method:
            return "unknown", description + " (density-matrix method: refused, 13 qubits needs ~1 GB)"
        if _has_lattice(be):        # Aer built from a device (e.g. AerSimulator.from_backend): treat it like IBM
            return "ibm_fake", description
        return ("aer_noise" if noisy else "aer"), description
    return "unknown", description


def _has_lattice(be):
    """True if the simulator models a device with fixed qubit connections (more qubits than ours + a coupling map)."""
    try:
        coupling_map = getattr(be, "coupling_map", None)
        qubit_count = getattr(be, "num_qubits", None)
        return coupling_map is not None and qubit_count is not None and qubit_count > N
    except Exception:  # noqa: BLE001
        return False


def needs_routing(be, kind):
    """Must the circuits be re-compiled for this device's qubit connections?

    Yes for lattice devices (IBM-style), where a two-qubit gate only works between neighbouring qubits.
    No for trapped ions (IonQ: every qubit connects to every other) and for plain simulators.
    """
    if kind in ("ionq", "basic", "braket"):
        return False
    return kind == "ibm_fake" or _has_lattice(be)


class OneJobGuard:
    """IonQ allows ONE job per code run. Every job goes through submit_once(), which asks this guard first;
    a second request in the same Run raises an error instead of reaching the simulator."""

    def __init__(self):
        self.calls = 0

    def check(self):
        if self.calls >= 1:
            raise RuntimeError("one-job guard: backend.run was already called in this Run")
        self.calls += 1


def submit_once(be, circuits, shots, guard, seed, kind="unknown"):
    """Send the job (the project's ONLY call to backend.run) and wait for it. Returns (result, seconds)."""
    guard.check()
    run_options = {"shots": int(shots)}
    if kind == "ionq":
        try:   # IonQ takes its random seed as a backend option, not as a run() argument
            be.set_options(sampler_seed=int(seed))
        except Exception:  # noqa: BLE001
            pass
    else:
        try:
            if hasattr(be.options, "seed_simulator"):
                run_options["seed_simulator"] = int(seed)
        except Exception:  # noqa: BLE001
            pass
    started = time.time()
    job = be.run(circuits, **run_options)
    try:
        job_id = job.job_id()
    except Exception:  # noqa: BLE001
        job_id = "?"
    print(f"  job submitted (id {job_id}); waiting for results ...", flush=True)
    result = job.result()
    return result, time.time() - started


# =================================================================================================================
# 5. Reading counts
# =================================================================================================================
def key_to_state(key):
    """Measured bitstring -> (panel number, any extra high bits).

    Accepts '0000000101111', keys with spaces between registers, and hex keys like '0x2f'.
    """
    digits = str(key).replace(" ", "")
    value = int(digits, 16) if digits.startswith("0x") else int(digits, 2)
    return value & ((1 << N) - 1), value >> N


def counts_for(result, name, index):
    """Counts {bitstring: count} of one circuit in a job result: by circuit name first, then by position.

    Simulators differ in what get_counts accepts and returns (a dict, or a list of dicts), so try each form.
    """
    for key in (name, index):
        try:
            counts = result.get_counts(key)
            if isinstance(counts, list):
                counts = counts[index]
            return dict(counts)
        except Exception:  # noqa: BLE001
            continue
    counts = result.get_counts()
    return dict(counts[index] if isinstance(counts, list) else counts)


def five_test_counts(counts):
    """Keep only shots with exactly five tests.

    Returns ({panel: count}, total shots, shots that had stray bits beyond the 13 test bits).
    """
    panel_counts, total, extra = {}, 0, 0
    for key, count in counts.items():
        panel, high_bits = key_to_state(key)
        total += int(count)
        extra += int(count) if high_bits else 0
        if panel.bit_count() == K:
            panel_counts[panel] = panel_counts.get(panel, 0) + int(count)
    return panel_counts, total, extra


def as_vector(panel_counts):
    """{panel: count} -> a vector of counts over the 1,287 five-test panels (FEAS_IDX order)."""
    from ftp_core import POS_IN_FEAS
    vector = np.zeros(len(FEAS_IDX))
    for panel, count in panel_counts.items():
        vector[POS_IN_FEAS[panel]] += count
    return vector
