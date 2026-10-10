# Prompt A, "Can a Quantum Circuit Spot a Tumor?": QSVC quantum-kernel SVM on Wisconsin Diagnostic Breast Cancer (WDBC). Research and experiments for the strongest beyond-tutorial build (as of 2026-10-10, ~13:10 ET)

**Context.** Georgia Tech Qiskit Fall Fest 2026 × Qollab/IonQ, Quantum Impact theme. Every GT team gets the same prompt, so the plain version (ZZ feature map + QSVC on PCA-reduced WDBC, reporting one accuracy) is tutorial-level by construction. The remaining build window is about 30 h.

**Tags:**
- **[Computed]**: numbers I produced in this session. Scripts and raw outputs are in `research_notes/QCA prompts Quantum Impact plan/scripts/prompt_a/`, and each table names its script.
- **[Lit]**: literature. **[Snippet]**: from a search summary only, not checked against full text.

**Environment:** native CPython 3.11 with numpy 1.26.4, scikit-learn 1.8.0, qiskit 2.3.0/2.3.1, qiskit-aer 0.17.2, and qiskit-machine-learning 0.9.1 (installed in `scripts/prompt_a/.venv`). The machine was shared with other agents' jobs, so the wall-clock timings here are pessimistic.

**Simulator check:** my vectorised NumPy simulator of Qiskit's `zz_feature_map` matches `Statevector` and `FidelityStatevectorKernel` to ≤3e-15 on states, kernels and Bloch vectors (n = 2–5, full and linear entanglement; `verify_qiskit.py`).

---

## Q1. What will the plain version look like? (Qiskit tutorials, plus 2019–2026 literature and repo claims)

### Takeaway
The plain submission every team can build in an hour is: z-score → PCA(2–8) → MinMax angles → `zz_feature_map(n, reps=2)` (default entanglement is **full**) → `FidelityStatevectorKernel` → `QSVC()` with C = 1, on a single 80/20 split.

- **[Computed]** With the real qiskit-machine-learning 0.9.1 API, mean accuracy over 25 random splits depends on the angle scaling:
  - MinMax [0,1]: **0.90–0.93** (n = 2–8);
  - MinMax [0,π]: 0.69–0.87;
  - z-scored angles (no MinMax): it **collapses to the majority class (0.61–0.63 accuracy, balanced accuracy 0.50–0.53)**. This reproduces the 0.63–0.64 "ZZ" results in the literature.

  Individual splits range from 0.84 to 0.97 for the same configuration.
- Tuned classical models reach about **0.97–0.98** on the same data.
- Neither reading-list tutorial touches real data: both use 2-qubit `ad_hoc_data`, have no classical baseline, and use no CV.
- The literature runs from the majority-class collapse up to "100%" on a 50-patient test set. The one rigorous nested-CV study (Kakavand et al. 2026) finds quantum kernels **lose** on WDBC.

### Cited Findings

**Reading-list tutorials** (current docs: qiskit-machine-learning 0.9.1, Qiskit 2.5.2)
- **Tutorial 03, "Quantum Kernel Machine Learning":**
  - Data: `ad_hoc_data`, 2 features / 2 qubits. Classification uses `training_size=20, test_size=5, gap=0.3`.
  - Map and kernel: `zz_feature_map(feature_dimension=2, reps=2, entanglement="linear")` with `FidelityQuantumKernel(fidelity=ComputeUncompute(sampler=StatevectorSampler()))`.
  - SVC with a callable kernel, SVC with a precomputed kernel, and `QSVC` **all score 1.00**; the page itself attributes this to the small dataset.
  - Also shown: spectral clustering (NMI 0.73) and KernelPCA + logistic regression (0.95).
  - No classical classifier is scored and there is no CV (one split, seed 12345).
  - Source: [Qiskit ML tutorial 03](https://qiskit-community.github.io/qiskit-machine-learning/tutorials/03_quantum_kernel.html).
- **Tutorial 08, "Quantum Kernel Training":**
  - Same 2-qubit `ad_hoc_data` (20/5).
  - The trainable map is a single **shared** `ry(θ[0])` on both qubits, composed with `zz_feature_map(2)`, using `TrainableFidelityQuantumKernel`.
  - Trainer: `QuantumKernelTrainer(loss="svc_loss", optimizer=SPSA(maxiter=10, learning_rate=0.05, perturbation=0.05), initial_point=[π/2])`.
  - Result: θ ≈ 1.5535, loss ≈ 16.85, **test balanced accuracy 0.8**. No baseline and no CV.
  - Source: [Qiskit ML tutorial 08](https://qiskit-community.github.io/qiskit-machine-learning/tutorials/08_quantum_kernel_trainer.html).
- **QSVC** is `QSVC(*, quantum_kernel=None, **kwargs)`, a subclass of sklearn `SVC` whose default kernel is `FidelityQuantumKernel` — [QSVC API](https://qiskit-community.github.io/qiskit-machine-learning/stubs/qiskit_machine_learning.algorithms.QSVC.html).
- **`FidelityStatevectorKernel`** computes |⟨φ(x)|φ(y)⟩|² from statevectors. `shots=None` means exact; `enforce_psd` is on by default — [API](https://qiskit-community.github.io/qiskit-machine-learning/stubs/qiskit_machine_learning.kernels.FidelityStatevectorKernel.html).
- **[Computed]** In 0.9.1 the signature is `zz_feature_map(feature_dimension, reps=2, entanglement='full', alpha=2.0, data_map_func=None, …)`. Teams who copy tutorial 03's `"linear"` get a chain; teams who don't get **full** entanglement (`verify_qiskit.py`, signature inspection).

**Published WDBC quantum-kernel/QML claims** (survey; WDBC = 569 × 30 unless noted)

| Source | Qubits / reduction | Protocol | Quantum result | Classical baseline | Flaws |
|---|---|---|---|---|---|
| [Kakavand, Strohmeyer, Schlotter, arXiv:2604.18837 (2026)](https://arxiv.org/html/2604.18837v1) | k = 4–14 (NMF/PCA/tree); ZZ full, R = 2 | **Nested CV** (5×3, 5×5), in-fold preprocessing, 16 seeds | Best ideal BA **0.913** (no-entanglement Rot2DoF); best quantum kernel training (QKT) BA **0.968**; ibm_fez hardware BA 0.47–0.76 | **RBF BA 0.976** | Rigorous. Quantum won 0 of 16 seeds; QKT cost ~2,060× compute; 13.6% of QKT configurations converged |
| [Zorlu & Colak, *Diagnostics* 16 (2026)](https://www.citedrive.com/en/discovery/a-robustness-oriented-quantumclassical-hybrid-machine-learning-pipeline-for-breast-cancer-diagnosis-external-validation-explainability-and-rigorous-benchmarking-in-the-nisq-era/) | 8-qubit VQC; ZZ QSVM | Optuna tuning, internal + external validation | **QSVM AUC 0.727**; VQC AUC 0.983 external | RBF-SVM AUC 0.998 / 0.986 external | Strong design. Authors call classical models "near the data ceiling". Full text blocked (403) |
| [Chaudhry et al., arXiv:2604.07856 (2026)](https://www.alphaxiv.org/abs/2604.07856.md) | 6–10 qubits, top-variance features | Single 80/20 split | GA-searched map 91.2%; **ZZ 64.0%** | RBF 93.0% | Single split; variants compared on the test set |
| [Jose P et al., *IET Quantum Commun.* (2024)](https://inspirehep.net/files/12c1dcfb19af78883870e7be6325ba36) | PCA 2–4 | 300 train / **50 test** | ~96–98%, "100%" after NSGA tuning; 98.6–99.4% claimed on IBM hardware | SVM ~92–95% | 50-sample test set; perfect scores; inconsistent tables |
| [Moradi et al., *Sci Rep* 12:1851 (2022)](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC8814029/fullTextXML) | 8/16 features, about 3–4 qubits | 10-fold, 80/20 | qKSVM AUC 0.92–0.93 (IBMQ Melbourne) | cSVM AUC **0.89** | Weak classical baseline (WDBC SVM AUC is normally ~0.99) |
| [Kölle et al., arXiv:2311.05559](https://arxiv.org/abs/2311.05559) | ~5 qubits (amplitude / autoencoder) | Scaling before split; LR chosen on test accuracy | VQC 0.849; hybrid 0.972 | NN 0.974 | Leakage; gains come from the classical parts |
| [Vasques, *Towards Data Science* (2024)](https://towardsdatascience.com/quantum-machine-learning-with-python-kernel-methods-and-neural-networks-d60738aa99e1) | PCA → 2 | 5-fold | ZZ QSVC **≈0.63**; QKT 0.65 | none | Majority-class rate; PCA fit on all data |
| [Bhavya & Murali, ICNCCom 2026](https://icnccom2026.aconf.org/presentation/151.html) | PSO → 8 qubits | not stated | QCNN 92.98% | RBF/LR 95.61% | Authors claim no advantage |
| [Akpinar et al., arXiv:2407.09930 (2024)](https://arxiv.org/abs/2407.09930) | PCA → 5 (**WBC-Original 699**, not WDBC) | no CV found | 0.65–0.98 across 9 maps | none found | Worst case equals the all-benign rate |

- **Classical state of the art since 1994–95:**
  - 97% by tenfold CV on 569 patients, and 100% on 54 new patients — [Wolberg, Street, Mangasarian, *Cancer Letters* 77 (1994)](https://iro.uiowa.edu/esploro/outputs/journalArticle/Machine-learning-techniques-to-diagnose-breast/9984380514102771).
  - "Linearly separable using all 30 input features". The best plane, on 3 features, reached 97.5% by repeated 10-fold CV — [WDBC.doc](https://ftp1.cs.wisc.edu/math-prog/cpo-dataset/machine-learn/cancer/WDBC/WDBC.doc).
- **Benchmarking critiques:**
  - [Bowles, Ahmed, Schuld 2024](https://arxiv.org/html/2403.07059v1): classical out-of-the-box models win; removing entanglement often doesn't hurt. Of 55 surveyed papers, about 40% claimed quantum outperformance.
  - [Gupta et al., *npj Digit. Med.* 8:237 (2025)](https://pmc.ncbi.nlm.nih.gov/articles/PMC12048600/): "no consistent trend to support empirical quantum utility in digital health".

**[Computed] The plain version, run with the real qiskit-ML API** (`exp0_plain_qsvc.py`; 25 random stratified 80/20 splits; scaler and PCA fit on all rows, as most repos do; `zz_feature_map(n, reps=2)` full entanglement; `FidelityStatevectorKernel`; `QSVC` C = 1)

| n qubits | Angle scaling | Mean acc. over 25 splits | Min–max single-split acc. | Balanced acc. | Kernel off-diagonal mean |
|---|---|---|---|---|---|
| 2 | MinMax [0,1] | 0.906 | 0.851–0.939 | 0.887 | 0.62 |
| 2 | MinMax [0,π] | 0.873 | 0.825–0.912 | 0.848 | 0.46 |
| 2 | z-score (no MinMax) | 0.622 | 0.579–0.658 | **0.504** | 0.32 |
| 4 | MinMax [0,1] | **0.928** | 0.886–**0.974** | 0.920 | 0.16 |
| 4 | MinMax [0,π] | 0.793 | 0.746–0.851 | 0.773 | 0.083 |
| 4 | z-score | 0.611 | 0.553–0.667 | 0.529 | 0.069 |
| 8 | MinMax [0,1] | 0.899 | 0.842–0.939 | 0.888 | 0.025 |
| 8 | MinMax [0,π] | 0.688 | 0.649–0.719 | 0.577 | 0.006 |
| 8 | z-score | 0.632 | 0.632–0.632 (**predicts all benign**) | **0.500** | 0.004 |

- **QSVC equals SVC on the precomputed kernel.** A real `QSVC(quantum_kernel=FidelityStatevectorKernel(...)).fit/score` on split seed 0 gave exactly the same accuracy as `SVC(kernel="precomputed")` on the qiskit-ML kernel, in all 9 configurations.
- **Tutorial-08 QKA, applied faithfully to WDBC** (n = 4, MinMax [0,1], 455 training patients; shared RY θ, `svc_loss`, `SPSA(maxiter=10, learning_rate=0.05, perturbation=0.05)`, θ₀ = π/2):
  - SVCLoss went **up** from 78.3 to 96.2: SPSA diverged, because WDBC's loss scale (about 80) is far larger than ad_hoc's.
  - θ ended at −2.10 and test accuracy **fell from 0.921 to 0.877**.
  - The fit took 166 s natively.
- **Cost of the qiskit-ML path:** `FidelityStatevectorKernel` takes **14 / 29 / 57 s** natively for the 569×569 kernel at n = 4 / 8 / 12 on an unloaded machine, against **0.03 / 0.08 / 1.4 s** for my vectorised NumPy simulator of the same map (same values to 1.7e-14; `verify_qiskit.py`). One `QSVC.fit + score` took 55–150 s on the loaded machine.

### Inferences
- **The tutorial bar is "QSVC returns about 0.90–0.93 on one split".** Any number in that band, or any single-split number up to 0.97, is consistent with the plain pipeline plus split luck. Judges who know the dataset will also know that tuned LR/SVM sits at about 0.97–0.98.
- **The commonest WDBC "quantum" failure is angle scaling.** The (π−x_i)(π−x_j) pair term with full entanglement makes the default map extremely high-bandwidth (see Q3), so unscaled z-scores give a near-diagonal kernel and a majority-class classifier. Teams that "fix" this by trial and error on the test split are leaking.
- **What no published WDBC study has done** (to my search's knowledge): nested-CV comparison **and** Huang-style geometric/complexity diagnostics **and** a positive control **and** a clinical operating-point analysis **and** a Forte-noise IonQ job design, all in one project. That combination is the gap Prompt A teams can own.

### Gaps
- I found no Kaggle notebook or GitHub repo with a verifiable QSVC accuracy on WDBC beyond tutorial-style posts. The table is limited to papers and articles.
- For Kakavand et al., the RBF γ tuning and whether QKT's loss is kernel-target alignment were not verified. The Zorlu & Colak full text was blocked (403).

---

## Q2. Rigorous replication: tuned classical models vs fidelity, projected and QKA-trained quantum kernels at 4/8/12 qubits

### Takeaway
**[Computed]** Under 5 repeats × 5-fold nested CV, with scaler and PCA fit inside each outer-training fold and every hyperparameter tuned in an inner 3-fold loop:
- **Classical:** the best models are LR on all 30 features, **0.977 accuracy [0.965, 0.987]**, and RBF-SVM on all 30, **0.974 [0.963, 0.984], AUC 0.994**.
- **Quantum:** every properly tuned quantum kernel lands at **0.955–0.972 accuracy (AUC 0.985–0.994)**. The best is the fidelity kernel at n = 8/12 with the extended bandwidth grid, at 0.970.
- **Paired differences** vs RBF-30 are −0.2 to −1.9 points for the extended-grid kernels, and **no quantum model is better on any metric**.
  - The Nadeau–Bengio corrected 95% CIs include 0 for every extended-grid kernel except PQK-linear\* at n = 8 (−1.4 points, CI upper bound ≈ 0.000).
  - With the first, coarser grid, FQK-full and PQK at n = 12 are significantly worse (−4.5 and −3.6 points).
- **Ablations:** separable (no-entanglement) kernels tie the entangled ones. Kernel training (QKA) raises training alignment 2–6× but **never** beats plain bandwidth tuning.
- **Plain QSVC:** loses 5.6 / 7.4 / **31.6** points at n = 4 / 8 / 12; the CIs exclude 0.

### Cited Findings
**Protocol design sources**
- Nested CV with in-fold preprocessing — [Kakavand et al. 2026](https://arxiv.org/abs/2604.18837).
- Separable-model ablation and full grid search for every model — [Bowles, Ahmed, Schuld 2024](https://arxiv.org/html/2403.07059v2).
- Bandwidth as a hyperparameter — [Shaydulin & Wild, PRA 106, 042407 (2022)](https://arxiv.org/abs/2111.05451); [Canatar et al., TMLR 2023](https://arxiv.org/abs/2206.06686).
- Projected kernel — [Huang et al., Nat. Commun. 12, 2631 (2021)](https://arxiv.org/abs/2011.01938).
- Kernel alignment training — [Hubregtsen et al., PRA 106, 042431 (2022)](https://arxiv.org/abs/2105.02276); [Glick et al., Nat. Phys. 20, 479 (2024)](https://arxiv.org/abs/2105.03406).
- Centred kernel-target alignment (KTA) — [Cortes, Mohri, Rostamizadeh, JMLR 13 (2012)](https://jmlr.org/papers/v13/cortes12a.html).
- Corrected resampled t-test — [Nadeau & Bengio, *Machine Learning* 52 (2003)](https://link.springer.com/article/10.1023/A:1024068626366).

**[Computed] Protocol** (`exp1_nested_cv.py`, `exp1b_lowbw.py`, `analyze_exp1.py`; raw data in `results/exp1_raw.pkl` and `results/exp1b_raw.pkl`; tables in `results/exp1_table.md` and `results/exp1_diffs.md`)
- **Outer loop:** 5 repeats × stratified 5-fold (seeds 1000–1004), so 25 test folds of about 114 patients each. Positive class = malignant (212 of 569).
- **Inner loop:** stratified 3-fold selection by accuracy (AUC breaks ties). C ∈ {0.1 … 10⁴}.
- **Classical grids:** RBF g·(1/n), g ∈ {0.003 … 3}; LR C ∈ {0.01 … 100}; HGB learning rate × leaves × L2.
- **Quantum feature map:** Qiskit's `zz_feature_map` (reps = 2) applied to c·z, where z are unit-variance PCA scores.
  - The first run's grid was c ∈ {0.02 … 1}.
  - Inner CV picked the grid edge (c = 0.02) in 25 of 25 folds at n = 8 and 12, so **I extended the grid to c ∈ {0.0025 … 0.75}** in a second run with the same seeds. Models from that run are marked `*`.
  - Extending a grid whose edge is selected is ordinary grid design; selection stays nested.
- **PQK:** 1-RDM Bloch-vector RBF (γ ∈ {0.1, 0.3, 1, 3} × 1/median distance), built on the full-map states, or on linear-map states for PQK-linear\*.
- **QKA-scale:** per-feature bandwidths learned by SPSA (50 iterations) on centred KTA, using a 250-patient subsample of the outer-train rows, initialised at the CV bandwidth.
- **QKA-RY:** tutorial-08-style trainable RY layer (n parameters), SVCLoss(C = 1), SPSA.
- **ARD-RBF:** the classical control for QKA. The same SPSA/KTA learns per-feature RBF length-scales.
- **QSVC-plain:** MinMax [0,1] angles, full map, C = 1, no tuning.
- **Metrics:** pooled out-of-fold predictions per repeat, averaged over 5 repeats. 95% CIs come from a 2,000-resample patient-level bootstrap, with the same resample applied to all repeats and models, so differences are paired.
- **Deployable operating point:** a threshold set on inner out-of-fold decision scores to give ≥98% sensitivity, then applied untouched to the test fold.

**[Computed] Main results** (accuracy and AUC with 95% bootstrap CI; "Deploy sens/spec" = realised sensitivity and specificity at the inner-calibrated 98%-sensitivity threshold)

| Model | n | Accuracy [95% CI] | AUC [95% CI] | Sens @ 95% spec | Deploy sens / spec | Typical selection |
|---|---|---|---|---|---|---|
| **LR-30** (all features) | 30 | **0.977 [0.965, 0.987]** | 0.990 | 0.968 | 0.973 / 0.920 | C = 1 |
| **RBF-SVM-30** | 30 | 0.974 [0.963, 0.984] | **0.994 [0.988, 0.998]** | 0.973 | 0.979 / 0.937 | g = 0.3–1 |
| HGB-30 (tuned) | 30 | 0.968 [0.955, 0.979] | 0.989 | 0.964 | 0.976 / 0.882 | — |
| LR-PCA | 4 / 8 / 12 | 0.966 / 0.973 / 0.972 | 0.992 / 0.991 / 0.992 | 0.97 | 0.97–0.98 / 0.90–0.91 | — |
| RBF-PCA | 4 / 8 / 12 | 0.961 / 0.969 / 0.972 | 0.992 / 0.993 / 0.994 | 0.97–0.98 | 0.97–0.98 / 0.93–0.94 | — |
| **QSVC-plain** | 4 / 8 / 12 | **0.918 / 0.901 / 0.658** | 0.973 / 0.960 / 0.893 | 0.86 / 0.80 / **0.52** | 0.975/**0.794**; 0.969/**0.717**; 0.977/**0.480** | n_SV = 169 / 401 / **455 of 455** |
| FQK-full (grid ≥ 0.02) | 4 / 8 / 12 | 0.959 / 0.956 / **0.929** | 0.992 / 0.991 / 0.980 | 0.97 / 0.96 / 0.90 | 0.975/0.929; 0.969/0.901; 0.974/0.788 | c = 0.02 (grid edge) |
| **FQK-full\*** | 4 / 8 / 12 | 0.964 / **0.970** / **0.970** | 0.992 / 0.992 / 0.992 | 0.97 / 0.973 / 0.975 | 0.97–0.98 / 0.93 | c = 0.0025–0.005 |
| FQK-linear\* | 4 / 8 / 12 | 0.955 / 0.968 / 0.969 | 0.991 / 0.990 / 0.991 | 0.96–0.98 | 0.98 / 0.91–0.95 | c = 0.0025–0.01 |
| PQK\* (full-map states) | 4 / 8 / 12 | 0.956 / 0.965 / **0.971** | 0.988 / 0.991 / 0.991 | 0.96–0.975 | 0.97 / 0.92–0.94 | c = 0.0025–0.005, γ = 0.1 |
| PQK-linear\* | 4 / 8 / 12 | 0.955 / 0.960 / 0.956 | 0.988 / 0.989 / 0.985 | 0.95–0.97 | 0.98 / 0.85–0.90 | — |
| **SEP** (no entanglers) | 4 / 8 / 12 | 0.963 / **0.972** / **0.972** | 0.993 / 0.993 / 0.993 | 0.97 | 0.97 / 0.93–0.95 | c = 0.02–0.05 |
| QKA-scale | 4 / 8 / 12 | 0.958 / 0.963 / 0.962 | 0.988 / 0.987 / 0.989 | 0.96–0.97 | 0.97 / 0.88–0.90 | KTA 0.08–0.21 → 0.41–0.59 |
| QKA-RY | 4 / 8 / 12 | 0.961 / 0.967 / 0.961 | 0.992 / 0.994 / 0.991 | 0.97 | 0.97–0.98 / 0.89–0.93 | SVCLoss 85–100 → 46–68 |
| ARD-RBF (classical QKA control) | 4 / 8 / 12 | 0.963 / 0.973 / 0.972 | 0.991 / 0.992 / 0.992 | 0.97 | 0.97–0.98 / 0.92–0.93 | KTA 0.22–0.36 → 0.63 |

**[Computed] Paired differences in accuracy** (quantum minus classical; bootstrap 95% CI; Nadeau–Bengio corrected 95% CI over 25 folds)

| Comparison | Δ acc | Bootstrap CI | NB-corrected CI | Δ AUC [boot CI] |
|---|---|---|---|---|
| FQK-full\*(8) − RBF-30 | −0.004 | [−0.012, +0.003] | [−0.018, +0.010] | −0.003 [−0.006, 0.000] |
| FQK-full\*(12) − RBF-30 | −0.004 | [−0.012, +0.003] | [−0.017, +0.008] | −0.002 [−0.004, 0.000] |
| PQK\*(12) − RBF-30 | −0.003 | [−0.011, +0.005] | [−0.016, +0.010] | −0.004 [−0.007, −0.001] |
| SEP(8) − RBF-30 | −0.003 | [−0.010, +0.004] | [−0.018, +0.013] | −0.001 [−0.004, +0.001] |
| FQK-full\*(8) − LR-30 | −0.007 | [−0.016, +0.002] | [−0.022, +0.008] | +0.001 [−0.002, +0.005] |
| FQK-full\*(8) − RBF-PCA(8) (same features) | +0.001 | [−0.005, +0.007] | [−0.011, +0.012] | −0.001 [−0.004, +0.002] |
| QKA-scale(8) − RBF-PCA(8) | −0.006 | [−0.016, +0.004] | [−0.028, +0.016] | −0.006 [−0.011, −0.001] |
| QKA-RY(12) − RBF-PCA(12) | −0.011 | [−0.021, −0.001] | [−0.030, +0.008] | −0.003 [−0.006, +0.001] |
| QSVC-plain(8) − LR-30 | **−0.076** | [−0.091, −0.062] | [−0.103, −0.049] | −0.031 [−0.041, −0.020] |
| QSVC-plain(12) − RBF-30 | **−0.316** | [−0.353, −0.275] | [−0.350, −0.281] | −0.102 [−0.122, −0.082] |

- **The resolution limit is about ±1.5 points.** One test-fold error is about 0.9 points. A paired difference must exceed about 1.5 points (NB-corrected) to be distinguishable, so **"parity" is the strongest honest claim** for any tuned quantum kernel here.
- **Clinical operating point** (pooled; 95% CI): every tuned model has **sensitivity 0.93–0.95 at the default SVM threshold**, so it misses about 1 cancer in 20.
  - The inner-calibrated threshold restores sensitivity to 0.97–0.98, at specificity:
    - RBF-30: 0.937 [0.916, 0.957]
    - FQK-full\*(8): 0.934 [0.914, 0.954]
    - PQK\*(8): 0.942 [0.922, 0.959]
    - SEP(8): 0.950 [0.931, 0.967]
    - LR-30: 0.920 [0.894, 0.945]
    - QSVC-plain(8): **0.717 [0.679, 0.754]**
  - QSVC-plain(12) at its default threshold has **sensitivity 0.083**: it calls almost every tumour benign.
- **Support vectors:** tuned kernels use about 46–80 (relevant to IonQ fidelity-kernel inference, Q4); the plain QSVC uses 169–455.

### Inferences
- **The prompt's "plain version" is beaten by tuning alone.** The plain QSVC → bandwidth-tuned FQK jump (+5 to +31 points) is far larger than any quantum-vs-classical gap (≤ 0.7 points, not significant). A team that reports only "QSVC 0.92 vs SVM 0.97" has measured a hyperparameter, not a quantum effect.
- **Entanglement is not doing the work.** The separable product kernel (no ZZ gates) is the best "quantum" kernel at n = 8 and 12 (0.972), and its g vs RBF is about 1.0–1.3 (Q3). This reproduces the Bowles et al. finding on a medical dataset.
- **Kernel training is bandwidth tuning in disguise.**
  - QKA-scale and ARD-RBF both triple training alignment and gain nothing on test.
  - Tutorial-style QKA-RY halves SVCLoss and gains nothing.
  - The faithful tutorial-08 QKA *diverged* on WDBC (Q1).
  - This matches Kakavand et al.'s observation that QKT behaves like bandwidth tuning.
- **Grid design matters more than qubit count.** FQK-full at n = 12 goes from 0.929 (grid floor 0.02) to 0.970 (floor 0.0025). Any team whose grid stops at "reasonable" angles will report a spurious "more qubits hurt" curve.

### Gaps
- CV still selected the smallest extended bandwidth (0.0025) in 18 of 25 folds at n = 8/12. Going lower drives the kernel toward its small-angle classical limit (Q3), so I expect at most a parity-level change, but I did not test c < 0.0025.
- QKA used 50 SPSA iterations on a 250-patient subsample (compute limits). A longer optimisation might raise alignment further; given ARD-RBF's identical pattern, I don't expect test gains.
- Pooled out-of-fold AUC mixes decision-function scales across folds (a slight bias, applied equally to all models).

---

## Q3. The prompt's question: does quantum similarity capture structure a classical kernel misses?

### Takeaway
**[Computed]** **On WDBC, no, and it is measurable why not.**
- **At the bandwidths that generalise, the quantum kernels look classical:** the geometric difference to the closest classical kernel is g_min ≈ 1.0–4 against √N ≈ 24. Their label alignment equals RBF's: top-30 spectral task alignment 0.77–0.79 vs 0.78–0.82.
- **Where they are geometrically different** (g ≈ 5–7.5 at larger bandwidths, especially with the all-to-all ZZ map), they **align worse with the labels** (A30 0.29–0.57) and lose accuracy.
- **Concentration:** the fidelity kernel's off-diagonal variance falls ~3× per qubit (5×10⁻² at n = 2 → 2×10⁻⁹ at n = 16 at unit bandwidth). Qiskit's default ZZ data map makes it worse, because its effective bandwidth grows with each qubit's entangling degree.
- **The tool works:** a **positive control** (labels engineered from the quantum kernel or from a quantum observable) is detected. The quantum kernel wins by **+25 to +46 points**, and a frozen task-alignment auditor predicted the winner on **6 of 7 fresh label sets** (7 of 7 counting the majority-class case correctly).

So the answer is a calibrated "no" on this dataset, from an instrument shown to say "yes" when the answer is yes.

### Cited Findings
**Tools from the literature**
- **Geometric difference and model complexity.** g(K^C‖K^Q) = √‖√K^Q (K^C+λI)⁻¹ √K^Q‖∞ with Tr K = N. If g is small relative to √N, a classical model with that kernel can match the quantum model on *any* labels; an advantage also needs s_C ≫ s_Q for the actual labels — [Huang et al. 2021](https://arxiv.org/abs/2011.01938).
- **Exponential concentration.** Expressive embeddings, global measurements (fidelity kernels), entanglement and noise make kernel values concentrate exponentially in n. With polynomially many shots, the trained model becomes input-independent — [Thanasilp et al., Nat. Commun. 15 (2024)](https://arxiv.org/abs/2208.11060v2).
- **Bandwidth.** Scaling inputs by c < 1 restores generalisation at large n — [Shaydulin & Wild 2022](https://arxiv.org/abs/2111.05451); [Canatar et al. 2023](https://arxiv.org/abs/2206.06686). Quantum kernels need a tunable inductive bias — [Kübler et al., NeurIPS 2021](https://arxiv.org/abs/2106.03747).
- **Task-model alignment.** Kernel generalisation is governed by how much of the target lies in the kernel's top eigenmodes ("spectral bias") — [Canatar, Bordelon, Pehlevan, Nat. Commun. 12, 2914 (2021)](https://arxiv.org/abs/2006.13198).
- **Engineered-label positive controls** (labels built from the quantum kernel, on which the projected kernel gains >20%) — [Huang et al. 2021](https://arxiv.org/abs/2011.01938). The QuEra/Harvard QRC advantage likewise appeared only on synthetic geometric-difference datasets — [Kornjača et al., arXiv:2407.02553](https://arxiv.org/abs/2407.02553v1).

**[Computed] 1. Geometry and alignment on the real labels** (`exp2b_real_auditor.py`, `exp2_diagnostics.py`; label-free global PCA; λ = 0.01; g_min = min over {RBF γ grid, linear})

| n | Kernel | c (CV-selected range) | Off-diagonal mean | g_min | Top-30 task alignment A30 |
|---|---|---|---|---|---|
| 8 | best classical (RBF g = 0.3) | — | 0.61 | — | **0.795** |
| 8 | FQK-full | 0.0025–0.01 | 0.81–0.99 | 2.0–3.6 | 0.785–0.792 |
| 8 | FQK-full | 0.05 | 0.14 | 7.35 | 0.567 |
| 8 | SEP (no entanglers) | 0.0025–0.05 | 0.96–1.00 | **1.0–1.55** | 0.787–0.789 |
| 8 | PQK | 0.0025–0.01 | 0.66–0.68 | 3.3–3.5 | 0.76–0.78 |
| 12 | best classical (RBF g = 0.3) | — | 0.61 | — | **0.781** |
| 12 | FQK-full | 0.0025–0.005 | 0.83–0.95 | 2.9–4.0 | 0.75–0.76 |
| 12 | FQK-full | 0.05 | 0.04 | 7.45 | **0.288** |
| 12 | PQK | 0.005 | 0.68 | 3.9 | 0.766 |

- **Auditor verdict on the real labels:** "no clear edge" at n = 4, 8 and 12. A_C / A_Q = 0.819 / 0.788, 0.795 / 0.792 and 0.781 / 0.766.
- In the earlier IQP-style study (`qk_bc.py`, prior notes), g ≈ 2–4 at CV bandwidths and the PQK was at parity. Here the Qiskit default map is used, with a finer grid, and the conclusion is unchanged.

**[Computed] 2. Concentration and the Qiskit default-map pathology** (`exp2_diagnostics.py`; 200 patients)

| n | FQK-full c = 1: off-diag mean / var | FQK-linear c = 1: var | FQK-full c = 0.2: var | Plain MinMax [0,1] full: mean | Mean single-qubit Bloch length (full, c = 1) |
|---|---|---|---|---|---|
| 2 | 0.31 / 5.4e-2 | 5.4e-2 | 9.8e-2 | 0.59 | 0.84 |
| 4 | 0.070 / 4.3e-3 | 6.9e-3 | 2.0e-2 | 0.13 | 0.40 |
| 8 | 0.0042 / 1.7e-5 | 9.0e-5 | 2.1e-4 | 0.017 | 0.097 |
| 12 | 3.3e-4 / 1.1e-7 | 8.1e-7 | 8.5e-6 | 0.0041 | 0.025 |
| 16 | 5.3e-5 / **1.9e-9** | 6.8e-9 | 1.2e-6 | 0.0015 | **0.008** |

- **Why the default map is so sharp.** Qiskit's pair term P(2(π−x_i)(π−x_j)) expands to 2π² − 2π(x_i + x_j) + 2x_i x_j. Each feature therefore enters **every** ZZ term it belongs to with slope 2π, against slope 2 in its own single-qubit term.
  - With full entanglement, a qubit has n−1 partners, so the data-dependent phase per feature is about 2π(n−1)·c.
  - Its effective bandwidth is therefore ~π(n−1) times the nominal c.
  - This is why the optimal c shrinks with n, and why z-scored or [0,π] angles collapse to the majority class (Q1).
- **Bandwidth scan** (`exp2_diagnostics.py` (c); 5-fold accuracy with C tuned; non-nested, diagnostic only):

  | n | c = 0.02 | c = 0.05 | c = 0.1 | c ≥ 0.5 |
  |---|---|---|---|---|
  | 4 | 0.961 | 0.960 | 0.919 | ≤ 0.71 |
  | 8 | 0.963 | 0.902 | 0.828 | **0.627 (majority class)** |
  | 12 | 0.938 | 0.784 | 0.634 | 0.627 |
  | 16 | 0.886 | 0.657 | 0.627 | 0.627 |

- **The PQK also concentrates, via vanishing Bloch vectors** (single-qubit reduced states become maximally mixed as entanglement grows). With a fixed γ = 1/n its off-diagonal mean goes to 0.999 at n = 12. Median-normalised γ hides this numerically, but the signal it rescales is smaller than shot noise (Q4).

**[Computed] 3. Positive control** (`exp3_positive_control.py`; n = 8, same WDBC inputs, engineered labels; nested CV 1×5 outer / 3 inner; accuracy)

| Labels | LR | RBF (tuned) | HGB | FQK-full | FQK-linear | PQK | Quantum − best classical |
|---|---|---|---|---|---|---|---|
| REAL (negative control) | **0.974** | 0.967 | 0.965 | 0.965 | 0.967 | 0.963 | −0.007 |
| HUANG (c = 0.75): y = sign(√K_Q v − median) | 0.496 | 0.548 | 0.506 | **0.821** | 0.597 | 0.641 | **+0.273** |
| HUANG (c = 0.35) | 0.482 | 0.487 | 0.478 | **0.838** | 0.485 | 0.490 | **+0.351** |
| HUANG (c = 0.75) + 10% label noise | 0.525 | 0.513 | 0.496 | **0.663** | 0.578 | 0.580 | +0.137 |
| OBS-1: sign ⟨Z₀⟩ of the patient's encoded state | 0.480 | 0.482 | 0.497 | 0.475 | 0.471 | **0.750** | **+0.253** |
| OBS-3: sign ⟨Z₀Z₃Z₆⟩ (c = 0.75) | 0.446 | 0.485 | 0.494 | 0.503 | 0.476 | 0.490 | ≈ 0: **nobody learns it** |

- **What each label type shows:**
  - The fidelity kernel wins exactly on labels built from its own geometry.
  - The projected kernel wins on labels set by a **local** observable, which its 1-RDM features contain.
  - **Neither** learns a weight-3 (global) observable's sign, even though that function is linear in ρ(x) and so lies in the fidelity kernel's RKHS. The kernel is too concentrated at c = 0.75 for 455 training patients. This is concentration made concrete.
- **Out-of-sample validation of the auditor** (`exp3c_auditor_validation.py`). The rule was written into the file **before** running, and nested CV judged:
  - **Rule:** A_Q − A_C ≥ 0.10 and A_Q ≥ 0.20 ⇒ quantum-favourable; the mirror case ⇒ classical-favourable; both A < 0.20 ⇒ unlearnable; otherwise no clear edge.

  | Fresh labels | A_C | A_Q | Predicted | Nested-CV accuracies (best classical / best quantum) | Observed |
  |---|---|---|---|---|---|
  | HUANG vs linear-map kernel (c = 0.35) | 0.068 | 0.376 | quantum | 0.58 / **0.80** (FQK-linear) | quantum ✓ |
  | HUANG (c = 0.1) | 0.063 | 0.700 | quantum | 0.48 / **0.92** (FQK-full) | quantum ✓ |
  | OBS-1 on qubit 5 (c = 0.35) | 0.065 | 0.368 | quantum | 0.50 / **0.77** (PQK) | quantum ✓ |
  | OBS-2 ⟨Z₁Z₄⟩ (c = 0.1) | 0.294 | 0.304 | no clear edge | 0.85 / 0.83 | no edge ✓ |
  | REVERSE-HUANG (classical-engineered) | 0.757 | 0.751 | no clear edge | 0.96 / 0.95 | no edge ✓ |
  | SHUFFLED real labels | 0.047 | 0.076 | unlearnable | 0.627 / 0.622 (= majority rate) | "no edge" by my accuracy rule ✗, but this *is* chance for 37/63 classes |
  | REAL + 20% flips | 0.322 | 0.299 | no clear edge | 0.78 / 0.77 | no edge ✓ |

- **What did *not* work as a discriminator** (`exp3b_auditor.py`): Huang's fixed-λ model-complexity ratio s_C/s_Q (λ = 0.1, Tr K = N). It gave 1.2–1.5 for every engineered label set, including the unlearnable ones, and 0.76 for the real labels. Near-diagonal kernels sit at the identity-kernel value N/(1+λ) ≈ 517 regardless of labels. KTA alone was also weak (e.g. 0.042 vs 0.037 on OBS-1, where the PQK wins by 25 points).

**[Computed] 4. IonQ-native all-to-all map vs linear map, and transpiled cost** (`exp5_gatecounts.py`; `zz_feature_map` rebuilt as H, P(2x), RZZ(2(π−x_i)(π−x_j)), identical to Qiskit's up to global phase, overlap 1 − 1e-15; transpiled with optimisation level 3)

| n | Map | 2Q per U(x): IonQ ZZ | All-to-all CX | **Heavy-hex CZ** (IBM, d = 5) | Fidelity circuit U(x)U†(x′): IonQ ZZ | Heavy-hex CZ | 2Q depth, IonQ / heavy-hex (fidelity circuit) |
|---|---|---|---|---|---|---|---|
| 4 | linear | 6 | 12 | 12 | 11 | 22 | 9 / 18 |
| 4 | full | 12 | 24 | 33 | 23 | 64 | 17 / 64 |
| 8 | linear | 14 | 28 | 28 | 27 | 54 | 17 / 34 |
| 8 | full | 56 | 112 | **240** | 111 | **496** | 41 / 318 |
| 12 | linear | 22 | 44 | 44 | 43 | 86 | 25 / 50 |
| 12 | full | 132 | 264 | **583** | 263 | **1,142** | 65 / 452 |
| 16 | full | 240 | 480 | 1,136 | 479 | 2,369 | 89 / 837 |

- **Accuracy, full vs linear:**
  - n = 8: FQK-full\* 0.970 vs FQK-linear\* 0.968.
  - n = 12: 0.970 vs 0.969.
  - At the first grid's floor (c = 0.02), full was worse (0.956 / 0.929 vs 0.965 / 0.955), because its effective bandwidth is larger.
- **Noise, full vs linear** (Q4): at n = 8 the fidelity-circuit return-probability scale is a = 0.60 (full) vs 0.91 (linear).

### Inferences
- **The honest one-line answer to the prompt.** "At every qubit count we tested, quantum similarity on WDBC is either (a) geometrically a classical kernel in disguise (g ≈ 1–4 ≪ √N, with alignment equal to RBF) and performs like one, or (b) genuinely different (g ≈ 6–7.5) and worse, because the extra structure is not where the tumour labels are. A positive control proves our instrument would have seen the difference."
- **All-to-all ZZ is where IonQ shines on cost but not on accuracy.**
  - On cost, IonQ-native all-to-all needs **4.3–4.6× fewer** two-qubit gates than heavy-hex for the full map at n = 8–12 (56 vs 240; 132 vs 583), and **7–9× lower 2Q depth** for the fidelity circuit. Even the linear map is 2× cheaper (one ZZ vs two CNOTs per term).
  - On accuracy, full entanglement buys nothing on WDBC. The connectivity advantage is a **resource** result, not an accuracy result.
- **Use spectral task alignment, not fixed-λ s_K, as the auditor's label-specific statistic.** Keep g_CQ as the label-free "could classical match on any labels" statistic.

### Gaps
- g and A30 were computed on a label-free global PCA (diagnostic). In-fold versions would move the numbers slightly.
- The auditor rule was calibrated on 8 label sets and validated on 7. That is too few to quote a false-positive rate. More random positive and negative controls (seeds × constructions) would be needed.
- The heavy-hex counts use a generic distance-5 heavy-hex coupling map with the CZ basis, not a calibrated IBM backend. IonQ native counts treat RZ as virtual and use RZZ ≡ ZZ(θ). I did not use the IonQ transpiler itself.

---

## Q4. Noise and IonQ execution

### Takeaway
**[Computed]** **Shot noise, not Forte-like gate noise, is the binding constraint.**
- **Gate noise is benign.** Under IonQ's (legacy) Forte-1 depolarising model:
  - fidelity-kernel entries are an almost exact affine rescaling, K_noisy ≈ a·K + b (a = 0.91 linear / 0.60 full map at n = 8; residual sd 3×10⁻⁴), which an SVM absorbs through C;
  - Bloch vectors for the PQK shrink by only 1.5–4% (n = 4, and n = 8 linear) to 7–14% (n = 8 full map).
- **Shot noise is not.** At 1,000 shots, accuracy drops by **2–4 points (fidelity kernel)** and **6–13 points (PQK)**.
  - The small bandwidths that win noiselessly carry tiny signals (Bloch-component sd 0.03–0.06, about 1/√1000).
  - **Training on exact features and testing on shot-noisy IonQ features is catastrophic: 0.59–0.72.**
  - Bandwidth must be chosen with shots in the loop.
- **One job fits PQK cleanly.** At n = 8 with the linear map, the PQK needs about **75 native gates per circuit**, so **all 569 patients × 3 bases (1,707 circuits, ~129k gates) fit in one IonQ job**. A fidelity-kernel block fits only about 20 test patients × 60 support vectors.
- **Simulator time is unknown.** IonQ's per-shot simulation time is not published. My Aer per-shot proxy puts a 114-patient × 1,000-shot PQK fold at about 5 minutes.

### Cited Findings
- **IonQ noisy simulation:**
  - Forte-class and ideal simulators: up to 29 qubits.
  - The model is a depolarising channel after each one- and two-qubit gate. Legacy Forte 1 rates: **r₁q = 0.0002667, r₂q = 0.0049493**. The updated (post-mid-September 2025) Forte 1 / Forte Enterprise 1 models are "more complex", and IonQ says their documentation is "in preparation".
  - **Each shot is simulated separately.** Noisy simulation does **not** include debiasing.
  - Selection: `backend.run(qc, shots=…, noise_model="forte-1")`, with an optional seed (1 to 2³¹).
  - Source: [IonQ docs: Simulation with noise models](https://docs.ionq.com/guides/simulation-with-noise-models).
- **Limits and errors:**
  - IonQ multi-circuit jobs: ≤ 5,000 circuits, ≤ 150,000 gates, request ≤ 10 MB — [IonQ API v0.4 create-job](https://docs.ionq.com/api-reference/v0.4/jobs/create-job), via the prior notes.
  - Qollab's one-job rule: pass every circuit to a single `backend.run` — [Qollab runtime docs](https://qollab.xyz/learn/docs/runtime-environment).
  - Possible errors near capacity: `SimulationTimeout`, `TooLongPredictedExecutionTime` — [Qollab compute backends](https://qollab.xyz/learn/docs/compute-backends).
  - I found no published per-circuit or per-shot simulator time limit. IonQ's error codes refer to a "runaway process timeout" and a predicted-execution-time preflight — [IonQ error codes](https://docs.ionq.com/api-reference/v0.3/error-codes.md).
- **Theory:**
  - Measurement-shot cost dominates QSVM training: O(M^4.67/ε²) for the dual problem — [Gentinetta et al., Quantum 2024](https://arxiv.org/abs/2203.00031).
  - With polynomially many shots, concentrated kernels make the learned model input-independent — [Thanasilp et al. 2024](https://arxiv.org/abs/2208.11060v2).
  - Diagonal-based mitigation and PSD projection for noisy kernels — [Hubregtsen et al. 2022](https://arxiv.org/abs/2105.02276).

**[Computed] Noise model used:** Aer density-matrix simulation of IonQ-native circuits (H = RZ·SX·RZ, P = RZ, ZZ term = RZZ). Depolarising p₁ = 2.67e-4 on SX/X, p₂ = 4.95e-3 on RZZ, RZ virtual. No SPAM or readout error, which is an assumption. Shots are binomial. The noiseless Aer construction matches my NumPy Bloch vectors to 1.5e-14.

**[Computed] A. Kernel entries** (`exp4_noise.py` part B: a 30-patient block, all 465 fidelity circuits simulated exactly with noise, n = 8, c = 0.35)

| Map | ZZ per fidelity circuit | Fitted a (slope) | b | Residual sd | Exact off-diag sd | 0.995^N2Q rule of thumb |
|---|---|---|---|---|---|---|
| linear | 28 | **0.914** | 0.0004 | 3e-4 | 0.0115 | 0.870 |
| full | 112 | **0.604** | 0.0017 | 2e-4 | 0.0076 | 0.574 |

- **PQK:** noisy Bloch vectors (exact expectations) are shrunk by a factor of 0.98–0.99 (n = 4 and n = 8 linear) and 0.86–0.97 (full map). Mean absolute error is 0.003–0.008 per component.

**[Computed] B. Accuracy under noise and shots** (`exp4_noise.py`, `exp4b_noise_lowbw.py`; label-free global PCA; nested CV 1×5 with hyperparameters chosen inside on the same noisy data unless stated)

| Kernel (n = 8) | Exact | Forte noise, ∞ shots | + 10,000 shots | + 1,000 shots | + 100 shots | Train exact/noise-sim, test 1,000-shot features |
|---|---|---|---|---|---|---|
| PQK, linear map (c ∈ 0.01–0.1) | 0.961 | 0.961 | 0.914 | 0.898 | 0.798 | **0.724** |
| PQK, full map (c ∈ 0.01–0.1) | 0.965 | 0.961 | 0.914 | 0.835 | 0.759 | **0.594** |
| PQK, linear (c ≥ 0.1 grid) | 0.895 | 0.895 | — | 0.863 | 0.849 | 0.868–0.870 |
| FQK, linear map (c ∈ 0.005–0.1) | 0.967 | (affine ⇒ same) | 0.931 | 0.931 | 0.891 (mitigated 0.919) | — |
| FQK, full map | 0.970 | (same) | 0.949 (mitigated 0.961) | 0.946 | 0.868 (mitigated 0.889) | — |
| PQK n = 4 linear (c ≥ 0.05) | 0.942 | 0.942 | — | 0.910 (3,000: 0.909) | 0.852 | 0.895 |

- **Shot cost vs signal.** Bloch-component signal sd across patients (exact) at n = 8 is:
  - linear map: 0.030 / 0.059 / 0.126 / 0.201 at c = 0.01 / 0.02 / 0.05 / 0.1;
  - full map: 0.014 / 0.031 / 0.067 / 0.074, because entanglement shrinks the local Bloch vectors.

  Shot noise per component is about 1/√S: 0.10 at 100 shots, 0.032 at 1,000, 0.01 at 10,000. The full map is therefore doubly penalised on IonQ: it needs 4× the ZZ gates *and* it gives half the local signal.

**[Computed] C. Single-IonQ-job designs** (`exp6_job_sizing.py`; IonQ-like basis {RZ virtual, SX, X, RZZ}; limits 5,000 circuits / 150,000 gates)

| Design | Circuits | Native gates per circuit | Total gates | Fits? | Aer per-shot-trajectory time proxy (native, 1 thread) |
|---|---|---|---|---|---|
| PQK demo: 20 test patients × {X, Y, Z}, n = 8 linear, 1,000 shots | 60 | ~75 | ~4.5k | ✓ | ~49 s |
| PQK one test fold: 114 × 3, n = 8 linear, 1,000 shots | 342 | ~75 | ~26k | ✓ | ~281 s (300 shots: ~84 s) |
| PQK **all 569 patients** × 3, n = 8 linear, 300 shots | 1,707 | ~75 | ~129k | ✓ (max 663 patients) | ~420 s |
| PQK one fold, n = 8 **full** map | 342 | ~117 | ~40k | ✓ (max 426 patients) | 1.6 ms/shot ⇒ ~9 min at 1,000 shots |
| PQK one fold, n = 12 linear, 1,000 shots | 342 | ~114 | ~39k | ✓ (max 438) | ~45 min ⚠ |
| FQK block: 16 test × 60 SV, n = 8 linear, 300 shots | 960 | ~125 | ~120k | ✓ (max 1,200 circuits ≈ 20 test patients) | ~236 s |
| FQK full test fold: 114 × 60 SV | 6,840 | ~125 | ~855k | ✗ | — |

- **Measured Aer noisy per-shot cost** (each shot simulated separately, native, 1 thread, unloaded): 0.35 ms (n = 4), **0.82 ms** (n = 8 linear), 1.6 ms (n = 8 full), **7.9 ms** (n = 12 linear).
- **One-job pipeline check** (`judge_run_prototype.py` block 5): 20 test patients × 3 bases, 1,000 shots on a local simulator, then parse counts → Bloch vectors → PQK rows → SVC.
  - Bloch mean absolute error 0.024. Predictions agreed 100% with the exact-feature predictions.
  - It used `backend.run(...).result().get_counts()`, not `BackendSamplerV2` (which returns zeros on IonQ, per the brief).

### Inferences
- **Recommended IonQ step:**
  - **PQK on a held-out batch**, n = 8, **linear** map (14 ZZ per circuit).
  - c chosen **with simulated shots in the inner loop** (c ≈ 0.05–0.1 at 1,000 shots), with the classifier trained on **shot-noise-augmented** training features.
  - 20–114 test patients × 3 bases × 300–1,000 shots in **one** `backend.run([...], shots=S, noise_model="forte-1")`.
  - Report: (i) Bloch error vs exact; (ii) agreement with exact-feature predictions; (iii) accuracy with a CI. Expect about 0.87–0.90 accuracy at 1,000 shots vs about 0.96 exact.
- **The fidelity kernel's one-job budget is 20 patients.** Because of the N_test × N_SV structure, one job covers at most about 20 test patients × 60 support vectors at n = 8 linear. That is only enough to show **entrywise** agreement (a, b fit), not a fold accuracy.
- **Don't mitigate what an SVM ignores.** Global-depolarising mitigation adds only 1.5–3 points, and only at 100 shots. The affine part of the noise is absorbed by C; spend the shot budget instead.
- **Time risk.** IonQ's cloud throughput is unknown. Keep the live IonQ call to ≤ 60–120 circuits × ≤ 1,000 shots at n = 8, show a cached `forte-1` result (with date, seed and shots) as the fallback, and never put n = 12 full-map circuits in the judge path.

### Gaps
- I did not run the actual IonQ `forte-1` cloud simulator: no API access from this environment, and the post-September-2025 model is undocumented. My noise model is the documented legacy depolarising one, without SPAM.
- IonQ cloud simulator throughput is unknown. The Aer timings are a proxy for "one simulation per shot", not a measurement of IonQ's service.
- The noise accuracy studies used a label-free global PCA and 1×5 nested CV (cheaper than the Q2 protocol), so compare within the table, not against Q2.

---

## Q5. Clinical and impact framing

### Takeaway
WDBC is a 1990s fine-needle-aspirate (FNA) image-feature dataset. A classifier on it plays the role of a **decision aid that reads the cytology image**, not a screening test. The clinically relevant metric is **sensitivity at a fixed, high specificity** (or specificity at ≥98% sensitivity), because a false negative delays a cancer diagnosis while a false positive mostly triggers a core biopsy.

Classical models already exceed published FNA cytology accuracy on this curated data. So the honest "impact" story for a quantum kernel is not "better diagnosis today". It is a **reusable, pre-registered test of whether a quantum similarity measure adds anything for a given clinical tabular task**, applied here to WDBC and positive-controlled.

### Cited Findings
- **Data provenance:**
  - 569 instances × 30 real features, no missing values. The features are "computed from a digitized image of a fine needle aspirate (FNA) of a breast mass" and describe cell nuclei. Creators: Wolberg, Mangasarian, Street; donated 1995 — [UCI WDBC](https://archive.ics.uci.edu/dataset/17/breast+cancer+wisconsin+diagnostic).
  - There are 10 nuclear features (radius, texture, perimeter, area, smoothness, compactness, concavity, concave points, symmetry, fractal dimension), each given as a mean, a standard error and a "worst" value (mean of the 3 largest). **357 benign / 212 malignant** — [WDBC.doc](https://ftp1.cs.wisc.edu/math-prog/cpo-dataset/machine-learn/cancer/WDBC/WDBC.doc).
- **Xcyt:**
  - The operator outlines nuclei interactively. It scored 97.9% on 192 FNAs and was positioned as an adjunct, not a stand-alone diagnosis — [Street, Xcyt paper](https://www.biz.uiowa.edu/faculty/nstreet/research/bj97.pdf) [Snippet].
  - The original system "correctly diagnosed 176 consecutive new patients" (as of Nov 1995) — [WDBC.doc](https://ftp1.cs.wisc.edu/math-prog/cpo-dataset/machine-learn/cancer/WDBC/WDBC.doc).
- **Workflow:**
  - The **triple test** combines clinical exam, imaging (mammography/ultrasound) and needle sampling (FNA or core needle biopsy, CNB) — [Ann Surg Oncol (2012)](https://link.springer.com/article/10.1245/s10434-012-2710-y) [Snippet].
  - UK 2010 best-practice guidance prefers CNB over FNA for most solid or suspicious lesions, because histology gives type, grade and receptor status — cited in [PMC7188022](https://pmc.ncbi.nlm.nih.gov/articles/PMC7188022) [Snippet]. I did not verify that this guidance is still current.
- **FNA performance in practice:**
  - IAC Yokohama meta-analysis (18 studies): counting "suspicious + malignant" as positive gives **sensitivity 91%** and a **false-positive rate of 2.33%**. Counting "malignant" only gives 76.6% and 0.75%. The risk of malignancy is 1% for "benign" and 86% for "suspicious" — [PMC9891409](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9891409/).
  - An older 46-study meta-analysis gives sensitivity 0.927 and specificity 0.948 — [PMC3283452](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3283452/) [Snippet].
  - Pooled CNB vs FNA (Wang 2017, 12 studies): sensitivity 87% vs 74%, specificity 98% vs 96% — via [Cancer Australia position statement](https://www.canceraustralia.gov.au/resources/position-statements/position-statement-use-fine-needle-aspiration-and-core-biopsy-breast-breastscreen-australia-program/interpretation-evidence) [Snippet; the page timed out].
- **Cost of false negatives (delay):**
  - Each 30-day increase in time to surgery was associated with about 9–10% higher all-cause mortality (NCDB HR 1.10, 95% CI 1.07–1.13). For stage I disease, a delay over 120 days had a breast-cancer-specific HR of 1.84 (Bleicher et al., *JAMA Oncol* 2016) — [Fox Chase summary](https://www.foxchase.org/news/2015-12-10-delaying-breast-cancer-surgery-lowers-survival-rate) [Snippet].
  - A meta-analysis of 34 studies found a 6–8% higher risk of death per 4-week delay. For breast surgery the increase was +17% at 8 weeks and +26% at 12 weeks (observational) — [Hanna et al., *BMJ* 2020](https://www.bmj.com/content/371/bmj.m4087.abstract).
- **Cost of false positives:**
  - $852 per false-positive mammogram; about $2.8B a year in the US — [Ong & Mandl, *Health Affairs* 2015](https://labs.childrenshospital.org/mandl/publications/national-expenditure-false-positive-mammograms-and-breast-cancer-overdiagnoses). These are screening-stage figures; WDBC models act after the aspirate.

### Inferences
- **Operating point:** report **sensitivity at 95% specificity** (a ROC summary) and a **deployable threshold**. The threshold is calibrated on inner out-of-fold scores to target ≥98% sensitivity and then applied untouched to the test fold, giving the realised sensitivity and specificity.
- **Cost framing:**
  - A false negative costs months of delay (about +9–26% mortality hazard per 1–3 months, observational).
  - A false positive costs a CNB, which is routine anyway for suspicious lesions.
  - So a 98–99% sensitivity target with the specificity that results is the defensible setting. This is also where small model differences show up most clearly.
- **"What this would need to matter":** a quantum kernel would matter clinically only if all of the following held:
  1. **Diagnostic gain:** on prospectively collected, multi-site cytology or imaging features (not 1995 curated morphometry), it gives a **statistically significant gain in sensitivity at fixed specificity** over the best tuned classical model. The CI on the difference must exclude 0 under nested CV and external validation.
  2. **Why it helps:** a diagnostic (g_CQ, s_C/s_Q) shows the gain comes from structure the classical kernel cannot represent cheaply, not from tuning luck.
  3. **Deployment:** it runs with acceptable shot cost on hardware, or classical simulation of it is cheaper than the alternatives.

  On WDBC, condition 1 cannot hold: the classical ceiling (about 97–98% accuracy, AUC ≈ 0.99) leaves no headroom that 114-patient test folds could resolve. So the realistic deliverable is the **auditing method** together with its WDBC verdict.

### Gaps
- I have no current (2025–26) guideline figure for the fraction of breast masses still triaged by FNA versus CNB in the US.
- I have no cost-per-false-negative figure specific to cytology (as opposed to screening).

---

## Q6. Beyond-tutorial extensions that stay inside Prompt A and fit Quantum Impact

### Takeaway
Five extensions clear the tutorial bar with **measured** differences from this session's experiments.
- **The strongest is E1, a positive-controlled "Will a quantum kernel help?" auditor**, because it is the only one that *answers the prompt's question* with an instrument shown to detect advantage when it exists.
- **E2 (sensitivity-first operating point)** and **E4 (one-job IonQ PQK inference with noise-aware bandwidth)** are the best add-on modules.
- **E3 (QKA vs bandwidth)** and **E5 (all-to-all connectivity frontier)** are cheap appendix panels.

All live computation fits in about 2 s native (about 7–25 s in Pyodide, estimated) if nested CV is precomputed and shipped as JSON.

### Cited Findings
Every number below is **[Computed]** in this session; scripts are named in Q1–Q4.

- **Judge-run timing basis:** `judge_run_prototype.py` runs the core live demo single-threaded on native CPython (unloaded machine) in **2.15 s total**:
  - (1) 5-fold CV of LR, RBF, FQK and PQK at n = 8 on 569 patients, with fold-internal PCA and inner-CV threshold calibration: **0.6 s**;
  - (2) auditor on the real labels: 0.2 s;
  - (3) positive-control labels + CV: 0.6 s;
  - (4) concentration curve n = 2–10: <0.1 s;
  - (5) 60-circuit, 1,000-shot one-job PQK batch on a local simulator, with parsing: 0.7 s;
  - plus 0.6 s for `import qiskit`.
- **Pyodide slowdown:** the browser runs the same libraries in WebAssembly on one thread and is "several times slower" than native — [Qollab docs](https://qollab.xyz/learn/docs/ideal-vs-noise-model-simulators). The prior notes measured NumPy kernels in Pyodide at about 3–10× native (`Quantum Unlocked theme deep dive/build_feasibility_and_stack.md`).
- **Not live-able:** full nested CV (exp1) took about 1 hour on 18 processes, and the qiskit-ML `FidelityStatevectorKernel` needs 14–57 s natively per 569² kernel. Both must be precomputed or replaced by the NumPy simulator.

### Inferences

**E1. "Tumor or not? A positive-controlled audit of quantum similarity"** (the auditor)
- **Tutorial-bar sentence:** "QSVC with ZZFeatureMap on PCA-4 WDBC reaches 92% accuracy."
- **Beyond-tutorial claim:** "Under nested CV at 4/8/12 qubits, the best quantum kernel is 0.4 points [NB-CI −1.8, +1.0] behind a tuned RBF-SVM. A frozen auditor (g_CQ, top-30 task alignment, concentration) explains why, and the same auditor flags quantum wins of +25 to +46 points on positive-control labels (6 of 7 out-of-sample predictions correct)."
- **Measurable difference:**
  - Δ accuracy and Δ AUC vs RBF-30/LR-30 with CIs (Q2).
  - g_min 1–4 ≪ √N = 24.
  - A30: classical 0.78–0.82 vs quantum 0.77–0.79 on real labels; on positive-control labels, 0.06–0.07 vs 0.37–0.70.
  - Concentration: variance 5e-2 → 2e-9 from n = 2 to 16.
- **Qubits / gates (IonQ native ZZ per U(x)):** n = 4 / 8 / 12; linear map 6 / 14 / 22, full map 12 / 56 / 132 (heavy-hex 12–33 / 28–240 / 44–583 CZ).
- **Judge-run time:** about 2 s native for the live core (prototype). Estimated 7–25 s in Pyodide plus package load. Nested-CV tables, the bandwidth curve and the positive-control nested CV are precomputed JSON (< 200 KB).
- **Build hours:** 10–14 (core numerics already exist in `qk_core.py`; the remaining work is UI, charts and write-up).
- **Hour-20 fallback:** precomputed tables + live 5-fold CV at n = 8 + live auditor on real vs Huang labels. Drop the interactive n-slider and the OBS controls.

**E2. "Don't miss a cancer": sensitivity-first QSVC with inner-CV threshold calibration**
- **Tutorial-bar sentence:** "QSVC gets 92% accuracy."
- **Beyond-tutorial claim:**
  - At the default threshold, *every* tuned model misses about 5–7% of malignancies (sensitivity 0.93–0.95); the plain QSVC at n = 12 misses 92%.
  - Calibrating the threshold on inner out-of-fold scores gives realised sensitivity 0.97–0.98 at specificity:
    - FQK-full\*(8): 0.934 [0.914, 0.954]
    - PQK\*(8): 0.942 [0.922, 0.959]
    - RBF-30: 0.937 [0.916, 0.957]
    - plain QSVC(8): 0.717
- **Measurable difference:**
  - Missed cancers per 212: default ≈ 10–15 vs calibrated ≈ 4–6.
  - Specificity at matched sensitivity, with CIs; sens@95% spec.
  - Parity between quantum and classical at the clinical operating point.
- **Qubits / gates:** as E1 (no extra circuits).
- **Judge-run time:** +3 SVC fits per fold, under 0.3 s native.
- **Build hours:** 3–4.
- **Hour-20 fallback:** report sens@95% spec from ROC only (1 h).

**E3. "Is quantum kernel alignment just bandwidth tuning?"**
- **Tutorial-bar sentence:** "We trained the kernel with QuantumKernelTrainer and the loss went down."
- **Beyond-tutorial claim:**
  - Faithful tutorial-08 QKA *diverges* on WDBC (SVCLoss 78 → 96; accuracy 0.921 → 0.877).
  - Per-feature-bandwidth QKA raises training KTA from 0.08–0.21 to 0.41–0.59, but its test accuracy is −0.6 [NB −2.8, +1.6] points vs RBF-PCA at n = 8.
  - The classical ARD-RBF trained the same way shows the same pattern (KTA 0.27 → 0.63, Δ acc +0.35 [−0.8, +1.5]).
  - So on WDBC, kernel training = bandwidth.
- **Measurable difference:** Δ KTA vs Δ test accuracy (quantum and classical), SPSA traces, n_SV.
- **Qubits / gates:** n = 8; the trainable layer adds n single-qubit RY (no 2Q cost).
- **Judge-run time:** a live 30-iteration KTA-SPSA on 250 patients at n = 8 is about 60 kernel evaluations × ~0.05 s ≈ 3 s native, so about 10–30 s in Pyodide behind a "train" button. Otherwise ship the traces.
- **Build hours:** 5–7.
- **Hour-20 fallback:** precomputed traces and table only.

**E4. "One job, one batch of patients": IonQ PQK inference with noise-aware bandwidth**
- **Tutorial-bar sentence:** "We ran our circuit on IonQ's simulator."
- **Beyond-tutorial claim:**
  - All PQK features for a test batch come from **one** `backend.run` (60–342 circuits; all 569 patients fit at about 129k gates).
  - Bandwidth and training are chosen with shots in the loop. The run shows that the naive train-exact/test-on-hardware pipeline collapses (0.72 at 1,000 shots) while noise-aware selection holds about 0.90 (exact 0.96).
  - Fidelity-kernel noise is quantified as an affine rescale (a = 0.91 linear vs 0.60 full).
- **Measurable difference:** Bloch error vs exact (0.024 at 1,000 shots on an ideal simulator), agreement with exact predictions, and accuracy vs shots {100, 300, 1,000, 10,000}.
- **Qubits / gates:** 8 qubits, linear map. 14 ZZ + about 60 one-qubit gates gives about 75 native gates per circuit; the 20-patient demo is about 4.5k gates.
- **Judge-run time:** the local built-in simulator does 60 circuits × 1,000 shots in 0.2 s native. The IonQ cloud is unknown; the Aer proxy is about 49 s for the 20-patient demo with Forte noise, so cache it.
- **Build hours:** 6–8, including Qollab IonQ plumbing, count parsing and cached fallback.
- **Hour-20 fallback:** local-simulator job plus a cached `forte-1` JSON, with 20 patients × 300 shots.

**E5. "What does all-to-all buy?": connectivity and the default-map bandwidth pathology**
- **Tutorial-bar sentence:** "We transpiled our circuit for the backend."
- **Beyond-tutorial claim:**
  - IonQ all-to-all ZZ needs 56 vs 240 two-qubit gates (n = 8 full map) and 132 vs 583 (n = 12) compared with heavy-hex, with 7–9× lower 2Q depth.
  - But the full map buys **zero** accuracy on WDBC (0.970 vs 0.968 linear).
  - It also halves the local Bloch signal and lowers fidelity-circuit visibility (a = 0.60 vs 0.91).
  - Qiskit's default (π−x)(π−x) map multiplies the effective bandwidth by about π(n−1).
- **Measurable difference:** 2Q count and depth; accuracy; noise visibility a; Bloch-signal sd.
- **Qubits / gates:** n = 4–16 (counts table, Q3).
- **Judge-run time:** precomputed table plus one live transpile at n = 8 (about 1–5 s native, estimated).
- **Build hours:** 3–4.
- **Hour-20 fallback:** static table and one chart.

### Gaps
- Pyodide timings are extrapolated (3–10× native), not measured on Qollab with this code.
- IonQ cloud simulator throughput is unknown; the timing estimates for E4 rest on an Aer proxy.
- E1's auditor rule has been validated on only 7 fresh label sets.

---

## Q7. Recommendation: one extension with a concrete build outline

### Takeaway
**Build E1 as the spine, with E2 and E4 as modules: "Does a Quantum Circuit See the Tumor? A positive-controlled audit of quantum similarity for breast-cancer cytology."**
- It is the only design that **answers the prompt's literal question** ("does quantum similarity capture structure a classical kernel misses?") with a pre-registered, falsifiable instrument.
- It **proves the instrument can say "yes"**, through the positive control and out-of-sample label sets.
- It reports the **clinically relevant** metric (sensitivity at fixed specificity, with a deployable threshold).
- Its IonQ step is designed around the one-job rule.
- Almost every GT team will submit a QSVC accuracy. This submission shows *why* that number is what it is, which scores on Novelty and Technical Execution, while E2 carries the Impact narrative.

### Cited Findings
- **Judging criteria:** Novelty & Creativity, Technical Execution, Impact Potential, Documentation Quality. Judges run every project on a free local simulator, and IonQ results "neither add nor subtract points" — [QCA prompt slides](C:/VS Code Projects/QC Hackathon/research_notes/QCA prompts Quantum Impact plan/qca_prompts_slides.txt).
- **Submission requirements:** MIT licence; a Qollab project page; a 2–3 min public demo video; built during the window, with prior code disclosed — same source.
- **Qollab runtime:** one `backend.run` per run; data files opened by string-literal path; no web workers — [Qollab runtime docs](https://qollab.xyz/learn/docs/runtime-environment); prior notes.

### Inferences
**Pre-registration** (write it into the README *before* the final runs):
- "A quantum kernel is declared **advantageous on WDBC** only if its nested-CV accuracy *and* sensitivity at 95% specificity exceed the best tuned classical model's, with the Nadeau–Bengio 95% CI on the paired difference excluding 0, *and* the auditor (A_Q − A_C ≥ 0.10) agrees."
- "Positive control passes if the same pipeline reports a quantum win of ≥ 10 points on Huang-engineered labels."

**Architecture**
- Pure NumPy and scikit-learn, with Qiskit used only to build, verify and send circuits.
- `qk_core.py` (already written and verified against Qiskit to 1e-15) does states, kernels, Bloch vectors and diagnostics in milliseconds. Do **not** use `FidelityStatevectorKernel` live (14–57 s natively per kernel). Keep one cell that shows `zz_feature_map` + `Statevector` reproducing `qk_core` on three patients, so judges see it is the same Qiskit map.
- **Precomputed JSON:**
  - Q2 tables with CIs;
  - the bandwidth curves;
  - positive-control and validation tables;
  - concentration vs n (n ≤ 16);
  - gate-count table;
  - noise and shot tables;
  - a cached `forte-1` run (written when the team runs it).

**Page layout** (top to bottom)
1. **Problem card:** FNA cytology; cost of a false negative; 357 benign / 212 malignant.
2. **Pre-registration card.**
3. **Live CV panel** (n = 8): LR, RBF, FQK, PQK, SEP, with accuracy, AUC, sens@95% spec and a threshold slider showing missed cancers per 212.
4. **"Does quantum similarity see anything RBF can't?" auditor panel:** g_min vs √N; A30 classical vs quantum; verdict badge.
5. **Positive-control toggle:** real labels ↔ Huang/OBS labels; the verdict flips and the CV gap opens to +27 to +46 points.
6. **Concentration and bandwidth chart:** why the default ZZ map collapses to "all benign".
7. **IonQ panel:** one job, 20 patients × 3 bases; Bloch error, agreement, cached `forte-1`.
8. **Honesty box:** Bowles 2024, Kakavand 2026, Thanasilp 2024; what this would need to matter (Q5).

**Hour plan** (from Sat ~13:15 ET to the Sun 19:00 deadline, ~30 h)

| Hours | Work | Milestone |
|---|---|---|
| H0–2 | Qollab project scaffolding. Port `qk_core.py`. Run the Qiskit-equivalence cell in Pyodide. Export JSON from `results/` (exp1 summary, exp2/2b, exp3/3b/3c, exp4/4b, exp5, exp6). | Code runs in the browser |
| H2–6 | Live CV panel (from `judge_run_prototype.py` blocks 1–2). Threshold calibration (E2). Auditor panel with real labels. | **Core demo works** |
| H6–9 | Positive-control toggle (block 3). Concentration and bandwidth charts (Chart.js or matplotlib). | Answer to the prompt is visible |
| H9–13 | IonQ module (block 5) → `backend.run(circs, shots=1000)` with try/catch and cached-result fallback. Run once on `forte-1` and cache it. | One-job IonQ step |
| H13–19 | Sleep / buffer | — |
| **H20 checkpoint** | Core demo, auditor, positive control and E2 must be done. If the IonQ step isn't stable, ship the local-sim job plus the cached JSON. | — |
| H20–24 | Project page write-up (problem, method, how to run, replicate, licence, disclosure of these research scripts). README with the pre-registration. GitHub repo with `scripts/prompt_a/` and `results/`. | Docs done |
| H24–27 | 2–3 min demo video: hook (plain QSVC 0.63 → "all benign"), answer (parity + why), positive control flip, IonQ job, clinical operating point. | Video |
| H27–29 | Judge-path test on the built-in simulator; time it; trim. | Submit |

**Optional, if ahead at H20:** the E3 panel (QKA traces) and the E5 table (all-to-all vs heavy-hex).

**Risks and mitigations**
- **"Negative result" perception.** Lead with the positive control and the clinical operating point. The headline is "an instrument that can tell", not "quantum lost".
- **Pyodide speed.** Live work ≤ n = 8, N = 569, ≤ 10 kernels; nothing O(N²·circuits).
- **IonQ timeout.** ≤ 60 circuits × 1,000 shots live; cached fallback.
- **File limits.** Ship JSON, not 569² kernels: a float64 569² kernel is 2.6 MB, over the 2 MB per-file guidance in the prior notes.

**Assets already in `research_notes/QCA prompts Quantum Impact plan/scripts/prompt_a/`**

| File | Purpose |
|---|---|
| `qk_core.py` | Vectorised `zz_feature_map` simulator; fidelity, projected, separable and RBF kernels; g, s_K, KTA, spectra; metrics and threshold calibration; SPSA |
| `verify_qiskit.py` | Equivalence check against Qiskit and qiskit-ML 0.9.1, plus timings |
| `exp0_plain_qsvc.py` | Plain QSVC replication (real API) and tutorial-08 QKA |
| `exp1_nested_cv.py`, `exp1b_lowbw.py`, `analyze_exp1.py` | Q2 replication, CIs and paired tests |
| `exp2_diagnostics.py`, `exp2b_real_auditor.py` | Concentration, bandwidth, g, alignment |
| `exp3_positive_control.py`, `exp3b_auditor.py`, `exp3c_auditor_validation.py` | Positive control and frozen-rule validation |
| `exp4_noise.py`, `exp4b_noise_lowbw.py` | Aer Forte-like noise and shots |
| `exp5_gatecounts.py`, `exp6_job_sizing.py` | Transpiled counts (IonQ vs heavy-hex) and one-job sizing |
| `judge_run_prototype.py` | Pyodide-compatible live-demo prototype, 2.2 s native |
| `results/*.json`, `*.md`, `*.pkl`, `*.npz` | All outputs (JSON for shipping; pickles for re-analysis) |
| `.venv/` | qiskit 2.3.1 + qiskit-machine-learning 0.9.1 + Aer, for re-running the real-API checks |

### Gaps
- No Qollab-side test of this code was possible from here: Pyodide timing, the IonQ backend object's options (`noise_model`, `sampler_seed`) through Qollab, and file-size behaviour all need checking in hour 0–2.
- The hour plan assumes 2–4 people. For a solo builder, drop E4 to the cached-result fallback.
