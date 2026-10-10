"""Five Tests, Priced -- choose a 5-test heart-disease panel at five price points with ONE 13-qubit QAOA job.

QCA Georgia Tech Qiskit Fall Fest 2026, Prompt B ("Heart Disease Readings"), theme Quantum Impact.
This effort is supported by Qollab & IonQ.

Press Run. The runtime calls main() with the settings below and passes in the simulator you picked as `backend`.
Defaults are chosen per backend; on IonQ the whole run is exactly ONE job.
  shots          0 = automatic (built-in 1000 per circuit, IonQ 500, IBM noise models 8)
  circuits       "auto", "all" (5 price points + bit-order check in one job) or "single" (one price point)
  single_mu      price weight used when circuits = "single"
  seed           seed for the simulator and the classical baselines
  run_baselines  also run simulated annealing / local search with the same number of evaluations
  revalidate_auc recompute cross-validated AUCs live with scikit-learn (slower; precomputed values are shown anyway)
  show_figures   draw the price-ladder figure
  dump_counts    print the raw five-test counts as one line of JSON (for archiving a run)
"""
import sys

for _name in [m for m in list(sys.modules) if m.startswith("ftp_")]:
    del sys.modules[_name]   # always use the files just uploaded, even if the interpreter is reused between Runs

import builtins
import json
import time

import numpy as np

import ftp_classical as classical
import ftp_core as core
import ftp_quantum as quantum
import ftp_report as rep

BUILD = "v1.1 2026-10-10"
ATTRIBUTION = "This effort is supported by Qollab & IonQ."


def _injected_backend():
    be = globals().get("backend")
    return be if be is not None else getattr(builtins, "backend", None)


def _load_json(which):
    try:
        if which == "precomputed":
            with open("results/precomputed.json") as fh:
                return json.load(fh)
        with open("results/forte_cache.json") as fh:
            return json.load(fh)
    except Exception as e:  # noqa: BLE001
        print(f"  (could not read results/{which}.json: {type(e).__name__})")
        return None


def _print_evidence(pre, show_figures):
    """Section 5: the evidence that cannot be recomputed in a few seconds, read from results/precomputed.json."""
    ev = pre.get("evidence", {})
    if not ev:
        return
    prov = pre.get("provenance", {})
    rep.section("5. Precomputed evidence (offline runs; file results/precomputed.json)")

    rec = ev.get("recovery")
    if rec:
        cols = ["100", "200", "500", "1000"]
        rows = [[name] + [rep.pct(rec["quantum_exact"][c][name]) for c in cols]
                for name in ("ideal QAOA circuit", "independent-choice", "uniform five-test panels")]
        noisy = ev.get("noisy")
        if noisy:
            rows.insert(1, ["QAOA circuit, IonQ forte-1-rate noise"] +
                        [rep.pct(noisy["closed_form_all_found"][c]) for c in cols])
        for name, d in rec["classical_pooled_200_jobs"].items():
            rows.append([name] + [rep.pct(d[str(rec["shots_to_evals"][c])]["all_found_rate"]) for c in cols])
        rep.table(["method", "100 shots (22 evals)", "200 (44)", "500 (111)", "1000 (222)"], rows,
                  note="chance ONE job finds all 4 optimal panels. Quantum rows: exact formula (noisy row from a "
                       "10,000-shot noisy reference); classical rows: 200 seeded jobs with the same number of "
                       f"evaluated panels per price weight [precomputed {prov.get('baselines', {}).get('created', '?')}]")

    pen = ev.get("penalty")
    if pen:
        rows = [[r["method"], r["p"], r["two_qubit_gates"], f"{r['P_opt_given_five']:.4f}",
                 f"{r['P_opt_per_raw_shot']:.5f}"] for r in pen["rows"]]
        rep.table(["formulation (mu = 0)", "layers p", "2-qubit gates", "P(optimum | 5 tests)",
                   "P(optimum) per raw shot"], rows,
                  note=f"QCA's penalty term vs the XY mixer, all angles tuned without knowing the answer. Penalty "
                       f"values: Qiskit automatic {pen['P_auto']:.3f}, textbook bound {pen['P_bound']:.3f}, "
                       f"smallest valid {pen['P_min']:.4f} (finding it requires solving the problem). "
                       f"Random 5-test panel: 0.00078.")

    hc = ev.get("honest_cv")
    if hc:
        rows = [[r["selection"], f"{r['AUC']:.3f} [{r['AUC_ci'][0]:.3f}, {r['AUC_ci'][1]:.3f}]",
                 f"{r['per_repeat_AUC']:.3f}", rep.money(r["mean_cost"]) if r["mean_cost"] else "n/a"]
                for r in hc["rows"]]
        rep.table(["panel chosen inside each training fold by", "held-out AUC [95% CI]", "per-repeat AUC",
                   "mean panel price"], rows,
                  note="honest numbers: the panel is re-selected on training patients only, then scored on unseen "
                       "patients (lower than the optimistic price ladder in section 2)")

    gt = ev.get("gates")
    if gt:
        rows = [[mu, a, b, c] for mu, a, b, c in zip(gt["mu"], gt["ionq_native_zz"], gt["cz_all_to_all"],
                                                    gt["cz_heavy_hex"])]
        rep.table(["mu", "IonQ native ZZ (all-to-all)", "IBM CZ, all-to-all", "IBM CZ, heavy-hex routed"], rows,
                  note="the same circuit on trapped ions vs a superconducting heavy-hex lattice")

    for key, title in (("confirm2", "pre-registered check 2"), ("confirm3", "pre-registered check 3")):
        c = ev.get(key)
        if not c:
            continue
        print(f"  {title}: {'PASSED' if c['passed'] else 'NOT PASSED'} -- {c['claim']}")
        if key == "confirm2":
            for r in c["rows"]:
                print(f"    mu={r['mu']}: QAOA {r['mean_qaoa']:.4f} vs independent-choice {r['mean_independent']:.4f} "
                      f"({r['ratio']:.2f}x; QAOA higher in {r['subsamples_qaoa_higher']} of 50 subsamples)")
        else:
            for r in c["rows"]:
                print(f"    mu={r['mu']}: best sampled panel ${r['cost']:.2f} AUC {r['auc']:.3f}; best possible "
                      f"at that price {r['best_auc_at_or_below_cost']:.3f} (gap {r['gap']:.3f})")
        print()


def main(shots: int = 0, circuits: str = "auto", single_mu: float = 0.2, seed: int = 7, run_baselines: bool = True, revalidate_auc: bool = False, show_figures: bool = True, dump_counts: bool = False):
    t_start = time.time()
    print(f"Five Tests, Priced   [build {BUILD}]")
    print(ATTRIBUTION)
    print("Theme: Quantum Impact. QCA Prompt B: pick 5 of 13 heart-disease measurements, now with real prices.\n")

    # ------------------------------------------------------------------------------------------------ 1. data
    X, y = core.load_data()
    C = core.redundancy(X)
    cost = core.cost_vector()
    worst = max(abs(cost[s] - core.panel_cost(s)) for s in range(2 ** core.N))
    pre = _load_json("precomputed") or {}
    auc = dict(zip(pre.get("auc_table", {}).get("states", []), pre.get("auc_table", {}).get("aucs", [])))

    rep.section("1. The decision")
    print(f"  {len(y)} Cleveland chest-pain patients ({int(y.sum())} with heart disease), 13 possible measurements.")
    print("  The clinic can collect only 5. Tests have real prices (Turney 1995, Ontario fee schedule 1992, CAD),")
    print("  and some share one procedure: pay for the procedure once, the extra readings are almost free.")
    sh = core.shared_costs()
    rep.table(["shared procedure", "tests", "paid once"],
              [[g, ", ".join(core.GROUPS[g]), rep.money(sh[g])] for g in core.GROUPS],
              note=f"price self-test: polynomial vs table on all 8,192 subsets, max difference {worst:.1e}")

    # ------------------------------------------------------------------------------------------------ 2. classical
    fs = {mu: core.objective(core.R_K10, C, cost, mu) for mu in core.MU_GRID}
    opts = {mu: core.exact_optimum(fs[mu]) for mu in core.MU_GRID}
    rep.section("2. Classical first: exhaustive search is exact and instant at 13 tests")
    t = time.time()
    rows, greedy_fails = [], 0
    for mu in core.MU_GRID:
        f, o = fs[mu], opts[mu]
        g, _ = classical.greedy(f)
        ls, _ = classical.local_search(f, g)
        greedy_fails += g != o
        rows.append([mu, rep.panel(core.state_to_names(o)), rep.money(cost[o]),
                     f"{auc[o]:.3f}" if o in auc else "?",
                     "optimal" if g == o else f"rank {core.rank_of(f, g)} of 1287",
                     "optimal" if ls == o else f"rank {core.rank_of(f, ls)}"])
    rep.table(["price weight mu", "exact best 5-test panel", "price", "CV AUC", "greedy", "greedy + 1-swap"], rows,
              note=f"exhaustive search over all 1,287 panels x 5 price weights took {time.time() - t:.2f}s; "
                   f"greedy misses the optimum at {greedy_fails} of 5 price weights")
    if auc:
        front = core.auc_front(auc, cost)
        rep.table(["price", "panel (cheapest way to reach this AUC)", "CV AUC"],
                  [[rep.money(cost[s]), rep.panel(core.state_to_names(s), 70), f"{auc[s]:.3f}"] for s in front],
                  note="[precomputed] cost-vs-accuracy front of all 1,287 five-test panels "
                       "(logistic regression, 5x3 CV, all 297 patients; optimistic: best of many)")
        if show_figures:
            rep.describe("a staircase of the best cross-validated AUC reachable at each panel price, from $9.20 "
                         "(AUC 0.838) to $293.10 (AUC 0.911); diamonds mark the exact optimum at each price weight. "
                         "The numbers are the table above.")
            try:
                short = {s: f"${cost[s]:.0f}: {core.procedures(s)}" for s in front}
                rep.price_ladder_figure([(cost[s], auc[s], short[s]) for s in front],
                                        [(cost[o], auc[o], f"mu={mu}") for mu, o in opts.items() if o in auc])
            except Exception as e:  # noqa: BLE001
                print(f"  (figure unavailable: {type(e).__name__}: {e})")
    if revalidate_auc:
        t = time.time()
        rows = []
        for o in sorted(set(opts.values()), key=lambda s: cost[s]):
            live = classical.cv_auc(X, y, o)
            rows.append([rep.panel(core.state_to_names(o)), rep.money(cost[o]), f"{live:.4f}",
                         f"{auc.get(o, float('nan')):.4f}"])
        rep.table(["optimal panel", "price", "CV AUC recomputed now", "precomputed"], rows,
                  note=f"[live] scikit-learn logistic regression, 5x3 repeated stratified CV, random_state=7 "
                       f"({time.time() - t:.1f}s)")

    # ------------------------------------------------------------------------------------------------ 3. quantum
    rep.section("3. The quantum step: one job, 13 qubits, exactly five tests in every sample")
    be = _injected_backend()
    if be is None:
        print("  No backend was injected (are you running outside Qollab?). Stopping here.")
        return
    kind, desc = quantum.classify_backend(be)
    print(f"  backend: {desc}  ->  treated as '{kind}'")
    mode = circuits.strip().lower()
    if mode not in ("auto", "all", "single"):
        print(f"  unknown circuits={circuits!r}; using auto")
        mode = "auto"
    if mode == "auto":
        mode = "all" if quantum.LIST_JOBS_OK.get(kind, True) else "single"
    mus = core.MU_GRID if mode == "all" else [min(core.MU_GRID, key=lambda m: abs(m - single_mu))]
    if mode == "single":
        why = ("IonQ through Qollab accepts one circuit per job" if kind == "ionq" and circuits.strip().lower() == "auto"
               else "circuits = single")
        print(f"  single-circuit mode ({why}): this run uses one price weight, mu = {mus[0]}. "
              f"Run on the built-in simulator to see all five in one job.")
    S = int(shots) if shots > 0 else quantum.SHOT_POLICY.get(kind, 100)

    t = time.time()
    logical = [quantum.build_circuit(fs[mu], f"ftp_mu{str(mu).replace('.', 'p')}", core.GAMMA, core.BETA)[0]
               for mu in mus]
    circs = quantum.portable(([quantum.sentinel_circuit()] if mode == "all" else []) + logical, seed)
    probe = circs[-1]
    p_ideal = {mu: core.qaoa_xy_probs(fs[mu]) for mu in mus}
    p_null = {mu: core.independent_choice(p_ideal[mu]) for mu in mus}
    tvd, p5 = quantum.submitted_vs_reference_tvd(probe, p_ideal[mus[-1]])
    twoq = [quantum.two_qubit_count(c) for c in circs if c.name != "ftp_sentinel"]
    print(f"  built {len(circs)} circuit(s) in {time.time() - t:.1f}s; two-qubit gates (RZZ) per circuit: {twoq}")
    print(f"  check: submitted circuit vs exact NumPy model, total-variation distance {tvd:.1e} "
          f"(P(five tests) = {p5:.4f}, expected {core.P_HW5:.4f})")
    if tvd > 1e-6:
        print("  WARNING: the circuit does not match the model (gate convention changed?). Results below are suspect.")
    if quantum.needs_routing(be, kind):
        from qiskit import transpile
        t = time.time()
        circs = transpile(circs, backend=be, optimization_level=1, seed_transpiler=seed)
        routed = [quantum.two_qubit_count(c) for c in circs if c.name != "ftp_sentinel"]
        active = max(len({circ.find_bit(q).index for inst in circ.data for q in inst.qubits}) for circ in circs)
        print(f"  routed to this device's coupling map in {time.time() - t:.1f}s: {routed} two-qubit gates per circuit "
              f"(at most {active} physical qubits touched)")
        print(f"  (all-to-all trapped ions need {twoq}: the same circuit costs "
              f"{np.mean(routed) / np.mean(twoq):.1f}x more two-qubit gates on this lattice)")
    if kind in ("ibm_fake", "aer_noise"):
        print(f"  note: this simulator applies noise shot by shot in your browser, so the default is {S} shots per "
              f"circuit (set 'shots' to change it); expect up to a minute or two.")
    elif kind == "ionq":
        print("  note: IonQ's cloud simulator runs once per shot; with queueing this can take a few minutes.")

    targets = sorted({core.exact_optimum(fs[mu]) for mu in mus})
    dists_ideal = [p_ideal[mu] for mu in mus]
    dists_null = [p_null[mu] for mu in mus]
    unif = [np.full(len(core.FEAS_IDX), 1 / len(core.FEAS_IDX)) for _ in mus]
    grid = sorted({100, 200, 500, 1000, S})
    rep.table(["sampler (same shots)"] + [f"{s} shots" + (" <- this run" if s == S else "") for s in grid],
              [[name] + [rep.pct(core.closed_form_all_found(d, targets, s)) for s in grid]
               for name, d in (("ideal QAOA circuit", dists_ideal), ("independent-choice", dists_null),
                               ("uniform 5-test panels", unif))],
              note=f"PREDICTION, computed before the job: chance that one job samples all {len(targets)} distinct "
                   f"optimal panel(s) at least once (exact formula; noise lowers the QAOA row)")
    if show_figures:
        sgrid = [25, 50, 100, 200, 300, 500, 750, 1000, 1500, 2000]
        rep.describe("three curves of the chance that one job finds every optimal panel versus shots per circuit "
                     "(log scale). The ideal circuit rises fastest (about 83% at 500 shots, 98% at 1,000), the "
                     "independent-choice sampler slower (26%, 63%), uniform panels slowest (2%, 11%). "
                     "The numbers are the table above.")
        try:
            rep.recovery_figure(sgrid, {
                "ideal QAOA circuit": [core.closed_form_all_found(dists_ideal, targets, s) for s in sgrid],
                "independent-choice (no correlations)": [core.closed_form_all_found(dists_null, targets, s)
                                                         for s in sgrid],
                "uniform five-test panels": [core.closed_form_all_found(unif, targets, s) for s in sgrid]},
                this_run=S)
        except Exception as e:  # noqa: BLE001
            print(f"  (figure unavailable: {type(e).__name__}: {e})")

    guard = quantum.OneJobGuard()
    label = f"[live run on {kind}, {S} shots per circuit]"
    result, elapsed, failed = None, 0.0, None
    print(f"  submitting ONE job: {len(circs)} circuit(s) x {S} shots ...", flush=True)
    try:
        result, elapsed = quantum.submit_once(be, circs if len(circs) > 1 else circs[0], S, guard, seed, kind)
        print(f"  job finished in {elapsed:.1f}s")
    except Exception as e:  # noqa: BLE001
        failed = f"{type(e).__name__}: {e}"
        print(f"  JOB FAILED: {failed}")
        if mode == "all":
            print("  hint: re-run with circuits = \"single\" (one circuit per job).")

    per_mu = {}
    if result is not None:
        if mode == "all":
            cnt = quantum.counts_for(result, "ftp_sentinel", 0)
            sent = {}
            for k, v in cnt.items():
                s_ = quantum.key_to_state(k)[0]
                sent[s_] = sent.get(s_, 0) + v
            frac = sent.get(quantum.SENTINEL_STATE, 0) / max(sum(sent.values()), 1)
            print(f"  bit-order check: {rep.yesno(frac >= 0.5)} ({rep.pct(frac)} of shots read the expected panel "
                  f"age, sex, cp, trestbps, fbs; readout noise explains the rest)")
        if kind == "ionq":
            print("  note: IonQ's noise-model simulator returns rounded expected counts (round(probability x shots)),")
            print("        not random samples, so panels rarer than about 1 in 2x(shots) do not appear at all.")
        for j, mu in enumerate(mus):
            idx = j + (1 if mode == "all" else 0)
            pc, total, extra = quantum.five_test_counts(quantum.counts_for(result, logical[j].name, idx))
            per_mu[mu] = (pc, total)
    else:
        cache = _load_json("forte_cache") if kind == "ionq" else None
        if cache and all(str(mu) in cache.get("counts", {}) for mu in mus):
            label = f"[cached IonQ run: {cache.get('backend', '?')}, {cache.get('date', '?')}, NOT this press]"
            for mu in mus:
                pc = {int(k): int(v) for k, v in cache["counts"][str(mu)].items()}
                per_mu[mu] = (pc, int(cache.get("shots", sum(pc.values()))))
        else:
            label = "[NOT A RUN: samples drawn from the exact ideal distribution so the tables below can be read]"
            rng = np.random.default_rng(seed)
            for mu in mus:
                n5 = int(rng.binomial(S, core.P_HW5))
                draws = rng.choice(len(core.FEAS_IDX), n5, p=p_ideal[mu])
                pc = {}
                for d in draws:
                    s = int(core.FEAS_IDX[d])
                    pc[s] = pc.get(s, 0) + 1
                per_mu[mu] = (pc, S)

    # ------------------------------------------------------------------------------------------------ 4. results
    rep.section("4. What the samples show " + label)
    rows, pooled = [], set()
    for mu in mus:
        pc, total = per_mu[mu]
        vec = quantum.as_vector(pc)
        n5 = int(vec.sum())
        o = opts[mu]
        hits = pc.get(o, 0)
        lo, hi = core.wilson(hits, n5)
        best = min(pc, key=lambda s: fs[mu][s]) if pc else None
        pooled |= set(pc)
        pos = core.POS_IN_FEAS[o]
        rows.append([mu, f"{n5} of {total}", f"{hits / n5 if n5 else 0:.4f} [{lo:.4f}, {hi:.4f}]",
                     f"{p_ideal[mu][pos]:.4f}", f"{p_null[mu][pos]:.4f}", f"{1 / 1287:.4f}",
                     rep.yesno(best == o)])
    rep.table(["mu", "five-test shots", "P(optimal panel) observed [95% CI]", "ideal circuit",
               "independent-choice", "uniform", "best sample = optimum?"], rows,
              note="independent-choice = same per-test odds as the circuit, tests drawn independently "
                   "(isolates what correlations between qubits add)")
    found = [t_ for t_ in targets if t_ in pooled]
    print(f"  pooled over the job: {len(found)} of {len(targets)} distinct optimal panels sampled")
    for t_ in targets:
        print(f"    {rep.yesno(t_ in pooled):3s}  {rep.money(cost[t_]):>8s}  {', '.join(core.state_to_names(t_))}")
    print()

    llr_rows = []
    for mu in mus:
        vec = quantum.as_vector(per_mu[mu][0])
        if vec.sum() < 5:
            llr_rows.append([mu, "too few five-test shots", "", "", ""])
            continue
        obs, (mi, si), (mn, sn), n = core.llr_stats(vec, p_ideal[mu], p_null[mu])
        closer = "ideal circuit" if abs(obs - mi) / max(si, 1e-9) < abs(obs - mn) / max(sn, 1e-9) else "independent-choice"
        llr_rows.append([mu, f"{obs:+.1f}", f"{mi:+.1f} +- {si:.1f}", f"{mn:+.1f} +- {sn:.1f}", closer])
    rep.table(["mu", "log-likelihood ratio (ideal vs independent)", "expected if ideal", "expected if independent",
               "samples look like"], llr_rows,
              note="a per-run test that the samples carry the circuit's correlations, not just its per-test odds")

    if run_baselines and pooled:
        rng = np.random.default_rng(seed)
        sa_pool, ls_pool = set(), set()
        for mu in mus:
            n5 = int(quantum.as_vector(per_mu[mu][0]).sum())
            if n5 > 0:
                sa_pool |= classical.sa_pool(fs[mu], n5, rng)
                ls_pool |= classical.rrls_pool(fs[mu], n5, rng)
        rep.table(["method (same number of evaluated panels per price weight)", "distinct optima found"],
                  [["QAOA job (this run)", f"{len(found)} of {len(targets)}"],
                   ["simulated annealing (one seeded run)", f"{sum(t_ in sa_pool for t_ in targets)} of {len(targets)}"],
                   ["random-restart local search (one seeded run)",
                    f"{sum(t_ in ls_pool for t_ in targets)} of {len(targets)}"]],
                  note="classical evaluations are microsecond function calls: this compares sample quality, not speed")

    _print_evidence(pre, show_figures)

    rep.section("6. What this does not claim")
    print("  * No advantage over exhaustive search: at 13 tests it is exact and takes milliseconds (section 2).")
    print("  * No speedup. The quantum job is compared on sample quality at equal numbers of samples.")
    print("  * Prices are 1992 Ontario fees, used as relative costs; patients are a referral cohort, not screening.")
    print("  * The AUC front is the best of 1,287 panels on all patients (optimistic); re-selecting the panel")
    print("    inside each cross-validation fold gives lower, honest numbers (project page, 'Results').")

    if dump_counts and per_mu:
        print("\nCOUNTS_JSON " + json.dumps({"build": BUILD, "backend": desc, "shots": S, "label": label,
                                             "counts": {str(mu): {str(k): v for k, v in per_mu[mu][0].items()}
                                                        for mu in mus}}, separators=(",", ":")))
    print(f"\nDone in {time.time() - t_start:.1f}s. {ATTRIBUTION}")
