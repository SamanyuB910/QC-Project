# Teach the Topics Qollab Never Covered

Your best shot at Best of Quantum Unlocked is an interactive lab that computes real multi-qubit physics in Qiskit and teaches a hard topic that Qollab's 104 public projects and its Learn curriculum have not touched. On the evidence, **entanglement distribution ranks first** (noisy Bell pairs, then distillation, swapping and use) and **circuit-level error correction beyond the repetition code is a close second**. A QSP/QSVT polynomial studio and a trapped-ion "pulse-to-program" explorer are higher-variance alternatives. The official brief names error correction, fault tolerance, quantum networking and algorithms as example topics and accepts a demo, game, animation, visualization or GUI. As of mid-afternoon October 9, no theme-specific problem statements had been published. Since October 7, two rules changed and an FAQ entry was added: outside repos must now also be MIT-licensed, the built-in-the-window rule no longer lists AI tools (AI use is still allowed with disclosure), and Safari cannot run projects. The real threat is the tutorial bar, which lets judges score both Novelty and Technical Execution at zero. Qollab's own team has already shipped polished showcases on the obvious picks: a distance-3 repetition-code game, zero-noise extrapolation, readout mitigation, the Clifford/T boundary, transpilation to trapped-ion gates and T1 calibration. Meanwhile, a full-text scan of every Qollab project finds no mention of BB84, CHSH, entanglement swapping, purification, matching decoders, magic-state distillation, QSVT or Deutsch–Jozsa. Past educational winners, from QAVE at Qollab to Superposition Arcade at the QAIF games hackathon, simulated genuine multi-qubit quantum mechanics; the entries that lost re-skinned tutorials or over-claimed. Education research supplies named targets: faster-than-light signaling beliefs, confusing superposition with mixtures, and subsystem-state questions that only 23–26% of students answer correctly. It also favors predict-then-observe tutorials over free play. The runtime can carry all of this if you keep the teaching math small and exact in Python, send one batched anchor circuit of at most 20 qubits to the judge's backend, and ship precomputed IonQ Forte noise-model results.

## The brief names four topics, and a zero-score gate guards them

The authoritative Quantum Unlocked brief is in Qollab's Rules & terms page, not the FAQ. Its tagline asks teams to "make the hardest ideas in quantum computing click" ([Qollab Rules & terms](https://qollab.xyz/programs/hackathon/terms)). The body says quantum computing is full of ideas that are hard to visualize and asks teams to pick a **timely** topic and teach it creatively. It offers **quantum error correction, fault tolerance, quantum networking and algorithms** as examples, not as a closed list. The accepted formats are an **interactive demo, game, animation, visualization or GUI**, and the goal is to make a complex concept intuitive, engaging and memorable. The shorter version on the hub and how-it-works pages leaves out the word *game*, stresses that the topic should be hard and timely, and points to the Rules & terms for the full text ([How it works](https://qollab.xyz/programs/hackathon/how-it-works); [Qollab hackathon hub](https://qollab.xyz/programs/hackathon)). Your notes file `theme_brief_and_qollab_platform.md` preserves the exact wording of all three versions. Best of Quantum Unlocked is one of six global specialty awards, each worth **US$500 cash plus US$5,000 in compute**, and one project can win a specialty award and a placement. The theme question at registration commits you to nothing. You declare a theme at submission and can change it until the October 11 deadline, and a project may cover more than one theme ([How it works](https://qollab.xyz/programs/hackathon/how-it-works); [Rules & terms](https://qollab.xyz/programs/hackathon/terms)).

The gate that decides most entries is the tutorial bar. Every submission must go beyond a reference implementation or tutorial-level exercise by showing at least one of three things:

- a novel application or problem context;
- a technical extension, such as noise mitigation, parameter optimization or comparative benchmarking;
- an original analytical or educational contribution, for which the rules' own example is a new way to visualize or explain a quantum phenomenon.

Judges may score a project that misses the bar **zero on both Novelty & Creativity and Technical Execution**, whatever its other merits ([Rules & terms](https://qollab.xyz/programs/hackathon/terms)). The third route is the natural one for Unlocked, and it is the route a re-skin of an existing Qollab teaching demo would fail. The four criteria are Novelty & Creativity, Technical Execution, Impact Potential and Documentation Quality. They still have no published weights or descriptors, so treat them as roughly equal ([How it works](https://qollab.xyz/programs/hackathon/how-it-works)).

Kickoff day brought small but real changes. Comparing the October 9 rules with the October 7 snapshot shows two edits. A new requirement says any outside repo the project relies on, such as a frontend or backend hosted elsewhere, must also be MIT-licensed. The built-in-the-window requirement no longer lists AI tools among acceptable starting points. However, AI use remains explicitly allowed elsewhere in the rules and FAQ, provided you disclose what existed before the window ([Rules & terms](https://qollab.xyz/programs/hackathon/terms); [How it works](https://qollab.xyz/programs/hackathon/how-it-works)). A new FAQ entry says projects need a recent Chrome, Edge, Brave or Opera, or Firefox 153 or later, because Safari lacks the WebAssembly JSPI support that Qollab's runtime needs. On iPhone and iPad every browser uses Safari's engine ([How it works](https://qollab.xyz/programs/hackathon/how-it-works)). Record your video in Chrome and state the browser requirement on the project page.

As of about 14:45 ET, no theme-specific problem statements or IonQ challenge materials had appeared on the Qollab site, the GT node site, the Qollab forum or in web search. The GT site still promises to link sponsor problem statements as they are released ([GT Fall Fest site](https://qhackathon-gt.lovable.app/)). Qollab's newest announcement is still an August 26 item about Google withholding an ECDSA circuit, and the forum contains only auto-created project threads ([Qollab announcements](https://qollab.xyz/explore/news); [Qollab forum](https://forum.qollab.xyz/latest.json)). Check the node and global Slack channels at 7 PM before you commit.

The judging mechanics explain why runnability and honesty matter so much. Judges open the project page, read the code and press Run on a free simulator. Results from IonQ simulators or hardware neither add nor subtract points ([Rules & terms](https://qollab.xyz/programs/hackathon/terms)). An externally hosted frontend or backend is allowed only if it is public, needs no sign-in, carries an MIT license, lists its dependencies and contains no secrets ([How it works](https://qollab.xyz/programs/hackathon/how-it-works)). The local panel pairs a faculty or staff judge with Qollab and IonQ representatives. A node can forward its top three plus up to one project for each global specialty award, including Best of Theme ([How it works](https://qollab.xyz/programs/hackathon/how-it-works); [Rules & terms](https://qollab.xyz/programs/hackathon/terms)). In practice, the people scoring an Unlocked entry include Qollab staff who wrote the showcases you would be competing against.

No mentor names are public. Mentors choose areas such as QAOA, error mitigation, chemistry, finance, optimization and tooling, and education is not a named area. When the schedule goes live at kickoff, look for anyone listing QEC or networking ([Qollab Mentors](https://qollab.xyz/programs/hackathon/mentors)). One local signal: Shivani Mayekar, a Georgia Tech M.S. student who built the QuantumCanvas drag-and-drop circuit sandbox and has run workshops for more than 250 people, is in Qollab's Spring 2026 cohort ([Spring 2026 cohort](https://qollab.xyz/explore/spring-2026-cohort)). A circuit-sandbox entry would therefore look derivative at this node.

## Educational winners simulated real physics; losers re-skinned tutorials

Whether a teaching tool can win outright depends on the venue. At game-focused or creative events, educational entries take top prizes:

- QCB's *Quantum Whack-A-Mole* won iQuHACK 2021 overall, and Team 47's game, in which the players are qubits, won that year's IonQ track ([iQuHACK 2021](https://github.com/iQuHACK/2021)).
- *Opti-maze*, which teaches QAOA through a climate-policy maze with compete and cooperate modes, won the 2022 Microsoft/IonQ game track ([IonQ blog](https://www.ionq.com/blog/february-09-2022-iquhack-winners-opti-maze)).
- Four games, including the ZX-calculus puzzle *Dave the Hackerman*, won QAIF's 2021 games hackathon ([Seskir et al., arXiv:2202.07756](https://arxiv.org/abs/2202.07756)).
- QAVE won Qollab's first Creative Challenge ([QAVE showcase](https://qollab.xyz/explore/qave)).

At research-oriented Qiskit and QHack events, teaching tools land in side slots:

- *Qat the Cat* took Best in Education at Qiskit Camp Africa 2019, while first place went to a commutator-algebra tool ([Qiskit Medium](https://medium.com/qiskit/recap-2019-qiskit-camp-africa-d30020ea859d)).
- An intro-to-QML notebook won a separate Best Education Hack at the 2021 CIC-IPN Fall Fest ([arXiv:2302.12119](https://arxiv.org/abs/2302.12119)).
- A hidden-shift explainer got an honorary mention at Qiskit Hackathon Korea 2022 ([repo](https://github.com/qiskit-community/qiskit-hackathon-korea-22)).
- QHack has never run an education category ([PennyLane QHack 2024](https://pennylane.ai/blog/2024/03/qhack-2024-highlights/)).

Quantum Unlocked has a dedicated award, which puts it in the first group.

The Qollab and IonQ precedents point the same way. QAVE, by Inho Choi, computes the state at every gate and synchronizes several views into one replay. Qollab's write-up stresses that it makes errors and corrections observable, and with 667 views it is the most-viewed project on the platform ([QAVE showcase](https://qollab.xyz/explore/qave); [q-inho/qave](https://qollab.xyz/u/q-inho/qave)). IonQ's own challenges show what its engineers value:

- Entanglement5 built *Game of Finches* around IonQ's all-to-all connectivity ([Entanglement5 PR](https://github.com/iQuHACK/2023_IonQ/pull/3)).
- fATCAT's winning story ran on power-law spin couplings that are native to trapped ions ([fATCAT PR](https://github.com/iQuHACK/2024_IonQ/pull/4)).
- The 2024 prompt required quantum to do more than generate random numbers ([2024_IonQ](https://github.com/iQuHACK/2024_IonQ)).
- 2025 entries were scored partly on the educational clarity of their explanations ([IonQuHack2025.ipynb](https://github.com/iQuHACK/2025-IonQ/blob/main/IonQuHack2025.ipynb)).
- The 2026 challenge was a competitive entanglement-distillation network game ([2026-IonQ](https://github.com/iQuHACK/2026-IonQ)).

The technically serious winners share one trait: a genuine simulation core. Superposition Arcade won first place and 15,000 PLN at QAIF 2023. It runs a custom simulator with unitary gates, measurement and noise, and its levels are built from circuit identities ([SuperpositionArcade README](https://github.com/rsoiffer/SuperpositionArcade); [QAIF 2023 winners](https://www.qaif.org/contests/quantum-games-hackathon-2023-winners)). The Entangled States team at Qiskit Hackathon Global 2020 rendered all 2^n amplitudes as rods, because they saw games falter on multi-qubit wavefunctions ([Qiskit Medium](https://medium.com/qiskit/these-amazing-quantum-computing-ideas-came-out-of-our-landmark-qiskit-hackathon-global-905a0063f8e5)). By contrast, of 23 jam games from 2020–2021, **only five used a numerical simulation and only one had clear educational aspects**. Organizers also concluded that meaningful quantum games needed both physics and game-design expertise ([Piispanen et al., arXiv:2408.09025](https://arxiv.org/html/2408.09025v1)).

Published rubrics reward the same few things:

- QAIF judged correctness of the quantum content, playability including educational potential, originality, and polish ([arXiv:2202.07756](https://arxiv.org/abs/2202.07756)).
- CIC-IPN counted educational value under Impact ([arXiv:2302.12119](https://arxiv.org/abs/2302.12119)).
- The ITU FLIQ 2025 Education track measured how well teams learn and teach. One of its track resources ran from repetition codes to Surface-17 ([AI for Good FLIQ](https://aiforgood.itu.int/the-future-leaders-in-quantum-hackathon/)).

The failure modes are just as consistent:

- **Random-number-only quantum.** Bitcamp 2025's *Schrödinger's Catch* used Qiskit only to randomize fish bites ([Devpost](https://devpost.com/software/schrodingers-catch-trout-of-this-world)).
- **Tutorial re-skins.** *Quant PlayGround* bundled a coin flip, teleportation, a Bloch sphere and a Bell state, and it won a small 2024 event ([Devpost](https://devpost.com/software/quantx)). That is exactly the content Qollab's bar zeroes.
- **Incomplete builds.** A Wisconsin Fall Fest gallery entry was a battleship game its maker said did not work ([WQCC gallery](https://wqcc.devpost.com/project-gallery)).
- **Over-claiming.** CQhack25's Streamlit QEC visualizer covered 3-, 5- and 7-qubit codes and a distance-3 surface code. It also advertised itself as industry-standard and bug-free, included a section arguing why it would win, and admitted to a mock Classiq integration in a Classiq-track entry. All six winners were application projects ([Devpost](https://devpost.com/software/quantum-error-correction-qec-educational-visualizer); [CQhack25 gallery](https://cqhack25.devpost.com/project-gallery)).
- **No evidence of learning.** Reviewers note that quantum games cannot be compared for lack of assessment tools. They also cite Aaronson's critique that explanations describing a qubit as zero and one at once omit phase, and so cannot distinguish interference from ignorance ([arXiv:2202.07756](https://arxiv.org/abs/2202.07756)).

Across 2019–2026, **no deep, winning interactive explainer** was found for any of these:

- live QEC thresholds and decoding;
- magic-state distillation and fault-tolerance overhead;
- entanglement distillation and repeaters;
- phase kickback and interference as the mechanism of speedup;
- Trotter error;
- measurement-based computation;
- trapped-ion gate physics.

The nearest attempts were unplaced or unjudged. At the February 2026 unitaryDESIGN hackathon, teams produced a lattice-surgery board game and a six-act trapped-ion theatre piece, but no winners were published ([unitaryDESIGN groups](https://quantum-design-hackathon.github.io/groups.html)). Qollab funded GraFT's fault-tolerance graphs, but they are not published on the platform ([Spring 2026 cohort](https://qollab.xyz/explore/spring-2026-cohort)). A neural QEC decoder game is in progress at another 2026 Fall Fest event ([NeuralDecoderGame](https://github.com/EDHE08232001/NeuralDecoderGame)). That last one is a reminder that QEC is the topic other teams will reach for first.

## Qollab's catalog covers the obvious lessons and nothing on networking

### The Qollab team's own showcases are the bar to clear

Qollab's gallery API lists **104 public projects**, 51 of them by the qollab team account ([Qollab project API](https://api.qollab.xyz/api/project/popular?limit=30)). On September 1 the team published interactive JS + Qiskit "showcases", each pitched as a template to fork. Together they define the house style judges will expect. Each one has:

- an honest failure case;
- a live Monte Carlo or analytic model running in the browser;
- one small "anchor" circuit run on the selected backend at load;
- a make-it-yours fork path.

| Showcase | What it already teaches | What it leaves open |
|---|---|---|
| [Error correction: the repetition-code game](https://qollab.xyz/u/qollab/error-correction-showcase-the) | Distance-3 bit-flip code with syndrome lights and majority vote, including the two-flip case that fools the decoder. A seeded *Storm mode* Monte Carlo for d=3 and 5 on log-log axes, threshold at p=0.5. Deliberately bit-flip only | Its own suggested forks are distance 7, phase-flip mode and a qubit-overhead calculator. No circuit-level noise, detectors, surface code or matching decoder |
| [Interactive ZNE explorer](https://qollab.xyz/u/qollab/error-mitigation-showcase-inte) and [Python ZNE](https://qollab.xyz/u/qollab/error-mitigation-showcase-zero) | GHZ-4 parity with CX folding at x1/x3/x5, linear or Richardson fits; the Python version recovers to about 1% | Zero-noise extrapolation is done |
| [Readout mitigation](https://qollab.xyz/u/qollab/readout-mitigation-showcase-fi) | GHZ-5 with readout sliders and ideal, raw and corrected histograms | Done |
| [Statevectors vs stabilizers](https://qollab.xyz/u/qollab/simulation-showcase-statevecto) | 2^n memory vs an n×2n tableau; a ~40-line JS stabilizer simulator builds a 100-qubit GHZ state and refuses a T gate | Forks suggested: find the wall, count the magic |
| [Textbook gates to trapped ions](https://qollab.xyz/u/qollab/transpilation-showcase-from-te) | Hover to see H become three native rotations and CX become one MS plus four rotations; live depth and gate counts | Nothing on why an MS gate entangles |
| [Where T1 comes from](https://qollab.xyz/u/qollab/calibration-showcase-where-t1) | Live T1 fit with shot noise and a drift button | T2/Ramsey left as a fork |
| Kernel, H2 bond-length VQE, cross-framework VQE, two Bloch spheres | Drag-a-point kernel, dissociation curve, Bloch rotations ([kernel](https://qollab.xyz/u/qollab/quantum-kernel-showcase-drag-t); [H2](https://qollab.xyz/u/qollab/quantum-chemistry-showcase-t-2); [Bloch](https://qollab.xyz/u/qollab/interactive-bloch-sphere)) | Done |

Outside the showcases, Qollab has:

- Python examples of teleportation (using deferred measurement because IonQ lacks mid-circuit feed-forward), Shor for N=15, QPE, Grover, GHZ and Bell states ([teleportation](https://qollab.xyz/u/qollab/quantum-teleportation)).
- Library showcases for qiskit-algorithms, nature, finance and machine learning.
- Community explainers: a QEC walkthrough of the bit-flip, Shor and 5-qubit codes ([sairamtummuri QEC](https://qollab.xyz/u/sairamtummuri/quantum-error-correction)), mitigation and noise dashboards, and a 2-qubit state visualizer whose QuTiP views were removed because QuTiP has no WebAssembly build ([2-qubit visualizer](https://qollab.xyz/u/onri-jay-benally/2-qubit-state-visualization)).
- Two projects published October 8: a pure-state entanglement meter ([Niharika28](https://qollab.xyz/u/Niharika28/pure-state-entanglement-meter)) and a bandit learner over mitigation strategies ([S0cra13s](https://qollab.xyz/u/S0cra13s/quantum-automitigation)).

A full-text scan of every write-up and main file found **zero matches** for BB84, E91, QKD, Steane, [[4,2,2]], [[7,1,3]], lattice surgery, magic state, minimum-weight matching, union-find, CHSH, Bell inequality, entanglement swapping, repeater, purification, Deutsch, Bernstein, Simon, QSVT, randomized benchmarking, quantum volume, cluster state, phonon and ion shuttling. Surface codes, HHL, amplitude estimation, no-cloning, superdense coding and distillation appear only in passing ([Qollab project API](https://api.qollab.xyz/api/project/popular?limit=30)).

Qollab Learn reinforces the gap. It has 5 courses with 27 lessons, six concept explainers (superposition, measurement, interference, entanglement, QAOA, VQE) and 50 docs, including 29 gate pages that cover IonQ's native gates. **Nothing covers error correction, fault tolerance or networking**, and noise appears in only one lesson and a few docs ([Qollab Learn](https://qollab.xyz/learn); [sitemap](https://qollab.xyz/sitemap-content.xml)). An Unlocked entry on those topics would also fill a hole in Qollab's own curriculum. That is an easy Impact Potential argument, since winners get featured placement on the platform.

QAVE is a one-click library on Qollab (`qave==0.1.0`), but its animation renderer is a Processing (Java) sketch plus ffmpeg, which cannot run in the browser runtime. Qollab's own adapted copy generates the trace, prints diagnostics and exits before rendering ([mirya/qave](https://qollab.xyz/u/mirya/qave); [QAVE README](https://github.com/qollabxyz/qave/blob/main/README.md)). Its NumPy backend has further limits ([backend_a.py](https://github.com/qollabxyz/qave/blob/main/backend/src/qave_backend/simulator/backend_a.py); [gates.py](https://github.com/qollabxyz/qave/blob/main/backend/src/qave_backend/simulator/gates.py)):

- pure states only, with no noise model;
- a recommended maximum of 16 qubits;
- only x, y, z, h, s, t, rx, ry, rz, cx, cz, ccx, cswap and swap gates.

So despite the showcase's error-correction framing, QAVE can show QEC only with errors injected as explicit gates, and a 17-qubit surface code slightly exceeds its cap. If you use it as a trace generator, disclose it.

### Outside Qollab, beginner tools are crowded and advanced tools are expert-only

| Tier | Representative tools (status) | Implication |
|---|---|---|
| Circuit sandboxes and Bloch intuition | Quirk, a 16-qubit browser toy, Apache-2.0 ([GitHub](https://github.com/Strilanc/Quirk)); IBM Composer, migrated after the classic platform's July 2025 sunset and no longer saving files ([IBM](https://www.ibm.com/quantum/blog/iql-migration)); PennyLane Codebook ([PennyLane](https://pennylane.ai/blog/2024/05/pennylane_codebook_makeover)); Black Opal; Brilliant; PhET Quantum Measurement (2025) ([guide](https://phet.colorado.edu/files/teachers-guide/quantum-measurement-html-guide_en.pdf)) | Saturated; another sandbox fails on novelty |
| Research-validated simulations | QuVis two-level systems and four QKD simulations ([QuVis](https://www.st-andrews.ac.uk/physics/quvis/de/index-about.php)); QuILT tutorials ([DeVore & Singh](https://link.aps.org/doi/10.1103/PhysRevPhysEducRes.16.010126)) | Evidence-backed but introductory, and not Qiskit |
| Optics and puzzle games | Quantum Flytrap Virtual Lab, up to 3 photons ([arXiv:2203.13300](https://arxiv.org/abs/2203.13300)); Quantum Odyssey (Steam, paid) ([feasibility study](https://arxiv.org/abs/2106.07077)); Decodoku decoding puzzles that hide the quantum layer ([arXiv:1712.09649](https://arxiv.org/pdf/1712.09649)) | Photon routing and gate puzzles are covered |
| Expert QEC and ZX tools | Crumble, a Stim prototype ([algassert](https://algassert.com/crumble)); qsurface, desktop-only ([docs](https://qsurface.readthedocs.io/)); QEC-Playground, pre-1.0 ([PyPI](https://pypi.org/project/qecp/0.2.3/)); Error Correction Zoo, a static catalog ([about](https://errorcorrectionzoo.org/about)); ZXLive and PyZX ([docs](https://zxlive.readthedocs.io/en/latest/gettingstarted.html)) | Powerful but not guided or novice-facing |
| Advanced-topic notebooks | Boulder Opal Mølmer–Sørensen dynamics ([Q-CTRL](https://docs.q-ctrl.com/boulder-opal/user-guides/how-to-calculate-system-dynamics-for-arbitrary-molmer-sorensen-gates)); magic-state distillation in QuEra Tsim and PennyLane Catalyst ([QuEra](https://bloqade.quera.com/tsim/tutorials/magic_state_distillation); [PennyLane](https://docs.pennylane.ai/projects/catalyst/en/stable/demos/magic_distillation_demo.html)); PennyLane QSVT demos ([intro QSVT](https://pennylane.ai/demos/tutorial_intro_qsvt)) | Code, not interactives |
| Retired | Qiskit Textbook, superseded and unmaintained ([textbook](https://qiskit.org/textbook/ch)); IBM Quantum Lab, sunset May 15, 2024; Hello Qiskit games, archived Jan 18, 2024 ([repo](https://github.com/qiskit-community/qiskit-community-tutorials/blob/master/games/)) | Old explainers are disappearing |

### Seven hard topics have no guided interactive anywhere

Combine the two inventories and a clear white space appears between beginner sandboxes and expert research tools: no browser-native, guided, misconception-targeted interactive exists for any advanced topic ([Resource Letter QIE-1](https://arxiv.org/html/2606.06445v1)). Specifically, nobody has shipped an interactive for:

- **measurement-based computation**, where no tool was found at all ([Raussendorf, Browne, Briegel](https://arxiv.org/pdf/quant-ph/0301052));
- **magic states and distillation**, which exist only as notebooks;
- **Mølmer–Sørensen gate physics**, which exists only as notebooks;
- **noise channels and density-matrix decoherence**;
- **reduced states and the partial trace**;
- **novice syndrome decoding with Pauli propagation**, where Crumble is too expert;
- **QSP/QSVT polynomial design**, where PennyLane's demos plot polynomials but are not designers.

Accessibility is equally empty. The only audio-enabled circuit tool found was a sonified Quirk fork ([Soniq-Quirk](https://github.com/QuantumVillage/Soniq-Quirk)). Multi-qubit visualization itself is unsettled: in a 2025 study of 25 instructors, there was little consensus on representations beyond symbolic notation ([Resource Letter QIE-1](https://arxiv.org/html/2606.06445v1)). On Qollab specifically, add **all of networking** (only 3-qubit teleportation exists), the oracle-algorithm family, and anything about decoders.

## Research says: name one misconception, demand a prediction, keep the math visible

The best-documented quantum-computing difficulties are now measured, not anecdotal. The Quantum Computing Conceptual Survey (QCCS) is 20 items validated on **777 responses from 55 courses at 46 institutions**, with α = 0.83. Its hardest items score **0.23, 0.25 and 0.26** correct. They cover finding the state of a subset of qubits, including recognizing when that subset has no well-defined ket, and Hilbert-space dimension ([Meyer et al. 2026, arXiv:2608.14459](https://arxiv.org/html/2608.14459v1)). The same work documents five more difficulties:

- believing all entangled states are maximally entangled;
- adding rather than multiplying tensor-product dimensions;
- overgeneralizing CNOT control/target rules;
- missing that CNOT creates entanglement;
- being unable to tell superpositions from mixtures experimentally.

Earlier work agrees. Passante, Emigh and Shaffer found that students from sophomore to graduate level can compute superposition probabilities, yet cannot identify their experimental implications or distinguish them from mixtures ([PRSTPER 11, 020135](https://link.aps.org/doi/10.1103/PhysRevSTPER.11.020135)). Hu, Li and Singh seeded their QC-basics tutorial with four known errors: qubit ordering, probability as amplitude rather than squared amplitude, conflating basis states with qubits, and confusing separability with entanglement ([arXiv:2408.04859](https://arxiv.org/pdf/2408.04859)). A 2026 study of whether CNOT can affect its control qubit found students switching between step-by-step computation and qualitative control/target rules that overgeneralize ([arXiv:2604.16624](https://arxiv.org/pdf/2604.16624)).

The entanglement and measurement misconceptions matter most for networking and QEC tools:

- **Faster-than-light signaling.** This belief appeared among 31 pre-service physics teachers and a 73-student university cohort, alongside confusion of entanglement with superposition ([Brang et al., EPJ QT 2024](https://epjqt.epj.org/articles/epjqt/abs/2024/01/40507_2024_Article_244/40507_2024_Article_244.html)). Instructors trace it partly to popular media ([Majidy, arXiv:2405.20923](https://arxiv.org/html/2405.20923)).
- **Perfect correlation along every axis.** QuVis studies found students assuming every entangled state is perfectly correlated along all common axes ([Kohnle & Deffebach](https://arxiv.org/pdf/1512.02346)).
- **Falling back on classical intuitions.** Students revert to classical correlations or hidden-variable ideas even after instruction ([Frontiers in Education 2025](https://www.frontiersin.org/journals/education/articles/10.3389/feduc.2025.1729099/full)).
- **Density-matrix misreadings.** Students conflate uncertainty about preparation with spread in measurement outcomes. Yet a pure state does not imply certain outcomes, and a mixed state may be the reduced state of an entangled system rather than ignorance ([Majidy](https://arxiv.org/html/2405.20923)).
- **Simultaneity wording.** Describing superpositions as simultaneous states is itself flagged as misleading ([ISSEP 2025 poster](https://issep2025.uni-trier.de/src/poster/ISSEP2025-Poster-Krosse-QuantumComputing.pdf)).
- **The parallel-trial myth.** Aaronson calls the belief that a quantum computer tries every answer in parallel the most common popular misconception ([Aaronson](https://scottaaronson.com/writings/highschool.html)). 3Blue1Brown's 2025 Grover video targeted it, and even its follow-up had to repair viewer confusion about the oracle ([3Blue1Brown](https://3blue1brown.substack.com/p/where-my-explanation-of-grovers-algorithm)). No physics-education study has tested this misconception on its own.

Several interventions have measured effects:

| Intervention | Result |
|---|---|
| Research-validated guided-inquiry tutorial (QuILT) on B92 QKD | Average **56% (N=49) before → 91% (N=50) after** ([DeVore & Singh](https://link.aps.org/doi/10.1103/PhysRevPhysEducRes.16.010126)) |
| QuILT on QC basics | Notable gains beyond lecture, with some persistent difficulties ([Resource Letter QIE-1](https://arxiv.org/html/2606.06445v1)) |
| QuVis two-level-system simulations | Learning shown at introductory and advanced levels ([Kohnle et al. 2015](https://arxiv.org/abs/1501.07905)) |
| Dimensional Circle Notation shown **alongside** Dirac notation | Better novice performance and lower cognitive load; learners who switched between notations more often benefited less ([Bley et al., arXiv:2505.21508](https://arxiv.org/html/2505.21508v3)) |
| Bloch sphere vs a "quantum bead" model (149 school students) | No difference in post-test learning; the Bloch sphere gave more efficient application-task performance ([Qerimi et al.](https://arxiv.org/abs/2507.21721)) |

There are cautions as well. A video that contained misconceptions *increased* them, and peer discussion with "trap" answers raised correctness from 52% to 80% in a classical example ([Majidy](https://arxiv.org/html/2405.20923)). No-code tools that never move learners to formal math show limited effectiveness, though attribution of that 2025 finding is uncertain ([MDPI Educ. Sci.](https://www.mdpi.com/2227-7102/15/9/1167)). Games have no controlled pre/post evidence, only perception studies ([Seskir et al.](https://arxiv.org/abs/2202.07756)).

Three independent design traditions converge on one recipe. PhET's quantum simulations make the unobservable visible, couple learner actions directly to the representation, and do the calculations so attention stays on concepts ([McKagan et al.](https://arxiv.org/abs/0709.4503)). QuVis refines its simulations through think-aloud observation ([QuVis](https://www.st-andrews.ac.uk/physics/quvis/de/index-about.php)). QuILTs build distractors from documented errors. For your tool, the recipe has four steps:

1. Open each module with a prediction about a named misconception.
2. Reveal the Qiskit-computed result in two linked representations, one visual and one in Dirac or matrix form.
3. Name the misconception in a short reconcile step.
4. Close with spaced micro-prompts. Quantum Country's data show about 95% recall of declarative prompts at five days, but that measures recall, not conceptual transfer ([Matuschak](https://notes.andymatuschak.org/zS5uKLsoTbkJSadTv2U3Z4G3uEBrFxTLy5E)).

Keep simultaneity and try-every-answer language out of your own copy. Interference-first language counters both.

Plan evaluation modestly. QCCS deliberately excludes algorithms and communication. QISCIT has 31 items and appeared in *American Journal of Physics* in 2026, but has not yet been tested on students ([arXiv:2506.17122](https://arxiv.org/abs/2506.17122)). A realistic 48-hour plan has five parts:

- 5–8 original items aimed at QCCS-style constructs plus your topic;
- a confidence rating on each item;
- logging of first-try correctness;
- a normalized gain, (post − pre)/(100 − pre), computed in memory;
- a JSON download of the results.

Frame it as a usability and feasibility pilot, as the Quantum Odyssey study did ([arXiv:2106.07077](https://arxiv.org/abs/2106.07077)). Cite QCCS as the alignment target without claiming validated results. Most importantly, **no physics-education study exists on learning QEC, no-cloning, decoherence, Kraus channels or quantum speedup** ([Resource Letter QIE-1](https://arxiv.org/html/2606.06445v1)). Any topic-specific teaching claim you make is untested, and even a five-person think-aloud during the build would count as new evidence. Say that openly. It reads as rigor, not weakness.

## What each candidate topic must get exactly right

Unless stated otherwise, the simulated numbers below come from the researchers' scripts in `research_notes/Quantum Unlocked theme deep dive/scripts/`, which are reusable starting points. All of them assume ~0.5% depolarizing two-qubit error and no idle noise. That is close to IonQ's legacy Forte model and optimistic for real hardware.

### Error correction and fault tolerance: honest numbers beat pretty lattices

Three ideas carry the whole field.

**First, no-cloning forces encoding into an entangled subspace.** The 3-qubit code maps α|0⟩+β|1⟩ to α|000⟩+β|111⟩, not to three copies ([Wootters & Zurek](https://doi.org/10.1038/299802a0)).

**Second, measuring commuting Pauli parities discretizes continuous noise.** Syndrome measurement projects an arbitrary error onto Pauli branches. A code that corrects {I, X, Y, Z} on t qubits therefore corrects every error on t qubits, coherent ones included, and never reveals the logical data ([Gottesman, arXiv:0904.2557](https://arxiv.org/abs/0904.2557)). Several precise statements follow:

- The Knill–Laflamme condition P E_a†E_b P = c_ab P says when an error set is correctable. A singular c_ab makes the code degenerate ([Knill & Laflamme](https://arxiv.org/abs/quant-ph/9604034)).
- An [[n,k,d]] code corrects ⌊(d−1)/2⌋ unknown errors, detects d−1, and corrects d−1 erasures ([Gottesman thesis](https://arxiv.org/abs/quant-ph/9705052)).
- The quantum Hamming bound forces n ≥ 5 for one logical qubit, and [[5,1,3]] saturates it exactly, since 2·16 = 32 ([Ekert & Macchiavello](https://arxiv.org/abs/quant-ph/9602022)).
- In the binary symplectic picture, a syndrome is just H·e over GF(2). That turns error correction into linear algebra a browser can do instantly.

**Third, Clifford circuits are classically simulable.** Gottesman–Knill makes stabilizer circuits easy to simulate ([Gottesman](https://arxiv.org/abs/quant-ph/9807006)). Aaronson–Gottesman tableaus cost O(n) per gate and O(n²) per measurement ([CHP](https://arxiv.org/abs/quant-ph/0406196)). Stim samples whole circuits by propagating Pauli "frames" from a single reference shot ([Gidney 2021](https://arxiv.org/abs/2103.02202)). That is why QEC demos with 20–100 qubits run in a browser when statevectors stop at 24.

The code zoo a tool should get right:

- **Repetition code.** Its code-capacity logical error is 3p² − 2p³, which beats a bare bit whenever p < 1/2. This is the curve Qollab's showcase plots ([Preskill ch. 7](http://theory.caltech.edu/~preskill/ph229/notes/chap7.pdf)).
- **Shor [[9,1,3]]** is degenerate ([Shor 1995](https://doi.org/10.1103/PhysRevA.52.R2493)).
- **Steane [[7,1,3]]** has a transversal Clifford group, with checks taken from the Hamming rows 0001111, 0110011, 1010101 ([Steane](https://arxiv.org/abs/quant-ph/9601029)).
- **[[4,2,2]]** detects any single error, and Gottesman proposed it as the minimal platform for demonstrating fault tolerance ([arXiv:1610.03507](https://arxiv.org/abs/1610.03507)).
- **Rotated surface code.** [[d²,1,d]] plus d²−1 measure qubits gives **17, 49 and 97 physical qubits at d=3, 5, 7** ([Fowler et al.](https://arxiv.org/abs/1208.0928)).
- **Thresholds depend on the noise model** ([Dennis et al.](https://arxiv.org/abs/quant-ph/0110143); [Wang, Harrington, Preskill](https://arxiv.org/abs/quant-ph/0207088); [Bombin et al.](https://arxiv.org/abs/1202.1852)), and learners routinely conflate them:

  | Noise model | Surface-code threshold |
  |---|---|
  | Code capacity | ~10.3% with matching (~10.9% optimal; ~18.9% with degenerate maximum-likelihood decoding under depolarizing noise) |
  | Phenomenological | ~2.9% |
  | Circuit-level | ~0.5–1% |

- **Fowler's scaling heuristic,** P_L ≈ 0.03(p/p_th)^((d+1)/2) with p_th ≈ 0.57%, implies **10³–10⁴ physical qubits per logical qubit** at p = 10⁻³ ([Fowler et al.](https://arxiv.org/abs/1208.0928)).
- **IBM's gross code** [[144,12,12]] uses 288 physical qubits to protect 12 logical qubits for about a million cycles at 0.1% error, where the surface code would need about 3,000. Its threshold is 0.8% and it needs degree-6 connectivity ([Bravyi et al.](https://arxiv.org/abs/2308.07915)).
- **Bosonic and hardware-native codes.** AWS's Ocelot cat-qubit repetition code reached 1.75% (d=3) and 1.65% (d=5) logical error per cycle ([arXiv:2409.13025](https://arxiv.org/abs/2409.13025)). Erasure conversion lifts a Yb-Rydberg threshold from 0.937% to 4.15% ([Wu et al.](https://arxiv.org/abs/2201.03540)).

Decoders are classical inference engines. A *detector* is any parity of measurements that is deterministic without noise. A detector error model is a hypergraph, and when every error flips at most two detectors the model is graphlike and can be decoded by matching ([Stim DEM docs](https://github.com/quantumlib/Stim/blob/main/doc/file_format_dem_detector_error_model.md)). The main decoder families:

- **Matching.** PyMatching v2 decodes surface codes at 0.1% error up to d=17 in under ~1 µs per round ([Higgott & Gidney](https://arxiv.org/abs/2303.15933)).
- **Union-find** runs in almost-linear time with a 9.9% code-capacity threshold, against matching's 10.3% ([Delfosse & Nickerson](https://arxiv.org/abs/1709.06218)).
- **Belief propagation** stalls on degeneracy, and OSD post-processing repairs it ([Roffe et al.](https://arxiv.org/abs/2005.07016)). IBM's Relay-BP beats BP+OSD on bivariate-bicycle codes ([arXiv:2506.01779](https://arxiv.org/abs/2506.01779)), and IBM reports real-time qLDPC decoding in under 480 ns ([IBM newsroom](https://newsroom.ibm.com/2025-11-12-ibm-delivers-new-quantum-processors,-software,-and-algorithm-breakthroughs-on-path-to-advantage-and-fault-tolerance)).
- **Neural decoders.** AlphaQubit made about 6% fewer errors than a tensor-network decoder and about 30% fewer than correlated matching on Google data ([Bausch et al.](https://arxiv.org/abs/2310.05900)). AlphaQubit 2 decodes surface codes in real time up to d=11 ([arXiv:2512.07737](https://arxiv.org/abs/2512.07737)).

Real-time throughput matters because a decoding backlog grows exponentially with T-depth ([Terhal](https://arxiv.org/abs/1302.3428)). Willow decoded at 63 µs average latency against a 1.1 µs cycle ([arXiv:2408.13687](https://arxiv.org/abs/2408.13687)). **IonQ claimed an end-to-end real-time decoder on a single CPU on September 22, 2026**, but its benchmarks were *simulated* workloads of up to 408 logical qubits. A secondary write-up reports a worst-case decoding window of 41.86 ms against a 15 ms budget ([IonQ release](https://investors.ionq.com/news/news-details/2026/IonQ-Demonstrates-Industrys-First-End-to-End-Real-Time-Quantum-Error-Decoder/default.aspx); [Wevolver](https://www.wevolver.com/article/real-time-quantum-error-decoding-single-cpu-408-logical-qubits)).

**Error correction is not fault tolerance.** Syndrome circuits spread errors: an ancilla fault halfway through four CNOTs becomes a weight-2 "hook" error, so CNOT order is chosen to point hooks away from the logical operator ([Fowler et al.](https://arxiv.org/abs/1208.0928)). Chao–Reichardt flags catch these spreads with just two extra qubits at distance 3 ([arXiv:1705.02329](https://arxiv.org/abs/1705.02329)). Universality then costs extra:

- **Eastin–Knill** forbids a universal transversal gate set ([arXiv:0811.4262](https://arxiv.org/abs/0811.4262)).
- **Bravyi–König** confines 2D topological codes' constant-depth gates to Cliffords ([arXiv:1206.1609](https://arxiv.org/abs/1206.1609)).
- **Magic states** fill the gap. Bravyi–Kitaev 15-to-1 distillation outputs error ≈ **35p³** ([quant-ph/0403025](https://arxiv.org/abs/quant-ph/0403025)).
- **Cultivation** reaches ~2×10⁻⁹ logical error at 10⁻³ noise for roughly the cost of a lattice-surgery CNOT ([Gidney, Shutty, Jones](https://arxiv.org/abs/2409.17595)). Google demonstrated it with a 40× error reduction and fidelity 0.9999(1), keeping about 8% of attempts ([Google Research](https://research.google/pubs/magic-state-cultivation-on-a-superconducting-quantum-processor/)).

These overheads feed resource estimates. **RSA-2048 fell from 20 million noisy qubits in 2019 to under 1 million in under a week (May 2025)** ([Gidney & Ekerå](https://arxiv.org/abs/1905.09749); [Gidney 2025](https://arxiv.org/abs/2505.15917)). Claims below 100,000 qubits from 2026 come from secondary sources and remain unverified ([postquantum.com](https://postquantum.com/quantum-research/quantum-breakthrough-rsa-2048/)).

| Platform | Milestone | Key number | Source |
|---|---|---|---|
| Google Willow | Surface code d=3→5→7 below threshold | Λ = 2.14 ± 0.02; 0.143%/cycle at d=7; 101 qubits; 2.4× the best physical qubit | [arXiv:2408.13687](https://arxiv.org/abs/2408.13687) |
| Google | Color code d=3→5 | Λ = 1.56; magic-state injection ~99% | [Google blog](https://research.google/blog/a-colorful-quantum-future/) |
| Quantinuum H2 | [[7,1,3]] and [[12,2,4]] with Microsoft | 9.8–500× and 4.7–800× below physical error | [arXiv:2404.02280](https://arxiv.org/abs/2404.02280) |
| Quantinuum | Break-even logical controlled-Hadamard | 2.3×10⁻⁴ vs 1.0×10⁻³ for the physical gate | [arXiv:2506.14688](https://arxiv.org/html/2506.14688v1) |
| Quantinuum Helios | 98 barium qubits, 99.921% 2Q fidelity | 94 error-detected / 48 error-corrected logical qubits | [Quantinuum](https://www.quantinuum.com/blog/introducing-helios-the-most-accurate-quantum-computer-in-the-world) |
| Harvard/QuEra | 448 atoms | 2.14(13)× below-threshold suppression | [arXiv:2506.20661](https://arxiv.org/abs/2506.20661) |
| IonQ (June 2026) | 9 codes on a 40-ion ¹³³Ba⁺ chain | BB5 qLDPC: 4 logical in 18 physical; best memory 3.95 s vs 1.1 s physical | [Quantum Computing Report](https://quantumcomputingreport.com/experimental-demonstration-of-breakeven-qldpc-and-block-codes-on-a-trapped-ion-architecture/) |
| IonQ Forte (Aug 2026) | Continuous-angle logical rotations in the Steane code | Abstract gives no headline numbers | [arXiv:2608.20676](https://arxiv.org/abs/2608.20676) |
| Earlier IonQ | [[4,2,2]] error detection | Helped on Harmony; no conclusive gain on lower-error Aria | [arXiv:2412.20736](https://arxiv.org/abs/2412.20736) |

Two literacy warnings belong in any QEC tool. First, Google's Λ of 2.14 and Harvard's 2.14 are numerically identical but measured differently: Google's is per-cycle memory across distances, while Harvard's comes from a four-round characterization. Second, logical-qubit leaderboards mix error-*detected* with error-*corrected* qubits and post-selected with non-post-selected results.

No education research studies QEC learners, so the hardest concepts are expert inference. They are:

- measuring parity without measuring the data;
- why correcting Paulis suffices (discretization);
- degeneracy, where different corrections are equally right;
- detectors versus raw stabilizer outcomes;
- hooks, and why correction differs from fault tolerance;
- the 10%/3%/1% threshold confusion;
- detection with post-selection versus correction;
- why Λ matters more than any single error rate;
- why Clifford gates are not enough.

The researchers' Pauli-frame simulator turns these into numbers ([frame_sims_v2.py](<../research_notes/Quantum Unlocked theme deep dive/scripts/frame_sims_v2.py>); cross-checked against Aer in [qec_sims.py](<../research_notes/Quantum Unlocked theme deep dive/scripts/qec_sims.py>)). It tracks an X/Z error frame per shot as boolean arrays, applies a random non-identity two-qubit Pauli after each CNOT with probability p2, sets p1 = p2/10, and uses readout flip = p2. It is about 60 lines of numpy, which is Stim's algorithm without bit-packing. Use `frame_sims_v2.py`, not v1: v2 adds the space-time diagonal edges without which matching loses to plain majority vote. Three findings are the most teachable.

**Finding 1: measure-then-decode beats measurement-free correction.** On the 3-qubit code at p2 = 0.5%, coherent Toffoli correction (8 CNOTs) gives 2.4% logical error even with no channel noise. Majority vote on measured data gives 0.46%, and correcting one qubit from ancilla syndromes gives 1.8%. At channel flip rate q = 0.10, bare is 10.4%, encoded with majority vote 3.6%, and Toffoli 5.1%. Decoding should be classical post-processing, which is exactly IonQ's no-feed-forward regime.

**Finding 2: error detection is not error correction.** The [[4,2,2]] logical Bell pair is exactly Bell(0,3) ⊗ Bell(1,2), costing 2 H and 2 CNOT. Measure all four qubits, reject odd parity, and read the logical parity:

| p2 | Bare Bell parity error | Encoded, post-selected | Acceptance | Gain |
|---|---|---|---|---|
| 0.001 | 0.27% | 0.0008% | 99.5% | ~335× |
| 0.003 | 0.79% | 0.0063% | 98.4% | ~126× |
| 0.005 | 1.31% | 0.018% | 97.4% | ~74× |
| 0.01 | 2.6% | 0.071% | 95.0% | ~37× |
| 0.02 | 5.1% | 0.29% | 90.4% | ~18× |

*Without* post-selection the encoded error equals the bare 1.31%. Resolving one failure in 5,000 accepted shots needs at least 50,000 shots, so the judge's anchor run cannot show that statistic and the browser simulation must.

A flag qubit turns non-fault-tolerant GHZ-style preparation (0.30% logical error at 97.3% acceptance) into fault-tolerant preparation (**0.028% at 95.8%**): **about 10× better from one extra qubit**. Bare preparation-and-measure error is 1.0%.

There is an analytic twist here. The uniform model predicts that the gain *grows* as gate error falls, yet IonQ's Aria showed no conclusive gain where Harmony did ([arXiv:2412.20736](https://arxiv.org/abs/2412.20736)). Correlated errors the model omits are the likely culprit, and explaining that gap is an original analytical contribution.

**Finding 3: suppression factors fall toward 1 near threshold.** A repetition-code memory with fresh ancillas per round needs d + R(d−1) qubits, so R = 3 rounds fit d = 3, 5 and 7 in 9, 17 and 25 qubits. Decoding uses networkx matching:

| p2 | d=3 (9q) | d=5 (17q) | d=7 (25q) | Bare qubit |
|---|---|---|---|---|
| 0.005 | 0.063% | 0.010% | <0.003% | 1.3% |
| 0.02 | 0.94% | 0.20% | 0.037% | 5.0% |
| 0.04 | 3.1% | 1.1% | 0.39% | 9.6% |
| 0.08 | 10.4% | 7.0% | 4.2% | 17.8% |
| 0.20 | 33.8% | 33.0% | 31.6% | 35.6% |

The suppression factors fall from about 4.7 (d=3→5) and 5.4 (d=5→7) at 2% error, to about 2.8–2.9 at 4%, and to 1.5–1.7 at 8%. That is the mechanism behind Willow's 2.14.

Be honest about one caveat: with only 3 rounds **the curves have not crossed even at 20%**. A textbook threshold plot needs R ≈ d rounds, which means 49 qubits at d = 7. That is fine for the numpy simulator but beyond IonQ's 29-qubit noise model.

The d = 3 rotated surface code (17 qubits per round, 24 CNOTs) decoded by a lookup table trained on 500,000 shots shows the p² signature of distance 3:

| p2 | Rounds | Qubits | ML-decoded error | Undecoded | Post-select all-trivial: acceptance / error |
|---|---|---|---|---|---|
| 0.001 | 1 | 17 | 0.011% | 0.67% | 97.0% / ~0 |
| 0.003 | 1 | 17 | 0.095% | 2.0% | 91.4% / ~0 |
| 0.005 | 1 | 17 | 0.25% | 3.3% | 86.0% / ~10⁻⁶ |
| 0.010 | 1 | 17 | 0.96% | 6.4% | 74.0% / 4×10⁻⁵ |
| 0.005 | 2 | 25 | 0.52% | 5.0% | 77.4% / 3×10⁻⁶ |

The pseudo-threshold crossing with the slope-1 line is near 1%. A tool should say which comparator it uses for that crossing. A learned lookup table also makes a teaching point: a decoder is literally conditional probability.

Other demos fit IonQ's no-feed-forward constraint:

- a **single-fault explorer** that lights up detectors, Crumble's core idea rebuilt on the numpy frame simulator with no sampling needed;
- [[5,1,3]] and [[7,1,3]] **syndrome puzzles** scored by logical coset;
- **deferred-measurement T-gate teleportation**, alongside the analytic 35p³ distillation curve.

### Entanglement and networking: one Werner slider orders every threshold

Two-qubit entanglement is fully characterized, which makes it ideal for exact live computation:

- For pure states, the Schmidt decomposition and E(ψ) = S(ρ_A) give both the distillable entanglement and the entanglement cost ([Bennett et al. 1996](https://arxiv.org/abs/quant-ph/9511030)).
- Peres–Horodecki partial transpose is necessary and sufficient for separability in 2×2 and 2×3 systems ([Peres](https://arxiv.org/abs/quant-ph/9604005); [Horodecki](https://arxiv.org/abs/quant-ph/9605038)).
- Every entangled two-qubit state is distillable ([Horodecki 1997](https://arxiv.org/abs/quant-ph/9607009)), while PPT-entangled bound states exist in larger dimensions ([Horodecki 1998](https://arxiv.org/abs/quant-ph/9801069)).
- Wootters concurrence gives C = 2|ad − bc| for pure states and a closed form for mixed states ([Wootters](https://arxiv.org/abs/quant-ph/9709029)).
- Qiskit's `quantum_info` provides partial_trace, entropy, concurrence, negativity, entanglement_of_formation and mutual_information as NumPy code ([Qiskit source](https://github.com/Qiskit/qiskit/tree/main/qiskit/quantum_info)).

Some niche facts make good puzzles:

- **Catalysis.** Nielsen's majorization theorem says when one pure state converts to another by local operations and classical communication (LOCC) ([Nielsen](https://arxiv.org/abs/quant-ph/9811053)). Under it, (0.4, 0.4, 0.1, 0.1) cannot become (0.5, 0.25, 0.25, 0) until a (0.6, 0.4) catalyst is borrowed and returned untouched ([Jonathan & Plenio](https://arxiv.org/abs/quant-ph/9905071)).
- **Monogamy.** CKW monogamy separates GHZ from W ([Coffman, Kundu, Wootters](https://arxiv.org/abs/quant-ph/9907047)). Losing one GHZ qubit leaves a separable mixture (C_AB = 0, 3-tangle 1). Losing one W qubit leaves an entangled pair (C_AB = 2/3, 3-tangle 0), computed in [sim_demos.py](<../research_notes/Quantum Unlocked theme deep dive/scripts/sim_demos.py>).

The Werner state ρ = p|Ψ⁻⟩⟨Ψ⁻| + (1−p)𝟙/4 is the master teaching object, because every major threshold sits on one slider. Werner states are entangled for p > 1/3 yet admit a local hidden-variable model for projective measurements when p ≤ 1/2, which was the original proof that entanglement is not Bell nonlocality ([Werner 1989](https://doi.org/10.1103/PhysRevA.40.4277)).

| Property unlocked | Visibility v | Singlet fraction F = (1+3v)/4 | Source |
|---|---|---|---|
| Entangled; teleportation beats the classical 2/3 | > 1/3 | > 0.500 | [Werner](https://doi.org/10.1103/PhysRevA.40.4277); [Horodecki 1999](https://arxiv.org/abs/quant-ph/9807091) |
| Steerable (projective measurements) | > 1/2 | > 0.625 | [Wiseman, Jones, Doherty](https://arxiv.org/abs/quant-ph/0612147) |
| Bell-nonlocal for some inequality | 0.6875–0.6961 (exact value open) | ~0.766–0.772 | [Designolle et al. 2023](https://arxiv.org/abs/2302.04721) |
| Violates CHSH | > 0.7071 | > 0.780 | [Brunner et al.](https://arxiv.org/abs/1303.2849) |
| Distillable by one-way hashing | — | > 0.8107 | [ent_numbers.py](<../research_notes/Quantum Unlocked theme deep dive/scripts/ent_numbers.py>) |

| v | F | Concurrence | Negativity | E_F | Hashing yield | CHSH S | CHSH-game win | Teleport fidelity |
|---|---|---|---|---|---|---|---|---|
| 0.50 | 0.625 | 0.25 | 0.125 | 0.118 | 0 | 1.414 | 0.677 | 0.750 |
| 0.7071 | 0.780 | 0.561 | 0.280 | 0.423 | 0 | 2.000 | 0.750 | 0.854 |
| 0.90 | 0.925 | 0.85 | 0.425 | 0.789 | 0.497 | 2.546 | 0.818 | 0.950 |
| 0.99 | 0.9925 | 0.985 | 0.4925 | 0.978 | 0.924 | 2.800 | 0.850 | 0.995 |

Most tutorials miss a subtle point here. The Bell-nonlocality threshold (~0.69) sits *below* the CHSH threshold (0.7071). States in between are nonlocal only for inequalities with many measurement settings.

Nonlocality turns these thresholds into games:

- **CHSH.** Local models are bounded by S ≤ 2, quantum mechanics by 2√2 (Tsirelson), and no-signaling boxes by 4 ([Tsirelson](https://doi.org/10.1007/BF00417500)). As a game, CHSH wins 75% classically and cos²(π/8) ≈ 85.4% with entanglement ([Cleve et al.](https://arxiv.org/abs/quant-ph/0404076)).
- **GHZ.** The GHZ game goes from 3/4 to 1, and the Mermin gap grows exponentially in n ([Mermin 1990](https://doi.org/10.1103/PhysRevLett.65.1838)).
- **Magic square.** The Mermin–Peres square goes from 8/9 to 1. It is simultaneously a contextuality proof and a pseudo-telepathy game ([Brassard, Broadbent, Tapp](https://arxiv.org/abs/quant-ph/0407221)).
- **PR box.** The box reaching S = 4 shows that no-signaling alone does not explain 2√2 ([Popescu & Rohrlich](https://arxiv.org/abs/quant-ph/9508009)). Information causality recovers it ([Pawłowski et al.](https://arxiv.org/abs/0905.2292)).
- **Loophole-free tests and the Nobel.** Delft measured S = 2.42 ± 0.20 over 245 trials with spins 1.3 km apart ([Hensen et al.](https://arxiv.org/abs/1508.05949)), and the 2022 Nobel recognized the photon experiments ([nobelprize.org](https://www.nobelprize.org/prizes/physics/2022/summary/)).
- **Device-independent QKD** became real in 2022 with trapped ions about 2 m apart at Oxford and atoms 400 m apart in Munich ([Nadlinger et al.](https://arxiv.org/abs/2109.14600); [Zhang et al.](https://arxiv.org/abs/2110.00575)).

Every core protocol reduces to Bell pairs plus Pauli-frame bookkeeping:

- **Teleportation** with a resource of singlet fraction F reaches average fidelity (2F+1)/3, against a classical 2/3 ([Horodecki 1999](https://arxiv.org/abs/quant-ph/9807091)).
- **Swapping** entangles the outer qubits after a Bell measurement on the inner pair ([Żukowski et al.](https://doi.org/10.1103/PhysRevLett.71.4287)).
- **A nonlocal CNOT** costs one ebit plus one classical bit each way ([Eisert et al.](https://arxiv.org/abs/quant-ph/0005101)).

Distillation is the richest topic. BBPSSW twirls the input to Werner form, works for any F > 1/2, and updates F' = [F² + ((1−F)/3)²] / [F² + 2F(1−F)/3 + 5((1−F)/3)²] ([Bennett et al. 1996](https://arxiv.org/abs/quant-ph/9511027)). DEJMPS rotates by Rx(±π/2) instead of twirling. It maps the Bell-diagonal vector (A, B, C, D) = (Φ⁺, Ψ⁻, Ψ⁺, Φ⁻) to A' = (A²+B²)/N, B' = 2CD/N, C' = (C²+D²)/N, D' = 2AB/N, with success probability N = (A+B)² + (C+D)², and converges much faster ([Deutsch et al.](https://arxiv.org/abs/quant-ph/9604039)). From [ent_numbers.py](<../research_notes/Quantum Unlocked theme deep dive/scripts/ent_numbers.py>), with ideal gates:

| F₀ | Round 1 BBPSSW / DEJMPS | Round 2 | Round 3 | Round 4 |
|---|---|---|---|---|
| 0.70 | 0.735 / 0.735 | 0.773 / 0.846 | 0.812 / 0.934 | 0.850 / 0.972 |
| 0.80 | 0.838 / 0.838 | 0.874 / 0.944 | 0.905 / 0.988 | 0.930 / 0.997 |
| 0.90 | 0.926 / 0.926 | 0.947 / 0.989 | 0.963 / 0.999 | 0.974 / 1.000 |

The cost per output pair grows fast. With DEJMPS from F₀ = 0.8, rounds 1 through 4 need about **2.6, 7.0, 15.5 and 31.7** raw pairs per output pair.

Noisy local gates impose a ceiling. One DEJMPS round with 0.5%-error CNOTs takes 0.90 to 0.921, against 0.926 with ideal gates, and **break-even sits near F ≈ 0.985** ([sim_demos.py](<../research_notes/Quantum Unlocked theme deep dive/scripts/sim_demos.py>)). That ceiling is the textbook motivation for nested purification in repeaters ([Briegel et al.](https://arxiv.org/abs/quant-ph/9803056)).

The deepest lesson is noise-tailoring. A bilateral CNOT followed by a Z-parity check catches only bit flips, and it *doubles* phase errors because Z errors propagate from target to control:

| (p_x, p_z) | F₀ | Z-check | X-check (H⊗H first) | Two rounds alternating |
|---|---|---|---|---|
| (0.1, 0) | 0.900 | 0.988 at p=0.82 | 0.820, worse | 0.976 |
| (0, 0.1) | 0.900 | 0.820, worse | 0.988 at p=0.82 | 0.976 |
| (0.1, 0.1) | 0.810 | no gain | no gain | 0.931 |
| (0.05, 0.2) | 0.760 | 0.678, worse | 0.852 | 0.880 (X first) / 0.814 (Z first) |

IonQ's iQuHACK 2026 challenge is built on exactly this lesson. Teams claimed graph edges by submitting OpenQASM 3 LOCC circuits that distill up to 8 noisy Bell pairs with secret X/Z flip noise ([game handbook](https://raw.githubusercontent.com/iQuHACK/2026-IonQ/main/game_handbook.md)):

- Pairs were nested from the outside in, and two-qubit gates could not cross the Alice/Bob boundary.
- The server post-selected on a player-chosen flag bit.
- Teams started with a 75-pair budget, and failed claims cost nothing.
- Claim strength on a vertex weighted each edge's fidelity × success probability by 1/√rank.

The handbook's own N = 2 example is a Z-check, so on a phase-noise edge it *lowers* fidelity. BYU's team says it won by matching circuits to each edge's noise type after organizers reset a leaderboard that other teams had exploited through a loophole. A UAM team also claims first place, crediting BBPSSW and DEJMPS; the two claims may reflect separate divisions ([BYU Universe](https://universe.byu.edu/campus/byu-students-win-mit-quantum-hackathon-in-debut-appearance); [UAM](https://www.uam.es/eps/escuela/noticias/estudiantes-eps-ganan-iquhack2026)). Do not clone the game. Build the tool that explains *why* it rewards noise-tailoring.

Repeaters and QKD supply real-world scale:

- **Repeaters.** BDCZ nested swapping plus purification gives polynomial overhead in distance ([Briegel et al.](https://arxiv.org/abs/quant-ph/9803056)). Repeater generations progress from two-way heralded purification to one-way, error-corrected links ([Muralidharan et al.](https://arxiv.org/abs/1509.08435)).
- **The PLOB bound** caps direct-transmission capacity at −log₂(1−η) ≈ 1.44η bits per channel use ([Pirandola et al.](https://arxiv.org/abs/1510.08863)). At 0.2 dB/km that gives **1.45×10⁻² at 100 km, 1.44×10⁻⁶ at 300 km and 1.44×10⁻¹⁰ at 500 km** ([ent_numbers.py](<../research_notes/Quantum Unlocked theme deep dive/scripts/ent_numbers.py>)).
- **Heralding.** Linear-optics Bell measurements succeed at most 50% of the time ([Calsamiglia & Lütkenhaus](https://arxiv.org/abs/quant-ph/0007058)).
- **BB84.** Full intercept-resend attacks produce a 25% QBER, and the Shor–Preskill rate 1 − 2h(Q) stays positive below Q ≈ 11% ([Shor & Preskill](https://arxiv.org/abs/quant-ph/0003004)).
- **Beyond the bound.** Twin-field QKD scales as √η and beats PLOB, reaching 1,002 km of fiber ([Liu et al.](https://doi.org/10.1103/PhysRevLett.130.210801)).

The 2024–2026 milestones give timely anchors:

- **Oxford, 2025:** a teleported CZ gate at **86%** fidelity and distributed Grover at **71%** across two ion modules ([ORA](https://ora.ox.ac.uk/objects/uuid:e8e788d3-e15c-48a3-ae23-107ad7d43ea2)).
- **USTC, Nature, April 2026:** remote ion–ion entanglement over 10 km whose **~550 ms coherence outlived its ~450 ms generation time**, plus DI-QKD producing 1,917 key bits from ~4.05×10⁵ Bell pairs ([Nature](https://www.nature.com/articles/s41586-026-10177-4); [arXiv:2602.08472](https://arxiv.org/abs/2602.08472)).
- **USTC, PRL, August 2026:** memory–memory entanglement through 420 km of fiber, at 78.7 dB loss and concurrence 0.046 ± 0.022. It beats the repeaterless limit beyond about 320 km, though both memories sat in one lab with about 20 km of deployed fiber ([arXiv:2504.05660](https://arxiv.org/pdf/2504.05660); [PostQuantum](https://postquantum.com/quantum-research/420-km-quantum-memory-entanglement/)).

IonQ has assembled a vertically integrated networking stack:

- ion–photon entanglement (February 2024) and remote ion–ion entanglement (October 2024) ([IonQ blog](https://ionq.com/blog/enabling-networked-quantum-computing-with-ion-photon-entanglement); [BusinessWire](https://businesswire.com/news/home/20241003150527/en/IonQ-Demonstrates-Remote-Ion-Ion-Entanglement-a-Significant-Milestone-in-Developing-Networked-Quantum-Systems-at-Scale/));
- telecom frequency conversion (September 2025) ([The Quantum Insider](https://thequantuminsider.com/2025/09/23/ionq-demonstrates-quantum-frequency-conversion-to-telecom-wavelengths/));
- a photonic interconnect between two commercial trapped-ion systems on **April 14, 2026**, with no fidelities disclosed ([IonQ](https://ionq.com/news/ionq-achieves-key-photonic-interconnect-milestone-demonstrating-networked-quantum-systems-using-entanglement));
- acquisitions spanning Qubitekk, ID Quantique, Lightsynq memories and Capella satellites ([eeNews](https://www.eenewseurope.com/en/ionq-buys-lightsynq-capella-for-satellite-qkd));
- a Tennessee quantum communications center to host an embedded quantum memory (August 2026) ([IonQ](https://ionq.com/news/ionq-and-epb-partner-to-launch-the-tennessee-quantum-communications-research-center));
- national QKD networks in Switzerland, Slovakia and Romania, reported with Q1 2026 results ([IonQ Q1 2026](https://www.ionq.com/news/ionq-announces-first-quarter-2026-financial-results)).

Simulated at 0.5% two-qubit error (from [sim_demos.py](<../research_notes/Quantum Unlocked theme deep dive/scripts/sim_demos.py>)), every core protocol keeps a large margin. The interesting teaching content is therefore *how* noise erodes advantage, not *whether* advantage exists:

| Demo | Qubits | Entangling gates | Noisy result | Classical bound |
|---|---|---|---|---|
| CHSH (4 setting circuits) | 2 | 1 | S = 2.750 (game 0.844) | 2 (0.75) |
| Teleportation, deferred-measurement corrections | 3 | 4 | 0.981 | 2/3 |
| Teleportation, Pauli-frame post-processing | 3 | 2 | 0.988 | 2/3 |
| Superdense coding | 2 | 2 | 0.980 | — |
| GHZ game | 3 | 2 | 0.9775 | 0.75 |
| Magic-square game | 4 | ≤4 | 0.979 (worst cell 0.967) | 0.889 |
| Swapping chain, 1 → 5 → 14 links | 2 → 10 → 28 | 2n−1 | F = 0.995 → 0.955 → 0.876 | — |
| GHZ fidelity at n = 12 / 20 / 29 (with 0.5% readout) | n | n−1 | 0.855 / 0.768 / 0.682 | Witness 0.5 |

Under intercept-resend, E91's CHSH value collapses to √2. The asymptotic device-independent key rate is **0.71 bits per round at S = 2.75** ([sim_demos.py](<../research_notes/Quantum Unlocked theme deep dive/scripts/sim_demos.py>)).

Three design tricks make all of this IonQ-legal:

- **Pauli-frame post-processing** replaces feed-forward. Flip Bob's outcome by m₂ for Z, by m₁ for X and by m₁⊕m₂ for Y. This keeps protocols genuinely LOCC and uses fewer gates.
- **Ancilla-purified noise** keeps simulation as a statevector. An Ry(θ) ancilla controlling an X on Bob's qubit realizes a flip with probability sin²(θ/2), so tunable noise runs on the 24-qubit browser simulator and on IonQ as-is.
- **A "referee" Bell measurement** reads output fidelity in one circuit, because P(Φ⁺) = F. Label it as a non-LOCC check.

### Algorithms and complexity: every algorithm is a polynomial

Every core algorithm follows one pattern. A query writes information into **phases** through kickback, and a structured transform makes the paths to wrong answers interfere destructively ([Cleve et al. 1998](https://arxiv.org/abs/quant-ph/9708016)). Entanglement alone is not enough: Clifford circuits are simulable, and so are weakly entangled pure-state computations ([Jozsa & Linden](https://arxiv.org/abs/quant-ph/0201143)).

The oracle algorithms carry caveats learners need:

- **Deutsch–Jozsa** beats deterministic algorithms (1 query vs 2^(n−1)+1) but not randomized ones, which need O(1) queries. This is a frequent teaching error ([de Wolf notes](https://arxiv.org/abs/1907.09415)).
- **Bernstein–Vazirani** gives only a polynomial gap ([Bernstein & Vazirani](https://doi.org/10.1137/S0097539796300921)).
- **Simon's problem** needs Ω(2^(n/2)) classical queries but only O(n) quantum runs plus Gaussian elimination over GF(2). It is the under-taught bridge to Shor ([Simon](https://doi.org/10.1137/S0097539796298637)).
- **The QFT** uses n(n−1)/2 controlled phases. Approximating it to b ~ log n bits suffices ([Coppersmith](https://arxiv.org/abs/quant-ph/0201067)). Its coefficients sit in amplitudes, so it is not a faster FFT ([Aaronson notes](https://www.scottaaronson.com/qclec.pdf)).

For the hackathon's constraints, the least-taught and most useful fact is that **phase and amplitude estimation need neither the QFT nor feed-forward**:

- Kitaev's single-ancilla Hadamard tests, robust phase estimation and QCELS are non-adaptive and reach Heisenberg scaling ([Kimmel, Low, Yoder](https://arxiv.org/abs/1502.02677); [Ding & Lin](https://arxiv.org/abs/2211.11973)).
- Maximum-likelihood amplitude estimation runs Q^m A|0⟩ on a fixed schedule with P(good) = sin²((2m+1)θ). It needs no controlled Q ([Suzuki et al.](https://arxiv.org/abs/1904.10246)).
- Iterative QPE and iterative amplitude estimation are adaptive, so they need feed-forward or several jobs ([Dobšíček et al.](https://arxiv.org/abs/quant-ph/0610214); [Grinko et al.](https://arxiv.org/abs/1912.05559)).
- "Compiled" phase-estimation demos that precompute U^(2^j) effectively assume the answer; Smolin, Smith and Vargo showed such shortcuts can "factor" any number ([Nature 2013](https://arxiv.org/abs/1301.7007)).

Grover search is a rotation by 2θ in a plane: after k iterations the good amplitude is sin((2k+1)θ), and ~(π/4)√(N/M) iterations are optimal ([Grover](https://arxiv.org/abs/quant-ph/9605043)). Ω(√N) is a hard floor, and NP ⊄ BQP relative to a random oracle ([BBBV](https://arxiv.org/abs/quant-ph/9701001)). Fixed-point amplitude amplification avoids overshooting the target with optimal query scaling, using Chebyshev-derived phases ([Yoder, Low, Chuang](https://arxiv.org/abs/1409.3305)). Quadratic speedups are unlikely to pay off on early fault-tolerant machines ([Babbush et al.](https://arxiv.org/abs/2011.04149)).

Grover connects directly to QSP. With a = sin θ, T_{2k+1}(a) = (−1)^k sin((2k+1)θ), so **k Grover iterations output an odd Chebyshev polynomial of the initial amplitude**, which is a QSP polynomial. Bernstein's inequality bounds any degree-d polynomial bounded by 1 at |P(1/√N)| ≤ d/√N. Reaching constant success within QSP-type algorithms therefore forces d = Ω(√N): a slider-sized picture of the lower bound, though not a proof of the general theorem.

QSP is the unifying framework ([Low, Yoder, Chuang](https://arxiv.org/abs/1603.03996); [Martyn et al., Grand Unification](https://arxiv.org/abs/2105.02859)):

- **The theorem.** A single-qubit sequence of signal rotations W(a) interleaved with Z phases realizes polynomial P exactly when three conditions hold: deg P ≤ d, P has parity d mod 2, and |P|² + (1−a²)|Q|² = 1 on [−1, 1].
- **Algorithms become polynomial choices.** Search, phase estimation, Hamiltonian simulation and matrix inversion are, respectively, a sign function, Chebyshev or threshold polynomials, a Jacobi–Anger expansion of e^(−iτx), and 1/x on [1/κ, 1].
- **Phase finding is solved numerically** past degree 10,000 at error below 10⁻¹² ([Dong, Meng, Whaley, Lin](https://arxiv.org/abs/2002.11649)). pyqsp exists, but whether it installs in Pyodide is unverified, and its TensorFlow mode cannot run there ([pyqsp](https://github.com/ichuang/pyqsp)).
- **QSVT** lifts the same phases to singular values of a block-encoded matrix ([Gilyén et al.](https://arxiv.org/abs/1806.01838)). Degree costs are O(κ log(κ/ε)) for inversion, O(log(1/ε)/δ) for the sign function, and |τ| plus a log term for simulation.
- **HHL's fine print** still applies: fast state loading, sparsity and conditioning, a quantum-state output, and comparison against the best classical algorithm for the same sampling task ([Aaronson, Nature Physics 2015](https://www.scottaaronson.com/papers/qml.pdf)).

Hamiltonian simulation and walks have their own exact results:

- **Trotter error** scales with nested commutators, (t²/2r)‖[A,B]‖ at first order ([Childs et al., PRX 2021](https://arxiv.org/abs/1912.08854)).
- **qDRIFT's** gate count λ²t²/ε does not depend on the number of terms ([Campbell](https://arxiv.org/abs/1811.08017)).
- **Generic Hamiltonians** cannot be fast-forwarded ([Berry et al.](https://arxiv.org/abs/quant-ph/0508139)).
- **Quantum walks** give an exponential oracle speedup on glued trees ([Childs et al. 2003](https://arxiv.org/abs/quant-ph/0209131)). Decoherence turns their ballistic spreading diffusive ([Kendon](https://arxiv.org/abs/quant-ph/0606016)).

Variational methods are best taught as a story and its counter-story:

- **The story.** QAOA at p=1 guarantees a 0.6924 approximation ratio on 3-regular MaxCut ([Farhi et al.](https://arxiv.org/abs/1411.4028)).
- **The limits.** Locality and symmetry obstruct low-depth QAOA ([Bravyi et al.](https://arxiv.org/abs/1910.08980)).
- **What survives.** Fixed linear-ramp QAOA ran on IonQ, Quantinuum and IBM up to 109 qubits and p = 100 ([npj QI 2025](https://arxiv.org/abs/2405.09169)).
- **Barren plateaus.** Gradients vanish for 2-designs ([McClean et al.](https://arxiv.org/abs/1803.11173)), for global costs ([Cerezo et al. 2021](https://arxiv.org/abs/2001.00550)) and under noise ([Wang et al.](https://arxiv.org/abs/2007.14384)). Loss variance scales as 1/dim(𝔤) of the dynamical Lie algebra ([Ragone et al.](https://arxiv.org/abs/2309.09342)).
- **The punchline.** A 2025 Nature Communications perspective argues that provable absence of barren plateaus often implies classical simulability after a data-acquisition phase ([Cerezo et al.](https://arxiv.org/abs/2312.09121v3)).
- **Dequantization.** Tang's result removed the exponential separation for recommendation systems ([Tang](https://arxiv.org/abs/1807.04271)), and quantum kernels concentrate exponentially ([Thanasilp et al.](https://arxiv.org/abs/2208.11060)).
- **Classical shadows** predict many observables from few randomized snapshots, with a shadow norm of 3^k for k-local Paulis ([Huang, Kueng, Preskill](https://arxiv.org/abs/2002.08953)).

The frontier is a ready-made "claim, then classical response" lesson:

- **DQI** reduces optimization to decoding and is superpolynomially faster on Optimal Polynomial Intersection ([Jordan et al., Nature 2025](https://arxiv.org/abs/2408.08292v3)). Follow-ups found no advantage for MaxCut ([Parekh](https://arxiv.org/abs/2509.19966)), an overlap-gap obstruction plus classical AMP beating DQI on random instances ([arXiv:2509.14509](https://arxiv.org/html/2509.14509v1)), and MCMC reproducing its ratios ([arXiv:2607.28120](https://arxiv.org/abs/2607.28120)).
- **Advantage claims are contested.** Quantum Echoes claims a verifiable 13,000× OTOC speedup ([Quantum Computing Report](https://quantumcomputingreport.com/google-quantum-ai-achieves-verifiable-quantum-advantage-on-willow-chip-with-quantum-echoes-algorithm/)). D-Wave's 2025 simulation claim drew tensor-network rebuttals ([Tindall et al.](https://arxiv.org/abs/2503.05693v2)). Certified randomness produced 71,313 bits against a restricted adversary using ~1.1 EFLOPS of verification ([Liu et al.](https://arxiv.org/abs/2503.20498)).
- **Cryptanalysis is timely.** Google's March 2026 whitepaper put ECDLP-256 at **under 500,000 physical qubits** and withheld the circuits behind a zero-knowledge proof ([The Quantum Insider](https://thequantuminsider.com/2026/03/31/q-day-just-got-closer-three-papers-in-three-months-are-rewriting-the-quantum-threat-timeline/)). That is the subject of Qollab's newest announcement.

On complexity, BQP escapes the polynomial hierarchy relative to an oracle via Forrelation ([Raz & Tal](https://eccc.weizmann.ac.il/report/2018/107/)). Exponential query separations need promises or structure, since total functions satisfy D(f) = O(Q(f)⁴) ([Aaronson et al.](https://arxiv.org/abs/2010.12629)). Guided local Hamiltonian estimation is BQP-complete, so QMA's hardness lies in state preparation ([Gharibian & Le Gall](https://arxiv.org/abs/2111.02474)). NLTS was proved using good qLDPC codes ([Anshu, Breuckmann, Nirkhe](https://arxiv.org/abs/2206.13228)).

The table below sizes the strongest algorithm demos. The two-qubit counts are hand-derived from IonQ's native-gate definitions ([IonQ native gates](https://docs.ionq.com/guides/getting-started-with-native-gates)) and must be confirmed with the transpiler. The derivations use five facts:

- any controlled phase costs one ZZ;
- XX+YY hopping costs 2 native gates;
- a weight-w Z rotation costs 2w−3 native gates;
- a dense 4-variable phase oracle costs at most 23;
- estimated success is 0.995 to the power of the two-qubit gate count.

| Demo | Qubits | Max 2Q gates | Est. success | Verdict |
|---|---|---|---|---|
| QSP polynomial studio | 1 per signal point, up to 29 in one circuit | 0 | Limited by SPAM and shot noise (~1.6% at 1,000 shots) | Excellent |
| QSVT on a 2+1-qubit LCU block encoding | 3 (up to 9 copies in parallel) | 27 / 45 / 63 at d = 9 / 15 / 21 | 0.87 / 0.80 / 0.73 | Best at d ≤ 15 |
| Trotter TFIM, n = 6 | 6 | 5 per step, ≤ 100 | 0.97 → 0.61 | Core lesson |
| All-to-all Ising, n = 6 | 6 | 15 per step | ~0.93 per step | IonQ showcase |
| Textbook QPE, t = 8 | 9 | 36 | 0.83 | Fine |
| Hadamard-test phase estimation | 2 each, 14 in parallel | 1 each | ~0.99 | Excellent |
| MLAE, realistic loader | ~5 (5 in parallel) | 60–90 | 0.74–0.64 | Needs a noise-aware fit |
| Forrelation, n = 4 | 4 | ≤ 46 | 0.79 | Runnable Raz–Tal |
| Simon, n = 4 | 8 | ~8 | 0.96 | Bridge to Shor |
| Linear-ramp QAOA, 8 nodes | 8 | 12p, ≤ 96 | 0.94 → 0.62 | One job, no optimizer |

### Foundations, noise and open systems: make the invisible computable

The Bloch ball, ρ = ½(I + r·σ), is exact for one qubit and fails for two ([Nielsen & Chuang](https://doi.org/10.1017/CBO9780511976667)). Counting parameters makes the failure concrete. A pure two-qubit state has 6 real parameters but two Bloch spheres hold only 4, and a mixed state has 15 against 6. The missing 9 are the correlation matrix T, which is why a Bell state shows two zero-length Bloch vectors ([Preskill notes](http://theory.caltech.edu/~preskill/ph229/)).

General measurement is best taught through Kraus operators and POVMs ([Nielsen & Chuang](https://doi.org/10.1017/CBO9780511976667)), and several experiments become IonQ-legal circuits:

- **Weak measurement.** A controlled-RY(θ) onto an ancilla gives Kraus operators M₀ = |0⟩⟨0| + cos(θ/2)|1⟩⟨1| and M₁ = sin(θ/2)|1⟩⟨1|. That is a measurement-strength slider whose unconditional back-action is dephasing.
- **The Zeno effect without dynamic circuits.** Split a π rotation into N steps, each followed by a CNOT onto a fresh ancilla. Survival is cos^(2N)(π/2N): **0.61 at N=5, 0.78 at N=10, 0.95 at N=50**, against ~5% accumulated gate error at N=10. The original trapped-ion demonstration used up to 64 pulses ([Itano et al. 1990](https://doi.org/10.1103/PhysRevA.41.2295)).
- **Contextuality.** Cabello's Peres–Mermin inequality bounds non-contextual models at 4, while quantum mechanics gives 6 for every state. It has been violated with trapped ions ([Cabello](https://arxiv.org/abs/0808.2456); [Kirchmair et al.](https://arxiv.org/abs/0904.1655)).
- **Tomography versus shadows.** Ten-qubit Pauli tomography needs **3¹⁰ = 59,049 settings**, against tens of thousands of shadow snapshots for all 2-local observables ([James et al.](https://arxiv.org/abs/quant-ph/0103121); [Huang, Kueng, Preskill](https://arxiv.org/abs/2002.08953)).

Every physical noise process is a CPTP map with Kraus, Choi and Stinespring forms ([Watrous](https://cs.uwaterloo.ca/~watrous/TQI/)). On the Bloch ball each single-qubit channel is an affine contraction you can animate exactly ([Nielsen & Chuang §8.3](https://doi.org/10.1017/CBO9780511976667)):

| Channel | Action on Bloch vector (x, y, z) | Teaching point |
|---|---|---|
| Amplitude damping | (√(1−γ)x, √(1−γ)y, γ + (1−γ)z) | Non-unital: pulls toward \|0⟩, not the center |
| Phase damping | x and y shrink by √(1−λ) | z untouched |
| Bit flip | x kept; y and z shrink by 1−2p | Not "just random flips" |

Amplitude damping is exactly a two-qubit circuit: a controlled-RY(θ) onto an ancilla, then a CNOT back, gives γ = sin²(θ/2). Dropping the CNOT gives pure phase damping. The lesson is that noise is entanglement with an environment you do not measure. The transpose map shows the difference between positive and completely positive maps: its Choi matrix has eigenvalue −1, and applied to half a Bell pair it produces a "density matrix" with eigenvalue −½. That is the natural door to the partial-transpose criterion.

The decisive noise lesson is coherent versus stochastic error. A coherent error's average infidelity scales as ε² while its worst case scales as ε ([Sanders et al.](https://arxiv.org/abs/1501.04932); [Kueng et al.](https://arxiv.org/abs/1510.05653)). Repeat RX(0.02) 100 times and the coherent infidelity is sin²(1) ≈ **0.71**. The Pauli-twirled version with the same per-gate fidelity gives about **0.01**, roughly 70× less. That gap is what randomized compiling fixes ([Wallman & Emerson](https://arxiv.org/abs/1512.01098)).

Mitigation's cost grows exponentially with circuit size times error rate ([Cai et al., RMP 2023](https://arxiv.org/abs/2210.00921); [Quek et al.](https://arxiv.org/abs/2210.11505)). IonQ's own documentation sets three limits on what a noise simulation can show:

- **Debiasing** is on by default on hardware, but **no IonQ noise-model simulation includes it** ([Microsoft Learn](https://learn.microsoft.com/azure/quantum/provider-ionq); [IonQ noise models](https://docs.ionq.com/guides/simulation-with-noise-models)).
- **The documented legacy model** is a single depolarizing channel after each gate, with forte-1 at 1q = 0.000267 and 2q = 0.004949. IonQ describes the models used after September 2025 as more complex, and they remain undocumented ([IonQ noise models](https://docs.ionq.com/guides/simulation-with-noise-models)).
- **The depolarizing convention is unstated.** For two qubits, Aer's parameter λ and the average infidelity r differ by r = 3λ/4, a 33% gap, so state which convention your tool uses ([Qiskit Aer noise API](https://qiskit.github.io/qiskit-aer/apidocs/aer_noise.html)).

### Trapped ions: the phonon bus nobody animates

IonQ's Forte and Aria qubits are hyperfine clock states of ¹⁷¹Yb⁺ split by about **12.6428 GHz**. They are cooled and detected on the 369.5 nm transition and read out by fluorescence ([Olmschenk et al.](https://arxiv.org/abs/0708.0657); [Microsoft Learn](https://learn.microsoft.com/azure/quantum/provider-ionq)). Tempo uses barium, though the isotope is not public ([Quantum Computing Report](https://quantumcomputingreport.com/ionq-announces-regulatory-approval-for-oxford-ionics-acquisition-and-provides-a-roadmap-update-at-its-2025-analyst-day-meeting/)).

The trap and mechanics:

- An RF Paul trap gives a time-averaged pseudopotential.
- An N-ion chain has 3N normal modes, and the transverse modes crowd together as N grows ([James 1998](https://arxiv.org/abs/quant-ph/9702053)).
- The Lamb–Dicke parameter η = Δk√(ħ/2Mω) sets the sideband strengths: ηΩ√n for the red sideband and ηΩ√(n+1) for the blue ([Leibfried et al., RMP 2003](https://doi.org/10.1103/RevModPhys.75.281)).
- For Yb at 3 MHz with 355 nm Raman beams, η ≈ 0.11. Doppler cooling leaves n̄ ≈ 3, already inside the Lamb–Dicke regime.

The Mølmer–Sørensen gate is the story nobody animates ([Sørensen & Mølmer](https://arxiv.org/abs/quant-ph/0002024); [Lee et al.](https://arxiv.org/abs/quant-ph/0505203)):

1. A bichromatic drive detuned symmetrically from the red and blue sidebands creates a spin-dependent force.
2. The propagator is exactly U(t) = D(α(t)S_φ)·exp(−iΦ(t)S_φ²).
3. Each spin eigenstate traces a circle in phase space. At τ = 2πK/δ the loops close, leaving a pure spin–spin phase Φ = 2πK(ηΩ/δ)².
4. For two ions, |++⟩ and |−−⟩ circle in opposite directions while |+−⟩ and |−+⟩ stay at the origin, and the phase difference *is* the entanglement.
5. A thermal motional state only translates the circles, so the enclosed area and the gate are unchanged. That is the "hot-ion" insensitivity.

A mistuned δ leaves the loops open and the spin entangled with the motion. Simulating two qubits with ~20 Fock levels (an 80-dimensional space) in scipy shows the resulting purity loss directly. Longer chains need amplitude- or frequency-modulated pulses that close every mode's loop ([Choi et al.](https://arxiv.org/abs/1401.1575)), which is the physical reason the field moved to QCCD shuttling, electronic control and photonic links.

Native gates are measured in turns, where 1 turn = 2π ([IonQ native gates](https://docs.ionq.com/guides/getting-started-with-native-gates)). GPi(φ), GPi2(φ) and a virtual Z act on single qubits. Aria adds MS(φ₀, φ₁), and Forte adds ZZ(θ) = exp(−iπθ Z⊗Z). Native circuits bypass IonQ's compiler and have debiasing off by default. The following identities were derived and checked numerically:

| Identity | Consequence |
|---|---|
| MS(0,0) = RXX(π/2); ZZ(θ) = RZZ(2πθ) | One native gate per Ising term |
| CZ ≅ ZZ(0.25) plus virtual Z(−0.25) on each qubit | One native gate per CZ or CNOT |
| CP(λ) ≅ one ZZ with \|θ\| = λ/4π plus virtual Z | A QFT costs n(n−1)/2 ZZ gates and no SWAPs |
| H = GPi(0)·GPi2(0.25); GPi2(0) = RX(π/2), GPi2(0.25) = RY(π/2), GPi2(0.5) = RX(−π/2) | Trust the matrix; one model summary misstated GPi2(0.5) |
| ZZ commutes with virtual Z | Phase propagation passes straight through Forte's entangler; MS must absorb it |

For an 8-qubit QFT, IonQ needs **28 ZZ gates**, an all-to-all CZ basis 56, and a linear nearest-neighbor layout about 84. At 0.995 per gate that is **0.87 vs 0.76 vs 0.66** success. A connectivity comparison on real hardware already favored the ion trap ([Linke et al., PNAS](https://arxiv.org/abs/1702.01852)).

Specifications for the narrative:

| System | Source | Key figures |
|---|---|---|
| Aria | Azure | T1 10–100 s, T2 ~1 s, 135 µs single-qubit gates, 600 µs two-qubit gates ([Microsoft Learn](https://learn.microsoft.com/azure/quantum/provider-ionq)) |
| Forte | Vendor | 0.4% two-qubit error ([IonQ Forte](https://ionq.co/quantum-systems/forte)) |
| Forte Enterprise 1 | Independent measurement | 99.15% two-qubit fidelity, 650 µs gates ([arXiv:2603.03801](https://arxiv.org/abs/2603.03801)) |
| R&D prototype (Oct 2025) | IonQ, company-reported | >99.99% two-qubit fidelity with electronic qubit control ([IonQ IR](https://investors.ionq.com/news/news-details/2025/IonQ-Achieves-Landmark-Result-Setting-New-World-Record-in-Quantum-Computing-Performance/default.aspx)) |

On Aria, T2 divided by gate time is about 1.7×10³, the same order as transmons. The belief that ions are worse because they are slow is a misconception. Ions win on error per gate and connectivity, and lose on wall-clock time ([Beverland et al.](https://arxiv.org/abs/2211.07629)).

### The niche sweep: sixteen topics sized for 29 qubits

Most advanced topics reduce to a few objects already in `qiskit.quantum_info`: Pauli expectations, reduced states, tableaus and Trotterized ZZ/XX evolution. IonQ's arbitrary-angle, all-to-all ZZ makes long-range models unusually cheap. The common pedagogical trap is that hardware noise mimics the physics being studied, so every demo needs a control that separates the two.

| Topic | Core fact | IonQ-sized demo and expected behavior |
|---|---|---|
| Gottesman–Knill | Clifford circuits are tableau-simulable ([Aaronson & Gottesman](https://arxiv.org/abs/quant-ph/0406196)) | Grow a 1,000-qubit Clifford circuit instantly, then add one T gate (Qollab's showcase already does this, so avoid) |
| Magic (stabilizer Rényi entropy) | M₂ is computable from Pauli expectations ([Leone, Oliviero, Hamma](https://arxiv.org/abs/2106.12587)) | \|T⟩ gives M₂ = log₂(4/3) ≈ 0.415; 4⁸ Paulis is browser-feasible |
| Measurement-based QC | Cluster state plus adaptive measurements is universal ([Raussendorf & Briegel](https://arxiv.org/abs/quant-ph/0010033)) | 4–5-qubit cluster with 3–4 ZZ gates; post-select non-adaptive branches to show *why* feed-forward is needed |
| ZX-calculus | Complete graphical rewriting ([van de Wetering](https://arxiv.org/abs/2012.13966)) | pyzx reduced an 8-qubit depth-200 circuit from 345 to 58 vertices in 5.27 s in Pyodide; ZZ maps to a phase gadget |
| Tensor networks | Entanglement entropy ≤ log χ ([Schollwöck](https://arxiv.org/abs/1008.3477)) | 12-qubit area law vs volume law via partial_trace |
| OTOCs and scrambling | Operator spreading ([Swingle et al.](https://arxiv.org/abs/1602.06271)) | ~10 qubits, ~54 2Q gates, ~0.76 success; normalize by the no-butterfly echo or noise looks like scrambling |
| Hayden–Preskill | Verified scrambling via teleportation on 7 Yb ions ([Landsman et al.](https://arxiv.org/abs/1806.02807)) | 7 qubits, 15–20 2Q gates, ~0.9 success |
| Many-body localization | Disorder blocks thermalization ([Smith et al.](https://arxiv.org/abs/1508.07026)) | ~270 2Q gates, too deep for hardware; noiseless only |
| Discrete time crystals | Period doubling in 10 Yb ions ([Zhang et al.](https://arxiv.org/abs/1609.08684)) | 20 Floquet periods ≈ 180 ZZ; compare with an ε = 0 control |
| Metrology | GHZ probes reach Heisenberg scaling; uncorrelated dephasing erases the gain ([Huelga et al.](https://arxiv.org/abs/quant-ph/9707014)) | Parity contrast ~0.95 / 0.90 / 0.85 at N = 10 / 20 / 29; add idle dephasing, which IonQ's model lacks |
| Hamiltonian learning | Robust phase estimation calibrates gates ([Kimmel et al.](https://arxiv.org/abs/1502.02677)) | Repeat ZZ(0.25+δ) 1–64 times; 1/K precision until 0.995⁶⁴ ≈ 0.73 caps it |
| Schwinger model | Pair creation on 4 Ca⁺ ions ([Martinez et al.](https://arxiv.org/abs/1605.04570)) | ~12 2Q gates per step on 4 qubits; 10 steps ≈ 0.55 |
| Long-range Ising | J ∝ 1/\|i−j\|^α, tunable α ([Porras & Cirac](https://arxiv.org/abs/quant-ph/0401102); [Richerme et al.](https://arxiv.org/abs/1401.5088)) | N = 8: 28 ZZ per step, 4 steps ≈ 0.57; α slider shows light cones |
| Many-body scars | Revivals from Néel states ([Bernien et al.](https://arxiv.org/abs/1707.04344)) | Noiseless PXP at N = 10–12 |
| Thermodynamics | Landauer bound k_BT ln 2 ([Bérut et al.](https://doi.org/10.1038/nature10872)) | Collision-model thermalization; coherent Maxwell demon |
| PQC vs QKD | FIPS 203/204/205 finalized Aug 13, 2024 ([NIST](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards)); RSA/ECC deprecation proposed by 2030 ([NIST IR 8547](https://csrc.nist.gov/pubs/ir/8547/ipd)) | BB84 plus a resource-estimate slider separating the threat from the two responses |

## Qollab's browser runtime rewards exact math and one batched backend call

### The bridge: JSON strings, callPromising, one run

A top-level `index.html` plus `main.js` makes a JS project, which renders in a sandboxed iframe above the console. Files inside folders do not count toward that detection. The runtime places `index.html` inside the body, so `<script>` tags in it never run, and `main.css` is the only stylesheet loaded ([Runtime environment](https://qollab.xyz/learn/docs/runtime-environment)).

The bridge works like this ([JS / Qiskit projects](https://qollab.xyz/learn/docs/js-qiskit-projects)):

- `main.js` imports your Python modules by dotted name, using `import * as svc from 'pkg.module'`. A default import gives `undefined`.
- Calls go through `.callPromising()` or `.callPromisingKwargs()`, and results convert with `.toJs()`.
- A plain synchronous call fails on IonQ with an XHR `ConnectionError`.
- Python `print()` inside a function called from JS never reaches the console.
- Complex statevectors must be split into real and imaginary lists on the Python side ([interactive-bloch-sphere](https://qollab.xyz/u/qollab/interactive-bloch-sphere)).

The sandbox imposes further limits ([Runtime environment](https://qollab.xyz/learn/docs/runtime-environment)):

- **File access.** JavaScript cannot fetch project files. Python loads only files whose paths appear as plain string literals; f-strings and `os.path.join` raise `OSError`.
- **Storage.** There is no localStorage, sessionStorage, IndexedDB or cookies.
- **Network.** Only GET requests are allowed, with `Origin: null`. XHR, WebSockets and web workers are unavailable.
- **Size.** A project holds up to 100 files of 2 MB each.
- **Run form.** JS projects get no `main()` parameter form.

The two official reference projects, QCFlows and the Quantum Hackathon Soundtrack, show the playbook to copy ([QCFlows](https://qollab.xyz/u/qollab/qcflows-multifile); [Soundtrack](https://qollab.xyz/u/qollab/quantum-hackathon-soundtrack)):

- Pass only JSON strings across the boundary.
- Poll for the DOM every 150 ms before touching it.
- Make the single `backend.run` call from JS.
- End `main.js` with `await new Promise(() => {})`, because remote IonQ backends are reachable only while `main.js` is still running.
- Convert counts from a `Map` to a plain object.
- Read the backend name inside try/catch.
- Ship real IonQ Forte measurements as `data/forte_takes.json`.
- Label every result's source, and fall back to ideal sampling with a visible message if the job fails.

The `backend` is injected and real, and whoever presses Run picks it ([Python / Qiskit projects](https://qollab.xyz/learn/docs/python-qiskit-projects); [Compute backends](https://qollab.xyz/learn/docs/compute-backends)):

| Choice | Engine | Max qubits |
|---|---|---|
| Built-in | Qollab-patched Qiskit `BasicSimulator` (einsum, 24-qubit statevector, 2,048-qubit Clifford path, `seed_simulator`) | 24 |
| AWS Braket local | `StateVectorSimulator` | 25 |
| IBM noise models | Fake backends on Aer, in-browser | 120–156 |
| IonQ remote simulators | IonQ cloud noise models | Aria 25, Forte 29 |
| IonQ hardware | Forte 1 / Forte Enterprise 1 | 36 |

The Qollab Qiskit fork makes three changes that affect your code ([qollabxyz/qiskit commits](https://api.github.com/repos/qollabxyz/qiskit/commits?per_page=15); [basic_simulator.py](https://raw.githubusercontent.com/qollabxyz/qiskit/main/qiskit/providers/basic_provider/basic_simulator.py)):

- Rust code runs single-threaded.
- `job.get_counts()` raises an error on non-IonQ backends.
- `seed_simulator` is supported on the built-in simulator.

Two primitive and backend pitfalls follow. **`BackendSamplerV2` silently returns all zeros on IonQ.** `BackendEstimatorV2` works everywhere, but on IonQ you get only one call per run ([Primitives](https://qollab.xyz/learn/docs/primitives)). So use `job.result().get_counts()`, and handle the list-of-dicts case.

There is one unresolved conflict to test on night one. The docs say to pass every circuit to a single `backend.run` call ([Runtime environment](https://qollab.xyz/learn/docs/runtime-environment)), and IonQ's API accepts multi-circuit jobs of up to 5,000 circuits ([IonQ API](https://docs.ionq.com/api-reference/v0.4/jobs/create-job)). Yet the Soundtrack packs everything side by side on disjoint qubits of *one* circuit because remote backends take one circuit per run ([Soundtrack](https://qollab.xyz/u/qollab/quantum-hackathon-soundtrack)). The safe default is register-packing in one circuit of at most 20 qubits.

Two last cautions. Mid-circuit measurement makes the built-in simulator rerun the circuit for every shot: 13 s instead of 0.07 s for 1,000 shots at 10 qubits ([Ideal vs. noise-model simulators](https://qollab.xyz/learn/docs/ideal-vs-noise-model-simulators)). And IonQ supports no dynamic circuits on any target ([IonQ OpenQASM 3](https://docs.ionq.com/api-reference/v0.4/openqasm3)). Use deferred measurement or Pauli-frame post-processing everywhere.

### Packages: numpy, scipy and networkx yes; stim, pymatching and QuTiP no

Qollab loads Pyodide 314.0.7 (Python 3.14.2) according to its own CSP header, and it builds its own patched Qiskit 2.5.x, since Qiskit publishes no WebAssembly wheel ([qcflows headers](https://qollab.xyz/u/qollab/qcflows-multifile); [PyPI qiskit](https://pypi.org/pypi/qiskit/json)).

| Status | Packages | Source |
|---|---|---|
| Built into Pyodide | numpy 2.4.6, scipy 1.18.0 (with sparse), sympy 1.14.0, networkx 3.6.1, matplotlib 3.10.8, pandas, scikit-learn, cvxpy-base, igraph | [Pyodide package list](https://pyodide.org/en/stable/usage/packages-in-pyodide.html) |
| Installs from PyPI (tested) | rustworkx 0.18.1 (pyemscripten wheel, 2.2 s); pyzx 0.10.7 (pure Python, 2.7 s) | [Pyodide console tests](https://pyodide.org/en/stable/console.html); [PEP 783](https://peps.python.org/pep-0783/) |
| Fails | **stim, pymatching, qutip**: no pure-Python or Emscripten wheel | [PyPI stim](https://pypi.org/project/stim/#files) |
| Risky | galois and quimb install but depend on numba, which Pyodide lacks | [PyPI galois](https://pypi.org/pypi/galois/json); [Pyodide package list](https://pyodide.org/en/stable/usage/packages-in-pyodide.html) |
| Qollab one-click presets | qiskit-algorithms 0.4.0, optimization 0.7.0, nature 0.8.0 + PySCF, finance 0.4.1, machine-learning 0.9.1, QAVE 0.1.0, PQCA (brings qiskit_aer 0.17.2) | [Runtime environment](https://qollab.xyz/learn/docs/runtime-environment) |

For QEC, the substitute for Stim and PyMatching is the numpy frame simulator plus `networkx.max_weight_matching`. In Pyodide, matching took **3.2 ms for 10 defects, 12.7 ms for 20 and 85.8 ms for 40**, which is ample for distance 3 to 7 ([Pyodide console tests](https://pyodide.org/en/stable/console.html)). A compiled package listed in `requirements.txt` with no Pyodide build stops the whole run ([Runtime environment](https://qollab.xyz/learn/docs/runtime-environment)).

### Performance: twelve qubits live, twenty on demand, eight for density matrices

Single-gate einsum timings, measured in stock Pyodide 314.0.7 on Chromium 152 with complex128 ([Pyodide console benchmark](https://pyodide.org/en/stable/console.html)):

| Qubits | 1-qubit gate | CX |
|---|---|---|
| 14 | 0.9 ms | 1.3 ms |
| 16 | 2.4 ms | 4.2 ms |
| 18 | 15 ms | 17 ms |
| 20 | 36 ms | 71 ms |
| 22 | 155 ms | 230 ms |
| 24 | 782 ms | 874 ms |

The WebAssembly heap topped out near 3.9 GiB, and a single 2^27-element complex array is impossible. A naive density-matrix gate took 19 ms at 8 qubits, 191 ms at 10 and 865 ms at 11; a 13-qubit ρ alone is 1 GiB ([Pyodide console benchmark](https://pyodide.org/en/stable/console.html)).

The practical budgets follow:

| Use | Statevector | Density matrix |
|---|---|---|
| Live, recomputed on every slider move | ≤12 qubits | 6–8 qubits |
| Press-to-compute | ~20 qubits (100 gates in about 4–7 s) | — |
| Avoid live | 24 qubits | ≥11 qubits |

Pyodide runs on the main thread and workers are blocked, so yield to the UI before heavy work. IonQ's remote noise simulation runs once per shot, and runs near 29 qubits may time out ([Compute backends](https://qollab.xyz/learn/docs/compute-backends)).

### CDNs and licenses: jsDelivr only, MIT-compatible only

The JS frame's CSP allows scripts only from Qollab itself and **cdn.jsdelivr.net**. Styles, fonts and images may come from anywhere, and workers are blocked ([jsworker.html](https://qollab.xyz/jsworker.html)). three.js 0.186.1 and postprocessing 6.39.5 import by bare name, and tween.js and meshline are bundled ([Runtime environment](https://qollab.xyz/learn/docs/runtime-environment)). Everything else comes from a pinned URL of the form `https://cdn.jsdelivr.net/npm/<pkg>@<exact-version>/+esm`, as QCFlows does with D3 ([QCFlows](https://qollab.xyz/u/qollab/qcflows-multifile)). Since only `main.css` loads automatically, inject KaTeX's stylesheet with a `<link>` element created from JS.

Given the new MIT rule, prefer these libraries:

- KaTeX, MIT ([KaTeX](https://api.github.com/repos/KaTeX/KaTeX))
- Plotly.js, MIT ([Plotly](https://api.github.com/repos/plotly/plotly.js))
- quantastica's quantum-circuit, MIT ([quantum-circuit](https://api.github.com/repos/quantastica/quantum-circuit))
- Chart2Music, MIT ([Chart2Music](https://cdn.jsdelivr.net/npm/chart2music@1.20.0/README.md))
- D3, ISC

Avoid depending on:

- p5.js, LGPL ([p5.js](https://api.github.com/repos/processing/p5.js))
- Quirk and Stim/Crumble, Apache-2.0 ([Quirk](https://api.github.com/repos/Strilanc/Quirk); [Stim](https://api.github.com/repos/quantumlib/Stim))
- Quantum Flytrap's tensors, which declare no license ([quantum-tensors](https://api.github.com/repos/Quantum-Flytrap/quantum-tensors))

Qiskit itself is Apache-2.0 and required, so the organizers evidently don't apply the clause to platform libraries. Ask in Slack before relying on any other non-MIT runtime dependency. Linking out to Quirk or Crumble is fine.

### Accessibility: the cheapest differentiator in the catalog

The rules require accessibility best practices ([Rules & terms](https://qollab.xyz/programs/hackathon/terms)), yet a scan of all 104 Qollab projects found **only one using `aria-` or `role=` attributes** ([Qollab project API](https://api.qollab.xyz/api/project/popular?limit=30)). Treat WCAG 2.2 AA as the baseline. Its newer criteria include focus not obscured (2.4.11), a non-drag alternative for every drag (2.5.7) and targets of at least 24×24 px (2.5.8) ([W3C WAI](https://www.w3.org/WAI/standards-guidelines/wcag/new-in-22/)).

A concrete checklist:

- **Native controls.** Build every control as native HTML: range inputs for angles and noise, buttons for gates, fieldsets for basis choices.
- **Meaningful slider text.** Give sliders aria-valuetext that carries quantum meaning, for example "visibility 0.75, entangled, CHSH not violated".
- **Accessible graphics.** Wrap each complex graphic in a figure with a caption or an aria-describedby long description ([W3C complex images](https://www.w3.org/WAI/tutorials/images/complex/)). SVGs get role="img" plus title and desc ([TPGI](https://tpgi.com/using-aria-enhance-svg-accessibility)).
- **Spoken updates.** Copy PhET's Interactive Description pattern: state descriptions plus object and context responses delivered through polite live regions, mirrored in a visible "description log" that also shows judges the work ([Coursera/PhET](https://www.coursera.org/learn/description-design-for-interactive-learning-resources)).
- **Color and phase.** Use the Okabe–Ito palette (#E69F00, #56B4E9, #009E73, #F0E442, #0072B2, #D55E00, #CC79A7) ([Okabe & Ito](https://jfly.uni-koeln.de/color/)). Encode phase as hue plus an angle tick plus a number.
- **Motion.** Honor prefers-reduced-motion by jumping to end states and providing a step button ([MDN](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion)).
- **Optional sonification.** Map probabilities to pitch and syndrome flips to earcons, after Desmos's audio trace ([Desmos](https://help.desmos.com/hc/en-us/articles/37064105800333-Audio-Trace)).

An auto-generated text description of every state (amplitudes, purity, whether the subsystem has a ket) does double duty. It serves screen-reader users, and it is a genuine pedagogical contribution.

### Reliability: ship the IonQ results, seed everything, fail visibly

Copy the Soundtrack pattern ([Soundtrack](https://qollab.xyz/u/qollab/quantum-hackathon-soundtrack)):

- Compute all teaching visuals with exact Python math.
- Make one try/caught `backend.run` with a labeled fallback.
- Record IonQ Forte noise-model results during the build and ship them as JSON, labeled with backend, date, shots and seed.
- Seed `seed_simulator`, `seed_transpiler` and NumPy.
- Transpile to a fixed basis without a backend.
- Keep `requirements.txt` tiny.
- Render a static first screen before Python finishes loading.

Before publishing, test on the built-in simulator, Braket, one IBM noise model and the IonQ Forte simulator. Judges probably need to be signed in, because anonymous quantum runs can be refused ([Error reference](https://qollab.xyz/learn/docs/error-reference)).

## The ranked shortlist: two front-runners, two gambles, three fallbacks

| Rank | Concept | Qollab coverage today | Named in brief | IonQ alignment | Misconception evidence | Backend anchor | 48-hour risk |
|---|---|---|---|---|---|---|---|
| 1 | **Bell-Pair Foundry**: noise, distillation, swapping, use | None (zero hits for CHSH, swapping, purification, BB84) | Networking | Very high: 2026 iQuHACK challenge, April 2026 interconnect, networking acquisitions | Strong: FTL signaling, the maximal-entanglement assumption, QKD tutorial gains of 56% → 91% | ≤20 qubits, ~20 entanglers; runs as-is on IonQ | Low to medium |
| 2 | **Syndrome to Threshold**: circuit-level QEC beyond the repetition code | Repetition-code game only (bit flips, code capacity) | QEC and fault tolerance | High: 2026 BB5 qLDPC, Steane on Forte, real-time decoder | Weak: no QEC education research; expert inference | 5–17 qubits | Medium |
| 3 | **Polynomial Studio**: QSP/QSVT | None (zero hits for QSVT) | Algorithms | Medium: zero two-qubit gates suits any device | Medium: try-every-answer and exponential-Grover beliefs | 1 qubit per point, ≤29 in parallel | Medium to high (phase finding) |
| 4 | **Pulse to Program**: MS phase-space loops to algorithm success | Transpilation showcase covers gate counts, not physics | Not named | Highest | Weak: expert and instructor reports only | 2–8 qubits | High |
| 5 | Fallbacks: lost-ket lab, nonlocal-games arcade, Trotter sweet spot | Partial overlaps | Mixed | Mixed | Lost-ket has the strongest evidence (QCCS 23–26%) | 2–8 qubits | Low |

### 1. Bell-Pair Foundry ranks first on novelty, fit and feasibility

The learner runs the lifecycle IonQ's networking business sells. They make noisy Bell pairs, diagnose them, distill them, swap them across a repeater chain, then spend them on teleportation or key generation. The evidence for this pick:

- Networking is named in the brief.
- Qollab's catalog and Learn curriculum contain zero networking content beyond 3-qubit teleportation.
- IonQ's last hackathon challenge was distillation, and its 2024–2026 news is dominated by interconnects, memories and QKD.
- The FTL-signaling and all-entangled-states-are-maximal misconceptions are documented.
- The most impressive measured gain in quantum-education research (56% → 91%) came from a QKD guided-inquiry tutorial.

The learning arc runs through five predict–observe–explain modules:

1. **No-signaling microscope.** Alice chooses her measurement basis and the learner predicts whether Bob's histogram changes. It stays at 50/50 within shot noise, and correlations appear only when the two records are joined after an animated light-speed classical message.
2. **Werner ladder.** A single visibility slider recomputes concurrence, negativity, CHSH value, teleportation fidelity and hashing yield live, crossing the thresholds 1/2 → 0.625 → ~0.77 → 0.780 → 0.8107.
3. **Distillation bench.** The Bell-diagonal vector (p_I, p_X, p_Y, p_Z) flows visibly through a bilateral CNOT. The learner predicts which check helps on X-, Z- or mixed noise. They discover that a Z-check drops a phase-noisy pair from 0.90 to 0.82, while an X-check lifts it to 0.988. Then they watch DEJMPS outrun BBPSSW, the per-pair cost climb from 2.6 to 31.7, and the gate-noise ceiling cap everything near 0.985.
4. **Repeater race.** A swapping chain of 1–14 links (0.995 → 0.876) races direct fiber under the PLOB bound. Inserting a distillation round shows the nested BDCZ idea, anchored by USTC's 550 ms vs 450 ms and 420 km results.
5. **Spend the pair.** Teleport three ways: deferred-measurement corrections at 0.981, Pauli-frame correction at 0.988, and post-selection keeping 25% of shots. Then turn the measured S into a key rate: 0.71 device-independent bits per round at S = 2.75, or 1 − 2h(Q) for BB84.

Computationally, the Bell-diagonal algebra is a 4-vector map that recomputes instantly in JS or Python, and Qiskit Statevector or DensityMatrix (≤8 qubits) verifies it. A single anchor circuit, ≤20 qubits with roughly 20 entanglers, packs three registers:

- an N = 2 distillation with ancilla-purified noise (8 qubits);
- four CHSH setting pairs (8 qubits);
- a 2-link swap (4 qubits).

It runs on any backend in one job. Precompute an N = 4 two-round distillation (about 16 qubits and 18 gates) on the IonQ Forte noise model and an IBM heavy-hex model, and ship both as JSON.

Two of the researchers' scripts give you working numerics on night one. [ent_numbers.py](<../research_notes/Quantum Unlocked theme deep dive/scripts/ent_numbers.py>) covers the Werner table, hashing threshold, BBPSSW/DEJMPS recurrences and noise tailoring. [sim_demos.py](<../research_notes/Quantum Unlocked theme deep dive/scripts/sim_demos.py>) covers CHSH, teleportation, superdense coding, the swapping chain and GHZ scaling with Aer noise.

Your claim against the tutorial bar has two parts. The original educational contribution is a Bell-diagonal flow visualization explaining *why* a parity check catches one error type. The technical extension is noise-tailored distillation and a gate-noise ceiling compared across IonQ and IBM noise models.

The risks are manageable:

| Risk | Mitigation |
|---|---|
| Cloning iQuHACK's game | Present the tool as the game's explainer, and say so |
| Scope creep | Freeze modules 1–3 plus one of 4 or 5 by hour 24 |
| Slow density matrices beyond ~10 qubits | Use the analytic Bell-diagonal algebra or purified statevectors |
| LOCC honesty | Label the referee measurement and the deferred-measurement variant as non-LOCC |

### 2. Syndrome to Threshold is the brief's headline topic, if you can beat Qollab's own showcase

This is the stronger pick if your team's edge is numerics, and it matches the brief's first-named topics. The evidence:

- Qollab Learn has no QEC.
- IonQ's 2026 QEC record (BB5 qLDPC on 18 ions, Steane rotations on Forte, the real-time decoder claim) makes it timely.
- The absence of QEC education research makes any careful teaching design an original contribution.

Seven modules carry the arc, each anchored to a number from [frame_sims_v2.py](<../research_notes/Quantum Unlocked theme deep dive/scripts/frame_sims_v2.py>):

1. **Parity without collapse.** Measure-then-decode gives 0.46%, while coherent Toffoli correction gives 2.4%.
2. **Detection is not correction.** The [[4,2,2]] logical Bell pair reaches 0.018% at 97.4% acceptance against a bare 1.31%, with no gain without post-selection.
3. **One extra qubit buys 10×.** Flagged preparation drops from 0.30% to 0.028%.
4. **Single-fault explorer.** Place one fault and watch which detectors light up; hooks and CNOT ordering are visible without sampling.
5. **Λ lab.** An unrolled repetition code at d = 3/5/7 with networkx matching shows Λ falling from ~5 to ~1.5 as error rises, set against Willow's 2.14.
6. **Surface-17 learned decoder.** Decoding becomes conditional probability: p² scaling, a ~1% pseudo-threshold, and 86% post-selection acceptance at 0.5%.
7. **Headline literacy.** Learners classify real claims as detected or corrected, post-selected or not, memory or computation. Examples: Helios's 94 error-detected versus 48 error-corrected qubits, Willow, and IonQ's BB5.

The engine is the ~60-line numpy Pauli-frame simulator, verified against Aer in [qec_sims.py](<../research_notes/Quantum Unlocked theme deep dive/scripts/qec_sims.py>), plus cached networkx matching at 10⁴–10⁵ shots in the browser. Qiskit's StabilizerState provides exact single-shot tableau views. The anchor circuit packs the [[4,2,2]] Bell pair in both bases (8 qubits) with a d = 3, R = 3 repetition memory (9 qubits), or runs a single 17-qubit surface-code round.

State plainly that the anchor run cannot resolve 0.018% errors, which would take at least 50,000 shots. It demonstrates syndromes and acceptance; the browser simulation and the shipped IonQ Forte JSON carry the statistics.

The original analytic twist is the IonQ [[4,2,2]] paradox. Uniform noise models predict bigger gains at lower error, yet Aria showed none where Harmony did ([arXiv:2412.20736](https://arxiv.org/abs/2412.20736)). Correlated errors are the likely reason.

| Risk | Mitigation |
|---|---|
| Qollab judges compare directly with their own repetition-code game | Open the project page by naming that game and stating exactly what is new: circuit-level noise, detectors, matching, surface code |
| Other teams pick QEC | Your honesty and numbers are the differentiator, against the over-claiming that sank CQhack25's visualizer |
| No true threshold crossing with 3 rounds | Do not fake a threshold plot; R = 3 curves never cross |
| No idle noise in the model | State that the numbers are optimistic for real ions |

### 3. Polynomial Studio is the boldest algorithms play

The concept is "every algorithm is a polynomial." A one-qubit QSP circuit draws a polynomial, and learners discover four things:

- Grover is T_{2k+1}.
- Fixed-point amplitude amplification avoids overshooting the target.
- The Jacobi–Anger degree grows with simulation time, and the 1/x degree grows with κ.
- Making P(0.1) ≥ 0.9 with |P| ≤ 1 forces degree at least 9, the √N lower bound in miniature.

The QSVT stage then applies the same phases to a real 2+1-qubit block encoding of c₁Z₀ + c₂X₀X₁. That costs three two-qubit gates per call, 27 at d = 9 (~0.87 success).

The scalar version uses **zero two-qubit gates**, and 29 signal values fit in one circuit, so it runs beautifully on every backend including IonQ's. No interactive QSP designer was found anywhere ([PennyLane intro QSVT](https://pennylane.ai/demos/tutorial_intro_qsvt); [Martyn et al.](https://arxiv.org/abs/2105.02859)).

The risks are real:

- **Phase finding.** Whether pyqsp loads in Pyodide is unverified, so budget for a numpy/scipy optimizer in the Dong–Lin style.
- **Audience.** The natural audience is upper-level undergraduates, which narrows Impact.
- **IonQ fit.** It is the least IonQ-specific of the top four.

### 4. Pulse to Program is the most IonQ-native gamble

Learners drive the Mølmer–Sørensen gate's detuning, Lamb–Dicke parameter, Rabi frequency and temperature, and watch the phase-space circles close or fail to close. The tool computes the resulting two-qubit unitary by scipy integration of 2 qubits ⊗ ~20 Fock levels. It reports the gate's fidelity to MS(0,0), then drops that gate into a GHZ or QFT circuit to show algorithm success under Forte-like noise. Algorithm success is compared against heavy-hex compilation (28 vs ~56–84 two-qubit gates for an 8-qubit QFT).

Nothing like it exists beyond a theatre piece and Boulder Opal notebooks, and IonQ's engineers live this physics. But there are three drawbacks:

- Qollab's transpilation showcase already owns the gate-count story.
- Forte's ZZ gate's physical implementation is undocumented.
- Ion physics is not one of the brief's four named topics.

Every phase-space picture must also be computed, not drawn, to earn Technical Execution. Pick it only if someone on the team is comfortable with the Magnus expansion tonight.

### 5. Three fallbacks if time or nerve runs short

The **lost-ket lab** watches a reduced density matrix go mixed as a CNOT entangles, and asks whether a subsystem still has a ket. It targets the QCCS's hardest items (23–26% correct) and the superposition-versus-mixture confusion, with an X-basis toggle that separates |+⟩ from I/2. It has the strongest evidence base but overlaps Qollab's October 8 entanglement meter and its 2-qubit visualizer.

The **nonlocal-games arcade** (CHSH 0.844 vs 0.75, GHZ 0.978 vs 0.75, magic square 0.979 vs 0.889, and Peres–Mermin) is better folded into the Bell-Pair Foundry as a module.

The **Trotter sweet-spot lab** shows total error a/r + b·r with an optimum near r ≈ 4–10 for a 6-qubit Ising chain at 5 ZZ per step, checked against an exact 64×64 scipy `expm`. It has a strong IonQ hook through native ZZ, but sits close to the Hamiltonian-simulation race in Qollab's Quantum Advantage Lab ([Quantum Advantage Lab](https://qollab.xyz/u/hsadeghi/quantum-advantage-lab)).

### What to avoid, and how to decide tonight

Avoid anything the catalog or the past has already exhausted:

- Bloch spheres and Bell/GHZ basics;
- repetition-code-only QEC;
- ZNE and readout mitigation;
- the Clifford/T wall;
- textbook-to-MS gate counts on their own;
- plain Grover, Shor-15 or QPE circuits;
- VQE/QAOA tours;
- drag-and-drop sandboxes;
- music;
- magic-state distillation at real code scale, which 20 qubits cannot honestly show.

Choose the Bell-Pair Foundry if your team wants the clearest novelty and the tightest fit to IonQ's strategy. Choose Syndrome to Threshold if you have a strong numerical programmer and want the brief's headline topic. Either way, the first 24 hours look like this:

| Clock (ET) | Milestone |
|---|---|
| Fri 7–9 PM | Read the Slack kickoff for problem statements; confirm the theme; scaffold a QCFlows-style project with a JSON bridge, DOM wait and keep-alive |
| Fri 9 PM – Sat 1 AM | Run the packed anchor circuit on the built-in simulator **and** the IonQ Forte simulator; settle the one-circuit vs circuit-list question |
| Sat 1 AM – 11 AM | Core engine (Bell-diagonal algebra or Pauli-frame plus matching) and modules 1–2 with prediction prompts |
| Sat 11 AM – 7 PM | Modules 3–4; record IonQ Forte and IBM noise-model JSON; **freeze scope and submit a rough runnable version** |
| Sat 7 PM – Sun 7 AM | Accessibility pass, description log, pre/post check, limitations section |
| Sun 7 AM – 3 PM | Project page, 2–3-minute video recorded in Chrome, fresh-account tests on four backends |
| Sun 3–5 PM | Disclosures (scripts, forks, AI use), the required Qollab & IonQ attribution line, final submit |

## Conclusion

The field you are competing against is not other teams' Bloch spheres. It is Qollab's own September showcases, which set both the floor and the house style the judges will expect: an honest failure case, a live model, one anchor run, a fork path. Winning this theme means matching that style on a topic those showcases skipped. That is why networking and circuit-level fault tolerance beat the more familiar options. The research also changes what "teaching" should mean here. At 0.5% two-qubit error, every protocol in these notes keeps a comfortable quantum margin. The content worth teaching in 2026 is therefore *how* noise erodes advantage: post-selection costs, gate-noise ceilings, Λ sliding toward 1, swap chains decaying, models that predict gains hardware does not deliver. That honesty is precisely what the over-claiming losers lacked. Its close cousin, matching the protocol to the noise actually present, is what IonQ's own distillation challenge rewarded.

Two cheap levers are also unusually strong. Physics-education research has nothing on how people learn QEC or networking, so even a five-person think-aloud and an embedded pre/post check count as novel evidence rather than decoration. Only one of 104 Qollab projects attempts accessibility markup, so a PhET-style description layer turns a hard requirement into a visible differentiator. Pick the topic tonight, prove the anchor circuit runs on IonQ's simulator before midnight, and spend Sunday on documentation, which is a quarter of the score and a separate award.
