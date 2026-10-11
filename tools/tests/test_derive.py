"""Every constant in ftp_core.py is re-derived from the project's own data by ftp_derive.py."""
import json

import numpy as np


def test_prices_are_turneys_files():
    import ftp_derive as derive
    expense, groups = derive.read_turney_prices()
    assert derive.prices_match_turney()
    assert len(expense) == 13 and sorted(groups) == ["blood draw", "thallium stress test", "treadmill ECG"]


def test_relevance_recomputes_exactly(model):
    import ftp_derive as derive
    core = model["core"]
    assert np.allclose(derive.relevance(model["X"], model["y"]), core.R_K10, rtol=0, atol=1e-12)


def test_angles_were_reproduced_by_the_tuning_procedure(model):
    """The full re-tuning takes about a minute (tools/precompute.py derive); its recorded result must match."""
    core = model["core"]
    with open("results/precomputed.json") as fh:
        derived = json.load(fh)["derivations"]
    assert derived["prices_match_turney_files"] is True
    assert derived["relevance_max_diff"] < 1e-12
    assert abs(derived["gamma"] - core.GAMMA) < 1e-9 and abs(derived["beta"] - core.BETA) < 1e-9
