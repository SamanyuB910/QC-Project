# Honest benchmarking and claims, plus the hybrid build stack on Qollab (Quantum Impact theme)

Snapshot: 2026-10-09, about 17:00 ET, on hackathon kickoff day.

**Labels.**
- **[Confirmed]** means a primary source says it, or I measured it myself (tool, date and setup given).
- **[Inferred]** means it is my reasoning.
- Every Cited Findings bullet carries a source.

**Scope.** These notes do not repeat the runtime facts already in `research_notes/Quantum Unlocked theme deep dive/build_feasibility_and_stack.md` (JS↔Python bridge, CSP, Pyodide packages, statevector timings, accessibility).

The sibling file `optimization_use_cases.md` already covers the Kipu BF-DCQO dispute and optimization baselines in depth, so here I only cross-reference them.

**My own tests (2026-10-09):**
- curl header probes of 45 data endpoints, sent with `Origin: null`.
- A real-browser fetch test from a **sandboxed `allow-scripts` iframe whose origin is `null`**, which is exactly Qollab's situation. I ran it in the Claude desktop browser pane (Chromium).
- An in-browser run of Microsoft's resource estimator (npm `qsharp-lang@1.33.1` from jsDelivr).
- Reading of 13 Qollab showcase projects through `https://api.qollab.xyz/api/project/id/<id>/versions/head`.
- Static inspection of the qiskit-algorithms 0.4.0, qiskit-optimization 0.7.0 and qiskit-machine-learning 0.9.1 wheels.

**Read-only.** I did not sign in, run, fork, submit or publish anything on Qollab.

---

## Q1. What is the community-accepted standard for an honest "measurable quantum step" in a small-scale demo?

### Takeaway
The 2025–2026 consensus (IBM/Lanes et al., the open Quantum Advantage Tracker, Huang–Choi–McClean–Preskill, Babbush et al., QOBLIB, Abbas et al., Bowles et al., Tuziemski et al.) converges on four requirements:
1. A **validated** output: error bars, a variational bound, or a classically checkable answer.
2. A comparison against the **strongest reasonable classical baseline**, tuned with equal effort, on the **same task, inputs and scoring function**.
3. **End-to-end, overhead-inclusive accounting** of time and cost, with all repetitions and statistics reported.
4. A **"hybrid null hypothesis" ablation**: replace the quantum subroutine with a classical one and show what changes.

For a 48-hour demo, the honest "measurable quantum step" is therefore a **pre-registered, reproducible, error-barred comparison**, not an advantage claim. Qollab's own Learn material models exactly this style:
- dated race results with binomial windows;
- "write thresholds before you run";
- one-layer QAOA openly losing to greedy search.

### Cited Findings

**Operational definitions of quantum advantage (IBM and partners)**
- **Lanes et al., "A Framework for Quantum Advantage" (IBM + Pasqal authors; arXiv 2506.20658, v1 25 Jun 2025, v2 14 Jul 2025; no journal reference listed)** — [arXiv:2506.20658](https://arxiv.org/abs/2506.20658); [HTML v2](https://arxiv.org/html/2506.20658v2)
  - Advantage requires that the output "can be rigorously validated" **and** that the run shows "superior efficiency, cost-effectiveness, or accuracy" versus classical computation alone.
  - Validation routes:
    - fault tolerance, "the cardinal approach";
    - provable error mitigation or post-selected error detection, which give rigorous error bars;
    - efficient classical verification (e.g. factoring, peaked circuits);
    - variational upper bounds, scored with uncertainty-aware metrics such as the V-score.
  - Candidate classes:
    - sampling: Shor, QAOA and heuristics, spin-glass sampling, peaked circuits; RCS "does not yet constitute a fully satisfactory pathway";
    - variational ground states: QPE, VQE, KQD, and SQD/SKQD, which have "the highest degree of verifiability";
    - expectation values: these depend on mitigation, which carries "exponential sampling overhead".
  - The relevant comparison is **hybrid quantum+classical versus classical alone**. Benchmarks should be defined "jointly with classical experts", and classical methods given "adequate opportunity to challenge the claim".
  - Claims are "a falsifiable scientific hypothesis", supported by "detailed methodologies and datasets" and "open-access leaderboards".
- **Open Quantum Advantage Tracker (IBM, Algorithmiq, Flatiron, BlueQubit; launched Nov 2025)** — [Tracker site](https://quantum-advantage-tracker.github.io/); [IBM blog, 23 Feb 2026](https://www.ibm.com/quantum/blog/quantum-advantage-tracker); [IBM QDC 2025 blog](https://www.ibm.com/quantum/blog/qdc-2025)
  - It has three pathways, each with an entry rule:
    - **Observable estimation**: "expectation values for observables alongside rigorous error bars".
    - **Variational**: entries "must provide upper bounds on the ground-state energy".
    - **Classically verifiable**: scored against known answers or efficiently checkable witnesses.
  - Statuses: **Active** (challenges leading classical methods), **Superseded** (later classical progress "has closed or reversed the apparent gap"), and **Baseline**.
  - Counts when fetched 2026-10-09:
    - observables: 4 active, 0 superseded, 1 baseline;
    - variational: "No active candidates recorded" (5 baselines);
    - classically verifiable: 2 active, 3 superseded.
  - IBM's Feb 2026 blog reported "30 submissions" on IBM and Quantinuum hardware. It defines advantage as "faster, more accurate, or more cost-effective than all classical alone methods" in a way that "can be rigorously validated", and says unverified RCS does not count.
  - IBM's QDC 2025 blog said advantage "hasn't been achieved yet" and targeted community-confirmed cases by end-2026 (from prior notes).

**Properties and criteria for a convincing claim (Google and Caltech authors)**
- **Huang, Choi, McClean, Preskill, "The vast world of quantum advantage" (arXiv 2508.05720; PRX, published Jul 2026)** gives five "keystone" properties of an ideal advantage: **predictability, typicality, robustness, verifiability, usefulness**. — [arXiv:2508.05720](https://arxiv.org/abs/2508.05720); [Caltech record, 9 Jul 2026](https://authors.library.caltech.edu/records/xays8-8vw38)
- **Babbush et al., "The Grand Challenge of Quantum Applications" (Google Quantum AI; arXiv 2511.09124, v3 4 Dec 2025)** — [arXiv:2511.09124](https://arxiv.org/abs/2511.09124); [HTML v3](https://arxiv.org/html/2511.09124v3)
  - Criteria for a convincing advantage demonstration:
    - verifiability;
    - average-case hardness over an efficiently constructible instance ensemble;
    - likely a **super-quadratic** speedup for practical advantage;
    - "no trivial concentration" (an input-dependent output signal);
    - robustness against the best classical heuristics, a "moving target".
  - The five stages are summarized under Q2.

**Benchmarking quantum optimization**
- **Abbas et al., "Challenges and Opportunities in Quantum Optimization" (46 authors; Nature Reviews Physics 2024, DOI 10.1038/s42254-024-00770-9)**, Section VI "Benchmarks" — [arXiv:2312.02279](https://arxiv.org/abs/2312.02279); [HTML v3](https://arxiv.org/html/2312.02279v3)
  - Run time is "an objectively fair metric", but "a fair comparison considers the total time": pre-processing, transpilation, embedding, compilation, execution and post-processing.
  - For stochastic methods, report "the whole boundary of time-to-target and optimality-gap-at-time values".
  - Feasibility comes first. Then report:
    - success rate in a fixed number of runs;
    - solution diversity / fair sampling;
    - energy or monetary cost where available;
    - an approximation ratio normalized by the range of achievable values (Sec. VI.5).
  - "Pre-processing should also be taken into account". It recommends model-independent benchmarks and warns that a feasible non-optimal solution "is not necessarily difficult for state-of-the-art classical methods".
- **QOBLIB, Koch et al., "Quantum Optimization Benchmarking Library – The Intractable Decathlon" (27 authors; Nat. Comput. Sci. 6, 653–671 (2026), DOI 10.1038/s43588-026-00991-1)** — [arXiv:2504.03832](https://arxiv.org/abs/2504.03832); [HTML v2](https://arxiv.org/html/2504.03832v2); [repo](https://git.zib.de/qopt/qoblib-quantum-optimization-benchmarking-library)
  - Ten problem classes: Market Split, LABS, Minimum Birkhoff Decomposition, Steiner Tree Packing, Sports Scheduling, Multi-period Portfolio, Max Independent Set, Network Design, Capacitated Vehicle Routing, and Graph Topology Design. Sizes range from <100 to ~100,000 variables.
  - Required reporting (Sec. 3.3):
    - best feasible objective (plus a bound if available);
    - for stochastic methods, the number of repetitions, the number of successful runs (within ε of best) and the best value over all runs;
    - "total wall-clock time" excluding queue idling, split into CPU/GPU/QPU/other;
    - software versions, hardware and memory.
  - Quantum runtime covers payload receipt, preparation, QPU execution and sample return. Transpilation is excluded, and shot count is treated as a hyperparameter.
  - QUBO objectives with different penalty weights are **not directly comparable**, so map solutions back to the original problem.
  - The authors say "We do not claim that our baseline results are the best solutions one can find."
  - My curl to the GitLab repo returned HTTP 429 twice (rate-limited) and no CORS header, so don't fetch QOBLIB live; vendor instances.
- **Tuziemski et al., "Recent quantum runtime (dis)advantages" (arXiv 2510.06337, v3 10 Feb 2026)** — [arXiv v3 HTML](https://arxiv.org/html/2510.06337v3); [abstract](https://arxiv.org/abs/2510.06337v3)
  - It reanalyses Kipu's BF-DCQO "runtime advantage" and D-Wave claims.
  - Its checklist for credible runtime claims:
    - direct timing, not estimates;
    - total time including readout, compilation, data transfer and **hyperparameter tuning**;
    - standardized metrics such as **time-to-ε** across diverse instances;
    - a broad size range, with "extrapolations with caution";
    - high-performance classical baselines that solve the problem class natively, tuned uniformly;
    - no selective reporting;
    - a **"hybrid null hypothesis"**: test whether replacing the quantum subroutine with a classical one gives comparable or better results.
  - The sibling notes record this paper as appearing in PR Applied 2026. The arXiv v3 page I read lists no journal, so that is unverified here.
  - Kipu's claim is [arXiv:2505.08663](https://arxiv.org/pdf/2505.08663).
- **Rønnow et al., "Defining and detecting quantum speedup" (Science 345, 420 (2014))** is the classic warning that "quantum speedup is elusive and can depend on the question posed". — [arXiv:1401.2910](https://arxiv.org/abs/1401.2910)

**Benchmarking quantum machine learning**
- **Bowles, Ahmed, Schuld, "Better than classical? The subtle art of benchmarking quantum machine learning models" (arXiv 2403.07059, Mar 2024)** — [arXiv:2403.07059](https://arxiv.org/abs/2403.07059); [HTML v2](https://arxiv.org/html/2403.07059v2)
  - Scale: 12 QML models, 6 binary tasks, 160 datasets.
  - "Out-of-the-box classical machine learning models outperform the quantum classifiers", and removing entanglement often doesn't hurt.
  - **Positivity bias**: of 55 surveyed papers, about 40% claim a quantum win and almost none report losses.
  - Downscaled MNIST is misleading: at 4×4 resolution about 70% of test images also appear in training.
  - Their method:
    - full grid search with **5-fold cross-validation** for every model, quantum and classical;
    - non-entangling ablations;
    - controlled synthetic data with a difficulty knob;
    - explicit disclosure of deviations.
  - The largest circuit simulated was 18 qubits, and about 20 was judged infeasible for the study.

**Program-level framing (DARPA)**
- **DARPA QBI**: "utility-scale" means a computer whose "computational value exceeds its cost". QBI's goal is to determine whether an industrially useful quantum computer can be built by **2033**. — [DARPA QBI page, fetched 2026-10-09](https://www.darpa.mil/research/programs/quantum-benchmarking-initiative)
  - Stage A (concept, ≤$1M), Stage B (R&D plan and risk retirement, ≤$15M), Stage C (government independent verification and validation (IV&V) that the design can be built and operated, ≤$300M).
  - The page (as of Oct 8, 2026) lists in Stage C: Atom Computing, Diraq, IBM, IonQ, Microsoft, PsiQuantum.
- **IonQ entered QBI Stage C on 7 Oct 2026** (up to $300M; Stage C "runs through 2029"; delivering several generations of "Superion" systems for DARPA's IV&V). — [IonQ press release, 7 Oct 2026](https://ionq.com/news/ionq-advances-to-final-stage-of-darpas-quantum-benchmarking-initiative)
  - Conflict: a July 2026 report called PsiQuantum one of only two Stage C companies. — [The Defense Post, 23 Jul 2026](https://thedefensepost.com/2026/07/23/psiquantum-darpa-quantum-computing/)

**Vendor claims and their critiques (IonQ-relevant)**
- **IonQ/Ansys, Mar 2025**: "up to 12%" faster blood-pump simulation via a VarQITE mesh partitioner. — [IonQ/Ansys press release](https://investors.ionq.com/news/news-details/2025/IonQ-and-Ansys-Achieve-Major-Quantum-Computing-Milestone--Demonstrating-Quantum-Outperforming-Classical-Computing/default.aspx); [arXiv:2503.13128](https://arxiv.org/pdf/2503.13128)
  - Hardware runs used coarsened graphs of ≤32 nodes, while production coarsens to ~10,000.
  - A critique notes: the headline gain came from classical simulation of the algorithm; the mesh was refined 100× denser; only 1 of 3 engineering cases improved; and the gains were −11.93/−11.51/−9.80%. — [Kirkpatrick Substack critique](https://wkirkpatrick.substack.com/p/ionq-and-ansys)
- **Kipu BF-DCQO "runtime advantage" (IBM hardware, May 2025)** was disputed by Tuziemski et al. (above). Details are in the sibling file `optimization_use_cases.md` Q2/Q4. — [arXiv:2505.08663](https://arxiv.org/pdf/2505.08663); [arXiv:2510.06337](https://arxiv.org/abs/2510.06337)

**Qollab's own published "honest comparison" pattern** (this is what Qollab staff, who write the docs and judge, consider good practice)
- **Lesson 5 of "Using quantum in a real application" (Nicolaas Spijker, Qollab)** prescribes five steps. — [Qollab Learn: Is quantum worth it in your app](https://qollab.xyz/learn/using-quantum-in-a-real-application/is-quantum-worth-it); [project learn-app-race](https://qollab.xyz/u/qollab/learn-app-race)
  1. "Write the thresholds before you run anything… a threshold chosen after seeing the result can be chosen to fit it."
  2. Solve it the ordinary way first.
  3. Solve it the quantum way with "the same inputs, output format and scoring function".
  4. Pass or fail both against the thresholds; "A relative comparison is not enough".
  5. "Write down the date and the backend."
  - Its race (22 Sep 2026, IonQ Aria 1 simulator): classical 0.20 ms against quantum 13.8 s (about 69,000×, "almost all of it queue and round trip").
  - Its binomial note: "two independent 1,000-shot draws land within about 40 of each other 95% of the time". The window is ~44 at p=0.5, 26 at 0.1 and 19 at 0.05.
  - It reminds readers that a simulator column "came from… classical hardware".
- **Same lesson, other examples:**
  - Regime Radar's 12-qubit test at 2,048 shots read 0.1768 (ideal), 0.0337 (Aria-1 noise model) and 0.1779 (exact offline).
  - A laptop brute-forces 36 binary variables (2^36 assignments) in "about a minute".
  - The Quantum Courier game publishes stage-by-stage wins (classical wins assignment, routing and time windows; quantum wins MaxCut "over a random-cut baseline"), and its author kept losses in "deliberately".

  — [Qollab Learn lesson 5](https://qollab.xyz/learn/using-quantum-in-a-real-application/is-quantum-worth-it)
- **Qollab Learn, Quantum Optimization and QAOA (15 Sep 2026)**, on a 24-node, 37-edge graph — [Qollab Learn: Quantum Optimization and QAOA](https://qollab.xyz/learn/quantum-optimization)
  - One tuned QAOA layer averages 25.5 of a possible 33 cut edges (ratio 0.77), versus 18.5 for a random split.
  - Greedy local search "averages about 31… and reaches 33 within a few restarts, in milliseconds". So "the average sample from one layer is worse than what a classical heuristic returns".
  - The best cut appears about once per thousand shots (≈4× in 4,096), versus once in 2.8 million for random.
  - It cites Goemans–Williamson's 0.878 guarantee.
- **Qollab Learn, Quantum Chemistry and VQE**: chemical accuracy is "1.6 millihartree, about 1 kcal/mol". — [Qollab Learn: Quantum Chemistry](https://qollab.xyz/learn/quantum-chemistry)
  - For H₂ read in two bases, 1σ energy uncertainty by shots per basis:

    | Shots per basis | 1σ uncertainty |
    |---|---|
    | 1,000 | 7.9 mHa |
    | 4,096 | 3.9 mHa |
    | 10,000 | 2.5 mHa |
    | 24,000 | 1.6 mHa |
    | 50,000 | 1.1 mHa |

  - So chemical accuracy costs ~48,000 shots per energy evaluation, and ~2.4 M shots for 50 optimizer evaluations.
  - Correlation energy is 20 mHa at equilibrium and 233 mHa at 2.5 Å.
- **Qollab's exact-QUBO showcase** states: "Keeping an exact classical baseline is how honest quantum benchmarking is done — you always know what the right answer is." — [showcase-qubo-exact (code via API)](https://api.qollab.xyz/api/project/id/019fbe15-b34f-7d75-b9df-987a2ad16033/versions/head)

**Metrics and statistics sources**
- **V-score** (variational energy plus its variance; Wu, …, Carleo, Science 386, 296–301 (2024)) is the accepted accuracy metric for variational ground-state claims without exact references. The tracker's variational pathway uses energy upper bounds. — [arXiv:2302.04919](https://arxiv.org/abs/2302.04919); [NCCR MARVEL summary](https://nccr-marvel.ch/highlights/carleo-vscore-science)
- **Generative models**: QCBM evaluation is moving from KL-to-target, which "limits… assessment to its ability to memorize data", to **generalization metrics**: fidelity of unseen valid samples, rate, coverage, plus KL_target vs KL_train. Report the mean over 5 trainings with standard error. — [Gili et al., "Do Quantum Circuit Born Machines Generalize?" arXiv:2207.13645](https://arxiv.org/abs/2207.13645v2); [Gili, Mauri, Perdomo-Ortiz, arXiv:2201.08770](https://web3.arxiv.org/pdf/2201.08770v3)
- **Bootstrap CIs** are available in SciPy (`scipy.stats.bootstrap`, BCa by default). SciPy 1.18 is built into Pyodide 314.0.7 (prior notes). — [SciPy docs](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.bootstrap.html)

### Inferences

**A "measurable quantum step" standard for a 48-hour Qollab demo.** Satisfy every line; judges and mentors can check each one.

1. **Pre-register.** Before running, write in the README:
   - the task;
   - the metric(s);
   - the pass threshold;
   - the classical baselines;
   - the instance set and its source dataset;
   - shots, seeds and backends.

   Commit it early. The project's version history serves as the timestamp.
2. **Define a two-or-three-tier baseline:**
   - (a) a trivial baseline: random or greedy;
   - (b) an exact or best-practice classical solver: brute force ≤ ~25 variables, HiGHS/cvxpy (in Pyodide), scikit-learn SVM/MLP with grid-search CV, or exact diagonalization;
   - (c) the **hybrid null**: the same classical outer loop with the quantum subroutine replaced by a classical sampler (uniform sampling, SA, or classical kernel), per Tuziemski.

   The quantum step is "measured" as the difference between the hybrid and (c), with error bars, not between the hybrid and (a).
3. **Metric per domain:**

   | Domain | Metrics |
   |---|---|
   | Optimization | Approximation ratio normalized to [best known, worst] (Abbas VI.5); P(optimal) per shot; time-to-target or TTS99 = t_run · ln(0.01)/ln(1−p_s); feasibility rate. Always map back to the original objective, never compare raw QUBO energies across penalty weights (QOBLIB). |
   | Chemistry | Energy error vs FCI/exact in mHa against the 1.6 mHa line; variance or V-score; shots needed at a given σ (Qollab's table). |
   | QML | Test accuracy, ROC-AUC or balanced accuracy, with a ≥5-fold-CV mean ± SD over ≥5 seeds; matched hyperparameter budget; a non-entangling ablation (Bowles). |
   | Generative | KL/TVD to the target and to the train set, MMD with a stated kernel bandwidth, plus generalization (fraction of valid, unseen samples). |
   | Sampling on hardware/simulator | TVD or Hellinger to ideal with a binomial/multinomial bootstrap. |

4. **Statistics:**
   - Every shot-based number gets a binomial or bootstrap 95% CI. SE = sqrt(p(1−p)/N); Qollab's window example is a good template. Use Wilson intervals near 0 or 1.
   - Every stochastic optimizer result gets ≥5 seeds (report the median and IQR). Every ML metric gets k-fold CV plus seeds.
   - When comparing two methods, report the paired difference with its CI, not two overlapping bars.
   - Label each result with backend name, date, shots and seed (Qollab lesson step 5).
5. **Time accounting:**
   - Report wall-clock for every method, including classical pre/post-processing and the optimizer loop. Label the quantum timing as "simulator in browser" or "IonQ cloud simulator incl. queue".
   - Never present simulated-quantum time as a speedup.
   - The defensible statements are quality-at-equal-budget (e.g. equal number of cost-function evaluations or samples) and a separately stated cost line.
6. **Scaling curves:**
   - Plot the metric versus problem size only over sizes you actually ran (e.g. 6–20 qubits), with CIs.
   - Show the classical baseline's curve on the same axes.
   - If you extrapolate, draw it dashed, state the fitted model and its uncertainty, and add a sentence on what would falsify it (Tuziemski: "treat extrapolations with caution"; Rønnow: speedup "can depend on the question posed").
   - Never extrapolate a noiseless-simulator trend to hardware.
7. **Verifiability tie-in (tracker language):**
   - Optimization or verifiable tasks are scored against an exact or classically checkable optimum.
   - Ground-state tasks report variational upper bounds versus exact energies.
   - Observable tasks report expectation values with error bars.

   Saying which tracker pathway your demo mirrors is a cheap credibility signal.

**How reviewers detect over-claiming.** Pre-empt each red flag in a "Limitations and threats to validity" section.
- "Quantum advantage" or "speedup" stated with no validated output, or from simulator timings.
- Only weak baselines (random, untuned), or a baseline that solves a reformulated problem.
- Unequal hyperparameter search budgets (Bowles' positivity bias).
- Cherry-picked instances or seeds.
- Raw QUBO energies compared across penalty choices.
- Toy or downscaled data presented as real-world (MNIST 4×4).
- Extrapolated scaling from 3–4 sizes.
- Omitted overheads (transpile, queue, optimizer iterations).
- Missing ablations (no entanglement, no quantum).
- Vendor press-release language: "outperforming classical" from classical simulations (the IonQ/Ansys critique) or "runtime advantage" from estimated runtimes (the Kipu critique).

**Positioning.** Given IonQ's Stage C entry two days before kickoff, a project that speaks DARPA's language reads as industry-literate rather than hype-driven. That means "value vs cost", "independent verification", and "what would need to be true by ~2029–2033".

### Gaps
- I could not read Abbas et al. Section VI end to end; only the summarized metrics above were extracted. QOBLIB's Section 5 (submission format) was not read.
- I found no primary source giving a formal standard for "measurable quantum step" in hackathon rubrics. The standard above is my synthesis.
- I did not find an MMD-specific recommendation paper for quantum generative models in this session.
- The Tuziemski journal status is unverified (the sibling notes say PR Applied 2026).
- Babbush et al.'s journal reference (sibling notes say PRX Quantum 2026) is not shown on arXiv.

---

## Q2. Which resource-estimation approaches can a team run in 48 h to make a credible "path to impact" claim?

### Takeaway
The most credible fast option is Microsoft's open-source resource estimator, which I confirmed runs **in the browser**:
- npm `qsharp-lang@1.33.1` (MIT) loads from jsDelivr.
- It accepts **Q# or OpenQASM 3** and returns logical/physical qubits, code distance, T/CCZ counts and runtime in under 1 s per estimate.
- A Qollab page can therefore compute a live "what this would need at scale" panel from the project's own circuit, exported to QASM 3.

Offline, the `qdk`/`qsharp` Python packages (MIT, native wheels only, not installable in Pyodide) do the same. Qualtran (Apache-2.0) and pyLIQTR are too heavy for the browser but fine offline.

Frame impact with:
- Babbush's five stages (say honestly that the project is at Stage II/III-thinking with a Stage IV estimate);
- DARPA's "value exceeds cost" definition;
- a stakeholder, numbers on problem size and cost, and a limitations section.

### Cited Findings

**In-browser estimator: what I measured**
- **My test (2026-10-09, Chromium in the Claude desktop browser pane; page origin pyodide.org, not inside Qollab):**
  - Code: `import("https://cdn.jsdelivr.net/npm/qsharp-lang@1.33.1/dist/browser.js")`, then `loadWasmModule(".../lib/web/qsc_wasm_bg.wasm")`, `getCompiler()` (main thread, no worker) and `getEstimates(program, "", paramsJSON)`. All succeeded.

    | Step | Time |
    |---|---|
    | Module import | 3.4 s |
    | Wasm instantiate | 0.47 s |
    | Two estimates | 0.81 s |
    | OpenQASM estimate | 0.29 s |

  - An 8-qubit Q# toy (H·T on each qubit plus 6 CCNOTs) gave T-count 8 and CCZ count 6 under two hardware settings:

    | Setting | Physical qubits | Code distance | Runtime |
    |---|---|---|---|
    | `qubit_gate_ns_e3`, surface code | 107,730 | 9 | 122.4 µs |
    | `qubit_maj_ns_e6` + `floquet_code` | 17,940 | 3 | 30.6 µs |

  - A 4-qubit **OpenQASM 3** program (`projectType: "openqasm"`) gave T-count 1, 1 rotation, 106,110 physical qubits and 72 µs.

  — own test; package files via [jsDelivr qsharp-lang@1.33.1](https://cdn.jsdelivr.net/npm/qsharp-lang@1.33.1/package.json)
- **Package details:**
  - `qsharp-lang` 1.33.1 was published to npm 2026-10-08 under the MIT license.
  - Its `ICompiler` interface exposes `getEstimates(program: ProgramConfig, expr: string, params: string): Promise<string>`, plus `getCircuit`, `run` and `runWithNoise`. `ProjectType` is `"qsharp" | "openqasm"`.
  - The wasm is 6,246,150 bytes, served by jsDelivr as `application/wasm` with `access-control-allow-origin: *`.

  — [npm registry qsharp-lang](https://registry.npmjs.org/qsharp-lang/latest); [compiler.d.ts](https://cdn.jsdelivr.net/npm/qsharp-lang@1.33.1/dist/compiler/compiler.d.ts); [main.d.ts](https://cdn.jsdelivr.net/npm/qsharp-lang@1.33.1/dist/main.d.ts)

**The estimator: documentation and Python packages**
- **Microsoft docs (updated 2026-07-31)** — [Microsoft Learn: Introduction to the resource estimator](https://learn.microsoft.com/en-us/azure/quantum/intro-to-resource-estimation)
  - The estimator is an open-source part of the QDK (`github.com/microsoft/qdk/tree/main/source/qre`).
  - It takes four inputs: an application model, an architecture model, a QEC/factory model, and an error budget.
  - It accepts Q#, Cirq, OpenQASM, QIR, logical counts or custom applications, and returns a **Pareto frontier** of qubits versus runtime.
- **PyPI (2026-10-09):**

  | Package | Version | License | Wheels / dependencies |
  |---|---|---|---|
  | `qsharp` | 1.31.0 (thin) | MIT | Depends on `qdk>=1.31.0` |
  | `qdk` | 1.33.1 (uploaded 2026-10-08) | MIT | macOS, manylinux and Windows wheels only, no Pyodide/Emscripten wheel; has a `qre` extra (pandas) and a `qiskit` extra |
  | `qualtran` | 0.7.0 | Apache-2.0 | Pure wheel, but depends on `galois`, `quimb`, `qsharp`, `cirq-core`, `pennylane`, `dash`, `notebook`, … |
  | `pyLIQTR` | 1.4.2 | listed as "BDS-2" (sic) | Pure wheel; depends on `qualtran==0.4.0`, `openfermion`, `juliacall`, `gmpy2`, … |

  — [PyPI qsharp](https://pypi.org/pypi/qsharp/json); [PyPI qdk](https://pypi.org/pypi/qdk/json); [PyPI qualtran](https://pypi.org/pypi/qualtran/json); [PyPI pyLIQTR](https://pypi.org/pypi/pyLIQTR/json)

**Analytic formulas you can compute by hand or in numpy**
- These are the surface-code defaults of the Microsoft model (Beverland et al.):
  - logical error per cycle P_L(d) = 0.03·(p/0.01)^((d+1)/2);
  - physical qubits per logical qubit = 2d²;
  - logical cycle time = (4·t_2q + 2·t_meas)·d.
  - Check: p = 10⁻³ at d = 5 gives P_L = 3×10⁻⁵ and 50 physical qubits per logical.
  - Caveat: the formula sources I found were the Qualtran port and mirror copies of Microsoft training pages, not learn.microsoft.com itself.

  — [Qualtran: Beverland et al. model](https://qualtran.readthedocs.io/en/latest/surface_code/beverland_et_al_model.html); [Qualtran ↔ Microsoft estimator interop](https://qualtran.readthedocs.io/en/latest/surface_code/msft_resource_estimator_interop.html)

**Reference resource numbers (Babbush et al., Stage IV examples)**
- RSA-2048: ~1,400 logical qubits, ~7×10⁹ Toffolis, ~10⁶ physical qubits, ~1 week.
- FeMoco (76 orbitals): ~1,500 logical qubits, ~10⁹ Toffolis, ~5×10⁶ physical qubits, ~9 h.
- DQI on optimal polynomial intersection: ~1,900 logical qubits, ~6×10⁶ Toffolis, ~8×10⁵ physical qubits, ~1 h.
- The authors note many estimates stop at sub-stage IV(b), and that manual estimation is "tedious and hard to verify".

— [arXiv:2511.09124 HTML](https://arxiv.org/html/2511.09124v3)

**The five stages of an application's maturity (Babbush et al.)**
- **I. Algorithm discovery** in an abstract, worst-case setting.
- **II. Identifying hard instances**: concrete instances where a quantum computer beats the best known classical method.
- **III. Real-world connection**: the speedup survives "after accounting for all real-world constraints and overheads". Only cryptanalysis and quantum simulation have convincingly reached this stage.
- **IV. Optimization and resource estimation**: "concrete, finite resource costs".
- **V. Deployment**: "entirely prospective".
- Stages II and III are the most under-resourced. The authors favour an "algorithm-first" over a "problem-first" approach.

— [arXiv:2511.09124](https://arxiv.org/abs/2511.09124); [HTML v3](https://arxiv.org/html/2511.09124v3)

**Utility and cost framing**
- DARPA's "utility-scale" = "computational value exceeds its cost", targeted by 2033. — [DARPA QBI](https://www.darpa.mil/research/programs/quantum-benchmarking-initiative)
- Qollab's lesson ties the ship/no-ship verdict to four dated quantities: qubit count (25–36 on Qollab's IonQ machines), error rate, queue latency and cost per run. — [Qollab Learn lesson 5](https://qollab.xyz/learn/using-quantum-in-a-real-application/is-quantum-worth-it)

### Inferences

**48-hour resource-estimation recipe** (each step is ≤ 2 hours of work)
1. **Logical counts from your own circuit.**
   - Export the exact circuit family you run (e.g. QAOA p = 1 at n = 8…20) with `qiskit.qasm3.dumps`. Also generate the same family at target sizes (n = 100, 1,000, 10,000) **offline**, or analytically count gates: QAOA p layers on a graph with |E| edges ≈ 2p|E| CNOTs and p|E| + pn rotations.
   - Feed the QASM to `getEstimates` in the browser, or to `qdk` offline.
   - Rotations dominate T-count, so state the synthesis precision the estimator assumes.
2. **Sweep hardware assumptions.** Run at least the `qubit_gate_ns_e3` and `qubit_gate_ns_e4` (gate-based, ion-like ns-to-µs timescales may need `qubit_gate_us_e3`/`us_e4`) presets, plus a custom error rate matching IonQ's published ~0.4–0.7% 2Q error.
   - Present a small table and a qubits-vs-runtime Pareto plot.
   - Trapped ions have µs-scale gates, so the `us_*` presets are the honest choice for an IonQ story.
3. **Compare with the classical cost at the same size.** For example, Gurobi/HiGHS solves an n = 1,000 instance in X s on a laptop, measured or cited. If the fault-tolerant runtime is hours against seconds classically, say so: that is the honest Stage IV result.
4. **Put the estimate on the page** as a live panel (the qsharp-lang wasm loads from jsDelivr, which Qollab's CSP allows):
   - first load ≈ 4 s, so make it lazy, behind a "Estimate at scale" button;
   - it runs on the main thread (Qollab blocks workers);
   - it is MIT, so it is compatible with the hackathon's MIT-only rule.
   - **Not yet verified inside Qollab's sandbox.** The CSP (`script-src cdn.jsdelivr.net 'unsafe-eval'`, `connect-src *`) suggests it should work, but test on day 1.
   - Fallback: precompute estimates offline and ship JSON.
5. **Use NISQ-era resources too**, not just fault-tolerant ones:
   - 2Q-gate count and depth after transpiling to IonQ native gates;
   - the expected circuit fidelity ≈ (1−ε₂)^(#2Q) at ε₂ ≈ 0.5%: e.g. 100 two-qubit gates gives ≈ 0.61, and 300 gives ≈ 0.22;
   - the shots needed for a target precision (Qollab's chemistry table method).

   This tells judges where the near-term regime ends.

**Impact-potential write-up template** (Documentation and Impact criteria)

| Section | Content |
|---|---|
| Problem and stakeholder | Who suffers the problem (grid operator, hospital scheduler, logistics SME), with 2–3 sourced numbers: cost, frequency, instance sizes in practice. |
| Today's best classical practice | Solver, typical runtime and its gap, and why it is hard (NP-hard class, instance size, latency constraint). |
| What we built | The hybrid loop diagram, and which step is quantum and why that step. |
| Measured result | Pre-registered thresholds; pass/fail per baseline, with CIs, backend and date. |
| Path to impact | Babbush stage placement ("this demo addresses Stage II/III questions for X; our Stage IV estimate says Y logical qubits / Z hours"); what hardware milestone would change the verdict (DARPA's 2033 utility-scale target, IonQ's roadmap labelled as vendor projections); a falsifiable "advantage would require …" sentence. |
| Limitations | Simulator-only results; tiny instances; subsampling; noise-model fidelity; no runtime advantage claimed. |

### Gaps
- I did not run qsharp-lang **inside** Qollab's `jsworker.html` frame, so whether `qsc_wasm.js` uses `import.meta.url` or worker features that the sandbox blocks is unverified.
- I did not test the `qdk` Python `qre` extra or Qualtran installs.
- The official learn.microsoft.com pages for qubit-parameter presets and QEC formulas returned 404 at the URLs I tried; the formulas come from Qualtran's port.
- IonQ-specific fault-tolerant presets (ion gate times and error rates) are not built into the estimator; teams must supply custom `qubitParams`.

---

## Q3. Which public data sources can a Qollab project fetch live in the browser?

### Takeaway
Qollab JS (and the Python it imports) fetches with **origin `null`** and **GET only**, and needs `Access-Control-Allow-Origin: *`. A server that echoes `null` also works.

I tested from a real null-origin sandboxed iframe. These work:
- raw.githubusercontent.com, the GitHub API, jsDelivr (`/gh/` and `/npm/`), Hugging Face (dataset-viewer and `resolve`), Zenodo API;
- Socrata portals, World Bank, Open-Meteo, NWS, NOAA NCEI and CO-OPS, NASA POWER, USGS;
- OSRM, PubChem PUG-REST, RCSB PDB, UniProt, ChEMBL, OpenML (direct URLs), Our World in Data (canonical URLs), Wikipedia (`origin=*`), EIA v2 (with a key);
- Kaggle public downloads (undocumented and fragile).

These fail:
- FRED;
- the UCI ML Repository;
- the Materials Project (CORS preflight lacks Allow-Origin, and it needs a key);
- the main Overpass interpreter (406, no CORS);
- data.gov's old CKAN endpoint (404);
- QOBLIB's GitLab (429).

Redirects are a trap: if any hop lacks CORS, the fetch fails.

### Cited Findings

**Qollab's network rules**
- GET via `pyodide.http.pyfetch(url)` or `fetch(url)`; POST, PUT and DELETE are blocked; no XHR, WebSocket or workers.
- Requests from a JS project "go out with the origin `null`, which a server that allows only named origins refuses". No cookies or credentials are sent.
- "Never put an API key, token or password in it", and "Keep the core of the project working without outside services".
- For datasets over 2 MB, "host it somewhere else and read it with a GET request… Read it in pieces", using a documented streaming `getReader()` example.

— [Qollab docs: Runtime environment](https://qollab.xyz/learn/docs/runtime-environment)

**My measurements**
- **Test A:** curl GET with `Origin: null`, recording the `Access-Control-Allow-Origin` header and status. — own test, 2026-10-09
- **Test B:** a real Chromium fetch from `<iframe sandbox="allow-scripts">` (`self.origin === "null"`), giving OK/FAIL plus size and latency. — own test, 2026-10-09

| Source | Example endpoint tested | curl ACAO | Browser (null origin) | Notes |
|---|---|---|---|---|
| raw.githubusercontent.com | `/plotly/datasets/master/2014_apple_stock.csv` | `*` | OK 114 ms | Best for small CSV/JSON you host yourself (MIT repo) |
| GitHub REST API | `/repos/plotly/datasets` | `*` | OK | 60 req/h unauthenticated (not re-verified) |
| jsDelivr `/gh/` | `/gh/plotly/datasets@master/…csv` | `*` | OK | Pin a tag or commit; CDN-cached |
| jsDelivr `/npm/` | `vega-datasets@2.8.1/data/cars.json` | `*` | (curl only) | Versioned, immutable |
| Hugging Face dataset-viewer | `datasets-server.huggingface.co/rows?…` | `null` (echo) + credentials true | OK | `/rows` max `length` = 100 per call; also `/parquet`, `/filter`, `/search` ([HF docs](https://huggingface.co/docs/dataset-viewer/rows)) |
| Hugging Face file `resolve` | `/datasets/scikit-learn/iris/resolve/main/Iris.csv` | `null` echo on 307 and 200 | OK | Redirect hops are CORS-enabled |
| Zenodo REST API | `zenodo.org/api/records?q=qubo` | `*` | OK | DOIs for citation |
| Socrata (NYC, Chicago) | `/resource/<id>.json?$limit=1` | `*` | OK | SoQL filters in the query string |
| data.gov CKAN | `catalog.data.gov/api/3/action/package_search` | none | — | **404** (endpoint changed); use the publisher's Socrata/ArcGIS API |
| World Bank v2 | `/v2/country/US/indicator/NY.GDP.MKTP.CD?format=json` | `*` | OK | No key |
| Open-Meteo forecast and archive | `api.open-meteo.com/v1/forecast…` | `*` | OK | Free non-commercial: <10,000 calls/day, 5,000/h, 600/min; CC BY 4.0 ([terms](https://open-meteo.com/en/terms)) |
| NWS api.weather.gov | `/points/33.75,-84.39` | `*` | OK | US only |
| NOAA NCEI Access Data Service | `/access/services/data/v1?dataset=daily-summaries…` | `*` | OK | No token needed |
| NOAA CO-OPS tides | `api.tidesandcurrents.noaa.gov/api/prod/datagetter…` | `*` | (curl) | — |
| NOAA CDO v2 | `/cdo-web/api/v2/datasets` | `*` | — | 400 without a token header (custom header; key would be public) |
| NASA POWER | `/api/temporal/daily/point…` | `*` | OK | Solar and met data |
| USGS earthquakes | `/fdsnws/event/1/query?format=geojson` | `*` | OK | — |
| EIA API v2 | `/v2/…?api_key=DEMO_KEY` | `*` | OK (DEMO_KEY) | Needs a key in the URL, which would be public; DEMO_KEY is rate-limited, so prefer a cached snapshot |
| FRED API and fredgraph.csv | `api.stlouisfed.org/fred/…`, `fred.stlouisfed.org/graph/fredgraph.csv` | none | **FAIL** | Not browser-fetchable |
| OSRM demo server | `/route/v1/driving/…`, `/table/v1/driving/…` | `*` | OK | The table service gives distance/duration matrices for routing QUBOs; demo server, fair use |
| Overpass (main) | `overpass-api.de/api/interpreter?data=…` | none (HTTP 406) | **FAIL** | `/api/status` has ACAO `*`; the mail.ru mirror returned CORS-OK but HTTP 504. Treat Overpass as unavailable live and pre-extract offline |
| PubChem PUG-REST | `/rest/pug/compound/name/aspirin/property/…/JSON` | `*` | OK | Molecule properties and geometries |
| RCSB PDB data API | `data.rcsb.org/rest/v1/core/entry/4HHB` | `*` | OK | — |
| UniProt REST | `rest.uniprot.org/uniprotkb/P69905.json` | `*` | OK | — |
| ChEMBL REST | `/chembl/api/data/molecule/CHEMBL25.json` | `*` | OK | — |
| Materials Project | `api.materialsproject.org/materials/summary/…` | none; preflight lists `X-Api-Key` but **no Allow-Origin** | **FAIL** | Also needs an API key header |
| UCI ML Repository | `archive.ics.uci.edu/static/public/53/iris.zip`, `/api/dataset?id=53` | none | **FAIL** | Use the OpenML or HF mirror |
| OpenML JSON API | `www.openml.org/api/v1/json/data/61` | `*` | OK | — |
| OpenML data download | `www.openml.org/data/v1/download/61` | `*` | OK | **`api.openml.org/data/v1/download/61` FAILS**: its 301 hop lacks CORS |
| Our World in Data grapher CSV | `ourworldindata.org/grapher/co-emissions-per-capita.csv` | `*` | OK (801 KB) | An old slug that 301-redirects FAILED; use the canonical slug |
| Kaggle | `/api/v1/datasets/download/uciml/iris` | `null` echo; 302 to a signed GCS URL | OK (3.7 KB zip) | Unauthenticated; **undocumented**; dataset licenses vary; may break; don't depend on it |
| Wikipedia API | `…/w/api.php?…&origin=*` | `*` | OK | Needs `origin=*` |
| CelesTrak GP | `/NORAD/elements/gp.php?…` | `*` | CORS OK but HTTP 500 at test time | — |
| QOBLIB (ZIB GitLab raw) | `git.zib.de/qopt/qoblib…/-/raw/main/README.md` | none | — | HTTP 429 twice; vendor instances instead |

**Fetch semantics behind these results**
- An opaque origin serializes as `null`, and a CORS check passes when ACAO is `*` (without credentials) or equals the request's serialized origin. — [Fetch Standard, CORS check](https://fetch.spec.whatwg.org/#cors-check)

**OpenStreetMap tiles (for maps)**
- Required: visible "© OpenStreetMap contributors" attribution, the HTTPS endpoint only, a valid Referer, and honoured caching.
- Prohibited: bulk or offline download and heavy use.
- Availability is best-effort with no SLA.

— [OSMF Tile Usage Policy](https://operations.osmfoundation.org/policies/tiles/)

### Inferences

**Data architecture for judging reliability**
- Ship a **frozen, cited snapshot** (≤2 MB JSON or CSV, with source URL, DOI, license, retrieval date and a SHA-256 in the README) as the default dataset.
- Make the live fetch an optional "Refresh from source" button that falls back silently to the snapshot. This follows Qollab's own advice that the project must keep working when servers are down.
- The data source that is both most reliable and most citable is **your own MIT-licensed GitHub repo, read via jsDelivr `/gh/user/repo@<tag>/file`**: immutable, CORS `*`, CDN-cached.
- Mirror a public dataset there, keeping its original license and citation, if the license allows redistribution.
  - CC BY / CC0 / ODbL data can be mirrored with attribution.
  - Check per-dataset terms on Kaggle and UCI.

**Good live sources for the Quantum Impact theme**

| Theme | Sources |
|---|---|
| Energy / grid | EIA (key problem: use a snapshot), Open-Meteo (weather-driven load or solar), NASA POWER (irradiance), World Bank |
| Logistics / routing | OSRM `/table` gives real road-distance matrices for 5–12 stops, which suits TSP/VRP QUBOs. Pre-extract POIs offline since Overpass is unreliable. |
| Chemistry / materials | PubChem (geometries for PySCF), RCSB / UniProt / ChEMBL (bio targets). The Materials Project is not usable live. |
| Finance | Not FRED (no CORS). World Bank works; ship stock price history as a snapshot in your repo. |
| Health / civic | Socrata city portals, CDC Socrata (`data.cdc.gov`) is likely but not tested |
| QML benchmarks | OpenML (direct `www` URLs) and the HF dataset-viewer (≤100 rows per call; page through or use `/parquet` URLs) |

**Citing and subsampling credibly**
1. Cite the dataset (author/publisher, title, version or date, DOI or URL, license), the exact query URL, and the retrieval timestamp.
2. Subsample with a **seeded, documented rule**: stratified k-of-N, a geographic radius, or top-N by demand. Report the full-size statistics next to the subsample's, so judges see representativeness.
3. Run the classical baseline on **both** the subsample and the full instance. This shows where classical handles full scale and makes the "quantum handles only 12–20 variables today" limitation explicit.
4. For QML, cap features with PCA fitted on the training fold only, to avoid leakage. Report class balance. Avoid toy "MNIST 4×4" style reductions (Bowles).
5. For optimization, prefer instances you can solve exactly (≤ ~25–30 binary variables via brute force or HiGHS) so the approximation ratio is exact.

**Never put API keys in a Qollab project.** For key-gated APIs (EIA, NOAA CDO, Materials Project), fetch offline and commit the snapshot.

### Gaps
- Not tested inside Qollab itself. My null-origin iframe reproduces the CORS situation, but not Qollab's exact CSP `connect-src` (`*`, so it should not matter) or any proxying Qollab might do.
- Not tested:
  - Python-side `pyfetch` (same browser fetch, so the same CORS rules; inferred);
  - CDC, Census, ArcGIS Hub, Eurostat, ENTSO-E, NREL;
  - GitHub release assets (my probe used a wrong URL and got a 404).
- Rate limits for the GitHub API (unauthenticated) and the OSRM demo server were not re-verified.
- I found no current data.gov API documentation; only that the old CKAN path 404s.

---

## Q4. Do the Qiskit application libraries actually run in Qollab's browser runtime, with what speed? (Includes hybrid-workflow and visualization engineering.)

### Takeaway
**Yes, they run.** Qollab published official one-file showcases (Aug 1, 2026) that run in the browser:
- **qiskit-optimization 0.7.0** `MinimumEigenOptimizer` with **QAOA** (`StatevectorSampler`, COBYLA, 50 evaluations) and with `NumPyMinimumEigensolver`;
- **qiskit-algorithms 0.4.0** VQE;
- **qiskit-nature 0.8.0 with PySCF compiled to WebAssembly** (H₂ scan at 4 bond lengths);
- **qiskit-finance 0.4.1** (option-pricing circuits, portfolio QP);
- **qiskit-machine-learning 0.9.1** (VQC on XOR, EstimatorQNN).

Speed is **only qualitatively documented**:
- "first run installs… give it a minute" (finance and ML);
- PySCF "takes a minute or two" to download, "the scan itself is fast";
- VQC training "adds a few seconds".

I could not time them myself without signing in. The engineering pattern Qollab's own polished JS showcases use is to **precompute the heavy library work offline** (e.g. Hamiltonians from qiskit-nature + PySCF), embed the results as tables, run tiny live optimizers in JS or Python, and send one small "anchor" circuit to the backend.

### Cited Findings

**Official library showcases** (Qollab team, published 2026-08-01, v1.0; code read via `api.qollab.xyz/.../versions/head`)

| Project | What runs | What the write-up says about load time | Source |
|---|---|---|---|
| Optimization & Algorithms: QUBO with QAOA | `QuadraticProgram` maxcut-2 → `MinimumEigenOptimizer(QAOA(sampler=StatevectorSampler(), optimizer=COBYLA(maxiter=50), reps=1))`, then `plot_histogram` of `result.samples` | "first run installs the optimization stack". Code silences the "docplex is not officially supported" (WASM 32-bit) warning and scipy's `SparseEfficiencyWarning` | [showcase-qaoa-qubo](https://qollab.xyz/u/qollab/showcase-qaoa-qubo); [code](https://api.qollab.xyz/api/project/id/019fbe15-b256-7ccc-8c31-1c271ab9db36/versions/head) |
| QUBO solved exactly | 3-variable QUBO, brute-force table, `MinimumEigenOptimizer(NumPyMinimumEigensolver())` | "first run installs qiskit-optimization and qiskit-algorithms" | [showcase-qubo-exact](https://qollab.xyz/u/qollab/showcase-qubo-exact); [code](https://api.qollab.xyz/api/project/id/019fbe15-b34f-7d75-b9df-987a2ad16033/versions/head) |
| Algorithms: VQE ground state | 2-qubit `SparsePauliOp`, `n_local(2,"ry","cz")`, `VQE(StatevectorEstimator(), …, COBYLA(maxiter=50), callback=…)` vs `NumPyMinimumEigensolver` | "within a few thousandths of the exact value" | [showcase-vqe-ground-state](https://qollab.xyz/u/qollab/showcase-vqe-ground-state); [code](https://api.qollab.xyz/api/project/id/019fbe14-08f9-7f16-98a6-2b2de944a42e/versions/head) |
| Nature: H₂ ground state | `PySCFDriver(atom=…)` → `GroundStateEigensolver(JordanWignerMapper(), NumPyMinimumEigensolver())` at 0.5/0.735/1.0/1.5 Å | "the first run downloads the chemistry stack (PySCF compiled to WebAssembly!), which takes a minute or two; the scan itself is fast" | [showcase-h2-ground-state](https://qollab.xyz/u/qollab/showcase-h2-ground-state); [code](https://api.qollab.xyz/api/project/id/019fbe15-b166-7c41-b15d-b47b3166daca/versions/head) |
| Finance: European call | `LogNormalDistribution(3, …)` + `EuropeanCallPricing(…).to_estimation_problem()`; draws the circuit; does **not** run IAE | "first run installs qiskit-finance, give it a minute" | [showcase-option-pricing](https://qollab.xyz/u/qollab/showcase-option-pricing); [code](https://api.qollab.xyz/api/project/id/019fbe14-0cc4-706f-89b2-f0084e2cde02/versions/head) |
| Finance: portfolio QP | `PortfolioOptimization(3 assets, budget=2).to_quadratic_program()` → exact eigensolver | "first run installs qiskit-finance" | [showcase-portfolio-opt](https://qollab.xyz/u/qollab/showcase-portfolio-opt); [code](https://api.qollab.xyz/api/project/id/019fbe14-0daa-7c44-9c0c-9a9fd7dc4ff7/versions/head) |
| ML: VQC on XOR | `VQC(zz_feature_map(2), real_amplitudes(2), COBYLA(maxiter=30))` on 4 points; unseeded ("If an unlucky optimization run scores below 1.00, simply run again") | "installing qiskit-machine-learning on first run takes a minute; training adds a few seconds" | [showcase-vqc-xor](https://qollab.xyz/u/qollab/showcase-vqc-xor); [code](https://api.qollab.xyz/api/project/id/019fbe15-af71-707c-b9b6-6f85824caf7f/versions/head) |
| ML: EstimatorQNN | 1-qubit QNN with `QMLEstimator()` from `qiskit_machine_learning.primitives` and `ParamShiftEstimatorGradient` | "first run installs qiskit-machine-learning" | [showcase-estimator-qnn](https://qollab.xyz/u/qollab/showcase-estimator-qnn); [code](https://api.qollab.xyz/api/project/id/019fbe14-0eab-7a8a-abb5-06d3663ebd5b/versions/head) |

**How the presets are installed**
- The API field `code_framework_version_flags` differs by preset: QAOA 25, exact QUBO 24, VQE 9, H₂ 32, finance 64/65, ML 129. — [Qollab project API](https://api.qollab.xyz/api/project/id/019fbe15-b256-7ccc-8c31-1c271ab9db36/versions/head)
- The editor's Libraries list adds these exact lines to `requirements.txt`:
  - `qiskit-algorithms==0.4.0`
  - `qiskit-optimization==0.7.0`
  - `qiskit-nature==0.8.0` and `pyscf>=2.14.0,<3.0.0`
  - `qiskit-finance==0.4.1`
  - `qiskit-machine-learning==0.9.1`

  Qiskit is always installed (`qiskit>=2.5.2,<3.0.0`).

  — [Qollab docs: Runtime environment](https://qollab.xyz/learn/docs/runtime-environment)

**Polished JS showcases precompute and run small**
- **H₂ bond-length slider:** "The qubit Hamiltonians (STO-3G basis, parity mapping, 2-qubit reduction) were precomputed with qiskit-nature + PySCF for 14 bond lengths and are embedded as a table of Pauli coefficients".
  - A 4-parameter Ry+CX ansatz is optimized by coordinate descent in JS ("milliseconds") against exact diagonalization and Hartree–Fock.
  - "Run optimized ansatz on backend" sends one 2-qubit circuit.
  - — [quantum-chemistry-showcase-t-2](https://qollab.xyz/u/qollab/quantum-chemistry-showcase-t-2); [code](https://api.qollab.xyz/api/project/id/01a05dad-14fe-731e-8630-11f70a85d26d/versions/head)
- **Quantum kernel showcase:**
  - A 2-qubit ZZ feature map runs as a ~30-line JS statevector. It builds a 60×60 training kernel, a ridge classifier solved by Gaussian elimination, and the decision boundary on a grid, all live.
  - A crossfade to a classical RBF boundary illustrates "on toy data they both work, which is the honest lesson".
  - The data is seeded (`mulberry32(11)`), and a 200-shot anchor circuit is sent via `await backend.run(_c,{shots:200})` inside try/catch.
  - — [quantum-kernel-showcase-drag-t](https://qollab.xyz/u/qollab/quantum-kernel-showcase-drag-t); [code](https://api.qollab.xyz/api/project/id/01a05db7-6721-74e1-89c2-466ca6c669d2/versions/head)

**What the wheels contain** (own inspection of PyPI wheels, 2026-10-09)
- qiskit-optimization 0.7.0 **vendors its own** `minimum_eigensolvers` (QAOA, VQE, SamplingVQE, NumPyMinimumEigensolver, diagonal estimator) and `optimizers` (COBYLA, Nelder–Mead, SPSA, SciPy wrapper). It depends on `docplex` and `networkx`, not on qiskit-algorithms.
- Each library has its **own** `utils/algorithm_globals.py`: qiskit_algorithms, qiskit_optimization and qiskit_machine_learning.
- qiskit-algorithms and qiskit-machine-learning both ship `P_BFGS`, which uses `multiprocessing`.
- qiskit-machine-learning 0.9.1 kernels: `FidelityQuantumKernel`, `FidelityStatevectorKernel`, and trainable variants. It requires `scikit-learn>=1.2`, `dill`, `setuptools`.

— [PyPI qiskit-optimization 0.7.0](https://pypi.org/pypi/qiskit-optimization/0.7.0/json); [PyPI qiskit-machine-learning 0.9.1](https://pypi.org/pypi/qiskit-machine-learning/0.9.1/json); [PyPI qiskit-algorithms 0.4.0](https://pypi.org/pypi/qiskit-algorithms/0.4.0/json)

**IonQ noise-model simulation facts** (for cached-result fallbacks)
- Noise models: `forte-1` and `forte-enterprise-1` (current); `aria-1` and `aria-2` (QPUs retired); `harmony` retired (Jul 2025).
- Selection: `backend.run(qc, shots=…, noise_model="forte-1")`, or a backend option with `sampler_seed` (integer from 1 to 2^31; otherwise returned in the job output).
- Limits: Forte-class and ideal ≤ 29 qubits; Aria ≤ 25.
- The model is depolarizing per gate type, with each shot simulated separately. **Debiasing is not included** in noisy simulation.
- The models were updated in Sept 2025, with newer docs "in preparation". They "should not be used to predict" whether a system can run a circuit.

— [IonQ docs: Simulation with noise models](https://docs.ionq.com/guides/simulation-with-noise-models)
- One-job rule: "Pass every circuit the run needs to a single `backend.run` call… The same rule covers the Estimator wrapper." — [Qollab docs: Runtime environment](https://qollab.xyz/learn/docs/runtime-environment)

**Visualization libraries** (GitHub API and npm, 2026-10-09)

| Library | License | Version (npm) | Main bundle size | Notes |
|---|---|---|---|---|
| Plotly.js | MIT | `plotly.js-dist-min` 4.1.2 | v3.1.1 `plotly.min.js` 4.83 MB | Heavy |
| Chart.js | MIT | 4.5.1 | ~208 KB UMD min | — |
| uPlot | MIT | 1.6.32 | ~145 KB | — |
| deck.gl | MIT | — | — | — |
| D3 | ISC | 7.9.0 | 280 KB min | — |
| Observable Plot | ISC | 0.6.17 | 209 KB min | — |
| Leaflet | **BSD-2-Clause** | 1.9.4 | 148 KB min | — |
| OpenLayers | BSD-2-Clause | — | — | — |
| MapLibre GL JS | **BSD-3-Clause** | 6.13.0 | — | — |
| Vega-Lite | BSD-3-Clause | — | — | — |
| ECharts | Apache-2.0 | — | — | — |
| Highcharts, ApexCharts | non-OSI / NOASSERTION | — | — | — |
| Chart2Music | MIT | 1.20.0 | — | — |

— [GitHub API repos](https://api.github.com/repos/Leaflet/Leaflet); [npm registry](https://registry.npmjs.org/maplibre-gl/latest); [jsDelivr package API](https://data.jsdelivr.com/v1/packages/npm/plotly.js-dist-min@3.1.1?structure=flat)
- **MapLibre GL JS uses web workers.** The worker is "laundered through a same-origin Blob URL", and the CSP guidance requires `worker-src` allowance. — [MapLibre GL JS docs](https://maplibre.org/maplibre-gl-js/docs/)
- **Qollab blocks workers** (`worker-src 'none'`; from prior notes). — [qollab.xyz/jsworker.html CSP](https://qollab.xyz/jsworker.html)

### Inferences

**Speed expectations** (inferred; measure on day 1)
- Qiskit's application libraries are pure Python on top of Qollab's Qiskit/NumPy/SciPy build. Timing is dominated by first-run package download and import (tens of seconds to ~2 minutes per Qollab's own wording), then by statevector cost (see the einsum table in the prior notes).
- Tiny problems (≤ 10 qubits, ≤ 100 optimizer evaluations) should finish in seconds.
- Each QAOA/VQE iteration is one or a few statevector simulations. At ≤ 12 qubits that is ~ms per gate layer, so 50–200 COBYLA iterations at 8–12 qubits should take seconds to tens of seconds.
- At 16–20 qubits, expect minutes. **Do not do optimizer loops live at ≥ 16 qubits.**
- `FidelityStatevectorKernel` builds an N×M kernel from N + M statevectors (not N·M circuits). That makes it the only practical in-browser kernel for N ≈ 100–300 at ≤ 10 qubits.
- `FidelityQuantumKernel` with a sampler runs N·M fidelity circuits, which is too slow live and must not go to IonQ as one job per pair.
- PySCF in WASM: the first download is ~1–2 minutes, and HF/FCI for H₂, LiH or H₂O in STO-3G should be seconds after that. Still, **precompute Hamiltonians offline and ship the Pauli tables** as the official slider does.
- `docplex` warns about WASM/32-bit. Large `QuadraticProgram`s through docplex may be slow; build `QuadraticProgram` directly or via `from_ising` for speed.

**Hybrid workflow under one-job-per-run** (recommended architecture)
1. **Offline (local Qiskit 2.5 + qiskit-optimization/ML/nature; full CPU):**
   - Run hyperparameter search, optimizer training (QAOA angles, VQE/VQC parameters) and multi-seed statistics.
   - Run the classical baselines (Gurobi/HiGHS/OR-Tools/sklearn) and scaling sweeps. Use Aer noise models plus the IonQ `forte-1` cloud simulator if you have API access.
   - Save everything to `data/*.json` (≤ 2 MB each, read by literal path), including seeds, versions and dates.
2. **In-browser live layer (fast, deterministic):**
   - Reload the shipped parameters.
   - Re-evaluate the final circuits exactly with `Statevector` (≤ 12 qubits live) to reproduce the headline numbers in front of the judge.
   - Run the baselines live where cheap (brute force ≤ 20 variables, sklearn SVM), so the comparison isn't just a static table.
   - Optionally run a short warm-started optimizer (≤ 20 iterations).
3. **Exactly one backend job:**
   - Either pass a **list of circuits** to one `backend.run([...])` (the documented rule), or pack small circuits side by side on disjoint qubits of one ≤ 20-qubit circuit (the Soundtrack pattern), decoding with bit shifts.
   - Prefer the list: it keeps shot statistics independent and avoids implying crosstalk-free hardware. Use packing only to cut per-circuit overhead on IonQ.
   - Use one `BackendEstimatorV2` call with all PUBs if you need expectation values.
   - Wrap it in try/catch; on failure, show the cached `forte-1` result (labelled with date, noise model, shots and seed) and the ideal result.
4. **Seeds:**
   - Set `algorithm_globals.random_seed` in **each** of the three libraries you import.
   - Pass `seed` to `StatevectorSampler`/`StatevectorEstimator`, `seed_simulator` to BasicSimulator/Aer runs, `seed_transpiler` to transpiles, and `sampler_seed` to IonQ noise-model runs.
   - Seed NumPy `default_rng`, and use a JS PRNG (mulberry32) for any JS-side randomness.
   - Note that the official VQC showcase is unseeded and tells users to rerun. Do better.
5. **Avoid `P_BFGS`** (multiprocessing) and anything using `parallel_map`. COBYLA, SPSA, Nelder–Mead and L-BFGS-B via SciPy are fine.

**Visualization recommendation under Qollab's constraints**
- **Charts:** Plotly.js (MIT) gives the richest interactive scientific charts (error bars, log axes, hover), but costs ~4.8 MB on first load. Chart.js (MIT, ~0.2 MB) or uPlot (MIT, ~0.15 MB) are lighter. D3 (ISC) works for custom scaling and Pareto plots, and QCFlows already uses it.
- **Maps:** MapLibre GL needs workers, so it will almost certainly fail in Qollab. Plotly's MapLibre-based `scattermap` traces should fail for the same reason. Plotly `scattergeo` and D3-geo use no workers and are MIT/ISC.
- **Leaflet** (no workers) works technically with OSM raster tiles (`img-src *`), but it is **BSD-2-Clause**. Under a strict reading of "outside repos must be MIT", ask organizers. Plotly scattergeo or D3-geo are the MIT/ISC-safe alternatives.
- **Accessibility:** pair every chart with a data table (or `<details>` table) and an `aria-live` summary sentence ("Quantum hybrid: 0.91 ± 0.03 approximation ratio vs greedy 0.95 ± 0.01; threshold 0.90 met"). Use Okabe–Ito colors and redundant markers, and optionally Chart2Music (MIT) sonification.
- **Recommended dashboard layout:**
  1. problem card (stakeholder, dataset citation, instance size);
  2. "pre-registered thresholds" card;
  3. results table with CIs and pass/fail badges;
  4. quality-vs-size scaling plot with the classical baseline;
  5. "this run" vs "cached IonQ Forte noise model" vs "ideal" source toggle;
  6. "Estimate at scale" (qsharp-lang) panel;
  7. limitations.

### Gaps
- **No measured Qollab timings** for library install/import or algorithm runtimes. Reading required no sign-in, but running would require using the platform, which was out of scope.
- I couldn't confirm whether presets are cached across runs in the same session.
- The `code_framework_version_flags` mapping (likely 1 = Visualizations, 8 = Algorithms, 16 = Optimization, 32 = Nature, 64 = Finance, 128 = ML) is my inference from the values, not documented.
- I didn't verify whether `FidelityStatevectorKernel` or `qiskit_machine_learning.primitives.QMLEstimator` have Pyodide-specific issues beyond what the showcases exercise.
- Not verified:
  - Plotly 4.x's default `topojsonURL` (where scattergeo fetches base maps);
  - whether Plotly works in Qollab's frame via `+esm`;
  - Leaflet's behaviour inside the sandbox (Referer handling for OSM tiles).
- The IonQ noise-model docs do not document the post-Sept-2025 Forte model in detail. Whether Qollab's IonQ remote simulator honours `noise_model` or `sampler_seed` options passed through `backend.run` is unverified.
