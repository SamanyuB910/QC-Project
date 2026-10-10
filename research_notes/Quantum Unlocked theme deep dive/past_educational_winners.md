# Past Winning and Notable Educational Quantum Projects at Hackathons and Challenges (2019-2026)

Research date: 2026-10-09. Scope: educational, teaching-tool, explainer, visualization and game projects at quantum hackathons and challenges from 2019 to 2026. It complements `research_notes/Qollab IonQ hackathon track/past_ionq_challenges_and_winners.md`, which covers IonQ iQuHACK tracks and the Qollab Creative Challenge (Quantum Garden, QAVE). Those items are only cross-referenced here.

**Label key:** **WINNER** means a placed prize (1st/2nd/3rd or a named category prize). **HM** means honorable mention or a special or minor award. **NOTABLE / unplaced** means the project was showcased or submitted but no placement was found. **FUNDED** means selected for a grant or cohort; that is not a competition win.

---

## Key Question 0 (Objective): Catalog of winning and notable educational quantum projects, 2019-2026

### Takeaway
Educational projects win outright mainly at **game-focused or creative-track events**: iQuHACK 2021 overall, the iQuHACK 2022 Microsoft/IonQ track, the QAIF Quantum Games Hackathons and the Qollab Creative Challenge. At **research-oriented Qiskit and QHack events** they usually get a side award such as "Best in Education" or an honorable mention, while 1st place goes to a research tool. QHack (2021-2024) has never run an education category, and no QHack education winner was found. Student hackathons on Devpost in 2024-2025 mostly gave prizes to application projects, and the generic "learn quantum" visualizers there did not place.

### Cited Findings

**2019**
- **Qiskit Camp Africa (Dec 11-12, 2019; Pilanesberg, South Africa; about 120 participants).**
  - **HM, "Best in Education": "Qat the Cat — an educational game."**
  - 1st place went to COBRA (symbolic commutator algebra for excited states), 2nd to an OpenPulse mock backend for spin qubits, and Community Choice to a Bayesian framework for Qiskit.
  - A QEC-themed entry, "Understanding the error correction function", is listed with no placement.
  - [Qiskit Medium recap, Jan 13, 2020](https://medium.com/qiskit/recap-2019-qiskit-camp-africa-d30020ea859d)
- **Quantum Game Jams (Finland, 2014-2019):** five events produced 68 prototypes. **Q|Cards**, an online card game teaching basic quantum-computing logic, began at a Quantum Game Jam and was then developed further with IBM — [arXiv 2408.09014 (via search snippet)](https://arxiv.org/html/2408.09014v1)

**2020**
- **Qiskit Hackathon Global (Oct 2020; 24 h, virtual, invite-only; 9 projects).** The winner was **QiskitFlow**, an experiment-tracking tool and not an educational project — [UKZN news](https://ukzn.ac.za/news/quantum-researcher-a-winner-at-qiskit-hackathon-global/). The educational entries Qiskit highlighted, none with a stated placement:
  - **Entangled States** (Nick Singstock, Spencer Moore, Elies Gil-Fuster), **NOTABLE / unplaced**. The team "noticed that ... games often falter when dealing with all of the amplitudes of a multi-qubit wavefunction". Its game shows all 2^n complex amplitudes as rods in space, and the player applies gates to reach a target n-qubit state. Built with Unreal Engine plus MicroQiskit (C++) so it could run on any device — [Qiskit Medium, Oct 23, 2020](https://medium.com/qiskit/these-amazing-quantum-computing-ideas-came-out-of-our-landmark-qiskit-hackathon-global-905a0063f8e5)
  - **OrQIStra**, **NOTABLE / unplaced**. Circuit to music and sheet music, aimed at "younger audiences". It applies H to every qubit, lets the user add gates, runs 1024 shots, and maps `get_counts()` probabilities to notes with conditional statements — [same](https://medium.com/qiskit/these-amazing-quantum-computing-ideas-came-out-of-our-landmark-qiskit-hackathon-global-905a0063f8e5)
  - Other entries: a "formalism to learn quantum chemistry more simply", and a Qiskit Pulse dephasing RNG behind a dad-joke Discord bot — [same](https://medium.com/qiskit/these-amazing-quantum-computing-ideas-came-out-of-our-landmark-qiskit-hackathon-global-905a0063f8e5)
- **Qiskit Community Summer Jam 2020 (Phase One, June 24-July 1).**
  - Regional winners: North Carolina, **"QuBayes: The Quantum Bayesian Circuit Builder for All"** (Quantum Ducks); New England, "Wavefunction Generation as Noise Evaluation"; Midwest, "Exploring Localization and Excited States with VQE"; California, "Quid Pro Quo" — [qiskit-summer-jam-20 repo](https://github.com/qiskit-community/qiskit-summer-jam-20)
  - A Qiskit blog snippet says one winning team "generated educational analogies between quantum circuits and quantum optics". Which team is not confirmed — [Qiskit Medium (via search snippet)](https://medium.com/qiskit/the-qiskit-community-summer-jam-brought-hackathon-energy-to-hundreds-at-home-a0f15c865bec)

**2021**
- **MIT iQuHACK 2021 (Jan 2021, remote).**
  - **Overall WINNER: QCB "Quantum Whack-A-Mole"**, an educational 2-qubit game for young students who build circuits that maximize amplitude.
  - **IonQ-track WINNER: Team 47 "Quantum Supremacy"**, where players are qubits, built to give "intuition for gate-model quantum computing, quantum entanglement, and measurement".
  - [iQuHACK 2021 README](https://github.com/iQuHACK/2021); [2021_QCB](https://github.com/iQuHACK/2021_QCB); [2021_Team-47](https://github.com/iQuHACK/2021_Team-47)
- **QAIF Quantum Games Hackathon 2021 (online; Quantum AI Foundation, Poland; winners announced Oct 3, 2021).**
  - 7 submissions, a 6-member jury, and four criteria: Correctness, Playability ("Does it have educational potential?"), Originality, Quality and completeness.
  - **WINNERS:**
    - **Dave the Hackerman** (Dodo Boys): "a game on diagrammatic ZX-calculus".
    - **QuanTetrum**: a Tetris-like game using superposition, entanglement and measurement.
    - **QG Crusher**: Candy-Crush-like, with quantum gates.
    - **Quaze**: a quantum maze in which "each maze tile is a gate changing the state of a quantum particle".
  - Quantum Flytrap funded an extra prize for the best JavaScript game. The paper does not say which game won it.
  - [Seskir et al., "Quantum Games and Interactive Tools for Quantum Technologies Outreach and Education," arXiv 2202.07756 (2022)](https://arxiv.org/abs/2202.07756)
- **Qiskit Fall Fest 2021, CIC-IPN Latin American hackathon (Oct 2021, in Spanish).** 29 hackers and 8 submitted projects.
  - 1st: Threerra (a Qiskit Pulse qutrit module). 2nd: quantum radio resource scheduling. 3rd: VQC on a protein-network graph.
  - **Separate "Best Education Hack" prize** (from Quantum Universal Education): **"Quantum classifier for medical data"**, which "propose[s] an introduction to quantum machine learning using a variational quantum algorithm for classification, applying it to two medical datasets".
  - Judging used four equal-weight criteria: Technical Challenge, Impact ("e.g. industrial application, educational value"), Creativity ("go beyond the scope of a typical hackathon project ... artistic, originality, user friendliness"), and Presentation ("thoughtfully explained and easy to understand").
  - [Maldonado-Romo & Yeh, arXiv 2302.12119 (Feb 2023)](https://arxiv.org/abs/2302.12119)
- **Qiskit Hackathon Korea 2021 (Feb 18-19, 2021; KAIST, SKKU, IBM):** criteria were Originality and Uniqueness 25%, Usefulness and Complexity 25%, **Quantum Community Benefit 25%**, Digital Presentation 25%. Winners were not found — [HackerEarth rules (via search snippet)](https://hackerearth.com/challenges/hackathon/qiskit-hackathon-korea/rules)
- **QHack 2021 (Xanadu, QML theme):** the winners were research projects (Notorious F.U.B., trainable quantum embedding kernels). There was no education category — [FU Berlin](https://physik.fu-berlin.de/en/einrichtungen/ag/ag-eisert/news/QHack.html); [PennyLane blog](https://pennylane.ai/blog/2021/03/qhack-the-quantum-machine-learning-hackathon/)

**2022**
- **MIT iQuHACK 2022 (Jan 28-30), Microsoft/IonQ "build a game" track.**
  - **Division WINNER: Opti-maze**, a game teaching QAOA with compete and cooperate modes, framed around CO2 and climate policy.
  - **2nd-place group:**
    - **Wyn**: "Learn quantum computing by battling with your quantum circuits."
    - Qic Qac Qoe: quantum tic-tac-toe.
    - Soulinq: platformer with entangled souls.
    - QuHackJack Casinos.
  - **Creativity award: QuanTris** (quantum Tetris). MIT News says the team aimed to teach quantum concepts through play.
  - The event had 400 participants, 75 projects and 57 countries.
  - [iQuHACK 2022 page](https://www.iquise.mit.edu/iquhack/2022-01-28); [IonQ blog](https://www.ionq.com/blog/february-09-2022-iquhack-winners-opti-maze); [MIT News, Apr 2022](https://news.mit.edu/2022/bringing-together-next-generation-quantum-coders-0405)
  - Microsoft's recap (as quoted in a search snippet) says entries "ranged from quantum-inspired variants of card games and Tetris to educational games on topics such as universal gate sets or state tomography" — [Microsoft Q# blog (via search snippet; page now redirects)](https://devblogs.microsoft.com/qsharp/?p=1707)
- **Qiskit Hackathon Korea 2022 (Feb 7-10, 2022).**
  - **1st place: "Q-urling (Quantum Curling)"**, a game.
  - **Honorary Mention: "Implement the algorithm for the hidden shift problem and explain it!"**, an algorithm explainer.
  - The other placements went to QML and QITE research projects.
  - [qiskit-hackathon-korea-22 README](https://github.com/qiskit-community/qiskit-hackathon-korea-22)
- **QAIF Quantum Games Hackathon 2022:** 1st **Verona-2049** (Quantum Lovers), 2nd **QodeUnlocked** (Quantum Potatoes), 3rd plus a special prize **SNAQE**, a quantum snake game (HackerGuys2000). Same four criteria as 2021 — [QAIF 2022 page](https://www.qaif.org/contests/quantum-games-hackathon-2022)
- **Q-munity Hack-Q-Thon 2022 (May 2022): Hacktopia, WINNER (3rd place).** A terminal-based game in which you "defeat a mad scientist by learning about quantum computing and solving pop quizzes", plus an ML recommender. The team admits "This is a terminal-based game so it could have been better." — [Devpost](https://devpost.com/software/hacktopia)
- **QHack 2022 (Feb 14-25):** none of the Open Hackathon categories covered education or games ("Quantum Games" existed only as a coding-challenge set). The IBM Qiskit Challenge 2nd place was "simulating anyons in the toric code model", a research project on a QEC topic — [PennyLane QHack 2022 post](https://pennylane.ai/blog/2022/03/qhack-2022-the-one-of-a-kind-celebration-of-quantum-computing/)
- **Qiskit Hackathon Melbourne (July 4-7, 2022):** 1st place turned Qiskit circuits into music videos. "A Visual Representation of Quantum Noise" built a quantum wheel of fortune driven by IBM device noise (placement unclear). A Minecraft-style circuit escape room ran as a social challenge — [quantum-melbourne repo (via search snippet)](https://github.com/quantum-melbourne/qiskit-hackathon-22)

**2023**
- **QHack 2023 Visualization/Plotting Challenge**, the closest QHack has come to an education category:
  - **1st Qualition**, "Quantum Image Processing – embeddings – from visualization to classification".
  - **2nd QSpace**, "Quantum Tubes".
  - **3rd Incho**, "qXR (Quantum & Mixed Reality)".
  - "LearnQPE" (1st, QEC and Compilation) is about *variational learning* of QPE, not pedagogy.
  - [PennyLane QHack 2023 highlights](https://pennylane.ai/blog/2023/04/qhack-2023-highlights)
- **MIT iQuHACK 2023, IonQ in-person 1st: Entanglement5 "Game of Finches"**, an interactive evolution model run on IonQ Harmony that uses all-to-all connectivity. Covered in the prior notes — [UMass CICS](https://www.cics.umass.edu/news/cics-student-wins-iquhack-2023)
- **QAIF Quantum Games Hackathon 2023 (Sept 30-Oct 8, 2023).** The jury included Piotr Migdał (Quantum Flytrap) and Paweł Gora. All entries are MIT-licensed.
  - **1st: Superposition Arcade** (Rory Soiffer; 15,000 PLN). A Unity puzzle in which each row of pegs is a quantum gate, so placing pegs builds a circuit that routes falling balls.
    - It runs on a **custom simulator with unitary gates plus measurement and noise**.
    - The README says the levels are "based on quantum circuit identities" and on finding small circuits for real problems.
  - **2nd: Schrödinger's Mice** (Obada Alabbadi). **3rd: Out of the Box** (Agata Gołębiowska). Special prizes: **Quantum Hashi** (dotQ) and **QuantaVania**.
  - [QAIF 2023 winners](https://www.qaif.org/contests/quantum-games-hackathon-2023-winners); [QAIF contest page](https://www.qaif.org/contests/quantum-games-hackathon); [SuperpositionArcade README](https://github.com/rsoiffer/SuperpositionArcade)
- **Quantum Game Jam 2023 (itch.io, Sept 15-17, 2023):** 36 entries, including educational-tagged platformers. Winners are not published on the jam page — [itch.io jam (via search snippet)](https://itch.io/jam/quantum-game-jam-2023)

**2024**
- **MIT iQuHACK 2024, IonQ "What if __ is Quantum" story challenge:** 1st fATCAT (story driven by a trapped-ion-style long-range Ising simulation), 2nd FalQon (professional networking). Covered in the prior notes — [iQuHACK 2024 page](https://www.iquise.mit.edu/iquhack/2024-02-02)
- **QHack 2024:** five Open Hackathon categories (amplitude embedding, spectral gap, qubit reduction, Hamiltonian evolution, phase transitions). All winners were research or algorithm projects, with no education or visualization category — [PennyLane QHack 2024 highlights](https://pennylane.ai/blog/2024/03/qhack-2024-highlights/)
- **Luna Vista ADC Q-Dev Hackathon 2024: "Quant PlayGround", WINNER of "Best Quantum Project".** A Streamlit + Qiskit app with a coin flip (H gate), a teleportation demo, a Bloch sphere and a Bell state, i.e. standard tutorial content. It was also submitted to the 2024 QC @ CMU Qiskit Fall Fest — [Devpost](https://devpost.com/software/quantx)
- **WQCC x IBM Qiskit Fall Fest 2024 (Wisconsin):** the public gallery has only 4 projects, including an Ekert91 distillation technique, a T1/T2 analysis tool, and "Quantum Battleships Godot WIP", described as "a game I made in Godot that doesnt work" — [WQCC Devpost gallery](https://wqcc.devpost.com/project-gallery)

**2025**
- **ITU AI for Good "Future Leaders in Quantum" (FLIQ) hackathon (May 16-20, 2025), Education track.** The track asks teams to make quantum concepts accessible through tutorials, visualizations and interactive tools.
  - Challenge "Implementing quantum experiments" (IBM + Quant A&M): **WINNER Team Vivek** (Vivek Pal and Mukul Kumar).
  - Challenge "Implementing quantum algorithms" (UPenn + IBM): **WINNER Team Qryptonian** (Dev Verma), who **also won the Education Track overall**. The success measure was "how well you learn—and how effectively you teach."
  - A linked track presentation is titled "From repetition codes to Surface-17: a gentle introduction to quantum error correction."
  - The winning projects themselves are not described.
  - [AI for Good FLIQ page](https://aiforgood.itu.int/the-future-leaders-in-quantum-hackathon/)
- **CQhack25 (Devpost student hackathon with a Classiq track; 74 submissions).**
  - The **six WINNERS were all application projects**: Quantum Route Optimizer (VRP), Q-Cure (drug interactions), Finbubu (finance), medical image QCNN, **EntangleMe** (a chat app "that actually uses quantum teleportation"), and Q-MediScan.
  - Educational submissions that **did not place**:
    - **"Quantum Error Correction (QEC) educational visualizer"**: a solo Streamlit app covering the 3-qubit, 5-qubit and Steane codes and a distance-3 surface code, with "neural network decoders", a "mock Classiq integration", a self-declared "No bugs", and a "🏅 Why This Wins" section.
    - "Quantum Search Visualizer" (classical vs. quantum maze race).
    - "QvC: Quantum vs Classical".
    - "QLogic" visual gate simulator.
  - [CQhack25 gallery](https://cqhack25.devpost.com/project-gallery); [QEC visualizer Devpost](https://devpost.com/software/quantum-error-correction-qec-educational-visualizer)
- **Bitcamp 2025 (a general hackathon): "Schrödinger's Catch"**, a VR fishing game using Qiskit only for "quantum randomness" on fish bites. It won "Hack That Made You Smile", a fun award with no educational depth — [Devpost](https://devpost.com/software/schrodingers-catch-trout-of-this-world)
- **Quantum Arcade Game Jam (Oct 20-Dec 20, 2025; grades 6-12 with mentors; UBC Geering Up, ICTC, KnowledgeFlow):** 22 entries, and top entries get a permanent place in the "Quantum Arcade". Winners are not listed — [itch.io (via search snippet)](https://itch.io/jam/quantum-arcade-game-jam)
- **Qollab Creative Challenge (Fall/Winter 2025): QAVE, WINNER.** A synchronized replay of state vector, density matrix and gates that "makes quantum errors and their corrections directly observable". Covered in the prior notes — [QAVE showcase](https://qollab.xyz/explore/qave)

**2026**
- **unitaryDESIGN "Quantum Design Hackathon" (Feb 20, 2026; Microsoft Garage).** Presented by Harmoniqs and the Unitary Foundation with J.P. Morgan support. The prompt was "how can we communicate the quantum world?" Teams prototyped a way to communicate one qubit modality to a broad audience. 9 teams; **no winners published**. Projects:
  - **"Entangled: The Game of Surface Code"**: a board game in which players initialize qubit patches, reshape them, and measure across edges to form logical qubits, i.e. lattice surgery.
  - **"The Qubitarium of Trapped Ions"**: a live six-act audience-participation performance.
  - **CAT qubit visualization** (noise-biased bosonic qubits).
  - **The Rydberg Room** (neutral atoms).
  - **QLight!** (photonic circuit demo with a NOISE gate).
  - **Silicon Pulse** (silicon spin qubits, 3D crystal view, hand-motion gate games).
  - **PHOTON & Quantum Rescue**.
  - [Event home](https://quantum-design-hackathon.github.io/); [Teams page](https://quantum-design-hackathon.github.io/groups.html)
- **Qollab Spring 2026 cohort (FUNDED, not winners):**
  - **GraFT**: 3D graphs of how one logical gate expands into thousands of fault-tolerant operations (magic-state distillation, syndrome extraction), built on the rmsynth library.
  - **QCFlows**: basis-dependent views of correlations, letting users "move between measurement views".
  - **qOrbital**: VQE/UCCSD orbitals with Copenhagen and Bohmian views, on IonQ hardware with a simulator fallback.
  - **Quantum Butterfly Field**: real scrambling circuits; "doubles as a teaching artifact".
  - **Quantum Market Game**: entanglement as correlation, for high-school classrooms.
  - **QuantumCanvas** (Georgia Tech, Shivani Mayekar): a drag-and-drop sandbox "for the post-tutorial 'now what'".
  - [Qollab Spring 2026 cohort](https://qollab.xyz/explore/spring-2026-cohort)
- **AWS Kiro x CS Careers Hackathon at Virginia Tech (Mar 2026; a general hackathon): "QuantumBridge", WINNER 1st Overall.**
  - An AI-personalized quantum-learning knowledge graph: explanations are reframed for the learner's field (for example "a music student learns superposition through harmonics").
  - Each node runs circuits on Amazon Braket's LocalSimulator, with 3D Bloch spheres, interference animations, AI-generated video (Nova Reel) and quizzes.
  - It has two modes, a structured "Pipeline" curriculum and a free "Explore" mode.
  - [Devpost](https://devpost.com/software/quantum-bridge)
- **Qiskit Fall Fest 2026: "Learning to Decode: a Neural QEC Decoder Game"** ("Gamifying Error Detection, Mitigation and Correction"). In progress; placement unknown — [GitHub (via search snippet)](https://github.com/EDHE08232001/NeuralDecoderGame)
- **MIT iQuHACK 2026, IonQ entanglement-distillation network game:** a competition, not an explainer. Winners BYU Q-gars and iQuackers, covered in the prior notes — [2026-IonQ repo](https://github.com/iQuHACK/2026-IonQ)

### Inferences
- **Venue determines the outcome.** At game-focused venues (QAIF, iQuHACK game/story tracks, Qollab Creative) an educational game or visualizer can take 1st overall. At research-heavy Qiskit and QHack events it tends to land in a separate "Best Education" or honorable-mention slot (Camp Africa 2019, CIC-IPN 2021, Korea 2022 honorary mention). Qollab's "Quantum Unlocked" is closer to the first group because it is a dedicated theme with its own "Best of theme" award.
- The most technically serious educational winners all **simulate real multi-qubit quantum mechanics**, not a Bloch sphere: Superposition Arcade (custom simulator with measurement and noise), Entangled States (all 2^n amplitudes), QAVE (state vector plus density matrix replay of errors and corrections), Opti-maze (real QAOA), and Dave the Hackerman (ZX rewriting).
- At low-bar, mostly undergraduate Devpost events, tutorial-level apps sometimes win (Quant PlayGround, Hacktopia 3rd). At larger student quantum hackathons (CQhack25) they lose to application projects. Neither pattern clears Qollab's "beyond the tutorial bar".

### Gaps
- The Medium pages for Qiskit Fall Fest 2022-2025 global recaps are not accessible, and IBM did not publish a central list of Fall Fest winners. Per-school results (Purdue, UW-Madison, CMU, IISc) are mostly unpublished. The CMU 2024 gallery was "not published yet".
- Final 2021 Korea winners, the Qiskit Hackathon Europe 2021 winners (the ICFO page was truncated), and Qiskit Global Summer School projects were not found. Global Summer School is a lecture and lab format with no project competition that I could find.
- I found no education-category winners for **unitaryHACK** (bounty-based, so it has no projects to "win"), **QOSF** (a mentorship program), **Womanium** (prizes were scholarships and fellowships, and the found winners were chemistry or social-good projects), **Classiq** competitions, **Q-CTRL** (its QCHack 2021 challenge was pulse design), **Quantinuum/Microsoft** QCHack tracks (Grover's or image processing), or IQC/Perimeter hackathons.
- **Unitary Fund microgrants for education:** only one is confirmed, BraKetVue (Quantum Flytrap's matrix visualizer) — [arXiv 2203.13300 (via search snippet)](https://arxiv.org/pdf/2203.13300). The grants page lists no individual recipients — [Unitary Foundation grants](https://unitary.foundation/grants/)
- No public description was found for Qat the Cat, Q-urling, Wyn, Verona-2049, Schrödinger's Mice, or the FLIQ 2025 education winners' projects.

---

## Key Question 1: Which hard topics have winning educational projects taught, and which have never been done well?

### Takeaway
Winners overwhelmingly teach **circuit-model basics**: gates as moves, superposition, entanglement as correlation, measurement. A smaller set covers **one named algorithm** (QAOA in Opti-maze, hidden shift in an HM, QML intro in Best Education Hack 2021) or a **formalism** (ZX-calculus in Dave the Hackerman). Every topic the Qollab "Quantum Unlocked" theme lists has almost no deep, *winning* interactive explainer: QEC/fault tolerance, networking/distillation, and how algorithms actually achieve speedups. Trapped-ion physics specifically appears only in one unjudged theatre piece.

### Cited Findings
**Topics taught by winners and placed entries**
- Gate and circuit intuition, and amplitude maximization: QCB Whack-A-Mole (iQuHACK 2021 overall winner) and Team 47 (IonQ 2021) — [iQuHACK 2021](https://github.com/iQuHACK/2021)
- Circuit identities and gate behavior: Superposition Arcade (QAIF 2023, 1st) — [README](https://github.com/rsoiffer/SuperpositionArcade)
- Superposition, entanglement and measurement inside game mechanics: QuanTetrum; QG Crusher; Quaze (a gate per maze tile) (QAIF 2021) — [arXiv 2202.07756](https://arxiv.org/abs/2202.07756)
- **ZX-calculus** (diagrammatic rewriting): Dave the Hackerman (QAIF 2021 winner) — [arXiv 2202.07756](https://arxiv.org/abs/2202.07756)
- **QAOA and combinatorial optimization**: Opti-maze (iQuHACK 2022 winner) — [IonQ blog](https://www.ionq.com/blog/february-09-2022-iquhack-winners-opti-maze)
- **Hidden shift algorithm** explained: Korea 2022 Honorary Mention — [repo](https://github.com/qiskit-community/qiskit-hackathon-korea-22)
- **Intro to QML / variational classifiers**: CIC-IPN 2021 Best Education Hack — [arXiv 2302.12119](https://arxiv.org/abs/2302.12119)
- **Quantum algorithms tutorials, and QEC from repetition codes to Surface-17** (as a track resource): FLIQ 2025 Education track — [AI for Good](https://aiforgood.itu.int/the-future-leaders-in-quantum-hackathon/)
- **Error dynamics and correction made observable** (state vector and density matrix replay, 5-qubit GHZ): QAVE (Qollab winner) — [QAVE](https://qollab.xyz/explore/qave)

**Hard topics attempted but unplaced, unjudged, or only funded**
- **Multi-qubit amplitude structure** (beyond the Bloch sphere): Entangled States (2020) — [Qiskit Medium](https://medium.com/qiskit/these-amazing-quantum-computing-ideas-came-out-of-our-landmark-qiskit-hackathon-global-905a0063f8e5)
- **Surface code and lattice surgery**: "Entangled" board game, unitaryDESIGN 2026, no winners published — [groups page](https://quantum-design-hackathon.github.io/groups.html)
- **QEC codes and decoders**: CQhack25 QEC visualizer (unplaced) — [Devpost](https://devpost.com/software/quantum-error-correction-qec-educational-visualizer); Neural QEC Decoder Game (Fall Fest 2026, in progress) — [GitHub (via search snippet)](https://github.com/EDHE08232001/NeuralDecoderGame); "Understanding the error correction function" (Camp Africa 2019, unplaced) — [Qiskit Medium](https://medium.com/qiskit/recap-2019-qiskit-camp-africa-d30020ea859d)
- **Fault-tolerant compilation overhead** (magic states, syndrome extraction): GraFT, funded Qollab cohort — [Qollab cohort](https://qollab.xyz/explore/spring-2026-cohort)
- **Measurement-basis dependence of correlations**: QCFlows (funded) — [same](https://qollab.xyz/explore/spring-2026-cohort)
- **Scrambling / the "no-butterfly effect"**: Quantum Butterfly Field (funded) — [same](https://qollab.xyz/explore/spring-2026-cohort)
- **Universal gate sets and state tomography** educational games (iQuHACK 2022 entries; placement not stated) — [Microsoft Q# blog (via search snippet)](https://devblogs.microsoft.com/qsharp/?p=1707)
- **Device noise visualized** ("quantum wheel of fortune"): Melbourne 2022 (placement unclear) — [repo (via search snippet)](https://github.com/quantum-melbourne/qiskit-hackathon-22)
- **Quantum networking / entanglement distillation**: at IonQ's iQuHACK 2026 this was a *competitive* game, not a teaching tool — [2026-IonQ](https://github.com/iQuHACK/2026-IonQ). Teleportation appears only as an application gimmick (EntangleMe chat app, CQhack25 winner) — [CQhack25 gallery](https://cqhack25.devpost.com/project-gallery)

**Known pedagogical blind spot**
- The Seskir et al. review warns that quantum mechanics "is known to be prone to misconceptions". It cites Aaronson's "Minus-Sign Test": popularizations that say a qubit is "0 and 1 simultaneously" fail to distinguish statistical uncertainty from interference, i.e. they omit **phase** — [arXiv 2202.07756](https://arxiv.org/abs/2202.07756)

### Inferences
- **Topics with no deep winning interactive explainer found (2019-2026):**
  - QEC thresholds and decoding as a *live, runnable* experience (noise sweep, logical vs. physical error rate).
  - Fault-tolerance overhead and magic-state distillation (only GraFT, which is funded and unjudged).
  - Entanglement distillation and repeaters for networking.
  - Phase kickback and interference as the mechanism of speedup (QPE, Shor, amplitude amplification geometry).
  - Hamiltonian simulation and Trotter error.
  - Measurement-based computation.
  - Trapped-ion gate physics (Mølmer–Sørensen gate, motional modes).
  - These are the topics Qollab names for "Quantum Unlocked" (QEC, fault tolerance, networking, algorithms), so the theme is aimed at real white space.
- Many games mention "entanglement" but model it only as correlated randomness. A project that makes **phase and interference** visible and manipulable (passing the "Minus-Sign Test") would stand apart from about a decade of hackathon games.

### Gaps
- The content and quality of the FLIQ 2025 education winners, and of the hidden-shift HM, are unknown.
- No judges' scoring sheets show *why* topic depth mattered in specific decisions.

---

## Key Question 2: What formats win, and with what technical depth?

### Takeaway
**Games are the most common winning educational format by count**: iQuHACK 2021 and 2022, QAIF 2021-2023, Korea 2022 Q-urling. **Interactive visualizers with synchronized multiple views** win at creative/education-focused calls (QAVE at Qollab; the QHack 2023 visualization challenge). **Plain notebooks** win only as "Best Education Hack"-type side prizes. **Narrative/theatre** formats appear but are unjudged or only win at IonQ's story track (fATCAT/FalQon, already covered). Winners pair the format with a real simulation core: a custom simulator with measurement and noise, real QAOA, ZX rewriting, or a state-vector/density-matrix replay. Thin wrappers around `get_counts()` do not win.

### Cited Findings
- **Game winners and their technical core:**
  - Superposition Arcade: Unity, a custom simulator with unitary gates plus non-unitary measurement and noise, levels from circuit identities — [README](https://github.com/rsoiffer/SuperpositionArcade)
  - Opti-maze: QAOA via Qiskit on Azure with an IonQ backend, two gameplay modes — [IonQ blog](https://www.ionq.com/blog/february-09-2022-iquhack-winners-opti-maze)
  - Team 47: players apply rotating or entangling gates and receive non-projective measurement glimpses — [2021_Team-47](https://github.com/iQuHACK/2021_Team-47)
- **Interactive-visualizer winners:**
  - QAVE "computes the quantum state at every gate operation, synchronizes multiple views into a single coherent replay", delivered as a short runnable notebook — [QAVE](https://qollab.xyz/explore/qave)
  - QHack 2023 visualization challenge: an image-embedding visualization pipeline (1st) and a mixed-reality "qXR" (3rd) — [PennyLane](https://pennylane.ai/blog/2023/04/qhack-2023-highlights)
- **Notebook winner:** an intro-to-QML classifier on medical datasets (CIC-IPN Best Education Hack) — [arXiv 2302.12119](https://arxiv.org/abs/2302.12119)
- **AI-tutor format:** QuantumBridge, 1st overall at a *general* hackathon in 2026: React Flow knowledge graph, Braket LocalSimulator circuits per concept node, Bloch spheres, interference animations, AI video and quizzes, plus learner-background personalization — [Devpost](https://devpost.com/software/quantum-bridge)
- **Physical and performance formats** (board game, theatre, art) at unitaryDESIGN 2026, with no winners published — [groups page](https://quantum-design-hackathon.github.io/groups.html)
- **Low-depth formats that still won at small events:** Quant PlayGround (Streamlit tutorial collection, "Best Quantum Project" at Luna Vista ADC Q-Dev 2024) — [Devpost](https://devpost.com/software/quantx); Hacktopia (terminal quiz game, 3rd at Hack-Q-Thon 2022) — [Devpost](https://devpost.com/software/hacktopia)
- **How often game-jam entries actually simulate quantum physics:** of 23 games from 2020-2021 jams, only 5 stated they used a numerical simulation, 3 had an unclear quantum connection, and the rest were mostly thematic. Only one had "clear educational aspects". In the 2021-2022 Global QGJ, Qiskit was used in most games with a quantum-technologies dimension — [Piispanen et al., arXiv 2408.09025 (2024)](https://arxiv.org/html/2408.09025v1)
- **Evidence that games can teach:** a two-afternoon intervention in a Treviso high school using Quantum TiqTaqToe showed "a high degree of effectiveness" on state, measurement, superposition and entanglement in designed questionnaires — [arXiv 2202.07756](https://arxiv.org/abs/2202.07756)

### Inferences
- For Qollab "Quantum Unlocked", the strongest pattern-match is a **QAVE-style synchronized multi-view interactive visualizer** with a game-like goal or challenge layer, backed by a **real Qiskit simulation** (density matrices, noise models, syndrome extraction) that judges can press "Run" on. Pure games risk the thematic-only trap; pure notebooks risk reading as "just a tutorial".
- A personalization layer (as in QuantumBridge) won a general hackathon, but quantum-expert judges are likely to weigh quantum depth more heavily than AI features (an inference; no direct source).

### Gaps
- There are no head-to-head data (scores) comparing formats within a single quantum event.
- The judging rationale behind QAIF's ranking of Superposition Arcade over the other games is not published.

---

## Key Question 3: What do judges, organizers, or winners say about why educational projects won or lost?

### Takeaway
Published rubrics consistently reward four things: **correctness of the quantum content**, **educational/community value** (often an explicit criterion), **creativity beyond a typical project**, and **clear presentation**. Organizer retrospectives add that the best educational games come from **teams that combine physics and game-design expertise** and from experienced, repeat teams. Explicit win/loss rationales for specific projects are almost never published.

### Cited Findings
- **QAIF Quantum Games Hackathon criteria (2021-2023):**
  - "Correctness: Are the assumptions and usage of quantum mechanics and quantum computing appropriate?"
  - "Playability: Is the game entertaining? Does it have educational potential? Is the user interface inviting?"
  - "Originality".
  - "Quality and completeness: Is the game polished and ready to play? Are the mechanics well introduced?"
  - [arXiv 2202.07756](https://arxiv.org/abs/2202.07756); [QAIF 2023](https://www.qaif.org/contests/quantum-games-hackathon-2023-winners)
- **Qiskit Fall Fest CIC-IPN 2021 criteria (equal weight):** Technical Challenge; Impact (includes "educational value"); Creativity ("Does the project go beyond the scope of a typical hackathon project? ... artistic, originality, user friendliness"); Presentation ("Is the project functioning and thorough? ... thoughtfully explained and easy to understand?") — [arXiv 2302.12119](https://arxiv.org/abs/2302.12119)
- **Qiskit Hackathon Korea 2021:** "Quantum Community Benefit" was worth 25% — [HackerEarth (via search snippet)](https://hackerearth.com/challenges/hackathon/qiskit-hackathon-korea/rules)
- **iQuHACK 2022:** "Utility of Concept" explicitly "could also include educational utility" (20%), alongside Technical Merit, Creativity, Relevance and Communication. Cited in the prior notes — [iQuHACK 2022 rubric doc](https://docs.google.com/document/d/e/2PACX-1vR5PVoInN_Fi42lIOchhblgGBPblgNyouj1XHukonZ4sdqY-p5ulS9TxdzvddEcDNFc5k_6teFyKzXv/pub)
- **FLIQ 2025 Education:** success is measured by "how well you learn—and how effectively you teach" — [AI for Good](https://aiforgood.itu.int/the-future-leaders-in-quantum-hackathon/)
- **IonQ 2025 iQuHACK** judged on the "educational clarity of your explanations". IonQ's 2024 story prompt required quantum to serve "a purpose beyond acting as a mere random number generator". Cited in the prior notes — [IonQuHack2025.ipynb](https://github.com/iQuHACK/2025-IonQ/blob/main/IonQuHack2025.ipynb); [2024_IonQ](https://github.com/iQuHACK/2024_IonQ)
- **A winner-side design rationale:** the Entangled States team built their game because existing games "falter when dealing with all of the amplitudes of a multi-qubit wavefunction" — [Qiskit Medium](https://medium.com/qiskit/these-amazing-quantum-computing-ideas-came-out-of-our-landmark-qiskit-hackathon-global-905a0063f8e5)
- **Organizer retrospective (Quantum Game Jams):**
  - Meaningful quantum games "typically required expertise in both quantum physics and game design".
  - Experienced, repeat teams produced the most successful prototypes.
  - Participants without physics backgrounds struggled to find a starting point.
  - Few gained substantial physics knowledge beyond thematic ideas.
  - Recommendation: provide example projects that use Qiskit or numerical simulation.
  - [arXiv 2408.09025](https://arxiv.org/html/2408.09025v1)
- **Review authors (Seskir et al.):** "The wide range of games and tools ... cannot be evaluated from a comparative point of view due to the lack of comprehensive assessment tools", and the purpose of a game should be "made explicit" through storytelling — [arXiv 2202.07756](https://arxiv.org/abs/2202.07756)
- **Organizer intent at iQuHACK 2022:** the chair wanted "people to learn first-hand that coding on quantum computers is not as hard as it sounds" — [MIT News](https://news.mit.edu/2022/bringing-together-next-generation-quantum-coders-0405)
- **Qollab's own description of its winning educational project** emphasizes making "quantum errors and their corrections directly observable" with synchronized views — [QAVE](https://qollab.xyz/explore/qave)

### Inferences
- Mapped to Qollab's four traits:
  - Correctness and depth become **Technical Execution**.
  - "Educational potential", "community benefit" and "how effectively you teach" become **Impact Potential**.
  - "Beyond a typical project" becomes **Novelty** plus the beyond-the-tutorial gate.
  - "Mechanics well introduced" and "easy to understand" become **Documentation Quality**.
- Educational entries likely lose when judges see standard tutorial content, which scores low on Novelty and Technical. They also lose when the quantum content is incorrect or merely thematic, which fails Correctness.
- Showing evidence of learning would differentiate an entry, since reviewers flag assessment as the field's gap. Examples: a short pre/post quiz, a "predict then run" loop, or a user test with a few classmates.

### Gaps
- No judge commentary was found for any specific educational winner (Qat the Cat, QCB, Superposition Arcade, Opti-maze, QAVE, FLIQ winners).
- There is no blog post by a winner explaining an educational win at QHack or a Qiskit event.

---

## Key Question 4: What are recurring weaknesses of educational entries?

### Takeaway
The recurring failure modes are:
1. **RNG-only quantum**: `H` then measure, used as dice.
2. **Tutorial re-skins**: coin flip, Bell state, teleportation, Bloch sphere.
3. **Single-qubit / Bloch-sphere-only** views that hide multi-qubit amplitudes and phase.
4. **Thematic-only quantum**, where the quantum label carries no mechanics.
5. **Incomplete or broken builds**.
6. **Over-claiming**: "industry-standard", "no bugs", "mock" SDK integrations, AI-boilerplate READMEs.
7. **No evidence that anyone learned anything**.

### Cited Findings
- **RNG-only:**
  - Schrödinger's Catch uses Qiskit only to make a fish bite "quantum-powered" random — [Devpost](https://devpost.com/software/schrodingers-catch-trout-of-this-world)
  - The Qiskit Hackathon Global dad-joke bot is an RNG — [Qiskit Medium](https://medium.com/qiskit/these-amazing-quantum-computing-ideas-came-out-of-our-landmark-qiskit-hackathon-global-905a0063f8e5)
  - OrQIStra maps H-on-all-qubits counts to notes via "conditional statements" — [same](https://medium.com/qiskit/these-amazing-quantum-computing-ideas-came-out-of-our-landmark-qiskit-hackathon-global-905a0063f8e5)
  - IonQ explicitly penalizes this ("beyond randomness") — [2024_IonQ](https://github.com/iQuHACK/2024_IonQ)
  - Qollab's Playground theme requires quantum to be essential, "beyond simply generating randomness" — [Qollab rules](https://qollab.xyz/programs/hackathon/terms)
- **Tutorial re-skin:** Quant PlayGround offers a coin flip, teleportation, a Bloch sphere and a Bell state — [Devpost](https://devpost.com/software/quantx). This is exactly the content Qollab's "beyond the tutorial bar" can score at 0 on Novelty and Technical — [Qollab rules](https://qollab.xyz/programs/hackathon/terms)
- **Bloch-sphere-only:**
  - The Entangled States team's critique of games that cannot show multi-qubit amplitudes — [Qiskit Medium](https://medium.com/qiskit/these-amazing-quantum-computing-ideas-came-out-of-our-landmark-qiskit-hackathon-global-905a0063f8e5)
  - Devpost has "BlochSphere.space", described by its maker as "a one shot prompt generated interactive 3D bloch sphere visualizer" — [Devpost search](https://devpost.com/software/search?query=quantum%20education%20visualizer)
  - The "Minus-Sign Test" critique of explanations that omit phase — [arXiv 2202.07756](https://arxiv.org/abs/2202.07756)
- **Thematic-only:** only 5 of 23 jam games (2020-2021) used a numerical simulation, some quantum connections were unclear, and only one had clear educational aspects — [arXiv 2408.09025](https://arxiv.org/html/2408.09025v1)
- **Incomplete:**
  - "Quantum Battleships Godot WIP — a game I made in Godot that doesnt work" — [WQCC gallery](https://wqcc.devpost.com/project-gallery)
  - Hacktopia: "terminal-based ... could have been better", with the website "in the future" — [Devpost](https://devpost.com/software/hacktopia)
- **Over-claiming and mock integration:** the unplaced CQhack25 QEC visualizer advertises:
  - "Industry Standards - Same codes used by Google & IBM"
  - "No bugs: Clean, tested implementation"
  - a "🏅 Why This Wins" section
  - and its author concedes "mock Classiq integration" for a Classiq-track entry.
  - It did not appear among the 6 winners — [Devpost](https://devpost.com/software/quantum-error-correction-qec-educational-visualizer); [CQhack25 gallery](https://cqhack25.devpost.com/project-gallery)
- **No learning evaluation:** the reviewers say comparative evaluation is impossible "due to the lack of comprehensive assessment tools" — [arXiv 2202.07756](https://arxiv.org/abs/2202.07756)

### Inferences
- A Quantum Unlocked entry should be able to answer three questions explicitly in its README:
  1. "What can a learner do here that they cannot do in the Qiskit textbook or IBM Composer?"
  2. "What multi-qubit or phase phenomenon is made visible?"
  3. "How do we know it teaches?"
- Honest scoping (stating what is simulated vs. idealized, and known limitations) is likely to read better to IonQ and Qollab judges than marketing claims. Qollab has a separate Best Documentation award.

### Gaps
- There are no published judge statements naming these weaknesses as reasons for specific losses. They are inferred from rubric language and from which entries did not place.

---

## Key Question 5: Are there educational projects built around trapped-ion physics or IonQ hardware?

### Takeaway
Very few, and none that is a judged, *winning* trapped-ion-physics teaching tool. The only explicitly trapped-ion educational artifact found is a **theatrical performance**, "The Qubitarium of Trapped Ions" (unitaryDESIGN, Feb 2026, no winners published). IonQ-hardware winners are games or creative pieces that *use* IonQ features (Opti-maze, Game of Finches, fATCAT) rather than teach how ions compute. No browser-based interactive visualizer of Mølmer–Sørensen gates, motional modes or ion-chain all-to-all connectivity was found. This is an open niche that aligns with the sponsor.

### Cited Findings
- **"The Qubitarium of Trapped Ions"** (Team 5, unitaryDESIGN Quantum Design Hackathon, Feb 20, 2026): a live six-act performance in which a narrator directs three ions (Dot, Bob, Sneaky).
  - The audience supplies the control fields, the photons (via phone flashlights) and the measurement.
  - The acts cover vacuum and emergence, electromagnetic rotation, **optical pumping**, a rotation pulse, entanglement and measurement.
  - The page publishes no winners.
  - [groups page](https://quantum-design-hackathon.github.io/groups.html); [event home](https://quantum-design-hackathon.github.io/)
- **IonQ-hardware educational winners:**
  - Opti-maze (QAOA game on the IonQ backend via Azure, with only "a tiny exposure to the real hardware") — [IonQ blog](https://www.ionq.com/blog/february-09-2022-iquhack-winners-opti-maze)
  - Entanglement5's Game of Finches explicitly exploited "the all-to-all connectivity of the IonQ platform" on Harmony — [Entanglement5 PR](https://github.com/iQuHACK/2023_IonQ/pull/3)
  - fATCAT's story was driven by power-law (J ~ 1/r^α) spin couplings typical of trapped ions — [fATCAT PR](https://github.com/iQuHACK/2024_IonQ/pull/4)
  - (All three covered in the prior notes.)
- **Qollab funded projects on IonQ hardware with educational intent:** qOrbital (VQE orbitals, "realistic shot budgets") and Quantum Market Game (classroom) — [Qollab cohort](https://qollab.xyz/explore/spring-2026-cohort)
- **Non-hackathon trapped-ion teaching resources** (useful as references; none is an interactive web visualizer):
  - Q-CTRL Boulder Opal tutorial on designing an MS gate for two ytterbium ions (code-based) — [Q-CTRL docs](https://docs.q-ctrl.com/boulder-opal/tutorials/optimize-molmer-sorensen-gates-for-trapped-ions)
  - IonVision (NQCC), which generates energy-level and pulse-sequence diagrams — [Indico](https://indico.fysik.su.se/event/9371/contributions/15138/)
  - A pedagogical review of ion trapping, qubit encodings and laser-ion gates — [arXiv 2505.20412](https://export.arxiv.org/abs/2505.20412)
  - A beginner's guide to trapped-ion QC — [arXiv 2303.16358](https://arxiv.org/abs/2303.16358v2)
  - A 3D-printed Paul-trap model plus simulation for Swedish upper-secondary physics, presented at Fysikdagarna 2022 — [Indico (via search snippet)](https://indico.global/event/7951/contributions/70600)
- In the Quantum Design Hackathon, other modalities (transmons, cat qubits, Rydberg, photonics, silicon spin) each got their own explainer. The trapped-ion team chose theatre rather than a simulator — [groups page](https://quantum-design-hackathon.github.io/groups.html)

### Inferences
- A Qiskit-based, in-browser **trapped-ion explainer** appears to have no precedent among winning projects. Examples:
  - Native-gate decomposition into MS/ZZ plus single-qubit rotations, contrasted with CNOT-based transpilation.
  - All-to-all connectivity versus heavy-hex SWAP overhead, shown by transpiling the same circuit for both topologies and counting two-qubit gates.
  - A phase-space-loop picture of the MS gate.
  - The IonQ simulator's noise model versus ideal.
- Such a project would be novel and sponsor-aligned. It can run on the free simulator, since hardware is unscored at Qollab.
- Caution: judges press "Run" on a Qiskit simulator. Any ion-physics content (phase-space trajectories, sideband couplings) needs to be computed or validated in code rather than just illustrated, to earn Technical Execution.

### Gaps
- Whether IonQ has published its own educational interactive tools (beyond docs and blog posts) was not checked.
- No hackathon project was found that teaches IonQ-specific concepts such as the AQ (algorithmic qubits) metric, the Forte/Tempo architecture, or barium-ion qubits.
- Whether Quantum Flytrap's Virtual Lab engine really models ions (claimed in one search summary) was not verified, so it is excluded from the findings.
