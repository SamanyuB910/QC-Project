# Past Winning and Finalist Application / Industry Quantum Projects (2019-2026): What Wins in Applied Quantum Challenges

Research date: 2026-10-09. Scope: application, real-world-impact and industry-use-case projects at quantum hackathons and industry challenges from 2019 to 2026. It complements two earlier notes and does not repeat them:
- `research_notes/Qollab IonQ hackathon track/past_ionq_challenges_and_winners.md` covers the IonQ iQuHACK tracks, the Qollab Creative Challenge, the Spring 2026 cohort list and the NQCC 2024 headline.
- `research_notes/Quantum Unlocked theme deep dive/past_educational_winners.md` covers educational winners and the CQhack25 educational losers.

Those items are only cross-referenced here.

**Label key:**
- **WINNER**: a placed prize (1st, 2nd, 3rd or a named category prize).
- **FINALIST / SEMIFINALIST**: advanced in a multi-phase challenge without (yet) winning.
- **FUNDED**: a grant or cohort selection, not a competition win.
- "(via search snippet)" means the fact was seen only in a search-result summary, not on a fetched page.

---

## Key Question 0 (Objective): Catalog of winning and finalist application projects, 2019-2026

### Takeaway
At expert-judged industry events, applied winners use **small, honest, well-benchmarked prototypes of a real end-user problem**:
- NQCC 2023, 1st: 4x4 linear systems on hardware.
- NQCC 2024, 1st: a quantum circuit Born machine copula for insurance risk, extending an IonQ paper.
- BMW 2021: winners who openly said classical methods win today.

Multi-year industry prizes (Airbus, BMW, Deloitte, XPRIZE, Q4Bio) increasingly reward **resource estimation, classical benchmarking and a credible scaling path** over claims of present-day advantage. At low-bar student Devpost events (CQhack25), flashy apps with large unverified claims also won.

### Cited Findings

**UK NQCC Quantum Hackathons (industry use cases, early-career researchers, expert panel)**
- **2023 (July, University of Birmingham; 10 teams; 2 days).** Use cases spanned energy, healthcare, telecom, aerospace and finance — [NQCC 2023 Technical Report](https://www.nqcc.ac.uk/wp-content/uploads/2024/04/NQCC_Quantum-Hackathon-2023_Technical-report.pdf)
  - **WINNER 1st: Rolls-Royce team, "Near-term quantum linear solver algorithms."**
    - Problem: CFD/FEM for power systems reduces to matrix inversion (Ax=b).
    - Methods: Coherent Variational Quantum Linear Solver (CVQLS) for NISQ, plus QSVT for fault tolerance, built mostly in Classiq with parts in PennyLane.
    - Hardware: IBM Guadalupe (16q), IonQ Aria (20 AQ) and IonQ Harmony.
    - Results: up to **4x4 systems on hardware and 16x16 in simulation**. QSVT could not be compiled to QASM for hardware.
    - [same report](https://www.nqcc.ac.uk/wp-content/uploads/2024/04/NQCC_Quantum-Hackathon-2023_Technical-report.pdf)
  - **WINNER 2nd: Jacobs team, "1-D Monte Carlo particle transport"** (neutron transport).
    - Methods: quantum sampling of distributions, and quantum amplitude estimation (QAE) of penetration probability as a "biased quantum coin", on the Quantinuum H1 Emulator.
    - Outcome, stated honestly: "solutions obtained via quantum sampling showed a large variation from the analytical solutions". The toy case had only two energy levels, and QAE was "not fully explored".
    - [same report](https://www.nqcc.ac.uk/wp-content/uploads/2024/04/NQCC_Quantum-Hackathon-2023_Technical-report.pdf)
  - **WINNER 3rd: Applied Quantum Computing team, "Vaccination centre location."**
    - Method: weighted set cover as a QUBO, solved with QAOA (Qiskit) and VQE (Braket simulators).
    - Size: instances of N=4 population centres with V=2 centres, and N=3, V=2.
    - Result: the best VQE initialization gave an **89% probability of the ground state**. The team flagged the open question of scaling and time-to-solution.
    - [same report](https://www.nqcc.ac.uk/wp-content/uploads/2024/04/NQCC_Quantum-Hackathon-2023_Technical-report.pdf)
  - Other 2023 use cases that did not place: DNA sequencing with equivariant embeddings, NHS TSP routing, unit commitment for the grid, fusion FEM, skills-constrained CVRP with time windows, price prediction, and unicast/multicast routing — [same report](https://www.nqcc.ac.uk/wp-content/uploads/2024/04/NQCC_Quantum-Hackathon-2023_Technical-report.pdf)
  - UKAEA's Fazal Chaudry: the algorithms "could in principle solve the problem" but hardware is not mature enough to show advantage, and "we need to rethink the way we encode information to achieve a speed up" — [Physics World](https://physicsworld.com/a/hackathon-offers-glimpse-of-quantum-potential/)
- **2024 (July 22-24, University of Warwick; 13 teams; 69 participants, 24 end-user mentors, 19 provider mentors, 4 judges).** Six use cases were QML, five optimisation and two simulation — [NQCC 2024 Technical Report](https://nqcc.ac.uk/wp-content/uploads/2025/04/NQCC_Quantum-Hackathon-2024_Technical-report.pdf). The IonQ press release says "over 70 coders" — [IonQ news](https://ionq.com/news/ionq-qpus-and-classiq-software-power-winning-projects-at-the-uks-national)
  - **WINNER 1st: KL Divergents, "Risk aggregation evaluation for insurance losses in case of natural disaster"** (use case from Mind Foundry and Aioi R&D Lab; resources from Quantinuum, IonQ and Classiq).
    - Approach: the team "extended the work in [1]", which is a Scientific Reports paper — [NQCC 2024 report](https://nqcc.ac.uk/wp-content/uploads/2025/04/NQCC_Quantum-Hackathon-2024_Technical-report.pdf). That paper is **"Copula-based risk aggregation with trapped ion quantum computers" by Daiwei Zhu et al. (IonQ and GE Research)**. It trains quantum circuit Born machines (QCBMs) to model 3- and 4-variable copulas on a trapped-ion device, and reports "comparable or better" predictions than standard classical models — [arXiv 2206.11937 / Sci Rep 2023 (via search snippet)](https://arxiv.org/abs/2206.11937)
    - Extensions:
      - A portfolio mixing financial assets *and* insurance losses.
      - Scalability, improved with a **randomised KL-divergence loss** using random binary splits, which reduces the data needed to fit the copula (important given limited historical records).
      - Insurance losses modelled as a hierarchical Bernoulli + LogNormal mixture.
      - "Quantitative evaluation against a classical" baseline.
      - Comparison of ansätze on emulators, then **inference on real hardware** (Quantinuum, and IonQ via Classiq).
    - The end-user mentor wrote that "the flexibility of a variational quantum circuit can outperform classical approaches for this task".
    - [NQCC 2024 report](https://nqcc.ac.uk/wp-content/uploads/2025/04/NQCC_Quantum-Hackathon-2024_Technical-report.pdf)
    - Judge Stasja Stanisic (Phasecraft) said a **robust benchmarking approach**, a structured comparison against other possible solutions, was a key factor. She also noted the team took time to understand the problem and adapted its algorithm to it — [Physics World](https://physicsworld.com/a/quantum-hackathon-makes-new-connections/)
  - **WINNER 2nd: Schrödinger's Apples, BT network coverage** (placement of transmitters, receivers and sensors).
    - Formulation: minimum vertex cover, extended to budget-constrained weighted assignment that prioritises vulnerable communities.
    - Methods: the D-Wave CQM hybrid solver was "very successful" on a BT-like topology. A QAOA version was "promising" in simulation but had limited QPU time.
    - Classical comparators named by BT: simulated annealing and MIP, whose guarantees are "often over 10% below" optimum.
    - [NQCC 2024 report](https://nqcc.ac.uk/wp-content/uploads/2025/04/NQCC_Quantum-Hackathon-2024_Technical-report.pdf)
  - **WINNER 3rd: "Trust me, I'm a Doctor...of physics...in training", NHS A&E forecasting** (NHS England).
    - Pivot: the team first tried quantum MCMC and found it "unsuitable" because the algorithms estimate means rather than full distributions. It switched to a 2022 variational time-series forecaster (4-value input window, 2 layers).
    - Hardware: developed on the Classiq emulator, then tested on a **25-qubit error-mitigated QPU**.
    - **Data: "we generated a fake time series representing linear growth"** instead of real A&E data. Some training runs learned the trend.
    - [NQCC 2024 report](https://nqcc.ac.uk/wp-content/uploads/2025/04/NQCC_Quantum-Hackathon-2024_Technical-report.pdf)
  - Non-placing examples:
    - CGI energy price forecasting: a 6-qubit angle-encoded PQC on ELEXON GB data (public, 30-minute resolution, Apr 2023-Mar 2024).
    - Johnson Matthey feature selection with D-Wave: "the classical approach outperformed the quantum approach". The best classical method was top-mean-|SHAP| features, and the team was "unable to demonstrate an advantage".
    - Other use cases: Homomorphic Labs federated qGANs, Nomura time series, North Wales Police deployment, Rolls-Royce Hamiltonians, UKAEA Hamiltonian NNs, Unisys supply chain, LTIMindtree flow-shop, Cisco network search.
    - [NQCC 2024 report](https://nqcc.ac.uk/wp-content/uploads/2025/04/NQCC_Quantum-Hackathon-2024_Technical-report.pdf)
- **2025 (July 21-23, University of Edinburgh; fourth edition)** — [NQCC 2025 page](https://www.nqcc.ac.uk/uk-quantum-hackathon-2025)
  - **WINNER 1st:** "Closure optimisation for road maintenance" (Aioi R&D Lab / Mind Foundry; D-Wave and IBM Quantum). The team name is not legible on the page.
  - **WINNER 2nd: Cubic Qubits**, "Quantum-enhanced 3D bin packing for complex logistics" (Decision Lab; AWS, Rigetti via AWS, and Classiq).
  - **WINNER 3rd: QuDITS**, "Quantum machine learning for diabetes identification" (Applied Quantum Computing; Infleqtion).
  - Methods and results are not described on the page.
  - [NQCC 2025 page](https://www.nqcc.ac.uk/uk-quantum-hackathon-2025)

**MIT iQuHACK industry (non-IonQ) challenges**
- **2023 challenge list:**
  - QuEra: graph problem optimization (in person). WINNER 1st 5-Headed Cat; 2nd braided_anyons.
  - Covalent x IBM: quantum-classical hybrid compute. WINNER 1st Entangled Entities; 2nd Entangled.
  - Quantinuum: resource optimization. WINNER 1st Pineapple; 2nd Quassant; 3rd Carls'.
  - Microsoft: algorithmic optimization (remote). Three-way tie for 1st.
  - Social Impact winners: Qrabs (in person) and Kyue (remote).
  - [iQuHACK 2023 page](https://www.iquise.mit.edu/iquhack/2023-01-27)
- **Covalent x IBM 2023 brief:**
  - Task: build a "cloud-based, quantum-powered application for a real-world problem" usable by ordinary users, on IBM Nairobi or Oslo hardware, with Covalent workflows.
  - **Rubric: technical aspects 30%, originality 25%, usefulness and complexity 25%, presentation 20%.**
  - [Covalent x IBM challenge repo (fork)](https://github.com/mannypaeza/2023_CovalentxIBM)
- **2024 winners by challenge:**
  - AWS: 1st Case Chicago Quantum.
  - IBM: 1st Bulldogs.
  - **Moody's: 1st <Y|🦆|H>, 2nd Dragon Inc.**
  - Quandela: 1st Yale Varsity Clash Royale Team.
  - Quantinuum: 1st Lion in a Box.
  - QuEra: 1st Plancktons.
  - Classiq (remote): 1st QuantumBuzzword, with a "Most Creative Solution" honorable mention.
  - In-person projects were "judged on your project's performance on an actual quantum computer".
  - [iQuHACK 2024 page](https://www.iquise.mit.edu/iquhack/2024-02-02)
- **Moody's 2024 (portfolio optimization):**
  - Brief: build "a quantum portfolio optimizer from start to finish" *plus* a pitch for why companies should invest in quantum now.
  - Winning approach (<Y|quack|H>, Yale/Harvard): quantum annealing on QUBO-formulated **mean-VaR** portfolio optimization, tested with simulated annealing and the D-Wave 2000Q. The team projected "up to 6% per business quarter" returns, which is its own projection.
  - [Yale Physics (via search snippet)](https://physics.yale.edu/node/7275)
- **2024 Social Impact WINNER:** an **organ donor-patient matching** mobile app using quantum matching algorithms. No results are reported — [MIT News](https://news.mit.edu/2024/hackathon-unlocking-quantum-future-0318)
- **Moody's 2025 (Jan 29-Feb 2):**
  - Brief: an **early-warning indicator for financial bubbles via topological data analysis (TDA)** and quantum algorithms, i.e. Betti-number shifts before market transitions, using quantum phase estimation (QPE). 12 of 15 teams (75 students) submitted.
  - **WINNER 1st "Submitted by God at 11:59 p.m."** "used rich visualizations" and explored several techniques for optimizing the quantum algorithm.
  - 2nd Backslash (included a former Moody's intern and 2024 prize winner); 3rd Looniverse.
  - [Moody's recap](https://www.moodys.com/web/en/us/insights/quantum/mit-hackathon-recap.html)
- **2025 sponsors** were Alice & Bob, Classiq, IonQ, Moody's, Quantinuum and QuEra. No official winners list is posted — [iQuHACK 2025 page](https://www.iquise.mit.edu/iquhack/2025-01-31)
- **2026:** Brown teams won **1st in the IQM challenge, 1st in the Quantum Rings challenge** and 3rd in IQM. The projects are not described — [Brown CS](https://awards.cs.brown.edu/2026/02/23/brown-cs-students-earn-two-first-place-and-one-third-place-awards-at-mit-iquhack-2026/)

**QHack (Xanadu) open hackathon application categories**
- **QHack 2022:**
  - **Quantum Finance 1st: Team Avocados, "Quantum Counselor for Portfolio Investment".** It also won QAOA and Quantum Entrepreneurship 1st. Design: an LSTM+quantum-layer forecaster feeds a QUBO portfolio optimizer solved with QAOA and VQE, **benchmarked against IBM CPLEX** — [QHack 2022 issue #122](https://github.com/XanaduAI/QHack2022/issues/122)
  - Other finance placements: 2nd my_favourite_team (asynchronous VQAs); 3rd Samras (quantum autoencoders for anomaly detection).
  - Quantum Entrepreneurship 2nd: UncertaintyHack (quantum LSTM for stock prices).
  - Bio-QML, Analog and Braket-QPU winner: Qnyble, "Quantum RNA Folding".
  - Quantum Chemistry 1st: PauliZ (fast Hamiltonian simulation).
  - Science 1st: Edelweiss (learning-based error mitigation for VQE).
  - Braket "Most creative": Qumpula Quantum (optimization for sustainable cloud data workflows).
  - [PennyLane QHack 2022 recap](https://pennylane.ai/blog/2022/03/qhack-2022-the-one-of-a-kind-celebration-of-quantum-computing/)
- **QHack 2023:**
  - Quantum Chemistry 1st: **jetix**, "Molecular Energy Landscapes of HEA in Quantum Computing for Carbon Capture". Quantum Computing Today! 3rd and a Braket top-3: **Avocados**, "Enhancing Portfolio Optimization Solutions". Hybrid 1st: Qumpula Quantum, "MatriQ". NVIDIA 2nd: QSVM/QCNN stellar classification — [PennyLane QHack 2023 highlights](https://pennylane.ai/blog/2023/04/qhack-2023-highlights/)
  - Amazon Braket judges evaluated the top 15 on "scientific and technical merit, depth of use of the quantum computing software and hardware stack, and potential for onward development" — [AWS Braket QHack 2023 winners](https://aws.amazon.com/blogs/quantum-computing/announcing-the-amazon-braket-challenge-winners-of-the-qhack-2023-hackathon)
  - **jetix (carbon capture):**
    - System: CO2 adsorption near Mn(II)/Cu(I) ions.
    - Method: 5-qubit VQE with a hardware-efficient ansatz, freezing near-0 or π/2 parameters (after Choy et al.) and grouping Hamiltonian terms.
    - Results: **60.8% faster convergence for a 2.82% error increase (within 0.002 Ha)**, plus 3 iterations on Rigetti Aspen-M-3.
    - Judges: they could "understand and implement VQE for a climate change application".
    - [AWS](https://aws.amazon.com/blogs/quantum-computing/announcing-the-amazon-braket-challenge-winners-of-the-qhack-2023-hackathon)
  - **QuantuMother (carcinogenicity):**
    - Data: rat carcinogenesis compounds as graphs.
    - Method: a Quantum Evolving Kernel via analog Hamiltonian simulation on a Rydberg-array simulator, plus a Trotterized gate version.
    - Results: the analog version separated classes; the gate version did not. No classical baseline is reported.
    - [AWS](https://aws.amazon.com/blogs/quantum-computing/announcing-the-amazon-braket-challenge-winners-of-the-qhack-2023-hackathon)
  - **Avocados (portfolio):**
    - Method: "unbalanced penalization" encodes inequality constraints without slack qubits (OpenQAOA), up to 24 assets, on SV1, IBM Guadalupe and IonQ.
    - Result: for 10 assets, about **1400x higher probability of the optimal solution** vs. the slack-variable encoding.
    - Judges: it "reduce[d] the number of qubits required".
    - [AWS](https://aws.amazon.com/blogs/quantum-computing/announcing-the-amazon-braket-challenge-winners-of-the-qhack-2023-hackathon)
- **QHack 2024:** the categories were algorithmic primitives (amplitude embedding, spectral gap, qubit reduction, Hamiltonian evolution, phase transitions). The applied wins were jetix ("Simulating lithium-ion batteries on quantum computers", 2nd Sound of Silence and NVIDIA 1st) and Curious Turtles ("Hamiltonian simulation for solving PDE", 1st) — [PennyLane QHack 2024 highlights](https://pennylane.ai/blog/2024/03/qhack-2024-highlights/)

**Corporate industry challenges (multi-month)**
- **Airbus Quantum Computing Challenge (launched 2019; finalists Oct 2020; winner Dec 10, 2020).**
  - Setup: five flight-physics problems; more than 800 registrants.
  - **WINNER: Machine Learning Reply** (Italy), **aircraft loading optimisation** (maximise cargo under weight, balance and centre-of-gravity limits) with quantum annealing — [Airbus press release](https://www.airbus.com/en/newsroom/press-releases/2020-12-airbus-quantum-computing-challenge-helps-advance-sustainable-flight); [Reply](https://www.reply.com/en/newsroom/news/machine-learning-reply-wins-the-airbus-quantum-computing-challenge)
  - **FINALISTS:**
    - Capgemini: wing-box optimisation with HHL- and QSVM-inspired algorithms (one fault-tolerant, one NISQ), claiming "an order of magnitude" gain.
    - Niels Backfisch: QML that computes many models' predictions at the cost of one.
    - Origin Quantum: a quantum-accelerated SU2 CFD solver claiming O(polylog N), conceding that fault tolerance and QRAM are needed.
    - Universidad de Montevideo: VQE for cargo loading as a constrained knapsack, *with qubit estimates and a near-term feasibility analysis*.
    - [The Quantum Insider](https://thequantuminsider.com/2020/10/22/airbus-names-its-five-finalists-for-quantum-computing-challenge/)
- **BMW Group Quantum Computing Challenge (with AWS; winners at Q2B Dec 2021).**
  - Setup: more than 70 teams, 15 finalists, 4 use cases. Braket credits gave access to D-Wave, IonQ and Rigetti.
  - **Criteria: comprehensibility, feasibility, scalability, innovation, benefit to BMW Group.**
  - **WINNERS:**
    - **Accenture (vehicle sensor placement):** a full workflow (preprocess, then MaxCover, then a visualization app). "Classical custom algorithms performed best today", with plugins for future quantum methods.
    - **Qu&Co (material deformation PDEs):** differentiable quantum circuits, benchmarked against exact solutions and classical neural nets.
    - **1QBit + NTT (pre-series vehicle configuration, SAT):** a hybrid MaxSAT sub-solver for the near term, plus Dürr-Høyer / amplitude amplification **with a scaling analysis** for the fault-tolerant regime.
    - **QC Ware (automated quality inspection, image classification):** three quantum algorithms for faster convolutions, complexity-theoretic arguments, and simulations on two image datasets. Judges: "While today QML will not be able to solve this classification task better than established classical methods", the work clarifies where quantum could help later.
  - [AWS blog](https://aws.amazon.com/blogs/quantum-computing/winners-announced-in-the-bmw-group-quantum-computing-challenge)
- **Airbus-BMW "Quantum Mobility Quest" (launched Dec 2023; winners Dec 2024).**
  - Setup: more than 100 proposals from 25+ countries, then 15 Phase II finalists, then 5 winners at €30,000 each. Braket gave access to IonQ, IQM, QuEra and Rigetti — [AWS blog](https://aws.amazon.com/blogs/quantum-computing/winners-announced-in-the-airbus-bmw-group-quantum-computing-challenge); [BMW press (via search snippet)](https://press.bmwgroup.com/global/article/detail/T0446782EN/bmw-group-and-airbus-reveal-winners-of-quantum-computing-challenge)
  - **WINNERS:**
    - **USC (smart coating):** DFT screening of corrosion inhibitors, then quantum embedding with VQA proofs of concept on simulator and hardware.
    - **4colors Research (logistics):** an "integrated, quantum-ready solver" that runs classically today with optional quantum plug-ins.
    - **Quandela (autonomy):** a qGAN that turns day images into night images for vision training.
    - **University of Hamburg (quantum solvers):** compressed representations for fluid and sound simulation.
    - **TU Delft (Golden App):** a VQA for carbon-fibre laminate stacking-sequence retrieval, simulated for 8 and 10 plies, *plus a quantum-inspired DMRG heuristic that "outperformed existing classical solutions in many cases"*.
    - [AWS blog](https://aws.amazon.com/blogs/quantum-computing/winners-announced-in-the-airbus-bmw-group-quantum-computing-challenge)
- **Deloitte Quantum Climate Challenge:**
  - **2022 (flight routing to cut climate impact, including contrails).**
    - Setup: 130 entrants and 5 finalists. All participants had a 7-qubit IBM device; finalists got a 16-qubit IBM system.
    - **WINNER 1st Quantimize**; 2nd Felix Frohnert; 3rd Lufthansa Industry Solutions (contrail-avoidance routing).
    - [kipark.de (via search snippet)](https://kipark.de/en/sieger-der-deloitte-quantum-climate-challenge-2022); [LHIND news (via search snippet)](https://www.lufthansa-industry-solutions.com/de-en/newsroom-downloads/news/quantum-climate-challenge-2022-team-of-experts-from-lufthansa-industry-solutions-among-the-top-5)
    - Quantimize's repo: baselines were straight-line fuel-efficient routes and a classical genetic algorithm (after AirTraf 1.0). Quantum attempts were QUBO + QAOA/annealing, a quantum GA and a QNN.
    - Its conclusion: "**the classical genetic algorithm is the best choice for a large dataset at present**", the quantum GA shows "no clear advantage", and the QNN cannot be trained with the qubits available.
    - [Quantimize GitHub](https://github.com/fjelljenta/Quantum-Challenge)
  - **2023 (quantum simulation of chemical reactions for MOF direct air capture).**
    - Setup: 120+ participants and 15 ideas; about 130 hours of QPU time, some on 27-qubit machines.
    - **WINNER 1st EcoQult (qBee):** dissociation energies of ion-gas systems with multiple classical and quantum methods, **compared on resources, run-time and accuracy**. Its hybrid approach (a cheap classical estimate plus VQE local corrections) scaled to a 6-ion / 6-molecule system.
    - **2nd JetiX:** VQE de-parameterization and an initial-point setter, plus density-matrix embedding for scale-up.
    - **3rd QuantuX:** a configurable VQE pipeline.
    - [The Quantum Insider](https://thequantuminsider.com/2023/05/08/quantum-climate-challenge-team-ecoqult-wins-the-deloittes-quantum-climate-challenge/)
  - **2024 (disaster prediction, flood forecasting, climate resilience).** **WINNER: Imperial College** (four PhD students), "a scalable hybrid quantum-machine-learning framework for environmental risk control", using NVIDIA compute. Judges came from AWS and D-Wave. €5,000 prize — [Imperial](https://imperial.ac.uk/news/253677/imperial-students-deloitte-quantum-climate-challenge)

**Grand challenges (2023-2027)**
- **XPRIZE Quantum Applications (Google Quantum AI + GESDA; $5M; launched 2024, winners Spring 2027).**
  - Funnel: 133 submissions from 31 countries, then 20 **SEMIFINALISTS** (Oct 2025), then 7 **FINALISTS** (Dec 10, 2025, at Q2B). The finalists share $1M; $4M (including a $3M grand prize) is due March 2027 — [Google blog](https://blog.google/technology/research/google-gesda-xprize-quantum-applications-finalists/); [XPRIZE](https://www.xprize.org/prizes/qc-apps)
  - **FINALISTS and their problems:**
    - **Calbee Quantum** (Garnet Chan, Caltech): materials and semiconductor/optoelectronics simulation, claiming a system-size speedup even at approximate accuracy.
    - **Gibbs Samplers** (András Gilyén, Rényi Inst.): thermalization and low-temperature Gibbs states to narrow candidate materials.
    - **Phasecraft Materials** (Toby Cubitt): quantum simulation to improve classical quantum-chemistry methods (batteries, solar, carbon capture).
    - **The QuMIT** (Alexander Schmidhuber, MIT): **hypergraph community detection for protein-protein interaction analysis in polygenic disease**.
    - **Xanadu** (J.M. Arrazola): time evolution of molecular processes (organic solar cells, photodynamic therapy).
    - **Q4Proteins** (Markus Reiher, ETH): quantum chemistry plus classical ML for drug discovery and biomolecular condensates.
    - **QuantumForGraphproblem** (Jianqiang Li, Rice): a linear-systems algorithm without the condition-number dependence.
    - [Google blog](https://blog.google/technology/research/google-gesda-xprize-quantum-applications-finalists/)
  - **SEMIFINALISTS (20):** 4colors Research, Algorithmiq, Another Quantum, Austinites, BQE, Calbee Quantum, Gibbs Samplers, HQS Quantum Simulations, Los Quanta, Nature, ParityQC, the Pasqal Alliance in Quebec, Phasecraft, Q-CTRL & UoE, Q4Proteins, QC-assisted biological electron microscopy, QuantumForGraphproblem, Riverlane, The QuMIT, Xanadu. They were "chosen for the plausibility and quality of their ideas" — [The Quantum Insider](https://thequantuminsider.com/2025/10/21/xprizes-quantum-for-real-world-impact-announces-semi-finalists/)
  - Location conflicts:
    - QuantumForGraphproblem is listed as Houston ([Google/QCR](https://quantumcomputingreport.com/xprize-quantum-applications-names-seven-finalists-in-5-million-global-competition/)), Richardson ([XPRIZE](https://www.xprize.org/prizes/qc-apps)) and State College ([TQI](https://thequantuminsider.com/2025/10/21/xprizes-quantum-for-real-world-impact-announces-semi-finalists/)).
    - Algorithmiq is listed as Wilmington (TQI) and Milan (XPRIZE).
    - A UMD QuICS post reportedly counts five finalists rather than seven (via search snippet), against seven in the official sources — [QuICS](https://www.quics.umd.edu/about/news/quics-researchers-advance-final-phase-5-million-xprize-quantum-applications-competition)
- **Wellcome Leap Quantum for Bio (Q4Bio; $50M program launched 2023; results Apr 16, 2026).**
  - Funnel: 12 teams, then 6 Phase III **FINALISTS** (led by Infleqtion, Nottingham, Harvard, Stanford, Algorithmiq and Oxford).
  - **$2M bar:** an experiment on **>50 qubits at depth O(10³-10⁴) with a clear trajectory to advantage**. The $5M grand prize requires advantage over best-in-class classical baselines.
  - [The Quantum Insider](https://thequantuminsider.com/2026/04/16/wellcome-leap-quantum-for-bio-challenge-prize/)
  - **WINNER ($2M): Algorithmiq + Cleveland Clinic + IBM.** End-to-end hybrid workflow for **excited states of a photodynamic-therapy photosensitizer**: active-space selection, state preparation, measurement and post-processing, on **up to 100 qubits** on IBM hardware — [IBM blog](https://www.ibm.com/quantum/blog/q4bio-finalists)
  - **FINALISTS:**
    - **Oxford/Sanger "Quantum Pangenomics":** QUBO genome encoding of Hepatitis-D on IBM Heron r2. No classical comparison.
    - **Infleqtion + UChicago + MIT:** hybrid GPU+QPU **biomarker discovery from multimodal cancer data**, *compared with a purely classical pipeline* and reported better.
    - **Stanford/MSU:** VQE for ATP/GTP hydrolysis with resource-cost analysis.
    - **Nottingham + Phasecraft + QuEra:** quantum data to augment DFT for **covalent inhibitors for myotonic dystrophy**, on 120-qubit IBM Nighthawk.
    - [IBM blog](https://www.ibm.com/quantum/blog/q4bio-finalists)
  - Program director Shihan Sajeed: Q4Bio gave "a much clearer understanding of where quantum can create value, where it cannot" — [The Quantum Insider](https://thequantuminsider.com/2026/04/16/wellcome-leap-quantum-for-bio-challenge-prize/). Whether the $5M grand prize was awarded is not stated in the fetched article. A search snippet of the same article said it "remained unawarded" — [TQI (via search snippet)](https://thequantuminsider.com/2026/04/16/wellcome-leap-quantum-for-bio-challenge-prize/)

**Other industry-use-case hackathons**
- **BIG Q Hackathon (Chicago Quantum Exchange + QuantX, fall 2023).**
  - Setup: 9 use cases from 8 companies (Boeing wing layering and corrosion, United Airlines O'Hare vehicle maintenance, CSL/Capgemini reactions, General Atomics fusion scattering, J&J, Mayo Clinic, an energy firm) and 7 platforms.
  - **Technical WINNER "Superball":** biomanufacturing optimisation via quantum annealing on Infleqtion.
  - **Business WINNER "Teq Staq":** a Boeing wing-manufacturing pitch on financial and climate savings.
  - [CQE](https://chicagoquantum.org/news/big-q-hackathon-demonstrated-key-quantum-progress-collaboration-between-tech-and-industry)
- **NYUAD Hackathon for Social Good (Womanium-linked prizes):**
  - 2025 WINNER **MohituQ:** decoded quantum interferometry to model ocean-waste circuits and place collection nets.
  - 2025 3rd **SAWTY:** quantum-secure e-voting.
  - 2024 WINNER **QGasBusters** (project not described).
  - [CERN OQI (via search snippet)](https://open-quantum-institute.web.cern.ch/harnessing-quantum-for-social-good-at-13th-nyuad-hackathon); [NYUAD 2025 (via search snippet)](https://nyuad.nyu.edu/en/news/latest-news/science-and-technology/2025/april/nyuad-hackathon-ai-quantum-computing.html)
- **Womanium program:** UCLA's "Bruinium" team won two prizes, one of which asked whether a gate-based device could simulate **LiH for hydrogen-storage fuel-cell vehicles** (year not given) — [UCLA Chemistry (via search snippet)](https://www.chemistry.ucla.edu/news/womanium-quantum-computing-and-entrepreneurship-program/)
- **QCHack 2022 Azure/IonQ:** WINNER Qu-Mongus, FRQI image processing on 11 qubits (covered in prior notes).
- **CQhack25 (online student hackathon, mid-2025; 304 participants; $1,900 prizes).** Judging (per the Devpost listing) covered functionality, depth of quantum use, and applicability to real problems — [CQhack25 Devpost (via search snippet)](https://cqhack25.devpost.com/). All six **WINNERS** were applications — [gallery](https://cqhack25.devpost.com/project-gallery):
  - **Quantum Route Optimizer:**
    - Method: VRP to QUBO/Ising to QAOA (Qiskit Aer, 1024 shots, COBYQA), with lazy-cut subtour elimination inside the loop.
    - Scale: **3 nodes with 1-2 vehicles**.
    - Results "match the optimal solutions for certain test cases".
    - Framing: drone delivery for EMS and wildfire. It claims quantum "can explore every route simultaneously".
    - [Devpost](https://devpost.com/software/quantum-route-optimizer)
  - **Q-Cure (drug-drug interactions):** RDKit descriptors (MolWt, LogP, H-bond donors/acceptors) encoded in a ZZFeatureMap, with **state fidelity** mapped to high/moderate/low risk. Streamlit, optional IBM hardware, and a benchmark.py "to compare quantum vs classical" — [Devpost](https://devpost.com/software/q-cure-quantum-drug-interaction-predictor)
  - **Finbubu:** QAOA portfolio optimisation plus QML forecasting on Yahoo Finance / Alpha Vantage data, with a React front end. It claims to surpass "classical methods in speed and scalability" — [Devpost](https://devpost.com/software/finbubu)
  - **Q-MediScan:**
    - Model: a 6-qubit, 72-parameter VQC (Classiq SDK) on the **UCI Breast Cancer Wisconsin dataset (569 samples)**, with ZNE and readout mitigation.
    - Claims: "**37.8% improvement in pattern detection over classical methods**", "16.5 months earlier detection", "10.6 lives saved per 1000 patients" and "medical-grade reliability".
    - [Devpost](https://devpost.com/software/q-mediscan)
  - **EntangleMe:** a teleportation "chat" that sends one bit via a simulated circuit. It claims "security that no classical encryption can match" — [Devpost](https://devpost.com/software/entangleme)
  - **Medical image QCNN/HQCNN** (details not fetched) — [gallery](https://cqhack25.devpost.com/project-gallery)

**Qollab Spring 2026 cohort, application-flavoured (FUNDED, not winners)** — [Qollab cohort](https://qollab.xyz/explore/spring-2026-cohort):
- **QuantumRegimeRadar:** quantum kernels for market-regime detection on real historical data, **against a GARCH baseline**. The stated aim is to show "where quantum kernels help and where they do not".
- **Qatalyst Game:** QAOA vehicle routing raced against a classical solver on live IonQ hardware.
- **Quantum Systemic Oracle:** a systemic-risk feed (Qollab flags it as high-risk).
- Qollab's editorial notes value an honest case for why "a simulator falls short", and teams that ship.

### Inferences
- Across expert-judged venues (NQCC, BMW, Airbus, Deloitte, Braket/QHack), the winners show the same pattern:
  1. A **named end-user problem**.
  2. A **standard formulation**: QUBO, a copula, Ax=b, or an energy surface.
  3. A **small instance actually run** (2-25 qubits).
  4. An **explicit classical comparator**.
  5. A **scaling/feasibility section** that says what hardware the full problem needs.
- **KL Divergents (NQCC 2024 1st) is the closest template for Qollab's Quantum Impact theme.** It extended a published **IonQ** application paper (QCBM copulas; first author Daiwei Zhu, who also writes IonQ's iQuHACK prompts), added a methodological improvement (randomized KL loss for data efficiency), benchmarked against classical models, and ran inference on trapped-ion hardware.

### Gaps
- Not found:
  - Team names and methods for the NQCC 2025 winners (only use cases are listed).
  - Project details for 2024-2026 iQuHACK industry winners beyond Moody's and Social Impact.
  - The QuEra, Quantinuum and Classiq challenge topics for 2024 and 2025.
  - Descriptions of the 2026 IQM and Quantum Rings challenges.
- No reliable data on application winners at Qiskit Fall Fest, Qiskit Hackathon Global/Europe/Korea, the Classiq Coding Competition, Q-CTRL challenges, QuEra/Harvard challenges, Quantum Coalition Hack 2023-2025 or FLIQ 2025 innovation-track winners (only a University of Tokyo Science-category win was found — [U Tokyo (via search snippet)](https://www.chem.s.u-tokyo.ac.jp/news/jp/jp-awards-s/news3694)), TreeHacks or HackMIT. The 2022 Bitcamp IonQ quantum track was individual challenge completion, not projects — [IonQ blog (via search snippet)](https://www.ionq.com/blog/april-22-2022-ionq-sponsors-bitcamp)
- Unitary Fund application microgrants: not researched in depth. The grants page lists no individual recipients (per prior notes).
- Deloitte 2022 winner Quantimize: the repo has no placement statement. The match to the winning team rests on the README's "team Quantimize" plus the kipark winners snippet.

---

## Key Question 1: Which application domains and methods win most often, and at what scale?

### Takeaway
**Combinatorial optimization via QUBO** (QAOA, annealing or hybrid solvers) is the most common winning applied format: logistics, routing, network coverage, portfolio, loading and maintenance scheduling. **Chemistry/materials VQE** dominates chemistry-specific tracks and the grand challenges. **Generative or kernel QML** wins when it is tied to a domain-specific data problem and rigorous benchmarking (risk copulas, biomarkers), but generic "QML beats classical" classifiers win only at low-bar events. Hackathon-scale winners run **3-25 qubits** and tiny instances. The grand challenges require **>50 qubits at depth 10³-10⁴** (Q4Bio) or fault-tolerant resource estimates (XPRIZE).

### Cited Findings
- **Optimization / QUBO winners:**
  - Airbus 2020 (aircraft loading, annealing) — [Reply](https://www.reply.com/en/newsroom/news/machine-learning-reply-wins-the-airbus-quantum-computing-challenge)
  - BMW 2021 sensor placement (MaxCover) and vehicle configuration (MaxSAT) — [AWS](https://aws.amazon.com/blogs/quantum-computing/winners-announced-in-the-bmw-group-quantum-computing-challenge)
  - NQCC 2023 3rd (vaccination-centre set cover) — [NQCC 2023](https://www.nqcc.ac.uk/wp-content/uploads/2024/04/NQCC_Quantum-Hackathon-2023_Technical-report.pdf)
  - NQCC 2024 2nd (BT vertex cover) — [NQCC 2024](https://nqcc.ac.uk/wp-content/uploads/2025/04/NQCC_Quantum-Hackathon-2024_Technical-report.pdf)
  - NQCC 2025 1st (road-maintenance closures) and 2nd (3D bin packing) — [NQCC 2025](https://www.nqcc.ac.uk/uk-quantum-hackathon-2025)
  - QHack 2022 Finance/QAOA/Entrepreneurship and QHack 2023 Braket (Avocados portfolio) — [PennyLane 2022](https://pennylane.ai/blog/2022/03/qhack-2022-the-one-of-a-kind-celebration-of-quantum-computing/); [AWS 2023](https://aws.amazon.com/blogs/quantum-computing/announcing-the-amazon-braket-challenge-winners-of-the-qhack-2023-hackathon)
  - iQuHACK 2024 Moody's (mean-VaR portfolio, annealing) — [Yale Physics (via search snippet)](https://physics.yale.edu/node/7275)
  - BIG Q 2023 technical winner (biomanufacturing, annealing) — [CQE](https://chicagoquantum.org/news/big-q-hackathon-demonstrated-key-quantum-progress-collaboration-between-tech-and-industry)
  - CQhack25 Quantum Route Optimizer — [Devpost](https://devpost.com/software/quantum-route-optimizer)
- **NQCC organizers on annealers:** "One particular theme that emerged was the usefulness of quantum annealers ... we saw many teams turn to the D-Wave hardware once they had formulated a QUBO problem" — [NQCC 2023 report](https://www.nqcc.ac.uk/wp-content/uploads/2024/04/NQCC_Quantum-Hackathon-2023_Technical-report.pdf)
- **Simulation / linear algebra / Monte Carlo winners:**
  - NQCC 2023 1st (CVQLS/QSVT linear solver) and 2nd (QAE/quantum sampling for particle transport) — [NQCC 2023](https://www.nqcc.ac.uk/wp-content/uploads/2024/04/NQCC_Quantum-Hackathon-2023_Technical-report.pdf)
  - BMW 2021 PDEs (differentiable quantum circuits) — [AWS](https://aws.amazon.com/blogs/quantum-computing/winners-announced-in-the-bmw-group-quantum-computing-challenge)
  - Airbus-BMW 2024 Hamburg (fluid/sound) — [AWS](https://aws.amazon.com/blogs/quantum-computing/winners-announced-in-the-airbus-bmw-group-quantum-computing-challenge)
  - QHack 2024 Curious Turtles (PDE via Hamiltonian simulation) — [PennyLane](https://pennylane.ai/blog/2024/03/qhack-2024-highlights/)
  - XPRIZE finalist QuantumForGraphproblem (linear systems) — [Google blog](https://blog.google/technology/research/google-gesda-xprize-quantum-applications-finalists/)
- **Chemistry / materials VQE winners:**
  - Deloitte 2023 (EcoQult, JetiX, QuantuX) — [TQI](https://thequantuminsider.com/2023/05/08/quantum-climate-challenge-team-ecoqult-wins-the-deloittes-quantum-climate-challenge/)
  - QHack 2023 chemistry (jetix carbon capture; BeH2 VQE) — [PennyLane](https://pennylane.ai/blog/2023/04/qhack-2023-highlights/)
  - Airbus-BMW 2024 USC smart coating — [AWS](https://aws.amazon.com/blogs/quantum-computing/winners-announced-in-the-airbus-bmw-group-quantum-computing-challenge)
  - 5 of 7 XPRIZE finalists target materials or molecular simulation — [Google blog](https://blog.google/technology/research/google-gesda-xprize-quantum-applications-finalists/)
  - The Q4Bio winner and 3 of its 5 described finalists are chemistry — [IBM](https://www.ibm.com/quantum/blog/q4bio-finalists)
- **QML / generative winners:**
  - NQCC 2024 1st (QCBM copula for risk) and 3rd (variational time-series) — [NQCC 2024](https://nqcc.ac.uk/wp-content/uploads/2025/04/NQCC_Quantum-Hackathon-2024_Technical-report.pdf)
  - NQCC 2025 3rd (diabetes QML) — [NQCC 2025](https://www.nqcc.ac.uk/uk-quantum-hackathon-2025)
  - BMW 2021 QC Ware (image classification, no claimed present-day advantage) — [AWS](https://aws.amazon.com/blogs/quantum-computing/winners-announced-in-the-bmw-group-quantum-computing-challenge)
  - Airbus-BMW 2024 Quandela qGAN — [AWS](https://aws.amazon.com/blogs/quantum-computing/winners-announced-in-the-airbus-bmw-group-quantum-computing-challenge)
  - QHack 2023 QuantuMother (analog quantum kernel for carcinogenicity) — [AWS](https://aws.amazon.com/blogs/quantum-computing/announcing-the-amazon-braket-challenge-winners-of-the-qhack-2023-hackathon)
  - Q4Bio Infleqtion (biomarkers) — [IBM](https://www.ibm.com/quantum/blog/q4bio-finalists)
  - CQhack25 Q-MediScan, Q-Cure and medical QCNN — [gallery](https://cqhack25.devpost.com/project-gallery)
- **Application-sector frequency (NQCC 2024):** 6 QML, 5 optimisation and 2 simulation use cases, across 10 sectors (telecom, energy, cybersecurity, healthcare, manufacturing, insurance, finance, law enforcement, aerospace, logistics) — [NQCC 2024](https://nqcc.ac.uk/wp-content/uploads/2025/04/NQCC_Quantum-Hackathon-2024_Technical-report.pdf)
- **Scale of hackathon winners:**
  - Rolls-Royce: 4x4 linear systems on hardware, 16x16 in simulation — [NQCC 2023](https://www.nqcc.ac.uk/wp-content/uploads/2024/04/NQCC_Quantum-Hackathon-2023_Technical-report.pdf)
  - Vaccination: N≤4, V=2 — [same](https://www.nqcc.ac.uk/wp-content/uploads/2024/04/NQCC_Quantum-Hackathon-2023_Technical-report.pdf)
  - NHS forecaster: 25-qubit QPU — [NQCC 2024](https://nqcc.ac.uk/wp-content/uploads/2025/04/NQCC_Quantum-Hackathon-2024_Technical-report.pdf)
  - CGI energy PQC: 6 qubits — [same](https://nqcc.ac.uk/wp-content/uploads/2025/04/NQCC_Quantum-Hackathon-2024_Technical-report.pdf)
  - jetix VQE: 5 qubits; Avocados: ≤24 assets with headline results at 10 assets — [AWS](https://aws.amazon.com/blogs/quantum-computing/announcing-the-amazon-braket-challenge-winners-of-the-qhack-2023-hackathon)
  - IonQ copula paper: 3-4 variable copulas — [arXiv 2206.11937 (via search snippet)](https://arxiv.org/abs/2206.11937)
  - TU Delft: 8-10 plies — [AWS](https://aws.amazon.com/blogs/quantum-computing/winners-announced-in-the-airbus-bmw-group-quantum-computing-challenge)
  - CQhack25 VRP: 3 nodes — [Devpost](https://devpost.com/software/quantum-route-optimizer)
  - Q-MediScan: 6 qubits — [Devpost](https://devpost.com/software/q-mediscan)
- **Scale at grand challenges:**
  - Q4Bio required >50 qubits at depth 10³-10⁴. The winner used up to 100 qubits; Nottingham used a 120-qubit device — [IBM](https://www.ibm.com/quantum/blog/q4bio-finalists)
  - XPRIZE Phase II requires "detailed resource estimates, including architectures, logical qubits, and error-correction assumptions" — [XPRIZE](https://www.xprize.org/prizes/qc-apps)

### Inferences
- Under Qollab's limits (about 24 simulator qubits, ≤29 with IonQ Forte noise models), every hackathon-scale applied winner above would have fit. Problem size is not a differentiator; **benchmark quality and framing are**.
- Repeat winners specialize. jetix won Deloitte 2023 2nd, QHack 2023 Chemistry 1st and QHack 2024 NVIDIA 1st, all with VQE efficiency tricks on climate chemistry. Avocados won QHack 2022 Finance 1st and QHack 2023 Braket, both with better constraint encodings for portfolio QUBOs. Winning applied work often reads as **"one well-chosen methodological improvement on a known application pipeline"**, not a new application from scratch.
- Trapped-ion-friendly applied methods with IonQ provenance include QCBM copulas for risk aggregation (IonQ/GE), varQITE for MaxCut (prior notes) and dense all-to-all ansätze. They line up with sponsor interests.

### Gaps
- No systematic count across all events. The "most common" ranking is based on the events cataloged here.
- Qubit counts for many winners (NQCC 2025, Deloitte 2024, BMW 2021) are not published.

---

## Key Question 2: How did winners handle classical baselines and claims of advantage? Did honest "no advantage yet" projects win?

### Takeaway
**Yes: honest "no advantage yet, but here is the scaling or resource story" projects win repeatedly at expert-judged events.**
- **BMW 2021:** two of four winners said outright that classical wins today (Accenture; QC Ware, per the judges).
- **Deloitte 2022:** the 1st-place repo concludes that the classical genetic algorithm is best for now.
- **NQCC 2023:** 2nd place reported large deviations from analytical results.
- **NQCC 2024:** 3rd place used synthetic data.

What these winners share is **an explicit comparator and a credible scaling/feasibility analysis**. The NQCC 2024 judges named rigorous benchmarking as the deciding factor. At grand-challenge level, Q4Bio's own $5M advantage prize went (reportedly) unawarded. Over-claiming does win at low-bar student events (CQhack25), but no expert panel was found rewarding it.

### Cited Findings
- **BMW 2021:**
  - Accenture: "Classical custom algorithms performed best today", with plugins for future quantum methods.
  - QC Ware: judges wrote "While today QML will not be able to solve this classification task better than established classical methods", and valued that the work clarifies future potential.
  - Qu&Co: benchmarked against exact solutions and classical neural nets.
  - 1QBit/NTT: included a fault-tolerant scaling analysis.
  - [AWS](https://aws.amazon.com/blogs/quantum-computing/winners-announced-in-the-bmw-group-quantum-computing-challenge)
- **Deloitte 2022, Quantimize (1st):** baselines were straight-line routes and a classical GA. Conclusion: the classical GA is "the best choice for a large dataset at present", and the quantum GA has "no clear advantage" — [Quantimize GitHub](https://github.com/fjelljenta/Quantum-Challenge)
- **Deloitte 2023, EcoQult (1st):** compared classical and quantum algorithms on "resource requirements, run-time, and solution accuracy". It used classical estimates plus VQE corrections at scale — [TQI](https://thequantuminsider.com/2023/05/08/quantum-climate-challenge-team-ecoqult-wins-the-deloittes-quantum-climate-challenge/)
- **Airbus-BMW 2024:**
  - TU Delft: its *quantum-inspired classical* DMRG heuristic "outperformed existing classical solutions in many cases".
  - 4colors: a solver that runs classically now with quantum plug-ins.
  - [AWS](https://aws.amazon.com/blogs/quantum-computing/winners-announced-in-the-airbus-bmw-group-quantum-computing-challenge)
- **NQCC 2024 judging:**
  - Criterion 1 explicitly includes "**comparison with the best classical solution**" and "the extent to which teams have attempted to verify their solution".
  - Criterion 3 asks "What happens when the toy problem is extended? ... What hardware capabilities would be required for a full-scale, realistic solution?"
  - [NQCC 2024 report](https://nqcc.ac.uk/wp-content/uploads/2025/04/NQCC_Quantum-Hackathon-2024_Technical-report.pdf)
- **NQCC 2024 judge quotes:** the winners had a "structured approach to comparing its results against other possible solutions" (Stanisic). BT's Cathy White said the students "don't claim quantum advantage without proper evidence" — [Physics World](https://physicsworld.com/a/quantum-hackathon-makes-new-connections/). A commentary said the "judges emphasised rigorous benchmarking as a key component in the winning team's submission" — [Mondaq (via search snippet)](https://www.mondaq.com/uk/patent/1523376/nqccs-2024-quantum-hackathon-is-a-success)
- **NQCC 2023, Jacobs (2nd):** "large variation from the analytical solutions", attributed to the lack of error correction, with future extensions listed. The vaccination team (3rd) flagged "how the approach scales with problem size" as unresolved — [NQCC 2023 report](https://www.nqcc.ac.uk/wp-content/uploads/2024/04/NQCC_Quantum-Hackathon-2023_Technical-report.pdf)
- **Honest negative results that did not place:** Johnson Matthey reported "the classical approach outperformed the quantum approach" (SHAP-based selection beat the D-Wave CQM/NLM selection) and that both gave only "slight improvements" over no feature selection — [NQCC 2024 report](https://nqcc.ac.uk/wp-content/uploads/2025/04/NQCC_Quantum-Hackathon-2024_Technical-report.pdf)
- **Airbus 2020 finalists** made big asymptotic claims ("order of magnitude", O(polylog N)) but conceded fault tolerance and QRAM were needed. The finalist that included **qubit estimates and near-term feasibility** (Montevideo) is noted explicitly. The *winner* was the more practical annealing loading optimiser — [TQI](https://thequantuminsider.com/2020/10/22/airbus-names-its-five-finalists-for-quantum-computing-challenge/); [Reply](https://www.reply.com/en/newsroom/news/machine-learning-reply-wins-the-airbus-quantum-computing-challenge)
- **XPRIZE rules:**
  - Phase II requires benchmarking "against state-of-the-art classical methods" and resource estimates.
  - Finalist selection weighed "benchmarking against classical methods rather than relying only on asymptotic scaling arguments".
  - Criterion C is "Strength of evidence supporting claims".
  - [XPRIZE](https://www.xprize.org/prizes/qc-apps)
- **Q4Bio:**
  - The $2M prize needs only a "clear trajectory toward quantum advantage". The winner reports "a scalable path to future quantum advantage", not a demonstrated advantage — [TQI](https://thequantuminsider.com/2026/04/16/wellcome-leap-quantum-for-bio-challenge-prize/)
  - The Stanford finalist noted that classical biochemistry methods have a long head start. Infleqtion compared its hybrid against a purely classical pipeline — [IBM](https://www.ibm.com/quantum/blog/q4bio-finalists)
- **Over-claiming that won at a low-bar event (CQhack25):**
  - Q-MediScan claimed "37.8% improvement ... over classical methods", "10.6 lives saved per 1000 patients" and "medical-grade reliability" for a 6-qubit VQC on the 569-sample UCI dataset — [Devpost](https://devpost.com/software/q-mediscan)
  - EntangleMe claimed teleportation-based messaging gives "security that no classical encryption can match" — [Devpost](https://devpost.com/software/entangleme)
  - Finbubu claimed to surpass classical methods "in speed and scalability" — [Devpost](https://devpost.com/software/finbubu)
- **iQuHACK 2024 Moody's winner:** projected "up to 6% per business quarter" returns, a self-reported projection — [Yale Physics (via search snippet)](https://physics.yale.edu/node/7275)

### Inferences
- For Qollab's "strong classical baseline + measurable quantum step" theme, the **winning posture is: an honest comparator, one metric where the quantum step is measurably better or more resource-efficient** (fewer qubits, higher success probability, better KL divergence, faster convergence), **plus a scaling and resource analysis.** It is not "quantum beats classical". Examples:
  - Avocados' 1400x success-probability gain was measured *against the standard quantum encoding*, not against classical.
  - jetix's gain was measured *against the full-parameter ansatz*.
- Being honestly beaten by the classical baseline is acceptable if the team **explains why** (encoding, depth, noise) and **what would change it** (Jacobs, Quantimize). It is not acceptable to stop at "classical won" with no analysis (Johnson Matthey did not place).
- IonQ and Qollab judges are quantum experts, so CQhack25-style marketing claims are likely to cost points on Technical Execution and Documentation. This is an inference; no Qollab judge statement was found.

### Gaps
- No scoring sheets show how much weight benchmarking carried relative to other criteria in any specific decision.
- The KL Divergents slides, code and exact baseline metrics (which classical copulas, what KL values) were not found. The report says a scientific publication was in preparation.

---

## Key Question 3: What do judges, organizers and retrospectives say distinguishes winning applied projects?

### Takeaway
Published rubrics and judge comments converge on six things:
1. **Solving the end-user's actual problem**, after taking time to understand it.
2. **Rigorous benchmarking and verification against the best classical solution.**
3. **A scaling and feasibility investigation**: what happens beyond the toy, and what hardware is needed.
4. **Creativity or novelty relative to the use case.**
5. **Clear presentation and Q&A**: the team must show it understands its own approach.
6. **Business or societal relevance**, including responsible-use considerations at NQCC.

Multi-month industry challenges add comprehensibility, end-to-end workflow and benefit to the sponsor.

### Cited Findings
- **NQCC 2024 rubric** — [NQCC 2024 report](https://nqcc.ac.uk/wp-content/uploads/2025/04/NQCC_Quantum-Hackathon-2024_Technical-report.pdf). Co-developed with judges Oliver Brown, Animesh Datta, Sarah Harris and Stasja Stanisic; total 55 points:
  - (1) Success of the solution for the use case: /10, including hardware, problem definition, "comparison with the best classical solution" and verification.
  - (2) Creativity and novelty given the use case: /10.
  - (3) Investigation into scaling and feasibility: /10.
  - (4) Responsible and ethical quantum computing: /10 (stakeholders, maximizing benefits and mitigating harms, using NQCC's "Quantum STATES" principles, which include "Manage expectations, cutting through overhype" and "Be open and honest about the capabilities and limitations").
  - (5) Presentation (clarity, engagement, length; down-scored if over 10 minutes): /10.
  - (6) Q&A ("Have they fully understood their problem and the approach they took?"): /5.
- **NQCC 2023 rubric:** success for the allocated resources; creativity and novelty; investigation into scaling; responsible and ethical QC; presentation clarity; presentation engagement and length; answers to questions — [NQCC 2023 report](https://www.nqcc.ac.uk/wp-content/uploads/2024/04/NQCC_Quantum-Hackathon-2023_Technical-report.pdf)
- **NQCC judge and mentor lessons (2024)** — [Physics World](https://physicsworld.com/a/quantum-hackathon-makes-new-connections/):
  - Understand the problem deeply before building.
  - Benchmark rigorously.
  - Be ready to switch platforms (White's team used both a D-Wave annealer and gate-model QAOA).
  - Use the extra time to consolidate results.
  - Consider social impact, explainability and transparency.
- **NQCC 2024 organizer note:** teams had primary and secondary hardware allocations, and "Access to quantum emulators meant that participants could compare 'ideal' emulated results to those from real quantum hardware", while some teams benchmarked across providers — [NQCC 2024 report](https://nqcc.ac.uk/wp-content/uploads/2025/04/NQCC_Quantum-Hackathon-2024_Technical-report.pdf)
- **BMW 2021 criteria:** comprehensibility, feasibility, scalability, innovation, benefit to BMW. Judges praised a "holistic workflow" (Accenture), a "detailed, NISQ-ready strategy" (Qu&Co) and a "comprehensive solution strategy" (1QBit/NTT) — [AWS](https://aws.amazon.com/blogs/quantum-computing/winners-announced-in-the-bmw-group-quantum-computing-challenge)
- **XPRIZE criteria:** (A) projected magnitude of real-world impact; (B) estimated quantum resources for advantage; (C) strength of evidence; (D) novelty ("thought delta") — [XPRIZE](https://www.xprize.org/prizes/qc-apps). Semifinalists were picked for "plausibility and quality of their ideas" — [TQI](https://thequantuminsider.com/2025/10/21/xprizes-quantum-for-real-world-impact-announces-semi-finalists/)
- **Amazon Braket at QHack 2023:** "scientific and technical merit, depth of use of the quantum computing software and hardware stack, and potential for onward development". Each winner was praised for **one concrete technical contribution**: implementing VQE for climate, learning analog Hamiltonian simulation, or cutting qubit counts — [AWS](https://aws.amazon.com/blogs/quantum-computing/announcing-the-amazon-braket-challenge-winners-of-the-qhack-2023-hackathon)
- **iQuHACK 2023 Covalent x IBM:** technical 30%, originality 25%, usefulness and complexity 25%, presentation 20%. The brief demanded a real-world application usable by ordinary users — [repo](https://github.com/mannypaeza/2023_CovalentxIBM)
- **Moody's 2025:** the winners "stood out in both their work and their presentations". The 1st-place team "used rich visualizations to show their understanding" — [Moody's](https://www.moodys.com/web/en/us/insights/quantum/mit-hackathon-recap.html). The **Moody's 2024 brief required an end-to-end optimizer plus a business pitch** — [Yale Physics (via search snippet)](https://physics.yale.edu/node/7275)
- **BIG Q 2023:** split into a technical phase (judged by quantum experts) and a business phase (judged by CEOs and investors). Organizers stressed iteration between users and developers: "most valuable use cases haven't been found yet" — [CQE](https://chicagoquantum.org/news/big-q-hackathon-demonstrated-key-quantum-progress-collaboration-between-tech-and-industry)
- **Deloitte 2023:** Renata Jovanovic said the winning approach showed "in a very direct way" what quantum computing already offers — [TQI](https://thequantuminsider.com/2023/05/08/quantum-climate-challenge-team-ecoqult-wins-the-deloittes-quantum-climate-challenge/)
- **Qollab cohort editorial values:** a clear case for why "a simulator falls short", honest rather than hyped framing, and the ability to ship — [Qollab cohort](https://qollab.xyz/explore/spring-2026-cohort)
- **Q4Bio program director:** the value was "a much clearer understanding of where quantum can create value, where it cannot" — [TQI](https://thequantuminsider.com/2026/04/16/wellcome-leap-quantum-for-bio-challenge-prize/)
- **Other rubrics with the same shape:**
  - NTU-IBM 2026: Originality and Uniqueness; Usefulness and Complexity; Potential Quantum Community Benefit; Presentation and Team Collaboration — [NTU (via search snippet)](https://quantum.ntu.edu.tw/?p=10159)
  - CIC-IPN 2021: technical challenge; impact ("industrial application"); creativity; presentation — [arXiv 2302.12119](https://arxiv.org/abs/2302.12119)

### Inferences
- Mapping NQCC's rubric onto Qollab's four traits:
  - "success + classical comparison + verification" → **Technical Execution**.
  - "creativity/novelty given the use case" → **Novelty & Creativity**.
  - "scaling/feasibility + responsible impact" → **Impact Potential**.
  - "presentation + Q&A" → **Documentation Quality**, since Qollab judges read the README and video instead of asking questions live.
- Because Qollab judges press Run, the "verification" expectation becomes a **reproducible notebook** that regenerates the baseline-vs-quantum table and plots, with seeds fixed and runtime short.
- A "scaling and resources" section is the cheapest high-value addition. It costs no qubits and appears in every serious rubric (NQCC criterion 3, BMW scalability, XPRIZE criterion B). Contents: qubits vs. problem size, gate counts after transpiling to IonQ native gates, and the projected logical-qubit needs.

### Gaps
- No Qollab-specific statement on how much weight each of the four traits carries.
- Judge commentary exists for only a handful of winners: KL Divergents, the BMW winners, the Braket winners and the Moody's 2025 1st place.

---

## Key Question 4: What are the recurring failure modes?

### Takeaway
Recurring weaknesses in applied entries:
1. **Toy or synthetic data** standing in for the real dataset.
2. **Instances so small** that a brute-force or classical solver is trivial, presented without a scaling story.
3. **Missing or weak baselines**, or baselines that are other quantum methods only.
4. **Over-claiming advantage**: exponential parallelism, "explores every route simultaneously", lives-saved projections.
5. **Wrong-algorithm fits**, discovered late (QMCMC for distributions, QNN untrainable).
6. **QML that is simply beaten by classical methods.**
7. **Hardware or compile blockers** (QSVT that would not compile).
8. **Asymptotic claims that require QRAM or fault tolerance** with no near-term path.

Several of these still placed at expert events when disclosed honestly. Undisclosed versions read as hype.

### Cited Findings
- **Synthetic data:** the NHS team (NQCC 2024 3rd) "generated a fake time series representing linear growth" rather than using A&E data, because of qubit limits — [NQCC 2024 report](https://nqcc.ac.uk/wp-content/uploads/2025/04/NQCC_Quantum-Hackathon-2024_Technical-report.pdf)
- **Wrong-algorithm fit:** quantum MCMC "proved unsuitable" because it estimates means, not full distributions — [same](https://nqcc.ac.uk/wp-content/uploads/2025/04/NQCC_Quantum-Hackathon-2024_Technical-report.pdf). Quantimize's QNN "can't be trained with the currently available qubits" — [Quantimize GitHub](https://github.com/fjelljenta/Quantum-Challenge)
- **Classical wins:** the Johnson Matthey feature selection was beaten by SHAP-based selection — [NQCC 2024 report](https://nqcc.ac.uk/wp-content/uploads/2025/04/NQCC_Quantum-Hackathon-2024_Technical-report.pdf). The QC Ware QML winner conceded that classical is better today — [AWS](https://aws.amazon.com/blogs/quantum-computing/winners-announced-in-the-bmw-group-quantum-computing-challenge)
- **Hardware and compile blockers:** PennyLane's QSVT "did not compile to QASM code" for hardware (Rolls-Royce), and hardware was limited to 4x4 systems — [NQCC 2023 report](https://www.nqcc.ac.uk/wp-content/uploads/2024/04/NQCC_Quantum-Hackathon-2023_Technical-report.pdf). The BT QAOA had "limited opportunity to test it on the real QPU" — [NQCC 2024 report](https://nqcc.ac.uk/wp-content/uploads/2025/04/NQCC_Quantum-Hackathon-2024_Technical-report.pdf)
- **Noise-dominated results:** quantum sampling showed "a large variation from the analytical solutions" (Jacobs) — [NQCC 2023 report](https://www.nqcc.ac.uk/wp-content/uploads/2024/04/NQCC_Quantum-Hackathon-2023_Technical-report.pdf)
- **Encoding blow-up:** the CGI energy team found the qubit count "highly dependent on the encoding scheme". Angle encoding needs one qubit per feature per time step, "potentially requiring several tens of qubits" — [NQCC 2024 report](https://nqcc.ac.uk/wp-content/uploads/2025/04/NQCC_Quantum-Hackathon-2024_Technical-report.pdf). The CQhack25 VRP noted that "Qubit and QUBO size scales exponentially with node and vehicle count leading to small sample sizes" — [Devpost](https://devpost.com/software/quantum-route-optimizer)
- **Over-claiming:**
  - "Quantum algorithms ... can explore every route simultaneously" (VRP) — [Devpost](https://devpost.com/software/quantum-route-optimizer)
  - "Quantum computers can see patterns that classical computers cannot", "37.8% improvement", "10.6 lives saved per 1000 patients" — [Q-MediScan](https://devpost.com/software/q-mediscan)
  - "Security that no classical encryption can match" for one simulated bit — [EntangleMe](https://devpost.com/software/entangleme)
  - These won at CQhack25 but contradict NQCC's "Manage expectations, cutting through overhype" principle — [NQCC 2024 report](https://nqcc.ac.uk/wp-content/uploads/2025/04/NQCC_Quantum-Hackathon-2024_Technical-report.pdf)
- **Asymptotic claims needing FT/QRAM:** Origin Quantum's O(polylog N) CFD (it "says fault-tolerant computing and QRAM are needed for quantum advantage") and Capgemini's "order-of-magnitude" claim. Both were finalists, not winners — [TQI](https://thequantuminsider.com/2020/10/22/airbus-names-its-five-finalists-for-quantum-computing-challenge/)
- **Organizer view of short formats:** NQCC 2023 concluded "it would be beneficial to find a balance between a time-limited event ... and an event with enough time for participants to make satisfying progress", and added a third day in 2024 — [NQCC 2023 report](https://www.nqcc.ac.uk/wp-content/uploads/2024/04/NQCC_Quantum-Hackathon-2023_Technical-report.pdf); [NQCC 2024 report](https://nqcc.ac.uk/wp-content/uploads/2025/04/NQCC_Quantum-Hackathon-2024_Technical-report.pdf)
- **No dataset at all:** many winners describe no dataset. Examples include QuantuMother's lack of a baseline ([AWS](https://aws.amazon.com/blogs/quantum-computing/announcing-the-amazon-braket-challenge-winners-of-the-qhack-2023-hackathon)), and Qatalyst and Quantum Systemic Oracle with no dataset stated ([Qollab cohort](https://qollab.xyz/explore/spring-2026-cohort)). Qollab's Quantum Impact theme explicitly requires a public dataset — [Qollab rules](https://qollab.xyz/programs/hackathon/terms)

### Inferences
- The Qollab Quantum Impact requirements (public dataset, strong classical baseline, measurable quantum step) directly target failure modes 1-4. An entry that uses **real public data**, a **tuned classical baseline** (not a strawman) and a **narrowly defined quantum metric** already beats most historical applied entries on rigor.
- A "fake data because of qubit limits" disclosure placed 3rd at NQCC, but it would likely fail Qollab's dataset requirement. Real data reduced to fit (feature selection or PCA to a few dimensions, a subset of assets or nodes, coarse-grained distributions) is the safer move, with the reduction documented.
- "Classical beats us" is survivable only with diagnosis. Without one, it reads as an unfinished project.

### Gaps
- No published judge statements naming over-claiming as a reason for a loss. The inference rests on rubric language (NQCC STATES) and on which entries placed at expert-judged events.

---

## Key Question 5: Which XPRIZE / Q4Bio / Deloitte / BMW / Airbus / NQCC problem framings could inspire a credible 48-hour Qollab project?

### Takeaway
The most transferable framings combine **a published small-scale quantum method, a public dataset and a standard classical baseline**:
- Copula/QCBM risk aggregation, the NQCC 2024 winner that extends IonQ's own paper.
- Constraint-efficient QUBO encodings for coverage, sensor placement or portfolio problems (BT, BMW, Avocados).
- Small linear-system or PDE solvers with resource estimates (Rolls-Royce, BMW, XPRIZE linear systems).
- VQE efficiency for climate chemistry (Deloitte 2023, jetix).
- Quantum-kernel regime or biomarker detection against GARCH or LASSO (Qollab cohort, Q4Bio Infleqtion).

Grand-challenge framings (XPRIZE, Q4Bio) are useful mainly as **problem statements plus resource-estimation templates**, not as things to reproduce at scale.

### Cited Findings (problem framings with provenance)
- **Insurance and catastrophe risk aggregation with QCBM copulas:** NQCC 2024 1st (Mind Foundry / Aioi), extending IonQ/GE's "Copula-based risk aggregation with trapped ion quantum computers" (3-4 variables) — [NQCC 2024 report](https://nqcc.ac.uk/wp-content/uploads/2025/04/NQCC_Quantum-Hackathon-2024_Technical-report.pdf); [arXiv 2206.11937](https://arxiv.org/abs/2206.11937). Related: copula risk aggregation via orthogonal-series density estimation and QMCI — [arXiv 2404.10624 (via search snippet)](https://arxiv.org/abs/2404.10624)
- **Telecom coverage / vertex cover with equity weighting:** BT, NQCC 2024 2nd. Classical comparators are simulated annealing and MIP, with weighting toward vulnerable communities — [NQCC 2024 report](https://nqcc.ac.uk/wp-content/uploads/2025/04/NQCC_Quantum-Hackathon-2024_Technical-report.pdf)
- **Vehicle sensor placement (MaxCover):** BMW 2021, where classical algorithms are best today — [AWS](https://aws.amazon.com/blogs/quantum-computing/winners-announced-in-the-bmw-group-quantum-computing-challenge)
- **Portfolio with inequality constraints via unbalanced penalization:** QHack 2023 Avocados (10-24 assets; about 1400x success probability vs. slack encoding; ran on IonQ) — [AWS](https://aws.amazon.com/blogs/quantum-computing/announcing-the-amazon-braket-challenge-winners-of-the-qhack-2023-hackathon)
- **Mean-VaR portfolio QUBO:** Moody's 2024 — [Yale Physics (via search snippet)](https://physics.yale.edu/node/7275)
- **TDA / Betti-number bubble early warning:** Moody's 2025 — [Moody's](https://www.moodys.com/web/en/us/insights/quantum/mit-hackathon-recap.html)
- **Market-regime detection with quantum kernels vs. GARCH:** Qollab cohort — [Qollab](https://qollab.xyz/explore/spring-2026-cohort)
- **Linear systems for CFD/FEM (CVQLS, plus QSVT resource path):** NQCC 2023 1st (2x2 to 16x16) — [NQCC 2023 report](https://www.nqcc.ac.uk/wp-content/uploads/2024/04/NQCC_Quantum-Hackathon-2023_Technical-report.pdf). The XPRIZE finalist QuantumForGraphproblem's linear-systems algorithm is the high-end framing — [Google blog](https://blog.google/technology/research/google-gesda-xprize-quantum-applications-finalists/)
- **Monte Carlo particle transport with QAE:** NQCC 2023 2nd — [NQCC 2023 report](https://www.nqcc.ac.uk/wp-content/uploads/2024/04/NQCC_Quantum-Hackathon-2023_Technical-report.pdf)
- **Facility location (vaccination centres) as weighted set cover:** NQCC 2023 3rd — [NQCC 2023 report](https://www.nqcc.ac.uk/wp-content/uploads/2024/04/NQCC_Quantum-Hackathon-2023_Technical-report.pdf)
- **Aircraft cargo loading (knapsack with centre-of-gravity constraints):** Airbus 2020 winner — [Reply](https://www.reply.com/en/newsroom/news/machine-learning-reply-wins-the-airbus-quantum-computing-challenge)
- **Climate-optimal flight routing / contrail avoidance:** Deloitte 2022. Baselines were straight-line routes and a GA; the quantum side was a discretized QUBO — [Quantimize GitHub](https://github.com/fjelljenta/Quantum-Challenge); [LHIND (via search snippet)](https://www.lufthansa-industry-solutions.com/de-en/newsroom-downloads/news/quantum-climate-challenge-2022-team-of-experts-from-lufthansa-industry-solutions-among-the-top-5)
- **CO2 capture chemistry (ion-gas dissociation; MOF binding PES):** Deloitte 2023 and QHack 2023 jetix (5-qubit VQE, parameter freezing) — [TQI](https://thequantuminsider.com/2023/05/08/quantum-climate-challenge-team-ecoqult-wins-the-deloittes-quantum-climate-challenge/); [AWS](https://aws.amazon.com/blogs/quantum-computing/announcing-the-amazon-braket-challenge-winners-of-the-qhack-2023-hackathon)
- **Flood and disaster forecasting with hybrid QML:** Deloitte 2024 — [Imperial](https://imperial.ac.uk/news/253677/imperial-students-deloitte-quantum-climate-challenge)
- **Composite stacking-sequence retrieval:** TU Delft, Airbus-BMW 2024, with a VQA at 8-10 plies plus a quantum-inspired DMRG baseline — [AWS](https://aws.amazon.com/blogs/quantum-computing/winners-announced-in-the-airbus-bmw-group-quantum-computing-challenge)
- **Day-to-night image generation (qGAN) for autonomy training:** Quandela, Airbus-BMW 2024 — [same](https://aws.amazon.com/blogs/quantum-computing/winners-announced-in-the-airbus-bmw-group-quantum-computing-challenge)
- **Road-maintenance closure scheduling; 3D bin packing; diabetes QML:** NQCC 2025 top 3 — [NQCC 2025](https://www.nqcc.ac.uk/uk-quantum-hackathon-2025)
- **Biomarker discovery from cancer data (hybrid optimization vs. a classical pipeline):** Q4Bio Infleqtion finalist — [IBM](https://www.ibm.com/quantum/blog/q4bio-finalists)
- **Protein-protein-interaction hypergraph community detection:** XPRIZE finalist The QuMIT — [Google blog](https://blog.google/technology/research/google-gesda-xprize-quantum-applications-finalists/)
- **Photodynamic-therapy photosensitizer excited states:** Q4Bio winner (100 qubits) and XPRIZE Xanadu — [IBM](https://www.ibm.com/quantum/blog/q4bio-finalists); [Google blog](https://blog.google/technology/research/google-gesda-xprize-quantum-applications-finalists/)
- **Carcinogenicity of compounds as graphs (quantum evolving kernel):** QHack 2023 QuantuMother — [AWS](https://aws.amazon.com/blogs/quantum-computing/announcing-the-amazon-braket-challenge-winners-of-the-qhack-2023-hackathon)
- **Energy price/demand forecasting on public ELEXON GB data with a 6-qubit PQC:** NQCC 2024 (unplaced, but the dataset is public) — [NQCC 2024 report](https://nqcc.ac.uk/wp-content/uploads/2025/04/NQCC_Quantum-Hackathon-2024_Technical-report.pdf)

### Inferences (candidate 48-hour Qollab "Quantum Impact" designs; these are my suggestions, not sourced facts)
1. **Catastrophe-risk copula with a QCBM (highest sponsor alignment).**
   - Data: public losses (e.g., NOAA billion-dollar disaster data or an insurance-loss proxy) plus a public equity index.
   - Baselines: Gaussian, Student-t and empirical-beta copulas.
   - Quantum step: a QCBM on 2-4 variables × 3-4 bits each (≤16 qubits), trained with KL or MMD and the randomized-split trick.
   - Metrics: KL to the empirical distribution, tail-dependence error, VaR/TVaR error.
   - Extra: an IonQ Forte noise-model run, plus a resource table for more variables and bits.
   - Why: it directly echoes the NQCC 2024 winner and IonQ's own paper.
2. **Equity-weighted coverage (vertex cover / facility location) on a real public network or census map.**
   - Baselines: MIP via OR-Tools/PuLP, greedy and simulated annealing.
   - Quantum step: QAOA with unbalanced penalization vs. slack encodings. Metrics: approximation ratio, P(optimal), qubit savings.
   - Optional: compare a heavy-hex vs. all-to-all transpile (two-qubit gate counts) to show the IonQ angle.
3. **Constrained portfolio on public price data (mean-variance or CVaR).**
   - Baseline: exact or MIP.
   - Quantum step: QAOA/varQITE with unbalanced penalization. Report P(optimal) and the qubit saving vs. slack, following Avocados.
   - Risk: it is a crowded topic, so novelty must come from the constraint encoding or the risk measure.
4. **A small-PDE or heat-equation linear solve (VQLS)** against `numpy.linalg.solve`, with condition-number scaling and a QSVT resource estimate. Follows Rolls-Royce and XPRIZE.
5. **Quantum-kernel regime detection vs. GARCH/HMM** on public index data, honestly reporting where kernels help or fail (QuantumRegimeRadar framing). Risk: kernel concentration and dequantization critiques.
6. **CO2-ion binding curve with VQE efficiency tricks** (parameter freezing, term grouping) against exact diagonalization. Follows Deloitte 2023 and jetix. Risk: Qollab's in-browser environment may lack PySCF-style integral generation; precomputed Hamiltonians would need to ship with the project.

### Gaps
- Not verified: which public datasets fit each framing in Qollab's in-browser environment (package availability, file upload limits).
- The NQCC 2025 winners' methods (road closures, bin packing, diabetes QML) are unpublished, so those framings carry no method template.
- Not checked whether newer critiques (e.g., dequantization of quantum-kernel or recommendation-style QML) apply to specific framings above. This should be checked before choosing a QML framing.
