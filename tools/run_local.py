"""Run five_tests_priced/main.py on a laptop the way Qollab does: working directory = project folder,
`backend` injected as a module global, main() called once with the Run-settings values.

    .venv/Scripts/python.exe tools/run_local.py --backend basic
    .venv/Scripts/python.exe tools/run_local.py --backend aer-forte --set shots=100
    .venv/Scripts/python.exe tools/run_local.py --backend fake-ibm
    .venv/Scripts/python.exe tools/run_local.py --backend basic --set circuits=single --set dump_counts=true
    .venv/Scripts/python.exe tools/run_local.py --backend basic --save-figures figures   # figures as PNG files

Backends: basic (Qiskit BasicSimulator = Qollab's built-in), aer (ideal Aer), aer-forte (Aer with IonQ forte-1
legacy depolarizing rates: 1q 2.67e-4, 2q 4.95e-3), fake-ibm (GenericBackendV2 heavy-hex device with noise).
The backend's run() is wrapped to count calls; the script fails if main() calls run() != 1 time.
"""
import argparse
import importlib.util
import os
import pathlib
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parents[1]
PROJECT = ROOT / "five_tests_priced"


def count_runs(be):
    """Wrap the backend's run() on the instance (type and module stay real, as in Qollab) and count calls."""
    original = be.run
    be.run_calls = 0

    def run(*a, **k):
        be.run_calls += 1
        return original(*a, **k)

    be.run = run
    return be


def make_backend(name):
    if name == "basic":
        from qiskit.providers.basic_provider import BasicSimulator
        return BasicSimulator()
    if name in ("aer", "aer-forte"):
        from qiskit_aer import AerSimulator
        if name == "aer":
            return AerSimulator()
        from qiskit_aer.noise import NoiseModel, depolarizing_error
        nm = NoiseModel()
        nm.add_all_qubit_quantum_error(depolarizing_error(2.67e-4, 1), ["rx", "ry", "rz", "x"])
        nm.add_all_qubit_quantum_error(depolarizing_error(4.95e-3, 2), ["rzz"])
        return AerSimulator(noise_model=nm)
    if name == "fake-ibm":
        from qiskit.providers.fake_provider import GenericBackendV2
        from qiskit_aer import AerSimulator
        return AerSimulator.from_backend(GenericBackendV2(num_qubits=27, seed=7))
    raise SystemExit(f"unknown backend {name}")


def parse_value(v):
    if v.lower() in ("true", "false"):
        return v.lower() == "true"
    for cast in (int, float):
        try:
            return cast(v)
        except ValueError:
            pass
    return v


def save_figures_instead_of_showing(folder):
    """On Qollab, plt.show() draws each figure in the Run output. Here, save each one as a PNG instead."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    folder.mkdir(parents=True, exist_ok=True)
    names = iter(["price_ladder.png", "recovery_vs_shots.png"])

    def show(*args, **kwargs):
        path = folder / next(names, f"figure_{len(list(folder.glob('*.png'))) + 1}.png")
        plt.gcf().savefig(path, dpi=150)
        print(f"  [run_local] figure saved: {path}")

    plt.show = show


def run(backend_name, settings, project=PROJECT, entry="main.py"):
    os.chdir(project)
    sys.path.insert(0, str(project))
    be = count_runs(make_backend(backend_name))
    spec = importlib.util.spec_from_file_location("main", project / entry)
    mod = importlib.util.module_from_spec(spec)
    mod.backend = be
    spec.loader.exec_module(mod)
    t = time.time()
    mod.main(**settings)
    return be.run_calls, time.time() - t


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--backend", default="basic")
    ap.add_argument("--set", action="append", default=[], help="main() setting, e.g. shots=200")
    ap.add_argument("--save-figures", metavar="FOLDER",
                    help="save the figures as PNG files in this folder (relative to the repository root)")
    args = ap.parse_args()
    settings = {}
    for kv in args.set:
        k, v = kv.split("=", 1)
        settings[k] = parse_value(v)
    os.environ.setdefault("MPLBACKEND", "Agg")
    if args.save_figures:
        save_figures_instead_of_showing((ROOT / args.save_figures).resolve())
    calls, secs = run(args.backend, settings)
    print(f"\n[run_local] backend={args.backend} run() calls={calls} main() wall time={secs:.1f}s")
    if calls != 1:
        raise SystemExit("ONE-JOB RULE VIOLATED")


if __name__ == "__main__":
    main()
