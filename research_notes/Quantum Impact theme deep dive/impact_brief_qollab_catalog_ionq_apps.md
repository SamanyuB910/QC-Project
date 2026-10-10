# Quantum Impact Theme: Brief, Qollab Application Catalog, and IonQ's Application Portfolio

Snapshot: 2026-10-09, 16:55–17:17 ET. That is about 1¾ hours before the 19:00 ET kickoff, so nothing "at or after kickoff" existed yet. A final re-check at 17:17 ET found the hub, how-it-works, terms, announcements and GT site text unchanged, and no new projects (see Q1 Gaps for a re-check recipe).

Sources:
- Raw SSR HTML of qollab.xyz pages, fetched with curl
- Qollab's public JSON API: `https://api.qollab.xyz/api/project/popular?limit=30&next=<cursor>`, plus `/api/project/id/<id>/versions/head` for each project's write-up and main file
- The Qollab forum JSON
- The Georgia Tech node site
- IonQ newsroom, blog and investor pages
- arXiv abstracts
- The Quantum Insider (TQI), Quantum Computing Report (QCR) and critical Substacks

Labels: **[Confirmed]** means stated in a primary source or read from project code/API. **[Inferred]** means my reasoning. Some IonQ details come from search-engine summaries of pages I could not open in full; those are marked "(via search summary)".

Prior notes I did not repeat (rules, prizes, runtime, backends, Unlocked inventory) are here:
- `research_notes/Qollab IonQ hackathon track/qollab_ionq_track.md`
- `research_notes/Quantum Unlocked theme deep dive/theme_brief_and_qollab_platform.md`

---

## Q1. What exactly does the Impact brief require, what examples or expectations does it give, and were any new problem statements or datasets released at kickoff?

### Takeaway
The authoritative Quantum Impact brief is on the Rules & terms page. It sets five explicit requirements:
1. a real industry challenge (examples: logistics, manufacturing, space, finance, energy)
2. a hybrid quantum-classical approach
3. a relevant **public dataset**
4. a **strong classical baseline**
5. a quantum subroutine shown to make a **measurable** difference (solution quality, efficiency, accuracy or "other measurable gains")

As of 17:10 ET Oct 9, no theme problem statements, IonQ challenge datasets or kickoff materials had been published on any public channel I could check: the Qollab site, API, forum and announcements; the GT site; and the web.

The best public evidence of what Qollab staff mean by "strong baseline" is their own Learn content. Their QAOA explainer dissects Quantum Courier's headline Impact-style result and shows that a greedy classical heuristic beats one-layer QAOA on that very instance.

### Cited Findings
**Verbatim brief text (three lengths), confirmed unchanged at 16:56 ET Oct 9**
- [Confirmed] **Full brief (Rules & terms)**: "Projects should leverage quantum computing's unique attributes and cover one or more of the following themes: **Quantum Impact** — solve real-world problems with quantum + classical computing. Take on a real challenge in logistics, manufacturing, space, finance, energy, or another industry using a hybrid quantum-classical approach. Choose a relevant public dataset, build a strong classical baseline, then identify where a quantum subroutine can make a difference. Show us the impact — from better solution quality to improved efficiency, accuracy, or other measurable gains." — [Qollab Rules & terms](https://qollab.xyz/programs/hackathon/terms)
- [Confirmed] **Short version (FAQ on hub and how-it-works)**: "Quantum Impact. Take on a real challenge in logistics, manufacturing, space, finance, energy or another industry with a hybrid quantum-classical approach: pick a public dataset, build a strong classical baseline, then show where a quantum subroutine makes a measurable difference." — [Qollab hackathon hub](https://qollab.xyz/programs/hackathon); [How it works](https://qollab.xyz/programs/hackathon/how-it-works)
- [Confirmed] **Award tagline**: "Best of theme: Quantum Impact — solving real-world problems with quantum + classical computing." "Most impact" is a separate specialty award. "A single project can win multiple specialty awards and placement awards." — [How it works](https://qollab.xyz/programs/hackathon/how-it-works)
- [Confirmed] "Impact Potential" is one of four rubric criteria for every project, alongside Novelty & Creativity, Technical Execution and Documentation Quality. No weights are given. — [Qollab Rules & terms](https://qollab.xyz/programs/hackathon/terms)
- [Confirmed] The "beyond the tutorial" bar names "A novel application or problem context (e.g., applying an existing technique to a specific domain)" and "A technical extension (e.g., noise/error mitigation, parameter optimization, comparative benchmarking)" as qualifying contributions. Panels "may score a submission at 0" on Novelty and Technical if a project fails the bar. — [Qollab Rules & terms](https://qollab.xyz/programs/hackathon/terms)

**Text changes since Oct 7.** A diff of extracted page text at 16:56 ET Oct 9 shows only the edits already logged in the Unlocked notes:
- the outside-repo MIT clause was added
- "AI tools" was dropped from the build-window bullet
- a Safari FAQ entry was added

Nothing Impact-specific changed. The hub and mentors pages are byte-identical in text. — [Rules & terms](https://qollab.xyz/programs/hackathon/terms); [How it works](https://qollab.xyz/programs/hackathon/how-it-works)

**No kickoff materials yet (as of 17:10 ET)**
- [Confirmed] GT site text is identical to the Oct 9 14:45 snapshot. It still says "Challenge themes and problem statements will be shared before the hackathon begins, following each sponsor's release schedule. We'll link the materials here as they become available." — [GT Fall Fest site](https://qhackathon-gt.lovable.app/)
- [Confirmed] Qollab Announcements has no hackathon item. The newest is "Google withheld an ECDSA circuit" (Aug 26, 2026). — [Qollab announcements](https://qollab.xyz/explore/news)
- [Confirmed] The forum's latest topics (to 20:18 UTC Oct 9) are only auto-created project threads, such as a user's copies of the Learn lessons. There is no kickoff, problem-statement or dataset post. — [forum.qollab.xyz latest.json](https://forum.qollab.xyz/latest.json)
- [Confirmed] The project API lists 109 public projects at 16:56 ET, up from 104 at 14:42 ET. All five new ones are copies of Learn lessons by user "chuyi". No hackathon submissions are visible yet, which is expected since the window opens at 19:00 ET. — [Qollab project API](https://api.qollab.xyz/api/project/popular?limit=30)

**How Qollab staff define a strong baseline and an honest comparison (their Learn content, Sep 2026)**
- [Confirmed] The QAOA explainer (Nicolaas Spijker, Sep 15, 2026) analyzes the 24-node Quantum Courier graph:
  - a random split averages 18.5 cut edges
  - one tuned QAOA layer averages 25.5 of a possible 33 (0.77)
  - "Greedy local search from a random split… averages about 31 on the same graph and reaches 33 within a few restarts, in milliseconds. So on this graph the average sample from one layer is worse than what a classical heuristic returns."
  - It recommends reporting "the best string in the tally, checked classically, rather than the average."
  - It quotes Goemans–Williamson's 0.878 guarantee against QAOA p=1's 0.6924 on 3-regular graphs.
  - Note: the explainer calls the instance "24-node, 37-edge", while Courier's code says 36 edges, 3 per node.

  — [Qollab Learn: Quantum Optimization and QAOA](https://qollab.xyz/learn/quantum-optimization)
- [Confirmed] The lesson "Is quantum worth it in your app" gives a five-step comparison protocol:
  1. "Write the thresholds before you run anything… because a threshold chosen after seeing the result can be chosen to fit it."
  2. "Solve it the ordinary way first. The classical version is your baseline and often your answer."
  3. "Solve it the quantum way, at the same task… same inputs, output format and scoring function."
  4. "Compare each result against the thresholds. A relative comparison is not enough."
  5. "Write down the date and the backend."

  Its verdict: "As of September 2026, the classical version wins that race for almost any feature you would ship." — [Qollab Learn: Is quantum worth it in your app](https://qollab.xyz/learn/using-quantum-in-a-real-application/is-quantum-worth-it)
- [Confirmed] The same lesson gives concrete figures:
  - **Noise.** Regime Radar's 12-qubit kernel read 0.1768 on the ideal simulator and 0.0337 on the Aria 1 noise model, against an exact 0.1779 (Sep 22, 2026).
  - **Latency.** A 1,000-shot quantum draw took 13.8 s against 0.20 ms for `random.choices` (69,044×).
  - **Scale.** "Your laptop solves a problem over 36 binary variables exactly by trying all 2^36 assignments, which takes about a minute."

  — [Qollab Learn: Is quantum worth it](https://qollab.xyz/learn/using-quantum-in-a-real-application/is-quantum-worth-it)
- [Confirmed] The lesson "What to build" says choose a project "by the output your application needs". It lists five ways to use a circuit's distribution:
  1. sample from it
  2. compare two of them (kernel/overlap)
  3. read structure inside it
  4. reduce it to one number
  5. watch it change

  It names four reasons an idea "does not map": it needs one correct answer quickly, it processes a lot of data ("loading a large dataset takes longer than reading it"), it needs the state at scale, or it must be reproducible. It adds that good first projects have "a stated reason for the quantum part to be there… None of the three needed to beat a classical computer." — [Qollab Learn: What to build](https://qollab.xyz/learn/using-quantum-in-a-real-application/what-to-build)
- [Confirmed] Qollab's finance explainer (Jul 3, 2026) praises the three Spring 2026 finance projects because "None of them claims an advantage. Each is honest about its limits, which is exactly what makes them worth running." It summarizes the field as "There is no demonstrated production quantum advantage in finance today." On quantum kernels it says "a well-tuned classical model tends to catch up… a pattern researchers call dequantization." — [Qollab Explore: Finance](https://qollab.xyz/explore/finance)

### Inferences
- [Inferred] The brief's operative words are **public dataset**, **strong classical baseline** and **measurable**. Qollab's own content shows its staff will check whether a "win" is against a weak baseline. Their QAOA explainer publicly downgrades Courier's "+46.2% vs random cut" by benchmarking greedy local search. An Impact entry that beats only random sampling, or an untuned heuristic, will likely lose Technical and Impact points with these judges.
- [Inferred] The safest framing mirrors Qollab's five-step protocol, which is nearly identical to IonQ's benchmark rule ("the bar is set before any system runs", Q4):
  - pre-registered thresholds
  - an exact or best-known classical solution on the same instances
  - the same scoring function for both methods
  - a pass/fail table
  - a dated, backend-labelled verdict
- [Inferred] "Public dataset" is the most under-delivered requirement in the existing catalog (Q2). Using a recognized public benchmark (named, versioned, shipped as a project file ≤2 MB) is a cheap way to stand out. Qollab's runtime is GET-only with CORS, and nothing persists between runs (prior notes), so ship the data rather than fetch it.
- [Inferred] "Space" and "energy" are named in the brief but have zero Qollab projects (Q2), and both map to IonQ stories (Capella SAR, ORNL/EPB grid). That makes them natural "novel application context" picks.

### Gaps
- Kickoff (19:00 ET Oct 9) had not happened at snapshot time. Re-check at or after 19:00 ET:
  - the GT site's materials section
  - [Rules & terms](https://qollab.xyz/programs/hackathon/terms), [How it works](https://qollab.xyz/programs/hackathon/how-it-works) and the hub (diff the extracted text)
  - [Announcements](https://qollab.xyz/explore/news)
  - [forum latest.json](https://forum.qollab.xyz/latest.json)
  - `https://api.qollab.xyz/api/project/recent?limit=30`, for newly published submissions
  - The Slack node and global channels are not publicly readable and are the most likely venue for any IonQ problem statement or dataset.
- No rubric descriptors exist for "Impact Potential" (what counts as impact: business value, scalability argument, or measured gain). None are published.
- Whether judges will accept a "public dataset" that is a published benchmark instance (e.g., a TSPLIB or IEEE test case) rather than raw real-world data is not stated. [Inferred] It is very likely acceptable, given the "relevant public dataset" wording.

---

## Q2. Which application areas are already crowded on Qollab, and which are wide open?

### Takeaway
Qollab has 109 public projects (API, 16:56 ET Oct 9). About 20 are application or Impact-style. They cluster in five areas:
- **QAOA logistics/MaxCut**: Quantum Courier
- **QAOA portfolio optimization**: Systemic Oracle, plus Qollab's own portfolio/QUBO showcases
- **quantum kernels for finance**: Regime Radar
- **small-molecule VQE**: H2, HeH⁺, LiH and methanol. This is the most crowded topic, with ~10 projects mentioning molecules.
- **lattice-peptide folding/design**: QuPepFold Sep 26, plus a very rigorous QAOA peptide-design project published Oct 8

Keyword scans of every project's write-up and main file found **zero** projects on:
- power-grid / unit commitment, battery chemistry, gate assignment, cargo or aircraft loading, bin packing / knapsack, job-shop scheduling
- satellite / SAR / earth observation, image classification, fraud / credit / anomaly detection
- graph partitioning / finite-element / sparse linear algebra, CFD / lattice Boltzmann
- generative models (QCBM / QGAN / copulas), LLM / NLP, supply chain, EV charging, facility location, max independent set
- healthcare / genomics, time-series forecasting

Almost no existing project uses a **named public dataset**.

### Cited Findings
**Method**
- [Confirmed] I paginated `/api/project/popular` (109 items) and fetched `versions/head` for 33 application-relevant projects. I also keyword-scanned the write-up plus main code of all projects, reusing the 14:45 ET full dump for the 104 older ones. The `code` field is the main file only, so multi-file projects may be under-counted. — [Qollab project API](https://api.qollab.xyz/api/project/popular?limit=30)

**A. Spring 2026 Creative Challenge application projects (featured, ran on IonQ hardware)**

| Project (published) | Problem | Data | Quantum method | Classical baseline | Claimed result |
|---|---|---|---|---|---|
| **Quantum Courier / "Qatalyst Quantum Game: Pizza Race"** (Sitifar/quantum-game-pizza-race), Dr. Siti Fariya, Qatalyst Quantum / Heriot-Watt; 2026-06-15; 98 views | Five logistics stages: assignment, TSP, VRPTW, MaxCut, joint QUBO | "Published formulations" with instances hard-coded in `stages.js`. No named public dataset. VRPTW has 25 customers. | QAOA p=1, 4,096 shots, on IonQ Forte via qBraid (24-node 3-regular MaxCut). In-browser "quantum-inspired" QUBO simulated quantum annealing. | Hungarian algorithm; 2-opt + simulated annealing; Goemans–Williamson SDP rounding | Classical wins stages 1 and 3; tie on 2; "quantum" wins stage 4 at "+46.2% on real IonQ Forte" **vs a random-cut baseline**; stage 5 "depends on instance structure". Four QAOA variants lost to SA on VRPTW. The playable game is hosted off-Qollab (qatalyst-quantum.co.uk/play). |
| **Quantum Systemic Oracle** (jamie/systemic-oracle), Jamie Dominguez; 2026-06-15; 69 views | Daily crypto "systemic risk index" (0–10,000 bps) published to a Chainlink-style oracle on Sepolia | Live crypto signals (vol, funding, prediction markets, DeFi TVL, stablecoin dominance). The Qollab version uses a **frozen snapshot**. | 14-qubit QAOA: 8 asset qubits + 6 "witness" qubits folded in as RY rotations. p=1 (56 CX) is hardware-optimal; methodology string "qaoa-14q-8asset-p2-v3". | Brute-force optimum over 256 portfolios | "QAOA repeatedly sampled the brute-force classical optimum, with gaps of +0.00% to ~5%" on the simulator. On Forte, "~90 two-qubit gates is the envelope". The QAOA signal is only **5%** of the index weight. Projects ~66 logical qubits for 60 assets on Tempo (forward-looking). |
| **Quantum Market Regime Radar** (alireza/quantum-regime-radar), Alireza Khodaei PhD (Nelnet) with Aaron Ben-Shalom; 2026-06-05; 112 views | Classify a live equity window into one of 5 volatility regimes | Reference regimes: SPY 2017, KRE 2023, SPY 2020 (×2), SPY late-2022. Live windows: META 2020, AMZN 2020, NVDA 2022, AAPL 2021, META 2022. GARCH/GJR-GARCH fingerprints from a "proprietary" pipeline. | 12-qubit amplitude-encoded fingerprints (8 layers). Inversion-test kernel = squared Bhattacharyya coefficient; swap-test alternative. | Plain NumPy correlation study, "topped out around 0.4 on its best sample" | Concedes "classical BC is cheap" and does not claim speedup; argues "right primitive". The original 20-regime library needed "80 to 100 qubits to represent one regime". The kernel decays to 0.0337 vs 0.1779 exact on the Aria-1 noise model (per the Qollab lesson). |
| **Quantum Market Game Theory Simulator** (q-aad), Aadarsh Venkat Ramanan (high-school senior); 131 views | Prisoner's dilemma with entangled traders (EWL 1999 scheme) | None | 2-qubit circuit, Streamlit | Classical game equilibria | A teaching object. Qollab itself says it is "A teaching lens more than a trading tool." |
| **Quantum Advantage Lab** (hsadeghi), Hossein Sadeghi (ex-D-Wave, Pasqal); 78 views | Four "races" | None (synthetic) | Grover; VQE; discrete-time quantum walk; Trotterized TFIM (1/2/4/8/16 steps) | Linear search; classical optimizer; random walk; SciPy `expm` | "Though currently no such speedup exists in practice." Reports TV distance vs Trotter depth. |
| **qOrbital** (bawa27), Aryan Bawa (Dartmouth) & Arnav Singh; 2026-06-19; 201 views | Molecular orbital visualizer: H2, HeH⁺, LiH | PySCF integrals | VQE (UCCSD) on IonQ Aria/Forte; Bohmian-trajectory "uncertainty cloud" of hardware noise | Hartree–Fock reference; Aer exact | Visualization rather than a performance claim. A precomputed hardware "Gallery". |

— [Quantum Courier write-up](https://qollab.xyz/u/Sitifar/quantum-game-pizza-race); [Explore: Quantum Courier](https://qollab.xyz/explore/quantum-courier); [Systemic Oracle write-up](https://qollab.xyz/u/jamie/systemic-oracle); [Explore: Systemic Oracle](https://qollab.xyz/explore/quantum-systemic-oracle); [Regime Radar write-up](https://qollab.xyz/u/alireza/quantum-regime-radar); [Explore: Regime Radar](https://qollab.xyz/explore/quantum-regime-radar); [Explore: Finance](https://qollab.xyz/explore/finance); [Explore: Quantum Advantage Lab](https://qollab.xyz/explore/quantum-advantage-lab); [qOrbital](https://qollab.xyz/u/bawa27/qorbital); [Spring 2026 cohort](https://qollab.xyz/explore/spring-2026-cohort)

- [Confirmed] The cohort page originally described Courier as "Built on React and Leaflet with a QAOA reformulation of the vehicle routing problem". The shipped version is vanilla JS, and its quantum win is MaxCut, not VRP. — [Spring 2026 cohort](https://qollab.xyz/explore/spring-2026-cohort); [Quantum Courier write-up](https://qollab.xyz/u/Sitifar/quantum-game-pizza-race)
- [Confirmed] Courier's roadmap lists an "Extension to grid storage siting QUBOs (DOE GIC 2026 submission, IEEE 14-bus testbed)". This energy idea was claimed by the Courier author but not published on Qollab. — [Quantum Courier write-up](https://qollab.xyz/u/Sitifar/quantum-game-pizza-race)

**B. Qollab-team application showcases (library demos, Aug–Sep 2026; all tiny, all "fork me" templates)**
- [Confirmed] Chemistry:
  - [H2 dissociation curve with VQE](https://qollab.xyz/u/qollab/quantum-chemistry-showcase-the): 2-qubit VQE vs exact diagonalization and HF, 0.3–2.5 Å, STO-3G, parity mapping
  - [H2 bond-length slider](https://qollab.xyz/u/qollab/quantum-chemistry-showcase-t-2)
  - [Cross-framework H2 VQE](https://qollab.xyz/u/qollab/cross-framework-showcase-one-v): Qiskit vs PennyLane
  - [qiskit-nature H2](https://qollab.xyz/u/qollab/showcase-h2-ground-state), [Jordan–Wigner](https://qollab.xyz/u/qollab/showcase-fermionic-op) and [VQE ground state](https://qollab.xyz/u/qollab/showcase-vqe-ground-state)
  - [Methanol VQE](https://qollab.xyz/u/qollab/quantum-chemistry) (Mar 7, 2026), adapted from IBM's SQD IEF-PCM methanol workflow
- [Confirmed] Finance and optimization:
  - [European call option pricing](https://qollab.xyz/u/qollab/showcase-option-pricing): the amplitude-estimation input
  - [Portfolio optimization](https://qollab.xyz/u/qollab/showcase-portfolio-opt): best 2 of 3 assets
  - [QAOA on a QUBO](https://qollab.xyz/u/qollab/showcase-qaoa-qubo): `x + y − 2xy`
  - [Exact QUBO](https://qollab.xyz/u/qollab/showcase-qubo-exact)
- [Confirmed] Machine learning:
  - [Quantum kernel on two-moons](https://qollab.xyz/u/qollab/quantum-kernel-showcase-drag-t)
  - [VQC on XOR](https://qollab.xyz/u/qollab/showcase-vqc-xor)
  - [EstimatorQNN](https://qollab.xyz/u/qollab/showcase-estimator-qnn)
- [Confirmed] [Learn: Is quantum worth it here](https://qollab.xyz/u/qollab/learn-app-race) (Sep 22): a quantum weighted picker vs `random.choices`, with the timing race.

**C. Community application-style projects outside the cohort**

| Project (published) | Problem / method | Baseline / result |
|---|---|---|
| [QuPepFold](https://qollab.xyz/u/akshayuttarkar/qupepfold) (2026-09-26) | CVaR-VQE (α=0.025) folding of 4–10-residue peptides on a tetrahedral lattice, 10–23 qubits. Browser edition of a package from Uttarkar et al., *PLoS One* 2026. | Default APRLRFY (7 residues, 10 qubits) reaches CVaR −2.94 (sampled −3.02). Caveats it states: a "seeded random MJ-like matrix" toy energy model; "Classically simulable"; no advantage claimed. |
| [Quantum-Assisted De Novo Peptide Sequence Design](https://qollab.xyz/u/qcat/qchemistry) (qcat, 2026-10-08, one day before the window) | Physicochemical objective → QUBO → Ising → QAOA (p≤3, ≤20 qubits). Also a "windowed" 12-qubit quantum large-neighbourhood search. | L=4 (16 qubits): QAOA p=2 hits the optimum per feasible shot at 0.0081 vs uniform 0.0078 ("roughly *one* uniform random sample"). L=10 (40 variables, 1,048,576 sequences): windowed QAOA finds the global optimum (−0.2113) in 31.3 s; **classical window-search control finds it in 0.02 s ("2000× faster")**; SA −0.1556; GA −0.1446. Has an explicit "What this project does not claim" section. Runs on Aer/Streamlit locally. |
| [Krylov Quantum Diagonalization](https://qollab.xyz/u/mirko/krylov-quantum-diagonalization) (Aug 11) | IBM tutorial adaptation (CC BY-SA), 30-qubit Heisenberg chain | "This runs the classical half" only |
| [QAIP Hardware Ranking](https://qollab.xyz/u/Rudra1x/qaip-hardware-ranking) (Oct 8); [Quantum Automitigation](https://qollab.xyz/u/S0cra13s/quantum-automitigation) (Oct 8); [Depth-Independent Coherence](https://qollab.xyz/u/WilliamDenyer/depth-independent-coherence) (Aug 22) | Tooling: calibration-aware backend choice, a mitigation bandit, a routing benchmark on ibm_marrakesh | Not industry applications |
| [Collapsing AI](https://qollab.xyz/u/jonromero/collapsing-ai) (May 15) | Maps transformer attention weights to RY gates on IonQ to test Orch-OR "Quantum-Classical Divergence" | Fringe; no baseline |
| Empty shells published Oct 8–9 (likely hackathon teams staging): [MejorRuta](https://qollab.xyz/u/plamsoft/mejorruta) ("ubicar 5 ciudades en un mapa…": a 5-city routing idea), [Distancia](https://qollab.xyz/u/plamsoft/distancia), [QChemistry "Protein synthesis"](https://qollab.xyz/u/manish/qchemistry), [registration vectors](https://qollab.xyz/u/ndazeo/registration-vectors) ("register vector clouds in 3d") | Descriptions only; empty write-ups and main files at fetch time | n/a |

— [Qollab project API](https://api.qollab.xyz/api/project/popular?limit=30)

**D. Keyword scan of every project's write-up plus main file (109 projects)**
- [Confirmed] **Zero hits:** "unit commitment", "power grid", "gate assignment", "cargo", "aircraft loading", "bin packing", "knapsack", "job shop", "satellite", "SAR", "image classification", "MNIST", "traffic sign", "fraud", "anomaly", "docking", "graph partition", "finite element", "lattice Boltzmann", "QCBM", "Born machine", "language model", "EV charging", "facility location", "independent set", "community detection", "feature selection", "supply chain", "warehouse", "catalyst", "lithium", "climate", "genom", "medical", "healthcare", "time series", "forecast", "kaggle". "Battery" and "drug" appear only as passing mentions in the Jordan–Wigner showcase.
- [Confirmed] **Clusters:**
  - "molecule": 10 projects
  - "portfolio": 4 (Oracle plus three Qollab showcases)
  - "protein": 3 (QuPepFold, qcat, one QUBO showcase mention)
  - "quantum kernel": 3 (Regime Radar plus two showcases)
  - "VRP"/"TSP"/"vehicle routing": 1 (Courier)
  - "option pric": 1 (showcase)
  - "amplitude estimation": 2 (showcases)
- [Confirmed] "dataset" appears in only 6 projects, and none uses a named public benchmark dataset for an industry problem. Regime Radar uses public ticker history through a proprietary fingerprinting step; the Oracle uses a frozen live-API snapshot.

— [Qollab project API](https://api.qollab.xyz/api/project/popular?limit=30) (scan of `versions/head` content and code)

### Inferences
- [Inferred] **Saturated, avoid unless clearly beyond what exists:**
  - small-molecule VQE (H2/LiH/HeH⁺ dissociation curves)
  - MaxCut / TSP / VRP QAOA "races"
  - Markowitz portfolio QAOA
  - quantum kernels on toy 2-D data
  - quantum prisoner's dilemma
  - QAOA lattice-peptide folding or design (two projects in the last two weeks, one of them extremely rigorous)
- [Inferred] **Wide open, and each maps to an IonQ application story (Q3):**
  - **Energy**: unit commitment / grid scheduling (ORNL, EPB)
  - **Manufacturing/CAE**: graph partitioning for sparse-matrix ordering (Ansys/Synopsys)
  - **Aviation**: flight-gate assignment (DESY); aircraft/cargo loading (Airbus)
  - **Logistics, not routing**: shipment selection (Einride)
  - **Space**: SAR/earth-observation change detection (Capella)
  - **Finance beyond portfolios**: copula/QCBM risk aggregation or synthetic data (GE, Fidelity); credit/fraud classification
  - **AI**: a quantum classification head on frozen embeddings (IonQ's LLM fine-tuning)
- [Inferred] The bar for honesty is now very high. qcat's peptide project shows a pre-window entrant already shipping matched classical controls, a uniform-sampling comparison and a "does not claim" section. Judges who saw it will expect similar rigor from Impact entries.
- [Inferred] A differentiator few entries have shown: a real, named public dataset, plus an exact or best-known classical optimum, plus a measured quantum contribution that is not just "found the optimum somewhere in 4,096 shots".

### Gaps
- Projects that are private, in draft, or published after 17:10 ET Oct 9 are invisible. Competing hackathon entries cannot be seen until they are published.
- For multi-file projects, only the main file and write-up were scanned. A domain term used only in secondary files would be missed.
- The off-Qollab parts of Courier (the game JS) and the Oracle (GitHub pipeline) were not inspected.

---

## Q3. Which IonQ application stories could a 48-hour team credibly echo or extend at ≤20–29 qubits, and what are the honest caveats of each?

### Takeaway
IonQ's 2022–2026 application portfolio follows one repeating pattern:
- a hybrid workflow where a small quantum subroutine (QAOA variants, VarQITE, QC-AFQMC shadows, QCBM, PQC heads) sits inside a large classical pipeline
- headline gains measured end-to-end ("up to" 12% / 14.6% wall-clock, ">20×" vs IonQ's own prior implementation, "up to 3.14%" accuracy, "up to 12.1% more shipments")
- qubit counts of 12–36 on Aria and Forte hardware, with larger sizes only in simulation (up to 150 qubits)

Independent critiques focus on baselines and on the gap between simulation and hardware.

The stories a browser-bound team can honestly echo at ≤24 qubits (built-in simulator) or ≤29 (IonQ Forte noise-model simulator) are:
- **graph partitioning for sparse-matrix fill reduction** (Ansys/Synopsys)
- **unit commitment** (ORNL)
- **flight-gate assignment** (DESY)
- **aircraft loading** (Airbus)
- **shipment selection as a warm start** (Einride)
- **QCBM copulas** (GE)
- **a PQC classification head on frozen text embeddings** (IonQ LLM paper)

Chemistry at AstraZeneca scale (QC-AFQMC) is not reproducible in-browser, and VQE on small molecules is saturated on Qollab.

### Cited Findings
**Engineering / CAE (Ansys, now Synopsys): graph partitioning inside LS-DYNA**
- [Confirmed] **Mar 20, 2025.** IonQ and Ansys reported Ansys "was able to speed processing performance by up to 12 percent compared to classical computing" on a blood-pump LS-DYNA simulation (meshes up to 2.6M vertices / 40M edges). IonQ's CEO called it "one of the first cases ever where quantum computing is outperforming key classical methods". — [IonQ news](https://www.ionq.com/news/ionq-and-ansys-achieve-major-quantum-computing-milestone-demonstrating); [TQI](https://thequantuminsider.com/2025/03/20/ionqs-devices-boost-ansys-simulations-achieving-up-to-12-faster-processing-over-classical-computers/)
- [Confirmed] **The underlying paper** is arXiv:2503.13128 (Aboumrad, Zhu, Girotto, Rouet, Jojo, Lucas, Pathak, Kaushik, Roetteler; Mar 17, 2025).
  - It applies **variational quantum imaginary time evolution (VarQITE) to graph partitioning** to reduce fill-in when factoring large sparse linear systems.
  - It ran both in simulation and on IonQ Aria and Forte.
  - A Fiduccia–Mattheyses-inspired classical heuristic improves the hardware solutions.
  - The "up to 12%" is LS-DYNA wall-clock "for some problems".

  — [arXiv:2503.13128](https://arxiv.org/abs/2503.13128)
- [Confirmed] **TQI's own headline** reads "Hybrid Quantum Solver Simulated with IonQ Framework Delivers 12% Speedup; Hardware Validated on Small Instances". — [TQI](https://thequantuminsider.com/2025/03/20/ionqs-devices-boost-ansys-simulations-achieving-up-to-12-faster-processing-over-classical-computers/)
- [Confirmed] **Critique** (Will Kirkpatrick, "IonQ & Ansys: Crying Wolf", Mar 23, 2025):
  - the 12% run was on a classical computer
  - the blood-pump mesh was refined "100x more dense"
  - the other two use cases "did not see any speed up"
  - hardware runs were "slightly worse" with no runtime reported

  Per a search summary, the paper's classical partitioner baseline is LS-GPart rather than METIS. A year-end newsletter gave the claim a "Marketing Spin" award. — [Kirkpatrick Substack](https://wkirkpatrick.substack.com/p/ionq-and-ansys) (via search summary); [Quantum Pirates 2025 Wrapped](https://quantumpirates.substack.com/p/quantum-2025-wrapped-the-year-in-4d2) (via search summary)
- [Confirmed] **Sep 17, 2026 follow-up with Synopsys**:
  - The quantum step "reorganizes equations before solving" ("quantum-enhanced sorting method").
  - Total simulation time is reduced by "at least 5.9%" and "up to 14.6%".
  - Models: automobile, drill component, fluid impeller, jet-engine assembly, with meshes up to 35M points.
  - Simulations ran "up to 150 qubits"; physical execution was on "IonQ's 36-qubit Forte".
  - Paper: arXiv:2603.15515, **Iterative-QAOA** for the Graph Partitioning Problem, described as "non-variational". 1st-place Best Paper at IEEE Quantum Week 2026.

  — [IonQ news](https://www.ionq.com/news/ionq-demonstrates-computer-aided-engineering-workload-acceleration-by-up-to-14-6-with-quantum-technology); [arXiv:2603.15515](https://arxiv.org/abs/2603.15515); [TQI Sep 17, 2026](https://thequantuminsider.com/2026/09/17/ionq-synopsys-14-6-percent-faster-engineering-simulations/)
- [Confirmed] QCR lists the simulations as CUDA-Q (150 qubits) and the hardware as IonQ Forte (36 qubits), with "Sedan car and Rolls-Royce engine models". A search summary attributes to IonQ's blog the statement that 14.6% was the CUDA-Q-simulated best case and ~12% the Forte best case. I did not verify this; TQI's write-up does not split simulation from hardware. — [QCR: nine papers](https://quantumcomputingreport.com/ionq-demonstrates-hybrid-hpc-and-quantum-ai-workflows-across-nine-peer-reviewed-papers-at-ieee-quantum-week-2026/amp/); [TQI](https://thequantuminsider.com/2026/09/17/ionq-synopsys-14-6-percent-faster-engineering-simulations/)

**Chemistry / pharma (AstraZeneca, AWS, NVIDIA)**
- [Confirmed] **Jun 9, 2025.** The press release claims a ">20x" end-to-end time-to-solution speedup on a Suzuki–Miyaura reaction step, with IonQ Forte + NVIDIA CUDA-Q + Amazon Braket/ParallelCluster + H200 GPUs, and "runtime from months to days" while maintaining accuracy. The baseline is IonQ's own prior implementations/benchmarks, not a classical method. — [IonQ news](https://ionq.com/news/ionq-speeds-quantum-accelerated-drug-development-application-with); [BusinessWire](https://www.businesswire.com/news/home/20250609358259/en/IonQ-Speeds-Quantum-Accelerated-Drug-Development-Application-With-AstraZeneca-AWS-and-NVIDIA)
- [Confirmed] **Paper**: arXiv:2506.22408, QC-AFQMC with matchgate shadows.
  - The oxidative-addition step of a **Ni-catalyzed** Suzuki–Miyaura reaction ran on **24 qubits of Forte**: 16 for the trial state plus 8 ancillas for error mitigation.
  - Data collection was ~9× faster, and post-processing showed 656× time-to-solution vs prior state of the art.
  - Barriers were within ~±4 kcal/mol of CCSD(T) on the ideal simulator, and ~10 kcal/mol on the QPU.
  - Per an alphaXiv summary, hardware noise flipped the predicted relative stability of reactants and products.

  — [arXiv:2506.22408](https://arxiv.org/abs/2506.22408) (via search summary); [alphaXiv overview](https://www.alphaxiv.org/overview/2506.22408) (via search summary)
- [Confirmed] **Critique context.** Prior analyses note that QC-AFQMC's classical post-processing cost is a barrier, scaling as a high power of system size per walker. A December 2025 OLCF talk by an IonQ speaker described accuracy as roughly on par with leading classical methods. — [arXiv:2312.09872](https://arxiv.org/abs/2312.09872) (via search summary); [OLCF user call Dec 2025](https://www.olcf.ornl.gov/calendar/userconcall-dec2025/) (via search summary)

**Aviation and logistics**
- [Confirmed] **Airbus (Aug 2022):** a 12-month project toward a prototype aircraft-loading quantum application. — [STAT Times](https://www.stattimes.com/amp/aviation/ionq-airbus-sign-agreement-to-collaborate-on-aircraft-loading-project-using-quantum-computing-1346287)
- [Confirmed] **Related paper**: arXiv:2504.01567, "Quantum Computing for Optimizing Aircraft Loading" (Kaushik, Kim, Aboumrad, Roetteler, Topi, Ashworth; Apr 2, 2025).
  - A multi-angle QAOA variant (MAL-VQA) with fewer 2-qubit gates and a cost function handling inequality constraints **without slack variables**.
  - 12–28 qubits on IonQ Aria and Forte; "optimal solutions for all studied instances".
  - The first Aria run was 4 containers × 3 slots = 12 qubits, 1,000 shots, ~70% probability on the optimum.
  - The abstract gives no head-to-head classical benchmark.

  — [arXiv:2504.01567](https://arxiv.org/abs/2504.01567); [arXiv HTML](https://arxiv.org/html/2504.01567v1) (via search summary)
- [Confirmed] **DESY flight-gate assignment (Sep 2023 runs; Mar 14–15, 2024 release):** a quadratic assignment problem with "logarithmic-linear encoding" on Aria. Nine flights × four gates (36 binary variables in a direct one-hot encoding). There was no runtime or quality comparison with classical solvers. DESY's Karl Jansen called the results "encouraging". — [IonQ news](https://ionq.com/news/ionq-and-desy-research-highlights-quantums-potential-benefits-for-airport); [IonQ blog](https://ionq.com/blog/ionq-and-desy-tackle-the-gate-assignment-problem); [TQI](https://thequantuminsider.com/2024/03/15/ionq-and-desy-research-highlights-quantums-potential-benefits-for-airport-flight-gate-optimization/)
- [Confirmed] **Einride**:
  - **May 2025**: investment partnership.
  - **Dec 2025** update: 15 use cases assessed; "modularized the fleet orchestration problem" so quantum targets shipment allocation. No qubit counts, baseline or metrics were given.
  - **2026** paper arXiv:2604.11758 (IonQ + Einride, "Shipment Selection Problem"): an MIQP with enhanced QAOA, used as a **warm start** for Einride's classical solver, on anonymized real schedules. 20–35-qubit scenarios ran on IonQ hardware; 90/130-qubit scenarios ran on an MPS simulator. The mean gain is **+1.7% shipments delivered**, best case **+12.1%**, with cost "effectively unchanged". Mean drive distance fell 3.5%, but distance per shipment rose 1.9%.

  — [TQI May 2025](https://thequantuminsider.com/2025/05/21/ionq-and-einride-partner-to-bring-quantum-enhanced-logistics-to-autonomous-freight-operations/); [TQI Dec 2025](https://thequantuminsider.com/2025/12/10/einride-and-ionq-partnership-uses-quantum-computing-to-optimize-the-logistics-of-electric-and-autonomous-freight/); [arXiv:2604.11758](https://arxiv.org/pdf/2604.11758) (via search summary); [IonQ blog "Mind the Gaps"](https://ionq.com/blog/mind-the-gaps-quantum-optimization-for-efficient-electric-and-autonomous-freight-dispatch-with-ionq-and-einride) (via search summary)

**Energy**
- [Confirmed] **ORNL / DOE GRID-Q unit commitment (arXiv Jun 2025; release Jul 31, 2025)**:
  - A quantum routine samples promising generator on/off configurations, and classical optimization does the dispatch.
  - Instances were 3, 10 and 26 generators × 24 hourly steps, on 36-qubit Forte Enterprise.
  - Simulated runs were within 0.55–2.7% of optimal cost (~2.5% at 26 units), and hardware was "similar".
  - ORNL: "As the quantum device scales, concurrent research is intended to test how the application performance can gain a quantum advantage."
  - IonQ forecasts that 100–200 high-fidelity qubits ("as early as 2026") will handle grid-scale UC.

  — [IonQ news](https://ionq.com/news/ionq-partners-with-oak-ridge-national-laboratory-demonstrating-quantum-power); [TQI Jun 8, 2025](https://thequantuminsider.com/2025/06/08/ionq-oak-ridge-researchers-use-quantum-classical-algorithm-to-solve-power-grid-problem/)
- [Confirmed] **EPB (Chattanooga)**: a $22M deal (Apr 2025) for a shared Forte Enterprise plus networking, with joint work on grid-optimization algorithms. The system was commissioned by Sep 2026. No published grid-application result was found. — [IonQ news](https://ionq.com/news/ionq-announces-usd22m-deal-with-epb-establishing-chattanooga-tennessee-as); [QCR](https://quantumcomputingreport.com/epb-commissions-ionq-forte-enterprise-quantum-computer-in-chattanooga-hub/)

**Finance / risk**
- [Confirmed] **GE Research (Jun 23, 2022):** a Quantum Circuit Born Machine **copula** learned the correlations of 3–4 standardized historical stock indexes on IonQ hardware. Quantum predictions beat classical "only in some cases". — [IonQ news](https://ionq.com/news/june-23-2022-ionq-ge-research-risk-aggregation); [GE Research](https://www.ge.com/research/newsroom/ionq-and-ge-research-demonstrate-high-potential-quantum-computing-risk-aggregation)
- [Confirmed] Qollab's finance explainer notes "IonQ and Fidelity's applied-technology center generated synthetic market data on trapped-ion hardware." — [Qollab Explore: Finance](https://qollab.xyz/explore/finance)

**AI / ML and materials (Hyundai and IonQ's own work)**
- [Confirmed] **Hyundai, Jan 19, 2022**: VQE for lithium compounds, specifically lithium oxide, billed as "the largest battery chemistry model yet". No qubit count or results were published. — [TQI](https://thequantuminsider.com/2022/01/19/ionq-and-hyundai-partner-to-use-quantum-computing-to-improve-next-gen-batteries/)
- [Confirmed] **Hyundai, Apr 2022**: classification of "43 types of road signs", then 3-D object detection (pedestrians, cyclists) planned on Aria. No benchmark data was found. — [Fierce Electronics](https://www.fierceelectronics.com/sensors/ionq-hyundai-expand-quantum-computing-partnership-object-detection-autonomous-vehicles)
- [Confirmed] **May 1, 2025, two papers**:
  1. **LLM fine-tuning** (arXiv:2504.08732): a sentence-transformer plus a PQC classification head with long-range connections, on sentiment (SST-2 per IonQ's blog). "Up to 3.14% improvements in accuracy over classical architectures of comparable model size". These were noisy simulations, with accuracy rising with qubit count.
  2. **Steel-microstructure QGAN** (arXiv:2504.08728): IonQ with Hyundai materials engineers. A QCBM on Aria feeds a classical Wasserstein GAN for 5-channel EBSD images, beating classical Bernoulli-prior GANs on MMD in ~70% of samples.

  — [arXiv:2504.08732](https://arxiv.org/abs/2504.08732); [IonQ blog](https://ionq.com/blog/supercharging-ai-with-quantum-computing-quantum-enhanced-large-language); [IonQ news](https://ionq.com/news/ionq-demonstrates-quantum-enhanced-applications-advancing-ai); [arXiv:2504.08728](https://arxiv.org/html/2504.08728v1) (via search summary)
- [Confirmed] IonQ's customers page case study lists "Improves accuracy by 3.14%" for hybrid LLM fine-tuning alongside the steel-image work, citing "46 qubits". I could not verify the 46-qubit figure against the paper. — [IonQ customers & partners](https://www.ionq.com/customers-and-partners)
- [Confirmed] **IEEE QCE26 (Sep 2026)**, quantum AI fine-tuning with QuantumBasel and Univ. of Basel on Forte Enterprise: a "24% reduction in classification error" vs classical baselines, with energy break-even at ~34 qubits. Also a clinical EHR imputation paper using log-depth "Butterfly" QNNs. — [QCR: nine papers](https://quantumcomputingreport.com/ionq-demonstrates-hybrid-hpc-and-quantum-ai-workflows-across-nine-peer-reviewed-papers-at-ieee-quantum-week-2026/amp/)

**Protein folding / optimization (Kipu Quantum)**
- [Confirmed] **Jun 19, 2025.** BF-DCQO (non-variational, counterdiabatic) on Forte: 3-D protein folding up to 12 amino acids, plus all-to-all spin-glass QUBO and MAX-4-SAT HUBO up to 36 qubits. arXiv:2506.07866. — [IonQ news](https://ionq.com/news/ionq-and-kipu-quantum-break-new-performance-records-for-protein-folding-and)
- [Confirmed] **QCE26 follow-up**: 14–16-residue lattice folding on a 64-qubit barium trapped-ion system (46–61 physical-qubit mappings, 5-body terms). It "Recovered Classical Reference Energies Across 4 of 6 Sequences". 3rd-place best paper. — [QCR](https://quantumcomputingreport.com/ionq-demonstrates-hybrid-hpc-and-quantum-ai-workflows-across-nine-peer-reviewed-papers-at-ieee-quantum-week-2026/amp/); [IonQ best-paper news](https://www.ionq.com/news/ionq-earns-four-best-paper-awards-ahead-of-ieee-quantum-week-2026-for-breakthroughs-in-ai-hybrid-computing-and-life-sciences)

**Space (Capella SAR)**
- [Confirmed] IonQ completed its acquisition of Capella Space (SAR satellites) in July 2025. The main stated goal was space QKD. — [BusinessWire](https://www.businesswire.com/news/home/20250715219783/en/ionq-completes-acquisition-of-capella-space-advancing-vision-for-space-based-quantum-communications)
- [Confirmed] IonQ tested a quantum generative model for change detection on Capella SAR/InSAR pairs (MCAS Miramar; Piton de la Fournaise) on a trapped-ion QPU. Details come only from secondary coverage. — [Quantum Zeitgeist](https://quantumzeitgeist.com/ionq-quantum-ai-tests-real/) (via search summary)

**Not an application**
- [Confirmed] Element Six (Sep 4, 2025) is a **materials/hardware** collaboration on quantum-grade diamond films for quantum memories and photonic networking. — [IonQ IR](https://investors.ionq.com/news/news-details/2025/IonQ-Breakthrough-in-Synthetic-Diamond-Materials-Accelerates-Quantum-Networking-Scale-and-Production/default.aspx)

**2026 corporate application claims (Investor Day Sep 8, 2026; shareholder letter Apr 30, 2026)**
- [Confirmed] At Investor Day, CEO Niccolo de Masi said IonQ is developing applications in "computation engineering, logistics, predictive medicine, pharmaceuticals, advanced satellite image analysis". No performance figures were given. — [IonQ blog: Investor Day highlights](https://www.ionq.com/blog/innovating-manufacturing-and-scaling-highlights-from-ionq-investor-day-2026)
- [Confirmed] TQI reports "no speedups or benchmark results were reported" at Investor Day. Its caveats: "qubit count alone does not show whether a quantum computer can perform long and useful calculations accurately", and IonQ "did not yet disclose gate fidelities, error rates or logical-qubit results" for Superion 256 prototypes. — [TQI Sep 8, 2026](https://thequantuminsider.com/2026/09/08/ionq-uses-investor-day-to-detail-superion-roadmap-skywater-strategy-and-quantum-security-plans/)
- [Confirmed] Roadmap: Superion 256 with customer deliveries in 2027, and Superion 10K with ~10,000 physical qubits. 2026 revenue guidance was raised to $450–460M after the SkyWater close. — [TQI Sep 8, 2026](https://thequantuminsider.com/2026/09/08/ionq-uses-investor-day-to-detail-superion-roadmap-skywater-strategy-and-quantum-security-plans/); [Motley Fool](https://www.fool.com/coverage/stock-market-today/2026/09/08/stock-market-today-sept-8-ionq-raises-2026-revenue-guidance-on-investor-day/)
- [Unverified] The Investor Day deck reportedly listed EPB, MyOme and ServiceNow as "Real applications, in production today". It reportedly showed a 2026 roadmap: Q1 "Quantum-accelerated CFD for a jet engine…", Q2 "Hybrid quantum-AI vehicle routing", Q3 "Generative modeling on change detection using IonQ SAR imagery". It also reportedly mentioned protein folding and institutional portfolio rebalancing. All of this comes from a search-engine extraction of the PDF, which it called garbled. The PDF exceeded my fetch limit, and no other source mentions MyOme or ServiceNow with IonQ. — [Investor Day deck PDF](https://s28.q4cdn.com/828571518/files/content_files/IONQ-2026-Investor-Day-vFINAL-2026-09-08.pdf) (via search summary)
- [Confirmed] Shareholder letter (Apr 30, 2026): IonQ's "systems and applications… already demonstrate a commercial advantage over classical alternatives in multiple areas related to engineering, life sciences, and AI". It cites "up to 10,000x faster Time-to-Solution over leading superconducting approaches, validated by a third-party." TQI notes "many of the claims in the letter reflect IonQ's own assessments." — [IonQ shareholder letter](https://www.ionq.com/news/ionq-2025-letter-to-shareholders); [TQI May 2, 2026](https://thequantuminsider.com/2026/05/02/ionq-ceo-says-2025-marked-turning-point-for-quantum-commercialization/)
- [Confirmed] The "third-party validation" is Kearney (advised by Cascade Quantum), dated Apr 14, 2026. It verified IonQ's **methodology and reproducibility** for QFT, Hidden Shift and LR-QAOA, and for VQE on execution time and quality scoring only. Results are "timebound to the system's calibration state". The page does not show Kearney endorsing a specific multiplier. IonQ's later pages cite "up to 1,000x" vs leading superconducting platforms. — [Kearney verification page](https://www.ionq.com/resources/application-centric-benchmark-verification-report-by-kearney); [Q4 2025 call coverage](https://finance.yahoo.com/news/ionq-ionq-q4-2025-earnings-235636516.html) (via search summary)
- [Confirmed] Broader critiques:
  - IonQ's #AQ metric was criticized by Quantinuum, a competitor, per a newsletter.
  - Past timeline over-promises, such as "32 perfect qubits" in 2020.
  - A Sep 2026 newsletter argues the "408 logical qubits" decoder headline misreads a classical-decoder benchmark.

  — [postquantum.com IonQ profile](https://postquantum.com/quantum-computing-companies/ionq/) (via search summary); [Quibit News](https://buttondown.com/quibit-news/archive/ionq-s-error-decoder-is-real-but-not-fault/) (via search summary)

### Inferences
Fit of each IonQ story to a 48-hour, in-browser, ≤24–29-qubit build, with the honest caveat to state on the project page:

1. **Sparse-matrix ordering by quantum graph partitioning (Ansys/Synopsys echo). Strongest IonQ alignment and fully open on Qollab.** [Inferred]
   - **Public data:** SuiteSparse Matrix Collection structural/FEA matrices, shipped as small coarsened graphs.
   - **Quantum step:** QAOA, LR-QAOA or iterative-QAOA bisection of ≤24-node coarse separator graphs, inside nested dissection.
   - **Measurable:** fill-in (nnz of the Cholesky factor) or factorization flop count, via SciPy.
   - **Baselines:** reverse Cuthill–McKee (`scipy.sparse.csgraph`), spectral bisection, Kernighan–Lin (networkx) and exact bisection at small n.
   - **Caveat:** IonQ's 12–14.6% are amortized **wall-clock** gains on 2.6M–35M-element LS-DYNA runs that partly rely on simulation and classical refinement, and they are disputed. A hackathon can measure fill or flops, not LS-DYNA time, and should say so.
2. **Unit commitment (ORNL/EPB echo). Open; energy is named in the brief.** [Inferred]
   - **Data:** a public IEEE/standard test system.
   - **Quantum step:** QAOA or sampling over on/off bitstrings for a few generators × a window of hours, with ≤24 qubits per window. Classical economic dispatch (SciPy `linprog`/`milp`) scores each sampled commitment, mirroring ORNL's "quantum proposes, classical dispatches".
   - **Baseline:** exact MILP (SciPy `milp`) and greedy priority-list commitment.
   - **Caveat:** at these sizes MILP is exact and fast. Report the optimality gap and the probability of sampling feasible low-cost commitments, not a speedup. ORNL itself says quantum advantage is still to be tested.
3. **Flight-gate assignment (DESY echo) or aircraft loading (Airbus echo). Open.** [Inferred]
   - Both are small constrained QUBOs. The log-encoding (DESY) or slack-free constraint trick (Airbus MAL-VQA) is the technical extension that cuts qubits; 9×4 one-hot = 36 variables, too many without encoding.
   - **Baseline:** exact solution by MILP or brute force.
   - **Caveat:** neither IonQ result reported a classical comparison. Your project would be stronger than the source if it did.
4. **Shipment selection as a QAOA warm start for a classical solver (Einride echo). Open in this framing.** [Inferred]
   - Logistics is crowded only around routing/MaxCut. Honest metric: the classical solver's result with vs without the quantum warm start, as mean and distribution, not only the best case.
   - **Caveat:** Einride's data is private. Use a public instance generator or dataset and disclose it. IonQ's own mean gain was 1.7%, and 12.1% was a best case.
5. **QCBM copula for multi-asset tail risk (GE/Fidelity echo). Open.** [Inferred]
   - **Data:** public index returns shipped as CSV.
   - **Baselines:** Gaussian and t-copulas, empirical copula.
   - **Metrics:** MMD/KL and tail-dependence error on held-out data.
   - **Caveat:** GE beat classical "only in some cases" with 3–4 variables.
6. **PQC classification head on frozen sentence embeddings (IonQ LLM paper echo). Open.** [Inferred]
   - **Data:** SST-2 embeddings precomputed offline and shipped as a file (disclose this). A transformer will not run in Pyodide.
   - **Baseline:** logistic regression or MLP with matched parameter count.
   - **Caveat:** IonQ's +3.14% was in noisy simulation at comparable model size. Dequantization concerns apply.
7. **SAR/earth-observation change detection (Capella echo). Open; "space" is named in the brief.** [Inferred] Very aligned with IonQ's stated 2026 focus ("advanced satellite image analysis"), but the riskiest to execute in 48 h. Data loading into a few qubits is the bottleneck: Qollab's "What to build" lesson warns that large data loading defeats the purpose.
8. **Avoid as primary topics:** [Inferred]
   - AstraZeneca-style chemistry: QC-AFQMC at 24 Forte qubits plus GPU post-processing is not reproducible in-browser, and small VQE is saturated on Qollab.
   - Kipu-style protein folding: two Qollab projects in the past two weeks.
   - MaxCut/VRP/portfolio QAOA: Courier, Oracle and showcases already cover it.
9. **Practical algorithm choice.** [Inferred] IonQ's recent wins use **non-variational or fixed-schedule** methods: Iterative-QAOA (Synopsys), BF-DCQO (Kipu), LR-QAOA (benchmarks). These fit Qollab's one-job-per-run limit on IonQ backends (prior notes): tune angles or use a linear ramp on the local simulator, then send one batched job. This is both a technical justification and an IonQ-aligned talking point.

### Gaps
- I could not open the full Investor Day deck (>10 MB), so the "EPB / MyOme / ServiceNow in production" and the quarterly 2026 application roadmap are unverified.
- Per-model hardware vs simulation splits for the Synopsys 14.6% / ~12% claim are not reconciled in the sources I read. The arXiv paper's full text was not read.
- No independent replication was found for any IonQ application claim (AstraZeneca, Ansys/Synopsys, Einride, ORNL, Kipu, LLM, QGAN). Critiques found were Substack and newsletter level, plus TQI caveats. No peer-reviewed rebuttals were found.
- Outcome reports for Hyundai battery/VQE (2022), Hyundai object detection, the Airbus project, and EPB grid applications were not found.
- The affiliations of Topi and Ashworth on the aircraft-loading paper (presumably Airbus) are not shown on the arXiv abstract page.
- The DESY gate-assignment preprint's qubit count was not stated in IonQ's release.

---

## Q4. What language does IonQ use about applications that judges will respond to?

### Takeaway
IonQ's 2026 vocabulary rests on a few phrases:
- **"Time-to-Solution" and "Cost-to-Solution"**, measured against a quality bar fixed in advance
- **"commercial advantage"**
- **hybrid / "quantum-accelerated" workflows** that "fit seamlessly into classical workflows" alongside GPUs
- **end-to-end** results on customer-relevant problems
- **all-to-all connectivity / native gates** as the trapped-ion edge

Qollab's own voice is different: **honesty**. "shows honestly which one wins, and why"; "None of them claims an advantage"; "date the verdict with its backend".

A local panel with both Qollab and IonQ judges will likely reward a project that pairs IonQ-style framing with Qollab-style rigor: TTS and quality thresholds fixed before running, an honest scorecard, and a scaling argument tied to IonQ's roadmap. That is a hybrid, end-to-end, threshold-first benchmark.

### Cited Findings
**IonQ: outcome metrics**
- [Confirmed] Shareholder letter, Apr 30, 2026:
  - "we measure success by our customers' outcomes, not hardware specifications. Consequently, we prioritize Time-to-Solution and Cost-to-Solution."
  - "holistic system performance dictates commercial utility"
  - "Our quantum computers can already fit seamlessly into classical workflows, operating in partnership with GPU-based machine learning…"
  - "Our north star is to pioneer quantum solutions and quantum applications that create durable value across global industries"

  — [IonQ shareholder letter](https://www.ionq.com/news/ionq-2025-letter-to-shareholders)
- [Confirmed] Benchmarks page:
  - "IonQ's framework measures whether a quantum system solves real computational problems accurately," against "a verified quality standard"
  - TTS: "The clock starts at job submission and stops when a verified, qualifying answer is returned"
  - "The bar is set before any system runs. A result that misses it is not counted, regardless of how fast it was produced."
  - LR-QAOA is described as a test where "no system can get a better score by optimizing around its hardware's weaknesses."

  — [IonQ quantum benchmarks](https://www.ionq.com/quantum-benchmarks)

**IonQ: application team pitch**
- [Confirmed] The application team offers to "build and deliver turnkey solutions to explore how quantum might be able to offer advantage over existing, classical approaches." Discovery includes "Review existing classical libraries and data sets." Listed areas:
  - computer vision, materials, NLP, pharmaceuticals, geo exploration
  - portfolio balancing, credit and lending models, procurement risk, project sequencing
  - supply chain, "Package loading optimization", predictive maintenance, shipping/logistics, fleet management

  — [IonQ Applications services](https://ionq.com/applications-services)

**IonQ: 2026 focus areas and quotes**
- [Confirmed] Investor Day focus areas: "computation engineering, logistics, predictive medicine, pharmaceuticals, advanced satellite image analysis". Also: "There will be far more applications than we can think of in advance as our machines roll out." — [IonQ Investor Day highlights](https://www.ionq.com/blog/innovating-manufacturing-and-scaling-highlights-from-ionq-investor-day-2026)
- [Confirmed] Best-paper release (Sep 15, 2026), Martin Roetteler: "quantum computing can solve high-impact problems across enterprise AI, life sciences, and advanced software engineering." Synopsys's Prith Banerjee frames the CAE work as "achievable breakthroughs in the NISQ era." — [IonQ best-paper news](https://www.ionq.com/news/ionq-earns-four-best-paper-awards-ahead-of-ieee-quantum-week-2026-for-breakthroughs-in-ai-hybrid-computing-and-life-sciences); [TQI Sep 17, 2026](https://thequantuminsider.com/2026/09/17/ionq-synopsys-14-6-percent-faster-engineering-simulations/)
- [Confirmed] Synopsys release, Roetteler: "By embedding an advanced quantum algorithm into the core workflow, we reduced total simulation times by up to 14.6 percent." — [IonQ news](https://www.ionq.com/news/ionq-demonstrates-computer-aided-engineering-workload-acceleration-by-up-to-14-6-with-quantum-technology)
- [Confirmed] Kipu release: protein folding "involves several long-range interactions, which makes the all-to-all connectivity of IonQ's trapped-ion systems an important asset." — [IonQ–Kipu news](https://ionq.com/news/ionq-and-kipu-quantum-break-new-performance-records-for-protein-folding-and) (via search summary)
- [Confirmed] Earlier framing (2024, then-CEO Peter Chapman): "It is imperative that we address performance, scale, and enterprise-grade quantum solutions simultaneously to achieve commercial advantage." — [IonQ IR 2024 roadmap](https://investors.ionq.com/news/news-details/2024/IonQ-Unveils-Accelerated-Roadmap-and-New-Technical-Milestones-to-Propel-Commercial-Quantum-Advantage-Forward/default.aspx) (via search summary)

**Qollab voice (the platform judges)**
- [Confirmed] Quantum Courier is described as "a browser game that races classical and quantum solvers across five real logistics problems, and shows honestly which one wins, and why." Also: "where quantum helps is a question of problem shape, and the honest answer is sometimes no." — [Explore: Quantum Courier](https://qollab.xyz/explore/quantum-courier)
- [Confirmed] Advantage Lab's write-up praises a design that "pairs each quantum method with a meaningful classical baseline, and is explicitly shaped around IonQ-native execution paths". It also points to the trapped-ion "no SWAP gates" depth advantage. — [Explore: Quantum Advantage Lab](https://qollab.xyz/explore/quantum-advantage-lab)
- [Confirmed] Regime Radar's story spotlights "Before claiming anything for the quantum side, the team built the classical case against themselves." — [Explore: Regime Radar](https://qollab.xyz/explore/quantum-regime-radar)

### Inferences
- [Inferred] **Phrasing that should land with both judge groups:**
  - "hybrid quantum-classical workflow where a quantum subroutine is embedded in an existing classical pipeline"
  - "end-to-end", "time-to-solution and solution quality against a threshold fixed before running"
  - "all-to-all connectivity → no SWAP overhead on IonQ native gates (GPi/GPi2/MS)", shown with a transpiled-depth comparison
  - "non-variational / fixed-schedule (LR-QAOA-style) to respect one job per run"
  - "warm start for a classical solver"
  - "what this project does not claim"
- [Inferred] **Avoid unqualified "quantum advantage" or "outperforms classical" claims.** Qollab's finance page, Learn lessons and QAOA explainer explicitly debunk such claims at this scale. IonQ's own strongest claims ("commercial advantage", "up to 10,000x") are the ones critics and TQI flag. An Impact entry can borrow IonQ's metrics vocabulary (TTS, quality threshold, cost-to-solution) without borrowing the advantage claim.
- [Inferred] A credible "Impact Potential" story at hackathon scale links four steps:
  1. a real sector named in the brief
  2. an IonQ precedent: "IonQ and ORNL showed X at 26 generators on Forte; we reproduce the hybrid pattern on public data at N qubits"
  3. a measured result against a strong baseline
  4. an explicit scaling argument to IonQ's stated roadmap (Tempo / Superion 256 in 2027), labelled as projection, not result

### Gaps
- No IonQ or Qollab statement says what the hackathon judges specifically weight under "Impact Potential". The mapping above is inferred from IonQ corporate language and Qollab editorial content.
- The identities of the IonQ representatives on judging panels are unknown, so I could not check their individual research interests (e.g., whether any are on the applications team: Roetteler, Kaushik, Kim, Aboumrad, Zhu).
