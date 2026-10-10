# Quantum Machine Learning (QML) Use Cases: Technical Knowledge Base for a "Quantum Impact" Project (as of 2026-10-09)

**What this is for.** A credible Qollab × IonQ "Quantum Impact" entry (Oct 9–11, 2026, 48 h). It needs a real-world problem, a hybrid approach, a public dataset, a strong classical baseline, and a measurable quantum step.

**Build constraints** (user-supplied, cross-checked against earlier notes in `research_notes/`):
- Qiskit 2.x in Pyodide 314.x (Python 3.14); qiskit-machine-learning 0.9.1.
- Built-in statevector simulator: 24 qubits. IonQ Forte noise simulator: ≤29 qubits.
- IonQ natives are GPi, GPi2 and ZZ(θ) with all-to-all connectivity. Budget about 100 two-qubit (2Q) gates.
- No dynamic circuits. One IonQ job per run, but a multi-circuit job is allowed: ≤5,000 circuits and ≤150,000 gates per job.
- Judges press Run on a free local simulator.

**Tags used throughout:**
- **[NEW 2025] / [NEW 2026]**: recent results.
- **[Vendor]**: claim made by a company about its own product or project.
- **[Independent]**: academic or third-party evaluation.
- **[Computed]**: numbers I produced myself. The scripts are in `research_notes/Quantum Impact theme deep dive/scripts/` (`qk_bc.py`, `qrc_mg.py`, `qrc_tune.py`, `qrc_shots.py`), run with NumPy 1.26.4 and scikit-learn 1.8.0 on native CPython. These are not literature values.

**Fidelity rule of thumb** (my arithmetic; it ignores 1Q, SPAM and crosstalk errors): F ≈ 0.995^N2Q at 0.5% 2Q error.

| N2Q | 14 | 28 | 36 | 44 | 48 | 56 | 84 | 100 | 112 |
|---|---|---|---|---|---|---|---|---|---|
| F | 0.93 | 0.87 | 0.84 | 0.80 | 0.79 | 0.76 | 0.66 | 0.61 | 0.57 |

---

## Q1. Methods: how each QML family works, what it costs, and where it stands

### Takeaway
Every near-term QML family has known classical "shadows":
- Fidelity kernels concentrate exponentially. Bandwidth tuning rescues them, but it also pulls them toward classically simulable regimes.
- Variational and data re-uploading models are truncated Fourier series, so random Fourier features (RFF) and classical surrogates often match them.
- Quantum convolutional neural networks (QCNNs) on standard benchmarks are effectively classically simulable (PRX Quantum 2026).
- Equivariant and small-dynamical-Lie-algebra (small-DLA) models are often simulable through their symmetry.

Provable separations exist mainly for **quantum data**, meaning learning from quantum experiments with quantum memory, or under cryptographic assumptions. **[NEW 2026]** There is now a claimed memory-size separation for massive classical data that needs about 60 *logical* qubits, which is not a NISQ result.

For a 48-hour IonQ-constrained build, the families that fit both the hardware and an honest benchmark are:
- **projected quantum kernels (PQK)**, which need only U(x) and O(N) circuits rather than O(N²);
- **restart-protocol quantum reservoirs** with native all-to-all ZZ;
- **quantum circuit Born machines (QCBMs)**, where the IonQ step is a single sampling circuit;
- a **re-uploading classifier head** on frozen embeddings, mirroring IonQ's own 2025–2026 papers.

### Cited Findings

#### 1.1 Quantum kernels

**Fidelity kernels and their theory**
- The fidelity ("quantum kernel estimation") kernel is k(x,x') = |⟨φ(x)|φ(x')⟩|², estimated as the all-zeros probability of U(x')†U(x)|0⟩. The ZZ feature map uses phases x_i on single qubits and (π−x_i)(π−x_j) on pairs. Havlíček et al. demonstrated it on 2 superconducting qubits — [Havlíček et al., Nature 567, 209 (2019)](https://arxiv.org/abs/1804.11326).
- Theory of kernels in feature Hilbert spaces — [Schuld & Killoran, PRL 122, 040504 (2019)](https://arxiv.org/abs/1803.07128).
- A provable end-to-end speedup exists for a quantum kernel on a discrete-log-based classification task, assuming DLP hardness. The dataset is artificial and cryptographic — [Liu, Arunachalam, Temme, Nat. Phys. 17, 1013 (2021)](https://arxiv.org/abs/2010.02174).

**Projected quantum kernel and geometric difference** (Huang et al., "Power of data in quantum machine learning", Nat. Commun. 12, 2631, 2021; numerical tests up to 30 qubits, "one of the largest numerical tests for gate-based QML" at the time) — [arXiv:2011.01938](https://arxiv.org/abs/2011.01938); [HTML v2](https://arxiv.org/html/2011.01938v2)
- **Projected quantum kernel (1-RDM version):** k^PQ(x_i,x_j) = exp(−γ Σ_k ‖ρ_k(x_i) − ρ_k(x_j)‖²_F), where ρ_k(x) is the one-qubit reduced density matrix (RDM) of qubit k after U(x).
- **Geometric difference:** g(K¹‖K²) = √‖√K² (K¹)⁻¹ √K²‖_∞, with both kernels normalised to Tr K = N. For classical versus quantum, g_CQ = g(K^C‖K^Q).
- **Model complexity:** s_K(N) = yᵀK⁻¹y, which equals ‖w‖² of the trained model.
- **Generalisation bound:** E|h(x) − f(x)| ≤ c·√(s_K(N)/N). The regularised version uses (K+λI)⁻¹.
- **Decision flowchart:**
  1. If g_CQ is small, then s_C ≤ g_CQ²·s_Q, so the classical model is competitive.
  2. If g_CQ and min(rank K^Q, Tr O²) are both small, the encoding is classically easy for any quantum neural network (QNN).
  3. An advantage on a given task needs a large gap between s_C and s_Q **for the actual labels**.
- **Experiments:** Fashion-MNIST (PCA to n features), three embeddings (E1 separable rotations, E2 IQP-type, E3 Hamiltonian evolution), and engineered labels with s_PQ = 1 and s_C = g². The PQK gains more than 20% at large n on those engineered labels. Projections can be estimated with classical shadows.

**Bandwidth and inductive bias**
- Quantum kernels without a tunable bias (bandwidth) have a flat spectrum and cannot generalise at large n. Projected or "biased" kernels are needed — [Kübler, Buchholz, Schölkopf, NeurIPS 2021](https://arxiv.org/abs/2106.03747).
- Scaling the data by a bandwidth factor c < 1 (x → c·x) restores generalisation of fidelity kernels at large qubit counts — [Shaydulin & Wild, PRA 106, 042407 (2022)](https://arxiv.org/abs/2111.05451); [Canatar et al., "Bandwidth enables generalization in quantum kernel models", TMLR 2023](https://arxiv.org/abs/2206.06686).

**Kernel training and alignment**
- Kernel-target alignment trains parameterised embeddings ("quantum embedding kernels"). The same paper discusses noise mitigation and regularisation of noisy kernel matrices (positive-semidefinite (PSD) projection, mitigation using the measured diagonal) — [Hubregtsen et al., PRA 106, 042431 (2022)](https://arxiv.org/abs/2105.02276).
- Covariant kernels for group-structured data were run on 27 IBM qubits with kernel alignment — [Glick et al., Nat. Phys. 20, 479 (2024)](https://arxiv.org/abs/2105.03406).

**Exponential concentration** (Thanasilp, Wang, Cerezo, Holmes, Nat. Commun. 15 (published 18 Jun 2024), DOI 10.1038/s41467-024-49287-w; arXiv first Aug 2022) — [arXiv:2208.11060](https://arxiv.org/abs/2208.11060v2); [PMC](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11189509/)
- Kernel values concentrate exponentially in n around a fixed value. Four causes: expressive embeddings, **global measurements** (enough on their own for fidelity kernels), entanglement, and noise.
- With polynomially many shots, the trained model becomes independent of the input data with high probability.
- Kernel-alignment training is also affected.

**Shot complexity of QSVMs**
- Solving the dual problem needs O(M^4.67/ε²) circuit evaluations for M training points.
- A Pegasos-style primal solver needs O(min{M²/ε⁶, 1/ε¹⁰}).
- Measurement noise drives the cost, and the bounds are empirically "essentially tight".
- Source: [Gentinetta, Thomsen, Sutter, Woerner, Quantum (Jan 2024)](https://arxiv.org/abs/2203.00031).

**qiskit-machine-learning 0.9.x** (the build target)
- **0.9.0:** migrated to Qiskit 2.x and V2 primitives. Circuit-library classes became functions (e.g., `ZZFeatureMap` → `zz_feature_map`). Added `QMLSampler`/`QMLEstimator` with exact and shot-noise modes, `predict_proba` for `PegasosQSVC`, and partial multi-class `VQC`.
- **0.9.1:** added regression kernel losses (`SVRLoss`, `MSRLoss`, `MARLoss`, `HuberLoss`) for `QuantumKernelTrainer`.
- **Earlier releases:** `FidelityQuantumKernel` gained `max_circuits_per_job` in 0.8.0. The kernel classes are `FidelityStatevectorKernel` (0.6), `TrainableFidelityQuantumKernel` (0.5), `TrainableFidelityStatevectorKernel` (0.7) and `PegasosQSVC` (0.3).
- Source: [qiskit-machine-learning release notes](https://qiskit-community.github.io/qiskit-machine-learning/release_notes.html).

**Pyodide package availability**
- **Included:** scikit-learn 1.8.0, scipy 1.18.0, pandas 3.0.2, numpy 2.4.6, statsmodels, **xgboost 2.1.4**, **lightgbm 4.6.0**, networkx, sympy.
- **Not included:** PyTorch and TensorFlow.
- Source: [Pyodide packages list (v314.0.7)](https://pyodide.org/en/stable/usage/packages-in-pyodide.html).

#### 1.2 Variational quantum classifiers (VQC) and data re-uploading
- A single qubit with repeated data encoding ("re-uploading") is a universal classifier — [Pérez-Salinas et al., Quantum 4, 226 (2020)](https://arxiv.org/abs/1907.02085).
- Pauli-rotation encodings make the model a truncated Fourier series. With L re-uploads of a single-qubit Pauli encoding, the accessible frequencies are integers in [−L, L], and the trainable blocks set the coefficients — [Schuld, Sweke, Meyer, PRA 103, 032430 (2021)](https://arxiv.org/abs/2008.08605).
- Re-uploading models can be exponentially more data-efficient than any kernel built from the same encoding on specific tasks. Any re-uploading model maps to an explicit linear model in a larger space — [Jerbi et al., Nat. Commun. 14, 517 (2023)](https://arxiv.org/abs/2110.13162).
- **Dequantisation routes for these models:**
  - Classical Fourier surrogates — [Schreiber, Eisert, Meyer, PRL 131, 100803 (2023)](https://arxiv.org/abs/2206.11740).
  - Random Fourier features (RFF) — [Landman et al., ICLR 2023](https://arxiv.org/abs/2210.13200).
  - Limits of RFF (when they fail to dequantise) — [Sweke et al., arXiv:2309.11647](https://arxiv.org/abs/2309.11647).

#### 1.3 Quantum convolutional neural networks (QCNNs)
- The original QCNN uses convolution, pooling by measurement plus controlled ops, and O(log n) depth. It was applied to symmetry-protected topological phase recognition and quantum-error-correction (QEC) code optimisation — [Cong, Choi, Lukin, Nat. Phys. 15, 1273 (2019)](https://arxiv.org/abs/1810.03787). QCNNs have no barren plateaus — [Pesah et al., PRX 11, 041011 (2021)](https://arxiv.org/abs/2011.02966).
- **[NEW 2026, Independent]** "Quantum Convolutional Neural Networks are Effectively Classically Simulable" (Bermejo, Braccia, Rudolph, Holmes, Cincio, Cerezo):
  - arXiv 22 Aug 2024, published in **PRX Quantum 7, 020304 (2026)**.
  - Randomly initialised QCNNs use only **low-bodyness** information. Standard phase-classification benchmarks are "locally easy".
  - A classical Pauli-shadow algorithm reproduces QCNN behaviour on up to **1,024 qubits**.
  - The authors' conclusion: "non-trivial datasets are a truly necessary ingredient".
  - Source: [arXiv:2408.12739](https://arxiv.org/abs/2408.12739).

#### 1.4 Quantum reservoir computing (QRC) and quantum extreme learning machines (QELMs)
- QRC uses fixed quantum dynamics as the reservoir with a trained linear readout — [Fujii & Nakajima, PR Applied 8, 024030 (2017)](https://arxiv.org/abs/1602.08159). Reviews of QRC and QELM — [Mujal et al., Adv. Quantum Technol. (2021)](https://arxiv.org/abs/2102.11831). Limits of QELMs (what the readout can extract) — [Innocenti et al., Commun. Phys. 6, 118 (2023)](https://arxiv.org/abs/2210.00780).
- **[NEW 2024, Vendor-led]** QuEra/Harvard ran a gradient-free QRC on neutral-atom analog hardware, scaling to **108 qubits**. They report "competitive" performance on classification and time series, and a "comparative advantage" only on **synthetic datasets built from geometric differences** between quantum and classical kernels — [Kornjača et al., arXiv:2407.02553](https://arxiv.org/abs/2407.02553v1); [TQI coverage](https://thequantuminsider.com/2024/07/22/researchers-report-quantum-reservoir-computing-scales-up-to-108-qubits-in-step-toward-real-world-quantum-machine-learning/).
- **[NEW 2026]** An experimental QRC in 9 correlated spins (platform not named in the abstract):
  - prediction error 1–2 orders of magnitude lower than previous QRC experiments;
  - on long-term weather forecasting it beats classical reservoirs "with thousands of nodes";
  - published in **PRL 136, 120602 (2026)**.
  - Source: [Hou et al., arXiv:2508.12383](https://arxiv.org/abs/2508.12383).
- **[NEW 2026]** An experimental QELM on IBM devices with up to 124 qubits and more than 5,000 2Q gates. The authors flag that noise erases the distinguishability of inputs at scale — [arXiv:2603.13005](https://arxiv.org/html/2603.13005v1) (via search summary).
- **Trapped ions:** I found **no completed trapped-ion QRC time-series experiment**. The nearest is a 2025 APS DAMOP *proposal* to embed a reservoir in a trapped-ion processor, using motional modes, for sensing — [DAMOP 2025 abstract](https://archive.aps.org/damop/2025/h00/86).
- **Strong classical baseline for reservoirs:** "next-generation reservoir computing" (nonlinear vector autoregression, NVAR: polynomial features of a delay window) — [Gauthier et al., Nat. Commun. 12, 5564 (2021)](https://arxiv.org/abs/2106.07688).

#### 1.5 Quantum generative models
- **QCBM**: p_θ(x) = |⟨x|U(θ)|0⟩|². Introduced in [Benedetti et al., npj QI 5, 45 (2019)](https://arxiv.org/abs/1801.07686). Differentiable training with a kernel MMD loss — [Liu & Wang, PRA 98, 062324 (2018)](https://arxiv.org/abs/1804.04168).
- **QCBM training barriers:** MMD with a Gaussian kernel trains only if the bandwidth targets low-order correlations, and explicit losses such as KL suffer barren plateaus — [Rudolph et al., npj QI (2024), "Trainability barriers and opportunities in quantum generative modeling"](https://arxiv.org/abs/2305.02881).
- **Generalisation metrics** for generative models (fidelity, rate and coverage of unseen valid samples) — [Gili et al., arXiv:2201.08770](https://arxiv.org/abs/2201.08770); [Gili et al., "Do QCBMs generalize?", QST 8, 035021 (2023)](https://arxiv.org/abs/2207.13645).
- **Finance:** QCBM versus a restricted Boltzmann machine (RBM) on correlated asset data — [Coyle et al., QST 6, 024013 (2021)](https://arxiv.org/abs/2008.00691).
- **"Qopula"** (IonQ + Fidelity CAT, 2021):
  - The copula-structured ansatz starts from Bell pairs (2 variables) or GHZ states (more variables).
  - QGAN and QCBM were trained on stock data on IonQ hardware with up to 8 qubits. **[Vendor/academic]** The authors report it "outperform[s]" equivalent classical generative learning.
  - Source: [Zhu et al., arXiv:2109.06315](https://www.arxiv.org/pdf/2109.06315v1).
- **Copula risk aggregation** (IonQ + GE Research, 2022): 3–4-variable copulas on four stock indexes, run on a simulator and on IonQ trapped-ion hardware (one run on Aria). Training degraded with scale, and an annealing-inspired schedule fixed it. Results were "comparable or better" than standard classical models — [arXiv:2206.11937](https://arxiv.org/pdf/2206.11937v1); [TQI](https://thequantuminsider.com/2022/06/25/ionq-ge-research-demonstrate-potential-of-quantum-computing-for-risk-aggregation/).
- **QCBM as a GAN prior:** Zapata + IonQ generated high-resolution handwritten digits using a QCBM prior on an ion trap — [Rudolph et al., PRX 12, 031010 (2022)](https://arxiv.org/abs/2012.03924).
- **qGAN** for loading distributions, e.g. for amplitude estimation — [Zoufal, Lucchi, Woerner, npj QI 5, 103 (2019)](https://arxiv.org/abs/1904.00043).
- **[NEW 2025, Vendor + customer] IonQ + Hyundai hybrid quantum Wasserstein GAN for steel microstructures** (5-channel electron backscatter diffraction (EBSD) images of ferrite and bainite):
  - A quantum circuit acts as the input/latent layer of a large classical WGAN.
  - The paper reports the hybrid "improves over classical Bernoulli GANs in 70% of samples" on maximum mean discrepancy (MMD). IonQ's press release words it as "higher quality score in up to 70% of cases".
  - It ran on IonQ hardware; a secondary summary says Aria-2.
  - The baseline is Bernoulli-prior GANs, not a tuned classical generator.
  - Sources: [arXiv:2504.08728](https://arxiv.org/pdf/2504.08728); [IonQ blog, 30 Apr 2025](https://ionq.com/blog/ionq-and-leading-global-automotive-manufacturer-collaborate-to-advance).
- **[NEW 2025] Google, "Generative quantum advantage for classical and quantum problems"**:
  - 68-qubit superconducting processor; tasks were learning classically intractable distributions and learning circuits for faster simulation.
  - The model families are claimed hard to simulate yet trainable without barren plateaus, using deep-to-shallow circuit mappings and a "sewing" learner.
  - Preprint, Sep 2025.
  - Sources: [arXiv:2509.09033](https://arxiv.org/abs/2509.09033); [Google Research](https://research.google/pubs/generative-quantum-advantage-for-classical-and-quantum-problems/).
- **[NEW 2025] Insilico / U. Toronto KRAS inhibitors** (Nature Biotechnology, Jan 2025; Ghazi Vakili et al.):
  - A QCBM prior on a **16-qubit IBM** device was combined with an LSTM, trained on 1.1M molecules (650 known KRAS inhibitors) and scored by Chemistry42.
  - 15 molecules were synthesised and 2 were active. The lead compound, ISM061-018-2, binds KRAS-G12D at 1.4 µM.
  - Insilico's CEO says this does **not** show the molecules beat classically found ones, and 16 qubits are classically simulable.
  - Sources: [arXiv:2402.08210](https://arxiv.org/pdf/2402.08210); [TQI](https://thequantuminsider.com/2025/01/23/quantum-computing-helps-design-new-cancer-drug-candidates/); [CQIQC listing](https://cqiqc.physics.utoronto.ca/research/recent-publications/quantum-computing-enhanced-algorithm-unveils-potential-kras-inhibitors/).

#### 1.6 Quantum Boltzmann machines (QBMs)
- QBMs use a transverse-field Ising Hamiltonian, ρ = e^{−H}/Z, with bounds on training — [Amin et al., PRX 8, 021050 (2018)](https://arxiv.org/abs/1601.02036).
- QBMs sit in the Bowles et al. benchmark; removing entanglers hurt the QBM "to some extent" — [Bowles, Ahmed, Schuld, arXiv:2403.07059](https://arxiv.org/html/2403.07059v2).
- Sample complexity of QBM learning (relative-entropy training is polynomial given Gibbs-state preparation) — [Coopmans & Benedetti, arXiv:2306.14969](https://arxiv.org/abs/2306.14969).

#### 1.7 Quantum transformers and attention
- **[NEW 2024, Vendor] Quixer (Quantinuum):** a transformer built from linear combination of unitaries (LCU) and quantum singular value transformation (QSVT) primitives. On Penn Treebank language modelling it is "competitive with an equivalent classical baseline". This was **classical simulation only**, and the blog calls it the first QML language model on a realistic dataset — [arXiv:2406.04305](https://arxiv.org/abs/2406.04305); [Quantinuum blog](https://www.quantinuum.com/blog/announcing-quixer---quantinuums-state-of-the-art-quantum-transformer-making-quantum-ai-a-little-more-realistic).
- **[Independent]** An Aalto thesis re-implementation matched the published baseline — [Aalto thesis](https://aaltodoc.aalto.fi/items/a3998701-7b17-48e2-a74e-bcf87d927c26/full).
- Quantum vision transformers (orthogonal-layer attention) — [Cherrat et al., Quantum 8, 1265 (2024)](https://arxiv.org/abs/2209.08167).

#### 1.8 Hybrid quantum layers in LLM fine-tuning (IonQ)
- **[NEW 2025, Vendor research] "Quantum Large Language Model Fine-Tuning"** (Kim, Mei, Girotto, Yamada, Roetteler; IonQ; 11 Apr 2025)
  - **Setup:**
    - SetFit-trimmed **SST-2** sentiment data: 256 positive + 256 negative training samples (85/15 train/validation) and 9,101 test samples.
    - Frozen `paraphrase-mpnet-base-v2` sentence transformer (768-d embeddings).
    - The quantum head is a "sentence quantum encoder" with RY angle encoding and data re-uploading (R = 4), using CNOT+RY blocks, 10–18 qubits, and 8,192 shots.
    - **Noisy simulation only:** depolarising noise of (1Q, 2Q) = (1e-4, 1e-3) and (2e-4, 2e-3), simulated in TorchQuantum and "derived from" Forte Enterprise. There were no hardware runs.
  - **Accuracy:**

    | Model | Accuracy | Parameters |
    |---|---|---|
    | Best multi-encoder quantum head, 14 qubits | **92.70%** | 886 |
    | Neural-network head | 91.44% | 148,034 |
    | Neural-network head | 91.05% | 1,538 |
    | SVC | 89.56% | 296 support vectors |
    | Logistic regression | 89.06% | — |

  - The headline "up to 3.14%" is 92.70 versus the SVC, which is not size-matched. The best NN encoder in the ablation reached 92.13%, and end-to-end fine-tuning reached 93.62%.
  - The energy "crossover at 46 qubits" is an analytical estimate.
  - Sources: [arXiv:2504.08732](https://arxiv.org/abs/2504.08732); [HTML](https://arxiv.org/html/2504.08732).
- **[NEW 2026, Vendor research] IonQ + QuantumBasel energy-to-solution study** (arXiv:2605.02798, submitted to IEEE Quantum Week; TQI coverage 21 Jul 2026)
  - **Hardware:** inference ran on **Forte Enterprise (36 qubits)**. Training was classical/simulated. Accuracy tests used circuits up to 18 qubits.
  - **Accuracy:** best hardware result with error mitigation was **91.2%**, against **92.06%** noiseless. The relative error reduction over the best classical fine-tuned baseline was about 24% in simulation and about 16% on hardware.
  - **Test set:** only **250 samples**, which is large statistical uncertainty.
  - **Energy:** QPU energy rose about linearly with qubits, GPU statevector energy exponentially. Projected break-even is about **34 qubits** against GPU statevector, extrapolated from measurements up to 28 qubits. An advantage over MPS simulation is "theoretical and not validated".
  - The authors call it "an experimental proof of concept rather than evidence of broad quantum advantage".
  - Source: [TQI, 21 Jul 2026](https://thequantuminsider.com/2026/07/21/ionq-quantumbasel-study-suggests-hybrid-ai-workloads-could-gain-energy-advantages-from-quantum-hardware-as-systems-scale/).

#### 1.9 Time-series forecasting, anomaly detection, QNLP
- **Time-series forecasting:** QRC and quantum LSTM (QLSTM) are the main routes. In a QLSTM versus LSTM comparison for solar power forecasting, the reported benefits are faster convergence and lower first-epoch test loss, plus a call for systematic hyperparameter optimisation and noise studies — [arXiv:2310.17032 / Frontiers in Physics (Oct 2024)](https://arxiv.org/abs/2310.17032v3).
- **Anomaly detection:**
  - Quantum anomaly detection on quantum data — [Liu & Rebentrost, PRA 97, 042315 (2018)](https://arxiv.org/abs/1710.07405).
  - **[Independent]** A classical autoencoder latent space feeds a quantum kernel (one-class SVM) and quantum clustering. In "one parameter regime" the quantum kernel beats its classical counterpart, and one instance was run on real hardware — [Belis, Woźniak et al., Commun. Phys. 7 (Oct 2024), DOI 10.1038/s42005-024-01811-6](https://arxiv.org/abs/2301.10780v3).
  - Unsupervised quantum fraud detection — [Kyriienko & Magnusson, arXiv:2208.01203](https://arxiv.org/abs/2208.01203).
- **Quantum natural language processing (QNLP):**
  - DisCoCat compositional semantics — [Coecke, Sadrzadeh, Clark (2010)](https://arxiv.org/abs/1003.4394).
  - lambeq toolkit — [Kartsaklis et al. (2021)](https://arxiv.org/abs/2110.04236).
  - QNLP in practice on hardware — [Lorenz et al., JAIR (2023)](https://arxiv.org/abs/2102.12846).
  - **[NEW 2024, Vendor]** Text-level QDisCoCirc on **Quantinuum H1-1**. Components are trained classically at small scale and composed into larger instances that run on hardware. The task is a **handcrafted toy** question-answering dataset; small neural models and GPT-4 failed to generalise compositionally on it. Quantinuum states it has "not yet solved a problem at scale" — [Duneau et al., arXiv:2409.08777](https://arxiv.org/pdf/2409.08777); [TQI](https://thequantuminsider.com/2024/09/18/quantinuum-unveils-first-contribution-toward-responsible-ai-uniting-power-of-its-quantum-processors-with-experimental-work-on-integrating-classical-quantum-computing/).
  - **[NEW 2025, Vendor]** λambeq Gen II (May 2025) moves from DisCoCat to DisCoCirc — [Quantinuum blog](https://www.quantinuum.com/blog/lambeq-gen-ii-a-quantum-enhanced-interpretable-and-scalable-text-based-nlp-software-package).

#### 1.10 Quantum-inspired, tensor-network, geometric and equivariant QML
- **Tensor networks:**
  - Matrix product state (MPS) classifiers — [Stoudenmire & Schwab, NeurIPS 2016](https://arxiv.org/abs/1605.05775).
  - Tensor-network QML circuits — [Huggins et al., QST 4, 024001 (2019)](https://arxiv.org/abs/1803.11537).
  - **[NEW 2025]** A tensor-network anomaly detector in the same LHC latent space as the quantum study above — [arXiv:2506.00102](https://arxiv.org/pdf/2506.00102).
- **Quantum-inspired classical algorithms:** Tang's dequantised recommendation systems and PCA — [Tang, STOC 2019](https://arxiv.org/abs/1807.04271); [Tang, PRL 127, 060503 (2021)](https://arxiv.org/abs/1811.00414).
- **Geometric/equivariant QML:**
  - Group-invariant QML — [Larocca et al., PRX Quantum 3, 030341 (2022)](https://arxiv.org/abs/2205.02261).
  - Exploiting symmetry in variational QML — [Meyer et al., PRX Quantum 4, 010328 (2023)](https://arxiv.org/abs/2205.06217).
  - Theory of equivariant QNNs — [Nguyen et al., PRX Quantum 5, 020328 (2024)](https://arxiv.org/abs/2210.08566).
  - **Caveat:** symmetric systems often admit efficient classical simulation — [Anschuetz et al., Quantum 7, 1189 (2023)](https://arxiv.org/abs/2211.16998).

#### 1.11 QML for quantum data: where provable advantages exist
- **Huang et al., "Quantum advantage in learning from experiments"** (Science 376, 1182, 2022):
  - Learners with quantum memory, which process copies coherently (e.g. Bell measurements on two copies), learn from **exponentially fewer experiments** than conventional measure-then-learn strategies.
  - Tasks: predicting properties of physical systems, quantum PCA of noisy states, and learning models of dynamics.
  - Hardware: up to **40 superconducting qubits and 1,300 gates**.
  - Source: [arXiv:2112.00778](https://arxiv.org/abs/2112.00778).
- Exponential separations between learning with and without quantum memory — [Chen, Cotler, Huang, Li, FOCS 2021](https://arxiv.org/abs/2111.05881).
- Provably efficient ML of ground-state properties from classical shadows. This is a *classical* learner on quantum data — [Huang, Kueng, Torlai, Albert, Preskill, Science 377, eabk3333 (2022)](https://arxiv.org/abs/2106.12627).
- Exponential advantages in learning quantum observables from classical data — [Molteni, Gyurik, Dunjko, arXiv:2405.02027](https://arxiv.org/pdf/2405.02027) (forthcoming in npj QI 2026, per search summary).
- **[NEW 2026] Danaci, Patel, Molteni, van Nieuwenburg, Dunjko, Krzywda**:
  - simulations and hardware-constraint analysis show a "clear performance separation" between coherent processing and measure-first strategies at **30–40 noisy qubits** on a quantum-data task with known asymptotic advantage;
  - matching it measure-first would take "months or even years of measurements";
  - not a hardware experiment.
  - Source: [arXiv:2605.21346](https://arxiv.org/abs/2605.21346).

### Inferences
- **The PQK is the IonQ-friendly kernel.**
  - The fidelity kernel needs U(x')†U(x), which doubles 2Q depth, and O(N_test × N_SV) circuits.
  - The PQK needs only U(x) plus three local measurement bases (or random Pauli shadows), so 3N circuits in total. The classical post-processing is exact.
  - For one multi-circuit IonQ job (≤5,000 circuits, ≤150k gates) this is the difference between "fits" and "doesn't fit" (see Q5).
- **Native ZZ(θ) makes IQP/ZZ-style maps, Ising-type reservoirs and QCBM entanglers cost one 2Q gate per term**, against two CNOTs elsewhere. The all-to-all connectivity matters for the dense random couplings typical of reservoirs.
- **A "hybrid head on frozen embeddings" is the IonQ-recognisable application pattern** (IonQ 2025 and 2026). Torch is absent from Pyodide, so embeddings must be **precomputed offline** and shipped. This is legitimate if disclosed.
- QCNNs, QNLP (DisCoCat) and quantum transformers are poor 48-hour choices:
  - QCNN benchmarks are classically simulable (Bermejo 2026).
  - lambeq is not in the Qollab library list. I did not check whether lambeq installs in Pyodide.
  - Quixer-like LCU/QSVT circuits exceed the 2Q budget.

### Gaps
- The full-text design of QuEra's QRC baselines and their "competitive" numbers were not retrieved.
- I found no 2025–2026 trapped-ion QRC or QELM hardware experiment. Absence of evidence is not evidence of absence.
- I did not confirm whether qiskit-machine-learning 0.9.1 ships any projected-kernel class (none appears in the release notes). Plan to implement the PQK by hand from `Statevector` reduced density matrices.
- The Google generative-advantage paper (2509.09033) is still a preprint as far as these searches show. The full Hou et al. PRL text (which platform?) was not retrieved.

---

## Q2. Evidence and critiques, 2022–2026: does QML beat classical ML?

### Takeaway
On classical data, the independent evidence is consistently "no robust advantage at small scale":
- **Bowles et al. 2024**: across 12 models and 160 datasets, out-of-the-box classical models ranked first in every model family, and removing entanglement often did not hurt.
- **[NEW 2026] Kakavand et al.**: 970 experiments with nested cross-validation; 0 of 29 quantum-versus-classical comparisons were significant.

The theory explains why:
- concentration;
- dequantisation by RFF and surrogates;
- "absence of barren plateaus ⇒ often simulable" (Cerezo et al. 2025);
- memorisation of random labels (Gil-Fuster et al. 2024).

The credible positive results are about **quantum data with quantum memory** (Huang 2022; Danaci 2026), **cryptographic or artificial structure** (Liu 2021), or **fault-tolerant, memory-size separations** ([NEW 2026] Zhao et al., under 60 logical qubits). Schuld and Killoran's 2022 reframing is the right posture for a hackathon: treat QML as a research programme into new model classes, with honest benchmarking, rather than a race for advantage.

### Cited Findings

**Bowles, Ahmed, Schuld, "Better than classical? The subtle art of benchmarking quantum machine learning models"** (Xanadu, arXiv Mar 2024) — [arXiv:2403.07059](https://arxiv.org/html/2403.07059v2); [PennyLane blog](https://pennylane.ai/blog/2024/03/benchmarking-near-term-quantum-algorithms-is-an-art/); [qml-benchmarks code](https://github.com/XanaduAI/qml-benchmarks)
- **Models (12):**
  - QNNs: CircuitCentric, DataReuploading, DressedQuantumCircuit, IQPVariational, QuantumBoltzmannMachine, QuantumMetricLearner, TreeTensor.
  - Kernels: IQPKernel, ProjectedQuantumKernel, QuantumKitchenSinks.
  - Convolutional: Quanvolutional, WeiNet.
- **Baselines:** MLP, Gaussian SVC and CNN, plus separable (unentangled) variational and kernel classifiers.
- **Data:** 6 generators producing 160 datasets (linearly separable, bars-and-stripes, downscaled MNIST, hidden manifold, two curves, hyperplanes-and-parity).
- **Protocol:** at most 18 qubits (about 20 qubits was infeasible). Full scikit-learn grid search with 5-fold cross-validation.
- **Results:**
  - Out-of-the-box classical models ranked first in every family.
  - Among QNNs the MLP was usually first and DressedQuantumCircuit (a classical network with a small quantum layer) usually second. The amplitude-encoding models (CircuitCentric, TreeTensor) were usually worst.
  - Among kernels the SVC was best in 4 of 7 benchmarks and QuantumKitchenSinks consistently worst. The CNN beat both quantum convolutional models.
  - Quantum models did especially badly on **linearly separable** data.
  - SeparableKernelClassifier ranked second among kernels. Removing entanglers did not hurt DressedQuantumCircuit, but did hurt DataReuploading and partly QBM.
- **The paper's five design questions:** do quantum components in hybrids help; what makes re-uploading work; what distances quantum kernels define; why polynomial features fail; why the linearly separable task is hard.

**[NEW 2026, Independent] Kakavand, Strohmeyer, Schlotter**, quantum kernel SVMs versus classical baselines on tabular data, with hardware validation (20 Apr 2026) — [arXiv:2604.18837](https://arxiv.org/abs/2604.18837)
- 970 experiments with nested cross-validation: 9 binary datasets, 4 quantum feature maps, 3 classical kernels. RBF was the best classical kernel.
- None of 29 pairwise comparisons was significant at α = 0.05.
- Quantum learning curves were steeper on 6 of 8 datasets but never closed the gap.
- **Dataset choice explained ε² = 0.73 of variance; kernel type about 9%.**
- Quantum kernel spectra are "either too flat or too concentrated", lacking the RBF's intermediate profile.
- The only competitive quantum result was kernel-target alignment on breast cancer (balanced accuracy 0.968), at about 2,000× the compute.
- Hardware kernel fidelity on ibm_fez was r ≥ 0.976.

**Benchmarks from particle physics**
- **[Independent]** ttH and H→μμ with 10–15 qubits: the quantum SVM and VQC "perform similarly" to classical SVM and BDTs. For ttH the VQC AUC was 0.81 against 0.83 for SVM and BDT — [Wu et al., PRR 3, 033221 (2021)](https://arxiv.org/abs/2104.05059) (numbers via search summary).
- Kernel-training benchmark: "despite outperforming classical methods in ad-hoc datasets, mixed results … among standard classical benchmarks" — [arXiv:2408.10274](https://arxiv.org/abs/2408.10274v2).

**Positioning and generalisation**
- Schuld & Killoran, "Is quantum advantage the right goal for quantum machine learning?": argue for studying QML as model design and theory, not for chasing advantage claims on toy data — [PRX Quantum 3, 030101 (2022)](https://arxiv.org/abs/2203.01340).
- Gil-Fuster, Eisert, Bravo-Prieto (Nat. Commun. 15, 2277, Mar 2024): state-of-the-art QNNs fit **random labels and random states**, so VC-dimension and Rademacher uniform bounds cannot explain QML generalisation. Good generalisation is still possible; it just is not guaranteed by the model family alone — [arXiv:2306.13461](https://arxiv.org/abs/2306.13461v2); [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC10938005/).

**Dequantisation**
- Tang's ℓ²-sampling dequantisation of recommendation systems — [arXiv:1807.04271](https://arxiv.org/abs/1807.04271).
- A general low-rank QSVT dequantisation framework — [Chia et al., STOC 2020](https://arxiv.org/abs/1910.06151).
- Cotler, Huang, McClean, "Revisiting dequantization and quantum advantage in learning tasks": the dequantised comparisons assume classical sample-and-query access; when the input is quantum states, exponential separations reappear — [arXiv:2112.00811](https://arxiv.org/abs/2112.00811).
- **[NEW 2025]** On the relation between trainability and dequantisation of variational QML models (ICLR 2025) — [Gil-Fuster, Gyurik, Pérez-Salinas, Dunjko, arXiv:2406.07072](https://arxiv.org/abs/2406.07072).

**Barren plateaus versus simulability**
- **[NEW 2025]** Cerezo et al., "Does provable absence of barren plateaus imply classical simulability?" (Nat. Commun. 16, 7907, 2025). Many BP-free models confine evolution to small, classically simulable subspaces. The paper proposes "quantum-enhanced classical simulation", where the quantum device is used for data acquisition only. It is a perspective, not a theorem — [arXiv:2312.09121](https://arxiv.org/abs/2312.09121v3) (details in `Quantum Unlocked theme deep dive/algorithms_and_complexity.md`).
- Noisy variational algorithms beyond logarithmic depth are classically efficient to match under depolarising noise — [Stilck França & García-Patrón, Nat. Phys. (2021)](https://arxiv.org/abs/2009.05532).

**Positive results, 2025–2026**
- **[NEW 2026] "Exponential quantum advantage in processing massive classical data"** (Zhao, Zlokapa, Neven, Babbush, Preskill, McClean, Huang; v1 8 Apr 2026, v2 1 Oct 2026)
  - "Quantum oracle sketching" gives access to classical data in superposition from **random classical samples, with no QRAM**. Combined with classical shadows it builds succinct classical models.
  - Claimed separation: a polylog-size quantum machine matches classical machines that must be exponentially larger. Smaller classical machines need superpolynomially more samples and time, "even if BPP = BQP".
  - Real-data evidence on single-cell RNA-seq and movie-review sentiment: a **10⁴–10⁶× reduction in size using fewer than 60 logical qubits**.
  - It is a preprint, and the logical qubits imply error correction.
  - Sources: [arXiv:2604.07639](https://arxiv.org/abs/2604.07639); [TQI](https://thequantuminsider.com/2026/04/10/study-finds-exponential-quantum-advantage-in-machine-learning-tasks/); [Quantum Frontiers](https://quantumfrontiers.com/2026/04/09/unleashing-the-advantage-of-quantum-ai/).
- **[NEW 2026] Danaci et al.**: a quantum-data advantage regime at 30–40 noisy qubits, from simulation — [arXiv:2605.21346](https://arxiv.org/abs/2605.21346).
- **[NEW 2025] Google generative quantum advantage** (68 qubits) — [arXiv:2509.09033](https://arxiv.org/abs/2509.09033).
- **[NEW 2026]** 9-spin QRC PRL — [arXiv:2508.12383](https://arxiv.org/abs/2508.12383).

### Inferences
- **What judges will believe:** "on dataset X, a quantum model with these resources reaches parity or loses, and here is the diagnostic (g_CQ, kernel spectrum, shots-to-break-even) explaining why". That is more credible than "beats classical by Y%".
- Kakavand et al. found that **dataset choice explains 73% of variance and kernel type 9%**. Choosing one dataset and declaring a win is statistically meaningless. Use several datasets and seeds, and report confidence intervals.
- Every ablation in Bowles et al. (separable variant, classical surrogate, untuned MLP) is cheap in scikit-learn and should be shipped as a toggle.

### Gaps
- I did not read the full text of the 2026 Zhao et al. paper. I cannot state the exact datasets, accuracy or the logical-qubit circuit depth.
- I did not retrieve the exact headline tables of Kakavand et al. beyond the abstract.

---

## Q3. Industry use cases with results (vendor claims vs independent)

### Takeaway
Industry QML results to date fall into three groups:
1. **Small-qubit demos with no published accuracy**: Hyundai/IonQ road signs.
2. **Hybrid models where a small quantum block sits inside a large classical model, with modest gains against weak or unmatched baselines**: IonQ LLM head (+1.26 points over the best NN head; +3.14 over an unmatched SVC); IonQ/Hyundai QGAN ("70% of samples" versus Bernoulli GANs); Insilico QCBM (2 of 15 molecules active, no classical-superiority claim).
3. **Noise-as-regulariser effects mistaken for quantum value**: HSBC/IBM's "up to 34%" appears only with hardware noise and vanishes in noiseless simulation.

Independent benchmarks (particle physics, EHR, fraud, EO, intrusion detection) consistently report **parity with RBF-SVM or BDTs**, sometimes with narrow regimes of advantage on chosen settings.

### Cited Findings

#### Automotive and vision (IonQ + Hyundai)
- **[Vendor]** April 2022: IonQ was "well underway in classifying 43 types of road signs" and expanding to 3D object detection — [BusinessWire, 19 Apr 2022](https://www.businesswire.com/news/home/20220419005265/en); [Fierce Electronics](https://www.fierceelectronics.com/sensors/ionq-hyundai-expand-quantum-computing-partnership-object-detection-autonomous-vehicles).
- **[Vendor research]** APS March 2023: end-to-end training on **up to 8 qubits** on trapped-ion hardware and inference on a **16-qubit** backend, for **up to 10 image categories**. The IonQ case study concedes 16 qubits "is not enough for commercial use". **I found no published accuracy figure**, and the 43-class result is unexplained — [APS 2023 M64.3](https://meetings-archive.aps.org/mar/2023/m64/3); [IonQ case study](https://ionq.com/resources/picturing-the-future-quantum-enabled-road-sign-recognition).
- **[NEW 2025, Vendor]** Steel-microstructure QGAN with Hyundai: see Q1.5 ([arXiv:2504.08728](https://arxiv.org/pdf/2504.08728)).

#### Finance
- **[NEW 2025] HSBC + IBM bond-trading fill probability** ("Enhanced fill probability estimates in institutional algorithmic bond trading…", Ciceri et al., 16 authors, arXiv 22 Sep 2025)
  - Intraday European corporate-bond request-for-quote (RFQ) data was transformed by a quantum algorithm on **IBM Heron** processors and fed to classical learners.
  - The abstract claims "a relative gain of **up to ~34%** in out-of-sample test scores" against models on the original data **or on noiseless-simulation transforms**, and suggests hardware noise may contribute.
  - Sources: [arXiv:2509.17715](https://arxiv.org/abs/2509.17715).
  - **[Independent critique]** Scott Aaronson (25 Sep 2025) called it a "qombie": the effect appears only with noise, hence it is an artefact of the methods compared, prone to selection bias, with no prior benchmark-level advantage — [Shtetl-Optimized](https://scottaaronson.blog/?p=9170).
  - **[Independent critique]** Others note the paper attributes the effect to "inherent noise" without theory, and that classical "random resampling with shrinkage" could reproduce it — [Global Trading / fi-desk](https://www.fi-desk.com/quantum-computing-breakthrough-has-more-red-flags-than-a-peoples-liberation-army-parade/).
  - The authors themselves did not claim quantum advantage — [PostQuantum](https://postquantum.com/quantum-research/hsbc-ibm-quantum-advantage/).
  - The metric is described inconsistently in coverage (AUC-type score versus "error reduction") — [Sovereign Magazine](https://www.sovereignmagazine.com/article/hsbc-and-ibm-show-quantum-can-help-price-bond-quotes-34-better-predictions-in-rfq-trials).
- **IonQ copula/QCBM risk work** (2021–22, with Fidelity and GE Research): see Q1.5.
- **Fraud detection (2025–26):** individual papers with their own datasets and baselines, so no standard benchmark exists:
  - a hybrid QLSTM against a single LSTM — [arXiv:2505.00137](https://arxiv.org/pdf/2505.00137);
  - CVQBoost on QCi's photonic Dirac-3 machine: AUC-PR above 0.8, about 9% relative to the "best published" baseline (ICAART 2026);
  - QSVM on BankSim (594,643 simulated transactions) "competitive" with GPU classical ML, with NISQ sampling inefficiency noted (ISC 2025 poster);
  - quantum mixture-of-experts routing — [arXiv:2603.06473](https://arxiv.org/abs/2603.06473).
  - Summaries via search: [ISC 2025 listing](https://isc.app.swapcard.com/widget/event/isc-high-performance-2025/planning/UGxhbm5pbmdfMjU4NDUyMA==).
  - Earlier: quantum feature selection for fraud (IBM with a bank) — [Grossi et al., arXiv:2208.07963](https://arxiv.org/abs/2208.07963).

#### Healthcare and drug discovery
- **[Independent + vendor] Amgen + IBM, "Quantum kernels for real-world predictions based on electronic health records"** (arXiv Dec 2021; IEEE TQE 2022)
  - Grid of 5–20 features × 200–300 samples; custom quantum kernel on IBM hardware against an RBF-SVM; task was six-month persistence of rheumatoid-arthritis biologic therapy.
  - Found settings where the quantum kernel appeared better. The APS abstract calls the advantage incomplete, and the paper offers a framework (a "terrain ruggedness index") for predicting such regimes.
  - Sources: [arXiv:2112.06211](https://arxiv.org/abs/2112.06211v2); [APS 2022](https://meetings-archive.aps.org/mar/2022/s37/6).
- **Medical imaging:** quantum orthogonal-layer networks applied to MedMNIST subsets (RetinaMNIST, PneumoniaMNIST), with IBM hardware experiments at small qubit counts — [Landman et al., Quantum 6, 881 (2022)](https://arxiv.org/abs/2109.01831).
- **[NEW 2025] Insilico KRAS QCBM–LSTM** (Nature Biotechnology): see Q1.5.

#### Earth observation
- Hybrid QNNs for remote-sensing classification on EuroSAT — [Sebastianelli et al., IEEE JSTARS (2022)](https://arxiv.org/abs/2109.09484).
- **[NEW 2025]** About 500 hybrid and quantum CNN configurations on EuroSAT. Encoding choice swings validation accuracy by more than 30%; ansatz and measurement basis by under 5% — [arXiv:2506.20355](https://arxiv.org/html/2506.20355v2).
- **[NEW 2026]** QMC-Net reports 93.8–94.7%, against about 96–98% for the largest classical models on EuroSAT. The text summary was ambiguous about whether the figure is for EuroSAT or SAT-6 — [arXiv:2604.11817](https://arxiv.org/pdf/2604.11817).
- Neural quantum kernels for solar-panel detection, competitive up to 8 qubits — [arXiv:2409.20356](https://arxiv.org/pdf/2409.20356).
- Cloud detection with quantum-kernel SVMs "on par" with SVM — [Le Saux, IGARSS/GRSS 2023 slides](https://www.grss-ieee.org/wp-content/uploads/2023/09/Day-4.2-Bertrand-Le-Saux-Bringing-the-power-of-Quantum-Computing-to-Earth-Observation.pdf).

#### Particle physics (CERN/LHC)
- **[Independent]** The latent-space quantum anomaly detection study (Belis/Woźniak et al., Commun. Phys. 2024). The `qad` code is public — [arXiv:2301.10780](https://arxiv.org/abs/2301.10780v3); [docs](https://latent-ad-qml.readthedocs.io/en/stable/).
- The LHCb b-jet charge identification study with QML — [Gianelle et al., JHEP (2022)](https://arxiv.org/abs/2202.13943).
- **[NEW 2025]** A quantum complete-graph GNN reached simulator AUC 0.932 (Top) and 0.822 (JetNet). **On IBM hardware the AUC fell to about 0.5** — [EPJ Web Conf. (Oct 2025)](https://www.epj-conferences.org/10.1051/epjconf/202533701285) (via search summary).
- **[NEW 2025]** Tensor-network anomaly detection in the same latent space — [arXiv:2506.00102](https://arxiv.org/pdf/2506.00102).

#### Cybersecurity
- **[NEW 2025]** A quantum-kernel SVM on 4 attack categories had average **hardware** accuracy of 85% with small run-to-run variation, compared against classical and noiseless baselines — [AAAI Symposium (Nov 2025)](https://ojs.aaai.org/index.php/AAAI-SS/article/view/36903).
- **[NEW 2026]** A 16-qubit, 3-layer QCBM learns benign CICIDS2017 traffic. Its negative log-likelihood "quantum anomaly score" is fused with flow features in LightGBM — [CMC 2026](https://www.sciopen.com/article/10.32604/cmc.2026.075326) (snippet only, no accuracy seen).
- **[NEW 2025]** A wavelet-plus-fidelity-kernel QSVM reached 96.67% on BoT-IoT and 89.67% on IoT-23 — [arXiv:2512.01365](https://arxiv.org/pdf/2512.01365).

#### Energy
- **[NEW 2026]** QRC with a fixed reservoir and Elastic-Net readout on the Tetouan and Spain load datasets: exact, 512-shot and IBM fake-backend noise runs. 6-bit readout quantisation keeps accuracy and cuts readout memory by 81.2%. The abstract does not state the classical baselines — [arXiv:2606.12806](https://arxiv.org/abs/2606.12806).
- **[NEW 2026]** Distributed QRC on Greek regional load claims MAE reductions up to 78.8% versus classical reservoirs — [arXiv:2605.04991](https://www.alphaxiv.org/abs/2605.04991) (via search summary; baselines not checked).
- QLSTM for solar forecasting — [Frontiers in Physics 2024](https://arxiv.org/abs/2310.17032v3).

#### Genomics
- **[NEW 2026]** The only 2025–26 genomics QML result I found with real data is the single-cell RNA-seq experiment in Zhao et al. (fault-tolerant regime) — [arXiv:2604.07639](https://arxiv.org/abs/2604.07639).

### Inferences
- **Recurring patterns in industrial claims, which our project should explicitly avoid:**
  - baselines not matched in size or tuning (IonQ 2025's 3.14% is against an SVC with 296 support vectors);
  - tiny test sets (250 samples in the IonQ 2026 hardware study, where ±2% is about ±5 samples);
  - effects that exist only with noise (HSBC);
  - toy datasets (Quantinuum QDisCoCirc).
- **The HSBC case is a teachable baseline trap.** If noise helps, a classical noise-injection or resampling baseline must be in the comparison. Any project that sees "noisy beats noiseless" should add Gaussian or bit-flip noise injection to the classical features as a control.

### Gaps
- There is no public accuracy number for Hyundai/IonQ road-sign classification.
- The HSBC paper's qubit count (a commenter said 109; unverified) and its exact feature map were not confirmed.
- I found no credible QM9 / molecular-property QML benchmark with tuned classical baselines in these searches.
- I found no reliable 2025–26 genomics QML result on NISQ hardware.

---

## Q4. Public datasets that fit 8–24 qubits after reduction (size, access, licence)

### Takeaway
The best datasets for a browser build are those **bundled with scikit-learn** (no network access at all), or small files shipped with the project (≤2 MB each):
- Breast Cancer Wisconsin (569 × 30), Wine (178 × 13), Digits (1,797 × 8×8);
- a stratified subsample of the Kaggle/OpenML credit-card fraud data (492 frauds out of 284,807; PCA features V1–V28 already);
- PneumoniaMNIST or BreastMNIST (28×28 uint8);
- a year of ERCOT/PJM hourly load;
- the C-MAPSS FD001 training file (about 3.4 MB raw, so trim it).

EuroSAT, CICIDS2017, QM9 and the LHC Olympics data are GB-scale and must be **pre-featurised offline**. Don't rely on runtime downloads: only CORS-enabled GET requests work, and most dataset hosts are not CORS-enabled.

### Cited Findings

| Dataset | Size and shape | Access notes | Source |
|---|---|---|---|
| Breast Cancer Wisconsin (diagnostic) | 569 samples × 30 features, binary | **Bundled** in scikit-learn as `load_breast_cancer()`. My experiments below use it. | [scikit-learn toy datasets](https://scikit-learn.org/stable/datasets/toy_dataset.html) |
| Wine / Digits / Iris | 178 × 13; 1,797 × 64; 150 × 4 | Bundled in scikit-learn. Iris is tutorial-level. | [scikit-learn toy datasets](https://scikit-learn.org/stable/datasets/toy_dataset.html) |
| Credit-card fraud (ULB) | 284,807 transactions, 492 frauds (0.172%). V1–V28 are PCA components; Time, Amount, Class. Use AUPRC. | OpenML ID 1597. Licence is reported as DbCL 1.0 / ODbL / "Public" by different indexes. **Ship a subsample.** | [OpenML 1597](https://api.openml.org/d/1597); [ecosyste.ms](https://science.ecosyste.ms/projects/106531) |
| PneumoniaMNIST | 5,856 pediatric chest X-rays (4,708 / 524 / 624 split), 28×28 uint8 | Official distribution is Zenodo `.npz` (6 keys). About 4.6 MB raw pixels by my arithmetic, so subsample or PCA. | [MedMNIST v2 paper](https://arxiv.org/pdf/2110.14795); [TFDS](https://www.tensorflow.org/datasets/catalog/pneumonia_mnist) |
| BreastMNIST | 780 ultrasound images, 28×28, 70/10/20 split | About 0.6 MB raw. | [MedMNIST v2](https://arxiv.org/pdf/2110.14795) |
| EuroSAT | 27,000 Sentinel-2 patches, 64×64, 10 classes. RGB zip about 90 MB; 13-band MS about 2 GB. | Precompute features (e.g., band means or CNN embeddings, then PCA) offline. | [EuroSAT paper](https://arxiv.org/pdf/1709.00029); [TFDS](https://www.tensorflow.org/datasets/catalog/eurosat?hl=en) |
| NASA C-MAPSS turbofan (FD001) | 100 train + 100 test engines, 1 operating condition, 1 fault mode, 21 sensors. Train file about 3.4 MB (estimate). | A NASA Glenn page (Aug 2025) said downloads are "currently unavailable". Hugging Face mirrors exist. | [data.gov](https://catalog.data.gov/dataset/cmapss-jet-engine-simulated-data); [HF mirror](https://huggingface.co/datasets/SoyVitou/NASA-C-MAPSS-Turbofan-Engine) |
| LHC Olympics 2020 R&D | 1M QCD dijets + 100k W′→XY (3.5 TeV / 500 GeV / 100 GeV); h5 of shape (1.1M, 2101); about 2.8 GB (v1). High-level feature files were added Nov 2020. | Use high-level features or an autoencoder latent space offline. | [Zenodo R&D](https://zenodo.org/records/6466204); [LHCO paper](https://arxiv.org/pdf/2101.08320) |
| CICIDS2017 | Intrusion flows. Used by the 2026 QCBM-IDS paper. | GB-scale; subsample per attack class. | [CMC 2026](https://www.sciopen.com/article/10.32604/cmc.2026.075326) |
| SST-2 (SetFit trimmed) | IonQ used 512 training sentences and 9,101 test sentences | Embeddings must be computed offline (no torch in Pyodide). | [arXiv:2504.08732](https://arxiv.org/html/2504.08732) |
| Tetouan / Spain energy load | Used in the 2026 QRC load paper | Public. | [arXiv:2606.12806](https://arxiv.org/abs/2606.12806) |

- Pyodide lacks torch and TensorFlow but has xgboost and lightgbm, so strong tree baselines run in-browser — [Pyodide packages](https://pyodide.org/en/stable/usage/packages-in-pyodide.html).
- Qollab platform rules (from earlier notes):
  - network access is GET-only to CORS-enabled servers;
  - nothing persists between runs, so ship saved states as project files;
  - Python must open data files using **plain string-literal paths**.
  - Sources: [Qollab FAQ](https://qollab.xyz/programs/hackathon/how-it-works#faq); [Qollab runtime docs](https://qollab.xyz/learn/docs/runtime-environment).

### Inferences
- **Recommended pairing:** one bundled scikit-learn dataset (zero-risk demo) plus one "real-world" shipped file. Examples: a fraud subsample of 492 frauds + 4,508 non-frauds × 30 float32 columns ≈ 0.6 MB as `.npy`; or one year of hourly regional load, 8,760 rows (well under 1 MB CSV).
- MedMNIST at 28×28 needs PCA to 8–12 components. The physics of the images is then mostly destroyed, so expect RBF-SVM parity at best.

### Gaps
- I did not verify the CORS headers of the UCI, OpenML, Zenodo or ERCOT hosts. Assume they are blocked and ship files.
- I did not verify the exact sizes of the MedMNIST `.npz` files, the C-MAPSS zip, ERCOT/PJM files or QM9.
- The current licence of the Kaggle fraud dataset is unconfirmed (sources conflict).

---

## Q5. Honest benchmarking protocol, with my own diagnostics on a real dataset

### Takeaway
The protocol that survives scrutiny:
- **Nested cross-validation.** Every model, classical included, gets its hyperparameters tuned in an inner loop. For quantum kernels that means bandwidth and C; for RBF, γ and C.
- **Matched inputs.** Every model sees the same PCA features.
- **Strong baselines:** logistic regression, RBF-SVM, random forest, gradient boosting, a small MLP, and a separable (unentangled) quantum ablation.
- **Uncertainty:** multiple seeds, learning curves, and confidence intervals.
- **Diagnostics:** kernel concentration (off-diagonal variance against n), the kernel spectrum, geometric difference g_CQ against √N, and label-specific complexity s_K.
- **A shot and noise budget:** shots × circuits, plus an IonQ job-size check.

**My runs on the breast-cancer data reproduce the literature in miniature** (PCA to 4, 8 and 12 qubits):
- Quantum kernels reach parity with classical baselines; all models land at 95–98%.
- At the bandwidths that cross-validation selects, g_CQ ≈ 2–4, far below √N ≈ 24. Huang's test therefore predicts that classical models can match, and they do.
- The fidelity kernel's off-diagonal variance falls about 380× from 2 to 12 qubits at unit bandwidth, against about 10× for the PQK.

### Cited Findings

#### Protocol elements from the literature
- Use full grid search with 5-fold cross-validation for all models, and include separable ablations — [Bowles et al. 2024](https://arxiv.org/html/2403.07059v2).
- Use **nested** cross-validation, significance testing, learning curves, kernel spectra, seed variance and a variance decomposition — [Kakavand et al. 2026](https://arxiv.org/abs/2604.18837).
- Geometric difference and model complexity diagnostics — [Huang et al. 2021](https://arxiv.org/html/2011.01938v2).
- Bandwidth must be treated as a hyperparameter — [Shaydulin & Wild 2022](https://arxiv.org/abs/2111.05451); [Canatar et al. 2023](https://arxiv.org/abs/2206.06686).
- Check concentration and shot scaling — [Thanasilp et al. 2024](https://arxiv.org/abs/2208.11060v2); [Gentinetta et al. 2024](https://arxiv.org/abs/2203.00031).
- When noise "helps", add a classical noise-injection control — [Aaronson on HSBC](https://scottaaronson.blog/?p=9170).
- IonQ multi-circuit jobs allow ≤5,000 circuits, ≤150,000 gates in total, and a request body ≤10 MB. Multiple circuits go in one job with `backend.run([qc1, qc2, ...])` — [IonQ API v0.4](https://docs.ionq.com/api-reference/v0.4/jobs/create-job); [IonQ Qiskit docs](https://docs.ionq.com/sdks/qiskit/index).
- IonQ remote noise simulation is one simulation per shot, so run time grows with shots. Near the 29-qubit ceiling, runs may fail with `SimulationTimeout` or `TooLongPredictedExecutionTime` — [Qollab compute backends](https://qollab.xyz/learn/docs/compute-backends).
- Forte: 99.6% 2Q and 99.98% 1Q fidelity. The native gate is ZZ(θ) = exp(−iπθ Z⊗Z), so RZZ(φ) is one native gate with θ = φ/2π — [IonQ notes in `Qollab IonQ hackathon track/ionq_hardware_and_sdk.md`](https://docs.ionq.com/api-reference/v0.3/native-gates-api).

#### [Computed] Experiment A: quantum kernels against classical baselines on breast cancer (`scripts/qk_bc.py`)

Setup:
- **Data:** standardise all 30 features, PCA to n, then unit variance. The scaler and PCA were fit on all 569 samples (transductive), which affects every model equally.
- **Feature map:** IQP/ZZ-style, U(x) = [D(x)·H^⊗n]², with D(x) = exp(−i(Σ_i x_i Z_i + Σ_(i,i+1) x_i x_{i+1} Z_i Z_{i+1})). It uses a chain of ZZ terms, so 2(n−1) native ZZ gates per U(x).
- **Bandwidths** bw ∈ {0.1, 0.25, 0.5, 1}. PQK γ ∈ {0.1, 0.3, 1}.
- **Model selection:** inner 3-fold cross-validation chooses (bw, γ, C) for quantum kernels and (γ, C) for RBF. The outer loop is 5-fold.
- **Classical baselines** LR, RF, HistGB and MLP(32) use **defaults (untuned)**, which slightly favours the quantum side.

Outer 5-fold accuracy:

| n qubits | LogReg | RF | HistGB | MLP(32) | RBF-SVM (nested) | Fidelity QK (nested) | Projected QK (nested) |
|---|---|---|---|---|---|---|---|
| 4 | 0.961 | 0.951 | 0.944 | 0.963 | 0.960 | 0.960 | 0.960 |
| 8 | **0.981** | 0.953 | 0.963 | 0.970 | 0.961 | 0.970 | 0.968 |
| 12 | 0.970 | 0.951 | 0.968 | 0.972 | 0.967 | 0.972 | **0.977** |

- Each outer fold has about 114 samples, so 1 error ≈ 0.9 percentage points. **All differences of 2 points or less are within noise.**
- Gate cost per U(x): 6 ZZ (n=4), 14 (n=8), 22 (n=12). A fidelity kernel circuit costs twice that: 12, 28 and 44 ZZ, giving F ≈ 0.94, 0.87 and 0.80 at 0.5% error.
- Native NumPy run time for states plus kernels at 4 bandwidths, N = 569: 3.8 s (n=4), 6.8 s (n=8), 23 s (n=12).

**Geometric difference g(K^RBF‖K^Q)**, with K^RBF at γ = 1/n and √N = 23.9:

| n | bw | g fidelity (λ=0.01 / 0.1) | g PQK γ=0.3 (λ=0.01 / 0.1) | s_RBF | s_fid | s_PQK (λ=0.1, true labels) |
|---|---|---|---|---|---|---|
| 4 | 0.25 | 2.66 / 2.52 | 3.73 / 3.52 | 673 | 965 | 1010 |
| 4 | 1.0 | 28.1 / 10.7 | 26.4 / 10.3 | 673 | 2360 | 2933 |
| 8 | 0.25 | 2.55 / 2.35 | 4.14 / 3.85 | 557 | 666 | 781 |
| 8 | 1.0 | 16.1 / 6.3 | 18.2 / 8.2 | 557 | 485 | 1633 |
| 12 | 0.25 | 2.33 / 2.04 | 3.85 / 3.64 | 502 | 500 | 629 |
| 12 | 1.0 | 11.5 / 4.4 | 13.3 / 6.6 | 502 | 458 | 982 |

**Concentration** (bw = 1, **all-pairs** ZZ, 2 reps, 150 random samples):

| n | 2Q per U(x) | Fidelity off-diagonal mean | Fidelity off-diagonal variance | PQK (γ=1/n) variance |
|---|---|---|---|---|
| 2 | 2 | 0.40 | 6.2e-2 | 3.2e-2 |
| 4 | 12 | 0.12 | 1.3e-2 | 1.1e-2 |
| 6 | 30 | 0.051 | 2.5e-3 | 6.3e-3 |
| 8 | 56 | 0.025 | 5.8e-4 | 4.6e-3 |
| 10 | 90 | 0.018 | 2.6e-4 | 3.7e-3 |
| 12 | 132 | 0.013 | 1.6e-4 | 3.2e-3 |

**Shots and noise** (n = 8, fixed bw = 0.5, chain map, 28 ZZ per kernel circuit; global depolarising model K_noisy = F·K + (1−F)/2ⁿ; binomial shot sampling):

| | Exact | 100 shots | 1,000 shots |
|---|---|---|---|
| Noiseless | 0.881 | 0.854 | 0.874 |
| 0.5% 2Q (F = 0.87) | 0.881 | 0.868 | 0.879 |
| 1% 2Q (F = 0.75) | 0.888 | 0.866 | 0.889 |

- **The fixed bandwidth costs about 9 points** against the nested-cross-validation bandwidth (0.88 versus 0.97). That dwarfs the noise effects at this size.

### Inferences
- **Reading Experiment A:**
  - At cross-validation-selected bandwidths the quantum kernels are geometrically close to RBF (g ≈ 2–4 ≪ √N), and s_Q ≥ s_C for the true labels. Huang's flowchart predicts no advantage, and the accuracies agree.
  - Large g (10–28) appears only at bw = 1, where the fidelity kernel is near-diagonal (off-diagonal mean 0.02 at n = 8) and generalises worse. Large g is **necessary, not sufficient**.
  - A credible "measurable quantum step" can be exactly this diagnostic, run live on the judges' machine.
- **Shot cost formulas for the IonQ step:**
  - **Fidelity kernel:** one entry is a Bernoulli estimate with σ = √(k(1−k)/S). Inference needs N_test × N_SV circuits; training needs N(N−1)/2. For example, N = 100 needs 4,950 training circuits.
  - **PQK:** each Bloch component has σ = √((1−r²)/S). It needs 3·N circuits in total, with no pairwise circuits.
- **IonQ one-job feasibility** (my estimates, assuming about 2n native 1Q gates per rep plus basis changes):

  | Kernel | Batch | Circuits | Gates per circuit (approx.) | Total gates | Fits 150k? |
  |---|---|---|---|---|---|
  | PQK, n=8 | 100 test points × 3 bases | 300 | ~14 ZZ + ~45 1Q ≈ 60 | ~18k | Yes |
  | Fidelity, n=8 | 20 test × 60 support vectors | 1,200 | ~100 | ~120k | Just |
  | Fidelity, n=8 | 50 × 100 | 5,000 | ~100 | 500k | No |

- **Simple noise mitigation for fidelity kernels:** under global depolarising noise the diagonal circuits K(x,x) estimate F directly. Invert with K = (K_noisy − (1−F)/2ⁿ)/F, then project to PSD (as in the Hubregtsen et al. 2022 mitigation family).
- **Browser feasibility:**
  - Don't build kernels through per-sample Qiskit circuits on BasicSimulator. At n = 8–10 that is about 0.4–0.9 ms per gate in Pyodide, or about 50 ms per state.
  - Instead use a **vectorised NumPy simulator** over all samples at once: diagonal phases as one elementwise `exp`, and H^⊗n via reshape. For n ≤ 12 and N ≤ 600 this is seconds natively, roughly 3–10× slower in Pyodide (inference), so precompute and ship the kernels or states.
  - A 569×569 float64 kernel is 2.6 MB, over the 2 MB file limit. Ship 569 × 256 complex64 statevectors (1.2 MB) or a float16 kernel instead.
  - Per-gate timings are from my earlier Pyodide benchmark in `Quantum Unlocked theme deep dive/build_feasibility_and_stack.md`.

### Gaps
- My global-depolarising model is crude. I did not run the actual IonQ Forte noise model on these circuits, and real coherent errors and readout errors behave differently.
- Classical baselines other than RBF were untuned. Tuned XGBoost or LightGBM may do better.
- I did not compute confidence intervals or significance tests per model.
- The PCA was fit transductively.
- I did not test IonQ cloud simulator run time for a 300-circuit × 500-shot job (`SimulationTimeout` risk unknown).

---

## Q6. What an honest "measurable quantum step" can be in 48 h: 5 concrete designs

### Takeaway
The strongest honest designs make the quantum step a **measured quantity with a pre-registered success criterion**, such as:
- g_CQ against √N;
- shots-to-break-even against an equal-size classical reservoir;
- MMD and tail-risk error of a QCBM against copula baselines;
- accuracy of a quantum head against size-matched classical heads, plus a separable ablation;
- or the number of experiments with and without quantum memory.

**[Computed] Quantum reservoirs:** an 8-qubit restart-protocol reservoir with 48 native ZZ gates **beats an equal-size 36-node echo state network (ESN) only with exact expectation values**. With 1,000–100,000 shots per circuit it loses to the 36-node ESN and to quadratic NVAR, and a 300-node ESN beats it by more than 2 orders of magnitude. That is a clean, quantified, judge-proof finding.

Ranking for this hackathon:
1. **D1, Kernel-advantage auditor** on real medical or fraud data (safest, most rigorous).
2. **D3, QCBM tail-risk generator** (the IonQ step is one circuit, and it continues IonQ's own copula work).
3. **D4, Audit of the IonQ-style quantum classifier head.**
4. **D2, QRC load forecasting** with a shots-to-break-even analysis.
5. **D5, Quantum-memory learning advantage** (the only provable advantage, but the dataset is quantum, not a public classical one).

### Cited Findings

#### [Computed] Experiment B: restart-protocol QRC against classical reservoirs on Mackey-Glass (`scripts/qrc_mg.py`, `qrc_tune.py`, `qrc_shots.py`)

Setup:
- **Series:** τ = 17, sampled every 3 time units, normalised to [0, 1]. 1,700 points: 1,000 for training (ridge α chosen on the last 200) and about 690 for test. Metric is test NMSE.
- **QRC:** 8 qubits, window w = 6. Each layer applies RY(s·w_i·u_t) on every qubit, then 8 random ZZ couplings (all-to-all random pairs, native ZZ), then RX(h). That is 48 ZZ per circuit. Features are ⟨Z_i⟩ and ⟨Z_iZ_j⟩ (36 features). "+window" means the 6 raw inputs are appended (a skip connection).
- No mid-circuit measurement: one fresh circuit per time step.
- **Caveat:** the QRC settings (s, h, couplings) were picked from a 12-configuration grid by looking at **test** NMSE, which is optimistic for QRC. The ESN was **not tuned** (spectral radius 0.9, density 0.1), which is pessimistic for ESN.

| Model | Features | 1-step NMSE | 5-step NMSE |
|---|---|---|---|
| Linear AR(6) | 6 | 1.7e-2 | 3.7e-1 |
| NVAR quadratic (window 6) | 28 | 3.2e-3 | 2.5e-2 |
| NVAR cubic | 84 | **5.5e-5** | 6.1e-3 |
| ESN, 36 nodes (+window) | 42 | 1.2e-3 | 2.4e-3 |
| ESN, 300 nodes | 300 | **2.0e-6** | **8.7e-6** |
| QRC, naive (s=π, h=1, no skip) | 36 | 2.1e-1 | 4.9e-2 |
| QRC, tuned (s=π/4, h=0.3) + window, exact | 42 | 4.6e-4 | 7.6e-4 |
| … 100,000 shots/circuit | 42 | 2.6e-3 | 4.9e-3 |
| … 10,000 shots | 42 | 4.2e-3 | 1.1e-2 |
| … 1,000 shots | 42 | 8.3e-3 | 4.4e-2 |
| … 0.5% global depolarising (F = 0.79) + 1,000 shots | 42 | 9.4e-3 | 6.6e-2 |

- Shot noise was modelled as Gaussian with binomial variance (1−⟨O⟩²)/S, independent per feature. Depolarising noise was modelled as uniform shrinkage of expectation values by F.
- Native run time: 15–23 s for 1,695 circuits with per-sample NumPy loops. Vectorising over time steps would be much faster.

#### Literature anchors for the designs
- **IonQ copula QCBM:** up to 8 qubits on IonQ hardware, with Bell/GHZ-seeded ansatz — [arXiv:2109.06315](https://www.arxiv.org/pdf/2109.06315v1); [arXiv:2206.11937](https://arxiv.org/pdf/2206.11937v1).
- **MMD bandwidth determines QCBM trainability** — [Rudolph et al. 2024](https://arxiv.org/abs/2305.02881).
- **IonQ LLM-head numbers** (92.70% quantum; 91.44% NN head; 89.56% SVC; 89.06% LR; 512 training samples; 10–18 qubits; R = 4) — [arXiv:2504.08732](https://arxiv.org/html/2504.08732). Hardware 91.2% against 92.06% noiseless on 250 test samples — [TQI 2026](https://thequantuminsider.com/2026/07/21/ionq-quantumbasel-study-suggests-hybrid-ai-workloads-could-gain-energy-advantages-from-quantum-hardware-as-systems-scale/).
- **Quantum-memory advantage** (two-copy Bell measurements; 40 qubits and 1,300 gates on hardware) — [Huang et al., Science 2022](https://arxiv.org/abs/2112.00778). A noisy 30–40-qubit regime — [Danaci et al. 2026](https://arxiv.org/abs/2605.21346).
- **QRC for load forecasting**, with readout quantisation and IBM fake-backend noise — [arXiv:2606.12806](https://arxiv.org/abs/2606.12806).

### Inferences: the five designs

All gate counts are IonQ-native (ZZ(θ) = 1 two-qubit gate). F = 0.995^N2Q. Pyodide times are my extrapolation (×3–10 the native NumPy timings).

**D1. "Should we spend quantum budget on this dataset?": a kernel-advantage auditor** (healthcare and fraud)
- **Problem:** before an organisation invests in QML for a tabular task (tumour diagnosis, fraud), predict whether quantum kernels *can* help.
- **Data:** scikit-learn breast cancer (bundled), plus a fraud subsample (492 fraud + about 4.5k normal, ≤1 MB), with PneumoniaMNIST PCA as an optional third dataset.
- **Quantum:** fidelity and projected kernels at 8 and 12 qubits; chain IQP map with 2 reps.
  - 2Q per U(x): 14 (n=8) / 22 (n=12).
  - Fidelity circuit: 28 / 44 ZZ, F ≈ 0.87 / 0.80.
- **Measured quantum step:**
  1. g_CQ against √N for each dataset and bandwidth;
  2. off-diagonal variance against n (concentration);
  3. kernel eigenspectrum against RBF;
  4. nested-cross-validation accuracy (AUPRC for fraud) with CIs over 5 seeds;
  5. a positive control: Huang-style engineered labels (s_PQ small, s_C = g²·s_PQ) where the PQK must win, proving the auditor can detect advantage when it exists;
  6. **IonQ batch:** 100 test points × 3 bases = 300 PQK circuits, about 18k gates, 500 shots each (150k shots) in one multi-circuit job. Compare the hardware-noise kernel with exact via kernel alignment and the resulting accuracy.
- **Expected:** parity (±2 points) on real labels; g ≈ 2–4 ≪ √N; the PQK wins only on engineered labels. Under 0.5% 2Q error the PQK test accuracy should drop at most a few points (Experiment A suggests shots and noise cost ≤3 points at this size).
- **Browser:** precompute 4 bandwidths' states (native: 7 s at n = 8, 23 s at n = 12). Live recomputation of one n = 8 kernel takes seconds. Nested cross-validation over about 50 kernel/C combinations with SVC on N = 569 takes about 10–30 s in Pyodide (extrapolated).
- **Risk:** "negative" headline. Mitigate by framing it as a decision tool and showing the positive control.

**D2. Quantum reservoir for grid-load forecasting** (energy)
- **Problem:** day-ahead or hour-ahead load forecasting on a small edge device.
- **Data:** one ERCOT or PJM region, hourly for one year (8,760 points, <1 MB), or the Tetouan dataset.
- **Quantum:** the restart-protocol QRC above. 8 qubits, w = 6 (hours), 8 random all-to-all ZZ per layer = 48 ZZ (F ≈ 0.79). Features ⟨Z_i⟩, ⟨Z_iZ_j⟩ (36) plus the raw window plus calendar features.
- **Baselines:** seasonal naive (t − 24 h, t − 168 h), linear AR, NVAR (quadratic/cubic), ESN-36 and ESN-300 (tuned), and HistGB/LightGBM on lags.
- **Measured quantum step:** a **shots-to-break-even curve** (NMSE against shots on a log axis, against the ESN-36 and NVAR lines), plus a noise curve (F sweep) and one IonQ Forte-noise evaluation of a one-week test window (168 circuits × about 150–250 natives ≈ 25–42k gates; 1,000 shots each).
- **Expected (from Experiment B):**
  - exact QRC beats ESN-36 and quadratic NVAR at equal readout size;
  - at ≤10⁴ shots it loses to both;
  - ESN-300 and LightGBM win outright.
  - Honest claim: "the quantum reservoir is shot-noise-limited; break-even needs more than 10⁵ shots per time step, i.e. more than 10⁷ shots per day of forecasts".
- **Browser:** training features precomputed and shipped (8,760 × 36 float32 ≈ 1.3 MB). A live vectorised NumPy reservoir for a 168-step window takes about 1 s.

**D3. QCBM tail-risk scenario generator** (finance; continues IonQ's own copula line)
- **Problem:** generate joint stress scenarios for a 2–3 asset portfolio (e.g., equity, bond and gold ETFs; daily returns about 2005–2026, about 5k rows, <0.5 MB).
- **Method:** rank-transform to a copula (uniform marginals), discretise to 3 bits per asset (2 assets = 6 qubits, 64 cells; 3 assets = 9 qubits, 512 cells).
- **Ansatz:** Bell/GHZ-seeded "qopula" or hardware-efficient GPi2 rotations plus L layers of all-to-all ZZ:
  - 6 qubits: 15 ZZ per layer × 3 = 45 (F ≈ 0.80);
  - 9 qubits: 36 per layer × 2 = 72 (F ≈ 0.70).
- **Training:** in the browser on exact probabilities (64–512 entries), with multi-bandwidth MMD loss (Rudolph 2024) and SPSA or COBYLA. Run time is seconds.
- **Baselines:** empirical histogram (overfits), Gaussian copula, Student-t copula, KDE, scikit-learn `BernoulliRBM`, and a classical MPS Born machine (tensor-network baseline).
- **Metrics:** held-out-period MMD and KL; lower-tail dependence; 99% VaR/ES backtest (Kupiec test); and Gili generalisation metrics (fidelity/rate/coverage of unseen valid cells).
- **IonQ step:** one circuit, 5,000–10,000 shots. That fits "one job" perfectly; generation *is* sampling.
- **Expected:** QCBM roughly matches the t-copula on MMD. Hardware noise (about 20–30% depolarising weight) mixes in near-uniform mass, which **fattens tails**. Measure how much 0.5% error inflates VaR. This is a concrete, sign-meaningful noise-impact metric.
- **Note:** IonQ's Zhu et al. reported outperforming "equivalent classical generative learning" on up to 8 qubits. Independently reproducing that with a stronger t-copula baseline is novel.

**D4. Audit of a quantum classification head on frozen sentence embeddings** (customer-feedback triage; mirrors IonQ 2025–2026)
- **Data:** SST-2 SetFit split (512 training sentences, the IonQ protocol) plus a 872-sentence dev set.
- **Embeddings:** computed offline with `paraphrase-mpnet-base-v2` (768-d) and reduced by PCA to 64 (shipped as float16, about 0.2 MB). In-browser reduction to 8–12 dimensions.
- **Quantum head:** a data re-uploading VQC on 10 qubits, R = 3–4 re-uploads, CNOT-equivalent chain = 9 ZZ per block → 27–36 ZZ (F ≈ 0.87–0.84).
- **Training:** SPSA or Adam on vectorised NumPy statevectors (512 × 1,024 complex), or offline with shipped parameters.
- **Baselines:** LR, SVC and MLP on (a) the same 10-d features and (b) the full 768-d embedding. Add a **separable ablation** (remove the ZZ gates) and an **RFF surrogate** using the head's Fourier frequencies (Landman/Sweke).
- **IonQ step:** 100–250 test sentences, 1 circuit each (≈150 natives → 15–38k gates), 1,000 shots. ⟨Z⟩ has σ ≈ 0.03.
- **Expected:**
  - on 10-d PCA features, classical heads match the quantum head;
  - LR on the full 768-d embedding reaches about 89–90% (IonQ: 89.06%);
  - the quantum head is about 90–92% exact, minus 1–2 points with noise and shots.
  - Report that on 250 test samples a 95% CI is about ±3.5 points. This statistical point is missing from vendor coverage.
- **Risk:** close to IonQ's own work, so the novelty must come from the audit (matched baselines, ablations, CIs).

**D5. Learning from quantum experiments with quantum memory** (quantum-native data; the only provable advantage)
- **Problem framing:** characterise an unknown device or sensor state. For example, find which Pauli observables have large |⟨P⟩|, or estimate purity.
- **Protocols:**
  - **conventional:** single-copy random Pauli measurements (classical shadows) followed by classical learning;
  - **quantum-enhanced:** two copies measured in the Bell basis. Each shot carries information about all |⟨P⟩|² at once (Huang et al. 2022).
- **Size:** n = 4–6 system qubits → 8–12 qubits. State preparation ≤ 20 ZZ per copy plus n Bell-basis entanglers ≈ 30–46 ZZ (F ≈ 0.86–0.79).
- **Measured quantum step:** the number of experiments (shots) needed for 95% success against n, for both protocols, under exact simulation and IonQ noise. Theory predicts O(n) against Ω(2ⁿ) scaling; with noise, measure where the gap survives.
- **IonQ step:** one multi-circuit job with both protocols' circuits.
- **Risk:** it does not use a "public classical dataset", so the "real-world" link is quantum-device benchmarking. It may score lower on Impact even though it is the most scientifically solid.

**Cross-cutting recommendations**
- **Pre-register success criteria** in the README before running: for example, "the quantum model counts as competitive if within 1 SE of the best tuned classical model" and "advantage requires g ≫ 1 and s_Q < s_C".
- **Ship an "honesty panel":** baselines, ablations, CIs, the shot and gate budget, and an "Is this quantum advantage?" box citing Bowles 2024, Kakavand 2026 and Cerezo 2025.
- **Make the judge's Run fast:**
  - precompute training (statevectors, kernels, QRC features, QCBM parameters) and ship JSON/NPY ≤2 MB per file;
  - recompute live only one small case (n ≤ 8);
  - put IonQ execution behind an optional single `backend.run([...])` call from JS (async, per Qollab docs).

### Gaps
- None of the designs has been run on the actual IonQ Forte noise model or hardware. All noise figures are global-depolarising approximations.
- The D3 and D5 outcomes are expectations from the literature and theory, not computed here.
- D4 needs offline embedding generation (torch outside Pyodide). Check whether the Qollab rules accept precomputed embeddings as a "data file".
- IonQ cloud-simulator throughput (shots per second at 8–12 qubits) is unknown, so the shot budgets above may need to shrink to avoid `SimulationTimeout`.
