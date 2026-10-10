# Quantum Unlocked Theme Brief and the Qollab Platform (for building an educational project)

Snapshot: 2026-10-09, about 14:45 ET. That is roughly four hours before the 19:00 ET kickoff. Sources:
- **Raw server-rendered HTML** of qollab.xyz pages, fetched with curl. Qollab is a Nuxt site, and most content pages are SSR'd.
- **Qollab's public JSON API**, which the site itself uses:
  - project list: `https://api.qollab.xyz/api/project/popular?limit=30&next=<cursor>`
  - project write-up and code: `https://api.qollab.xyz/api/project/id/<id>/versions/head`
- **The Qollab sitemaps**: `https://qollab.xyz/sitemap-content.xml`.
- **The Qollab Discourse forum JSON**: `https://forum.qollab.xyz/latest.json`.
- **The GitHub API and raw files** for `github.com/qollabxyz`.
- **The Georgia Tech node site** (raw HTML).

Labels: **[Confirmed]** means stated in a primary source or read from code. **[Inferred]** means my reasoning.

---

## Q1. What is the verbatim Quantum Unlocked brief, and is there anything new as of kickoff day (problem statements, IonQ materials, rule changes)?

### Takeaway
The full, authoritative Quantum Unlocked brief is in the Rules & terms page, not the FAQ. It names four example topics: quantum error correction, fault tolerance, quantum networking, and algorithms. It also lists five acceptable formats: interactive demo, game, animation, visualization, or GUI. The goal it sets is to make a complex concept "intuitive, engaging, and memorable."

As of mid-afternoon Oct 9, no theme-specific problem statements or IonQ challenge materials had been published on any channel I could check (Qollab site, GT site, Qollab forum, web search).

Two rule edits appeared between Oct 7 and Oct 9:
- Any outside repo the project relies on must also be MIT-licensed.
- "AI tools" was removed from the "built during the window" bullet. AI use is still explicitly allowed elsewhere in the rules.

A new FAQ entry also appeared: Safari can't run projects.

### Cited Findings
**Verbatim theme text (three places, three lengths)**
- [Confirmed] Full brief, Rules & terms. The theme section opens: "Projects should leverage quantum computing's unique attributes and cover one or more of the following themes:" Then: "**Quantum Unlocked** — make the hardest ideas in quantum computing click. Quantum computing is full of fascinating ideas that can be difficult to visualize and understand. Pick a timely topic, such as quantum error correction, fault tolerance, quantum networking, or algorithms, and find a creative way to teach it. Build an interactive demo, game, animation, visualization, or GUI that turns a complex concept into something intuitive, engaging, and memorable." — [Qollab Rules & terms](https://qollab.xyz/programs/hackathon/terms)
- [Confirmed] Short version, FAQ on the hub and on how-it-works: "Quantum Unlocked. Pick a hard, timely topic such as error correction, fault tolerance, quantum networking or algorithms, and teach it: an interactive demo, animation, visualisation or GUI that makes it intuitive." The FAQ adds that "Full descriptions are in the Rules & terms." — [Qollab hackathon hub](https://qollab.xyz/programs/hackathon); [How it works](https://qollab.xyz/programs/hackathon/how-it-works)
- [Confirmed] Award tagline: "Quantum Unlocked — make the hardest ideas in quantum computing click." It is one of six global specialty awards, each "$500" cash plus "$5,000" compute, and "A single project can win multiple specialty awards and placement awards." — [How it works](https://qollab.xyz/programs/hackathon/how-it-works)
- [Confirmed] On theme choice: "Registration asks which theme you are leaning toward, but the answer is optional and binds nothing; it only helps us plan mentors and AMA topics. You declare your project's theme when you submit it, and you can change that up to the submission deadline on Oct 11." The rules also say projects "cover one or more of the following themes". — [How it works](https://qollab.xyz/programs/hackathon/how-it-works); [Rules & terms](https://qollab.xyz/programs/hackathon/terms)

**"Beyond the tutorial bar" (verbatim, Rules & terms)**
- [Confirmed] "Each submission must go beyond a standard reference implementation or tutorial-level exercise and demonstrate at least one of the following:"
  - "A novel application or problem context (e.g., applying an existing technique to a specific domain)"
  - "A technical extension (e.g., noise/error mitigation, parameter optimization, comparative benchmarking)"
  - "An original analytical or educational contribution (e.g., a genuinely new way of visualizing or explaining a quantum phenomenon)"

  "The judging panel will assess these traits as part of the Novelty & Creativity and Technical Execution rubric criteria. Panels may score a submission at 0 on these criteria, independent of other scores, if it fails to meet this bar." — [Rules & terms](https://qollab.xyz/programs/hackathon/terms)

**Submission requirements, current text (Rules & terms, "Every project must")**
- [Confirmed] "Use the Qiskit framework"
- [Confirmed] "Follow industry best practices on UI accessibility"
- [Confirmed] "Run on Qollab's free simulators, including IonQ's quantum simulator. Judges run every project on a free local simulator, and results from IonQ's simulators or hardware neither add nor subtract points."
- [Confirmed] "Be published and runnable on Qollab.xyz on an MIT license before the submission deadline"
- [Confirmed] "**Use an MIT license for any outside repo the project relies on, such as a frontend or backend hosted elsewhere**" (new since Oct 7)
- [Confirmed] "Have a project page on Qollab.xyz covering what the submission does, what problem it explores, how to run it, and other information to enable others to understand, replicate, or extend it"
- [Confirmed] "Be built during the hackathon window. Existing code, templates and forks are fine as a starting point when disclosed… judging is based on what the team adds during the window." The Oct 7 snapshot read "Existing code, AI tools, templates and forks…".
- [Confirmed] "Include a demo video of 2 to 3 minutes, at a public link that opens without signing in"
- [Confirmed] Attribution line: "This effort is supported by Qollab & IonQ"
- [Confirmed] The project must stay on Qollab 12 months. Winners must "Post at least once on their social channels about their participation."

— [Rules & terms](https://qollab.xyz/programs/hackathon/terms). The diff is against the Oct 7 raw-HTML snapshot kept in the prior research scratchpad.

**AI and originality**
- [Confirmed] AI is still allowed: "Using AI, open-source libraries, prior tutorials, or Qollab-hosted templates as a starting point is fine and encouraged. The differentiator is what teams build on top of them."
- [Confirmed] Disqualifying conduct includes "Copying code, circuit designs, or written explanations from external sources… without disclosure and attribution" and "Using a Qollab-hosted template or open-source library as a starting point without disclosure."
- [Confirmed] The FAQ still says "Can I use AI tools or existing code to start? Yes… Say on your project page what existed before the build window and credit its source."

— [Rules & terms](https://qollab.xyz/programs/hackathon/terms); [How it works](https://qollab.xyz/programs/hackathon/how-it-works)

**Judging mechanics (FAQ)**
- [Confirmed] "Judges open the project page, read the description and the code, and press Run on a free simulator. A frontend or backend hosted elsewhere can support it. Keep that repo public, with no sign-in, under an MIT license, with its dependencies listed and no API keys or secrets." — [How it works](https://qollab.xyz/programs/hackathon/how-it-works)
- [Confirmed] The local panel is "A local panel including a faculty or staff judge, alongside Qollab and IonQ representatives." Node panels may advance "up to one project for each of the specialized global awards," including Best of Theme. — [How it works](https://qollab.xyz/programs/hackathon/how-it-works); [Rules & terms](https://qollab.xyz/programs/hackathon/terms)

**Submission logistics**
- [Confirmed] "The team captain submits from the registration page, between Oct 9, 19:00 ET and Oct 11, 19:00 ET. A team can submit up to 5 projects… The captain can edit a submission in the form until the deadline."
- [Confirmed] Partial projects: "Submit what you have. Partial and rough projects are still eligible for judging."

— [How it works](https://qollab.xyz/programs/hackathon/how-it-works)

**New FAQ (added since Oct 7)**
- [Confirmed] "Which browsers can run projects? A recent Chrome, Edge, Brave or Opera, or Firefox 153 or later. Safari can't run projects yet: it lacks WebAssembly JSPI, which Qollab's runtime needs. On iPhone and iPad every browser uses Safari's engine, so build on a computer." — [How it works](https://qollab.xyz/programs/hackathon/how-it-works)

**Kickoff and problem statements**
- [Confirmed] The GT node site still says "Choose from Quantum Impact, Quantum Playground, or Quantum Unlocked when themes are released." It also says "Challenge themes and problem statements will be shared before the hackathon begins, following each sponsor's release schedule. We'll link the materials here as they become available."
- [Confirmed] The GT site lists the kickoff as "October 9 · 7:00 PM ET · Qollab × IonQ hackathon kickoff · Online through Qollab." No materials were linked as of the snapshot.

— [GT Fall Fest site](https://qhackathon-gt.lovable.app/)
- [Confirmed] The hackathon hub, how-it-works, terms and mentors pages contain no problem statements. The hub text is otherwise unchanged from Oct 7; a diff of the extracted text showed no changes. — [Qollab hackathon hub](https://qollab.xyz/programs/hackathon)
- [Confirmed] Qollab's announcements page has no hackathon-kickoff item. Its newest item is "Google withheld an ECDSA circuit" (Aug 26, 2026). — [Qollab announcements](https://qollab.xyz/explore/news)
- [Confirmed] The Qollab forum (Discourse) has no hackathon or kickoff thread. Its 30 latest topics are auto-created project discussion threads (Sept 24 to Oct 9) plus a June welcome post. — [forum.qollab.xyz latest.json](https://forum.qollab.xyz/latest.json)
- [Confirmed] Web searches found no new IonQ or Qollab press or social posts about the hackathon in the last week.
  - The latest coverage is Quantum Zeitgeist on Sept 7, 2026.
  - A Stackademic roundup repeats the outdated "closes October 6" registration date.

  — [Quantum Zeitgeist](https://quantumzeitgeist.com/ionq-quantum-hackathon-qollab-host/); [Stackademic roundup](https://blog.stackademic.com/20-hackathons-in-october-2026-worth-your-time-c8677df0f160)
- [Confirmed] On Oct 3, Qollab published a hackathon-themed project, "Quantum Hackathon Soundtrack": "Ambient background music for the Qollab x IonQ hackathon… IonQ Forte shots, a quantum Markov chain for chords, one 20-qubit circuit per run. Fork of Superposition Sequencer." The FAQ cites it as an example of a properly disclosed fork. — [qollab/quantum-hackathon-soundtrack](https://qollab.xyz/u/qollab/quantum-hackathon-soundtrack)

### Inferences
- [Inferred] The brief's four named topics are examples ("such as"), not a closed list. Any "hard, timely" concept qualifies. Naming one of the four (QEC, fault tolerance, networking, algorithms) aligns most clearly with judges' expectations for Best of Quantum Unlocked.
- [Inferred] The third "beyond the tutorial" bullet ("a genuinely new way of visualizing or explaining a quantum phenomenon") is the explicit novelty path for Unlocked projects. A re-skin of an existing Qollab teaching demo (see Q2) risks a 0 on Novelty and Technical Execution.
- [Inferred] The new MIT rule for outside repos means any externally hosted frontend or backend must be MIT-licensed, public and secret-free. Keeping everything inside the Qollab project avoids that requirement.
- [Inferred] "Safari can't run projects" matters for the demo video and for anyone reviewing on a Mac with Safari. Record in Chrome, Edge or Firefox 153+, and state the browser requirement on the project page.
- [Inferred] Any sponsor problem statements will most likely appear in Slack (node and global channels) or on the GT site at or after 19:00 ET. Check both at kickoff.

### Gaps
- Theme-specific problem statements or IonQ challenge materials, if any, were not public as of ~14:45 ET Oct 9. They may be released at the 19:00 ET kickoff in Slack, which is not publicly readable.
- Rubric weights and per-criterion descriptors are still unpublished.
- Qollab's and IonQ's LinkedIn and X posts could not be read directly (LinkedIn requires sign-in). Search surfaced no recent posts.

---

## Q2. Which hard topics do existing Qollab projects already cover (full inventory), and which are conspicuously missing?

### Takeaway
Qollab has **104 public projects** (API, Oct 9); **51 are by the "qollab" team account**. Qollab itself has already published a set of polished interactive teaching "showcases" (Sep 1, 2026) on exactly the obvious Quantum Unlocked topics:
- a **distance-3 repetition-code game** with a threshold Monte Carlo
- **interactive ZNE**
- **readout-error mitigation**
- **statevector vs stabilizer simulation** (the Clifford/T boundary)
- **transpilation to trapped-ion MS gates**
- **T1 calibration**
- a **quantum kernel**
- an **H2 bond-length VQE**

There are also basic Python examples of teleportation (deferred measurement), Shor N=15, QPE, Grover and GHZ, and community explainers on QEC codes, noise, entanglement and correlations.

Conspicuously absent:
- surface codes, decoders and logical-qubit overhead beyond repetition codes
- magic-state distillation and lattice surgery (GraFT covered this in the Spring cohort but is not published on Qollab)
- all of quantum networking beyond 3-qubit teleportation: QKD/BB84/E91, entanglement swapping, repeaters, purification, CHSH/Bell tests
- the oracle-algorithm family (Deutsch–Jozsa, Bernstein–Vazirani, Simon)
- HHL, QSVT/QSP, an interactive amplitude-estimation explainer, and randomized benchmarking

### Cited Findings
**Method and scale**
- [Confirmed] The site's gallery API returns 104 projects in total across paginated calls (`/api/project/popular`, cursor `next`). The "recent" ordering returns the same 104. Owners: `qollab` 51, `sairamtummuri` 4, `plamsoft` 3, and ~40 others with 1–2 each. — [Qollab project API (popular)](https://api.qollab.xyz/api/project/popular?limit=30); [Qollab Projects gallery](https://qollab.xyz/projects)
- [Confirmed] Gallery tags include education, visualization, interactive, entanglement, superposition, quantuminformation, vqe, chemistry, fall2025 and spring2026. — [Qollab Projects gallery](https://qollab.xyz/projects)

**A. Qollab-team interactive teaching showcases (JS + Qiskit, published Sep 1, 2026; each pitched as "a template - fork it")**

| Project | What it teaches and how |
|---|---|
| [Error correction showcase: the repetition-code game](https://qollab.xyz/u/qollab/error-correction-showcase-the) | "The whole bet of fault tolerance, playable." Distance-3 bit-flip repetition code: click qubits to flip them, see "syndrome lights" and the majority-vote decoder, including "the honest case where two flips fool the decoder." **Storm mode** is a seeded in-browser Monte Carlo for distances 3 and 5, plotting logical vs physical error on log-log axes with the threshold at p = 0.5. "Bit-flip-only by design." Suggested forks: "Go distance 7", "Phase-flip mode", and "Build the calculator" (qubits needed for a target logical rate). Tags: showcase, education, circuit, noise. |
| [Error mitigation showcase: interactive ZNE explorer](https://qollab.xyz/u/qollab/error-mitigation-showcase-inte) | GHZ-4 parity under depolarizing noise. Scale factors x1/x3/x5 (folding CX → CX·CX†·CX), with linear or Richardson fits. Sampling comes from an analytic model in the browser. A "Run GHZ-4 on backend" anchor uses the real backend. |
| [Error mitigation showcase: zero-noise extrapolation](https://qollab.xyz/u/qollab/error-mitigation-showcase-zero) | Python version: GHZ-4 parity recovered "to within ~1% of ideal with Richardson extrapolation." |
| [Readout mitigation showcase](https://qollab.xyz/u/qollab/readout-mitigation-showcase-fi) | GHZ-5 with readout-error sliders and three histograms (ideal, raw, corrected), live in the browser. |
| [Simulation showcase: statevectors vs stabilizers](https://qollab.xyz/u/qollab/simulation-showcase-statevecto) | 2^n memory counter vs an n×2n tableau. A ~40-line JS stabilizer simulator builds a 100-qubit GHZ, and "press '+T gate' and the tableau refuses." Suggested forks: add S/CZ for graph states, "Find the wall", "Count the magic". |
| [Transpilation showcase: from textbook gates to trapped ions](https://qollab.xyz/u/qollab/transpilation-showcase-from-te) | Hover a GHZ gate to see its trapped-ion native expansion: "each H becomes three native rotations, each CX becomes one MS entangler plus four rotations." Includes a peephole optimize toggle and live depth and gate counts. |
| [Calibration showcase: where T1 comes from](https://qollab.xyz/u/qollab/calibration-showcase-where-t1) | Live T1 experiment and fit with shot noise, plus a "hardware drift" button. Suggested fork: "Add T2… Ramsey." |
| [Quantum kernel showcase: drag the test point](https://qollab.xyz/u/qollab/quantum-kernel-showcase-drag-t) | Feature-map kernel on two-moons. Drag a point and watch its class flip. |
| [Cross-framework showcase: one VQE, two languages](https://qollab.xyz/u/qollab/cross-framework-showcase-one-v) | H2 VQE in Qiskit vs PennyLane racing on one energy landscape. |
| [Quantum chemistry showcase: the H2 bond-length slider](https://qollab.xyz/u/qollab/quantum-chemistry-showcase-t-2) | Drag the atoms apart and trace the dissociation curve. Live VQE, with Hamiltonians precomputed using qiskit-nature + PySCF. |
| [Interactive Bloch Sphere](https://qollab.xyz/u/qollab/interactive-bloch-sphere) (Aug 31) and [JS Bloch Sphere](https://qollab.xyz/u/qollab/js-bloch-sphere) (Sep 28, a three.js template) | Single-qubit gates H, X, Y, Z, S, Sdg, T, Tdg and RX/RY/RZ, with live amplitudes, angles and probabilities. 1024 shots are sampled locally. |

**B. Qollab-team Python "example" projects (Mar 2026) and library showcases (Aug 2026)**
- [Confirmed] [Quantum Teleportation](https://qollab.xyz/u/qollab/quantum-teleportation): 3 qubits, Ry(π/3) state. Uses deferred measurement because "Most cloud quantum hardware (including IonQ) doesn't support mid-circuit measurement with classical feedback." It is the most viewed qollab example (159 views).
- [Confirmed] Other examples:
  - [Shor's N=15](https://qollab.xyz/u/qollab/shors) (7 qubits, 230 views)
  - [Quantum Phase Estimation](https://qollab.xyz/u/qollab/quantum-phase-estimation)
  - [Grovers Search](https://qollab.xyz/u/qollab/grovers-search)
  - [Scaled Entanglement (GHZ)](https://qollab.xyz/u/qollab/scaled-entanglement)
  - [Bell State](https://qollab.xyz/u/qollab/bell-state)
  - [Quantum Chemistry (methanol VQE)](https://qollab.xyz/u/qollab/quantum-chemistry)
- [Confirmed] Library showcases (Aug 1):
  - qiskit-algorithms: Grover, VQE
  - QAOA/QUBO, exact QUBO
  - qiskit-nature: H2 ground state, Jordan–Wigner fermionic operator
  - qiskit-finance: option pricing via amplitude estimation, portfolio optimization
  - qiskit-machine-learning: VQC-XOR, EstimatorQNN
  - PQCA automaton
  - histograms
  - Bell on Braket, Bell on IBM fake-Boston noise

  — [Qollab project API](https://api.qollab.xyz/api/project/popular?limit=30)
- [Confirmed] Course companion projects:
  - "Learn: …" projects for each lesson of *Programming your first quantum circuits*: first circuit, superposition, two qubits, rotations, interference ("Make a phase visible"), Grover on two qubits, noise.
  - Five of the six lessons of *Using quantum in a real application* (learn-app-observe, -boundary, -ui, -race, -slice).
- [Confirmed] Multi-file templates (Sep 28–29): [Bell state across JS files](https://qollab.xyz/u/qollab/bell-state-across-js-files), [Bell state across Python files](https://qollab.xyz/u/qollab/bell-state-across-python-files), [Bell state from JS and Python](https://qollab.xyz/u/qollab/bell-state-from-js-and-python), and [QCFlows: Multi-file Example](https://qollab.xyz/u/qollab/qcflows-multifile).

**C. Creative Challenge winners and Spring 2026 cohort (education-relevant)**
- [Confirmed] The Education explore page (Nicolaas Spijker, Jul 4, 2026) names six "interactive quantum computing tools":

  | Tool | What it does | Runs on | Builder |
  |---|---|---|---|
  | QAVE | Algorithm viewer | Simulator | Inho Choi |
  | QuantumCanvas | Drag-and-drop circuit sandbox | IonQ hardware or simulator | Shivani Mayekar, Georgia Tech |
  | Quantum Courier | Routing game vs a quantum solver | IonQ | Dr. Siti Fariya |
  | Quantum Advantage Lab | Races quantum vs classical algorithms | IonQ | Hossein Sadeghi |
  | qOrbital | VQE orbitals, with noise overlaid | IonQ | Aryan Bawa & Arnav Singh |
  | QCFlows | Correlation and entanglement graph | Simulator ("IonQ tomography planned") | Paulo Itaboraí, Iosifina Angelidi, Kostas Blekos |

  The page's thesis: "rather than explain quantum computing, show it." — [Qollab Explore: Education](https://qollab.xyz/explore/education)
- [Confirmed] [Quantum Advantage Lab](https://qollab.xyz/u/hsadeghi/quantum-advantage-lab) runs four races:
  1. Grover vs linear search
  2. VQE vs classical optimization
  3. Discrete-time quantum walk vs classical random walk
  4. Hamiltonian simulation vs matrix exponentiation

  It says plainly that no practical speedup exists at these sizes.
- [Confirmed] The Spring 2026 cohort (13 teams) includes:
  - **GraFT** (David Nizovsky, Vanderbilt/Superquantum, with Daniil Shatokhin): "3D explorable graphs of how a single logical gate expands into thousands of fault-tolerant physical operations… including magic state distillation and syndrome extraction."
  - **Quantum Butterfly Field** (Xinyi Zhang): "real scrambling circuits, making the no-butterfly effect tangible."
  - **Quantum Market Game** (Aadarsh Venkat Ramanan): "Designed for high school and early college students," an "entanglement primer."
  - **QCFlows**, **QuantumCanvas**, **qOrbital**, **Qatalyst Game**, **Musiq**, **Quantum Patterns**, **Superposition Sequencer**, **Entangled Body**, **QuantumRegimeRadar**, **Quantum Systemic Oracle**.

  — [Meet the Spring 2026 cohort](https://qollab.xyz/explore/spring-2026-cohort)
- [Confirmed] **GraFT does not appear among the 104 public Qollab projects**, and web search found no public GraFT artifact. — [Qollab project API](https://api.qollab.xyz/api/project/popular?limit=30)

**D. Other community explainers on Qollab**
- [Confirmed] [Quantum Error Correction (sairamtummuri)](https://qollab.xyz/u/sairamtummuri/quantum-error-correction), May 2026, 35 views:
  - Shows "logical qubit encoding, stabilizer measurements, syndrome extraction, error detection, correction process."
  - Error injection uses X, Z and Y. A syndrome table is shown (Z1Z2, Z2Z3).
  - Codes listed: 3-qubit bit-flip, 9-qubit Shor, and the 5-qubit code ("The smallest code that can correct any single-qubit error").
- [Confirmed] Also by sairamtummuri: [Quantum Error Mitigation Playground](https://qollab.xyz/u/sairamtummuri/quantum-error-mitigation-playg) (ideal vs noisy vs mitigated, ZNE) and [Quantum Noise Simulator Dashboard](https://qollab.xyz/u/sairamtummuri/quantum-noise-simulator-dashbo) (noise channels, fidelity degradation).
- [Confirmed] [2-qubit states, visualized 8 ways](https://qollab.xyz/u/onri-jay-benally/2-qubit-state-visualization) by Onri Jay Benally: Bloch spheres, steering ellipsoids, Wigner functions and more. Note: "QuTiP has no WebAssembly build, so the visualisations that depend on it were removed."
- [Confirmed] Expert notes (articles, all by Onri Jay Benally, Jul–Aug 2026): cross-resonance gate heatmaps, pulse shapes and envelopes, Wigner functions for single-qubit gates, Rabi oscillations, and a sampling-budget analogy. These are mostly superconducting-control physics. — [Qollab Expert notes](https://qollab.xyz/explore/expert-notes)
- [Confirmed] Further community explainers:
  - [Quima Quantum 3D playground](https://qollab.xyz/u/emmanuellaadams/quima): Schrödinger-equation wave mechanics, Born rule, potential barriers.
  - [Krylov Quantum Diagonalization of Lattice Hamiltonians](https://qollab.xyz/u/mirko/krylov-quantum-diagonalization): a tutorial with a 30-qubit Heisenberg chain and Hadamard tests.
  - [QuantumCanvas](https://qollab.xyz/u/ShivaniMayekar/quantum-canvas): logic nodes and constraint links that compile to circuits.
  - [Quantum Market Game Theory Simulator](https://qollab.xyz/u/q-aad/quantum-market-game-theory-sim): a quantum prisoner's dilemma.
- [Confirmed] New projects published Oct 6–9, just before the build window:
  - [Pure-State Entanglement Measurement](https://qollab.xyz/u/Niharika28/pure-state-entanglement-meter) (Oct 8): reduced density matrix, von Neumann entropy, concurrence on a Bell state.
  - [Quantum Automitigation](https://qollab.xyz/u/S0cra13s/quantum-automitigation) (Oct 8): a bandit learner over ZNE, Pauli twirling and transpiler level, scored by mirror circuits.
  - [QAIP Hardware Ranking](https://qollab.xyz/u/Rudra1x/qaip-hardware-ranking) (Oct 8): calibration-aware backend ranking.
  - Several "Fork of Learn: …" and "test" projects.

**E. Full-text topic scan (write-ups plus main code of all 104 projects)**
- [Confirmed] Zero matches: BB84, E91, QKD, Steane, [[4,2,2]], [[7,1,3]], lattice surgery, magic state, MWPM/minimum-weight, union-find, CHSH, Bell inequality, entanglement swapping, repeater, purification, Deutsch, Bernstein, Simon, QSVT, randomized benchmarking, quantum volume, measurement-based/cluster state, phonon, ion shuttling.
- [Confirmed] Thin coverage (passing mentions only):
  - "surface code": only as a QAVE use case and in the repetition-code write-up's closing remark
  - "HHL": a mention in QPE
  - "amplitude estimation": the library showcases only
  - "no-cloning": the teleportation write-up
  - "superdense": Bell write-ups only
  - "distillation": a "count the magic" fork suggestion

  — [Qollab project API](https://api.qollab.xyz/api/project/popular?limit=30), with each project's `versions/head` endpoint

### Inferences
- [Inferred] **Already well covered; avoid unless clearly beyond what exists:**
  - single-qubit Bloch spheres
  - Bell/GHZ entanglement basics
  - the 3-qubit bit-flip repetition code with a threshold Monte Carlo (Qollab's own showcase even lists the obvious extensions: distance 7, phase-flip, overhead calculator)
  - ZNE and readout mitigation
  - statevector vs stabilizer
  - textbook-to-MS transpilation
  - Grover, Shor-15, QPE and basic teleportation circuits
  - VQE/H2 and QAOA/QUBO
  - QAVE-style step-by-step state animation
  - QCFlows-style correlation graphs
- [Inferred] **Clearest gaps for Quantum Unlocked:**
  1. **Fault tolerance beyond repetition codes:**
     - surface/rotated-surface or color code: interactive stabilizer plaquettes, syndrome graphs, a matching-decoder visualization, logical error vs distance
     - [[4,2,2]] error detection actually run on IonQ noise models
     - Steane [[7,1,3]] with transversal gates
     - magic-state distillation and T-count overhead (GraFT's topic, unpublished on Qollab)
     - lattice surgery
  2. **Quantum networking:**
     - BB84/E91 QKD with an eavesdropper and QBER
     - entanglement swapping and repeater chains
     - entanglement purification/distillation
     - CHSH/Bell-inequality violation (a natural fit for a game)
     - superdense coding as an interactive protocol

     Only 3-qubit teleportation exists.
  3. **Algorithms not yet taught interactively:**
     - Deutsch–Jozsa, Bernstein–Vazirani, Simon (phase kickback, oracles)
     - an interactive QFT/period-finding explainer (Shor is only a static example)
     - amplitude estimation, HHL, QSP/QSVT
  4. **Trapped-ion physics:**
     - MS gate phase-space loops, the phonon bus, all-to-all connectivity vs SWAP overhead, ion shuttling
     - randomized benchmarking, or T2/Ramsey (the T1 showcase leaves T2 as a fork suggestion)

  These would also resonate with IonQ judges.
- [Inferred] The Qollab team's showcase style shows what Qollab considers good teaching UX:
  - honest failure cases
  - a live Monte Carlo or analytic model in the browser
  - one "anchor" run on the selected backend
  - a "Make it yours" fork path

  Mirroring and exceeding that standard is probably the bar.
- [Inferred] Shivani Mayekar (QuantumCanvas) is a Georgia Tech M.S. student who has run quantum workshops for 250+ participants. She may be known to the GT node organizers or judges. A drag-and-drop circuit sandbox would look derivative at the GT node.

### Gaps
- For about half the community projects, only the write-up and main file were inspected, not every file. Coverage claims rest on keyword scans of write-ups plus main code.
- Four project write-ups could not be fetched (HTTP 429 rate limits): mirya/js-default, qollab/cross-framework-showcase-one-v, qollab/learn-app-boundary, qollab/readout-mitigation-showcase-fi. Their descriptions came from the list API instead.
- Private and draft projects, and projects created after ~14:45 ET Oct 9, are not visible. Other hackathon teams' in-progress work cannot be seen.
- Whether GraFT exists elsewhere (GitHub, its own site) could not be confirmed.

---

## Q3. What exactly can QAVE do and how is it used? Which Qollab Learn lessons exist and what do they cover?

### Takeaway
QAVE (Quantum Algorithm Visualization Engine) is a Python library that runs its own NumPy statevector simulation of a Qiskit or OpenQASM circuit and emits a versioned `trace.json`. The trace contains **in-gate evolution samples** and per-step observables:
- amplitudes
- per-qubit Bloch vectors
- purity and entropy
- density matrices
- pairwise mutual information
- bipartition entropy
- seeded measurement shot replays

The animated rendering is done by a **Processing (Java) sketch plus ffmpeg**, which cannot run in Qollab's Pyodide runtime. **On Qollab, QAVE can generate traces and histograms but cannot render its animation.** Qollab's own adapted copy says so in code.

QAVE has **no noise model, no mixed states**, a recommended max of 16 qubits, and a small gate set.

Qollab Learn has:
- 5 courses (27 lessons)
- 6 concept explainers with runnable and forkable code
- 50 docs, including 29 gate pages

### Cited Findings
**QAVE: identity and provenance**
- [Confirmed] Repo: `github.com/qollabxyz/qave`, MIT. Description: "Quantum Algorithm Visualization Engine turns Qiskit/OpenQASM quantum circuits into deterministic traces and synchronized animations, making quantum algorithms easier to teach and understand." Last push 2026-07-03, 1 star. — [GitHub API: qollabxyz repos](https://api.github.com/orgs/qollabxyz/repos)
- [Confirmed] Original author: Inho Choi (@q-inho), "Quantum Creative Challenge · Fall 2025" winner. Qollab project: [q-inho/qave](https://qollab.xyz/u/q-inho/qave) (667 views, the most viewed project). Upstream: [github.com/q-inho/qave](https://github.com/q-inho/qave). — [QAVE showcase](https://qollab.xyz/explore/qave)
- [Confirmed] Qollab installs it as the one-click library `qave==0.1.0`, which also swaps in `qiskit[visualization]>=2.5.2,<3.0.0`. — [Runtime environment doc](https://qollab.xyz/learn/docs/runtime-environment)

**QAVE: public API (`qave/__init__.py`, `options.py`)**
- [Confirmed] Entry points:
  - `generate_trace_from_qiskit`, `generate_trace_from_openqasm`
  - `generate_animation_from_qiskit`, `generate_animation_from_openqasm`
  - `simulate_backend_a`
  - result types `TraceGenerationResult`, `AnimationGenerationResult`, `ArtifactPaths`, `DiagnosticEntry`
  - an error hierarchy: `QaveError`, `InputValidationError`, `RuntimeDependencyError`, `RenderExecutionError`, …

  — [qave/__init__.py](https://github.com/qollabxyz/qave/blob/main/backend/src/qave/__init__.py)
- [Confirmed] `SimulationOptions` fields:
  - `algorithm_id` ∈ {"bell","ghz","qft","teleportation","grover","vqe","custom"}
  - `mode` ∈ {"preview","validation"}
  - `measurement_mode` = "collapse" only ("branching is no longer supported")
  - `seed`, `shot_count`
  - `precision_profile` ∈ {"fast","balanced","strict"}
  - `animation_profile` ∈ {"teaching_default","analysis_slow","presentation_fast"}
  - `params` dict
- [Confirmed] `RenderOptions` defaults: 1920×1080 at 60 fps, `emit_mp4=True`, `processing_runner`, `ffmpeg_bin="ffmpeg"`, `sketch_dir`.
- [Confirmed] `ArtifactOptions`: `out_dir`, `write_result_json`, `write_validation_json`.

  — [qave/options.py](https://github.com/qollabxyz/qave/blob/main/backend/src/qave/options.py)
- [Confirmed] README quickstart:

  ```python
  generate_animation_from_qiskit(
      circuit,
      options=SimulationOptions(algorithm_id="ghz", mode="validation", seed=24, shot_count=100),
      render=RenderOptions(width=960, height=540, fps=20, keep_frames=False, emit_mp4=False, emit_gif=True),
      artifacts=ArtifactOptions(out_dir=Path("artifacts/ghz3")),
  )
  ```

  It "requires Processing, PeasyCam, and ffmpeg." — [QAVE README](https://github.com/qollabxyz/qave/blob/main/README.md)
- [Confirmed] Showcase notebook flow:
  1. `generate_trace_from_qiskit(circuit, options=SimulationOptions(algorithm_id="ghz", mode="preview", seed=24, shot_count=100))`
  2. `result.require_measurement_shot_replay()` ("Repeatable shot outcomes")
  3. `render_animation(result, render=resolve_notebook_render_options(width=1280, height=720, fps=60))`
  4. `display(display_animation(anim))`

  — [QAVE showcase](https://qollab.xyz/explore/qave)

**QAVE: simulator capabilities (`backend_a.py`, `gates.py`, `extractor.py`)**
- [Confirmed] Backend capability: `backend_id="backend_a_statevector_numpy"`, `supports_pure_state=True`, `supports_mixed_state=False`, `supports_noise=False`, `max_recommended_qubits=16`. — [backend_a.py](https://github.com/qollabxyz/qave/blob/main/backend/src/qave_backend/simulator/backend_a.py)
- [Confirmed] Scalability policy:

  | Size | Features |
  |---|---|
  | small_n_max=8 | full amplitudes, Bloch, purity/entropy, full density |
  | medium_n_max=16 | top-k amplitudes, Bloch, purity/entropy, full density |
  | large | full density, entanglement metrics, measurement distribution |

  Each gate step is animated in phases `pre_gate` (0–0.2), `apply_gate` (0.2–0.75) and `settle` (0.75–1.0). In-gate samples use a fractional unitary U^τ (principal-branch eigenphases). — [backend_a.py](https://github.com/qollabxyz/qave/blob/main/backend/src/qave_backend/simulator/backend_a.py); [gates.py](https://github.com/qollabxyz/qave/blob/main/backend/src/qave_backend/simulator/gates.py)
- [Confirmed] Supported unitary gates: x, y, z, h, s, t, rx, ry, rz, cx, cz, ccx/toffoli, cswap, swap. "Controlled variant… is unsupported," any other name raises "Unsupported gate," and unbound symbolic parameters are rejected ("bind parameters before import"). Measurement collapse and reset are handled by the engine. — [gates.py](https://github.com/qollabxyz/qave/blob/main/backend/src/qave_backend/simulator/gates.py); [qiskit_importer.py](https://github.com/qollabxyz/qave/blob/main/backend/src/qave_backend/ingest/qiskit_importer.py)
- [Confirmed] Observables extracted per step:
  - per-qubit Bloch vectors (from single-qubit reduced density matrices)
  - per-qubit purity and von Neumann entropy
  - top-k amplitudes (32/16/8 by size)
  - the full density matrix
  - pairwise entropies/mutual information for ≤8 qubits
  - half-split bipartition entropy
  - a histogram of up to 64 outcomes

  — [extractor.py](https://github.com/qollabxyz/qave/blob/main/backend/src/qave_backend/observables/extractor.py)
- [Confirmed] Reference viewer: a Processing sketch with AmplitudePane, CircuitPane, DensityPane, MatrixEvolutionPane, ProbabilityPane, CameraDirector, TimelineEngine, ControlOverlay and FrameExporter. `render.py` shells out to `processing-java`/Processing CLI and `ffmpeg` via `subprocess`. JSON schemas for `AlgorithmTrace`, `SimulationResult`, `ObservableSnapshot` and others live in `contracts/schemas/`. — [qave repo tree](https://github.com/qollabxyz/qave); [render.py](https://github.com/qollabxyz/qave/blob/main/backend/src/qave/render.py)
- [Confirmed] Bundled example circuits: `build_bell`, `build_ghz(qubits, measure)`, `build_qft3` (decomposed controlled-phase). — [examples.py](https://github.com/qollabxyz/qave/blob/main/backend/src/qave/examples.py)

**QAVE on Qollab specifically**
- [Confirmed] The Qollab-adapted copy [mirya/qave](https://qollab.xyz/u/mirya/qave) generates the trace, prints diagnostics and replay outcomes, and plots a histogram. It then stops: "The actual animation rendering would only work in IPython notebook with appropriate dependencies installed, exiting..." (Mirya is a committer on the qollabxyz Qiskit forks.) — [mirya/qave](https://qollab.xyz/u/mirya/qave); [GitHub qollabxyz/qiskit commits](https://api.github.com/repos/qollabxyz/qiskit/commits)
- [Confirmed] The showcase claims QAVE "makes quantum errors and their corrections directly observable." The project page lists "Error correction walkthroughs" (surface code or bit-flip) as a *use case*. The repo's examples are only Bell, GHZ and QFT-3. — [QAVE showcase](https://qollab.xyz/explore/qave); [q-inho/qave](https://qollab.xyz/u/q-inho/qave)
- [Confirmed] Inho Choi's stated roadmap:
  - "a realistic noise mode so users can compare ideal and hardware-like behavior"
  - "a tensor-network or MPS view"
  - "a hybrid-loop mode for VQE or QML"
  - a hardware-aware layer showing "how noise propagates from the physical device to the final algorithmic performance"
  - a companion project comparing "superconducting, trapped-ion, and neutral-atom platforms"

  — [QAVE showcase](https://qollab.xyz/explore/qave)

**Qollab Learn: courses (lesson slugs from the sitemap)**
- [Confirmed] *Programming your first quantum circuits* (6 lessons, "Start here"): your-first-circuit, superposition, two-qubits (Bell pair), rotations, interference ("your first algorithm", Grover on 2 qubits), noise-and-the-real-machine. Each lesson has a "Learn: …" companion project run on the IonQ simulator.
- [Confirmed] *Quantum foundations* (5): what's quantum computing, qubits, gates, matrices, complex numbers. "About an hour, no account needed."
- [Confirmed] *Building your first Qollab project* (5): create-project, code-playground, run-in-javascript, fork-a-project, bring-your-own-code.
- [Confirmed] *Quantum computing with Python and Qiskit* (5): python-setup, python-basics, qiskit-setup, ionq-setup, ionq-hardware (local machine setup with UV).
- [Confirmed] *Using quantum in a real application* (6): what-to-build, where-the-circuit-sits, what-crosses-the-boundary, inputs-in-result-out, the-app-around-it, is-quantum-worth-it.

— [Qollab Learn](https://qollab.xyz/learn); [Qollab sitemap-content.xml](https://qollab.xyz/sitemap-content.xml)

**Qollab Learn: concept explainers (by Nicolaas Spijker, Community manager)**
- [Confirmed] Each explainer, with the community projects it walks through:

  | Explainer | Covers | Projects featured |
  |---|---|---|
  | [Understanding Quantum Superposition](https://qollab.xyz/learn/quantum-superposition) | phase, sampling, a 24-qubit MaxCut | Superposition Sequencer, Quantum Courier |
  | [Understanding Quantum Measurement](https://qollab.xyz/learn/quantum-measurement) | basis choice, readout errors | Musiq, Quantum Garden, QAVE seeded shots |
  | [Understanding Quantum Interference](https://qollab.xyz/learn/quantum-interference) | Grover, over-rotation, interference on noisy hardware | Quantum Advantage Lab quantum walk, Quantum Regime Radar |
  | [Building with Quantum Entanglement](https://qollab.xyz/learn/quantum-entanglement) | Bell, GHZ | Market Game, the 2-qubit visualiser, Entangled Body, Quantum Garden, Quantum Patterns, Quantum Butterfly Field |
  | [Quantum Optimization and QAOA](https://qollab.xyz/learn/quantum-optimization) | one layer, penalties, depth on sim vs machine; "from one qubit to a 24-node graph" | |
  | [Quantum Chemistry and VQE](https://qollab.xyz/learn/quantum-chemistry) | H2 on 2 qubits, Hamiltonians, ansätze, shot counts for chemical accuracy, noise | |

  — [Qollab Learn](https://qollab.xyz/learn)
- [Confirmed] Docs: "Account 1 doc, Projects 5 docs, Running code 10 docs, Gates 29 docs, Credits 2 docs, Troubleshooting 3 docs." Each gate page gives "its matrix, its calls in Python and JS, and what it becomes on hardware," including the IonQ natives GPi, GPi2, MS and ZZ. — [Qollab Learn](https://qollab.xyz/learn); [Docs index](https://qollab.xyz/learn/docs)
- [Confirmed] Nothing in Learn covers error correction, fault tolerance or networking. Noise appears only in lesson 6 and in the docs ("Why your results look wrong", "Error mitigation and debiasing", "Ideal vs. noise-model simulators"). — [Qollab Learn](https://qollab.xyz/learn); [Qollab sitemap-content.xml](https://qollab.xyz/sitemap-content.xml)

### Inferences
- [Inferred] QAVE is useful in-project only as a **trace generator**. Python calls `generate_trace_from_qiskit` and returns per-step amplitudes, Bloch vectors, density matrices and entropies to `main.js`, which renders them with three.js or D3. Its animation pipeline cannot run in the browser.
  - A **browser-native renderer for QAVE's `trace.json`** (or for a noise-aware or QEC-specific trace) would fill a real gap Qollab's own team has acknowledged.
  - Forking or extending QAVE must be disclosed.
- [Inferred] QAVE's limits matter for QEC and fault-tolerance teaching:
  - Pure states only and no noise, so errors must be injected as explicit X/Z gates.
  - No S†/T†/SX/P/CP/RZZ/MS gates, so circuits must be transpiled to {x,y,z,h,s,t,rx,ry,rz,cx,cz,ccx,cswap,swap} first.
  - A 16-qubit soft cap. A distance-3 surface code (17 qubits with ancillas) slightly exceeds it; a [[4,2,2]] or Steane encoder fits.
- [Inferred] Because Learn has no QEC, fault-tolerance or networking content, an Unlocked project on those topics also fills a hole in Qollab's own curriculum. That is a plausible "Impact Potential" argument, since a winner gets "featured placement on Qollab."

### Gaps
- `qave==0.1.0` was not imported or tested in Pyodide. That the `generate_trace_*` path works in-browser is inferred from mirya/qave's code, which calls it before exiting. I did not run it.
- The QAVE PyPI page and its 0.1.0 vs GitHub HEAD differences were not checked.
- The lesson bodies of the courses were not fully read; only titles, descriptions and companion-project descriptions were.

---

## Q4. What are the exact mechanics of Qollab's JS↔Python bridge and UI capabilities for an interactive educational tool?

### Takeaway
A project with top-level `index.html` + `main.js` runs as a **JS project** in a sandboxed iframe, rendered above the console. Optional `main.css` is the only stylesheet.

How the bridge works:
- `main.js` imports Qiskit directly (`import { QuantumCircuit } from 'qiskit'`) through Pyodide proxies: no `new`, kwargs via `.callKwargs`, values via `.toJs()`.
- `main.js` imports your own Python modules by dotted name and calls them with `.callPromising(...)`, which is mandatory for anything that may hit IonQ.
- `backend` is injected; whoever presses Run picks it. Judges press Run on a free local simulator.
- three.js 0.186.1, postprocessing, tween.js and meshline import by name. Anything else comes from a CDN `+esm` URL.

Constraints:
- no storage
- GET-only network
- JS cannot read project files (route them through Python)
- `<script>` tags in `index.html` don't run
- one job per run on IonQ backends
- the Sampler primitive silently returns zeros on IonQ

### Cited Findings
**Project type and files**
- [Confirmed] "index.html and main.js at the top level make a JS project (the editor labels it HTML/JS). Your page renders above the console, and its JavaScript can call Python." A top-level `main.py` alone makes a Python project. "Files in folders do not count." — [Runtime environment](https://qollab.xyz/learn/docs/runtime-environment)
- [Confirmed] The JS project "runs entirely in the browser, in a sandboxed iframe, which means it has no browser storage and keeps nothing between runs." Build one "when you want a widget, an animation, or a custom chart rather than plain text output." — [JS / Qiskit projects](https://qollab.xyz/learn/docs/js-qiskit-projects)
- [Confirmed] HTML and CSS rules:
  - "index.html is placed inside the page body, so write body content only. The runtime drops <html>, <head> and <body> tags. <script> tags do not run, so put your code in main.js."
  - "main.css is optional and is the only stylesheet the runtime loads. Other .html and .css files are not loaded."
  - `console.log` prints each argument as text, so use `JSON.stringify` for objects.

  — [Runtime environment](https://qollab.xyz/learn/docs/runtime-environment)
- [Confirmed] When creating a project, choose "JS / Qiskit wrapper" under Project shape. The starter includes `main.css` and `requirements.txt`. — [Run a circuit in JavaScript (lesson)](https://qollab.xyz/learn/building-your-first-qollab-project/run-in-javascript)

**Calling Qiskit and Python from JS**
- [Confirmed] "The API is the Python Qiskit 2.x API made available to JavaScript":
  - "Import from qiskit," e.g. `import { JobStatus } from 'qiskit.providers.jobstatus'`.
  - "No new": `const circuit = QuantumCircuit(2, 2)`.
  - "Named arguments use .callKwargs": `circuit.draw.callKwargs({ output: 'mpl' })`.
  - "Unpack Python values with .toJs()": `result.get_counts().toJs()`.
  - "backend is pre-created, and running is async": `const job = await backend.run(circuit, { shots: 100 })`. Top-level `await` works, and "the injected setTimeout returns a promise you can await while polling job.status() against JobStatus.DONE and JobStatus.ERROR."

  — [JS / Qiskit projects](https://qollab.xyz/learn/docs/js-qiskit-projects)
- [Confirmed] Your own Python from JS:
  - `import * as bell from 'quantum.bell'; const counts = (await bell.run_bell.callPromising(backend, 1000)).toJs();`
  - Use `.callPromisingKwargs` for keyword arguments.
  - "On IonQ backends, a plain call such as bell.run_bell(backend, 1000) stops the run with a ConnectionError that says XHR is not supported."
  - "Use named imports or import * as; a default import of a Python module gives undefined."
  - "A Python package that only your JavaScript imports is not installed automatically, so add it to requirements.txt."

  — [JS / Qiskit projects](https://qollab.xyz/learn/docs/js-qiskit-projects); [Runtime environment](https://qollab.xyz/learn/docs/runtime-environment)
- [Confirmed] "Python print() inside a function called from JavaScript does not reach the run console, so return the value and pass it to console.log() instead." — [Run a circuit in JavaScript](https://qollab.xyz/learn/building-your-first-qollab-project/run-in-javascript)
- [Confirmed] Getting a complex statevector into JS (official project code): "A raw numpy complex array does not cross into JS cleanly, so the real and imaginary parts are split on the Python side first and unpacked with toJs()":

  ```js
  const sv = Statevector.from_instruction(qc);
  const re = sv.data.real.tolist().toJs();
  const im = sv.data.imag.tolist().toJs();
  ```

  Here `import { Statevector } from 'qiskit.quantum_info'`. — [qollab/interactive-bloch-sphere](https://qollab.xyz/u/qollab/interactive-bloch-sphere)
- [Confirmed] JS file imports: "a path that starts with ./ or ../. The runtime tries the exact path, then adds .js or .mjs, then looks for index.js or index.mjs… Other file types cannot be imported." Python imports work normally from the project root (first on `sys.path`). A file of yours "with the same name as an installed package wins over the package." — [Runtime environment](https://qollab.xyz/learn/docs/runtime-environment)

**Rendering and graphics**
- [Confirmed] Bundled JS libraries: "three and three/addons/… (three.js 0.186.1) and postprocessing (6.39.5) can be imported by name, and @tweenjs/tween.js and meshline are bundled in. Import anything else from a full URL, such as https://cdn.jsdelivr.net/npm/<package>/+esm." — [Runtime environment](https://qollab.xyz/learn/docs/runtime-environment)
- [Confirmed] Matplotlib in a JS project: "circuit.draw.callKwargs({ output: 'mpl' }) returns a Matplotlib figure. The call needs Qiskit Visualizations turned on first, in the Libraries list. Pass the figure to URL.createObjectURL(figure) to get a URL you can drop into an <img>; the runtime turns the figure into an SVG." — [JS / Qiskit projects](https://qollab.xyz/learn/docs/js-qiskit-projects)
- [Confirmed] In Python projects, "plt.show() shows the figure as an SVG. plt.savefig("result.png") shows it and offers the PNG as a download." `sendFile(name, content_type, data)` (from `js`) puts any file in the console, with image previews and copy buttons for text/JSON/LaTeX. — [Runtime environment](https://qollab.xyz/learn/docs/runtime-environment)
- [Confirmed] Changelog (Aug 30, 2026): "plt.show() and savefig() render in the output pane, in every format matplotlib can write." Pyodide 314.0.6 (Python 3.14). qiskit-aer runs in the browser (Jun 9), with statevector simulation "about 2.67x faster" since Jul 8. Project write-ups render TeX before markdown (Aug 15) and support YouTube embeds (Apr 26). — [Qollab changelog](https://qollab.xyz/explore/changelog)
- [Confirmed] "QuTiP has no WebAssembly build." — [onri-jay-benally/2-qubit-state-visualization](https://qollab.xyz/u/onri-jay-benally/2-qubit-state-visualization)

**Data, storage, network**
- [Confirmed] "JavaScript cannot read project files: fetch("data.csv") does not reach them. To get data into the page, read it in a Python module and return it to main.js."
- [Confirmed] Python loads only files whose path "appear[s] as a plain string" in code. Paths built with f-strings or `os.path.join` "are not picked up."

  — [Runtime environment](https://qollab.xyz/learn/docs/runtime-environment)
- [Confirmed] "localStorage, sessionStorage, IndexedDB and cookies are not available… ship it as a project file, such as states/demo.json." — [Runtime environment](https://qollab.xyz/learn/docs/runtime-environment)
- [Confirmed] Network rules:
  - GET only; "POST, PUT, DELETE… are blocked."
  - "XMLHttpRequest, WebSocket and web workers are not available."
  - The JS frame sends `Origin: null`, so servers must allow `Access-Control-Allow-Origin: *`.

  — [Runtime environment](https://qollab.xyz/learn/docs/runtime-environment)
- [Confirmed] Limits: "A project holds up to 100 files of up to 2 MB each, and all your projects together can use 200 MB. A run has no time limit." Stop gives Python 5 s to finish. — [Runtime environment](https://qollab.xyz/learn/docs/runtime-environment)

**Python-side run form (`main()` parameters)**
- [Confirmed] In a Python project, a `main()` whose one-line signature has only `int`/`float`/`str`/`bool` annotated parameters makes Run show a form "under Run settings, at the top of the Select QPU dialog." Parameter names become labels ("lowProbabilityThreshold" shows as "Low Probability Threshold"). Breaking the rules means silently no form and no call. — [Runtime environment](https://qollab.xyz/learn/docs/runtime-environment)

**Backend selection, attributes and judging**
- [Confirmed] "Whoever presses Run picks one in the Select QPU dialog, and the runtime hands it to your code as backend… Do not create or hardcode a backend yourself." — [Runtime environment](https://qollab.xyz/learn/docs/runtime-environment)
- [Confirmed] "Judges run every project on a free local simulator." The FAQ says judges "press Run on a free simulator." — [Rules & terms](https://qollab.xyz/programs/hackathon/terms); [How it works](https://qollab.xyz/programs/hackathon/how-it-works)
- [Confirmed] Local and ideal backends:
  - "Built-in simulator" = Qiskit `BasicSimulator`, 24 qubits, ideal.
  - "AWS Braket local simulator" = `StateVectorSimulator`, 25 qubits.
  - IBM noise-model simulators run Aer with fake-backend noise.
  - IonQ remote simulators are "IonQ's cloud simulator with that QPU's noise model."
- [Confirmed] "On a 10-qubit test circuit with one mid-circuit measurement, 1,000 shots took 13 seconds instead of 0.07" on BasicSimulator, which re-runs per shot when measurements or resets are mid-circuit.

  — [Ideal vs. noise-model simulators](https://qollab.xyz/learn/docs/ideal-vs-noise-model-simulators); [Compute backends](https://qollab.xyz/learn/docs/compute-backends)
- [Confirmed] Backend attributes readable in JS, from official project code:
  - `backend.name` (may be a function: `(typeof raw === 'function') ? raw.call(backend) : raw`)
  - `backend.num_qubits`
  - `backend.options.noise_model`

  Each is wrapped in try/catch because "backend does not advertise a width" or "carries no noise model." These are "Metadata only - reading it does not talk to the provider." — [qollab/interactive-bloch-sphere](https://qollab.xyz/u/qollab/interactive-bloch-sphere)
- [Confirmed] Shots: "Leave the argument out and the backend's own default applies, which is 1024 on both the built-in simulator and the IonQ backends." On the built-in simulator and IonQ backends, a Probabilities panel shows beside the console, and IonQ runs add a Circuit panel. — [Running your code](https://qollab.xyz/learn/docs/run-your-code)
- [Confirmed] One job per run on IonQ (remote simulators and QPUs). "Pass every circuit the run needs to a single backend.run call." Local simulators take unlimited jobs. — [Runtime environment](https://qollab.xyz/learn/docs/runtime-environment)
- [Confirmed] Primitives:
  - `BackendSamplerV2` "does not work on IonQ backends: the wrapper reads… memory, which qiskit-ionq 1.0.2 does not return, and fills every shot with 0 instead, so a Bell pair comes back as all 00 with no error."
  - `BackendEstimatorV2` works everywhere, but on IonQ only "one call per run" with every circuit/observable inside it.

  — [Primitives](https://qollab.xyz/learn/docs/primitives)
- [Confirmed] Qollab's own teleportation example uses deferred measurement (controlled CX/CZ corrections) because IonQ cloud lacks mid-circuit measurement with classical feedback. — [qollab/quantum-teleportation](https://qollab.xyz/u/qollab/quantum-teleportation)

**Project page and publishing**
- [Confirmed] The write-up (Project Card) is Markdown with a Preview toggle and math. The sidebar holds contributors, tags, About, versions, repo and website links. — [Write your project page](https://qollab.xyz/learn/docs/write-your-project-page); [Project anatomy](https://qollab.xyz/learn/docs/project-anatomy)
- [Confirmed] A top-level `README.md` in an upload becomes the write-up, up to 65,000 characters. — [Upload your files](https://qollab.xyz/learn/docs/upload-your-files)
- [Confirmed] Publishing creates immutable versions (v1.0, v1.1, …), up to 10 per hour. The project is public at `qollab.xyz/u/<user>/<project>` once a default version exists. — [Publishing and versions](https://qollab.xyz/learn/docs/publish)
- [Confirmed] Browser support: Chrome, Edge, Opera, or Firefox 153+; "Safari is not supported." — [Runtime environment](https://qollab.xyz/learn/docs/runtime-environment)

**Official "anchor run" pattern**
- [Confirmed] Qollab's showcases share a pattern. At load, one small circuit runs on the selected backend as an "anchor," and the interactive physics (Monte Carlo or analytic noise) runs in-browser JS. Examples:
  - ZNE explorer: "executes the real circuit through Qollab's backend to anchor the demo"
  - Repetition-code game: "At load, the encode circuit runs on your selected backend as the anchor"
  - Calibration showcase: "submitted to your selected backend as an anchor"

  — [qollab/error-mitigation-showcase-inte](https://qollab.xyz/u/qollab/error-mitigation-showcase-inte); [qollab/error-correction-showcase-the](https://qollab.xyz/u/qollab/error-correction-showcase-the); [qollab/calibration-showcase-where-t1](https://qollab.xyz/u/qollab/calibration-showcase-where-t1)

### Inferences
- [Inferred] Recommended architecture for an interactive Unlocked tool:
  1. **Python modules** build Qiskit circuits and compute exact states (`Statevector`/`DensityMatrix`, or Aer for noisy density matrices on local backends). They return plain lists or dicts (split real/imag).
  2. **`main.js`** owns the UI (SVG/D3 via a jsdelivr `+esm` import, or three.js for 3D) and calls Python with `.callPromising`.
  3. Exactly **one** `backend.run` per Run, containing every circuit, so the project works on IonQ's simulator.
  4. Interactive "what-if" sliders recompute locally without new backend jobs.
- [Inferred] JS projects get no `main()` parameter form; that is a Python-project feature. All controls must be built in `index.html`/`main.js`, which suits a GUI anyway.
- [Inferred] For QEC or networking demos with syndrome measurements or feed-forward:
  - Use deferred measurement (coherent CX/CZ corrections) or end-of-circuit syndrome readout plus classical decoding in JS. IonQ lacks mid-circuit feed-forward.
  - Mid-circuit measurements also slow the built-in simulator dramatically: per-shot re-simulation, 13 s per 1,000 shots on a 10-qubit test.
- [Inferred] Never use `BackendSamplerV2`. Use `backend.run(...).result().get_counts()` so results aren't silently zero on IonQ.
- [Inferred] For accessibility, which is a hard requirement, the default dark showcase style needs real ARIA work. In the project-code scan, only 1 of 104 projects used `aria-` or `role=` attributes. That is easy differentiation. Add:
  - keyboard operation for every control
  - text alternatives for every visual state
  - non-color-only encodings (shape and pattern for syndromes)
  - sufficient contrast
  - `prefers-reduced-motion` handling

### Gaps
- No doc states how judges choose among free simulators (built-in, Braket, IBM noise, or IonQ remote). The terms say only "a free local simulator," which suggests the built-in or Braket ideal simulators or the IBM noise models, not IonQ remote.
- Whether `backend.name` and `num_qubits` resolve identically on every backend type is not documented. The only evidence is defensive code in an official project.
- Whether Aer's `DensityMatrix`/noise simulation can be called freely from user code in JS projects (outside the injected backend) is not documented. Aer runs in-browser per the changelog, and PQCA pulls in `qiskit_aer==0.17.2`.
- No doc lists a maximum `index.html`/`main.js` size beyond the 2 MB per-file cap, or any iframe size limits.

---

## Q5. Who are the Qollab mentors (names, expertise), and do any specialize in education?

### Takeaway
No mentor names are public. The mentors page recruits volunteers by expertise area, and a "mentor schedule" becomes visible to teams once the build starts. The named people in Qollab's education orbit are content authors and builders, not confirmed mentors:
- Nicolaas Spijker (Community manager, author of the Learn explainers)
- Onri Jay Benally (Expert notes)
- Inho Choi (QAVE)
- Shivani Mayekar (Georgia Tech, QuantumCanvas, workshops for 250+ people)

### Cited Findings
- [Confirmed] "You choose the area or areas you take questions on: QAOA and variational methods, error mitigation, chemistry, finance, optimization, tooling, or something else, in your own words. Teams pick mentors by area." Education is not a named area.
- [Confirmed] Mentors give "at least two hours across October 10 and 11, in one-hour windows," plus optional async Slack. On Oct 9, "Your windows are on the mentor schedule teams use to find you."
- [Confirmed] Mentors are "Researchers, engineers and graduate students who work with quantum algorithms or quantum applications." "Qollab and IonQ read every application and confirm mentors by email."
- [Confirmed] Mentors may compete: "we keep the teams you compete against out of your windows."

— [Qollab Mentors](https://qollab.xyz/programs/hackathon/mentors)
- [Confirmed] The mentors page text is unchanged between Oct 7 and Oct 9 (text diff), and no names are listed. — [Qollab Mentors](https://qollab.xyz/programs/hackathon/mentors)
- [Confirmed] Nicolaas Spijker is "Community manager, Qollab." He authored the Education roundup, the Spring 2026 cohort post, the QAVE showcase and the Learn concept explainers. — [Qollab Explore: Education](https://qollab.xyz/explore/education); [Meet the Spring 2026 cohort](https://qollab.xyz/explore/spring-2026-cohort)
- [Confirmed] Onri Jay Benally authored all five Expert notes (Jul–Aug 2026) on pulse-level and visualization topics. — [Qollab Expert notes](https://qollab.xyz/explore/expert-notes)
- [Confirmed] Shivani Mayekar: "an M.S. Computer Science student at Georgia Tech… winning the QRISE 2024 Infleqtion Challenge… co-founded Qtangled and has organized quantum computing workshops for over 250 participants." — [Meet the Spring 2026 cohort](https://qollab.xyz/explore/spring-2026-cohort)
- [Confirmed] Qollab platform engineers visible on GitHub: commits on `qollabxyz/qiskit` and `qollabxyz/qiskit-ionq` by "Mirya" and "Kenzo." Inho Choi also appears as a contributor to the upstream qiskit-ionq history. — [GitHub qollabxyz/qiskit commits](https://api.github.com/repos/qollabxyz/qiskit/commits); [GitHub qollabxyz/qiskit-ionq commits](https://api.github.com/repos/qollabxyz/qiskit-ionq/commits)
- [Confirmed] The site's JS bundle includes a `mentor-booking` stylesheet chunk, which suggests an in-platform mentor-booking UI. — [Qollab Nuxt entry bundle](https://qollab.xyz/_nuxt/C30t4T_n.js)

### Inferences
- [Inferred] Education-flavored help is most likely under "tooling" (Qollab platform) or "error mitigation" mentors. For a QEC or fault-tolerance teaching tool, check the mentor schedule at 19:00 ET for anyone listing QEC or fault tolerance.
- [Inferred] Theme-leaning answers at registration were used "to plan mentors and AMA topics." If many registrants leaned toward Unlocked, some mentors may be matched to it, but nothing confirms this.

### Gaps
- Mentor names, affiliations and areas are not public. They appear only on the in-event mentor schedule and in Slack.
- No confirmation that any mentor specializes in education or pedagogy.
- The identities of the Georgia Tech faculty or staff judge and of the Qollab and IonQ judge representatives remain unpublished.
