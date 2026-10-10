"""The precomputed evidence the project page quotes: present, consistent with live code, and unchanged."""
import json

import numpy as np
import pytest

from conftest import PROJECT


@pytest.fixture(scope="module")
def ev():
    return json.loads((PROJECT / "results" / "precomputed.json").read_text())["evidence"]


def test_all_evidence_blocks_present(ev):
    assert {"recovery", "noisy", "penalty", "gates", "honest_cv", "confirm2", "confirm3"} <= set(ev)


def test_preregistered_checks_passed(ev):
    assert ev["confirm2"]["passed"] and ev["confirm3"]["passed"]
    assert all(r["subsamples_qaoa_higher"] >= 48 for r in ev["confirm2"]["rows"])
    assert max(r["gap"] for r in ev["confirm3"]["rows"]) <= 0.005


def test_claim1_replication(ev):
    q = ev["recovery"]["quantum_exact"]["1000"]["ideal QAOA circuit"]
    best_classical = max(d["222"]["all_found_rate"] for d in ev["recovery"]["classical_pooled_200_jobs"].values())
    assert q - best_classical >= 0.20


def test_quoted_numbers(ev):
    r = ev["recovery"]
    assert round(r["quantum_exact"]["1000"]["ideal QAOA circuit"], 2) == 0.98
    assert round(r["quantum_exact"]["1000"]["independent-choice"], 2) == 0.63
    assert round(ev["noisy"]["closed_form_all_found"]["1000"], 2) == 0.92
    cl = r["classical_pooled_200_jobs"]
    assert round(cl["simulated annealing (T0=0.3)"]["222"]["all_found_rate"], 2) == 0.55
    assert round(cl["random-restart local search"]["222"]["all_found_rate"], 2) == 0.63
    assert ev["gates"]["ionq_native_zz"][0] == 234 and min(ev["gates"]["cz_heavy_hex"]) >= 700


def test_penalty_rows_random_without_the_answer(ev):
    for row in ev["penalty"]["rows"]:
        if "automatic" in row["method"] or "textbook" in row["method"]:
            assert row["P_opt_given_five"] < 0.0015           # ~ 1/1287 = 0.00078: random level
        if row["method"].startswith("XY"):
            assert row["P_opt_given_five"] > 0.015


def test_noisy_counts_reproduce_closed_form(ev, model):
    """The noisy row is recomputed from the stored counts with the live closed-form code."""
    import ftp_core as core
    import ftp_quantum as quantum
    fs = model["fs"]
    targets = sorted({core.exact_optimum(fs[mu]) for mu in core.MU_GRID})
    dists = []
    for mu in core.MU_GRID:
        v = quantum.as_vector({int(k): c for k, c in ev["noisy"]["five_test_counts"][str(mu)].items()})
        dists.append(v / v.sum())
    got = core.closed_form_all_found(dists, targets, 1000, ev["noisy"]["P_five_tests"])
    assert abs(got - ev["noisy"]["closed_form_all_found"]["1000"]) < 1e-12
    assert np.isclose(sum(ev["noisy"]["P_five_tests"]) / 5, core.P_HW5, atol=0.01)
