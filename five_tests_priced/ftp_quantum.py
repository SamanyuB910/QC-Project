"""Five Tests, Priced -- quantum side: circuits, the one-job guard, backend handling, count parsing.

Circuit (p = 1 QAOA, ported from prompt_b/s10_pareto_onejob.py):
  1. RY(2 asin sqrt(5/13)) on every qubit: each test is "in" with probability 5/13. Keeping only shots with exactly
     five 1s turns this into the uniform superposition of all 1,287 five-test panels (a Dicke state) for free.
  2. Cost layer exp(-i gamma f_norm): the objective's exact Walsh (Ising) expansion -> RZ, RZZ and one CX-RZ-CX
     ladder for the treadmill's three-test price term.
  3. XY mixer: XXPlusYYGate(-2 beta) on all 78 pairs. It swaps a test in for a test out, so the number of tests
     never changes -- the "exactly five" rule is built into the circuit instead of a penalty term.
"""
import math
import time
from itertools import combinations

import numpy as np

from ftp_core import FEAS_IDX, K, N, complete_pairs

SENTINEL_STATE = 0b0000000101111   # age, sex, cp, trestbps, fbs -> reversed bit order would read as thal, ca, ...

# How many shots per circuit each backend kind gets by default (per-shot noisy simulators are slow in a browser).
SHOT_POLICY = {"basic": 1000, "braket": 1000, "aer": 1000, "ionq": 500, "ibm_fake": 8, "aer_noise": 100,
               "unknown": 100}
# Whether a list of circuits may be sent as ONE job. Confirmed per backend kind by the Phase 0 smoke test.
LIST_JOBS_OK = {"basic": True, "braket": True, "aer": True, "aer_noise": True, "ibm_fake": True, "ionq": True,
                "unknown": True}


# ----------------------------------------------------------------------------------------------- circuits
def walsh_terms(f, tol=1e-10):
    """Exact expansion f(x) = const + sum_S c_S prod_{i in S} z_i with z = 1 - 2x (orders 1..3).
    Asserts the expansion reproduces f exactly (it is a cubic polynomial in x)."""
    from ftp_core import BITS
    Z = 1.0 - 2.0 * BITS.astype(float)
    const = float(f.mean())
    terms = {}
    recon = np.full(len(f), const)
    for order in (1, 2, 3):
        for S in combinations(range(N), order):
            zs = np.prod(Z[:, list(S)], axis=1)
            c = float((f * zs).mean())
            if abs(c) > tol:
                terms[S] = c
                recon += c * zs
    err = float(np.max(np.abs(recon - f)))
    assert err < 1e-9, f"Walsh expansion does not reproduce the objective (max error {err:.2e})"
    return terms


def build_circuit(f, name, gamma, beta):
    """The logical p=1 circuit for one price weight. f: objective over all 2^13 subsets."""
    from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister
    from qiskit.circuit.library import XXPlusYYGate
    sd = float(f[FEAS_IDX].std())
    terms = walsh_terms(f)
    q, c = QuantumRegister(N, "q"), ClassicalRegister(N, "c")
    qc = QuantumCircuit(q, c, name=name)
    th = 2 * math.asin(math.sqrt(K / N))
    for i in range(N):
        qc.ry(th, i)
    for S, cf in terms.items():
        ang = 2 * gamma * cf / sd
        if len(S) == 1:
            qc.rz(ang, S[0])
        elif len(S) == 2:
            qc.rzz(ang, S[0], S[1])
        else:
            a, b, t = S
            qc.cx(a, t)
            qc.cx(b, t)
            qc.rz(ang, t)
            qc.cx(b, t)
            qc.cx(a, t)
    for (i, j) in complete_pairs():
        qc.append(XXPlusYYGate(-2 * beta), [i, j])
    qc.measure(q, c)
    return qc, terms


def sentinel_circuit():
    """No two-qubit gates: always reads panel {age, sex, cp, trestbps, fbs}. Proves the bit order on every run."""
    from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister
    q, c = QuantumRegister(N, "q"), ClassicalRegister(N, "c")
    qc = QuantumCircuit(q, c, name="ftp_sentinel")
    for i in range(N):
        if (SENTINEL_STATE >> i) & 1:
            qc.x(i)
    qc.measure(q, c)
    return qc


def portable(circuits, seed):
    """Transpile once, with no backend, to gates every simulator here accepts. The same circuits go to the built-in
    simulator, IonQ, Braket and Aer, and the equivalence check runs on exactly what is submitted."""
    from qiskit import transpile
    return transpile(circuits, basis_gates=["rz", "ry", "rx", "rzz", "x"], optimization_level=1,
                     seed_transpiler=seed)


def submitted_vs_reference_tvd(tqc, p_ref):
    """Total-variation distance between the submitted circuit's exact five-test distribution and the NumPy model."""
    from qiskit.quantum_info import Statevector
    p = Statevector(tqc.remove_final_measurements(inplace=False)).probabilities()
    p5 = p[FEAS_IDX]
    return 0.5 * float(np.abs(p5 / p5.sum() - p_ref).sum()), float(p5.sum())


def two_qubit_count(qc):
    ops = qc.count_ops()
    return int(sum(v for k, v in ops.items() if k in ("rzz", "cx", "cz", "ecr", "rxx", "ryy", "xx_plus_yy", "swap")))


# ----------------------------------------------------------------------------------------------- backends
def classify_backend(be):
    """Return (kind, description). kind in basic | ionq | ibm_fake | aer_noise | aer | braket | unknown."""
    mod = type(be).__module__.lower()
    name = str(getattr(be, "name", "") or "").lower()
    desc = f"{type(be).__module__}.{type(be).__name__} name={getattr(be, 'name', '?')!r}"
    if "basic_provider" in mod or name == "basic_simulator":
        return "basic", desc
    if "ionq" in mod or "ionq" in name:
        return "ionq", desc
    if "braket" in mod or "braket" in name:
        return "braket", desc
    if "fake" in mod or name.startswith("fake") or "ibm" in mod:
        return "ibm_fake", desc
    if "aer" in mod:
        try:
            noisy = getattr(be.options, "noise_model", None) is not None
        except Exception:  # noqa: BLE001
            noisy = False
        try:
            method = str(getattr(be.options, "method", ""))
        except Exception:  # noqa: BLE001
            method = ""
        if "density" in method:
            return "unknown", desc + " (density-matrix method: refused, 13 qubits needs ~1 GB)"
        return ("aer_noise" if noisy else "aer"), desc
    return "unknown", desc


def needs_routing(be):
    """True for coupling-map devices (IBM fake backends): they must be transpiled against the device."""
    try:
        cmap = getattr(be, "coupling_map", None)
        nq = getattr(be, "num_qubits", None)
        return cmap is not None and nq is not None and nq > N
    except Exception:  # noqa: BLE001
        return False


class OneJobGuard:
    """IonQ allows ONE job per code run. Every quantum call in this project goes through submit_once(); the guard
    makes a second call impossible within a single Run press."""

    def __init__(self):
        self.calls = 0

    def check(self):
        if self.calls >= 1:
            raise RuntimeError("one-job guard: backend.run was already called in this Run")
        self.calls += 1


def submit_once(be, circuits, shots, guard, seed, kind="unknown"):
    guard.check()
    kwargs = {"shots": int(shots)}
    if kind == "ionq":
        try:   # IonQ seeds its noise simulation from the backend option, not from a run() argument
            be.set_options(sampler_seed=int(seed))
        except Exception:  # noqa: BLE001
            pass
    else:
        try:
            if hasattr(be.options, "seed_simulator"):
                kwargs["seed_simulator"] = int(seed)
        except Exception:  # noqa: BLE001
            pass
    t0 = time.time()
    job = be.run(circuits, **kwargs)
    try:
        jid = job.job_id()
    except Exception:  # noqa: BLE001
        jid = "?"
    print(f"  job submitted (id {jid}); waiting for results ...", flush=True)
    result = job.result()
    return result, time.time() - t0


# ----------------------------------------------------------------------------------------------- counts
def key_to_state(key):
    """Measured key -> 13-bit panel integer. Accepts '0101...', keys with spaces, and '0x..' hex keys."""
    k = str(key).replace(" ", "")
    v = int(k, 16) if k.startswith("0x") else int(k, 2)
    return v & ((1 << N) - 1), v >> N


def counts_for(result, name, index):
    """Counts of one circuit, by name first, then by position; tolerates list-of-dicts results."""
    for key in (name, index):
        try:
            c = result.get_counts(key)
            if isinstance(c, list):
                c = c[index]
            return dict(c)
        except Exception:  # noqa: BLE001
            continue
    c = result.get_counts()
    return dict(c[index] if isinstance(c, list) else c)


def five_test_counts(counts):
    """Keep only shots with exactly five tests. Returns ({panel: count}, raw total, shots with stray extra bits)."""
    out, total, extra = {}, 0, 0
    for key, v in counts.items():
        s, hi = key_to_state(key)
        total += int(v)
        extra += int(v) if hi else 0
        if s.bit_count() == K:
            out[s] = out.get(s, 0) + int(v)
    return out, total, extra


def as_vector(panel_counts):
    """{panel: count} -> counts vector over the 1,287 five-test panels (FEAS_IDX order)."""
    from ftp_core import POS_IN_FEAS
    v = np.zeros(len(FEAS_IDX))
    for s, c in panel_counts.items():
        v[POS_IN_FEAS[s]] += c
    return v
