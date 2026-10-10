"""Five Tests, Priced -- Qollab smoke test (Phase 0).

Upload these files to a scratch Qollab project (keep the folder layout):
    main.py, ftp_smoke_helper.py, smoke_data.json, data/heart_cleveland_297.csv
Then press Run once per backend (built-in, IonQ Forte 1, one IBM device, AWS Braket local) and copy the
whole output back. Each press makes at most ONE backend.run call.

Run settings: mode = "list" (2 circuits in one job), "single" (1 circuit), or "none" (no quantum job);
shots = shots per circuit (use 50 on IonQ, 4 on IBM noise models, 200 on built-in).
"""
import builtins
import json
import math
import os
import sys
import time

import numpy as np

print(f"[smoke] module executing: __name__={__name__!r}", flush=True)

FEATURES = ["age", "sex", "cp", "trestbps", "chol", "fbs", "restecg",
            "thalach", "exang", "oldpeak", "slope", "ca", "thal"]
N, K = 13, 5
# k=10 kNN mutual information (20 seeds, discrete mask) -- research_notes/.../prompt_b/results/s07_robustness.json
R_K10 = [0.02809099244605955, 0.04011519336902181, 0.13669130599364226, 0.02024255183378254,
         0.009050224611943514, 5.01278870687627e-06, 0.016270742304905654, 0.09439720938402159,
         0.09169989289124486, 0.10784624302560919, 0.07539719598659554, 0.12797945853741322,
         0.14572276699853198]
# Turney (1995) costs: (full, discount); shared-procedure groups
EXPENSE = {"age": (1.00, 1.00), "sex": (1.00, 1.00), "cp": (1.00, 1.00), "trestbps": (1.00, 1.00),
           "chol": (7.27, 5.17), "fbs": (5.20, 3.10), "restecg": (15.50, 15.50),
           "thalach": (102.90, 1.00), "exang": (87.30, 1.00), "oldpeak": (87.30, 1.00),
           "slope": (87.30, 1.00), "ca": (100.90, 100.90), "thal": (102.90, 1.00)}
GROUPS = {"A": ["chol", "fbs"], "B": ["thalach", "thal"], "C": ["exang", "oldpeak", "slope"]}
GAMMA, BETA, LAM, MU = 1.7181724313553923, 0.16760994251739314, 0.1, 0.1
EXPECT_OPT_STATE, EXPECT_P_OPT_HW5 = 4238, 0.0150   # mu = 0.1 optimum and its ideal P(opt | Hamming weight 5)


def _sec(title):
    print(f"\n== {title}", flush=True)


def _timed_import(name):
    t = time.time()
    try:
        mod = __import__(name)
        return f"OK {getattr(mod, '__version__', '?')} ({time.time() - t:.2f}s)"
    except Exception as e:  # noqa: BLE001
        return f"FAILED {type(e).__name__}: {e}"


def _complete_pairs(n=N):
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


def _energy(X):
    allst = np.arange(2 ** N)
    B = ((allst[:, None] >> np.arange(N)) & 1).astype(float)
    C = np.abs(np.corrcoef(X, rowvar=False))
    np.fill_diagonal(C, 0.0)
    r = np.array(R_K10)
    d = np.array([EXPENSE[f][1] for f in FEATURES])
    cost = B @ d
    fi = {f: i for i, f in enumerate(FEATURES)}
    for mem in GROUPS.values():
        idx = [fi[f] for f in mem]
        cost = cost + (EXPENSE[mem[0]][0] - EXPENSE[mem[0]][1]) * (1 - np.prod(1 - B[:, idx], axis=1))
    E = -(B @ r) + LAM * 0.5 * np.einsum("si,ij,sj->s", B, C, B) + MU * cost / 100.0
    hw = B.sum(1).astype(int)
    return E, hw, B


def _build_circuit(E, hw, B):
    from itertools import combinations
    from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister
    from qiskit.circuit.library import XXPlusYYGate
    sd = float(E[hw == K].std())
    Z = 1.0 - 2.0 * B
    terms = {}
    for order in (1, 2, 3):
        for S in combinations(range(N), order):
            c = float((E * np.prod(Z[:, list(S)], axis=1)).mean())
            if abs(c) > 1e-10:
                terms[S] = c
    q, c = QuantumRegister(N, "q"), ClassicalRegister(N, "c")
    qc = QuantumCircuit(q, c, name="ftp_mu0p10")
    th = 2 * math.asin(math.sqrt(K / N))
    for i in range(N):
        qc.ry(th, i)
    for S, cf in terms.items():
        ang = 2 * GAMMA * cf / sd
        if len(S) == 1:
            qc.rz(ang, S[0])
        elif len(S) == 2:
            qc.rzz(ang, *S)
        else:
            a, b, t = S
            qc.cx(a, t); qc.cx(b, t); qc.rz(ang, t); qc.cx(b, t); qc.cx(a, t)
    for (i, j) in _complete_pairs():
        qc.append(XXPlusYYGate(-2 * BETA), [i, j])
    qc.measure(q, c)
    return qc, terms


def main(mode: str = "list", shots: int = 50, statevector_check: bool = True):
    t_start = time.time()
    _sec("environment")
    print("python", sys.version.split()[0], "| __name__", __name__, "| cwd", os.getcwd())
    try:
        print("files:", sorted(os.listdir(".")), "| data/:", sorted(os.listdir("data")))
    except Exception as e:  # noqa: BLE001
        print("listdir failed:", e)
    builtins._ftp_smoke_presses = getattr(builtins, "_ftp_smoke_presses", 0) + 1
    print("press counter (persists between Runs if > 1):", builtins._ftp_smoke_presses)

    _sec("imports")
    import qiskit
    print("qiskit", qiskit.__version__, "| numpy", np.__version__)
    for name in ("scipy", "sklearn", "matplotlib", "pandas"):
        print(f"  {name:11s}", _timed_import(name))
    try:
        t = time.time()
        from sklearn.feature_selection import mutual_info_classif  # noqa: F401
        print(f"  sklearn.feature_selection.mutual_info_classif OK ({time.time() - t:.2f}s)")
    except Exception as e:  # noqa: BLE001
        print("  mutual_info_classif FAILED:", e)
    try:
        import ftp_smoke_helper
        print("  sibling module import:", ftp_smoke_helper.HELLO, ftp_smoke_helper.double(21))
    except Exception as e:  # noqa: BLE001
        print("  sibling module import FAILED:", type(e).__name__, e)

    _sec("data files (literal paths)")
    X = None
    try:
        arr = np.loadtxt("data/heart_cleveland_297.csv", delimiter=",", skiprows=1)
        X, y = arr[:, :13], arr[:, 14].astype(int)
        print("csv OK:", arr.shape, "positives", int(y.sum()))
    except Exception as e:  # noqa: BLE001
        print("csv FAILED:", type(e).__name__, e)
    try:
        with open("smoke_data.json") as fh:
            print("json OK:", json.load(fh))
    except Exception as e:  # noqa: BLE001
        print("json FAILED:", type(e).__name__, e)

    _sec("backend")
    be = globals().get("backend", None)
    where = "module global"
    if be is None:
        be, where = getattr(builtins, "backend", None), "builtins"
    print("found backend via:", where if be is not None else "NOT FOUND")
    if be is not None:
        print("type:", type(be).__module__, type(be).__name__, "| name:", getattr(be, "name", "?"))
        for attr in ("num_qubits", "max_circuits", "version"):
            try:
                print(f"  {attr}:", getattr(be, attr))
            except Exception as e:  # noqa: BLE001
                print(f"  {attr}: <error {e}>")
        try:
            print("  options:", sorted(vars(be.options).keys()) if hasattr(be.options, "__dict__") else be.options)
        except Exception as e:  # noqa: BLE001
            print("  options: <error>", e)
        try:
            print("  target ops:", sorted(be.target.operation_names)[:40])
        except Exception as e:  # noqa: BLE001
            print("  target ops: <unavailable>", type(e).__name__)

    if X is None:
        print("\nno data -> stopping")
        return
    _sec("circuit build (mu=0.1) + sign-convention check")
    from qiskit import QuantumCircuit, transpile
    t = time.time()
    E, hw, B = _energy(X)
    feas = np.where(hw == K)[0]
    opt = int(feas[np.argmin(E[feas])])
    print("mu=0.1 exact optimum state:", opt, "(expected", EXPECT_OPT_STATE, ")",
          [FEATURES[i] for i in range(N) if (opt >> i) & 1])
    qc, terms = _build_circuit(E, hw, B)
    print(f"built in {time.time() - t:.2f}s; terms by order:",
          {o: sum(1 for S in terms if len(S) == o) for o in (1, 2, 3)})
    t = time.time()
    tqc = transpile(qc, basis_gates=["rz", "ry", "rx", "rzz"], optimization_level=1, seed_transpiler=7)
    print(f"portable transpile {time.time() - t:.2f}s; ops:", dict(tqc.count_ops()))
    if statevector_check:
        from qiskit.quantum_info import Statevector
        t = time.time()
        p = Statevector(tqc.remove_final_measurements(inplace=False)).probabilities()
        p5 = p[feas].sum()
        print(f"Statevector {time.time() - t:.2f}s: P(HW5)={p5:.6f} (expect 0.222784)  "
              f"P(opt|HW5)={p[opt] / p5:.5f} (expect ~{EXPECT_P_OPT_HW5}; ~0.0008 would mean a sign flip)")

    sentinel = QuantumCircuit(*tqc.qregs, *tqc.cregs, name="ftp_sentinel")
    for i in (0, 1, 2, 3, 5):   # age, sex, cp, trestbps, fbs -> state 47
        sentinel.x(i)
    sentinel.measure(range(N), range(N))

    _sec("figure")
    try:
        import matplotlib
        import matplotlib.pyplot as plt
        print("matplotlib backend:", matplotlib.get_backend())
        fig, ax = plt.subplots(figsize=(3, 2))
        ax.plot([0, 1, 2], [0, 1, 0], marker="o")
        ax.set_title("smoke figure")
        plt.show()
        plt.close("all")
        print("figure shown (check that a small plot appeared)")
    except Exception as e:  # noqa: BLE001
        print("figure FAILED:", type(e).__name__, e)

    _sec(f"quantum job (mode={mode}, shots={shots})")
    if be is None or mode == "none":
        print("skipped")
    else:
        run_kwargs = {"shots": int(shots)}
        try:
            if "seed_simulator" in vars(be.options):
                run_kwargs["seed_simulator"] = 7
        except Exception:  # noqa: BLE001
            pass
        circs = [sentinel, tqc] if mode == "list" else tqc
        print("submitting ONE job:", [c.name for c in circs] if isinstance(circs, list) else circs.name,
              "kwargs", run_kwargs, flush=True)
        t = time.time()
        try:
            job = be.run(circs, **run_kwargs)
            print("job submitted:", type(job).__name__, getattr(job, "job_id", lambda: "?")(), flush=True)
            res = job.result()
            print(f"result in {time.time() - t:.1f}s:", type(res).__name__)
            for key in (["ftp_sentinel", 0, "ftp_mu0p10", 1] if mode == "list" else [None, 0]):
                try:
                    cnt = res.get_counts() if key is None else res.get_counts(key)
                    ks = list(cnt)[:3]
                    tot = sum(cnt.values())
                    hw5 = {k: v for k, v in cnt.items()
                           if bin(int(str(k).replace(" ", ""), 16 if str(k).startswith("0x") else 2)).count("1") == K}
                    n5 = sum(hw5.values())
                    print(f"  get_counts({key!r}): total={tot} distinct={len(cnt)} sample_keys={ks} "
                          f"HW5={n5} key_len={len(str(ks[0])) if ks else '?'}")
                except Exception as e:  # noqa: BLE001
                    print(f"  get_counts({key!r}) FAILED: {type(e).__name__}: {e}")
        except Exception as e:  # noqa: BLE001
            print(f"JOB FAILED after {time.time() - t:.1f}s: {type(e).__name__}: {e}")
    print(f"\n[smoke] total {time.time() - t_start:.1f}s")
