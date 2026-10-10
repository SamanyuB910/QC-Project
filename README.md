# Five Tests, Priced

[![tests](https://github.com/SamanyuB910/QC-Project/actions/workflows/tests.yml/badge.svg)](https://github.com/SamanyuB910/QC-Project/actions/workflows/tests.yml)

**Which five heart tests should a clinic order, and what does each extra dollar buy? A 13-qubit QAOA answers that for five budgets at once, in a single job.**

**This effort is supported by Qollab & IonQ.**

- **Theme:** Quantum Impact. **Prompt:** QCA Georgia Tech Qiskit Fall Fest 2026, Prompt B ("Heart Disease Readings").
- **Submissions:** Georgia Tech Qiskit Fall Fest (this repo + demo video) and Qollab × IonQ hackathon (project on qollab.xyz).
- **Full project page:** [`five_tests_priced/README.md`](five_tests_priced/README.md). This is the same text as the Qollab write-up.
- **Qollab project:** *(link added after publishing)* · **Demo video:** *(link added after recording)*

## In 30 seconds

- **Problem.** A chest-pain clinic can collect only **5 of 13** measurements. Tests have **real prices** (Turney 1995), and some share one procedure: one treadmill ECG gives three readings. Price is therefore not a simple sum, and greedy selection is **wrong at 3 of 5 budgets**.
- **Quantum step.** There is one qubit per test and one circuit per budget. An XY mixer swaps a test in for a test out, so **every sample has exactly five tests**. There is no penalty term: every penalty value you can choose without knowing the answer made QAOA random-level. All five circuits run as **one job** on any simulator, IonQ's included.
- **Result.** At equal numbers of evaluated panels, one 1,000-shot job finds every budget's optimal panel **98%** of the time (ideal), or **92%** with IonQ forte-1-rate noise. The comparisons:
  - independent-choice sampler (same per-test odds, no correlations): **63%**;
  - simulated annealing: **55%**;
  - local search: **63%**.
- **Pre-registered checks.** Both confirmatory checks **passed**.
- **What we don't claim.** No speedup: at 13 tests exhaustive search is exact and instant.

| Price | Best five-test panel | AUC* |
|---|---|---|
| $9.20 | history + one blood test | 0.838 |
| $91.30 | history + one treadmill ECG | 0.875 |
| $191.20 | + treadmill ECG + fluoroscopy | 0.902 |
| $293.10 | + treadmill + thallium + fluoroscopy | 0.911 |

\*Cross-validated on all 297 patients, best of 1,287 panels, so optimistic. The honest held-out numbers are on the project page.

## Run it

**On Qollab:** upload [`five_tests_priced/`](five_tests_priced/) and press **Run** on any simulator.

**On a laptop:** this mimics Qollab, with the working directory set to the project folder, `backend` injected, and `main()` called once.

```
py -3.12 -m venv .venv
.venv/Scripts/pip install -r requirements.txt
.venv/Scripts/python tools/run_local.py --backend basic          # Qollab's built-in simulator (BasicSimulator)
.venv/Scripts/python tools/run_local.py --backend aer-forte      # Aer with IonQ forte-1 legacy noise rates
.venv/Scripts/python tools/run_local.py --backend fake-ibm       # a routed, noisy IBM-style device
.venv/Scripts/python -m pytest tools/tests                       # the test suite (~1 min)
.venv/Scripts/python tools/precompute.py auc baselines penalty gates honestcv confirm2 confirm3 noisy
```

`run_local.py` fails if the program calls `backend.run` anything other than exactly once.

## Pre-registration

*Registered **Sat Oct 10, 2026, 15:00 ET**, after exploratory simulation (Oct 9–10) and before any confirmatory, live-Qollab or IonQ run. Git tag [`prereg`](https://github.com/SamanyuB910/QC-Project/releases/tag/prereg) marks this text; results are in the right-hand column.*

**Fixed in advance:**
- **Objective:** f_μ(x) = −Σ rᵢxᵢ + 0.1·Σ_{i<j} cᵢⱼxᵢxⱼ + μ·cost(x)/100, subject to Σx = 5.
  - rᵢ = kNN mutual information (k = 10, 20 seeds, discrete-feature mask), shipped as constants.
  - cᵢⱼ = |Pearson correlation|.
  - cost(x) = Turney's 1992 Ontario test costs with shared-procedure discounts.
- **Price weights:** μ ∈ {0, 0.02, 0.05, 0.1, 0.2}.
- **Circuit:** p = 1, complete-graph XY mixer (`XXPlusYYGate`, round-robin pair order), RY(2·asin√(5/13)) start, post-selection on exactly five 1s.
- **Frozen angles:** (γ, β) = (1.7181724313553923, 0.16760994251739314), tuned offline on 12 × 80% subsamples × 5 μ.

| # | Claim (as registered) | Outcome |
|---|---|---|
| 1 | **Replication** (already seen during exploration, so not confirmatory). At 1,000 raw shots per circuit, the share of 200 simulated jobs that recover every μ-optimum exceeds the best classical heuristic at matched pooled evaluations by ≥ 20 percentage points. | 98% vs 63%: **met** |
| 2 | **Confirmatory.** On 50 fresh 80% subsamples of the patients (new seed 20261010, never used before), the mean ideal QAOA P(optimum given five tests) exceeds the independent-choice sampler at **every** μ. | **Passed.** 1.33×, 1.42×, 1.91×, 2.20×, 3.78×; QAOA higher in 48–50 of 50 subsamples per μ |
| 3 | **Confirmatory.** The pre-declared run is the built-in simulator, `seed = 7`, default shots, run with `tools/run_local.py --backend basic`. For each μ, take its best sampled panel by objective; its cross-validated AUC (logistic regression, 5×3 stratified CV, `random_state = 7`) lies within 0.005 of the best AUC of any five-test panel costing no more than it. | **Passed.** Gaps 0.000, 0.002, 0.002, 0.000, 0.000 |
| 4 | **Reported as-is.** One run on IonQ's Forte noise-model simulator, with per-μ P(optimum given five tests), the bit-order sentinel, and the closed-form expectation printed *before* the job. A miss is not evidence against the method, and a hit is not evidence of advantage. | Pending (run log will be in [`docs/runs/`](docs/runs/)) |
| 5 | **No claim** against exhaustive enumeration, which is exact and instant at 13 features. | n/a |

## Repository map

| Path | What it is |
|---|---|
| [`five_tests_priced/`](five_tests_priced/) | **The project**: exactly the files uploaded to Qollab. Its README is the project page. |
| [`tools/`](tools/) | Offline only: `precompute.py` (every precomputed number, with provenance), `run_local.py`, the Qollab smoke test, `tests/` |
| [`docs/`](docs/) | Video script, submission checklist, Qollab steps, [disclosure](docs/DISCLOSURE.md), archived run outputs |
| `research_notes/`, `reports/`, `ideation/` | Supporting research (Oct 7–10); see [disclosure](docs/DISCLOSURE.md) for what predates the build window |

## Pre-existing work, AI use, licences

- **Disclosure.** See [`docs/DISCLOSURE.md`](docs/DISCLOSURE.md) for what existed before the build window (Oct 9, 19:00 ET), what was built during it, every outside source we credit, and our AI use. Code and text were produced with substantial assistance from an AI model (Anthropic's Claude), directed and reviewed by the team.
- **Licences.** Code: MIT ([`LICENSE`](LICENSE)). Data: UCI Heart Disease (CC BY 4.0) and Turney (1995) test costs; see [`DATA_NOTICE.md`](DATA_NOTICE.md).
