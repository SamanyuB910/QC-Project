# QCA Prompt B "Heart Disease Readings": research and experiments for a beyond-tutorial Quantum Impact build (Sat Oct 10, 2026)

Scope: UCI Heart Disease (Cleveland, 297 complete rows), choose k = 5 of 13 features with the prompt's QUBO, solved with QAOA, and turned into something more than the tutorial every Georgia Tech team will build. Everything numeric below comes either from a cited web source or from scripts run in this session.

- **Scripts and logs:** [`scripts/prompt_b/`](scripts/prompt_b/), with logs and JSON in [`scripts/prompt_b/results/`](scripts/prompt_b/results/).
- **Environment:** local CPython 3.11, qiskit 2.3.0, qiskit-aer 0.17.2, scikit-learn 1.8. The "plain version" check used a venv with qiskit-optimization 0.7.0, qiskit-algorithms 0.4.0 and qiskit 2.3.1.
- **Verification:** the NumPy QAOA simulators were checked against Qiskit `Statevector` on the real circuits. The total-variation distance was ≤ 1.6e-15 for every configuration tested, including the cubic cost term ([s04_log](scripts/prompt_b/results/s04_log.txt)).
- **No oracle tuning.** Every QAOA schedule was tuned on 12 resampled training instances (bootstrap, or 80% subsamples without replacement), frozen, then evaluated on the full-data instance and on 12 held-out resamples.

Shorthand used throughout:

- **"null|k"** is the independent-choice sampler. It uses QAOA's own per-qubit marginals, conditioned on exactly 5 features being chosen.
- **"uniform-k"** is 1/1287 = 0.00078 per shot.

---

## Q1. Data and cost facts: files, ucimlrepo fields, the 13 features, Turney's test costs, and clinical context

### Takeaway
**The cost files exist.** Peter Turney's `costs/` folder, with `.cost`, `.expense`, `.group`, `.delay` and a README, ships inside the official UCI zip.

- **Source of the numbers:** per-test Canadian-dollar costs from the Ontario Ministry of Health fee schedule of Oct 1, 1992.
- **Shared-procedure discounts** come in three groups: blood draw {chol, fbs}; thallium/exercise {thalach, thal}; exercise ECG {exang, oldpeak, slope}.
- **Exact cost polynomial:** with the discounts, a panel's cost is a polynomial with one cubic term. I verified it on all 8,192 subsets.
- **The data cannot be fetched live.** The legacy `machine-learning-databases/heart-disease/` URL now returns 404, and neither the UCI `data.csv` nor the zip sends CORS headers. The data must ship as a file; my 297-row CSV is 19 KB.
- **The clinical guideline baseline is three $1 history items.** Pre-test probability guidelines use age, sex and chest-pain type. On this data those three alone give a cross-validated AUC of 0.839 for $3.

### Cited Findings
**Files and loaders**
- **UCI dataset page:**
  - It states "This dataset is licensed under a Creative Commons Attribution 4.0 International (CC BY 4.0) license", gives DOI 10.24432/C52P4X and 303 instances, and shows the loader `fetch_ucirepo(id=45)`.
  - It says "To see Test Costs (donated by Peter Turney), please see the folder 'Costs'".
  - Requested citation: Janosi, Steinbrunn, Pfisterer & Detrano (1989).
  - — [UCI dataset 45](https://archive.ics.uci.edu/dataset/45/heart+disease)
- **UCI API record for id = 45:**
  - `data_url` = `https://archive.ics.uci.edu/static/public/45/data.csv`; target column `num`; missing-value symbol NaN; last updated Nov 3, 2023.
  - The `license` field is null in the API, even though the page states CC BY 4.0.
  - The variable list gives units only for age ("years"), trestbps ("mm Hg") and chol ("mg/dl").
  - It labels `oldpeak` "Integer", but the values are real (for example 2.3).
  - It lists `ca` and `thal` as having missing values.
  - — [UCI API](https://archive.ics.uci.edu/api/dataset?id=45); saved as `scripts/prompt_b/data_raw/uci_api_45.json`
- **Legacy URL is gone.** The folder `https://archive.ics.uci.edu/ml/machine-learning-databases/heart-disease/` (and `/costs/`) returns HTTP 404 as of 2026-10-10.
  - The same files are in `https://archive.ics.uci.edu/static/public/45/heart+disease.zip`: 128,894 bytes, 24 entries including `costs/`, `processed.cleveland.data` (18,461 B), the `WARNING` file, `heart-disease.names` and `ask-detrano`.
  - — local download and test, [zip](https://archive.ics.uci.edu/static/public/45/heart+disease.zip)
- **The loader's file and the processed file are the same data.**
  - `data.csv` (what `fetch_ucirepo(id=45)` downloads) and `processed.cleveland.data` are value-identical: 303 rows; the 6 incomplete rows are ca ×4, thal ×2.
  - After `dropna`: 297 rows; 160 with num = 0 and 137 with num 1–4.
  - Raw distribution of num: 0 = 164, 1 = 55, 2 = 36, 3 = 35, 4 = 13.
  - — [s01_log](scripts/prompt_b/results/s01_log.txt); [heart-disease.names](https://archive.ics.uci.edu/static/public/45/heart+disease.zip)
- **The unprocessed file is unreliable.** The UCI `WARNING` file says `cleveland.data` "has been unfortunately messed up" and `processed.cleveland.data` "seems to be in good shape". Use only the processed file.
- **No CORS on either file.** A `curl` request with `Origin: https://qollab.xyz` to `data.csv` and to the zip returned HTTP 200 with **no** `Access-Control-Allow-Origin` header (local test, 2026-10-10). The shipped file is `scripts/prompt_b/heart_cleveland_297.csv` (19,083 bytes).

**The 13 features**

Sources for the table:
- Meanings and codes: [heart-disease.names](https://archive.ics.uci.edu/static/public/45/heart+disease.zip).
- Costs, groups and delays: `costs/heart-disease.{cost,expense,group,delay}` and [Turney 1995, Table 17](https://arxiv.org/abs/cs/9503102).

| # | Feature | Meaning / units / codes | Full cost (CAD 1992) | Group | Discount cost | Delay |
|---|---|---|---|---|---|---|
| 1 | age | age in years | 1.00 | – | 1.00 | immediate |
| 2 | sex | 1 = male, 0 = female | 1.00 | – | 1.00 | immediate |
| 3 | cp | chest pain: 1 typical angina, 2 atypical, 3 non-anginal, 4 asymptomatic | 1.00 | – | 1.00 | immediate |
| 4 | trestbps | resting blood pressure, mm Hg, on admission | 1.00 | – | 1.00 | immediate |
| 5 | chol | serum cholesterol, mg/dl | 7.27 | A (blood draw) | 5.17 | delayed |
| 6 | fbs | fasting blood sugar > 120 mg/dl (1/0) | 5.20 | A | 3.10 | delayed |
| 7 | restecg | resting ECG: 0 normal, 1 ST-T abnormality, 2 probable/definite LVH | 15.50 | – | 15.50 | delayed |
| 8 | thalach | maximum heart rate achieved | 102.90 | B | 1.00 | delayed |
| 9 | exang | exercise-induced angina (1/0) | 87.30 | C (exercise ECG) | 1.00 | delayed |
| 10 | oldpeak | ST depression induced by exercise relative to rest | 87.30 | C | 1.00 | delayed |
| 11 | slope | slope of peak-exercise ST segment: 1 up, 2 flat, 3 down | 87.30 | C | 1.00 | delayed |
| 12 | ca | number of major vessels (0–3) "colored by flourosopy" | 100.90 | – | 100.90 | delayed |
| 13 | thal | 3 normal, 6 fixed defect, 7 reversible defect | 102.90 | B | 1.00 | delayed |
| – | num (target) | angiographic disease: 0 = < 50% diameter narrowing, 1–4 = > 50% | – | – | – | – |

**Turney's cost files**
- **The README** (Peter Turney, June 7, 1995) explains the files:
  - "The cost is in Canadian dollars. The cost information is from the Ontario Health Insurance Program's fee schedule."
  - Expense semantics: "The full cost is charged when the given test is the first test of its group … The discount cost is charged when the given test is the second or later test of its group."
  - On the treadmill group: "Once you've decided to pay for one of the tests in this group, the others are virtually free. The major cost is the expertise required to interpret the ECG."
  - — `costs/heart-disease.README` in the [UCI zip](https://archive.ics.uci.edu/static/public/45/heart+disease.zip)
- **The paper:** Turney, "Cost-Sensitive Classification: Empirical Evaluation of a Hybrid Genetic Decision Tree Induction Algorithm", JAIR 2:369–409 (1995).
  - Appendix A says the costs are "based on information from the Ontario Ministry of Health (1992)", and that "the relative costs are important, not the absolute costs".
  - "A nominal cost of $1.00 was assigned to the first four tests."
  - Group A blood tests "share the common cost of $2.10 for collecting blood".
  - Groups B and C "involve measurements of the heart during exercise".
  - Turney deleted cases with missing values and kept 296 (we get 297).
  - Reference: Ontario Ministry of Health (1992), *Schedule of benefits: Physician services under the health insurance act*, October 1, 1992.
  - — [arXiv cs/9503102](https://arxiv.org/abs/cs/9503102); [JAIR](https://jair.org/index.php/jair/article/view/10129); DOI 10.1613/jair.120
- **Exact cost polynomial (my derivation, verified).** Let d_i be the discount cost and s_A = 2.10, s_B = 101.90, s_C = 86.30 the shared procedure costs. Then:
  - cost(x) = Σ d_i x_i + s_A·OR(chol, fbs) + s_B·OR(thalach, thal) + s_C·OR(exang, oldpeak, slope)
  - OR(a, b, c) = a + b + c − ab − ac − bc + abc, so the exercise-ECG group contributes the **only cubic term**.
  - The polynomial equals the table-driven Turney cost on all 8,192 subsets (max |diff| 1.4e-14).
  - Five-feature panels range from **$9.20** (age, sex, cp, trestbps, fbs) to **$313.87**; all 13 features cost $323.97.
  - — [s06_log](scripts/prompt_b/results/s06_log.txt), [s06_helpers.py](scripts/prompt_b/s06_helpers.py)
- **Licence of the cost files.** They sit inside the UCI dataset folder, which the page licenses as CC BY 4.0. They carry no separate licence text; the README is a technical note.
  - Attribute both Turney (1995) and the four principal investigators that `heart-disease.names` asks to be named: Janosi, Steinbrunn, Pfisterer, Detrano.
  - — [UCI page](https://archive.ics.uci.edu/dataset/45/heart+disease); `heart-disease.names`

**Clinical context**
- **Origin of the data:** Detrano et al., Am J Cardiol 64:304–310 (1989), PMID 2756873.
  - A discriminant function was derived from 303 Cleveland Clinic angiography patients.
  - Validation cohorts and disease prevalence: Budapest 425 (38%), Long Beach VA 200 (75%), Zurich/Basel 143 (84%).
  - The authors judged it "clinically useful" for chest-pain patients at intermediate prevalence.
  - The label is angiographic stenosis above 50%. So this is a **diagnostic, symptomatic-referral** population, not general-population screening.
  - — [Europe PMC, PMID 2756873](https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:2756873%20AND%20SRC:MED&resultType=core&format=json); [UCI API intro_paper](https://archive.ics.uci.edu/api/dataset?id=45)
- **ESC 2019 chronic coronary syndrome guidelines:**
  - Pre-test probability (PTP) is estimated from three inputs: **age, sex and type of symptoms**.
  - A "clinical likelihood" step then adds risk factors, resting-ECG changes, LV dysfunction, and "findings of exercise ECG or coronary calcification".
  - Exercise ECG "has limited power to rule in or rule out obstructive CAD". An imaging test is recommended instead of exercise ECG as the initial non-invasive test where possible.
  - "Coronary calcium detection by computed tomography is not recommended for identifying individuals with obstructive CAD."
  - — [Saraste & Knuuti, Herz 45:409–420 (2020), PMC7391397](https://pmc.ncbi.nlm.nih.gov/articles/7391397)
- **General-population risk calculators use none of the specialist tests:**
  - ACC/AHA Pooled Cohort Equations: age, sex, race, total cholesterol, HDL-C, systolic BP, BP treatment, diabetes, smoking.
  - AHA PREVENT (2023/2024): age 30–79, sex-specific and race-free; total and HDL cholesterol, systolic BP, BP-lowering and statin treatment, diabetes, smoking, eGFR.
  - Neither uses exercise-ECG, fluoroscopy or thallium variables.
  - — [PCE, PMC5007709](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5007709/); [PREVENT abstract, Khan et al., Circulation 2024;149:430–449](https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:37947085) (both gathered by a helper agent; whether PREVENT uses BMI is unresolved)
- **Modern US prices are only roughly known:**
  - Single-provider Medicare averages (year unspecified): CPT 93000 (12-lead ECG) about $15 allowed; 93015 (treadmill stress ECG) about $69; 78452 (SPECT myocardial perfusion) about $487.
  - A coronary calcium scan typically costs about $100 out of pocket.
  - These are search-summary-level numbers, **not** national rates.
  - — [CMS look-up tool](https://data.cms.gov/tools/medicare-physician-other-practitioner-look-up-tool/provider/1942279401); [GoodRx CAC](https://www.goodrx.com/health-topic/heart/coronary-artery-calcium-scan-cost) (helper-agent search summaries)

### Inferences
- **The cost files make "cheap screening test" literal, and the cost is natively higher-order.**
  - Two of the three discount groups are quadratic OR terms (−s·x_a x_b). The exercise-ECG group needs one cubic term.
  - These terms are *attractive* (negative couplings): picking one exercise-ECG feature makes the other two almost free.
  - That is a real complementarity, which greedy and additive selectors handle badly (Q2 and Q6 show greedy failing on the cost-aware objective).
- **Two framing corrections for the page:**
  - The data is a symptomatic referral cohort (Detrano). So "screening" should be phrased as "first-line triage panel for chest-pain patients", not population screening.
  - Turney's prices are 1992 Canadian dollars. Present them as *relative* costs, as Turney did, with modern US anchors (ECG about $15, treadmill about $69, SPECT about $487) as a sanity check only.
- **The ESC PTP inputs give a natural guideline baseline.** Age, sex and cp are exactly three $1 features. Their cross-validated AUC of 0.839 (Q4) is the honest bar any 5-feature panel must clear to justify spending on exercise or imaging tests.

### Gaps
- I did not install `ucimlrepo` itself. I checked its fields through the UCI API JSON and the identical `data.csv` it downloads.
- There is no separate licence statement for the `costs/` files. Treat them as part of the CC BY 4.0 dataset, with attribution to Turney.
- I have no modern national Medicare or CMS fee-schedule numbers for these CPT codes; the figures above are single-provider averages from search summaries.
- Detrano 1989's full text was not read, so the exact clinical protocol for `ca` (fluoroscopic calcification) and `thal` (thallium scintigraphy) is described only as the UCI names file states it.

---

## Q2. The prompt's QUBO exactly as specified: r_i, c_ij, exact enumeration, λ/P sweeps, classical baselines

### Takeaway
**As specified, the instance is classically trivial and badly scaled.**
- **Greedy mRMR finds the exact optimum.** It does so at λ ≤ 0.2 on the full data, and on 58–83% of held-out resamples. Exact enumeration takes about 3 ms to build all 8,192 energies and sort the 1,287 feasible ones (0.05 ms to re-rank once the energies exist).
- **The prompt never fixes λ, and the units clash.**
  - r_i is mutual information in nats (0–0.146); c_ij is a correlation in [0, 1].
  - For λ ≥ 0.5 the redundancy term dominates. The "optimal" panel then contains fasting blood sugar, whose MI is 0.0000, and is a median-quality classifier (rank 669 of 1,287 by CV AUC).
  - For λ ≥ 0.75 the optimum f\* is positive, so the prompt's approximation ratio f/f\* changes sign and becomes meaningless.
- **The penalty needed is tiny, but qiskit-optimization's automatic penalty is huge.**
  - P\* = 0.035 is enough at λ = 0.2, but qiskit-optimization picks 4.35, which is 125× too big.
  - Writing the constraint with fractional coefficients makes it fall back to 1e5.
- **The relevance estimator itself is fragile.** sklearn's default kNN-MI (k = 3) inflates cholesterol's relevance 4–10× relative to k = 10 or binned MI.

### Cited Findings
**Relevance r_i** (all from [s01_log](scripts/prompt_b/results/s01_log.txt), [s07_log](scripts/prompt_b/results/s07_log.txt))
- **Estimator:** `sklearn.feature_selection.mutual_info_classif(X, y, discrete_features=mask, n_neighbors=3, random_state=s)`, averaged over seeds s = 0..19, in nats.
  - Discrete features: sex, cp, fbs, restecg, exang, slope, ca, thal.
  - Continuous features (age, trestbps, chol, thalach, oldpeak) use the Kraskov/Ross kNN estimator. The seed only sets the jitter sklearn adds to break ties.
- **Values (mean ± sd over 20 seeds):**

  | Feature | r_i |
  |---|---|
  | thal | 0.1457 |
  | cp | 0.1367 |
  | ca | 0.1280 |
  | oldpeak | 0.0964 ± 0.0147 |
  | exang | 0.0917 |
  | chol | 0.0818 ± 0.0091 |
  | slope | 0.0754 |
  | thalach | 0.0693 ± 0.0085 |
  | sex | 0.0401 |
  | restecg | 0.0163 |
  | age | 0.0103 ± 0.0124 |
  | trestbps | 0.0043 ± 0.0094 |
  | fbs | 0.0000 |

- **Seed sensitivity:** the top-5-by-MI set takes **5 different values across the 20 seeds**.
- **Estimator sensitivity, cholesterol's r:**

  | Estimator | r_chol |
  |---|---|
  | kNN k = 3 | 0.082 |
  | kNN k = 5 | 0.023 |
  | kNN k = 10 | 0.009 |
  | 5-bin quantile MI | 0.008 |

  - Cholesterol's univariate |AUC − 0.5| is 0.067, 12th of 13 features.
  - The λ = 0.2 QUBO optimum flips from [cp, chol, slope, ca, thal] (k = 3) to [sex, cp, trestbps, slope, ca] (k = 10 or binned MI).
- **Bootstrap makes it worse.** Resampling *with replacement* duplicates rows, which inflates kNN-MI for continuous features. Cholesterol then enters 100% of the bootstrap optima.
  - With 80% subsampling *without* replacement, the full-data optimum is recovered in only **46%** (k = 3) or **42%** (k = 10) of 200 subsamples, across 14–20 distinct optimal panels.

**Redundancy c_ij**
- c_ij = |Pearson r| on the raw numeric codes. Note that cp, restecg, slope and thal are nominal codes, so Pearson on them is a convention, not a measurement.
- Mean c_ij is 0.157 over the 78 pairs. The largest are oldpeak–slope 0.579, age–thalach 0.395, thalach–slope 0.389, thalach–exang 0.384 and sex–thal 0.384.
- The Σ c_ij over all pairs (i < j) is 12.27, versus Σ r_i = 0.896. — [s01_log](scripts/prompt_b/results/s01_log.txt)

**Exact optimum across λ** (enumeration over 1,287 subsets; feature costs from Q1) — [s01_log](scripts/prompt_b/results/s01_log.txt)

| λ | Optimal panel | f\* | Gap to 2nd | Turney cost |
|---|---|---|---|---|
| 0 | cp, exang, oldpeak, ca, thal (= SelectKBest-MI) | −0.599 | 0.0099 | $293.10 |
| 0.02–0.05 | cp, chol, oldpeak, ca, thal | −0.55 / −0.50 | 0.005 | $299.37 |
| 0.1–0.2 | **cp, chol, slope, ca, thal** | −0.417 / −0.266 | 0.012 / 0.009 | $299.37 |
| 0.3 | sex, cp, chol, slope, ca | −0.154 | 0.006 | $197.47 |
| 0.5–5 | sex, cp, chol, **fbs**, slope | −0.019 at λ = 0.5; **+0.138 at 0.75, +0.296 at 1.0** | 0.04–0.11 | $99.67 |

**Penalty sweep** (smallest P that makes the global minimum over all 2^13 states feasible) — [s01_log](scripts/prompt_b/results/s01_log.txt), [s02_log](scripts/prompt_b/results/s02_log.txt)
- **Critical penalty P\*:**

  | λ | P\* |
  |---|---|
  | 0.1 | ≤ 0 (any P works) |
  | 0.2 | 0.035 |
  | 0.3 | 0.065 |
  | 0.5 | 0.103 |
  | 1.0 | 0.239 |

- **What qiskit-optimization 0.7.0 actually picks:**
  - `LinearEqualityToPenalty` chooses **P = 4.349** for the integer constraint Σx = 5 at λ = 0.2, which is 125× P\*.
  - The same constraint written as Σ 0.2·x_i = 1 triggers the logged fallback "Using 100000.000000 for the penalty coefficient because a float coefficient exists in constraints".
- **How much of the energy scale the objective keeps** (in units of the cost Hamiltonian's standard deviation, λ = 0.2):

  | Penalty | Spread of the 1,287 feasible energies | Optimum-to-2nd gap |
  |---|---|---|
  | P\* | 1.17 | 0.019 |
  | P_safe = max_i(r_i + λΣ_j c_ij) = 0.644 | 0.118 | 1.9e-3 |
  | qiskit auto 4.35 | 0.018 | 2.9e-4 |
  | 1e5 | ~0 | 1.3e-8 |

  — [s01b_log](scripts/prompt_b/results/s01b_log.txt)

**Classical baselines at λ = 0.2** (rank among 1,287; normalised AR = (f_worst − f)/(f_worst − f\*)) — [s01_log](scripts/prompt_b/results/s01_log.txt)

| Method | Rank | Normalised AR |
|---|---|---|
| Exact | 1 | 1.000 |
| Greedy mRMR | **1** | 1.000 |
| SelectKBest-MI | 572 | 0.61 |
| SelectKBest-F | 1,042 | 0.42 |
| SelectKBest-χ² | 869 | 0.50 |
| L1-logistic first 5-feature model (C = 0.021): cp, thalach, exang, ca, thal | 849 | 0.51 |

- **Simulated annealing** (swap moves inside k-subsets, 300 restarts), P(finds the optimum) by evaluation budget:

  | Evaluations | P(finds optimum) | 95% CI |
  |---|---|---|
  | 10 | 0.027 | – |
  | 25 | 0.14 | – |
  | 50 | 0.36 | – |
  | 100 | **0.73** | [0.67, 0.77] |
  | 200 | 0.91 | – |
  | 1,000 | **1.00** | [0.987, 1] |

- **Uniform random k-subset:** 1/1287 per draw; mean normalised AR 0.574.
- **λ = 0.5:** greedy ranks 3rd.
- **Held-out resamples (λ = 0.2):** greedy is optimal on 83% of bootstrap and 58% of subsample instances. — [s03_qaoa logs](scripts/prompt_b/results/s03_summary.txt)

### Inferences
- **The prompt's "approximation ratio" needs a defined normaliser.** f/f\* only works when f\* < 0 and every compared f < 0. I recommend reporting:
  - the normalised AR over the feasible set, (f_worst − f)/(f_worst − f\*);
  - P(optimum) per shot;
  - best-of-N AR.
- **Ground λ in units, or let the data choose it.** Two options:
  - Normalise r and c to comparable scales. Equal average weight for a 5-panel is λ ≈ (5·mean r)/(10·mean c) = (5×0.069)/(10×0.157) ≈ 0.22.
  - Pick λ by inner cross-validation. Q4 shows λ = 0.1 with a debiased estimator tracks downstream AUC best.
- **Any team that pastes the prompt into qiskit-optimization is solving a penalty problem, not the feature problem.** The objective occupies under 2% of the energy scale at the automatic penalty.

### Gaps
- I did not test other redundancy measures (pairwise MI, as in Mücke et al., or Cramér's V for the nominal features). With nominal codes, Pearson correlation is a modelling choice that the prompt makes for the team.

---

## Q3. Quantum experiments: penalty QAOA, XY mixers, independent-choice null, uniform/SA, gate counts, noise

### Takeaway
**Penalty-QAOA (the plain version) learns the penalty, not the panel.**
- At p = 1–3 it gives P(opt) of 0.0004–0.0024 per shot, at or below uniform-k (0.00078) and the null|k.
- Its feasible-sample AR is about 0.58, the same as random.

**Constraint-preserving XY mixing helps, but with caveats.**
- The complete-graph XY mixer from a Dicke start (frozen, transferred angles) reaches P(opt) = 0.018 / 0.08 / 0.16 at p = 1/2/3: 23–210× uniform with 100% feasibility.
- Most of that gain is reproduced by an independent-choice sampler using QAOA's own marginals: QAOA / null|k = 1.0–1.7× on the prompt's QUBO.
- The ring XY mixer is weak, often below null|k.
- Warm starts are degenerate: greedy is already optimal, and top-k never moves.

**The cost-aware HUBO shows the largest QAOA-vs-null gap** (Q6): up to 3.9×.

**Hardware cost is the binding constraint.**
- On all-to-all hardware, p = 1 complete-XY costs 234 RZZ, against 695 two-qubit gates on heavy-hex.
- Under forte-1 depolarizing rates, P(opt|feasible) drops from 0.019 to 0.012 at p = 1, and from 0.082 to 0.014 at p = 2. That falls to or below the ideal null|k.

**Two engineering results are directly reusable:**
1. A product-RY start plus post-selection on Hamming weight 5 reproduces Dicke-start QAOA *exactly* with zero extra two-qubit gates. Bärtschi–Eidenbenz Dicke preparation costs 290 RZZ.
2. The plain `MinimumEigenOptimizer(QAOA(StatevectorSampler()))` path is impractically slow at 11–13 qubits unless the ansatz is decomposed first.

### Cited Findings
**Protocol** — [s03_qaoa.py](scripts/prompt_b/s03_qaoa.py), [s03_summary.txt](scripts/prompt_b/results/s03_summary.txt)
- 2p angles were tuned by Nelder–Mead on 12 training resamples and frozen.
- Two training objectives were used:
  - "E": mean normalised ⟨E⟩. This needs no optimum knowledge.
  - "Popt": mean P(opt) of each *training* instance's own optimum.
- Results are reported on the full-data instance; "held-out" is the mean over 12 other resamples.
- Energies were normalised by their standard deviation over the space the mixer reaches.
- Mixer convention: exp(+iβX) = RX(−2β) and exp(+iβ(XX+YY)/2) = XXPlusYYGate(−2β).

**(a) Penalty QAOA, λ = 0.2, P = P_safe = 0.644** (also P = 0.3·P_safe; 1,000-shot Wilson CIs)

| p | P(opt)/shot | null\|k | P(feasible) | AR \| feasible |
|---|---|---|---|---|
| 1 | 0.0004–0.0005 | 0.0008 | 0.48–0.58 | 0.577 |
| 2 | 0.0005–0.0008 | 0.0008–0.0011 | 0.60–0.80 | 0.58–0.61 |
| 3 | 0.0007–0.0024 | 0.0009–0.0025 | 0.51–0.90 | 0.58–0.68 |

- Uniform-k AR is 0.574.
- λ = 0.1 and λ = 0.5 give the same picture.
- — [s03_summary](scripts/prompt_b/results/s03_summary.txt)

**Plain-version emulation** (qiskit auto P = 4.349, COBYLA maxiter 100 on the instance's own ⟨E⟩, random initial angles, 10 seeds, 1,024 shots, return the best sample)
- P(opt)/shot is 0.0002–0.0004; P(feasible) 0.23–0.47; AR|feasible 0.55–0.59.
- The "best of 1,024 shots equals the optimum" outcome happened in 0–6 of 10 runs.
- For comparison, 1,024 uniform draws over all 2^13 states hit the optimum with probability 0.118, and 1,024 uniform k-subsets with probability 0.55.
- — [s02c_log](scripts/prompt_b/results/s02c_log.txt)

**The library path is slow, which matters for Pyodide**
- Passing the undecomposed `QAOAAnsatz` to `StatevectorSampler`, as `QAOA(sampler=StatevectorSampler())` does, took **6.8 s per sampler call at 9 qubits** and **206 s per call at 11 qubits**, with Python peak allocation of 49 MB and 709 MB.
- The real 13-qubit run reached 6.4 GB RSS and over 16 CPU-minutes without finishing one COBYLA run.
- Decomposing the 13-qubit ansatz to rz/rzz/rx first: **1.1 s per call, 27 MB**.
- Caveat: measured locally under heavy CPU contention, on Qiskit 2.3.1. Qollab runs 2.5.x and was not tested.
- — [s02b_log](scripts/prompt_b/results/s02b_log.txt)

**(b) XY mixers** (λ = 0.2 unless stated; Dicke start; full-data P(opt), with 1,000-shot hits and Wilson CI where shown)

| Mixer and start | p | Tuned on | P(opt) | null\|k | Product null (unconditioned) | Held-out mean (min) |
|---|---|---|---|---|---|---|
| complete, Dicke | 1 | E / Popt | 0.0151–0.0194 | 0.011–0.016 | 0.003 | 0.014–0.023 |
| complete, Dicke | 2 | E | 0.042–0.051 | 0.038–0.043 | 0.010–0.012 | 0.042 |
| complete, Dicke | 2 | Popt | **0.080–0.082** (78/1000, CI 0.063–0.096) | 0.049–0.063 | 0.013–0.017 | 0.063–0.076 |
| complete, Dicke | 3 | E / Popt | 0.105 / 0.164 | 0.102 / 0.148 | 0.030 / 0.043 | 0.10 / 0.13 |
| complete, Dicke, λ = 0.1 | 3 | E | 0.2345 | 0.2291 | 0.084 | 0.209 |
| complete, Dicke, λ = 0.5 | 3 | E | 0.0825 | 0.0554 | 0.015 | 0.052 |
| ring, Dicke | 1–3 | E / Popt | 0.0002–0.0055 | 0.005–0.017 | 0.001–0.004 | 0.004–0.023 |
| ring or complete, greedy k-hot | 1–3 | both | 1.000 (stays put: greedy is optimal; angles collapse to β ≈ 0) | 1.000 | 1.000 | 0.58–0.83 |
| ring or complete, top-5-by-MI | 1–3 | both | 0.0000–0.0015 | ≈ 0 | ≈ 0 | ≤ 0.02 |

- All XY runs are 100% feasible by construction. Uniform-k is 0.00078.
- — [s03_summary](scripts/prompt_b/results/s03_summary.txt)

**(c)/(d) The nulls**
- The unconditioned product null with QAOA's marginals has P(feasible) of only 0.22–0.27. Per raw shot it therefore loses to XY-QAOA by 4–6×.
- Conditioned on k = 5 (a fair classical sampler such as conditional Poisson sampling), it is within 1.0–1.7× of QAOA on the prompt's QUBO.
- **SA and greedy at matched evaluations, counting feasible evaluations:**
  - Noisy complete-XY p = 2 (P(opt|HW5) = 0.0144, about 22% of shots feasible) finds the optimum with about 27% probability from 100 raw shots (about 22 evaluations), against 14% for SA with 25 evaluations.
  - From 1,000 raw shots (about 222 evaluations) the figures are about 96% against 91% for SA with 200.
  - Ideal p = 2 reaches about 1.00 by 100 feasible samples.
  - Greedy, however, needs only 55 evaluations and is exactly optimal on this instance (Q2). On the prompt's QUBO, classical wins.
- — [s01_log](scripts/prompt_b/results/s01_log.txt), [s04_log](scripts/prompt_b/results/s04_log.txt)

**Gate counts**
- Method: transpiled with `basis_gates=['rzz','rx','rz']` and no coupling map (IonQ-like), versus `GenericBackendV2` on `CouplingMap.from_heavy_hex(5)` (57 qubits, cz/rz/sx/x, opt-level 3, best of 3 seeds).
- I had no IBM `FakeBackend` installed, so the heavy-hex numbers are generic.
- Penalty and complete-XY counts below are for the prompt's QUBO. The cost-aware HUBO adds +3 RZZ for the cubic term (234 → 237).

| Circuit | 2Q all-to-all (depth) | 2Q heavy-hex (depth) |
|---|---|---|
| Penalty-QAOA p = 1 | **78** (28) | 312 (447) |
| Penalty-QAOA p = 2 | 156 (43) | 697 (767) |
| XY ring, product start, p = 1 | **104** (47) | 383 (555) |
| XY ring, p = 2 | 208 (91) | 837 (1,111) |
| XY complete, product start, p = 1 | **234** (107) | 695 (849) |
| XY complete, p = 2 | 468 (211) | 1,467 (1,838) |
| XY complete p = 1 with Bärtschi–Eidenbenz Dicke prep | 524 (664) | 1,359 (2,487) |
| Dicke(13,5) prep alone | 290 | – |

- One XY pair costs 2 RZZ. — [s04_log](scripts/prompt_b/results/s04_log.txt)

**"Dicke by post-selection" (zero two-qubit gates)**
- Why it works: RY(θ) on every qubit with sin²(θ/2) = 5/13 gives every Hamming-weight-5 basis state the same amplitude, so its HW = 5 component *is* the Dicke state. Diagonal cost layers and XY mixers never mix Hamming-weight sectors.
- Measured P(HW = 5) = C(13,5)(5/13)^5(8/13)^8 = **0.2228**, and the HW = 5-conditional distribution equals Dicke-start QAOA (TVD 6.8e-16).
- Under noise, HW post-selection also discards errors that leak out of the sector. Noisy P(HW5) stayed between 0.200 and 0.228.
- — [s04_log](scripts/prompt_b/results/s04_log.txt), [s10_log](scripts/prompt_b/results/s10_log.txt)

**Noise**
- Model: Aer `depolarizing_error(2.67e-4)` after rx/rz and `(4.95e-3)` after rzz. This matches IonQ's documented forte-1 noise-model parameters (single depolarizing channel per gate, r1q ≈ 0.000267, r2q ≈ 0.004949). 4,000 shots per circuit.
  - — [IonQ noise-model docs via prior notes](https://docs.ionq.com/guides/simulation-with-noise-models); [s04_log](scripts/prompt_b/results/s04_log.txt)
- Results:

  | Circuit | Ideal → noisy P(opt\|HW5) | Noisy 95% CI | Global-fidelity proxy F |
  |---|---|---|---|
  | complete p = 1 | 0.0194 → **0.0123** | [0.0069, 0.0218] | ~0.26 |
  | complete p = 2 | 0.0816 → 0.0144 | [0.0082, 0.0250] | ~0.07 |
  | ring p = 1 | 0.0055 → 0.0047 | – | – |
  | Dicke-prepared complete p = 1 | 0.0194 → 0.0084 | – | – |
  | penalty p = 1 / p = 2 | 0.0004 / 0.0005 → 0.0005 / 0.0005 per raw shot | – | – |

  - The product-start version beats the Dicke-prepared one at the same angles.
- Aer wall time: 15–108 s per 4,000 shots locally.

### Inferences
- **On the prompt's own QUBO there is no honest "quantum advantage" story, but there is an honest measurable one.** Constraint-preserving mixing turns QAOA from "worse than random k-subsets" (penalty) into "20–200× random with 100% feasibility" (XY). The independent-choice null shows most of that comes from single-qubit biases, not entanglement.
- **Resolving QAOA versus null|k needs far more shots than IonQ allows.**
  - At 95% confidence and 80% power, telling 0.0816 from 0.0629 apart needs about 1,400 feasible samples against the exactly computable null|k probability, or about 3,000 per arm against a sampled null.
  - After HW-5 post-selection (22% of shots kept), that is about 6,400–13,500 raw shots.
  - With about 1,000 raw shots on IonQ, the defensible claims are only XY versus penalty and XY versus uniform.
- **Do not warm-start from greedy on this instance.** Greedy is optimal, so the result is trivially P(opt) = 1. It reads as a quantum win and is not one.
- **On IonQ, p = 1 complete-XY with a product start is the sweet spot** (234 RZZ, F ≈ 0.26). Going to p = 2 buys nothing under noise.

### Gaps
- I did not run LR-QAOA with large p (p ≥ 5) because the noise budget rules it out. I also did not test parity-ordered XY mixers or sparser mixer graphs (circulant), which could sit between ring and complete.
- I did not run the IonQ cloud simulator itself, which needs a key. IonQ compiles to GPI/GPI2/ZZ natively, so real 2Q counts may differ slightly from my RZZ counts.
- The Qollab Qiskit version (2.5.x) and whether its `StatevectorSampler` slowness on undecomposed `PauliEvolutionGate`s persists are untested.

---

## Q4. Downstream value: nested-CV accuracy, AUC and sensitivity of the panels; is the QUBO optimum the best panel?

### Takeaway
**At λ ≤ 0.2 the QUBO-optimal panel is a good classifier, but not measurably better than simpler selectors.**
- [cp, chol, slope, ca, thal]: AUC about 0.89–0.90 under nested CV, rank 9 of 1,287 panels. SelectKBest-MI, L1-logistic and all 13 features land at 0.88–0.90, with overlapping CIs.

**The prompt's objective is a poor proxy, and gets worse with λ.**
- Spearman ρ between the QUBO objective and CV AUC over all 1,287 panels: 0.80 at λ = 0, 0.41 at λ = 0.2, −0.05 at λ = 0.5. At λ = 0.5 the QUBO optimum is a median panel.

**A debiased relevance estimator fixes the proxy.**
- kNN-MI with k = 10, or binned MI minus a permutation null, gives ρ = 0.91–0.92 at λ = 0.1.
- With the Turney cost term, the QUBO optimum then lands on, or within 0.002 AUC of, the exact cost-versus-AUC Pareto front at μ = 0, 0.02, 0.05, 0.1 and 0.2.

**Honest pipelines with selection inside each fold:**
- QUBO (k = 10, λ = 0.1, μ = 0.1): AUC 0.846 at a mean $101 per patient.
- QUBO (k = 10, λ = 0.1, μ = 0.2): 0.818 at $19.
- All 13 features: 0.897 at $324.
- Routine risk-factor panel (age, sex, trestbps, chol, fbs): 0.695 at $13.

### Cited Findings
**(A) Fixed panels** (chosen once on the full data, so mildly optimistic)
- Method: outer 5-fold × 5 repeats, inner 5-fold grid search.
  - LR: C ∈ {0.01, 0.1, 1, 10}. SVM: RBF kernel, C ∈ {0.1, 1, 10}, γ ∈ {scale, 0.01, 0.1}. GB: 100 trees, depth ∈ {1, 2}.
  - Nominal features (cp, restecg, slope, thal) one-hot encoded, others standardised.
- The table gives the per-repeat mean AUC, with a 95% CI from a patient bootstrap of the repeat-averaged OOF scores. Accuracy and sensitivity are at threshold 0.5 (SVM threshold: 0).

| Panel (Turney cost) | LR AUC | SVM AUC | GB AUC | LR acc / sens |
|---|---|---|---|---|
| QUBO λ = 0.1–0.2: cp, chol, slope, ca, thal ($299.37) | 0.894 [0.864, 0.934] | 0.882 [0.863, 0.934] | 0.899 [0.862, 0.934] | 0.815 / 0.693 |
| QUBO λ = 0 = SelectKBest-MI: cp, exang, oldpeak, ca, thal ($293.10) | 0.893 [0.858, 0.929] | 0.891 | 0.899 | 0.835 / 0.781 |
| L1-logistic 5: cp, thalach, exang, ca, thal ($293.10) | 0.896 [0.860, 0.931] | 0.894 | 0.893 | 0.828 / 0.766 |
| QUBO λ = 0.5: sex, cp, chol, fbs, slope ($99.67) | 0.835 [0.789, 0.878] | 0.823 | 0.838 | 0.758 / 0.781 |
| Greedy mRMR λ = 0.5: cp, chol, fbs, restecg, thal ($129.77) | 0.840 [0.808, 0.891] | 0.804 (sens 0.32) | 0.850 | 0.764 / 0.701 |
| "No imaging": age, sex, cp, thalach, exang ($193.20) | 0.844 [0.807, 0.889] | 0.819 | 0.843 | 0.774 / 0.730 |
| Routine risk factors: age, sex, trestbps, chol, fbs ($13.37) | 0.695 [0.643, 0.759] | 0.697 | 0.685 | 0.650 / 0.613 |
| All 13 ($323.97) | **0.897** [0.865, 0.934] | 0.900 [0.871, 0.936] | 0.899 | 0.855 / 0.803 |

— [s05_AB.log](scripts/prompt_b/results/s05_AB.log)

**(B) Honest pipelines** (the selector re-run inside each outer training fold, LR downstream; per-repeat mean AUC, with averaged-OOF AUC and CI in brackets)

| Selector | Per-repeat AUC | Averaged-OOF AUC [95% CI] | Distinct panels across 25 folds |
|---|---|---|---|
| QUBO λ = 0.1 | 0.872 | 0.887 [0.849, 0.923] | 5 |
| QUBO λ = 0.2 | 0.867 | 0.891 [0.851, 0.924] | 8 |
| QUBO λ = 0.5 | 0.825 | 0.844 [0.798, 0.885] | 6 |
| Greedy λ = 0.5 | 0.832 | 0.872 [0.828, 0.909] | 11 |
| SelectKBest-MI | 0.887 | 0.895 [0.857, 0.928] | 7 |
| L1-logistic | 0.884 | 0.890 [0.852, 0.924] | 4 |
| All 13 | 0.897 | 0.902 [0.865, 0.934] | 1 |

— [s05_AB.log](scripts/prompt_b/results/s05_AB.log)

**(C) All subsets of size 1–5 (2,379 panels)**
- Method: logistic regression with C = 1, repeated 5 × 3 CV AUC, the same folds for every panel.
- Best 5-panel: **sex, cp, slope, ca, thal = 0.911** (optimistic: the maximum over 1,287 panels). Median 5-panel: 0.848.
- QUBO objective vs AUC:

  | λ | Spearman(QUBO f, −AUC) | QUBO optimum's AUC rank |
  |---|---|---|
  | 0 | 0.80 | 15th |
  | 0.05 | 0.79 | – |
  | 0.1 | 0.70 | 9th |
  | 0.2 | 0.41 | 9th |
  | 0.3 | 0.18 | 44th |
  | 0.5 | −0.05 | 669th |
  | 1.0 | −0.22 | – |

- — [s05_C.log](scripts/prompt_b/results/s05_C.log)
- **Cost-versus-CV-AUC Pareto front over all subsets of size ≤ 5** (exact):

  | Cost | Panel | AUC |
  |---|---|---|
  | $1 | cp | 0.755 |
  | $2 | sex, cp | 0.806 |
  | **$3** | **age, sex, cp** | **0.839** |
  | $4 | + trestbps | 0.841 |
  | $19.50 | + restecg | 0.842 |
  | $89.30 | sex, cp, oldpeak | 0.849 |
  | $90.30 | sex, cp, oldpeak, slope | 0.869 |
  | $91.30 | age, sex, cp, oldpeak, slope | 0.875 |
  | $106.90 | sex, cp, trestbps, thalach, thal | 0.878 |
  | $191.20 | sex, cp, trestbps, slope, ca | 0.902 |
  | $206.80 | sex, cp, thalach, ca, thal | 0.904 |
  | $293.10 | sex, cp, slope, ca, thal | 0.911 |

  - The shared-procedure bundles (oldpeak + slope; thalach + thal) both appear on the front.
  - — [s06_log](scripts/prompt_b/results/s06_log.txt)

**Proxy quality** (does the QUBO optimum sit on the cost-AUC front?) — [s08_log](scripts/prompt_b/results/s08_log.txt)

| Estimator | λ | Spearman | Regret at μ = 0 / 0.02 / 0.05 / 0.1 / 0.2 |
|---|---|---|---|
| kNN-MI k = 3 (prompt default) | 0.2 | 0.41 | 0.007 / 0.008 / 0.029 / 0.029 / 0.022 |
| **kNN-MI k = 10** | **0.1** | **0.91** | **0.000 / 0.002 / 0.002 / 0.000 / 0.000** |
| Binned MI − permutation null | 0.1 | 0.92 | 0.000 / 0.000 / 0.000 / 0.000 / 0.007 |

- Regret = best AUC at the same or lower cost, minus the panel's AUC.
- Caveat: λ and the estimator were compared on the same full-data CV table, so this is a *selection* result. (B) and (D) are the honest checks.

**(D) Honest cost-aware pipelines** (selection inside each fold; per-repeat mean AUC; mean panel cost)

| Configuration | AUC | Mean cost |
|---|---|---|
| k = 3, λ = 0.2, μ = 0 | 0.867 | $242 |
| k = 3, λ = 0.2, μ = 0.05 | 0.834 | $146 |
| k = 3, λ = 0.2, μ = 0.1 | 0.819 | $76 |
| k = 10, λ = 0.1, μ = 0 | 0.874 | $290 |
| k = 10, λ = 0.1, μ = 0.02 | 0.868 | $249 |
| **k = 10, λ = 0.1, μ = 0.1** | **0.846** (averaged-OOF 0.868 [0.826, 0.905]) | **$101** |
| k = 10, λ = 0.1, μ = 0.2 | 0.818 (averaged-OOF 0.827 [0.776, 0.870]) | $19 |

- — [s09_log](scripts/prompt_b/results/s09_log.txt)

### Inferences
- **The QUBO optimum is not "the best panel for prediction".** At the λ a team will likely pick (0.2–1), the redundancy term actively *hurts* agreement with downstream AUC.
- **The honest, interesting deliverable is a cost–accuracy frontier.** On it, quantum sampling is one way to enumerate candidate panels, not "the best 5".
- **The clinical punchline is strong and data-backed.**
  - Three $1 history questions (age, sex, chest-pain type) get AUC 0.84.
  - One paid exercise ECG ($86.30 shared) lifts that to 0.875 with oldpeak and slope together.
  - Imaging tests (ca, thal) are needed to reach 0.90 or more.
- **Differences among the top panels (0.89–0.91) are within CI.** Report them as ties.

### Gaps
- I did not compute paired bootstrap CIs for AUC *differences* between panels (OOF scores were not stored). The individual CIs overlap heavily at the top.
- Calibration and decision-curve or net-benefit analyses were not run.
- The all-subsets AUC table used a fixed C = 1, not nested tuning.

---

## Q5. Literature (2019–2026) and existing implementations of quantum feature selection; what the "plain version" looks like

### Takeaway
**The field is well trodden:** MI or correlation QUBOs on D-Wave, QAOA or VQE on tiny IBM devices, and a 2026 IonQ Forte HUBO paper.
- None of the papers reviewed here uses real test costs.
- None reports P(opt) against an independent-choice null.
- None tests whether the QUBO optimum is the best downstream classifier.

**No public QUBO/QAOA feature-selection project on UCI Heart Cleveland was found.**

**The plain version every team will build:**
- `QuadraticProgram` with −r and λc;
- `linear_constraint(Σx == 5)`;
- `MinimumEigenOptimizer(QAOA(StatevectorSampler(), COBYLA, reps=p))`;
- a histogram, and "QAOA found the optimum".

### Cited Findings
- **Mücke, Heese, Müller, Wolter, Piatkowski, "Feature selection on quantum computers"** (Quantum Mach. Intell. 5, 11, 2023; arXiv:2203.13261):
  - QUBO −α Σ I(x_i; y) x_i + (1 − α) Σ I(x_i; x_j) x_i x_j, with 20-bin MI.
  - **No penalty term:** a binary search on α gives exactly k features, with a proof.
  - Hardware: D-Wave Advantage, and an IBM 27-qubit device running **VQE, not QAOA**, on 10 qubits.
  - How often the true optimum was reached: D-Wave 10.78% on synth_10, 0.18% on waveform; SA 100% / 20%; IBM VQE 0.14%.
  - — [arXiv](https://arxiv.org/abs/2203.13261), [ar5iv](https://ar5iv.labs.arxiv.org/html/2203.13261) (via helper agent)
- **Nembrini, Ferrari Dacrema, Cremonesi, CQFS** (Entropy 23(8):970, 2021):
  - Penalty-based cardinality, s(Σx − k)².
  - D-Wave hybrid and QPU on recommender data.
  - The authors say there is "not yet conclusive evidence" that the QPU beats SA.
  - — [MDPI](https://www.mdpi.com/1099-4300/23/8/970) (via helper agent)
- **Otgonbaatar & Datcu** (IEEE JSTARS 14:7057–7065, 2021): MI band-subset QUBO on D-Wave for hyperspectral images (Indian Pines). — [DLR elib](https://elib.dlr.de/143093) (helper agent; qubit counts not verified)
- **Turati, Ferrari Dacrema, Cremonesi, "Feature Selection for Classification with QAOA"** (IEEE QCE 2022; arXiv:2211.02861). This is the closest to the plain version:
  - correlation and MI QUBOs;
  - penalty (Σx − k)²;
  - QAOA p = 1–10 with COBYLA and 100 shots;
  - ibm-perth for p ≤ 6 on the three smallest datasets, including **wine, with 13 features**.
  - "There is no QUBO formulation that outperforms the others."
  - They report classifier accuracy, not approximation ratio or P(opt).
  - — [ar5iv](https://ar5iv.labs.arxiv.org/html/2211.02861) (via helper agent)
- **Kipu Quantum + IonQ, "Quantum Feature Selection with Higher-Order Binary Optimization on Trapped-Ion Hardware"** (arXiv:2604.26834, Apr 2026):
  - HUBO with 1-, 2- and 3-body MI terms plus a hinge-style linear term; no fixed k.
  - IonQ Forte, 32 qubits, about 1,000 ZZ gates, 2,000 shots; digitized counterdiabatic optimization.
  - Features are kept by how often they appear in the lowest-energy 25% of samples.
  - Gallstone, Forte vs SelectKBest: 0.79 vs 0.75 accuracy and 0.88 vs 0.84 AUC. Spambase: 0.9475 vs 0.9414.
  - No quantum-advantage claim and no variance across runs.
  - — [arXiv](https://arxiv.org/abs/2604.26834), [HTML](https://arxiv.org/html/2604.26834v1) (via helper agent)
- **D-Wave `SelectFromQuadraticModel`** (dwave-scikit-learn-plugin):
  - Minimises Σ_{i≠j} |ρ_ij| x_i x_j − 2αk Σ |ρ_iy| x_i with a **hard** k-hot CQM constraint.
  - Defaults: alpha = 0.5, method "correlation", num_features = 10.
  - This is essentially Prompt B's objective, with correlation in place of MI for relevance.
  - — [source](https://raw.githubusercontent.com/dwavesystems/dwave-scikit-learn-plugin/main/dwave/plugins/sklearn/transformers.py) (via helper agent)
- **D-Wave MIQUBO example (Titanic):** linear MI plus conditional-MI quadratic terms. — [GitHub](https://github.com/dwave-examples/mutual-information-feature-selection) (via helper agent)
- **Milne, Rounds, Goddard (1QBit, 2017):** QUBO feature selection for credit scoring on a quantum annealer. — [1QBit](https://1qbit.com/whitepaper/optimal-feature-selection-in-credit-scoring-classification-using-quantum-annealer/) (search summary)
- **Liu et al., "Quantum Feature Selection for Biomedical Data Analysis"** (arXiv:2609.30256, Sep 2026): relevance/redundancy QUBO with BF-DCQO and QAOA on autism metabolomics; "These results do not claim quantum advantage." — [arXiv](https://arxiv.org/abs/2609.30256) (partly search summary)
- **XY-mixer and Dicke-state background:**
  - Wang, Rubin, Dominy, Rieffel, PRA 101, 012320 (2020): ring versus complete XY mixers. — [arXiv:1904.09314](https://arxiv.org/abs/1904.09314)
  - Cook, Eidenbenz, Bärtschi, Max-k-Vertex-Cover: the complete-graph XY mixer beat the ring with Dicke starts. — [arXiv:1910.13483](https://arxiv.org/abs/1910.13483) (search summary)
  - Bärtschi & Eidenbenz, deterministic Dicke states. — [arXiv:1904.07358](https://arxiv.org/abs/1904.07358)
  - "Coupling-Grouped XY-QAOA for Joint Anomaly-Feature Selection" — [arXiv:2606.13244](https://arxiv.org/pdf/2606.13244) (search summary only)
- **Heart Cleveland implementations found:**
  - Only QSVM/VQC classifiers, for example [Ria-K912](https://github.com/Ria-K912/Quantum-ML-Algorithms-for-Heart-Disease-Detection) and [yhubham](https://github.com/yhubham/DISEASE-PREDICTION-QML) (classical ANOVA top-4, then QML).
  - Feature-selection QUBO templates exist on sklearn datasets: [ArunSehrawat](https://github.com/ArunSehrawat/Quantum_Machine_Learning_use_cases_with_Qiskit).
  - No QUBO/QAOA feature selection on Heart Cleveland surfaced in GitHub, Kaggle or blog searches. — (helper agent, extended search)
- **Qollab's own QAOA showcase** uses exactly the plain pipeline on a 2-node maxcut: `MinimumEigenOptimizer(QAOA(sampler=StatevectorSampler(), optimizer=COBYLA(maxiter=50), reps=1))`. — [prior notes: benchmarking_and_build_stack.md](../Quantum%20Impact%20theme%20deep%20dive/benchmarking_and_build_stack.md); [showcase](https://qollab.xyz/u/qollab/showcase-qaoa-qubo)

### Inferences
- **The plain version will report a feasible "optimum" found by QAOA.** That success is mostly best-of-N sampling luck (Q3), and it inherits the penalty trap and the λ unit mismatch.
- **Beyond-tutorial white space, all inside Prompt B:**
  - real per-test costs with shared-procedure discounts (a native cubic term);
  - a QUBO-objective-versus-downstream-AUC audit over all 1,287 panels;
  - constraint-preserving mixing with zero-cost Dicke-by-post-selection;
  - the independent-choice null.
- **Kipu/IonQ is the precedent to cite** for HUBO feature selection on Forte, and for reading features out of the low-energy sample fraction rather than the argmin.

### Gaps
- Several items (Otgonbaatar details, the 2606.13244 paper, Cook et al., Milne, Liu et al.) rest on search summaries, not full reads.
- Absence of a Heart-Cleveland QAOA repo is "not found", not proven.

---

## Q6. Beyond-tutorial extensions inside Prompt B (with measured results)

### Takeaway
Ranked:

1. **E1 Cost-aware screening frontier** (recommended): Turney costs as an exact HUBO, swept over a price μ, sampled in one multi-circuit job.
2. **E2 Penalty versus constraint-preserving mixers**, with Dicke-by-post-selection and noise.
3. **E3 Proxy audit**: QUBO objective versus downstream AUC over all 1,287 panels, plus a debiased-MI fix.
4. **E4 Panel robustness** under resampling.
5. **E5 Conditional-MI 3-body terms** (Kipu-style), the most speculative.

E1 contains E2–E4 as supporting experiments.

### Cited Findings
**E1. Cost-aware screening frontier (Turney costs, HUBO, one job)**
- **Tutorial-bar sentence:** No tutorial prices each heart test from a published fee schedule, encodes "pay for the treadmill once" as an exact three-body term, and samples the whole cost-versus-accuracy frontier in one IonQ job checked against an independent-choice sampler.
- **Formulation:**
  - f_μ(x) = −Σ r_i x_i + 0.1 Σ c_ij x_i x_j + μ·cost(x)/100, with r from kNN-MI k = 10 and cost(x) from Q1 (one cubic term).
  - k = 5 via the complete XY mixer, with a product-RY start and HW = 5 post-selection.
  - p = 1, with one frozen (γ, β) = (1.7182, 0.1676), tuned on 12 subsamples × 5 μ.
- **Exact μ-grid optima on the full data, each on or within 0.002 AUC of the CV-AUC Pareto front:**

  | μ | Panel | Cost | AUC |
  |---|---|---|---|
  | 0 | sex, cp, slope, ca, thal | $293.10 | 0.911 |
  | 0.02, 0.05 | cp, trestbps, thalach, ca, thal | $206.80 | 0.902 (front at that cost: 0.904) |
  | 0.1 | sex, cp, trestbps, thalach, thal | $106.90 | 0.878 |
  | 0.2 | age, sex, cp, trestbps, fbs | $9.20 | 0.838 |

  — [s10_log](scripts/prompt_b/results/s10_log.txt)
- **Measured difference, ideal** (1,000 raw shots per circuit, about 222 feasible each, 200 repeats):

  | Sampler | All 5 μ-optima found | Exact score-Pareto panels found (of 13) | AUC-front panels found (of 8) |
  |---|---|---|---|
  | QAOA | **98%** of runs | 12.7 | 7.18 |
  | null\|k | 62% | 11.0 | 6.04 |
  | uniform-k | 10% | 7.6 | 4.76 |

  - P(opt|HW5) per μ: QAOA 0.006–0.023 versus null|k 0.0025–0.014 versus uniform 0.00078.
  - Noisy forte-1 single job (Aer): all 5 μ-optima, 13/13 Pareto panels, 8/8 AUC-front panels found; noisy P(opt|HW5) 0.000–0.018.
  - The shot-budget and matched-evaluation results are in the E1 shot-budget table below. — [s10_log](scripts/prompt_b/results/s10_log.txt), [s10b_log](scripts/prompt_b/results/s10b_log.txt)
- **Cost-aware instance, k = 3 relevance, λ = 0.2:**
  - Greedy is no longer reliably optimal: ranks 2–5 at μ = 0.01–0.08, and optimal on only 33–50% of held-out subsamples.
  - Complete-XY Dicke p = 2: P(opt) = 0.061 vs null|k 0.016 (**3.9×**) at μ = 0.02; 0.045 vs 0.031 at μ = 0.05.
  - P(sample better than greedy) at μ = 0.05: 0.114 vs 0.058.
  - Held-out mean P(opt) 0.054–0.067. — [s06_log](scripts/prompt_b/results/s06_log.txt)
- **Qubits / gates:** 13 qubits.
  - Per circuit: 234–237 RZZ all-to-all (+3 for the cubic term), about 700 on heavy-hex.
  - One job = 5 circuits, 1,181 RZZ total, far below IonQ's 150,000-gate multi-circuit cap. — [s10_log](scripts/prompt_b/results/s10_log.txt); [IonQ API, via prior notes](https://docs.ionq.com/api-reference/v0.4/jobs/create-job)
- **Judge-run time** (native, single thread):
  - relevance with 20 seeds: 0.33–0.43 s;
  - enumeration: 3 ms;
  - NumPy QAOA simulation: 2 ms per circuit;
  - transpile: 0.06–0.09 s; Statevector: 0.06–0.07 s;
  - Aer ideal 5 × 1,000 shots: 0.24–0.28 s;
  - one panel's 5×3 CV: 0.10 s.

  Estimate under Pyodide at 3–10× slower: **about 5–20 s after packages load**, if the 2,379-panel AUC table is shipped precomputed (240 s natively) and only the 5–8 frontier panels are re-validated live. — [s01b_log](scripts/prompt_b/results/s01b_log.txt); the one-panel CV timing was measured inline this session
- **Build hours and fallback:**
  - About 18 engineering hours plus 6 for documentation and video.
  - **Hour-20 fallback** (≈ Sun 08:00 ET): exact enumeration, cost polynomial, Pareto table, honest CV (all classical, done in this session), plus the 5-circuit job on the ideal simulator. Drop the noisy run and the robustness panel.

**E2. Penalty versus constraint-preserving mixers** (the quantum-method audit)
- **Tutorial-bar sentence:** Instead of trusting the 1e5 or auto penalty, we measure what the penalty costs: penalty-QAOA at 0.0004–0.0024 P(opt) per shot against XY-QAOA at 0.018–0.16, at 100% feasibility, with a zero-gate Dicke start.
- **Results:** see Q3. Penalty p = 1 is 78 RZZ; XY complete p = 1 is 234.
- **Build:** about 8 h on top of E1.
- **Fallback:** report ideal-only numbers.

**E3. Proxy audit: is the QUBO even the right objective?**
- **Tutorial-bar sentence:** We cross-validate all 1,287 possible panels and show the prompt's objective ranks them with Spearman 0.41, at λ = 0.2 with the prompt's own MI estimator. A debiased MI estimate raises that to 0.91 and puts every cost-aware optimum on, or within 0.002 AUC of, the true cost–AUC frontier.
- **Results:** Q4 (C) and the proxy-quality table.
- **Compute:** classical only; ship the table.
- **Build:** about 4 h.

**E4. Panel robustness under resampling**
- **Tutorial-bar sentence:** We show "the optimal five" changes in 54–58% of 80% subsamples, and report per-feature selection frequencies and the panel distribution instead of one panel.
- **Results:**
  - Feature selection frequencies (k = 3): cp 1.00, chol 0.86, ca 0.83, slope 0.82, thal 0.68.
  - The cost-aware μ = 0.05 optimum is spread over 22–23 distinct panels.
  - A pitfall: bootstrap with kNN-MI is biased. — [s07_log](scripts/prompt_b/results/s07_log.txt)
- **Build:** about 3 h. Optional "QAOA sample frequency as a stability score" in the Kipu style.

**E5. Three-body conditional-MI terms (Kipu-style HUBO)**
- **Tutorial-bar sentence:** Add I(x_i; x_j; y) interaction terms to capture synergy that pairwise redundancy misses.
- **Not run.**
- **Cost:** all C(13,3) = 286 triples would cost about 4 RZZ each, so 1,144 extra 2Q per layer, beyond the noise budget. It needs top-m pruning, for example m ≤ 10, adding about 40 RZZ.
- **Risk:** MI-of-triples estimation on 297 rows is very noisy (see E4). Lowest priority.

**E1 shot-budget table (the measurable difference)**

Task: find all five price-point optima in one 5-circuit job. "Feasible" = samples left after HW-5 post-selection. Each cell is the % of 200 simulated jobs that found all five optima, with the mean number found (of 5) in brackets.

| Raw shots per circuit (feasible) | QAOA ideal | QAOA noisy (forte-1) | null\|k (ideal marginals) | Uniform-k | SA, pooled (best T0) | Random-restart 1-swap LS, pooled |
|---|---|---|---|---|---|---|
| 100 (~22) | 8% (2.50) | 2% (1.79) | 0% (1.41) | 0% (0.45) | 0% (1.00) | 0% (0.38) |
| 200 (~44) | 32% (3.62) | 12% (3.04) | 2% (2.40) | 0% (0.84) | 3% (2.10) | 1% (0.93) |
| 500 (~111) | **78%** (4.63) | **66%** (4.46) | 25% (3.78) | 0% (1.82) | 28% (3.92) | 20% (3.65) |
| 1,000 (~222) | **98%** (4.98) | **94%** (4.93) | 62% (4.57) | 10% (3.07) | 55% (4.42) | 63% (4.58) |

- **How the comparison is matched:**
  - The QAOA job's ~5×B feasible samples are pooled, and every price point's optimum is looked for in the pool.
  - SA and local search therefore also run once per price point with B evaluations each, and *all* states they evaluate are pooled.
  - SA schedules T0 ∈ {0.1, 0.3} were checked; T0 ∈ {0.003–0.3} at 222 evaluations gives single-run P(all five) of only 3–8% without pooling.
- **Reference points:**
  - Greedy alone is optimal at only 2 of the 5 price points (rank 3, 7 and **26** at μ = 0, 0.02, 0.1).
  - Greedy + 1-swap local search fixes μ = 0 and 0.02 but stays stuck at μ = 0.1.
  - Exhaustive enumeration (1,287 evaluations per price point, milliseconds) is exact.
- **How the noisy curve was made:**
  - It resamples a 10,000-shot noisy Aer reference distribution per circuit.
  - Noisy P(opt|HW5) was 0.0167 / 0.0055 / 0.0051 / 0.0029 / 0.0186 for μ = 0 / 0.02 / 0.05 / 0.1 / 0.2, against null|k 0.0137 / 0.0044 / 0.0025 / 0.0038 / 0.0039.
  - At μ = 0.1 the noisy circuit is *below* the null, but its optimum still turns up in the other circuits' samples.
- — [s10b_log](scripts/prompt_b/results/s10b_log.txt), [s10c_log](scripts/prompt_b/results/s10c_log.txt), [s10d_log](scripts/prompt_b/results/s10d_log.txt), [s10e_log](scripts/prompt_b/results/s10e_log.txt), [s10f_log](scripts/prompt_b/results/s10f_log.txt)
- **Caveats to print next to this table:**
  - The QAOA angles came from offline classical simulation on 60 training instances, compute that the table does not count.
  - The baselines were only lightly tuned.
  - n = 13 is tiny.
  - The noise is a depolarizing model, not IonQ hardware.
  - This is a sampling-quality result at matched evaluations, **not** a claim of beating exhaustive classical search.

### Inferences
- **E1 is the only extension where the quantum part has a non-trivial job and the problem is literally "cheap screening".** The instance is no longer greedy-solvable, the HUBO is native (no extra qubits), and the deliverable (a frontier with prices) is useful to a clinic. E2–E4 are its evidence sections.
- **Keep the claim scoped.** At 13 features everything is enumerable in milliseconds. The quantum result is "a 237-gate p = 1 circuit samples the right frontier panels more reliably than an independent-choice sampler, SA and random-restart local search at matched pooled evaluations, in simulation, with or without forte-1 depolarizing noise". It is not "better than classical": exhaustive search is exact and instant.

### Gaps
- I did not run E5.
- E1's noisy result comes from one Aer job, plus resampling in s10b from a 10,000-shot noisy reference distribution. I did not run the IonQ simulator itself.

---

## Q7. Recommendation and concrete build outline (including one-job-per-run on IonQ)

### Takeaway
**Build E1, "Five tests, priced": a cost-aware heart-test panel frontier.**
- The prompt's QUBO, with a debiased relevance estimate and Turney's real 1992 test costs.
- Shared procedures appear as exact 2- and 3-body discounts.
- Solved by p = 1 complete-XY QAOA from a zero-gate product start with Hamming-weight post-selection.
- Five price points (μ) run as **one `backend.run([5 circuits])` job**.
- Validated against exact enumeration, greedy, SA, the independent-choice sampler and uniform sampling, with honest nested CV for every panel on the frontier.

**Headline numbers already in hand:**
- $3 → AUC 0.84 (age, sex, cp);
- $91 → 0.875 (add an exercise ECG);
- $107 → 0.878;
- $191–207 → 0.90;
- $293 → 0.911 (CV, optimistic for the top panel).
- QAOA recovers all five price-point optima in **98% of 1,000-shot jobs (94% under forte-1 depolarizing noise)**.
- At matched pooled evaluations the comparison rates are 62% for the independent-choice null, 55% for simulated annealing, 63% for random-restart local search and 10% for uniform.
- At 500 shots: 78% / 66% (QAOA ideal / noisy) versus 20–28% for the classical heuristics.

### Cited Findings
- **One job per run.**
  - Qollab: "IonQ backends accept one job per run, so everything an IonQ run measures must go in one circuit" (FAQ).
  - IonQ's Qiskit docs: multiple circuits go in one job with `backend.run([qc1, qc2])` (multi-circuit job type, up to 5,000 circuits and 150,000 gates).
  - Plan for both readings. Primary: a 5-circuit list in one `backend.run`. Fallback: a single circuit at μ = 0.1, the clinic's operating point.
  - — [prior notes: official_event_details.md / ionq_hardware_and_sdk.md](../Qollab%20IonQ%20hackathon%20track/ionq_hardware_and_sdk.md); [IonQ Qiskit docs](https://docs.ionq.com/sdks/qiskit/index); [Qollab FAQ](https://qollab.xyz/programs/hackathon/how-it-works#faq)
- **Readout:** BackendSamplerV2 returns zeros on IonQ (constraint given), so use `backend.run(...).result().get_counts(i)`.
  - Bitstring-to-subset: int(bitstring, 2) bit i = feature i (Qiskit little-endian). This convention was verified in [s04](scripts/prompt_b/s04_circuits_noise.py) and [s10](scripts/prompt_b/s10_pareto_onejob.py).
- **Recommended shot budget:**
  - 1,000 shots per circuit (about 222 feasible after post-selection) recovers all frontier optima in 98% of ideal runs and 94% of noisy (forte-1 depolarizing) runs.
  - If IonQ's per-shot simulation is slow, use 200–500 shots per circuit and report the s10b curve.
- **Circuit recipe** (13 qubits, about 237 RZZ):
  1. RY(2·asin√(5/13)) on all qubits.
  2. Cost layer: RZ for 1-body, RZZ for 2-body, and a CX–RZ–CX ladder for the single 3-body (exang, oldpeak, slope) term. Coefficients come from an exact Walsh expansion of f_μ, divided by its feasible-set standard deviation.
  3. 78 XXPlusYY(−2β) gates over a round-robin pair ordering.
  4. Measure, and keep bitstrings with exactly five 1s.
  - Verified against the NumPy simulator: TVD 1.6e-15. — [s10_pareto_onejob.py](scripts/prompt_b/s10_pareto_onejob.py)

### Inferences
**Build outline** (~30 h from Sat ~13:00 to Sun 19:00 ET; 2–4 people)

1. **Data and cost module (Sat 12–15).**
   - Ship `heart_cleveland_297.csv` (19 KB) and the Turney cost table, with the README attribution.
   - Code `cost_vector()` and the OR polynomial.
   - Unit-test it against the table on all 8,192 subsets.
2. **Classical core (Sat 15–20).**
   - Relevance: kNN-MI k = 10, 20 seeds; redundancy |Pearson|; λ = 0.1.
   - Exact enumeration, μ sweep, greedy, SA at matched evaluations, uniform.
   - Ship the precomputed 2,379-panel CV-AUC table and the Pareto front. The page highlights the clinical ladder: $3 / $91 / $107 / $191 / $293.
3. **Quantum core (Sat 20 – Sun 02).**
   - Schedule tuner: an offline script that tunes (γ, β) on 12 subsamples × 5 μ and freezes it.
   - Ship the angles as constants, with the training script for transparency.
   - Live: build the 5 circuits, then run them on the free local simulator (judge path), and optionally as one IonQ job (forte-1 noise model).
   - Post-select HW = 5, then compute P(opt|HW5) with Wilson CIs, frontier recovery, and the null|k and uniform baselines at matched shots.
4. **Audits (Sun 02–08), i.e. E2–E4.**
   - Penalty-QAOA p = 1 versus XY, with the qiskit auto-penalty demonstration (4.35 and 1e5).
   - Noise panel: precomputed Aer forte-1 numbers.
   - Proxy audit: Spearman by λ and estimator.
   - Robustness: subsample frequencies.
   - **Hour-20 fallback (Sun ≈ 08:00):** items 1–3 on the ideal simulator only.
5. **Docs and video (Sun 08–19).**
   - Project-page sections: problem (the triage clinic); data and licence (CC BY 4.0 + Turney 1995); exact baseline; method; results with CIs; "what this does not claim" (no advantage at n = 13; differences among top panels within CI; 1992 CAD relative costs; symptomatic referral cohort, not population screening; a selection result for λ/estimator noted).
   - Pitfalls box: penalty 4.35 / 1e5; f/f\* undefined; bootstrap kNN-MI bias; greedy warm start is trivial.
   - Video: 2:30.

**Pyodide engineering notes**
- Do **not** pass an undecomposed `QAOAAnsatz` to `StatevectorSampler` (Q3). Build the circuit by hand, as in s10, or use the NumPy simulator for the judge-run statevector.
- Precompute the 2,379-panel AUC table and the tuned angles. Recompute live only the 5–8 frontier panels' CV, 0.1 s each natively.

### Gaps
- The noisy E1 numbers come from an Aer depolarizing model, both a single 1,000-shot job and resampling of a 10,000-shot reference, not from IonQ's own simulator or hardware.
- IonQ cloud-simulator wall time per shot at 13 qubits with about 237 2Q gates is unknown.
- It is untested whether Qollab's IonQ wrapper accepts a list of circuits as one job. Test it on day 1, and fall back to the single μ = 0.1 circuit.
