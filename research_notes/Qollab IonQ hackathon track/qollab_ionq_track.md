# Qollab and the Qollab × IonQ Track at Georgia Tech Qiskit Fall Fest 2026

Research current as of 2026-10-07, two days before the build window opens on Oct 9 at 19:00 ET. Primary sources are the Georgia Tech event site (a Lovable SSR page, read from its raw HTML) and Qollab's own pages: the hackathon hub, how-it-works/FAQ, rules and terms, mentors, programs, docs, privacy policy and contributors. Pages that render client-side were read in a browser. Labels used below: "Confirmed" means it is stated in a primary source; "Inferred" means it is my reasoning.

## Q1. What is Qollab (and what it is not), and is the event really Georgia Tech-affiliated?

### Takeaway
Qollab (qollab.xyz, two Ls) is a browser-based, open-source quantum-coding community and platform. Its privacy policy says it is operated by a private company, **fluxDev, Inc.** It is not a nonprofit, a student organization or a research lab, and it has no connection to **Qolab** (one L), John Martinis's superconducting-qubit hardware startup. The Georgia Tech event is run by Georgia Tech's student Quantum Computing Association ("Quantum Computing @ GT"). It is one of Qollab's university "nodes" in a global Qollab × IonQ hackathon.

### Cited Findings
**Identity and operator**
- Qollab's privacy policy names the operator as "fluxDev, Inc. (the 'Company')". It defines the Service as one "in which users can create, share, and collaborate on quantum computing projects and educational resources" at qollab.xyz. The policy was last updated September 5, 2026. — [Qollab Privacy Policy](https://qollab.xyz/privacy)
- Self-description: "Qollab is an emerging community effort dedicated to making quantum computing more accessible for builders of all backgrounds and experiences." It says it launched Qollab "to bring together developers, designers, and enthusiasts from around the world to demystify the 'how' of quantum" through shared code, tutorials and showcase demos. — [Qollab About/Mission](https://qollab.xyz/about)
- The site tagline is "Quantum creativity, in the open." The Creative Challenge page describes Qollab as "a community of developers, designers, and creative technologists figuring out what quantum software looks like by actually making things and sharing every step in the open." — [Qollab Creative Challenge page](https://qollab.xyz/explore/creative-challenge)
- IonQ's March 18, 2026 press release calls Qollab a "new, community-led initiative." It lists the platform's features:
  - A browser-based playground that runs quantum code with no setup
  - Sharing, forking and remixing of code
  - Showcases of signature experiments
  - Tips on production-ready apps
  - Coding challenges and tutorials

  The release says Qollab is "in its foundational stage." — [IonQ newsroom](https://www.ionq.com/news/ionq-partners-with-qollabs-creative-challenge-advancing-creative-quantum-innovation)

**Platform and tooling**
- Projects run entirely in the browser:
  - Python runs on Pyodide (WebAssembly). JS projects run in the page.
  - "No code runs on a server except the quantum job itself, which runs on IonQ's servers when you pick a remote backend."

  — [Qollab docs: Runtime environment](https://qollab.xyz/learn/docs/runtime-environment)
- Qiskit is always installed. If `requirements.txt` doesn't name it, the runtime adds `qiskit>=2.5.2,<3.0.0`.
  - Optional one-click libraries: qiskit-algorithms 0.4.0, qiskit-optimization 0.7.0, qiskit-nature 0.8.0 plus pyscf, qiskit-finance 0.4.1, qiskit-machine-learning 0.9.1, qave 0.1.0, and PQCA (which brings qiskit_aer 0.17.2 and qiskit_ibm_runtime 0.50.0).
  - Pure-Python PyPI wheels and Pyodide-built packages also install. NumPy, SciPy and Matplotlib auto-load.

  — [Qollab docs: Runtime environment](https://qollab.xyz/learn/docs/runtime-environment)
- The Qollab GitHub org `qollabxyz` (created 2025-10-08) has three public repos:
  - `qiskit`: "A fork of Qiskit with local patches to make it more usable in Qollab/Pyodide environment"
  - `qiskit-ionq`: "Qiskit provider for IonQ backends: a fork with changes specific to Qollab/Pyodide environment"
  - `qave`: Quantum Algorithm Visualization Engine

  — [GitHub qollabxyz](https://github.com/qollabxyz) (via GitHub API)
- Official LinkedIn: linkedin.com/company/qollabxyz, from the page's JSON-LD. — [Qollab Creative Challenge page](https://qollab.xyz/explore/creative-challenge)
- Scale: 35 contributors, 88 projects, 7 total forks. The top publisher is "Qollab Team (@qollab)" with 51 projects. — [Qollab Contributors](https://qollab.xyz/contributors)
- Qollab's current programs:
  - The Qollab Quantum Hackathon
  - The Qollab Grant Program: "Port, fork, or publish open-source quantum work on Qollab and earn up to $20,000 in IonQ compute credits," reviewed on a rolling basis
  - The past Quantum Creative Challenge, closed April 7, 2026

  — [Qollab Programs](https://qollab.xyz/programs)

**Disambiguation**
- **Qolab** (one L, qolab.ai) is a superconducting quantum hardware startup. It was co-founded by Alan Ho (CEO, ex-Google Quantum AI), John Martinis (CTO, 2025 Nobel laureate in Physics) and Robert McDermott (Head of Hardware, UW–Madison). It has no stated connection to Qollab. — [Qolab team](https://qolab.ai/team); [BusinessWire: Martinis Nobel](https://www.businesswire.com/news/home/20251008963295/en)
- GitHub has many unrelated "qollab" repos and accounts, for example a QGIS plugin "QollabEO" and a self-hosted Quarto editor "luftaquila/qollab". Only `qollabxyz` is tied to qollab.xyz. — [GitHub search API, "qollab"](https://github.com/search?q=qollab&type=repositories)
- "Quantum Garden," the Qollab Creative Challenge winner, is not the Aalto University / Robin Baumgarten citizen-science installation of the same name. — [Aalto: Quantum Garden](https://www.aalto.fi/news/world-premiere-play-quantum-garden-and-help-build-a-quantum-computer); [Qollab Creative Challenge page](https://qollab.xyz/explore/creative-challenge)

**Georgia Tech affiliation**
- The event site's schema.org metadata lists:
  - Organizer: "Quantum Computing @ GT" (LinkedIn: georgiatech-quantum)
  - Location: Georgia Institute of Technology, Atlanta
  - Event: "Georgia Tech Qiskit Fall Fest 2026", Oct 1–16

  The footer reads "Quantum Computing Student Association at Georgia Institute of Technology" and lists event partners "IBM & IonQ". — [GT Fall Fest site](https://qhackathon-gt.lovable.app/)
- The Terms & Conditions say the event is "organized by the Quantum Computing Association." They also say Qollab/IonQ prizes "are provided and administered by the relevant partner organization and are not provided or guaranteed by the Quantum Computing Association." — [GT Participant Terms](https://qhackathon-gt.lovable.app/terms-and-conditions)
- Georgia Tech appears in Qollab's official list of participating nodes (North America). — [Qollab Hackathon hub](https://qollab.xyz/programs/hackathon)
- The GT site is also part of IBM's Qiskit Fall Fest 2026; it links to IBM's Fall Fest page and an IBM check-in at ibm.biz/IBMQFF26. — [GT Fall Fest site](https://qhackathon-gt.lovable.app/)

### Inferences
- Qollab is best described as a for-profit startup (fluxDev, Inc.) that runs a community platform. The "community" framing is marketing; the legal operator is a company. Its business model appears to be at least partly reselling IonQ compute: the credits doc says "Qollab charges credits from your balance" and calls Qollab IonQ's "partner." — [Qollab docs: How credits work](https://qollab.xyz/learn/docs/how-credits-work)
- The site is on lovable.app rather than gatech.edu, so it is student-built. The GT affiliation is real at the student-org level, confirmed by Qollab's node list. It is not an official Institute-run event.

### Gaps
- **Founders and team:** I found no public names. The About page, privacy policy, contributors page (only "Qollab Team @qollab"), IonQ press release and Quantum Zeitgeist article all omit them. Searches for "fluxDev, Inc." returned nothing relevant. LinkedIn (company/qollabxyz) was not readable without sign-in.
- **Funding, headquarters and incorporation state** of fluxDev, Inc.: not found.
- Whether "Quantum Computing @ GT" is the same group as the "Georgia Tech Quantum Computing Association" listed by qBraid: not directly confirmed. The GT terms page uses "Quantum Computing Association," which suggests it is.

## Q2. What does the Qollab × IonQ track ask of competitors: problem statement, deliverables, judging, prizes, starter code?

### Takeaway
There is no single problem statement. Teams of 1–4 build any open-source Qiskit project in 48 hours (Oct 9, 19:00 ET to Oct 11, 19:00 ET). Each project must be published and runnable on Qollab under MIT, include a 2–3 minute demo video, and optionally target one of three themes: **Quantum Impact** (hybrid quantum-classical against a classical baseline), **Quantum Playground** (art, games, music) or **Quantum Unlocked** (teaching tools).

Judging covers four criteria: **Novelty & Creativity, Technical Execution, Impact Potential, Documentation Quality**. No weights are published. Judging is local first, then global.

There is no official starter repo. Starting points are Qollab's Learn courses and its forkable projects.

### Cited Findings
**Dates, all ET**
- Registration opened Sept 28 at 11:00. An optional AMA was held Sept 29 at 13:00. Registration closes **Oct 8 at 11:00**.
- The build runs Oct 9 at 19:00 to **Oct 11 at 19:00**, which is also the submission deadline.
- Local judging finishes the week of Oct 12. Global winners are announced the week of Oct 19.

— [Qollab Rules & Terms](https://qollab.xyz/programs/hackathon/terms); [Qollab How it works](https://qollab.xyz/programs/hackathon/how-it-works)

**Conflict on the registration deadline:** Quantum Zeitgeist (Sept 7, 2026) gave Oct 6 at 11:00 ET, and a QUTE.sk (Slovak node) LinkedIn post surfaced in search also said Oct 6. Official Qollab pages and the GT site say Oct 8 at 11:00 ET. The official date should govern. — [Quantum Zeitgeist](https://quantumzeitgeist.com/ionq-quantum-hackathon-qollab-host/); [Qollab Hackathon hub](https://qollab.xyz/programs/hackathon)

**GT-specific schedule**
- Georgia Tech Demo Day is Oct 16, 4:00–6:00 PM ET. The site says it "is not the submission deadline."
- IBM guest sessions with James Weaver (IBM Quantum) are on Oct 8 at 7 PM and Oct 9 at 8 PM ET. These belong to the IBM/BasQ track.

— [GT Fall Fest site](https://qhackathon-gt.lovable.app/)

**Team and eligibility**
- Solo or up to 4 people, aged 18+, based in one of 45 eligible countries (the US is included).
- Everyone on a team competes at the same node.
- A student-track team must have every member enrolled at the node university; all other teams register as professional. Both tracks use the same rubric and the same prize pools.
- A team may submit up to 5 projects, each judged separately. Each person can be on only one team.

— [Qollab Rules & Terms](https://qollab.xyz/programs/hackathon/terms); [Qollab How it works](https://qollab.xyz/programs/hackathon/how-it-works)

**Registration**
- Georgia Tech participants must complete both the GT form and the separate Qollab registration. The site says the "Georgia Tech form does not register you for the partner competition."

— [GT Fall Fest site](https://qhackathon-gt.lovable.app/)

**Themes (official wording, lightly condensed)**
- **Quantum Impact:** "Take on a real challenge in logistics, manufacturing, space, finance, energy or another industry with a hybrid quantum-classical approach: pick a public dataset, build a strong classical baseline, then show where a quantum subroutine makes a measurable difference."
- **Quantum Playground:** "Turn quantum mechanics into a creative medium: a game, music, art, an interactive experience… The bar is that superposition, interference, entanglement or measurement is essential to the piece, beyond simply generating randomness."
- **Quantum Unlocked:** "Pick a hard, timely topic such as error correction, fault tolerance, quantum networking or algorithms, and teach it: an interactive demo, animation, visualisation or GUI that makes it intuitive."
- Projects that fit no theme are still eligible for placement and local awards, but not theme specialty awards. You declare a theme at submission and can change it until the deadline.

— [Qollab How it works (FAQ)](https://qollab.xyz/programs/hackathon/how-it-works)

The GT site adds that "Challenge themes and problem statements will be shared before the hackathon begins, following each sponsor's release schedule." — [GT Fall Fest site](https://qhackathon-gt.lovable.app/)

**Hard submission requirements**
- Use Qiskit.
- Follow UI accessibility best practices.
- Run on Qollab's free simulators, including IonQ's simulator.
- Be published and runnable on qollab.xyz under the MIT license before the deadline.
- Have a Qollab project page that explains the problem and how to run it, with enough detail to "understand, replicate, or extend it."
- Be built during the build window. Existing code, AI tools, templates and forks are allowed only if disclosed; judging covers what the team adds.
- Include a 2–3 minute demo video at a public, no-sign-in link (YouTube, Loom, Vimeo or Google Drive). A screen recording with voiceover is enough.
- Include the attribution: "This effort is supported by Qollab & IonQ".
- Stay hosted on Qollab for 12 months.

— [Qollab Rules & Terms](https://qollab.xyz/programs/hackathon/terms); [Qollab How it works](https://qollab.xyz/programs/hackathon/how-it-works)

**"Beyond the tutorial bar"**
Each submission must show at least one of:
- A novel application or problem context
- A technical extension
- An original analytical or educational contribution

Panels may score a project **0 on Novelty & Creativity and Technical Execution** if it fails this bar. (Paraphrased from the rules page via a fetch summary.) — [Qollab Rules & Terms](https://qollab.xyz/programs/hackathon/terms)

**Judging**
- The four traits are Novelty & creativity, Technical execution, Impact potential, and Documentation quality. "Local judges score first. Top scorers advance to a global panel, which re-scores using the same rubric." No weights or point scales are published.
- Judges "open the project page, read the description and the code, and press Run on a free simulator." Hardware versus simulator use "is not scored." IonQ results "neither add nor subtract points."
- Scoring decisions are final except for disqualification. A disqualification can be appealed within 24 hours to hello@qollab.xyz.

— [Qollab How it works (FAQ)](https://qollab.xyz/programs/hackathon/how-it-works); [Qollab Rules & Terms](https://qollab.xyz/programs/hackathon/terms)

**Prizes, global**

| Place | Cash | Compute credits |
|---|---|---|
| 1st | US$10,000 | US$20,000 |
| 2nd | US$5,000 | US$15,000 |
| 3rd | US$2,500 | US$10,000 |

- Six specialty awards, each US$500 cash plus US$5,000 compute: Most Novel/Creative, Most Impact, Best Documentation, and Best of each theme (Quantum Impact, Quantum Playground, Quantum Unlocked). A project can win both a placement and a specialty award.
- The global top 3 also get three one-to-one mentorship sessions with IonQ engineers over 12 months, plus 12 months of expedited IonQ interview access. Interns and early-career applicants skip initial screening. Employment is not guaranteed.

— [Qollab How it works](https://qollab.xyz/programs/hackathon/how-it-works); [GT Fall Fest site](https://qhackathon-gt.lovable.app/)

**Prizes, local (Georgia Tech node)**
- Local awards apply only if the node gets **10 or more eligible submissions**:

| Place | Cash | Compute credits |
|---|---|---|
| 1st | US$500 | US$5,000 |
| 2nd | US$300 | US$3,000 |
| 3rd | US$200 | US$2,000 |

- With fewer than 10 submissions, the top 3 advance directly to global judging and there are no local cash awards.
- Each node may also advance up to one project per specialty category.
- Disqualified teams forfeit unused credits.

— [Qollab Rules & Terms](https://qollab.xyz/programs/hackathon/terms); [GT Fall Fest site](https://qhackathon-gt.lovable.app/)

**Qollab Fellows**
- Qollab "may invite selected participants to become Qollab Fellows" from November to April. Fellows receive cash, research compute credits and a small grant pool, and help onboard newcomers. Qollab runs this separately from IonQ.

— [Qollab How it works](https://qollab.xyz/programs/hackathon/how-it-works)

**Starter code and resources**
- No official starter repo or notebook was found.
- The organizers point to:
  - Qollab's six-lesson course "Programming your first quantum circuits," which runs circuits on the IonQ simulator from the browser. Lesson 6 is "Noise, and the real machine."
  - Concept explainers with forkable code: QAOA (up to a 24-node graph), VQE on hydrogen, interference/Grover, and entanglement.
  - Docs on compute backends, publishing, writing a project page, and the runtime environment.

  — [Qollab Learn](https://qollab.xyz/learn); [Qollab How it works](https://qollab.xyz/programs/hackathon/how-it-works)
- Two forks are cited as examples of properly disclosed starting code: "QCFlows: Multi-file Example" and "Quantum Hackathon Soundtrack." — [Qollab How it works (FAQ)](https://qollab.xyz/programs/hackathon/how-it-works)
- GitHub search for "qollab ionq" found only one participant's empty repo, `DianaDancea/Qollab-and-IonQ-Hackathon-2026`, created Oct 7, 2026. "qhackathon" results are unrelated, mostly a Korean Qiskit hackathon and other QHackathons. — [GitHub: DianaDancea/Qollab-and-IonQ-Hackathon-2026](https://github.com/DianaDancea/Qollab-and-IonQ-Hackathon-2026)

**Runtime constraints that matter for building**
- The `backend` object is injected by the runtime, chosen by whoever presses Run. "Do not create or hardcode a backend yourself."
- **IonQ backends accept one job per run**, so "put everything an IonQ run measures into one circuit" or pass all circuits in a single `backend.run` call.
- Network access is GET-only and needs CORS (`Access-Control-Allow-Origin: *`). POST, WebSockets and workers are blocked.
- Nothing persists between runs, so ship saved data as project files. `input()` does not work.
- If `main()` has typed parameters (int, float, str or bool), Run shows a form for them.
- `index.html` plus `main.js` makes a JS project with a rendered page that can call Python.
- Limits: 100 files of 2 MB each, 200 MB per account, no run time limit.

— [Qollab docs: Runtime environment](https://qollab.xyz/learn/docs/runtime-environment)

### Inferences
- **Fit to IonQ's constraints.** Since judges press Run on a free local simulator, the project must run quickly and reliably on the built-in simulator (24 qubits) or the AWS Braket local simulator (25 qubits). Also test it once on an IonQ remote simulator within the one-job-per-run rule. A run failure is the only way IonQ limits affect the score.
- **Theme strategy.** Each theme has its own US$500 + US$5k specialty award, and Best Documentation is a separate award. A well-documented, themed project has several paths to a prize.
  - For Quantum Impact, an honest comparison against a strong classical baseline on a public dataset is explicitly what judges want. The showcase project "Quantum Courier," which "shows honestly which one wins," is the model for this framing.
  - For Playground, randomness alone fails the bar; interference, entanglement or measurement must matter to the experience.
- **Interactive projects.** JS projects with `index.html` + `main.js` give a rendered interactive page, which suits Playground and Unlocked. Accessibility (contrast, legible fonts) is a stated requirement.
- **Documentation counts.** Documentation Quality is a full rubric trait and a specialty award, so the Qollab project page deserves real time. It should state the problem, explain how to run it, disclose prior code and AI use, include the attribution line, and give a replication/extension path.
- **GT node size.** Demo Day on Oct 16 is after submissions and outside Qollab judging. It is for local recognition only. Whether GT reaches 10 submissions decides if local cash awards exist; either way the top 3 go to global judging.

### Gaps
- No track-specific problem statements beyond the three themes were found. The GT site says sponsor materials will be linked "as they become available." Check again at kickoff (Oct 9, 19:00 ET) and in the Qollab Slack.
- Rubric weights, point scales and per-criterion descriptors are not published.
- No official starter repo or notebook exists on GitHub for this hackathon.

## Q3. What have Qollab and IonQ done together before?

### Takeaway
They have collaborated at least three times:
- The **Quantum Creative Challenge** (2nd edition, spring 2026, IonQ as official partner). The inaugural edition ran in "Winter of 2025," and the sources do not say whether IonQ was involved then.
- The ongoing **Qollab Grant Program**, which pays out IonQ credits.
- This **global hackathon**, with Qollab acting as an IonQ access partner.

Past winners are creative and educational visual projects, not benchmark-style algorithm papers.

### Cited Findings
**Creative Challenge 2026 (2nd annual)**
- IonQ announced the collaboration on Mar 18, 2026.
- Prizes: $50,000 in IonQ compute credits funded by Qollab, up to $5,000 cash per team, and an extra $20,000 in IonQ credits for the first three selected teams.
- IonQ provided technical support, judged submissions, promoted projects, mentored teams and offered presentations to IonQ's executive team.
- Submissions were due Apr 7, 2026, with public launches around end of May 2026.

— [IonQ newsroom](https://www.ionq.com/news/ionq-partners-with-qollabs-creative-challenge-advancing-creative-quantum-innovation)

- Challenge requirements:
  - Qiskit
  - Open source in a public repo
  - Listed on Qollab with runnable examples
  - Documentation sufficient to "understand, replicate, or extend"
  - Basic accessibility
  - Public for 12 months
- The creative brief asked for work that demonstrates quantum speedups; uses "superposition, entanglement, interference, or probabilistic outputs as part of its storytelling"; inspires curiosity; and encourages remixing, with "Bonus points for quirky and playful."
- Review criteria: creativity and originality; technical feasibility; clarity of idea and potential impact; and "Alignment with our open, accessible ethos."
- Credits "expire after 60 days." Selected teams also got "Weekly support from IonQ experts."
- The page says the challenge "funded developers to build on real IonQ hardware with Qiskit."

— [Qollab Creative Challenge page](https://qollab.xyz/explore/creative-challenge); [Qollab Programs](https://qollab.xyz/programs)

**Inaugural challenge winners ("Winter of 2025")**
- **Quantum Garden:** "An interactive generative art installation… where digital plants exist in quantum superposition until observed."
  - Credited builders differ by source. The Creative Challenge page says "Amber Pincar and Justin Pincar," the Explore page says "Amber Wang & Justin Pincar," and the IonQ release uses the username "AmberPincar."
- **QAVE (Quantum Algorithm Visualization Engine)**, by Inho Choi (@q-inho): "A scientifically rigorous quantum circuit and algorithm visualization engine built for teaching and conceptual clarity." It is now a Qollab-maintained library (`qave==0.1.0`) and a qollabxyz GitHub repo.

— [Qollab Creative Challenge page](https://qollab.xyz/explore/creative-challenge); [Qollab Explore](https://qollab.xyz/explore); [IonQ newsroom](https://www.ionq.com/news/ionq-partners-with-qollabs-creative-challenge-advancing-creative-quantum-innovation); [GitHub qollabxyz/qave](https://github.com/qollabxyz/qave)

**Other featured projects (likely 2026 Challenge outputs)**
The Explore page features:
- Entangled Body (Chanhyuk Park & Luke Shim)
- QCFlows
- Quantum Patterns (live-coding music)
- Superposition Sequencer
- Musiq
- Quantum Courier (classical vs. quantum on five logistics problems)
- Quantum Systemic Oracle (portfolio-optimization circuit on IonQ feeding an on-chain risk score)
- qOrbital (quantum chemistry with hardware noise visualized)
- Quantum Advantage Lab
- Quantum Regime Radar (QML market-regime detection)
- Quantum Market Game
- Quantum Butterfly Field
- QuantumCanvas

— [Qollab Explore](https://qollab.xyz/explore)

- **Entangled Body** is under a GitHub org named "IonQ-Qollab-Quantum-Challenge." It uses a Next.js/Three.js frontend and a FastAPI backend with Qiskit Aer, with optional IonQ simulator or hardware. — [GitHub: IonQ-Qollab-Quantum-Challenge/Entangled-Body](https://github.com/IonQ-Qollab-Quantum-Challenge/Entangled-Body)

**Grant Program and access partnership**
- Grants: "Up to $20,000 in IonQ compute credits per project," rolling, MIT, runnable on Qollab for one year. — [Qollab Programs](https://qollab.xyz/programs)
- Qollab describes itself as IonQ's partner for hardware access: IonQ's pricing "may not apply directly to anyone reaching those systems through a partner… Qollab is that partner." — [Qollab docs: How credits work](https://qollab.xyz/learn/docs/how-credits-work)

### Inferences
- The Qollab–IonQ relationship works like a channel or ecosystem partnership. IonQ supplies hardware, simulators, credits, engineers and judging; Qollab runs the community, platform and programs.
- Past winners favor visual, interactive, remixable and educational work. That suggests Playground and Unlocked entries play to the judges' demonstrated taste. Impact entries need rigorous honest baselines to stand out.

### Gaps
- The inaugural (Winter 2025) Creative Challenge's prize structure, IonQ's involvement in it, and its number of entrants were not found.
- The official list of 2026 Creative Challenge awardees was not found. The Explore-page projects are likely but unconfirmed recipients.
- IonQ–Georgia Tech institutional ties were not researched in depth. No IonQ announcement about this October hackathon was found on ionq.com. The only press coverage is Quantum Zeitgeist.

## Q4. Who from Qollab or IonQ is likely to judge or mentor?

### Takeaway
No judges, mentors or committee members are named anywhere public. Each local panel consists of a faculty or staff judge plus Qollab and IonQ representatives. Mentors are openly recruited volunteers (researchers, engineers, grad students) who commit to live one-hour windows on Oct 10–11.

### Cited Findings
- "Who judges the local round? A local panel including a faculty or staff judge, alongside Qollab and IonQ representatives." — [Qollab How it works (FAQ)](https://qollab.xyz/programs/hackathon/how-it-works)
- The mentors page names no one. Mentors commit to "at least two one-hour live windows on October 10 or 11" in their own time zone, plus optional async Slack support. — [Qollab Mentors](https://qollab.xyz/programs/hackathon/mentors)
- Mentor applications were open to researchers, engineers and graduate students anywhere, and mentors may also compete. — [Quantum Zeitgeist](https://quantumzeitgeist.com/ionq-quantum-hackathon-qollab-host/)
- Communication runs on Slack: a node channel for local logistics and a global support channel for platform, submission and hardware questions. — [Qollab How it works (FAQ)](https://qollab.xyz/programs/hackathon/how-it-works)
- IonQ's 2026 press release quotes no named IonQ or Qollab people. — [IonQ newsroom](https://www.ionq.com/news/ionq-partners-with-qollabs-creative-challenge-advancing-creative-quantum-innovation)
- The only named speaker on the GT site is **James Weaver (IBM Quantum)**, who leads the IBM/BasQ track sessions, not Qollab × IonQ. — [GT Fall Fest site](https://qhackathon-gt.lovable.app/)
- Authors on Qollab's content feed include Nicolaas Spijker (Guide, Sep 18, 2026, on quantum compute costs) and Onri Jay Benally (Expert note, Aug 6, 2026, on cross-resonance gates). Their roles at Qollab are not stated. — [Qollab Explore](https://qollab.xyz/explore)

### Inferences
- Qollab's content and docs show what Qollab reviewers are likely to value:
  - Runnable, forkable, well-documented projects
  - Honest reporting of noise and hardware limits, as in the docs on "Why your results look wrong," debiasing and ideal vs. noise-model simulators
  - Accessible UIs
- IonQ representatives will probably appreciate projects that use IonQ-relevant concepts: native gates (GPi, GPi2, MS, ZZ, all documented on Qollab), all-to-all connectivity, debiasing error mitigation, and running against the Forte noise model. This is inference, not a stated criterion.

### Gaps
- The names, titles and research interests of IonQ or Qollab judges and mentors are not public. They may be announced in the Slack channels after registration.
- The identity of the Georgia Tech faculty or staff judge was not found.

## Q5. What resources do track participants get (simulators, noise models, hardware, credits)?

### Takeaway
All simulators are free on Qollab:
- In-browser simulators, including IBM device noise models
- IonQ cloud noise-model simulators for Aria 1/2 (retired hardware), Forte 1 and Forte Enterprise 1

Real IonQ hardware (Forte 1, Forte Enterprise 1, 36 qubits) costs Qollab credits. No build-time hardware credit allotment for hackathon participants was found, and hardware use is not scored. Compute credits are a prize, not an entry resource.

### Cited Findings
**Backends available on Qollab**

Local, in-browser, free:

| Backend | Qubits |
|---|---|
| Built-in simulator | 24 |
| AWS Braket local simulator | 25 |
| IBM noise-model simulators: Boston, Kingston, Pittsburgh, Fez, Marrakesh, Aachen (Heron) | 156 |
| IBM noise-model simulators: Miami, Berlin (Nighthawk r1) | 120 |

Remote IonQ simulators, free, on IonQ cloud (each "a noise model of one IonQ QPU"):

| Backend | Qubits |
|---|---|
| IonQ Aria 1 | 25 |
| IonQ Aria 2 | 25 |
| IonQ Forte 1 | 29 |
| IonQ Forte Enterprise 1 | 29 |

Quantum computers, cost credits:

| Backend | Qubits |
|---|---|
| IonQ Forte 1 | 36 |
| IonQ Forte Enterprise 1 | 36 |

— [Qollab docs: Compute backends](https://qollab.xyz/learn/docs/compute-backends)

**Notes on these backends**
- "IonQ has retired the Aria 1 and Aria 2 hardware, so the two Aria entries model a system that no longer runs." — [Qollab docs: Compute backends](https://qollab.xyz/learn/docs/compute-backends)
- IonQ noise-model simulation is shot-aware, so run time grows with shot count. Simulations near the qubit ceiling "may still fail." Qollab does not show IonQ characterization data; it points users to IonQ's own backend list. — [Qollab docs: Compute backends](https://qollab.xyz/learn/docs/compute-backends)
- "Every simulator is free… You can write, run, and publish an entire project without spending a credit."
  - Hardware runs show an estimate first and ask for confirmation above an allowance, which defaults to a tenth of your balance.
  - IonQ's cost drivers are 1Q and 2Q gate counts after compilation, plus shots. An N-qubit gate counts as 6(N−2) 2Q gates.
  - Debiasing is on by default at 500 or more shots, and there is a per-circuit minimum.

  — [Qollab docs: How credits work](https://qollab.xyz/learn/docs/how-credits-work)

**Hardware for the hackathon**
- Hardware or simulator use "is not scored." Hardware-access questions go to the global Slack support channel. — [Qollab How it works (FAQ)](https://qollab.xyz/programs/hackathon/how-it-works)
- The GT site's checklist says "Use Qiskit on IonQ's quantum simulator." — [GT Fall Fest site](https://qhackathon-gt.lovable.app/)
- Quantum Zeitgeist describes the prize compute as "IonQ hardware time, usable only through the platform, not cash." It says the article "doesn't say whether teams get real hardware access during the build." — [Quantum Zeitgeist](https://quantumzeitgeist.com/ionq-quantum-hackathon-qollab-host/)
- Platform outages: if the platform or simulator is down for more than 12 hours, Qollab may extend the deadline or accept late submissions with an outage-impact statement. Shorter outages do not qualify. — [Qollab Rules & Terms](https://qollab.xyz/programs/hackathon/terms)
- Precedent: Creative Challenge credits expired after 60 days. — [Qollab Creative Challenge page](https://qollab.xyz/explore/creative-challenge)

### Inferences
- Plan the whole project around the free simulators. Use the IonQ Forte 1 remote noise-model simulator (29 qubits, free) to show realistic trapped-ion noise behavior. That is the closest thing to "running on IonQ" available without credits, and it shows IonQ judges you engaged with their platform.
- Keep circuits at 24 qubits or fewer and shot counts modest. The judge's default run on the built-in simulator, and the shot-aware IonQ noise simulation, should finish quickly.
- If a project compares noise models (IBM Heron vs. IonQ Forte), the Qollab backend menu supports this natively. It is a cheap way to add technical depth for Quantum Unlocked or Impact entries. This is inference.

### Gaps
- No confirmation that hackathon registrants receive any starting credit balance for hardware during the build window. Ask in the global Slack support channel.
- The expiry and usage terms of prize credits for this hackathon are not stated. Only the Creative Challenge's 60-day expiry is documented.
- Whether IonQ will publish a hackathon-specific challenge, dataset or noise model at kickoff is unknown.
