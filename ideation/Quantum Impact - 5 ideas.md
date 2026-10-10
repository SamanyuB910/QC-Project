# Quantum Impact: five ideas, one decision

*Written Fri Oct 9, 2026, 20:50 ET. The build window opened at 19:00 ET and the deadline is Sun Oct 11, 19:00 ET, about 46 hours away. The datasets below were downloaded and checked between 20:39 and 20:49 ET. The calibration numbers come from scratch scripts in `ideation/calibration/`.*

> **Update, Sat Oct 10, 01:15 ET (from the organizers' Discord):**
> - **One project, two submissions.**
>   - (1) **Qiskit Fall Fest / QCA:** a public **GitHub repo** plus the **demo video**, through QCA's form. QCA pays local prizes directly; there is no global round.
>   - (2) **Qollab × IonQ:** the Qollab project page plus video, under Qollab's rules.
>   - Keep the GitHub repo **MIT-licensed** and identical to the Qollab code.
> - **"Create one project based on our prompts."** QCA has a prompt list that is not on the GT site (checked 01:03 ET). Get it from Discord and check that the chosen idea maps to one of the prompts.
> - **IonQ submissions must run through IonQ's simulators**: the Forte 1 / Forte Enterprise 1 noise models, 29 qubits, free. These accept **one job per run**, and they simulate each shot separately. Consequences for idea #1:
>   - **Batch every window into one `backend.run`**, or pack two 12-qubit windows side by side in one 24-qubit circuit.
>   - **Keep shots in the hundreds.**
>   - **Use p=1 QAOA.** Re-test, noiseless, instance 54: the QAOA ÷ independent-choice ratio is still a median of 1.69× at p=1 (1.63× at p=2, 1.71× at p=3). At p=1 a window is about 26–59 two-qubit gates, which is roughly 0.75–0.88 fidelity at 0.5% error, so expect the gain to shrink toward about 1.2–1.5×. Measure it on `forte-1`.
>   - **Use `backend.run` + counts, not `BackendSamplerV2`**, which returns zeros on IonQ.
>   - Still test on the built-in simulator.
>
> **Check first:** Qollab registration closed Oct 8 at 11:00 ET. If you are not registered on a team at the Georgia Tech node, none of this applies.
> Quantum Impact is a **theme**, not a track. The tracks are Student and Professional. You declare the theme on the project page and can change it until the deadline. One Impact entry has three ways to win something: a placement, the **Most Impact** award, and **Best of Quantum Impact**.

---

## 1. The decision

**Build "Tomorrow's Photo Plan": the quantum step repairs one tangled group of an Earth-observation satellite's daily photo plan at a time, tested on the real CNES SPOT5 benchmark.**

The overnight calibration supports this choice over the other four:

- It is the only candidate whose cost function converts to a QUBO **exactly**, with no approximation (penalty terms reproduce the hard constraints exactly).
- It showed the clearest gain from quantum correlations over a classical sampler that matches each choice's probability but makes the choices independently.
- Space is a sector the brief names, and no Qollab project touches it.
- The classical baseline is exact and verified.

### How the five were ranked

The weights are deliberately unequal. **Shippability ×3**: an unfinished project scores nothing, and in 46 hours ambition is the usual killer. **Tutorial-bar clearance ×2** and **honest measurable difference ×2**: these are the two ways an Impact entry gets zeroed or discounted. **Judge experience ×1.5** and **impact legibility ×1.5**: these matter, but a good README can partly fix them. The maximum is 50.

| Rank | Idea | Sector | Tutorial bar (×2) | Ship (×3) | Judge (×1.5) | Legible (×1.5) | Honest diff (×2) | **Score** | Class | Build h |
|---|---|---|---|---|---|---|---|---|---|---|
| **1** | **Tomorrow's Photo Plan**: quantum improvement step for SPOT5 satellite photo scheduling | Space | 5 | 4 | 5 | 4 | 5 (measured) | **45.5** | A | ~28 + 6 docs |
| 2 | **Commit & Dispatch**: which power plants to run for 2 hours, on the RTS-GMLC test grid | Energy | 4 | 4 | 5 | 5 | 3 (measured, mixed) | **41.0** | A | ~30 + 6 |
| 3 | **Sensor Shortlist**: choosing which jet-engine sensors to keep for health monitoring (C-MAPSS) | Aerospace / manufacturing | 3 | 5 | 5 | 4 | 3 (untested) | **40.5** | A (weakest novelty) | ~22 + 6 |
| 4 | **Qopula Energy Stress**: a quantum model of how oil, gas and rate moves move together, for tail risk | Finance / energy | 4 | 4 | 4 | 4 | 3 (untested; parity likely) | **38.0** | A | ~24 + 6 |
| 5 | **Quantum Nested Dissection**: reordering sparse engineering matrices to save solver work (SuiteSparse) | Manufacturing | 5 | 2 | 4 | 4 | 3 (untested) | **34.0** | A, borderline B | ~34 + 6 |

---

## 2. Recommendation in full: Tomorrow's Photo Plan

| Field | Content |
|---|---|
| **Name** | Tomorrow's Photo Plan |
| **The real problem** | Each day, SPOT5's mission planners at CNES (the French space agency) decide **which candidate photographs the satellite takes tomorrow, and with which instrument**. Each photo has a priority weight and up to three ways to shoot it across three instruments. Hard constraints forbid overlapping shots and too-short transition times on the same instrument, and cap the instantaneous telemetry data flow (pairwise and three-way forbidden combinations). The goal is the admissible subset with maximum total priority. |
| **Public dataset** | **SPOT5 daily photograph scheduling benchmark** (Bensana, Lemaître & Verfaillie 1999), generated by CNES's order-book simulator. Mirror: Wei & Hao 2021, **CC BY 4.0**, 21 instances, 633 KB zip. Page: https://data.mendeley.com/datasets/2kbzg9nw3b/1. Direct file URL from the Mendeley public API: `https://data.mendeley.com/public-files/datasets/2kbzg9nw3b/files/5d047c47-1625-4943-9ed0-ce82300fd67c/file_downloaded`. **Downloaded and parsed Oct 9, 20:41 ET.** Ship the plain-text `.spot` files for 54, 404, 503 and 408 (5–41 KB each). A local copy is in `ideation/calibration/data/spot5/spot5.zip`. |
| **Classical baseline** | Four tiers. **(a) Exact:** a mixed-integer linear program (MILP) via `scipy.optimize.milp` (HiGHS). Verified locally on the instances without a memory-capacity limit (table below), and every result matches the published optima. **(b) Rule-of-thumb:** priority-weight greedy. **(c) Strong heuristic:** classical large-neighbourhood search (LNS), which repeatedly frees a small group of photo choices and re-solves it, using an exact window re-solve or simulated-annealing (SA) window samplers. **(d) Hybrid nulls:** the *same* LNS loop with (i) a uniform sampler and (ii) a sampler that gives each choice the same marginal probability as QAOA's output but draws them independently. Its job is to isolate what the quantum correlations add. |
| **Quantum subroutine** | The **repair step inside the LNS loop**. Around the current best plan, free a neighbourhood of 12 binary photo-option variables in the constraint graph. Encode that window **exactly** as a polynomial cost: −weights, plus penalties for forbidden pairs, forbidden triples (native 3-body terms) and at-most-one option per photo. Sample it with **fixed-schedule linear-ramp QAOA** (no optimizer loop at run time); the schedule is tuned on held-out instance-503 windows and frozen. Keep the best feasible sample. **Why this part:** windows are dense conflict graphs where the choices depend on each other ("photo A on instrument 2 only if B isn't on instrument 1"). Correlated choices are exactly what an independent sampler cannot represent. |
| **The measurable difference** | (1) **P(window optimum) per shot** for QAOA, the independent-choice sampler, uniform and SA, at **matched shots** (e.g. 128 per window), over ≥20 windows × 5 seeds, with bootstrap 95% CIs. (2) **LNS objective against total shots**, starting from the greedy plan, with the final gap to the MILP optimum. Units: priority points and % gap. **No speed claim:** the MILP finds the exact optimum in 0.01–3.7 s. |
| **Qubit count** | 12 by default. 14–16 is optional behind a flag. Calibrated windows had 20–41 two-body and 0–6 three-body terms, so about 30–50 RZZ-equivalent gates per QAOA layer. Well under the 24-qubit built-in simulator limit. |
| **Judge-run time** | **Estimate (not measured inside Qollab):** 10–30 s for the default run (instance 54, 3 windows, 128 shots each, p≈4). Parsing is under 1 s. A 12-qubit circuit with about 200 gates takes well under a second on the in-browser simulator (≈1 ms/gate at 14 qubits per our earlier Pyodide benchmark). Exact window enumeration over 4,096 states × local constraints takes about 1–3 s per window. Multi-seed statistics are precomputed into JSON and labelled as such. |
| **Tutorial-bar sentence** | No tutorial schedules a real CNES satellite order book, encodes its three-way telemetry constraints as native 3-body terms, or uses QAOA as the repair step of a classical search, checked against a classical sampler with the same per-choice probabilities. |
| **Class** | **A** |
| **Build hours** | About 28 hours of engineering plus 6 for documentation and video, for 2–4 people. Solo, use the smaller version in §10. |
| **Hour-20 shippable state** (Sat 17:00) | Published and runnable: the parser; MILP, greedy and classical-LNS results on 4 instances; project page v1; **the quantum window audit on instance 54** (P(opt)/shot against the independent-choice sampler and uniform, with CIs). Not yet: the full quantum LNS loop. |
| **Rubric read** | **Novelty:** first space project on Qollab; a native 3-body encoding; QAOA used as a repair step rather than a standalone solver. **Technical:** exact HUBO (polynomial with 3-body terms), verified exact baseline, a classical-null ablation, CIs. **Impact:** a real agency workload, a sector the brief names, aligned with IonQ's satellite work (Capella). The honest framing is a research step, not a product. **Docs:** a plain-language decision story, pre-registered thresholds, and an explicit "does not claim" section. |

### What the calibration actually showed (scratch, Oct 9, 20:40–20:50 ET)

The **exact baseline** (`scipy.optimize.milp`, local CPython) was run on every instance without a memory-capacity limit. Each optimum matches the published value:

| Instance | Photos / binaries | 2-body / 3-body constraints | MILP optimum (time) | Greedy | Greedy gap |
|---|---|---|---|---|---|
| 54 | 67 / 125 | 389 / 23 | **70** (0.01 s) | 63 | 10.0% |
| 404 | 100 / 158 | 919 / 18 | **49** (0.04 s) | 43 | 12.2% |
| 503 | 143 / 259 | 705 / 86 | **9,096** (0.04 s) | 9,085 | 0.12% |
| 42 | 190 / 304 | 1,762 / 64 | **108,067** (0.43 s) | 100,067 | 7.4% |
| 408 | 200 / 328 | 2,560 / 389 | **3,082** (0.41 s) | 2,073 | **32.7%** |
| 412 | 300 / 544 | 6,585 / 389 | **16,101** (0.31 s) | 13,074 | 18.8% |
| 28 | 230 / 346 | 6,302 / 590 | **56,053** (1.31 s) | 43,048 | 23.2% |

The **quantum window audit** used 12-qubit windows around the greedy plan, an exact HUBO, and LR-QAOA run on a NumPy statevector simulator. Each cell gives P(window optimum):

| Window | QAOA | Independent-choice sampler (same probabilities) | Uniform | QAOA ÷ independent |
|---|---|---|---|---|
| 54-w0 | 0.189 | 0.088 | 0.0010 | 2.1× |
| 54-w1 | 0.227 | 0.205 | 0.0005 | 1.1× |
| 54-w2 | 0.024 | 0.009 | 0.0002 | 2.7× |
| 54-w3 | 0.039 | 0.027 | 0.0002 | 1.4× |
| 503-w0 | 0.011 | 0.002 | 0.0002 | 5.5× |
| 503-w1 | 0.013 | 0.002 | 0.0002 | 5.1× |
| 503-w2 | 0.041 | 0.016 | 0.0002 | 2.6× |
| 503-w3 | 0.251 | 0.191 | 0.0010 | 1.3× |

**Caveat:** these are **upper bounds**. The QAOA schedule was grid-searched per window *knowing the optimum*. The project must use a schedule tuned on held-out windows (from 503) and frozen before testing on 54. Expect the ratios to shrink, and report whatever survives.

---

## 3. Build plan (Fri 21:00 → Sun 19:00 ET)

Roles for 4 people: **Q** = quantum lead, **C** = classical baselines and data, **D** = docs, video and accessibility, **V** = verification and stats. With fewer people, merge D into V and C into Q.

| Block (ET) | Hours | What | Who |
|---|---|---|---|
| Fri 21:00–23:00 | H0–2 | **Smoke tests inside Qollab.** Publish a throwaway project. `import scipy.optimize; scipy.optimize.milp`. Time a 12-qubit p=4 RZZ circuit on the built-in simulator. Read `data/54.spot` by literal path. Render one matplotlib figure. **Write the pre-registration into the README:** metrics, thresholds, instances, shots, seeds. | All |
| Fri 23:00–Sat 02:00 | H2–5 | **Classical baseline first:** parser, MILP optimum (if `milp` is missing in Pyodide, ship the optimal assignment as a certificate and verify it live), greedy, classical LNS with exact and SA window repair, on 54/404/503/408. Save `results/classical.json`. | C, V |
| Sat 02:00–08:00 | — | Sleep | — |
| Sat 08:00–11:00 | H11–14 | **Project page v1:** problem in plain language, dataset, baselines, how to run. **Publish a runnable classical-only version as a safety submission.** | D, C |
| Sat 11:00–17:00 | H14–20 | **Quantum step:** window extraction, exact HUBO → Qiskit circuit (RZ, RZZ; 3-body as CX·RZZ·CX), LR-QAOA schedule tuned **offline on 503 windows**, then frozen. Independent-choice and uniform nulls. P(opt)/shot table on instance 54. | Q, V |
| **Sat 17:00** | **H20** | **CHECKPOINT:** baselines, page and a quantum window audit that runs in under 30 s. **Update the submission.** If this isn't green, cut §10's extras and go straight to docs. | All |
| Sat 17:00–23:00 | H20–26 | Quantum LNS loop against classical LNS at matched shots. Multi-seed statistics offline → `results/*.json`. Bootstrap CIs. Figures in the Okabe–Ito colour-blind-safe palette. Optional `--big` flag for 408. Side panel: transpiled gate counts, all-to-all versus IBM heavy-hex. | Q, V, C |
| Sat 23:00–Sun 07:00 | — | Sleep | — |
| Sun 07:00–12:00 | H36–41 | **Documentation block** (scored work, not paperwork): final page, limitations, "does not claim", disclosure, accessibility pass (alt text, a data table behind every figure, no colour-only encoding). | D, V |
| Sun 12:00–15:00 | H41–44 | **Video:** record in Chrome, edit, upload a public no-sign-in link. Test Run from a fresh account on the built-in simulator and one other free simulator. | D, Q |
| Sun 15:00–17:00 | H44–46 | Final checks: MIT licence, data-licence attribution, theme = Quantum Impact, attribution line, video link opens signed out. **Submit by 17:00.** | All |
| Sun 17:00–19:00 | — | Buffer. No new features. | — |

Documentation time reserved: 3 h on Saturday morning, plus 8 h on Sunday including the video.

---

## 4. Project page outline (mixed-expertise panel)

1. **Title, one-line summary**, theme = Quantum Impact, and the line **"This effort is supported by Qollab & IonQ."**
2. **The decision, in plain language.** A satellite can't photograph everything tomorrow. Which photos should it take, and with which camera? Include one diagram of an orbit pass with conflicting requests.
3. **The data.** SPOT5 benchmark (CNES order-book simulator; Bensana et al. 1999; Mendeley mirror, CC BY 4.0). What one file contains, which instances ship, and their sizes.
4. **How to run.** Press Run. The default is instance 54 with 3 windows, about X s (measured). Explain the optional flags. Browser note: Chrome, Edge or Firefox 153+, not Safari.
5. **What we committed to before running.** The pre-registered metrics and thresholds, dated.
6. **Classical baseline.** Exact MILP (times), greedy (gaps), classical LNS. Results table.
7. **Where the quantum step sits and why.** Diagram: current plan → free a 12-option window → quantum sampler → keep best feasible → repeat. Explain why correlated choices matter here.
8. **The comparison.** Matched shots; the independent-choice and uniform nulls; CIs. Mark clearly which numbers are **precomputed** (JSON, with seeds and dates) and which are **live**.
9. **What this project does not claim.** No quantum advantage. The MILP solves these instances exactly in under 4 s. Results are from noiseless simulation. Window sizes are tiny.
10. **What would have to change for it to matter.** Real order books and constellations: hundreds to thousands of requests, multiple satellites, memory capacity limits. Windows of 50–100+ qubits at high fidelity. Where the trend would have to go (stated, not extrapolated).
11. **IonQ notes** (optional). All-to-all connectivity means no SWAPs. A 3-body term costs about 3 two-qubit gates. Transpiled gate-count table.
12. **Replicate / extend.** File map, how to swap instances, how to add the capacity-limited instances (1xxx).
13. **What existed before the build window, and AI use.** SPOT5 data; Qiskit; the calibration scripts (written with AI assistance on Oct 9 after 20:39 ET, inside the window); any forks or templates.
14. **Licences and credits.** Code is MIT. Data is CC BY 4.0 with citation. Qollab & IonQ attribution.
15. **Accessibility notes.** Alt text, data tables, colour-blind-safe palette.

---

## 5. Video beat sheet (~2:40)

| Time | Beat |
|---|---|
| 0:00–0:15 | Hook: "Every day, a satellite operator has to decide which photos to take tomorrow." Show the Run button and the result table appearing. |
| 0:15–0:40 | The problem and the CNES SPOT5 dataset: photos, three instruments, conflicts. |
| 0:40–1:05 | Classical baseline first: the exact solver needs milliseconds; greedy leaves 10–33% on the table; classical improvement search. |
| 1:05–1:40 | The quantum step: free a tangled window → 12-qubit circuit → samples → repair. Why correlations matter. |
| 1:40–2:10 | The measured comparison: P(optimum) per shot against the independent-choice sampler, with error bars; improvement-search curve. |
| 2:10–2:35 | Honest limits and what would have to change. |
| 2:35–2:40 | Attribution line and link. |

---

## 6. The other four ideas

### #2 Commit & Dispatch (energy): runner-up, with measured but mixed results

| Field | Content |
|---|---|
| Real problem | Day-ahead **unit commitment**: which generators to switch on each hour so demand plus reserve is met at least cost. Includes start-up costs and minimum outputs. |
| Dataset | **pglib-uc, RTS-GMLC instances** (73 thermal + 81 renewable generators, 48 hourly periods, demand and reserves; about 90 KB JSON each; CC BY 4.0). https://github.com/power-grid-lib/pglib-uc/tree/master/rts_gmlc. Verified Oct 9, 20:40 ET. |
| Classical baseline | Exact enumeration of the window (4,096 states) with greedy economic dispatch, which is optimal for convex piecewise costs. Industry **priority-list** rule. SA on the true cost. The full 73×48 MILP offline. |
| Quantum subroutine | QAOA proposes on/off patterns for 6 marginal units × 2 hours (12 qubits, start-up costs couple the hours). Each sample is priced by the exact classical dispatch. |
| Measurable difference | P(within 1% of optimal cost) per shot against the independent-choice null and uniform at matched shots; feasibility rate. |
| Calibration (scratch, oracle-tuned) | **Mixed.** Off-peak, QAOA beat the independent-choice sampler 1.4–2.3×. At peak hours it lost (0.42–0.85×). The priority-list rule was within 0.6% of optimal everywhere and optimal in 2 of 4 cases. The bottleneck is turning dispatch cost into a QUBO (its best solution is 1–13% off the true optimum). That diagnosis is itself the honest story. |
| Qubits / judge time | 12 / about 10–20 s (estimate). |
| Tutorial-bar sentence | No tutorial prices every quantum sample with real economic dispatch on a public 73-generator test system and isolates the quantum correlations with an ablation. |
| Class / build | A / about 30 h + 6. **Hour-20:** classical commitment, dispatch, priority list, page. |
| Rubric read | Novelty good (no grid project on Qollab); Technical good; **Impact most legible of the five**; the honest difference is weaker (quantum helps on some hours, hurts on others). |

### #3 Sensor Shortlist (aerospace / manufacturing): lowest build risk

| Field | Content |
|---|---|
| Real problem | Choose the **k of 14 informative engine sensors** to keep on a bandwidth-limited health-monitoring channel. The criterion is max relevance to remaining useful life, min redundancy (mRMR). |
| Dataset | **NASA C-MAPSS turbofan degradation** (FD001). https://phm-datasets.s3.amazonaws.com/NASA/6.+Turbofan+Engine+Degradation+Simulation+Data+Set.zip (12.4 MB zip, verified Oct 9). Ship a ≤2 MB derived CSV and state how it was derived. |
| Classical baseline | Exact enumeration of the mRMR objective over C(14,5)=2,002 subsets; greedy mRMR; SelectKBest; SA. Downstream: remaining-life prediction with `HistGradientBoostingRegressor`, nested-CV RMSE. |
| Quantum subroutine | QAOA with an **XY ring mixer** started from the greedy k-hot plan, so every sample keeps exactly k sensors. Optional 3-body conditional-mutual-information terms. Precedent: Kipu + IonQ's 2026 feature selection on Forte. |
| Measurable difference | P(optimal subset) per shot against the independent-choice null and SA at matched evaluations; downstream RMSE difference with a CI (likely within noise, so say so). |
| Qubits / judge time | 14 / about 10–20 s (estimate). |
| Tutorial-bar sentence | No tutorial picks NASA turbofan sensors with a cardinality-preserving mixer and checks the choice with a downstream remaining-life model. |
| Class / build | A (weakest novelty: feature-selection QUBOs are known) / about 22 h + 6. **Hour-20:** exact and greedy selection plus the downstream model and page. |

### #4 Qopula Energy Stress (finance): follows the template that won NQCC 2024

| Field | Content |
|---|---|
| Real problem | An energy trading or utility risk desk's **joint tail risk**: how WTI crude, Henry Hub gas and 10-year Treasury yields move together in a crisis. The output is VaR / expected shortfall of a hedged book. |
| Dataset | FRED CSVs: `DCOILWTICO`, `DHHNGSP`, `DGS10` (also `DEXUSEU`). These come from EIA and Federal Reserve sources. All downloaded Oct 9 (116–269 KB each). Example: https://fred.stlouisfed.org/graph/fredgraph.csv?id=DHHNGSP. WTI went to **−$37.63 on 2020-04-20**, so rank-transform daily *changes*, not log returns. |
| Classical baseline | Gaussian and Student-t copulas (fitted with scipy); empirical bootstrap; a classical Born machine or `BernoulliRBM`. |
| Quantum subroutine | A quantum circuit Born machine (QCBM): 3 assets × 3 bits = 9 qubits, all-to-all ZZ layers. Trained offline on exact probabilities with an MMD loss, then sampled live. |
| Measurable difference | Train 2010–2019, test 2020–2026: held-out MMD/KL, lower-tail dependence, and a 99% VaR exceedance backtest (Kupiec test), at matched parameter count. **Untested; expect parity with the t-copula and say so.** |
| Qubits / judge time | 9 / about 5–15 s (estimate). |
| Tutorial-bar sentence | No tutorial backtests a quantum copula on real energy-commodity crisis data against a Student-t copula, out of sample. |
| Class / build | A / about 24 h + 6. **Hour-20:** classical copulas, backtest and page. |

### #5 Quantum Nested Dissection (manufacturing): highest IonQ alignment, highest risk

| Field | Content |
|---|---|
| Real problem | Reordering a finite-element stiffness matrix so a sparse direct solver creates less fill-in (less memory and fewer flops). This is the CAE (computer-aided engineering) step behind IonQ's Ansys/Synopsys 12–14.6% claims. |
| Dataset | **SuiteSparse Matrix Collection**: `HB/bcsstk14` (structural, 1,806 rows), `HB/nos3`, `Pothen/mesh2e1`. Example: https://suitesparse-collection-website.herokuapp.com/MM/HB/bcsstk14.tar.gz. Verified Oct 9. |
| Classical baseline | SciPy SuperLU's COLAMD / MMD orderings; reverse Cuthill–McKee; spectral bisection; `networkx` Kernighan–Lin; exact minimum bisection at the coarse level. |
| Quantum subroutine | Balanced bisection QAOA (XY mixer) on the coarsened 12–16-node graph at the top separator, with classical recursion and refinement below it. |
| Measurable difference | Fill nnz(L+U) and flops against each ordering; P(exact bisection) per shot against the independent-choice null. Untested. |
| Qubits / judge time | 12–16 / about 20–40 s (estimate; SuperLU in Pyodide is untested). |
| Tutorial-bar sentence | No tutorial replays IonQ's engineering partitioning result on a public FEA matrix against standard orderings. |
| Class / build | A, borderline B / about 34 h + 6. **Hour-20:** classical nested-dissection pipeline and fill table only. That is thin on quantum, which is why it ranks last. |

---

## 7. Rejected (so you recognise the shape)

| Candidate | Killed by | One-line reason |
|---|---|---|
| VQE on H₂ / LiH / methanol "for batteries or drugs" | Tutorial bar (C) | A textbook circuit on a toy molecule; Qollab already has about 10 of these. |
| QAOA MaxCut / TSP / VRP "delivery routes" | Tutorial bar (C) | Qollab's Quantum Courier exists, and staff have publicly shown greedy beating it; one-hot TSP encodings blow up the qubit and gate budget. |
| Markowitz portfolio QAOA on 5–10 stocks | Tutorial bar (C) | Four Qollab projects plus a CQhack25 winner; a stock showcase. |
| Quantum classifier (QSVM/VQC) on Iris or breast cancer "for diagnosis" | Tutorial bar (C) | Our run showed parity with classical; the CQhack25 "Q-MediScan" pattern of over-claiming. |
| Grover "search the logistics database" | Tutorial bar (C) | No oracle exists for real data; a pure textbook demo. |
| qiskit-finance European option with amplitude estimation | Tutorial bar (C) | It is Qollab's own showcase; the stock circuits blow the gate budget. |
| MLAE tail-risk VaR with a lookup-table oracle | Near miss | The payoff is tabulated classically, so it demonstrates the estimator, not an end-to-end pipeline. Its noiseless 1.9× RMSE gain over Monte Carlo is real but hard to defend as "Impact". |
| Quantum reservoir forecasting of grid load | Honest-difference test | Our run: it loses to a 300-node classical echo-state network by more than 100× once shots are counted. |
| Fixed-budget SQD on N₂ bond breaking | Not buildable in time (B) | PySCF in Qollab is uncertain; the science tier needs 300+ ZZ gates; it needs a chemist. |
| Quantum CFD / HHL for aerodynamics | B / C | Needs fault tolerance; a 4×4 linear solve is tutorial-level. |
| SAR change detection with QML | Not buildable in time (B) | Loading gigabyte-scale imagery into a few qubits is the bottleneck. |
| Any IonQ-hardware or noise-mitigation centrepiece | Runtime rule / §8 | Hardware results are unscored; judges run a free noiseless simulator; queue time is pure risk. |

---

## 8. Flag back

**Datasets:**
- **Verified downloadable at 20:39–20:49 ET Oct 9:** pglib-uc RTS-GMLC JSON; the SPOT5 zip via the Mendeley API direct URL (the page's "Download All" button itself was not tested); FRED `DCOILWTICO`, `DHHNGSP`, `DGS10`, `DEXUSEU`; SuiteSparse `bcsstk14`, `nos3`, `mesh2e1`; the NASA C-MAPSS zip; UCI SECOM.
- **Not usable:** Stooq (JavaScript bot wall) and EIA's API (needs a key). Neither is used above.
- **Licences:** SPOT5 and pglib-uc data are **CC BY 4.0**, not MIT. The rules require MIT for outside *repos*. Shipping CC-BY data inside an MIT project with attribution is probably fine, but **ask in Slack**. FRED series from EIA and the Federal Reserve are public domain, but check FRED's terms for each series.

**Guesses, not calculations:**
- All judge-run times; nothing was timed inside Qollab.
- All build-hour figures.
- Gate counts for 3-body terms after transpilation.
- Ideas #3–#5's measurable differences, which are untested.
- The calibration numbers for #1 and #2 are **oracle-tuned upper bounds**, from my own NumPy simulator, not Qiskit. LR-QAOA schedule transfer between instances is untested.

**§2 rules check:**
- Everything matches the Oct 9 rules snapshot from earlier research.
- Qollab has no notebooks. Projects are `main.py`, or `index.html` + `main.js`, so read §5.1's "notebook" as "the project's default run".
- "Judges use a free local simulator": Qollab's docs say the judge picks from the free simulators. Design for the built-in one (24 qubits) and make sure the run doesn't fail on the others.
- Whether `scipy.optimize.milp` exists in Qollab's Pyodide SciPy is unverified. The fallback is a shipped optimality certificate plus the literature optimum.
- I can't confirm you're registered.

**Achievable?**
- **Team of 2–4: yes.** It is a conventional software build: a parser, MILP, LNS and a 12-qubit circuit. The Saturday 17:00 checkpoint protects you.
- **Solo: use the smaller version.** Skip the full LNS loop and submit the **window audit**: 2 instances, about 20 windows each, QAOA against the independent-choice and uniform samplers, plus the classical baselines and documentation. That alone clears the tutorial bar and fits in about 20 hours.
