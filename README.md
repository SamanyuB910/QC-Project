# Five Tests, Priced

*Choosing a heart-disease test panel with real prices, sampled by a 13-qubit QAOA in one IonQ job.*

**This effort is supported by Qollab & IonQ.**

> **Status: under construction.** The build window runs from Fri Oct 9, 19:00 ET to Sun Oct 11, 19:00 ET. This README becomes the full project page as the build proceeds. The runnable Qollab project is the folder [`five_tests_priced/`](five_tests_priced/). Everything under `research_notes/`, `reports/` and `ideation/` is supporting research (see *Pre-existing work* below).

- **Theme:** Quantum Impact. **Prompt:** QCA Georgia Tech Qiskit Fall Fest 2026, Prompt B ("Heart Disease Readings").
- **Submissions:** Qiskit Fall Fest (GitHub + video) and Qollab × IonQ (project on qollab.xyz).

## The decision, in one paragraph

A chest-pain clinic can collect only **5 of 13** measurements per patient, and the tests have real prices. Some tests share a procedure: one blood draw, one thallium scan, one treadmill ECG. Buying one test in a group makes the others in that group nearly free, so prices do not simply add up. We encode the prompt's relevance-minus-redundancy QUBO plus Turney's published test costs, including one exact three-test "pay for the treadmill once" term. A 13-qubit QAOA, whose XY mixer always keeps exactly five tests, then samples the best panel at five price points in **one** job. We compare it honestly against exhaustive search, greedy, simulated annealing, local search, and an "independent-choice" sampler that copies the circuit's per-test odds but ignores correlations.

## Pre-registration

*Registered **Sat Oct 10, 2026, 15:00 ET**, after exploratory simulation (Oct 9–10) and before any confirmatory, live-Qollab or IonQ run. The git tag `prereg` marks this text.*

Fixed in advance:

- **Objective:** f_μ(x) = −Σ rᵢxᵢ + 0.1·Σ_{i<j} cᵢⱼxᵢxⱼ + μ·cost(x)/100, subject to Σx = 5.
  - rᵢ = kNN mutual information (k = 10, 20 seeds, discrete-feature mask), shipped as constants.
  - cᵢⱼ = |Pearson correlation|.
  - cost(x) = Turney's 1992 Ontario test costs with shared-procedure discounts.
- **Price points:** μ ∈ {0, 0.02, 0.05, 0.1, 0.2}.
- **Circuit:** p = 1, complete-graph XY mixer (`XXPlusYYGate`, round-robin pair order), RY(2·asin√(5/13)) start, post-selection on exactly five 1s.
- **Frozen angles:** (γ, β) = (1.7181724313553923, 0.16760994251739314), tuned offline on 12 × 80% subsamples × 5 μ.

Claims and how each will be judged:

1. **Replication** (already observed during exploration, so not confirmatory). At 1,000 raw shots per circuit, the share of 200 simulated jobs that recover every μ-optimum exceeds the best classical heuristic at matched pooled evaluations by ≥ 20 percentage points.
2. **Confirmatory.** On 50 fresh 80% subsamples of the patients (new seed 20261010, never used before), the mean ideal QAOA P(optimum | five tests) exceeds the independent-choice sampler at **every** μ.
3. **Confirmatory.** The pre-declared run is the built-in simulator, `seed = 7`, default shots, run locally with `tools/run_local.py --backend basic`. For each μ, take its best sampled panel by objective. That panel's cross-validated AUC (logistic regression, 5×3 stratified CV, `random_state = 7`) must lie within 0.005 of the best AUC of any five-test panel costing no more than it.
4. **Reported as-is.** One run on IonQ's Forte noise-model simulator is reported with whatever it gives: per-μ P(optimum | five tests), the bit-order sentinel, and the closed-form expectation printed *before* the job. A miss is not evidence against the method, and a hit is not evidence of advantage.
5. **No claim** against exhaustive enumeration, which is exact and instant at 13 features.

## Repository map

| Path | What it is |
|---|---|
| [`five_tests_priced/`](five_tests_priced/) | **The project.** Exactly the files uploaded to Qollab. |
| `tools/` | Offline tools, not uploaded: precompute, local runner, Qollab smoke test, tests |
| `docs/` | Project-page text, video script, submission checklist, archived run outputs |
| `research_notes/`, `reports/`, `ideation/` | Supporting research, Oct 7–10 (see disclosure) |

## Licences

Code: MIT (`LICENSE`). Data: UCI Heart Disease, CC BY 4.0, plus Turney (1995) test costs. See [`DATA_NOTICE.md`](DATA_NOTICE.md).
