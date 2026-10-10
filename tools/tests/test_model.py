"""Data, prices, objective and exact classical answers -- regression against the research logs
(prompt_b/results/s06_log.txt, s10_log.txt, s10d_log.txt)."""
import json

import numpy as np
import pandas as pd

from conftest import PROJECT, RESEARCH_B

MU_OPT_STATES = [7174, 6284, 6284, 4238, 47]          # mu = 0, 0.02, 0.05, 0.1, 0.2
MU_OPT_COSTS = [293.10, 206.80, 206.80, 106.90, 9.20]
PARETO = [47, 62, 79, 103, 782, 806, 4238, 4276, 4294, 3334, 6284, 6292, 7174]


def test_data_matches_raw_uci_file(model):
    X, y = model["X"], model["y"]
    assert X.shape == (297, 13) and int(y.sum()) == 137
    raw = pd.read_csv(RESEARCH_B / "data_raw" / "processed.cleveland.data", header=None, na_values="?").dropna()
    assert np.allclose(raw.iloc[:, :13].to_numpy(float), X)
    assert np.array_equal((raw.iloc[:, 13].to_numpy() > 0).astype(int), y)


def test_relevance_constants_match_research(model):
    core = model["core"]
    s07 = json.loads((RESEARCH_B / "results" / "s07_robustness.json").read_text())
    assert np.allclose(core.R_K10, s07["estimators"]["kNN-MI k=10"]["r"], atol=0, rtol=0)
    pre = json.loads((PROJECT / "results" / "precomputed.json").read_text())
    assert np.allclose(core.R_K10, pre["constants_mirror"]["r_k10"])
    assert core.GAMMA == pre["constants_mirror"]["gamma"] and core.BETA == pre["constants_mirror"]["beta"]


def test_costs(model):
    core, cost = model["core"], model["cost"]
    assert {k: round(v, 2) for k, v in core.shared_costs().items()} == \
        {"blood draw": 2.10, "thallium stress test": 101.90, "treadmill ECG": 86.30}
    worst = max(abs(cost[s] - core.panel_cost(s)) for s in range(2 ** 13))
    assert worst < 1e-12
    c5 = cost[core.FEAS_IDX]
    assert round(c5.min(), 2) == 9.20 and round(c5.max(), 2) == 313.87
    assert round(cost[2 ** 13 - 1], 2) == 323.97


def test_exact_optima_and_pareto(model):
    core, fs, cost = model["core"], model["fs"], model["cost"]
    opts = [core.exact_optimum(fs[mu]) for mu in core.MU_GRID]
    assert opts == MU_OPT_STATES
    assert [round(cost[o], 2) for o in opts] == MU_OPT_COSTS
    assert core.score_pareto(fs[0.0], cost) == PARETO


def test_auc_front(model):
    core, cost = model["core"], model["cost"]
    pre = json.loads((PROJECT / "results" / "precomputed.json").read_text())
    auc = dict(zip(pre["auc_table"]["states"], pre["auc_table"]["aucs"]))
    assert len(auc) == 2379
    front = core.auc_front(auc, cost)
    assert len(front) == 8
    assert round(auc[front[-1]], 3) == 0.911 and round(cost[front[-1]], 2) == 293.10


def test_greedy_and_local_search(model):
    core, fs = model["core"], model["fs"]
    import ftp_classical as classical
    ranks, ls_ok = [], []
    for mu in core.MU_GRID:
        g, ev = classical.greedy(fs[mu])
        assert ev == 55
        ranks.append(core.rank_of(fs[mu], g))
        ls, _ = classical.local_search(fs[mu], g)
        ls_ok.append(ls == core.exact_optimum(fs[mu]))
    assert ranks == [3, 7, 1, 26, 1]
    assert ls_ok == [True, True, True, False, True]
