# Data notice

The **code** in this repository is MIT-licensed (see `LICENSE`). The **data** it uses is not ours. It is redistributed under its own licence, with attribution as follows.

## UCI Heart Disease (Cleveland subset)

- **Source:** UCI Machine Learning Repository, *Heart Disease* dataset (id 45), https://archive.ics.uci.edu/dataset/45/heart+disease
- **Creators:** Andras Janosi, M.D. (Hungarian Institute of Cardiology, Budapest); William Steinbrunn, M.D. (University Hospital, Zurich); Matthias Pfisterer, M.D. (University Hospital, Basel); Robert Detrano, M.D., Ph.D. (V.A. Medical Center, Long Beach, and Cleveland Clinic Foundation). Donated 1988.
- **Citation:** Janosi, A., Steinbrunn, W., Pfisterer, M., & Detrano, R. (1989). *Heart Disease* [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C52P4X
- **Licence:** Creative Commons Attribution 4.0 International (CC BY 4.0), https://creativecommons.org/licenses/by/4.0/
- **Changes we made**, as CC BY 4.0 requires us to indicate. The file `five_tests_priced/data/heart_cleveland_297.csv` is derived from `processed.cleveland.data`:
  1. The 6 rows with missing values (`?` in `ca` or `thal`) were dropped, leaving 297 rows.
  2. A binary `target` column was added (0 if `num` = 0, else 1).
  3. The file was converted to CSV with a header row.
  
  No values were otherwise altered.
- **Cohort caveat:** these are symptomatic patients referred for coronary angiography, not a general screening population.

## Test costs (Turney 1995)

- **Source:** the `costs/` folder distributed inside the same UCI Heart Disease archive (`heart-disease.cost`, `.expense`, `.group`, `.delay`).
- **Origin:** Peter D. Turney, *Cost-Sensitive Classification: Empirical Evaluation of a Hybrid Genetic Decision Tree Induction Algorithm*, Journal of Artificial Intelligence Research 2 (1995) 369–409, https://arxiv.org/abs/cs/9503102. The costs are from the Ontario Ministry of Health fee schedule (October 1992), in Canadian dollars.
- **Use here:** `heart-disease.expense` and `heart-disease.group` are shipped unchanged in `five_tests_priced/data/`. Each test's full cost, its discounted cost, and its shared-procedure group (A = {chol, fbs}, B = {thalach, thal}, C = {exang, oldpeak, slope}) are also written as code constants, and every Run checks them against these files. We treat them as **relative** prices, not as current prices.
- The cost files carry no separate licence. We treat them as part of the UCI archive (CC BY 4.0) and credit Turney.
