import os
import pathlib
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[2]
PROJECT = ROOT / "five_tests_priced"
RESEARCH_B = ROOT / "research_notes" / "QCA prompts Quantum Impact plan" / "scripts" / "prompt_b"

if str(PROJECT) not in sys.path:
    sys.path.insert(0, str(PROJECT))
os.environ.setdefault("MPLBACKEND", "Agg")


@pytest.fixture(autouse=True)
def _in_project_dir(monkeypatch):
    """The project reads data files by paths relative to its own folder (Qollab's working directory)."""
    monkeypatch.chdir(PROJECT)


@pytest.fixture(scope="session")
def model():
    os.chdir(PROJECT)
    import ftp_core as core
    X, y = core.load_data()
    C = core.redundancy(X)
    cost = core.cost_vector()
    fs = {mu: core.objective(core.R_K10, C, cost, mu) for mu in core.MU_GRID}
    return {"core": core, "X": X, "y": y, "C": C, "cost": cost, "fs": fs}
