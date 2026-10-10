"""Offline precompute for Five Tests, Priced. Writes five_tests_priced/results/precomputed.json.

Step 1 (Phase 1): the cross-validated AUC of every panel of 1-5 tests (2,379 panels) and provenance.
Later steps add the precomputed evidence tables (see --step).

Every number written here comes from re-running or reading the research scripts in
research_notes/QCA prompts Quantum Impact plan/scripts/prompt_b/ -- nothing is typed in by hand.

Usage:  .venv/Scripts/python.exe tools/precompute.py --step 1
"""
import argparse
import datetime as dt
import json
import pathlib
import platform
import sys

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[1]
RESEARCH = ROOT / "research_notes" / "QCA prompts Quantum Impact plan" / "scripts" / "prompt_b"
OUT = ROOT / "five_tests_priced" / "results" / "precomputed.json"


def load_existing():
    if OUT.exists():
        return json.loads(OUT.read_text(encoding="utf-8"))
    return {"provenance": {}, "tables": {}}


def versions():
    import qiskit
    import scipy
    import sklearn
    return {"python": platform.python_version(), "numpy": np.__version__, "scipy": scipy.__version__,
            "sklearn": sklearn.__version__, "qiskit": qiskit.__version__}


def step1(doc):
    z = np.load(RESEARCH / "results" / "s05_all_subsets.npz")
    states = [int(s) for s in z["states"]]
    aucs = [round(float(a), 6) for a in z["aucs"]]
    doc["auc_table"] = {
        "description": ("Cross-validated AUC of logistic regression (max_iter=2000, C=1) on every panel of 1-5 "
                        "tests; 5x3 repeated stratified CV, random_state=7, on all 297 patients."),
        "source": "research_notes/QCA prompts Quantum Impact plan/scripts/prompt_b/results/s05_all_subsets.npz "
                  "(computed by s05_downstream.py part C)",
        "states": states,
        "aucs": aucs,
    }
    s07 = json.loads((RESEARCH / "results" / "s07_robustness.json").read_text())
    s10 = json.loads((RESEARCH / "results" / "s10_pareto_onejob.json").read_text())
    doc["constants_mirror"] = {
        "note": "Mirror of constants hard-coded in ftp_core.py (tests check they agree).",
        "r_k10": s07["estimators"]["kNN-MI k=10"]["r"],
        "gamma": s10["gamma"][0],
        "beta": s10["beta"][0],
    }
    doc["provenance"]["step1"] = {"created": dt.datetime.now().isoformat(timespec="seconds"),
                                  "versions": versions()}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--step", type=int, default=1)
    args = ap.parse_args()
    doc = load_existing()
    if args.step == 1:
        step1(doc)
    else:
        sys.exit(f"unknown step {args.step}")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, separators=(",", ":")), encoding="utf-8")
    print(f"wrote {OUT} ({OUT.stat().st_size / 1024:.1f} KB)")


if __name__ == "__main__":
    main()
