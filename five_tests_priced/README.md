# Five Tests, Priced

**Choosing a heart-disease test panel when tests have real prices, sampled by one 13-qubit QAOA job.**

This effort is supported by Qollab & IonQ.

*Theme: Quantum Impact · QCA Georgia Tech Qiskit Fall Fest 2026, Prompt B ("Heart Disease Readings") · Code: [github.com/SamanyuB910/QC-Project](https://github.com/SamanyuB910/QC-Project)*

> Build **v0** (safety version, Sat Oct 10). The full write-up, figures and precomputed evidence tables arrive in later builds before the deadline.

## The decision

A chest-pain clinic can collect only **5 of 13 measurements** per patient. QCA's prompt asks which five: the most informative, least redundant set. Real tests also have **prices**, and some share a procedure:

| Shared procedure | Tests it yields | Paid once |
|---|---|---|
| Blood draw | cholesterol, fasting blood sugar | $2.10 |
| Thallium stress test | max heart rate, thallium result | $101.90 |
| Treadmill ECG | exercise angina, ST depression, ST slope | $86.30 |

Buying one test in a group makes the others nearly free, so prices do not simply add up. The result is a price ladder: what each extra dollar buys in diagnostic accuracy (cross-validated AUC):

| Price | Best five-test panel | AUC |
|---|---|---|
| $9.20 | age, sex, chest-pain type, resting BP, fasting sugar | 0.838 |
| $91.30 | age, sex, chest-pain type, ST depression, ST slope (one treadmill ECG) | 0.875 |
| $106.90 | sex, chest-pain type, resting BP, max heart rate, thallium result | 0.878 |
| $191.20 | sex, chest-pain type, resting BP, ST slope, fluoroscopy vessels | 0.902 |
| $293.10 | sex, chest-pain type, ST slope, fluoroscopy vessels, thallium result | 0.911 |

*(Precomputed: logistic regression, 5×3 cross-validation on all 297 patients. This is optimistic, because it is the best of 1,287 panels.)*

## What the program does when you press Run

1. **Classical first.** It checks all 1,287 five-test panels exactly, in milliseconds, at five price weights μ ∈ {0, 0.02, 0.05, 0.1, 0.2}. Greedy selection misses the optimum at 3 of the 5 price weights, so the problem is not trivial.
2. **The quantum step.** It builds five 13-qubit circuits, one qubit per test and one circuit per price weight, and sends them as **one job**:
   - **Start:** each test is "in" with probability 5/13. Keeping only shots with exactly five tests gives an equal superposition of all valid panels, at no gate cost.
   - **Cost layer:** the objective's exact Ising expansion. It includes one three-qubit term for "pay for the treadmill once".
   - **Mixer:** an XY mixer that swaps a test in for a test out. The "exactly five" rule is built into the circuit rather than added as a penalty term. Penalties chosen without knowing the answer made QAOA no better than random in our tests.
   - **Angles:** one QAOA layer with frozen angles, tuned offline on random patient subsamples.
3. **The prediction before the result.** An exact formula gives the chance that one job finds every optimal panel, for the ideal circuit and for two comparison samplers:
   - an **independent-choice sampler**, with the same per-test odds as the circuit but tests drawn independently;
   - **uniform** five-test panels.
4. **The measured comparison:**
   - per price weight, P(optimal panel) with 95% intervals;
   - whether the best sampled panel is the true optimum;
   - a log-likelihood test of whether the samples carry the circuit's correlations;
   - simulated annealing and local search given the same number of evaluated panels.

In simulation, one 1,000-shot job finds all the optimal panels with probability **98%**, against 63% for the independent-choice sampler and 11% for uniform. It is **94%** under IonQ Forte-like noise.

## How to run

Press **Run**. The defaults pick sensible shots per simulator: built-in 1000, IonQ 500, IBM noise models 8. Run settings:

| Setting | Meaning |
|---|---|
| `circuits` | `all` = 5 price points plus a bit-order check, in one job; `single` = one circuit (`single_mu`) |
| `shots` | Shots per circuit (0 = automatic) |
| `seed` | Seed for the simulator and the classical baselines |
| `run_baselines` | Run simulated annealing and local search at matched evaluations |
| `dump_counts` | Print the raw counts as JSON |

On IonQ the entire run is exactly one job. Use Chrome, Edge, Brave, Opera or Firefox 153+; Safari cannot run Qollab projects.

## What this does not claim

- **No advantage over exhaustive search**, which is exact and instant at 13 tests. The comparison is about **sample quality at equal numbers of samples**, not speed.
- Prices are 1992 Ontario fees, used as *relative* costs.
- The patients are a symptomatic referral cohort, not a screening population.

## Pre-existing work, AI use, credits

- **Built during the window.** This project was built Oct 9–11, 2026, during the hackathon. The research behind it (Oct 9–10) is in the GitHub repo under `research_notes/`.
- **AI assistance.** Code and text were written with AI assistance (Claude) and reviewed by the team, who are responsible for them.
- **Libraries:** Qiskit, NumPy.
- **Methods:**
  - the XY-mixer QAOA follows Hadfield et al. (2019) and Wang et al. (2020);
  - Kipu Quantum and IonQ (2026) ran trapped-ion feature selection as a precedent.
- **Data:**
  - UCI Heart Disease, Cleveland subset (Janosi, Steinbrunn, Pfisterer, Detrano 1989), CC BY 4.0. Six rows with missing values were dropped and a binary target added.
  - Test costs from Turney (1995), JAIR 2:369–409, distributed with the UCI data.
  - See `DATA_NOTICE.md`.
- **Licence:** MIT (`LICENSE`).
