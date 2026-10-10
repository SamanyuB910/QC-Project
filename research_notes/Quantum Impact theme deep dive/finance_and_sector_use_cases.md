# Finance and sector-by-sector quantum use cases (knowledge base for a 48 h "Quantum Impact" build, Qollab × IonQ, Oct 9–11 2026)

Conventions used below:
- **[2025]**/**[2026]** marks results from those years.
- **[vendor]** = a company claim (press release or blog) with no independent check. **[peer-reviewed]** = journal paper. **[preprint]** = arXiv only. **[independent]** = critique or check by someone outside the team.
- **[measured]** = numbers I computed in this session with Qiskit 2.3.0 + qiskit-finance 0.4.1 + qiskit-algorithms 0.4.0 + qiskit-aer, on a local CPU. The scripts are in `research_notes/Quantum Impact theme deep dive/scripts/` (`qae_counts.py`, `qae_lut.py`, `cors_check.sh`).
- "CX" counts come from transpiling to {rz, sx, x, cx} at optimization_level=3 with no coupling map (all-to-all, like IonQ Forte). On IonQ one CX costs about one native ZZ/MS entangler, so a CX count approximates the native two-qubit (2Q) count.

---

## Q1. Finance: which algorithms can be honestly demonstrated at ≤20 qubits without feed-forward, and what does an honest "measurable step" look like?

### Takeaway
The finance primitive that fits the event's constraints (no dynamic circuits, one job, about 100 2Q gates) and does not overlap Qollab's existing finance projects is **amplitude estimation without phase estimation (QPE-free), using MLAE with a fixed schedule**. It can price an option or estimate a tail-risk probability (VaR/CVaR, credit loss) on 3–5-qubit registers. Several registers can sit side by side in one job.

The honest measurable step is a **sample-complexity comparison at equal oracle calls**: estimation error (RMSE) against the number of oracle calls, measured against classical Monte Carlo (MC) with the same budget, on (i) a noiseless simulation, (ii) the IonQ noise model, and (iii) a noise-aware MLAE fit. That is paired with a **fault-tolerant resource extrapolation** (Chakrabarti 2021; Stamatopoulos & Zeng 2024) which shows the real barrier is **logical clock speed (~45–50 MHz), not qubit count**.

Two warnings:
- qiskit-finance's stock European-call circuits are too deep for the budget: at 2 uncertainty qubits, A costs 45 CX and one Grover step 128 CX [measured].
- A hand-built "lookup-table" oracle fits: at 2 uncertainty qubits, Q⁴A costs 57 CX [measured]. But it tabulates the payoff classically. The demo therefore shows the estimator's scaling, **not** an end-to-end speedup. This is the same fine-print issue Herbert (2021) identified.

### Cited Findings

**A1. Amplitude estimation (QAE) for Monte Carlo pricing: core papers**
- **Stamatopoulos et al., "Option Pricing using Quantum Computers"** — Quantum 4, 291 (2020) [peer-reviewed]
  - Uses amplitude estimation, a quadratic speedup over classical MC.
  - Builds circuits for vanilla, multi-asset, and path-dependent (barrier) options and for portfolios of options.
  - Ran on **IBM Q Tokyo** with a simple error-mitigation scheme for noisy 2Q gates. The abstract page does not state the qubit count.
  - Source: [arXiv:1905.02666](https://arxiv.org/abs/1905.02666)
- **Chakrabarti et al. (Goldman Sachs, IBM, UMD), "A Threshold for Quantum Advantage in Derivative Pricing"** — Quantum 5, 463 (2021) [peer-reviewed]
  - Benchmarks are an autocallable and a TARF.
  - Introduces a "re-parameterization" method that pairs pre-trained variational circuits with fault-tolerant execution.
  - **Published estimate: ~8k logical qubits and T-depth 54 million. Advantage requires running this program in about one second.**
  - The earlier arXiv v2 said 7.5k logical qubits, T-depth 46M, and a 10 MHz logical clock. Cite the published numbers.
  - Sources: [Quantum journal](https://quantum-journal.org/papers/q-2021-06-01-463/); [arXiv:2012.03819](https://arxiv.org/abs/2012.03819v2); version discrepancy noted by [PostQuantum](https://postquantum.com/quantum-utility-map/quantum-computing-finance-wall-street/)
- **Stamatopoulos & Zeng, "Derivative Pricing using Quantum Signal Processing"** — Quantum (2024; arXiv July 2023) [peer-reviewed]
  - Loads payoffs directly into amplitudes with QSP and avoids quantum arithmetic.
  - About **16× fewer T-gates** and **~4× fewer logical qubits** than the previous state of the art (autocallable), and a logical clock requirement about **5× lower**.
  - Threshold: **4.7k logical qubits, 10⁹ T-gates at a 45 MHz rate**.
  - Source: [arXiv:2307.14310](https://arxiv.org/abs/2307.14310v2)
- **Stamatopoulos, Mazzola, Woerner, Zeng, "Towards Quantum Advantage in Financial Market Risk using Quantum Gradient Algorithms"** — Quantum (July 2022) [peer-reviewed]
  - Quantum gradient methods for the Greeks cut the required logical clock rate from about **50 MHz to about 7 MHz**.
  - A secondary summary says the paper cites feasible logical clock rates of **~10 kHz** (secondhand, unverified).
  - Sources: [arXiv:2111.12509](https://arxiv.org/abs/2111.12509v1); [PostQuantum summary](https://postquantum.com/quantum-utility-map/quantum-computing-finance-wall-street/)
- **Herman et al. (JPMorgan, UChicago, Argonne, others), "Quantum computing for finance"** — Nature Reviews Physics 5, 450–465 (Aug 2023) [peer-reviewed review]
  - Quantum MC integration and gradient estimation "can provide quadratic speedup", but "more work is required to reduce the amount of quantum resources for early fault-tolerant feasibility".
  - Sources: [UDSpace record](https://udspace.udel.edu/handle/19716/34417); [arXiv:2201.02773](https://arxiv.org/pdf/2201.02773v3)
- **Quadratic speedups need fault tolerance and fast logical clocks.** Error-correction overheads swamp Grover-type speedups on early fault-tolerant machines.
  - Sources: [Babbush et al., PRX Quantum 2, 010103 (2021)](https://arxiv.org/abs/2011.04149); [Hoefler, Häner, Troyer, CACM 2023](https://arxiv.org/abs/2307.00523) (both already in the earlier notes, `algorithms_and_complexity.md`)

**A2. QPE-free amplitude estimation that runs without feed-forward**
- **MLAE (Suzuki et al. 2020).**
  - Runs Q^m A|0⟩ for a fixed schedule of m and fits a maximum-likelihood estimate.
  - Needs no QPE and no controlled-Q.
  - Is fully non-adaptive, so every circuit is known in advance and the whole schedule fits in one job.
  - Source: [arXiv:1904.10246](https://arxiv.org/abs/1904.10246)
- **Noise-aware MLAE (Tanaka et al. 2021).** Puts a depolarizing decay into the likelihood.
  - Source: [arXiv:2006.16223](https://arxiv.org/abs/2006.16223)
- **IQAE (Grinko, Gacon, Zoufal, Woerner 2021).** Provable accuracy, but the next k is chosen adaptively between circuits, so it needs several jobs.
  - Source: [arXiv:1912.05559](https://arxiv.org/abs/1912.05559)
- **Power-law / low-depth AE (Giurgica-Tiron et al., Quantum 6, 745, 2022).** A dial that trades circuit depth for query count.
  - Source: [arXiv:2012.03348](https://arxiv.org/abs/2012.03348)
- **The one IonQ-hardware finance-flavoured QAE experiment: "Low depth amplitude estimation on a trapped ion quantum computer"** — Goldman Sachs, IonQ, QC Ware, Stanford, Paris; arXiv Sept 2021; Phys. Rev. Research 4, 033034 (July 2022) [peer-reviewed]
  - Compared MLE- and CRT-based low-depth AE on an IonQ machine. The test quantity was a dot-product-style amplitude from random 4-dimensional unit vectors.
  - **MLE reached a mean additive error of about 10⁻² with circuits of more than 90 2Q gates and depth 60.**
  - CRT was less robust to noise.
  - Baseline: plain sampling of the oracle.
  - Sources: [arXiv:2109.09685](https://arxiv.org/pdf/2109.09685); [INSPIRE record](https://inspirehep.net/literature/2161562)

**A3. The state-loading problem**
- **Grover–Rudolph** loading works for efficiently integrable distributions.
  - Source: [Grover & Rudolph 2002, arXiv:quant-ph/0208112](https://arxiv.org/abs/quant-ph/0208112)
- **Herbert (2021) proves there is no quantum speedup** when quantum MC estimates the mean (and other moments) of analytically defined log-concave distributions loaded with Grover–Rudolph.
  - Source: Phys. Rev. E 103, 063302, [arXiv:2101.02240](https://arxiv.org/abs/2101.02240)
- **qGANs (Zoufal, Lucchi, Woerner 2019)** learn an approximate loading circuit from data. They are the standard workaround in Qiskit finance tutorials.
  - Source: [arXiv:1904.00043](https://arxiv.org/abs/1904.00043)
- **IonQ copula ("qopula") work:**
  - **Fidelity CAT + IonQ** (arXiv Sept 2021; Phys. Rev. Research, Oct 2022) [peer-reviewed]:
    - Maps any copula to a maximally entangled state.
    - Trained a qGAN and a quantum circuit Born machine on **two-variable historical stock data**, up to **8 qubits on IonQ hardware**.
    - Reported noise resilience and **20–1000× fewer training iterations** than equivalent classical models.
    - Source: [arXiv:2109.06315](https://arxiv.org/pdf/2109.06315)
  - **GE Research + IonQ** (June 2022) [preprint + vendor]:
    - Quantum copula models with **up to 4 variables (four stock indexes)** on IonQ hardware.
    - Training efficacy fell as models scaled; an annealing-inspired training strategy fixed this.
    - Some configurations were "comparable or better" than classical models for risk aggregation.
    - Sources: [arXiv:2206.11937](https://arxiv.org/pdf/2206.11937); [IonQ IR](https://investors.ionq.com/news/news-details/2022/IonQ-and-GE-Research-Demonstrate-High-Potential-of-Quantum-Computing-for-Risk-Aggregation/default.aspx)

**A4. Credit risk, VaR and CVaR**
- **Egger, García Gutiérrez, Cahué Mestre, Woerner (IBM), "Credit Risk Analysis using Quantum Computers"** [preprint verified; journal venue not verified]
  - Estimates the **economic capital requirement (VaR minus expected loss)** with a quadratic speedup over MC.
  - Includes estimates of total qubits, circuit depth, and fault-tolerant runtime.
  - Source: [arXiv:1907.03044](https://www.arxiv.org/pdf/1907.03044)
- **Follow-up, "A More General Quantum Credit Risk Analysis Framework."** Adds multiple systemic risk factors and non-integer loss-given-default, at the cost of deeper and wider circuits. Tested in simulation and on IBM QPUs.
  - Source: [IBM Research](https://researchweb.draco.res.ibm.com/publications/a-more-general-quantum-credit-risk-analysis-framework)
- **Woerner & Egger, "Quantum risk analysis"** is the foundational VaR/CVaR-via-QAE paper.
  - Source: [arXiv:1806.06893](https://arxiv.org/abs/1806.06893)
- **qiskit-finance 0.4.1 contents:**
  - Circuit library: `GaussianConditionalIndependenceModel`, `LogNormalDistribution`, `NormalDistribution`, `UniformDistribution`, `EuropeanCallPricingObjective`, `EuropeanCallDeltaObjective`, `FixedIncomePricingObjective`.
  - Applications: `EuropeanCallPricing`, `EuropeanCallDelta`, `FixedIncomePricing`, `EstimationApplication`, `PortfolioOptimization`, `PortfolioDiversification`.
  - Data providers: `YahooDataProvider`, `WikipediaDataProvider`, `DataOnDemandProvider` (NASDAQ), `ExchangeDataProvider`, `RandomDataProvider`.
  - Source: [qiskit-finance API docs](https://qiskit-community.github.io/qiskit-finance/apidocs/qiskit_finance.data_providers.html)
  - Qiskit credit-risk tutorial: [qiskit.org tutorial 09](https://qiskit.org/ecosystem/finance/tutorials/09_credit_risk_analysis.html)

**A5. My gate counts and noisy MLAE** [measured]

These counts decide what fits in ~100 2Q gates. Script: `scripts/qae_counts.py`, `scripts/qae_lut.py`.

- **qiskit-finance `EuropeanCallPricing`** (LogNormal loader, comparator plus piecewise-linear payoff; S=2, σ=0.4, r=5%, T=40/365, K=1.896):

  | uncertainty qubits n | total qubits | A (CX) | one Grover step Q (CX) | Q¹A | Q²A | Q⁴A |
  |---|---|---|---|---|---|---|
  | 2 | 5 | 45 | 128 | 173 | 301 | 557 |
  | 3 | 7 | 92 | 310 | 400 | 708 | 1324 |
  | 4 | 9 | 139 | 532 | 669 | 1199 | 2259 |

  - The loader itself is cheap (1, 4 and 11 CX). The comparator and payoff arithmetic dominate.
  - **Under a ~100-2Q budget, only m=0 (no amplification) fits**, and from n=3 not even that.
- **qiskit-finance credit-risk expected-loss A operator** (GCI model with n_z=2, WeightedAdder, LinearAmplitudeFunction):
  - K=2 obligors: 8 qubits, **61 CX**
  - K=3: 12 qubits, 275 CX
  - K=4: 13 qubits, 343 CX
  - The GCI loader alone is 9/13/17 CX.
  - So noisy credit-risk QAE is feasible only for K=2 at m=0. m≥1 needs a noiseless simulation.
- **Hand-built lookup-table oracle:** A = StatePreparation(√p) on n qubits, plus a uniformly controlled RY on one objective qubit encoding the normalized payoff f(x).

  | n | qubits | A | Q | Q¹A | Q²A | Q³A | Q⁴A |
  |---|---|---|---|---|---|---|---|
  | 2 | 3 | 5 | 15 | 18 | 31 | 44 | 57 |
  | 3 | 4 | 12 | 38 | 48 | 84 | 120 | 156 |
  | 4 | 5 | 27 | 90 | 115 | 203 | 291 | 379 |

  - n=2 supports m up to 4–6, and n=3 supports m up to 2, inside 100 CX.
- **MLAE on the n=2 lookup-table oracle** (true a=0.1967; schedule m=[0,1,2]; 1,000 shots per circuit; 20 repetitions; generic depolarizing noise with p₂ per CX and p₁=p₂/10, *not* the IonQ noise model):

  | p₂ | naive MLAE RMSE | noise-aware MLAE RMSE |
  |---|---|---|
  | 0 | 0.0022 | 0.0026 |
  | 0.5% | 0.0063 | 0.0034 |
  | 1% | 0.0115 | 0.0030 |
  | 2% | 0.0167 | 0.0044 |

  - Classical MC with the same 9,000 oracle-call-equivalent samples has a theoretical RMSE of √(a(1−a)/9000) = **0.0042**.
  - **Reading:** noiseless MLAE beats MC by about 1.9×. This matches the Fisher-information ratio Σ(2m+1)²/Σ(2m+1) = 35/9 ≈ 3.9 in variance.
  - With noise, naive MLAE becomes biased and loses to MC once p₂ ≥ 0.5%.
  - Noise-aware MLAE recovers roughly MC-level accuracy. It does **not** beat MC at these noise levels.
  - With 20 repetitions, these RMSEs are uncertain by roughly ±15–20%.

**A6. Portfolio optimization: 2025–2026 hardware results** (the area that overlaps Qollab's existing projects)
- **IonQ + Kipu Quantum** [2026] [vendor blog + preprint]
  - Problem: cardinality-constrained Markowitz QUBO, **K=125 of 250 S&P 500 assets**.
  - Solver: Kipu's non-variational **BF-DCQO**.
  - Pipeline: Random Matrix Theory denoising, Louvain clustering, recursive partitioning to the qubit cap, repair to exactly K, and swap local search.
  - Hardware: **Forte (36 qubits)** and a **64-qubit barium development system** "similar to the forthcoming Tempo".
  - Reference optimum: Gurobi.
  - **The blog gives no numeric optimality gaps.** It claims 64-qubit decomposition is "systematically" better than 36-qubit.
  - Blog dated 2026-03-23. Sources: [IonQ blog](https://www.ionq.com/blog/quantum-computing-meets-wall-street-running-real-portfolio-optimization-on-trapped-ion-hardware); [arXiv:2602.23976](https://arxiv.org/abs/2602.23976); [TQI 2026-03-24](https://thequantuminsider.com/2026/03/24/study-finds-more-qubits-yield-better-financial-optimization-outcomes/)
- **IonQ Italia CEO Marco Pistoia's blog** (2026-05-12) [vendor]
  - Claims a hybrid BF-DCQO workflow on a "100-physical-qubit system" is "better than any classical solver" and "production-ready".
  - Gives **no baseline, runtime or objective values**.
  - Source: [IonQ blog](https://www.ionq.com/blog/from-wall-street-hypothesis-to-nyse-production-the-real-world-arrival-ofquantum-finance)
- **JPMorgan + AWS + Quantinuum + 55 North, qReduMIS** [2026] [preprint]
  - Portfolio diversification posed as Maximum Independent Set.
  - Hardware: **Quantinuum Helios (98 qubits)**, using up to **78 qubits and >1,000 2Q gates**, with up to 225 assets.
  - Data: DAX, FTSE 100, S&P 100 and Nikkei 225.
  - Success probability 95% (Nikkei 225) and 40% (S&P 100); approximation ratio ≥0.96; ≤5 QPU calls.
  - Time-to-solution scaling exponent about 3.2× better than standalone QAOA.
  - **No practical advantage claimed.** Not compared to the strongest classical optimizers at scale.
  - Sources: [TQI 2026-07-06](https://thequantuminsider.com/2026/07/06/hybrid-quantum-algorithm-improves-portfolio-optimization-on-trapped-ion-quantum-computer/); arXiv:2607.01037
- **Goldman Sachs + AWS, Dalzell et al., "End-to-end resource analysis for quantum interior point methods and portfolio optimization"** — PRX Quantum 4, 040325 (Nov 2023) [peer-reviewed]
  - Large constant prefactors, poorly conditioned linear systems and costly tomography mean "fundamental improvements to the QIPM are required" for practical advantage.
  - Source: [arXiv:2211.12489](https://arxiv.org/pdf/2211.12489)
- **IQM + DATEV** finished a Markowitz project on a **20-qubit** system in January 2025 [vendor].
  - Source: [IQM press release](https://meetiqm.com/press-releases/iqm-and-datev-advance-quantum-solutions-for-portfolio-optimisation)
- **Unverified secondary claim:** JPMorgan ran a 512-asset rebalance on a 433-qubit IBM system with an 18% higher Sharpe ratio. No primary source was found; treat it as unreliable.
  - Source: noted in the search summary of [vfuturemedia](https://vfuturemedia.com/?p=1542)

**A7. ML-flavoured finance claims and their critiques**
- **HSBC + IBM bond trading** [2025] [preprint + vendor; contested]
  - Paper: "Enhanced fill probability estimates in institutional algorithmic bond trading using statistical learning algorithms with quantum computers", announced 2025-09-25.
  - Data: **1.7 million RFQs over 294 trading days (Sept 2023–Oct 2024)**, mainly European corporate bonds.
  - Method: **216 input features become 327 quantum features** via projected quantum feature maps on **IBM Heron**. The quantum step runs offline, and classical models (logistic regression, gradient boosting, random forest, neural nets) use the features, evaluated by AUC in rolling time-ordered backtests.
  - Headline: **"up to 34%" better fill-probability prediction**.
  - The authors report better results when hardware noise is *not* mitigated.
  - Sources: [arXiv:2509.17715](https://arxiv.org/pdf/2509.17715); [TQI deep dive](https://thequantuminsider.com/2025/09/28/bond-trading-quantum-bond-trading-a-deeper-look-at-hsbc-and-ibms-bond-trading-study/); [HSBC release](https://www.hsbc.com/news-and-views/news/media-releases/2025/hsbc-demonstrates-worlds-first-known-quantum-enabled-algorithmic-trading-with-ibm)
  - **Critiques [independent]:**
    - Scott Aaronson: "more red flags than a People's Liberation Army parade". Experts dispute that noise helped. — [fi-desk/Global Trading](https://www.fi-desk.com/quantum-computing-breakthrough-has-more-red-flags-than-a-peoples-liberation-army-parade/)
    - No live trading. The authors themselves did not claim advantage. — [Kapronasia](https://kapronasia.com/insight/blogs/capital-markets-research/a-look-at-hsbcs-quantum-enabled-algorithmic-trading-announcement)
    - The classical baselines are not clearly specified. — [Sovereign Magazine](https://www.sovereignmagazine.com/article/hsbc-and-ibm-show-quantum-can-help-price-bond-quotes-34-better-predictions-in-rfq-trials)
    - PostQuantum reports the encoding used 109 Heron qubits (secondary, unverified). — [PostQuantum](https://postquantum.com/quantum-research/hsbc-ibm-quantum-advantage/)
- **JPMorgan certified randomness** — Nature 640, 343–348, published 2025-03-26 [peer-reviewed] [2025]
  - Team: JPMorganChase, Quantinuum, Argonne, ORNL, UT Austin.
  - Hardware: **56-qubit Quantinuum H2**, accessed remotely.
  - Protocol: Aaronson's 2018 random-circuit-sampling protocol.
  - Output: **71,313 bits of certified entropy**.
  - Classical verification: **1.1 × 10¹⁸ FLOPS** sustained across DOE supercomputers.
  - Aaronson calls it a "first step" toward cryptographic use.
  - Sources: [JPMorganChase blog](https://www.jpmorganchase.com/about/technology/blog/certified-randomness1); [ORNL/OLCF](https://www.olcf.ornl.gov/2025/05/05/quantum-computing-experiment-realizes-verifiably-random-number/)
- **Crédit Agricole CIB + Pasqal + Multiverse** (announced 2023-01-26) [vendor]
  - Predicted counterparty rating downgrades 6–15 months ahead.
  - A **50-qubit** processor was "as accurate as the production system". A 300-qubit machine was *projected* to beat it.
  - The derivatives-valuation project used **quantum-inspired** classical methods.
  - Sources: [Crédit Agricole pressroom](https://pressroom.credit-agricole.com/news/quantum-computing-two-real-world-experiments-conducted-by-credit-agricole-cib-in-partnership-with-pasqal-and-multiverse-computing-produce-conclusive-results-in-finance-cddc-94727.html); [TQI 2023-01-26](https://thequantuminsider.com/2023/01/26/researchers-say-studies-step-toward-quantum-computers-for-real-world-finance/)
- **Fraud detection (2025):**
  - Quantum-assisted RBM on **145M transactions** from fintech Stone. Claims superior figures of merit even on noisy annealers [preprint, Dec 2025]. — [arXiv:2512.17660](https://arxiv.org/abs/2512.17660v1)
  - FD4QC (IBM AML dataset): **classical tree models won**. Random forest reached ~97.3% accuracy; the best quantum model (QSVM) had ~77% precision with lower recall. — [emergentmind summary of arXiv:2507.19402](https://www.emergentmind.com/papers/2507.19402) (ID-to-FD4QC mapping taken from search results, not opened)
  - QSVM on BankSim (594,643 simulated transactions) was "competitive" with GPU models, but slow on NISQ devices and emulators. — [ISC 2025 abstract](https://isc.app.swapcard.com/widget/event/isc-high-performance-2025/planning/UGxhbm5pbmdfMjU4NDUyMA==)
  - A 2024 review notes QSVM fraud results used "drastically reduced" datasets. — [arXiv:2405.10119](https://arxiv.org/pdf/2405.10119)

**A8. Overlap with existing Qollab projects**
- **Quantum Systemic Oracle:** a portfolio-optimization circuit on IonQ feeding an on-chain risk score. No dataset stated.
- **Quantum Regime Radar:** quantum kernels for market-regime detection against a GARCH baseline.
- **Quantum Market Game:** a quantum prisoner's dilemma / entanglement primer for classrooms.
- Sources: `research_notes/Qollab IonQ hackathon track/qollab_ionq_track.md` and `research_notes/Quantum Impact theme deep dive/past_application_winners.md`, citing the [Qollab Spring 2026 cohort](https://qollab.xyz/explore/spring-2026-cohort)
- **Finbubu** (CQhack25 winner) already did "QAOA portfolio optimisation plus QML forecasting on Yahoo Finance / Alpha Vantage data". — [Devpost](https://devpost.com/software/finbubu)

### Inferences
- **Honest-at-≤20-qubit finance menu, ranked:**
  1. **MLAE (fixed schedule) for a tail probability** P(L > ℓ) or a European/digital payoff, with a lookup-table oracle on 2–3 uncertainty qubits. Several thresholds or m-values run as parallel 3–4-qubit registers in **one job** (for example 7 registers × 4 qubits = 28 qubits). This yields a VaR/CVaR curve from a single submission.
  2. **qiskit-finance GCI credit-risk model** with K=2 obligors (8 qubits, 61 CX): A only (m=0) on the noise model, m≥1 on statevector.
  3. **qGAN/QCBM loading** of a real two-asset joint distribution (copula), as in IonQ/Fidelity and IonQ/GE.
  4. Portfolio QUBO with QAOA or BF-DCQO-style circuits. **Avoid** this one: it overlaps Systemic Oracle and Finbubu, and IonQ/Kipu and JPM/Quantinuum already ran it at 36–78 qubits.
- **What the "measurable step" should be.** Not wall-clock and not "accuracy versus an untuned baseline". Use:
  - (a) log-log RMSE versus oracle calls, with slope about −1 for noiseless MLAE against −½ for MC;
  - (b) the knee where noise bends the slope back, and how far noise-aware MLAE pushes the knee out;
  - (c) bias of naive versus noise-aware estimates on the IonQ Forte noise model;
  - (d) resource extrapolation: "to beat MC for a TARF/autocallable you need ~4.7k–8k logical qubits at 45–50 MHz logical T-rate". The bottleneck is speed. IonQ's own 2030 target of 80k logical qubits (see `ionq_hardware_and_sdk.md`) would cover the qubit count, but trapped-ion logical clocks are expected to be orders of magnitude slower than 45 MHz. This is my inference from the cited ~10 kHz figure, which is itself secondhand.
- **State the lookup-table caveat on the slide:** "f(x) and p(x) are tabulated classically, so this demonstrates the estimator, not a speedup (cf. Herbert 2021)". Judges who know QAE will look for it.
- qiskit-finance's stock circuits are useful as a **reference oracle for statevector runs**. For noisy runs, write a custom UCRY payoff oracle.
- Under "one job", MLAE beats IQAE because IQAE is adaptive. The earlier notes reach the same conclusion.

### Gaps
- I did not verify the journal venue of Egger et al. (credit risk), the qubit count of the Stamatopoulos 2020 IBM Q Tokyo experiment, or the qGAN hardware details. The Zoufal 2019, Grover–Rudolph 2002 and Woerner–Egger 2019 links are cited from known arXiv IDs without re-reading them this session.
- Not found: any Moody's quantum result, Goldman Sachs results after 2023, or any QAE/MC result on IonQ hardware after 2021.
- I did not run the actual IonQ Forte noise model (it is in the Qollab runtime, not local). The depolarizing sweep is a stand-in.
- The IonQ/Kipu portfolio preprint's numeric optimality gaps were not retrieved. The blog omits them.
- No independent replication of the HSBC 34% result exists. I did not read the full paper's baseline section.

---

## Q2. Sector by sector: use cases, evidence, data, baselines, and the single most credible 48-hour project

### Takeaway
Across sectors, the credible 48-hour pattern is the same: a **small combinatorial or estimation core (10–24 qubits) carved out of a real public dataset**, solved by QAOA or MLAE, with a hybrid pipeline in which classical decomposition and repair do the heavy lifting. That core is compared against **exact enumeration or MILP plus a good heuristic**. This is how IonQ/ORNL (unit commitment), IonQ/Airbus (loading), IonQ/DESY (gate assignment) and IonQ/Kipu (portfolio, folding) structure their own published work.

Fault-tolerant-only problems (FeMoco, CFD/climate PDEs, RSA/ECC) are honest to present as **resource-estimate dashboards**, not as builds.

### Cited Findings

#### B1. Energy and power grids
- **Unit commitment (UC), IonQ + ORNL** [2025] [preprint + vendor]
  - Paper: "A New Hybrid Quantum-Classical Algorithm for Solving the Unit Commitment Problem", Aboumrad, Marthi, Debnath, Roetteler, Epifanovsky.
  - Method: a variational quantum algorithm produces candidate commitment vectors, then a Benders-type classical heuristic with SLSQP economic dispatch sets power levels.
  - Test systems: 3, 10 and 26 units; convergence checked on **IonQ Forte**.
  - The July 2025 release states **26 generators × 24 periods** on a **36-qubit Forte Enterprise**, under DOE's **GRID-Q** program led by ORNL.
  - IonQ projects "100 to 200 high-fidelity qubits … could address grid-scale UC" [vendor].
  - ORNL frames it as a **feasibility** demonstration.
  - Sources: [arXiv:2505.00145](https://arxiv.org/html/2505.00145v1); [IonQ IR 2025-07-31](https://investors.ionq.com/news/news-details/2025/IonQ-Partners-with-Oak-Ridge-National-Laboratory-Demonstrating-Quantum-Power-Grid-Optimization-Advancements/default.aspx); [TQI 2025-06-08](https://thequantuminsider.com/2025/06/08/ionq-oak-ridge-researchers-use-quantum-classical-algorithm-to-solve-power-grid-problem/)
- **EPB Chattanooga** [2025–2026]
  - A $22M IonQ deal created a commercial quantum hub around a **Forte Enterprise** system, with commissioning planned for early 2026. Partners also include ORNL and an NVIDIA DGX.
  - **No operational grid results had been published** at the time of the source articles.
  - Eight graduate fellows are funded by a $4M federal grant.
  - Sources: [Sovereign Magazine](https://www.sovereignmagazine.com/article/epb-first-us-utility-commercial-quantum-computing); [NewsChannel 9](https://newschannel9.com/news/local/chattanoogas-new-quantum-computer-is-online-epb-says-businesses-can-use-it-next-month-ionq-quantum-computing-utc-vanderbilt-quantum-center-nist); [Smart Cities World](https://www.smartcitiesworld.net/smart-grids/using-quantum-technology-to-optimise-power-grids-11950)
- **Other grid work** [2025–2026]:
  - Deep QAOA on simplified UC with DC power flow (IEEE 57-bus), **simulation only**. QAOA beat simulated annealing (SA) more often (by up to 15%) than SA beat QAOA (by up to 5%).
  - Annealing-based power flow and OPF: AQPF/AQOPF (Kaseb et al., May 2025).
  - QAOA power-system islanding run on **IBM ibm_marrakesh** (REGRID-QAOA, PACE-QAOA; up to the IEEE 30-bus case). Hardware lost at most 5.6% against the noise-model simulation.
  - Q-CTRL vendor case study: a **69-bus** network on hardware.
  - Sources: [arXiv:2505.16444](https://arxiv.org/abs/2505.16444?context=cs) and [arXiv:2505.15978](https://arxiv.org/abs/2505.15978) (IDs from search results; which ID is Adler's deep-QAOA paper and which is Kaseb's AQPF paper was not verified); [REGRID-QAOA arXiv:2606.15083](https://arxiv.org/pdf/2606.15083); [PACE-QAOA arXiv:2608.02789](https://arxiv.org/pdf/2608.02789); [Q-CTRL case study](https://q-ctrl.com/case-study/optimizing-power-grid-performance-with-hybrid-quantum-workflows)
- **EV charging placement:** existing hardware work uses D-Wave annealing (Nov 2024). A Grover-based intercity placement paper is theory only. I found **no gate-model hardware result**.
  - Sources: [arXiv:2411.06684](https://arxiv.org/pdf/2411.06684); [arXiv:2410.16231](https://arxiv.org/html/2410.16231v1)
- **Data, all browser-fetchable** (see Q3):
  - pglib-opf and MATPOWER case files on GitHub
  - EIA hourly RTO demand API (needs a free API key; DEMO_KEY works)
  - UK Carbon Intensity API
  - Open-Meteo and NASA POWER for wind and solar resource
  - Sources: [pglib-opf](https://api.github.com/repos/power-grid-lib/pglib-opf); my CORS tests in Q3

#### B2. Healthcare and life sciences
- **Protein folding, IonQ + Kipu** [2025] [vendor]
  - "Largest known" 3D lattice protein-folding problem on hardware: **up to 12 amino acids**.
  - Dense QUBO/HUBO instances (spin glass, MAX-4-SAT) on **up to 36 qubits**, all solved optimally, with BF-DCQO.
  - Released 2025-06-19. No independent replication.
  - Source: [TQI 2025-06-20](https://thequantuminsider.com/2025/06/20/ionq-and-kipu-quantum-break-new-performance-records-for-protein-folding-and-optimization-problems/)
- **Radiotherapy beam-angle optimization (QC-BAO)** [2025] [preprint; journal status unclear]
  - Shinde et al. (KU Medical Center, SJTU). Quantum handles the binary beam selection; classical iterative convex relaxation and ADMM handle spot intensities. Applied to proton therapy.
  - Better conformity index and lower organ-at-risk dose than clinical angles and two heuristics.
  - Baselines are clinical plans and heuristics, **not a strong MILP**.
  - TNO has a fluence-map QUBO benchmarked against simulated annealing.
  - Sources: [arXiv:2504.07844](https://arxiv.org/pdf/2504.07844); [PMC record](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12036446/); [TNO use case](https://qal.tno.nl/use-cases/quantum-radiotherapy/)
- **Genomics** [2026]
  - Oxford and the Wellcome Sanger Institute (with Cambridge, Melbourne and Kyiv Academic University) encoded the **~1,700-base hepatitis D genome into 117 qubits** of a 156-qubit **IBM Heron**. This is a data-loading milestone, not an analysis.
  - The team is in **Wellcome Leap Q4Bio Phase 3** with $2M.
  - Sources: [Sanger news](https://www.sanger.ac.uk/news_item/genome-loaded-onto-a-quantum-computer-in-world-first/); [TQI 2026-04-16](https://thequantuminsider.com/2026/04/16/scientists-load-genome-onto-ibm-quantum-computer/)
- **Wellcome Leap Q4Bio outcome** [2026]
  - **Algorithmiq + IBM + Cleveland Clinic won the $2M prize.** The project modelled photosensitizer excited states for photodynamic therapy on 100 qubits at depth 1,000–10,000.
  - The **$5M grand prize for provable quantum advantage went unawarded**.
  - 5 of the 6 finalists used IBM hardware.
  - Sources: [QCR](https://quantumcomputingreport.com/algorithmiq-wins-2-million-q4bio-prize-for-quantum-driven-cancer-therapy-simulation/); [TQI 2026-03-27](https://thequantuminsider.com/2026/03/27/wellcome-leap-q4bio-finalists-present-quantum-approaches/)
- **Clinical trials**
  - A perspective paper covers trial simulation, **site selection** and cohort identification via quantum optimization and QML, and judges hybrid methods the only viable path for now.
  - A Jan 2026 preprint claims a hybrid stratification benchmark on real trial data with ">100×" efficiency and "up to fivefold" higher statistical significance [preprint, unverified].
  - Sources: [arXiv:2404.13113](https://arxiv.org/html/2404.13113v1); [TQI 2024-10-05](https://thequantuminsider.com/2024/10/05/researchers-say-quantum-machine-learning-quantum-optimization-could-enhance-the-design-and-efficiency-of-clinical-trials/); [arXiv:2601.11413](https://arxiv.org/html/2601.11413v1)
- **Other IonQ partner context:**
  - AstraZeneca/AWS/NVIDIA Suzuki–Miyaura reaction: >20× time-to-solution, measured against prior IonQ-stack runs.
  - Ansys blood pump: "up to 12%", with the full-scale run simulated.
  - Source: `research_notes/Qollab IonQ hackathon track/ionq_hardware_and_sdk.md` Q8, citing [IonQ IR 2025-06-09](https://investors.ionq.com/news/news-details/2025/IonQ-Speeds-Quantum-Accelerated-Drug-Development-Application-With-AstraZeneca-AWS-and-NVIDIA/default.aspx) and [TQI 2025-03-20](https://thequantuminsider.com/2025/03/20/ionqs-devices-boost-ansys-simulations-achieving-up-to-12-faster-processing-over-classical-computers/)
  - IonQ's 2026 Investor Day named **oncology and personalized medicine** as priorities. — [TQI 2026-09-08](https://thequantuminsider.com/2026/09/08/ionq-uses-investor-day-to-detail-superion-roadmap-skywater-strategy-and-quantum-security-plans/)
- **Data, browser-fetchable:**
  - ClinicalTrials.gov API v2 (trial sites and enrollment)
  - openFDA
  - UniProt, EBI Proteins, PDB files, PubChem, NCBI E-utilities
  - cBioPortal (cancer genomics)
  - PhysioNet is **not** CORS-enabled (Q3).

#### B3. Climate and sustainability
- **Carbon-capture materials: Deloitte Quantum Climate Challenge 2023**
  - Topic: MOFs for direct air capture.
  - Winner **EcoQult** (three employees of the Belgian start-up qBee), from 118 registrations across 33 countries. Prize €5,000 plus IBM, Quantistry and AWS access.
  - Method: ion–gas dissociation energies, with **VQE local corrections on top of a classical bulk method** (MOF-74). They argue a small-scale potential advantage [preprint].
  - Another Deloitte edition addressed **flood forecasting** (year not established).
  - Sources: [TQI 2023-05-08](https://thequantuminsider.com/2023/05/08/quantum-climate-challenge-team-ecoqult-wins-the-deloittes-quantum-climate-challenge/); [arXiv:2309.05465](https://arxiv.org/pdf/2309.05465); [Deloitte page](https://www.deloitte.com/de/de/issues/sustainability-climate/deloitte-quantum-climate-challenge.html); [Digital Engineering 24/7](https://www.digitalengineering247.com/article/next-gen-quantum-computing-takes-on-environment/education-and-training)
- **XPRIZE Phasecraft–Materials team** (a finalist) targets clean-energy materials for batteries, solar, hydrogen and **carbon capture**. — [TQI](https://thequantuminsider.com/?p=2383234)
- **Weather, climate and CFD: the caveats** [independent]
  - **Penuel et al. (Zapata AI + L3Harris)** — [arXiv:2406.06323](https://arxiv.org/pdf/2406.06323)
    - v1/v2 (2024): drag on a sphere needs **logical qubits × T gates ≈ 10²²–10²⁸**, so useful incompressible CFD is "unlikely" without major algorithmic advances.
    - **v3 (Dec 2025): range 10²¹–10³⁹.** A Carleman-linearized lattice-Boltzmann approach scales about **Re^2.68 versus classical Re^3**, so there is **no exponential advantage** for explicit time-evolution of nonlinear ODEs and PDEs.
  - A Sept 2025 counter-claim of exponential speedup estimates **8.71M physical qubits and 42.6 days** for a Navier–Stokes case [preprint, unvalidated]. — [arXiv:2509.08807](https://arxiv.org/html/2509.08807v1)
  - Airbus acknowledges boundary-layer CFD needs fault tolerance. — [Digital Catapult](https://www.digicatapult.org.uk/case-studies/study/using-quantum-computing-to-design-fuel-efficient-airbus-products)
  - The generic fine print on HHL-style linear solvers (state preparation, condition number, readout) is in [Aaronson, "Read the fine print", Nature Physics 11, 291 (2015)](https://www.nature.com/articles/nphys3272).
- **Data, browser-fetchable:**
  - Open-Meteo forecast and archive
  - NASA POWER (solar and agro-climate)
  - NOAA NCEI daily summaries
  - UK Carbon Intensity
  - Electricity Maps (needs a key; returns 401 without one, but the CORS header is present)

#### B4. Telecommunications
- **NTT DOCOMO + D-Wave** (2024-08-20) [vendor]
  - Optimized tracking areas using handset-movement data: **15% fewer paging signals at peak**, about **1.2× more connectable terminals**, and **40 s versus 27 h** for traditional solvers.
  - Source: [TQI](https://thequantuminsider.com/2024/08/23/ntt-docomo-and-d-wave-improve-mobile-network-performance-by-15-with-quantum-optimization-technology/)
- **SoftBank** (2025-07-29) [vendor]
  - An **Ising machine** (which may be classical or quantum-inspired) optimized carrier-aggregation link patterns among 10 base stations: 45 pairs, 3.5 × 10¹³ patterns.
  - About **+10% downlink speed** and **up to +50% capacity** in a Tokyo proof of concept.
  - Sources: [SoftBank press release](https://www.softbank.jp/en/corp/news/press/sbkk/2025/20250729_01/); [RCR Wireless](https://www.rcrwireless.com/20250729/5g/softbank-quantum-5g-ran)
- **Vodafone + ORCA:** solved a Steiner-tree network-design problem on a **PT-2 photonic** device; no speedup or size published [vendor]. — [ORCA](https://orcacomputing.com/vodafone-partners-with-orca-computing-to-model-future-networks-in-minutes-using-quantum-technology/)
- **Ericsson** (Jan 2025): an exploratory review naming antenna tilt and PAPR minimization as candidates. — [Ericsson Technology Review](https://www.ericsson.com/en/reports-and-papers/ericsson-technology-review/articles/quantum-computing-in-telecom-networks)
- **Annealing for baseband processing** would need roughly **≥1 million qubits** before beating CMOS in some scenarios. — [arXiv:2109.01465](https://arxiv.org/pdf/2109.01465)
- **Industry count:** 75 telco quantum deployments by 29 operators through June 2025. — [RCR Wireless](https://www.rcrwireless.com/?p=431279)
- **Data:**
  - OpenStreetMap via the Overpass API is CORS-enabled (cell masts, `communication:mobile_phone`).
  - SNDlib network instances are **not** CORS-enabled (ship them).
  - OpenCellID was not tested.

#### B5. Cybersecurity
- **Mosca inequality.** If x (how long data must stay secret) + y (migration time) > z (time to a cryptographically relevant quantum computer, CRQC), the data is already at risk ("harvest now, decrypt later").
  - Source: [Mosca, IACR ePrint 2015/1075](https://eprint.iacr.org/2015/1075)
- **Global Risk Institute / evolutionQ Quantum Threat Timeline Report 2025** (Mosca & Piani) [expert survey]
  - Probability of a CRQC **within 10 years: 28–49%** (the highest in the report's history); **within 15 years: 51–70%**.
  - **26 experts**, down from 32 in 2024 and 37 in 2023.
  - 2024 report: about 19–34% within 10 years.
  - One source dates the 2025 report to 2026-03-09.
  - Sources: [GRI 2025 report](https://globalriskinstitute.org/publication/quantum-threat-timeline-report-2025b/); [PostQuantum summary](https://postquantum.com/security-pqc/quantum-threat-timeline-report-2025/)
- **Resource-estimate trajectory for breaking public-key crypto:**
  - **Gidney (May 2025): RSA-2048 with <1M noisy qubits in <1 week.** Assumes 0.1% gate error, 1 µs surface-code cycle, square grid. The 2019 estimate was 20M qubits and 8 h. — [arXiv:2505.15917](https://arxiv.org/abs/2505.15917v1)
  - **Iceberg Quantum (Feb 2026):** <100k physical qubits using QLDPC codes ("Pinnacle"). Validated in simulation only; Gidney flags decoder reaction-time assumptions.
  - **Google Quantum AI (2026-03-31), with Boneh and Drake:** **ECDLP-256 on <500k physical qubits**, about **70–90M Toffoli**, about **9 minutes** after precomputation. Circuits withheld; a zero-knowledge proof was published instead.
  - Source for the last two plus the trajectory summary (~1B in 2012, ~20M in 2019, <1M in 2025, <100k in 2026): [TQI 2026-03-31](https://thequantuminsider.com/2026/03/31/q-day-just-got-closer-three-papers-in-three-months-are-rewriting-the-quantum-threat-timeline/)
  - **IonQ (Investor Day 2026-09-08):** secp256k1 needs **19,397 physical / 1,457 logical** qubits [vendor]. — via `ionq_hardware_and_sdk.md`, citing [TQI 2026-09-08](https://thequantuminsider.com/2026/09/08/ionq-uses-investor-day-to-detail-superion-roadmap-skywater-strategy-and-quantum-security-plans/)
- **Policy deadlines**
  - **NIST IR 8547** (initial public draft 2024-11-12): 112-bit quantum-vulnerable public-key algorithms (e.g., RSA-2048) **deprecated after 2030 and disallowed after 2035**. Still draft as of mid-2026.
  - **NSA CNSA 2.0:** new national-security systems quantum-safe by **Jan 2027**.
  - 18-nation European statement: high-risk use cases migrated by 2030.
  - **Google's internal PQC deadline: 2029.**
  - Sources: [Encryption Consulting](https://www.encryptionconsulting.com/nist-ir-8547-2030-2035-action-plan/); [TQI 2026-05-08](https://thequantuminsider.com/2026/05/08/post-quantum-migration-timelines-government-industry-impact/); [TQI 2026-03-31](https://thequantuminsider.com/2026/03/31/q-day-just-got-closer-three-papers-in-three-months-are-rewriting-the-quantum-threat-timeline/)
- **Quantum randomness:** see the JPMorgan certified-randomness entry in A7 (71,313 bits; 1.1 EFLOPS verification).
- **Data:** the NVD CVE API 2.0 is CORS-enabled.

#### B6. Aerospace and automotive
- **Airbus aircraft loading on IonQ** [2025] [preprint]
  - Multi-angle QAOA built for fewer 2Q gates; optimal solutions for **12–28-qubit** instances on Aria and Forte.
  - A 12-qubit Aria run (4 containers × 3 slots, 1,000 shots, COBYLA) gave about **70% probability of the optimum**.
  - Source: `ionq_hardware_and_sdk.md` Q8, citing [arXiv:2504.01567](https://arxiv.org/abs/2504.01567)
- **IonQ + DESY flight-gate assignment** (2024-03-15) [vendor + preprints]
  - Ran on IonQ Aria with a **logarithmic-linear encoding**: **9 flights × 4 gates, up to 36 variables**.
  - IonQ's interpretation that this points to outperforming classical methods is a vendor reading of a small demonstration.
  - A 2023 VQE study on Aria found "good solutions with high probability".
  - Sources: [IonQ news](https://ionq.com/news/ionq-and-desy-research-highlights-quantums-potential-benefits-for-airport); [arXiv:2309.09686](https://arxiv.org/abs/2309.09686)
  - Earlier: DLR used D-Wave 2000Q on real data from a mid-sized German airport. — [arXiv:1811.09465](https://arxiv.org/pdf/1811.09465)
- **Binary paint shop.** This is **Volkswagen's** work, not BMW's.
  - **Streif et al. (VW Data:Lab), PRA 104 (2021):** constant-depth QAOA beats all known heuristics on average as n→∞. Small instances ran on a **trapped-ion QPU via Amazon Braket**. Depth-7 QAOA reached a swap ratio of 0.393 against Recursive Greedy's 0.4. — [arXiv:2011.03403](https://arxiv.org/pdf/2011.03403)
  - **2025 follow-up:** XQAOA at depth 1 averages **0.357** on 2⁷–2¹² cars, against a *conjectured* 0.361 for Recursive Star Greedy. RQAOA degrades at scale. — [arXiv:2509.15294](https://arxiv.org/html/2509.15294v1)
- **VW Lisbon, Web Summit, Nov 4–8 2019** [vendor]
  - **9 MAN buses** (Carris), 26 stops on 4 routes. Classical ML predicted traffic; D-Wave 2000Q distributed the vehicles.
  - **No measured travel-time results published.** TechCrunch said D-Wave "played a small part". A D-Wave case study says 23 stops on 3 lines (a discrepancy).
  - Sources: [Automotive World](https://www.automotiveworld.com/news-releases/volkswagen-optimizes-traffic-flow-with-quantum-computers/); [TQI 2019-12-19](https://thequantuminsider.com/2019/12/19/volkswagen-traffic-jam-eradication-project-hits-the-road/)
- **Airbus + BMW Quantum Mobility Quest** (winners announced 2024-12-10)
  - More than 100 submissions; five categories with €30k each.
  - Confirmed winners include Univ. Hamburg "Quantum Leaps" (quantum solvers), Quandela (autonomy QML) and 4ColorResearch (logistics).
  - Sources: [TQI](https://thequantuminsider.com/2024/12/10/airbus-and-bmw-harness-quantum-computing-for-future-mobility/); [Airbus](https://www.airbus.com/en/innovation/digital-transformation/quantum-technologies/airbus-quantum-computing-challenge)
- **Other IonQ mobility partners**
  - **Hyundai:** a hybrid QCNN trained on 8 qubits with 16-qubit inference, for road-sign classification (2022–2023). — via `ionq_hardware_and_sdk.md`
  - **Einride:** electric/autonomous freight orchestration; 15 candidate use cases; a pilot for e-freight dispatch reported May 2026 [vendor, no numbers]. — [IonQ news](https://ionq.com/news/einride-and-ionq-partnership-uses-quantum-computing-to-optimize-the-logistics-of-electric-and-autonomous-freight); [Dealroom](https://app.dealroom.co/news/feed/ionq-pilots-quantum-optimisation-for-electric-freight-dispatch-with-einride)
  - **US Air Force Research Lab:** a $54.5M, four-year contract (announced 2024-09-25/27) for **networking and deployable systems hardware**, not optimization applications. — [IonQ IR](https://investors.ionq.com/news/news-details/2024/IonQ-Announces-Largest-2024-U.S.-Quantum-Contract-Award-of-54.5M-with-United-States-Air-Force-Research-Lab/default.aspx)
  - **AFRL's own quantum-algorithms group** studies scheduling optimization (annealing versus gate-model). — [AFRL fact sheet](https://www.afrl.af.mil/About-Us/Fact-Sheets/Fact-Sheet-Display/Article/3017916/afrlritq-quantum-algorithms)
- **Data:**
  - OpenSky's API returns `Access-Control-Allow-Origin: https://opensky-network.org` only, so it is **not** browser-usable from Qollab (ship it).
  - OSM Overpass is fine.

#### B7. Agriculture
- **Nitrogen fixation (FeMoco)**
  - THC benchmark: **2,196 logical qubits, 6.7 × 10⁹ Toffoli**. Physical: about 2.8–4M qubits for about 3.7–4.1 days at 10⁻³ error and a 1 µs cycle, per the Qualtran reproduction. — [arXiv:2011.03494](https://arxiv.org/pdf/2011.03494); [Qualtran docs](https://qualtran.readthedocs.io/en/latest/surface_code/thc_compilation.html)
  - **May 2026 preprint: about 89k superconducting qubits, under a month**, 1.3 mega-qubit-hours. — [arXiv:2605.30455](https://arxiv.org/pdf/2605.30455)
  - A 76-orbital QPE variant with <500 logical qubits (PennyLane, Apr 2026). — [PennyLane demo](https://pennylane.ai/demos/tutorial_re_for_qubitizedQPE)
- **Crop planning**
  - I found **no peer-reviewed quantum crop-rotation paper**.
  - Closest: a D-Wave DQM crop-rotation repository (README claim of 82.8% land use), a QAOA irrigation-scheduling QUBO (July 2026 preprint), and QYieldOpt (simulated QAOA for irrigation valves).
  - Bayer Crop Science used **Fujitsu's quantum-inspired Digital Annealer** (2022).
  - The classical ILP baseline (Benini et al., 2023) converts directly to a QUBO.
  - Sources: [arXiv:2607.13374](https://arxiv.org/abs/2607.13374); [Springer QYieldOpt](https://link.springer.com/article/10.1186/s13677-025-00769-2); [Fujitsu/Bayer](https://global.fujitsu/en-CA/customer-stories/cs-bayer-crop-science-20220805)
- **OQI nutrition use case:** quantum-inspired optimization to grow more nutritious food locally on less land (EPFL, GAIN, NITheCS; Phase 2 of OQI incubation). — [GESDA Quantum For All Progress Report 2024](https://www.gesda.global/wp-content/uploads/2025/07/GESDA-Quantum-For-All-Progress-Report-2024_Final.pdf)
- **Data:**
  - NASA POWER (agro-climate) and GBIF are CORS-enabled.
  - The FAOSTAT API returned HTTP 521 (down) during testing.
  - USDA NASS QuickStats needs a key and showed no CORS header on a 401 response.

#### B8. Public sector and social good
- **GESDA/CERN Open Quantum Institute (OQI)**
  - 2022 white paper (2022-10-10). 2024 edition with 10 new use cases from 22 countries.
  - **2025 Use Case White Paper (2025-10-14):** maps the full SDG portfolio plus 7 new use cases.
  - **18 SDG use cases in development as of March 2025.**
  - Examples: last-mile food delivery, plant genomics, antibiotic discovery, urban water-leak detection, nutrition.
  - Sources: [TQI 2024-10-11](https://thequantuminsider.com/2024/10/11/open-quantum-institute-details-quantum-computing-solutions-for-global-challenges-from-food-security-to-climate/); [CERN repository](https://repository.cern/records/8hxhj-za327); [2022 white paper](https://open-quantum-institute.web.cern.ch/wp-content/uploads/2023/10/GESDA_OQI_Use-Cases_WhitePaper2022.pdf)
- **XPRIZE Quantum Applications**
  - $5M, 3 years, launched March 2024. **7 finalists named 2025-12-10.**
  - **Phase II** requires benchmarking against state-of-the-art classical methods and **detailed fault-tolerant resource estimates**. Winners due **spring 2027**. A wildcard round ran Jan 14–Mar 4 2026.
  - Finalists:
    - Calbee Quantum / Caltech (Chan): semiconductor optoelectronics
    - Gibbs Samplers / Rényi Institute (Gilyén)
    - Phasecraft: clean-energy materials
    - Q4Proteins / ETH (Reiher)
    - Rice: new quantum linear-system algorithm
    - QuMIT / MIT (Schmidhuber): hypergraph community detection for protein–protein interactions
    - Xanadu: organic solar cells
  - Sources: [TQI](https://thequantuminsider.com/?p=2383234); [XPRIZE](https://go.xprize.org/news/2026-finalist-teams-book-xprize-quantum-applications); [UMD QuICS](https://quics.umd.edu/about/news/quics-researchers-advance-final-phase-5-million-xprize-quantum-applications-competition)
- **Disaster response, food and vaccine distribution:** I found no hardware quantum results specific to these. All the data sources below are CORS-enabled (Q3):
  - USGS earthquake GeoJSON
  - OpenFEMA
  - HDX (Humanitarian Data Exchange)
  - OSM Overpass

#### B9. Summary table: the single most credible 48-hour project per sector

Every row uses ≤24 qubits, browser-fetchable or shipped (≤2 MB) data, a strong classical baseline, and a measurable quantum step.

| Sector | 48 h project (scope) | Quantum method (qubits, 2Q) | Public data | Classical baseline | Measurable step | Closest real-world precedent |
|---|---|---|---|---|---|---|
| **Finance** | **Tail-risk (VaR/CVaR) estimator for a real 2–3-asset portfolio** via batched MLAE. Several thresholds and m-values as parallel 3–4-qubit registers in one job. | MLAE, lookup-table oracle (n=2: Q⁴A = 57 CX; n=3: Q²A = 84 CX) [measured] | Crypto OHLC (Coinbase/Kraken/Binance.vision/CoinGecko, CORS ✔); equities shipped (Stooq/Yahoo CSV, no CORS) | Classical MC at equal oracle calls; exact discretized value; historical VaR | RMSE vs oracle calls (slope), noise knee, naive vs noise-aware bias; FT resource extrapolation | Stamatopoulos 2020; Egger 2021; Woerner & Egger 2019; IonQ/Goldman low-depth AE 2022 |
| Energy | **Hybrid unit commitment**: QAOA proposes on/off vectors for 10 units × 1–2 h (10–20 qubits); classical convex dispatch scores each | QAOA (multi-angle) + classical economic dispatch (Benders-style, as in ORNL/IonQ) | IEEE RTS-GMLC / pglib-opf generator data (GitHub, CORS ✔); EIA hourly load (CORS ✔) | MILP (HiGHS via `scipy.optimize.milp`) + brute force at ≤20 bits | Optimality gap, P(optimal in top-k samples), candidates needed vs random/greedy | arXiv:2505.00145 (26 gen × 24 h on Forte) |
| Healthcare | **Clinical-trial site selection**: choose k of 12–20 candidate sites to maximize expected enrollment and demographic coverage under budget | QUBO + QAOA with XY / Dicke-state mixer (cardinality-preserving) | ClinicalTrials.gov v2 sites/enrollment (CORS ✔); Census/CDC demographics (ship) | Exact enumeration (C(20,5)=15,504), greedy, MILP | Approximation ratio and P(opt) vs depth; noise-model degradation | arXiv:2404.13113 perspective; IonQ oncology priority |
| Climate | **Renewable-site portfolio**: pick k of N wind/solar sites maximizing capacity factor and minimizing output correlation (Markowitz-style on weather) | Same QUBO/QAOA as portfolio, on real weather-driven covariance | Open-Meteo archive + NASA POWER (CORS ✔) | Exact enumeration; mean-variance QP + rounding | Gap to exact; diversification benefit (variance reduction) | Markowitz QUBO literature; OQI SDG framing |
| Telecom | **Channel/frequency assignment** on a real cell-site interference graph (10–12 sites, 4 channels, log-encoded, 20–24 qubits) | QAOA for Max-k-Cut / graph colouring | OSM Overpass cell masts (CORS ✔) | DSatur greedy, exact ILP | Conflicts vs ILP optimum; P(zero-conflict) vs depth | SoftBank CA (Ising machine); DOCOMO paging |
| Cybersecurity | **Mosca-inequality HNDL risk estimator**: P(x + y > z) over the GRI expert distributions, estimated with the same MLAE engine; plus an RSA/ECC resource-trajectory chart | MLAE (tail probability) | GRI 2025 survey numbers (shipped); NVD CVE API (CORS ✔) | Classical MC; analytic convolution | Same RMSE-vs-calls step; policy dates (2027/2029/2030/2035) | Mosca 2015; GRI 2025; Gidney 2025; Google 2026 |
| Aerospace/auto | **Aircraft cargo loading** (reproduce the 12-qubit Airbus/IonQ instance, then scale to 20–24 qubits) or **gate assignment** with log encoding | Multi-angle QAOA (low 2Q count) | Airbus 2019 challenge problem parameters (public); flight schedules shipped (OpenSky has no CORS for third parties) | MILP; greedy loading | P(opt) vs qubits; 2Q count vs standard QAOA | arXiv:2504.01567; IonQ/DESY 2024 |
| Agriculture | **Crop allocation under rotation and water constraints**: 4 plots × 4 crops one-hot (16 qubits) | QUBO + QAOA (XY mixer per plot) | NASA POWER (CORS ✔); FAOSTAT yields (ship) | ILP (Benini 2023-style), greedy | Gap to ILP; constraint-violation rate | Bayer/Fujitsu (quantum-inspired); OQI nutrition |
| Public sector | **Post-earthquake depot/shelter siting** (max-coverage / p-median on 12–20 candidate sites) for a real USGS event | QUBO + QAOA (Dicke-state init) | USGS GeoJSON, OSM Overpass, OpenFEMA, HDX (all CORS ✔) | Greedy max-coverage (1−1/e guarantee); exact MILP | Coverage gap vs MILP; P(opt) | OQI last-mile food delivery; XPRIZE impact framing |

### Inferences
- **Across sectors, the most credible build for IonQ judges** is either:
  - **finance MLAE risk estimation**, which no Qollab project covers, uses one job, and has a clean MC baseline and published fault-tolerant thresholds; or
  - **energy hybrid unit commitment**, which mirrors IonQ's own ORNL/GRID-Q paper, uses public IEEE/EIA data, and has a clear MILP baseline.
- Both line up with IonQ's 2025–2026 narrative (finance with Kipu/JPM alumni; grid with ORNL/EPB).
- Optimization projects should state explicitly that classical MILP solves these sizes exactly in milliseconds. The quantum metric is **sample quality per shot** and **2Q-gate efficiency**, not beating MILP.
- Fault-tolerant-only sectors (FeMoco, CFD/climate PDEs, RSA/ECC) suit a "time-to-advantage" panel inside any project rather than being the project.
- BMW is often credited with paint-shop optimization, but the QAOA paint-shop papers are Volkswagen's. BMW's public quantum work in this period is the Airbus–BMW challenge.

### Gaps
- No credible quantum results were found for **MRI reconstruction**, **hospital/nurse scheduling**, **vaccine distribution**, **airline crew scheduling** or **5G/6G beamforming** in 2022–2026. These were searched lightly or not at all.
- I did not verify that `scipy.optimize.milp` (HiGHS) is included in the Pyodide scipy build. Test it on day 1.
- The radiotherapy datasets (CORT, TROTS) were not checked for size or CORS.
- The full XPRIZE 2026 wildcard finalist list (PDF) was not readable.
- I found no IonQ–Einride numbers, no 2025–2026 AFRL application results, and no EPB grid results.
- Hyperion Research sector valuations were not retrieved.

---

## Q3. Which data sources can a browser fetch (CORS) and which must be shipped?

### Takeaway
**I tested this directly** on 2026-10-09 with curl: a simple GET carrying an `Origin` header, from a US IP. A Pyodide `pyfetch` can only read the response when `Access-Control-Allow-Origin` (ACAO) is `*` or echoes the page origin.

- **Mainstream equity and macro sources fail:** Yahoo Finance, Stooq, FRED, World Bank API, SEC EDGAR, Nasdaq API, UCI, OR-Library and Ken French all send no ACAO header.
- **These work:**
  - Alpha Vantage (key needed; the `demo` key only serves IBM)
  - Twelve Data (key)
  - Crypto exchanges: Coinbase, Kraken, Binance.vision, CoinGecko
  - ECB, Frankfurter, US Treasury FiscalData
  - Science, health and geo APIs: EIA, Open-Meteo, NASA POWER, NOAA, USGS, OpenFEMA, HDX, NVD, ClinicalTrials.gov, openFDA, UniProt, PDB files, PubChem, NCBI, OSM Overpass, OpenML
  - **raw.githubusercontent.com and cdn.jsdelivr.net** (both ACAO `*`). The simplest pattern is to commit a ≤2 MB CSV to GitHub and fetch it through jsDelivr.

### Cited Findings
All rows below are [measured] with `scripts/cors_check.sh`.

**Finance**

| Endpoint | HTTP | ACAO | Verdict |
|---|---|---|---|
| Yahoo `query1/query2.finance.yahoo.com/v8/finance/chart` | 200 | none | **Ship** |
| Stooq CSV `stooq.com/q/d/l/?s=aapl.us&i=d` | 200 | none | **Ship** |
| FRED `fredgraph.csv` | timeout | none | **Ship** |
| FRED API `api.stlouisfed.org` | 400 (bad key) | none | **Ship** |
| Alpha Vantage `query?function=TIME_SERIES_DAILY` | 200 | `*` | **Fetchable**. The `demo` key returned IBM data dated 2026-10-09; AAPL with `demo` returned "claim your free API key". |
| Twelve Data | 200 | `*` | Fetchable (key) |
| Financial Modeling Prep | 401 | `*` | Fetchable with key |
| Nasdaq Data Link `data.nasdaq.com` | 200 | none | Ship |
| `api.nasdaq.com` | 200 | none | Ship |
| SEC `data.sec.gov` | 200 | none | Ship |
| Treasury FiscalData `api.fiscaldata.treasury.gov` | 200 | `*` | Fetchable |
| TreasuryDirect | 200 | none | Ship |
| ECB `data-api.ecb.europa.eu` | 200 | `*` | Fetchable |
| ECB `eurofxref-hist.zip` | 200 | none | Ship |
| Frankfurter `api.frankfurter.dev/v1` | 200 | `*` | Fetchable. The old `api.frankfurter.app` 301-redirects there; the redirect response carries no ACAO, so use the new host. |
| World Bank `api.worldbank.org/v2` | 200 | none | Ship |
| CoinGecko | 200 | `*` | Fetchable |
| Coinbase Exchange candles | 200 | `*` | Fetchable |
| Kraken OHLC | 200 | echoes origin | Fetchable |
| `data-api.binance.vision` | 200 | `*` | Fetchable |
| `api.binance.com` | **451** (geo-blocked from the US) | — | Use binance.vision |
| OR-Library portfolio files (`port1.txt`, Beasley) | 200 | none | Ship (tiny) |
| UCI German Credit | 200 | none | Ship (tiny) |
| Ken French factors zip | 200 | none | Ship |
| Kaggle API | echoes origin | — | Requires auth; ship a subset |
| GitHub `datasets/s-and-p-500-companies` constituents CSV | 200 | `*` | Fetchable |
| `datasets/finance-vix` daily CSV | 200 | `*` | Fetchable |
| vega-datasets `stocks.csv` via jsDelivr | 200 | `*` | Fetchable |

**Energy, climate and agriculture**

| Endpoint | HTTP | ACAO | Verdict |
|---|---|---|---|
| MATPOWER `case14.m` (raw GitHub and jsDelivr) | 200 | `*` | Fetchable |
| pglib-opf `case14_ieee.m` | 200 | `*` | Fetchable |
| EIA v2 `electricity/rto/region-data` with DEMO_KEY | 200 | `*` | Fetchable |
| Open-Meteo forecast and archive | 200 | `*` | Fetchable |
| NASA POWER | 200 | `*` | Fetchable |
| NOAA NCEI | 200 | `*` | Fetchable |
| UK Carbon Intensity | 200 | `*` | Fetchable |
| Electricity Maps | 401 | `*` | Key needed |
| energy-charts.info | 200 | fixed own origin | Not usable |
| ERCOT dashboard | 200 | fixed `mis.ercot.com` | Not usable |
| Open Power System Data | 302 | none | Ship |
| GridStatus | 401 | `*` | Key |
| NREL developer API | timeout | — | Unknown |
| FAOSTAT | 521 | — | Down |
| USDA NASS | 401 | none | Ship |
| GBIF | 200 | `*` | Fetchable |

**Health and biology**

| Endpoint | HTTP | ACAO | Verdict |
|---|---|---|---|
| ClinicalTrials.gov v2 | 200 | `*` | Fetchable |
| openFDA | 200 | `*` | Fetchable |
| UniProt REST | 200 | `*` | Fetchable |
| EBI Proteins | 200 | `*` | Fetchable |
| `files.rcsb.org` PDB | 200 | `*` | Fetchable |
| `rcsb.org/fasta` | 200 | none | Use `files.rcsb.org` |
| PubChem PUG | 200 | `*` | Fetchable |
| NCBI E-utilities | 200 | `*` | Fetchable |
| NCBI FTP over https | 200 | `*` | Fetchable |
| NCBI Datasets v2 | 200 | echoes origin | Fetchable |
| cBioPortal | 200 | `*` | Fetchable |
| PhysioNet | 200 | none | Ship |
| CDC Socrata | 404 for my test ID | `*` | Domain is CORS-enabled |
| ECDC | 200 | `*` | Fetchable |

**Public sector, security and geo**

| Endpoint | HTTP | ACAO | Verdict |
|---|---|---|---|
| USGS earthquake GeoJSON | 200 | `*` | Fetchable |
| OpenFEMA v2 | 200 | `*` | Fetchable |
| HDX CKAN | 200 | `*` | Fetchable |
| ReliefWeb v1 | 410 Gone | `*` | Endpoint retired |
| OSM Overpass | 200 | `*` | Fetchable |
| NVD CVE 2.0 | 200 | `*` | Fetchable |
| OpenSky | 200 | fixed `https://opensky-network.org` | Not usable |
| US Census | 302 to missing-key page | — | Key needed; CORS unknown |
| SNDlib | 200 | none | Ship |
| Zenodo API | 403 to curl | — | Unknown |

**General hosting**

| Endpoint | HTTP | ACAO | Verdict |
|---|---|---|---|
| OpenML JSON API | 200 | `*` | Fetchable |
| OpenML data download | 301 | none | Ship |
| Hugging Face Hub API | 200 | echoes origin | Fetchable |
| Hugging Face datasets-server | 200 | echoes origin | Fetchable |
| GitHub REST API | 200 | `*` | Fetchable |

### Inferences
- **Prefer hosts that send ACAO `*` over hosts that echo the origin.** If Qollab runs Pyodide inside a sandboxed iframe, the request Origin may be `null`. Wildcard hosts still work for non-credentialed GETs; echo-based hosts may not. I could not verify Qollab's actual origin or its Content-Security-Policy `connect-src`. Test one fetch from inside the runtime first.
- **Finance:**
  - Live equities need Alpha Vantage or Twelve Data with a free key. Embedding the key in client code exposes it; acceptable for a free key, but say so.
  - Crypto is the only key-free live market data that is CORS-enabled (Coinbase, Kraken, Binance.vision, CoinGecko).
  - For reproducible judging, **ship a frozen CSV** (for example 5 years of daily closes for 2–10 tickers, roughly 50–300 KB) and offer an optional live refresh.
  - The qiskit-finance providers (`YahooDataProvider`, `WikipediaDataProvider`, Nasdaq `DataOnDemandProvider`) depend on services that are CORS-blocked or discontinued (my inference from the tests above plus the provider names). Use `RandomDataProvider` or your own loader instead.
- **The "public dataset" criterion is satisfied by documenting provenance** (URL, retrieval date, licence) of a shipped file. Using GitHub plus jsDelivr gives both reproducibility and a live-looking fetch.
- Results may differ from a browser (bot blocking, geo-IP) and can change over time. Re-run `cors_check.sh` during the event.

### Gaps
- The Qollab page origin and CSP were not tested.
- No preflight (OPTIONS) tests were run. They are not needed for simple GETs without custom headers. Adding an `Authorization` header would trigger a preflight, and none of these APIs were tested for that.
- Alpha Vantage's free-key rate limits were not verified this session.

---

## Q4. Impact framing: how industry values these use cases, and how to present "impact potential" credibly

### Takeaway
Analyst valuations are large but soft:
- **McKinsey QTM 2026 (Apr 20 2026): $1.3–2.7T** economic value from quantum computing by 2035.
- **BCG (July 2024): $450–850B** by 2040.

Independent critics note these mix AI and quantum effects and compare 2035 quantum against today's classical baseline.

The credible way to present impact in a 48-hour project is bottom-up:
1. the real decision and its classical cost today;
2. what the quantum subroutine measurably did at toy scale (with a baseline);
3. **a fault-tolerant resource estimate for the full-size version** (logical qubits, T/Toffoli count, required logical clock) from a peer-reviewed or XPRIZE-style analysis;
4. where IonQ's roadmap (Tempo 100 qubits, then Superion 256 in 2027, then a fault-tolerance demo in 2027 and a commercial system in 2028, then 80k logical qubits by 2030) would and would not close the gap.

### Cited Findings
- **McKinsey Quantum Technology Monitor 2025** (June 2025)
  - Quantum computing revenue **$28–72B by 2035**.
  - All quantum technology up to **$97B (2035)** and **$198B (2040)**.
  - Computing economic value **$0.9–2.0T by 2035**.
  - Chemicals, life sciences, finance and mobility see the most growth.
  - Sources: [McKinsey](https://www.mckinsey.com/our-insights/the-year-of-quantum-from-concept-to-reality-in-2025); [e27](https://e27.co/mckinsey-quantum-computing-20250812/); [CFO Dive](https://www.cfodive.com/news/quantum-advantage-boost-businesses-2t-2035-mckinsey-it-technology-computing-tech/714489/)
- **McKinsey QTM 2026** (5th edition, released 2026-04-20)
  - **$1.3–2.7T** economic value by 2035; **pharma $50–400B** (5–20% R&D and 5–15% clinical-trial savings).
  - Quantum computing company revenue **>$1B in 2025**, about **$4.4B in 2028**; internal QT market $60–100B by 2035, of which quantum computing is $43–71B.
  - **$12.6B invested in 2025** (6.3× the prior year), 97% private.
  - Leading adopters: chemicals/life sciences (simulation), travel/logistics (optimization), and financial services (risk modelling and PQC preparation).
  - **Critique (Ivezic, PostQuantum):** projections compare 2035 quantum against today's classical computing; the lower bound is more credible; a July 2026 addendum says the **$400–600B finance figure "cannot be reproduced"** from the stated assumptions.
  - Source: [PostQuantum](https://postquantum.com/industry-news/mckinsey-quantum-monitor-2026/)
- **BCG** (2024-07-18)
  - Reaffirms **$450–850B** economic value by 2040 and a **$90–170B** provider market.
  - Admits **NISQ-era assumptions "proved overly optimistic"** because of hardware difficulty and stronger classical and AI competition.
  - The 2021 release framed the same range as *annual* value.
  - Sources: [BCG press release](https://bcg.com/press/18july2024-quantum-computing-create-up-to-850-billion-of-economic-value-2040); [BCG 2021](https://www.bcg.com/press/21july2021-quantum-computing-transform-multiple-industries-create-850-billion-annual-value)
- **XPRIZE Phase II rubric** asks for quantified real-world impact, benchmarks against the best classical methods, and **detailed resource estimates (architecture, logical qubits, error-correction assumptions)**. It is a ready-made template for a hackathon "impact" slide. — [TQI](https://thequantuminsider.com/?p=2383234)
- **Resource anchors to quote:**

  | Problem | Estimate | Source |
  |---|---|---|
  | Derivative pricing | 8k logical qubits, T-depth 54M, ~1 s | [Chakrabarti 2021](https://quantum-journal.org/papers/q-2021-06-01-463/) |
  | Derivative pricing | 4.7k logical qubits, 10⁹ T at 45 MHz | [Stamatopoulos & Zeng 2024](https://arxiv.org/abs/2307.14310v2) |
  | Portfolio QIPM | Needs fundamental improvements | [Dalzell 2023](https://arxiv.org/pdf/2211.12489) |
  | FeMoco | 2,196 logical qubits, 6.7B Toffoli, ~4 days on ~3M physical; or ~89k physical in under a month | [Lee 2021](https://arxiv.org/pdf/2011.03494); [arXiv:2605.30455](https://arxiv.org/pdf/2605.30455) |
  | RSA-2048 | <1M physical, <1 week | [Gidney 2025](https://arxiv.org/abs/2505.15917v1) |
  | ECDLP-256 | <500k physical, minutes | [TQI](https://thequantuminsider.com/2026/03/31/q-day-just-got-closer-three-papers-in-three-months-are-rewriting-the-quantum-threat-timeline/) |
  | CFD drag | 10²¹–10³⁹ logical-qubit×T, no exponential advantage | [Penuel v3](https://arxiv.org/pdf/2406.06323) |

- **IonQ roadmap facts** (from `ionq_hardware_and_sdk.md`):
  - **Tempo:** 100 qubits, #AQ 64 claimed 2025-09-25; sold on-premises, **not on public clouds**.
  - **Superion 256:** deliveries 2027.
  - **Superion 10K:** fault-tolerance demo 2027, commercial system 2028.
  - **2M physical / 80k logical qubits by 2030** (arXiv 2604.04761).
  - Sources: [IonQ news](https://www.ionq.com/news/ionq-achieves-record-breaking-quantum-performance-milestone-of-aq-64); [TQI 2026-09-08](https://thequantuminsider.com/2026/09/08/ionq-uses-investor-day-to-detail-superion-roadmap-skywater-strategy-and-quantum-security-plans/); [arXiv:2604.04761](https://arxiv.org/html/2604.04761v1)
  - Pistoia's May 2026 blog also says "10,000 physical qubits and 800 logical qubits by next year", while its heading reads "8,000 logical" [vendor, internally inconsistent]. — [IonQ blog](https://www.ionq.com/blog/from-wall-street-hypothesis-to-nyse-production-the-real-world-arrival-ofquantum-finance)

### Inferences
- **An "impact potential" slide that judges will trust:**
  - (i) Size of the decision. Example: a bank runs thousands of MC risk revaluations nightly; a grid operator solves UC hourly.
  - (ii) Measured toy-scale result with error bars against a tuned classical baseline.
  - (iii) A "what scales" chart that extrapolates the measured 2Q-count and error-versus-calls curves to the fault-tolerant threshold from the literature.
  - (iv) A time-to-advantage bar for each roadmap milestone: Tempo 100 (2026), Superion 256 (2027), the fault-tolerance demo (2027–2028), 80k logical qubits (2030).
  - (v) An explicit "what would have to be true" line. For finance QAE: a logical T-rate of about 45 MHz.
- **What Tempo-class hardware improves for the recommended projects:**
  - MLAE: 99.9% 2Q fidelity (target) allows roughly 5–10× more 2Q gates before the noise knee, which means larger m or n=3–4 registers. It does not change the fault-tolerant conclusion.
  - Optimization: 64–100-qubit subproblems, as in the IonQ/Kipu 36-to-64 scaling claim.
  - This is my inference from the fidelity target, not a measured result.
- Avoid quoting McKinsey's or BCG's top-down dollar values as a project's impact. Use them only as sector-priority context, and cite the critiques.

### Gaps
- I did not retrieve the McKinsey 2026 per-sector value table for finance, energy, logistics or automotive. The only number available is the critic's "$400–600B finance" figure.
- Hyperion Research figures and BCG's 2025 "business ready" report were not retrieved from primary sources.
- I found no peer-reviewed estimate of trapped-ion logical clock rates for 2028–2030. The ~10 kHz figure is secondhand.
