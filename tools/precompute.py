"""Offline precompute for Five Tests, Priced. Writes five_tests_priced/results/precomputed.json.

Every number written here is either recomputed from the project's own code (five_tests_priced/ftp_*.py) or read
from the research results in research_notes/QCA prompts Quantum Impact plan/scripts/prompt_b/results/ (provenance
recorded) -- nothing is typed in by hand.

Steps (run any subset, in any order; each updates its own block):
  auc        2,379-panel cross-validated AUC table + constants mirror           (fast)
  baselines  SA / random-restart local search, pooled, 200 jobs, matched evals   (~1 min)
  penalty    penalty-QAOA vs XY-QAOA on THIS project's objective, p = 1..3        (~3 min)
  gates      two-qubit gates: all-to-all (IonQ) vs heavy-hex (IBM)               (fast)
  honestcv   honest nested-CV table (read from research s09/s05 results)         (fast)
  confirm2   pre-registered check 2: 50 fresh 80% subsamples, seed 20261010      (~1 min)
  confirm3   pre-registered check 3: the declared built-in run (seed 7, 1000)    (fast)
  noisy      noisy reference: Aer with IonQ forte-1 legacy depolarizing rates, 10,000 shots per circuit (~7 min)

Usage:  .venv/Scripts/python.exe tools/precompute.py auc baselines penalty gates honestcv confirm2 confirm3 noisy
"""
import datetime as dt
import json
import os
import pathlib
import platform
import sys
import time

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[1]
PROJECT = ROOT / "five_tests_priced"
RESEARCH = ROOT / "research_notes" / "QCA prompts Quantum Impact plan" / "scripts" / "prompt_b"
OUT = PROJECT / "results" / "precomputed.json"

sys.path.insert(0, str(PROJECT))
os.chdir(PROJECT)
import ftp_classical as classical  # noqa: E402
import ftp_core as core            # noqa: E402
import ftp_quantum as quantum      # noqa: E402

DISCRETE = np.array([f in {"sex", "cp", "fbs", "restecg", "exang", "slope", "ca", "thal"} for f in core.FEATURES])


def now():
    return dt.datetime.now().isoformat(timespec="seconds")


def versions():
    import qiskit
    import scipy
    import sklearn
    return {"python": platform.python_version(), "numpy": np.__version__, "scipy": scipy.__version__,
            "sklearn": sklearn.__version__, "qiskit": qiskit.__version__}


def model():
    X, y = core.load_data()
    C = core.redundancy(X)
    cost = core.cost_vector()
    fs = {mu: core.objective(core.R_K10, C, cost, mu) for mu in core.MU_GRID}
    return X, y, C, cost, fs


def relevance(X, y, seeds, k=10):
    from sklearn.feature_selection import mutual_info_classif
    return np.mean([mutual_info_classif(X, y, discrete_features=DISCRETE, n_neighbors=k, random_state=s)
                    for s in seeds], axis=0)


# ------------------------------------------------------------------------------------------------------- steps
def step_auc(doc):
    z = np.load(RESEARCH / "results" / "s05_all_subsets.npz")
    doc["auc_table"] = {
        "description": ("Cross-validated AUC of logistic regression (max_iter=2000, C=1; numeric tests standardised, "
                        "cp/restecg/slope/thal one-hot) on every panel of 1-5 tests; 5x3 repeated stratified CV, "
                        "random_state=7, all 297 patients. ftp_classical.cv_auc reproduces it exactly."),
        "source": "research_notes/QCA prompts Quantum Impact plan/scripts/prompt_b/results/s05_all_subsets.npz "
                  "(s05_downstream.py part C)",
        "states": [int(s) for s in z["states"]],
        "aucs": [round(float(a), 6) for a in z["aucs"]],
    }
    s07 = json.loads((RESEARCH / "results" / "s07_robustness.json").read_text())
    s10 = json.loads((RESEARCH / "results" / "s10_pareto_onejob.json").read_text())
    doc["constants_mirror"] = {"note": "Mirror of constants hard-coded in ftp_core.py (tests check they agree).",
                               "r_k10": s07["estimators"]["kNN-MI k=10"]["r"],
                               "gamma": s10["gamma"][0], "beta": s10["beta"][0]}


def step_baselines(doc):
    """Port of prompt_b/s10f_pooled_matched.py (same generator seed and call order), plus exact closed-form rows."""
    X, y, C, cost, fs = model()
    opts = {mu: core.exact_optimum(fs[mu]) for mu in core.MU_GRID}
    rng = np.random.default_rng(11)
    rows = {}
    for B in (22, 44, 111, 222):
        for name, fn in (("simulated annealing (T0=0.1)", lambda f: classical.sa_pool(f, B, rng)),
                         ("simulated annealing (T0=0.3)", lambda f: classical.sa_pool(f, B, rng, T0=0.3)),
                         ("random-restart local search", lambda f: classical.rrls_pool(f, B, rng))):
            found = []
            for _ in range(200):
                pool = set()
                for mu in core.MU_GRID:
                    pool |= fn(fs[mu])
                found.append(sum(opts[mu] in pool for mu in core.MU_GRID))
            found = np.array(found)
            rows.setdefault(name, {})[str(B)] = {"all_found_rate": float((found == 5).mean()),
                                                 "mean_found_of_5": float(found.mean())}
    targets = sorted(set(opts.values()))
    ideal = [core.qaoa_xy_probs(fs[mu]) for mu in core.MU_GRID]
    null = [core.independent_choice(p) for p in ideal]
    unif = [np.full(1287, 1 / 1287)] * 5
    exact = {}
    for S in (100, 200, 500, 1000):
        exact[str(S)] = {"ideal QAOA circuit": core.closed_form_all_found(ideal, targets, S),
                         "independent-choice": core.closed_form_all_found(null, targets, S),
                         "uniform five-test panels": core.closed_form_all_found(unif, targets, S)}
    doc.setdefault("evidence", {})["recovery"] = {
        "description": ("Chance that ONE job (5 circuits) finds all 4 distinct optimal panels. Quantum rows: exact "
                        "closed form at S raw shots per circuit (about 0.2228*S five-test samples each). Classical "
                        "rows: s10f protocol, 200 seeded repetitions, each method gets B evaluations per price "
                        "weight with every evaluated panel pooled; B = 22/44/111/222 matches S = 100/200/500/1000."),
        "shots_to_evals": {"100": 22, "200": 44, "500": 111, "1000": 222},
        "quantum_exact": exact,
        "classical_pooled_200_jobs": rows,
        "source": "port of research_notes/.../prompt_b/s10f_pooled_matched.py (rng seed 11, same call order)",
    }


def _xy_probs_p(f, gammas, betas, maps):
    ff = f[core.FEAS_IDX]
    e = (ff - ff.mean()) / ff.std()
    phi = np.full(1287, 1 / np.sqrt(1287), dtype=complex)
    for g, b in zip(gammas, betas):
        phi = phi * np.exp(-1j * g * e)
        c, s = np.cos(b), 1j * np.sin(b)
        for i10, i01 in maps:
            a, bb = phi[i10].copy(), phi[i01].copy()
            phi[i10], phi[i01] = c * a + s * bb, s * a + c * bb
    p = np.abs(phi) ** 2
    return p / p.sum()


def _x_probs_p(E, gammas, betas):
    e = (E - E.mean()) / E.std()
    n = core.N
    psi = np.full(2 ** n, 2 ** (-n / 2), dtype=complex)
    idx = np.arange(2 ** n)
    for g, b in zip(gammas, betas):
        psi = psi * np.exp(-1j * g * e)
        c, s = np.cos(b), 1j * np.sin(b)          # exp(+i b X): |+> is the ground state of -X (minimisation)
        for q in range(n):
            lo = idx[((idx >> q) & 1) == 0]
            hi = lo | (1 << q)
            a, bb = psi[lo].copy(), psi[hi].copy()
            psi[lo], psi[hi] = c * a + s * bb, s * a + c * bb
    return np.abs(psi) ** 2


def _tune(sim, score, p):
    """Energy-based tuning (no knowledge of the optimum): linear-ramp grid, then Nelder-Mead for all 2p angles."""
    from scipy.optimize import minimize
    best = None
    for dg in np.linspace(0.05, 3.0, 30):
        for db in np.linspace(-np.pi / 2, np.pi / 2, 25):
            gs = [(k + 1) / p * dg for k in range(p)]
            bs = [(1 - k / p) * db for k in range(p)]
            v = score(sim(gs, bs))
            if best is None or v < best[0]:
                best = (v, gs, bs)
    res = minimize(lambda x: score(sim(x[:p], x[p:])), np.array(best[1] + best[2]), method="Nelder-Mead",
                   options={"maxiter": 400 * p, "xatol": 1e-6, "fatol": 1e-10})
    if res.fun < best[0]:
        best = (res.fun, list(res.x[:p]), list(res.x[p:]))
    return best[1], best[2]


def step_penalty(doc):
    """The prompt's penalty formulation vs the XY mixer on THIS project's objective (mu = 0, k=10 MI, lambda=0.1)."""
    from qiskit_optimization import QuadraticProgram
    from qiskit_optimization.converters import LinearEqualityToPenalty
    X, y, C, cost, fs = model()
    f = fs[0.0]
    opt = core.exact_optimum(f)
    hw = core.HW
    # Qiskit's automatic penalty for exactly this QUBO + "choose 5" constraint
    qp = QuadraticProgram()
    for i in range(core.N):
        qp.binary_var(f"x{i}")
    qp.minimize(linear=list(-core.R_K10),
                quadratic={(f"x{i}", f"x{j}"): core.LAM * C[i, j] for i in range(core.N) for j in range(i + 1, core.N)})
    qp.linear_constraint(linear={f"x{i}": 1 for i in range(core.N)}, sense="==", rhs=core.K)
    conv = LinearEqualityToPenalty()
    conv.convert(qp)
    p_auto = float(conv.penalty)
    lo, hi = 0.0, 100.0           # smallest P making the true optimum the global minimum (needs the answer)
    for _ in range(60):
        mid = (lo + hi) / 2
        if (f + mid * (hw - core.K) ** 2)[hw != core.K].min() > f[opt]:
            hi = mid
        else:
            lo = mid
    p_min = hi
    p_bound = float(np.max(np.abs(core.R_K10) + core.LAM * C.sum(1)))   # textbook single-flip bound, no answer needed
    maps = core.pair_maps(core.complete_pairs())
    pos = core.POS_IN_FEAS[opt]
    rows = []
    ff = f[core.FEAS_IDX]
    for p in (1, 2, 3):
        g, b = _tune(lambda gs, bs: _xy_probs_p(f, gs, bs, maps), lambda pr: float(pr @ ff), p)
        pr = _xy_probs_p(f, g, b, maps)
        rows.append({"method": "XY mixer (always exactly five tests)", "P": None, "p": p,
                     "two_qubit_gates": 234 * p, "P_opt_given_five": float(pr[pos]),
                     "P_valid": core.P_HW5, "P_opt_per_raw_shot": float(core.P_HW5 * pr[pos])})
        for label, P in (("penalty, Qiskit's automatic value", p_auto),
                         ("penalty, textbook bound (no answer needed)", p_bound),
                         ("penalty, 2x smallest valid value (needs the answer)", 2 * p_min)):
            E = f + P * (hw - core.K) ** 2
            g, b = _tune(lambda gs, bs: _x_probs_p(E, gs, bs), lambda pr: float(pr @ E), p)
            pr = _x_probs_p(E, g, b)
            pv = float(pr[core.FEAS_IDX].sum())
            rows.append({"method": label, "P": P, "p": p, "two_qubit_gates": 78 * p,
                         "P_opt_given_five": float(pr[opt] / pv), "P_valid": pv, "P_opt_per_raw_shot": float(pr[opt])})
        print(f"  penalty step: p={p} done", flush=True)
    doc.setdefault("evidence", {})["penalty"] = {
        "description": ("Prompt B's penalty formulation (X mixer, P(sum x - 5)^2) vs the XY mixer, mu = 0, this "
                        "project's objective. Angles for every row tuned by minimising expected energy (no knowledge "
                        "of the optimum). Random five-test panel: 1/1287 = 0.00078."),
        "P_auto": p_auto, "P_bound": p_bound, "P_min": p_min, "rows": rows,
        "source": "tools/precompute.py step 'penalty' (re-implements research penalty_check/followup.py with "
                  "the project's discrete-mask relevance)",
    }


def step_gates(doc):
    from qiskit import transpile
    from qiskit.transpiler import CouplingMap
    X, y, C, cost, fs = model()
    logical = [quantum.build_circuit(fs[mu], f"c{i}", core.GAMMA, core.BETA)[0] for i, mu in enumerate(core.MU_GRID)]
    ionq = quantum.portable(logical, seed=7)
    a2a = transpile(logical, basis_gates=["rz", "sx", "x", "cz"], optimization_level=1, seed_transpiler=7)
    hh = transpile(logical, coupling_map=CouplingMap.from_heavy_hex(5), basis_gates=["rz", "sx", "x", "cz"],
                   optimization_level=1, seed_transpiler=7)
    doc.setdefault("evidence", {})["gates"] = {
        "description": ("Two-qubit gates per circuit. IonQ: native ZZ (one per RZZ), all-to-all connectivity. "
                        "IBM-style: CZ basis; without and with heavy-hex routing (57-qubit heavy-hex, d=5)."),
        "mu": core.MU_GRID,
        "ionq_native_zz": [int(c.count_ops().get("rzz", 0)) for c in ionq],
        "cz_all_to_all": [int(c.count_ops().get("cz", 0)) for c in a2a],
        "cz_heavy_hex": [int(c.count_ops().get("cz", 0)) for c in hh],
        "depth_ionq": [int(c.depth()) for c in ionq],
        "depth_heavy_hex": [int(c.depth()) for c in hh],
    }


def step_honestcv(doc):
    s09 = json.loads((RESEARCH / "results" / "s09_honest_cost_pipelines.json").read_text())
    s05 = json.loads((RESEARCH / "results" / "s05_downstream_AB.json").read_text())
    rows = [{"selection": f"cost-aware QUBO, mu={r['mu']}", "AUC": r["AUC"], "AUC_ci": r["AUC_ci"],
             "per_repeat_AUC": r["per_repeat_AUC"], "mean_cost": r["mean_cost"]}
            for r in s09 if r["kn"] == 10 and r["lam"] == 0.1]
    for key, label in (("SelectKBest_MI", "SelectKBest (mutual information), 5 tests"),
                       ("L1_logistic_5", "L1-logistic, 5 tests"), ("all_13", "all 13 tests")):
        r = s05["B"][key]
        rows.append({"selection": label, "AUC": r["AUC"], "AUC_ci": r["AUC_ci"],
                     "per_repeat_AUC": r["per_repeat_mean"][0], "mean_cost": None})
    doc.setdefault("evidence", {})["honest_cv"] = {
        "description": ("Honest nested evaluation: the panel is re-selected inside every outer training fold "
                        "(relevance re-estimated on training patients only), then scored on held-out patients; "
                        "5x5 repeated stratified outer folds. AUC = pooled out-of-fold, [95% bootstrap CI]."),
        "rows": rows,
        "source": "research_notes/.../prompt_b/results/s09_honest_cost_pipelines.json and s05_downstream_AB.json",
    }


def step_confirm2(doc):
    """Pre-registered check 2 (README, tag prereg): 50 fresh 80% subsamples, seed 20261010 (never used before)."""
    X, y, C, cost, fs = model()
    rng = np.random.default_rng(20261010)
    maps = core.pair_maps(core.complete_pairs())
    per = {mu: {"qaoa": [], "null": []} for mu in core.MU_GRID}
    t = time.time()
    for _ in range(50):
        s = rng.choice(len(y), int(0.8 * len(y)), replace=False)
        r = relevance(X[s], y[s], seeds=range(5))
        Cs = core.redundancy(X[s])
        for mu in core.MU_GRID:
            f = core.objective(r, Cs, cost, mu)
            p = core.qaoa_xy_probs(f, maps=maps)
            q = core.independent_choice(p)
            o = core.POS_IN_FEAS[core.exact_optimum(f)]
            per[mu]["qaoa"].append(float(p[o]))
            per[mu]["null"].append(float(q[o]))
    rows = []
    for mu in core.MU_GRID:
        a, b = np.array(per[mu]["qaoa"]), np.array(per[mu]["null"])
        rows.append({"mu": mu, "mean_qaoa": float(a.mean()), "mean_independent": float(b.mean()),
                     "ratio": float(a.mean() / b.mean()), "subsamples_qaoa_higher": int((a > b).sum())})
    doc.setdefault("evidence", {})["confirm2"] = {
        "claim": "On 50 fresh 80% subsamples (seed 20261010), mean ideal QAOA P(optimum | five tests) exceeds the "
                 "independent-choice sampler at every price weight.",
        "rows": rows, "passed": all(r["mean_qaoa"] > r["mean_independent"] for r in rows),
        "protocol": "relevance re-estimated per subsample (kNN MI k=10, 5 seeds, discrete mask); frozen angles",
        "seconds": round(time.time() - t, 1),
    }


def step_confirm3(doc):
    """Pre-registered check 3: the declared run = built-in simulator, seed 7, default 1000 shots per circuit."""
    from qiskit.providers.basic_provider import BasicSimulator
    X, y, C, cost, fs = model()
    auc = dict(zip(doc["auc_table"]["states"], doc["auc_table"]["aucs"]))
    logical = [quantum.build_circuit(fs[mu], f"ftp_mu{str(mu).replace('.', 'p')}", core.GAMMA, core.BETA)[0]
               for mu in core.MU_GRID]
    circs = quantum.portable([quantum.sentinel_circuit()] + logical, 7)
    res = BasicSimulator().run(circs, shots=1000, seed_simulator=7).result()
    five = [s for s in auc if bin(s).count("1") == 5]
    rows = []
    for j, mu in enumerate(core.MU_GRID):
        pc, total, _ = quantum.five_test_counts(quantum.counts_for(res, logical[j].name, j + 1))
        best = min(pc, key=lambda s: fs[mu][s])
        cheaper = [auc[s] for s in five if cost[s] <= cost[best] + 1e-9]
        gap = max(cheaper) - auc[best]
        rows.append({"mu": mu, "best_sampled": core.state_to_names(best), "cost": float(cost[best]),
                     "auc": auc[best], "best_auc_at_or_below_cost": max(cheaper), "gap": round(gap, 6),
                     "is_exact_optimum": best == core.exact_optimum(fs[mu])})
    doc.setdefault("evidence", {})["confirm3"] = {
        "claim": "For each price weight, the best sampled panel's CV AUC lies within 0.005 of the best AUC of any "
                 "five-test panel costing no more than it (declared run: built-in simulator, seed 7, 1000 shots).",
        "rows": rows, "passed": all(r["gap"] <= 0.005 for r in rows),
    }


def step_noisy(doc, shots=10000):
    from qiskit_aer import AerSimulator
    from qiskit_aer.noise import NoiseModel, depolarizing_error
    X, y, C, cost, fs = model()
    logical = [quantum.build_circuit(fs[mu], f"c{i}", core.GAMMA, core.BETA)[0] for i, mu in enumerate(core.MU_GRID)]
    circs = quantum.portable(logical, seed=7)
    nm = NoiseModel()
    nm.add_all_qubit_quantum_error(depolarizing_error(2.67e-4, 1), ["rx", "ry", "rz", "x"])
    nm.add_all_qubit_quantum_error(depolarizing_error(4.95e-3, 2), ["rzz"])
    t = time.time()
    res = AerSimulator(noise_model=nm, seed_simulator=17).run(circs, shots=shots).result()
    secs = time.time() - t
    counts, phw5 = {}, []
    for j, mu in enumerate(core.MU_GRID):
        pc, total, _ = quantum.five_test_counts(res.get_counts(j))
        counts[str(mu)] = {str(k): v for k, v in sorted(pc.items())}
        phw5.append(sum(pc.values()) / total)
    opts = {mu: core.exact_optimum(fs[mu]) for mu in core.MU_GRID}
    targets = sorted(set(opts.values()))
    dists = []
    for mu in core.MU_GRID:
        v = quantum.as_vector({int(k): c for k, c in counts[str(mu)].items()})
        dists.append(v / v.sum())
    doc.setdefault("evidence", {})["noisy"] = {
        "description": ("Noisy reference: Aer with IonQ's documented legacy forte-1 depolarizing rates (1-qubit "
                        "2.67e-4 on rx/ry/rz/x, 2-qubit 4.95e-3 on rzz), the exact submitted circuits, "
                        f"{shots} shots per circuit, seed 17. Not IonQ hardware and not IonQ's current noise model."),
        "shots": shots, "seconds": round(secs, 1), "P_five_tests": phw5,
        "P_opt_given_five": [float(dists[j][core.POS_IN_FEAS[opts[mu]]]) for j, mu in enumerate(core.MU_GRID)],
        "closed_form_all_found": {str(S): core.closed_form_all_found(dists, targets, S, phw5)
                                  for S in (100, 200, 500, 1000)},
        "five_test_counts": counts,
    }


STEPS = {"auc": step_auc, "baselines": step_baselines, "penalty": step_penalty, "gates": step_gates,
         "honestcv": step_honestcv, "confirm2": step_confirm2, "confirm3": step_confirm3, "noisy": step_noisy}


TOP_KEYS = {"auc": ["auc_table", "constants_mirror"]}
EVIDENCE_KEY = {"baselines": "recovery", "penalty": "penalty", "gates": "gates", "honestcv": "honest_cv",
                "confirm2": "confirm2", "confirm3": "confirm3", "noisy": "noisy"}


def _load():
    return json.loads(OUT.read_text(encoding="utf-8")) if OUT.exists() else {}


def main():
    names = sys.argv[1:] or ["auc"]
    for n in names:
        t = time.time()
        print(f"step {n} ...", flush=True)
        doc = _load()
        STEPS[n](doc)
        fresh = _load()          # merge only this step's output, so steps can run in separate processes
        for k in TOP_KEYS.get(n, []):
            fresh[k] = doc[k]
        if n in EVIDENCE_KEY:
            fresh.setdefault("evidence", {})[EVIDENCE_KEY[n]] = doc["evidence"][EVIDENCE_KEY[n]]
        fresh.setdefault("provenance", {})[n] = {"created": now(), "seconds": round(time.time() - t, 1),
                                                 "versions": versions()}
        OUT.write_text(json.dumps(fresh, separators=(",", ":")), encoding="utf-8")
        print(f"step {n} done in {time.time() - t:.1f}s; wrote {OUT.stat().st_size / 1024:.1f} KB", flush=True)


if __name__ == "__main__":
    main()
