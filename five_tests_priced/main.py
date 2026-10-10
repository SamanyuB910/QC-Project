"""Five Tests, Priced: which five heart tests should a clinic order, and what does each extra dollar buy?

QCA Georgia Tech Qiskit Fall Fest 2026, Prompt B ("Heart Disease Readings"), theme Quantum Impact.
This effort is supported by Qollab & IonQ.

THE PROBLEM
  A chest-pain clinic can collect only 5 of 13 measurements per patient. Each measurement has a real price, and
  some share one procedure (one treadmill ECG gives three readings). For five price weights mu, from "ignore
  price" (mu = 0) to "price matters a lot" (mu = 0.2), we want the five-test panel with the best score:
  informative, not redundant, and cheap. There are only 1,287 possible panels, so the program checks them all;
  that exact answer is what every quantum result is graded against.

THE QUANTUM PART
  Each test is a qubit (1 = order the test). One QAOA circuit per price weight makes good panels more likely to
  be measured. Its mixer only ever swaps a test in for a test out, so every measured panel with five tests is a
  valid answer. All circuits go to the simulator in ONE job (IonQ's rule; on IonQ, Qollab accepts one circuit).

HOW TO READ THIS FILE
  main() just below is the table of contents. Each step is one function and one section of the printed report:
    step_1_the_decision            the patients, the decision, and the test prices
    step_2_classical_first         the exact answer by checking every panel, and how greedy shortcuts do
    step_3_build_circuits          build the circuits and check them against an exact model
    step_3_predict                 print, BEFORE the job, what an ideal circuit should achieve
    step_3_run_the_job             send the one job and read back the measured panels
    step_4_results                 compare the samples with the exact answer and with classical methods
    step_5_precomputed_evidence    offline results (too slow for a Run), from results/precomputed.json
    step_6_what_this_does_not_claim

THE OTHER FILES
  ftp_core.py       data, prices, the objective, exact search, an exact NumPy model of the circuit, statistics
  ftp_quantum.py    builds the Qiskit circuits, sends the one job, reads the measured counts
  ftp_classical.py  classical comparison methods (greedy, local search, simulated annealing) and accuracy (AUC)
  ftp_report.py     printing helpers: section titles, tables, accessible figures

RUN SETTINGS (Qollab shows these as a form; the runtime calls main() with them)
  shots          0 = automatic (built-in and IonQ 1000 per circuit, IBM noise models 8)
  circuits       "auto", "all" (5 price points + bit-order check in one job), "single" (one price point; what
                 IonQ through Qollab gets) or "probe" (a short test of how the simulator reads gate angles)
  single_mu      price weight used when circuits = "single"
  seed           seed for the simulator and the classical baselines
  run_baselines  also run simulated annealing / local search with the same number of evaluations
  revalidate_auc recompute cross-validated AUCs live with scikit-learn (slower; precomputed values are shown anyway)
  show_figures   draw the figures (each also has a text description and a table)
  dump_counts    print the raw five-test counts as one line of JSON (for archiving a run)

A NOTE ON PANELS
  A panel is stored as a 13-bit integer: bit i = 1 means test i is in it (see ftp_core.py). Measured bitstrings
  from the circuit read directly as panel numbers.
"""
import sys

# Qollab may reuse one Python interpreter for several Run presses. Forget project modules imported by an earlier
# Run, so this Run always uses the files that were just uploaded.
for _module_name in [m for m in list(sys.modules) if m.startswith("ftp_")]:
    del sys.modules[_module_name]

import builtins
import json
import time

import numpy as np

import ftp_classical as classical   # classical comparison methods and accuracy (AUC)
import ftp_core as core             # data, prices, objective, exact search, exact circuit model, statistics
import ftp_quantum as quantum       # Qiskit circuits, the one job, reading counts
import ftp_report as rep            # section titles, tables, figures

BUILD = "v1.5 2026-10-10"
ATTRIBUTION = "This effort is supported by Qollab & IonQ."


# =================================================================================================================
# main(): the table of contents. Qollab calls it when you press Run, passing the values of the Run settings form.
# Qollab only recognises main() if its signature stays on ONE line with simple types, so it is left long.
# =================================================================================================================
def main(shots: int = 0, circuits: str = "auto", single_mu: float = 0.2, seed: int = 7, run_baselines: bool = True, revalidate_auc: bool = False, show_figures: bool = True, dump_counts: bool = False):
    run_started = time.time()
    print(f"Five Tests, Priced   [build {BUILD}]")
    print(ATTRIBUTION)
    print("Theme: Quantum Impact. QCA Prompt B: pick 5 of 13 heart-disease measurements, now with real prices.\n")

    # Load the problem, and the offline results that ship with the project.
    problem = Problem()
    precomputed = load_project_json("precomputed") or {}
    auc = auc_lookup(precomputed)

    # Sections 1-2: the clinic's decision, then the exact answer found by checking every panel.
    step_1_the_decision(problem)
    step_2_classical_first(problem, auc, show_figures, revalidate_auc)

    # Section 3: the quantum step. First: which simulator did Qollab give us, and what should we send it?
    rep.section("3. The quantum step: one job, 13 qubits, exactly five tests in every sample")
    backend = injected_backend()
    if backend is None:
        print("  No backend was injected (are you running outside Qollab?). Stopping here.")
        return
    kind, backend_description = quantum.classify_backend(backend)
    print(f"  backend: {backend_description}  ->  treated as '{kind}'")

    mode = choose_circuit_mode(circuits, kind)
    if mode == "probe":
        run_gate_probe(backend, kind, int(shots) if shots > 0 else 1000, seed)
        return
    price_weights = choose_price_weights(mode, circuits, kind, single_mu)
    shots_per_circuit = int(shots) if shots > 0 else quantum.SHOT_POLICY.get(kind, 100)

    # The exact answers the circuits are graded against, from the NumPy model in ftp_core (no Qiskit involved):
    #   ideal[mu]        probability of each five-test panel if the circuit ran without noise
    #   independent[mu]  the same per-test odds, but tests chosen independently (no correlations between qubits)
    #   targets          the distinct optimal panels we hope the job samples
    ideal = {mu: core.qaoa_xy_probs(problem.objective[mu]) for mu in price_weights}
    independent = {mu: core.independent_choice(ideal[mu]) for mu in price_weights}
    targets = sorted({problem.optimum[mu] for mu in price_weights})

    logical_circuits, job_circuits, gate_counts = step_3_build_circuits(problem, price_weights, mode, ideal, seed)
    if quantum.needs_routing(backend, kind):
        job_circuits = route_for_lattice_device(job_circuits, backend, seed, gate_counts)
    print_runtime_note(kind, shots_per_circuit)
    step_3_predict(price_weights, ideal, independent, targets, shots_per_circuit, show_figures)
    counts, label = step_3_run_the_job(backend, kind, mode, job_circuits, logical_circuits, price_weights,
                                       shots_per_circuit, seed, ideal)

    # Sections 4-6: what the samples show, the offline evidence, and what the project does not claim.
    step_4_results(problem, price_weights, counts, ideal, independent, targets, label, run_baselines, seed)
    step_5_precomputed_evidence(precomputed)
    step_6_what_this_does_not_claim()

    if dump_counts and counts:
        print_counts_json(backend_description, shots_per_circuit, label, counts, price_weights)
    print(f"\nDone in {time.time() - run_started:.1f}s. {ATTRIBUTION}")


# =================================================================================================================
# Loading
# =================================================================================================================
class Problem:
    """The clinic's problem, built once per Run and shared by every step.

    X, y        the patients: 297 x 13 test results, and the diagnosis (1 = heart disease, 0 = none)
    redundancy  13 x 13 table of how much each pair of tests repeats each other (|correlation|)
    price       price of every possible panel (a vector indexed by panel number, 8,192 entries)
    objective   {mu: score of every possible panel}, one per price weight; lower is better
    optimum     {mu: the best five-test panel}, found by checking all 1,287 of them
    """

    def __init__(self):
        self.X, self.y = core.load_data()
        self.redundancy = core.redundancy(self.X)
        self.price = core.cost_vector()
        self.objective = {mu: core.objective(core.R_K10, self.redundancy, self.price, mu) for mu in core.MU_GRID}
        self.optimum = {mu: core.exact_optimum(self.objective[mu]) for mu in core.MU_GRID}


def injected_backend():
    """The simulator Qollab passes in as a global variable named `backend` (None when run anywhere else)."""
    backend = globals().get("backend")
    return backend if backend is not None else getattr(builtins, "backend", None)


def load_project_json(which):
    """Read results/precomputed.json (which = "precomputed") or results/forte_cache.json ("forte_cache").

    Returns None, with a short message, if the file is missing or unreadable. The paths are written out in full
    because Qollab only ships data files whose paths appear literally in the code.
    """
    try:
        if which == "precomputed":
            with open("results/precomputed.json") as fh:
                return json.load(fh)
        with open("results/forte_cache.json") as fh:
            return json.load(fh)
    except Exception as e:  # noqa: BLE001
        print(f"  (could not read results/{which}.json: {type(e).__name__})")
        return None


def auc_lookup(precomputed):
    """{panel: cross-validated AUC} for all 1,287 five-test panels, from the precomputed file ({} if missing)."""
    auc_table = precomputed.get("auc_table", {})
    return dict(zip(auc_table.get("states", []), auc_table.get("aucs", [])))


# =================================================================================================================
# Sections 1 and 2: the problem, solved classically
# =================================================================================================================
def step_1_the_decision(problem):
    """Section 1: the patients, the decision the clinic faces, and the procedures that several tests share."""
    # Self-test: the fast price formula (a polynomial, which the circuit uses) must equal the obvious
    # test-by-test price for all 8,192 possible panels.
    worst_difference = max(abs(problem.price[panel] - core.panel_cost(panel)) for panel in range(2 ** core.N))

    rep.section("1. The decision")
    print(f"  {len(problem.y)} Cleveland chest-pain patients ({int(problem.y.sum())} with heart disease), "
          f"13 possible measurements.")
    print("  The clinic can collect only 5. Tests have real prices (Turney 1995, Ontario fee schedule 1992, CAD),")
    print("  and some share one procedure: pay for the procedure once, the extra readings are almost free.")
    shared = core.shared_costs()
    rep.table(["shared procedure", "tests", "paid once"],
              [[group, ", ".join(core.GROUPS[group]), rep.money(shared[group])] for group in core.GROUPS],
              note=f"price self-test: polynomial vs table on all 8,192 subsets, max difference {worst_difference:.1e}")


def step_2_classical_first(problem, auc, show_figures, revalidate_auc):
    """Section 2: the exact best panel at each price weight, how greedy shortcuts compare, and the price ladder
    (the best accuracy reachable at each price)."""
    rep.section("2. Classical first: exhaustive search is exact and instant at 13 tests")

    # (a) Exact answer vs greedy selection, for each price weight.
    started = time.time()
    rows, greedy_misses = [], 0
    for mu in core.MU_GRID:
        f, best = problem.objective[mu], problem.optimum[mu]
        greedy_panel, _ = classical.greedy(f)
        greedy_then_swaps, _ = classical.local_search(f, greedy_panel)   # greedy, then 1-swaps until stuck
        greedy_misses += greedy_panel != best
        rows.append([mu, rep.panel(core.state_to_names(best)), rep.money(problem.price[best]),
                     f"{auc[best]:.3f}" if best in auc else "?",
                     "optimal" if greedy_panel == best else f"rank {core.rank_of(f, greedy_panel)} of 1287",
                     "optimal" if greedy_then_swaps == best else f"rank {core.rank_of(f, greedy_then_swaps)}"])
    rep.table(["price weight mu", "exact best 5-test panel", "price", "CV AUC", "greedy", "greedy + 1-swap"], rows,
              note=f"exhaustive search over all 1,287 panels x 5 price weights took {time.time() - started:.2f}s; "
                   f"greedy misses the optimum at {greedy_misses} of 5 price weights")

    # (b) The price ladder: cheapest panel that reaches each new level of accuracy (needs the precomputed AUCs).
    if auc:
        ladder = core.auc_front(auc, problem.price)
        rep.table(["price", "panel (cheapest way to reach this AUC)", "CV AUC"],
                  [[rep.money(problem.price[s]), rep.panel(core.state_to_names(s), 70), f"{auc[s]:.3f}"]
                   for s in ladder],
                  note="[precomputed] cost-vs-accuracy front of all 1,287 five-test panels "
                       "(logistic regression, 5x3 CV, all 297 patients; optimistic: best of many)")
        if show_figures:
            rep.describe("a staircase of the best cross-validated AUC reachable at each panel price, from $9.20 "
                         "(AUC 0.838) to $293.10 (AUC 0.911); diamonds mark the exact optimum at each price weight. "
                         "The numbers are the table above.")
            try:
                short_label = {s: f"${problem.price[s]:.0f}: {core.procedures(s)}" for s in ladder}
                rep.price_ladder_figure([(problem.price[s], auc[s], short_label[s]) for s in ladder],
                                        [(problem.price[best], auc[best], f"mu={mu}")
                                         for mu, best in problem.optimum.items() if best in auc])
            except Exception as e:  # noqa: BLE001
                print(f"  (figure unavailable: {type(e).__name__}: {e})")

    # (c) Optional: recompute the optimal panels' accuracy live, to show the precomputed numbers are reproducible.
    if revalidate_auc:
        started = time.time()
        rows = []
        for best in sorted(set(problem.optimum.values()), key=lambda s: problem.price[s]):
            live = classical.cv_auc(problem.X, problem.y, best)
            rows.append([rep.panel(core.state_to_names(best)), rep.money(problem.price[best]), f"{live:.4f}",
                         f"{auc.get(best, float('nan')):.4f}"])
        rep.table(["optimal panel", "price", "CV AUC recomputed now", "precomputed"], rows,
                  note=f"[live] scikit-learn logistic regression, 5x3 repeated stratified CV, random_state=7 "
                       f"({time.time() - started:.1f}s)")


# =================================================================================================================
# Section 3: the quantum step
# =================================================================================================================
def choose_circuit_mode(requested, kind):
    """Turn the 'circuits' setting into "all", "single" or "probe".

    "auto" sends all five circuits in one job, except where the simulator only accepts one circuit per job
    (IonQ through Qollab), where it sends one.
    """
    mode = requested.strip().lower()
    if mode == "probe":
        return mode
    if mode not in ("auto", "all", "single"):
        print(f"  unknown circuits={requested!r}; using auto")
        mode = "auto"
    if mode == "auto":
        mode = "all" if quantum.LIST_JOBS_OK.get(kind, True) else "single"
    return mode


def choose_price_weights(mode, requested, kind, single_mu):
    """All five price weights, or (single-circuit mode) the one closest to the single_mu setting."""
    if mode == "all":
        return core.MU_GRID
    price_weights = [min(core.MU_GRID, key=lambda mu: abs(mu - single_mu))]
    if kind == "ionq" and requested.strip().lower() == "auto":
        why = "IonQ through Qollab accepts one circuit per job"
    else:
        why = "circuits = single"
    print(f"  single-circuit mode ({why}): this run uses one price weight, mu = {price_weights[0]}. "
          f"Run on the built-in simulator to see all five in one job.")
    return price_weights


def circuit_name(mu):
    """Circuit name for a price weight, e.g. 0.1 -> 'ftp_mu0p1' (results are looked up by this name)."""
    return f"ftp_mu{str(mu).replace('.', 'p')}"


def step_3_build_circuits(problem, price_weights, mode, ideal, seed):
    """Build one QAOA circuit per price weight, plus the bit-order check circuit when all five go in one job.
    Compile them to simple gates, and check the result against the exact NumPy model.

    Returns (circuits as built, compiled circuits to send, two-qubit gates per QAOA circuit).
    """
    started = time.time()
    logical_circuits = [quantum.build_circuit(problem.objective[mu], circuit_name(mu), core.GAMMA, core.BETA)[0]
                        for mu in price_weights]
    bit_order_check = [quantum.sentinel_circuit()] if mode == "all" else []
    job_circuits = quantum.portable(bit_order_check + logical_circuits, seed)

    # Safety check on exactly what will be submitted: simulate the last circuit exactly with Qiskit and compare it
    # with the NumPy model. A distance near 1e-15 means they agree; a large one means a gate convention changed.
    tvd, p_five_tests = quantum.submitted_vs_reference_tvd(job_circuits[-1], ideal[price_weights[-1]])
    gate_counts = [quantum.two_qubit_count(c) for c in job_circuits if c.name != "ftp_sentinel"]
    print(f"  built {len(job_circuits)} circuit(s) in {time.time() - started:.1f}s; "
          f"two-qubit gates (RZZ) per circuit: {gate_counts}")
    print(f"  check: submitted circuit vs exact NumPy model, total-variation distance {tvd:.1e} "
          f"(P(five tests) = {p_five_tests:.4f}, expected {core.P_HW5:.4f})")
    if tvd > 1e-6:
        print("  WARNING: the circuit does not match the model (gate convention changed?). Results below are suspect.")
    return logical_circuits, job_circuits, gate_counts


def route_for_lattice_device(job_circuits, backend, seed, all_to_all_gate_counts):
    """Re-compile the circuits for an IBM-style device, where two-qubit gates only work between neighbouring
    qubits, and print how many extra gates that costs compared with all-to-all trapped ions."""
    from qiskit import transpile
    started = time.time()
    routed = transpile(job_circuits, backend=backend, optimization_level=1, seed_transpiler=seed)
    routed_gate_counts = [quantum.two_qubit_count(c) for c in routed if c.name != "ftp_sentinel"]
    qubits_touched = max(len({c.find_bit(q).index for inst in c.data for q in inst.qubits}) for c in routed)
    print(f"  routed to this device's coupling map in {time.time() - started:.1f}s: {routed_gate_counts} two-qubit "
          f"gates per circuit (at most {qubits_touched} physical qubits touched)")
    print(f"  (all-to-all trapped ions need {all_to_all_gate_counts}: the same circuit costs "
          f"{np.mean(routed_gate_counts) / np.mean(all_to_all_gate_counts):.1f}x more two-qubit gates on this lattice)")
    return routed


def print_runtime_note(kind, shots_per_circuit):
    """Tell the user when a simulator is slow, and why."""
    if kind in ("ibm_fake", "aer_noise"):
        print(f"  note: this simulator applies noise shot by shot in your browser, so the default is "
              f"{shots_per_circuit} shots per circuit (set 'shots' to change it); expect up to a minute or two.")
    elif kind == "ionq":
        print("  note: IonQ's simulator runs in IonQ's cloud; with queueing this can take a few minutes.")


def step_3_predict(price_weights, ideal, independent, targets, shots_per_circuit, show_figures):
    """BEFORE the job runs, print the exact chance that one job of this size samples every optimal panel: for the
    ideal circuit, and for two samplers without its correlations. The run is then graded against this."""
    uniform = [np.full(len(core.FEAS_IDX), 1 / len(core.FEAS_IDX)) for _ in price_weights]
    ideal_list = [ideal[mu] for mu in price_weights]
    independent_list = [independent[mu] for mu in price_weights]

    shot_grid = sorted({100, 200, 500, 1000, shots_per_circuit})
    rep.table(["sampler (same shots)"] +
              [f"{s} shots" + (" <- this run" if s == shots_per_circuit else "") for s in shot_grid],
              [[name] + [rep.pct(core.closed_form_all_found(dists, targets, s)) for s in shot_grid]
               for name, dists in (("ideal QAOA circuit", ideal_list), ("independent-choice", independent_list),
                                   ("uniform 5-test panels", uniform))],
              note=f"PREDICTION, computed before the job: chance that one job samples all {len(targets)} distinct "
                   f"optimal panel(s) at least once (exact formula; noise lowers the QAOA row)")

    if show_figures:
        figure_shots = [25, 50, 100, 200, 300, 500, 750, 1000, 1500, 2000]
        at_500_and_1000 = {name: [core.closed_form_all_found(dists, targets, s) for s in (500, 1000)]
                           for name, dists in (("ideal", ideal_list), ("null", independent_list),
                                               ("unif", uniform))}
        rep.describe("three curves of the chance that one job finds every optimal panel versus shots per circuit "
                     f"(log scale). The ideal circuit rises fastest (about {rep.pct(at_500_and_1000['ideal'][0])} "
                     f"at 500 shots, {rep.pct(at_500_and_1000['ideal'][1])} at 1,000), the independent-choice "
                     f"sampler slower ({rep.pct(at_500_and_1000['null'][0])}, "
                     f"{rep.pct(at_500_and_1000['null'][1])}), uniform panels slowest "
                     f"({rep.pct(at_500_and_1000['unif'][0])}, {rep.pct(at_500_and_1000['unif'][1])}). "
                     f"The numbers are the table above.")
        try:
            rep.recovery_figure(figure_shots, {
                "ideal QAOA circuit": [core.closed_form_all_found(ideal_list, targets, s) for s in figure_shots],
                "independent-choice (no correlations)": [core.closed_form_all_found(independent_list, targets, s)
                                                         for s in figure_shots],
                "uniform five-test panels": [core.closed_form_all_found(uniform, targets, s) for s in figure_shots]},
                this_run=shots_per_circuit)
        except Exception as e:  # noqa: BLE001
            print(f"  (figure unavailable: {type(e).__name__}: {e})")


def step_3_run_the_job(backend, kind, mode, job_circuits, logical_circuits, price_weights, shots_per_circuit, seed,
                       ideal):
    """Send the ONE job and read back, for each price weight, how often each five-test panel was measured.

    Returns ({mu: ({panel: count}, raw shots)}, label). If the job fails, the counts come from the cached IonQ run
    (IonQ only) or are drawn from the ideal model, and the label says so clearly.
    """
    label = f"[live run on {kind}, {shots_per_circuit} shots per circuit]"
    result = None
    print(f"  submitting ONE job: {len(job_circuits)} circuit(s) x {shots_per_circuit} shots ...", flush=True)
    try:
        # A single circuit is sent on its own, not as a one-item list.
        to_send = job_circuits if len(job_circuits) > 1 else job_circuits[0]
        result, elapsed = quantum.submit_once(backend, to_send, shots_per_circuit, quantum.OneJobGuard(), seed, kind)
        print(f"  job finished in {elapsed:.1f}s")
    except Exception as e:  # noqa: BLE001
        print(f"  JOB FAILED: {type(e).__name__}: {e}")
        if mode == "all":
            print("  hint: re-run with circuits = \"single\" (one circuit per job).")
    if result is None:
        return fallback_counts(kind, price_weights, shots_per_circuit, seed, ideal)

    if mode == "all":
        check_bit_order(result)
    if kind == "ionq":
        print("  note: IonQ's noise-model simulator returns rounded expected counts (round(probability x shots)),")
        print("        not random samples, so panels rarer than about 1 in 2x(shots) do not appear at all.")
    counts = {}
    for j, mu in enumerate(price_weights):
        position_in_job = j + (1 if mode == "all" else 0)      # in "all" mode the bit-order check circuit is first
        raw_counts = quantum.counts_for(result, logical_circuits[j].name, position_in_job)
        panel_counts, total_shots, _ = quantum.five_test_counts(raw_counts)
        counts[mu] = (panel_counts, total_shots)
    return counts, label


def check_bit_order(result):
    """The bit-order check circuit should always read the panel {age, sex, cp, trestbps, fbs}. Print whether it did."""
    panel_counts = {}
    for key, count in quantum.counts_for(result, "ftp_sentinel", 0).items():
        panel = quantum.key_to_state(key)[0]
        panel_counts[panel] = panel_counts.get(panel, 0) + count
    share_expected = panel_counts.get(quantum.SENTINEL_STATE, 0) / max(sum(panel_counts.values()), 1)
    print(f"  bit-order check: {rep.yesno(share_expected >= 0.5)} ({rep.pct(share_expected)} of shots read the "
          f"expected panel age, sex, cp, trestbps, fbs; readout noise explains the rest)")


def fallback_counts(kind, price_weights, shots_per_circuit, seed, ideal):
    """Counts to show when the job failed, so the rest of the report can still be read. Always clearly labelled.

    On IonQ: the counts of an earlier real IonQ run (results/forte_cache.json), if it has these price weights.
    Otherwise: samples drawn from the exact ideal model, labelled NOT A RUN.
    """
    counts = {}
    cache = load_project_json("forte_cache") if kind == "ionq" else None
    if cache and all(str(mu) in cache.get("counts", {}) for mu in price_weights):
        label = f"[cached IonQ run: {cache.get('backend', '?')}, {cache.get('date', '?')}, NOT this press]"
        for mu in price_weights:
            panel_counts = {int(panel): int(n) for panel, n in cache["counts"][str(mu)].items()}
            counts[mu] = (panel_counts, int(cache.get("shots", sum(panel_counts.values()))))
        return counts, label

    label = "[NOT A RUN: samples drawn from the exact ideal distribution so the tables below can be read]"
    rng = np.random.default_rng(seed)
    for mu in price_weights:
        five_test_shots = int(rng.binomial(shots_per_circuit, core.P_HW5))
        draws = rng.choice(len(core.FEAS_IDX), five_test_shots, p=ideal[mu])
        panel_counts = {}
        for d in draws:
            panel = int(core.FEAS_IDX[d])
            panel_counts[panel] = panel_counts.get(panel, 0) + 1
        counts[mu] = (panel_counts, shots_per_circuit)
    return counts, label


def run_gate_probe(backend, kind, shots, seed):
    """Run setting circuits = "probe": one shallow circuit with known answers for every gate type we submit.

    If the simulator read gate angles differently from Qiskit, the measured values would be far from the
    expected ones; noise only moves them a little. Exactly one job, then the Run stops.
    """
    print("  gate-convention probe: one shallow circuit, known answers for rz, ry, rx, rzz and x.")
    circuit = quantum.portable([quantum.probe_circuit()], seed)[0]
    from qiskit.quantum_info import Statevector
    exact = Statevector(circuit.remove_final_measurements(inplace=False)).probabilities_dict()
    exact_values, _ = quantum.probe_readout(exact)
    print(f"  submitting ONE job: 1 circuit x {shots} shots ...", flush=True)
    try:
        result, elapsed = quantum.submit_once(backend, circuit, shots, quantum.OneJobGuard(), seed, kind)
    except Exception as e:  # noqa: BLE001
        print(f"  JOB FAILED: {type(e).__name__}: {e}")
        return
    measured, measured_shots = quantum.probe_readout(quantum.counts_for(result, circuit.name, 0))
    rows = []
    for (test, _, expected, _), exact_value, got in zip(quantum.PROBE_TESTS, exact_values, measured):
        assert abs(exact_value - expected) < 1e-9, "probe expectations are wrong"
        standard_error = (max(expected * (1 - expected), 0.01) / max(measured_shots, 1)) ** 0.5
        consistent = abs(got - expected) < max(4 * standard_error, 0.06)
        rows.append([test, f"{expected:.3f}", f"{got:.3f}",
                     "yes" if consistent else "NO (convention mismatch or heavy noise)"])
    rep.table(["test", "expected", f"measured ({measured_shots} shots, {kind})", "consistent?"], rows,
              note=f"job finished in {elapsed:.1f}s; tolerance max(4 standard errors, 0.06). A wrong angle convention "
                   f"would move the RZZ rows to about 0.75 / 1.00 (angle doubled) or 0.07 / 0.15 (halved).")
    print(f"Done. {ATTRIBUTION}")


# =================================================================================================================
# Section 4: what the samples show
# =================================================================================================================
def step_4_results(problem, price_weights, counts, ideal, independent, targets, label, run_baselines, seed):
    """Section 4: grade the measured panels against the exact answer, the two models, and classical methods."""
    rep.section("4. What the samples show " + label)

    # (a) For each price weight: how often the optimal panel was measured, vs what each model predicts.
    rows, sampled = [], set()
    for mu in price_weights:
        panel_counts, total_shots = counts[mu]
        five_test_shots = int(quantum.as_vector(panel_counts).sum())
        best = problem.optimum[mu]
        hits = panel_counts.get(best, 0)
        low, high = core.wilson(hits, five_test_shots)
        best_sampled = min(panel_counts, key=lambda s: problem.objective[mu][s]) if panel_counts else None
        sampled |= set(panel_counts)
        position = core.POS_IN_FEAS[best]
        rows.append([mu, f"{five_test_shots} of {total_shots}",
                     f"{hits / five_test_shots if five_test_shots else 0:.4f} [{low:.4f}, {high:.4f}]",
                     f"{ideal[mu][position]:.4f}", f"{independent[mu][position]:.4f}", f"{1 / 1287:.4f}",
                     rep.yesno(best_sampled == best)])
    rep.table(["mu", "five-test shots", "P(optimal panel) observed [95% CI]", "ideal circuit",
               "independent-choice", "uniform", "best sample = optimum?"], rows,
              note="independent-choice = same per-test odds as the circuit, tests drawn independently "
                   "(isolates what correlations between qubits add)")

    # (b) Pooled over all circuits in the job: which of the distinct optimal panels were measured at least once.
    found = [t for t in targets if t in sampled]
    print(f"  pooled over the job: {len(found)} of {len(targets)} distinct optimal panels sampled")
    for t in targets:
        print(f"    {rep.yesno(t in sampled):3s}  {rep.money(problem.price[t]):>8s}  {', '.join(core.state_to_names(t))}")
    print()

    # (c) Do the samples look like the ideal circuit, or like the sampler without correlations?
    llr_rows = []
    for mu in price_weights:
        vector = quantum.as_vector(counts[mu][0])
        if vector.sum() < 5:
            llr_rows.append([mu, "too few five-test shots", "", "", ""])
            continue
        observed, (mean_if_ideal, sd_if_ideal), (mean_if_null, sd_if_null), _ = \
            core.llr_stats(vector, ideal[mu], independent[mu])
        closer_to_ideal = abs(observed - mean_if_ideal) / max(sd_if_ideal, 1e-9) < \
            abs(observed - mean_if_null) / max(sd_if_null, 1e-9)
        llr_rows.append([mu, f"{observed:+.1f}", f"{mean_if_ideal:+.1f} +- {sd_if_ideal:.1f}",
                         f"{mean_if_null:+.1f} +- {sd_if_null:.1f}",
                         "ideal circuit" if closer_to_ideal else "independent-choice"])
    rep.table(["mu", "log-likelihood ratio (ideal vs independent)", "expected if ideal", "expected if independent",
               "samples look like"], llr_rows,
              note="a per-run test that the samples carry the circuit's correlations, not just its per-test odds")

    # (d) Classical methods given the same number of evaluated panels as the job produced.
    if run_baselines and sampled:
        rng = np.random.default_rng(seed)
        annealing_evaluated, local_search_evaluated = set(), set()
        for mu in price_weights:
            budget = int(quantum.as_vector(counts[mu][0]).sum())      # five-test panels the job produced
            if budget > 0:
                annealing_evaluated |= classical.sa_pool(problem.objective[mu], budget, rng)
                local_search_evaluated |= classical.rrls_pool(problem.objective[mu], budget, rng)
        rep.table(["method (same number of evaluated panels per price weight)", "distinct optima found"],
                  [["QAOA job (this run)", f"{len(found)} of {len(targets)}"],
                   ["simulated annealing (one seeded run)",
                    f"{sum(t in annealing_evaluated for t in targets)} of {len(targets)}"],
                   ["random-restart local search (one seeded run)",
                    f"{sum(t in local_search_evaluated for t in targets)} of {len(targets)}"]],
                  note="classical evaluations are microsecond function calls: this compares sample quality, not speed")


# =================================================================================================================
# Sections 5 and 6: offline evidence, and limits
# =================================================================================================================
def step_5_precomputed_evidence(precomputed):
    """Section 5: results that take minutes to hours to compute, so they were run offline (tools/precompute.py in
    the GitHub repo) and saved in results/precomputed.json."""
    evidence = precomputed.get("evidence", {})
    if not evidence:
        return
    provenance = precomputed.get("provenance", {})
    rep.section("5. Precomputed evidence (offline runs; file results/precomputed.json)")

    # (a) Chance that one job finds all four optimal panels, at several job sizes: quantum vs classical.
    recovery = evidence.get("recovery")
    if recovery:
        columns = ["100", "200", "500", "1000"]
        rows = [[name] + [rep.pct(recovery["quantum_exact"][c][name]) for c in columns]
                for name in ("ideal QAOA circuit", "independent-choice", "uniform five-test panels")]
        noisy = evidence.get("noisy")
        if noisy:
            rows.insert(1, ["QAOA circuit, IonQ older noise rates"] +
                        [rep.pct(noisy["closed_form_all_found"][c]) for c in columns])
        for name, method in recovery["classical_pooled_200_jobs"].items():
            rows.append([name] + [rep.pct(method[str(recovery["shots_to_evals"][c])]["all_found_rate"])
                                  for c in columns])
        rep.table(["method", "100 shots (22 evals)", "200 (44)", "500 (111)", "1000 (222)"], rows,
                  note="chance ONE job finds all 4 optimal panels. Quantum rows: exact formula (noisy row from a "
                       "10,000-shot noisy reference); classical rows: 200 seeded jobs with the same number of "
                       f"evaluated panels per price weight "
                       f"[precomputed {provenance.get('baselines', {}).get('created', '?')}]")

    # (b) Why there is no penalty term: QCA's penalty formulation vs our XY mixer.
    penalty = evidence.get("penalty")
    if penalty:
        rows = [[r["method"], r["p"], r["two_qubit_gates"], f"{r['P_opt_given_five']:.4f}",
                 f"{r['P_opt_per_raw_shot']:.5f}"] for r in penalty["rows"]]
        rep.table(["formulation (mu = 0)", "layers p", "2-qubit gates", "P(optimum | 5 tests)",
                   "P(optimum) per raw shot"], rows,
                  note=f"QCA's penalty term vs the XY mixer, all angles tuned without knowing the answer. Penalty "
                       f"values: Qiskit automatic {penalty['P_auto']:.3f}, textbook bound {penalty['P_bound']:.3f}, "
                       f"smallest valid {penalty['P_min']:.4f} (finding it requires solving the problem). "
                       f"Random 5-test panel: 0.00078.")

    # (c) Honest accuracy: the panel is chosen on training patients only, then scored on unseen patients.
    honest = evidence.get("honest_cv")
    if honest:
        rows = [[r["selection"], f"{r['AUC']:.3f} [{r['AUC_ci'][0]:.3f}, {r['AUC_ci'][1]:.3f}]",
                 f"{r['per_repeat_AUC']:.3f}", rep.money(r["mean_cost"]) if r["mean_cost"] else "n/a"]
                for r in honest["rows"]]
        rep.table(["panel chosen inside each training fold by", "held-out AUC [95% CI]", "per-repeat AUC",
                   "mean panel price"], rows,
                  note="honest numbers: the panel is re-selected on training patients only, then scored on unseen "
                       "patients (lower than the optimistic price ladder in section 2)")

    # (d) Two-qubit gate counts: trapped ions (all-to-all) vs an IBM-style heavy-hex lattice.
    gates = evidence.get("gates")
    if gates:
        rows = [[mu, ionq, ibm_all_to_all, ibm_heavy_hex] for mu, ionq, ibm_all_to_all, ibm_heavy_hex in
                zip(gates["mu"], gates["ionq_native_zz"], gates["cz_all_to_all"], gates["cz_heavy_hex"])]
        rep.table(["mu", "IonQ native ZZ (all-to-all)", "IBM CZ, all-to-all", "IBM CZ, heavy-hex routed"], rows,
                  note="the same circuit on trapped ions vs a superconducting heavy-hex lattice")

    # (e) The two pre-registered confirmatory checks.
    for key, title in (("confirm2", "pre-registered check 2"), ("confirm3", "pre-registered check 3")):
        check = evidence.get(key)
        if not check:
            continue
        print(f"  {title}: {'PASSED' if check['passed'] else 'NOT PASSED'} -- {check['claim']}")
        if key == "confirm2":
            for r in check["rows"]:
                print(f"    mu={r['mu']}: QAOA {r['mean_qaoa']:.4f} vs independent-choice {r['mean_independent']:.4f} "
                      f"({r['ratio']:.2f}x; QAOA higher in {r['subsamples_qaoa_higher']} of 50 subsamples)")
        else:
            for r in check["rows"]:
                print(f"    mu={r['mu']}: best sampled panel ${r['cost']:.2f} AUC {r['auc']:.3f}; best possible "
                      f"at that price {r['best_auc_at_or_below_cost']:.3f} (gap {r['gap']:.3f})")
        print()


def step_6_what_this_does_not_claim():
    rep.section("6. What this does not claim")
    print("  * No advantage over exhaustive search: at 13 tests it is exact and takes milliseconds (section 2).")
    print("  * No speedup. The quantum job is compared on sample quality at equal numbers of samples.")
    print("  * Prices are 1992 Ontario fees, used as relative costs; patients are a referral cohort, not screening.")
    print("  * The AUC front is the best of 1,287 panels on all patients (optimistic); re-selecting the panel")
    print("    inside each cross-validation fold gives lower, honest numbers (project page, 'Results').")


def print_counts_json(backend_description, shots_per_circuit, label, counts, price_weights):
    """Run setting dump_counts: one line of JSON with the five-test counts, for archiving a run."""
    payload = {"build": BUILD, "backend": backend_description, "shots": shots_per_circuit, "label": label,
               "counts": {str(mu): {str(panel): n for panel, n in counts[mu][0].items()} for mu in price_weights}}
    print("\nCOUNTS_JSON " + json.dumps(payload, separators=(",", ":")))
