"""Backend paths the judges may pick (built-in is covered in test_quantum.py) and import hygiene."""
import subprocess
import sys

import pytest

from conftest import PROJECT, ROOT


def _run(backend_name, **settings):
    sys.path.insert(0, str(ROOT / "tools"))
    import run_local
    return run_local.run(backend_name, settings)


@pytest.mark.parametrize("backend_name,settings", [
    ("aer-forte", {"shots": 100, "run_baselines": False, "show_figures": False}),
    ("fake-ibm", {"shots": 8, "run_baselines": False, "show_figures": False}),
    ("aer", {"shots": 200, "circuits": "single", "show_figures": False}),
])
def test_noisy_and_device_backends_run_in_one_job(backend_name, settings, capsys):
    calls, secs = _run(backend_name, **settings)
    out = capsys.readouterr().out
    assert calls == 1
    assert "JOB FAILED" not in out and "What the samples show" in out
    assert "This effort is supported by Qollab & IonQ." in out


def test_device_path_reports_gate_ledger(capsys):
    _run("fake-ibm", shots=8, run_baselines=False, show_figures=False)
    out = capsys.readouterr().out
    assert "routed to this device's coupling map" in out and "more two-qubit gates on this lattice" in out


def test_importing_main_stays_light():
    """A default import must not pull in heavy optional packages (they cost seconds in the browser)."""
    code = ("import sys, os; os.chdir(r'%s'); sys.path.insert(0, '.'); import main; "
            "print([m for m in ('sklearn', 'pandas', 'matplotlib', 'qiskit_aer', 'scipy') if m in sys.modules])"
            % PROJECT)
    out = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, check=True).stdout
    assert out.strip().splitlines()[-1] == "[]"
