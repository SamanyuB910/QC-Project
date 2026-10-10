# Quantum Computing Education Tools Landscape and Evidence-Based Quantum Pedagogy (research notes, compiled 2026-10-09)

Scope: (A) inventory of existing quantum-education tools (what they teach, interaction model, strengths, gaps, open-source and maintenance status as of 2026), and (B) physics education research (PER) and quantum information science education (QISE) literature from 2015 to 2026 on misconceptions, what works, design principles, and evaluation. Context: the "Quantum Unlocked" theme of the Qollab x IonQ hackathon. The tool must use Qiskit, run in the browser through Pyodide, and avoid being "just a tutorial".

Source-quality note: the single most useful anchor found is the 2026 *Resource Letter QIE-1: Research in quantum information education* by Meyer, Goorney, Kushimo and Seskir ([arXiv:2606.06445](https://arxiv.org/html/2606.06445v1)). Many entries below rely on it. Vendor figures (Q-CTRL, IBM) are self-reported. Tool-status claims are dated wherever possible. Items not verified in this session are listed separately in the Gaps subsections and flagged as background knowledge.

---

## Key Question 1: What notable quantum-education tools already exist, and what are their strengths, gaps and status (2026)?

### Takeaway
The space is crowded for **single-qubit and Bloch-sphere intuition, small gate-circuit sandboxes, photon and optics interferometry, and intro "qubits + gates + entanglement" courses**: Quirk, IBM Composer and Learning, PennyLane Codebook, Black Opal, PhET, QuVis, Quantum Flytrap, Quantum Odyssey and Brilliant all cover this ground. Advanced topics have only expert or research tools (Crumble, ZXLive, qsurface, QEC-Playground, Boulder Opal notebooks) or static catalogs (Error Correction Zoo). Several early tools are archived or unmaintained: Qiskit Textbook, Hello Qiskit, IBM Quantum Lab, the old Xanadu Codebook, and the legacy Microsoft QuantumKatas repo. Rigorous learning-gain evidence exists for only a handful (QuVis, QuILTs, PhET).

### Cited Findings

**Circuit sandboxes and simulators**
- **Quirk** (Craig Gidney): a drag-and-drop browser circuit simulator with no install and real-time output displays. It supports up to 16 qubits. Measurement is implemented through the deferred-measurement principle, so measured qubits cannot be "recohered". The author calls it a "toy" for exploring small circuits. Open source on GitHub (Strilanc/Quirk), with many forks. No controlled classroom study of Quirk was found. — [GitHub Strilanc/Quirk](https://github.com/Strilanc/Quirk); [Algassert 2016 post](https://algassert.com/2016/05/22/quirk.html)
- **Soniq-Quirk** (Quantum Village): a sonically enabled fork of Quirk. It is the only audio-based (potentially accessibility-relevant) circuit tool surfaced. — [GitHub QuantumVillage/Soniq-Quirk](https://github.com/QuantumVillage/Soniq-Quirk)
- **IBM Quantum Composer and IBM Quantum Learning**: the classic IBM Quantum Platform was sunset on July 1, 2025. Learning and Composer moved to quantum.cloud.ibm.com. Composer is "mostly unchanged", but project files are no longer saved on the platform and must be downloaded locally. Learning advertises 10+ courses plus "Qiskit in Classrooms" teacher modules. New 2025 material includes Quantum Diagonalization Algorithms (SQD and Krylov) and Quantum Computing in Practice. Content is viewable without login. Learning got a refreshed homepage and catalog pages in Oct 2025. — [IBM blog: IQL migration](https://www.ibm.com/quantum/blog/iql-migration); [IBM 2025-06-20 platform update](https://quantum.cloud.ibm.com/announcements/en/product-updates/2025-06-20-platform-updates); [IBM 2025-10-02 learning update](https://quantum.cloud.ibm.com/announcements/en/product-updates/2025-10-02-learning-updates)
- **Qiskit Textbook**: its repo states it "has been superseded by IBM Quantum Learning", its source files are no longer maintained and may contain errors, and contributions are not accepted. **IBM Quantum Lab** (hosted Jupyter) was sunset May 15, 2024. The "Games and Demos" notebooks repo (including **Hello Qiskit**) was archived on Jan 18, 2024. — [Qiskit textbook page](https://qiskit.org/textbook/ch); [Hello Qiskit page](https://qiskit.org/textbook/ch-ex/hello-qiskit.html); [qiskit-community-tutorials games](https://github.com/qiskit-community/qiskit-community-tutorials/blob/master/games/)
- **Microsoft Quantum Katas**: open-source, self-paced Q# exercises in which each task requires filling in code and a test harness gives real-time feedback. An aggregator shows the legacy GitHub repo's last push on May 6, 2024. — [ecosyste.ms listing of microsoft/QuantumKatas](https://awesome.ecosyste.ms/projects/github.com%2Fmicrosoft%2FQuantumKatas)
- **PennyLane Codebook** (Xanadu): relaunched May 2024 with account-linked progress. The old Xanadu Quantum Codebook was retired after Dec 31, 2024, and a Quantum Machine Learning module was added later. Format: short reading plus coding exercises in PennyLane, not Qiskit. — [PennyLane blog: Codebook makeover (2024)](https://pennylane.ai/blog/2024/05/pennylane_codebook_makeover); [PennyLane forum: farewell to old Codebook](https://discuss.pennylane.ai/t/final-farewell-to-the-old-xanadu-quantum-codebook-completing-the-transition-to-the-new-pennylane-codebook/7450); [QML module thread](https://discuss.pennylane.ai/t/quantum-machine-learning-module-on-codebook/8845)
- **Q-CTRL Black Opal** (commercial): visual, gamified, step-by-step lessons. The company reports 400+ lessons across 10 core topics, 26,000+ users, LMS compatibility, a 2025 EdTech Breakthrough award, and large deployments (Tamil Nadu: 3,000+ students at 83% completion; UK NQCC: 30,000+). Figures are company-reported. Not open source. — [Quantum Insider, Sept 2025](https://thequantuminsider.com/2025/09/17/q-ctrl-partners-with-qucan-to-offer-global-virtual-classroom-experience-to-aspiring-quantum-professionals/); [Quantum Insider, June 2025](https://thequantuminsider.com/2025/06/11/q-ctrl-expands-presence-in-india-with-four-new-collaborations/); [The New Stack (2021)](https://thenewstack.io/q-ctrl-black-opal-quantum-learning-for-the-masses/)
- **Brilliant "Quantum Computing" course**: launched May 2019 with Microsoft and Alphabet's X (and Caltech IQIM). Browser circuit puzzles run on a drag-and-drop simulator that "does the heavy math". It later introduces Q# with Python as host. Estimated 16–24 hours. Paywalled beyond free chapters. — [Engadget 2019](https://www.engadget.com/2019/05/26/microsoft-brilliant-quantum-computing-curriculum/); [Brilliant course page](https://brilliantorg-infra-prod.brilliant.org/courses/quantum-computing)

**Research-based simulations (PER-backed)**
- **QuVis** (Univ. of St Andrews, Antje Kohnle): research-based simulations from advanced high school to advanced undergraduate level, iteratively refined from one-on-one observation sessions and in-class trials. The two-level-systems (qubit-equivalent) suite was evaluated in Kohnle et al., *Am. J. Phys.* 83, 560 (2015), which reports evidence of learning at intro and advanced levels and positive student perceptions. There are four QKD simulations (BB84-style, with photons or spin-1/2) refined over 3 years of student evaluation. Newer builds are HTML5 and tablet-friendly, while older builds were Flash. The newest evaluations found are from 2015–2017. — [QuVis about](https://www.st-andrews.ac.uk/physics/quvis/de/index-about.php); [Kohnle et al. 2015, arXiv:1501.07905](https://arxiv.org/abs/1501.07905); [QKD simulations, St Andrews portal](https://research-portal.st-andrews.ac.uk/en/publications/interactive-simulations-for-quantum-key-distribution/)
- **PhET "Quantum Measurement" and "Quantum Coin Toss"** (2025, HTML5): screens cover classical vs quantum "coins" with a chosen superposition, single-photon polarization through a PBS, and a **Spin screen** (prepare spin-1/2 states, Stern–Gerlach chains, a Bloch sphere showing precession under a B-field, and collapse on measurement). There is an April 2025 teacher's guide. GPL-3.0, with GitHub last pushed Nov 2025 per an aggregator. Target: high school and intro college. — [AAPT SM 2025 abstract](https://archive.aps.org/aaptsm/2025/d05/3); [PhET teacher guide](https://phet.colorado.edu/files/teachers-guide/quantum-measurement-html-guide_en.pdf); [ecosyste.ms listing](https://awesome.ecosyste.ms/projects/github.com%2Fphetsims%2Fquantum-measurement)
- **QuILTs** (Quantum Interactive Learning Tutorials, Univ. of Pittsburgh, Singh, Marshman et al.): research-validated guided-inquiry tutorials, often paired with simulations. Topics include B92 QKD, entanglement-based QKD (PERC 2025), Mach–Zehnder with single photons, quantum eraser, and basics of quantum computing (Hu, Li & Singh, PRPER 20, 020108, 2024). — [DeVore & Singh, PRPER 16, 010126 (2020)](https://link.aps.org/doi/10.1103/PhysRevPhysEducRes.16.010126); [PERC 2025 entanglement-QKD QuILT](https://www.per-central.org/perc/2025/detail.cfm?ID=19285); [Marshman & Singh, PRPER 13, 010117 (2017)](https://link.aps.org/doi/10.1103/PhysRevPhysEducRes.13.010117); [Hu, Li & Singh arXiv:2408.04859](https://arxiv.org/pdf/2408.04859)
- **AceQIS** (Corsiglia et al.) and **VQOL** (La Cour et al., IEEE QCE 2022, web optics simulator): listed in the Resource Letter. AceQIS effectiveness evidence is only in a 2023 thesis, not peer-reviewed. — [Resource Letter QIE-1](https://arxiv.org/html/2606.06445v1)

**Photon and optics sandboxes and games**
- **Quantum Flytrap Virtual Lab** (Migdał et al.): a free, browser-based, no-code optical table with real-time simulation of up to 3 entangled photons, drag-and-drop elements, and a sandbox mode. A 2021 talk said it was used in Stanford and Oxford undergrad QI courses. Its visualization libraries are open-source TypeScript (Quantum Tensor, BraKetVue). Paper: *Opt. Eng.* 61(8) 081808 (2022) and CHI EA 2022. — [arXiv:2203.13300](https://arxiv.org/abs/2203.13300); [ACM CHI EA 2022](https://dl.acm.org/doi/10.1145/3491101.3519885); [IEEE Quantum Ed post](https://ed.quantum.ieee.org/?p=3424)
- **Quantum Game with Photons** (Migdał): v1 was 2016. v2 (beta Apr 3, 2020) was built with CQT Singapore. Open source, playable at quantumgame.io, with 31 puzzles in which players route photons to detectors. Some levels reproduce famous experiments (e.g., building an interferometer). — [CQT highlight](https://www.quantumlah.org/about/highlight.php?id=357); [Boing Boing 2017](https://boingboing.net/2017/12/15/schroedingers-browser.html/amp)
- A 2025 paper argues that no-code approaches (including Flytrap) have limited effectiveness when learners do not transition to formal, mathematical approaches. Exact attribution is uncertain; it surfaced via search alongside [MDPI Educ. Sci. 15(9):1167 (2025)](https://www.mdpi.com/2227-7102/15/9/1167).

**Puzzle, board and citizen-science games**
- **Quantum Odyssey** (Quarks Interactive): a visual puzzle sandbox for designing and reverse-engineering quantum algorithms without code, ranging from guided tutorials to very hard puzzles. Steam early access opened Jan 29, 2025. Paid. A feasibility study (UK, 10 groups of 5 students aged 11–18, 30-minute sessions) found its visuals "efficient in portraying counterintuitive quantum computational logic"; the piloted version had no narration. — [Steam](https://store.steampowered.com/app/2802710/Quantum_Odyssey/); [Nita et al. arXiv:2106.07077](https://arxiv.org/abs/2106.07077)
- **Hello Quantum** (IBM Research and Univ. of Basel / James Wootton): a free iOS/Android puzzle app (2018) in which players find the circuit taking an input state to a target state. **Current store availability could not be verified.** — [TNW 2018](https://www.thenextweb.com/news/ibms-hello-quantum-is-a-devilishly-difficult-puzzle-game-about-qubits); [Aalto quantum games portfolio](https://quantumgames.aalto.fi/portfolio/hello-quantum/)
- **Decodoku** (Wootton): citizen-science QEC decoding puzzles (qudit surface-code variants) that need no quantum background. Player strategies can inform decoders. iOS, Android and browser. MIT license. — [Wikipedia: Decodoku](https://en.wikipedia.org/wiki/Decodoku); [Wootton arXiv:1712.09649](https://arxiv.org/pdf/1712.09649)
- **Quantum Moves / Quantum Moves 2** (ScienceAtHome, Aarhus): citizen-science optimization of atom transport. QM2 launched 2018 (ReGAME Cup). Reported player counts conflict (3,600 unique vs 250,000+). An educational version was tested with 3 high-school classes using perception-based measures: authentic research participation was motivating, and expert role assignment raised perceived learning. — [Wikipedia: Quantum Moves](https://en.wikipedia.org/wiki/Quantum_Moves); [arXiv:1511.01653](https://arxiv.org/abs/1511.01653v1); [Aarhus game-based education](https://phys.au.dk/forskning/forskningscentre-og-grupper/quantum-measurement-and-manipulation-group/research-game-based-education)
- **Entanglion** (IBM Research, Ashoori & Weisz, 2018): an open-source cooperative 2-player board game teaching qubits, superposition, entanglement, measurement and error. Iterative design with playtesters reporting it was engaging and educational. Used with notebook tools for Year 9–12. — [IBM Research publication page](https://research.ibm.com/publications/entanglion-a-board-game-for-teaching-the-principles-of-quantum-computing); [analog.games listing](https://www.analog.games//gameItem/show/419cd83f9683336701968401d1250e09?lang=DE)
- **QPlayLearn**: includes "Qubit", an interactive Bloch-sphere trainer for composing small circuits. Built on Qiskit, with explanations pitched at multiple levels (school to researcher). — [Quantum Zeitgeist roundup](https://quantumzeitgeist.com/10-quantum-games-that-can-help-you-learn-the-field-of-quantum-computing/) (secondary source)
- **Survey of games and tools** (Seskir et al., *Opt. Eng.* 61(8) 081809, 2022): presents tools as described by their developers. It found **no common design methodology and no universal evaluation tool** for quantum games. Only a few (Quantum Moves 2, Particle in a Box, Quantum Odyssey) had peer-reviewed evaluations. — [arXiv:2202.07756](https://arxiv.org/pdf/2202.07756)

**Spaced repetition and explanatory media**
- **Quantum Country** (Matuschak and Nielsen, the "mnemonic medium"): essays with embedded spaced-repetition prompts. Data are from Matuschak's working notes, not peer-reviewed. Once a prompt is recalled at a 5-day interval, the typical reader answers correctly ~95% of the time (25th/50th/75th percentiles: 89/95/98% at 5 days; 96/99/100% at 4 months). Lapses are under 2% of repetitions for most readers. Median demonstrated retention grows from ~8 days after the first review to ~150 days by the fifth. In an informal 2019 causal test, delaying reviews dropped accuracy by 4 pp, while controls rose 7 pp. Caveats: survivorship and selection effects. — [Matuschak: five-day retention](https://notes.andymatuschak.org/zS5uKLsoTbkJSadTv2U3Z4G3uEBrFxTLy5E); [2019 efficacy experiment](https://notes.andymatuschak.org/z2cKiAiZ8tAWiz4ZUoTaaBv); [causal impact note](https://notes.andymatuschak.org/zuCfBJSkm5BnqC1qw1bLH2)
- **3Blue1Brown**: "But what is Quantum Computing? (Grover's Algorithm)", posted Apr 30, 2025, opens with a "Misconceptions" segment targeting "tries all possibilities in parallel". Scott Aaronson was consulted. A May 4, 2025 follow-up ("Where my explanation of Grover's algorithm failed") clarified oracle-setup confusion. This shows that even expert explainers trip over the oracle/black-box framing. — [Video mirror](https://yt.chop.dev/en/v/RQWpF2Gb-gU); [3B1B members post (follow-up)](https://members.3blue1brown.com/posts/where-my-of-128116047)

**QEC, stabilizer and ZX tools (expert-oriented)**
- **Crumble** (Gidney, part of Google's Stim): an "early prototype" browser stabilizer-circuit editor for exploring, editing and **propagating Paulis** in 2D stabilizer circuits (via marker pragmas). It has surface-code examples, layer navigation, and Stim-text import/export. **CrumPy** brings Crumble timelines into Jupyter. Used in a Coursera QEC course. — [algassert.com/crumble](https://algassert.com/crumble); [CrumPy on PyPI](https://pypi.org/project/crumpy/); [Coursera QEC course](https://www.coursera.org/de-DE/learn/quantum-error-correction)
- **qsurface** (Python): step-by-step surface-code simulation and decoding visualization with MWPM and Union-Find decoders and history scrubbing. Requires Tkinter/PyQt (desktop, not browser). Last push Dec 2025. — [qsurface docs](https://qsurface.readthedocs.io/)
- **QEC-Playground** (Yale, Rust): a research tool for surface codes with a 3D GUI and an interactive tutorial credited to one contributor. Docs are "in progress" (pre-1.0). — [PyPI qecp](https://pypi.org/project/qecp/0.2.3/)
- **Error Correction Zoo** (Victor V. Albert, Philippe Faist et al.): a curated catalog of classical and quantum codes with "succinct pedagogical descriptions" and code hierarchies and graphs. 300+ codes as of 2023, data on GitHub, and a Handbook edition on arXiv (CC-BY-SA 4.0, 2026). It is a **reference, not interactive**. Companion: **QECirc** (2026) for QEC circuits. — [EC Zoo about](https://errorcorrectionzoo.org/about); [APS MAR23 abstract](https://meetings.aps.org/Meeting/MAR23/Session/S72.1); [Handbook arXiv:2606.11484](https://arxiv.org/pdf/2606.11484); [QECirc arXiv:2609.20182](https://arxiv.org/pdf/2609.20182)
- **"Quantum Error Correction for Kids"** (Wolf, 2024): an intuitive gamified approach to the **stabilizer formalism**. No learning outcomes are reported in the excerpt seen. — [arXiv:2405.06795](https://arxiv.org/pdf/2405.06795)
- **ZXLive and PyZX**: ZXLive is a visual proof assistant for ZX-diagrams. Users draw diagrams or load QASM, then "Start Derivation", after which the diagram can change only through ZX rewrites (e.g., drag a Z spider onto an X spider to apply bialgebra). It exports TikZ. Desktop Qt app via pip, Apache-2.0, self-described "pretty early stage". PyZX (Kissinger and van de Wetering 2019) is the engine. — [ZXLive docs](https://zxlive.readthedocs.io/en/latest/gettingstarted.html); [GitHub zxcalc/zxlive](https://github.com/zxcalc/zxlive); [PyZX arXiv:1904.04735](https://arxiv.org/abs/1904.04735v2)

**Hardware-physics and advanced-topic tutorials (code notebooks, not interactives)**
- Trapped-ion **Mølmer–Sørensen gates**: Q-CTRL Boulder Opal Python notebooks show entangling-phase evolution and motional phase-space trajectories, and one tutorial designs an MS gate for two Yb ions. These are notebooks, not browser interactives. — [Boulder Opal MS dynamics](https://docs.q-ctrl.com/boulder-opal/user-guides/how-to-calculate-system-dynamics-for-arbitrary-molmer-sorensen-gates); [Boulder Opal MS tutorial](https://docs.q-ctrl.com/boulder-opal/tutorials/optimize-molmer-sorensen-gates-for-trapped-ions)
- **Magic-state distillation**: QuEra Tsim tutorial (85-qubit circuit) and a PennyLane Catalyst T-state purification demo. Both are code notebooks. — [QuEra Tsim tutorial](https://bloqade.quera.com/tsim/tutorials/magic_state_distillation); [PennyLane Catalyst demo](https://docs.pennylane.ai/projects/catalyst/en/stable/demos/magic_distillation_demo.html)

**2024–2026 newcomers**
- AI tutors: an ODU Intelligent Teaching Assistant (knowledge-graph-augmented, with two LLM agents for live dialogue and lesson planning) appeared at IEEE QCE 2025 and is being tested in an advanced QC course. Benefits are claimed in news coverage, not measured. — [arXiv:2504.18603](https://arxiv.org/pdf/2504.18603); [ODU news](https://www.odu.edu/article/odus-new-ai-tutor-for-quantum-computing-empowers-students-to-find-the-answers-themselves); [ODU classroom preprint arXiv:2604.24807](https://arxiv.org/pdf/2604.24807)
- **QuantAid**: an LLM analogy engine tailored to students' hobbies, plus quizzes. Pilot N=21 showed higher engagement and "modest conceptual gains" vs static materials. — [ACM DL](https://dl.acm.org/doi/10.1145/3770762.3772593)
- LLM-generated hints were on par with expert-created tips for QC questions, with caveats about a possible "AI placebo" and leading hints. — [arXiv:2407.17024](https://arxiv.org/html/2407.17024)
- "ChatGPT Solves All Tested Qiskit Homework Assignments" (2026, title only seen), which raises integrity concerns for code-exercise tools. — [arXiv:2608.19707](https://arxiv.org/pdf/2608.19707)
- Others: Quantum Intuition XR (Meta Quest 3 Bloch-sphere/measurement VR, 2025) — [arXiv:2504.08984](https://arxiv.org/pdf/2504.08984); Quantum Table (tangible circuit demonstrator, QP 2025) — [programming-conference.org](https://2025.programming-conference.org/details/qp-2025-papers/3/Quantum-Table-A-Tangible-Quantum-Circuit-Demonstrator); Bloch Cubes hands-on manipulatives — [arXiv:2412.03003](https://arxiv.org/pdf/2412.03003); CQHack25 QEC Visualizer (Streamlit hackathon project, Classiq track) — [Devpost](https://devpost.com/software/quantum-error-correction-qec-educational-visualizer).

**Qollab context**
- IonQ partnered with Qollab.xyz's second annual Creative Challenge (announced March 2026). It seeks "original, open-source quantum experiments" emphasizing creativity, storytelling, interactivity and technical rigor. Selected projects are showcased and remain public for at least a year. The previous winners, **"Quantum Garden" and "QAVE"**, are live on Qollab's projects page; check them for novelty overlap. — [IonQ press release](https://www.ionq.com/news/ionq-partners-with-qollabs-creative-challenge-advancing-creative-quantum-innovation)

### Inferences
- A Qiskit/Pyodide tool that is "another circuit sandbox", "another Bloch sphere" or "another photon interferometer" competes with Quirk, Composer, PhET (2025), QPlayLearn, Flytrap and Quantum Odyssey, and will struggle on novelty.
- The space between expert tools (Crumble, ZXLive, qsurface, Boulder Opal) and beginner sandboxes is mostly empty. Nothing is a **browser-native, guided, misconception-targeted interactive for an advanced topic**. That is the clearest novelty opening.
- Because IonQ judges, a trapped-ion-native topic (e.g., MS-gate phase-space loops, or all-to-all connectivity) may resonate. Only Python notebooks exist there.

### Gaps
The following were **not verified in this session**. Descriptions are background knowledge and should be checked before citing:
- **Qubit by Qubit** (The Coding School): free, year-long intro QC course for high schoolers, launched around 2020 with industry partners. Current status unknown.
- **Quantum Tic-Tac-Toe** (Allan Goff, mid-2000s; *Am. J. Phys.* paper as a "teaching metaphor for superposition") and **Quantum Chess** (Chris Cantwell / Quantum Realm Games, Steam): maintenance status unknown.
- **Quantum Inspire** (QuTech, cloud hardware and knowledge base), **Classiq** (high-level synthesis platform with a learning library and hackathon partnerships), **SandboxAQ** (not primarily an education provider): education offerings unverified.
- **Quantum Atlas** (Univ. of Maryland/JQI illustrated explainers), **Algassert blog** visualizations, **QuTiP** visualization (Bloch, Wigner, Hinton plots; Python, not browser), and standalone Bloch-sphere simulators: not checked.
- Whether Qollab's runtime is Pyodide with Qiskit could not be confirmed from public sources. One developer reported Qiskit import failures under PyScript. — [Zeroqode forum](https://forum.zeroqode.com/t/help-needed-integrating-qiskit-for-quantum-circuit-visualization-in-pyscript/12890)
- The current Hello Quantum app-store status and the current Quirk commit activity were not confirmed.

---

## Key Question 2: Which hard quantum topics are underserved by existing interactive tools?

### Takeaway
No beginner-to-intermediate, browser-based, guided interactive was found for: **measurement-based QC (cluster states with adaptive measurement)**, **magic states and distillation**, **trapped-ion MS-gate physics**, **noise channels, Kraus operators and decoherence of density matrices**, **reduced states and partial trace of subsystems**, and **novice-friendly stabilizer/syndrome decoding with Pauli propagation**. QSVT and entanglement distillation were not specifically searched (see Gaps). Several of these coincide with topics PER shows are hardest: subsystem states, mixed vs pure, and entanglement and CNOT.

### Cited Findings
- **MBQC**: no interactive educational tool found. The structure (prepare a cluster state, then measure single qubits with bases that depend on earlier outcomes) is well defined by Raussendorf, Browne and Briegel (PRA 2003). — [arXiv quant-ph/0301052](https://arxiv.org/pdf/quant-ph/0301052)
- **Magic-state distillation**: only code notebooks (QuEra Tsim, PennyLane Catalyst) and a research paper rendering distillation as dynamical-system flow diagrams. No interactive explorer. — [QuEra](https://bloqade.quera.com/tsim/tutorials/magic_state_distillation); [PennyLane](https://docs.pennylane.ai/projects/catalyst/en/stable/demos/magic_distillation_demo.html); [arXiv:2412.04402](https://arxiv.org/html/2412.04402v1)
- **Trapped-ion MS gate**: physics is a bichromatic field near the red and blue sidebands, with a geometric phase proportional to the enclosed phase-space loop area. Visualization exists only in Q-CTRL Boulder Opal Python notebooks. — [Boulder Opal](https://docs.q-ctrl.com/boulder-opal/user-guides/how-to-calculate-system-dynamics-for-arbitrary-molmer-sorensen-gates); [Monroe lecture notes](https://boulderschool.yale.edu/sites/default/files/files/MonroLectureNotes%20-%20IonTrapGates.pdf)
- **QEC decoding and stabilizers**: Crumble is an expert prototype, qsurface is a desktop Python research tool, QEC-Playground is pre-1.0 research software, and Decodoku hides the quantum layer. The EC Zoo is a static catalog. — [Crumble](https://algassert.com/crumble); [qsurface](https://qsurface.readthedocs.io/); [qecp](https://pypi.org/project/qecp/0.2.3/); [Decodoku](https://en.wikipedia.org/wiki/Decodoku); [EC Zoo](https://errorcorrectionzoo.org/about)
- **Multi-qubit state visualization is unsettled**: 25 instructors showed little consensus on representations beyond standard symbolic forms, especially for multiple qubits (Rexigel et al., *EPJ QT* 12, 22, 2025). — [Resource Letter QIE-1](https://arxiv.org/html/2606.06445v1)
- **QEC, no-cloning and decoherence learning are essentially unstudied in PER**: no student-understanding study specific to these was found. QCCS deliberately excludes algorithms and communication. — [QCCS paper](https://arxiv.org/html/2608.14459v1); [Resource Letter QIE-1](https://arxiv.org/html/2606.06445v1) (which lists no QEC/decoherence difficulty studies)
- **Accessibility**: no screen-reader-native, tactile or sonified quantum-circuit education tool was found apart from the Soniq-Quirk fork. — [Soniq-Quirk](https://github.com/QuantumVillage/Soniq-Quirk)

### Inferences
- The strongest "underserved + evidence-backed + IonQ-relevant" candidates are:
  - (a) **Reduced states and entanglement detection**: QCCS's hardest items concern subsystem states (see KQ3), and no tool targets this.
  - (b) **Noise channels, Kraus operators and density matrices**: well-documented superposition-vs-mixture confusion, with no interactive.
  - (c) **Stabilizer/syndrome extraction for novices**: Crumble is too expert, and CNOT/phase-kickback misconceptions are documented.
  - (d) **Trapped-ion MS-gate phase-space geometry**: IonQ-native, notebooks only.
  - (e) **MBQC**: no tool at all.
- Each can be made "not just a tutorial" with a manipulable model, predict-then-reveal challenges, and a Qiskit-computed ground truth.

### Gaps
- **QSVT, entanglement distillation and purification, and Kraus/noise-channel visualizers** were not explicitly searched. Absence of evidence here is not evidence of absence.
- Graph-state and MBQC libraries (e.g., Graphix) may have visual outputs, but these were not checked.

---

## Key Question 3: What are the most common, well-documented misconceptions, and which interventions measurably fix them?

### Takeaway
The best-documented QISE difficulties are:
- confusing **superposition with mixtures**
- misreading **measurement probability** (amplitude vs squared amplitude)
- **qubit-ordering and basis-state vs qubit** conflation
- **separability vs entanglement** errors, including "all entangled states are maximal"
- **CNOT overgeneralization** (missing that CNOT creates entanglement, or that it can affect the control via phase kickback)
- **tensor-product dimension added instead of multiplied**
- **subsystem (reduced) states**
- **Bloch-sphere/global-phase equivalence**
- "**entanglement allows FTL signaling**"
- "**quantum computers try all answers in parallel**"

Interventions with measured gains are mainly **research-validated guided-inquiry tutorials (QuILTs)**, **iteratively tested sims (QuVis, PhET)**, and **pairing a visualization with Dirac notation (dimensional circle notation)**. Evidence for games, misty states and AI tutors is mostly perception-based.

### Cited Findings

**Documented difficulties**
- **Superposition vs mixed states**: students can compute probabilities from a superposition but often cannot identify its experimental implications, and they struggle to distinguish superposition from mixtures (Passante, Emigh & Shaffer, PRSTPER 11, 020135, 2015; sophomore to graduate). — [PRSTPER 11, 020135](https://link.aps.org/doi/10.1103/PhysRevSTPER.11.020135)
- **Distractors in Hu, Li & Singh (2024) QC-basics QuILT** were built on known errors: qubit order, probability as magnitude rather than squared magnitude, conflating basis states with qubits, and confusing separability with entanglement. "A few persistent challenges" remained after the tutorial. — [arXiv:2408.04859](https://arxiv.org/pdf/2408.04859); [Resource Letter QIE-1](https://arxiv.org/html/2606.06445v1)
- **QCCS background difficulties**: belief that all entangled states are maximally entangled; trouble linking entanglement, product states and separability; tensor-product dimension added rather than multiplied; overgeneralized CNOT control/target rules and failure to see that CNOT creates entanglement; inability to experimentally distinguish superpositions from mixtures or relative-phase variants. — [Meyer et al. 2026, arXiv:2608.14459](https://arxiv.org/html/2608.14459v1)
- **Hardest QCCS items** (v2.2, CTT proportion correct): I15 = 0.23, I20 = 0.25, I18 = 0.26, then I14 = 0.46 and I11 = 0.47. I18 maps to "find the state of a subset of qubits (or state it is not well-defined as a ket)". I15 maps to subsystem state, post-measurement state, gate evaluation and circuit final state. I20 maps to Hilbert-space dimension. The item-to-objective mapping is partially truncated, so treat it as tentative. — [arXiv:2608.14459](https://arxiv.org/html/2608.14459v1)
- **CNOT and phase kickback**: "Can a CNOT Gate Affect the Control Qubit?" (2026). Students switch between "playing quantum computer" (computing) and conceptual arguments across contexts. Qualitative control/target rules help at first but overgeneralize. — [arXiv:2604.16624](https://arxiv.org/pdf/2604.16624); [AAPT SM 2025 poster](https://archive.aps.org/aaptsm/2025/db01/49)
- **Interpreting states**: students use "Naive Measurement Probabilities" vs "Virtual Quantum Computer" strategies (Meyer et al., PERC 2021). "Are quantum computers just analog classical computers?" misconceptions appear among upper-division and graduate students (Meyer et al., PERC 2022; interviews with 22 undergrads and 6 grads). — [Resource Letter QIE-1](https://arxiv.org/html/2606.06445v1); [PhysPort QCCS page](https://www.physport.org/assessments/assessment.cfm?A=QCCS)
- **Entanglement**: persistent misconceptions (Kohnle & Deffebach, PERC 2015; Brang et al., *EPJ QT* 11, 33, 2024). Classical textbook analogies can oversimplify entanglement (Zwickl & Hersom, PERC 2024). Instructors report the **FTL-signaling** belief, partly traced to popular media. — [Resource Letter QIE-1](https://arxiv.org/html/2606.06445v1); [Majidy arXiv:2405.20923](https://arxiv.org/html/2405.20923)
- **Measurement needs a conscious observer**: an instructor-reported misconception linked to textbook illustrations and media. — [Majidy 2024/2026](https://arxiv.org/html/2405.20923)
- **Density matrices**: students conflate uncertainty about preparation with the spread of measurement outcomes. "A pure state does not imply certainty, nor can a mixed state be equated simply with classical ignorance" (it may be the reduced state of an entangled system). — [Majidy, arXiv:2405.20923](https://arxiv.org/html/2405.20923)
- **Bloch sphere**: Hu et al. (*Eur. J. Phys.* 45, 025705, 2024) address measurement probabilities and **equivalent states** (global phase) on the Bloch sphere. — [Resource Letter QIE-1](https://arxiv.org/html/2606.06445v1)
- **Language "simultaneous"**: an ISSEP 2025 poster argues that "simultaneous states" wording leads to misinterpretation of superposition. — [ISSEP 2025 poster](https://issep2025.uni-trier.de/src/poster/ISSEP2025-Poster-Krosse-QuantumComputing.pdf)
- **"Tries all answers in parallel"**: Aaronson calls it the single most common popular misconception. 3Blue1Brown's 2025 Grover video explicitly targets it. **No PER study testing it as a standalone misconception was found.** — [Aaronson, QC for high school students](https://scottaaronson.com/writings/highschool.html); [Aaronson on 3B1B video](https://www.goodreads.com/author_blog_posts/25718407-quantum-ai-everything-but-trump)
- **Math and notation barriers**: Dirac notation, translating across notations, inner and outer products, and tensor products (Kushimo & Thacker, IEEE QCE 2023). — [search summary citing Kushimo & Thacker](https://arxiv.org/pdf/2606.06445)
- **General upper-level QM pattern**: overgeneralizing concepts from one context to another, and difficulty distinguishing closely related concepts (Singh & Marshman 2015 review). — [arXiv:1504.02056](https://arxiv.org/pdf/1504.02056)
- **Secondary and lower-undergrad research gap**: superposition, time dependence and measurement are barely investigated at these levels (Krijtenburg-Lewerissa et al. 2017, 74 articles). — [PRPER Feb 2017 (DOAJ)](https://doaj.org/article/c63959061bd9423f8d8b14bf640fca80)

**Interventions with measured or semi-measured effects**
- **QuILT, B92 QKD**: average pretest 56% (N=49) to posttest 91% (N=50) (DeVore & Singh, PRPER 16, 010126, 2020). — [PRPER 16, 010126](https://link.aps.org/doi/10.1103/PhysRevPhysEducRes.16.010126)
- **QuILT, QC basics** (Hu, Li & Singh, PRPER 20, 020108, 2024): "notable learning gains beyond traditional lecture-based instruction", with some persistent challenges. — [Resource Letter QIE-1](https://arxiv.org/html/2606.06445v1)
- **QuILT, entanglement-based QKD** (Doyle & Singh, PERC 2025): validation suggests improved understanding. Effect sizes are not in the abstract. — [PERC 2025](https://www.per-central.org/perc/2025/detail.cfm?ID=19285)
- **QuILT, Mach–Zehnder with single photons**: in-class evaluations suggest effectiveness (Marshman & Singh 2017). — [PRPER 13, 010117](https://link.aps.org/doi/10.1103/PhysRevPhysEducRes.13.010117)
- **QuVis two-level systems**: evidence of learning at intro and advanced levels (Kohnle et al., AJP 2015). — [arXiv:1501.07905](https://arxiv.org/abs/1501.07905)
- **Dimensional Circle Notation (DCN)** (Bley et al.): each qubit gets a spatial axis, so separability appears as **visual symmetry** (PR Research 6, 023077, 2024). An eye-tracking study (PRPER 22, 010126, 2026) on Hadamard problems found that showing DCN **alongside Dirac notation increased performance and reduced cognitive load for novices**. Learners who switched more often between notations benefited less. — [arXiv:2305.07596](https://arxiv.org/pdf/2305.07596); [arXiv:2505.21508](https://arxiv.org/html/2505.21508v3)
- **Bloch sphere vs "Quantum Bead"** (Qerimi et al. 2025, N=149 school students): no difference in post-test learning. The Bloch sphere gave significantly more efficient application-task performance, cognitive load was similar, and 1–2-week retention was stable. Early performance best predicted retention. — [arXiv:2507.21721](https://arxiv.org/abs/2507.21721)
- **Misty states / Q is for Quantum**: high-school participants rated felt learning at 8.6/10 vs 7.4 for Quantum Flytrap (2026). There was an 8-week CS-sophomore course built on it (APS 2024, described as "incredibly effective"). Evidence is self-report from the developers' group, with no control group. — [arXiv:2608.12437](https://arxiv.org/pdf/2608.12437); [APS MAR24 K61.4](https://meetings.aps.org/Meeting/MAR24/Session/K61.4); [Teaching QIS to HS students, arXiv:2005.07874](https://arxiv.org/pdf/2005.07874)
- **Generic PER strategies applicable to quantum** (Majidy review of 122 works plus 12 instructor interviews):
  - predict–observe–explain (prediction associated with better retention, but not causally isolated)
  - peer discussion with "trap" poll answers (52% to 80% correct in a classical example)
  - simulation plus tutoring (ViPS)
  - multi-tier diagnostics

  Cautions: a video containing misconceptions *increased* misconceptions (Kulgemeyer & Wittwer). — [arXiv:2405.20923](https://arxiv.org/html/2405.20923)

**Spaced repetition**
- Mnemonic-medium data (Quantum Country) show high long-term retention of declarative prompts, plus a small informal causal test (KQ1). These measure **recall of prompts**, not conceptual transfer. — [Matuschak notes](https://notes.andymatuschak.org/zS5uKLsoTbkJSadTv2U3Z4G3uEBrFxTLy5E)

**Games**
- No controlled pre/post evidence of quantum-knowledge gains from quantum games was found. The literature is developer self-descriptions, a few single-game evaluations, and perception studies. Examples: a quantum-technology escape game (N=87) with interest and perceived understanding rated above neutral, and no gender, grade or prior-knowledge differences; and the Quantum Odyssey feasibility study. — [Seskir et al. 2022](https://arxiv.org/pdf/2202.07756); [2026 quantum education ecosystem review](https://arxiv.org/pdf/2604.06293); [escape-game study](https://openaccess-api.cms-conferences.org/articles/download/979-8-950676-13-0_44)
- Games are argued to support "creative abstraction" (Chiofalo et al. 2024), and Piispanen et al. (*EPJ QT* 12, 7, 2025) give an analytical definition of quantum games. Both are conceptual, not outcome studies. — [Resource Letter QIE-1](https://arxiv.org/html/2606.06445v1)

### Inferences
- The two QCCS items that are hardest by a wide margin (~23–26% correct) concern **states of subsets of qubits / non-factorizable states** and **Hilbert-space dimension**. A tool that lets learners *see* when a subsystem has no ket (a reduced density matrix becoming mixed as CNOT entangles) targets a measured, unsolved difficulty. It also links to the superposition-vs-mixture confusion (Passante 2015).
- "Simultaneous" and "tries all answers" language should be avoided in the tool's own text. Interference-based framing (amplitudes cancel or reinforce, then measurement samples once) directly counters both.
- Effective designs pair a novel visual (e.g., DCN-like symmetry for separability) **with** the formal notation rather than replacing it. The 2025 critique of no-code tools and the Bley 2026 results both point this way.

### Gaps
- No PER studies were found on student understanding of **QEC, no-cloning, decoherence, Kraus channels or quantum speedup**. Teaching claims there are untested.
- The full QCCS distractor analysis (which wrong answers dominate) was not available in the fetched text.
- Background knowledge, not verified this session: Dür & Heusler's qubit-first Bloch-sphere approach is documented in *Phys. Teach.* 52, 489 (2014) and 54, 156 (2016) ([arXiv:1312.1463](https://arxiv.org/pdf/1312.1463)), but **no outcome study of it was found**. "QSR" as a named instrument or representation could not be located. The closest are the Qerimi et al. category system for visual representations (*EPJ QT* 12, 45, 2025; [arXiv:2409.17197](https://arxiv.org/pdf/2409.17197)) and Bley's DCN.

---

## Key Question 4: What design principles make interactive quantum simulations effective (QuVis, PhET, QuILT research), including visualization and accessibility?

### Takeaway
Across PhET, QuVis and QuILT research the consistent principles are:
- make invisible quantities visible
- couple learner actions directly to the representation
- reduce math load so attention goes to concepts, while still linking to the formalism
- build on documented student difficulties
- iterate with think-aloud observation and in-class trials
- embed sims in guided-inquiry activities (predict, test, reconcile) rather than free play alone

Newer representation research adds: pair visuals with Dirac notation, keep representation-switching manageable, and measure cognitive load and efficiency, not just correctness. Accessibility in quantum tools is essentially unaddressed. Use WCAG as the baseline.

### Cited Findings
- **PhET quantum sims** (McKagan et al., *Am. J. Phys.* 76, 406, 2008): visualize the unobservable, couple student actions directly to animations, connect to everyday life, do the calculations so students focus on concepts, and build on PER and educator feedback tested with interviews and classroom studies. — [arXiv:0709.4503](https://arxiv.org/abs/0709.4503)
- **QuVis**: research-based and iteratively refined from one-on-one observation sessions and in-class trials, with accompanying activities. HTML5 for tablets as well as desktops. — [QuVis about](https://www.st-andrews.ac.uk/physics/quvis/de/index-about.php); [Kohnle et al. 2015](https://arxiv.org/abs/1501.07905)
- **QuILTs**: built on documented difficulties and validated with interviews, then evaluated with pre/post tests (e.g., 56% to 91%). Distractors are seeded from known errors. — [DeVore & Singh 2020](https://link.aps.org/doi/10.1103/PhysRevPhysEducRes.16.010126); [Hu, Li & Singh](https://arxiv.org/pdf/2408.04859)
- **Representations**:
  - DCN plus Dirac side by side helps novices, but frequent switching reduces the benefit (Bley 2026). — [arXiv:2505.21508](https://arxiv.org/html/2505.21508v3)
  - The Bloch sphere improves task efficiency, though not post-test scores (Qerimi 2025). — [arXiv:2507.21721](https://arxiv.org/abs/2507.21721)
  - Qerimi et al. propose a category system judging representations on salience, cognitive load and misconception risk (*EPJ QT* 12, 45, 2025). — [arXiv:2409.17197](https://arxiv.org/pdf/2409.17197); [Resource Letter](https://arxiv.org/html/2606.06445v1)
  - Seskir et al. (2024) suggest emphasizing **qubit over spin** in public outreach. — [Resource Letter](https://arxiv.org/html/2606.06445v1)
- **No-code limitation**: no-code tools without a transition to formal math have limited effectiveness (2025; attribution uncertain, see KQ1). — [MDPI Educ. Sci. 15(9):1167](https://www.mdpi.com/2227-7102/15/9/1167)
- **Role framing and authenticity**: in Quantum Moves classes, assigning expert roles and doing "real research" raised motivation and perceived learning. — [arXiv:1511.01653](https://arxiv.org/abs/1511.01653v1)
- **AI hints**: LLM tips are comparable to expert tips, but beware "leading" hints and placebo effects. Design AI help to guide, not answer (ODU's tutor steers toward answers instead of supplying them). — [arXiv:2407.17024](https://arxiv.org/html/2407.17024); [ODU news](https://www.odu.edu/article/odus-new-ai-tutor-for-quantum-computing-empowers-students-to-find-the-answers-themselves)
- **Accessibility baseline (WCAG 2.2)**:
  - SC 1.1.1 Non-text Content: text alternatives for diagrams
  - SC 1.4.1 Use of Color: color must not be the only cue (relevant for phase-as-hue encodings)
  - SC 1.4.3: 4.5:1 text contrast
  - SC 1.4.11 Non-text Contrast: 3:1 for UI and graphical objects
  - SC 2.1.1 Keyboard operability
  - SC 2.2.2 Pause, Stop, Hide for moving content

  — [W3C WCAG 2.2](https://www.w3.org/TR/WCAG22/)
- **Color-blind-safe palette**: the Okabe–Ito palette is a standard reference. — [Okabe & Ito, Color Universal Design](https://jfly.uni-koeln.de/color/)
- **Quantum-specific accessibility**: no screen-reader quantum circuit tool was found. Classical-circuit accessibility research (TangibleCircuits: 3D-printed model plus audio, CHI 2020) shows that plain screen-reader output cannot convey circuit structure, and that tutorials are visually biased. — [Dartmouth TangibleCircuits news](https://web.cs.dartmouth.edu/news/2020/06/cs-research-brings-tech-tutorials-people-visual-impairments); [Soniq-Quirk](https://github.com/QuantumVillage/Soniq-Quirk)

### Inferences
- Concrete design checklist for the hackathon tool, synthesized from the above:
  1. Start each module with a **prediction prompt** on a known misconception (e.g., "after CNOT, does the control change?").
  2. Let learners manipulate, and show the Qiskit-computed result in **two linked representations** (visual and Dirac/matrix), highlighting correspondences.
  3. Use a **"reconcile" step** that names the misconception.
  4. Add **spaced-retrieval micro-prompts** (mnemonic-medium style) at the end and on return visits.
  5. Encode phase with **hue plus a non-color cue** (angle tick or pattern) using Okabe–Ito colors.
  6. Provide an **auto-generated text description** of each state (amplitudes, probabilities, "entangled / not entangled; reduced state purity = x"). This doubles as a screen-reader alternative and a novel accessibility contribution.
- Pyodide plus Qiskit can compute reduced density matrices and purity (`qiskit.quantum_info.partial_trace`, `DensityMatrix.purity`) live in the browser. That makes "is this subsystem describable by a ket?" a computable, visual, interactive check. This should be verified against the Qollab runtime.

### Gaps
- Full-text design-principle lists from Kohnle's QuVis papers (e.g., specific UI conventions) and PhET's "implicit scaffolding" papers were not retrieved; only the abstracts were.
- No empirical study was found on sonification or screen-reader access for quantum state visualizations.
- A claim by Modir, Thompson & Sayre (that many QM "difficulties" come from unproductive epistemological framing rather than misconceptions) surfaced in a search summary, but its primary source was not retrieved, so it is unverified.

---

## Key Question 5: How should a quantum-education tool be evaluated (concept inventories, pre/post design)?

### Takeaway
For quantum computing content, use items aligned with the **Quantum Computing Conceptual Survey (QCCS)**, the first broadly validated QC concept test (20 items, α = 0.83, 777 responses from 55 courses). Supplement with targeted items for topics QCCS excludes. Measure cognitive load and efficiency, and a delayed retention check, as recent representation studies do. QISCIT is a broader 31-item QIS inventory that has not yet been student-validated. The QCI (K-12) is earlier-stage. Older QM inventories (QMCS, QMVI) cover traditional QM, not QC.

### Cited Findings
- **QCCS** (Meyer, Griston, Passante, Pollock & Wilcox, arXiv Aug 2026):
  - 20 multiple-choice/multiple-select items (v2.2) on qubits, superposition, gates (CNOT, H, I, Pauli), entanglement, measurement, circuit diagrams, and math foundations (Dirac notation, complex numbers, inner products, tensor products, Hilbert-space dimension).
  - Excludes algorithms and communication.
  - 777 responses from 55 courses at 46 institutions.
  - α = ω = 0.83; Rasch person reliability 0.79; Ferguson's δ = 0.98; discrimination 0.26–0.51; good one-factor CFA fit; no gender DIF.
  - Recommended uses: pre/post evaluation of curricular change, cross-course comparison, and identifying persistent misconceptions, used only where course goals match.
  - PhysPort lists it with ~2,000 pilot students across versions.

  — [arXiv:2608.14459](https://arxiv.org/html/2608.14459v1); [PhysPort QCCS](https://www.physport.org/assessments/assessment.cfm?A=QCCS)
- **QISCIT** (Durkin et al.): 31 items covering states, measurement, qubits, entanglement, coherence and decoherence, gates and computing, and teleportation. Avoids advanced math and is usable down to high school. Developed with 11 experts via the assessment triangle. Published in *Am. J. Phys.* 94(8), 614 (2026). The Resource Letter notes it "has not been tested on students". — [arXiv:2506.17122](https://arxiv.org/abs/2506.17122); [AJP](https://pubs.aip.org/aapt/ajp/article/94/8/614/3399001/QISCIT-A-concept-inventory-assessment-for-quantum); [Resource Letter](https://arxiv.org/html/2606.06445v1)
- **Quantum Concept Inventory (QCI)**: a community-based, modular project under the EU Quantum Flagship, aimed at K-12 and at an earlier stage (Faletič et al. 2024). — [arXiv:2303.07055](https://arxiv.org/pdf/2303.07055); [Resource Letter](https://arxiv.org/html/2606.06445v1)
- **Feasibility of a "Quantum Computing Concept Inventory"** (8-expert interview study): jargon-free items accessible to students without QM study are hard to write and need international buy-in. Follows the Adams–Wieman procedure (expert consultation, draft items, think-aloud interviews, large-N testing). No quantum inventory has approached the Force Concept Inventory's impact. — [arXiv:2512.20836](https://arxiv.org/html/2512.20836)
- **Other instruments**: a quantum-measurement questionnaire across two-state contexts (Bitzenbauer et al., PRPER 20, 020136, 2024). Attitudes and interest surveys (Darienzo et al., PRPER 20, 020126, 2024; Kelly et al., *EPJ QT* 12, 11, 2025). — [Resource Letter](https://arxiv.org/html/2606.06445v1)
- **Process measures in recent representation studies**: cognitive load (intrinsic and extraneous), accuracy per time, eye-tracking, and 1–2-week delayed retention. — [Bley et al. arXiv:2505.21508](https://arxiv.org/html/2505.21508v3); [Qerimi et al. arXiv:2507.21721](https://arxiv.org/abs/2507.21721)
- **European Competence Framework for Quantum Technologies** (Greinert et al.; latest on Zenodo): maps QT skills and proficiency levels (2025 "proficiency triangle" and qualification profiles). Useful for stating learning objectives and target level. — [Zenodo record 15209861](https://zenodo.org/records/15209861); [Resource Letter](https://arxiv.org/html/2606.06445v1)
- **Caution on self-report**: game and misty-state studies rely on perceived learning, which is weaker evidence. A 2025 K-12 QC systematic review calls for more rigorous studies. — [Comp. Sci. Educ. 36(3), 2025](https://www.tandfonline.com/doi/full/10.1080/08993408.2025.2545915); [Seskir et al. 2022](https://arxiv.org/pdf/2202.07756)

### Inferences
- A practical evaluation plan for a 48-hour hackathon:
  1. Build a 5–8-item embedded pre/post quiz modeled on QCCS objectives and known distractors (subsystem state, separability, CNOT entangling, squared-amplitude probabilities, tensor dimension). Cite QCCS as the alignment target, without claiming QCCS-validated results.
  2. Log interaction traces: predictions made, first-try correctness, time on task.
  3. Include a confidence rating per item (multi-tier diagnosis).
  4. Offer an optional 1-week return prompt (spaced retrieval doubles as a retention measure).
  5. Document a future-study protocol (think-alouds, then classroom pre/post with the full QCCS from PhysPort). This strengthens "Documentation Quality" and "Impact Potential".
- Avoid claiming learning gains from tiny hackathon samples. Frame the pilot as usability and feasibility, as Quantum Odyssey and QuantAid did.

### Gaps
- QCCS item text and access terms (PhysPort typically gates assessments to verified educators) were not confirmed.
- Background knowledge, not verified this session:
  - **QMCS** (Quantum Mechanics Conceptual Survey; McKagan, Perkins & Wieman, PRSTPER 2010)
  - **QMVI** (Quantum Mechanics Visualization Instrument; Cataloglu & Robinett, AJP 2002)
  - **QMFPS** (Quantum Mechanics Formalism and Postulates Survey; Marshman & Singh)

  These target traditional QM (wavefunctions, potentials, formalism) and are poorly aligned with QC tools.
- Pre/post effect sizes for the 2024 QC-basics QuILT and the 2025 entanglement-QKD QuILT were not available in the fetched text.
