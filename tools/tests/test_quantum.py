"""Circuits vs the exact model, closed-form predictions, the one-job rule, and count parsing."""
import numpy as np
import pytest

IDEAL = [0.0229, 0.0070, 0.0057, 0.0150, 0.0208]   # s10_log: ideal P(opt | five tests)
NULL = [0.0137, 0.0044, 0.0025, 0.0038, 0.0039]    # s10_log: independent-choice sampler


@pytest.fixture(scope="module")
def circuits(model):
    import ftp_quantum as quantum
    core, fs = model["core"], model["fs"]
    logical = [quantum.build_circuit(fs[mu], f"ftp_mu{str(mu).replace('.', 'p')}", core.GAMMA, core.BETA)
               for mu in core.MU_GRID]
    return logical, quantum.portable([c for c, _ in logical], seed=7)


def test_walsh_terms(model, circuits):
    logical, _ = circuits
    for mu, (_, terms) in zip(model["core"].MU_GRID, logical):
        by_order = {o: sorted(S for S in terms if len(S) == o) for o in (1, 2, 3)}
        assert len(by_order[1]) == 13 and len(by_order[2]) == 78
        assert by_order[3] == ([] if mu == 0.0 else [(8, 9, 10)])   # treadmill ECG: exang, oldpeak, slope


def test_submitted_circuits_match_exact_model(model, circuits):
    import ftp_quantum as quantum
    core, fs = model["core"], model["fs"]
    _, tqcs = circuits
    for mu, tqc, ideal in zip(core.MU_GRID, tqcs, IDEAL):
        p = core.qaoa_xy_probs(fs[mu])
        tvd, p5 = quantum.submitted_vs_reference_tvd(tqc, p)
        assert tvd < 1e-9, f"mu={mu}: TVD {tvd}"
        assert abs(p5 - core.P_HW5) < 1e-9
        assert abs(p[core.POS_IN_FEAS[core.exact_optimum(fs[mu])]] - ideal) < 5e-5
        assert 230 <= quantum.two_qubit_count(tqc) <= 240
        assert set(tqc.count_ops()) <= {"rz", "ry", "rx", "rzz", "x", "measure"}


def test_independent_choice_null(model):
    core, fs = model["core"], model["fs"]
    for mu, ref in zip(core.MU_GRID, NULL):
        p = core.qaoa_xy_probs(fs[mu])
        q = core.independent_choice(p)
        assert abs(q[core.POS_IN_FEAS[core.exact_optimum(fs[mu])]] - ref) < 5e-5


def test_closed_form_matches_simulation(model):
    core, fs = model["core"], model["fs"]
    targets = sorted({core.exact_optimum(fs[mu]) for mu in core.MU_GRID})
    ideal = [core.qaoa_xy_probs(fs[mu]) for mu in core.MU_GRID]
    null = [core.independent_choice(p) for p in ideal]
    unif = [np.full(1287, 1 / 1287)] * 5
    assert abs(core.closed_form_all_found(ideal, targets, 1000) - 0.985) < 0.005
    assert abs(core.closed_form_all_found(null, targets, 1000) - 0.627) < 0.005
    assert abs(core.closed_form_all_found(unif, targets, 1000) - 0.112) < 0.005
    assert core.closed_form_all_found(ideal, targets, 500) > core.closed_form_all_found(null, targets, 500)


def test_count_parsing():
    import ftp_quantum as quantum
    assert quantum.key_to_state("0000000101111") == (47, 0)
    assert quantum.key_to_state("0000 0001 01111") == (47, 0)
    assert quantum.key_to_state("0x2f") == (47, 0)
    assert quantum.key_to_state("1" + "0000000101111") == (47, 1)
    pc, total, extra = quantum.five_test_counts({"0000000101111": 3, "1111111111111": 2, "0x2f": 1})
    assert pc == {47: 4} and total == 6 and extra == 0

    class ListResult:
        def __init__(self, items):
            self.items = items

        def get_counts(self, key=None):
            if key is None:
                return self.items
            raise KeyError(key)

    r = ListResult([{"0000000101111": 5}, {"0000000001111": 7}])
    assert quantum.counts_for(r, "ftp_x", 1) == {"0000000001111": 7}


def _run_main(backend, **settings):
    import importlib.util
    import pathlib
    import sys
    project = pathlib.Path.cwd()
    sys.path.insert(0, str(project))
    spec = importlib.util.spec_from_file_location("main_under_test", project / "main.py")
    mod = importlib.util.module_from_spec(spec)
    mod.backend = backend
    spec.loader.exec_module(mod)
    mod.main(**settings)


class CountingSim:
    """BasicSimulator stand-in that counts run() calls; optionally raises like a rejected job."""

    def __init__(self, fail=False):
        from qiskit.providers.basic_provider import BasicSimulator
        self.inner, self.fail, self.calls, self.name = BasicSimulator(), fail, 0, "basic_simulator"
        self.options = self.inner.options

    def run(self, circuits, **kw):
        self.calls += 1
        if self.fail:
            raise RuntimeError("only one job is allowed per code run")
        return self.inner.run(circuits, **kw)


@pytest.mark.parametrize("circuits_mode", ["auto", "all", "single"])
def test_exactly_one_job(circuits_mode, capsys):
    be = CountingSim()
    _run_main(be, circuits=circuits_mode, shots=200, run_baselines=False)
    assert be.calls == 1
    out = capsys.readouterr().out
    assert "This effort is supported by Qollab & IonQ." in out and "JOB FAILED" not in out


def test_failed_job_shows_labelled_fallback(capsys):
    be = CountingSim(fail=True)
    _run_main(be, shots=200, run_baselines=False)
    assert be.calls == 1
    out = capsys.readouterr().out
    assert "JOB FAILED" in out and "NOT A RUN" in out


def test_basic_simulator_end_to_end_statistics(model):
    """20,000 seeded shots on the built-in simulator: P(five tests) and each P(opt | five tests) agree with theory."""
    import ftp_quantum as quantum
    from qiskit.providers.basic_provider import BasicSimulator
    core, fs = model["core"], model["fs"]
    circs = quantum.portable([quantum.sentinel_circuit()] +
                             [quantum.build_circuit(fs[mu], f"c{i}", core.GAMMA, core.BETA)[0]
                              for i, mu in enumerate(core.MU_GRID)], seed=7)
    S = 20000
    res = BasicSimulator().run(circs, shots=S, seed_simulator=11).result()
    res2 = BasicSimulator().run(circs, shots=S, seed_simulator=11).result()
    assert res.get_counts(3) == res2.get_counts(3)
    assert res.get_counts(0) == {"0000000101111": S}
    for i, mu in enumerate(core.MU_GRID):
        pc, total, _ = quantum.five_test_counts(res.get_counts(i + 1))
        n5 = sum(pc.values())
        sd = np.sqrt(S * core.P_HW5 * (1 - core.P_HW5))
        assert abs(n5 - S * core.P_HW5) < 4 * sd
        o = core.exact_optimum(fs[mu])
        lo, hi = core.wilson(pc.get(o, 0), n5, z=3.29)
        assert lo <= IDEAL[i] <= hi, f"mu={mu}: {pc.get(o, 0)}/{n5} outside 99.9% interval"
