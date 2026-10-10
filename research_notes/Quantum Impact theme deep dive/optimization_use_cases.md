# Quantum Optimization Use Cases (2026 knowledge base for a "Quantum Impact" project)

Scope: building a credible hybrid quantum-classical optimization project for the Qollab × IonQ hackathon (Oct 9–11, 2026). The project needs a real-world problem, a public dataset, a strong classical baseline and a measurable quantum step. Build stack: Qiskit 2.x in Pyodide, qiskit-optimization 0.7.0, qiskit-algorithms 0.4.0, IonQ Forte noise model ≤29 qubits, ~100 two-qubit-gate budget at ~0.5% 2Q error, one IonQ job per run, no dynamic circuits.

Conventions:
- **[2025]** and **[2026]** mark results from those years.
- **VENDOR** marks a claim whose authors include the vendor of the hardware or algorithm. **INDEP** marks an independent or academic result. **COMPETITOR** marks a critique by a rival vendor's staff.
- † marks a link I cited from the established literature without re-fetching it this session. The arXiv IDs are the ones I'm confident of, but check them before putting them on a slide.
- Statements under "Inferences" are my own derivations or synthesis, not source claims.

---

## Q1. Problem formulation: QUBO/Ising mappings, penalties, constrained mixers, HUBO cost on IonQ, encodings, decomposition beyond 29 variables

### Takeaway
How a problem is encoded matters more on a ~100-2Q-gate budget than which algorithm is used. On IonQ hardware:
- Each nonzero quadratic coupling costs exactly one native ZZ gate per layer.
- A k-body term costs 2k−3 two-qubit gates.
- One-hot penalties make the coupling graph dense.

So the winning moves are compact encodings (domain-wall or log, as in IonQ-DESY's 36-variable → 18-qubit flight-gate run), constraint-preserving XY mixers (JPMC on trapped ions, 20 qubits), hand-tuned penalties (qiskit-optimization's auto-penalty falls back to 1e5 when any constraint coefficient is fractional), and decomposition that is honest about how its subproblems are carved out.

### Cited Findings

**Canonical mappings**
- Lucas (2014) gives Ising/QUBO Hamiltonians for Karp's 21 NP-complete problems and many NP-hard ones: partitioning, covering, packing, coloring, Hamiltonian cycles/TSP, clique, set cover, knapsack and more. The standard construction is H = A·H_constraints + B·H_objective, with A chosen large enough relative to B that violating any constraint never pays. TSP uses N² spins (city × tour position). — [Lucas, Front. Phys. 2:5 (2014), arXiv:1302.5843](https://arxiv.org/abs/1302.5843) †
- Glover–Kochenberger–Du tutorial ("Quantum Bridge Analytics I"). It is the standard reference for turning constraints into quadratic penalties:
  - x+y ≤ 1 → P·xy
  - x+y = 1 → P(1−x−y+2xy)
  - x ≤ y → P(x−xy)
  - Linear equalities Ax = b in general → P(Ax−b)²

  — [Glover, Kochenberger, Du, 4OR 17 (2019), arXiv:1811.11538](https://arxiv.org/abs/1811.11538) †
- The Quantum *Alternating Operator* Ansatz generalizes QAOA to mixers that keep the state inside the feasible subspace. Examples are XY mixers for one-hot and Hamming-weight constraints, and controlled mixers for independent set. This removes the penalty terms from the cost Hamiltonian. — [Hadfield et al., Algorithms 12(2):34 (2019), arXiv:1709.03489](https://arxiv.org/abs/1709.03489) †
- XY mixers come in ring, parity and complete-graph variants. They preserve Hamming weight, and how well they perform depends on the variant and the initial state. — [Wang, Rubin, Dominy, Rieffel, PRA 101, 012320 (2020), arXiv:1904.09314](https://arxiv.org/abs/1904.09314) †
- The Grover mixer (GM-QAOA) uses any feasible-state preparation unitary as the mixer. It is limited by the cost of preparing that state. — [Bärtschi & Eidenbenz, IEEE QCE 2020, arXiv:2006.00354](https://arxiv.org/abs/2006.00354) †

**Penalty tuning (with concrete library behaviour)**
- qiskit-optimization's `LinearEqualityToPenalty._auto_define_penalty` (read from source this session):
  - It returns `default_penalty = 1e5`, with a logged warning, if *any* constraint coefficient or right-hand side is a float with a nonzero fractional part.
  - Otherwise it returns `1.0 + (lin_b.upperbound − lin_b.lowerbound) + (quad_b.upperbound − quad_b.lowerbound)`, i.e. 1 plus the ranges of the objective's linear and quadratic coefficients.
  - The docstring says that if None is passed, "a penalty factor will be automatically calculated on every conversion."

  — [qiskit-optimization source](https://raw.githubusercontent.com/qiskit-community/qiskit-optimization/main/qiskit_optimization/converters/linear_equality_to_penalty.py); [API docs](https://qiskit-community.github.io/qiskit-optimization/stubs/qiskit_optimization.converters.LinearEqualityToPenalty.html)
- There is a trade-off between penalties and mixers on trapped-ion hardware. JPMorgan's extractive-summarization study notes "the trade-off between the in-constraint probability and the quality of the solution" for unconstrained (penalty) methods, which "makes choosing good parameters difficult in general." Their XY-QAOA (Hamming-weight-preserving) "natively preserves constraints on quantum hardware." Circuits ran up to 20 qubits with 2Q depth up to 159 on a trapped-ion machine. — [Niroula et al., Sci Rep 12, 17171 (2022), arXiv:2206.06290](https://arxiv.org/abs/2206.06290) (VENDOR-adjacent: JPMC authors, trapped-ion hardware partner)
- The Kipu/IonQ protein-folding HUBO used a constraint Lagrange multiplier of λ_gc = 10. — [arXiv:2506.07866](https://arxiv.org/html/2506.07866v1) **[2025]**

**Encodings: one-hot vs domain-wall vs binary/log vs Pauli-correlation**
- Domain-wall encoding represents an m-valued variable with m−1 qubits, versus m for one-hot. The constraint becomes a chain of 2-body ferromagnetic couplings rather than a dense one-hot penalty. — [Chancellor, QST 4, 045004 (2019), arXiv:1903.05068](https://arxiv.org/abs/1903.05068) †
- There is a systematic study of the trade-offs between one-hot, unary/domain-wall and binary/Gray encodings for coloring, routing and scheduling. Binary encodings save qubits but create higher-order terms and unused (invalid) codewords. — [Sawaya et al., Quantum 7, 1111 (2023), arXiv:2203.14432](https://arxiv.org/abs/2203.14432) †; [Glos, Krawiec, Zimborás, npj QI 8, 39 (2022), arXiv:2009.07309](https://arxiv.org/abs/2009.07309) †
- **IonQ + DESY flight-gate assignment (hardware Sept 2023, announced Mar 14, 2024):**
  - Used a "logarithmic-linear encoding" on IonQ Aria, which required re-engineering the Hamiltonian, with COBYLA in a hybrid loop.
  - Instances ran from 8 variables (2 flights × 4 gates) on 4 qubits up to 36 variables (9 flights × 4 gates) on 18 qubits.
  - Only the small cases were fully tuned on hardware. The larger ones were tuned on a simulator and then run once as inference on the QPU.

  This is a VENDOR result. The press framing of beating "traditional classical computing" was not independently validated. — [IonQ blog](https://ionq.com/blog/ionq-and-desy-tackle-the-gate-assignment-problem); [IonQ news](https://ionq.com/news/ionq-and-desy-research-highlights-quantums-potential-benefits-for-airport); [TQI](https://thequantuminsider.com/2024/03/15/ionq-and-desy-research-highlights-quantums-potential-benefits-for-airport-flight-gate-optimization/)
- **Pauli Correlation Encoding (PCE) [2025]:**
  - m = O(n^k) binary variables are encoded in n qubits via x_i = sgn(⟨Π_i⟩), where the Π_i are k-body Pauli strings in 3 commuting families. That means only 3 measurement settings are needed.
  - Parameter count grows roughly linearly and depth sublinearly in m.
  - Published as Sciorilli et al., Nat. Commun. 16, 476 (2025), per a later citing paper.
  - Follow-ups cover portfolio optimization and LABS. LABS reportedly reaches N=44 with 6 qubits, but that comes from an automated overview and is unverified.
  - This is a variational, expectation-value method. It is not peaked-sample QAOA, and it needs many shots per evaluation.

  — [arXiv:2401.09421](https://arxiv.org/abs/2401.09421); [portfolio PCE arXiv:2511.21305](https://arxiv.org/pdf/2511.21305); [LABS PCE arXiv:2506.17391](https://arxiv.org/html/2506.17391v1); [IBM tutorial](https://quantum.cloud.ibm.com/docs/tutorials/pauli-correlation-encoding-for-qaoa)

**Higher-order (HUBO) terms**
- **Kipu + IonQ BF-DCQO protein folding (June 2025)** used a tetrahedral lattice with Miyazawa–Jernigan contacts and Hamiltonian terms up to **5-body**:

  | Instance | Qubits | Pauli terms |
  |---|---|---|
  | GYDPETGTWG | 22 | 589 |
  | QPPGGSKVILF | 27 | 901 |
  | WTFGQGTKVEIK | 33 | 1371 |

  After angle-cutoff pruning, a single Trotter step compiled to **269–646 ZZ gates**: soft pruning (630–646) or hard pruning (269–292) for the 22-qubit peptide, and 334–601 for the 33-qubit one.
  - MAX 4-SAT (4-body terms) at 24–36 qubits needed ~7,400–13,000 ZZ gates unpruned, cut to 75–913 by pruning.
  - SK spin glass at 36 qubits (2-body) used 86–364 ZZ.

  VENDOR (Kipu + IonQ authors). — [arXiv:2506.07866 (html)](https://arxiv.org/html/2506.07866v1)
- **Feature selection as HUBO [2026]:** "one-, two-, and three-body interaction terms derived from mutual-information measures" plus structured linear penalties that suppress the trivial all-selected solution. Datasets were Gallstone and Spambase. It ran on IonQ Forte with digitized counterdiabatic optimization. VENDOR (Kipu + IonQ). — [arXiv:2604.26834](https://arxiv.org/abs/2604.26834) (submitted Apr 29, 2026)

**Decomposition for >29 variables**
- **Iterative-QAOA on JIT job-shop [2025]:**
  - The master instance is 20 jobs × 3 machines with time slots {20, 22, 23} per machine, which gives **1,300 binary variables** in a time-indexed one-hot encoding. It was solved classically to an optimal makespan of 193.
  - The 24–36-qubit QPU sub-instances were built by **"freezing" most variables to the optimal solution.**

  VENDOR (IonQ). — [arXiv:2510.26859v2 (html)](https://arxiv.org/html/2510.26859v2)
- **QAOA-in-QAOA:** partition a large MaxCut graph into subgraphs, solve each with QAOA, then solve a second-level MaxCut over subgraph "flip" variables to merge the results. — [Zhou et al., arXiv:2205.11762](https://arxiv.org/abs/2205.11762) †
- **Unit-commitment decompositions:**
  - Three-block ADMM, with QAOA on the binary QUBO block and classical solvers on the continuous blocks. — [Mahroo & Kargarian, arXiv:2201.03701](https://arxiv.org/pdf/2201.03701)
  - Splitting by grid topology into parallel limited-qubit subproblems **[2025]**. — [Zhou et al., arXiv:2503.20509](https://arxiv.org/html/2503.20509v1)
- **RQAOA** eliminates variables recursively using the largest-magnitude measured correlation ⟨Z_iZ_j⟩, fixing Z_i = ±Z_j. That reduces the problem one variable at a time and natively shrinks oversized instances. — [Bravyi, Kliesch, Koenig, Tang, PRL 125, 260505 (2020), arXiv:1910.08980](https://arxiv.org/abs/1910.08980) †
- **CVaR objective:** optimize the mean of the best α-fraction of sampled energies instead of the full expectation. This improves convergence for sampling-based optimization. — [Barkoutsos et al., Quantum 4, 256 (2020), arXiv:1907.04769](https://arxiv.org/abs/1907.04769) †

### Inferences
- **2Q-gate cost on IonQ (my derivation):**
  - A 2-body term exp(−iθZ_iZ_j) is 1 native ZZ(θ). Per QAOA layer, the cost costs |E| native ZZ gates, where |E| is the number of nonzero off-diagonal QUBO entries.
  - A k-body term exp(−iθZ⊗k) costs **2k−3** two-qubit gates: a CNOT ladder of 2(k−2), where each CNOT is 1 native, plus 1 RZZ. That gives 3-body = 3, 4-body = 5, 5-body = 7.
  - Compare quadratization (Rosenberg: xy → auxiliary z plus penalty M(xy−2xz−2yz+3z)). It costs **one extra qubit per replaced product** plus 3 new couplings. On IonQ it is almost always better to keep native HUBO terms than to quadratize, because qubits are scarcer than gates under the 29-qubit simulation cap.
- **One-hot is the budget killer.**
  - A one-hot group of size m adds m(m−1)/2 couplings via (Σx−1)².
  - TSP with n cities (first city fixed) needs (n−1)² qubits: 5 cities = 16 qubits, 6 cities = 25.
  - Its constraint-penalty graph alone has 2·(n−1)·C(n−1,2) couplings: 48 at n=5 and 100 at n=6. That reaches or exceeds the budget before the distance terms are added.
  - This is why TSP/VRP is a bad fit and also why Qollab's existing QAOA logistics games make it unoriginal.
- **XY mixer cost:** exp(−iβ(XX+YY)/2) is 2 native 2Q gates because XX and YY commute. A ring-XY mixer over n qubits therefore costs about 2n two-qubit gates per layer, plus a feasible initial state.
  - The initial state can be a single basis state, such as a greedy solution with exactly k ones, at **0 extra 2Q gates**.
  - Alternatively it can be a Dicke state with O(kn) CNOTs; see [Bärtschi & Eidenbenz, arXiv:1904.07358](https://arxiv.org/abs/1904.07358) †.
  - For k-of-n selection the XY mixer also deletes the dense (Σx−k)² penalty clique, which saves n(n−1)/2 couplings unless the objective is dense anyway, as Markowitz covariance is.
- **Penalty practice for the build:**
  - Never rely on the 1e5 fallback.
  - Set P slightly above the largest single-variable objective swing, which is roughly what the integer-case formula does.
  - Then sweep P ∈ {0.5, 1, 2, 4}×P₀ in simulation and report feasibility rate against P(opt) as a curve. That curve is itself a credible, judge-legible result.
  - Rescale the whole Hamiltonian (for example, so the max |coefficient| = 1) before applying any fixed or transferred QAOA angles.
- **Decomposition honesty.** The IonQ JSSP paper built its sub-instances by freezing variables *to the known optimum*, so the quantum subproblem is guaranteed to contain the global optimum. A credible hackathon version should freeze around a *heuristic* incumbent (greedy, SA or CP-SAT with a short time limit) and use the quantum sampler as a **large-neighborhood-search (LNS) move**. It should then report how often the move improves the incumbent.

### Gaps
- I did not fetch Lucas's exact penalty-magnitude bounds for each problem class, or the Rosenberg quadratization source. Both are standard textbook results, cited above from memory.
- No primary source was fetched for domain-wall versus one-hot hardware performance on IonQ specifically. The IonQ-DESY "log-linear" encoding details (exact Hamiltonian) are in the IonQ blog and preprint, which I did not open in full.
- The IonQ-DESY preprint's arXiv ID was not found in this session.

---

## Q2. Algorithms with 2023–2026 evidence (QAOA family, counterdiabatic, annealing, QITE, GAS, QeMCMC, DQI, IonQ hardware papers)

### Takeaway
On trapped-ion hardware, what works in 2024–2026 is **non-variational or lightly variational sampling**: LR-QAOA, Iterative-QAOA, multi-angle QAOA and BF-DCQO, combined with classical post-processing. The optimum "appears in the samples" at 12–36 qubits, but raw hardware probabilities can be tiny (0.7–0.9% at 32–33 qubits for Iterative-QAOA before mitigation).

Every 2025 "runtime advantage" claim for optimization was challenged within months:
- BF-DCQO by D-Wave staff and by an independent Polish group (published in PR Applied 2026)
- D-Wave/USC annealing scaling advantage by GPU-based classical heuristics

Credible framing in 2026 is "a quantum sampler inside a classical loop, with an ablation". It is not "quantum beats classical".

### Cited Findings

**QAOA fundamentals and limits**
- p=1 QAOA on 3-regular MaxCut has a guaranteed ratio of 0.6924. Low-depth QAOA is limited by Z2 symmetry and locality: Bravyi et al. 2020; Farhi–Gamarnik–Gutmann 2020; Hastings 2019, which showed local classical algorithms match or beat p=1. — summarized with links in prior notes: [Farhi et al. arXiv:1411.4028](https://arxiv.org/abs/1411.4028); [Bravyi et al. arXiv:1910.08980](https://arxiv.org/abs/1910.08980)
- **[2025 workshop report]** "Proving robust separations between quantum and classical algorithms for optimization problems is a fundamental challenge". Log-depth QAOA "does not have an asymptotic quantum advantage for a large class of sparse combinatorial optimization problems." — [NQI Joint Algorithms Workshop report, arXiv:2508.13973](https://arxiv.org/pdf/2508.13973)
- On Google Sycamore, QAOA on hardware-native planar graphs performed independently of size. Non-native problems (3-regular MaxCut, SK model), which need routing/SWAPs, degraded. This is the classic evidence for why connectivity matters. — [Harrigan et al., Nat. Phys. 17, 332 (2021), arXiv:2004.04197](https://arxiv.org/abs/2004.04197) †
- Trapped-ion QAOA history: p=1 QAOA on a long-range Ising model with up to 40 trapped-ion qubits at UMD/Monroe, the lineage IonQ grew out of. — [Pagano et al., PNAS 117, 25396 (2020), arXiv:1906.02700](https://arxiv.org/abs/1906.02700) †

**Parameter concentration / transfer / fixed schedules**
- For fixed parameters, the QAOA objective concentrates across typical instances drawn from the same ensemble, so parameters can be trained on small instances and reused. — [Brandão et al., arXiv:1812.04170](https://arxiv.org/abs/1812.04170) †
- Parameter transfer works for weighted MaxCut and other weighted problems after appropriate rescaling of the weights. — [Shaydulin et al., arXiv:2201.11785](https://arxiv.org/abs/2201.11785) †; [Sureshbabu et al., Quantum 8, 1231 (2024), arXiv:2305.15201](https://arxiv.org/abs/2305.15201) †
- **LR-QAOA [2025]:**
  - Uses a fixed linear ramp with no optimizer.
  - The success probability fits P(x*) ~ 2^(−η(p)N + C), with η improving from 0.22 at p=10 to 0.05 at p=100 on weighted MaxCut.
  - Hardware runs on IonQ, Quantinuum and IBM went up to 109 qubits and p=100, with up to 21,200 CNOTs.

  INDEP (Jülich). — [Montañez-Barrera & Michielsen, npj QI 11, 131 (2025), arXiv:2405.09169](https://arxiv.org/abs/2405.09169)
- **Iterative-QAOA on IonQ Forte (Oct 2025, revised Dec 2025)**, a non-variational fixed schedule with warm-start iterations. VENDOR (IonQ).
  - **Schedule:** β_k = (1−k/p)Δβ and γ_k = ((k+1)/p)Δγ, with Δβ = Δγ = 0.17.
  - **Warm-start update:**
    - After each run, samples are Boltzmann-weighted, P(s_j) ∝ exp(−β_T E_j), with β_T going 0.1 → 1.0 over 10 iterations.
    - Each qubit's flip probability p_q = ½(1 − η⟨σ_z⟩_T) sets the next product initial state R_y(2·arcsin√p_q).
    - The mixer is modified so that this state is an eigenstate.
  - **Resources:**

    | Qubits | p | 2Q gates (RZZ) |
    |---|---|---|
    | 24 | 4 | 312 |
    | 32 | 5 | 780 |
    | 33 | 5 | 840 |
    | 36 | 6 | 972 |

    4,000 shots per circuit; 40,000 executions over 10 iterations.
  - **Results:**
    - 32 qubits: P(opt) ideal 0.780; QPU raw **0.007**; QPU + "DNL" mitigation 0.693.
    - 33 qubits: ideal 0.914; QPU raw **0.009**; with DNL 0.755.
    - 36 qubits: the QPU best was 198, the first excited state, versus the optimum of 193, with P(opt) = 0.
    - MPS simulation at 50 and 97 qubits (χ=256) did not find the optimum (best 198 and 206).
  - **Comparators:**
    - LR-QAOA at 24 qubits needed p=50 (3,900 2Q gates) to reach P(opt) = 3.82%.
    - VarQITE needed about **1,006,200 circuit executions** (129 circuits × 120 shots × 65 steps) and reached only excited states.

  — [arXiv:2510.26859v2](https://arxiv.org/html/2510.26859v2); [abstract](https://arxiv.org/abs/2510.26859)
- **Shipment selection [2026]:** Iterative-QAOA on Forte at 20–35 qubits, with "only IonQ's default debiasing… no further error mitigation". The main results come from noiseless simulation. — [arXiv:2604.11758](https://arxiv.org/abs/2604.11758) (from prior notes)

**Multi-angle, warm-start, recursive, CVaR, filtering**
- Multi-angle QAOA gives each term its own angle: |E|+|V| parameters per layer. It reaches higher approximation ratios at fewer layers. — [Herrman et al., Sci Rep 12, 6781 (2022), arXiv:2109.11455](https://arxiv.org/abs/2109.11455) †
- **Airbus aircraft loading on IonQ Aria and Forte [2025]:**
  - A multi-angle variant with fewer 2Q gates, and a cost function that handles inequality constraints without slack qubits.
  - Found "the optimal solutions for all the problem instances studied ranging from 12 qubits to 28 qubits". In the 12-qubit case, P(opt) was about 70% with 1000 shots and COBYLA (≤100 iterations).
  - No classical runtime comparison. VENDOR-partner.

  — [arXiv:2504.01567](https://arxiv.org/abs/2504.01567) (from prior notes)
- **Warm-start QAOA:**
  - Solve a continuous relaxation (QP, or the Goemans–Williamson SDP with randomized rounding).
  - Initialize qubit i in R_y(θ_i) with θ_i = 2·arcsin(√c_i), where c_i is the relaxed value regularized by ε, and use a matching mixer.
  - With GW rounding this keeps the GW guarantee at depth 0.

  Implemented as `WarmStartQAOAOptimizer` in qiskit-optimization. — [Egger, Mareček, Woerner, Quantum 5, 479 (2021), arXiv:2009.10095](https://arxiv.org/abs/2009.10095) †
- **RQAOA and its generalization QIRO** (quantum-informed recursive optimization, which uses quantum correlations to guide classical variable elimination). — [Bravyi et al. 2020](https://arxiv.org/abs/1910.08980) †; [Finžgar et al., PRX Quantum 5, 020327 (2024), arXiv:2308.13607](https://arxiv.org/abs/2308.13607) †
- **CVaR-QAOA/VQE.** — [Barkoutsos et al. 2020](https://arxiv.org/abs/1907.04769) †
- **Filtering VQE (Quantinuum)** applies a filter operator f(H) that pushes amplitude toward low-energy states, with better convergence than QAOA on small weighted MaxCut. — [Amaro et al., QST 7, 015021 (2022), arXiv:2106.10055](https://arxiv.org/abs/2106.10055) †

**Counterdiabatic / BF-DCQO (Kipu), with the advantage dispute**
- **Method:** start in |+⟩^N under H_i = −Σσˣ. Run a digitized counterdiabatic evolution, using a first-order nested-commutator CD term and pruning small angles. Then update per-qubit bias fields from ⟨σᶻ⟩ over the lowest-energy α-fraction of samples. Each iteration starts from the previous solution, and circuit resources shrink over iterations. — [arXiv:2506.07866](https://arxiv.org/html/2506.07866v1); original algorithm [arXiv:2405.13898](https://arxiv.org/pdf/2405.13898); HUBO version [arXiv:2409.04477](https://arxiv.org/html/2409.04477)
- **Kipu + IonQ protein folding on Forte and Forte Enterprise (36 qubits) [2025, VENDOR]:**
  - Device median 2Q DRB fidelity was 99.3% (Forte) and 99.5% (Forte Enterprise).
  - Each run used 2,000 shots per iteration, ≤10 iterations and 1 Trotter step.
  - Post-processing was zero-temperature SA local search on the best 5% of samples, with ≤3 sweeps.
  - **With post-processing**, the optimum was reached for all three peptides (10–12 residues).
  - MAX 4-SAT reached the optimum on every instance size (24–36 qubits); misses were off by 1–2 clauses.
  - The SK model hit the exact ground state on 2 of 3 36-qubit instances in under 10 iterations.
  - References for scoring were brute force, PySAT and Gurobi.
  - The press release claims the "most complex known protein folding problem ever run on a quantum computer". The paper's claim is narrower: largest *on quantum hardware*.

  — [arXiv:2506.07866](https://arxiv.org/html/2506.07866v1); [IonQ press release, Jun 19, 2025](https://ionq.com/news/ionq-and-kipu-quantum-break-new-performance-records-for-protein-folding-and); [TQI](https://thequantuminsider.com/2025/06/20/ionq-and-kipu-quantum-break-new-performance-records-for-protein-folding-and-optimization-problems/)
- **Kipu/IBM "runtime quantum advantage" (May 2025, VENDOR):**
  - BF-DCQO on IBM's 156-qubit hardware on HUBO instances.
  - Claimed "up to 80× faster than CPLEX" and "12× faster than SA" at comparable quality.
  - The 156-qubit instance was the hardest out of a pool of 250 generated instances.

  — [arXiv:2505.08663](https://arxiv.org/pdf/2505.08663); [Kipu blog](https://kipu-quantum.com/knowledge-hub/blog/runtime-quantum-advantage-with-bf-dcqo/)
- **Critique 1, COMPETITOR [Sep 2025]:** Farré, Ordog, Chern and McGeoch report that D-Wave annealers find solutions of "far greater quality than claimed" using "far less computation time". They also report that the quantum part of BF-DCQO makes "minimal contributions to solution quality". The abstract page lists no affiliations; to my knowledge the authors are D-Wave staff. — [arXiv:2509.14358](https://arxiv.org/abs/2509.14358)
- **Critique 2, INDEP (Gardas group, Poland) [Oct 2025 → Phys. Rev. Applied 25, 044084 (2026)]:**
  - "The runtime advantage of the BF-DCQO hybrid algorithm is not observed under more comprehensive benchmarking."
  - On the USC/D-Wave annealing PRL, it says the work "effectively uses annealing time as a proxy for runtime".
  - Overall: "runtime-based quantum advantage has not yet been demonstrated under experimentally grounded performance metrics."

  — [Tuziemski et al., arXiv:2510.06337](https://arxiv.org/abs/2510.06337)
- **Classical "BF-Null" control.** A secondary analysis reports that replacing the quantum subroutine with a classical routine in the same bias-field loop matches or exceeds BF-DCQO. It also describes Kipu's framing as shifting from "runtime quantum advantage" to "hybrid sequential quantum computing". The source is an automated LLM verification paper, so treat it as a pointer rather than expert consensus. — [AutoVerifier, arXiv:2604.02617](https://arxiv.org/pdf/2604.02617) **[2026]**
- **Kipu's 2026 follow-up [Mar 2026, VENDOR + Koch (ZIB) + Woerner (IBM)]:** an end-to-end HSQC benchmark on IBM Heron r3 over 20 HUBO instances.
  - HSQC matched the ground state on 14 of 20 in under 1 s end to end.
  - At equal runtime, SA, memetic tabu and EasySolve did not reach the HSQC value.
  - **Enhanced parallel tempering and GPU ABS3 "reach or surpass it."**
  - The authors' claim is "competitive with" 128 vCPUs or 8 A100 GPUs, which is not advantage.

  — [arXiv:2603.13607](https://arxiv.org/abs/2603.13607); [Sequential Quantum Computing, arXiv:2506.20655](https://arxiv.org/pdf/2506.20655)

**Quantum annealing comparisons**
- **USC/D-Wave [2025]:**
  - Quantum annealing correction gives more than 1,300 error-suppressed logical qubits on D-Wave.
  - On 2D spin glasses with high-precision couplings, it shows a *scaling* advantage in time-to-ε over PT-ICM for optimality gaps ≥1%.
  - Exact-optimization advantage "has so far remained elusive."

  — [Munoz-Bauza & Lidar, PRL 134, 160601 (2025), arXiv:2401.07184](https://arxiv.org/pdf/2401.07184); [USC news](https://today.usc.edu/quantum-computer-outperforms-supercomputers-in-approximate-optimization/)
- **Rebuttal, INDEP [2025 → PR Applied 2026]:** a GPU-based classical method (SBM) "scales as well as, or better than" the QA results across the accuracy levels tested. An earlier version concluded that current annealers are "unlikely" to show supremacy on discrete approximate optimization under practical conditions. — [Pawłowski et al., arXiv:2505.22514](https://arxiv.org/pdf/2505.22514)
- **Binary paint shop [Apr 2026]:** a classical Mean-Field AOA reaches a paint-swap ratio of ≈0.2799, which "beats all known classical heuristics and quantum algorithms to date". D-Wave Advantage2 reached 0.320. — [arXiv:2604.00607](https://arxiv.org/html/2604.00607v2)

**Other IonQ-hardware optimization papers (2025–2026)**
- **Feature selection, HUBO, Forte [Apr 2026, VENDOR Kipu + IonQ]:**
  - Gallstone and Spambase datasets.
  - Baselines were SelectKBest (mutual information) and PCA.
  - Hardware showed "good qualitative agreement" with noiseless simulation and "competitive classification performance".
  - Prior notes record 32 qubits, ~1,000 2Q gates and 2,000 shots per circuit, with results "after 1 iteration… already competitive". The abstract does not give numeric accuracy deltas.

  — [arXiv:2604.26834](https://arxiv.org/abs/2604.26834)
- **Network routing under link failures on Forte [Feb 2026]:**
  - QAOA layers were cut from 20 to 8 "to improve the fidelity"; only 3 cases were run because of cost.
  - The best valid solution appeared 2, 5 and 16 times, while most other bitstrings appeared once. The signal was weak but present.

  — [arXiv:2602.04495](https://arxiv.org/abs/2602.04495) (from prior notes)

**QITE, GAS, QeMCMC, DQI**
- **QITE** prepares ground states by imaginary-time evolution using local unitary approximations. — [Motta et al., Nat. Phys. 16, 205 (2020), arXiv:1901.07653](https://arxiv.org/abs/1901.07653) †
- **VarQITE on IonQ cost about 1M executions** for a 32-qubit JSSP and only reached excited states (see the Iterative-QAOA entry). — [arXiv:2510.26859v2](https://arxiv.org/html/2510.26859v2)
- **Grover adaptive search** for constrained polynomial binary optimization is a quadratic speedup over exhaustive search. It needs quantum-dictionary arithmetic oracles (`GroverOptimizer` in qiskit-optimization). — [Gilliam, Woerner, Gonciulea, Quantum 5, 428 (2021), arXiv:1912.04088](https://arxiv.org/abs/1912.04088) †
- **Quantum-enhanced MCMC [2023]:** the quantum processor proposes moves by evolving in superposition, and a classical computer accepts or rejects them. It "converges in fewer iterations than common classical MCMC alternatives on relevant problem instances, both in simulations and experiments", on a superconducting processor with classical Ising models. — [Layden et al., Nature 619, 282 (2023), arXiv:2203.12497](https://arxiv.org/abs/2203.12497)
- **DQI [Nature 2025]:**
  - Gives a superpolynomial speedup for Optimal Polynomial Intersection, which has Reed–Solomon structure.
  - Advantage on sparse max-XORSAT is unresolved.
  - **[2025–2026] critiques:**
    - No DQI advantage for MaxCut. — [Parekh, arXiv:2509.19966](https://arxiv.org/abs/2509.19966)
    - The overlap-gap property obstructs DQI and AMP beats it on random LDPC instances. — [arXiv:2509.14509](https://arxiv.org/html/2509.14509v1)
    - DQI sits low in PH. — [arXiv:2509.14443](https://arxiv.org/abs/2509.14443)
    - Block-Gibbs MCMC reproduces DQI's ratios on max-XORSAT. — [arXiv:2607.28120](https://arxiv.org/abs/2607.28120)

  — [Jordan et al., arXiv:2408.08292](https://arxiv.org/abs/2408.08292v3) (details in prior notes algorithms_and_complexity.md)
- **LABS scaling evidence [2024]:**
  - Fixed-parameter QAOA plus quantum minimum-finding showed better scaling than branch-and-bound in noiseless simulation up to 40 qubits.
  - Hardware runs used Quantinuum with error detection.
  - This is the main positive QAOA scaling claim that the debate references.

  — [Shaydulin et al., Sci. Adv. 10, eadm6761 (2024), arXiv:2308.02342](https://arxiv.org/abs/2308.02342)

### Inferences
- **Algorithms ranked by fit under the build constraints** (one hardware job, ~100 2Q gates, no mid-circuit measurement):
  1. **LR-QAOA, or Iterative-QAOA with all iterations except the last done on the noise model.** No optimizer loop is needed. Parameters come from Δβ = Δγ ≈ 0.17-style ramps or from small-instance transfer.
  2. **Warm-start QAOA at p=1–2.** The classical relaxation comes from `scipy` or a precomputed GW solution.
  3. **Multi-angle QAOA, trained in simulation and then one hardware shot batch.**
  4. **BF-DCQO-style bias iterations** in simulation, with the final iteration on hardware, **only with a BF-Null ablation**.

  GAS and DQI are simulator-only teaching pieces: their oracle and decoder circuits run to hundreds or thousands of 2Q gates. QeMCMC is plausible in simulation at ≤12 spins, but its hardware story needs many short jobs, which conflicts with one job per run.
- The Iterative-QAOA numbers are the most useful calibration point for IonQ. **Raw hardware P(opt) is below 1% at roughly 800 2Q gates and 32 qubits.** At about 100 2Q gates and 12–16 qubits, expect a far stronger signal: global-fidelity proxy ≈ 0.61 at 0.5% error (see Q5).
- "VENDOR found the optimum" claims nearly always involve **post-processing** (SA local search on the top 5% of samples, or mitigation such as DNL). A credible project must report raw, mitigated and post-processed results separately, and must report what the post-processor alone achieves from random inputs.

### Gaps
- What "DNL" error mitigation in the IonQ JSSP paper stands for and how it works was in the unread portion of the paper (characters after 100k).
- I did not fetch the scaling exponents claimed by Layden et al. or the qubit count of their hardware run. Later critiques of QeMCMC were not searched.
- No independent (non-Kipu, non-D-Wave) replication of BF-DCQO on IonQ hardware was found.
- The IBM "quantum advantage tracker" and any optimization entries in it (2025–2026) were not examined. The [IBM blog](https://www.ibm.com/quantum/blog/quantum-advantage-era) frames advantage as hypothesis, then community validation or falsification.
- I did not fetch the details of the March 2026 "multi-core classical" benchmark (problem families, time budgets).

---

## Q3. Application domains, public datasets, honest qubit sizes, and how to subsample credibly

### Takeaway
The domains with real hardware precedent on IonQ are aircraft loading (Airbus), flight-gate assignment (DESY), job-shop scheduling (IonQ/Clemson), protein folding, MAX-SAT and spin glasses (Kipu), feature selection (Kipu), shipment selection and network routing. All fit 12–36 qubits only after aggressive subsampling or variable freezing.

Domains that are *not* already Qollab logistics races, and that have clean public data and natural 10–20-variable cores, are the best bets:
- feature selection (UCI)
- unit commitment (MATPOWER)
- cardinality-constrained portfolio
- stand/gate assignment
- QOBLIB small instances

### Cited Findings

**Benchmark libraries (optimization-native)**
- **QOBLIB "Intractable Decathlon" [2025]:**
  - Ten problem classes chosen to be hard for leading classical solvers while still studiable on current quantum machines: market split, LABS, minimum Birkhoff decomposition, Steiner tree packing, sports scheduling, portfolio optimization, independent set, network design, vehicle routing and graph topology design.
  - It uses model-independent benchmarking and publishes solution track records.
  - The authors come from ZIB/TU Berlin, IBM, Kipu, E.ON, NTT Data and others.
  - Trade press reports about 1,264 instances and 2,600+ submissions; both counts are unverified, and the press size ranges are internally inconsistent.

  — [Koch et al., arXiv:2504.03832](https://arxiv.org/html/2504.03832v2); [QCR](https://quantumcomputingreport.com/global-consortium-launches-quantum-optimization-benchmarking-library-qoblib-to-track-path-to-quantum-advantage/)
- **QPLIB:** a library of quadratic programs (including binary QPs/QUBOs) at ZIB. — [qplib.zib.de](https://qplib.zib.de/) †
- **MQLib:** a library of 3,000+ MaxCut/QUBO instances with dozens of heuristics implemented in C++. The paper is a systematic "what works best when" study. — [Dunning, Gupta, Silberholz, INFORMS J. Comput. 30(3) (2018)](https://github.com/MQLib/MQLib) †
- **Gset:** MaxCut graphs with 800+ nodes (Rudy generator), the standard benchmark for GW/BLS. — [Gset](https://web.stanford.edu/~yyye/yyye/Gset/) †

**Logistics / routing**
- CVRPLIB, hosted at PUC-Rio (galgos), includes Set E (Christofides & Eilon 1969). — [course pointer to CVRPLIB galgos site](https://kam.mff.cuni.cz/~kolman/MATPROG/project.pdf); [heumilkr cvrplib_E docs](https://rdrr.io/cran/heumilkr/man/cvrplib_E.html). The smallest instances, E-n13-k4 (12 customers) and P-n16-k8, could not be confirmed from a source this session.
- TSPLIB has burma14, ulysses16, gr17 and others. — [TSPLIB95](http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/) †
- Network routing under link failures was run on Forte. — [arXiv:2602.04495](https://arxiv.org/abs/2602.04495)

**Scheduling**
- **JIT job-shop:** 20×3 machines with 1,300 variables, cut to 24–36-qubit sub-instances by freezing variables. — [arXiv:2510.26859v2](https://arxiv.org/html/2510.26859v2)
- OR-Library job-shop instances include ft06 (6×6, Fisher–Thompson), la01–la40, abz and orb. — [OR-Library jobshop](http://people.brunel.ac.uk/~mastjjb/jeb/orlib/jobshopinfo.html) †
- Taillard flow-shop and job-shop instances. — [Taillard benchmarks](http://mistic.heig-vd.ch/taillard/problemes.dir/ordonnancement.dir/ordonnancement.html) †
- Sports scheduling is a QOBLIB class. — [arXiv:2504.03832](https://arxiv.org/html/2504.03832v2)

**Aviation / aerospace**
- **IonQ-DESY flight gate:**
  - 2 flights × 4 gates (4 qubits) up to 9 × 4 (18 qubits) with log-linear encoding on Aria.
  - The goal is to cut passenger transfer walking time and gate idle time.
  - It is a reduced quadratic assignment problem.
  - Earlier QA work on the same problem used D-Wave and IBM.

  — [IonQ blog](https://ionq.com/blog/ionq-and-desy-tackle-the-gate-assignment-problem)
- **Earlier DLR flight-gate work on D-Wave.** — [Stollenwerk et al., arXiv:1811.09465](https://arxiv.org/abs/1811.09465) †
- **Airbus aircraft loading** (containers × slots, 12–28 qubits on Aria/Forte). — [arXiv:2504.01567](https://arxiv.org/abs/2504.01567)

**Finance**
- Portfolio optimization is a QOBLIB class. Large-scale PCE portfolio [2025] and a power-demand portfolio [2026] follow-up. — [arXiv:2511.21305](https://arxiv.org/pdf/2511.21305); [arXiv:2607.24722](https://arxiv.org/pdf/2607.24722)
- QAOA portfolio benchmarking (IBM) and early portfolio rebalancing with the Quantum Alternating Operator Ansatz (Rigetti/NASA). — [Brandhofer et al., QIP 22, 25 (2023), arXiv:2207.10555](https://arxiv.org/abs/2207.10555) †; [Hodson et al., arXiv:1911.05296](https://arxiv.org/abs/1911.05296) †
- JPMC constrained (Hamming-weight) XY-QAOA on trapped ions, up to 20 qubits. — [arXiv:2206.06290](https://arxiv.org/abs/2206.06290)

**Energy / power grids**
- Unit commitment and QAOA:
  - Koretsky et al. [2021]: classical solvers are effective below about 400 units; a quantum edge is only plausible at several hundred units. — [arXiv:2110.12624](https://arxiv.org/abs/2110.12624)
  - ADMM hybrid. — [arXiv:2201.03701](https://arxiv.org/pdf/2201.03701)
  - Topology-informed decomposition [2025]. — [arXiv:2503.20509](https://arxiv.org/html/2503.20509v1)
  - Warm-start hybrid with spinning reserve: a single-layer warm-start is within 5.1% of the reference classical solution. — [arXiv:2412.11312](https://export.arxiv.org/abs/2412.11312)
  - QuSO on the IEEE 57-bus system, up to 20 qubits, >1000 QAOA layers in simulation, SA baseline. — [arXiv:2505.16444](https://ar5iv.labs.arxiv.org/html/2505.16444)
- MATPOWER case files (case5, case9, case14, case24_ieee_rts, case30, case39, case57, case118) include generator cost curves and limits. — [matpower.org](https://matpower.org/) †

**Life sciences**
- **Protein folding on a tetrahedral lattice [2025]:** 10–12-residue peptides at 22, 27 and 33 qubits, with up to 5-body terms, on IonQ Forte. — [arXiv:2506.07866](https://arxiv.org/html/2506.07866v1)
- **Earlier resource-efficient lattice folding (IBM).** — [Robert et al., npj QI 7, 38 (2021), arXiv:1908.02163](https://arxiv.org/abs/1908.02163) †
- **Molecular docking as max-weighted-clique** on a binding-interaction graph, done with Gaussian boson sampling. — [Banchi et al., Sci. Adv. 6, eaax1950 (2020), arXiv:1902.00462](https://arxiv.org/abs/1902.00462) †

**Machine learning / data**
- **Feature selection HUBO on Gallstone and Spambase** (IonQ Forte, [2026]). — [arXiv:2604.26834](https://arxiv.org/abs/2604.26834)
- **UCI repository.** In scikit-learn: Wine (13 features), Breast Cancer Wisconsin (30 features), Spambase (57 features). — [UCI ML Repository](https://archive.ics.uci.edu/) †
- **Community detection / graph partitioning:** the SNAP collection; Zachary karate club (34 nodes) ships with networkx. — [SNAP](https://snap.stanford.edu/data/) †
- **Extractive summarization** as constrained QUBO (JPMC). — [arXiv:2206.06290](https://arxiv.org/abs/2206.06290)

**Other impact domains (datasets only, no quantum hardware precedent found)**
- Wildfire / disaster response: NASA FIRMS active-fire detections. — [FIRMS](https://firms.modaps.eosdis.nasa.gov/) †
- EV charging: Caltech ACN-Data (session-level charging data). — [ACN-Data](https://ev.caltech.edu/dataset) †
- Crop / agriculture planning: USDA NASS Quick Stats. — [Quick Stats](https://quickstats.nass.usda.gov/) †

### Inferences
**Domain-by-domain fit at 12–29 qubits (my sizing; IonQ 2Q counts are per QAOA layer with a dense cost graph unless noted)**

| Domain | Dataset | Formulation | Honest size | Qubits | 2Q/layer on IonQ | Subsampling that stays credible |
|---|---|---|---|---|---|---|
| Feature selection | UCI Wine (13 features); Breast Cancer (top-14 by MI) | mRMR QUBO: −relevance (MI with label) + redundancy (pairwise MI) + (Σx−k)² or XY mixer | n=12–14, k=4–5 | 12–14 | 66–91 dense | Prefilter by MI rank (state it). Evaluate the chosen subsets downstream with 5-fold CV accuracy. Brute force over C(n,k) gives the exact optimum. |
| Unit commitment | MATPOWER case24_ieee_rts or case30 generator data; demand from a real hourly load profile | u_g ∈ {0,1} per unit (× period); cost = no-load + linearized marginal; (Σ P_g^max u_g − D − R)² demand/reserve penalty; or "≥" via slack-free cost-shaping | 10–12 units × 1 period, or 6 units × 2 periods | 10–12 | 45–66 (penalty makes it dense) | Aggregate small units by type. Report that dispatch (continuous) is solved classically with `scipy.optimize.linprog`. |
| Portfolio with cardinality | Daily returns for 12–16 tickers (precompute μ, Σ offline into JSON) | min qΣ_ij x_i x_j − Σ μ_i x_i s.t. Σx = k; XY ring mixer from a greedy k-hot start | n=10–12, k=3–4 | 10–12 | 45–66 cost + 2n XY | Fix sector-diversified tickers; state the date window. Exact optimum by enumerating C(n,k) ≤ 495. |
| Gate/stand assignment | Real flight times from BTS on-time data (one airport, one hour); stand-distance matrix approximated | Quadratic assignment: transfer-passenger × distance + conflict penalties | 6 flights × 3–4 stands | one-hot 18–24; domain-wall 12–18; log 12 | one-hot dense; log gives 3–4-body terms (3–5 2Q each) | Encoding comparison *is* the contribution (extends IonQ-DESY). |
| Job-shop repair (LNS) | OR-Library ft06 or Taillard; incumbent from CP-SAT with a short time limit or greedy | Time-indexed one-hot on a freed window (2–3 operations × 4–5 slots) | 12–16 freed binaries | 12–16 | 30–80 | Free a window around a *heuristic* incumbent, not the optimum. Measure improvement probability. |
| Lattice protein folding | Short peptide (≤7–8 residues) | Tetrahedral-lattice HUBO (up to 5-body) | ≤8 residues | ~9–16 | HUBO pruned; budget tight | Mostly replicates Kipu/IBM; low novelty. |
| MaxCut / community detection | Karate club (34), SNAP or Gset subgraphs | Modularity / MaxCut QUBO with QAOA-in-QAOA decomposition | 3 × 12-node blocks + merge | 12 per block | ≤66 | Risky: looks "tutorial-level" and overlaps Qollab QAOA content. |
| VRP/TSP | CVRPLIB E-set or TSPLIB subsets | One-hot route | ≤5 cities | 16 | ≥48 penalty edges | Avoid as primary: already on Qollab, penalty-dominated. |

- **Credible subsampling rules.**
  - (a) Pre-register the rule: MI rank, top-k tickers by market cap, the first hour of the day.
  - (b) Release the subsample as JSON.
  - (c) Compute the exact optimum of the subsample by brute force.
  - (d) Show at least two subsample sizes, so a scaling plot exists.
  - (e) State plainly that the full-size real problem is solved classically in milliseconds, and that the project measures *sampler quality* and *resource scaling*.
- Feature selection, unit commitment and portfolio map to impact narratives judges understand (diagnostics, grid decarbonization, financial inclusion). They have IonQ-adjacent precedent ([arXiv:2604.26834](https://arxiv.org/abs/2604.26834); [arXiv:2206.06290](https://arxiv.org/abs/2206.06290)) without duplicating Qollab's logistics games.

### Gaps
- I did not verify the exact smallest instances in CVRPLIB Set E/P, or the current CVRPLIB URL.
- I found no 2024–2026 quantum-hardware papers on EV charging, wildfire response, crop planning, sports scheduling hardware runs or satellite scheduling. The table entries for those are formulations I propose, not precedents.
- I did not obtain the Gallstone dataset's feature count or the qubit-to-feature mapping in arXiv:2604.26834 from the abstract. Prior notes say 32 qubits.
- MATPOWER's case24_ieee_rts generator count and the Breast Cancer, Wine and Spambase feature counts are from memory (†).

---

## Q4. Classical baselines and honest benchmarking: solvers, metrics, QOBLIB, and the 2025–2026 advantage debate

### Takeaway
At 12–29 variables every problem is solved *exactly* by classical means: brute force up to ~25 vectorized, or MILP/CP. So the quantum contribution can only be framed as sample quality per shot, scaling trends, or resource and robustness comparisons.

The 2025–2026 literature makes three things non-negotiable for credibility:
- a strong tuned heuristic baseline (SA/PT/tabu, plus GW for MaxCut)
- an end-to-end time accounting or explicit equal-sample comparison
- an ablation that swaps the quantum sampler for a classical one in the same loop

A 2026 review found that 25 of 57 quantum-optimization studies had no classical baseline, and only 10 of 24 isolated the quantum contribution.

### Cited Findings

**Exact and heuristic baselines**
- **Goemans–Williamson SDP rounding** gives 0.87856 for MaxCut. Beating it is UGC-hard (Khot et al.). — [Goemans & Williamson, J. ACM 42(6):1115 (1995)](https://doi.org/10.1145/227683.227684) †
- **MQLib** implements and compares many MaxCut/QUBO heuristics (tabu, SA, Burer–Monteiro, and others) and shows no single heuristic dominates. It is the right source for a "strong heuristic" claim. — [MQLib](https://github.com/MQLib/MQLib) †
- **Parallel tempering with isoenergetic cluster moves (PT-ICM)** is considered "the top classical heuristic" for 2D spin glasses in the USC/D-Wave study. — [arXiv:2401.07184](https://arxiv.org/pdf/2401.07184)
- **GPU simulated bifurcation (SBM)** matched or beat quantum annealing scaling. — [arXiv:2505.22514](https://arxiv.org/pdf/2505.22514)
- **2026 HSQC benchmark.** SA, memetic tabu and EasySolve were weaker at equal time, while enhanced PT and GPU ABS3 "reach or surpass" the QPU result. This shows that baseline *choice* changes the conclusion. — [arXiv:2603.13607](https://arxiv.org/abs/2603.13607)
- **Kipu reference solvers** for their IonQ runs were brute force (protein), PySAT (MAX-SAT) and Gurobi (spin glass). — [arXiv:2506.07866](https://arxiv.org/html/2506.07866v1)
- **qiskit-optimization classical solvers.** It ships `NumPyMinimumEigensolver`-backed exact solving, `ScipyMilpOptimizer` (HiGHS via SciPy), `GoemansWilliamsonOptimizer` (needs cvxpy) and ADMM. — [qiskit-optimization docs](https://qiskit-community.github.io/qiskit-optimization/) †

**Metrics**
- **Time-to-solution:** TTS = t_run · ln(1−0.99) / ln(1−p_s), where p_s is the per-run success probability. — [Rønnow et al., Science 345, 420 (2014), arXiv:1401.2910](https://arxiv.org/abs/1401.2910) †
- **Time-to-ε** generalizes TTS to reaching within ε of the optimum. — [Munoz-Bauza & Lidar 2025](https://arxiv.org/pdf/2401.07184)
- **End-to-end runtime.** Tuziemski et al. propose end-to-end quantum runtime definitions (digital and analog) and a procedure for choosing strong classical baselines: "credible claims require careful time accounting, appropriate performance measures". — [arXiv:2510.06337](https://arxiv.org/abs/2510.06337)
- **What IonQ-hardware papers report:** P(opt) (ideal / QPU / mitigated), best-found energy against the known optimum, and the number of executions. — [arXiv:2510.26859v2](https://arxiv.org/html/2510.26859v2)

**Benchmark infrastructure and reviews**
- **QOBLIB.** Its stated purpose is a fair and systematic benchmarking effort toward quantum advantage, with model-independent instances. — [arXiv:2504.03832](https://arxiv.org/html/2504.03832v2)
- **Abbas et al.** "Challenges and opportunities in quantum optimization" is a broad multi-institution review (IBM-led) covering complexity, algorithms, benchmarking and hardware. — [Nat. Rev. Phys. 6, 718 (2024), arXiv:2312.02279](https://arxiv.org/abs/2312.02279) †
- **[Oct 2026] Lau review of 119 papers (67 coded):**
  - "25 of 57 studies include no classical baseline".
  - "the quantum contribution is fully isolated in 10 of 24 studies where an ablation applies".
  - "the median experiment uses 17 qubits".
  - It proposes an M0–M5 evidence hierarchy and finds no broadly convincing result at the top level.

  — [Lau, arXiv:2610.11759](https://arxiv.org/abs/2610.11759)

**2025–2026 advantage debate (timeline)**
- **May 2025:** Kipu/IBM claim runtime advantage (VENDOR). — [arXiv:2505.08663](https://arxiv.org/pdf/2505.08663)
- **May 2025:** USC/D-Wave PRL claims a scaling advantage in approximate optimization. — [arXiv:2401.07184](https://arxiv.org/pdf/2401.07184)
- **May 2025 → 2026:** Pawłowski et al. answer with GPU SBM scaling (INDEP). — [arXiv:2505.22514](https://arxiv.org/pdf/2505.22514)
- **Sep 2025:** D-Wave staff answer BF-DCQO (COMPETITOR). — [arXiv:2509.14358](https://arxiv.org/abs/2509.14358)
- **Oct 2025 → PR Applied 2026:** "runtime-based quantum advantage has not yet been demonstrated" (INDEP). — [arXiv:2510.06337](https://arxiv.org/abs/2510.06337)
- **Jan 2026:** trade press frames it as "Quantum Advantage Has Likely Been Achieved — The Debate Is Over What Counts". This is opinion and was not fetched. — [TQI](https://thequantuminsider.com/2026/01/12/quantum-advantage-has-likely-been-achieved-the-debate-is-over-what-counts/)
- **Mar 2026:** Kipu/ZIB/IBM end-to-end HSQC report "competitive", with the best classical solvers matching or surpassing it. — [arXiv:2603.13607](https://arxiv.org/abs/2603.13607)
- **Apr 2026:** a classical mean-field algorithm beats all quantum results on binary paint shop. — [arXiv:2604.00607](https://arxiv.org/html/2604.00607v2)
- **Ongoing:** IBM's framing is that groups "hypothesize" advantage and the community validates or falsifies it. — [IBM blog](https://www.ibm.com/quantum/blog/quantum-advantage-era)

### Inferences
**Baseline stack for the build (precompute offline and ship as JSON ≤2 MB)**
1. **Exact.**
   - Brute force. 2^20 ≈ 1M states is fine in browser numpy, vectorized as x·Q·x over chunks. Precompute 2^25 offline.
   - For constrained problems, enumerate only feasible states, e.g. C(16,5) = 4,368.
   - `scipy.optimize.milp` (HiGHS) on the linearized QUBO for an independent check.
2. **Heuristics.**
   - Greedy (problem-specific, e.g. mRMR forward selection, priority-list unit commitment).
   - Simulated annealing (≥ the same number of energy evaluations as quantum shots, and also at a 100× budget).
   - Tabu search (1-flip).
   - Parallel tempering.
   - For MaxCut: GW (offline cvxpy plus SCS/Clarabel) and Burer–Monteiro in numpy.
3. **Domain baselines.** SelectKBest/mRMR/PCA for feature selection; MILP unit commitment; mean-variance with cardinality via enumeration.
4. **"Classical-null" ablation.** Use the same iterative loop (warm-start / bias update / post-processing) with the quantum sampler replaced by (a) uniform random, (b) product-state sampling from the same bias fields, and (c) a short SA run. This answers the BF-Null critique directly.

**cvxpy-base caveat (needs checking in Pyodide).** `cvxpy-base` ships without bundled solvers. A GW SDP may not solve in-browser unless SCS or Clarabel is importable, so precompute GW offline or write a numpy Burer–Monteiro rank-2/3 relaxation.

**Metrics to report** (all are cheap from counts):
- P(opt) and P(within 1% / 5%)
- feasibility rate
- approximation ratio of the best-of-N and of the mean
- TTS99 in *shots*, not seconds, because hardware wall-clock is dominated by queue and 650–950 µs per 2Q gate per prior notes
- the energy-quantile curve (CVaR_α for α ∈ {0.01, 0.1, 0.5})
- all of the above at equal sample counts against the random, product-state and SA baselines

**Honesty statements to put on the slide.** "All instances are exactly solvable classically; we do not claim advantage." "We report raw / mitigated / post-processed separately." "Ablation: quantum sampler vs classical sampler in the same loop."

### Gaps
- I did not fetch Abbas et al. 2024 this session, so specific claims from it (e.g. its recommended benchmarking protocol) are not quoted.
- I did not confirm whether QOBLIB contains instances small enough (≤29 binaries) for in-browser use. It is described as "intractable", so most instances are likely far larger.
- I found no source on SCS or Clarabel availability in Pyodide.

---

## Q5. What a "measurable quantum step" can honestly be in 48 h, with 3–5 concrete designs (qubits, 2Q gates, expected results at ~0.5% 2Q error)

### Takeaway
In 48 hours the honest, measurable quantum step is **sample quality at equal shots** (P(opt), feasibility, approximation-ratio quantiles) from a **fixed-schedule or warm-started QAOA-family sampler**, measured in three settings:
- ideal simulation
- the IonQ Forte noise model
- one IonQ hardware job

This sits against random, product-state and SA samplers in the same loop, plus a resource comparison: IonQ all-to-all versus heavy-hex.

At 0.5% 2Q error, a 66-gate circuit keeps a global-fidelity proxy of about 0.72 and a 100-gate circuit about 0.61. So 12–14-variable dense QUBOs at p=1, or sparse/XY-constrained ones at p=2, should keep a clear signal, consistent with Airbus's ~70% P(opt) at 12 qubits on Aria/Forte.

### Cited Findings
- **Hardware calibration points:**
  - Airbus multi-angle QAOA, 12 qubits, ~70% P(opt) with 1000 shots. — [arXiv:2504.01567](https://arxiv.org/abs/2504.01567)
  - Iterative-QAOA, 32 qubits and 780 2Q gates: raw P(opt) 0.7%, mitigated 69%. — [arXiv:2510.26859v2](https://arxiv.org/html/2510.26859v2)
  - Kipu on Forte: device DRB fidelity 99.3–99.5%; 2,000 shots per iteration; optimum reached with SA post-processing. — [arXiv:2506.07866](https://arxiv.org/html/2506.07866v1)
  - Routing on Forte: best solution seen only 2–16 times. — [arXiv:2602.04495](https://arxiv.org/abs/2602.04495)
- **LR-QAOA success scaling.** P(x*) ~ 2^(−η(p)N+C), so the exponent η is a measurable "scaling of success probability vs n" quantity. — [arXiv:2405.09169](https://arxiv.org/abs/2405.09169)
- **Fault-tolerant resource framing.** Compilation estimates of quantum heuristics (amplitude amplification and annealing variants) on surface-code hardware conclude that quadratic speedups are not enough for practical advantage given error-correction overheads. — [Sanders et al., PRX Quantum 1, 020312 (2020), arXiv:2007.07391](https://arxiv.org/abs/2007.07391) †; [Babbush et al., PRX Quantum 2, 010103 (2021), "Focus beyond quadratic speedups…", arXiv:2011.04149](https://arxiv.org/abs/2011.04149) †
- **Connectivity matters.** Non-native problems degrade on planar hardware because of routing overhead. — [Harrigan et al. 2021](https://arxiv.org/abs/2004.04197) †
- **Unit commitment needs a scale caveat.** Classical solvers are effective below about 400 units. — [arXiv:2110.12624](https://arxiv.org/abs/2110.12624)

### Inferences

**Noise rule of thumb (my calculation; global-depolarizing proxy, single-qubit and readout error ignored)**
- F(N₂q) = (1−0.005)^N₂q:

  | 2Q gates | F |
  |---|---|
  | 36 | 0.835 |
  | 45 | 0.798 |
  | 66 | 0.718 |
  | 78 | 0.676 |
  | 91 | 0.634 |
  | 100 | 0.606 |
  | 132 | 0.516 |
  | 198 | 0.371 |

  At a more pessimistic 0.7%: 66 → 0.63 and 100 → 0.50.
- P_noisy(opt) ≈ F·P_ideal(opt) + (1−F)·2^(−n). This is a lower-bound-ish proxy, because real noise concentrates near low-Hamming-distance states.
- *Illustrative:* n=12, 66 gates, P_ideal = 0.30 → P_noisy ≈ 0.22 → TTS99 ≈ 19 shots, versus 18,861 shots for uniform random (2^−12). For n=16, 96 gates, P_ideal = 0.10 → ≈0.062 → TTS99 ≈ 72 shots.
- Verify every number on the qiskit-ionq Forte noise model before quoting.

**IonQ vs heavy-hex (measurable, cheap, credible)**
- A complete-graph cost layer is n(n−1)/2 native ZZ on IonQ: 66 at n=12, 91 at n=14, 120 at n=16.
- A linear-chain swap network needs roughly 3·n(n−1)/2 CNOTs: 198, 273 and 360 respectively, about 3×. Heavy-hex is similar or worse after transpilation.
- Measure it directly: `transpile` against an all-to-all coupling map with basis {rzz, r} versus an IBM heavy-hex fake backend coupling map (CZ/ECR basis) at optimization_level=3. Plot 2Q count and estimated fidelity against n.

**Concrete designs (ranked)**

**D1. "Quantum mRMR": feature selection for medical diagnosis (recommended)**
- **Data:** UCI Breast Cancer Wisconsin (sklearn), prefiltered to the top-12 or top-14 features by mutual information (MI). Alternatively Wine (13 features, all used).
- **Formulation:** QUBO with linear terms −MI(feature, label) and quadratic terms +λ·MI(f_i, f_j) for redundancy. Use k=4 or 5 features, with a Hamming-weight constraint via an XY ring mixer from a greedy-mRMR k-hot start. That gives no penalty clique and 100% feasibility by construction.
  - Optional 3-body conditional-MI terms (2k−3 = 3 2Q gates each) are a cheap nod to Kipu's HUBO.
- **Resources:**
  - n=12: cost 66 + XY ring 24 = **90 2Q at p=1**.
  - n=10: 45 + 20 = 65 at p=1, or 130 at p=2.
  - A sparse variant keeps only the top-30 redundancy pairs: 30 + 24 = 54 per layer, so p=2 ≈ 108.
- **Quantum step:** P(optimal subset) and P(top-1% subsets) at 1,000 shots in four settings (ideal, Forte noise model, one hardware job, against random k-hot, SA and greedy).
  - Downstream: 5-fold CV accuracy of the best sampled subset versus SelectKBest, greedy mRMR and the exact best of C(12,4) = 495 subsets.
  - Ablation: warm-start bias update with a classical product-state sampler.
- **Expected:** F ≈ 0.63 at 90 2Q gates. The feasible space is 495 states, so random P(opt) ≈ 0.2%. A p=1 XY-QAOA with transferred angles should give P(opt) of a few percent to ~10%+ ideal and 0.6× that on noise. That is still more than 10× random, with 100% feasibility; verify in simulation.
- **Impact:** cheaper diagnostic panels.
- **Novelty vs Qollab:** not logistics; constrained XY mixer on all-to-all hardware.

**D2. Unit commitment on a real grid case (hybrid: quantum commitment, classical dispatch)**
- **Data:** MATPOWER generator data (e.g. case24_ieee_rts or case30), aggregated to 10–12 units, with a real hourly demand profile.
- **Quantum part:** binary u_g. Cost: no-load cost plus a linearized marginal cost, plus a demand-coverage penalty (Σ P_g^max u_g − D − R)². The penalty makes the graph dense: 45 (n=10) or 66 (n=12) 2Q at p=1.
- **Classical part:** for each sampled commitment, `scipy.optimize.linprog` economic dispatch gives the true cost. Infeasible samples are flagged.
- **Measurable step:**
  - Distribution of true operating cost over 1,000 samples (QAOA vs random vs priority-list greedy vs SA).
  - Penalty-sweep curve of feasibility against cost.
  - Exact optimum via 2^12 enumeration plus LP.
- **Expected:** F ≈ 0.72 at 66 2Q. A good penalty choice should give 30–60% feasible samples and a clear low-cost tail. Report honestly that MILP solves this in milliseconds, and cite the ~400-unit crossover argument.
- **Risk:** quadratic penalty tuning; the auto-penalty falls back to 1e5 with fractional MW values.

**D3. Cardinality-constrained portfolio: penalty vs XY-mixer vs warm-start, on IonQ vs heavy-hex**
- **Data:** 10–12 tickers with real daily returns over a stated window (μ, Σ precomputed to JSON); k = 3–4.
- **Resources:** cost layer is dense from Σ, 45–66 2Q, plus XY ring 2n = 20–24, so 65–90 per layer at p=1. Penalty version: (Σx−k)² adds no new edges, because Σ is already dense, but it changes the landscape.
- **Measurable step:** a 3×2 grid of {X-mixer + penalty, XY-mixer, warm-start (Egger)} × {IonQ all-to-all, heavy-hex transpiled}. It reports feasibility, approximation ratio, P(opt), 2Q count and estimated fidelity.
- **Expected:** XY gives 100% feasibility versus roughly 10–40% with penalties. IonQ needs about 3× fewer 2Q gates than heavy-hex at n=12.
- **Precedent:** JPMC XY-QAOA on trapped ions at 20 qubits.
- **Risk:** finance is heavily explored. Novelty comes from the rigorous grid and the hardware-connectivity analysis.

**D4. Stand/gate assignment: an encoding study extending IonQ-DESY**
- **Data:** one hour of real arrivals and departures at one airport (BTS on-time data, †), 6 flights × 3–4 stands, with a stand-distance matrix and transfer-passenger weights. Approximate the matrix and state it.
- **Encodings compared:**
  - one-hot: 18–24 qubits, dense penalties
  - domain-wall: 12–18 qubits
  - log: 12 qubits, up to 4-body terms, 5 native 2Q each, plus invalid-code handling when stands aren't 2^k
- **Measurable step:** a table of qubits, 2Q gates, feasibility, P(opt) and noise-model P(opt) for each encoding at the same instance. This answers whether log encoding still wins once IonQ's 2k−3 HUBO gate cost is counted.
- **Expected:** log and domain-wall fit the 100-gate budget at p=1 only for 4–5 flights. One-hot exceeds it.
- **Strength:** novel and directly about IonQ's all-to-all and native ZZ. **Risk:** the data has to be partly synthetic.

**D5. Job-shop repair as a quantum LNS move (scheduling, real benchmark)**
- **Data:** OR-Library ft06 (6×6) or a small Taillard instance. Incumbent from greedy dispatching or CP-SAT with a 1 s limit (offline).
- **Quantum step:** free a window of 2–3 operations × 4–5 time slots (12–15 binaries), freeze the rest *to the incumbent, not the optimum*, and sample with LR-QAOA or Iterative-QAOA using Δβ = Δγ ≈ 0.17. Do 9 iterations on the noise model and the final one on hardware.
  - Sparse one-hot plus precedence couplings give about 30–80 2Q per layer, so p=1–2.
- **Measurable step:** the probability that one quantum LNS move improves makespan, against a random or SA move on the same window and a classical-null bias loop.
- **Expected:** at 12 qubits and ≤80 2Q gates (F ≥ 0.67), the in-window optimum should appear in most 1,000-shot batches.
- **Strength:** honest framing of the IonQ JSSP paper's "freezing" trick. **Risk:** time-indexed formulation bugs.

**Overall build recommendations**
- Only the final circuit goes to hardware, because IonQ allows one job per run.
- Angles come from small-instance transfer or LR ramps, with no on-hardware variational loop.
- Use the IonQ Forte noise model at n ≤ 16 for the main curves, and 20–24 qubits in ideal statevector for scaling-exponent plots.
- Include a fault-tolerant "what it would take" slide citing Sanders 2020 and Babbush 2021: quadratic speedups don't survive QEC overhead, so the case rests on heuristic sampling quality, not proven speedup.

### Gaps
- I did not simulate the projected P(opt) values for D1–D5 in this session. The numbers are a rule-of-thumb noise proxy combined with illustrative ideal probabilities, and must be checked on the Forte noise model.
- Whether IonQ "one job" can contain multiple circuits (a multicircuit job), which would allow a full Iterative-QAOA loop on hardware, was not verified.
- I found no published IonQ-hardware results for XY-mixer QAOA specifically (JPMC's trapped-ion run used a different vendor per prior knowledge). So D1/D3 hardware expectations rest on the noise-model proxy.
- The heavy-hex 2Q counts here are estimated from swap-network theory, not from a transpile run.
