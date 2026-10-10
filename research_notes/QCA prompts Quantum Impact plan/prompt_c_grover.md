# QCA Prompt C "Grover the Seismologist": research and experiments for a beyond-tutorial Quantum Impact entry

Notes written Sat 10 Oct 2026, roughly 11:50–14:00 ET. All experiments were run locally (Python 3.11, qiskit 2.3.0, qiskit-aer 0.17.2) on a 20-core machine that other sessions were also using, so wall-clock timings are pessimistic. Scripts, raw outputs and figures are in `scripts/prompt_c/` (paths below are relative to this file). `gs_core.py` holds the shared code: catalog slices, list oracle, honest oracle, diffusion, transpile targets and the noise model. The data snapshot was fetched on 2026-10-10 and lives in `scripts/prompt_c/data/`.

## 1. Data: USGS query and CORS, a sensible "rare, expensive-to-check" condition, real match rates, and what makes a check genuinely expensive

### Takeaway
The USGS FDSN event service is browser-fetchable from Qollab. Both CSV and GeoJSON return `Access-Control-Allow-Origin: *`, and the CORS preflight succeeds. A year of M≥5 events is 1,507 rows, about 0.28 MB as CSV.

The best default condition for 8–64-event slices is **shallow (<70 km) and M≥6.0**, which matches 72 of 1,504 events (4.8%). For a needle-like regime use **shallow and M≥7.0** (8/1,504 = 0.53%) or **PAGER alert ≥ yellow** (20/1,504 = 1.3%).

The predicate itself is not expensive. It is a range filter on two catalog columns, which the USGS server evaluates for you (`minmagnitude=6&maxdepth=70` returns 72 in under a second). The genuinely expensive per-event computations sit downstream and take minutes to hundreds of thousands of core-hours: W-phase moment tensors, tsunami propagation, physics-based ground motion.

### Cited Findings
**Endpoint and CORS (my tests, 2026-10-10 15:46 UTC, request header `Origin: null` as from Qollab's sandboxed iframe)**
- `GET .../fdsnws/event/1/query?format=csv&starttime=2024-01-01&endtime=2024-12-31&minmagnitude=5` returns 200 `text/csv` with these headers: `Access-Control-Allow-Origin: *`, `Access-Control-Allow-Methods: GET, OPTIONS`, `Access-Control-Allow-Headers: *`, `Access-Control-Max-Age: 86400`, `Cache-Control: public, max-age=60` (served via CloudFront). — [USGS FDSN query (CSV)](https://earthquake.usgs.gov/fdsnws/event/1/query?format=csv&starttime=2024-01-01&endtime=2024-12-31&minmagnitude=5)
- The OPTIONS preflight returns 200 with the same ACAO/ACAM headers. `format=geojson` also returns ACAO `*`. This agrees with the earlier GeoJSON test in prior notes. — [USGS FDSN docs](https://earthquake.usgs.gov/fdsnws/event/1/); [prior notes: benchmarking_and_build_stack.md](../Quantum%20Impact%20theme%20deep%20dive/benchmarking_and_build_stack.md)
- The slide's example URL uses `endtime=2024-12-31`, which **excludes Dec 31**. It returns 1,504 events (283,862 bytes CSV; 1,124,116 bytes GeoJSON). `endtime=2025-01-01` returns 1,507. — [count endpoint](https://earthquake.usgs.gov/fdsnws/event/1/count?starttime=2024-01-01&endtime=2025-01-01&minmagnitude=5); [data files](scripts/prompt_c/data/)
- 2024 counts from the `count` endpoint: all magnitudes 155,899; M≥2.5 25,153; M≥4.5 6,397 (1.21 MB CSV); M≥5 1,507; M≥6 99; M≥7 10. — [results_c01](scripts/prompt_c/results_c01_match_rates.txt)
- The CSV has no `alert`, `tsunami`, `felt`, `sig` or product `types` columns. GeoJSON has all of them, so use GeoJSON, or ship a slim JSON snapshot (all 1,504 events, 0.46 MB with product types; under 0.2 MB if trimmed to id/time/mag/depth/alert/tsunami). — [c01 script](scripts/prompt_c/c01_catalog_match_rates.py)

**Real match rates, 2024 M≥5 catalog (N = 1,504, GeoJSON) — [results_c01](scripts/prompt_c/results_c01_match_rates.txt)**

| Condition | M | M/N | 1 in … |
|---|---|---|---|
| shallow (<70 km) & M≥7.0 | 8 | 0.53% | 188 |
| M≥7.0 (any depth) | 10 | 0.66% | 150 |
| shallow & M≥6.5 | 18 | 1.20% | 84 |
| **shallow & M≥6.0 (recommended default)** | **72** | **4.79%** | **21** |
| shallow & M≥7.5 ("tsunamigenic-class") | 1 (Noto, Japan) | 0.07% | 1,504 |
| USGS `tsunami` flag = 1 | 62 | 4.12% | 24 |
| tsunami flag & shallow & M≥6.5 | 15 | 1.00% | 100 |
| PAGER alert yellow / orange / red | 18 / 0 / 2 | 1.33% (≥ yellow) | 75 |
| DYFI felt reports ≥ 1,000 | 9 | 0.60% | 167 |
| `sig` ≥ 600 | 84 | 5.59% | 18 |
| deep (≥300 km) | 60 | 3.99% | 25 |

- Product availability on the same 1,504 events: moment-tensor 48.9%, shakemap 37.2%, losspager 35.4%, DYFI 40.0%, ground-failure 8.2%, finite-fault 0.7% (10 events). — [results_c01](scripts/prompt_c/results_c01_match_rates.txt)
- The 2024 M≥7 list includes a **639.5 km-deep M7.1** (Philippines) and a **127 km-deep M7.4** (Chile) with `tsunami=1`. Both PAGER-red events (Noto M7.5; Aykol, China M7.0) are shallow. — [results_c01](scripts/prompt_c/results_c01_match_rates.txt)
- Random contiguous windows of the time-ordered catalog under shallow & M≥6.0 (5,000 windows per size) — [results_c02](scripts/prompt_c/results_c02_exact_grover.txt):

  | N | mean M | P(M=0) | P(M=1) | P(M≥2) |
  |---|---|---|---|---|
  | 8 | 0.37 | 0.672 | 0.286 | 0.042 |
  | 16 | 0.75 | 0.415 | 0.430 | 0.155 |
  | 32 | 1.52 | 0.088 | 0.445 | 0.467 |
  | 64 | 3.07 | 0.002 | 0.051 | 0.947 |

- **Bit encoding for an honest oracle:** magnitude code = ⌊(mag−5.0)·10⌋ in 5 bits (range 5.0–8.1; observed 0..25, none clipped); depth code = ⌊depth/10 km⌋ in 4 bits (0–150 km, capped). The test "code_mag ≥ 10 AND code_depth < 7" disagrees with the float predicate on **0 of 1,504** events. — [results_c02](scripts/prompt_c/results_c02_exact_grover.txt)

**Server-side filtering is the realistic classical baseline (my tests)**
- FDSN `count` round trips from my machine: `minmagnitude=6&maxdepth=70` returned **72** in 669 ms; `minmagnitude=7&maxdepth=70` returned **8** in 863 ms; `alertlevel=yellow` returned 18 in 854 ms. — [results_c08](scripts/prompt_c/results_c08_classical.txt)
- A count over the whole ComCat (1900–2026, all magnitudes) returned HTTP 503 (too large for one request). — [results_c08](scripts/prompt_c/results_c08_classical.txt)

**What a genuinely expensive per-event check costs**
- **W-phase moment-tensor inversion.**
  - At USGS, PTWC and IPGS it delivers solutions "within 30–60 min after the origin time" for moderate and large earthquakes. — [AGU FM15 abstract](https://agu.confex.com/agu/fm15/webprogram/Paper77162.html)
  - For Tohoku 2011, useful tsunami-warning results came about 20 min after origin. — [Duputel et al., EPS 2011](https://earth-planets-space.springeropen.com/articles/10.5047/eps.2011.05.032)
  - PTWC issues its W-phase solution internally within 30 min. — [W phase method page](https://wphase.unistra.fr/method.html)
  - This latency is mostly *waiting for long-period data*, not CPU (see Inferences).
- **Tsunami propagation (Tsunami-HySEA, GPU).** It computes "in several minutes" the maximum amplitude and arrival time at about 17,000 Mediterranean coastal points. Single-scenario times have fallen "to a few minutes or even seconds" depending on hardware. These are self-reported by the developers. — [HySEA, RIUMA](https://riuma.uma.es/entities/publication/0073a3e0-2ceb-4ef0-ab32-7b7be570e73f); [EGU24-8319](https://meetingorganizer.copernicus.org/EGU24/EGU24-8319.html)
- **Physics-based hazard (SCEC CyberShake).**
  - The planning estimate is about 181,000 core-hours per site at 0.5 Hz, with about 550,000 rupture variations per site.
  - Study 14.2 used 520,535 node-hours (~15.8M core-hours) for 286 sites, i.e. about 55,000 core-hours per site.
  - — [CyberShake Computational Estimates](https://strike.scec.org/scecpedia/CyberShake_Computational_Estimates); [CyberShake Study 14.2](https://strike.scec.org/scecpedia/CyberShake_Study_14.2)

### Inferences
- **Recommended condition.**
  - Use "shallow (<70 km) & M≥6.0" as the in-demo default. It is seismologically meaningful: shallow, strong events dominate damage and tsunami potential, and the 70 km cutoff is the conventional shallow/intermediate boundary. At N = 32–64 it gives M ≈ 1.5–3, which keeps k_opt = 3–4.
  - Offer a "rarer" toggle (shallow & M≥7.0, or PAGER ≥ yellow) for the needle regime.
  - Do **not** call the USGS `tsunami` flag "tsunamigenic potential". The flagged 639 km-deep event shows it behaves like a "large and oceanic" flag rather than physical potential. If you want a tsunamigenic proxy, define it explicitly as shallow & M≥7.5 (only 1 event in 2024) or shallow & M≥7 & `tsunami=1`.
- **Ship the data as a file.** A slimmed 2024 M≥5 snapshot (0.46 MB, well under the 2 MB limit) is safer than a live fetch. Keep the live FDSN fetch as an optional "refresh" button. Note the endtime off-by-one.
- **Make the expensive check real without lying.** The condition a seismologist screens on (magnitude/depth/alert) is a cheap column filter. The expensive thing is the model you run *after* screening.
  - W-phase latency is set by wave arrival and data availability. The inversion itself is a small least-squares problem, so it is not a compute-bound "expensive check" in the Grover sense.
  - A Grover-relevant expensive predicate would be something like "events whose tsunami simulation exceeds 1 m at a given coast" or "rupture scenarios whose CyberShake PGV exceeds a threshold at a site". The oracle would then have to run that simulation reversibly in superposition (cost: see Q2).
- **A real "seismologist with an expensive check" setting is a stochastic event set, not a catalog.** Hazard models such as CyberShake enumerate about 550k rupture variations per site, so the items are generated from compact parameters (a "virtual database"). That is the only setting where the black-box model is even arguable (Q2).

### Gaps
- I could not retrieve USGS's official definitions of the `tsunami`, `alert` and `sig` fields this session. The event-terms page renders client-side and WebFetch/curl returned only the schema. The "large and oceanic" reading of `tsunami=1` is inferred from the data, not quoted.
- I found no authoritative wall-clock compute figure for PAGER or ShakeMap per event, nor for a single W-phase inversion's CPU time.
- I did not test the fetch inside Qollab's own iframe. The test used `Origin: null` headers via curl and relies on prior notes' sandboxed-iframe test for GeoJSON.

## 2. The honest oracle problem: why the list oracle is circular, honest alternatives and their costs, the black-box and QRAM models, and where a fault-tolerant crossover would sit

### Takeaway
A phase oracle built from the list of matching indices encodes the answer: whoever built it already evaluated the predicate on all N events. Grover's "√N oracle calls" therefore measures nothing about search.

The honest alternative (QROM loads each event's raw depth/magnitude bits, then a reversible comparator evaluates the condition in superposition) works. I verified that it marks exactly the same events. But it costs ≈ b·N two-qubit gates **per oracle call** (b = data bits per event), so total Grover cost is Θ(N^1.5) gates, against N cheap comparisons classically.

Even fault-tolerantly with the best table lookup (QROAM, ~2√(Nb) Toffolis per call), the total is Θ(N) and about 10⁶× slower than a classical scan, with no crossover. A crossover exists only in the expensive-black-box regime. Even there it needs N* ≈ 6.6×10¹¹ items at Babbush et al.'s 170 µs Toffoli, against 155,899 earthquakes in all of 2024.

### Cited Findings
**Tutorial oracle**
- IBM's tutorial `grover_oracle()` takes "a bitstring or list of equal-length bitstrings". For each target it applies X gates on '0' positions, then `MCMTGate(ZGate(), n-1, 1)`, then undoes the X gates. Optimal iterations are `floor(pi / (4*asin(sqrt(len(marked_states)/2**n))))`. The example uses 3 qubits with marked states ["011","100"]. — [IBM Grover tutorial](https://quantum.cloud.ibm.com/docs/en/tutorials/grovers-algorithm)

**My experiments**
- **The honest oracle is correct.** For one real slice per n = 3..6, Grover with the honest QROM+comparator oracle gives the same P(success) at k_opt as the list oracle: 0.945312 / 0.945313 / 0.961319 / 0.998139. Probability mass left in dirty ancillas is 0. The circuits use 18 / 19 / 20 / 21 qubits. — [results_c02](scripts/prompt_c/results_c02_exact_grover.txt)
- **Per-oracle-call 2Q gate counts** after transpiling to an all-to-all {rz, rx, rzz} basis (IonQ-like) and to a 115-qubit heavy-hex `GenericBackendV2` {cz, rz, sx, x} (IBM-like), opt level 3 — [results_c03](scripts/prompt_c/results_c03_gate_counts.txt):

  | n (N) | M | list oracle (needs answer) IonQ / heavy-hex | honest QROM-ucry + comparators IonQ / HH | honest QROM-select IonQ / HH | diffusion IonQ / HH |
  |---|---|---|---|---|---|
  | 3 (8) | 1 | 5 / 7 | 221 / 604 | 491 / 1,279 | 5 / 7 |
  | 4 (16) | 2 | 26 / 35 | 409 / 1,146 | 1,657 / 3,836 | 13 / 18 |
  | 5 (32) | 2 | 54 / 128 | 613 / 1,659 | 4,180 / 9,862 | 27 / 65 |
  | 6 (64) | 3 | 217 / 471 | 1,109 / 2,828 | 10,430 / 23,866 | 73 / 160 |

- **QROM load cost scales as b·N.** A multiplexed-RY QROM load alone needs 2Q = 0.83–1.00 × b·N for n = 3..8 and b = 1..16 (e.g. n=8, b=16: 4,070 vs b·N = 4,096). One oracle call is load + unload ≈ 2bN. — [results_c03b](scripts/prompt_c/results_c03b_qrom_scaling.txt)
- **Full Grover circuit at k_opt.** List oracle: 20 / 78 / 243 / 870 IonQ-like 2Q for n = 3..6. Honest oracle: 452 / 844 / 1,911 / 3,423 IonQ-like 2Q, and 1,220 / 2,343 / 5,337 / 9,321 on heavy-hex. — [results_c03](scripts/prompt_c/results_c03_gate_counts.txt)
- **IonQ billing rule.** An n-qubit multi-controlled gate is billed as 6(n−2) 2Q gates. Under that rule a 6-qubit MCZ costs 24, while Qiskit's ancilla-free synthesis to rzz produces 73. The billed list-Grover at n=6 is 288 2Q against 870 transpiled. — [results_c03](scripts/prompt_c/results_c03_gate_counts.txt); [results_c05](scripts/prompt_c/results_c05_bbht.txt)

**Literature on loading costs, QRAM and practicality**
- **Unary iteration / QROM (Babbush et al. 2018).**
  - "Our unary iteration has a T-count of 4L-4" with "only log L ancillae".
  - "Our implementation of QROM consumes only 4L T gates and log L ancillae". Data are encoded by "the presence or absence of CNOTs on the data lines", so the T cost "is independent of the number of bits used to store each element".
  - — [Babbush et al., PRX 8, 041015 (2018), arXiv:1805.03662](https://ar5iv.labs.arxiv.org/html/1805.03662)
- **Select-swap trade-off (Low, Kliuchnikov, Schaeffer).** The T-gate cost can be reduced "to O(N/λ + λ log(N/ε) log(log N/ε))" with λ dirty qubits, and the trade-off is "optimal up to logarithmic factors". It is built on "a T-efficient circuit implementation of a quantum oracle for arbitrary classical data". — [arXiv:1812.00954](https://arxiv.org/abs/1812.00954)
- **Babbush et al. 2021, "Focus beyond quadratic speedups".**
  - Surface-code cycle about 1 µs, physical error about 10⁻³, distance about 30, Toffoli time t ≈ 30 × 5.5 × 1 µs ≈ **170 µs**, using "around 130,000 physical qubits".
  - Ion traps at about 10 kHz cycles give about **17 ms** per Toffoli.
  - For search, "one must perform a reflection that requires O(N) Toffoli gates".
  - Breakeven for quadratic speedups: 2.4 hours (lower-bound primitive, one core) up to 880 millennia (simulated annealing, 10⁶-way classical parallelism).
  - Even a 100× faster Toffoli leaves breakeven at 15 min to 32 days with 10³-way parallelism.
  - Conclusion: "quadratic speedups will not enable quantum advantage on early generations of such fault-tolerant devices".
  - — [arXiv:2011.04149](https://arxiv.org/abs/2011.04149); [ar5iv full text](https://ar5iv.labs.arxiv.org/html/2011.04149)
- **Jaques & Rattew, Quantum 9, 1922 (2025).**
  - Active QRAM has an opportunity cost: "one could repurpose the control hardware for the qubits in the QRAM" to run a parallel classical algorithm.
  - "most asymptotic quantum advantage disappears with active QRAM systems".
  - "cheap, asymptotically scalable passive QRAM is unlikely with existing proposals".
  - "circuit-based QRAM still helps in many applications".
  - — [arXiv:2305.10310](https://arxiv.org/abs/2305.10310)
- **Aaronson, "Read the fine print", Nat. Phys. 11, 291 (2015).**
  - Caveat (1): the input "somehow needs to be loaded quickly into the quantum computer's memory", possibly via a "quantum RAM".
  - "if preparing |b⟩ already takes n^c steps … the exponential speedup of HHL vanishes in the very first step".
  - These algorithms all face "how to load a large amount of classical data into a quantum computer (or else compute the data 'on-the-fly')".
  - — [qml.pdf](https://www.scottaaronson.com/papers/qml.pdf)
- **Viamontes, Markov & Hayes, "Is quantum search practical?" (CiSE 2005).**
  - Three requirements for useful Grover: a search application where classical methods scale poorly; a Grover implementation that is asymptotically faster than any classical algorithm; and a practical actual runtime.
  - Real-life database applications rarely satisfy the first.
  - Classical simulation of quantum search can be competitive with Grover's algorithm on useful instances.
  - (Summarised from search results; I did not read the full text.) — [arXiv:quant-ph/0405001](https://arxiv.org/abs/quant-ph/0405001)
- Broda (2015) builds a Grover oracle for a "real unstructured classical database" that "contains a kind of quantumly accessible classical memory". — [arXiv:1502.04943](https://arxiv.org/abs/1502.04943)

**My fault-tolerant crossover model** — [c09 script](scripts/prompt_c/c09_ft_crossover.py) / [results_c09](scripts/prompt_c/results_c09_ft_crossover.txt)
- **Cheap check, data in RAM.** The classical filter costs ~3 ns/row (measured in c08). At a 170 µs Toffoli, quantum takes 1.1×10⁶–5.6×10⁹ times longer than a random-order scan, for N from 64 to 10⁹. With QROAM lookup the ratio is about 1.07×10⁶ at every N, because both are Θ(N). Against an index the gap grows without bound.
- **Expensive black-box check of W operations** (optimistic: 1 logical Toffoli per classical op; classical op 0.33 ns; M=1; one classical core).
  - Crossover at √N* = (π/2)·t_Toff/t_op.
  - N* = **6.6×10¹¹** items at 170 µs, **6.6×10¹⁵** at 17 ms (ion trap), and **6.6×10⁷** at a hypothetical 1.7 µs.
  - At N*, the classical run already costs 1.0×10⁴ core-years (1 CPU-second check, 170 µs Toffoli) up to 2×10¹² core-years (one CyberShake-site check).
- **Honest Grover over the 2024 M≥5 catalog** (N = 1,504, M = 1): 30 iterations × 523 Toffoli/iteration (QROAM) ≈ 1.6×10⁴ Toffolis ≈ **2.7 s** at 170 µs. A classical scan takes about 752 checks × 3 ns ≈ **2.3 µs**.

### Inferences
- **Why the list oracle is circular.** Let f(i) = [depth_i < 70 ∧ mag_i ≥ 6]. The list oracle O = I − 2Σ_{i∈S}|i⟩⟨i| takes S = f⁻¹(1) as its input. Computing S requires evaluating f on all N events: N predicate evaluations, or one indexed query. That is strictly more than the classical search problem asks, since it yields every match rather than one.
  - Given S, any element of S can be output with zero queries.
  - So "(π/4)√(N/M) oracle calls vs N/2 checks" compares a lookup into the answer list with a search. It measures Grover's rotation geometry, not search.
  - The same holds for any oracle compiled from a truth table (e.g. `DiagonalGate` with ±1 entries). The compiler must read all N values.
- **Counting argument.** A generic N-entry ±1 diagonal on n = log₂N qubits needs Ω(N/log N) gates from any finite gate set. There are 2^N such diagonals, while circuits of G gates number at most (poly(n))^G. So the per-call cost of an honest oracle for an unstructured explicit database is at least about N/log N gates. Total Grover gate cost is then Ω(N^1.5/log N), more than the N classical comparisons.
  - My QROM measurement (≈ b·N 2Q gates per load) is this bound made concrete.
  - This is my derivation, in the spirit of Babbush et al.'s "reflection requires O(N) Toffoli gates".
- **What the honest oracle buys.** The circuit compiler reads raw fields and never evaluates the predicate, and the thresholds are circuit parameters. That makes "the oracle recognises, it doesn't know" literally true. It is the right teaching and accounting artifact, but it is not a speedup.
- **When the expensive black-box model is legitimate.** All four conditions must hold:
  1. Items are *implicit*, generated from a compact index (a "virtual database" or search space such as rupture-parameter grids or SAT assignments), so no O(N) load is needed.
  2. The check is a uniform, polynomial-size reversible computation.
  3. The check dominates every other per-call cost.
  4. There is no exploitable structure (index, sort order, monotonicity, pruning).

  A catalog search fails all four: explicit data, a 2-column range predicate perfect for a B-tree, a ns-scale check, and the server already filters.
- **QRAM.**
  - Assuming O(log N)-time QRAM makes the √N story true on paper.
  - Jaques & Rattew show active QRAM's control hardware could run a parallel classical scan at least as fast.
  - Passive QRAM rests on dubious physics.
  - Aaronson's fine print says the loading cost must be counted.
  - So a judge-proof project states the QRAM assumption explicitly and also shows the circuit-QROM cost.
- **Crossover.** For catalog-style search there is none; quantum time scales at least as classical scan time times 10⁵–10⁹. For expensive implicit checks, N* ≈ ((π/2)·t_Toff/t_op)² is independent of how expensive the check is, and with P classical cores it grows by about P². Real earthquake catalogs (~1.6×10⁵ events/year, all magnitudes) are 6–10 orders of magnitude below N*.

### Gaps
- I did not verify the exact clean-ancilla QROAM Toffoli formula (⌈N/λ⌉ + b(λ−1), usually attributed to Berry et al. 2019). The c09 model uses the balanced form 2√(Nb), labelled as an inference from Low et al.'s O(N/λ + λ·…) trade-off.
- The counting-argument lower bound is my own sketch, not taken from a cited source.
- I did not read the full Viamontes et al. paper.

## 3. Experiments at n = 3–6 (8–64 events) on real catalog slices

### Takeaway
On real 2024 slices, exact-M Grover reproduces sin²((2k+1)θ) exactly and overshoots hard. At N=64 with M=3, P goes 0.998 at k=3, then 0.090 at k=6, then 0.017 at k=7.

With M unknown, BBHT finds a verified match in **7.10 [6.94, 7.26]** predicate evaluations at N=64, against **16.38 [15.93, 16.86]** for a random-order scan (95% bootstrap CIs, 3,000 real windows). That is a real 2.3× query gap. An indexed classical lookup needs about 10 rows and is O(log N + K).

At IonQ forte-1 noise rates with Qiskit's MCZ synthesis, the noise-aware Grover still beats classical checks at n ≤ 6 in the single-match (needle) case: 26.1 vs 32.5 expected evaluations at N=64.
- It **loses at n = 7** (67.2 vs 64.5).
- P(success) at k_opt is statistically indistinguishable from random guessing by **n = 8** (0.004 vs M/N = 0.0039).
- At the real catalog rate (M grows with N), it loses from n = 6, and the best noise-aware choice for n ≥ 7 is k = 0, i.e. random sampling.

### Cited Findings
**Exact-M Grover and overshoot** (statevector, list oracle; matches theory to 1e-9) — [results_c02](scripts/prompt_c/results_c02_exact_grover.txt); figure [fig_c02_overshoot.png](scripts/prompt_c/fig_c02_overshoot.png)

| n, N, M (real slice) | matches | P(k=0..9) |
|---|---|---|
| 3, 8, 1 | M6.2 16 km Tamarindo, Costa Rica | .125 .781 **.945** .330 .012 .548 1.000 .577 |
| 4, 16, 2 | M7.0 13 km Aykol, China; M6.3 31 km Port-Vila | .125 .781 **.945** .330 .012 .548 1.000 .577 |
| 5, 32, 2 | M6.5 Kimbe PNG; M6.3 Uwajima JP | .062 .473 .908 **.961** .582 .125 .020 .365 .836 .992 |
| 6, 64, 3 | M6.4 Tobelo ID; M6.5 Kimbe; M6.3 Uwajima | .047 .371 .787 **.998** .853 .456 .090 .017 .290 .712 |

**Classical baselines** — [results_c08](scripts/prompt_c/results_c08_classical.txt)
- **Random-order scan.** Exact E = (N+1)/(M+1) and Var = (N+1)(N−M)M/((M+1)²(M+2)), checked by 20,000-permutation simulation. N=64, M=1: E 32.5, SD 18.5. N=1,504, M=72: E 20.6, SD 19.8. N=1,504, M=8: E 167.2, SD 149.1.
- **numpy filter.** 8.4 µs on the real 1,504 rows (5.6 ns/row). 2.7 ms at 10⁶ rows; 37.8 ms at 10⁷ rows (~3 ns/row).
- **sqlite at 10⁶ rows.** `mag>=7 AND depth<70`: 487 ms without an index, 56 ms with a B-tree on mag (plan: `SEARCH ev USING INDEX ix_mag (mag>?)`).
- **FDSN server-side filter.** About 0.7–0.9 s round trip; returns the exact count.

**Unknown M: BBHT vs classical over 3,000 random real windows per n** (bootstrap 95% CI)
- Cost counts every oracle call plus every classical verification of a measured candidate.
- BBHT stop budget calibrated so that P(miss | M=1) ≤ 5%: c·√N with c = 1.25 / 1.25 / 1.75 / 1.75 for n = 3..6.
- Noisy BBHT uses the global-depolarizing model at forte-1 rates with Qiskit-synthesis MCZ costs.
- — [results_c05](scripts/prompt_c/results_c05_bbht.txt)

| n (N) | P(M=0) | BBHT ideal (M≥1) | BBHT noisy (M≥1) | random scan (M≥1) | indexed rows (M≥1) | M=0: BBHT / scan / index | correct rate ideal / noisy |
|---|---|---|---|---|---|---|---|
| 3 (8) | 0.669 | 3.63 [3.51, 3.74] | 3.71 | 4.40 [4.26, 4.55] | 4.27 | 8.51 / 8 / 3.15 | 0.997 / 0.992 |
| 4 (16) | 0.419 | 5.09 [4.96, 5.23] | 5.56 | 7.68 [7.48, 7.89] | 5.53 | 11.83 / 16 / 4.30 | 0.987 / 0.973 |
| 5 (32) | 0.092 | 6.93 [6.77, 7.08] | 8.58 | 13.54 [13.20, 13.86] | 7.21 | 17.12 / 32 / 6.01 | 0.987 / 0.895 |
| 6 (64) | 0.003 | 7.10 [6.94, 7.26] | 14.66 [14.36, 14.98] | 16.38 [15.93, 16.86] | 10.22 | 22.8 / 64 / 8.0 | 0.997 / 0.599 |

- BBHT beats the scan on 52.8% / 62.9% / 70.2% / 70.5% of individual M≥1 slices (n = 3..6). — [results_c05](scripts/prompt_c/results_c05_bbht.txt)
- **Needle scaling (M=1, 4,000 runs).** BBHT ideal costs 1.39–1.65·√N total evaluations for n = 3..10, e.g. 51.6 at N=1,024 against 512.5 for the scan. Noisy BBHT degrades past n=6: 58.9 at N=64, 302.9 at N=128, 1,595.8 at N=1,024. — [results_c05](scripts/prompt_c/results_c05_bbht.txt)

**Noise at IonQ forte-1 rates** (1q 2.67e-4 depolarizing on rx, 2q 4.95e-3 on rzz, rz virtual, no readout error). Exact density-matrix probabilities; the global-depolarizing analytic model agrees within 0.001–0.04. — [results_c04](scripts/prompt_c/results_c04_noise.txt); [fig_c04_noise.png](scripts/prompt_c/fig_c04_noise.png)

| n (N), M=1 | k_opt | 2Q at k_opt | P ideal | P noisy | random guess M/N | classical with k_opt+1 checks | noise-aware k* | E[evals] noisy at k* | classical (N+1)/2 |
|---|---|---|---|---|---|---|---|---|---|
| 3 (8) | 2 | 20 | 0.945 | 0.869 | 0.125 | 0.375 | 1 | 2.7 | 4.5 |
| 4 (16) | 3 | 78 | 0.961 | 0.696 | 0.0625 | 0.250 | 2 | 4.1 | 8.5 |
| 5 (32) | 4 | 216 | 0.999 | 0.407 | 0.031 | 0.156 | 2 | 7.9 | 16.5 |
| 6 (64) | 6 | 876 | 0.997 | 0.042 | 0.016 | 0.109 | 1 | 26.1 | 32.5 |
| 7 (128) | 8 | 1,808 | 0.996 | **0.009** | **0.0078** | 0.070 | 1 | **67.2** | **64.5** |
| 8 (256) | 12 | 3,960 | 1.000 | 0.004 | 0.0039 | 0.051 | 1 | 184.9 | 128.5 |
| 9 (512) (analytic) | 17 | 7,854 | 0.999 | 0.002 | 0.0020 | 0.035 | 0 | 512.0 | 256.5 |

- n = 3..6 use shallow & M≥6.0; n ≥ 7 use shallow & M≥7.0. In both cases a real window with exactly one match was chosen. — [results_c04](scripts/prompt_c/results_c04_noise.txt)
- **Real-rate regime** (random real windows, shallow & M≥6.0, so M grows with N and k_opt ≈ 3). The list oracle needs M MCZs per call, so its cost grows with M (1,086 2Q at n=6 with M=4; 46,665 at n=10 with M=50).
  - Noisy P at k_opt: 0.075 / 0.055 / 0.059 / 0.051 / 0.049 for n = 6..10, against random-guess M/N of 0.0625 / 0.0547 / 0.0586 / 0.0508 / 0.0488.
  - Noise-aware Grover **loses already at n=6** (14.1 vs 13.0 expected evaluations).
  - For n ≥ 7 the best noise-aware choice is k = 0, i.e. random sampling (n=10: 20.5 vs 20.1).
  - n = 6–7 are density-matrix runs; n ≥ 8 use the analytic model.
  - — [results_c04](scripts/prompt_c/results_c04_noise.txt)

- **Honest QROM+comparator oracle under the same noise** (n=3, 18 qubits, Aer statevector trajectories, 2,000 shots):
  - k=0: P = 0.117 ± 0.007 (ideal 0.125).
  - k=1 (226 2Q): **P = 0.417 ± 0.011** against 0.250 for classical with 2 checks (ideal 0.781; analytic model 0.354).
  - k=2 (452 2Q): P = 0.318 ± 0.010, now *below* classical with 3 checks (0.375); ideal 0.945.
  - Expected cost with restarts at the best k=1 is 2/0.417 ≈ 4.8 evaluations, against 4.5 for a random scan. So the honest oracle wins at a fixed small budget but not in expected cost, even at N = 8.
  - The analytic model is pessimistic here by 0.06–0.09.
  — [results_c04b](scripts/prompt_c/results_c04b_honest_noisy.txt)
- **Bracketing IonQ's compiler** (global-depolarizing model, M=1). With the billed 6(n−2) 2Q per MCZ instead of Qiskit's synthesis (n=6: 24 vs 73):
  - P(k_opt) at n=6 is 0.273, against 0.032 with Qiskit synthesis (classical with the same budget: 0.109).
  - Noise-aware Grover then stays ahead of the scan through n=12. The optimal k saturates at 2–3, so the advantage shrinks to a constant factor: E = 1,389.5 vs 2,048.5 at N=4,096.
  - With Qiskit synthesis, Grover loses from n=7.
  - — [results_c11](scripts/prompt_c/results_c11_billed_noise_horizon.txt)

**Counting M** (MLAE with schedule m = 0, 1, 2, 4 and equal shots; QPE counting) — [results_c06](scripts/prompt_c/results_c06_counting.txt)
- **Small budgets on real slices.** MLAE suffers likelihood multimodality.
  - At N=16, M=1, budget 22 evaluations: RMSE(M̂) = 3.1 for ideal MLAE, against 0.85 for classical random sampling. An exact classical count costs only 16 checks.
  - At N=64, M=3, budget 22: RMSE 11.4 (MLAE) vs 2.7 (sampling).
- **At budget 176** (16 shots per circuit), ideal MLAE beats sampling: RMSE 0.09–0.14 vs 0.28–0.42 at N = 16–32. But that budget is already larger than N, so an exact count is cheaper.
- **Under forte-1 noise, naive MLAE is badly biased** (RMSE 2.1–4.2 at budget 176). A noise-aware likelihood that fits the decay γ jointly restores RMSE to 0.31–1.17.
  - At N=64, M=5, budget 176: ideal MLAE 1.02, noisy-naive 9.15, noisy-aware 2.97, classical sampling 1.20 (exact count costs 64).
- **Asymptotic ideal sweep** (schedule 0, 1, 2, 4, …, 2^K at 32 shots each; budget counts oracle calls plus labels).
  - At the real 4.8% rate, MLAE reaches relative RMSE 0.081 with a budget of 352. Classical sampling needs about 3,000 for the same error.
  - At budget 16,672, MLAE reaches 0.002 relative RMSE; sampling would need about 3.8 M.
  - At the 0.53% rate, MLAE is at 0.010 with budget 4,320 against about 1.7 M for sampling. Above max m = 64 it plateaus at about 0.011, a likely grid/aliasing limit of my MLE.
  - The Heisenberg-vs-shot-noise gap is real, but only matters when the catalog is much larger than the budget, and only noiselessly.
- **QPE quantum counting** (n=4 + t counting qubits, list oracle, real slice with M=1; corrected decode in c06b).
  - t=4 (8 qubits, 15 controlled-G, 2,346 2Q): P(|M̂−M| ≤ 0.5) = 0.772 ideal, **0.188** under forte-1 (mean M̂ 6.23 vs true 1).
  - t=5 (9 qubits, 4,846 2Q): 0.827 ideal, 0.178 noisy.
  - — [results_c06b](scripts/prompt_c/results_c06b_qpe_counting.txt)
- The QPE lines in `results_c06_counting.txt` came from a version whose diffusion I − 2|s⟩⟨s| made controlled-G eigenphases π ± 2θ, so the estimates read as N − M. The global-phase fix is now in both scripts.

**Fixed-point amplitude amplification (Yoder–Low–Chuang)**
- The phase implementation matches the closed form P_L = 1 − δ²T_L(T_{1/L}(1/δ)√(1−λ))² to 1e-9. A Qiskit circuit (MCPhase-based) reproduces it exactly at n=4.
- Design used: w = 1/N (at least one match), δ = 0.5. — [results_c07](scripts/prompt_c/results_c07_fixed_point.txt)

| n (N) | FPAA iterations l | Grover k (tuned for M=1) | real slices M≥1: mean P FPAA (min) | mean P Grover (min) | mean expected evals with restarts FPAA / Grover |
|---|---|---|---|---|---|
| 4 (16) | 3 | 3 | 0.951 (0.769) | 0.785 (0.000) | 4.2 / 1,846 |
| 5 (32) | 4 | 4 | 0.924 (0.756) | 0.720 (0.012) | 5.4 / 16.6 |
| 6 (64) | 6 | 6 | 0.844 (0.754) | 0.224 (0.020) | 8.4 / 134.0 |

- FPAA costs about 31% more 2Q than plain Grover at equal iterations (n=4, l=3: 102 vs 78 IonQ-like 2Q for M=1; 204 vs 156 for M=3), because MCPhase replaces MCZ. — [results_c07](scripts/prompt_c/results_c07_fixed_point.txt)

**One-job packaging and judge-run timing** — [results_c10](scripts/prompt_c/results_c10_one_job.txt)
- **List-of-circuits job.** 21 circuits at n=5 (Grover sweep k=0..8 plus 12 pre-drawn BBHT rounds): 4,131 IonQ-like 2Q in total. `StatevectorSampler` ran 256 shots of all 21 in 0.81 s; `BasicSimulator` took 11.3 s (local CPython on a loaded machine).
- **Packed registers.** 4 independent n=6 Grover circuits (k=0..3) on 24 qubits in one circuit decode to P = 0.031 / 0.260 / 0.607 / 0.891, against theory 0.031 / 0.258 / 0.602 / 0.897.
- **Honest oracle in pure-numpy `qiskit.quantum_info.Statevector`.** 45 s for n=3 (18 qubits, 1,133 u/cx gates); **420 s** for n=4 (19 qubits).

### Inferences
- **Where the query gap is real, and how big it is.** The quantum effect in the black-box metric is genuine but small at these sizes: a 1.2× (N=8) to 2.3× (N=64) reduction in expected predicate evaluations. Its 95% CIs do not overlap the scan's. It is the measurable difference to report, with the honest caveat that each "evaluation" on the quantum side is a ~10²–10³-gate circuit (Q2).
- **The realistic baseline.** The indexed/sorted baseline (B-tree on magnitude) touches about log₂N + K_mag rows. It roughly ties BBHT at N ≤ 32 and needs no quantum resources. At N=1,504 it would touch about 11 + 99 rows and return *all* matches. Present it as the realistic seismologist baseline; linear scan is the textbook baseline.
- **"Below random guessing".** Under depolarizing noise P(success) decays toward M/N from above and never meaningfully below it. At n = 8 it equals M/N to three decimals (0.004 vs 0.0039), so n = 8 is where Grover becomes *indistinguishable* from random guessing.
  - The decision-relevant threshold is "loses to classical with the same budget". With Qiskit-synthesized MCZs that happens at **n = 6** for P at k_opt (0.042 < 0.109) and at **n = 7** for the best noise-aware k (67.2 > 64.5).
  - If IonQ's compiler achieves its billed 6(n−2), the horizon moves out, but the advantage becomes a constant factor because k* saturates at 2–3.
  - At the real catalog rate, the list oracle's cost grows with M, so it loses from n = 6.
- **The real catalog rate caps the interesting regime.** At the real rate of ~4.8%, k_opt ≈ (π/4)/√0.048 ≈ 3.6 for *every* N, and the classical expectation is ≈ 1/0.048 ≈ 21 checks for every N. The "√N vs N" gap only appears if the condition gets rarer as the slice grows (the needle regime). For "find *all* matches", classical needs N checks and quantum about √(N·M) calls, plus about √N to certify that none remain.
- **Counting at N ≤ 64.** Quantum counting cannot beat an exact classical count (N checks). MLAE needs a noise-aware likelihood to be unbiased on forte-1. That makes it a technical-depth extension, not an impact claim.
- **FPAA vs BBHT.** FPAA is the most robust unknown-M method under the one-job rule: a single fixed-depth circuit with no adaptivity and P ≥ 0.75 for every M ≥ 1. BBHT has lower expected cost (7.1 vs 8.4 at N=64) but is adaptive. It can be made non-adaptive by resampling shots from a pre-run Grover sweep (Q6).
- **Simulation bottleneck.** The honest oracle cannot be simulated live in Pyodide at 18+ qubits with pure-numpy statevectors (45–420 s locally). The live demo must use either the verified diagonal equivalent or a basis-state (sparse) simulation of the reversible oracle, and must say that this simulation itself evaluated the predicate on all N events (Viamontes et al.'s point).

### Gaps
- I did not run IonQ's actual cloud `forte-1` noise model; all noise numbers are Aer depolarizing at the given rates. I did not model readout/SPAM error.
- I did not test whether IonQ's compiler actually reaches 6(n−2) 2Q gates per MCZ with that error budget.
- The density-matrix sweep stops at n=8 (needle) and n=7 (real rate). Larger n uses the analytic model, which runs 0.001–0.04 pessimistic relative to the density matrix at n ≤ 7.
- Timings come from CPython on a shared machine. I did not measure Pyodide timings.

## 4. What exists: tutorials, Qiskit examples, Grover-on-earthquake projects, and what the plain version will look like

### Takeaway
The plain version is essentially IBM's tutorial with a CSV filter in front: pandas finds the matching rows, their indices become the marked bitstrings for `MCMTGate`, k = ⌊π/(4·asin√(M/N))⌋, and the output is a histogram plus maybe a P-vs-k plot. A peer-reviewed 2026 paper already did exactly this on 5,000 Indonesian USGS events and reported "3 iterations vs 5000". I found no project that uses an honest data-loading oracle, handles unknown M, or prices the oracle.

### Cited Findings
- **IBM tutorial.**
  - 3 qubits, marked ["011","100"], oracle from bitstrings via `MCMTGate(ZGate(), n-1, 1)`, `grover_operator(oracle)`, `StatevectorSampler` (10,000 shots) and then `SamplerV2` on a ≥127-qubit backend (est. "under one minute on an Eagle r3").
  - A scaling study (single marked state "1"*n) reports 2Q depth 39 / 111 / 466 / 1,646 / 3,550 / 7,989 / 14,824 for n = 3..9 at k_opt = 2 / 3 / 4 / 6 / 8 / 12 / 17, and concludes that depth "grows roughly exponentially".
  - — [IBM Grover tutorial](https://quantum.cloud.ibm.com/docs/en/tutorials/grovers-algorithm)
- **Mahardhika, Listiyanto, Yulianto & Aji (Universitas Negeri Semarang), published 2026-09-11, Vol. 10 No. 2, DOI 10.15294/pc.v10i2.59296.**
  - "Implementation of Grover's Search Algorithm for Tectonic Activity Detection in an Unsorted Seismic Database": 5,000 USGS events in Indonesia (2019–2024), magnitude/depth criteria, Python and Qiskit simulation.
  - "both Grover's algorithm and the classical search method successfully identified 353 target data points"; "Grover's algorithm required only 3 iterations, whereas the classical method required 5000 iterations".
  - The landing page doesn't describe how the oracle was built.
  - — [UNNES journal page](https://journal.unnes.ac.id/journals/pc/article/view/59296)
- **Figgatt et al. (Nature Comm. 8, 1918, 2017)**, trapped-ion 3-qubit Grover on IonQ's predecessor hardware. It ran all 8 single-solution and 28 two-solution oracles, compared phase-flip and Boolean (ancilla) oracles, and reported that all quantum solutions outperform their classical counterparts. — [arXiv:1703.10535](https://arxiv.org/pdf/1703.10535)
- A generic "Quantum-Database-Model" GitHub project (Grover over a CSV via Qiskit and an IBM token) turned up in search. I did not open the repo. — [search hit via ecosyste.ms](https://science.ecosyste.ms/projects/83480)
- Viamontes et al. separate real (explicit) databases from virtual (implicit) search spaces and argue real database search rarely satisfies their usefulness requirement. — [arXiv:quant-ph/0405001](https://arxiv.org/abs/quant-ph/0405001)
- Prior notes cover Grover as rotation, BBBV optimality, fixed-point AA (Yoder–Low–Chuang), MLAE (Suzuki et al.; noisy MLAE by Tanaka et al.), and quantum counting (Brassard–Høyer–Tapp). — [algorithms_and_complexity.md](../Quantum%20Unlocked%20theme%20deep%20dive/algorithms_and_complexity.md); [BBHT, arXiv:quant-ph/9605034](https://arxiv.org/abs/quant-ph/9605034); [YLC, arXiv:1409.3305](https://arxiv.org/abs/1409.3305); [MLAE, arXiv:1904.10246](https://arxiv.org/abs/1904.10246); [noisy MLAE, arXiv:2006.16223](https://arxiv.org/abs/2006.16223); [counting, arXiv:quant-ph/9805082](https://arxiv.org/abs/quant-ph/9805082)

### Inferences
- **Decoding the "3 vs 5000" claim.** With N = 5,000 and M = 353, (π/4)√(N/M) = (π/4)·3.76 ≈ 2.96, so their "3 iterations" is exactly k_opt. It finds *one* random match. The classical "5000 iterations" scans everything to find *all 353*.
  - The like-for-like classical figure for one match is (N+1)/(M+1) ≈ 14 checks, a 4.7× gap, not 1,667×.
  - Finding all 353 with Grover needs on the order of √(N·M) ≈ 1,300 oracle calls.
  - Each call needs an O(N)-gate oracle, and the oracle was presumably built from the 353 known indices.
  - This is my arithmetic. It is the cleanest "what the plain version gets wrong" exhibit, and it is real, recent and seismology-specific.
- **What most GT teams will build.** 8–64 events from the slide URL; pandas `df[(df.depth<70)&(df.mag>=6)]`; marked bitstrings; the IBM `grover_oracle`; one histogram; perhaps a P-vs-k overshoot plot (the prompt names "overshoot"); "√N vs N/2" in the README; possibly an IonQ simulator run. Under the rules this scores near zero on Novelty and Technical Execution.
- **Gap a team can own.** Honest oracle construction, unknown-M algorithms, noise-aware k, and a cost ledger. None appear in the tutorial or in the earthquake paper.

### Gaps
- I did not find Kaggle notebooks or GitHub repos specifically titled "Grover earthquake". The search surfaced only the UNNES paper and one generic database repo. Other teams' private work is unknowable.
- I could not read the UNNES paper's methods (oracle construction, qubit count).

## 5. Beyond-tutorial extensions inside Prompt C, and whether Prompt C can be a credible Impact entry

### Takeaway
Five extensions stay inside Prompt C and are each backed by an experiment above. The strongest pair is an **unknown-M search measured on real slices with CIs** (a real, positive query-count gap) combined with an **honest oracle-cost ledger** (gate counts, noise, fault-tolerant crossover) that converts the query gap into physical cost.

Candidly, Prompt C cannot honestly claim that a quantum subroutine makes a measurable *practical* difference to seismology. The classical baseline is an indexed query the USGS server already answers, and the crossover sits at N ≳ 10¹¹ even for expensive checks. A credible Impact entry must therefore be a rigorous decision instrument: "here is the measured gap, here is what it costs, here is when it would matter (never, for catalogs)". In spirit it fits Quantum Unlocked better.

### Cited Findings
All numbers below come from the experiments in Q2–Q3 (results files cited there). Build-hour and judge-time figures are my estimates.

| # | Extension | Tutorial bar it clears (one sentence) | Measurable difference (measured here) | Qubits / 2Q (IonQ-like) | Judge-run time (est.) | Build h | Hour-20 fallback |
|---|---|---|---|---|---|---|---|
| E1 | **Honest oracle ledger**: QROM + comparator oracle compiled from raw depth/mag bits, equivalence-checked, priced on IonQ and heavy-hex, under forte-1 noise and in fault-tolerant time | "The oracle is built from the data, not from the answer, and every gate is paid for." | Per call: 221–1,109 2Q (honest) vs 5–217 (list), n=3..6; load ≈ b·N. Full Grover 452–3,423 (IonQ) / 1,220–9,321 (heavy-hex). n=3 honest under noise: P = 0.417 ± 0.011 vs 0.250 classical at k=1, but expected cost 4.8 vs 4.5 (scan). Fault-tolerant: quantum/scan time ratio 10⁶–10⁹ (cheap check); N* = 6.6×10¹¹ (expensive check, 170 µs) | 18–21 qubits honest; ≤6 for live sim | Transpile and count: a few seconds; live sim via verified diagonal or sparse reversible sim < 1 s | 8–10 | Precomputed gate-count JSON plus the n=3 honest circuit only; fault-tolerant calculator in plain numpy |
| E2 | **Unknown-M search** (BBHT with calibrated stop rule, M=0 handled) on thousands of real windows, with bootstrap CIs vs scan and index | "We don't know how many events match, and we measure evaluations to a verified match with error bars." | N=64: 7.10 [6.94, 7.26] (ideal), 14.66 (noisy) vs scan 16.38 [15.93, 16.86] vs index 10.22; M=0 certification 22.8 vs 64 | ≤6 (list or diagonal oracle) | Sweep job (≈10 circuits × 256 shots) ≈ 1–5 s; resampling post-processing < 1 s | 6–8 | Ideal-only BBHT with cached noisy table |
| E3 | **Overshoot-free search** (Yoder–Low–Chuang fixed-point AA) | "We remove the soufflé problem with Chebyshev-designed phases instead of guessing k." | Real slices: mean P 0.84–0.95 vs 0.22–0.79 (Grover tuned for M=1); expected evals 8.4 vs 134 (N=64) | ≤6; about 1.3× Grover's 2Q per iteration | < 1 s | 4–5 | Closed-form P(λ) curves plus one verified circuit |
| E4 | **Noise-aware iteration choice on Forte** | "We pick k to minimise expected cost under the hardware noise model, and show the horizon where Grover stops paying." | k* = 1–2 instead of 4–8; needle case beats classical through n=6 (26.1 vs 32.5), loses at n=7 (67.2 vs 64.5), equals random guessing at n=8; real-rate case loses from n=6 (14.1 vs 13.0); with IonQ-billed MCZ the gain becomes a constant ~1.5× through n=12 | ≤8 | Analytic model instant; one IonQ job for calibration | 4 | Analytic global-depolarizing model only (validated within 0.04) |
| E5 | **How many events match?** (MLAE with noise-aware likelihood; QPE counting as a reference) | "We estimate M without QPE and correct for hardware noise." | At N ≤ 64 an exact classical count wins at every budget; MLAE beats random sampling only at budget ≫ N (ideal sweep: 8% rel. error for 352 vs ~3,000 samples); naive MLAE biased under noise (RMSE 2–4) and noise-aware fixes it (0.3–1.2); QPE counting falls from 0.77 to 0.19 accuracy under forte-1 (2,346 2Q) | ≤6 (MLAE); n+t ≤ 10 (QPE) | Reuses the E2 sweep counts: < 1 s | 5–6 | Drop |
| (F) | **"Triage" framing**: Grover picks which events get the expensive model run | — | Not a real gain: the screening predicate is cheap and Grover does not reduce the M expensive runs you still need | — | — | — | Use only as a sentence in the limitations |

### Inferences
- **Why not "triage".** The expensive model (tsunami, PAGER, CyberShake) runs *after* a cheap catalog filter selects candidates. Grover can only reduce evaluations of the *predicate*. If the predicate is cheap, there is nothing to save. If the predicate is the expensive model itself, the oracle must run that model reversibly in superposition, which hits the N* ≈ 10¹¹ wall. Judges with any seismology or cost sense will spot a triage pitch, so present it only as a cautionary note.
- **Is Prompt C credible for Impact?**
  - Only as an *honest negative result with a decision tool*. The measurable quantum difference that survives scrutiny is the query-count gap under the black-box model: 1.2–2.3× at N = 8–64 with CIs, growing like √N in the needle regime.
  - The measurable *practical* difference is negative by 6–9 orders of magnitude for catalog search.
  - This matches the Impact rubric ("strong classical baseline, measurable difference") better than any "√N speedup" claim, and is defensible in front of a global panel.
  - If the team wants a positive practical story, Prompt C is the wrong prompt. Its natural home is Quantum Unlocked ("the fine print of Grover").
- **Ranking for a 30-hour build.** E2 + E1 (core) > E4 (cheap add-on, uses the same job) > E3 (small, high visual value) > E5 (most fragile).

### Gaps
- I did not verify the build-hour estimates against this team's speed.
- Judge-run times are extrapolated from CPython timings on a loaded machine (Pyodide is typically slower; not measured).
- How the GT/global judges weigh an honest negative result under "Impact Potential" is not documented. The criteria list only names Novelty & Creativity, Technical Execution, Impact Potential and Documentation Quality.

## 6. Recommendation: one extension, a build outline, and how to satisfy one-job-per-run on IonQ

### Takeaway
Build **"Unknown-M Grover with an honest cost ledger"**: E2 as the core, with E1's ledger as the accounting layer. E4 and E3 are cheap add-ons that reuse the same job.

A single `backend.run([...])` of about 10–12 circuits covers everything:
- a Grover sweep G^k, k = 0..⌈√N⌉, on one real slice;
- one FPAA circuit;
- the n=3 honest-oracle circuits for k = 0, 1.

The same counts then feed the overshoot curve, BBHT (by resampling shots per k), noise-aware k selection and MLAE. The headline is the measured evaluations-to-first-verified-match with CIs against scan and index, followed by the ledger: what those evaluations cost in gates, noise and fault-tolerant seconds.

### Cited Findings
- Qollab's one-job rule: "Pass every circuit the run needs to a single `backend.run` call… The same rule covers the Estimator wrapper." — [Qollab docs: Runtime environment (via prior notes)](https://qollab.xyz/learn/docs/runtime-environment)
- IonQ noise models: `forte-1` and `forte-enterprise-1`, selected via `backend.run(qc, shots=…, noise_model="forte-1")`. Forte-class simulation is limited to ≤29 qubits; `sampler_seed` is optional. — [IonQ docs: simulation with noise models (via prior notes)](https://docs.ionq.com/guides/simulation-with-noise-models)
- **List-of-circuits and packed-register jobs both work in Aer.**
  - 21 circuits at n=5 ran 256 shots in 0.81 s (StatevectorSampler).
  - The 4 × 6-qubit packed circuit on 24 qubits decodes within 0.006 of theory.
  - — [results_c10](scripts/prompt_c/results_c10_one_job.txt)
- BBHT only ever uses G^j with j < √N, so a sweep over k = 0..⌈√N⌉ contains every circuit BBHT can request. — [BBHT](https://arxiv.org/abs/quant-ph/9605034); [c05 implementation](scripts/prompt_c/c05_bbht_vs_classical.py)

### Inferences
**Build outline** (about 30 h remain; times are for a 3–4-person team, working in parallel where marked)
1. **Data layer (2 h).**
   - Ship `catalog_2024_m5_slim.json` (1,504 events, 0.46 MB) in the project, plus an optional live FDSN GeoJSON refresh.
   - Expose the predicate (thresholds) and the bit encoding (5-bit magnitude, 4-bit depth).
   - Unit-test that the encoding agrees with the float predicate on all events (c02 shows 0 disagreements).
2. **Oracle compiler (4 h, parallel with step 3).**
   - `honest_oracle(slice, thresholds)` builds the QROM-ucry + `IntegerComparator` circuit (reuse `gs_core.py`).
   - `diagonal_equivalent(...)` derives the ±1 diagonal by classically evaluating the reversible circuit on each index, labelled in the UI as "this simulation touched all N events".
   - Add an equivalence test against the list oracle (c02 pattern).
   - Live simulation uses only the ≤6-qubit diagonal form. The 18–21-qubit honest circuit is transpiled live for gate counts and simulated offline only, because it takes 45–420 s in pure numpy.
3. **One-job runner (5 h).**
   - `circuits = [G^k for k in 0..K] + [FPAA] + [honest n=3, k=0,1]`, then `job = backend.run(circuits, shots=S)` with S = 256 locally and on IonQ, then read `get_counts(i)`. Do not use BackendSamplerV2 on IonQ (it returns zeros).
   - On the local simulator the same list goes to StatevectorSampler/BasicSimulator.
   - Wrap the IonQ path in try/except and fall back to a cached `forte-1` result labelled with date, shots and seed.
4. **Post-processing (4 h).** From the per-k counts:
   - (a) the overshoot curve with Wilson CIs;
   - (b) BBHT trajectories by drawing j per the BBHT rule and consuming *unused* shots from circuit j, verifying each candidate classically and counting calls plus checks, giving about 100+ independent trajectories per job;
   - (c) noise-aware k* = argmin (k+1)/P̂(k);
   - (d) MLAE estimate of M with a noise-aware likelihood (optional).
5. **Baselines (2 h).**
   - Random-scan theory and simulation, (N+1)/(M+1) with variance.
   - Indexed sqlite (in Pyodide) with a B-tree on magnitude: rows touched and time.
   - The FDSN server-side count, shown as "what the seismologist actually does".
   - Bootstrap CIs over many random windows (c05 pattern, 3,000 windows takes seconds).
6. **Ledger panel (3 h).**
   - Per-call and total 2Q counts (list vs honest; IonQ-like vs heavy-hex; IonQ-billed 6(n−2)).
   - Noisy P at forte-1 rates.
   - Fault-tolerant calculator: T_q = (π/4)√(N/M)·(2·Lookup + 4b + 2n)·t_Toff with t_Toff ∈ {170 µs, 17 ms, 1.7 µs} (Babbush et al.), against scan and index time, plus the N* formula.
   - A "QRAM assumed" toggle that shows the √N story and its critique (Jaques & Rattew; Aaronson).
7. **UI, plots and project page (5 h); video (2 h); IonQ run and cache (1 h).**

**Hour-20 checkpoint** (Sun ~08:00 ET)
- Must have: data, oracle compiler with equivalence test, local one-job sweep, BBHT-by-resampling with CIs vs scan and index, and a static ledger table.
- Drop if behind: MLAE (E5), live heavy-hex transpile (use cached counts), FPAA live circuit (keep closed-form curve).

**One-job-per-run on IonQ**
- **Preferred: a list of circuits** in one `backend.run`. It keeps statistics independent and avoids implying crosstalk-free hardware.
- **Alternative: packed registers.** Four n=6 sweeps fit in 24 ≤ 29 qubits; decode with bit shifts (validated in c10). Use it only if per-circuit overhead matters.
- Budget shots carefully, because IonQ's noise simulators simulate each shot separately. About 12 circuits × 256 shots ≈ 3k shots is a reasonable target (runtime unmeasured).
- Keep honest-oracle circuits to n=3, k ≤ 1 (226 2Q) on IonQ; the noise erases larger ones (F ≈ 1.4×10⁻⁴ at n=5, k=3 by the analytic model).

**Headline sentences for the page** (all measured)
- "On 3,000 real 64-event windows of the 2024 USGS catalog, Grover-type search found a shallow M≥6 quake in 7.1 [6.9, 7.3] predicate evaluations vs 16.4 [15.9, 16.9] for a random scan and about 10 rows for an index."
- "Building the oracle honestly costs about 2·b·N gates per call. At fault-tolerant speeds the search would take seconds where numpy takes microseconds. Grover helps a seismologist only for implicit search spaces beyond about 10¹¹ items."

### Gaps
- I did not verify end-to-end inside Qollab that `backend.run(list)` returns per-circuit counts for IonQ noise-model jobs, or how long a ~3k-shot forte-1 job takes.
- I did not verify whether Qollab's IonQ wrapper passes `noise_model`/`sampler_seed` through (prior notes flag this as unverified).
- I did not test the shot-resampling BBHT's independence assumptions beyond the ideal simulation. With S = 256 shots per circuit, the number of independent trajectories is limited by the least-populated j (estimate 100+; not measured).
