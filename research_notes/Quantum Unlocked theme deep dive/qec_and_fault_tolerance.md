# Quantum Error Correction and Fault Tolerance: Technical Knowledge Base for a Teaching Tool (state as of Oct 2026)

Scope notes for the report writer:
- Results from 2025 and 2026 are tagged **[2025]** or **[2026]**. Untagged results are pre-2025 and well established.
- Anything labelled **[own sim]** was computed in this research session with a pure-numpy Pauli-frame simulator. The Clifford-only parts were cross-checked against qiskit-aer 0.17.2 (stabilizer and density-matrix methods). These are model estimates, not literature values. The noise model, used throughout unless stated otherwise: depolarizing p2 after every CNOT, p1 = p2/10 after every 1-qubit gate, symmetric readout flip pm = p2, no idle noise. Idle noise is a reasonable omission for trapped ions, which have long coherence, but not for superconducting qubits.
- Build environment assumed: Qiskit 2.x in Pyodide, IonQ Forte noise model (p2 ≈ 0.0049, ≤29 qubits), no feed-forward, limited mid-circuit measurement, one job per run.

---

## 1. Foundations: classical vs quantum errors, Knill–Laflamme, bounds, stabilizer formalism, Gottesman–Knill, tableaus, CSS

### Takeaway
The whole field rests on three ideas. (i) You cannot copy a quantum state (no-cloning), so you encode it into an entangled subspace instead. (ii) Measuring commuting Pauli "checks" (stabilizers) projects arbitrary continuous noise onto a discrete set of Pauli errors without revealing the logical information. (iii) Codes built from Pauli stabilizers and Clifford circuits are classically simulable (Gottesman–Knill, Aaronson–Gottesman tableaus, Stim's Pauli frames). That is why QEC can be taught, simulated and decoded at scale on a laptop or in a browser.

### Cited Findings

**Why quantum is different from classical repetition**
- No-cloning: no unitary maps |ψ⟩|0⟩ → |ψ⟩|ψ⟩ for all |ψ⟩. The 3-qubit "repetition" code therefore encodes α|0⟩+β|1⟩ → α|000⟩+β|111⟩, an entangled state, not |ψ⟩⊗3. — [Wootters & Zurek, Nature 299, 802 (1982)](https://doi.org/10.1038/299802a0)
- Quantum errors are continuous and come in two conjugate types (bit flips X and phase flips Z). Measurement disturbs the state, so error information must be extracted by measuring only parities (syndromes), never the data itself. — [Preskill, Ph219 Lecture Notes ch. 7](http://theory.caltech.edu/~preskill/ph229/notes/chap7.pdf); [Gottesman, "An Introduction to QEC and Fault-Tolerant QC", arXiv:0904.2557 (2009)](https://arxiv.org/abs/0904.2557)
- Discretization of errors: any single-qubit operator can be written E = e₀I + e₁X + e₂Y + e₃Z. Syndrome measurement projects the corrupted state onto one Pauli branch, so a code that corrects the Pauli errors {I, X, Y, Z} on any t qubits corrects arbitrary (including coherent and continuous) errors on t qubits. The same linearity argument extends to any error set that is a linear span of correctable errors. — [Gottesman arXiv:0904.2557](https://arxiv.org/abs/0904.2557); [Preskill ch. 7](http://theory.caltech.edu/~preskill/ph229/notes/chap7.pdf)

**Knill–Laflamme conditions, distance, bounds**
- Knill–Laflamme (KL) conditions: a code with projector P can correct the error set {E_a} iff P E_a† E_b P = c_ab P for some Hermitian matrix c_ab. Equivalently ⟨ī|E_a†E_b|j̄⟩ = c_ab δ_ij: errors may not distinguish codewords, and they must map orthogonal codewords to orthogonal states. If c_ab is singular, the code is **degenerate**: distinct errors act identically on the code space, so they need not be distinguished. — [Knill & Laflamme, PRA 55, 900 (1997), quant-ph/9604034](https://arxiv.org/abs/quant-ph/9604034); [Bennett, DiVincenzo, Smolin, Wootters, quant-ph/9604024](https://arxiv.org/abs/quant-ph/9604024)
- [[n,k,d]] notation: n physical qubits, k logical qubits, and distance d. d is the minimum weight of a Pauli that acts non-trivially on the code space; for stabilizer codes this is min wt(N(S) \ S). A distance-d code corrects t = ⌊(d−1)/2⌋ arbitrary errors, detects up to d−1 errors, and corrects d−1 erasures (errors at known locations). — [Gottesman PhD thesis, quant-ph/9705052 (1997)](https://arxiv.org/abs/quant-ph/9705052)
- Quantum Hamming bound (non-degenerate codes): 2^k · Σ_{j=0}^{t} C(n,j)·3^j ≤ 2^n. For k=1, t=1 this gives 2(1+3n) ≤ 2^n, so n ≥ 5. The [[5,1,3]] code saturates it (2·16 = 32 = 2⁵), so it is "perfect". — [Ekert & Macchiavello, PRL 77, 2585 (1996), quant-ph/9602022](https://arxiv.org/abs/quant-ph/9602022); [Laflamme, Miquel, Paz, Zurek, quant-ph/9602019](https://arxiv.org/abs/quant-ph/9602019)
- Quantum Singleton bound: n − k ≥ 2(d − 1). [[5,1,3]] meets it with equality. — [Knill & Laflamme quant-ph/9604034](https://arxiv.org/abs/quant-ph/9604034)

**Stabilizer formalism**
- Pauli group P_n = {±1, ±i} × {I,X,Y,Z}^{⊗n}. A stabilizer group S is an abelian subgroup of P_n with −I ∉ S. The code space is V_S = {|ψ⟩ : s|ψ⟩ = |ψ⟩ ∀ s∈S}. With r = n−k independent generators, dim V_S = 2^k. — [Gottesman thesis](https://arxiv.org/abs/quant-ph/9705052)
- Logical operators are elements of the normalizer (= centralizer, for Pauli groups) N(S) that are not in S. Logical X̄_i, Z̄_i are chosen to satisfy the Pauli algebra. Two logical operators differing by a stabilizer act identically on the code space; this is the origin of degeneracy. — [Gottesman thesis](https://arxiv.org/abs/quant-ph/9705052)
- Syndrome: for a Pauli error E and generator g_i, the syndrome bit is s_i = 1 iff E anticommutes with g_i. Errors in the same coset E·S give the same syndrome and need the same correction. Errors E·L (L a logical) give the same syndrome but need a different correction; a decoder that confuses them causes a logical error. — [Gottesman arXiv:0904.2557](https://arxiv.org/abs/0904.2557)
- Binary symplectic representation: a Pauli maps to (x|z) ∈ F₂^{2n}. Two Paulis commute iff x·z′ + z·x′ = 0 mod 2. A code is described by a check matrix H = [H_X | H_Z], and syndrome = H·(symplectic error). This turns QEC into linear algebra over GF(2), which is also how decoders are implemented. — [Gottesman thesis](https://arxiv.org/abs/quant-ph/9705052)

**Clifford group, Gottesman–Knill, tableau simulation**
- Gottesman–Knill theorem: circuits made of Clifford gates (H, S, CNOT), computational-basis preparation, Pauli measurements and classical control can be simulated efficiently on a classical computer. — [Gottesman, "The Heisenberg Representation of Quantum Computers", quant-ph/9807006](https://arxiv.org/abs/quant-ph/9807006)
- The 2-qubit Clifford group has 11,520 elements modulo global phase. This sets the scale for Clifford randomized benchmarking, which is how "logical Clifford RB" numbers in experiments are produced. — [Córcoles et al., PRA 87, 030301 (2013), arXiv:1210.7011](https://arxiv.org/abs/1210.7011)
- Aaronson–Gottesman (CHP) tableau: store n stabilizers plus n destabilizers as a 2n×(2n+1) bit table. Each Clifford gate costs O(n) bit operations and each measurement O(n²); the destabilizers remove the O(n³) Gaussian elimination. — [Aaronson & Gottesman, PRA 70, 052328 (2004), quant-ph/0406196](https://arxiv.org/abs/quant-ph/0406196)
- Stim takes one reference sample from a tableau simulation and then propagates batches of Pauli "frames" (error differences) with SIMD bit-packing. This makes sampling QEC circuits orders of magnitude faster than a full tableau simulation per shot. Stim also derives "detector error models" from annotated circuits. — [Gidney, "Stim: a fast stabilizer circuit simulator", Quantum 5, 497 (2021), arXiv:2103.02202](https://arxiv.org/abs/2103.02202)

**CSS construction**
- Take classical linear codes C₂ ⊂ C₁. Then CSS(C₁, C₂) is an [[n, k₁−k₂, d ≥ min(d(C₁), d(C₂^⊥))]] code. X-type stabilizers come from the rows of the parity-check matrix of C₂^⊥ (equivalently the generators of C₂), and Z-type stabilizers from the parity-check matrix H₁ of C₁. The commutation condition is H_X·H_Zᵀ = 0. X and Z errors can then be decoded independently, which ignores Y correlations. — [Calderbank & Shor, quant-ph/9512032](https://arxiv.org/abs/quant-ph/9512032); [Steane, quant-ph/9601029](https://arxiv.org/abs/quant-ph/9601029)
- Steane [[7,1,3]] = CSS(Hamming[7,4,3], its dual [7,3,4]). Both X- and Z-checks use the Hamming parity-check matrix rows 0001111, 0110011, 1010101. — [Steane quant-ph/9601029](https://arxiv.org/abs/quant-ph/9601029)

### Inferences
- The most "teachable" bridge is the GF(2) symplectic picture. A browser tool can show a Pauli error as a coloured string, compute the syndrome as H·e, and animate the commute/anticommute rule. All of this is plain numpy, with no quantum simulation needed.
- Degeneracy is the conceptual cliff where classical intuition fails. Error E and error E·s (s ∈ S) are physically different but logically identical. A learner exercise could have the user find two different-looking corrections that both succeed.
- Tableau/frame simulation is the technical justification for running 20–100+ qubit QEC demos in a browser even though statevector simulation stops at ~24 qubits.

### Gaps
- I did not re-verify page/section numbers in Nielsen & Chuang ch. 10. The KL conditions and Hamming bound appear there (§10.3 and §10.3.1), but the citations above are to the primary papers instead.

---

## 2. The code zoo: repetition, Shor, Steane, [[5,1,3]], [[4,2,2]], surface/toric, color, Bacon–Shor, heavy-hex, qLDPC, bosonic, concatenated, Floquet, erasure

### Takeaway
Small codes ([[4,2,2]], [[5,1,3]], [[7,1,3]], [[9,1,3]]) are the pedagogical workhorses. The surface code (d² data + d²−1 ancillas, ~1% circuit threshold, nearest-neighbour checks) is the industrial baseline. Since 2024 the frontier has moved to high-rate qLDPC codes (IBM gross code [[144,12,12]], about 10× fewer qubits than the surface code), color codes (transversal Cliffords, magic-state cultivation), concatenated codes on trapped ions (Quantinuum Helios), and hardware-native tricks (cat qubits, erasure conversion, Floquet codes).

### Cited Findings

**Repetition and Shor codes**
- The 3-qubit bit-flip code (stabilizers Z₁Z₂, Z₂Z₃) corrects one X error but no Z errors. The phase-flip code is the same in the |±⟩ basis (checks X₁X₂, X₂X₃). Shor's [[9,1,3]] concatenates the two: |0̄⟩ = (|000⟩+|111⟩)^{⊗3}/2√2. It is degenerate, because e.g. Z₁Z₂ acts trivially. It was the first code to correct an arbitrary single-qubit error. — [Shor, PRA 52, R2493 (1995)](https://doi.org/10.1103/PhysRevA.52.R2493)
- Under independent bit flips with probability p and perfect syndromes ("code capacity"), the distance-3 repetition code's logical error is P_L = 3p²(1−p) + p³ = 3p² − 2p³. It beats a bare bit iff p < 1/2. — standard result; see [Preskill ch. 7](http://theory.caltech.edu/~preskill/ph229/notes/chap7.pdf)

**Steane, [[5,1,3]], [[4,2,2]]**
- Steane [[7,1,3]] (also the smallest 2D color code): 6 weight-4 generators. The whole Clifford group is transversal (H, S up to a known Pauli/inverse convention, CNOT between blocks); T is not transversal. — [Steane quant-ph/9601029](https://arxiv.org/abs/quant-ph/9601029); [Gottesman arXiv:0904.2557](https://arxiv.org/abs/0904.2557)
- [[5,1,3]]: generators XZZXI and its cyclic shifts. It is the smallest code correcting any single-qubit error, it is non-CSS, and it is perfect. — [Laflamme et al. quant-ph/9602019](https://arxiv.org/abs/quant-ph/9602019); [Bennett et al. quant-ph/9604024](https://arxiv.org/abs/quant-ph/9604024)
- [[4,2,2]]: stabilizers XXXX and ZZZZ. It detects (but cannot correct) any single-qubit error. Gottesman proposed it as the minimal platform for demonstrating fault tolerance, since qubit permutations and transversal gates implement logical gates (e.g. transversal H gives logical H⊗H plus a swap of the two logical qubits). — [Gottesman, "Quantum fault tolerance in small experiments", arXiv:1610.03507 (2016)](https://arxiv.org/abs/1610.03507)

**Surface / toric code**
- Kitaev's toric code on an L×L torus is [[2L², 2, L]]. Its vertex (X-star) and plaquette (Z-plaquette) checks have weight 4. Violated checks are anyons: e-particles (Z-check defects) and m-particles (X-check defects). Logical operators are non-contractible string operators. — [Kitaev, quant-ph/9707021](https://arxiv.org/abs/quant-ph/9707021); [Dennis, Kitaev, Landahl, Preskill, "Topological quantum memory", quant-ph/0110143](https://arxiv.org/abs/quant-ph/0110143)
- The planar code with boundaries (rough/smooth) encodes 1 qubit: [[L²+(L−1)², 1, L]] (unrotated). — [Bravyi & Kitaev, quant-ph/9811052](https://arxiv.org/abs/quant-ph/9811052)
- Rotated surface code: [[d², 1, d]] with d²−1 measure qubits, so 2d²−1 physical qubits in total (17 at d=3, 49 at d=5, 97 at d=7). — layout as in [Fowler, Mariantoni, Martinis, Cleland, PRA 86, 032324 (2012), arXiv:1208.0928](https://arxiv.org/abs/1208.0928). Google's d=7 Willow experiment used 101 qubits — [Google Quantum AI, arXiv:2408.13687](https://arxiv.org/abs/2408.13687)
- Fowler et al. scaling heuristic: P_L ≈ 0.03·(p/p_th)^{d_e} with d_e = ⌊(d+1)/2⌋ and p_th ≈ 0.57% for their circuit model with MWPM decoding. Reaching ~10⁻¹⁴–10⁻¹⁵ needs on the order of 10³–10⁴ physical qubits per logical qubit at p ≈ 10⁻³. — [Fowler et al. arXiv:1208.0928](https://arxiv.org/abs/1208.0928)
- Commonly quoted circuit-level thresholds: ~0.75% (Raussendorf–Harrington), ~1.1% with weighted matching (Wang–Fowler–Hollenberg). — [Raussendorf & Harrington, quant-ph/0610082](https://arxiv.org/abs/quant-ph/0610082); [Wang, Fowler, Hollenberg, arXiv:1009.3686](https://arxiv.org/abs/1009.3686)
- The error-suppression factor Λ = ε_d/ε_{d+2} ≈ p_th/p is the experimental "below threshold" metric. Willow measured Λ = 2.14 ± 0.02. — [arXiv:2408.13687](https://arxiv.org/abs/2408.13687)

**Color codes**
- 2D color codes (on 3-colourable lattices: 4.8.8, 6.6.6) have the full Clifford group transversal. 3D color codes have transversal T but not H. — [Bombin & Martin-Delgado, PRL 97, 180501 (2006), quant-ph/0605138](https://arxiv.org/abs/quant-ph/0605138)
- Gauge color codes allow switching between 2D and 3D gauge fixings to get a universal fault-tolerant gate set without distillation. — [Bombin, arXiv:1311.0879](https://arxiv.org/abs/1311.0879)
- **[2025]** Google color code on Willow (d=3 → 5): Λ_{3/5} = 1.56 (vs 2.31 for its surface-code comparison); magic-state injection into a color-code logical qubit at ~99% fidelity; logical entanglement/state transfer via lattice surgery at 86–91% fidelity; a logical Hadamard taking ~20 ns. Blog dated June 23, 2025; Nature DOI 10.1038/s41586-025-09061-4. — [Google Research blog, "A colorful quantum future"](https://research.google/blog/a-colorful-quantum-future/)

**Subsystem codes: Bacon–Shor, heavy-hex**
- Bacon–Shor [[m², 1, m]] on an m×m grid. Gauge operators are weight-2 (XX between neighbours in one direction, ZZ in the other); stabilizers are products of gauge operators over two adjacent rows/columns. Measuring only weight-2 operators simplifies the circuits. — [Bacon, quant-ph/0506023](https://arxiv.org/abs/quant-ph/0506023)
- Heavy-hex code: a hybrid of surface code and Bacon–Shor on a degree-2/3 lattice that uses flag qubits. It was designed for IBM's heavy-hex hardware to reduce frequency collisions and crosstalk. — [Chamberland, Zhu, Yoder, Hertzberg, Cross, PRX 10, 011022 (2020), arXiv:1907.09528](https://arxiv.org/abs/1907.09528)

**qLDPC codes**
- Review: qLDPC codes have bounded check weight and bounded qubit degree, and can achieve k, d growing with n. 2D-local codes are constrained by the BPT/Bravyi–Poulin–Terhal bounds, so good qLDPC codes need long-range connectivity. — [Breuckmann & Eberhardt, PRX Quantum 2, 040101 (2021), arXiv:2103.06309](https://arxiv.org/abs/2103.06309)
- Hypergraph product (HGP): from two classical codes it builds a quantum code with k ∝ n and d ∝ √n. — [Tillich & Zémor, arXiv:0903.0566](https://arxiv.org/abs/0903.0566)
- Asymptotically good qLDPC codes (k ∝ n and d ∝ n) via lifted products. — [Panteleev & Kalachev, STOC 2022, arXiv:2111.03654](https://arxiv.org/abs/2111.03654). Quantum Tanner codes are an alternative construction — [Leverrier & Zémor, arXiv:2202.13641](https://arxiv.org/abs/2202.13641)
- Constant-overhead fault tolerance is possible with qLDPC codes. — [Gottesman, arXiv:1310.2984](https://arxiv.org/abs/1310.2984)
- IBM bivariate bicycle (BB) "gross" code [[144,12,12]] ("gross" = 144). It uses 288 physical qubits (144 data + 144 check) to protect 12 logical qubits for ~1 million syndrome cycles at p = 0.1%; the surface code would need ~3,000 qubits for the same. Circuit-level threshold 0.8%, depth-7 syndrome circuit, degree-6 connectivity that decomposes into two planar subgraphs (thickness 2). Nature 627, 778 (2024). — [Bravyi et al., arXiv:2308.07915](https://arxiv.org/abs/2308.07915)
- **[2025]** IBM "Tour de gross" describes a modular architecture based on BB codes. — [Yoder et al., arXiv:2506.03094](https://arxiv.org/abs/2506.03094) (title/ID from my own knowledge; not re-fetched in this session)
- **[2026]** IonQ ran a BB-family "BB5" qLDPC code with 4 logical qubits in 18 physical ions on hardware (details in §5). — [Quantum Computing Report, June 6 2026 (arXiv:2606.06455)](https://quantumcomputingreport.com/experimental-demonstration-of-breakeven-qldpc-and-block-codes-on-a-trapped-ion-architecture/)

**Bosonic codes**
- GKP codes encode a qubit in an oscillator using grid states, protecting against small displacements. — [Gottesman, Kitaev, Preskill, quant-ph/0008040](https://arxiv.org/abs/quant-ph/0008040)
- GKP beyond break-even: real-time QEC of a GKP qubit exceeded the best passive encoding in the same cavity by a factor of ~2.3. — [Sivak et al., Nature 616, 50 (2023), arXiv:2211.09116](https://arxiv.org/abs/2211.09116)
- Cat qubits: two-photon-dissipation-stabilized cats have bit-flip rates suppressed exponentially in mean photon number, while phase flips grow only linearly. A repetition code against phase flips alone can therefore suffice. — [Mirrahimi et al., arXiv:1312.2017](https://arxiv.org/abs/1312.2017); [Guillaud & Mirrahimi, "Repetition cat qubits", arXiv:1904.09474](https://arxiv.org/abs/1904.09474)
- **[2025]** AWS Ocelot (Putterman et al., Nature 638, 927, Feb 27 2025): a phase-flip repetition code of 5 cat data qubits plus 4 transmon ancillas (9 qubits at d=5), 2.8 µs cycle. Minimum logical error per cycle was 1.75(2)% at d=3 and 1.65(3)% at d=5. Phase-flip error decreases with distance, while total error is roughly flat because bias suppresses bit flips. AWS projects ~0.5%/cycle with improvements. — [Caltech record](https://authors.library.caltech.edu/records/ydw1a-c2t23); [AWS summary via Quantum Computing Report](https://quantumcomputingreport.com/?p=28379); [paper arXiv:2409.13025](https://arxiv.org/abs/2409.13025)

**Concatenated codes**
- Concatenating a distance-3 code L times gives p^{(L)} ≈ p_th (p/p_th)^{2^L}. This yields the threshold theorem with polylogarithmic overhead. A rigorous lower bound ε_th ≥ 2.73×10⁻⁵ applies for concatenated distance-3 codes under local stochastic noise. — [Aliferis, Gottesman, Preskill, quant-ph/0504218](https://arxiv.org/abs/quant-ph/0504218)
- Knill's C4/C6 scheme (error-detecting codes, teleportation-based EC, heavy postselection) estimated thresholds of a few percent. — [Knill, Nature 434, 39 (2005), quant-ph/0410199](https://arxiv.org/abs/quant-ph/0410199)
- **[2025–2026]** Quantinuum Helios uses concatenated codes for a near-2:1 physical:logical ratio (98 physical → 48 error-corrected logical qubits). It also uses a [[20,2,6]] "C4-Helix" code built by concatenating a [[10,2,3]] twisted toric code with [[4,2,2]] blocks. — [HPCwire Nov 5 2025](https://www.hpcwire.com/2025/11/05/quantinuum-introduces-helios-quantum-system-as-roadmap-advances-toward-apollo/); [Quantum Computing Report on Helix](https://quantumcomputingreport.com/quantinuum-demonstrates-helix-quantum-error-correction-architecture-on-helios-hardware/)

**Floquet / dynamical codes**
- Honeycomb code: only weight-2 check measurements, in a period-3 schedule. The logical qubits are "dynamically generated": the instantaneous stabilizer group changes every round. — [Hastings & Haah, Quantum 5, 564 (2021), arXiv:2107.02194](https://arxiv.org/abs/2107.02194)
- Honeycomb memory thresholds: ~0.2–0.3% with standard (SD6) circuit noise, ~1.5–2.0% if native two-qubit parity measurements (EM3) are available. — [Gidney, Newman, Fowler, Broughton, arXiv:2108.10457](https://arxiv.org/abs/2108.10457)

**Erasure conversion**
- If most errors can be flagged as erasures (known location), thresholds rise sharply. For Yb Rydberg gates with 98% erasure fraction, the surface-code threshold rises from 0.937% to 4.15%. A distance-d code corrects d−1 erasures but only ⌊(d−1)/2⌋ unknown errors. — [Wu, Kolkowitz, Puri, Thompson, Nat. Commun. 13, 4657 (2022), arXiv:2201.03540](https://arxiv.org/abs/2201.03540)

**Microsoft 4D codes [2025]**
- Microsoft's 4D geometric codes are aimed at all-to-all-connected hardware (ions, atoms, photonics). Microsoft claims ~5× fewer physical qubits per logical qubit and a 10⁻³ → 10⁻⁶ error reduction. — [Microsoft Azure Quantum blog, June 19 2025](https://azure.microsoft.com/en-us/blog/quantum/2025/06/19/microsoft-advances-quantum-error-correction-with-a-family-of-novel-four-dimensional-codes/); [R&D World](https://www.rdworldonline.com/microsofts-4d-geometric-codes-slash-quantum-errors-by-1000x/)

### Inferences
- For an IonQ-targeted tool, all-to-all connectivity is the key differentiator. Codes that are "impossible" on a 2D superconducting chip (BB/gross, 4D geometric, [[5,1,3]], concatenated codes) become wiring-free on trapped ions. A teaching tool could show the same code's CNOT schedule on a square grid (with SWAP overhead) vs on all-to-all hardware.
- The cleanest scaling demonstration that fits ≤29 qubits is the repetition code. It is a "classical" code against one Pauli type, but Google used it up to d=29 as a serious experimental probe of correlated errors ([arXiv:2408.13687](https://arxiv.org/abs/2408.13687)).
- Cat qubits / Ocelot are a good teaching example that "biased noise changes which code you need".

### Gaps
- I could not confirm the exact qubit breakdown behind Willow's 101 qubits (2d²−1 = 97 is the code itself). I believe the extra 4 are leakage-removal qubits, but did not verify this.
- No primary-source [[n,k,d]] parameters were found for IonQ's BB5 [[18,4,?]] code. The distance was not stated in the secondary source.
- The Helios C4-Helix numbers come from secondary sources (Quantum Computing Report, quentir.ai); the arXiv preprint itself (Sept 2 2026) was not opened.

---

## 3. Decoding: noise models, detector error models, MWPM, union-find, BP+OSD, neural, correlated, real-time, leakage

### Takeaway
A decoder is a classical inference engine. It maps detection events (changes in stabilizer outcomes) to the most likely logical-class correction. Matching (MWPM/PyMatching) is the surface-code standard. Union-find trades a little accuracy for near-linear time. BP+OSD and IBM's Relay-BP target qLDPC codes. Neural decoders (AlphaQubit 1 and 2) beat matching on real data. Real-time throughput and latency are now hard engineering constraints: Google decodes with 63 µs latency on a 1.1 µs cycle, IBM reports <480 ns qLDPC decoding, and IonQ's [2026] single-CPU decoder has so far been shown in simulation.

### Cited Findings

**Noise models and thresholds (surface code)**
- Code capacity: only data errors, perfect syndrome measurement. Optimal threshold ~10.9% for independent X/Z noise (mapping to the random-bond Ising model); MWPM ~10.3%. Phenomenological: data errors plus syndrome-bit flips; MWPM ~2.9%, optimal ~3.3%. Circuit-level: every gate, idle, reset and measurement can fail; ~0.5–1%. — [Dennis et al. quant-ph/0110143](https://arxiv.org/abs/quant-ph/0110143); [Wang, Harrington, Preskill, quant-ph/0207088](https://arxiv.org/abs/quant-ph/0207088); [Fowler et al. arXiv:1208.0928](https://arxiv.org/abs/1208.0928)
- Under depolarizing code-capacity noise, the optimal (degenerate maximum-likelihood) surface-code threshold is ~18.9%. Exploiting X–Z (Y) correlations matters. — [Bombin et al., PRX 2, 021004 (2012), arXiv:1202.1852](https://arxiv.org/abs/1202.1852)
- Union-find decoder: almost-linear time O(n·α(n)), with a ~9.9% code-capacity threshold vs MWPM's 10.3%. — [Delfosse & Nickerson, arXiv:1709.06218](https://arxiv.org/abs/1709.06218)

**Detectors and detector error models (DEMs)**
- A detector is a parity of measurement outcomes that is deterministic in the absence of noise. Examples: the first-round Z-check outcome on |0…0⟩, the XOR of the same check in consecutive rounds, and the XOR of the last check with the matching parity of final data readout. A DEM lists independent error mechanisms, each with a probability, the set of detectors it flips and the logical observables it flips; it is a hypergraph. If every mechanism flips ≤2 detectors it is "graphlike" and can be decoded by matching. — [Stim DEM file-format documentation](https://github.com/quantumlib/Stim/blob/main/doc/file_format_dem_detector_error_model.md); [Gidney arXiv:2103.02202](https://arxiv.org/abs/2103.02202)

**Matching**
- PyMatching v2 implements "sparse blossom". It reports decoding circuit-level surface-code noise at p=0.1% up to d=17 in under ~1 µs per round on a single CPU core, and is 100–1000× faster than v1. — [Higgott & Gidney, arXiv:2303.15933](https://arxiv.org/abs/2303.15933); [PyMatching v1 paper, arXiv:2105.13082](https://arxiv.org/abs/2105.13082)
- Correlated matching re-weights the X and Z matching graphs using Y-error correlations. — [Fowler, arXiv:1310.0863](https://arxiv.org/abs/1310.0863)
- Correlated decoding across blocks lets transversal-gate algorithms use ~O(1) syndrome rounds per logical gate instead of O(d). — [Cain et al., "Correlated decoding of logical algorithms with transversal gates", arXiv:2403.03272](https://arxiv.org/abs/2403.03272)

**BP and BP+OSD (qLDPC)**
- Plain belief propagation fails on quantum codes because of degeneracy (many equally likely minimal errors split the beliefs) and short cycles. OSD post-processing (ordered-statistics, via Gaussian elimination, roughly O(n³)) fixes failures. — [Panteleev & Kalachev, "Degenerate quantum LDPC codes with good finite length performance", arXiv:1904.02703](https://arxiv.org/abs/1904.02703); [Roffe et al., "Decoding across the quantum LDPC code landscape", arXiv:2005.07016](https://arxiv.org/abs/2005.07016)
- **[2025]** IBM Relay-BP: BP with varied (including negative) memory strengths, chained "relay" legs and multiple candidate solutions. It significantly outperforms BP+OSD+CS-10 on BB codes ([[144,12,12]] gross, [[288,12,18]] two-gross), is comparable to MWPM on surface codes, and is inherently parallel (FPGA/ASIC friendly). — [arXiv:2506.01779](https://arxiv.org/abs/2506.01779)
- **[2025]** IBM reports real-time qLDPC decoding in <480 ns on classical hardware (announced with Loon, Nov 12 2025). — [IBM newsroom](https://newsroom.ibm.com/2025-11-12-ibm-delivers-new-quantum-processors,-software,-and-algorithm-breakthroughs-on-path-to-advantage-and-fault-tolerance); [The Quantum Insider](https://thequantuminsider.com/2025/11/12/ibm-reveals-new-quantum-processors-software-and-algorithm-advances/)

**Neural decoders**
- AlphaQubit (recurrent transformer) on Google Sycamore d=3/5 data made ~6% fewer errors than a tensor-network decoder and ~30% fewer than correlated matching. Nature 635, 834 (2024). — [Bausch et al., arXiv:2310.05900](https://arxiv.org/abs/2310.05900)
- **[2025]** AlphaQubit 2 (preprint posted Dec 8 2025): near-optimal logical error rates for surface and color codes at large distances. It decodes surface codes in real time (<1 µs per cycle) up to d=11 on commercial accelerators, and is the first real-time color-code decoder (to d=9). — [arXiv:2512.07737](https://arxiv.org/abs/2512.07737)

**Real-time decoding and the backlog problem**
- If the decoder processes syndrome data more slowly than it is produced, a backlog builds up. Logical non-Clifford gates must wait on decoded Pauli frames, so the waiting time grows exponentially with T-depth. Throughput must therefore match the syndrome rate, and latency adds to every feed-forward step. — [Terhal, Rev. Mod. Phys. 87, 307 (2015), arXiv:1302.3428](https://arxiv.org/abs/1302.3428)
- **[2024/2025]** Willow: average decoder latency 63 µs at d=5 against a 1.1 µs cycle, sustained over up to 1 million cycles. — [arXiv:2408.13687](https://arxiv.org/abs/2408.13687)
- **[2026]** IonQ (Sept 22 2026) claimed an "end-to-end real-time decoder" on a single conventional CPU. Benchmarks were **simulated** trapped-ion workloads of up to 408 logical qubits in 88 memory blocks plus magic factories, >31.5M operations, with a reported 0.02% overhead figure. A secondary write-up notes a worst-case decoding window of 41.86 ms vs a 15 ms budget at 5×10⁻⁴ error. — [IonQ investor release](https://investors.ionq.com/news/news-details/2026/IonQ-Demonstrates-Industrys-First-End-to-End-Real-Time-Quantum-Error-Decoder/default.aspx); [The Quantum Insider](https://thequantuminsider.com/2026/09/23/ionq-demonstrates-industrys-first-end-to-end-real-time-quantum-error-decoder/); [Wevolver](https://www.wevolver.com/article/real-time-quantum-error-decoding-single-cpu-408-logical-qubits)

**Leakage and correlated errors**
- Leakage (transmon |2⟩, an ion outside the qubit manifold, atom loss) is not a Pauli error and can spread. Leakage-reduction units convert it back. — [Aliferis & Terhal, quant-ph/0511065](https://arxiv.org/abs/quant-ph/0511065); [McEwen et al., Nat. Commun. 12, 1761 (2021), arXiv:2102.06131](https://arxiv.org/abs/2102.06131); [Miao et al., "Overcoming leakage in QEC", arXiv:2211.04728](https://arxiv.org/abs/2211.04728)
- Willow's repetition codes (to d=29) hit a floor set by rare correlated bursts, roughly once per hour (~3×10⁹ cycles). — [arXiv:2408.13687](https://arxiv.org/abs/2408.13687)
- **[2025]** The Harvard/QuEra 448-atom experiment used atom-loss detection plus machine-learning decoding to reach 2.14(13)× below-threshold suppression. — [arXiv:2506.20661](https://arxiv.org/abs/2506.20661); [Quantum Computing Report](https://quantumcomputingreport.com/harvard-and-collaborators-demonstrate-scalable-fault-tolerant-architecture-with-448-neutral-atom-qubits/)

### Inferences
- For a browser tool, MWPM is easy to implement without PyMatching. networkx 3.6.1 ships with Pyodide and has `max_weight_matching`. Precompute all-pairs shortest paths on the detector graph (Dijkstra), then match defects plus per-defect boundary copies. In this session that worked for repetition codes up to d=7 with 3 rounds (24 detectors), with caching by syndrome pattern.
- For d=3 surface code, a "learned maximum-likelihood lookup table" is the best pedagogical decoder. Sample N shots, count logical-flip frequency per detection pattern, then pick the majority. It is literally optimal in the large-sample limit, and it shows students that a decoder is just conditional probability. It is feasible for ≤ ~16 detector bits.
- Teaching the three noise models side by side (code capacity → phenomenological → circuit-level) on the same repetition code is high-impact. The threshold moves from 50% → ~a few % → ~1–3% for the repetition code, and learners see where the famous "1%" comes from.

### Gaps
- I did not find independent verification of IonQ's real-time decoder numbers. The arXiv ID of the IonQ decoder paper was not located in this session.
- Union-find and BP thresholds under circuit-level noise vary a lot by noise model, and I did not pin down canonical values.

---

## 4. Fault tolerance: syndrome extraction gadgets, flags, transversal gates, Eastin–Knill, magic states, distillation, cultivation, lattice surgery, code switching, threshold theorem, resource estimates

### Takeaway
Error correction is not fault tolerance. Syndrome-extraction circuits themselves spread errors: a single ancilla fault can become a weight-2 data error, a "hook". FT gadgets (Shor cat ancillas, Steane/Knill ancilla blocks, Chao–Reichardt flags) keep one fault from becoming an uncorrectable error. Eastin–Knill forbids a universal transversal gate set, so universality comes from magic states: distilled (15-to-1), cultivated (Gidney 2024; Google experiment Dec 2025), or obtained via code switching or gauge fixing. The resource frontier for RSA-2048 fell from 20M qubits (2019) to <1M (May 2025), and secondary reports claim <100k with qLDPC codes [2026].

### Cited Findings

**FT syndrome extraction**
- Shor-style EC: each stabilizer is measured with a verified cat-state ancilla using transversal CNOTs, repeated to guard against measurement errors. — [Shor, "Fault-tolerant quantum computation", quant-ph/9605011](https://arxiv.org/abs/quant-ph/9605011)
- Steane-style EC (CSS codes): prepare and verify an encoded |0̄⟩ or |+̄⟩ ancilla block, apply a transversal CNOT, and measure the ancilla transversally. Classical decoding of the measured codeword yields the full X or Z syndrome in one step. — [Steane, PRL 78, 2252 (1997), quant-ph/9611027](https://arxiv.org/abs/quant-ph/9611027)
- Knill-style EC teleports the data through an encoded Bell pair, so correction and logical gates are applied in the Pauli frame. — [Knill, quant-ph/0410199](https://arxiv.org/abs/quant-ph/0410199)
- **[2024]** Quantinuum measured logical teleportation process fidelities of 0.975 ± 0.002 (transversal), 0.851 ± 0.009 (lattice surgery) and 0.989 ± 0.002 for Knill-style QEC teleportation with the [[7,1,3]] code on H2 (up to 30 ions). — [Ryan-Anderson et al., arXiv:2404.16728](https://arxiv.org/abs/2404.16728)

**Flag qubits**
- Chao–Reichardt: distance-3 codes can be corrected fault-tolerantly with only 2 extra qubits (1 syndrome + 1 flag). The flag detects when an ancilla fault has propagated into a weight-≥2 data error, which triggers an extra unflagged syndrome round. — [Chao & Reichardt, PRL 121, 050502 (2018), arXiv:1705.02329](https://arxiv.org/abs/1705.02329); generalized to arbitrary distance by [Chamberland & Beverland, arXiv:1708.02246](https://arxiv.org/abs/1708.02246)
- Hook errors in the surface code: an X fault on an X-check ancilla midway through its 4 CNOTs leaves a weight-2 data error. CNOT ordering ("N" vs "Z" pattern) is chosen so hooks run perpendicular to the logical operator they could shorten, preserving the effective distance. — [Fowler et al. arXiv:1208.0928](https://arxiv.org/abs/1208.0928); [Dennis et al. quant-ph/0110143](https://arxiv.org/abs/quant-ph/0110143)

**Transversal gates and no-go theorems**
- Eastin–Knill: for any code that detects arbitrary single-qubit errors, the transversal logical gates form a finite group, hence are not universal. — [Eastin & Knill, PRL 102, 110502 (2009), arXiv:0811.4262](https://arxiv.org/abs/0811.4262)
- Bravyi–König: for D-dimensional local stabilizer codes, constant-depth logical gates lie in level D of the Clifford hierarchy. 2D topological codes therefore have only Clifford constant-depth gates. — [Bravyi & König, PRL 110, 170503 (2013), arXiv:1206.1609](https://arxiv.org/abs/1206.1609)
- Workarounds:
  - Code switching between Steane [[7,1,3]] (transversal Clifford) and Reed–Muller [[15,1,3]] (transversal T). — [Anderson, Duclos-Cianci, Poulin, arXiv:1403.2734](https://arxiv.org/abs/1403.2734)
  - Gauge fixing. — [Paetznick & Reichardt, arXiv:1304.3709](https://arxiv.org/abs/1304.3709); [Bombin arXiv:1311.0879](https://arxiv.org/abs/1311.0879)
  - Concatenating codes with complementary transversal sets. — [Jochym-O'Connor & Laflamme, arXiv:1309.3310](https://arxiv.org/abs/1309.3310)
  - Pieceable fault tolerance. — [Yoder, Takagi, Chuang, arXiv:1603.03948](https://arxiv.org/abs/1603.03948)

**Magic states, distillation, cultivation**
- The magic state |T⟩ = T|+⟩ plus Clifford operations, measurement and a classically controlled S correction implements a T gate by gate teleportation. Bravyi–Kitaev 15-to-1 distillation, based on the [[15,1,3]] Reed–Muller code, outputs one state with error ≈ 35p³ from 15 inputs of error p. — [Bravyi & Kitaev, PRA 71, 022316 (2005), quant-ph/0403025](https://arxiv.org/abs/quant-ph/0403025)
- Optimized factory layouts make distillation much cheaper than earlier estimates. — [Litinski, "Magic State Distillation: Not as Costly as You Think", Quantum 3, 205 (2019), arXiv:1905.06903](https://arxiv.org/abs/1905.06903)
- Magic state cultivation (Gidney, Shutty, Jones, Sept 26 2024): a T state is grown inside a color-code patch by repeated checking with postselection, then grafted into a surface code. It reaches logical error ~2×10⁻⁹ at 10⁻³ uniform depolarizing noise and ~4×10⁻¹¹ at 5×10⁻⁴. Its cost is roughly that of a lattice-surgery CNOT of equal reliability, and it uses an order of magnitude fewer qubit-rounds than prior work. The authors suggest further distillation "may never be needed in practice". — [arXiv:2409.17595](https://arxiv.org/abs/2409.17595)
- **[2025]** Google demonstrated cultivation on hardware (preprint arXiv:2512.13908): error reduced 40×, magic-state fidelity 0.9999(1), ~8% of attempts retained after postselection, including code switching into a surface code. — [Google Research publication page](https://research.google/pubs/magic-state-cultivation-on-a-superconducting-quantum-processor/); cited in [Nature 2026, "Reinforcement learning control of QEC"](https://www.nature.com/articles/s41586-026-10759-2)
- **[2026]** An RL agent tuning >1,000 control parameters improved d=5/d=7 surface-code and d=5 color-code memories, and gave ~10× improvement in cultivation error and post-selection rate. — [Nature, s41586-026-10759-2](https://www.nature.com/articles/s41586-026-10759-2)
- **[2026]** Follow-up theory work examines degraded fault distance in cultivation circuits (arXiv:2609.17706), exact logical error rates (arXiv:2609.18922) and in-patch multiplexing to cut postselection overhead (arXiv:2605.03616). Titles only were retrieved. — [2609.17706](https://arxiv.org/pdf/2609.17706); [2609.18922](https://arxiv.org/pdf/2609.18922); [2605.03616](https://arxiv.org/pdf/2605.03616)
- **[2025]** Quantinuum's break-even logical non-Clifford gate: a logical controlled-Hadamard on H1-1 with infidelity 2.3×10⁻⁴ vs 1.0×10⁻³ for the physical gate. It uses an 8-qubit protocol in which magic states are prepared in a small error-detecting code (a [[6,2,2]] code per a 2026 APS abstract). — [arXiv:2506.14688](https://arxiv.org/html/2506.14688v1); [APS 2026 abstract](https://meetings-archive.aps.org/smt/2026/mar-s05/1/)
- **[2025]** Quantinuum code-switching magic states: distance-3 magic states limited mainly by SPAM error of 1.38(12)×10⁻³ (arXiv:2506.14169). Quantinuum's blog claims a record magic-state infidelity of 7×10⁻⁵, while The Quantum Insider attributes 5.1×10⁻⁴ to a related protocol. **These figures conflict and need checking against the papers.** — [arXiv:2506.14169](https://arxiv.org/pdf/2506.14169); [Quantinuum blog](https://www.quantinuum.com/blog/quantinuum-overcomes-last-major-hurdle-to-deliver-scalable-universal-fault-tolerant-quantum-computers-by-2029); [The Quantum Insider](https://thequantuminsider.com/2025/06/27/quantinuum-crosses-key-quantum-error-correction-threshold-marks-turn-from-nisq-to-utility-scale/)

**Lattice surgery and Pauli-based computation**
- Lattice surgery merges and splits surface-code patches to measure joint logical operators (Z̄Z̄ or X̄X̄) over ~d rounds. A CNOT takes an ancilla patch plus one ZZ and one XX measurement. — [Horsman, Fowler, Devitt, Van Meter, NJP 14, 123011 (2012), arXiv:1111.4022](https://arxiv.org/abs/1111.4022)
- "A Game of Surface Codes" compiles Clifford+T into multi-patch Pauli-product measurements: Cliffords are commuted to the end, and each T becomes a π/8 Pauli rotation that consumes a magic state. It gives space–time trade-offs for whole architectures. — [Litinski, Quantum 3, 128 (2019), arXiv:1808.02892](https://arxiv.org/abs/1808.02892)

**Threshold theorem**
- If physical error per location is below a constant ε_th, arbitrarily long computations succeed with polylogarithmic overhead. — [Aharonov & Ben-Or, quant-ph/9906129](https://arxiv.org/abs/quant-ph/9906129); [Aliferis, Gottesman, Preskill quant-ph/0504218](https://arxiv.org/abs/quant-ph/0504218)

**Resource estimates**
- In 2019, RSA-2048 was estimated at 20M noisy qubits and 8 hours, assuming p=10⁻³, a 1 µs surface-code cycle and 10 µs reaction time. — [Gidney & Ekerå, arXiv:1905.09749](https://arxiv.org/abs/1905.09749)
- **[2025]** Gidney (May 21 2025) estimates fewer than 1 million noisy qubits and under a week under the same hardware assumptions (square grid, p=0.1%, 1 µs cycle, 10 µs reaction time). The savings come from approximate residue arithmetic (Chevignard–Fouque–Schrottenloher 2024), yoked surface codes for idle storage and magic-state cultivation. The Toffoli count is >100× lower than CFS 2024. — [arXiv:2505.15917](https://arxiv.org/abs/2505.15917v1); [The Quantum Insider](https://thequantuminsider.com/2025/05/24/google-researcher-lowers-quantum-bar-to-crack-rsa-encryption/); yoked surface codes: [Gidney et al. arXiv:2312.04522](https://arxiv.org/abs/2312.04522)
- **[2026, single secondary source, unverified]** Iceberg Quantum's "Pinnacle" (Feb 2026) claims <100,000 physical qubits for RSA-2048 using qLDPC codes. A March 2026 sketch by Cain et al. proposes ~10,000 reconfigurable neutral atoms. — [postquantum.com (June 2026 note)](https://postquantum.com/quantum-research/quantum-breakthrough-rsa-2048/)
- **[2025]** IBM Starling (2029, Poughkeepsie): 200 logical qubits and 10⁸ operations. Blue Jay: 2,000 logical qubits and 10⁹ operations. Loon (2025) tests c-couplers for up to degree-6 connectivity. — [IBM newsroom Nov 12 2025](https://newsroom.ibm.com/2025-11-12-ibm-delivers-new-quantum-processors,-software,-and-algorithm-breakthroughs-on-path-to-advantage-and-fault-tolerance); [Intelligent CIO June 2025](https://www.intelligentcio.com/north-america/2025/06/13/ibm-quantum-starling-expected-to-be-first-large-scale-fault-tolerant-quantum-computer/)

### Inferences
- The "hook error" and "flag" concepts are ideal for a no-feed-forward demo. Flags are just extra measured qubits whose outcomes are post-processed. On IonQ, "flag fired → reject shot" (post-selection) is fully implementable without dynamic circuits (see §6 demo D2b).
- Magic-state topics are hard to demo on 20 qubits with real codes. A teaching tool can still (a) show the T-gate teleportation circuit with **deferred** correction (classically-controlled S replaced by a controlled-S from the measured qubit, which is legal by the deferred measurement principle), and (b) compute the 15-to-1 output error curve 35p³ analytically and show when distillation pays off.
- Eastin–Knill can be taught constructively. Let the learner try every transversal single-qubit product on [[7,1,3]] or [[4,2,2]] and discover that the induced logical gates close into a finite group.

### Gaps
- The RSA-2048 claims below 1M qubits [2026] were not verified against primary preprints.
- The exact 15-to-1 input-error threshold and Litinski's factory footprints were not re-verified in this session, so they are deliberately not quoted.

---

## 5. State of the art 2023–2026 experiments (with numbers)

### Takeaway
Three platforms have now shown below-threshold scaling or beyond-break-even logical operation.
- Superconducting (Google): Λ = 2.14 at d=3→5→7 [published 2025]; color codes; cultivation [Dec 2025].
- Neutral atoms (Harvard/QuEra): 48 → 96 logical qubits; Λ ≈ 2.14 in a 448-atom architecture [2025–2026].
- Trapped ions (Quantinuum): break-even non-Clifford gates [2025]; Helios with 48 error-corrected logical qubits [Nov 2025]; [[20,2,6]] Helix [Sept 2026].

IonQ's own QEC record is thinner but growing fast in 2026: a hardware qLDPC breakeven (June 2026), Steane-code logical rotations on Forte (Aug 2026), and a simulated real-time decoder (Sept 2026).

### Cited Findings

**Google Quantum AI**
- 2023 (Nature 614, 676): first evidence that a larger surface code does better. d=5 had a logical error of ~2.914% per cycle vs ~3.028% for d=3 (Sycamore, 72 qubits). These numbers are from my own knowledge. — [arXiv:2207.06431](https://arxiv.org/abs/2207.06431)
- **[2025 publication; arXiv Aug 2024]** Willow (Nature 638, 920–926, 2025):
  - d = 3, 5, 7 surface-code memories; 101 qubits at d=7.
  - Λ = 2.14 ± 0.02; d=7 logical error 0.143% ± 0.003% per cycle.
  - Logical lifetime 2.4 ± 0.3× the best physical qubit.
  - 1.1 µs cycle; real-time decoding at 63 µs average latency for d=5 over up to 1M cycles.
  - Repetition codes to d=29, limited by correlated events about once per hour.
  - — [arXiv:2408.13687](https://arxiv.org/abs/2408.13687)
- **[2025]** Color code d=3→5, Λ = 1.56 (details in §2). — [Google blog](https://research.google/blog/a-colorful-quantum-future/)
- **[2025]** Magic-state cultivation experiment: 40× error reduction, F = 0.9999(1), 8% acceptance. — [Google Research](https://research.google/pubs/magic-state-cultivation-on-a-superconducting-quantum-processor/)
- **[2026]** RL-based calibration of QEC published in Nature. — [s41586-026-10759-2](https://www.nature.com/articles/s41586-026-10759-2)

**Quantinuum (trapped ions, QCCD, all-to-all via ion transport)**
- 2021: real-time fault-tolerant QEC with the [[7,1,3]] color code on H1, with repeated rounds and real-time decoding. — [Ryan-Anderson et al., PRX 11, 041058 (2021), arXiv:2107.07505](https://arxiv.org/abs/2107.07505)
- 2024 (with Microsoft): [[7,1,3]] logical error rates 9.8–500× below physical; [[12,2,4]] (Knill C4/C6-based) rates 4.7–800× below physical, depending on post-selection. Repeated EC cycles of >100 physical CNOTs each reached an error rate near that of two physical CNOTs. — [Paetznick et al., arXiv:2404.02280](https://arxiv.org/abs/2404.02280)
- 2024: logical teleportation fidelities 0.975 (transversal), 0.851 (lattice surgery), 0.989 (Knill EC). — [arXiv:2404.16728](https://arxiv.org/abs/2404.16728)
- 2024 (with Microsoft): [[16,4,4]] tesseract code encoding 4 logical qubits in 16 physical qubits. — [arXiv:2409.04628](https://arxiv.org/abs/2409.04628) via [The Quantum Insider](https://thequantuminsider.com/2025/01/03/how-microsoft-and-partners-are-shaping-the-future-of-quantum-computing/)
- **[2025]** Break-even logical CH gate (2.3×10⁻⁴ vs 1.0×10⁻³) and code-switching magic states (§4). — [arXiv:2506.14688](https://arxiv.org/html/2506.14688v1); [arXiv:2506.14169](https://arxiv.org/pdf/2506.14169)
- **[2025]** Helios (launched Nov 5 2025): 98 trapped-ion (barium) qubits, 99.921% two-qubit fidelity, 94 error-detected and 48 error-corrected logical qubits (~2:1), real-time decoding on NVIDIA GPUs. Apollo (universal fault tolerance) is targeted for 2029. — [Quantinuum blog](https://www.quantinuum.com/blog/introducing-helios-the-most-accurate-quantum-computer-in-the-world); [HPCwire](https://www.hpcwire.com/2025/11/05/quantinuum-introduces-helios-quantum-system-as-roadmap-advances-toward-apollo/)
- **[2026]** March 2026: computations with up to 94 error-detected and 48 error-corrected logical qubits using iceberg codes ([[k+2,k,2]] style) and nested distance-4 constructions. Logical gate error ~1×10⁻⁴ vs ~8×10⁻⁴ for physical 2q gates. — [The Quantum Insider Mar 10 2026](https://thequantuminsider.com/2026/03/10/quantinuum-researchers-demonstrates-quantum-computations-with-dozens-of-protected-logical-qubits/); [postquantum.com](https://postquantum.com/quantum-research/quantinuum-94-logical-qubits/). Iceberg code origin: [Self, Benedetti, Amaro, arXiv:2211.06703](https://arxiv.org/abs/2211.06703)
- **[2026]** Sept 2 2026 preprint: [[20,2,6]] C4-Helix code on Helios. Reported 4.6×10⁻⁵ logical error per logical qubit per cycle over 20 rounds, and logical Clifford RB 2.8×10⁻⁴ vs 1.2×10⁻³ unencoded, without postselection. **Secondary sources only.** — [Quantum Computing Report](https://quantumcomputingreport.com/quantinuum-demonstrates-helix-quantum-error-correction-architecture-on-helios-hardware/); [quentir.ai analysis](https://www.quentir.ai/blog/2026/quantinuum-helios-c4-helix-20-2-6-fault-tolerant-architecture-logical-error-rates)

**Harvard / MIT / QuEra (neutral atoms)**
- Dec 2023 (Nature 626, 58, 2024): logical processor with 280 atoms. It ran 48 logical qubits in [[8,3,2]] 3D color codes executing IQP-type circuits, with hundreds of logical entangling operations, and showed logical entanglement improving as surface-code distance grew from 3 to 7. Transversal gates were applied by moving atoms. Detail beyond "48 logical qubits / 280 atoms" is from my own knowledge and was not re-fetched. — [Bluvstein et al., arXiv:2312.03982](https://arxiv.org/abs/2312.03982)
- **[2025]** "Architectural mechanisms of a universal FT quantum computer" (arXiv June 2025; reported as published in Nature):
  - Up to 448 ⁸⁷Rb atoms.
  - 2.14(13)× below-threshold surface-code performance (atom-loss detection plus ML decoding).
  - Transversal teleportation with 3D [[15,1,3]] codes for arbitrary-angle synthesis.
  - Deep circuits sustained for >1 s via mid-circuit qubit reuse.
  - — [arXiv:2506.20661](https://arxiv.org/abs/2506.20661); [Quantum Computing Report](https://quantumcomputingreport.com/harvard-and-collaborators-demonstrate-scalable-fault-tolerant-architecture-with-448-neutral-atom-qubits/)
- **[2026]** Deep logical circuits with up to 96 logical qubits on >400 physical qubits (QuEra blog, Jan 2026). A tracker lists this as a Nature paper (Jan 2026), but I could not confirm that. — [QuEra blog](https://www.quera.com/blog-posts/the-core-architecture-is-validated-now-we-go); [Quantum Zeitgeist leaderboard](https://quantumzeitgeist.com/quantum-logical-qubit-leaderboard/)

**Microsoft + Atom Computing (neutral atoms)**
- Nov 2024: 24 entangled logical qubits (GHZ/cat state), plus 28 logical qubits in a Bernstein–Vazirani computation with error detection/correction that beat physical performance. — [Microsoft blog June 2025](https://azure.microsoft.com/en-us/blog/quantum/2025/06/19/microsoft-advances-quantum-error-correction-with-a-family-of-novel-four-dimensional-codes/); [Reichardt et al. arXiv:2411.11822](https://arxiv.org/abs/2411.11822)
- **[2025]** 4D geometric codes (§2).

**AWS**
- **[2025]** Ocelot cat-qubit repetition code (§2): 1.75%/1.65% per cycle at d=3/5. — [arXiv:2409.13025](https://arxiv.org/abs/2409.13025)

**IBM**
- Gross code proposal (Nature 2024). **[2025]** Relay-BP; Loon with c-couplers; <480 ns decoding; Starling 2029 (§3, §4). — [arXiv:2308.07915](https://arxiv.org/abs/2308.07915); [IBM newsroom](https://newsroom.ibm.com/2025-11-12-ibm-delivers-new-quantum-processors,-software,-and-algorithm-breakthroughs-on-path-to-advantage-and-fault-tolerance)
- Earlier heavy-hex subsystem-code experiments compared matching and maximum-likelihood decoders on IBM hardware. — [Sundaresan et al., arXiv:2203.07205](https://arxiv.org/abs/2203.07205) (from my own knowledge; not re-fetched)

**Trapped-ion QEC lineage relevant to IonQ**
- 2017: fault-tolerant [[4,2,2]] error detection on a 5-qubit trapped-ion system (Monroe group, UMD), compared with IBM's 5-qubit superconducting device. Fault-tolerant encoding beat non-FT encoding on the ions; Gottesman's small-FT proposal was tested directly. — [Linke et al., Sci. Adv. 3, e1701074 (2017), arXiv:1611.06946](https://arxiv.org/abs/1611.06946)
- 2017–2019: [[4,2,2]] FT state prep and logical gates on IBM devices. — [Takita et al., arXiv:1705.09259](https://arxiv.org/abs/1705.09259); [Harper & Flammia, arXiv:1806.02359](https://arxiv.org/abs/1806.02359)
- 2021: fault-tolerant control of a [[9,1,3]] Bacon–Shor logical qubit on a 13+ ion chain (UMD/Duke). — [Egan et al., Nature 598, 281 (2021), arXiv:2009.11482](https://arxiv.org/abs/2009.11482)
- 2022: fault-tolerant universal gate set on two Steane-code logical qubits, with flag-based FT and a magic-state-based T gate (Innsbruck). — [Postler et al., Nature 605, 675 (2022), arXiv:2111.12654](https://arxiv.org/abs/2111.12654)

**IonQ specifically**
- Native gates: GPi(φ), GPi2(φ), MS and (on Forte-class systems) ZZ(θ). Connectivity is all-to-all. — [IonQ docs, native gates](https://docs.ionq.com/guides/getting-started-with-native-gates)
- Forte page lists 36 qubits, ~0.02% 1q error and ~0.4% 2q error. The page is old, so treat these as dated. — [IonQ Forte](https://www.ionq.com/quantum-systems/forte)
- **[2025]** 99.99% two-qubit gate fidelity (Oct 21 2025). It was achieved on an R&D prototype using Electronic Qubit Control (from the Oxford Ionics acquisition). Oxford Ionics' previous record was 99.97% (2024). — [Quantum Computing Report](https://quantumcomputingreport.com/ionq-achieves-99-99-two-qubit-gate-fidelity-using-electronic-qubit-control-technology/); [The Quantum Insider](https://thequantuminsider.com/2025/10/21/ionq-achieves-99-99-two-qubit-gate-performance/)
- **[2025] roadmap:**
  - 256 physical qubits at 99.99% in 2026 (delivery slipped to 2027 per May 2026 earnings coverage).
  - ~10,000 physical qubits on one chip in 2027, interpreted as ~800 logical qubits at <10⁻⁷.
  - 20,000 physical qubits across two chips in 2028.
  - >2,000,000 physical qubits → 40,000–80,000 logical qubits by 2030, with a logical error target <10⁻¹² for "shallow memory".
  - — [IonQ blog, accelerated roadmap](https://www.ionq.com/blog/ionqs-accelerated-roadmap-turning-quantum-ambition-into-reality); [Quantum Computing Report, analyst day](https://quantumcomputingreport.com/ionq-announces-regulatory-approval-for-oxford-ionics-acquisition-and-provides-a-roadmap-update-at-its-2025-analyst-day-meeting/); [MarketBeat Q1 2026 call](https://www.marketbeat.com/instant-alerts/ionq-q1-earnings-call-highlights-2026-05-10/)
- **[2026]** Breakeven qLDPC and block codes on hardware (arXiv:2606.06455, reported June 6 2026). The device was a linear chain of 40 ¹³³Ba⁺ ions; the specific IonQ system was not named. Results:
  - 9 codes across qLDPC, topological and concatenated families.
  - BB5 qLDPC code with 4 logical qubits in 18 physical qubits: per-cycle logical error ~4× (Z) and ~9× (X) lower than prior superconducting long-range-coupler implementations.
  - Best configuration (weight-5 generalized "GB4" code): total logical memory lifetime 3.95 s vs 1.1 s physical relaxation baseline, non-post-selected.
  - Mid-circuit measurement used an "Optical-Metastable-Ground" (OMG) scheme: a global 1762 nm laser shelves spectator data qubits into a metastable manifold during readout, and the readout ancillas double as sympathetic coolants.
  - MWPM decoding.
  - — [Quantum Computing Report](https://quantumcomputingreport.com/experimental-demonstration-of-breakeven-qldpc-and-block-codes-on-a-trapped-ion-architecture/)
- **[2026]** "Continuous-angle logical rotations in the Steane code" (Huang, Zhu, Ippoliti, Monroe, Gullans; Aug 21 2026). It ran [[7,1,3]] on IonQ Forte: a transversal physical Z(θ) plus Steane syndrome extraction produces syndrome-dependent logical Z rotations, characterized by logical Ramsey and process tomography, with ±θ cancellation over two rounds. No headline numbers are given in the abstract. — [arXiv:2608.20676](https://arxiv.org/abs/2608.20676)
- **[2026]** Real-time decoder (simulated workloads, Sept 2026) (§3). IonQ's Aug 2026 earnings release still listed publishing hardware QEC results as in progress. — [IonQ 8-K](https://www.sec.gov/Archives/edgar/data/0001824920/000119312526335040/ionq-ex99_1.htm)

### Inferences
- It is a striking coincidence that Google's surface-code Λ (2.14 ± 0.02) and Harvard's below-threshold factor (2.14 ± 0.13) are numerically equal. A teaching tool should warn that the two are measured differently: Google's is per-cycle memory across d=3/5/7, Harvard's is from a 4-round characterization circuit.
- For the IonQ hackathon, the most on-brand narrative is "all-to-all connectivity makes high-rate codes cheap". IonQ's own 2026 hardware papers (BB5 qLDPC on 18 ions, Steane on Forte) are the citations to anchor it.
- "Logical qubit count" leaderboards conflate error-detected with error-corrected qubits and post-selected with non-post-selected results. A teaching tool that makes users classify claims (detected/corrected, post-selected or not, memory or computation) would address a real literacy gap.

### Gaps
- The Willow 2023 d=3/d=5 numbers (2.914%/3.028%) are from my knowledge, not re-fetched.
- I found no primary source confirming that the 96-logical-qubit Harvard/QuEra result is published in Nature.
- No IonQ hardware [[4,2,2]] or Steane logical-error numbers were found (the Forte Steane paper's numbers are not in its abstract).
- I found nothing reliable on USTC/Zuchongzhi surface-code results in 2025–2026; not searched in depth.

---

## 6. Teaching angle: what is hard, existing visual tools, and concrete demos that run under the hackathon constraints

### Takeaway
No education-research literature studies QEC learners specifically. Adjacent evidence on quantum measurement and upper-level QM points to measurement/collapse, the formalism, and carrying ideas across contexts as the main difficulties. Existing tools are either expert-grade (Crumble, Stim, the Error Correction Zoo) or game-like (Decodoku). The gap to fill is interactive, quantitatively honest demos that tie a learner's choices to measured logical-error numbers. Stim and PyMatching have **no Pyodide/WASM wheels** (stim 1.16.0 and PyMatching 2.4.0, both May 22 2026). Pyodide 314.0.7 ships numpy, scipy, networkx and sympy, so a ~60-line numpy Pauli-frame simulator plus networkx matching is a complete, verified substitute for ≤ ~100-qubit Clifford QEC demos. Demos D1–D4 below were simulated in this session with a ~0.5% two-qubit error model.

### Cited Findings

**What learners find hard (adjacent evidence)**
- No education research specific to QEC was found. For upper-level QM, student difficulties persist across institutions and textbooks. Common sources are making sense of the formalism, over-generalizing an idea from one context into another, and confusing related concepts. — [Singh & Marshman, "Review of student difficulties in upper-level quantum mechanics", arXiv:1504.02056](https://arxiv.org/abs/1504.02056)
- Quantum measurement is a documented difficulty, and research-based tutorials improved understanding in preliminary evaluations. QEC depends on exactly this: measuring parities without measuring the data. — [Zhu & Singh, arXiv:1602.05720](https://arxiv.org/abs/1602.05720)
- The research base on QIST pedagogy effectiveness is described as limited. — [arXiv:2111.06438](https://arxiv.org/abs/2111.06438)

**Existing tools and visual intuitions**
- Crumble: a browser-based prototype stabilizer-circuit editor. It imports/exports Stim circuit text, visualizes Pauli propagation and detecting regions, and is a sub-project of Stim. CrumPy embeds Crumble in Jupyter. — [algassert.com/crumble](https://algassert.com/crumble); [CrumPy on PyPI](https://pypi.org/project/crumpy/)
- Error Correction Zoo: a catalogue of codes with parameters, relationships, transversal gates and thresholds. — [errorcorrectionzoo.org](https://errorcorrectionzoo.org)
- Decodoku: citizen-science puzzle games in which players act as surface-code decoders by pairing anyons. — [Wootton, "Getting the public involved in quantum error correction", arXiv:1712.09649](https://arxiv.org/abs/1712.09649)
- Stim's repo contains `glue/crumble` and `glue/javascript` directories. Their contents (e.g. whether there is an Emscripten build of Stim) were not verified. — [quantumlib/Stim glue/](https://github.com/quantumlib/Stim/tree/main/glue)
- Other recommended references (not re-fetched in this session): Arthur Pesah's interactive stabilizer/surface-code blog posts ([arthurpesah.me/blog](https://arthurpesah.me/blog/)); Craig Gidney's blog ([algassert.com](https://algassert.com)); qiskit-qec ([GitHub](https://github.com/qiskit-community/qiskit-qec), maintenance status not verified); Watrous's IBM course "Foundations of quantum error correction" (IBM Quantum Learning; URL may have moved to quantum.cloud.ibm.com).

**Pyodide / WASM availability (verified)**
- stim 1.16.0 (May 22 2026) ships CPython wheels only for win_amd64, manylinux x86_64 and macOS. There are **no emscripten/wasm32/pyodide wheels**; an sdist exists. — [PyPI stim](https://pypi.org/project/stim/#files)
- PyMatching 2.4.0 (May 22 2026) is a compiled C++ library with the same platform set and **no wasm wheels**; an sdist exists. — [PyPI PyMatching](https://pypi.org/project/PyMatching/#files)
- Pyodide 314.0.7 built-ins include numpy 2.4.6, scipy 1.18.0, networkx 3.6.1 and sympy 1.14.0. **Not included:** stim, pymatching, qiskit, qiskit-aer, rustworkx, ldpc, galois. — [Pyodide package list](https://pyodide.org/en/stable/usage/packages-in-pyodide.html)
- micropip installs only pure-Python wheels or wasm32/emscripten wheels. Since Pyodide 314, maintainers can publish WASM wheels to PyPI under a new `pyemscripten` platform tag. Self-built wheels must match the exact Pyodide/Emscripten ABI. — [micropip docs](https://micropip.pyodide.org/en/v0.2.0/project/usage.html); [Simon Willison, June 2026](https://simonwillison.net/2026/jun/13/publishing-wasm-wheels); [Pyodide build docs](https://pyodide-build.readthedocs.io/en/latest/tutorials/quickstart.html)

### Inferences — likely hardest concepts (expert inference, not from education research)
1. "Measuring the syndrome doesn't collapse my qubit?" Parity measurement versus data measurement.
2. Discretization: why correcting X/Y/Z is enough for continuous and coherent errors.
3. Degeneracy and cosets: two different corrections can both be right, while two identical-looking syndromes can need different corrections.
4. Detectors versus stabilizer outcomes: the first X-check round is random, comparisons across time carry the information, and measurement errors are time-like edges.
5. Error correction versus fault tolerance: CNOTs spread errors (hooks), so gadget design matters.
6. Code capacity vs phenomenological vs circuit-level thresholds (10% vs 3% vs 1%) are routinely conflated.
7. Error detection with post-selection versus error correction; error-detected versus error-corrected "logical qubit" counts.
8. Λ and exponential suppression: why d=3 → 5 → 7 matters more than any single logical error number.
9. Why Cliffords are not enough: Gottesman–Knill, then Eastin–Knill, then magic states.
10. A memory experiment's final transversal readout already contains most of the information. Repeated syndrome rounds earn their keep only over long or ongoing computations; D3/D4 show this quantitatively.

### Inferences — concrete demos (all numbers are [own sim])

Simulator used (pure numpy, Pyodide-compatible), verified against qiskit-aer: track an X/Z error frame per shot as boolean arrays; propagate through H (swap X↔Z) and CNOT (X_t ^= X_c; Z_c ^= Z_t); after each CNOT apply one of 15 non-identity 2-qubit Paulis with probability p2; the flip of a Z-measurement is the frame's X bit XOR a readout flip. Detector and logical parities computed from flips are exact for any parity that is deterministic in the noiseless circuit. This is Stim's algorithm minus bit-packing. In CPython on a desktop, 2M shots of a 5-qubit circuit took ~3–4 s. D4 (18 configurations of 1M shots at 17–33 qubits, including the pure-Python lookup decoder) took 216 s in total, about 12 s per configuration. Pyodide/WASM is typically slower by a small factor (not measured), so use 10⁴–10⁵ shots in-browser. The networkx MWPM decoder is the bottleneck at high p: tens of seconds for 30k shots at d=7, mitigated by caching per syndrome pattern.

Core code (tested):
```python
class Frame:
    def __init__(s, n, S, p2, p1=None, pm=None, seed=0):
        s.S=S; s.x=np.zeros((S,n),bool); s.z=np.zeros((S,n),bool)
        s.p2=p2; s.p1=p2/10 if p1 is None else p1; s.pm=p2 if pm is None else pm
        s.rng=np.random.default_rng(seed); s.meas=[]
    def _n1(s,q):
        m=s.rng.random(s.S)<s.p1; r=s.rng.integers(1,4,s.S)
        s.x[:,q]^=m&(r&1).astype(bool); s.z[:,q]^=m&((r>>1)&1).astype(bool)
    def _n2(s,a,b):
        m=s.rng.random(s.S)<s.p2; r=s.rng.integers(1,16,s.S)
        s.x[:,a]^=m&(r&1).astype(bool);      s.z[:,a]^=m&((r>>1)&1).astype(bool)
        s.x[:,b]^=m&((r>>2)&1).astype(bool); s.z[:,b]^=m&((r>>3)&1).astype(bool)
    def h(s,q):  s.x[:,q],s.z[:,q]=s.z[:,q].copy(),s.x[:,q].copy(); s._n1(q)
    def cx(s,c,t): s.x[:,t]^=s.x[:,c]; s.z[:,c]^=s.z[:,t]; s._n2(c,t)
    def m(s,q):  f=s.x[:,q]^(s.rng.random(s.S)<s.pm); s.meas.append(f); return f
    def mx(s,q): s.h(q); return s.m(q)
```

**D1: 3-qubit bit-flip code; measurement + classical decode vs coherent (Toffoli) correction**
- Resources: 3 data + 2 ancilla qubits; 2 CNOTs to encode, 4 to extract the syndrome. Errors are injected as X with probability q per data qubit to emulate a noisy channel. Everything is measured at the end, so no feed-forward is needed.
- Results at p2=0.005, logical error rate:

| q | bare | encoded + majority of data | encoded + ancilla-syndrome lookup on q0 | coherent Toffoli correction | code-capacity theory |
|---|---|---|---|---|---|
| 0 | 0.54% | 0.46% | 1.8% | 2.4% | — |
| 0.01 | 1.53% | 0.54% | — | 2.41% | 0.03% |
| 0.05 | 5.47% | 1.38% | — | 3.09% | — |
| 0.10 | 10.4% | 3.6% | 4.6% | 5.1% | — |
| 0.20 | 20.3% | 11.2% | — | 12.3% | 10.4% |

  - Coherent Toffoli correction: decoding circuit CX, CX, Toffoli, decomposed into 8 CNOTs in total. With an ideal noiseless Toffoli it is ~1.3% at q=0.
- Teaching points:
  - (a) Encoding wins by ~3–4× once channel noise q ≫ p2.
  - (b) The gap between theory 3q²−2q³ and the circuit result is the cost of noisy gates.
  - (c) Measurement-free (Toffoli) correction is worse than measure-then-classically-decode at today's gate errors. This directly motivates "decoding is classical post-processing", which is exactly IonQ's no-feed-forward regime.
  - (d) Using ancilla syndromes to correct a single data qubit is worse than majority-voting all data, because the syndrome CNOTs add noise. This is a nice "more measurement is not free" lesson.

**D2: [[4,2,2]] logical Bell pair vs bare Bell pair (no mid-circuit measurement; ideal for IonQ)**
- Key trick: the logical Bell state (|00̄⟩+|11̄⟩)/√2 of the [[4,2,2]] code with Z̄₁=Z₀Z₁, Z̄₂=Z₀Z₂, X̄₁=X₁X₃, X̄₂=X₂X₃ is stabilized by {XXXX, ZZZZ, Z₁Z₂, X₁X₂}. That is exactly Bell(0,3) ⊗ Bell(1,2): 2 H + 2 CNOT, vs 1 H + 1 CNOT for a bare Bell pair. Measure all 4 qubits in Z (or X), reject odd total parity, and read the logical ZZ (XX) parity as b₁⊕b₂.
- Results (two circuits, Z and X basis):

| p2 | bare Bell parity error | encoded, post-selected | acceptance | gain |
|---|---|---|---|---|
| 0.001 | 0.27% | 0.0008% | 99.5% | ~335× |
| 0.003 | 0.79% | 0.0063% | 98.4% | ~126× |
| 0.005 | 1.31% | 0.018% | 97.4% | ~74× |
| 0.01 | 2.6% | 0.071% | 95.0% | ~37× |
| 0.02 | 5.1% | 0.29% | 90.4% | ~18× |

  - Without post-selection the encoded error equals the bare error (1.31%). Detection only helps if you are allowed to throw shots away. This is a crucial honesty point for teaching "error detection ≠ error correction".
- Shots needed to resolve the encoded error on hardware: at p2≈0.005 roughly 1 in 5,000 accepted shots fail, so ≥ 50k shots are needed to see ~10 failures. Under a "one job per run" constraint, put both basis circuits in one multi-circuit job, or alternate bases across runs.

**D2b: fault-tolerant vs non-FT [[4,2,2]] state prep using a flag qubit (Linke et al. 2017 style)**
- Non-FT GHZ encoder (H, CX01, CX02, CX03): post-selected logical error 0.30% at 97.3% acceptance. A single fault on qubit 0 after CX02 spreads to a weight-2 X₀X₃ error, which is undetectable.
- Adding a 5th qubit that checks Z₁Z₃ (2 extra CNOTs) and rejecting when it fires gives a post-selected logical error of 0.028% at 95.8% acceptance: ~10× better from one extra qubit.
- Bare |00⟩ prep+measure error: 1.0%.
- Caveat for honest teaching: when the final readout is in the Z basis, the same information is visible in the data bits. The flag's real value is certifying the state *before* further logical gates, so the demo should follow prep with, e.g., a transversal logical operation or X-basis readout.

**D3: repetition-code memory with "unrolled time" (fresh ancillas per round instead of mid-circuit reset)**
- Qubits = d + R(d−1); CNOTs = 2R(d−1); detectors = (R+1)(d−1). With R=3: d=3 needs 9 qubits / 12 CNOTs; d=5 needs 17 / 24; d=7 needs 25 / 36. All fit the 29-qubit Forte noise model in one job. Detection events are built classically: XOR of consecutive ancilla layers, then the final layer from data-qubit parities.
- Decoder: MWPM via networkx, using space-like, time-like, boundary and space-time diagonal edges. The diagonal edges model a data error between two checks' CNOTs, and without them MWPM lost to plain majority vote. Uniform weights; 30k shots per point.
- Results, logical error after 3 rounds:

| p2 | d=3 (9q) | d=5 (17q) | d=7 (25q) | bare qubit (q0 flip) |
|---|---|---|---|---|
| 0.005 | 0.063% | 0.010% | <0.003% (0 events) | 1.3% |
| 0.01 | 0.22% | 0.030% | <0.003%* | 2.6% |
| 0.02 | 0.94% | 0.20% | 0.037% | 5.0% |
| 0.04 | 3.1% | 1.1% | 0.39% | 9.6% |
| 0.08 | 10.4% | 7.0% | 4.2% | 17.8% |
| 0.12 | 19.2% | 15.6% | 12.6% | 25% |
| 0.16 | 27.1% | 25.1% | 22.6% | 30.7% |
| 0.20 | 33.8% | 33.0% | 31.6% | 35.6% |

  *An earlier 100k-shot run without diagonal edges gave 0.009% at d=7, p2=0.01.
  - Λ-like suppression factors: at p2=0.02, 0.94/0.20 ≈ 4.7 (d=3→5) and 0.20/0.037 ≈ 5.4 (d=5→7). At p2=0.04, ≈2.8 and ≈2.9. At p2=0.08, ≈1.5 and ≈1.7. This shows Λ falling toward 1 as p approaches threshold, which is the mechanism behind Google's Λ = 2.14.
- Honest caveat for teaching: with only R=3 rounds the curves have **not crossed even at p2=20%**. The repetition code ignores Z errors, and the short time dimension inflates the apparent threshold.
- For a textbook threshold plot, use R ≈ d rounds. The phenomenological repetition code maps onto a 2D matching problem, i.e. the random-bond Ising model, the same as surface-code code capacity, with a threshold of ~10% per effective fault location. — mapping per [Dennis et al. quant-ph/0110143](https://arxiv.org/abs/quant-ph/0110143). R=d at d=7 needs 49 qubits: fine for the numpy simulator, too many for the 29-qubit Forte noise model.
- Final-data majority vote alone is nearly as good as MWPM at low p for 3 rounds (e.g. d=3, p2=0.01: 0.25% vs 0.22%) but clearly worse at d=7 (p2=0.04: 0.64% vs 0.39%; p2=0.08: 5.6% vs 4.2%). Use this to show why syndrome history matters more as codes and runs grow.

**D4: d=3 rotated surface code (17 qubits per round), Z-memory, unrolled rounds**
- Layout (data 0–8 row-major):
  - X-checks: {0,1,3,4}, {4,5,7,8}, {1,2}, {6,7}
  - Z-checks: {1,2,4,5}, {3,4,6,7}, {0,3}, {5,8}
  - Z̄ = Z₀Z₁Z₂, X̄ = X₀X₃X₆
  - CNOT orders: X-checks TL,TR,BL,BR; Z-checks TL,BL,TR,BR. These make hooks perpendicular to the relevant logical.
- Cost: 24 CNOTs per round. R=1 uses 17 qubits; R=2 uses 25 (fits Forte's 29); R=3 uses 33 (local simulation only).
- Decoder: learned maximum-likelihood lookup. 4 Z-detectors per layer, so 8 bits at R=1, 12 at R=2 and 16 at R=3. The table was trained on 500k shots and tested on another 500k.
- Results:

| p2 | R | qubits | CNOTs | ML-decoded logical error | undecoded | post-select all-trivial: acceptance / error |
|---|---|---|---|---|---|---|
| 0.001 | 1 | 17 | 24 | 0.011% | 0.67% | 97.0% / ~0 |
| 0.003 | 1 | 17 | 24 | 0.095% | 2.0% | 91.4% / ~0 |
| 0.005 | 1 | 17 | 24 | 0.25% | 3.3% | 86.0% / ~1e-6 |
| 0.010 | 1 | 17 | 24 | 0.96% | 6.4% | 74.0% / 4e-5 |
| 0.020 | 1 | 17 | 24 | 3.3% | 11.9% | 54.9% / 2.4e-4 |
| 0.005 | 2 | 25 | 48 | 0.52% | 5.0% | 77.4% / 3e-6 |
| 0.005 | 3 | 33 | 72 | 0.82% | 6.7% | 69.7% / 1e-5 |

  - Logical error per round at p2=0.005 is ~0.27–0.3%. Compare one physical qubit taking X/Y errors from the 2–4 CNOTs it touches per round, at 8/15·p2 ≈ 0.27% each, i.e. ~0.5–1% per round.
  - Logical error scales roughly ∝ p2² at low p (0.011% → 0.095% → 0.25% for p2 = 0.1% → 0.3% → 0.5%), the signature of a distance-3 code (t=1).
  - Decoding from final data only: 0.26% (R=1), 0.64% (R=2), 1.15% (R=3) at p2=0.005, vs 0.25% / 0.52% / 0.82% using all rounds. The intermediate rounds matter more as rounds accumulate.
- Teaching points:
  - (a) Post-selection on "no detector fired" gives almost error-free outputs at a 14–30% rejection cost. This is the error-detection regime IonQ can run today without feed-forward.
  - (b) The p² scaling is the key visual: plot logical error vs p2 on log-log axes against the slope-1 line LER = p2, and the crossing is the pseudo-threshold. Here the d=3, R=1 crossing is ≈1% (LER 0.96% at p2 = 1.0%). The pseudo-threshold depends on the chosen comparator (p2, per-round physical flip probability, or undecoded error), and a teaching tool should make that choice explicit.
  - (c) A true threshold needs d=5, which is 49 qubits per round (25 data + 24 ancilla). That exceeds the 29-qubit Forte noise model but is easy for the numpy frame simulator; decode it with networkx MWPM.
- Caveat: the model has no idle noise. On real trapped-ion hardware, serialized gates and ion transport add dephasing/heating not modelled here, so treat these as optimistic.

**Other demo ideas that respect "no feed-forward, one job"**
- Deferred-measurement T-gate teleportation: replace "measure then classically-controlled S" with a quantum controlled-S from the would-be-measured qubit. This teaches magic-state injection without dynamic circuits.
- Syndrome-table puzzles for [[5,1,3]] and [[7,1,3]]. Generate a random Pauli, show the syndrome bits, let the learner guess the correction, and score by logical class (cosets). This is pure GF(2) and runs instantly.
- "Detector error model explorer": let users place a single fault anywhere in the D3/D4 circuit and highlight which detectors light up. This is Crumble's core idea, rebuilt with the numpy frame sim; propagation of one fault needs no sampling.
- Forte vs IBM noise comparison: run the D2 circuit under IonQ's Forte noise model and an IBM fake-backend noise model (with SWAP routing on heavy-hex). Show that connectivity, through extra SWAPs, changes the encoded advantage. This is not simulated here, so treat it as a hypothesis.

### Gaps
- No QEC-specific education research was found, so the "hardest concepts" list for the report should be framed as expert inference: measurement without collapse, degeneracy, detectors vs syndromes, error propagation/hooks, thresholds and scaling, and why Cliffords are not enough.
- Whether Stim can be built for Pyodide 314 from its sdist (pybind11 C++) is untested. No community-hosted Stim wasm wheel was found.
- Pyodide performance of the numpy frame simulator was not measured, only CPython.
- Not simulated: the IonQ Forte noise model itself (not available offline). My uniform-depolarizing proxy omits crosstalk, coherent errors and SPAM asymmetry.
