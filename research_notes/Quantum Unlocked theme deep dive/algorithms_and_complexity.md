# Quantum Algorithms & Quantum Complexity: Knowledge Base for a Teaching Tool (as of Oct 2026)

Scope: core primitives, advanced frameworks (QSP/QSVT etc.), advantage experiments and the arguments about whether they hold up, complexity theory, teaching angles, and concrete demos that fit the Qollab x IonQ "Quantum Unlocked" constraints (Qiskit 2.x in Pyodide, at most 29 simulated qubits with IonQ noise, no dynamic circuits, one job per run, native GPi/GPi2/ZZ(theta), all-to-all connectivity, a budget of about 100 two-qubit gates).

Tag convention: **[NEW 2024]**, **[NEW 2025]** and **[NEW 2026]** mark recent results. Everything else is classic material. Fidelity rule of thumb used throughout: with p2 = 0.5% error per two-qubit (2Q) gate, circuit success is roughly F ~ 0.995^N2Q. That gives F(20) ~ 0.90, F(40) ~ 0.82, F(60) ~ 0.74, F(80) ~ 0.67, F(100) ~ 0.61. This is my own arithmetic and ignores single-qubit, SPAM and crosstalk errors.

---

## Q1. Core primitives and why they work (interference, kickback, DJ/BV/Simon, QFT, QPE and its feed-forward-free variants, Shor, Grover/AA, amplitude estimation, counting)

### Takeaway
Every core algorithm uses one pattern. A query writes information into **phases** (phase kickback). A structured unitary (Hadamard transform or QFT) then makes the paths to wrong answers **interfere destructively**. Speedups come from interference, never from "reading out all branches". For a tool that has to fit the hackathon constraints, the most useful (and least-taught) facts are these:
- Phase estimation and amplitude estimation do **not** need the QFT or mid-circuit feed-forward. Non-adaptive single-ancilla schedules (Kitaev/robust phase estimation, QCELS, MLAE) reach Heisenberg-limited scaling and can all be batched into one job.
- Grover's success amplitude is literally a Chebyshev polynomial T_{2k+1}(sqrt p). That ties search, its optimality proof and QSP into one picture.

### Cited Findings

#### Interference & phase kickback
- Phase kickback: if U|u> = e^{i phi}|u>, then controlled-U maps (|0>+|1>)|u> to (|0>+e^{i phi}|1>)|u>. The eigenphase moves onto the control, which is the unifying view of Deutsch-Jozsa, Simon, Shor and phase estimation — [Cleve, Ekert, Macchiavello, Mosca 1998, "Quantum algorithms revisited"](https://arxiv.org/abs/quant-ph/9708016)
- The standard oracle trick O_f|x>|-> = (-1)^{f(x)}|x>|-> turns a bit oracle into a phase oracle — [Cleve et al. 1998](https://arxiv.org/abs/quant-ph/9708016); [de Wolf, Quantum Computing Lecture Notes (arXiv 2019, updated)](https://arxiv.org/abs/1907.09415)
- Sum-over-paths view: each output amplitude of a circuit of H, phase and Toffoli gates is an exponential sum over classical paths (a polynomial over Z2), so cancellation between paths is what carries the computation — [Dawson et al. 2004, "Quantum computing and polynomial equations over Z2"](https://arxiv.org/abs/quant-ph/0408129)
- Entanglement is not sufficient for speedup: Clifford circuits with stabilizer inputs are classically simulable (Gottesman-Knill) — [Gottesman 1998](https://arxiv.org/abs/quant-ph/9807006). Pure-state computations that stay only slightly entangled are also classically simulable — [Jozsa & Linden 2002](https://arxiv.org/abs/quant-ph/0201143)

#### Deutsch-Jozsa, Bernstein-Vazirani, Simon
- Deutsch-Jozsa (1992) decides "constant vs balanced" with 1 query. A deterministic classical algorithm needs 2^{n-1}+1 queries, but a bounded-error randomized classical algorithm needs only O(1). The separation holds **only against exact/deterministic** algorithms, which is a frequent teaching error — [Deutsch & Jozsa, Proc. R. Soc. A 439:553 (1992)](https://doi.org/10.1098/rspa.1992.0167); [de Wolf notes](https://arxiv.org/abs/1907.09415)
- Bernstein-Vazirani: one query to f(x) = s·x mod 2 recovers s, against n classical queries. That is only a polynomial gap. The recursive version gives a superpolynomial oracle separation — [Bernstein & Vazirani, SIAM J. Comput. 26(5) 1997](https://doi.org/10.1137/S0097539796300921)
- Simon's problem: f(x) = f(y) iff x XOR y is in {0, s}. Each quantum run returns a uniformly random y with y·s = 0, so O(n) queries plus Gaussian elimination over GF(2) finds s. Classical algorithms need Omega(2^{n/2}) queries (birthday bound). This was the first exponential oracle separation and directly inspired Shor — [Simon, SIAM J. Comput. 26(5) 1997](https://doi.org/10.1137/S0097539796298637)

#### QFT
- QFT_N |j> = N^{-1/2} sum_k e^{2 pi i jk/N}|k>. Product form: |j> maps to the tensor product over l of (|0> + e^{2 pi i 0.j_{n-l+1}...j_n}|1>)/sqrt2. Each output qubit is a "phase wheel" turning at a binary-scaled rate. The circuit uses n H gates, n(n-1)/2 controlled-phase gates and floor(n/2) SWAPs, and the SWAPs can be removed by relabelling — [Nielsen & Chuang §5.1; de Wolf notes ch. 4](https://arxiv.org/abs/1907.09415)
- Approximate QFT: dropping controlled rotations with angle below pi/2^b gives O(n·b) gates with error O(n·2^{-b}), so b ~ log n is enough — [Coppersmith 1994 (posted 2002)](https://arxiv.org/abs/quant-ph/0201067)
- The QFT does not compute a classical FFT faster in any usable sense, because the Fourier coefficients sit in amplitudes and cannot be read out — [Aaronson, "Introduction to Quantum Information Science" lecture notes](https://www.scottaaronson.com/qclec.pdf)

#### Quantum phase estimation (QPE) and feed-forward-free variants
- Textbook QPE with t ancillas returns the best t-bit approximation of phi with probability at least 4/pi^2 ~ 0.405. Using t = n + ceil(log2(2 + 1/(2 epsilon))) ancillas gives n correct bits with probability at least 1 - epsilon — [Nielsen & Chuang §5.2; de Wolf notes](https://arxiv.org/abs/1907.09415)
- Kitaev's original phase estimation uses **one ancilla per Hadamard test**. Each test measures cos or sin of 2^j·2 pi phi, and the bits are combined classically. No QFT is needed — [Kitaev 1995](https://arxiv.org/abs/quant-ph/9511026)
- Iterative QPE (IPEA) measures one bit at a time, but the correction phase applied in round k depends on the earlier bits, so it is **adaptive**. That needs feed-forward between rounds, or sequential jobs — [Dobšíček et al. 2007](https://arxiv.org/abs/quant-ph/0610214)
- Heisenberg-limited phase estimation **without adaptive measurements** has been shown experimentally, by repeating each power 2^j a carefully chosen number of times — [Higgins et al. 2009, NJP](https://arxiv.org/abs/0809.3308)
- Robust phase estimation (RPE) is non-adaptive. It uses Hadamard-test data at depths 2^j and reaches Heisenberg scaling, with an error tolerance per generation — [Kimmel, Low, Yoder, PRA 92, 062315 (2015)](https://arxiv.org/abs/1502.02677)
- Bayesian phase estimation (particle-filter/rejection-filter posterior updates) is efficient and robust to depolarizing noise — [Wiebe & Granade, PRL 117, 010503 (2016)](https://arxiv.org/abs/1508.00869)
- Early-fault-tolerant ground-state energy estimation: Heisenberg-limited estimation with a single ancilla and classical post-processing — [Lin & Tong, PRX Quantum 3, 010318 (2022)](https://arxiv.org/abs/2102.11340). QCELS (quantum complex exponential least squares) needs much shorter maximal circuit depth — [Ding & Lin, PRX Quantum 4, 020331 (2023)](https://arxiv.org/abs/2211.11973)
- Warning case: "compiled" demos that replace controlled-U^{2^j} with a precomputed phase gate effectively assume the answer. Smolin, Smith and Vargo showed that such simplifications can "factor" any number — [Smolin, Smith, Vargo, Nature 499, 163 (2013)](https://arxiv.org/abs/1301.7007)

#### Shor's algorithm and resource estimates
- Order finding: U_a|y> = |a·y mod N> has eigenphases s/r. QPE with t ~ 2n+1 bits followed by continued fractions recovers s/r whenever |k/2^t - s/r| <= 1/(2r^2), because s/r is then a convergent of k/2^t. Factoring reduces to order finding: for random a, r is even and a^{r/2} is not -1 mod N with probability at least 1/2 — [Shor 1995/1997](https://arxiv.org/abs/quant-ph/9508027); [Nielsen & Chuang §5.3, Thm 5.1]
- Gidney & Ekerå (preprint 2019, Quantum 2021): RSA-2048 in about 8 hours with about 20 million noisy qubits, assuming 0.1% error — [arXiv:1905.09749](https://arxiv.org/abs/1905.09749)
- **[NEW 2025]** Gidney (21 May 2025): RSA-2048 with **fewer than 1 million noisy qubits in under a week**. Assumptions: 0.1% uniform gate error, 1 µs surface-code cycle, 10 µs reaction time, square grid with nearest-neighbour connections. The savings come from approximate residue arithmetic (Chevignard-Fouque-Schrottenloher 2024), yoked surface codes for idle qubits, and magic state cultivation. Toffoli count is more than 100x lower than the 2024 approximate-arithmetic approach — [arXiv:2505.15917](https://arxiv.org/abs/2505.15917). Secondary coverage puts RSA-2048 at about 6.5 billion Toffolis — [The Quantum Insider, 31 Mar 2026](https://thequantuminsider.com/2026/03/31/q-day-just-got-closer-three-papers-in-three-months-are-rewriting-the-quantum-threat-timeline/)
- **[NEW 2026]** Iceberg Quantum's "Pinnacle" architecture (Feb 2026, preprint) claims RSA-2048 with **fewer than 100,000 physical qubits** using qLDPC codes. It assumes non-local connectivity and decoder reaction-time requirements that have not been demonstrated — [TQI, 31 Mar 2026](https://thequantuminsider.com/2026/03/31/q-day-just-got-closer-three-papers-in-three-months-are-rewriting-the-quantum-threat-timeline/); [TQI summary of Gidney 2025 and follow-ups](https://thequantuminsider.com/2025/05/24/google-researcher-lowers-quantum-bar-to-crack-rsa-encryption/)
- **[NEW 2026]** Google Quantum AI whitepaper (31 Mar 2026, co-authors include Justin Drake and Dan Boneh): ECDLP-256 (the elliptic-curve problem behind Bitcoin and Ethereum signatures) with **fewer than 500,000 physical qubits**, about 70-90 million Toffolis, and a runtime of minutes. The circuits were withheld and a zero-knowledge proof was published instead. The previous best was Litinski 2023 at about 9 million qubits — [TQI, 31 Mar 2026](https://thequantuminsider.com/2026/03/31/q-day-just-got-closer-three-papers-in-three-months-are-rewriting-the-quantum-threat-timeline/)
- A March 2026 neutral-atom study proposed as few as about 10,000 atoms, at the cost of much longer runtimes. It is a preprint and not directly comparable to the others — [search summary of 2026 follow-ups via TQI coverage](https://thequantuminsider.com/2026/03/31/q-day-just-got-closer-three-papers-in-three-months-are-rewriting-the-quantum-threat-timeline/)

#### Grover search, amplitude amplification, optimality, fixed point
- Geometry: |psi> = sin(theta)|good> + cos(theta)|bad> with sin^2(theta) = M/N. The Grover iterate G = -S_psi S_chi is a rotation by 2 theta in the 2D plane spanned by |good> and |bad>. After k iterations the good amplitude is sin((2k+1) theta), so k ~ (pi/4) sqrt(N/M) is optimal — [Grover 1996](https://arxiv.org/abs/quant-ph/9605043); [Nielsen & Chuang §6.1]
- Amplitude amplification generalises this to any state-preparation unitary A with success probability a: O(1/sqrt(a)) uses of A — [Brassard, Høyer, Mosca, Tapp 2000/2002](https://arxiv.org/abs/quant-ph/0005055)
- Optimality: any quantum algorithm needs Omega(sqrt N) queries (hybrid argument). Relative to a random oracle, NP is not contained in BQP with probability 1 — [Bennett, Bernstein, Brassard, Vazirani 1997](https://arxiv.org/abs/quant-ph/9701001). Grover's iteration count is exactly optimal — [Zalka 1999](https://arxiv.org/abs/quant-ph/9711070)
- Polynomial method: a T-query algorithm's acceptance probability is a polynomial of degree at most 2T in the input bits. This gives lower bounds such as Omega(sqrt N) for OR — [Beals, Buhrman, Cleve, Mosca, de Wolf 1998](https://arxiv.org/abs/quant-ph/9802049)
- Overshoot ("soufflé problem"): with M unknown, too many iterations rotates past the target. Grover's pi/3 fixed-point search removes the oscillation but loses the quadratic speedup — [Grover 2005, PRL 95, 150501](https://arxiv.org/abs/quant-ph/0503205)
- Fixed-point amplitude amplification with **optimal** query scaling: L >= log(2/delta)/sqrt(w) queries guarantee success at least 1 - delta^2 for every unknown success probability lambda >= w. The phases come from a Chebyshev-polynomial construction — [Yoder, Low, Chuang, PRL 113, 210501 (2014)](https://arxiv.org/abs/1409.3305)
- Quadratic speedups (Grover-type) are unlikely to give practical advantage on early fault-tolerant machines, because error-correction overheads swamp them — [Babbush et al., PRX Quantum 2, 010103 (2021), "Focus beyond quadratic speedups"](https://arxiv.org/abs/2011.04149); [Hoefler, Häner, Troyer, CACM 2023](https://arxiv.org/abs/2307.00523)

#### Amplitude estimation (QAE), QPE-free variants, quantum counting
- Canonical QAE (QPE on Q = -A S_0 A^-1 S_chi) with M applications of Q gives |a_est - a| <= 2 pi sqrt(a(1-a))/M + pi^2/M^2 with probability at least 8/pi^2. The error scales as 1/M ("Heisenberg"), against 1/sqrt(M) for Monte Carlo — [Brassard et al. 2002](https://arxiv.org/abs/quant-ph/0005055)
- Quantum counting: QPE on the Grover operator, whose eigenphases are ±2 theta, estimates M = N sin^2(theta) — [Brassard, Høyer, Tapp 1998](https://arxiv.org/abs/quant-ph/9805082). Lower bounds for approximate counting — [Nayak & Wu 1999](https://arxiv.org/abs/quant-ph/9804066)
- MLAE (maximum-likelihood AE): run Q^{m_k} A|0> for a schedule m_k (e.g. 0, 1, 2, 4, ...), measure, and maximise the likelihood. There is no QPE and no controlled-Q. Each circuit has P(good) = sin^2((2m_k+1) theta), and the Fisher information grows like (2m_k+1)^2, which gives near-Heisenberg scaling — [Suzuki et al., QIP 19, 75 (2020)](https://arxiv.org/abs/1904.10246)
- MLAE on noisy hardware: model depolarizing decay of the signal in the likelihood — [Tanaka et al. 2021, "Amplitude estimation via maximum likelihood on noisy quantum computer"](https://arxiv.org/abs/2006.16223)
- IQAE (iterative QAE): no QPE, provable epsilon-accuracy with O((1/epsilon) log(...)) queries, but the choice of next k is **adaptive** (classical, between circuits) — [Grinko, Gacon, Zoufal, Woerner, npj QI 7, 52 (2021)](https://arxiv.org/abs/1912.05559)
- Low-depth / power-law AE: a dial between Monte Carlo (depth 1) and full QAE trades maximum circuit depth for query count, which matters on noisy devices — [Giurgica-Tiron et al., Quantum 6, 745 (2022)](https://arxiv.org/abs/2012.03348)

### Inferences
- **Grover = Chebyshev (derivation).** Write a = sin(theta) = cos(pi/2 - theta). Then T_{2k+1}(a) = cos((2k+1)(pi/2 - theta)) = (-1)^k sin((2k+1) theta). So k Grover iterations output the odd Chebyshev polynomial T_{2k+1} of the initial amplitude, which is a QSP polynomial (see Q2). By Bernstein's inequality, |P'(x)| <= d/sqrt(1-x^2), any bounded degree-d polynomial has |P(1/sqrt N)| <= d/sqrt N. So reaching success probability Omega(1) **within QSP-type algorithms** needs d = Omega(sqrt N). This is a one-line, visual version of the BBBV/polynomial-method bound that learners can explore with sliders. It is not a proof of the general BBBV theorem, which covers all algorithms.
- **Non-adaptivity is the key property under "no dynamic circuits, one job".** Kitaev/RPE/QCELS (for phase) and MLAE with a fixed schedule (for amplitude) are fully non-adaptive: every circuit is known in advance. IPEA and IQAE are adaptive between circuits, so they need multiple jobs. Canonical QPE/QAE use the QFT plus many controlled-U gates and are the most noise-fragile.
- **Parallel-register batching (my suggestion).** With all-to-all connectivity and up to 29 qubits, several independent small circuits can run side by side on disjoint qubits in one circuit. Examples: 14 two-qubit Hadamard tests at different powers, or about 7 four-qubit MLAE circuits with different m_k. Measuring all qubits then delivers a whole non-adaptive schedule in **one job**. This needs checking against crosstalk in the IonQ noise model.
- Deutsch-Jozsa should be taught together with its caveat (no advantage over randomized algorithms). Simon is the under-taught bridge to Shor and to the hidden subgroup problem.

### Gaps
- I did not verify the logical-qubit count in Gidney 2025; the abstract does not state it, and I remember it as roughly 1,400 logical qubits but did not confirm this. I also did not find arXiv IDs for the Iceberg Pinnacle and Google ECDLP 2026 papers; only secondary coverage (TQI) was available.
- I did not verify current IonQ single-qubit and SPAM error rates, which matter for the single-qubit-heavy demos.

---

## Q2. Advanced frameworks: block encodings, LCU, qubitization, QSP/QSVT, HHL, Hamiltonian simulation, quantum walks, AQC, QAOA, VQE, barren plateaus, QML and dequantization, kernels, classical shadows, DQI, Regev, Yamakawa-Zhandry

### Takeaway
QSP/QSVT is the cleanest "grand unification" for teaching. One single-qubit circuit family with different phase lists implements search, phase estimation, Hamiltonian simulation and matrix inversion, as polynomials of the "signal". Variational and QML methods are now best taught through their critiques:
- barren plateaus and their Lie-algebraic theory;
- **[NEW 2025]** the Cerezo et al. perspective that provable absence of barren plateaus often implies classical simulability;
- Tang's dequantization;
- kernel concentration.

The frontier algorithms (DQI 2024-25, Regev 2023, Yamakawa-Zhandry 2022) all lean on algebraic structure plus the QFT. The 2025-2026 follow-ups show DQI's advantage needs that structure.

### Cited Findings

#### QSP (single-qubit "signal processing")
- QSP origin: composite-pulse sequences as polynomial transformations — [Low, Yoder, Chuang, PRX 6, 041067 (2016)](https://arxiv.org/abs/1603.03996). Optimal Hamiltonian simulation by QSP — [Low & Chuang, PRL 118, 010501 (2017)](https://arxiv.org/abs/1606.02685)
- QSP theorem (Wx convention): W(a) = e^{i arccos(a) X} = [[a, i sqrt(1-a^2)], [i sqrt(1-a^2), a]], and U_Phi = e^{i phi_0 Z} times the product over k=1..d of W(a) e^{i phi_k Z}. Phases Phi in R^{d+1} exist with U_Phi = [[P, iQ sqrt(1-a^2)], [iQ* sqrt(1-a^2), P*]] **iff** (i) deg P <= d and deg Q <= d-1; (ii) P has parity d mod 2 and Q has parity (d-1) mod 2; (iii) |P|^2 + (1-a^2)|Q|^2 = 1 on [-1, 1]. Any real polynomial f with parity d mod 2 and |f| <= 1 on [-1, 1] can be reached as Re P (or as a <+|·|+> matrix element) — [Martyn, Rossi, Tan, Chuang, "Grand Unification of Quantum Algorithms", PRX Quantum 2, 040203 (2021)](https://arxiv.org/abs/2105.02859)
- In the unification paper, search, phase estimation, Hamiltonian simulation, matrix inversion and eigenvalue thresholding all become polynomial choices: sign function, Chebyshev polynomials, the Jacobi-Anger expansion of e^{-i tau x}, and 1/x on [1/kappa, 1] — [Martyn et al. 2021](https://arxiv.org/abs/2105.02859)
- Phase-factor ("angle") finding:
  - Double-precision optimisation handles degree above 10,000 at error below 1e-12 — [Dong, Meng, Whaley, Lin, PRA 103, 042419 (2021)](https://arxiv.org/abs/2002.11649).
  - Symmetric-QSP energy landscape: non-convex, yet a fixed initial guess works reliably — [Wang, Dong, Lin, Quantum (2022)](https://arxiv.org/abs/2110.04993).
  - Older approaches: polynomial factorisation — [Haah 2019](https://arxiv.org/abs/1806.10236); "Finding angles with machine precision" — [Chao et al. 2020](https://arxiv.org/abs/2003.02831).
- pyqsp generates phase angles. Its "laurent" method builds on the Chao et al. angle-sequence code; its "tf" method optimises with TensorFlow. It supports both Wx and Wz conventions (related by a Hadamard). Built-in examples include a sign function (oblivious amplitude amplification) and a threshold function — [pyqsp on PyPI](https://pypi.python.org/project/pyqsp/0.1.3/); [GitHub ichuang/pyqsp](https://github.com/ichuang/pyqsp)
- PennyLane's QSVT tutorials (updated Apr 2026) fix the signal and vary the phases, then plot the polynomial. pyqsp angles must be converted for QSVT conventions — [PennyLane intro QSVT](https://pennylane.ai/demos/tutorial_intro_qsvt); [PennyLane QSVT hardware demo](https://pennylane.ai/qml/demos/tutorial_qsvt_hardware)

#### Block encodings, LCU, qubitization, QSVT
- Block encoding: U is an (alpha, a, epsilon) block encoding of A if ||A - alpha (<0^a| ⊗ I) U (|0^a> ⊗ I)|| <= epsilon — [Gilyén, Su, Low, Wiebe, "QSVT", STOC 2019](https://arxiv.org/abs/1806.01838)
- LCU: for H = sum_j alpha_j U_j with lambda = sum_j |alpha_j|, PREP|0> = sum_j sqrt(alpha_j/lambda)|j> and SELECT = sum_j |j><j| ⊗ U_j. Then <0|PREP^dagger SELECT PREP|0> = H/lambda — [Childs & Wiebe 2012](https://arxiv.org/abs/1202.5822); [Berry, Childs, Cleve, Kothari, Somma, PRL 114, 090502 (2015)](https://arxiv.org/abs/1412.4687)
- Qubitization: the walk operator built from a block encoding has eigenphases ±arccos(E_k/lambda) in 2D invariant subspaces. Hamiltonian simulation then costs O(lambda t + log(1/epsilon)/log log(1/epsilon)) queries, which is additively optimal — [Low & Chuang, Quantum 3, 163 (2019)](https://arxiv.org/abs/1610.06546)
- QSVT: with alternating projector-controlled phases e^{i phi (2 Pi - I)} interleaved with U and U^dagger, the projected block becomes P^{(SV)}(A) = sum_k P(sigma_k)|w_k><v_k| for any QSP-achievable P — [Gilyén et al. 2019](https://arxiv.org/abs/1806.01838)
- Polynomial degree costs (QSVT):
  - matrix inversion on [1/kappa, 1]: d = O(kappa log(kappa/epsilon));
  - sign function with gap delta: d = O(log(1/epsilon)/delta);
  - e^{-i tau x}: d = O(|tau| + log(1/epsilon)/log log(1/epsilon)) via Jacobi-Anger, e^{-i tau x} = J_0(tau) + 2 sum_k (-i)^k J_k(tau) T_k(x).
  - Sources: [Gilyén et al. 2019](https://arxiv.org/abs/1806.01838); [Martyn et al. 2021](https://arxiv.org/abs/2105.02859)

#### HHL and its fine print
- HHL produces the quantum state |x> proportional to A^{-1}|b> in time O~(log(N) s^2 kappa^2/epsilon) for s-sparse A. Matrix inversion is BQP-complete — [Harrow, Hassidim, Lloyd, PRL 103, 150502 (2009)](https://arxiv.org/abs/0811.3171)
- Aaronson's "read the fine print" caveats:
  1. |b> must be loadable quickly (QRAM-type assumptions);
  2. A must be sparse/structured and well-conditioned (kappa enters polynomially);
  3. the output is a quantum state, so you get samples or expectation values, not x;
  4. the comparison must be against the best classical algorithm for the **same** sampling/estimation task.
  - Source: [Aaronson, "Read the fine print", Nature Physics 11, 291 (2015)](https://www.scottaaronson.com/papers/qml.pdf)
- Better precision dependence: O(kappa polylog(kappa/epsilon)) — [Childs, Kothari, Somma 2017](https://arxiv.org/abs/1511.02306). Optimal O(kappa log(1/epsilon)) via the discrete adiabatic theorem — [Costa et al., PRX Quantum 3, 040303 (2022)](https://arxiv.org/abs/2111.08152)

#### Hamiltonian simulation
- Lloyd 1996: local Hamiltonians are efficiently simulable with product formulas — [Lloyd, Science 273, 1073 (1996)](https://doi.org/10.1126/science.273.5278.1073)
- Commutator scaling of Trotter error:
  - First order with two terms: ||e^{-i(A+B)t} - (e^{-iAt/r} e^{-iBt/r})^r|| <= (t^2/2r)||[A,B]||.
  - For a p-th order formula with r steps, the error is O(alpha_comm t^{p+1}/r^p), where alpha_comm = sum ||[H_{gamma_{p+1}}, ..., [H_{gamma_2}, H_{gamma_1}]]||.
  - So r = O(alpha_comm^{1/p} t^{1+1/p}/epsilon^{1/p}). Nearest-neighbour lattices give near-linear-in-volume costs.
  - Source: [Childs, Su, Tran, Wiebe, Zhu, "Theory of Trotter error with commutator scaling", PRX 11, 011020 (2021)](https://arxiv.org/abs/1912.08854)
- qDRIFT: randomly sample term j with probability |h_j|/lambda. The gate count N = O(lambda^2 t^2/epsilon) is **independent of the number of terms L**. It wins for Hamiltonians with many small terms (chemistry) — [Campbell, PRL 123, 070503 (2019)](https://arxiv.org/abs/1811.08017)
- Truncated Taylor series via LCU: O(lambda t log(lambda t/epsilon)/log log(lambda t/epsilon)) — [Berry et al. 2015](https://arxiv.org/abs/1412.4687)
- No-fast-forwarding: generic Hamiltonians cannot be simulated in time sublinear in t — [Berry, Ahokas, Cleve, Sanders 2007](https://arxiv.org/abs/quant-ph/0508139)

#### Quantum walks
- Continuous-time quantum walk (CTQW): U(t) = e^{-iAt}. Coined discrete-time walks and walks on graphs are formalised in [Aharonov, Ambainis, Kempe, Vazirani 2001](https://arxiv.org/abs/quant-ph/0012090); first algorithmic use in [Farhi & Gutmann 1998](https://arxiv.org/abs/quant-ph/9706062)
- Glued trees: two binary trees of depth n joined by a random cycle. A CTQW crosses in poly(n) time, while any classical algorithm needs exponentially many oracle queries. This is an exponential **algorithmic** (oracle) speedup — [Childs, Cleve, Deotto, Farhi, Gutmann, Spielman, STOC 2003](https://arxiv.org/abs/quant-ph/0209131)
- Szegedy walks: quadratic speedup of Markov-chain hitting times, roughly 1/sqrt(delta) against 1/delta for spectral gap delta — [Szegedy 2004](https://arxiv.org/abs/quant-ph/0401053). Element distinctness in O(N^{2/3}) queries (optimal) — [Ambainis 2004](https://arxiv.org/abs/quant-ph/0311001). NAND-tree / game-tree evaluation in O(sqrt N) — [Farhi, Goldstone, Gutmann 2007](https://arxiv.org/abs/quant-ph/0702144). CTQW is universal for quantum computation — [Childs, PRL 102, 180501 (2009)](https://arxiv.org/abs/0806.1972)
- Decoherence makes quantum-walk spreading cross over from ballistic to diffusive, i.e. classical — [Kendon, "Decoherence in quantum walks – a review" 2006](https://arxiv.org/abs/quant-ph/0606016)
- Exponential speedup for simulating 2^n coupled classical oscillators, a modern quantum-walk-flavoured result — [Babbush et al., PRX 13, 041041 (2023)](https://arxiv.org/abs/2303.13012)

#### Adiabatic QC, QAOA, VQE
- AQC: H(s) = (1-s)H_0 + sH_P. Runtime is governed by the minimum gap; heuristically T >> ||dH/ds||/g_min^2 — [Farhi, Goldstone, Gutmann, Sipser 2000](https://arxiv.org/abs/quant-ph/0001106); [Albash & Lidar, RMP 90, 015002 (2018)](https://arxiv.org/abs/1611.04471)
- AQC is polynomially equivalent to the circuit model — [Aharonov, van Dam, Kempe, Landau, Lloyd, Regev 2004/2007](https://arxiv.org/abs/quant-ph/0405098)
- Exponentially small gaps can occur (e.g. Anderson-localisation arguments for random NP-hard instances) — [van Dam, Mosca, Vazirani 2001](https://arxiv.org/abs/quant-ph/0206003); [Altshuler, Krovi, Roland 2010](https://arxiv.org/abs/0908.2782). A local adiabatic schedule recovers Grover's sqrt N — [Roland & Cerf 2002](https://arxiv.org/abs/quant-ph/0107015)
- QAOA: |gamma, beta> = product over p of e^{-i beta_p B} e^{-i gamma_p C}|+>^n, with B = sum X_i. It recovers adiabatic evolution as p goes to infinity (Trotterised annealing). At p = 1 on 3-regular MaxCut it achieves approximation ratio at least 0.6924 — [Farhi, Goldstone, Gutmann 2014](https://arxiv.org/abs/1411.4028)
- QAOA limits: Z2 symmetry plus locality obstacles at low depth (worse than Goemans-Williamson on some families) — [Bravyi, Kliesch, Koenig, Tang, PRL 125, 260505 (2020)](https://arxiv.org/abs/1910.08980). "QAOA needs to see the whole graph" — [Farhi, Gamarnik, Gutmann 2020](https://arxiv.org/abs/2004.09002). Local classical algorithms match or beat p = 1 — [Hastings 2019](https://arxiv.org/abs/1905.07047)
- **[NEW 2024]** Fixed-parameter QAOA on LABS (low-autocorrelation binary sequences), from noiseless simulations up to 40 qubits: QAOA plus quantum minimum-finding scales better than branch-and-bound. Hardware runs used algorithm-specific error detection on Quantinuum — [Shaydulin et al., Science Advances 10, eadm6761 (29 May 2024)](https://arxiv.org/abs/2308.02342)
- **[NEW 2025]** Linear-ramp QAOA (LR-QAOA) uses non-variational, fixed linear schedules (a first-order Trotterisation of adiabatic evolution). Success probability fits P(x*) ~ 2^{-eta(p) N + C}, with eta improving from 0.22 at p = 10 to 0.05 at p = 100 for weighted MaxCut. Hardware runs on IonQ, Quantinuum and IBM reached up to 109 qubits, p = 100 and 21,200 CNOTs — [Montañez-Barrera & Michielsen, npj QI 11, 131 (Aug 2025)](https://arxiv.org/abs/2405.09169)
- VQE: minimise E(theta) = <psi(theta)|H|psi(theta)> >= E_0 using a hybrid loop — [Peruzzo et al., Nat. Commun. 5, 4213 (2014)](https://arxiv.org/abs/1304.3061)
- Noise limits: noisy variational optimisation is efficiently matched by classical algorithms beyond logarithmic depth under depolarizing noise — [Stilck França & García-Patrón, Nat. Phys. 2021](https://arxiv.org/abs/2009.05532). **[NEW 2024]** There is a polynomial-time classical algorithm for estimating expectation values of noisy random circuits — [Schuster et al. 2024](https://arxiv.org/abs/2407.12768)

#### Barren plateaus (BP) and classical simulability
- McClean 2018: for ansätze forming approximate 2-designs, Var[dC/d theta_k] is exponentially small in n — [McClean et al., Nat. Commun. 9, 4812 (2018)](https://arxiv.org/abs/1803.11173)
- Cost-function dependence: **global** costs (e.g. 1 - |<0^n|psi>|^2) have barren plateaus even at shallow depth. **Local** costs at depth O(log n) have variance in Omega(1/poly(n)) — [Cerezo, Sone, Volkoff, Cincio, Coles, Nat. Commun. 12, 1791 (2021)](https://arxiv.org/abs/2001.00550)
- Noise-induced barren plateaus: under local Pauli noise, gradients decay exponentially in **depth**, regardless of how the parameters are initialised — [Wang et al., Nat. Commun. 12, 6961 (2021)](https://arxiv.org/abs/2007.14384)
- **[NEW 2024]** Lie-algebraic theory: the loss variance scales as about 1/dim(g), where g is the dynamical Lie algebra (DLA) of the generators, when the input state or observable lies in g — [Ragone et al., Nat. Commun. 2024](https://arxiv.org/abs/2309.09342); [Fontana et al., Nat. Commun. 2024](https://arxiv.org/abs/2309.07902). Small DLAs (e.g. free-fermion/matchgate circuits) allow "g-sim" classical simulation — [Goh et al. 2023](https://arxiv.org/abs/2308.01432)
- **[NEW 2025]** Review: [Larocca et al., "Barren plateaus in variational quantum computing", Nature Reviews Physics (2025)](https://arxiv.org/abs/2405.00781)
- **[NEW 2025]** Cerezo et al., "Does provable absence of barren plateaus imply classical simulability? Or, why we need to rethink variational quantum computing", Nat. Commun. 16, 7907 (2025):
  - It is a perspective that gathers case-by-case evidence, not a theorem.
  - Many commonly used BP-free models confine the problem to small, classically simulable subspaces. They can be simulated classically after an initial **data-acquisition** phase on the quantum device.
  - The authors propose "quantum-enhanced classical simulation" in place of on-device training.
  - The published abstract hedges more than arXiv v2 did.
  - Sources: [arXiv:2312.09121](https://arxiv.org/abs/2312.09121v3); [publication record](https://strathprints.strath.ac.uk/93944)

#### QML, dequantization, quantum kernels
- Kerenidis-Prakash: recommendation systems in polylog time given QRAM — [2016](https://arxiv.org/abs/1603.08675). Tang 2018 dequantised it: a classical algorithm with ℓ²-norm **sample-and-query access** runs in time poly(k, 1/epsilon, kappa) · polylog(mn), which removes the exponential separation — [Tang, STOC 2019](https://arxiv.org/abs/1807.04271)
- A general framework dequantises low-rank QSVT: QRAM state preparation corresponds to classical ℓ²-sampling access — [Chia, Gilyén, Li, Lin, Tang, Wang, STOC 2020 / JACM](https://arxiv.org/abs/1910.06151)
- Quantum kernels k(x, x') = |<phi(x)|phi(x')>|^2 (ZZ feature map) — [Havlíček et al., Nature 567, 209 (2019)](https://arxiv.org/abs/1804.11326). There is a provable speedup on a learning task built from discrete log, assuming DLP is hard — [Liu, Arunachalam, Temme, Nat. Phys. 2021](https://arxiv.org/abs/2010.02174)
- Exponential concentration: expressive embeddings, global measurements, entanglement and noise all make kernel values concentrate exponentially, so exponentially many shots are needed — [Thanasilp et al., Nat. Commun. 2024](https://arxiv.org/abs/2208.11060). Classical ML with data can often match quantum models; the "geometric difference" test checks this — [Huang et al., Nat. Commun. 12, 2631 (2021)](https://arxiv.org/abs/2011.01938)

#### Shadow tomography and classical shadows
- Shadow tomography: predict M two-outcome observables using poly(log M, n, 1/epsilon) copies — [Aaronson, STOC 2018](https://arxiv.org/abs/1711.01053)
- Classical shadows:
  - Apply a random unitary from an ensemble, measure in the computational basis, and invert the measurement channel.
  - For random single-qubit Pauli bases the snapshot is rho_hat = tensor product over i of (3 U_i^dagger|b_i><b_i|U_i - I).
  - With median-of-means, N = O(log(M/delta) · max_i ||O_i||^2_shadow / epsilon^2).
  - For Pauli measurements and a k-local Pauli observable, ||O||^2_shadow = 3^k ("measure first, ask questions later"). For random Clifford measurements the shadow norm is bounded by about 3 tr(O^2), which suits fidelity estimation.
  - Source: [Huang, Kueng, Preskill, Nat. Phys. 16, 1050 (2020)](https://arxiv.org/abs/2002.08953)
- Derandomized shadows choose fixed measurement bases deterministically — [Huang, Kueng, Preskill, PRL 127, 030503 (2021)](https://arxiv.org/abs/2103.07510). Robust shadows calibrate noisy measurements — [Chen, Yu, Zeng, Flammia, PRX Quantum 2, 030348 (2021)](https://arxiv.org/abs/2011.09636). **[NEW 2024]** Triply efficient shadow tomography — [King, Gosset, Kothari, Babbush 2024](https://arxiv.org/abs/2404.19211)

#### DQI (decoded quantum interferometry) [NEW 2024 preprint, NEW 2025 Nature]
- DQI uses the QFT to reduce optimisation (max-LINSAT, max-XORSAT, Optimal Polynomial Intersection) to **decoding**. Published as Jordan et al., "Optimization by decoded quantum interferometry", Nature 646, 831-836 (2025). The Nature byline order starts Jordan, Wootters, Schmidhuber, King, Isakov; the arXiv version also lists Shutty, Zalcman, Babbush and others, so check the journal page for the definitive list — [arXiv:2408.08292](https://arxiv.org/abs/2408.08292v3); [Google Research page](https://research.google/pubs/optimization-by-decoded-quantum-interfereometry/)
- Superpolynomial speedup over known classical algorithms for OPI (finite-field polynomial fitting), because the Reed-Solomon algebraic structure carries over into an efficiently decodable code. For sparse unstructured problems (max-k-XORSAT with LDPC codes), advantage is **unresolved**: on one instance family DQI with belief-propagation decoding beat simulated annealing but not specialised classical solvers — [arXiv:2408.08292](https://arxiv.org/abs/2408.08292v3); [UW seminar listing, Mar 2026](https://phys.washington.edu/events/2026-03-10/optimization-decoded-quantum-interferometry)
- The Yamakawa-Zhandry problem is a special case of a problem DQI solves efficiently — [APS March Meeting 2025 abstract](https://meetings-archive.aps.org/smt/2025/mar-t16/2)
- **[NEW 2025-26]** Follow-ups:
  - "No quantum advantage in DQI for MaxCut": any MaxCut family where DQI has a nontrivial asymptotic guarantee is classically solvable exactly in polynomial time — [Parekh, arXiv:2509.19966 (TQC 2026)](https://arxiv.org/abs/2509.19966).
  - "DQI requires structure": on random LDPC-type max-XORSAT, DQI is obstructed by the overlap-gap property if decoding stops at the folklore threshold, and approximate message passing (AMP) beats DQI numerically — [arXiv:2509.14509](https://arxiv.org/html/2509.14509v1).
  - DQI is hard to simulate classically but sits in a low level of PH, which rules out supremacy-style hardness arguments — [Marwaha et al., arXiv:2509.14443](https://arxiv.org/abs/2509.14443).
  - Nearly linear-time DQI for OPI — [Rosmanis, arXiv:2601.15171 (Jan 2026)](https://arxiv.org/abs/2601.15171).
  - MCMC (block-Gibbs) sampling reproduces DQI's expected approximation ratios on max-XORSAT, and on OPI scales empirically as about 1.1^n — [arXiv:2607.28120 (Jul 2026)](https://arxiv.org/abs/2607.28120).

#### Regev factoring (2023) and Yamakawa-Zhandry (2022)
- Regev: each circuit has O~(n^{3/2}) gates (against about n^2 for Shor), and the circuit is run sqrt(n) + 4 times. Results are combined with polynomial-time classical (lattice-based) post-processing under a number-theoretic heuristic assumption. The paper itself says practical gains are unclear — [Regev, arXiv:2308.06572 (Aug 2023)](https://arxiv.org/abs/2308.06572)
- Follow-up reducing Regev's qubit count and adding noise robustness — [Ragavan & Vaikuntanathan 2023/24](https://arxiv.org/abs/2310.00899)
- Yamakawa-Zhandry: an NP search problem relative to a **random oracle** (no promise structure) that quantum algorithms solve with poly queries while classical algorithms need exponentially many. It gives verifiable quantum advantage and is built on folded Reed-Solomon codes — [Yamakawa & Zhandry, FOCS 2022 / JACM 2024](https://arxiv.org/abs/2204.02063)

### Inferences
- **Unification ladder for a teaching tool.** (1) One-qubit QSP draws polynomials. (2) Grover = T_{2k+1}, fixed-point AA = a different phase list. (3) Phase estimation = a step/threshold polynomial in the eigenphase. (4) Hamiltonian simulation = Jacobi-Anger cos/sin polynomials. (5) HHL = 1/x with degree about kappa log(kappa/epsilon). (6) The same phases applied to a block-encoded matrix give QSVT. All of this stays inside one widget, and the hardware cost of step (1) is **zero two-qubit gates**.
- Variational methods should be taught as a story with its counter-story: "Why we hoped (VQE/QAOA) → why gradients vanish (BP, NIBP) → why curing BP often kills the advantage (DLA dimension ↔ simulability, Cerezo 2025) → what survives (LR-QAOA-style non-variational schedules, data-acquisition paradigms)."
- DQI is an excellent advanced topic because it is a QFT-plus-structure story. Its semicircle-law performance can be plotted analytically, and the 2025-26 follow-ups give a ready-made "advantage claim, then classical response" lesson. My recollection of the DQI semicircle law for max-XORSAT is <s>/m = 1/2 + sqrt((l/m)(1 - l/m)) for l/m <= 1/2, where l is the number of correctable errors. It must be checked against Theorem 4.1 of arXiv:2408.08292 before use.

### Gaps
- I did not confirm that pyqsp installs in Pyodide (its dependencies are numpy/scipy, and optionally TensorFlow, which is not available in Pyodide). A fallback is a small numpy implementation of the Dong-Lin-style optimisation.
- I did not find the details of the "tailored classical solver" that beats DQI on its own max-XORSAT benchmark family.
- I did not verify the Ragavan-Vaikuntanathan exact qubit scaling (I recall about O(n log n)).

---

## Q3. Quantum-advantage experiments and the arguments over classical spoofing (RCS, Willow, Quantum Echoes/OTOC, D-Wave 2025, certified randomness, trackers)

### Takeaway
Every "beyond-classical" claim since 2019 has been followed by classical counter-work. For teaching, the important distinctions are:
- **sampling** advantages (RCS: hard but neither useful nor efficiently verifiable);
- **physically verifiable expectation values** (Quantum Echoes 2025: reproducible on another quantum device or in nature, but not cryptographically verifiable);
- **cryptographically / classically verifiable** advantage (proofs of quantumness, Yamakawa-Zhandry, certified randomness, which in 2025 still used exaflop classical verification).

### Cited Findings
- Sycamore 2019: 53 qubits, random circuit sampling (RCS) in about 200 s, against a claimed 10,000 years classically — [Arute et al., Nature 574, 505 (2019)](https://arxiv.org/abs/1910.11333). Later reproduced by tensor-network simulation — [Pan, Chen, Zhang, PRL 129, 090502 (2022)](https://arxiv.org/abs/2111.03011)
- Asymptotically, noisy RCS at a constant noise rate is classically easy in polynomial time (given anti-concentration) — [Aharonov, Gao, Landau, Liu, Vazirani, STOC 2023](https://arxiv.org/abs/2211.03999). **[NEW 2024]** Noisy RCS has a "weak-noise phase" in which cross-entropy benchmarking (XEB) tracks fidelity — [Morvan et al., Nature 634, 328 (2024)](https://arxiv.org/abs/2304.11119)
- Complexity basis for RCS (heavy-output generation, HOG) — [Aaronson & Chen, CCC 2017](https://arxiv.org/abs/1612.05903)
- **[NEW 2024]** Willow (Dec 2024):
  - Below-threshold surface-code memory: logical error per cycle is suppressed by Lambda ~ 2.14 each time the code distance rises by 2, with about 0.143% per cycle at d = 7 — [Google Quantum AI, Nature 2025](https://arxiv.org/abs/2408.13687).
  - RCS in under 5 minutes, against an estimated 10^25 years classically — [Google blog, Dec 2024](https://blog.google/technology/research/google-willow-quantum-chip/).
- **[NEW 2025]** Quantum Echoes (Google, Nature, Oct 2025, DOI 10.1038/s41586-025-09526-6):
  - Measures second-order out-of-time-order correlators OTOC^(2) on a 103-qubit Willow processor.
  - OTOC^(2) stays sensitive to the dynamics at long times because of constructive interference between Pauli strings forming large loops in configuration space.
  - The authors say the measurements exceed the capacity of known classical algorithms — [arXiv:2506.10191](https://arxiv.org/html/2506.10191v1); [APS 2026 abstract](https://meetings-archive.aps.org/smt/2026/mar-l05/1/).
  - Google reports 13,000x faster than the best known classical algorithm on Frontier (about 2 h against about 3 years). "Verifiable" here means reproducible on another quantum computer of similar quality, or checkable against experiments such as NMR — [Quantum Computing Report](https://quantumcomputingreport.com/google-quantum-ai-achieves-verifiable-quantum-advantage-on-willow-chip-with-quantum-echoes-algorithm/); [Nasdaq/coverage](https://www.nasdaq.com/articles/google-achieves-first-verifiable-quantum-advantage-quantum-echoes-algorithm)
- **[NEW 2025]** D-Wave, "Beyond-classical computation in quantum simulation" (Science, Mar 2025): quench dynamics of spin glasses on annealers, with an estimate of about a million years on Frontier using MPS. The scale was reported as more than 5,000 qubits across four lattice types (secondary report) — [King et al., arXiv:2403.00910](https://arxiv.org/abs/2403.00910); [QCR](https://quantumcomputingreport.com/flatiron-institute-tensor-network-algorithm-overturns-historical-d-wave-quantum-supremacy-claim/)
  - Rebuttals: 2D/3D tensor networks evolved with belief propagation simulate these dynamics accurately with modest resources. This was later published in Science — [Tindall, Mello, Fishman, Stoudenmire, Sels, arXiv:2503.05693](https://arxiv.org/abs/2503.05693v2). Time-dependent variational Monte Carlo with Jastrow-Feenberg wavefunctions, up to 128 spins on a 3D diamond lattice with correlation errors below 7% — [Mauron & Carleo, arXiv:2503.08247](https://arxiv.org/html/2503.08247v1)
  - D-Wave's comment calls the classical work "impressive" but disputes that it covers all geometries, scales and coupling regimes — [King, Amin et al., arXiv:2504.06283](https://arxiv.org/html/2504.06283v1); [QCR on the D-Wave rebuttal](https://quantumcomputingreport.com/d-wave-systematically-rebuts-flatiron-claims-reaffirming-beyond-classical-simulation-milestones/)
- **[NEW 2025]** Certified randomness (JPMorganChase, Quantinuum, Argonne, ORNL, UT Austin), Nature 640, 343-348 (online 26 Mar 2025):
  - 56-qubit Quantinuum H2-1 accessed remotely; RCS-based randomness expansion following Aaronson's 2018 protocol.
  - 71,313 certified bits of entropy, valid against a **restricted adversary class**, with about 1.1 EFLOPS of classical verification.
  - About 2 s per circuit on the device against about 100 s per circuit on the largest supercomputer — [Liu et al., arXiv:2503.20498](https://arxiv.org/abs/2503.20498); [JPMorgan blog](https://www.jpmorganchase.com/about/technology/blog/certified-randomness); [UT Austin](https://cns.utexas.edu/news/research/researchers-achieve-quantum-computing-milestone-realizing-certified-randomness)
  - Underlying theory — [Aaronson & Hung, STOC 2023](https://arxiv.org/abs/2303.01625)
- Classically verifiable proofs of quantumness from trapdoor claw-free functions — [Brakerski et al. 2018](https://arxiv.org/abs/1804.00640); [Kahanamoku-Meyer et al., Nat. Phys. 2022](https://arxiv.org/abs/2104.00687)
- **[NEW 2025]** An open quantum-advantage tracker (IBM, Algorithmiq, Flatiron, BlueQubit) launched with three candidate categories (observable estimation, variational, classically verifiable). IBM said in Nov 2025 that advantage "hasn't been achieved yet" and predicted first verified cases by the end of 2026 — [IBM QDC 2025 blog](https://www.ibm.com/quantum/blog/qdc-2025)
- **[NEW 2025/2026]** "The vast world of quantum advantage" (Huang, Choi, McClean, Preskill; arXiv Aug 2025; PRX 16, 030501, Jul 2026):
  - Five keystone properties of an ideal advantage: predictability, typicality, robustness, verifiability, usefulness.
  - Four domains: computation, learning/sensing, cryptography/communication, space.
  - Proves that some advantages are inherently unpredictable with classical resources alone — [arXiv:2508.05720](https://arxiv.org/abs/2508.05720)
- **[NEW 2025/2026]** "The Grand Challenge of Quantum Applications" (Babbush et al., arXiv:2511.09124; PRX Quantum 7, 020101, 2026) sets out a five-stage pipeline from theoretical advantage to compilation. It singles out finding concrete hard instances and connecting them to real-world use as under-resourced — [arXiv:2511.09124](https://arxiv.org/abs/2511.09124)

### Inferences
- A classroom-ready taxonomy: (a) **hard but useless** (RCS); (b) **useful-ish physics, verifiable by repetition or nature** (Quantum Echoes, D-Wave dynamics); (c) **cryptographically verifiable** (proofs of quantumness, certified randomness, Yamakawa-Zhandry); (d) **useful and fault-tolerant** (Shor, chemistry; not yet). Each claim's classical rebuttal shows how "advantage" is a moving target.
- A "spoof-it-yourself" demo fits the constraints well. Let learners run a small RCS circuit (about 12-20 qubits, about 60-100 ZZ gates) under the IonQ noise model, compute linear XEB, and then compare with a cheap classical "spoofer" (e.g. keep only part of the circuit). Watching XEB degrade with noise and depth makes Aharonov et al. 2023 tangible.

### Gaps
- I found no independent classical spoofing or rebuttal of Quantum Echoes (as of these searches). Its absence is not evidence that none exists.
- A July 2026 claim that IBM and partners entered an "advantage era" appeared only on an aggregator and is **unverified**.
- I did not confirm the publication date of the Tindall et al. Science version.

---

## Q4. Complexity: BQP and its relations to P/NP/PH, Raz-Tal, QMA and the local Hamiltonian problem, query vs gate complexity, BQP vs BPP evidence, NP-completeness, sampling hardness, quantum PCP, NLTS

### Takeaway
BQP is believed to be strictly larger than BPP (factoring, Simon/Forrelation oracles) but not to contain NP (BBBV). Relative to an oracle it even escapes the entire polynomial hierarchy (Raz-Tal 2018). Quantum "NP" is QMA, with the local Hamiltonian problem as its complete problem. The quantum PCP conjecture is open, but its necessary consequence NLTS was proved in 2022 using good quantum LDPC codes. Sampling advantages rest on "PH does not collapse" arguments.

### Cited Findings
- Containments: BPP ⊆ BQP ⊆ PP ⊆ PSPACE, and PostBQP = PP — [Aaronson 2005, "Quantum computing, postselection, and probabilistic polynomial-time"](https://arxiv.org/abs/quant-ph/0412187); [Bernstein & Vazirani 1997](https://doi.org/10.1137/S0097539796300921)
- BQP vs PH:
  - [Aaronson 2009, "BQP and the polynomial hierarchy"](https://arxiv.org/abs/0910.4698) introduced Forrelation-type problems.
  - Raz & Tal 2018 constructed an oracle A with BQP^A ⊄ PH^A, using a Forrelation distribution and AC^0 lower bounds — [ECCC TR18-107; STOC 2019 / JACM 2022](https://eccc.weizmann.ac.il/report/2018/107/).
  - Forrelation shows that 1 vs Omega~(sqrt N) queries is the largest possible separation — [Aaronson & Ambainis 2015](https://arxiv.org/abs/1411.5729).
- NP vs BQP: Grover is optimal and NP^A ⊄ BQP^A for a random oracle, so black-box search gains only quadratically — [BBBV 1997](https://arxiv.org/abs/quant-ph/9701001). Popular overview — [Aaronson, "The Limits of Quantum Computers", Scientific American 2008](https://www.scottaaronson.com/papers/limitsqc-draft.pdf)
- Query vs gate complexity:
  - Polynomial method: [Beals et al. 1998](https://arxiv.org/abs/quant-ph/9802049).
  - Adversary method: [Ambainis 2000](https://arxiv.org/abs/quant-ph/0002066).
  - The general adversary bound characterises quantum query complexity up to a constant: [Reichardt 2009](https://arxiv.org/abs/0904.2759).
  - For **total** Boolean functions, quantum and classical query complexities are polynomially related; the best known bound is D(f) = O(Q(f)^4) — [Aaronson, Ben-David, Kothari, Rao, Tal, STOC 2021](https://arxiv.org/abs/2010.12629). Exponential separations therefore need promises/structure (Simon, Forrelation) or search problems relative to random oracles (Yamakawa-Zhandry) — [arXiv:2204.02063](https://arxiv.org/abs/2204.02063).
- QMA and local Hamiltonians: the k-local Hamiltonian problem (decide whether the ground energy is <= a or >= b with b - a >= 1/poly) is QMA-complete. Kitaev proved it for 5-local; 2-local is also complete — [Kempe, Kitaev, Regev 2006](https://arxiv.org/abs/quant-ph/0406180)
- Guided local Hamiltonian: given a guiding state with good overlap, estimating ground energy to 1/poly precision is **BQP-complete**. The hardness of QMA therefore lies in preparing the state — [Gharibian & Le Gall, STOC 2022](https://arxiv.org/abs/2111.02474). There is no evidence yet of *generic* exponential advantage for ground-state chemistry, because of state-preparation overlap — [Lee et al., Nat. Commun. 14, 1952 (2023)](https://arxiv.org/abs/2208.02199)
- Quantum PCP conjecture: approximating the ground energy of local Hamiltonians to **constant relative** accuracy (epsilon·m) stays QMA-hard. It is open — [Aharonov, Arad, Vidick, "The quantum PCP conjecture", SIGACT News 2013](https://arxiv.org/abs/1309.7495)
- **NLTS theorem (2022; STOC 2023)**: there are families of local Hamiltonians for which every state with energy below a constant fraction epsilon·m has circuit complexity omega(log n). In other words, there are no low-energy trivial states. The construction uses good quantum LDPC codes, and NLTS is a necessary consequence of qPCP — [Anshu, Breuckmann, Nirkhe](https://arxiv.org/abs/2206.13228)
- Sampling hardness:
  - Exact (or multiplicative-error) classical BosonSampling would collapse PH to its third level. Additive-error hardness rests on conjectures about permanents (average-case #P-hardness, anti-concentration) — [Aaronson & Arkhipov, STOC 2011](https://arxiv.org/abs/1011.3245).
  - IQP circuits have the same exact/multiplicative collapse — [Bremner, Jozsa, Shepherd 2011](https://arxiv.org/abs/1005.1407) — and additive-error hardness under conjectures — [Bremner, Montanaro, Shepherd, PRL 2016](https://arxiv.org/abs/1504.07999).
- Hamiltonian simulation is BQP-complete (circuit-to-Hamiltonian / Feynman-Kitaev constructions); matrix inversion is BQP-complete — [HHL 2009](https://arxiv.org/abs/0811.3171)
- **[NEW 2025]** DQI can be simulated in a low level of PH, which rules out supremacy-style (PH-collapse) hardness arguments for it — [Marwaha et al., arXiv:2509.14443](https://arxiv.org/abs/2509.14443)

### Inferences
- **Forrelation demo (complexity made runnable).** The circuit H^n, O_f, H^n, O_g, H^n gives amplitude <0^n|·|0^n> = Phi(f, g) = N^{-3/2} sum_{x,y} f(x)(-1)^{x·y} g(y) with one query to each function. Classically about sqrt N queries are needed. This is the problem behind the Raz-Tal oracle separation, so the "BQP is not in PH (relative to an oracle)" theorem becomes a 4-qubit experiment. Cost estimate: below.
- **Teaching sentence:** "Quantum computers are believed to be exponentially faster only when the problem has hidden algebraic or Fourier structure (periodicity, Forrelation, codes). Black-box search gains only quadratically (BBBV). NP-complete problems are not believed to be in BQP, and that is a conjecture, not a theorem."

### Gaps
- I did not check whether any 2025-2026 progress has been made on qPCP itself, beyond NLTS and its follow-ups. I recall work on combinatorial NLTS and the NLSS variants but did not verify it.

---

## Q5. Teaching angle: misconceptions and the best existing visual intuitions

### Takeaway
The most common and harmful misconception is "a quantum computer tries all answers at once". It should be replaced with "amplitudes, interference, and one sample at the end". Other recurring errors: confusing superposition with ignorance or mixtures; believing Grover is exponential; reading the QFT as a faster FFT; treating HHL or QML as exponential speedups for free; and accepting compiled Shor/QPE demos at face value. The best existing intuitions are Grover as a 2D rotation, phase wheels / circle notation for the QFT, and polynomial plots for QSP. **I found no dedicated interactive QSP/QSVT polynomial designer**, which is a clear novelty gap.

### Cited Findings
- Aaronson's long-running message (and the Shtetl-Optimized tagline): quantum computers do not solve hard search problems by trying every solution at once; the power is in choreographing interference — [Aaronson, Scientific American 2008](https://www.scottaaronson.com/papers/limitsqc-draft.pdf); [SMBC × Aaronson comic "The Talk" (2015)](https://www.smbc-comics.com/comic/the-talk-3)
- **[NEW 2025]** 3Blue1Brown, "But what is Quantum Computing? (Grover's Algorithm)" (about 36 min, released around 30 Apr 2025). It opens with a misconceptions segment and teaches Grover with the 2D geometric picture — [video](https://www.youtube.com/watch?v=RQWpF2Gb-gU). A follow-up post (4 May 2025) addresses viewer confusion that Grover "requires knowing the answer" and stresses linearity — [3Blue1Brown Substack](https://3blue1brown.substack.com/p/where-my-explanation-of-grovers-algorithm)
- Physics education research:
  - Students can compute with superpositions but often cannot identify their experimental implications, and they confuse superpositions with mixtures — [Passante, Emigh, Shaffer, PRST-PER 11, 020135 (2015)](https://link.aps.org/doi/10.1103/PhysRevSTPER.11.020135).
  - Learners taught "exponential advantage" sometimes conclude that classical computers can only occupy N states, which is a state-counting error — [arXiv:2408.04859, "Investigating and improving student understanding of the basics of quantum computing"](https://arxiv.org/abs/2408.04859).
  - **[NEW 2026]** Resource letter on quantum information education research — [arXiv:2606.06445](https://arxiv.org/abs/2606.06445).
- Grover-as-rotation (two reflections compose to a rotation by 2 theta) is the standard textbook figure — [Nielsen & Chuang §6.1]; [de Wolf notes](https://arxiv.org/abs/1907.09415)
- Circle notation / "phase wheels" for registers and the QFT — [Johnston, Harrigan, Gimeno-Segovia, "Programming Quantum Computers" (O'Reilly 2019)](https://www.oreilly.com/library/view/programming-quantum-computers/9781492039679/). Quirk, a live amplitude/phase visualiser — [algassert.com/quirk](https://algassert.com/quirk)
- QSP polynomial plots (|P(a)|^2 against signal a) are the central figures of the unification paper — [Martyn et al. 2021](https://arxiv.org/abs/2105.02859). PennyLane's notebook-based QSVT demos plot polynomials but are not interactive designers — [PennyLane intro QSVT](https://pennylane.ai/demos/tutorial_intro_qsvt)
- Lecture-note sources to align terminology:
  - [Childs, Lecture Notes on Quantum Algorithms](https://www.cs.umd.edu/~amchilds/qa/)
  - [de Wolf](https://arxiv.org/abs/1907.09415)
  - [Lin Lin, "Lecture Notes on Quantum Algorithms for Scientific Computation"](https://arxiv.org/abs/2201.08309)
  - [Dalzell et al., "Quantum algorithms: A survey of applications and end-to-end complexities" (2023; CUP 2025)](https://arxiv.org/abs/2310.03011)
  - [Jordan's Quantum Algorithm Zoo](https://quantumalgorithmzoo.org/)
- "Compiled" factoring/QPE demos can be misleading — [Smolin, Smith, Vargo 2013](https://arxiv.org/abs/1301.7007)

### Inferences
Misconception → corrective demo mapping:

| Misconception | Corrective idea | Demo hook |
|---|---|---|
| "Tries all answers in parallel" | Only interference patterns are readable; measurement yields one sample | Path-sum explorer: show the individual Feynman paths and their cancellation in a 3-qubit circuit |
| "Grover is exponential" / "QC solves NP-complete" | BBBV Omega(sqrt N); Bernstein-inequality steepness | QSP designer: try to make P(1/sqrt N) ~ 1 with low degree and fail |
| "Grover needs to know the answer" | The oracle *recognises*, it does not *know*; verify vs find | Let users write a predicate (e.g. a SAT clause) compiled to a phase oracle |
| "QFT = fast FFT" | Coefficients are amplitudes; one sample per run | Phase-wheel view plus a sampling histogram |
| "QPE gives any eigenvalue exponentially fast" | Needs eigenstate overlap, controlled-U^{2^j} cost, no compiled cheats | Honest vs compiled QPE cost counter |
| "HHL/QML = exponential speedup" | Aaronson's fine print; Tang dequantization | Checklist overlay on an HHL-as-QSVT 1/x polynomial |
| "No barren plateau = good model" | BP-free ↔ small DLA ↔ often classically simulable (Cerezo 2025) | Variance-vs-n plot with a DLA-dimension overlay |
| "Advantage has been shown, so QC is useful now" | Sampling vs verifiable vs useful; spoofing history | XEB spoofing mini-lab |
| "Superposition = we just don't know" | Superposition ≠ mixture; interference distinguishes them | Same-populations states: H|+> vs H applied to a 50/50 mixture |

- A novel framing for the hackathon's "fresh angle" requirement: **"Every quantum algorithm is a polynomial"**. QSP/QSVT turns algorithm design into polynomial design and lower bounds into polynomial-approximation limits (Markov/Bernstein inequalities). One interactive plot does both, and the circuits cost no two-qubit gates, so they run well on IonQ noise models.

### Gaps
- I found no rigorous education-research study that targets the phrase "tries all answers in parallel" specifically; the evidence is expert commentary plus adjacent PER studies.
- I did not assess which existing web tools (Quirk, IBM Composer, Quantum Odyssey) already offer QSP-like visualisations. The search found no interactive QSVT designer, but it was not exhaustive.

---

## Q6. Concrete interactive demos that run under the constraints (qubit counts, 2Q gate counts, expected behaviour at about 0.5% 2Q error)

### Takeaway
The best demos for the constraints:
1. a **QSP/QSVT polynomial designer** (0 two-qubit gates for the scalar version; about 3 per degree for a 1-ancilla block-encoded 2-qubit matrix);
2. a **Trotter "sweet-spot" lab** with native ZZ (5-15 ZZ per step), showing that algorithmic error (∝ 1/r^p) and hardware error (∝ r) trade off at an optimal step count;
3. **QFT-free phase and amplitude estimation** (1 ZZ per Hadamard test; MLAE with about 20 2Q per Grover operator), batched in parallel registers into one job;
4. quantum-walk spreading with decoherence-induced ballistic-to-diffusive crossover;
5. classical shadows;
6. barren-plateau variance plots with Lie-algebra overlays;
7. a Forrelation (Raz-Tal) experiment.

All the gate counts below are my own derivations from the identities listed. They need confirming with Qiskit's transpiler targeting IonQ natives.

### Cited Findings
- Hackathon constraints (as given by the user/organiser brief): Qiskit 2.x in Pyodide; qiskit-algorithms 0.4, qiskit-optimization 0.7, qiskit-nature 0.8, qiskit-finance 0.4.1 and qiskit-machine-learning 0.9.1 available; IonQ noise models up to 29 qubits; no dynamic circuits; one job per run; natives GPi, GPi2, ZZ(theta); all-to-all connectivity; about 100 2Q gates. (User-provided; not independently verified.)
- Theory each demo relies on:
  - Trotter commutator bounds — [Childs et al. 2021](https://arxiv.org/abs/1912.08854)
  - qDRIFT — [Campbell 2019](https://arxiv.org/abs/1811.08017)
  - MLAE — [Suzuki et al. 2020](https://arxiv.org/abs/1904.10246); noisy MLAE — [Tanaka et al. 2021](https://arxiv.org/abs/2006.16223)
  - Single-ancilla, non-adaptive QPE — [Kimmel-Low-Yoder 2015](https://arxiv.org/abs/1502.02677); [Ding-Lin 2023](https://arxiv.org/abs/2211.11973)
  - Classical shadows — [HKP 2020](https://arxiv.org/abs/2002.08953)
  - BP variance — [McClean 2018](https://arxiv.org/abs/1803.11173); [Cerezo 2021](https://arxiv.org/abs/2001.00550); [Wang 2021](https://arxiv.org/abs/2007.14384); [Ragone 2024](https://arxiv.org/abs/2309.09342)
  - Quantum-walk decoherence — [Kendon 2006](https://arxiv.org/abs/quant-ph/0606016)
  - LR-QAOA, which needs no classical optimiser loop, so one job suffices — [Montañez-Barrera & Michielsen 2025](https://arxiv.org/abs/2405.09169)
  - Forrelation — [Aaronson & Ambainis 2015](https://arxiv.org/abs/1411.5729); [Raz & Tal 2018](https://eccc.weizmann.ac.il/report/2018/107/)
- qiskit-algorithms provides `PhaseEstimation`, `IterativePhaseEstimation`, `HamiltonianPhaseEstimation`, `AmplitudeEstimation`, `MaximumLikelihoodAmplitudeEstimation`, `IterativeAmplitudeEstimation`, `FasterAmplitudeEstimation`, `EstimationProblem` and `Grover`. (From my knowledge of the library; I did not re-check the 0.4 API in this session.)
- Derandomized shadows remove the per-snapshot random basis — [HKP 2021](https://arxiv.org/abs/2103.07510). Useful because "one job per run" makes many random bases awkward.

### Inferences

**Useful IonQ-native identities (derived):**
- CP(lambda) = e^{i lambda/4} · RZ(lambda/2) ⊗ RZ(lambda/2) · RZZ(-lambda/2), so **any controlled-phase costs exactly 1 ZZ**. The full QFT on t qubits therefore costs t(t-1)/2 ZZ with no SWAPs (relabel outputs).
- CNOT and CZ cost 1 native 2Q gate each.
- e^{-i theta (XX+YY)/2} = RXX(theta)·RYY(theta), and the two commute, so it costs **2** natives exactly.
- A weight-w Pauli rotation e^{-i theta Z^{⊗w}/2} costs 2w-3 natives (CNOT ladder to w-2, then one RZZ): 1, 3, 5, 7 for w = 2, 3, 4, 5.
- A Boolean phase oracle (-1)^{f(x)} equals the product over subsets S of e^{-i(pi/2) f_hat(S) Z_S} (Walsh expansion). A dense 4-variable function costs at most 6·1 + 4·3 + 1·5 = **23** natives.
- CCZ costs 6 natives (phase polynomial: three weight-2 terms plus one weight-3 term).

**D1. QSP Polynomial Studio ("Every algorithm is a polynomial")**
- *Concept:* sliders or a target picker (sign, threshold, Chebyshev T_{2k+1}, fixed-point AA, e^{-i tau x}, 1/x). Phases are solved in-browser (numpy Dong-Lin-style optimiser, or pyqsp if it loads). The tool plots the target, the ideal |P(a)|^2 and the measured |P(a)|^2.
- *Circuit:* 1 qubit per signal value: Rz(phi_0) followed by d pairs of [Rx(-2 arccos a), Rz(phi_k)] (or the Wx convention). Batch 29 signal values on 29 qubits **in one circuit** (one job, no entanglers).
- *2Q gates:* **0**. Single-qubit count 2d+1 (Z rotations are likely virtual on IonQ; unverified).
- *Noise expectation:* insensitive to the 0.5% 2Q error. Limited by single-qubit error (about 1e-4 to 1e-3 per gate, unverified) and SPAM (about 0.5%) plus shot noise sigma = sqrt(p(1-p)/S), about 1.6% at S = 1000. Degree up to about 50 should still show clean curves.
- *Lessons:*
  - Grover = T_{2k+1}.
  - Fixed-point AA avoids the soufflé overshoot.
  - Lower-bound mini-game: "make P(0.1) ≥ 0.9 with |P| ≤ 1"; Bernstein forces d ≥ 9 (the analogue of sqrt N = 10).
  - Jacobi-Anger degree grows with |tau|; 1/x degree grows with kappa.

**D2. QSVT on a real block encoding (2 system qubits + 1 ancilla)**
- LCU block encoding of H = c1 Z_0 + c2 X_0 X_1: PREP = RY on the ancilla; SELECT = (anc=0) controlled-Z_0 (1 native) and (anc=1) controlled-X_0X_1 (2 natives). That is **3 2Q gates per block-encoding call**. The projector phases e^{i phi(2 Pi - I)} with Pi = |0><0|_anc are single-qubit Z rotations on the ancilla.
- *Degree d:* about 3d 2Q gates. d = 9 → 27 (F ~ 0.87); d = 15 → 45 (F ~ 0.80); d = 21 → 63 (F ~ 0.73). Qubits: 3, and up to about 9 parallel copies in 29 qubits for different input eigenstates.
- *Noise expectation:* post-selection on ancilla = 0 is required. Depolarizing noise pushes the ancilla toward 50/50, so the post-selected output is a mixture of the polynomial-filtered state and noise. Eigenvalue thresholding should stay visible up to d ~ 15.
- *Lesson:* the same phases from D1 now act on matrix eigenvalues (here, singular values of H/lambda).

**D3. Trotter sweet-spot lab (native ZZ)**
- *Model A:* transverse-field Ising chain, n = 6. A first-order step is 5 RZZ + 6 RX, i.e. **5 ZZ per step**. A second-order (Strang) step merges half-steps, so it costs r·5 + 5 ZZ, **about the same 2Q count** with error O(t^3/r^2). r = 1..20 → 5..100 ZZ.
- *Model B (IonQ showcase):* all-to-all Ising, n = 6 → 15 ZZ per step, about 6 steps within budget. Transpile the same step for IBM heavy-hex in-browser and show the SWAP overhead.
- *Error model:* the first-order commutator bound for TFIM is ε ≤ (t^2/2r)·sum ||[ZZ_{i,i+1}, X_j]||, i.e. about 2(n-1)|Jh| t^2/r (loose). Hardware error is about 1 - 0.995^{5r} ≈ 0.025r. Total ≈ a/r + b·r with optimum r* ≈ sqrt(a/b). The "sweet spot" should appear around r ≈ 4-10 for t ≈ 1-2, J = h = 1 (to be confirmed numerically).
- *Exact reference:* scipy `expm` on a 64x64 matrix is trivial in Pyodide.
- *Extensions:* qDRIFT (random term sampling; error ∝ lambda^2 t^2/N, independent of term count). Note that qDRIFT needs many random circuits; with one job, place several random compilations in parallel registers or use the simulator. Also overlay the commutator bound against the actual error to show how loose worst-case bounds are.

**D4. "Phase estimation without the QFT": precision against noise**
- *Textbook QPE*, U = P(2 pi phi) on 1 target qubit, t ancillas: t controlled-U^{2^j} (each 1 ZZ when U^{2^j} is a compiled phase; label this "compiled") plus a t(t-1)/2-ZZ inverse QFT. t = 4 → 10 ZZ; t = 6 → 21; t = 8 → 36 (F ~ 0.83); t = 10 → 55 (F ~ 0.76). Approximate QFT with b = 3 cuts t = 10 to about 10 + 24.
- *Single-ancilla Hadamard tests* (Kitaev/RPE/QCELS): each test is 2 qubits and 1 ZZ (compiled) and gives cos or sin of 2^j·2 pi phi. Put about 14 tests in parallel on 28 qubits in one job, then use classical RPE/Bayesian post-processing.
- *Honest version (multi-qubit U):* U = e^{-iHt} for a 2-qubit Heisenberg H. Controlled-U costs about 3-6 natives per Trotter step, and controlled-U^k needs k repetitions. Precision ε ~ 1/(total evolution time), but under 0.5% error the useful maximum k is about 1/(p·c), roughly 15-30, which gives a **precision floor**. Plot error against maximum depth: noiseless follows 1/K; noisy is U-shaped.
- *Lesson:* Heisenberg limit against noise; why early-fault-tolerant algorithms (Lin-Tong, QCELS) avoid the QFT.

**D5. Amplitude estimation without QPE (MLAE), finance or counting flavour**
- *Toy:* A = RY(2 theta) on 1 qubit, so Q is a single-qubit rotation and the cost is **0 2Q gates**. This isolates the statistics: error against total queries, slope -1 (Heisenberg) against -1/2 (Monte Carlo).
- *Realistic:* A = 3-qubit distribution loader (about 2-4 2Q) plus an objective qubit with controlled RY (about 2 2Q). Q = A S_0 A^-1 S_chi, where S_chi is single-qubit Z on the objective qubit and S_0 is a 4-qubit reflection about |0000> (C3Z, about 23 natives without an ancilla, about 12-14 with one). Q ≈ 20-30 2Q gates.
  - Schedule m = {0, 1, 2, 3}: largest circuit about 60-90 2Q.
  - Schedule m = {0, 1, 2, 4}: up to about 100-120 2Q (over budget).
  - Fit the parallel-register layout: 5 qubits × up to 5 schedules ≈ 25 qubits in one job.
- *Noise expectation:* P(good) after m Grover steps decays toward 1/2 as roughly e^{-gamma m}. An unmodelled MLAE estimate becomes **biased**. Adding the noise parameter to the likelihood (Tanaka et al.) restores consistency. The plot shows a "knee" where noise ends the Heisenberg slope; the power-law AE dial (Giurgica-Tiron) is the principled response.

**D6. Quantum walk: ballistic vs diffusive, and decoherence**
- *Option A (one-hot / XY chain):* N = 12 sites on 12 qubits, one excitation. Hopping e^{-i theta(XX+YY)/2} costs 2 natives per edge, so a Trotter step over 11 edges costs 22 2Q. 4 steps → 88 2Q (F ~ 0.64).
  - *Built-in error detection:* post-select Hamming weight 1, because errors leak out of the 1-excitation subspace.
  - *Physics:* CTQW on a line has amplitudes i^x J_x(2t) (Bessel), so sigma = sqrt(2)·t (ballistic), against sigma = sqrt(t) for a classical random walk. Noise produces Kendon's ballistic-to-diffusive crossover, which is a natural visual for "what noise does".
  - *Honesty note:* one-hot uses N qubits for N nodes and the XY chain is free-fermion (classically simulable). Use it to teach why encoding matters for exponential speedups (glued trees need compact encoding plus oracle access).
- *Option B (binary encoding, fast-forwarding):* a cycle of 16 nodes on 4 qubits. e^{-iAt} = QFT^dagger · diag(e^{-2it cos(2 pi k/16)}) · QFT. Each QFT costs 6 ZZ, and the diagonal phase is built from Z_S rotations (≤ 23 natives). That is **about 35 2Q gates for any t**. This teaches fast-forwarding of circulant Hamiltonians against no-fast-forwarding in general.

**D7. Classical shadows: many observables from few measurements**
- *State:* GHZ-n or 1D cluster state, n = 8-12 (n-1 2Q gates; F ~ 0.95 for n = 10).
- *Measurement:* random local Pauli bases. Estimate all k ≤ 2 Pauli expectations (for n = 10: 3·10 + 9·45 = 435 observables), stabilisers and entanglement witnesses.
- *Sample complexity:* single-snapshot variance ≤ 3^k = 9 for k = 2, so ε ≈ 3/sqrt(N). N = 1000 gives ε ≈ 0.1, and N = 10,000 gives about 0.03. The HKP worst-case bound with log M is much looser; show both.
- *One-job workaround:* (i) derandomized shadows (a fixed basis list); (ii) parallel copies, e.g. 5 copies of a 5-qubit GHZ on 25 qubits, each with an independent random basis, plus many shots (an N_U × N_M estimator); (iii) simulator for the full random-basis version.
- *Noise:* stabiliser expectations shrink by roughly F. Robust-shadow calibration corrects measurement noise.
- *Lesson:* "measure first, ask later". Show that full tomography needs 3^n bases against log M scaling.

**D8. Barren plateau explorer (simulator; small-n noisy runs on IonQ model)**
- *Ansatz:* hardware-efficient with L layers of RY, RZ and an (n-1)-CZ ladder (n-1 2Q per layer); n = 2..14 (statevector in Pyodide). Use 200 random theta samples and parameter-shift gradients (2 circuits each).
- *Costs:* global C = 1 - P(0^n) against local C = 1 - (1/n) sum_i P(0_i).
- *Expected plots:* log Var[dC] against n. Global cost decays with slope about -ln 2 per qubit (≈ 2^{-n}). Local cost at shallow depth decays only polynomially.
- *Noise-induced BP:* with the IonQ noise model at n = 6 and L = 1..15 (5..75 2Q), variance decays exponentially in L even for the local cost.
- *DLA overlay:* compute dim(g) numerically by Lie closure for n ≤ 5. Show Var ∝ 1/dim(g), and that a matchgate/XY ansatz (dim so(2n) = n(2n-1)) has no BP **and** is classically simulable (the Cerezo 2025 punchline).

**D9. Forrelation: the BQP vs PH separation as an experiment**
- n = 4. Circuit H^4 · O_f · H^4 · O_g · H^4, measure P(0000) = Phi^2. Two dense phase oracles cost up to 2 × 23 = **46 2Q (F ~ 0.79)**. Raz-Tal-style correlated pairs give |Phi| large, independent random pairs give |Phi| about 0.
- A Hadamard-test variant with one control gives (1+Phi)/2 but needs controlled oracles, which costs more.
- Run n = 4 on hardware and n up to about 12 in the simulator. Show classical query cost growing like sqrt N against 2 quantum queries.

**D10. Simon → Shor → DQI ladder ("hidden structure + Fourier = speedup")**
- *Simon* with n = 3-6 on 2n ≤ 12 qubits; oracle about n + |s| CNOTs (≤ 12 2Q, F ≥ 0.94). Live GF(2) Gaussian elimination against a classical birthday-collision counter (~2^{n/2}).
- Link to period finding. Show an "honest vs compiled" cost counter for N = 15/21 modular exponentiation and the 2025-26 RSA/ECDLP resource estimates (Gidney <1M qubits; Pinnacle <100k claimed; ECDLP <500k).
- *DQI* as a simulator-only toy: m = 8 constraints, n = 4 variables, decoding radius l = 1. The reversible decoder makes it about 100-200 2Q, so hardware is impractical. Plot the analytic semicircle law against random assignment and simulated annealing, and show the 2025-26 classical responses.

**D11. QAOA as Trotterised adiabatic evolution (LR-QAOA, one job, no optimiser)**
- 8-node 3-regular MaxCut: 12 edges → **12 ZZ per layer**. p = 1..8 → 12..96 ZZ (F(96) ~ 0.62).
- Plot P(optimal cut) against p, noiseless vs noisy. Overlay the exact instantaneous spectrum of H(s) (2^8 = 256-dimensional, cheap to diagonalise) to show how the minimum gap sets the needed p, and where noise caps p.
- No variational loop means a single job; this fits the constraint.

**Summary table (derived estimates; confirm with the transpiler):**

| Demo | Qubits | 2Q gates (max circuit) | Est. F at 0.5% | Hardware-viable? |
|---|---|---|---|---|
| D1 QSP studio | 1 per point (≤29 parallel) | 0 | ~SPAM-limited | Yes (excellent) |
| D2 QSVT 2+1 | 3 (×9 parallel) | 27-63 (d = 9-21) | 0.87-0.73 | Yes (d ≤ 15 best) |
| D3 Trotter TFIM n=6 | 6 | 5r (r ≤ 20) | 0.97-0.61 | Yes (core lesson) |
| D3b all-to-all Ising | 6 | 15/step | ~0.93/step | Yes (IonQ showcase) |
| D4 textbook QPE t=8 | 9 | 36 | 0.83 | Yes |
| D4 Hadamard tests | 2 each (14 parallel) | 1 each (compiled) | ~0.99 | Yes |
| D5 MLAE realistic | ~5 (×5 parallel) | 60-90 | 0.74-0.64 | Marginal; noise-aware fit needed |
| D6A walk one-hot N=12 | 12 | 22/step (88 at 4 steps) | 0.64 (+ post-select) | Yes |
| D6B cycle via QFT | 4 | ~35 any t | ~0.84 | Yes |
| D7 shadows GHZ-10 | 10 | 9 | 0.96 | Yes (basis-randomisation caveat) |
| D8 BP explorer | 2-14 | (n-1)L | n/a (simulator) | Simulator plus small noisy runs |
| D9 Forrelation n=4 | 4 | ≤46 | 0.79 | Yes |
| D10 Simon n=4 | 8 | ~8 | 0.96 | Yes |
| D11 LR-QAOA 8 nodes | 8 | 12p (≤96) | 0.94-0.62 | Yes |

### Gaps
- All gate counts above are hand derivations, not transpiler outputs. Single-qubit gate errors, SPAM, crosstalk between parallel registers, and whether IonQ's ZZ(theta) error depends on theta were not verified.
- The "one job per run" rule's exact meaning (whether a job may contain several circuits, as some IonQ multi-circuit jobs allow) was not confirmed. It decides whether parallel-register batching is needed or only nice to have.
- Pyodide performance limits (e.g. the cost of 14-qubit parameter-shift sweeps, and whether qiskit-algorithms estimators run without Aer) were not benchmarked.
- The DQI semicircle-law formula quoted in Q2's inferences must be checked against the paper before it goes into the tool.
