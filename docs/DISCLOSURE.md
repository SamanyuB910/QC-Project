# Pre-existing work and outside sources

The hackathon build window ran from **Fri Oct 9, 2026, 19:00 ET to Sun Oct 11, 2026, 19:00 ET**. Qollab's rules require us to say what existed before the window and to credit everything we used.

## What existed before the window (background research, not used by the project code)

These files were created **before 19:00 ET on Oct 9** (file modification times). They are general background research on the event rules, the Qollab platform, IonQ hardware and possible themes. **No code or text from them is part of the project** in `five_tests_priced/`.

| Path | Created | Content |
|---|---|---|
| `reports/Qollab IonQ hackathon track.md` | Oct 7 | Event rules, dates and judging criteria |
| `research_notes/Qollab IonQ hackathon track/` | Oct 7 | Notes behind that report |
| `reports/Quantum Unlocked theme deep dive.md`, `research_notes/Quantum Unlocked theme deep dive/` | Oct 9, 14:50–15:34 | A different theme (education); platform runtime notes |
| `reports/Quantum Impact theme deep dive.md`, `research_notes/Quantum Impact theme deep dive/` | Oct 9, 17:07–17:48 | Survey of application areas, benchmarking practice, platform notes |

Facts about Qollab's runtime were taken from these notes and re-checked against Qollab's documentation during the window. Examples: literal file paths, one IonQ job per run, and `BackendSamplerV2` returning zeros on IonQ.

## Built during the window

- `ideation/` (from Oct 9, 20:39 ET) and `research_notes/QCA prompts Quantum Impact plan/`, with its experiment scripts (Oct 10). This is where the Prompt B design was found and tested.
- Everything in `five_tests_priced/`, `tools/` and `docs/` (Oct 10–11). The project modules are ports of the Oct 10 research scripts in `research_notes/QCA prompts Quantum Impact plan/scripts/prompt_b/` (`common.py`, `qsim.py`, `s06_helpers.py`, `s10_pareto_onejob.py`, `s10d`/`s10f`, `s05_downstream.py`).
- The git history (tags `prereg`, `v0-safety`, …) timestamps each stage.

## Outside sources we rely on (credited)

- **Problem statement:** QCA Georgia Tech Qiskit Fall Fest 2026 prompt slides, Prompt B "Heart Disease Readings": the relevance-minus-redundancy QUBO with a "choose exactly k" penalty. We kept the objective but replaced the penalty with a constraint-preserving mixer (see the project page).
- **Data:** UCI Heart Disease (Janosi, Steinbrunn, Pfisterer, Detrano 1989), CC BY 4.0. Test costs from Turney (1995). See `DATA_NOTICE.md`.
- **Methods:**
  - QAOA: Farhi, Goldstone, Gutmann (2014).
  - Constraint-preserving (XY) mixers: Hadfield et al. (2019), *Algorithms* 12, 34; Wang, Rubin, Dominy, Rieffel (2020), *Phys. Rev. A* 101, 012320.
  - Linear-ramp / fixed-schedule ideas: Montañez-Barrera & Michielsen (2024).
  - Precedent for trapped-ion feature selection: Kipu Quantum & IonQ (2026), arXiv:2604.26834.
  - Mutual-information estimator: Kraskov et al. (2004) / Ross (2014) via scikit-learn.
  - Benchmarking practice: Bowles, Ahmed & Schuld (2024); Abbas et al. (2024).
- **Libraries:** Qiskit (Apache-2.0), NumPy, SciPy, scikit-learn, matplotlib (BSD-style), all used as installed packages. No library source is copied into the project.
- **No tutorial code was copied.** The Qiskit quantum-kernel and QAOA tutorials were read, but none of their code is used.

## AI use

AI tools were used during development.
