# Build Prompt B: Price Every Heart Test

Build Prompt B, reframed as **"Five Tests, Priced"**. Keep QCA's relevance-minus-redundancy QUBO but fix its estimator, and add Peter Turney's real per-test prices (Ontario fee schedule, 1992) as an exact cost polynomial. The shared-procedure discounts in those prices produce one native three-body term. A 13-qubit, p = 1 QAOA with a complete-graph XY mixer then samples the whole cost-versus-accuracy frontier as **one IonQ job of five circuits (1,181 two-qubit gates)**. Of the three prompts, only B leaves a *positive*, honestly scoped quantum difference in this session's experiments. At matched pooled evaluations, the frozen circuit recovers every price-point optimum in **98% of simulated 1,000-shot jobs (94% under Forte-1 depolarizing noise)**. The classical comparators manage 63% (random-restart local search), 62% (an independent-choice sampler built from QAOA's own marginals), 55% (simulated annealing) and 10% (uniform sampling). The best honest answer for Prompt A is parity: the best tuned quantum kernel sits 0.4 points behind a tuned RBF-SVM, with a confidence interval spanning zero. Prompt C's practical difference is negative by six to nine orders of magnitude. So neither A nor C can show the "measurable difference" QCA's Impact brief asks for. B also hands judges a result a clinic can read: three $1 history questions reach AUC 0.84, one exercise ECG ($91) lifts that to 0.875, imaging ($191–207) reaches 0.90, and the best $293 panel reaches 0.911. The claim stays bounded, because exhaustive search ranks all 1,287 five-test panels in milliseconds; the result is about sampling quality, not speed. Starting at Saturday 15:00 ET (H0), the plan publishes a runnable safety version by **Sat 21:00**, which is also the last moment to switch to the runner-up (Prompt A's positive-controlled kernel audit); cuts scope at a **Sun 08:00** checkpoint; and submits both entries by **Sun 17:00**, leaving two hours of buffer. The four largest unknowns have never been tested inside Qollab: whether its IonQ path accepts a five-circuit list as one job, how long IonQ's per-shot Forte simulation takes, how IonQ's current noise model differs from the legacy depolarizing rates used here, and real in-browser timings. All four get tested in the first two hours.

## Only Prompt B leaves a positive, measured quantum gap

QCA's Quantum Impact brief has three steps: pick a public dataset, build a strong classical baseline, "then show where a quantum subroutine makes a measurable difference" ([QCA prompt slides](https://docs.google.com/presentation/d/1O5WEDQost04m8rjneB8nCuAGwgyVhckoyc87dRa8j0g); [local transcript](<../research_notes/QCA prompts Quantum Impact plan/qca_prompts_slides.txt>)). Every Georgia Tech team receives the same three prompts, so the version a team builds from the reading list is tutorial-level by construction, and Qollab's rules allow such entries to score zero on both Novelty and Technical Execution ([Qollab Rules & terms](https://qollab.xyz/programs/hackathon/terms)). This session reproduced each prompt's plain version and then a rigorous version. Each plain version fails for its own measurable reason, and the rigorous versions separate sharply on whether any quantum difference survives.

| Criterion | A: quantum-kernel QSVC, Wisconsin breast cancer | B: QUBO/QAOA, 5 of 13 heart features | C: Grover over the USGS catalog |
|---|---|---|---|
| What the plain version produces | QSVC averages 0.90–0.93 over 25 splits (single splits 0.84–0.97). It falls to 0.61–0.63, i.e. "everything benign", if angles are z-scored. | qiskit-optimization's automatic penalty (4.35, 125× what is needed) leaves the objective under 2% of the energy scale. Penalty-QAOA then hits the optimum at 0.0004–0.0024 per shot, no better than random 5-subsets. Greedy is already exact. | The IBM tutorial with a pandas filter in front. A 2026 paper has already published "3 iterations vs 5000" on USGS events. |
| Quantum vs strong classical on the real task | Parity at best: −0.4 points vs RBF-SVM (Nadeau–Bengio CI −1.8 to +1.0). A kernel with no entanglement ties the entangled ones. | **Positive at matched evaluations:** all price-point optima recovered in 98% / 94% (ideal / Forte-1 depolarizing) of 1,000-shot jobs. Classical comparators: 63%, 62%, 55%, 10%. | 2.3× fewer predicate checks at N = 64 when ideal (7.1 vs 16.4). But an index needs about 10 rows, the USGS server answers in under 1 s, and Grover loses under noise from n = 6–7. |
| Impact legibility | Tumour diagnosis reads well, but classical models already score 97–98%, so the deliverable is an audit, not a better test. | Literal: what each extra dollar buys a chest-pain clinic, priced from a published fee schedule. | Weak: the seismologist's "expensive" check is a cheap two-column filter. |
| IonQ one-job and noise fit | A 60-circuit projected-kernel job fits (about 4.5k gates). But 1,000 shots cost 6–13 points of accuracy, and training on exact features then testing on shot data collapses to 0.59–0.72. | 5 circuits, 13 qubits, 1,181 RZZ in one job. Noise costs 4 points of frontier recovery. | A 10–12-circuit sweep fits. The honest oracle only fits at n = 3, k ≤ 1. Grover equals random guessing by n = 8. |
| Judge-run time | 2.15 s native prototype; about 7–25 s in the browser (estimate). | About 5–20 s in the browser after packages load (estimate). | 1–5 s for the sweep. The honest 18–21-qubit oracle takes 45–420 s to simulate, so it cannot run live. |
| Build hours and ready assets | 10–14 h for the core. Numerics and a judge-path prototype exist. | About 18 h of engineering plus 6 h of docs. A verified circuit recipe and every baseline exist as scripts. | About 28 h. The oracle compiler and BBHT code exist. |
| Weighted score (ideation weights; my scoring) | 39 / 50 | **43.5 / 50** | 28.5 / 50 |

Sources for the table: [Prompt A notes](<../research_notes/QCA prompts Quantum Impact plan/prompt_a_quantum_kernel.md>), [Prompt B notes](<../research_notes/QCA prompts Quantum Impact plan/prompt_b_feature_selection.md>) and [Prompt C notes](<../research_notes/QCA prompts Quantum Impact plan/prompt_c_grover.md>).

**The weighted score** reuses the earlier ideation's weights: shippability ×3, tutorial-bar clearance ×2, honest difference ×2, judge experience ×1.5, legibility ×1.5. Per-criterion scores, in that order:

| Prompt | Ship | Tutorial | Honest diff | Judge | Legible |
|---|---|---|---|---|---|
| A | 5 | 4 | 2 | 4 | 4 |
| B | 4 | 5 | 4 | 4 | 5 |
| C | 3 | 4 | 2 | 3 | 2 |

These are judgement calls, but the ranking does not depend on the weights: A wins only on shippability, while B leads or ties on every other criterion.

**Prompt A is a rigorous "no".** Setup: 5 repeats × 5-fold nested CV, with scaling and PCA fitted inside every fold. Under it, logistic regression on all 30 features reaches **0.977** and RBF-SVM **0.974** (AUC 0.994). Every properly tuned quantum kernel lands at 0.955–0.972. The plain QSVC loses 5.6, 7.4 and **31.6 points** at 4, 8 and 12 qubits ([Prompt A notes](<../research_notes/QCA prompts Quantum Impact plan/prompt_a_quantum_kernel.md>)).

The session also built a strong instrument. Its auditor combines geometric difference, task alignment and concentration. It answers "no edge" on the real labels, yet detects quantum wins of **+25 to +46 points** on engineered labels, and it predicted the winner on 6 of 7 fresh label sets. That is excellent science, but it answers the prompt's question with "quantum similarity adds nothing here". A rigorous 2026 nested-CV study already reached that conclusion on the same dataset ([Kakavand et al. 2026](https://arxiv.org/abs/2604.18837)), and broader benchmarks find the same pattern ([Bowles, Ahmed, Schuld 2024](https://arxiv.org/html/2403.07059v1)). An Impact panel will read a parity result as a strong Technical Execution score but a weak Impact Potential score.

**Prompt C is worse for this theme.** The tutorial's list oracle is circular: it is built from the indices of the matching events, so whoever built it already evaluated the predicate on every event. An honest oracle that loads each event's raw depth and magnitude bits costs about b·N two-qubit gates *per call* (b = bits per event). Under the black-box metric, BBHT finds a match in **7.10 [6.94, 7.26]** predicate evaluations against 16.38 [15.93, 16.86] for a random scan over 3,000 real 64-event windows. But a B-tree index needs about 10 rows, and the USGS service returned the exact count of shallow M≥6 events in 669 ms ([Prompt C notes](<../research_notes/QCA prompts Quantum Impact plan/prompt_c_grover.md>); [USGS FDSN](https://earthquake.usgs.gov/fdsnws/event/1/)). Even fault-tolerantly, with Babbush et al.'s 170 µs Toffoli ([Babbush et al. 2021](https://arxiv.org/abs/2011.04149)), the session's crossover model puts break-even for an expensive black-box check at about **6.6×10¹¹ items**, against 155,899 events of all magnitudes in the whole 2024 catalog ([c09 results](<../research_notes/QCA prompts Quantum Impact plan/scripts/prompt_c/results_c09_ft_crossover.txt>)). The notes' own verdict is that C belongs in Quantum Unlocked.

**Prompt B starts as tutorial-trivial but becomes non-trivial once it is made honest.** Read literally, the prompt's QUBO is solved exactly by greedy mRMR. Its units clash (mutual information in nats against correlation in [0, 1]), so for λ ≥ 0.5 the "optimal" panel includes fasting blood sugar, whose MI is 0.0000, and ranks 669th of 1,287 by cross-validated AUC. Its default k = 3 MI estimator also inflates cholesterol's relevance 4–10×. The plain library path is impractical in the browser too: `MinimumEigenOptimizer(QAOA(StatevectorSampler()))` needed **206 s per sampler call at 11 qubits**, and at 13 qubits it reached 6.4 GB without finishing one optimizer run ([Prompt B notes](<../research_notes/QCA prompts Quantum Impact plan/prompt_b_feature_selection.md>)). Two changes fix the instance. A **debiased estimator (k = 10 MI, λ = 0.1)** raises the rank correlation between the QUBO objective and downstream AUC from 0.41 (the prompt's default estimator at λ = 0.2) to **0.91**. **Turney's real test costs** then break greedy, which is optimal at only 2 of 5 price points and ranks 3rd, 7th and **26th** at the others ([s10d log](<../research_notes/QCA prompts Quantum Impact plan/scripts/prompt_b/results/s10d_log.txt>)). That gap is exactly where a sampler has a job to do, and where the measured quantum edge over classical heuristics at matched evaluations appears.

## "Five Tests, Priced" turns the prompt's QUBO into a clinic's price ladder

### Checklist: what changes on top of the plain Prompt B

The plain version is the slide formula with a penalty term, QAOA via `MinimumEigenOptimizer`, and an approximation ratio. Each change below is detailed in the section named.

| # | Change | Plain Prompt B does | We do instead | Detailed in |
|---|---|---|---|---|
| 1 | **Real test prices** | No cost anywhere, even though the prompt asks for a "cheap" test | Turney's per-test fees (Ontario fee schedule, 1992; ships in the UCI zip under `costs/`) | Specification → Costs |
| 2 | **Shared-procedure discounts** | — | One blood draw {chol, fbs}, one thallium test {thalach, thal}, one treadmill ECG {exang, oldpeak, slope}: pay once per procedure | Specification → Costs |
| 3 | **Exact cost polynomial with one 3-body term** | Quadratic only | cost(x) = Σdᵢxᵢ + OR-terms. The treadmill group becomes one cubic term (a CX–RZ–CX ladder), checked on all 8,192 subsets | Specification → Costs, Quantum subroutine |
| 4 | **Price ladder (five price weights μ)** | One answer | μ ∈ {0, 0.02, 0.05, 0.1, 0.2}, giving the best panel at each budget | Specification → Objective; the clinical ladder |
| 5 | **Better relevance estimate** | sklearn's default kNN mutual information (k=3), which inflates cholesterol 4–10× | kNN mutual information with k=10, averaged over 20 seeds | Specification → Objective; why plain B fails |
| 6 | **λ = 0.1** | λ unspecified; at λ ≥ 0.5 the "best" panel includes a zero-information feature | λ = 0.1. Rank correlation between the objective and downstream AUC rises from 0.41 to 0.91 | Specification → Objective |
| 7 | **Drop the penalty term** | P(Σx−k)². The auto-penalty of 4.35, or a 1e5 fallback, swamps the objective, so QAOA does no better than random | No penalty. The constraint is enforced by the mixer. **Independent re-check (Sat 14:00–14:40, `scripts/penalty_check/`, simulators match Qiskit to 1e-15):** at p = 1–6, QAOA finds the optimum exactly at the random rate (0.0008) with any P chosen without knowing the answer, meaning Qiskit's 4.35 or the textbook single-flip bound (0.39–0.67). A penalty works only within about 2× of the smallest valid P, and finding that value means solving the problem first. Even then, at equal depth it trails the XY mixer: P(opt given feasible) at p = 1/2/3 is 0.0012/0.0033/0.011 against 0.015/0.033/0.048. At equal two-qubit-gate count, an oracle-tuned penalty catches up; report this honestly. | Pitfalls box (page §7) |
| 8 | **XY mixer** | Standard X mixer, so many invalid samples | Complete-graph `XXPlusYYGate` mixer (78 gates). Every sample keeps exactly 5 tests | Specification → Quantum subroutine |
| 9 | **Free 5-of-13 start** | — | RY(2·asin√(5/13)) on every qubit, then keep only samples with exactly five 1s. This equals a Dicke-state start at zero two-qubit cost (about 22% of shots kept) | Specification → Quantum subroutine |
| 10 | **Frozen angles, p = 1** | COBYLA optimizer loop (206 s per sampler call at 11 qubits) | (γ, β) = (1.7182, 0.1676), tuned offline on held-out subsamples. No optimizer runs when the judge presses Run | Specification → Quantum subroutine; Assumption 6 |
| 11 | **One IonQ job** | Many jobs | 5 circuits in one `backend.run([...])`, read with `get_counts(i)`. 1,181 RZZ in total | Specification; Assumption 1 (fallback: run only μ=0.1) |
| 12 | **Exact answer** | Approximation ratio against an unchecked optimum | Exhaustive enumeration of all 1,287 panels (milliseconds) as ground truth | Specification → Classical baselines |
| 13 | **Classical baselines** | Often none | Greedy mRMR (wrong at 3 of 5 prices), greedy + swap, simulated annealing, random-restart local search, uniform | Specification → Classical baselines |
| 14 | **Independent-choice sampler** | — | QAOA's own per-test probabilities, sampled independently. Isolates what qubit correlations add | Measured difference |
| 15 | **Matched budgets** | — | Every method gets the same number of evaluated panels | Measured difference (headline table) |
| 16 | **Accuracy check** | — | Cross-validated AUC for every frontier panel. Compare to all 13 tests, the ESC age/sex/chest-pain triplet, SelectKBest and L1-logistic | Clinical ladder |
| 17 | **Strict accuracy** | — | Feature selection re-run inside each CV fold (0.868 at about $101) | Clinical ladder (honest table) |
| 18 | **Noise check** | — | Forte-1-rate depolarizing noise (94% / 66%), plus a cached IonQ Forte run. Use p=1, since p=2 is worse under noise | Measured difference; Assumption 3 |
| 19 | **Honesty box** | Often claims advantage | Print the four caveats and "does not claim": exhaustive search is exact and instant at 13 features | Measured difference (caveats); page §10 |

### The specification

| Field | Specification |
|---|---|
| **Name** | Five Tests, Priced: a cost-aware heart-test panel frontier, sampled in one IonQ job |
| **Problem** | A chest-pain clinic can collect only 5 of 13 measurements per patient. The tests have real prices, and three groups share a procedure: blood draw {chol, fbs}; thallium/exercise {thalach, thal}; exercise ECG {exang, oldpeak, slope}. Prices are therefore not additive. Output: the best five-test panel at each price point, i.e. a cost-versus-accuracy frontier. The cohort is a symptomatic angiography-referral population ([Detrano 1989](https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:2756873%20AND%20SRC:MED&resultType=core&format=json)), so call it a "first-line triage panel", not population screening. |
| **Dataset** | UCI Heart Disease, Cleveland processed file: **297 complete rows** (160 without disease, 137 with), label = num > 0, CC BY 4.0, cite Janosi, Steinbrunn, Pfisterer and Detrano (1989) ([UCI dataset 45](https://archive.ics.uci.edu/dataset/45/heart+disease)). Ship `heart_cleveland_297.csv` (19 KB). It cannot be fetched live: the legacy URL returns 404, and the current files send no CORS header. |
| **Costs** | Turney's `costs/` files from the same UCI zip: Ontario Ministry of Health fee schedule, Oct 1 1992, Canadian dollars, to be presented as *relative* costs ([Turney 1995](https://arxiv.org/abs/cs/9503102)). The exact form is cost(x) = Σ dᵢxᵢ + 2.10·OR(chol, fbs) + 101.90·OR(thalach, thal) + 86.30·OR(exang, oldpeak, slope), which gives **one cubic term**. It was verified against Turney's tables on all 8,192 subsets (max error 1.4×10⁻¹⁴). Five-test panels cost **$9.20–$313.87**. |
| **Objective** | f_μ(x) = −Σ rᵢxᵢ + 0.1·Σ cᵢⱼxᵢxⱼ + μ·cost(x)/100, subject to Σx = 5. rᵢ = kNN mutual information (k = 10) averaged over 20 seeds; cᵢⱼ = absolute Pearson correlation. Price weights μ ∈ {0, 0.02, 0.05, 0.1, 0.2}. |
| **Classical baselines, search side** | Exhaustive enumeration: exact, in milliseconds, and the ground truth for every claim. Greedy mRMR (55 evaluations; optimal at 2 of 5 μ). Greedy plus 1-swap local search (still stuck at μ = 0.1). Simulated annealing (T₀ from 0.003 to 0.3) and random-restart 1-swap local search, both at matched evaluations. An independent-choice sampler (QAOA's own per-feature marginals, conditioned on exactly five). Uniform random five-test panels. |
| **Classical baselines, prediction side** | Nested-CV logistic regression, SVM and gradient boosting on every frontier panel. Fixed reference panels: all 13 tests (AUC 0.897 at $324); the ESC pre-test-probability triplet of age, sex and chest-pain type ($3, AUC 0.839) ([ESC 2019 via Saraste & Knuuti](https://pmc.ncbi.nlm.nih.gov/articles/7391397)); routine risk factors ($13, AUC 0.695). Standard selectors: SelectKBest-MI and L1-logistic (0.88–0.89). |
| **Quantum subroutine** | 13 qubits, one per test, starting with RY(2·asin√(5/13)) on every qubit. Post-selecting Hamming weight 5 makes this exactly the Dicke start, at zero two-qubit cost (P(HW = 5) = 0.223; total variation distance 6.8×10⁻¹⁶). Cost layer: an exact Walsh expansion of f_μ, normalised by its standard deviation over the feasible set, applied as RZ for one-body terms, RZZ for two-body terms and a CX–RZ–CX ladder for the single cubic term. Mixer: 78 `XXPlusYYGate(−2β)` gates in round-robin order. Schedule: p = 1 with **frozen (γ, β) = (1.7182, 0.1676)**, tuned offline on 12 subsamples × 5 μ. Run: one `backend.run([5 circuits])`, read `result().get_counts(i)`, keep weight-5 bitstrings, then rank the pooled panels by (cost, score). |
| **Measurable difference** | Frontier recovery at matched pooled evaluations: the share of jobs that find every μ-optimum, the exact score-Pareto panels found (of 13), and the AUC-front panels found (of 8). Also P(optimum given weight 5) per μ against the independent-choice sampler and uniform. All are reported with shot budgets of 100–1,000 per circuit, ideal and under Forte-1 depolarizing noise. |
| **Qubits and gates** | 13 qubits, which fits the built-in simulator (24), Braket local (25) and Forte simulators (29). 234–237 RZZ per circuit on all-to-all hardware, against 695 two-qubit gates on IBM heavy-hex for the same p = 1 mixer. One job = **1,181 RZZ**, far under IonQ's 150,000-gate multi-circuit cap ([IonQ create-job API](https://docs.ionq.com/api-reference/v0.4/jobs/create-job)). |
| **Shots** | 1,000 per circuit by default (about 222 feasible samples each). Drop to 500 on IonQ if per-shot simulation is slow; at 500 shots recovery is 78% ideal / 66% noisy, against at most 28% for the classical heuristics. |
| **Tutorial-bar sentence** | No tutorial prices each heart test from a published fee schedule, encodes "pay for the treadmill once" as an exact three-body term, and samples the whole cost-versus-accuracy frontier in one IonQ job, checked against an independent-choice sampler, simulated annealing and local search at matched evaluations. |
| **Does not claim** | Any advantage over exhaustive search, which is exact and instant at 13 features; any speedup; that 1992 Canadian prices are today's prices; that differences among the top panels (AUC 0.89–0.91) are significant. |

The precedent is close but not identical. Kipu Quantum and IonQ ran a three-body mutual-information feature-selection HUBO on Forte in 2026 with no fixed k and no test costs ([Kipu + IonQ, arXiv:2604.26834](https://arxiv.org/abs/2604.26834)). Turati et al. ran penalty-QAOA feature selection on 13-feature wine data on IBM hardware ([Turati et al. 2022](https://ar5iv.labs.arxiv.org/html/2211.02861)). The session's search found no QUBO or QAOA feature selection on Heart Cleveland, and no study that uses real test costs, reports an independent-choice null, or checks the QUBO optimum against downstream accuracy ([Prompt B notes](<../research_notes/QCA prompts Quantum Impact plan/prompt_b_feature_selection.md>)). Cite Kipu/IonQ as the hardware precedent, and Wang et al. for the XY-mixer design ([Wang et al. 2020](https://arxiv.org/abs/1904.09314)).

### The measured difference survives noise but needs four caveats on the page

The table below is the headline. Each QAOA cell pools about 5 × B feasible samples from one simulated five-circuit job. Each classical heuristic gets B evaluations per price point, and every state it evaluates is pooled. Each cell is the share of 200 jobs that found all five price-point optima ([s10b log](<../research_notes/QCA prompts Quantum Impact plan/scripts/prompt_b/results/s10b_log.txt>); [s10f log](<../research_notes/QCA prompts Quantum Impact plan/scripts/prompt_b/results/s10f_log.txt>)).

| Raw shots per circuit (feasible) | QAOA ideal | QAOA, Forte-1 depolarizing | Independent-choice sampler | Simulated annealing (best T₀) | Random-restart local search | Uniform |
|---|---|---|---|---|---|---|
| 100 (~22) | 8% | 2% | 0% | 0% | 0% | 0% |
| 200 (~44) | 32% | 12% | 2% | 3% | 1% | 0% |
| 500 (~111) | **78%** | **66%** | 25% | 28% | 20% | 0% |
| 1,000 (~222) | **98%** | **94%** | 62% | 55% | 63% | 10% |

The same circuits beat the independent-choice sampler 1.6–5.3× on P(optimum given weight 5) at each price point when ideal: 0.0229 vs 0.0137 at μ = 0, and 0.0208 vs 0.0039 at μ = 0.2 ([s10 log](<../research_notes/QCA prompts Quantum Impact plan/scripts/prompt_b/results/s10_log.txt>)). Ideal-simulation recovery of the 8 panels on the exact cost-versus-AUC front averages 7.18, against 6.04 for the independent-choice sampler and 4.76 for uniform. The independent-choice comparison matters most: it isolates what correlations between qubits add beyond single-qubit biases, which is the only honest sense in which a 13-qubit circuit does something a coin-flipper cannot.

The page must print four caveats beside that table, because the judges will find them otherwise. First, **"matched evaluations" counts feasible samples**: QAOA spends about 4.5 raw shots per feasible sample, while each classical evaluation is a microsecond function call, so the comparison measures sampling quality, not wall-clock time. Second, **the angles came from offline classical simulation** on 60 training instances, compute the table does not count, and the classical heuristics were only lightly tuned. Third, **only four distinct panels sit behind "all five optima"**, because μ = 0.02 and μ = 0.05 share one optimum. Fourth, **one noisy circuit falls below the null**: in the 10,000-shot noisy reference, μ = 0.1 hits its optimum at 0.0029, *below* the independent-choice sampler's 0.0038. Its optimum is still recovered from the other circuits' samples, which is why pooling across price points is the right design. One more limit belongs in the honesty box. On the prompt's original, cost-free QUBO, XY-QAOA beats the independent-choice sampler by only 1.0–1.7×. Resolving that gap would need 6,400–13,500 raw shots, far beyond a judge's run ([Prompt B notes](<../research_notes/QCA prompts Quantum Impact plan/prompt_b_feature_selection.md>)).

Noise is gentle here for a structural reason. Post-selecting weight-5 bitstrings discards errors that leak out of the feasible sector, and noisy P(weight = 5) stayed at 0.200–0.228. At p = 1 the circuit's global fidelity is about 0.26, and the frontier statistic depends on the union of samples, not on one circuit's argmax. Going to p = 2 buys nothing under noise: P(optimum given weight 5) drops from 0.082 ideal to 0.014 ([s04 log](<../research_notes/QCA prompts Quantum Impact plan/scripts/prompt_b/results/s04_log.txt>)). Keep p = 1.

### The clinical ladder, with the honest numbers beside the optimistic ones

The exact cost-versus-cross-validated-AUC front over all panels of up to five tests is the story a mixed panel will remember ([s06 log](<../research_notes/QCA prompts Quantum Impact plan/scripts/prompt_b/results/s06_log.txt>)):

| Price (1992 CAD, relative) | Panel | CV AUC (logistic, 5×3 CV, full data) | What the clinic buys |
|---|---|---|---|
| $3.00 | age, sex, chest-pain type | 0.839 | ESC pre-test-probability inputs; free history |
| $9.20 | + resting BP, fasting sugar | 0.838 | Cheapest five-test panel (μ = 0.2 optimum) |
| $91.30 | age, sex, cp, oldpeak, slope | 0.875 | One exercise ECG; its second reading is nearly free |
| $106.90 | sex, cp, trestbps, thalach, thal | 0.878 | Thallium stress test (μ = 0.1 optimum) |
| $191.20 | sex, cp, trestbps, slope, ca | 0.902 | Fluoroscopy plus exercise ECG |
| $206.80 | sex, cp, thalach, ca, thal | 0.904 | Imaging (μ = 0.02 and 0.05 optima within 0.002) |
| $293.10 | sex, cp, slope, ca, thal | 0.911 | Best panel (μ = 0 optimum); optimistic, as the top of 1,287 |

Two shared-procedure bundles (oldpeak + slope, and thalach + thal) both appear on the front. That is the cubic and quadratic discount terms doing visible work. The page must also show the honest numbers, in which feature selection is re-run inside every outer training fold ([s09 log](<../research_notes/QCA prompts Quantum Impact plan/scripts/prompt_b/results/s09_log.txt>)):

| Selection rule (inside each fold) | Per-repeat AUC | Averaged out-of-fold AUC [95% CI] | Mean panel cost |
|---|---|---|---|
| Cost-aware QUBO, μ = 0.1 | 0.846 | 0.868 [0.826, 0.905] | $101 |
| Cost-aware QUBO, μ = 0.2 | 0.818 | 0.827 [0.776, 0.870] | $19 |
| All 13 tests | 0.897 | — | $324 |

So the frontier's value sits in the middle of the price range, where the discounts matter. At the cheap end, the guideline triplet chosen *a priori* ($3, 0.839) is already as good as anything data-selected. Saying so is a strength under Impact Potential, not a weakness.

## A 28-hour plan with a Sunday 08:00 cut line

### Architecture: one Python entry point, precomputed evidence, one live job

Build a **Python-only Qollab project**: no JS front end, so no JS↔Python bridge and no PyProxy lifetime issues. `main()` takes typed parameters on one line starting at column 1. Qollab then renders a run-settings form and calls `main()` itself ([Qollab runtime environment](https://qollab.xyz/learn/docs/runtime-environment)). Output is printed tables plus two matplotlib figures, each followed by its data table for accessibility. The earlier platform research fixes the rest ([build feasibility notes](<../research_notes/Quantum Unlocked theme deep dive/build_feasibility_and_stack.md>)). Data files must be opened by plain string-literal paths, and the current `common.py` builds paths with `os.path.join`, which Qollab rejects, so it must be edited. Counts must come from `backend.run(circs, shots=S).result().get_counts(i)`, never from `BackendSamplerV2` (which returns all zeros on IonQ) or `job.get_counts()` ([Qollab primitives](https://qollab.xyz/learn/docs/primitives)). Each run makes exactly one `backend.run` call, every file stays under 2 MB, and every outside dependency is MIT-licensed.

```
main.py           # def main(shots: int = 1000, run_audits: bool = True, revalidate_auc: bool = True):
heartcost.py      # common.py + s06_helpers.py: CSV loader (literal path), Turney costs, cost polynomial, 8,192-subset self-test
frontier.py       # enumeration over 2^13, exact (cost, score) Pareto, greedy, greedy+1-swap, SA, RR-LS, null|k, uniform
qaoa_circuits.py  # s10_pareto_onejob.circuit(): Walsh expansion -> RY / RZ / RZZ / CX-ladder / XXPlusYY, frozen (gamma, beta)
qsim.py           # NumPy XY-QAOA simulator (as is): equivalence check vs circuit, exact distributions for 200-job statistics
runjob.py         # ONE backend.run(list), result().get_counts(i), weight-5 post-selection, Wilson CIs, cached-result fallback
validate.py       # logistic 5x3 CV re-validation of the 5-8 frontier panels (from s05_downstream.py)
data/heart_cleveland_297.csv   data/turney_costs.json
results/*.json    # precomputed: r, panel-AUC table (from s05_all_subsets.npz), s10b/c/d/f, s03/s02c, s04, s07, s08, s09, forte cache
LICENSE (MIT)  README.md (= project page)  DISCLOSURE.md
```

**Live on the judge's Run** are the cost self-test; exact enumeration and the Pareto front for five μ; one seeded draw each of greedy, simulated annealing and local search at matched evaluations; the five-circuit job on whatever backend the judge picked; the 200-job recovery rates for QAOA, the independent-choice sampler and uniform, recomputed cheaply from exact NumPy distributions; cross-validation of the sampled frontier panels; and the circuit-versus-NumPy equivalence check, printed as a total variation distance. **Precomputed and labelled as such** are the angle tuning, the simulated-annealing and local-search 200-job tables, the 2,379-panel AUC table, the honest nested pipelines, the proxy, penalty and robustness audits, the heavy-hex gate counts, the noisy Aer reference, and the cached IonQ Forte run with its date, backend name and shots. The prompt-B notes estimate 5–20 s in the browser after package load ([Prompt B notes](<../research_notes/QCA prompts Quantum Impact plan/prompt_b_feature_selection.md>)). One defensive rule matters: if the backend name contains "ionq", default to 500 shots per circuit; if it looks like an IBM fake-device noise model, cap at 200 with a printed note. Per-shot noise simulation is the one place where run time grows with shots ([Qollab ideal vs noise-model simulators](https://qollab.xyz/learn/docs/ideal-vs-noise-model-simulators)).

### Hour by hour from Saturday 15:00

Roles follow the earlier ideation: **Q** = quantum lead, **C** = classical baselines and data, **D** = docs, video and accessibility, **V** = verification and statistics. With three people, merge V into C; with two, also merge D into Q.

| Clock (ET) | Hours | Work | Who | Exit test |
|---|---|---|---|---|
| Sat 15:00–17:00 | H0–2 | **Smoke tests on a throwaway Qollab project:** import numpy, pandas, scikit-learn and qiskit; read the CSV by literal path; build the five circuits from the s10 recipe and run them as one list on the built-in simulator; time it all. Send a 2-circuit × 50-shot list job to an IonQ Forte simulator. Create the public GitHub repo with an MIT LICENSE. Write the pre-registration below into the README. | All | Five count dictionaries from one built-in `backend.run`; IonQ list-job behaviour known |
| Sat 17:00–21:00 | H2–6 | **C:** `heartcost.py`, `frontier.py`, precomputed r, exported JSON. **Q:** `qaoa_circuits.py`, `runjob.py`, equivalence check against `qsim.py`. **D:** page skeleton, README, disclosure, data attribution. | C, Q, D | `main()` prints the frontier and the live job on built-in |
| **Sat 21:00** | **H6** | **Gate 1 (safety publish):** v0 public on Qollab (theme Quantum Impact, MIT), identical code pushed to GitHub. This is the last moment to switch to Prompt A. | All | v0 runs from a second account |
| Sat 21:00–01:00 | H6–10 | **Evidence:** the 200-job recovery table (live part plus precomputed simulated annealing and local search); CV re-validation; penalty-vs-XY and proxy-audit tables; frontier-staircase and recovery-vs-shots figures (Okabe–Ito palette, markers plus direct labels). **V:** confirmatory run of the frozen angles on 50 fresh subsamples with a new seed. **Q:** run the five-circuit job once on IonQ Forte and cache the counts. | Q, V, C | Every number on the page comes from `main()` or a named JSON |
| Sun 01:00–07:00 | H10–16 | Sleep, staggered if the IonQ job is still queued | — | — |
| Sun 07:00–08:00 | H16–17 | Fresh-account Run on the built-in simulator, timed | V | Wall time recorded |
| **Sun 08:00** | **H17** | **Cut-line checkpoint** (below) | All | — |
| Sun 08:00–12:00 | H17–21 | Full project page, README identical to it, limitations, disclosure, accessibility pass; republish | D, V | Page complete |
| Sun 12:00–14:00 | H21–23 | Video: record, caption, upload as public with no sign-in | D, Q | Link opens signed out |
| Sun 14:00–16:00 | H23–25 | Judge-path tests from a fresh account on built-in, Braket local and one IonQ Forte selection; final checklist | All | All three run or fail gracefully |
| Sun 16:00–17:00 | H25–26 | Submit: publish the Qollab page; send the QCA Fall Fest form with the GitHub repo and the video | All | Confirmations saved |
| Sun 17:00–19:00 | H26–28 | Buffer; no new features | — | — |

### The Sunday 08:00 checkpoint is the hour-20-style cut line

At 08:00 five things must exist: a published, runnable build; the live exact frontier with its classical baselines; the live five-circuit job on the built-in simulator with weight-5 post-selection; the matched-evaluation recovery table; and the honest CV table. If any is missing, cut in a fixed order: first the live IonQ path (keep the cached result or document the failure), then the robustness panel, then the proxy audit (down to one sentence and a static table), then the live penalty-QAOA demonstration (keep its static table), and finally figure polish. Documentation starts at 08:00 regardless, because Documentation Quality is a quarter of the score. **Solo builders** should aim for the minimal version from the start: frontier, greedy and simulated annealing, the five-circuit job against the independent-choice and uniform samplers, precomputed tables, and the page. That is about 14 engineering hours plus 5 for docs and video.

### Pre-registration to paste into the README

> Registered Sat Oct 10, 2026, after exploratory simulation and before the live, confirmatory and IonQ runs.
>
> (1) With the frozen p = 1 schedule at 1,000 raw shots per circuit, the share of 200 simulated jobs recovering every μ-optimum exceeds the best classical heuristic at matched pooled evaluations by ≥ 20 points.
>
> (2) On 50 fresh 80% subsamples (new seed), the mean QAOA P(optimum given weight 5) exceeds the independent-choice sampler at every μ.
>
> (3) The sampled frontier panels' CV AUC lies within 0.005 of the exact cost–AUC front at their price.
>
> (4) We make no claim against exhaustive enumeration.

This follows Qollab's own five-step "is quantum worth it" protocol ([Qollab Learn](https://qollab.xyz/learn/using-quantum-in-a-real-application/is-quantum-worth-it)).

### Reusable scripts and data

All paths are relative to `research_notes/QCA prompts Quantum Impact plan/scripts/`.

| File | Use in the build |
|---|---|
| `prompt_b/heart_cleveland_297.csv` | Ship as `data/`. It has `num` and `target` columns, so swap `load_data()`'s raw-file reader for this file. |
| `prompt_b/common.py` | Features, Turney costs and groups, MI relevance, redundancy, bit convention (qubit i = bit i of `int(bitstring, 2)`), `panel_cost`, `wilson`. Replace its `os.path.join` paths with literals. |
| `prompt_b/s06_helpers.py` | `cost_vector()`: the exact OR-polynomial cost over all 8,192 states |
| `prompt_b/qsim.py` | NumPy XY-QAOA simulator, `complete_pairs()` round-robin order, `Inst`, `dicke_init`, `product_dist`/`marginals_full` (the independent-choice sampler) |
| `prompt_b/s10_pareto_onejob.py` | **The recipe:** angle tuning, the Walsh-expansion circuit builder, `front_quality()`, the one-job run. Its `results/s10_pareto_onejob.json` holds the frozen angles. |
| `prompt_b/s10b_pareto_shots.py`, `s10c_sa_matched.py`, `s10d_localsearch_matched.py`, `s10e_sa_schedules.py`, `s10f_pooled_matched.py` | Matched-evaluation baselines; JSON and logs feed the headline table |
| `prompt_b/s05_downstream.py`, `results/s05_all_subsets.npz` (48 KB) | Cross-validation code and the precomputed 2,379-panel AUC table (convert to JSON) |
| `prompt_b/s09_honest_cost_pipelines.py`, `s08_proxy_quality.py`, `s07_robustness.py` | Honest nested pipelines, proxy audit, panel robustness (results JSON present) |
| `prompt_b/s02_plain_qiskit_opt.py`, `s02b_plain_diagnose.py`, `s02c_plain_emulated.py`, `s03_qaoa.py`, `s01b_penalty_scale_and_timing.py` | The pitfalls box: the 4.35 automatic penalty and the 1e5 fallback; penalty vs XY mixers; library-path timings |
| `prompt_b/s04_circuits_noise.py` | Gate counts (all-to-all vs heavy-hex), Dicke-by-post-selection check, Aer Forte-1-rate noise |
| `prompt_b/data_raw/costs/*`, `heart-disease.names`, `WARNING` | Turney README and cost files for attribution; reason to use only the processed file |
| `prompt_a/qk_core.py`, `judge_run_prototype.py`, `verify_qiskit.py`, `results/exp1_summary.json`, `exp3c_auditor_validation.json`, `exp4b_noise_lowbw.json`, `exp6_job_sizing.json` | The fallback build (next subsection) |
| `prompt_c/gs_core.py`, `data/catalog_2024_m5_slim.json` (0.46 MB), `c05_bbht_vs_classical.py`, `c09_ft_crossover.py` | Not used. Kept for a Quantum Unlocked-style "fine print of Grover" project. |

### Runner-up fallback: Prompt A's positive-controlled kernel audit

If the switch is needed, build Prompt A as **"Does a Quantum Circuit See the Tumour?"**: a positive-controlled auditor (its E1), a sensitivity-first clinical operating point (its E2), and a 60-circuit projected-kernel job on IonQ covering 20 patients × 3 measurement bases at 8 qubits. Its judge path already exists as `judge_run_prototype.py` and runs in 2.15 s natively ([prototype timings](<../research_notes/QCA prompts Quantum Impact plan/scripts/prompt_a/results/judge_run_prototype.json>)). Its headline is parity on the real labels (CI −1.8 to +1.0) from an instrument that detects +25 to +46-point wins on engineered labels. Expect 10–14 hours plus documentation ([Prompt A notes](<../research_notes/QCA prompts Quantum Impact plan/prompt_a_quantum_kernel.md>)).

Switch only at the Saturday 21:00 gate, and only if the 13-qubit circuits cannot be built or simulated in Qollab's single-threaded Qiskit in under about a minute even after transpiling to {rz, ry, rx, rzz}, or if B's classical half (pandas, scikit-learn MI and CV) cannot be made to run in the browser. Both failures would spare A, whose live demo is 8-qubit NumPy work. After 21:00, cut scope inside B rather than switch.

## The page and video sell a price ladder, not a speedup

### Project page outline (Qollab page and GitHub README, identical)

| # | Section | Content |
|---|---|---|
| 1 | Title and summary | "Five Tests, Priced". Theme: Quantum Impact. One-line summary. The required line "This effort is supported by Qollab & IonQ" ([Qollab Rules & terms](https://qollab.xyz/programs/hackathon/terms)). |
| 2 | The decision in plain words | A chest-pain clinic can collect five measurements: which five, and what does each extra dollar buy? The price-ladder table up top. |
| 3 | Data and costs | The UCI Cleveland file (297 rows; why 6 rows were dropped; CC BY 4.0 citation); Turney's 1992 Ontario costs as relative prices; the referral-cohort caveat |
| 4 | How to run | Press Run. Built-in simulator is the default; measured time X s. The parameters. Running on IonQ Forte (one job, 500 shots). Browser note: Chrome, Edge, or Firefox 153+. |
| 5 | Pre-registration | The dated block above |
| 6 | Classical baselines first | Exhaustive enumeration (ms), greedy (fails at 3 of 5 prices), greedy plus swap, simulated annealing, local search; ESC triplet; all 13 tests |
| 7 | Why the prompt's QUBO had to change | Pitfalls box: the penalty swamps the objective (4.35 / 1e5); f/f* is undefined for λ ≥ 0.75; the k = 3 MI bias; greedy warm starts are trivially "optimal" |
| 8 | The quantum step | Diagram: prices → HUBO → 5 circuits → one job → weight-5 post-selection → pooled frontier. Why correlations matter (the independent-choice null). Gate counts: IonQ all-to-all vs heavy-hex. |
| 9 | Results | Recovery-vs-shots table and figure; per-μ P(optimum); honest CV table; the four caveats. Every number tagged *live* or *precomputed (file, date, seed)*. |
| 10 | What this does not claim | No advantage over exhaustive search; no speedup; depolarizing noise model, not IonQ hardware; n = 13 |
| 11 | What would have to change to matter | Dozens to hundreds of priced tests, where enumeration stops being instant; modern prices; prospective multi-site data; deeper circuits at higher fidelity |
| 12 | Replicate and extend | File map; how to change prices, k, λ and the μ grid; how to re-tune the angles |
| 13 | Pre-existing work and AI use | Qiskit, scikit-learn, NumPy, pandas, matplotlib; UCI data and Turney files; no tutorial code copied; research scripts written Oct 10 inside the window with AI assistance, reviewed by the team, who remain responsible for accuracy |
| 14 | Licences and credits | Code MIT; data CC BY 4.0 with citations (Janosi et al. 1989; Turney 1995) |
| 15 | Accessibility | Alt text on every image; a data table after every figure; Okabe–Ito palette with markers and labels (never colour alone); video captions |

### Video beat sheet (about 2:40)

| Time | Beat |
|---|---|
| 0:00–0:15 | Hook: "A clinic can afford five heart tests. Which five, and what does each extra dollar buy?" Press Run; the price ladder appears. |
| 0:15–0:35 | The data: 297 Cleveland patients, 13 tests, Turney's fee schedule, and "pay for the treadmill once" |
| 0:35–1:00 | Classical first: enumeration takes milliseconds. The prompt's QUBO as written is trivial, and its library penalty swamps it. Real prices break greedy at 3 of 5 price points. |
| 1:00–1:35 | The quantum step: 13 qubits, a free Dicke start by post-selection, an XY mixer that keeps exactly five tests, one job of five circuits, 234 vs 695 two-qubit gates on IonQ vs heavy-hex |
| 1:35–2:05 | The measurement: 98% / 94% vs 63 / 62 / 55 / 10% at matched evaluations, with the shots curve; live job on screen; cached Forte result |
| 2:05–2:30 | The ladder ($3 → 0.84, $91 → 0.875, $191–207 → 0.90) and the limits: no win over exhaustive search, 1992 relative prices, referral cohort |
| 2:30–2:40 | Attribution line, Qollab and GitHub links |

### Two submissions, one codebase

The same MIT-licensed code goes to both places. The two entries need different things:

| Requirement | QCA Fall Fest form | Qollab × IonQ |
|---|---|---|
| Code | **Public GitHub repo** (MIT LICENSE), identical to Qollab | Published and runnable on qollab.xyz under MIT; runs on the free simulators, IonQ's included |
| Video | 2–3 min demo | 2–3 min at a public link that opens without signing in |
| Page | README mirrors the page | Project page with theme Quantum Impact, the attribution line, pre-existing-code and AI disclosure, and accessibility practices ([Qollab Rules & terms](https://qollab.xyz/programs/hackathon/terms)) |
| IonQ | Not scored | Per the organizers on Discord, it must run through IonQ's Forte simulators within ≤29 qubits as one job, so the code must work on that path. QCA's slides say IonQ results neither add nor subtract points ([QCA prompt slides](https://docs.google.com/presentation/d/1O5WEDQost04m8rjneB8nCuAGwgyVhckoyc87dRa8j0g)). |

## Ten assumptions nobody has tested inside Qollab

Every timing and noise number above comes from native CPython and Aer on a shared machine. None was measured on Qollab or on IonQ's cloud.

| # | Assumption | Why it matters | Test (when) | If it is false |
|---|---|---|---|---|
| 1 | Qollab's IonQ path accepts a **list of five circuits as one job** and returns per-circuit counts via `result().get_counts(i)`. Qollab's FAQ says IonQ runs "must go in one circuit"; its runtime docs say pass every circuit to a single `backend.run` ([Qollab FAQ](https://qollab.xyz/programs/hackathon/how-it-works#faq); [runtime docs](https://qollab.xyz/learn/docs/runtime-environment)). IonQ itself supports multi-circuit jobs ([IonQ Qiskit docs](https://docs.ionq.com/sdks/qiskit/index)). | The one-job design | 2 circuits × 50 shots on Forte (H0–2) | Run the μ = 0.1 circuit alone on IonQ and show the other four from built-in plus cache. Two 13-qubit circuits could also be packed into 26 ≤ 29 qubits on IonQ only. |
| 2 | Passing `noise_model="forte-1"` works through Qollab's wrapper, or the backend picker already sets the model; it is also unknown which Forte model judges select | Reproducibility of the cached run | Same test; print the backend name | Don't pass it; record what ran |
| 3 | **IonQ's real noise model** resembles the legacy depolarizing rates (1q 0.000267, 2q 0.00495, no SPAM). IonQ says the post-September-2025 Forte models are "more complex" and their docs are in preparation ([IonQ noise models](https://docs.ionq.com/guides/simulation-with-noise-models)). | The 94% / 66% noisy figures | The cached Forte run | Report what Forte gives. Readout error lowers P(weight 5) but post-selection still filters it. |
| 4 | IonQ per-shot simulation of 5 × 1,000 shots at about 240 RZZ finishes without `SimulationTimeout` or `TooLongPredictedExecutionTime`. The Aer proxy took 46.7 s natively ([s10 log](<../research_notes/QCA prompts Quantum Impact plan/scripts/prompt_b/results/s10_log.txt>); [Qollab compute backends](https://qollab.xyz/learn/docs/compute-backends)). | Judges' IonQ Run | 1 circuit × 200 shots, then extrapolate | 500 or 200 shots per circuit; quote the s10b curve |
| 5 | Judge path takes 5–20 s in the browser after load. This is extrapolated at 3–10× native; first-load time for scikit-learn, SciPy, matplotlib and Qiskit is unknown. | Judge experience | Time the smoke test (H0–2) | Precompute r and CV; trim live re-validation to 3 panels |
| 6 | Qollab's Qiskit 2.5.x `BasicSimulator` accepts `XXPlusYYGate`/`rzz` and keeps the `XXPlusYYGate(−2β)` sign convention the frozen angles assume. The scripts ran on Qiskit 2.3.x. | Wrong sign means wrong distribution | Print TVD of circuit vs `qsim.py` on every run | Transpile to {rz, ry, rx, rzz} first; flip β if the TVD says so |
| 7 | Browser scikit-learn 1.8 reproduces the seeded kNN-MI relevance | Frontier drift | Compare with the shipped r | Use the shipped r as the default |
| 8 | Gate counts hold on IonQ. They are RZZ-basis transpiles; IonQ compiles to GPI/GPI2/ZZ natively. | Ledger accuracy | Read the counts back from the IonQ job metadata, if exposed | Label the counts "RZZ-basis estimate" |
| 9 | CC BY 4.0 data (UCI and Turney's files) may ship inside an MIT project with attribution | Rules compliance | Ask the organizers on Discord or Slack (H0–2) | No substitute exists (scikit-learn does not bundle this dataset); attribute prominently and follow the organizers' answer |
| 10 | Judges reward a scoped "sampling quality at matched evaluations, no speedup" claim under Impact Potential. No rubric descriptor defines impact. | Score risk | Not testable | Lead with the clinical ladder; keep the honesty box short and concrete |

Two smaller unknowns remain. The frozen angles were tuned on 80% subsamples that overlap the full data, a gap the fresh-seed confirmatory check at H6–10 closes. And Qollab registration closed Oct 8, so the plan assumes the team is registered at the Georgia Tech node.

## Conclusion

Across all three prompts the plain version fails for a reason that can itself be measured: a penalty that swamps the objective, a bandwidth that collapses the kernel to "all benign", an oracle that already contains the answer. In a field where every team has the same prompt, documenting that failure with numbers is the cheapest novelty available. B is the only prompt where fixing the failure also creates a legitimate job for the quantum circuit. Real prices destroy greedy's exactness, and in that gap a 13-qubit p = 1 circuit samples the frontier better than its own independent-choice shadow, simulated annealing and local search.

The broader lesson for the build is to make the instance honest *before* asking whether quantum helps. A comparison against a classical method that is already exact can only produce a fake win or a trivial loss, and Impact judges will reward a team that shows it understood this. The decisive tests are now operational rather than scientific: one list-job probe, one timed browser run and one cached Forte job, all before Saturday 17:00.
