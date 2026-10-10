# Measure the Quantum Step on Real Data

The strongest Quantum Impact entry puts a small quantum sampler (10–16 qubits, under about 100 IonQ-native two-qubit gates) inside a classical pipeline that works on a named public dataset. It should sit in a sector the brief names but no Qollab project has touched, and it should be measured three ways: against an exact optimum, against a tuned classical heuristic, and against a "hybrid null" that swaps the quantum sampler for a classical one. On the evidence, the best pick is **hybrid unit commitment on a public IEEE/MATPOWER grid with real EIA hourly load**, in which quantum proposes generator on/off patterns and classical dispatch prices them. It mirrors IonQ and Oak Ridge's 26-generator run on Forte and EPB's commercial Forte in Chattanooga. Close behind are two others. **Quantum graph bisection for sparse-matrix fill reduction** is an honest replay of IonQ's flagship Ansys/Synopsys engineering result. A **QCBM copula tail-risk generator** follows the template that won the UK's NQCC 2024 hackathon by extending IonQ's own paper. The brief asks for five things: a real industry problem, a hybrid method, a public dataset, a strong classical baseline, and a quantum subroutine that makes a measurable difference. As of the last check at 17:17 ET on October 9, under two hours before the 19:00 kickoff, no problem statements, datasets or theme-specific rule changes had appeared. Qollab's 109 public projects cluster on five topics: small-molecule VQE, QAOA routing and MaxCut, Markowitz portfolios, toy quantum kernels and lattice peptides. Energy, space, manufacturing, aviation, healthcare and generative finance have none, and almost no project uses a named public dataset. The judges have set the honesty bar themselves. Qollab's own QAOA explainer shows greedy search beating one-layer QAOA on Quantum Courier's showcase instance. IonQ's application headlines (12–14.6% engineering speedups, ">20×" chemistry time-to-solution, "+3.14%" LLM accuracy) are real hybrid workflows, but they were measured against soft or self-referential baselines and partly in simulation. Borrow IonQ's vocabulary, not its advantage claims. At 12–24 qubits a classical computer solves every candidate problem exactly, so the measurable quantum step can only be three things: sample quality per shot, resource efficiency (all-to-all hardware needs about a third of heavy-hex's two-qubit gates on dense cost layers), and a falsifiable estimate of what scale-up would take. Expert-judged winners from NQCC to BMW won with exactly that posture.

## The brief demands five things, and nothing new had appeared by 17:17 ET

The authoritative Quantum Impact brief sits on Qollab's Rules & terms page ([Qollab Rules & terms](https://qollab.xyz/programs/hackathon/terms)). It asks teams to solve real-world problems with quantum plus classical computing. Teams take on a real challenge in **logistics, manufacturing, space, finance, energy or another industry** with a hybrid quantum-classical approach, then:

1. choose a relevant **public dataset**;
2. build a **strong classical baseline**;
3. identify where a quantum subroutine can make a difference;
4. show the impact as better solution quality, efficiency, accuracy or another **measurable** gain.

The hub and how-it-works FAQ compress this into one sentence with the same requirements ([Qollab hackathon hub](https://qollab.xyz/programs/hackathon); [How it works](https://qollab.xyz/programs/hackathon/how-it-works)). The verbatim text of all three versions is in `impact_brief_qollab_catalog_ionq_apps.md` (Q1). **Best of Quantum Impact** is one of six specialty awards, each US$500 cash plus US$5,000 in compute. **Most Impact** is a separate specialty award, and one project can win several specialty awards as well as a placement ([How it works](https://qollab.xyz/programs/hackathon/how-it-works)). Every project is scored on four unweighted criteria: Novelty & Creativity, Technical Execution, **Impact Potential** and Documentation Quality. No descriptor says what counts as "impact" ([Qollab Rules & terms](https://qollab.xyz/programs/hackathon/terms)).

The **tutorial bar** is friendlier to Impact entries than to any other theme. The qualifying contributions it lists include a novel application or problem context, explicitly including applying an existing technique to a specific domain, and a technical extension such as noise mitigation, parameter optimization or **comparative benchmarking**. A project that misses the bar can still be scored zero on both Novelty and Technical Execution ([Qollab Rules & terms](https://qollab.xyz/programs/hackathon/terms)). The practical reading is that an existing algorithm on a real domain with a real dataset clears the bar, while a textbook QAOA on a toy graph does not. Two judging mechanics shape the design ([Qollab Rules & terms](https://qollab.xyz/programs/hackathon/terms)):

- Judges press Run on a free simulator, and IonQ simulator or hardware results neither add nor subtract points. The headline comparison must therefore reproduce on the judge's machine.
- The IonQ job is a demonstration, not a scoring lever.

**Kickoff check.** A text diff of the Rules & terms, how-it-works and hub pages at 16:56 ET found only the edits already logged on October 7–9: the MIT clause for outside repos, AI tools dropped from one bullet, and a Safari FAQ entry. Nothing changed for the Impact theme. A re-check at 17:17 ET found the hub, terms, announcements and Georgia Tech site unchanged ([Rules & terms](https://qollab.xyz/programs/hackathon/terms); [How it works](https://qollab.xyz/programs/hackathon/how-it-works)). The GT site still promises to link sponsor problem statements once each sponsor releases them ([GT Fall Fest site](https://qhackathon-gt.lovable.app/)). Qollab's newest announcement is still the August 26 ECDSA item, and the forum holds only auto-created project threads ([Qollab announcements](https://qollab.xyz/explore/news); [forum latest.json](https://forum.qollab.xyz/latest.json)). The public project API listed **109 projects at 16:56 ET**, up from 104 at 14:42. All five new ones are copies of Learn lessons, and no hackathon submissions were visible, as expected before the 19:00 ET opening ([Qollab project API](https://api.qollab.xyz/api/project/popular?limit=30)).

The likeliest venue for any IonQ problem statement or dataset is the node and global Slack, which is not publicly readable. After 19:00, re-run the catalog scripts in `scripts/qollab_api/`:

- `pag.py` paginates both the `popular` and `recent` endpoints, saves `now_popular.json` and `now_recent.json`, and prints every project missing from an older dump. Edit its hard-coded `../qollab/all_popular.json` path, or drop the diff step.
- `apps.py` pulls the write-up and main file of a named project list into `apps_writeups.txt`, so new competitors can be read as they publish.

**Qollab's staff have already said what a strong baseline means.** Their QAOA explainer (Nicolaas Spijker, September 15, 2026) dissects Quantum Courier's 24-node MaxCut showcase ([Qollab Learn: Quantum Optimization and QAOA](https://qollab.xyz/learn/quantum-optimization)):

| Solver on the Courier instance | Cut edges (of 33 possible) |
|---|---|
| Random split, average | 18.5 |
| One tuned QAOA layer, average | 25.5 (0.77) |
| Greedy local search from a random split, average | about 31, in milliseconds |
| Greedy local search, a few restarts | 33 |

So the average one-layer sample is worse than a classical heuristic. The explainer recommends reporting the best string in the tally, checked classically, rather than the average. It quotes Goemans–Williamson's 0.878 guarantee against QAOA p=1's 0.6924 on 3-regular graphs. The explainer calls the graph 37-edge, while Courier's code has 36.

The Learn lesson "Is quantum worth it in your app" prescribes a five-step protocol ([Qollab Learn: Is quantum worth it](https://qollab.xyz/learn/using-quantum-in-a-real-application/is-quantum-worth-it)):

1. Write thresholds before running anything.
2. Solve the problem classically first.
3. Solve the same task with the same inputs, output format and scoring function.
4. Judge pass or fail against the thresholds, not by relative comparison.
5. Record the date and backend.

The same lesson concludes that as of September 2026 the classical version wins for almost any shippable feature. It notes that a laptop brute-forces 36 binary variables in about a minute. It reports Regime Radar's 12-qubit kernel reading 0.1768 ideal, 0.0337 on the Aria 1 noise model and 0.1779 exact.

A companion lesson, "What to build," sorts projects by what the circuit's distribution is used for: sampling, comparing two distributions, reading structure, reducing to one number, or watching change. It warns that loading a large dataset takes longer than reading it ([Qollab Learn: What to build](https://qollab.xyz/learn/using-quantum-in-a-real-application/what-to-build)). Qollab's finance explainer praises the Spring 2026 finance projects because none claims an advantage. It states flatly that no production quantum advantage in finance has been demonstrated ([Qollab Explore: Finance](https://qollab.xyz/explore/finance)).

These pages are written by the same platform staff who sit on judging panels. An Impact entry that beats only random sampling or an untuned heuristic will be marked down by people who have already published that critique.

**What "public dataset" needs to mean in practice.** The brief does not say whether a published benchmark instance (a MATPOWER case, a SuiteSparse matrix, a scikit-learn dataset) counts. The phrase "relevant public dataset" makes it very likely acceptable; this is an inference. Because Qollab's runtime is GET-only with `Origin: null` and nothing persists between runs, the robust pattern is to ship a frozen, cited snapshot (≤2 MB per file) and offer an optional live refresh (see the runtime section).

## Qollab's 109 projects crowd five topics and leave the brief's own sectors empty

The research team paginated the API and read the write-up and main file of 33 application-relevant projects. It then keyword-scanned all 109 ([Qollab project API](https://api.qollab.xyz/api/project/popular?limit=30)). Roughly 20 projects are application-style.

**Spring 2026 Creative Challenge projects (featured, ran on IonQ hardware)**

| Project | What it does | What it reports |
|---|---|---|
| Quantum Courier ("Pizza Race") | Races classical and quantum solvers on five logistics stages | Classical wins assignment and time-windowed routing; the two tie on TSP. Quantum's "+46.2% on real IonQ Forte" MaxCut win is **against a random-cut baseline**. Four QAOA variants lost to simulated annealing (SA) on VRPTW. ([write-up](https://qollab.xyz/u/Sitifar/quantum-game-pizza-race); [Explore](https://qollab.xyz/explore/quantum-courier)) |
| Quantum Systemic Oracle | Uses 14-qubit QAOA for a crypto systemic-risk index, on a frozen live-data snapshot | QAOA contributes **5%** of the index weight. It cites about 90 two-qubit gates as Forte's envelope. ([write-up](https://qollab.xyz/u/jamie/systemic-oracle)) |
| Quantum Market Regime Radar | Classifies volatility regimes with 12-qubit amplitude-encoded GARCH fingerprints and a Bhattacharyya-coefficient kernel, against a NumPy correlation study | Concedes the classical computation is cheap and claims no speedup. ([write-up](https://qollab.xyz/u/alireza/quantum-regime-radar)) |
| qOrbital | Visualizes H₂, HeH⁺ and LiH VQE results | Hardware gallery only ([qOrbital](https://qollab.xyz/u/bawa27/qorbital)) |
| Quantum Advantage Lab | Grover, VQE, quantum walk and Trotter "races" | Says outright that no speedup exists in practice ([Explore](https://qollab.xyz/explore/quantum-advantage-lab)) |
| Market Game Theory Simulator | 2-qubit prisoner's dilemma | A teaching lens ([Spring 2026 cohort](https://qollab.xyz/explore/spring-2026-cohort)) |

The Qollab team's own library showcases (August–September 2026) are tiny "fork me" templates:

- an H₂ dissociation curve, a bond-length slider, cross-framework H₂ VQE and a methanol VQE;
- European-call circuit construction, a best-2-of-3 portfolio, and QAOA and exact solutions for a 3-variable QUBO;
- a two-moons quantum kernel, an XOR VQC and an EstimatorQNN.

These are listed in `impact_brief_qollab_catalog_ionq_apps.md` (Q2B).

Two community projects published in the last two weeks raise the rigor bar sharply:

- **QuPepFold** (September 26) runs CVaR-VQE peptide folding on a tetrahedral lattice at 10–23 qubits. It labels its energy model a seeded toy and says the problem is classically simulable ([QuPepFold](https://qollab.xyz/u/akshayuttarkar/qupepfold)).
- **Quantum-Assisted De Novo Peptide Sequence Design** (October 8, the eve of the window) is more striking ([qcat peptide design](https://qollab.xyz/u/qcat/qchemistry)). It is a QUBO→QAOA pipeline with p ≤ 3 and ≤ 20 qubits. At 16 qubits, QAOA hits the optimum per feasible shot at 0.0081 against 0.0078 for uniform sampling, which the author equates to about one uniform random sample. At 40 variables, a windowed QAOA finds the optimum in 31.3 s while a classical window search finds it in **0.02 s**. The project has an explicit section listing what it does not claim.

Judges who have seen qcat's page will expect matched classical controls and an explicit non-claims section from every Impact entry. Four empty projects published October 8–9 look like hackathon teams staging; one, "MejorRuta," describes a 5-city routing idea. Routing will get more crowded, not less.

**Crowded versus open, from the full-text scan of 109 projects** ([Qollab project API](https://api.qollab.xyz/api/project/popular?limit=30)):

| Status | Topics |
|---|---|
| **Saturated** | Molecules (10 projects, mostly H₂/LiH/HeH⁺ VQE); portfolio (4); lattice protein folding or design (3); quantum kernels (3); routing/MaxCut QAOA (Courier, plus staging shells); option pricing and amplitude estimation (showcases only) |
| **Zero hits, and named in the brief** | Unit commitment / power grid; satellite / SAR; cargo or aircraft loading; job-shop scheduling; supply chain; warehouse |
| **Zero hits, other industries** | Graph partitioning, finite element, sparse linear algebra; fraud, anomaly, credit; healthcare, medical, genomics; climate; time series and forecasting; QCBM / Born machine / copula; facility location; independent set; feature selection; EV charging; catalyst / lithium; LLM / language model |
| **Datasets** | "Dataset" appears in only 6 projects, and **none uses a named public benchmark dataset** for an industry problem |

The open lanes map one-to-one onto IonQ's own application stories:

| Lane | IonQ story |
|---|---|
| Energy | ORNL and EPB grid work |
| Manufacturing / CAE | Ansys and Synopsys partitioning |
| Aviation | DESY gate assignment and Airbus loading |
| Logistics beyond routing | Einride shipment selection |
| Space | Capella SAR |
| Generative finance | GE and Fidelity copulas |
| AI | The LLM classification head |

Courier's roadmap mentions a grid-storage-siting QUBO on the IEEE 14-bus testbed as a DOE submission. It is unpublished on Qollab, but it means energy is not entirely unclaimed in people's heads ([Quantum Courier write-up](https://qollab.xyz/u/Sitifar/quantum-game-pizza-race)). The scan reads only each project's main file and write-up, so domain terms used only in secondary files would be missed, and private or draft projects are invisible.

## IonQ's portfolio puts small quantum cores inside big classical pipelines, measured against soft baselines

### Each flagship result measured something narrower than its headline

IonQ's 2022–2026 application work follows one pattern. A small quantum subroutine (QAOA variants, VarQITE, QC-AFQMC shadows, QCBMs, PQC heads) sits inside a large classical pipeline on 12–36 hardware qubits. The headline gain is measured end to end, and larger sizes run only in simulation. The table pairs each headline with what it was actually measured against.

| Partner, date | Problem and quantum step | Headline | What it was measured against, and the caveat |
|---|---|---|---|
| **Ansys**, Mar 2025 | VarQITE graph partitioning to cut fill-in in LS-DYNA's sparse solver (blood pump, meshes up to 2.6M vertices) | "Up to 12%" faster | Wall-clock on some problems. The large instances ran in classical simulation, hardware graphs were coarsened to ≤32 nodes, and a Fiduccia–Mattheyses-style refinement cleaned up hardware samples. A critique says the mesh was refined about 100× and the other two cases saw no speedup. ([IonQ news](https://www.ionq.com/news/ionq-and-ansys-achieve-major-quantum-computing-milestone-demonstrating); [arXiv:2503.13128](https://arxiv.org/abs/2503.13128); [Kirkpatrick critique](https://wkirkpatrick.substack.com/p/ionq-and-ansys)) |
| **Synopsys**, Sep 2026 | Non-variational Iterative-QAOA graph partitioning that reorders the equations before solving (automobile, drill, impeller and jet-engine models, up to 35M points) | At least 5.9% and up to 14.6% less simulation time; 1st-place Best Paper, IEEE Quantum Week 2026 | Simulations ran up to 150 qubits (CUDA-Q); physical runs were on 36-qubit Forte. The paper's own range (about 7–15%) differs from the release. A secondary summary says 14.6% was simulated and ~12% was the Forte best case; unverified. ([IonQ news](https://www.ionq.com/news/ionq-demonstrates-computer-aided-engineering-workload-acceleration-by-up-to-14-6-with-quantum-technology); [arXiv:2603.15515](https://arxiv.org/abs/2603.15515); [QCR](https://quantumcomputingreport.com/ionq-demonstrates-hybrid-hpc-and-quantum-ai-workflows-across-nine-peer-reviewed-papers-at-ieee-quantum-week-2026/amp/)) |
| **AstraZeneca + AWS + NVIDIA**, Jun 2025 | QC-AFQMC with matchgate shadows on an (8e,8o) slice of a Ni-catalysed Suzuki–Miyaura oxidative addition; 24 Forte qubits (16 trial + 8 leakage ancillas) | ">20×" time-to-solution | Against IonQ's own earlier 4-qubit workflow, not a classical method. Within the 20×: 9× is QPU circuit time and 656× is GPU post-processing. QPU barriers were about 10 kcal/mol off CCSD(T) (ideal simulator about 4), at 13–17k GPU-hours per molecule. ([IonQ news](https://ionq.com/news/ionq-speeds-quantum-accelerated-drug-development-application-with); [arXiv:2506.22408](https://arxiv.org/html/2506.22408v1)) |
| **ORNL (DOE GRID-Q)**, Jun–Jul 2025 | Quantum sampler proposes generator commitments; classical Benders-style heuristic plus SLSQP dispatch; 3, 10 and 26 units × 24 h on Forte Enterprise | Within 0.55–2.7% of optimal cost (about 2.5% at 26 units) in simulation; hardware "similar" | A feasibility demonstration. ORNL says advantage is for future testing. IonQ forecasts 100–200 high-fidelity qubits for grid scale [vendor]. ([IonQ news](https://ionq.com/news/ionq-partners-with-oak-ridge-national-laboratory-demonstrating-quantum-power); [arXiv:2505.00145](https://arxiv.org/html/2505.00145v1); [TQI](https://thequantuminsider.com/2025/06/08/ionq-oak-ridge-researchers-use-quantum-classical-algorithm-to-solve-power-grid-problem/)) |
| **EPB Chattanooga**, Apr 2025 onward | US$22M shared Forte Enterprise and networking hub, with joint grid-optimization work | Commissioned by Sep 2026 | No published grid result found ([IonQ news](https://ionq.com/news/ionq-announces-usd22m-deal-with-epb-establishing-chattanooga-tennessee-as); [QCR](https://quantumcomputingreport.com/epb-commissions-ionq-forte-enterprise-quantum-computer-in-chattanooga-hub/)) |
| **Airbus**, 2022 project; Apr 2025 paper | Aircraft loading with multi-angle QAOA and slack-free inequality handling, 12–28 qubits on Aria and Forte | Optimal solutions on all instances; about 70% P(opt) at 12 qubits with 1,000 shots | No head-to-head classical benchmark ([arXiv:2504.01567](https://arxiv.org/abs/2504.01567)) |
| **DESY**, runs Sep 2023, release Mar 2024 | Flight-gate quadratic assignment with log-linear encoding (36 variables → 18 qubits) on Aria | DESY called the results encouraging | Only small cases were tuned on hardware; no classical runtime or quality comparison ([IonQ blog](https://ionq.com/blog/ionq-and-desy-tackle-the-gate-assignment-problem); [IonQ news](https://ionq.com/news/ionq-and-desy-research-highlights-quantums-potential-benefits-for-airport)) |
| **Einride**, 2026 paper | Enhanced QAOA as a **warm start** for a classical shipment-selection MIQP; 20–35 qubits on hardware, 90–130 on an MPS simulator | Mean **+1.7%** shipments delivered, best case +12.1% | Private data. Distance per shipment rose 1.9%. ([arXiv:2604.11758](https://arxiv.org/pdf/2604.11758), via search summary) |
| **GE Research**, Jun 2022 | QCBM copula for 3–4 stock indexes on IonQ hardware | Beat classical models only in some cases; comparable or better in the paper's wording | Training degraded with scale, fixed by an annealing-style schedule ([IonQ news](https://ionq.com/news/june-23-2022-ionq-ge-research-risk-aggregation); [arXiv:2206.11937](https://arxiv.org/abs/2206.11937)) |
| **Fidelity CAT**, 2021 | "Qopula": Bell/GHZ-seeded copula ansatz, QGAN and QCBM on 2-variable stock data, up to 8 hardware qubits | Outperformed "equivalent" classical generative learning; 20–1000× fewer training iterations | Small, two-variable ([arXiv:2109.06315](https://www.arxiv.org/pdf/2109.06315v1)) |
| **IonQ LLM fine-tuning**, Apr 2025 | Re-uploading PQC head (10–18 qubits) on frozen 768-d sentence embeddings, SST-2 SetFit split | "Up to 3.14%" accuracy gain | 3.14 points is 92.70% against an SVC (89.56%), not a size-matched head. The best NN head reached 91.44%, and end-to-end fine-tuning 93.62%. Noisy simulation only. ([arXiv:2504.08732](https://arxiv.org/html/2504.08732)) |
| **QuantumBasel**, 2026 | Same head with inference on Forte Enterprise | 91.2% on hardware against 92.06% noiseless; energy break-even projected at about 34 qubits | Only **250** test samples; the authors call it a proof of concept ([TQI](https://thequantuminsider.com/2026/07/21/ionq-quantumbasel-study-suggests-hybrid-ai-workloads-could-gain-energy-advantages-from-quantum-hardware-as-systems-scale/)) |
| **Hyundai**, 2025 | QCBM latent prior for a classical Wasserstein GAN of steel microstructures, on Aria | Better MMD than Bernoulli-prior GANs in 70% of samples | Baseline is not a tuned classical generator ([arXiv:2504.08728](https://arxiv.org/abs/2504.08728)) |
| **Kipu Quantum**, Jun 2025 | BF-DCQO lattice protein folding (≤12 residues) and 36-qubit spin-glass / MAX-4-SAT runs on Forte | Optimum reached on all peptides | Only with SA post-processing on the best 5% of samples ([IonQ news](https://ionq.com/news/ionq-and-kipu-quantum-break-new-performance-records-for-protein-folding-and); [arXiv:2506.07866](https://arxiv.org/html/2506.07866v1)) |
| **Capella Space**, acquired Jul 2025 | SAR satellites, acquired mainly for space QKD; a quantum generative change-detection test on SAR pairs | Secondary coverage only | ([BusinessWire](https://www.businesswire.com/news/home/20250715219783/en/ionq-completes-acquisition-of-capella-space-advancing-vision-for-space-based-quantum-communications); [Quantum Zeitgeist](https://quantumzeitgeist.com/ionq-quantum-ai-tests-real/)) |

Read together, the table yields three lessons:

- **Every IonQ claim measures the whole workflow, and the quantum core is small.** That is a pattern a hackathon can copy honestly.
- **The baselines are where critics attack.** The targets are IonQ's own prior work (AstraZeneca), an unmatched SVC (LLM), Bernoulli GANs (QGAN), LS-GPart rather than METIS (Ansys, per a search summary of the paper), or nothing at all (DESY, Airbus).
- **Simulation carries the large instances.** Hardware runs stay at 12–36 qubits, often with classical post-processing doing visible work.

No independent replication of any IonQ application claim was found.

### The 2026 corporate claims are bigger, and the critics are louder

At its September 8, 2026 Investor Day, IonQ named its application focus as computation engineering, logistics, predictive medicine, pharmaceuticals and advanced satellite image analysis. It gave no performance figures ([IonQ Investor Day highlights](https://www.ionq.com/blog/innovating-manufacturing-and-scaling-highlights-from-ionq-investor-day-2026)). TQI noted that no speedups or benchmarks were reported, and that IonQ disclosed no gate fidelities, error rates or logical-qubit results for its Superion 256 prototypes. TQI also gave the roadmap: Superion 256 deliveries in 2027, with 2026 revenue guidance raised to US$450–460M ([TQI, Sep 8 2026](https://thequantuminsider.com/2026/09/08/ionq-uses-investor-day-to-detail-superion-roadmap-skywater-strategy-and-quantum-security-plans/)). A garbled extraction of the Investor Day deck reportedly listed EPB, MyOme and ServiceNow as applications already in production and showed a 2026 application roadmap (jet-engine CFD, hybrid quantum-AI vehicle routing, SAR change detection). This is unverified; the PDF was too large to fetch.

The April 30, 2026 shareholder letter says IonQ systems already show "commercial advantage" in engineering, life sciences and AI. It cites "up to 10,000x" faster time-to-solution than superconducting approaches, validated by a third party ([IonQ shareholder letter](https://www.ionq.com/news/ionq-2025-letter-to-shareholders)). The third party, Kearney, verified the **methodology and reproducibility** of IonQ's application-centric benchmarks (QFT, Hidden Shift, LR-QAOA and VQE timing). Its page does not endorse a multiplier, and it says results are bound to the system's calibration state ([Kearney verification page](https://www.ionq.com/resources/application-centric-benchmark-verification-report-by-kearney)). TQI notes many letter claims reflect IonQ's own assessments ([TQI, May 2 2026](https://thequantuminsider.com/2026/05/02/ionq-ceo-says-2025-marked-turning-point-for-quantum-commercialization/)). One fresh item is useful context: **IonQ entered Stage C of DARPA's Quantum Benchmarking Initiative on October 7, 2026**, two days before kickoff ([IonQ news](https://ionq.com/news/ionq-advances-to-final-stage-of-darpas-quantum-benchmarking-initiative)). QBI defines utility-scale as a computer whose computational value exceeds its cost, with a 2033 target ([DARPA QBI](https://www.darpa.mil/research/programs/quantum-benchmarking-initiative)).

### Pair IonQ's metrics vocabulary with Qollab's honesty vocabulary

IonQ's 2026 language rests on outcomes, not hardware specifications ([IonQ shareholder letter](https://www.ionq.com/news/ionq-2025-letter-to-shareholders)):

- **Time-to-Solution and Cost-to-Solution**;
- quantum systems that **fit into classical workflows** alongside GPUs;
- **end-to-end** results on customer problems.

Its benchmark page defines time-to-solution from job submission until a verified, qualifying answer returns, against a quality bar **set before any system runs** ([IonQ quantum benchmarks](https://www.ionq.com/quantum-benchmarks)). The applications team pitches turnkey work that starts by reviewing existing classical libraries and datasets. Its stated areas include package loading, procurement risk, project sequencing, predictive maintenance and fleet management ([IonQ Applications services](https://ionq.com/applications-services)). Kipu releases stress that all-to-all connectivity suits long-range interactions ([IonQ–Kipu news](https://ionq.com/news/ionq-and-kipu-quantum-break-new-performance-records-for-protein-folding-and)). Martin Roetteler frames the Synopsys result as embedding a quantum algorithm into the core workflow ([IonQ news](https://www.ionq.com/news/ionq-demonstrates-computer-aided-engineering-workload-acceleration-by-up-to-14-6-with-quantum-technology)).

Qollab's editorial voice is different. It praised Courier for showing honestly which solver wins and why, Advantage Lab for pairing each quantum method with a meaningful classical baseline on IonQ-native execution paths, and Regime Radar for building the classical case against itself first ([Explore: Quantum Courier](https://qollab.xyz/explore/quantum-courier); [Explore: Quantum Advantage Lab](https://qollab.xyz/explore/quantum-advantage-lab); [Explore: Regime Radar](https://qollab.xyz/explore/quantum-regime-radar)).

The phrasing likely to land with a mixed Qollab–IonQ panel combines the two:

- "a hybrid workflow with one quantum subroutine embedded in an existing classical pipeline";
- "time-to-solution and solution quality against a threshold fixed before running";
- "all-to-all connectivity means no SWAP overhead on IonQ's native ZZ", backed by a transpiled gate-count comparison;
- "fixed-schedule (LR-QAOA or Iterative-QAOA style) so one job per run suffices";
- "warm start for a classical solver";
- "what this project does not claim".

Avoid unqualified "quantum advantage" and "outperforms classical." Qollab's Learn pages debunk them at this scale, and IonQ's own strongest versions are exactly the claims TQI and critics flag.

## Past application winners scoped tiny, benchmarked hard, and explained their losses

### Expert panels rewarded a small run, a named comparator and a scaling section

The UK's NQCC hackathons are the closest analogue, because they use industry use cases and expert panels. The **2024 rubric** is published and totals 55 points ([NQCC 2024 report](https://nqcc.ac.uk/wp-content/uploads/2025/04/NQCC_Quantum-Hackathon-2024_Technical-report.pdf)):

| Criterion | Points | What it covers |
|---|---|---|
| Success | 10 | Includes comparison with the best classical solution, and verification |
| Creativity given the use case | 10 | |
| Scaling and feasibility | 10 | What happens beyond the toy, and what hardware a full solution needs |
| Responsible quantum computing | 10 | Includes cutting through overhype |
| Presentation | 10 | |
| Q&A | 5 | |

The 2024 winner, **KL Divergents**, modelled insurance losses from natural disasters. They extended IonQ and GE's trapped-ion copula paper in four ways:

- a mixed financial-and-insurance portfolio;
- a randomized-split KL loss that cut the data needed;
- a quantitative evaluation against a classical baseline;
- inference on Quantinuum hardware and on IonQ via Classiq.

Judge Stasja Stanisic named the structured comparison against other solutions as decisive, and BT's Cathy White praised the students for not claiming quantum advantage without proper evidence ([Physics World](https://physicsworld.com/a/quantum-hackathon-makes-new-connections/)). The other 2024 placings were:

- **2nd:** a BT network-coverage vertex cover, solved on D-Wave's hybrid solver, with QAOA promising in simulation.
- **3rd:** NHS A&E forecasting. The team pivoted after finding quantum MCMC unsuitable and used a **fake linear-growth time series** instead of real data ([NQCC 2024 report](https://nqcc.ac.uk/wp-content/uploads/2025/04/NQCC_Quantum-Hackathon-2024_Technical-report.pdf)).

NQCC 2023 ([NQCC 2023 report](https://www.nqcc.ac.uk/wp-content/uploads/2024/04/NQCC_Quantum-Hackathon-2023_Technical-report.pdf)):

- **1st, Rolls-Royce:** CVQLS linear solvers for CFD/FEM, 4×4 on hardware (IBM and IonQ) and 16×16 in simulation.
- **2nd, Jacobs:** quantum amplitude estimation (QAE) for neutron transport. The team openly reported large deviations from analytic answers.
- **3rd:** vaccination-centre set cover with N ≤ 4 sites.
- A **unit-commitment use case that did not place.**

NQCC 2025 went to road-maintenance closure scheduling, 3D bin packing and diabetes QML, with methods unpublished ([NQCC 2025](https://www.nqcc.ac.uk/uk-quantum-hackathon-2025)).

Multi-month industry prizes reward the same posture.

**BMW 2021** ([AWS](https://aws.amazon.com/blogs/quantum-computing/winners-announced-in-the-bmw-group-quantum-computing-challenge)):

- Criteria: comprehensibility, feasibility, scalability, innovation and benefit to BMW.
- Two of four winners said classical methods win today. Accenture shipped a full sensor-placement workflow with plug-ins for future quantum methods. QC Ware's image classification was praised for clarifying future potential while conceding that classical is better now.
- 1QBit/NTT added a fault-tolerant scaling analysis.

**Airbus–BMW 2024** ([AWS](https://aws.amazon.com/blogs/quantum-computing/winners-announced-in-the-airbus-bmw-group-quantum-computing-challenge)):

- 4colors won with a solver that runs classically today and accepts quantum plug-ins.
- TU Delft won partly on a quantum-inspired classical heuristic.

**Airbus 2020:** won by Machine Learning Reply's practical annealing cargo-loading optimizer. The finalists that claimed O(polylog N) or order-of-magnitude gains, while conceding they needed fault tolerance and QRAM, did not win ([Reply](https://www.reply.com/en/newsroom/news/machine-learning-reply-wins-the-airbus-quantum-computing-challenge); [TQI](https://thequantuminsider.com/2020/10/22/airbus-names-its-five-finalists-for-quantum-computing-challenge/)).

**Deloitte Quantum Climate Challenge:**

- 2022: the winning Quantimize repository concludes that a classical genetic algorithm is the best choice for now ([Quantimize GitHub](https://github.com/fjelljenta/Quantum-Challenge)).
- 2023: EcoQult won by comparing classical and quantum methods on resources, runtime and accuracy, with VQE corrections on a cheap classical estimate ([TQI](https://thequantuminsider.com/2023/05/08/quantum-climate-challenge-team-ecoqult-wins-the-deloittes-quantum-climate-challenge/)).

**Grand challenges** formalize the bar.

**XPRIZE Quantum Applications** (finalists December 2025, winners spring 2027) scores four things: projected impact, estimated quantum resources, strength of evidence, and novelty. Phase II demands benchmarking against state-of-the-art classical methods, with detailed fault-tolerant resource estimates ([XPRIZE](https://www.xprize.org/prizes/qc-apps); [Google blog](https://blog.google/technology/research/google-gesda-xprize-quantum-applications-finalists/)).

**Wellcome Leap's Q4Bio:**

- It paid **US$2M to Algorithmiq, Cleveland Clinic and IBM** for a 100-qubit photosensitizer excited-state workflow that showed a "trajectory" toward advantage ([IBM](https://www.ibm.com/quantum/blog/q4bio-finalists)).
- Its US$5M advantage prize reportedly went unawarded ([TQI](https://thequantuminsider.com/2026/04/16/wellcome-leap-quantum-for-bio-challenge-prize/)).

**QHack** winners show the value of a single methodological improvement on a known pipeline ([AWS QHack 2023](https://aws.amazon.com/blogs/quantum-computing/announcing-the-amazon-braket-challenge-winners-of-the-qhack-2023-hackathon)):

- **Avocados** cut qubits with unbalanced penalization for inequality-constrained portfolios. At 10 assets they reported about **1,400× higher probability of the optimal solution** than the slack-variable encoding, running on IonQ among other devices.
- **jetix** froze near-constant VQE parameters for a carbon-capture molecule: 60.8% faster convergence for a 2.82% error increase.

Both gains were measured against the standard quantum method, not against classical solvers. Both teams won repeatedly with the same move.

### Over-claiming won only where nobody checked

At the online student event CQhack25, all six winners were applications, and several over-claimed. Q-MediScan claimed a 37.8% improvement over classical methods and 10.6 lives saved per 1,000 patients from a 6-qubit VQC on the 569-sample UCI breast-cancer set. Other winners claimed that QAOA explores every route at once on a 3-node VRP, or that a one-bit simulated teleportation gives security beyond any classical encryption ([CQhack25 gallery](https://cqhack25.devpost.com/project-gallery); [Q-MediScan](https://devpost.com/software/q-mediscan)). No expert-judged venue was found rewarding claims like these. NQCC's responsible-computing criterion explicitly penalizes hype.

The recurring failure modes are:

1. toy or synthetic data in place of the real dataset;
2. instances so small that brute force is trivial, with no scaling story;
3. baselines that are random, untuned, or other quantum methods only;
4. advantage language;
5. algorithms that turn out to be the wrong fit late, such as quantum MCMC for full distributions or an untrainable QNN;
6. compile blockers (Rolls-Royce's QSVT would not compile to QASM);
7. asymptotic claims that need QRAM.

An honest loss to classical is survivable only with a diagnosis of why (encoding, depth, noise) and what would change it. Johnson Matthey's 2024 feature-selection team reported that the classical approach beat the quantum one, without that analysis, and did not place ([NQCC 2024 report](https://nqcc.ac.uk/wp-content/uploads/2025/04/NQCC_Quantum-Hackathon-2024_Technical-report.pdf)).

**Mapping NQCC's rubric onto Qollab's four criteria** gives a clear template:

| NQCC element | Qollab criterion |
|---|---|
| Success, classical comparison and verification | Technical Execution |
| Creativity given the use case | Novelty |
| Scaling and responsible framing | Impact Potential |
| Presentation and Q&A | Documentation |

Qollab judges read the page and press Run instead of asking questions, so "verification" becomes a seeded, reproducible run that regenerates the baseline-versus-quantum table on their machine. The cheapest high-value addition is a scaling-and-resources section. It costs no qubits, and every serious rubric asks for it.

## Use-case families: what is technically true at 12–24 qubits

The hard constraints, carried over from the earlier briefings:

- Qiskit 2.5.x in Pyodide;
- the built-in 24-qubit statevector simulator;
- IonQ Forte noise models up to 29 qubits;
- IonQ's native GPi/GPi2/ZZ(θ) gates with all-to-all connectivity;
- roughly a 100-two-qubit-gate budget at about 0.5% error per gate;
- one IonQ job per run, and no dynamic circuits.

The algorithm fundamentals (QAOA guarantees, DQI, barren plateaus, QSVT) are covered in `Quantum Unlocked theme deep dive/algorithms_and_complexity.md` and are not repeated here.

A noise rule of thumb runs through every family. Treat global fidelity as F ≈ 0.995^(number of two-qubit gates) (research-team arithmetic, ignoring one-qubit and readout error).

| Two-qubit gates | 36 | 45 | 66 | 78 | 91 | 100 | 132 | 198 |
|---|---|---|---|---|---|---|---|---|
| F at 0.5% error | 0.835 | 0.798 | 0.718 | 0.676 | 0.634 | 0.606 | 0.516 | 0.371 |

At 0.7% error, 66 gates give 0.63 and 100 gates give 0.50. A useful proxy for the noisy success probability is P_noisy ≈ F·P_ideal + (1−F)·2⁻ⁿ. Real noise concentrates near low-Hamming-distance states, so this is roughly a lower bound. Verify every number on the qiskit-ionq Forte noise model before quoting it.

### Optimization: on a 100-gate budget, encoding matters more than algorithm

**The gate arithmetic.** On IonQ, every nonzero quadratic QUBO coupling costs exactly one native ZZ per QAOA layer, and a k-body term costs **2k−3** two-qubit gates (3 for 3-body, 5 for 4-body, 7 for 5-body). Quadratizing a product instead costs an extra qubit and three couplings. Under a 29-qubit cap, it is usually better to keep higher-order (HUBO) terms native (research-team derivation in `optimization_use_cases.md`). **One-hot encodings exhaust the budget.** An m-way one-hot group adds m(m−1)/2 couplings. TSP needs (n−1)² qubits (16 at 5 cities, 25 at 6), and its constraint graph alone has 48 couplings at 5 cities and 100 at 6, before any distances. That is one more reason routing is a poor Impact choice.

**Penalties.** The standard construction is H = A·H_constraints + B·H_objective, with A large enough that breaking a constraint never pays ([Lucas, arXiv:1302.5843](https://arxiv.org/abs/1302.5843)). Glover's tutorial gives the quadratic penalties ([Glover et al., arXiv:1811.11538](https://arxiv.org/abs/1811.11538)):

| Constraint | Penalty |
|---|---|
| x + y ≤ 1 | P·xy |
| x + y = 1 | P(1−x−y+2xy) |
| x ≤ y | P(x−xy) |
| Ax = b | P(Ax−b)² |

One library trap matters for any real-valued dataset. qiskit-optimization's `LinearEqualityToPenalty` auto-penalty **falls back to 1e5 if any constraint coefficient is fractional**. Otherwise it uses 1 plus the ranges of the objective coefficients ([qiskit-optimization source](https://raw.githubusercontent.com/qiskit-community/qiskit-optimization/main/qiskit_optimization/converters/linear_equality_to_penalty.py)). With megawatts or prices, that fallback flattens the landscape. Set P by hand slightly above the largest single-variable objective swing, then sweep 0.5–4× and plot feasibility rate against P(optimal). That curve is itself a judge-legible result. Rescale the Hamiltonian, for example so the largest coefficient is 1, before applying any fixed or transferred angles.

**Constraint-preserving mixers and compact encodings.**

- **XY mixers.** The quantum alternating operator ansatz replaces penalties with mixers that stay in the feasible subspace ([Hadfield et al., arXiv:1709.03489](https://arxiv.org/abs/1709.03489)). XY mixers preserve Hamming weight ([Wang et al., arXiv:1904.09314](https://arxiv.org/abs/1904.09314)). On IonQ each XY term costs two native gates, so a ring mixer costs about 2n per layer. The initial state can be a greedy k-hot basis state at zero extra cost. JPMorgan ran Hamming-weight-preserving XY-QAOA on trapped ions up to 20 qubits. It noted that penalty methods force a trade-off between staying in the constraint and solution quality ([Niroula et al., arXiv:2206.06290](https://arxiv.org/abs/2206.06290)).
- **Domain-wall encoding** needs m−1 qubits per m-valued variable ([Chancellor, arXiv:1903.05068](https://arxiv.org/abs/1903.05068)).
- **Log/binary encodings** save more qubits but create higher-order terms and invalid codewords ([Sawaya et al., arXiv:2203.14432](https://arxiv.org/abs/2203.14432)). IonQ–DESY's log-linear encoding put 36 gate-assignment variables on 18 Aria qubits ([IonQ blog](https://ionq.com/blog/ionq-and-desy-tackle-the-gate-assignment-problem)).
- **Inequalities without slack qubits.** Use unbalanced penalization (Avocados) or Airbus's multi-angle construction ([arXiv:2504.01567](https://arxiv.org/abs/2504.01567)).
- **Pauli Correlation Encoding** packs O(nᵏ) binaries into n qubits through the signs of Pauli correlators. It is variational and shot-hungry, not peaked sampling ([arXiv:2401.09421](https://arxiv.org/abs/2401.09421)).

**Decomposition honesty.** IonQ's Iterative-QAOA job-shop paper solved a 1,300-variable master instance classically to its optimal makespan of 193. It then built 24–36-qubit sub-instances by **freezing most variables to the known optimum**, so every subproblem contained the global optimum by construction ([arXiv:2510.26859v2](https://arxiv.org/html/2510.26859v2)). The credible hackathon version freezes around a heuristic incumbent (greedy, SA or a short CP-SAT run). It then uses the quantum sampler as a large-neighbourhood-search move and reports how often the move improves the incumbent. Other decompositions are:

- QAOA-in-QAOA graph splitting ([arXiv:2205.11762](https://arxiv.org/abs/2205.11762));
- ADMM for unit commitment ([arXiv:2201.03701](https://arxiv.org/pdf/2201.03701));
- recursive QAOA, which eliminates variables with the strongest measured ZZ correlation ([Bravyi et al., arXiv:1910.08980](https://arxiv.org/abs/1910.08980)).

**Which algorithms have 2025–2026 evidence on trapped ions**

| Method | How it works | Evidence and caveat |
|---|---|---|
| **LR-QAOA** | Fixed linear ramp, no optimizer | Success probability scales as 2^(−η(p)N+C), with η falling from 0.22 at p=10 to 0.05 at p=100. Ran on IonQ, Quantinuum and IBM up to 109 qubits and p=100 [independent] ([Montañez-Barrera & Michielsen, arXiv:2405.09169](https://arxiv.org/abs/2405.09169)) |
| **Iterative-QAOA** (IonQ) | Schedule β_k=(1−k/p)Δβ, γ_k=((k+1)/p)Δγ, with Δβ=Δγ=0.17. Boltzmann-weighted samples set the next product-state warm start, over 10 iterations of 4,000 shots | 24q/p4 used 312 RZZ; 32q used 780. At 32 qubits P(opt) was 0.780 ideal, **0.007 raw on the QPU** and 0.693 after "DNL" mitigation. At 36 qubits P(opt) was 0. LR-QAOA at 24q needed p=50 (3,900 gates) for 3.82%. VarQITE needed about 1M executions and reached only excited states [vendor] ([arXiv:2510.26859v2](https://arxiv.org/html/2510.26859v2)) |
| **Multi-angle QAOA** | One angle per term | Airbus loading: optimum at 12–28 qubits, about 70% at 12 qubits ([arXiv:2504.01567](https://arxiv.org/abs/2504.01567); [Herrman et al., arXiv:2109.11455](https://arxiv.org/abs/2109.11455)) |
| **Warm-start QAOA** | Ry(2·arcsin√cᵢ) from a continuous relaxation, with a matching mixer | Keeps the Goemans–Williamson guarantee at depth 0; `WarmStartQAOAOptimizer` in qiskit-optimization ([Egger et al., arXiv:2009.10095](https://arxiv.org/abs/2009.10095)) |
| **BF-DCQO** (Kipu) | Counterdiabatic, non-variational, with bias-field iterations | Kipu's IBM runtime-advantage claim was disputed by D-Wave staff ([arXiv:2509.14358](https://arxiv.org/abs/2509.14358)) and independently by Tuziemski et al., who found the advantage disappears under more comprehensive benchmarking ([arXiv:2510.06337](https://arxiv.org/abs/2510.06337)). A classical "BF-Null" control reportedly matches it ([arXiv:2604.02617](https://arxiv.org/pdf/2604.02617)). Kipu's March 2026 end-to-end study claims only "competitive", with parallel tempering and GPU solvers reaching or surpassing it ([arXiv:2603.13607](https://arxiv.org/abs/2603.13607)) |
| Annealing | Quantum annealing correction on D-Wave | USC's scaling advantage for approximate optimization ([arXiv:2401.07184](https://arxiv.org/pdf/2401.07184)) was matched by GPU simulated bifurcation ([arXiv:2505.22514](https://arxiv.org/pdf/2505.22514)). In April 2026 a classical mean-field algorithm beat every quantum result on binary paint shop ([arXiv:2604.00607](https://arxiv.org/html/2604.00607v2)) |
| GAS, DQI, QeMCMC | Grover adaptive search; decoded quantum interferometry; quantum-enhanced MCMC | GAS and DQI oracles run to hundreds or thousands of gates, so simulator-only. Four 2025–2026 critiques narrow DQI's advantage ([arXiv:2509.19966](https://arxiv.org/abs/2509.19966); [arXiv:2607.28120](https://arxiv.org/abs/2607.28120)). QeMCMC needs many short jobs, which conflicts with one job per run ([Layden et al., arXiv:2203.12497](https://arxiv.org/abs/2203.12497)) |

The theory backdrop is sobering. A 2025 workshop report concludes that log-depth QAOA has no asymptotic advantage for a large class of sparse problems ([arXiv:2508.13973](https://arxiv.org/pdf/2508.13973)). The main positive scaling claim remains fixed-parameter QAOA on LABS, up to 40 qubits in noiseless simulation ([Shaydulin et al., arXiv:2308.02342](https://arxiv.org/abs/2308.02342)). For a one-job build, the ranking is:

1. LR-QAOA or Iterative-QAOA, with all but the final iteration on the noise model;
2. warm-start QAOA at p=1–2;
3. multi-angle QAOA trained in simulation;
4. BF-DCQO-style bias loops, but only with a classical-null ablation.

"Found the optimum" claims from vendors nearly always involve post-processing. Report raw, mitigated and post-processed results separately, plus what the post-processor achieves alone from random inputs.

**Expected signal.** As an illustration, take n=12 at 66 gates with an ideal P(opt) of 0.30. The noisy P(opt) is about 0.22, so TTS99 is about 19 shots, against 18,861 for uniform random sampling. At n=16, 96 gates and an ideal 0.10, it is about 72 shots. Connectivity is the IonQ-native story:

| n | Complete-graph cost layer on IonQ (native ZZ) | Linear-chain swap network (CNOTs) |
|---|---|---|
| 12 | 66 | ≈198 |
| 14 | 91 | ≈273 |
| 16 | 120 | ≈360 |

That is about 3× fewer on IonQ; heavy-hex is similar or worse. These are swap-network estimates, so measure them by transpiling the same circuit against an all-to-all map and an IBM fake backend. Harrigan et al. showed non-native problems degrading on planar hardware because of routing ([arXiv:2004.04197](https://arxiv.org/abs/2004.04197)).

**Datasets, baselines and metrics.**

| Area | Sources |
|---|---|
| Optimization-native libraries | QOBLIB's ten "intractable decathlon" classes ([arXiv:2504.03832](https://arxiv.org/html/2504.03832v2)), mostly far above 29 variables, and its GitLab rate-limits; QPLIB; MQLib; Gset |
| Logistics and scheduling | TSPLIB, CVRPLIB, OR-Library job-shop ft06/la01–40, Taillard |
| Energy | MATPOWER cases with generator costs ([matpower.org](https://matpower.org/)) |
| Bundled in scikit-learn | Wine, Breast Cancer and Digits |

The baseline stack follows. **Exact solutions**: brute force to 2²⁰ in browser NumPy and 2²⁵ offline, feasible-set enumeration such as C(16,5) = 4,368, and `scipy.optimize.milp` (HiGHS), which is not yet verified in Pyodide. **Heuristics**: greedy, SA at both equal and 100× evaluations, tabu and parallel tempering. For MaxCut, add Goemans–Williamson offline or a NumPy Burer–Monteiro, since Pyodide's cvxpy-base ships without solvers. Finally, a **classical-null loop** replaces the quantum sampler with uniform, product-state and SA samplers.

Report these metrics:

- P(opt) and P(within 1% / 5%);
- feasibility rate;
- approximation ratio for best-of-N and for the mean, normalized to the achievable range;
- TTS99 in **shots**, not seconds;
- a CVaR quantile curve.

A **2026 review of 67 coded quantum-optimization studies** found that 25 of 57 included no classical baseline. Only 10 of 24 isolated the quantum contribution where an ablation applied, and the median experiment used 17 qubits ([Lau, arXiv:2610.11759](https://arxiv.org/abs/2610.11759)). Simply doing the ablation puts a hackathon entry above the literature's median.

### Chemistry and physics: SQD fits one job, but at small scale its classical half finds the answer anyway

**Pipeline and IonQ-native costs.** The electronic-structure pipeline runs: geometry → Hartree–Fock → active space → second-quantized Hamiltonian → qubit mapping → state preparation → measurement → mitigation → classical post-processing ([McArdle et al., arXiv:1808.10402](https://arxiv.org/abs/1808.10402)). The research team transpiled the fermionic building blocks to an `rzz` basis standing in for Forte's ZZ(θ) ([gatecount.py](<../research_notes/Quantum Impact theme deep dive/scripts/chemistry/gatecount.py>)):

| Building block | Native ZZ |
|---|---|
| Givens rotation (XX+YY) | 2 |
| Density–density (Jastrow) phase | 1 |
| Heisenberg bond | 3 |
| Jordan–Wigner hop across a 2-qubit Z string | 9 |

UCCSD needs thousands of entanglers even for small systems ([Zhao et al., arXiv:2212.02482](https://arxiv.org/abs/2212.02482)). The circuit family that fits is LUCJ/UCJ, orbital rotations alternating with Jastrow layers and parameterized from classical CCSD ([Motta et al., Chem. Sci. 2023](https://pubs.rsc.org/en/Content/ArticleLanding/2023/SC/D3SC02516K)). On IonQ every Jastrow pair is one native ZZ, while heavy-hex "local" UCJ must drop most opposite-spin pairs ([Robledo-Moreno et al., arXiv:2405.05068](https://arxiv.org/html/2405.05068v3)).

Measured one-layer UCJ costs for N₂/cc-pVDZ, from [small_counts.py](<../research_notes/Quantum Impact theme deep dive/scripts/chemistry/small_counts.py>). F is a white-noise estimate including per-qubit readout error.

| Active space | Qubits | All-to-all UCJ (native ZZ) | Heavy-hex-pattern LUCJ (native ZZ) | F (all-to-all / LUCJ) |
|---|---|---|---|---|
| (4e,4o) | 8 | 60 | 39 | 0.71 / 0.79 |
| (6e,5o) | 10 | 76 | 54 | 0.65 / 0.73 |
| (10e,6o) | 12 | 58 | 53 | 0.70 / 0.72 |
| (10e,8o) | 16 | 206 | 149 | 0.33 / 0.44 |
| (10e,10o) | 20 | 314–348 | 242–258 | 0.16–0.19 / 0.25–0.27 |
| (10e,12o) | 24 | 484 | 378 | 0.08 / 0.13 |

**VQE's measurement bill is the structural problem.** Jordan–Wigner Hamiltonians for these spaces have 61–4,201 Pauli terms. That is **17–878 qubit-wise-commuting measurement circuits per energy evaluation** at 8–24 qubits ([grouping_and_fcidump.py](<../research_notes/Quantum Impact theme deep dive/scripts/chemistry/grouping_and_fcidump.py>)). Qollab's own chemistry lesson shows chemical accuracy (1.6 mHa) costing about 24,000 shots per basis even for H₂, or 2.4M shots over a 50-step optimization ([Qollab Learn: Quantum Chemistry](https://qollab.xyz/learn/quantum-chemistry)).

Sample-based diagonalization (QSCI/SQD/SKQD) needs only **one circuit, measured in the Z basis**. It samples configurations from an approximate state and diagonalizes classically in the sampled subspace, with built-in particle-number post-selection ([Kanno et al., arXiv:2302.11320](https://arxiv.org/abs/2302.11320); [Robledo-Moreno et al., arXiv:2405.05068](https://arxiv.org/html/2405.05068v3)). IBM's SQD ran 58–77 qubits with 1–3.5k two-qubit gates, backed by Fugaku. N₂ landed within tens of mHa of HCI, while [4Fe-4S] was worse than classical methods. IBM's "configuration recovery" tolerated about 2% signal in N₂ numerics. SKQD reached 85 qubits on an Anderson impurity model ([arXiv:2501.09702](https://arxiv.org/abs/2501.09702)). The method has two independent critiques. Reinholdt et al. find QSCI keeps resampling configurations it already has ([arXiv:2501.07231](https://arxiv.org/abs/2501.07231)). Gaberle & Jattana show the configurations needed grow exponentially with system size, even under optimal ordering ([arXiv:2605.02494](https://arxiv.org/abs/2605.02494)). On trapped ions, BlueQubit ran SQD on Quantinuum H2 and saw slow convergence, with noise oddly helping ([arXiv:2512.04962](https://arxiv.org/abs/2512.04962)). **No IonQ SQD paper exists.**

**What the team's SQD runs show.** These are N₂/cc-pVDZ runs with qiskit-addon-sqd 0.14, ffsim and PySCF in WSL, using a white-noise proxy for Forte ([sqd_noise_study.py](<../research_notes/Quantum Impact theme deep dive/scripts/chemistry/sqd_noise_study.py>); [sqd_capped_study.py](<../research_notes/Quantum Impact theme deep dive/scripts/chemistry/sqd_capped_study.py>)). The headline pitfall is this: **at 16–20 qubits, uncapped SQD returns the exact FCI energy even from pure-noise samples.** The α×β product space plus configuration recovery fills 98–100% of the 63,504-determinant FCI space. Meanwhile, ideal UCJ samples, being concentrated, give subspaces of only 16–64 determinants and 27–31 mHa error. The quantum contribution becomes visible only when the subspace is **capped** and compared with classical selection at the same budget. All errors below are in mHa.

| Equilibrium R=1.1 Å, (10e,10o) | 20 strings per spin | 40 | 80 |
|---|---|---|---|
| Ideal UCJ samples | 27.7 (only 7 distinct strings) | — | — |
| Noisy UCJ (F=0.16) | 30.1 | 30.0 | 22.4 |
| Classical excitation-level heuristic | 18.6 | 5.2 | **3.1** |
| Oracle (strings ranked by exact FCI weight) | 8.2 | 1.7 | 0.26 |
| Uniform random | 65–852 | | |

| Stretched R=2.0 Å, (10e,10o) | 20 strings (dim 400) | 40 strings | 80 strings (dim 6,400) |
|---|---|---|---|
| Ideal all-to-all UCJ | **19.8** | 17.7 (saturates at 23 strings) | — |
| Noisy all-to-all UCJ (F=0.19) | 35.8 | 34.8 | 31.8 |
| Ideal heavy-hex-pattern LUCJ | 72.5 | — | — |
| Classical heuristic | 133.5 | 46.4 | **21.4** |
| Oracle | 34.7 | 9.2 | 2.3 |

Quantum samples beat the simple heuristic only at the strongly correlated geometry and small budgets. They lose at 6,400 determinants and lose outright at equilibrium. At 24 qubits, ideal UCJ gave 38 mHa from 16 distinct strings, against 11.5 mHa for the heuristic. A stronger baseline, such as CISD-amplitude ranking or heat-bath CI, would likely widen the classical win. Two findings are publishable-grade for a hackathon: the crossover budget, and **all-to-all UCJ beating heavy-hex LUCJ (19.8 against 72.5 mHa)**. This is also where a quantum step is meaningful at all. At 2.0 Å, CCSD and CCSD(T) fail non-variationally, landing 35.6 and 77.3 mHa *below* FCI. At equilibrium, CCSD(T) is within 0.70–0.81 mHa. That is under the 1.6 mHa chemical-accuracy line, so the gold standard needs no help there.

**Can the browser do the chemistry? Mostly, but precompute.** The team's tests conflict with Qollab's showcase.

- In **stock** Pyodide 314.0.7, `micropip.install('pyscf')` fails. PyPI pyscf 2.14 ships no Emscripten or Windows wheel, so offline work on Windows needs WSL, macOS, Linux or Colab ([PyPI pyscf](https://pypi.org/pypi/pyscf/json)).
- Qollab's official "Nature: H₂ ground state" showcase calls `PySCFDriver` live. It says its first run downloads **a WebAssembly build of PySCF** in a minute or two ([showcase-h2-ground-state](https://qollab.xyz/u/qollab/showcase-h2-ground-state)).

So Qollab evidently ships its own build, though which basis sets and molecule sizes it handles is unknown. A three-line `from pyscf import gto, scf` test inside Qollab settles it on night one. Other packaging facts:

- qiskit-addon-sqd is a pure wheel, but its solver path imports jax and pyscf. Its `configuration_recovery.py`, `subsampling.py` and `counts.py` need only NumPy and Qiskit, so they can be vendored under Apache-2.0 ([PyPI qiskit-addon-sqd](https://pypi.org/pypi/qiskit-addon-sqd/json)).
- qiskit-nature 0.8.0 (June 1, 2026) parses FCIDUMP files without PySCF ([PyPI qiskit-nature](https://pypi.org/pypi/qiskit-nature/json)).
- The team's ~60-line NumPy Knowles–Handy FCI ([kh_fci.py](<../research_notes/Quantum Impact theme deep dive/scripts/chemistry/kh_fci.py>)), validated against exact diagonalization, runs **(8e,8o) in 4.0 s and (10e,10o) in 189 s** in Pyodide.
- Sparse Hubbard exact diagonalization takes about 2 s at 20 qubits and about 30 s at 24.
- FCIDUMP files are small: 5.4 KB at 8 orbitals, 240 KB at 20 and 633 KB at 26 (N₂, D2h).

PubChem, RCSB PDB, PDBe, NCI CACTUS and GitHub raw are CORS-fetchable for geometries. NIST CCCBDB, the Materials Project, OQMD and COD are not.

**What chemistry advantage would actually require.** Lee et al. find no evidence of generic exponential advantage for ground-state energies, only possible polynomial speedups ([arXiv:2208.02199](https://arxiv.org/abs/2208.02199)). Fault-tolerant estimates for FeMoco-class catalysis have fallen from about 10¹⁴–10¹⁵ T gates in 2017 ([Reiher et al., arXiv:1605.03590](https://arxiv.org/abs/1605.03590)). Double factorization brought them to about 10¹⁰ Toffolis on about 3,600–4,000 logical qubits, roughly a day at 10 µs per Toffoli ([von Burg et al., arXiv:2007.14460](https://arxiv.org/abs/2007.14460)). Tensor hypercontraction brought them to about 2,100–2,200 logical qubits and 5–7×10⁹ Toffolis; secondary sources disagree on the exact figures ([Lee et al., arXiv:2011.03494](https://arxiv.org/abs/2011.03494)). Cytochrome P450 needs about 4.6M physical qubits for 73 hours at 0.1% error ([Goings et al., arXiv:2202.01244](https://arxiv.org/abs/2202.01244)).

**IonQ's own chemistry hardware record is small:**

| Year | Work | Result |
|---|---|---|
| 2019 | Water VQE with 3 parameters | 27–35 mHa off FCI ([arXiv:1902.10171](https://ar5iv.labs.arxiv.org/html/1902.10171)) |
| 2022 | 12-qubit pair-correlated VQE on Li₂O | Aria had 38% less error than Harmony ([arXiv:2212.02482](https://arxiv.org/abs/2212.02482)) |
| 2025 | 24-qubit QC-AFQMC (AstraZeneca) | See the portfolio table above |

**Physics targets that suit all-to-all hardware.** In a 1D Fermi–Hubbard chain the on-site term couples qubit i to qubit i+L, one native ZZ on Forte. A Trotter step costs 5L−4 ZZ, so 36 at L=8 (16 qubits). A Heisenberg chain costs 3(N−1), and a gauge-eliminated Schwinger model about 2(N−1) + N(N−1)/2, roughly 63 at N=10. These counts are research-team estimates from the measured blocks, not transpiled. Exact baselines run in the browser in under a second at these sizes. These are scientifically clean but carry a weaker "industry" story.

### Quantum machine learning: on classical data, parity is the honest ceiling

**Methods and their classical shadows.**

- **Fidelity kernels** k(x,x′)=|⟨φ(x)|φ(x′)⟩|² ([Havlíček et al., arXiv:1804.11326](https://arxiv.org/abs/1804.11326)) **concentrate exponentially** with qubit count. Expressivity, global measurement, entanglement and noise each cause it, and with polynomial shots the trained model stops depending on the data ([Thanasilp et al., arXiv:2208.11060](https://arxiv.org/abs/2208.11060v2)). Bandwidth scaling restores generalization ([Shaydulin & Wild, arXiv:2111.05451](https://arxiv.org/abs/2111.05451); [Canatar et al., arXiv:2206.06686](https://arxiv.org/abs/2206.06686)), but it also pulls the kernel toward classically easy regimes.
- **Projected quantum kernels (PQK)** compare one-qubit reduced density matrices. Huang et al.'s **geometric difference g_CQ** and **model complexity s_K = yᵀK⁻¹y** give a test: if g_CQ is small compared with √N, a classical model is competitive ([Huang et al., arXiv:2011.01938](https://arxiv.org/abs/2011.01938)).
- **Variational and re-uploading classifiers** are truncated Fourier series ([Schuld et al., arXiv:2008.08605](https://arxiv.org/abs/2008.08605)), so random Fourier features often match them ([Landman et al., arXiv:2210.13200](https://arxiv.org/abs/2210.13200)).
- **QCNNs** on standard benchmarks are effectively classically simulable, reproduced classically up to 1,024 qubits ([Bermejo et al., PRX Quantum 2026, arXiv:2408.12739](https://arxiv.org/abs/2408.12739)).
- Provable absence of barren plateaus often implies classical simulability ([Cerezo et al., arXiv:2312.09121](https://arxiv.org/abs/2312.09121v3)).
- QNNs memorize random labels, so uniform generalization bounds explain little ([Gil-Fuster et al., arXiv:2306.13461](https://arxiv.org/abs/2306.13461v2)).

**The independent evidence on classical data is consistent.**

- **Bowles, Ahmed and Schuld** tested 12 models on 160 datasets with full grid search. Out-of-the-box classical models ranked first in every family, removing entanglement often did not hurt, and quantum models did especially badly on linearly separable data. Of 55 surveyed papers, about 40% claimed a quantum win and almost none reported a loss ([arXiv:2403.07059](https://arxiv.org/abs/2403.07059)).
- **Kakavand et al. (April 2026)** ran 970 nested-cross-validated experiments and found **0 of 29** quantum-versus-classical comparisons significant. **Dataset choice explained 73% of the variance, and kernel type 9%** ([arXiv:2604.18837](https://arxiv.org/abs/2604.18837)).

Credible positive results all lie outside a hackathon's reach:

- learning from quantum experiments with quantum memory (40 qubits, [Huang et al., arXiv:2112.00778](https://arxiv.org/abs/2112.00778));
- cryptographically structured data ([Liu et al., arXiv:2010.02174](https://arxiv.org/abs/2010.02174));
- the April 2026 "quantum oracle sketching" separation for massive classical data, which needs fewer than 60 **logical** qubits ([Zhao et al., arXiv:2604.07639](https://arxiv.org/abs/2604.07639)).

Industry QML claims share recognizable traps:

- **Unmatched baselines.** IonQ's 3.14 points are measured against an SVC.
- **Tiny test sets.** At 250 samples, a 95% interval is about ±3.5 points.
- **Effects that exist only with noise.** HSBC and IBM's "up to 34%" bond fill-probability gain appeared with hardware noise and vanished in noiseless simulation. Scott Aaronson called it a "qombie" ([arXiv:2509.17715](https://arxiv.org/abs/2509.17715); [Shtetl-Optimized](https://scottaaronson.blog/?p=9170)).

If noise ever appears to help, add a classical noise-injection control. Sector studies in particle physics, Earth observation and intrusion detection mostly report parity with RBF-SVMs or boosted trees ([EuroSAT sweep, arXiv:2506.20355](https://arxiv.org/html/2506.20355v2)). Where an advantage appears, it is confined to chosen settings: Amgen and IBM's EHR kernels beat RBF only in some feature/sample regimes, and the authors call the advantage incomplete ([Amgen/IBM, arXiv:2112.06211](https://arxiv.org/abs/2112.06211v2)).

**The team's own QML runs reproduce the literature in miniature.**

*Experiment A* ([qk_bc.py](<../research_notes/Quantum Impact theme deep dive/scripts/qk_bc.py>)) used scikit-learn's breast-cancer data, PCA to n qubits, an IQP/ZZ chain feature map with two repetitions, and nested CV for both quantum kernels and RBF. The other classical models were left untuned, which favours the quantum side. Outer 5-fold accuracy:

| Qubits | LogReg | RF | HistGB | MLP | RBF-SVM | Fidelity QK | Projected QK |
|---|---|---|---|---|---|---|---|
| 4 | 0.961 | 0.951 | 0.944 | 0.963 | 0.960 | 0.960 | 0.960 |
| 8 | **0.981** | 0.953 | 0.963 | 0.970 | 0.961 | 0.970 | 0.968 |
| 12 | 0.970 | 0.951 | 0.968 | 0.972 | 0.967 | 0.972 | **0.977** |

One error is about 0.9 points per fold, so every difference of 2 points or less is noise. The diagnostics explain the parity:

- **g_CQ.** At cross-validation-selected bandwidths, g_CQ ≈ 2–4, far below √N ≈ 24. Large g (10–28) appears only at bandwidth 1, where the fidelity kernel is nearly diagonal and generalizes worse.
- **Concentration.** The fidelity kernel's off-diagonal variance fell about 380× from 2 to 12 qubits, against about 10× for the PQK.
- **Bandwidth versus noise.** A fixed bandwidth cost about 9 points (0.88 against 0.97), dwarfing shot and noise effects at 0.5–1% error.

*Experiment B* ([qrc_mg.py](<../research_notes/Quantum Impact theme deep dive/scripts/qrc_mg.py>), [qrc_tune.py](<../research_notes/Quantum Impact theme deep dive/scripts/qrc_tune.py>), [qrc_shots.py](<../research_notes/Quantum Impact theme deep dive/scripts/qrc_shots.py>)) is an 8-qubit restart-protocol reservoir on Mackey–Glass: 48 native ZZ per circuit, 36 ⟨Z⟩/⟨ZZ⟩ features plus the input window. QRC settings were picked on test error, which flatters QRC, and the ESN was untuned. Test NMSE:

| Model | 1-step | 5-step |
|---|---|---|
| Quadratic NVAR (28 features) | 3.2e-3 | 2.5e-2 |
| ESN, 36 nodes | 1.2e-3 | 2.4e-3 |
| **ESN, 300 nodes** | **2.0e-6** | **8.7e-6** |
| QRC, exact expectations | 4.6e-4 | 7.6e-4 |
| QRC, 10⁵ shots per circuit | 2.6e-3 | 4.9e-3 |
| QRC, 10³ shots | 8.3e-3 | 4.4e-2 |
| QRC, 10³ shots + 0.5% depolarizing | 9.4e-3 | 6.6e-2 |

The quantum reservoir beats an equal-size ESN **only with exact expectation values**. With realistic shots it loses to both small classical baselines, and a 300-node ESN wins by more than two orders of magnitude. That is a clean, quantified, judge-proof finding, but a negative headline.

**Job sizing on IonQ.** A fidelity kernel needs N_test × N_SV circuits. A PQK needs only 3N (one per measurement basis), with no pairwise circuits. 100 test points come to 300 circuits and about 18k gates, which fits one multi-circuit job (≤5,000 circuits, ≤150,000 gates, ≤10 MB per IonQ's API, [IonQ API v0.4](https://docs.ionq.com/api-reference/v0.4/jobs/create-job)). A 50 × 100 fidelity kernel at about 500k gates does not fit.

**Datasets and in-browser baselines.** Pyodide includes scikit-learn 1.8, xgboost 2.1.4, lightgbm 4.6 and statsmodels, but **no PyTorch or TensorFlow** ([Pyodide packages](https://pyodide.org/en/stable/usage/packages-in-pyodide.html)). Strong tree baselines therefore run live, while any embedding model must run offline. Good data:

- bundled breast cancer (569 × 30) and Wine (178 × 13);
- a stratified fraud subsample of the ULB credit-card data (492 frauds, PCA features), about 0.6 MB shipped ([OpenML 1597](https://api.openml.org/d/1597));
- BreastMNIST (780 images, about 0.6 MB);
- a year of hourly regional load, under 1 MB.

EuroSAT, CICIDS2017 and the LHC Olympics data are gigabyte-scale and need offline featurization. QCNN, QNLP (lambeq) and quantum transformers are poor 48-hour choices. QCNN is simulable, lambeq is not in Qollab's library list, and LCU/QSVT circuits exceed the gate budget.

### Finance: amplitude estimation fits only with a lookup-table oracle, and noise erases the gain

**The primitives and their fault-tolerant price.** QAE gives a quadratic speedup over Monte Carlo for option pricing and risk ([Stamatopoulos et al., arXiv:1905.02666](https://arxiv.org/abs/1905.02666); [Woerner & Egger, arXiv:1806.06893](https://arxiv.org/abs/1806.06893); [Egger et al., credit risk, arXiv:1907.03044](https://www.arxiv.org/pdf/1907.03044)). The thresholds for real advantage are steep:

- Goldman Sachs, IBM and UMD put derivative pricing at **about 8k logical qubits and T-depth 54M, run in about one second** ([Chakrabarti et al., Quantum 5, 463](https://quantum-journal.org/papers/q-2021-06-01-463/)).
- QSP-based payoff loading cut that to **4.7k logical qubits and 10⁹ T gates at a 45 MHz logical rate** ([Stamatopoulos & Zeng, arXiv:2307.14310](https://arxiv.org/abs/2307.14310v2)).
- Quantum gradients cut the needed clock from about 50 to about 7 MHz ([arXiv:2111.12509](https://arxiv.org/abs/2111.12509v1)).

The bottleneck is logical clock speed, not qubit count. Herbert proved there is **no quantum speedup** for moments of analytically defined log-concave distributions loaded by Grover–Rudolph ([arXiv:2101.02240](https://arxiv.org/abs/2101.02240)). Data-learned loaders (qGANs, QCBMs) are the standard workaround ([Zoufal et al., arXiv:1904.00043](https://arxiv.org/abs/1904.00043)).

**Under one job per run, use MLAE, not IQAE.** Maximum-likelihood AE runs Q^m·A on a fixed schedule of m, with no phase estimation and no controlled-Q, so every circuit is known in advance ([Suzuki et al., arXiv:1904.10246](https://arxiv.org/abs/1904.10246)). A noise-aware variant adds depolarizing decay to the likelihood ([Tanaka et al., arXiv:2006.16223](https://arxiv.org/abs/2006.16223)). IQAE chooses its next circuit adaptively, which forces several jobs ([Grinko et al., arXiv:1912.05559](https://arxiv.org/abs/1912.05559)). The one IonQ-hardware finance-flavoured experiment, with Goldman Sachs and QC Ware, reached about 10⁻² mean additive error with low-depth MLE-AE at more than 90 two-qubit gates ([arXiv:2109.09685](https://arxiv.org/pdf/2109.09685)).

**The team's gate counts settle feasibility** ([qae_counts.py](<../research_notes/Quantum Impact theme deep dive/scripts/qae_counts.py>); [qae_lut.py](<../research_notes/Quantum Impact theme deep dive/scripts/qae_lut.py>); CX counts after all-to-all transpilation):

| Oracle | Uncertainty qubits | A | One Grover step Q | Q¹A | Q²A | Q⁴A |
|---|---|---|---|---|---|---|
| qiskit-finance `EuropeanCallPricing` | 2 | 45 | 128 | 173 | 301 | 557 |
| same | 3 | 92 | 310 | 400 | 708 | 1,324 |
| Hand-built lookup table (StatePreparation + UCRY) | 2 | 5 | 15 | 18 | 31 | **57** |
| same | 3 | 12 | 38 | 48 | 84 | 156 |

Two consequences follow:

- qiskit-finance's stock circuits allow only m=0 within 100 gates. Its credit-risk model fits at 61 CX only for two obligors.
- The lookup-table oracle tabulates the payoff classically, so it demonstrates the **estimator**, not an end-to-end speedup. State that caveat on the page.

MLAE on the n=2 lookup table (true a=0.1967, m∈{0,1,2}, 1,000 shots per circuit, 20 repetitions, generic depolarizing noise):

| Two-qubit error | Naive MLAE RMSE | Noise-aware MLAE RMSE |
|---|---|---|
| 0 | 0.0022 | 0.0026 |
| 0.5% | 0.0063 | 0.0034 |
| 1% | 0.0115 | 0.0030 |
| 2% | 0.0167 | 0.0044 |

Classical Monte Carlo with the same 9,000-sample budget has RMSE 0.0042. Noiseless MLAE beats it about 1.9×, matching the Fisher-information ratio. **Naive MLAE loses once error reaches 0.5%, and noise-aware MLAE only recovers MC-level accuracy.** RMSEs carry about ±15–20% uncertainty.

**Portfolio optimization is crowded and has been run far bigger.** IonQ and Kipu decomposed a K=125-of-250 S&P 500 Markowitz problem onto Forte and a 64-qubit barium system, with no numeric gaps in the blog ([IonQ blog](https://www.ionq.com/blog/quantum-computing-meets-wall-street-running-real-portfolio-optimization-on-trapped-ion-hardware)). JPMorgan, AWS and Quantinuum ran a 78-qubit, 225-asset independent-set diversification on Helios without claiming advantage ([TQI](https://thequantuminsider.com/2026/07/06/hybrid-quantum-algorithm-improves-portfolio-optimization-on-trapped-ion-quantum-computer/)). Goldman's analysis of quantum interior-point portfolio methods concluded that fundamental improvements are needed ([Dalzell et al., arXiv:2211.12489](https://arxiv.org/pdf/2211.12489)). Qollab already hosts the Systemic Oracle and three portfolio showcases, and Finbubu won CQhack25 with QAOA portfolios. The open finance lanes are **generative copulas** and **estimation with honest noise accounting**.

**Market data is the main CORS problem.** Yahoo, Stooq, FRED, Nasdaq and SEC EDGAR send no CORS header. Crypto venues (Coinbase, Kraken, Binance.vision, CoinGecko), ECB, Frankfurter and Treasury FiscalData do. Alpha Vantage works only with a key ([cors_check.sh](<../research_notes/Quantum Impact theme deep dive/scripts/cors_check.sh>)). Ship a frozen equity CSV. qiskit-finance's Yahoo, Wikipedia and Nasdaq data providers depend on blocked or discontinued services; this is an inference from the tests.

### Sector by sector: the same small-core pattern, with data you can actually fetch

Across sectors, the credible 48-hour shape is the one IonQ itself publishes: a 10–24-qubit combinatorial or estimation core carved from real public data, with classical decomposition and repair doing the heavy lifting. Fault-tolerant-only problems (FeMoco, CFD, cryptanalysis) belong in a resource-estimate panel, not in the build.

**Energy.** IonQ/ORNL unit commitment is the anchor (portfolio table). Koretsky et al. found classical solvers effective below about **400 units** ([arXiv:2110.12624](https://arxiv.org/abs/2110.12624)). Other grid results so far are QAOA islanding on IBM hardware up to the IEEE 30-bus case ([arXiv:2606.15083](https://arxiv.org/pdf/2606.15083)) and deep QAOA unit commitment in simulation only. MATPOWER and pglib-opf cases, EIA hourly demand (with DEMO_KEY), Open-Meteo, NASA POWER and UK Carbon Intensity are all CORS-enabled.

**Healthcare.** Precedents:

- IonQ/Kipu protein folding;
- radiotherapy beam-angle selection against clinical plans rather than a strong MILP ([arXiv:2504.07844](https://arxiv.org/pdf/2504.07844));
- a 117-qubit hepatitis-D genome load, a data-loading milestone rather than an analysis ([Sanger](https://www.sanger.ac.uk/news_item/genome-loaded-onto-a-quantum-computer-in-world-first/));
- Q4Bio's outcome.

IonQ named predictive medicine and pharmaceuticals as priorities. ClinicalTrials.gov v2, openFDA, UniProt, PubChem, NCBI and cBioPortal are CORS-enabled; PhysioNet is not.

**Climate.** Deloitte's carbon-capture winners used VQE corrections on classical bulk methods ([TQI](https://thequantuminsider.com/2023/05/08/quantum-climate-challenge-team-ecoqult-wins-the-deloittes-quantum-climate-challenge/)). Quantum CFD for weather needs 10²¹–10³⁹ logical-qubit×T resources, with no exponential advantage for nonlinear PDEs ([Penuel et al., arXiv:2406.06323](https://arxiv.org/pdf/2406.06323)).

**Telecom.** The wins are vendor claims on annealers or Ising machines: DOCOMO cut peak paging by 15% ([TQI](https://thequantuminsider.com/2024/08/23/ntt-docomo-and-d-wave-improve-mobile-network-performance-by-15-with-quantum-optimization-technology/)), and SoftBank's carrier-aggregation proof of concept reported about +10% downlink ([SoftBank](https://www.softbank.jp/en/corp/news/press/sbkk/2025/20250729_01/)).

**Cybersecurity.** The resource trajectory is the story:

- RSA-2048 under 1M noisy qubits in under a week ([Gidney, arXiv:2505.15917](https://arxiv.org/abs/2505.15917v1));
- ECDLP-256 under 500k physical qubits in about 9 minutes ([TQI](https://thequantuminsider.com/2026/03/31/q-day-just-got-closer-three-papers-in-three-months-are-rewriting-the-quantum-threat-timeline/));
- a 28–49% expert probability of a cryptographically relevant machine within 10 years ([GRI 2025](https://globalriskinstitute.org/publication/quantum-threat-timeline-report-2025b/));
- NIST IR 8547's draft deprecating RSA-2048 after 2030 and disallowing it after 2035.

**Aerospace and automotive.** Airbus loading and DESY gates (IonQ), plus Volkswagen's paint-shop QAOA on a trapped-ion QPU ([arXiv:2011.03403](https://arxiv.org/pdf/2011.03403)). OpenSky's API is **not** CORS-usable from Qollab.

**Agriculture.** No peer-reviewed quantum crop-rotation paper exists. FeMoco nitrogen fixation is the fault-tolerant story, about 2,200 logical qubits ([Lee et al., arXiv:2011.03494](https://arxiv.org/pdf/2011.03494)).

**Public sector.** CERN's Open Quantum Institute lists 18 SDG use cases in development ([TQI](https://thequantuminsider.com/2024/10/11/open-quantum-institute-details-quantum-computing-solutions-for-global-challenges-from-food-security-to-climate/)), and no hardware results exist for disaster logistics. USGS, OpenFEMA and HDX are CORS-enabled.

| Sector | Most credible 48 h core | Public data (CORS status) | Strong baseline | Measurable step |
|---|---|---|---|---|
| Energy | Unit commitment, 10–12 units (QAOA proposes, LP dispatch prices) | MATPOWER/pglib-opf on GitHub ✔; EIA v2 ✔ (key in URL) | Exact enumeration + LP; MILP; priority list | Cost distribution per sample against a classical null; feasibility; gap |
| Finance | MLAE tail-probability (VaR) estimator, or QCBM copula | Crypto OHLC ✔; equities shipped | MC at equal oracle calls; t-copula | RMSE against calls; noise knee; held-out MMD and tail error |
| Healthcare | Clinical-trial site selection, k of 12–20 (XY mixer), or mRMR feature selection | ClinicalTrials.gov ✔; sklearn bundled | Exact C(n,k); greedy; MILP | Approximation ratio and P(opt); downstream CV |
| Climate | Renewable-site portfolio on weather-driven covariance | Open-Meteo, NASA POWER ✔ | Exact enumeration; mean-variance QP | Gap; variance reduction |
| Telecom | Channel assignment on a cell-site interference graph | OSM extracts (pre-extract offline) | DSatur; ILP | Conflicts against optimum |
| Cybersecurity | Mosca-inequality risk estimator with the same MLAE engine | GRI survey numbers (ship); NVD ✔ | MC; analytic convolution | RMSE against calls |
| Aerospace | Cargo loading or gate assignment encoding study | Airbus 2019 parameters; flights shipped | MILP; greedy | P(opt) and gate count by encoding |
| Agriculture | Crop allocation, 4 plots × 4 crops | NASA POWER ✔; yields shipped | ILP; greedy | Gap; violation rate |
| Public sector | Post-earthquake shelter siting, 12–20 sites | USGS, OpenFEMA, HDX ✔ | Greedy (1−1/e); MILP | Coverage gap; P(opt) |

Sources: [finance_and_sector_use_cases.md B9](<../research_notes/Quantum Impact theme deep dive/finance_and_sector_use_cases.md>), compiled from the sector sources above.

**Space** is named in the brief and maps to IonQ's Capella SAR work and its stated 2026 focus on satellite image analysis. It is still the riskiest 48-hour bet: loading imagery into a few qubits is the bottleneck that Qollab's own "What to build" lesson warns against.

## Honest benchmarking: pre-register, beat the hybrid null, then estimate the scale-up

### Seven frameworks converge on four rules

**Lanes et al. (IBM with Pasqal)** define advantage as a rigorously validated output plus superior efficiency, cost or accuracy against classical computation alone. They treat claims as falsifiable hypotheses, compare hybrid quantum-plus-classical against classical alone, and want benchmarks defined jointly with classical experts ([arXiv:2506.20658](https://arxiv.org/abs/2506.20658)). The **Open Quantum Advantage Tracker** has three pathways: observables with rigorous error bars, variational energies as upper bounds, and classically verifiable answers. Entries are labelled active, superseded or baseline. On October 9 its variational pathway had **no active candidates**, and three classically verifiable entries had been superseded by classical progress ([Tracker](https://quantum-advantage-tracker.github.io/); [IBM blog](https://www.ibm.com/quantum/blog/quantum-advantage-tracker)). Three more frameworks add criteria:

- **Huang, Choi, McClean and Preskill** name five keystone properties: predictability, typicality, robustness, verifiability and usefulness ([arXiv:2508.05720](https://arxiv.org/abs/2508.05720)).
- **Babbush et al.** add average-case hardness, likely super-quadratic speedup, and robustness against a moving classical target. They lay out five application stages: algorithm discovery, hard instances, real-world connection, resource estimation and deployment. Only cryptanalysis and quantum simulation have convincingly reached Stage III ([arXiv:2511.09124](https://arxiv.org/abs/2511.09124)).
- **Abbas et al.** ask optimization studies for total time (pre-processing, transpilation, execution, post-processing), feasibility first, and approximation ratios normalized to the achievable range ([arXiv:2312.02279](https://arxiv.org/abs/2312.02279)).

**QOBLIB** requires best feasible objective, repetitions, successes and split wall-clock, mapping solutions back to the original problem because penalized QUBO energies are not comparable ([arXiv:2504.03832](https://arxiv.org/abs/2504.03832)). **Tuziemski et al.**'s checklist for runtime claims demands direct timing including hyperparameter tuning, standardized time-to-ε, strong native classical baselines, no selective reporting, and a **"hybrid null hypothesis"**: replace the quantum subroutine with a classical one and see whether results hold ([arXiv:2510.06337](https://arxiv.org/html/2510.06337v3)). Their journal status is unverified. The classic warning still stands: whether a speedup exists can depend on exactly which question is posed ([Rønnow et al., arXiv:1401.2910](https://arxiv.org/abs/1401.2910)).

Read together, the seven converge on four rules. First, the output must be **validated**, with error bars, a variational bound or a classically checkable answer. Second, the comparison must be against the **strongest reasonable classical baseline**, tuned with equal effort, on the same task, inputs and scoring function. Third, time and cost accounting must be **end to end**, including every overhead and repetition. Fourth, a **hybrid-null ablation** must show what changes when the quantum part is replaced by a classical one. None of the frameworks gives a formal standard for a hackathon-scale "measurable quantum step"; the checklist below is the research team's synthesis of them.

Distilled for a 48-hour demo, with every line checkable by a judge:

- **Pre-register.** Before running, commit to the README the task, metrics, pass thresholds, baselines, instance set and dataset source, shots, seeds and backends. Qollab's version history is the timestamp, and Qollab's own lesson demands exactly this.
- **Use three baseline tiers.** A trivial tier (random or greedy), a best-practice tier (exact solver, tuned heuristic or tuned ML), and the hybrid null. The quantum step is the difference from the hybrid null, with error bars, not the difference from random.
- **Report statistics.** Give a Wilson or bootstrap 95% interval on every shot-based number (`scipy.stats.bootstrap` is in Pyodide's SciPy 1.18, [SciPy docs](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.bootstrap.html)). Use ≥5 seeds per stochastic method, k-fold CV plus seeds for ML, and **paired differences** rather than two overlapping bars. Qollab's binomial note is a good template: two 1,000-shot draws land within about 40 counts 95% of the time near p=0.5 ([Qollab Learn lesson 5](https://qollab.xyz/learn/using-quantum-in-a-real-application/is-quantum-worth-it)).
- **Account for time honestly.** Report every method's wall-clock, label quantum timings as "browser simulator" or "IonQ cloud including queue", and never present simulated-quantum time as a speedup. Compare quality at equal budget (equal samples or cost evaluations) and state the cost separately.
- **Show scaling only over sizes actually run.** Draw any extrapolation dashed, with the fitted model and a sentence on what would falsify it, and never extrapolate a noiseless trend to hardware.

**Metrics by domain**

| Domain | Report |
|---|---|
| Optimization | Normalized approximation ratio; P(opt) per shot; TTS99 in shots; feasibility; original-objective values, never raw penalized energies |
| Chemistry | Error against exact in mHa against the 1.6 mHa line; variational bound; V-score where no exact answer exists ([arXiv:2302.04919](https://arxiv.org/abs/2302.04919)); shots per σ |
| QML | Nested-CV accuracy, AUC or balanced accuracy, mean ± SD over ≥5 seeds; matched tuning budget; non-entangling ablation; g_CQ and kernel spectrum |
| Generative | Held-out KL/MMD with a stated bandwidth; generalization metrics such as fidelity, rate and coverage of unseen valid samples ([Gili et al., arXiv:2207.13645](https://arxiv.org/abs/2207.13645v2)) |
| Hardware or noise-model sampling | TVD or Hellinger distance to ideal, with a multinomial bootstrap |

Reviewers detect over-claiming from a recognizable list:

- advantage language on simulator timings;
- random or untuned baselines;
- unequal tuning budgets;
- cherry-picked seeds;
- raw QUBO energies compared across penalty weights;
- downscaled data presented as real (4×4 MNIST overlaps its training set about 70% of the time, per Bowles);
- three-point extrapolations;
- omitted overheads;
- missing ablations.

Pre-empt each in a "Limitations and threats to validity" section.

### Resource estimation now runs inside the browser

Microsoft's open-source resource estimator loads from jsDelivr as npm `qsharp-lang@1.33.1` (MIT, published October 8). It accepts Q# or **OpenQASM 3** and returns logical and physical qubits, code distance, T/CCZ counts and runtime. The research team ran it in Chromium:

| Step | Time |
|---|---|
| Module import | 3.4 s |
| WebAssembly instantiation | 0.47 s |
| Two estimates | 0.81 s |
| One OpenQASM estimate | 0.29 s |

An 8-qubit toy came out at 107,730 physical qubits at code distance 9 on the `qubit_gate_ns_e3` surface-code preset ([jsDelivr qsharp-lang](https://cdn.jsdelivr.net/npm/qsharp-lang@1.33.1/package.json); [Microsoft Learn](https://learn.microsoft.com/en-us/azure/quantum/intro-to-resource-estimation)). It runs on the main thread, which matters because Qollab blocks workers. **It has not been tested inside Qollab's sandbox.** The CSP allows jsDelivr scripts, but precompute a JSON fallback.

Trapped ions have microsecond gates, so the `us_e3`/`us_e4` presets or custom parameters at IonQ's roughly 0.4–0.7% two-qubit error are the honest choice. The surface-code arithmetic is simple enough to show live ([Qualtran port of Beverland et al.](https://qualtran.readthedocs.io/en/latest/surface_code/beverland_et_al_model.html)):

- logical error per cycle P_L(d) = 0.03(p/0.01)^((d+1)/2);
- physical qubits per logical qubit = 2d²;
- logical cycle time = (4·t_2q + 2·t_meas)·d.

Useful anchors from Babbush et al.'s Stage IV examples:

| Problem | Logical qubits | Toffolis | Physical qubits | Runtime |
|---|---|---|---|---|
| RSA-2048 | ~1,400 | ~7×10⁹ | ~10⁶ | ~1 week |
| FeMoco (76 orbitals) | ~1,500 | ~10⁹ | ~5×10⁶ | ~9 hours |

The impact write-up that judges will trust runs bottom-up:

1. the stakeholder and the decision, with two or three sourced numbers on size and cost;
2. today's classical practice and its runtime;
3. the hybrid loop diagram, saying which step is quantum and why;
4. the pre-registered pass/fail table with intervals, backend and date;
5. the path to impact: Babbush stage placement, a Stage IV estimate, IonQ roadmap milestones labelled as vendor projections, and a falsifiable "advantage would require…" sentence;
6. limitations.

The IonQ roadmap milestones are: Tempo at 100 qubits (sold on-premises, not on public clouds), Superion 256 deliveries in 2027, a fault-tolerance demo in 2027, a commercial system in 2028, and 80k logical qubits by 2030 ([TQI](https://thequantuminsider.com/2026/09/08/ionq-uses-investor-day-to-detail-superion-roadmap-skywater-strategy-and-quantum-security-plans/); [arXiv:2604.04761](https://arxiv.org/html/2604.04761v1)). Keep top-down market numbers out of the impact claim. McKinsey's 2026 monitor projects US$1.3–2.7T by 2035, but a critic found its finance figure cannot be reproduced from the stated assumptions ([PostQuantum](https://postquantum.com/industry-news/mckinsey-quantum-monitor-2026/)). BCG admits its NISQ-era assumptions proved overly optimistic ([BCG](https://bcg.com/press/18july2024-quantum-computing-create-up-to-850-billion-of-economic-value-2040)).

## Qollab's runtime runs the Qiskit application stack if you precompute and send one job

The JS↔Python bridge, CSP, statevector timings, packages that fail (stim, pymatching, QuTiP) and accessibility checklist are in the Quantum Unlocked report's runtime section and `build_feasibility_and_stack.md`. The facts below are new for application work.

**The application libraries run.** Qollab's official showcases (August 1, 2026) run these live in the browser ([Qollab docs: Runtime environment](https://qollab.xyz/learn/docs/runtime-environment)):

| Library | Showcase |
|---|---|
| qiskit-optimization 0.7.0 | `MinimumEigenOptimizer` with QAOA (`StatevectorSampler`, COBYLA, 50 evaluations) and the exact eigensolver ([showcase-qaoa-qubo](https://qollab.xyz/u/qollab/showcase-qaoa-qubo)) |
| qiskit-algorithms 0.4.0 | VQE ([showcase-vqe-ground-state](https://qollab.xyz/u/qollab/showcase-vqe-ground-state)) |
| qiskit-nature 0.8.0 with WebAssembly PySCF | H₂ at four bond lengths |
| qiskit-finance 0.4.1 | Option-pricing circuit and portfolio QP ([showcase-option-pricing](https://qollab.xyz/u/qollab/showcase-option-pricing)) |
| qiskit-machine-learning 0.9.1 | XOR VQC and EstimatorQNN ([showcase-vqc-xor](https://qollab.xyz/u/qollab/showcase-vqc-xor)) |

The editor adds pinned lines to `requirements.txt`. Speed is documented only qualitatively: first-run installs take about a minute, PySCF a minute or two, and VQC training a few seconds. Inspection of the wheels turned up four pitfalls:

- qiskit-optimization 0.7.0 **vendors its own** QAOA, VQE and optimizers. It depends on docplex, which warns about 32-bit WASM, so build `QuadraticProgram` directly or via `from_ising`.
- Each of qiskit-algorithms, qiskit-optimization and qiskit-machine-learning has its **own** `algorithm_globals`, so seed all three.
- `P_BFGS` uses multiprocessing; avoid it, along with anything using `parallel_map`.
- `FidelityStatevectorKernel` builds an N×M kernel from N+M statevectors and is the only practical in-browser kernel. `FidelityQuantumKernel` runs N·M circuits and must never go to IonQ pair by pair ([PyPI qiskit-machine-learning 0.9.1](https://pypi.org/pypi/qiskit-machine-learning/0.9.1/json)).

Two things remain unverified and should be tested on night one: whether `scipy.optimize.milp` (HiGHS) is in Pyodide's SciPy, and whether cvxpy-base has any solver (it ships without bundled solvers).

**The hybrid architecture under one job per run** is what Qollab's own polished showcases do. The H₂ slider embeds precomputed Pauli tables and optimizes a tiny ansatz in JS. The kernel showcase builds a 60×60 kernel live in about 30 lines of JS and sends one 200-shot anchor circuit inside try/catch ([quantum-chemistry-showcase-t-2](https://qollab.xyz/u/qollab/quantum-chemistry-showcase-t-2); [quantum-kernel-showcase-drag-t](https://qollab.xyz/u/qollab/quantum-kernel-showcase-drag-t)). The architecture has three layers:

- **Offline.** Do hyperparameter search, parameter training, multi-seed statistics, full classical baselines, scaling sweeps and Forte noise-model runs. Save them as `data/*.json` files of ≤2 MB, read by literal path, with seeds, versions and dates recorded.
- **Live in the browser.** Reload parameters, re-evaluate the headline circuits exactly at ≤12 qubits, re-run cheap baselines (brute force to 2²⁰, scikit-learn), and optionally run a short warm-started optimizer. Do not run optimizer loops live at 16+ qubits.
- **Exactly one backend call.** The runtime docs say to pass every circuit to a single `backend.run([...])`, and IonQ accepts multi-circuit jobs of up to 5,000 circuits. The official Soundtrack instead packs circuits side by side on disjoint qubits of one circuit. Test the list form on night one and keep packing as the fallback.

Seed `StatevectorSampler`/`StatevectorEstimator`, `seed_simulator`, `seed_transpiler`, NumPy `default_rng` and IonQ's `sampler_seed`. IonQ's noise models (`forte-1`, `forte-enterprise-1`) run up to 29 qubits and simulate each shot separately. They **do not include debiasing**, may time out near the qubit ceiling, and the docs warn against using them to predict hardware success ([IonQ docs: noise models](https://docs.ionq.com/guides/simulation-with-noise-models)). Whether Qollab passes `noise_model` and `sampler_seed` through `backend.run` is unverified. On any failure, show the cached Forte-noise result labelled with date, model, shots and seed, next to the ideal result.

**Live data requires `Access-Control-Allow-Origin: *`** (or an echo of `null`). Qollab fetches GET-only with `Origin: null`, without credentials, and its docs say never to embed API keys ([Qollab docs: Runtime environment](https://qollab.xyz/learn/docs/runtime-environment); [Fetch Standard](https://fetch.spec.whatwg.org/#cors-check)). A real fetch from a null-origin sandboxed iframe gave these results:

| Result | Sources |
|---|---|
| **Succeeded** | raw.githubusercontent.com; GitHub API; jsDelivr `/gh/` and `/npm/`; Hugging Face dataset-viewer and `resolve`; Zenodo API; Socrata portals; World Bank v2; Open-Meteo; NWS; NOAA NCEI; NASA POWER; USGS; OSRM `/table` (road-distance matrices); PubChem; RCSB; UniProt; ChEMBL; OpenML via `www.` URLs; Our World in Data canonical CSVs; Wikipedia with `origin=*`; EIA v2 with a key |
| **Failed** | FRED; the UCI repository; the Materials Project; the main Overpass interpreter; data.gov's old CKAN API; QOBLIB's GitLab |

Three conflicts with the separate curl survey need flagging:

- **World Bank** sent no CORS header in one curl test but passed in the null-origin browser test.
- **Overpass** is called CORS-enabled in one note, but its interpreter returned 406 in the browser test.
- **OpenML** downloads fail through `api.openml.org`'s redirect but work via `www.openml.org`.

Redirects are a trap: one hop without CORS kills the fetch. Trust the browser test, and re-run `cors_check.sh` with `null` as its argument during the event. Its default Origin is `https://qollab.xyz`, which does not match Qollab's real `null` origin ([benchmarking_and_build_stack.md Q3](<../research_notes/Quantum Impact theme deep dive/benchmarking_and_build_stack.md>)).

The robust data pattern:

- Ship a frozen, cited snapshot (source URL or DOI, licence, retrieval date, SHA-256) as the default.
- Mirror it in your own MIT repo and read it through a pinned jsDelivr `/gh/user/repo@tag/` URL, which is immutable, CORS-open and cached.
- Make "refresh from source" an optional button that falls back silently.
- Subsample with a seeded, documented rule, show full-dataset statistics beside the subsample, and run the classical baseline on both.

**Visualization under Qollab's constraints:**

| Library | Licence and size | Status in Qollab |
|---|---|---|
| Plotly.js | MIT, about 4.8 MB | Usable; richest error bars, log axes and hover |
| Chart.js | MIT, about 208 KB | Usable, light |
| uPlot | MIT, about 145 KB | Usable, light |
| D3 | ISC, about 280 KB | Usable for Pareto and scaling plots |
| MapLibre GL | BSD-3 | **Will almost certainly fail**: it needs web workers, which Qollab blocks; Plotly's MapLibre-based maps fail for the same reason |
| Leaflet | BSD-2 | Technically works without workers, but the licence collides with the strict "outside repos must be MIT" reading; ask organizers |
| Plotly `scattergeo`, D3-geo | MIT / ISC | Safe for maps |

([npm registry](https://registry.npmjs.org/maplibre-gl/latest); [MapLibre docs](https://maplibre.org/maplibre-gl-js/docs/); [jsworker CSP](https://qollab.xyz/jsworker.html)). A dashboard layout that maps onto the rubric runs in seven panels:

1. a problem card with stakeholder, dataset citation and instance size;
2. a pre-registered thresholds card;
3. a results table with intervals and pass/fail badges;
4. a quality-against-size plot with the classical curve;
5. a "this run / cached Forte noise model / ideal" toggle;
6. an "estimate at scale" panel;
7. limitations.

## The ranked shortlist: grid commitment first, engineering partitioning second, copulas third

| Rank | Concept | Brief sector; Qollab coverage | IonQ precedent | Public data | Quantum core | Honest measurable step | 48 h risk |
|---|---|---|---|---|---|---|---|
| 1 | **Commit & Dispatch**: hybrid unit commitment | Energy (named); **zero** projects | ORNL GRID-Q on Forte (26 units × 24 h); EPB Chattanooga | MATPOWER/pglib-opf + EIA hourly load, both CORS ✔ | 10–12 qubits, 45–66 native ZZ per layer (F≈0.72–0.80) | Dispatch-priced cost distribution per sample against a classical null; feasibility; gap to exact | Low–medium |
| 2 | **Quantum Nested Dissection**: fill-reducing ordering | Manufacturing (named); **zero** | Ansys 12% and Synopsys 14.6% (Best Paper 2026); "computation engineering" focus | SuiteSparse FEA matrices (shipped) | 12–20-node balanced bisection | Factor fill/flops against RCM, spectral, KL and exact bisection; hybrid null | Medium–high |
| 3 | **Qopula Stress Lab**: QCBM copula tail risk | Finance (named); zero generative projects, but finance explored | GE copulas, Fidelity qopula; NQCC 2024 winner | Equity CSV (shipped) or crypto (CORS ✔) | 6–9 qubits, 45–72 ZZ, **one sampling circuit** | Held-out MMD/KL, tail dependence, VaR/ES backtest against t-copula; noise-induced tail inflation | Low–medium |
| 4 | **Quantum mRMR**: diagnostic feature-panel selection | Healthcare (other industry); zero | Kipu + IonQ feature-selection HUBO on Forte (2026) | sklearn breast cancer (bundled) | 12 qubits, 90 ZZ at p=1 with XY ring | P(optimal subset) against random/SA/greedy at equal shots; downstream nested CV | Low |
| 5 | **Fixed-Budget SQD**: N≡N bond breaking | Chemistry (agriculture/climate framing); molecules crowded, SQD absent | None for SQD; QC-AFQMC (AstraZeneca) | FCIDUMP from PySCF (shipped) | 10–12 qubits live (58–76 ZZ); 20-qubit science tier over budget | Energy error against determinant budget: all-to-all UCJ against LUCJ, heuristic and random | High |

### 1. Commit & Dispatch ranks first on brief fit, openness, data and baseline clarity

This concept is the cleanest match to every requirement:

- Energy is named in the brief, and no Qollab project touches grids.
- The IonQ precedent is direct and recent: a sampler proposing commitments with classical dispatch, 26 generators × 24 hours on Forte Enterprise, within 0.55–2.7% of optimal in simulation ([arXiv:2505.00145](https://arxiv.org/html/2505.00145v1); [IonQ news](https://ionq.com/news/ionq-partners-with-oak-ridge-national-laboratory-demonstrating-quantum-power)).
- EPB's commercial Forte Enterprise in Chattanooga gives a regional stakeholder ([QCR](https://quantumcomputingreport.com/epb-commissions-ionq-forte-enterprise-quantum-computer-in-chattanooga-hub/)).
- The data is public and fetchable: generator limits and costs from MATPOWER or pglib-opf on GitHub, and hourly demand from EIA v2. Ship a snapshot of one balancing authority's day, because the EIA key in the URL is public and rate-limited.

**The quantum core.** Aggregate the case to 10–12 units for one hour, or 6 units × 2 hours with start-up coupling. Use binary u_g with cost = no-load cost + linearized marginal cost, and enforce demand-plus-reserve coverage. Encode coverage by unbalanced penalization (the Avocados technique for inequality constraints) or by a hand-set quadratic penalty, never qiskit-optimization's 1e5 fallback. The penalty makes the cost graph dense: 45 native ZZ at n=10 and 66 at n=12, so F ≈ 0.72–0.80 at p=1. Use an LR-QAOA ramp or IonQ's Iterative-QAOA schedule (Δβ=Δγ=0.17), warm-started from the LP relaxation, so no optimizer loop touches hardware.

**The classical half and baselines.** Each sampled commitment gets priced by economic dispatch. For a single bus with linear costs that is just merit-order filling, so no LP solver is needed per sample (research-team inference). `scipy.optimize.linprog` remains available for network or ramping variants. The exact optimum comes from enumerating all 4,096 commitments, cross-checked by MILP. Add a priority-list greedy and SA at equal and 100× sample budgets. The **hybrid null** reruns the same loop with uniform, product-state (from the same warm-start biases) and SA proposal samplers.

**Suggested pre-registered thresholds** (these are suggestions):

- The best-of-1,000 dispatched QAOA sample is within 1% of the exact optimum on at least 20 of 24 hours of a real day.
- P(sample within 2% of optimum) beats the product-state null by ≥5×, with non-overlapping 95% Wilson intervals.
- QAOA loses to MILP on wall-clock; say so.

**Expected and IonQ-native extras.** With a decent penalty, expect 30–60% feasible samples and a clear low-cost tail at 66 gates (research-team estimate; verify on `forte-1`). Show the complete-graph cost layer at 66 native ZZ against roughly 198 CNOTs on a swap network. Send all 24 hourly circuits in one multi-circuit job. Add a resource panel for 26 units × 24 hours.

**The honesty paragraph writes itself.** MILP solves this in milliseconds, classical solvers are effective below about 400 units ([Koretsky et al., arXiv:2110.12624](https://arxiv.org/abs/2110.12624)), IonQ's 100–200-qubit grid-scale forecast is a vendor projection, and ORNL itself calls advantage future work. One caution from history: a unit-commitment use case did not place at NQCC 2023 ([NQCC 2023 report](https://www.nqcc.ac.uk/wp-content/uploads/2024/04/NQCC_Quantum-Hackathon-2023_Technical-report.pdf)), so rigor and presentation, not the topic, carry the score.

**Reusable code:** the brute-force and penalty-sweep pattern in `optimization_use_cases.md` (Q4/Q5 design D2), and `cors_check.sh` for the data endpoints.

### 2. Quantum Nested Dissection has the strongest IonQ alignment and the most engineering

This is the honest, public-data replay of IonQ's flagship application, the one IonQ now calls computation engineering and that won IEEE Quantum Week's Best Paper. Manufacturing is named in the brief, and Qollab has zero partitioning or sparse-linear-algebra projects.

**The pipeline:**

1. Take structural/FEA symmetric positive-definite matrices from the SuiteSparse collection, shipped as ≤2 MB files since its CORS status is untested.
2. Build the adjacency graph and coarsen by heavy-edge matching (networkx) to 12–20 nodes at the top separator level.
3. Run a **quantum balanced bisection**, with weighted cut as cost and balance as a Hamming-weight constraint. Balance maps naturally onto an XY mixer started from a balanced split, which is an inference, not a published IonQ design.
4. Refine with Kernighan–Lin/Fiduccia–Mattheyses, as Ansys did.
5. Recurse classically.
6. Factor the permuted matrix with SciPy's SuperLU and count fill (nnz of L+U) and flops ([SciPy splu](https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.linalg.splu.html)).

**Baselines:**

- natural ordering;
- reverse Cuthill–McKee (`scipy.sparse.csgraph`);
- SuperLU's built-in minimum-degree and COLAMD orderings;
- spectral (Fiedler) bisection;
- Kernighan–Lin;
- exact minimum bisection at the coarse level.

The **hybrid null** swaps the quantum bisection for exact, KL and random-balanced bisection at the same step.

**What to expect, and what to say.** At ≤20 coarse nodes the quantum step can at best match exact bisection. The measurable step is therefore how often a 1,000-shot batch contains the exact bisection (ideal, Forte-noise and one hardware job), whether the resulting fill equals the exact-bisection ordering, and how the whole nested-dissection pipeline compares with RCM and minimum degree. Say plainly that IonQ's 12–14.6% are amortized LS-DYNA wall-clock gains on 2.6M–35M-element models. Those gains rest partly on 150-qubit simulations and classical refinement, and critics dispute them ([Kirkpatrick critique](https://wkirkpatrick.substack.com/p/ionq-and-ansys); [TQI](https://thequantuminsider.com/2026/09/17/ionq-synopsys-14-6-percent-faster-engineering-simulations/)). The hackathon measures fill, not production runtime.

The selling point is that this project adds what the critics asked for: a public dataset, standard orderings as baselines, and an ablation. The risk is engineering load (coarsening, recursion, fill accounting) and a quantum contribution diluted by construction. METIS is presumably unavailable in Pyodide, which is not tested. Choose this if the team is strong in numerical linear algebra.

### 3. Qopula Stress Lab copies the proven winner's template with one sampling circuit

This concept comes closest to a guaranteed respectable entry. **KL Divergents won NQCC 2024 by extending IonQ and GE's copula paper** ([NQCC 2024 report](https://nqcc.ac.uk/wp-content/uploads/2025/04/NQCC_Quantum-Hackathon-2024_Technical-report.pdf); [arXiv:2206.11937](https://arxiv.org/abs/2206.11937)). Fidelity and IonQ ran the Bell/GHZ-seeded "qopula" on up to 8 hardware qubits ([arXiv:2109.06315](https://www.arxiv.org/pdf/2109.06315v1)). On IonQ, generation is sampling, so **the whole quantum step is one circuit** with 5,000–10,000 shots, a perfect fit for one job per run. Qollab has zero QCBM or copula projects, although finance generally is explored.

**The build:**

- **Data.** Rank-transform about 20 years of daily returns for two or three assets, for example equity, bond and gold ETFs at about 5k rows and under 0.5 MB, shipped because equity sources lack CORS. Alternatively, use crypto pairs fetched live.
- **Encoding.** Discretize to 3 bits per asset: 6 qubits and 64 cells, or 9 qubits and 512 cells.
- **Ansatz.** A Bell/GHZ-seeded copula ansatz plus all-to-all ZZ layers: 45 ZZ at 6 qubits (F≈0.80) or 72 at 9 (F≈0.70).
- **Training.** Train in the browser on exact probabilities with a multi-bandwidth MMD loss. Rudolph et al. show the bandwidth decides trainability ([arXiv:2305.02881](https://arxiv.org/abs/2305.02881)). The randomized-split KL from the winning team is optional.
- **Baselines.** Empirical histogram, Gaussian and Student-t copulas, KDE, scikit-learn's `BernoulliRBM`, and a classical MPS Born machine.
- **Metrics.** Held-out-period MMD and KL, lower-tail dependence, a 99% VaR/ES backtest (Kupiec test), and Gili's generalization metrics for unseen valid cells.

**Expected.** Rough parity with the t-copula, which is the honest finding to state up front, given that GE beat classical models only in some cases. The distinctive, sign-meaningful measurement is noise. Depolarizing noise mixes near-uniform mass into the distribution, which **fattens tails**, so measure how much 0.5% two-qubit error inflates VaR between ideal, `forte-1` and hardware samples. That number matters to a risk manager and is absent from the vendor papers. Choose this if the team is strongest in statistics or finance, or if a low-risk entry is the priority.

### 4. Quantum mRMR is the lowest-risk build with a clean exact baseline

This is feature selection for a cheaper diagnostic panel. It echoes Kipu and IonQ's April 2026 mutual-information HUBO feature selection on Forte, which used the Gallstone and Spambase datasets with SelectKBest and PCA baselines ([arXiv:2604.26834](https://arxiv.org/abs/2604.26834)).

**The build:**

- **Data.** scikit-learn's bundled breast-cancer data, with no network risk, prefiltered to the top 12 features by mutual information. State the prefilter.
- **QUBO.** Linear −MI(feature, label) terms plus λ·MI(fᵢ,fⱼ) redundancy couplings, selecting k=4 or 5.
- **Mixer.** Enforce k with an **XY ring mixer from a greedy-mRMR k-hot start**, so feasibility is 100% by construction. That costs 66 + 24 = 90 native ZZ at p=1 (F≈0.63). Optional 3-body conditional-MI terms (3 gates each) nod to Kipu's HUBO.
- **Exact optimum.** There are C(12,4) = 495 feasible subsets, so random P(opt) is about 0.2%. Expect a few percent to 10%+ ideal and about 0.6× that on noise (research-team estimate; verify).
- **Downstream test.** 5-fold nested CV of the chosen subset against SelectKBest, greedy mRMR and the exact-best subset.

Reuse `qk_bc.py`'s vectorized NumPy and nested-CV scaffolding for the downstream half. **Be prepared for downstream accuracy differences to fall within noise**, about 0.9 points per error, as Experiment A showed. The defensible quantum step is sample quality at equal shots, not diagnostic accuracy. The risks are that breast cancer reads as tutorial data (CQhack25's Q-MediScan used it) and that the impact story is modest. Pair it with a second shipped clinical dataset to lift it.

### 5. Fixed-Budget SQD is the most novel science and the hardest to land

Nobody has published SQD on IonQ, and the all-to-all advantage is concrete and measured: full UCJ beat heavy-hex LUCJ, 19.8 against 72.5 mHa at a 400-determinant budget. The problem is N₂ dissociation, the chemistry behind nitrogen fixation and the FeMoco motivation. Compute at R = 1.1, 1.5 and 2.0 Å, comparing five samplers against a capped determinant budget of 400, 1,600 and 6,400:

- all-to-all UCJ samples, noisy;
- LUCJ samples;
- a classical excitation-level heuristic, ideally also CISD-amplitude ranking;
- uniform random;
- the oracle.

The headline is the **crossover budget**, not chemical accuracy.

**The build:**

- **Live tier.** (6e,5o) or (10e,6o) at 10–12 qubits and 58–76 ZZ (F≈0.65–0.70), where saturation is trivial. Report the correct-particle-number post-selection rate and shots to accuracy.
- **Science tier.** 20 qubits at 314–348 ZZ, run once on `forte-1` with a cached fallback.
- **In the browser.** Vendor the NumPy-only SQD modules and run `kh_fci.py` on capped subspaces.
- **Precompute.** Every FCIDUMP, CCSD amplitude and FCI/CCSD(T) reference, offline with the `scripts/chemistry/` toolkit in WSL.

**The risks are the highest of the five:**

- the science tier is three times over the gate budget;
- a stronger classical selector will likely erase the quantum win;
- molecules are Qollab's most crowded topic;
- the industry framing is indirect;
- the uncapped pitfall must be explained clearly or it reads as a quantum success it is not.

Choose this only with a chemist on the team.

### Fallbacks, things to avoid, and how to decide tonight

Three fallbacks are credible.

- **MLAE tail-risk estimator.** Several 3–4-qubit lookup-table registers and m-values in one job give a VaR curve. The measured result is RMSE against oracle calls, the noise knee, and naive against noise-aware bias. It is honest and novel on Qollab, but it delivers a negative headline at 0.5% error (`qae_lut.py` already does the work).
- **Gate-assignment encoding study.** Extend IonQ–DESY by comparing one-hot (18–24 qubits), domain-wall (12–18) and log (12 qubits, 4-body terms at 5 gates each) on one instance. Its weakness is a partly synthetic distance matrix.
- **Post-earthquake shelter siting.** A real USGS event plus OpenFEMA/HDX data, max-coverage QUBO with Dicke or XY initialization, against greedy (1−1/e guarantee) and MILP. It has the best live-data story but no IonQ precedent.

Avoid these as primary topics, because Qollab or the literature has already covered them: small-molecule VQE curves, MaxCut/TSP/VRP races, Markowitz QAOA, toy-2D quantum kernels, QAOA peptide folding, prisoner's dilemmas, QCNNs, QNLP, quantum transformers, SAR change detection, HHL-style CFD claims, and anything whose result improves with noise.

**Before committing at 19:00:**

1. Read the node and global Slack and re-run `pag.py`. If IonQ releases a problem statement or dataset, adopt it and keep this benchmarking frame.
2. Otherwise choose by team strength: optimization or energy for #1, numerical linear algebra for #2, statistics or finance for #3, ML for #4, chemistry for #5.
3. Spend the first two hours on smoke tests inside Qollab:
   - `import scipy.optimize; scipy.optimize.milp`;
   - `from pyscf import gto` (for #5);
   - one multi-circuit `backend.run` on the IonQ simulator with `noise_model` and `sampler_seed`;
   - one CORS fetch of your chosen data URL;
   - the qsharp-lang import;
   - timed install of the chosen qiskit-* preset.
4. Commit a README with pre-registered thresholds before the first real run.
5. Make an early safety submission, since rough projects remain eligible and edits are allowed until the deadline.
6. Spend Sunday on the honesty panel, the limitations section, the 2–3-minute video and the required attribution line.

## Conclusion

The Impact theme looks like the "real-world" theme, but its judges have turned it into a measurement contest. Qollab's staff publicly downgraded a showcase project for beating only random cuts. IonQ's headline numbers survive mainly as workflow engineering. Every serious 2025–2026 framework, from IBM's tracker to Tuziemski's hybrid null, says advantage claims at this scale are hypotheses to falsify. The winning move is therefore not a cleverer quantum algorithm. It is the best-documented *small* quantum step on a real public dataset, set against a classical baseline strong enough that the judges cannot improve on it. The research team's own runs make the stakes concrete:

- quantum kernels tie classical ones and lose their meaning at the wrong bandwidth;
- quantum reservoirs lose to a 300-node echo-state network by two orders of magnitude once shots are counted;
- naive amplitude estimation loses to Monte Carlo at 0.5% gate error;
- SQD reaches the exact energy from pure noise.

Each of these failures, measured and explained, is worth more to these judges than an unexamined success.

The underused opportunity is the overlap between three empty sets: sectors the brief names, sectors with no Qollab project, and IonQ application stories nobody has replayed on public data with an ablation. Grid commitment and sparse-matrix partitioning sit squarely in that overlap. IonQ's own papers in both lack the classical comparisons critics asked for. A 48-hour team that supplies those comparisons is doing something IonQ's applications group has not published. In both lanes, the all-to-all gate-count advantage is a real, measurable property of IonQ hardware. That is a stronger Impact Potential argument than any projected speedup, because judges can check it in the transpiler output.
