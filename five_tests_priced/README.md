# Five Tests, Priced

**Which five heart tests should a clinic order, and what does each extra dollar buy? A 13-qubit QAOA answers that for five budgets at once, in a single job.**

This effort is supported by Qollab & IonQ.

*Theme: **Quantum Impact** · QCA Georgia Tech Qiskit Fall Fest 2026, Prompt B ("Heart Disease Readings") · Code, tests and history: [github.com/SamanyuB910/QC-Project](https://github.com/SamanyuB910/QC-Project)*

---

## In 30 seconds

- **Problem.** A chest-pain clinic can collect only **5 of 13** measurements. The tests have **real prices**, and some share one procedure: one treadmill ECG gives three readings. Price is therefore not a simple sum, and the obvious greedy choice is **wrong at 3 of 5 budgets**.
- **Quantum step.** There is one qubit per test and one circuit per budget. The circuit can only swap a test in for a test out, so **every sample has exactly five tests**. All five circuits go in **one job**. On IonQ through Qollab, which accepts one circuit per job, the run sends the μ = 0.2 circuit.
- **Result.** At equal numbers of evaluated panels, one 1,000-shot job finds every budget's optimal panel **98%** of the time. With IonQ's older published noise rates it is **92%**. The comparisons manage less:
  - a sampler with the same per-test odds but no correlations: **63%**;
  - simulated annealing: **55%**;
  - local search: **63%**.
  
  Both checks we registered before running **passed**. On IonQ's current Forte 1 noise model the 238-gate circuit **missed** (section 6); a probe job showed the gates run correctly there, so the cause is noise. There is **no speedup claim**: exhaustive search is exact and instant at this size.

---

## 1. The decision

A clinic sees patients with chest pain and must decide which measurements to collect. QCA's prompt asks for the five that are most informative and least redundant. We add the question a clinic actually faces: **what does each extra dollar buy?**

Tests come from procedures with real prices: Turney 1995, Ontario Ministry of Health fee schedule, Oct 1992, CAD. Three procedures yield several readings, so you pay once:

| Shared procedure | Readings it yields | Paid once | Each reading after that |
|---|---|---|---|
| Blood draw | cholesterol, fasting blood sugar | $2.10 | $5.17 / $3.10 |
| Thallium stress test | max heart rate, thallium scan result | $101.90 | $1.00 each |
| Treadmill ECG | exercise angina, ST depression, ST slope | $86.30 | $1.00 each |

History and vitals cost $1 each (age, sex, chest-pain type, resting blood pressure). A resting ECG costs $15.50 and fluoroscopy $100.90.

**The answer, as a price ladder.** These are the best five-test panels and their cross-validated AUC: logistic regression, 5×3 cross-validation on all 297 patients. This is the optimistic view, because it is the best of 1,287 panels; section 6 gives the honest held-out numbers.

| Price | Best five-test panel | What the clinic does | AUC |
|---|---|---|---|
| $9.20 | age, sex, chest-pain type, resting BP, fasting sugar | history + one blood test | 0.838 |
| $91.30 | age, sex, chest-pain type, ST depression, ST slope | history + **one treadmill ECG** | 0.875 |
| $106.90 | sex, chest-pain type, resting BP, max heart rate, thallium | history + thallium scan | 0.878 |
| $191.20 | sex, chest-pain type, resting BP, ST slope, fluoroscopy | + treadmill ECG + fluoroscopy | 0.902 |
| $293.10 | sex, chest-pain type, ST slope, fluoroscopy, thallium | + treadmill + thallium + fluoroscopy | 0.911 |

The program also draws this ladder as a figure, with a text description first.

## 2. Data and prices

- **Patients.** UCI Heart Disease, Cleveland subset: 297 patients after dropping 6 with missing values, 137 with heart disease. CC BY 4.0. Janosi, Steinbrunn, Pfisterer, Detrano 1989. See `DATA_NOTICE.md` for attribution and changes.
- **Cohort caveat.** These are **symptomatic patients referred for angiography**, not a general screening population, so read the panels as first-line triage for chest pain.
- **Prices.** Turney's cost files ship inside the same UCI archive. They are 1992 Canadian fees, used as **relative** prices.

## 3. How to run

Press **Run**. It needs no setup: the defaults are chosen per simulator, and the data and precomputed tables are in the project.

| Simulator | What happens | Typical time |
|---|---|---|
| Built-in | 6 circuits × 1,000 shots, one job | seconds |
| IonQ Forte 1 / Forte Enterprise 1 (noise models) | **One circuit** (price weight μ = 0.2) × 1,000 shots in one job: Qollab's IonQ path accepts one circuit per job | seconds to minutes |
| IBM noise models | Routed to the device lattice; 8 shots each, because per-shot noise is slow in a browser | about 1 minute |
| AWS Braket local | Same as built-in | seconds |

**Run settings:**

| Setting | Default | Meaning |
|---|---|---|
| `shots` | 0 | Shots per circuit; 0 = automatic per simulator |
| `circuits` | `auto` | `all` = 5 price points + a bit-order check in one job; `single` = one circuit |
| `single_mu` | 0.2 | Price weight used when `circuits = single` |
| `seed` | 7 | Seed for the simulator and the classical baselines |
| `run_baselines` | true | Also run simulated annealing / local search with the same number of evaluations |
| `revalidate_auc` | false | Recompute the optimal panels' AUC live with scikit-learn (adds about 3 s) |
| `show_figures` | true | Draw the two figures; each has a text description and a data table |
| `dump_counts` | false | Print the raw counts as one line of JSON, for archiving a run |

**Browsers:** Chrome, Edge, Brave, Opera or Firefox 153+. Safari cannot run Qollab projects.

## 4. Classical first

Exhaustive search over all 1,287 five-test panels is **exact and takes milliseconds**, so every claim below is checked against the true answer. The objective has five price weights μ:

f_μ(x) = −Σ relevanceᵢ·xᵢ + 0.1·Σ redundancyᵢⱼ·xᵢxⱼ + μ·price(x)/100, subject to exactly five tests

- relevance = mutual information with the diagnosis;
- redundancy = |correlation|;
- μ = 0 ignores price and μ = 0.2 makes price matter a lot.

| μ | Exact best panel | Price | Greedy | Greedy + local search |
|---|---|---|---|---|
| 0 | sex, cp, slope, ca, thal | $293.10 | 3rd best | optimal |
| 0.02 | cp, trestbps, thalach, ca, thal | $206.80 | 7th best | optimal |
| 0.05 | cp, trestbps, thalach, ca, thal | $206.80 | optimal | optimal |
| 0.1 | sex, cp, trestbps, thalach, thal | $106.90 | **26th best** | **26th best (stuck)** |
| 0.2 | age, sex, cp, trestbps, fbs | $9.20 | optimal | optimal |

### Why we changed the prompt's formula

> **Pitfalls we hit, all measured.**
> - **The penalty term.** The prompt enforces "exactly five" with P·(Σx − 5)². Every penalty you can choose without already knowing the answer makes QAOA **no better than random**: Qiskit's automatic value 3.12, and the textbook safe bound 0.395.
> - **The relevance estimate.** scikit-learn's default k = 3 nearest-neighbour estimate inflates cholesterol's relevance 4–10×. We use k = 10, averaged over 20 seeds.
> - **Fixed constants.** Two optimal panels are nearly tied, so the relevance values ship as fixed constants rather than being re-estimated on every Run.
> - **Units.** Relevance is in nats and redundancy is a correlation. With λ ≥ 0.5 the "optimal" panel includes a feature with zero information, so we use λ = 0.1.

Probability of the optimal panel per valid sample, at μ = 0, with all angles tuned **without** knowing the answer (random five-test panel = 0.00078):

| Layers | XY mixer (ours) | Penalty: Qiskit automatic | Penalty: textbook bound | Penalty: 2× smallest valid (needs the answer) |
|---|---|---|---|---|
| p = 1 | **0.0200** | 0.0008 | 0.0008 | 0.0013 |
| p = 2 | **0.0491** | 0.0008 | 0.0008 | 0.0049 |
| p = 3 | **0.0611** | 0.0008 | 0.0009 | 0.0195 |

## 5. The quantum step

```
13 qubits, one per test
  RY(2·asin√(5/13)) on each qubit           each test "in" with probability 5/13
  cost layer  exp(−iγ·f_μ / sd)            exact Ising expansion: 13 RZ, 78 RZZ, and one 3-qubit
                                            CX–RZ–CX ladder for "pay for the treadmill once"
  XY mixer    XXPlusYYGate(−2β) on all 78 pairs   swaps a test in for a test out: count never changes
  measure; keep shots with exactly five 1s  = equal superposition of all 1,287 valid panels, for free
γ = 1.7182, β = 0.1676 (one layer, frozen; tuned offline on random 80% patient subsamples, never on the answer)
```

- **One job.** The five price-weight circuits and a bit-order check circuit go in a **single `backend.run` call**. A guard object makes a second call impossible, so the run respects IonQ's one-job-per-run rule. IonQ through Qollab also rejects jobs with more than one circuit, so there the run sends one circuit (μ = 0.2).
- **Checked against an exact model on every Run.** The submitted circuit's distribution matches an exact NumPy model of the same algorithm to a total-variation distance of about 10⁻¹⁵, so a changed gate convention would be caught immediately.
- **Trapped ions vs a lattice.** On IonQ's all-to-all connectivity each circuit needs **234–238** native two-qubit gates. The same circuit routed onto a heavy-hex lattice (IBM-style) needs **750–775** CZ gates, about 3.2× more.
- **The comparison that matters.** The *independent-choice* sampler gives every test the same probability as the circuit but draws tests independently. Beating it shows the circuit's **correlations between qubits** do work, not just its per-test biases.

## 6. Results

### Prediction (printed before every job) and the classical comparison

This is the chance that **one job** finds **all four** distinct optimal panels. Equal budgets: about 22% of raw shots have exactly five tests, so 1,000 shots per circuit gives about 222 evaluated panels per price weight.

| Method | 100 shots / 22 evals | 200 / 44 | 500 / 111 | 1,000 / 222 |
|---|---|---|---|---|
| **QAOA circuit, ideal** (exact formula) | 7% | 30% | 83% | **98%** |
| **QAOA circuit, IonQ's older published noise rates** (10,000-shot reference) | 2% | 12% | 59% | **92%** |
| Independent-choice sampler (no correlations) | 0% | 3% | 26% | 63% |
| Simulated annealing (best of two schedules) | 0% | 3% | 28% | 55% |
| Random-restart local search | 0% | 1% | 20% | 63% |
| Uniform five-test panels | 0% | 0% | 2% | 11% |

*Classical rows: 200 seeded jobs, every evaluated panel counted. The noise rows use IonQ's documented legacy depolarizing rates, which are not IonQ's current model or hardware.*

### Pre-registered checks (registered Sat Oct 10, 15:00 ET; git tag `prereg`)

| # | Claim | Result |
|---|---|---|
| 1 | *(replication)* At 1,000 shots the QAOA job beats the best classical heuristic by ≥ 20 points | **98% vs 63%**: met |
| 2 | On 50 fresh 80% patient subsamples, QAOA's P(optimal panel) beats the independent-choice sampler at every price weight | **Passed.** 1.3–3.8× higher; QAOA higher in 48–50 of 50 subsamples at each μ |
| 3 | In the declared built-in run, each budget's best sampled panel is within 0.005 AUC of the best panel at that price | **Passed.** Gaps 0.000–0.002 |
| 4 | One IonQ Forte simulator run, reported as-is | **Miss.** 0 optimal panels in 193 five-test shots; the samples look like the independent-choice sampler. See below |

### IonQ Forte 1 noise-model simulator (claim 4, reported as-is)

One circuit (μ = 0.2) × 1,000 shots through Qollab, Sat Oct 10, 2026. IonQ job `01a12765-eba3-7143-8c4e-c19db91ce475`.

| | IonQ run | Ideal circuit | Independent-choice | Uniform |
|---|---|---|---|---|
| Shots with exactly five tests | 193 of 1,000 | 223 expected | n/a | n/a |
| P(optimal panel given five tests) [95% CI] | **0.000** [0.000, 0.020] | 0.021 | 0.004 | 0.0008 |
| Log-likelihood ratio, ideal vs independent | **−107.9** | +111.8 ± 15.0 | −119.2 ± 17.0 | n/a |

- **A miss.** The optimal panel never appeared, and the samples look like the independent-choice sampler, not the ideal circuit.
- **Not a bug.** A second IonQ job ran a shallow probe with known answers for every gate type we submit. All seven readings matched within noise; for example RZZ(π/2) gave 0.482 against 0.500. The main run's per-test frequencies correlate 0.66 with the ideal circuit's, and only 0.06 if the bit order were reversed. IonQ runs our gates with Qiskit's conventions.
- **The cause is noise.** Each circuit has 238 two-qubit gates. By per-sample log-likelihood, the IonQ run sits about a quarter of the way from random panels to the ideal circuit. Our Aer reference with IonQ's older published rates sits about two thirds of the way. The 92% row above is therefore optimistic for IonQ's current model.
- Raw counts and both run logs are in the GitHub repo (`docs/runs/`). If a later IonQ job fails, the program shows these counts, labelled as a cached run.

### Honest accuracy (panel re-selected on training patients, scored on unseen patients)

| Panel chosen inside each training fold by | Held-out AUC [95% CI] | Mean price |
|---|---|---|
| Cost-aware QUBO, μ = 0 | 0.889 [0.849, 0.923] | $289.94 |
| Cost-aware QUBO, μ = 0.1 | 0.868 [0.826, 0.905] | $100.61 |
| Cost-aware QUBO, μ = 0.2 | 0.827 [0.776, 0.870] | $18.95 |
| SelectKBest (mutual information), 5 tests | 0.895 [0.857, 0.928] | n/a |
| All 13 tests | 0.902 [0.865, 0.934] | $323.97 |

The honest numbers are lower than the optimistic ladder in section 1, as they should be. At the cheap end, three free history questions (age, sex, chest-pain type) already reach AUC 0.84. **The ladder's value is in the middle, where shared procedures make some upgrades nearly free.**

### Caveats

1. "Equal budgets" counts evaluated panels. A classical evaluation is a microsecond function call, so this compares **sample quality, not speed**.
2. The angles were tuned offline (60 small simulations), and that compute is not counted.
3. "All optimal panels" means four distinct panels, because μ = 0.02 and μ = 0.05 share an optimum.
4. **Noise hurts some circuits more than others.** Under the older noise rates, each circuit's chance of hitting its own optimum falls 25–56% below ideal. At μ = 0 and μ = 0.02 it drops *below* the independent-choice sampler built from the ideal circuit's odds: 0.0100 vs 0.0137, and 0.0032 vs 0.0044. Pooling the samples of all five circuits still recovers every optimum in 92% of 1,000-shot jobs.
5. **Two panels share the $206.80 price.** On the AUC ladder the program prints, the $206.80 panel (sex, cp, thalach, ca, thal; AUC 0.904) is not the μ = 0.02 optimum (cp, trestbps, thalach, ca, thal; AUC 0.902). The objective is a proxy for accuracy, not accuracy itself.

## 7. What this does not claim

- **No quantum advantage and no speedup.** With 13 tests, exhaustive search is exact and instant.
- **No clinical recommendation.** The prices are 1992 and relative, and the cohort is a referral population.
- **Not IonQ's current noise model.** The 92% figure uses IonQ's documented legacy depolarizing rates. IonQ's current Forte 1 model is harsher, and our live run there missed (section 6).

## 8. What would have to change for this to matter

- **Larger panels.** Dozens to hundreds of priced tests or biomarkers, where checking every panel stops being possible: 2ⁿ grows quickly, and C(100, 10) ≈ 1.7×10¹³.
- **Current data.** Today's prices, and prospective multi-site data.
- **Better hardware.** Deeper circuits at higher fidelity. One layer was enough here; harder instances will need more.
- **A clinical objective.** Diagnostic yield per dollar, sensitivity at fixed specificity, and delay or patient burden. Turney's files include test *delays* too.

## 9. Replicate and extend

| File | What it holds |
|---|---|
| `main.py` | The run, top to bottom: classical → circuits → prediction → one job → comparison |
| `ftp_core.py` | Data, prices, objective, exact search, exact QAOA model, independent-choice sampler, closed-form prediction |
| `ftp_quantum.py` | Circuit builder (with an exactness assertion), one-job guard, backend handling, count parsing |
| `ftp_classical.py` | Greedy, local search, simulated annealing, cross-validated AUC |
| `ftp_report.py` | Tables and accessible figures |
| `results/precomputed.json` | AUC table, evidence tables, provenance |

**To extend:**
- **Change prices:** edit `EXPENSE` and `GROUPS` in `ftp_core.py`.
- **Change k:** set `K`.
- **Add budgets:** edit `MU_GRID`.
- **Re-tune the angles** and regenerate every table with `tools/precompute.py` in the GitHub repo. The repo also has a test suite and a laptop runner (`tools/run_local.py`) that mimics Qollab.

## 10. Pre-existing work, credits and AI use

- **When it was built.** The project code was written during the hackathon window, Oct 10–11, 2026. It is ported from research scripts written Oct 9–10, also during the window.
- **Background research.** Notes from Oct 7–9, made before the window, cover the event rules and the platform; no project code comes from them. Full list: `docs/DISCLOSURE.md` in the repo.
- **Methods:**
  - QAOA: Farhi, Goldstone, Gutmann (2014).
  - Constraint-preserving XY mixers: Hadfield et al. (2019); Wang et al. (2020).
  - Trapped-ion feature-selection precedent: Kipu Quantum & IonQ (2026).
  - Mutual-information estimator: Kraskov et al. (2004), via scikit-learn.
  - Benchmarking practice: Bowles, Ahmed, Schuld (2024).
- **Libraries.** Qiskit, NumPy; optionally scikit-learn and matplotlib. No tutorial code was copied.
- **Data.** UCI Heart Disease (CC BY 4.0) and Turney (1995) test costs; see `DATA_NOTICE.md`.
- **AI use.** Code and text were produced with substantial assistance from an AI model (Anthropic's Claude), directed and reviewed by the team, who remain responsible for them. Every number above is generated by code in this project and checked by the repository's test suite.

## 11. Accessibility

- All results are plain-text tables that screen readers can read. Words like "yes/no" are used instead of colour or symbols.
- Each figure is preceded by a text description, and its numbers are printed as a table.
- Figures use the Okabe–Ito colour-blind-safe palette with distinct markers and line styles.
- The demo video has captions.

**Licence:** MIT (`LICENSE`). Data notice: `DATA_NOTICE.md`.
