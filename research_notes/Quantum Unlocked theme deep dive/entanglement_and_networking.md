# Entanglement Theory, Nonlocality, and Quantum Networking: Knowledge Base for a Teaching Tool (as of Oct 2026)

Conventions used throughout: Bell states |Φ±⟩=(|00⟩±|11⟩)/√2, |Ψ±⟩=(|01⟩±|10⟩)/√2; h(x)=−x log2 x−(1−x)log2(1−x); "ε2" = average two-qubit gate error; "v" = Werner visibility. Items tagged **[2025]** or **[2026]** are recent results. Items tagged **[Computed]** are numbers I produced myself with Qiskit 2.3.0 / Qiskit Aer 0.17.2 (density-matrix or stabilizer simulation). They are not literature values; assumptions are listed in Q6.

---

## Q1. Entanglement theory: what precise definitions, measures and theorems should the tool teach?

### Takeaway
Two-qubit entanglement is completely characterized: there are closed forms for concurrence, negativity, entanglement of formation and PPT, and every entangled two-qubit state is distillable. Mixed-state and multipartite entanglement are where the niche but teachable material lives: bound entanglement, LOCC irreversibility, majorization, monogamy, GHZ vs W, and graph states. One-parameter Werner states are the best single teaching object because every threshold in Q1–Q3 can be read off one slider.

### Cited Findings

**Pure states, Schmidt decomposition, reduced states**
- Any bipartite pure state can be written |ψ⟩=Σᵢ√λᵢ|aᵢ⟩|bᵢ⟩ (Schmidt decomposition). The λᵢ are the eigenvalues of both reduced states ρ_A=Tr_B|ψ⟩⟨ψ| and ρ_B. The state is entangled iff the Schmidt rank is >1. The entropy of entanglement is E(ψ)=S(ρ_A)=−Σλᵢ log2 λᵢ, and for pure states it equals both the distillable entanglement and the entanglement cost (entanglement concentration/dilution) — [Bennett, Bernstein, Popescu, Schumacher 1996, PRA 53, 2046](https://arxiv.org/abs/quant-ph/9511030); [Horodecki⁴, "Quantum entanglement", RMP 81, 865 (2009)](https://arxiv.org/abs/quant-ph/0702225)
- Qiskit 2.x ships `schmidt_decomposition`, `partial_trace`, `entropy`, `concurrence`, `negativity`, `entanglement_of_formation` and `mutual_information` in `qiskit.quantum_info`. All are pure-Python/NumPy, so they should run in Pyodide. **[Computed: verified present in Qiskit 2.3.0]**
- Bell-state stabilizers: Φ+ ↔ (+XX,+ZZ); Φ− ↔ (−XX,+ZZ); Ψ+ ↔ (+XX,−ZZ); Ψ− ↔ (−XX,−ZZ). Because XX and ZZ commute, one Bell measurement (CNOT, then H on the control, then Z-measure both) reads both parities at once. This is the textbook Bell-measurement circuit — [Nielsen & Chuang, §1.3.6–1.3.7 and §2.6](https://doi.org/10.1017/CBO9780511976667)

**Mixed-state criteria and measures**
- **PPT/Peres–Horodecki:** separable ⇒ ρ^{T_B}≥0 (Peres 1996). The converse holds only in 2×2 and 2×3 dimensions (Horodecki 1996) — [Peres, PRL 77, 1413](https://arxiv.org/abs/quant-ph/9604005); [Horodecki³, PLA 223, 1](https://arxiv.org/abs/quant-ph/9605038)
- **Bound entanglement:** PPT entangled states exist in 3×3 and 2×4. They cannot be distilled (E_D=0) yet need entanglement to create (E_C>0), so entanglement manipulation is irreversible — [Horodecki³, PRL 80, 5239 (1998)](https://arxiv.org/abs/quant-ph/9801069); [Horodecki RMP 2009](https://arxiv.org/abs/quant-ph/0702225)
- **All entangled two-qubit states are distillable** — [Horodecki³, PRL 78, 574 (1997)](https://arxiv.org/abs/quant-ph/9607009)
- **Negativity:** N(ρ)=(‖ρ^{T_B}‖₁−1)/2 and log-negativity E_N=log2‖ρ^{T_B}‖₁. Both are computable LOCC monotones, and E_N upper-bounds distillable entanglement — [Vidal & Werner, PRA 65, 032314 (2002)](https://arxiv.org/abs/quant-ph/0102117)
- **Concurrence (Wootters):** let λ₁≥…≥λ₄ be the square roots of the eigenvalues of ρ(σ_y⊗σ_y)ρ*(σ_y⊗σ_y). Then C=max(0,λ₁−λ₂−λ₃−λ₄) and E_F=h((1+√(1−C²))/2). For a pure state a|00⟩+b|01⟩+c|10⟩+d|11⟩, C=2|ad−bc| — [Wootters, PRL 80, 2245 (1998)](https://arxiv.org/abs/quant-ph/9709029)
- **Measure zoo:** E_D (distillable), E_C (cost, which is the regularized E_F), E_F, relative entropy of entanglement and squashed entanglement satisfy E_D ≤ E_C. All coincide with S(ρ_A) on pure states — [Horodecki RMP 2009](https://arxiv.org/abs/quant-ph/0702225)
- **Hashing bound:** for Bell-diagonal states, E_D ≥ 1−S(ρ) (one-way hashing). Breeding achieves the same yield but consumes pre-shared pure pairs — [Bennett, DiVincenzo, Smolin, Wootters, PRA 54, 3824 (1996)](https://arxiv.org/abs/quant-ph/9604024)
- **Entanglement witnesses:** a Hermitian W with Tr(Wσ)≥0 for all separable σ detects ρ when Tr(Wρ)<0. Fidelity-based witnesses have the form W=α𝟙−|ψ⟩⟨ψ|. For GHZ_n, α=1/2, so F_GHZ>1/2 certifies genuine multipartite entanglement (GME). For W₃, α=2/3 — [Gühne & Tóth, "Entanglement detection", Phys. Rep. 474, 1 (2009)](https://arxiv.org/abs/0811.2803)

**LOCC, majorization, monotones**
- **Nielsen's theorem:** |ψ⟩→|φ⟩ by LOCC with certainty iff λ^ψ ≺ λ^φ. Here ≺ is majorization of the Schmidt-coefficient vectors: Σ_{i≤k}λ^ψ_{i↓} ≤ Σ_{i≤k}λ^φ_{i↓} for all k — [Nielsen, PRL 83, 436 (1999)](https://arxiv.org/abs/quant-ph/9811053)
- **Catalysis:** the incomparable pair ψ=(0.4,0.4,0.1,0.1), φ=(0.5,0.25,0.25,0) becomes convertible with the catalyst (0.6,0.4), which is returned untouched. This makes a good puzzle for a teaching game — [Jonathan & Plenio, PRL 83, 3566 (1999)](https://arxiv.org/abs/quant-ph/9905071)
- **Vidal monotones:** E_k(ψ)=Σ_{i≥k}λ_{i↓}. Optimal probabilistic conversion: P(ψ→φ)=min_k E_k(ψ)/E_k(φ) — [Vidal, PRL 83, 1046 (1999)](https://arxiv.org/abs/quant-ph/9902033)

**Monogamy**
- **CKW inequality:** C²_{AB}+C²_{AC} ≤ C²_{A(BC)}=4 det ρ_A. The residual 3-tangle τ=C²_{A(BC)}−C²_{AB}−C²_{AC} is permutation-invariant — [Coffman, Kundu, Wootters, PRA 61, 052306 (2000)](https://arxiv.org/abs/quant-ph/9907047). It generalizes to n qubits — [Osborne & Verstraete, PRL 96, 220503 (2006)](https://arxiv.org/abs/quant-ph/0502176)
- **[Computed]** GHZ₃: C_AB=0, C²_{A(BC)}=1, τ=1, S(ρ_A)=1. W₃: C_AB=2/3, negativity_AB=0.206, C²_{A(BC)}=8/9, τ=0, S(ρ_A)=0.918. Losing one qubit of a GHZ state leaves a separable mixture; losing one qubit of a W state leaves an entangled pair.

**Multipartite entanglement**
- Three qubits have exactly two SLOCC-inequivalent genuinely entangled classes, GHZ and W. Together with fully separable and three biseparable classes this gives 6 classes — [Dür, Vidal, Cirac, PRA 62, 062314 (2000)](https://arxiv.org/abs/quant-ph/0005115). Four qubits have 9 SLOCC families, some continuous — [Verstraete, Dehaene, De Moor, Verschelde, PRA 65, 052112 (2002)](https://arxiv.org/abs/quant-ph/0109033)
- **Graph states:** |G⟩=∏_{(a,b)∈E}CZ_{ab}|+⟩^{⊗n}, with stabilizers K_a=X_a∏_{b∈N(a)}Z_b. The entanglement entropy across a cut A|B equals the GF(2) rank of the off-diagonal adjacency block. The star and complete graphs are LC-equivalent to GHZ — [Hein, Eisert, Briegel, PRA 69, 062311 (2004)](https://arxiv.org/abs/quant-ph/0307130); [Hein et al. review (2006)](https://arxiv.org/abs/quant-ph/0602096). LC-equivalence is generated by local complementation — [Van den Nest, Dehaene, De Moor, PRA 69, 022316 (2004)](https://arxiv.org/abs/quant-ph/0308151)
- **Cluster states:** 2D cluster states are universal resources for measurement-based QC — [Raussendorf & Briegel, PRL 86, 5188 (2001)](https://arxiv.org/abs/quant-ph/0010033)

**Werner states (the master teaching object)**
- ρ_W = p|Ψ⁻⟩⟨Ψ⁻| + (1−p)𝟙/4, with singlet fraction F=(1+3p)/4. Werner states are entangled iff p>1/3 (F>1/2), yet admit a local hidden-variable model for all projective measurements when p≤1/2. This was the original proof that entanglement ≠ Bell nonlocality — [Werner, PRA 40, 4277 (1989)](https://doi.org/10.1103/PhysRevA.40.4277)
- **[Computed]** closed forms for the Werner state: C=max(0,2F−1)=max(0,(3p−1)/2); N=max(0,(3p−1)/4); E_N=log2(2F) for F>1/2; partial-transpose eigenvalues are (1−3p)/4 (once) and (1+p)/4 (three times).

### Inferences
- A single "Werner slider" can show the full hierarchy computed live (see the Q2 table): separable (F≤0.5), entangled and teleportation-useful (F>0.5), steerable (p>0.5, F>0.625), Bell-nonlocal (p≳0.69), CHSH-violating (p>0.7071, F>0.780), hashable (F>0.8107).
- IonQ's all-to-all connectivity means any graph state costs exactly |E| entangling gates with no SWAPs. Pairing "graph state ↔ stabilizers ↔ entanglement across a cut" is a hardware-matched, non-tutorial angle.

### Gaps
- Critical visibility for Werner states under POVMs, as opposed to projective measurements, was not researched.
- I did not verify which multipartite measures, such as geometric entanglement, are available in Qiskit. Only the bipartite functions listed above were checked.

---

## Q2. Nonlocality: Bell/CHSH, Tsirelson, loophole-free tests, nonlocal games, steering, contextuality, no-signaling, PR boxes, DI and self-testing

### Takeaway
CHSH is S=E₀₀+E₀₁+E₁₀−E₁₁, with bounds ≤2 for local models, ≤2√2 for quantum (Tsirelson) and ≤4 for no-signaling theories (PR box). Nonlocal games turn these bounds into win rates: CHSH game 75%→85.4%, GHZ game 75%→100%, magic square 88.9%→100%. Under a 0.5% two-qubit error model, all three quantum advantages survive with large margins **[Computed]**. Loophole-free tests (2015) and the 2022 Nobel prize close the experimental story. Self-testing and DI-QKD turn nonlocality into a certification tool.

### Cited Findings

**Foundations**
- EPR argument — [Einstein, Podolsky, Rosen, Phys. Rev. 47, 777 (1935)](https://doi.org/10.1103/PhysRev.47.777). Bell's theorem — [Bell, Physics 1, 195 (1964)](https://doi.org/10.1103/PhysicsPhysiqueFizika.1.195). CHSH inequality — [Clauser, Horne, Shimony, Holt, PRL 23, 880 (1969)](https://doi.org/10.1103/PhysRevLett.23.880). Tsirelson bound 2√2 — [Tsirelson, Lett. Math. Phys. 4, 93 (1980)](https://doi.org/10.1007/BF00417500)
- **Local hidden variables (LHV):** P(ab|xy)=∫dλ q(λ)P(a|x,λ)P(b|y,λ). For Φ+ with measurements in the X–Z plane, E(θ_a,θ_b)=cos(θ_a−θ_b). Optimal settings are A₀=Z, A₁=X, B₀=(Z+X)/√2, B₁=(Z−X)/√2. For any two-qubit state, the maximum CHSH value is 2√(t₁²+t₂²), where t₁, t₂ are the two largest singular values of the correlation matrix T_ij=Tr(ρσᵢ⊗σⱼ) (Horodecki criterion) — [Brunner et al., "Bell nonlocality", RMP 86, 419 (2014)](https://arxiv.org/abs/1303.2849)
- **Werner nonlocality threshold:** for projective measurements the critical visibility satisfies 0.6875 ≤ v_c ≤ 0.6961, improving the earlier 0.6829 ≤ v_c ≤ 0.7012. This equivalently bounds the Grothendieck constant K_G(3) — [Designolle et al., PRR 5, 043059 (2023), arXiv:2302.04721](https://arxiv.org/abs/2302.04721); [Hirsch et al., Quantum 1, 3 (2017)](https://arxiv.org/abs/1609.06114). The exact value remains open.
- **Steering:** the assemblage σ_{a|x}=Tr_A[(M_{a|x}⊗𝟙)ρ] is unsteerable iff it admits a local-hidden-state model. Bell-nonlocal ⊊ steerable ⊊ entangled. Werner states with projective measurements are steerable iff p>1/2 — [Wiseman, Jones, Doherty, PRL 98, 140402 (2007)](https://arxiv.org/abs/quant-ph/0612147); [Uola et al., RMP 92, 015001 (2020)](https://arxiv.org/abs/1903.06663)

**Loophole-free Bell tests and the Nobel prize**
- Delft (Hensen et al., Nature 526, 682, 2015): NV electron spins 1.3 km apart, event-ready, S=2.42±0.20 over 245 trials, p=0.039 — [arXiv:1508.05949](https://arxiv.org/abs/1508.05949). Vienna photonic test — [Giustina et al., PRL 115, 250401](https://arxiv.org/abs/1511.03190). NIST photonic test — [Shalm et al., PRL 115, 250402](https://arxiv.org/abs/1511.03189). Munich atoms 398 m apart — [Rosenfeld et al., PRL 119, 010402 (2017)](https://arxiv.org/abs/1611.04604). ETH superconducting qubits 30 m apart, S=2.0747±0.0033 — [Storz et al., Nature 617, 265 (2023)](https://doi.org/10.1038/s41586-023-05885-0)
- 2022 Nobel Prize in Physics: Aspect, Clauser and Zeilinger, "for experiments with entangled photons, establishing the violation of Bell inequalities and pioneering quantum information science" — [nobelprize.org](https://www.nobelprize.org/prizes/physics/2022/summary/)

**Nonlocal games**
- **CHSH game:** win iff a⊕b=x∧y. ω_classical=3/4, ω_quantum=cos²(π/8)≈0.8536, ω_NS=1, and ω=1/2+S/8 — [Cleve, Høyer, Toner, Watrous, CCC 2004](https://arxiv.org/abs/quant-ph/0404076)
- **GHZ/Mermin:** M₃=XXX−XYY−YXY−YYX gives |⟨M₃⟩|≤2 for LHV and 4 for the GHZ state. The n-party Mermin value is 2^{n−1} quantum versus 2^{⌊n/2⌋} LHV, an exponential gap — [Mermin, PRL 65, 1838 (1990)](https://doi.org/10.1103/PhysRevLett.65.1838); [Greenberger, Horne, Shimony, Zeilinger, AJP 58, 1131 (1990)](https://doi.org/10.1119/1.16243)
  - **GHZ game:** inputs xyz∈{000,011,101,110}, win iff a⊕b⊕c=x∨y∨z. Classical 3/4, quantum 1 (measure X on input 0, Y on input 1).
- **Mermin–Peres magic square:** a 3×3 grid of two-qubit Paulis whose rows multiply to +𝟙 and columns to −𝟙. It is a state-independent Kochen–Specker contextuality proof, and as a two-player game it has classical value 8/9 and quantum value 1 using two ebits (pseudo-telepathy) — [Mermin, PRL 65, 3373 (1990)](https://doi.org/10.1103/PhysRevLett.65.3373); [Peres, PLA 151, 107 (1990)](https://doi.org/10.1016/0375-9601(90)90172-K); [Brassard, Broadbent, Tapp, "Quantum pseudo-telepathy" (2005)](https://arxiv.org/abs/quant-ph/0407221)
  - Square used in my simulation: rows (XI, IX, XX), (IZ, ZI, ZZ), (−XZ, −ZX, YY).

**Contextuality**
- Kochen–Specker contextuality is the general framework. CHSH corresponds to an n-cycle (n=4) scenario, KCBS is the 5-cycle qutrit case, and the magic square is a state-independent proof — [Budroni et al., RMP 94, 045007 (2022)](https://arxiv.org/abs/2102.13036); [Klyachko et al. (KCBS), PRL 101, 020403 (2008)](https://arxiv.org/abs/0706.0126)

**No-signaling and PR boxes**
- Quantum no-signaling: for any local CPTP map on A, Tr_A[(ℰ_A⊗𝟙)ρ]=ρ_B, so Bob's marginal statistics cannot depend on Alice's choice. In operational form, Σ_a P(ab|xy) is independent of x — [Brunner et al. RMP 2014](https://arxiv.org/abs/1303.2849)
- **PR box:** P(ab|xy)=1/2 if a⊕b=xy, else 0. It reaches S=4 while remaining no-signaling, so no-signaling alone does not explain Tsirelson's bound — [Popescu & Rohrlich, Found. Phys. 24, 379 (1994)](https://arxiv.org/abs/quant-ph/9508009)
  - PR boxes would trivialize communication complexity — [van Dam (2005)](https://arxiv.org/abs/quant-ph/0501159)
  - They also violate information causality, a principle that recovers 2√2 — [Pawłowski et al., Nature 461, 1101 (2009)](https://arxiv.org/abs/0905.2292)

**Device independence and self-testing**
- **Self-testing:** a maximal CHSH value of 2√2 certifies, up to local isometry, a singlet and anticommuting Pauli measurements — [Mayers & Yao (2004)](https://arxiv.org/abs/quant-ph/0307205); [Šupić & Bowles review, Quantum 4, 337 (2020)](https://arxiv.org/abs/1904.10042)
- **DI randomness** certified by CHSH violation — [Pironio et al., Nature 464, 1021 (2010)](https://arxiv.org/abs/0911.3427)
- **DI-QKD** proposal — [Acín et al., PRL 98, 230501 (2007)](https://arxiv.org/abs/quant-ph/0702152). Collective-attack key rate r ≥ 1 − h(Q) − h((1+√((S/2)²−1))/2) — [Pironio et al., NJP 11, 045021 (2009)](https://arxiv.org/abs/0903.4460)
- **First DI-QKD experiments (2022):**
  - Oxford trapped ions about 2 m apart, finite-key secret key — [Nadlinger et al., Nature 607, 682](https://arxiv.org/abs/2109.14600)
  - Munich atoms 400 m apart — [Zhang et al., Nature 607, 687](https://arxiv.org/abs/2110.00575)

**[Computed] Reference table: Werner state vs visibility** (F = Φ+ fidelity = (1+3v)/4)

| v | F | Concurrence | Negativity | E_F | Hashing yield 1−S | CHSH S=2√2v | CHSH-game win | Teleport avg fidelity (2F+1)/3 |
|---|---|---|---|---|---|---|---|---|
| 1/3 | 0.500 | 0 | 0 | 0 | 0 | 0.943 | 0.618 | 0.667 |
| 0.50 | 0.625 | 0.25 | 0.125 | 0.118 | 0 | 1.414 | 0.677 | 0.750 |
| 0.6875 | 0.766 | 0.531 | 0.266 | 0.389 | 0 | 1.945 | 0.743 | 0.844 |
| 0.7071 | 0.780 | 0.561 | 0.280 | 0.423 | 0 | 2.000 | 0.750 | 0.854 |
| 0.75 | 0.8125 | 0.625 | 0.3125 | 0.499 | 0.007 | 2.121 | 0.765 | 0.875 |
| 0.90 | 0.925 | 0.85 | 0.425 | 0.789 | 0.497 | 2.546 | 0.818 | 0.950 |
| 0.99 | 0.9925 | 0.985 | 0.4925 | 0.978 | 0.924 | 2.800 | 0.850 | 0.995 |

- The hashing threshold for Werner states is F*=0.81071 **[Computed]**.

### Inferences
- Note for the tool: S=2√2·v is the CHSH value obtained with the *standard* settings, which are optimal for Werner states. The Bell-nonlocality threshold (~0.69) lies slightly *below* the CHSH threshold (0.7071). Between them, states are nonlocal only for Bell inequalities with many settings. This is a subtle point most tutorials get wrong.
- Contextuality ↔ nonlocality is a strong "niche" teaching thread. The magic square works both as a single-system contextuality proof and as a two-player game, on the same 4-qubit circuit.

### Gaps
- I did not verify Nadlinger et al.'s exact key length or CHSH value; the paper should be checked before quoting numbers.
- I did not verify that the tight robust self-testing bound (Kaniewski 2016) is F ≥ ½ + ½(S−β*)/(2√2−β*) with β*≈2.106. It is recalled from memory, so verify before use.

---

## Q3. Protocols: teleportation, dense coding, swapping, distillation, repeaters, memories/heralding, QKD family, secret sharing, blind QC, quantum money

### Takeaway
All core protocols reduce to Bell pairs plus Pauli-frame bookkeeping, so they can be taught and run *without* feed-forward: correct in classical post-processing, or use deferred measurement where a physical correction is pedagogically needed.

Distillation is the richest topic. On Werner inputs, recurrence protocols (BBPSSW/DEJMPS) work from F>1/2 but their yield vanishes over many rounds, while hashing has nonzero yield only for F>0.8107. DEJMPS converges far faster than twirled BBPSSW. With noisy local gates there is a fidelity ceiling: about F≈0.985 at 0.5% CNOT error for one round on Werner inputs **[Computed]**.

### Cited Findings

**Teleportation, dense coding, swapping, gate teleportation**
- **Teleportation:** 1 ebit + 2 cbits transmit 1 qubit. Bob applies X^{m₂}Z^{m₁}, where m₁ is Alice's H-qubit outcome and m₂ her CNOT-target outcome — [Bennett et al., PRL 70, 1895 (1993)](https://doi.org/10.1103/PhysRevLett.70.1895)
  - With a resource state of singlet fraction F, the optimal average teleportation fidelity is f=(2F+1)/3, against a classical limit of 2/3 — [Horodecki³, PRA 60, 1888 (1999)](https://arxiv.org/abs/quant-ph/9807091)
- **Deferred measurement:** classically controlled gates can be replaced by quantum-controlled gates (CNOT, CZ) with measurement moved to the end — [Nielsen & Chuang §4.4](https://doi.org/10.1017/CBO9780511976667)
- **Superdense coding:** 1 ebit + 1 qubit transmit 2 cbits — [Bennett & Wiesner, PRL 69, 2881 (1992)](https://doi.org/10.1103/PhysRevLett.69.2881)
- **Entanglement swapping:** a Bell-state measurement (BSM) on the inner halves of two Bell pairs entangles the outer qubits — [Żukowski, Zeilinger, Horne, Ekert, PRL 71, 4287 (1993)](https://doi.org/10.1103/PhysRevLett.71.4287)
- **Gate teleportation:** gates can be teleported using prepared resource states — [Gottesman & Chuang, Nature 402, 390 (1999)](https://arxiv.org/abs/quant-ph/9908010)
  - A nonlocal CNOT costs exactly 1 ebit + 1 cbit in each direction — [Eisert, Jacobs, Papadopoulos, Plenio, PRA 62, 052317 (2000)](https://arxiv.org/abs/quant-ph/0005101)

**Distillation / purification**
- **BBPSSW (recurrence plus twirl):** works for any Werner F>1/2.
  - F' = [F² + ((1−F)/3)²] / [F² + 2F(1−F)/3 + 5((1−F)/3)²]
  - The success probability is the denominator.
  - Source: [Bennett et al., PRL 76, 722 (1996)](https://arxiv.org/abs/quant-ph/9511027)
- **DEJMPS:** Alice applies Rx(π/2) and Bob Rx(−π/2) to each qubit, then a bilateral CNOT, then both measure Z and keep the pair if the outcomes agree.
  - Bell-diagonal coefficients (A,B,C,D) = (Φ+, Ψ−, Ψ+, Φ−) map to A'=(A²+B²)/N, B'=2CD/N, C'=(C²+D²)/N, D'=2AB/N, with N=(A+B)²+(C+D)² the success probability.
  - No twirl is needed, and convergence is much faster.
  - Source: [Deutsch et al., PRL 77, 2818 (1996)](https://arxiv.org/abs/quant-ph/9604039); review [Dür & Briegel, Rep. Prog. Phys. 70, 1381 (2007)](https://arxiv.org/abs/0705.4165)
  - Independent sources state that DEJMPS beats BBPSSW over nested rounds because it exploits the Z-vs-X/Y asymmetry instead of twirling — [arXiv:1803.10111](https://arxiv.org/pdf/1803.10111); [arXiv:2504.11670](https://arxiv.org/pdf/2504.11670)
- **Hashing/breeding:** asymptotic yield 1−S(ρ) for Bell-diagonal states, one-way classical communication — [Bennett, DiVincenzo, Smolin, Wootters 1996](https://arxiv.org/abs/quant-ph/9604024). In practice, recurrence is used to push F above ≈0.81, and hashing finishes.
- **Imperfect local operations:** these impose a minimum input fidelity and a maximum attainable fidelity below 1, and they motivate nested purification in repeaters — [Briegel, Dür, Cirac, Zoller, PRL 81, 5932 (1998)](https://arxiv.org/abs/quant-ph/9803056); [Dür & Briegel 2007](https://arxiv.org/abs/0705.4165)

**[Computed] Recurrence on Werner inputs (ideal gates): fidelity after round r (success probability of that round)**

| F₀ | r=1 BBPSSW / DEJMPS | r=2 BBPSSW / DEJMPS | r=3 BBPSSW / DEJMPS | r=4 BBPSSW / DEJMPS |
|---|---|---|---|---|
| 0.60 | 0.620 (0.61) / 0.620 (0.61) | 0.645 / 0.689 | 0.673 / 0.772 | 0.705 / 0.841 |
| 0.70 | 0.735 (0.68) / 0.735 (0.68) | 0.773 / 0.846 (0.64) | 0.812 / 0.934 (0.77) | 0.850 / 0.972 (0.90) |
| 0.80 | 0.838 (0.77) / 0.838 (0.77) | 0.874 / 0.944 (0.75) | 0.905 / 0.988 (0.90) | 0.930 / 0.997 (0.98) |
| 0.90 | 0.926 (0.88) / 0.926 (0.88) | 0.947 / 0.989 (0.87) | 0.963 / 0.999 | 0.974 / 1.000 |

- **[Computed] Expected raw pairs per output pair** (DEJMPS, F₀=0.8): round 1 needs ≈2.6 pairs (F=0.838), round 2 ≈7.0 (F=0.944), round 3 ≈15.5 (F=0.988), round 4 ≈31.7 (F=0.997). The cost grows as 2^r/∏p.
- **[Computed] One DEJMPS round with 0.5%-error local CNOTs** (Werner inputs, density-matrix simulation, no readout error):

  | F_in | F_out, ideal gates | F_out, noisy gates |
  |---|---|---|
  | 0.70 | 0.7353 | 0.7301 |
  | 0.90 | 0.9264 | 0.9208 |
  | 0.98 | 0.9864 | 0.9809 |
  | 0.99 | 0.9933 | 0.9878 |

  The break-even point is F≈0.985, which is the gate-noise ceiling.

**Repeaters, memories, heralding**
- **BDCZ repeater:** nested swapping plus purification gives polynomial overhead in distance — [Briegel, Dür, Cirac, Zoller 1998](https://arxiv.org/abs/quant-ph/9803056)
- **DLCZ:** atomic ensembles with linear optics and single-photon heralding — [Duan, Lukin, Cirac, Zoller, Nature 414, 413 (2001)](https://arxiv.org/abs/quant-ph/0105105)
- **Repeater generations** — [Muralidharan et al., Sci. Rep. 6, 20463 (2016)](https://arxiv.org/abs/1509.08435):
  - 1G: heralded entanglement generation + heralded purification, needing two-way classical signalling, so the rate is limited by communication time.
  - 2G: heralded generation plus QEC against operation errors, which removes two-way purification.
  - 3G: QEC against both loss and operation errors, one-way, memoryless, with rates limited only by local processing.
- **Repeaterless bound (PLOB):** secret-key or entanglement capacity of a lossy channel ≤ −log2(1−η) ≈ 1.44η bits per use — [Pirandola, Laurenza, Ottaviani, Banchi, Nat. Commun. 8, 15043 (2017)](https://arxiv.org/abs/1510.08863)
  - **[Computed]** at 0.2 dB/km: 100 km gives η=10⁻², PLOB=1.45×10⁻²; 300 km gives η=10⁻⁶, PLOB=1.44×10⁻⁶; 500 km gives 1.44×10⁻¹⁰ bits/use.
- **Heralding:** linear-optics BSMs succeed at most 50% of the time — [Calsamiglia & Lütkenhaus (2001)](https://arxiv.org/abs/quant-ph/0007058)
  - Two-photon (Barrett–Kok) heralding has rate ∝η² and is phase-insensitive — [Barrett & Kok, PRA 71, 060310 (2005)](https://doi.org/10.1103/PhysRevA.71.060310)
  - Single-photon schemes have rate ∝η but need optical phase stability — [Cabrillo et al., PRA 59, 1025 (1999)](https://doi.org/10.1103/PhysRevA.59.1025)

**QKD family**
- **BB84:** four states in two bases, about 50% sifting. Full intercept-resend gives QBER=25%. The Shor–Preskill key rate r=1−2h(Q) is positive for Q<11.0% — [Bennett & Brassard 1984 (reprint)](https://arxiv.org/abs/2003.06557); [Shor & Preskill, PRL 85, 441 (2000)](https://arxiv.org/abs/quant-ph/0003004)
  - **[Computed]** h(0.11)=0.4999.
- **E91:** security checked by CHSH — [Ekert, PRL 67, 661 (1991)](https://doi.org/10.1103/PhysRevLett.67.661)
- **BBM92:** entanglement-based BB84 without Bell test — [Bennett, Brassard, Mermin, PRL 68, 557 (1992)](https://doi.org/10.1103/PhysRevLett.68.557)
- **B92:** two non-orthogonal states — [Bennett, PRL 68, 3121 (1992)](https://doi.org/10.1103/PhysRevLett.68.3121)
- **Decoy states:** defeat photon-number-splitting attacks on weak coherent pulses — [Hwang 2003](https://arxiv.org/abs/quant-ph/0211153); [Lo, Ma, Chen 2005](https://arxiv.org/abs/quant-ph/0411004); [Wang 2005](https://arxiv.org/abs/quant-ph/0410075)
- **MDI-QKD:** an untrusted middle node performs the BSM, which removes all detector side channels — [Lo, Curty, Qi, PRL 108, 130503 (2012)](https://arxiv.org/abs/1109.1473)
- **Twin-field QKD:** single-photon interference at the middle node gives key rate ∝√η, beating PLOB — [Lucamarini et al., Nature 557, 400 (2018)](https://arxiv.org/abs/1811.06826)
- **Secret sharing (HBB):** each of three parties measures their GHZ qubit in X or Y. Bob and Charlie can reconstruct Alice's bit only together. The correlations are those of the GHZ game — [Hillery, Bužek, Berthiaume, PRA 59, 1829 (1999)](https://arxiv.org/abs/quant-ph/9806063). There is also a graph-state generalization — [Markham & Sanders, PRA 78, 042309 (2008)](https://arxiv.org/abs/0808.1532)
- **Blind QC (UBQC):** the client sends |+_θ⟩ states, and the server builds a brickwork state and measures at angles δ=φ'+θ+rπ. The server learns only upper bounds on the computation's size — [Broadbent, Fitzsimons, Kashefi, FOCS 2009](https://arxiv.org/abs/0807.4154)
- **Quantum money:** Wiesner's bills carry BB84 states — [Wiesner, SIGACT News 15, 78 (1983)](https://doi.org/10.1145/1008908.1008920)
  - Optimal simple counterfeiting succeeds with probability (3/4)^n for an n-qubit bill — [Molina, Vidick, Watrous (2012)](https://arxiv.org/abs/1202.4010)
  - Public-key money from hidden subspaces — [Aaronson & Christiano (2012)](https://arxiv.org/abs/1203.4740)

### Inferences
- **Pauli-frame verification without feed-forward:** if Bob's qubit is measured in Pauli basis P, the correction X^{m₂}Z^{m₁} simply flips the outcome when it anticommutes with P. For Z the flip is m₂, for X it is m₁, and for Y it is m₁⊕m₂.
  - The same XOR bookkeeping applies to swapping chains (the XOR of all BSM bits) and to distillation flags.
  - This keeps the protocol genuinely LOCC; the deferred-measurement version is not, since its CNOT/CZ correction gates cross the Alice/Bob boundary. It also uses fewer gates, so it is more honest and gives higher fidelity on IonQ hardware, which has no feed-forward.
- **Recommend:** use Pauli-frame post-processing as the default for IonQ runs. Show deferred measurement only as a comparison: "physical correction costs two more entangling gates and ~0.7% fidelity" (see Q6).
- **Teaching the order of thresholds** in one visualization: F>1/2 (distillable/teleport-useful) < F>0.625 (steerable) < F≈0.766 (Bell-nonlocal) < F>0.780 (CHSH) < F>0.8107 (hashable).

### Gaps
- I did not compute rate–distance curves for specific repeater-generation parameters; that would need NetSquid- or SeQUeNCe-style simulation.
- I did not verify the exact TF-QKD 1002 km key rate.

---

## Q4. Quantum internet: stages, distributed QC, networked trapped ions, IonQ networking roadmap/demos, satellites, testbeds, 2024–2026 milestones

### Takeaway
The field moved from "metropolitan heralded memory links" (2024) through "a distributed algorithm across two ion-trap modules" (Oxford, 2025) to "long-lived remote ion–ion entanglement beating generation time and 10 km DI-QKD" (USTC, Nature 2026) and "memory–memory entanglement over 420 km of fiber, beating direct transmission" (USTC, PRL 2026).

IonQ has assembled a vertically integrated networking stack:
- ion–photon entanglement (2024)
- remote ion–ion entanglement (2024)
- telecom frequency conversion (2025)
- a photonic interconnect between two commercial systems (Apr 2026)
- SiV quantum-memory nodes (Lightsynq)
- QKD (ID Quantique)
- networking hardware (Qubitekk)
- satellites (Capella)
- a metro testbed (EPB Chattanooga)

### Cited Findings

**Framework**
- **Wehner–Elkouss–Hanson stages:** (0) trusted-repeater networks → (1) prepare-and-measure → (2) entanglement distribution (enabling DI-QKD) → (3) quantum-memory networks (blind QC, clock synchronization) → (4) few-qubit fault-tolerant networks → (5) quantum-computing networks — [Wehner, Elkouss, Hanson, Science 362, eaam9288 (2018)](https://doi.org/10.1126/science.aam9288)
- **Network simulators:**
  - [NetSquid](https://arxiv.org/abs/2010.12535) (Coopmans et al., Commun. Phys. 2021)
  - [SeQUeNCe](https://arxiv.org/abs/2009.12000) (Wu et al., QST 2021)
  - [QuNetSim](https://arxiv.org/abs/2003.06397) (DiAdamo et al.)

**Distributed trapped-ion QC**
- **[2025] Oxford** (Main et al., Nature 638, 383–388, DOI 10.1038/s41586-024-08404-x):
  - Two modules about 2 m apart, each with a Sr⁺ network ion and a Ca⁺ circuit ion, linked photonically.
  - Teleported CZ gate with 86% fidelity.
  - Distributed Grover search with 71% success, described as the first distributed algorithm with several non-local two-qubit gates.
  - Also distributed iSWAP and SWAP, using 2 and 3 gate teleportations respectively.
  - Sources: [ORA record](https://ora.ox.ac.uk/objects/uuid:e8e788d3-e15c-48a3-ae23-107ad7d43ea2); [summary](https://thebrighterside.news/post/oxford-scientists-achieve-quantum-gate-teleportation-between-two-quantum-supercomputers)
- **Innsbruck** trapped-ion qubits entangled across 230 m — [Krutyanskiy et al., PRL 130, 050803 (2023)](https://doi.org/10.1103/PhysRevLett.130.050803)
- **[2026] USTC/Pan group, "Long-lived remote ion–ion entanglement for scalable quantum repeaters"** (Nature, 2 Apr 2026, Wen-Zhao Liu, Ya-Bin Zhou et al.):
  - Memory–memory entanglement over 10 km of spooled fiber.
  - Coherence of about 550 ms versus an average generation time of about 450 ms, meeting the "entanglement outlives generation time" requirement for repeaters.
  - Telecom interface.
  - DI-QKD: 1,917 secret key bits from about 4.05×10⁵ Bell pairs at 10 km (finite-size). A positive key rate at 101 km is only an asymptotic projection.
  - Sources: [Nature link](https://www.nature.com/articles/s41586-026-10177-4); [arXiv:2602.08472](https://arxiv.org/abs/2602.08472); [teleportation review citing it, arXiv:2607.25395](https://arxiv.org/pdf/2607.25395)
  - Caveat: the preprint-to-paper match comes from search snippets.

**Metropolitan / long-distance memory networks**
- **[2024] Harvard/AWS:** two SiV-in-diamond nanophotonic memory nodes linked through a 35 km deployed fiber loop in Boston, with conversion to 1350 nm (Knaut et al., Nature, May 2024) — [Singularity Hub](https://singularityhub.com/2024/05/16/scientists-step-towards-quantum-internet-with-experiment-under-the-streets-of-boston/); [Labcompare](https://www.labcompare.com/617-News/613140-Harvard-Physicists-Create-The-First-Metro-Area-Quantum-Network/)
- **[2024] Delft/QuTech:** heralded entanglement of diamond spin qubits in nodes 10 km apart, via a midpoint station over 25 km of deployed fiber, with L-band conversion (Stolk et al., Science Advances, Oct 2024) — [arXiv:2404.03723](https://arxiv.org/abs/2404.03723); [QuTech](https://qutech.nl/2024/10/30/a-rudimentary-quantum-network-link-between-dutch-cities/)
- **[2024] USTC Hefei:** three atomic-ensemble memory nodes up to 12.5 km apart, with telecom conversion and single-photon heralding; memory lifetime exceeds the round-trip time (Nature 629, 579) — [arXiv:2309.00221](https://arxiv.org/pdf/2309.00221); [IDEAS/RePEc](https://ideas.repec.org/a/nat/nature/v629y2024i8012d10.1038_s41586-024-07308-0.html)
- **[2026] USTC (Luo et al., PRL, Aug 2026):** two quantum memories entangled through 420 km of fiber.
  - Loss is 78.7 dB at 420 km. Concurrence is 0.046±0.022 with an entangling probability of about 1×10⁻⁶. At 320 km, concurrence is 0.052±0.007 at 6.86×10⁻⁶.
  - Beyond about 320 km the scheme beats the repeaterless limit.
  - Caveat: both memories sit in one lab, and only about 20 km is deployed fiber (two ~10.1 km arms to the Charlie node).
  - Sources: [arXiv:2504.05660](https://arxiv.org/pdf/2504.05660); [phys.org](https://phys.org/news/2026-08-physicists-entangle-quantum-memories-km.html); [PostQuantum analysis](https://postquantum.com/quantum-research/420-km-quantum-memory-entanglement/)

**Satellites and long-distance QKD**
- **Micius:**
  - Entanglement distribution over 1203 km with CHSH S=2.37±0.09 — [Yin et al., Science 356, 1140 (2017)](https://arxiv.org/abs/1707.01339)
  - Satellite-to-ground decoy-state QKD up to about 1200 km — [Liao et al., Nature 549, 43 (2017)](https://arxiv.org/abs/1707.00542)
  - Entanglement-based QKD over 1120 km at 0.12 bits/s — [Yin et al., Nature 582, 501 (2020)](https://doi.org/10.1038/s41586-020-2401-y)
  - Integrated space–ground network over 4600 km — [Chen et al., Nature 589, 214 (2021)](https://doi.org/10.1038/s41586-020-03093-8)
- **[2025] Jinan-1 microsatellite** (≈96 kg, ~23 kg payload, ~500 km orbit):
  - Real-time QKD between China and Stellenbosch, South Africa, 12,900 km apart.
  - Up to 1.07 million secure bits in a single pass; one-time-pad image encryption.
  - Experiment run in Oct 2024, published in Nature 640 on 19 Mar 2025.
  - This is a trusted-relay arrangement, not entanglement across 12,900 km.
  - Sources: [Scientific American](https://scientificamerican.com/article/mini-satellite-sends-encrypted-quantum-message-a-record-breaking-distance); [Space in Africa](https://spaceinafrica.com/2025/03/20/south-africa-and-china-establish-12900-km-quantum-satellite-link/); [PostQuantum caveats](https://postquantum.com/industry-news/microsatellite-qkd-record/)
- **TF-QKD over 1002 km of fiber** (Liu et al., PRL 130, 210801, 2023) — [DOI 10.1103/PhysRevLett.130.210801](https://doi.org/10.1103/PhysRevLett.130.210801)

**IonQ networking track record**
- **Feb 2024:** ion–photon entanglement, step 1 of a 4-step photonic-interconnect plan — [IonQ blog](https://ionq.com/blog/enabling-networked-quantum-computing-with-ion-photon-entanglement); [QCR](https://quantumcomputingreport.com/ionq-breakthrough-pioneering-ion-photon-entanglement-for-quantum-networking/)
- **Sept/Oct 2024:** remote ion–ion entanglement between two separate trap wells via photons collected into a central detection hub, step 2 of 4 — [BusinessWire, 3 Oct 2024](https://businesswire.com/news/home/20241003150527/en/IonQ-Demonstrates-Remote-Ion-Ion-Entanglement-a-Significant-Milestone-in-Developing-Networked-Quantum-Systems-at-Scale/); [QCR](https://quantumcomputingreport.com/ionq-advances-quantum-networking-with-remote-ion-ion-entanglement-breakthrough/)
- **[2025] Sept 23, 2025:** quantum frequency conversion of photons from Ba⁺ (visible) to telecom wavelengths on a prototype, with AFRL. No peer-reviewed details were released — [The Quantum Insider](https://thequantuminsider.com/2025/09/23/ionq-demonstrates-quantum-frequency-conversion-to-telecom-wavelengths/); [Optica OPN](https://www.optica-opn.org/home/industry/2025/september/ionq_announces_quantum_networking_breakthrough/)
- **[2026] Apr 14, 2026:** IonQ says it photonically interconnected two *independent commercial* trapped-ion systems, validating generation, transmission and detection of the entangling photons, and calls it the first such commercial demo. The work was partly AFRL-funded. No fidelities, rates, distances or model names were disclosed — [IonQ press release](https://ionq.com/news/ionq-achieves-key-photonic-interconnect-milestone-demonstrating-networked-quantum-systems-using-entanglement)
- **Acquisitions:**
  - Qubitekk (networking) and a controlling stake in ID Quantique (QKD, with SK Telecom ties).
  - Lightsynq (ex-Harvard SiV quantum-memory and interconnect team with 20+ patents), completed June 2025 for about 12.3M shares. A later SEC filing values it at about $306.8M.
  - Capella Space (satellites), completed 15 Jul 2025, with the stated aim of space-to-space and space-to-ground QKD.
  - Sources: [eeNews Europe](https://www.eenewseurope.com/en/ionq-buys-lightsynq-capella-for-satellite-qkd); [TQI on Lightsynq](https://thequantuminsider.com/2025/06/03/ionq-reports-completion-of-lightsynq-acquisition/); [IonQ on Capella](https://ionq.com/news/ionq-completes-acquisition-of-capella-space-advancing-vision-for-space-based); [Constellation Research](https://www.constellationr.com/insights/news/ionqs-plan-quantum-networks-extending-space)
- **EPB Chattanooga:**
  - Apr 2025: a $22M deal brings a Forte Enterprise to Chattanooga and builds on the EPB Quantum Network, launched in 2022, where IonQ is the primary technology partner — [IonQ IR](https://investors.ionq.com/news/news-details/2025/IonQ-Announces-22M-Deal-with-EPB-Establishing-Chattanooga-Tennessee-as-the-First-Quantum-Computing--Networking-Hub-in-the-U-S-/default.aspx); [Fiber Broadband Assoc.](https://fiberbroadband.org/2025/04/25/epb-and-ionq-partner-to-establish-chattanooga-as-the-first-quantum-computing-and-networking-hub-in-the-u-s/)
  - **[2026] Aug 3, 2026:** Tennessee Quantum Communications Research Center, a five-year $15M IonQ commitment, set to host "the world's first commercial Quantum Memory embedded within an operational communications network" — [IonQ](https://ionq.com/news/ionq-and-epb-partner-to-launch-the-tennessee-quantum-communications-research-center); [EPB](https://epb.com/newsroom/press-releases/ionq-epb-tennessee-quantum-communications-center/)
- **[2026] Apr 13, 2026:** $7.5M IonQ–UMD QLab expansion, including the first deployment of IonQ's SiV-based quantum-memory node, complementing the Mid-Atlantic Region Quantum Internet (MARQI) — [IonQ IR](https://investors.ionq.com/news/news-details/2026/IonQ-and-University-of-Maryland-Expand-QLab-Collaboration-to-Advance-Quantum-Networking-and-Research/default.aspx); [TQI](https://thequantuminsider.com/2026/04/14/ionq-umd-qlab-quantum-networking-expansion/)
- **[2026] Q1 2026 results:**
  - Revenue of $64.7M.
  - National QKD networks deployed in Switzerland, Slovakia and Romania.
  - First commercial sale of a quantum-memory node into the US Mid-Atlantic regional quantum internet.
  - Sale of a 256-qubit 6th-generation system "anchored by a secure quantum network".
  - Selection for DARPA HARQ (heterogeneous qubit networking; IonQ's role is diamond quantum memories).
  - Sources: [IonQ Q1 2026](https://www.ionq.com/news/ionq-announces-first-quarter-2026-financial-results); [TQI](https://thequantuminsider.com/2026/05/06/ionq-reports-64-7-million-q1-2026-revenue-fueled-by-quantum-contracts-and-system-sales/); [QCR on HARQ](https://quantumcomputingreport.com/ionq-selected-for-darpa-harq-program-and-demonstrates-first-remote-photonic-interconnect/)

### Inferences
- IonQ's public narrative is "modular trapped-ion QPUs + photonic interconnects + memories + QKD + space". A teaching tool that connects an on-chip Bell pair to a networked Bell pair (with heralding, memory decoherence, distillation and swapping) maps directly onto that narrative. The step is: "this Bell pair could be the photonic link between two Forte systems".
- The 2026 USTC results give quotable "why memories matter" numbers: 550 ms coherence versus 450 ms generation time, and the 320 km crossover beyond direct transmission. These anchor a "repeater race" mini-game against the PLOB bound.

### Gaps
- IonQ's 4-step interconnect roadmap: steps 3–4 are not defined in the sources I found, and the April 2026 press release does not say which step it is.
- No IonQ interconnect fidelity or rate figures are public.
- I found no reliable sources on the status of DARPA QuANET or the DOE testbeds (Chicago, Long Island, DC-QNet) in 2025–2026.
- The Qubitekk and ID Quantique deal-closing dates were not verified.
- Duke/IonQ photonic-interconnect papers (e.g., 2024 fast ion–ion entanglement rates) were not verified in this session.

---

## Q5. iQuHACK 2026 IonQ challenge (github.com/iQuHACK/2026-IonQ): exact rules, mechanics, winners, strategies

### Takeaway
IonQ's iQuHACK 2026 challenge (MIT, Jan 30–Feb 1, 2026) was a competitive *entanglement-distillation network game*. Teams claimed graph edges by submitting OpenQASM 3 LOCC circuits that distill N≤8 noisy Bell pairs with secret X/Z-flip noise above a per-edge fidelity threshold. Two teams, one from UAM and one from BYU, each publicly claim first place. UAM's win is credited to BBPSSW and DEJMPS; BYU's to matching circuits to the specific noise types.

The game encodes what IonQ engineers find interesting: LOCC constraints, noise-tailored distillation, the trade-off between fidelity and success probability, and resource budgeting.

### Cited Findings

**Event context**
- About 1,400 participants (about 400 in person, about 1,000 remote from 76 countries) and 15 sponsors. qBraid's recap describes IonQ's entry as "a gamified entanglement distillation challenge set across a quantum network graph" — [qBraid](https://qbraid.com/blog-posts/qbraid-iquhack-2026)

**Repository**
- Files: README.md, client.py, demo.ipynb, game_handbook.md, requirements.txt, visualization.py.
- The API is hosted on Cloud Run. Public endpoints: GET /v1/graph and /v1/leaderboard. Bearer-token endpoints: /v1/register, /v1/select_starting_node, /v1/claim_edge, /v1/status/{id}, /v1/restart. Submission was via a Google Form.
- Source: [README](https://github.com/iQuHACK/2026-IonQ)

**Game rules (handbook)** — [game_handbook.md](https://raw.githubusercontent.com/iQuHACK/2026-IonQ/main/game_handbook.md)
- Nodes are quantum computers holding "utility qubits" (points). Edges are potential Bell-pair links. Teams build a connected subgraph from one starting node, and any player may claim any edge, with no capacity limit on edges.
- Fidelity is F=|⟨Φ+|ψ⟩|². All raw pairs on an edge are identical. The edge's noise is described as "Noise Type & Probability (secret) – X/Z flip probabilities on raw Bell pairs". Edges also display a "Difficulty Rating" (a hint) and a "Base Threshold Fidelity".
- **Circuit format:** request N raw pairs, with N≤8 and N≤budget. The engine creates 2N qubits paired "outside-in": pair 1 is (0, 2N−1) and pair N is (N−1, N). Qubits 0…N−1 belong to Alice and N…2N−1 to Bob.
- **LOCC rule:** two-qubit gates (CNOT/CZ/SWAP) may act only within one side; nothing may cross the boundary. Classical feed-forward is allowed. The output pair must end on qubits (N−1, N).
- **Post-selection:** the player names a `flag_bit`, and the server keeps outcomes where that bit is 0. The server "simulates all measurement outcomes" and returns the post-selected fidelity and the success probability.
- OpenQASM 3 conditionals use `if (c[0])` syntax.
- **N=2 example:** Alice applies CNOT q1→q0 and measures q0→c[0]. Bob applies CNOT q2→q3 and measures q3→c[1]. Each side applies a conditional Z correction. flag_bit=2, although the example never writes c[2]; presumably it should hold c[0]⊕c[1].
- **Budget:** 75 Bell pairs to start. Budget is spent only on *successful* claims, so failed attempts are free. A budget at or below zero ends the game unless the player restarts.
- **Vertex rewards:** claim strength on a vertex is Σ over owned incident edges of (fidelity × success probability)/√rank, with edges ranked by fidelity (weights 1, ≈0.71, ≈0.58, 0.5). Only the top-"capacity" players by strength receive the vertex's utility qubits and bonus Bell pairs, and being displaced removes those rewards. Score is the sum of utility qubits on owned nodes.
- **Starting nodes:** four candidate starting nodes are assigned, in the Americas for in-person players and in Europe/Asia/Africa for remote players.
- **Client:** `claim_edge(edge, circuit, flag_bit, num_bell_pairs)` serializes a Qiskit circuit with `qasm3.dumps`. Range checks happen server-side; the docstring says 1–8 — [client.py](https://raw.githubusercontent.com/iQuHACK/2026-IonQ/main/client.py)
- **README strategy tips:** balance utility qubits against bonus Bell pairs when picking a start; begin with low-difficulty edges; more pairs improve fidelity but cost budget; failed attempts are free — [README](https://github.com/iQuHACK/2026-IonQ)

**Winners**
- UAM (Madrid) team claims first place in IonQ's challenge, crediting "advanced quantum distillation protocols (BBPSSW and DEJMPS)" — [UAM EPS news](https://www.uam.es/eps/escuela/noticias/estudiantes-eps-ganan-iquhack2026)
- BYU "Q-gars" also report first place in the IonQ challenge — [BYU Universe](https://universe.byu.edu/campus/byu-students-win-mit-quantum-hackathon-in-debut-appearance)
  - The team was last for 12+ hours behind teams exploiting a loophole. Organizers fixed the bug around 2 a.m. and reset the leaderboard.
  - At 3 a.m. they "matched their solutions to the system's specific types of noise", expanded across the network, and turned the challenge into a playable web game.
  - Judges reportedly rewarded clear communication and creative problem-solving.

**[Computed] Why noise-tailoring wins.** One bilateral-CNOT round (Z-basis parity check) under independent X-flip probability p_x and Z-flip probability p_z:

| (p_x, p_z) | F₀ | Z-check (catches X flips) | X-check (H⊗H first; catches Z flips) | 2 rounds alternating (4 pairs) |
|---|---|---|---|---|
| (0.1, 0) | 0.900 | F=0.988, p=0.82 | F=0.820, p=1.00 (worse!) | 0.976 |
| (0, 0.1) | 0.900 | F=0.820 (worse!) | F=0.988, p=0.82 | 0.976 |
| (0.1, 0.1) | 0.810 | 0.810 (no gain) | 0.810 (no gain) | 0.931 |
| (0.05, 0.2) | 0.760 | 0.678 (worse) | 0.852 | 0.880 (X-check first) / 0.814 (Z-check first) |

### Inferences
- **Core physics lesson the game rewards:** a bilateral CNOT plus Z-parity check detects only bit-flip (Ψ-type) errors. It *doubles* phase errors because Z errors propagate target→control.
  - The handbook's own N=2 example is a Z-check, so on a phase-flip-dominated edge it lowers fidelity.
  - The fix is a basis change before the check: H on all qubits, or the DEJMPS Rx(±π/2) rotation, which permutes Φ−↔Ψ−.
  - Alternate check bases across rounds when both errors are present.
- **Strategy implications of the rules:**
  - Failed claims are free and the server returns F and p. Players could therefore probe each edge for free (N=1 gives raw F; N=2 Z-check vs X-check reveals p_x vs p_z) before committing budget.
  - Claim strength multiplies F by p_success. Aggressive post-selection, multi-flag rejection and deep recurrence lower p, so the optimum balances them rather than maximizing F.
  - The 1/√rank weighting makes a node's first edge worth the most.
  - The two "first place" claims plausibly correspond to separate in-person and remote divisions, since the game itself splits candidates by in-person vs remote. This is not confirmed.
- **Relevance for the Qollab × IonQ build:**
  - Do *not* clone the game.
  - Build its *pedagogical complement*: a tool that explains *why* a check catches one error type, shows the Bell-diagonal (I, X, Y, Z) probability vector flowing through each gate, and then runs the same circuits on IonQ Forte noise models to show the gate-noise ceiling.
  - This would show judges continuity with iQuHACK 2026 without duplicating it.

### Gaps
- Exact edge thresholds, noise values, difficulty-to-threshold mapping, vertex capacities and restart penalties are not in the public files; they were generated server-side.
- The nature of the loophole exploited by other teams is unknown.
- I found no public repository of the winning teams' code.
- No official iQuHACK results page reconciles the UAM and BYU first-place claims.

---

## Q6. Teaching angle: misconceptions, existing intuitions, and concrete demos runnable under the constraints (Qiskit 2.x in Pyodide, ≤24-qubit built-in sim, IonQ Forte noise ≤29 qubits, no feed-forward on IonQ, one job per run)

### Takeaway
The best-documented misconception is FTL signaling via entanglement. Others are "all entangled states give perfect correlations along every axis" and conflating entanglement with superposition.

Every core demo fits in ≤29 qubits with ≤20 entangling gates. At ε2≈0.5% the quantum advantage stays large: CHSH S≈2.75, teleportation fidelity ≈0.99, magic square ≈97.9%, GHZ game ≈97.8%, 29-qubit GHZ fidelity ≈0.68–0.84. The interesting teaching content is therefore *how* noise erodes advantage (thresholds, ceilings, scaling), not *whether* the advantage exists.

### Cited Findings

**Documented misconceptions**
- FTL signaling via entanglement appeared in a study of 31 pre-service physics teachers and a 73-student university cohort. That study also documents learners conflating entanglement with superposition — [Brang et al., EPJ Quantum Technology 11 (2024)](https://epjqt.epj.org/articles/epjqt/abs/2024/01/40507_2024_Article_244/40507_2024_Article_244.html)
- An educator review lists "controllable local action on A instantly sends a message" as a common misconception, partly traced to popular materials. The correct framing: conditional predictions are possible, but unconditional marginals are unchanged — [arXiv:2405.20923](https://arxiv.org/pdf/2405.20923)
- Students assume all entangled states are maximally entangled, i.e. perfectly correlated along all common axes. This was found with the QuVis interactive simulations — [Kohnle & Deffebach, arXiv:1512.02346](https://arxiv.org/pdf/1512.02346)
- Students fall back on pre-existing classical correlations or local-hidden-variable ideas even after instruction — [Frontiers in Education (2025)](https://www.frontiersin.org/journals/education/articles/10.3389/feduc.2025.1729099/full)

**[Computed] Simulation results** (Qiskit Aer density-matrix or stabilizer simulation; two-qubit depolarizing error with average gate error 0.5%, i.e. λ=0.00667; one-qubit error 0.02%; symmetric 0.5% readout flip unless noted; ideal = no noise)

| Demo | Qubits | Entangling gates | Ideal | Noisy (0.5%) | Classical bound / note |
|---|---|---|---|---|---|
| CHSH S (4 setting circuits) | 2 | 1 | 2.833 (shot noise) | **2.750** | 2; game win 0.8438 vs 0.75 |
| Teleportation, deferred-measurement corrections (CNOT+CZ), avg over 6 states | 3 | 4 | 1.000 | **0.981** | 2/3 |
| Teleportation, Pauli-frame post-processing (no feed-forward) | 3 | 2 | 1.000 | **0.988** | 2/3 |
| Superdense coding, mean success over 4 messages | 2 | 2 | 1.000 | **0.980** | 1 bit per qubit classically |
| GHZ game (3 players) | 3 | 2 | 1.000 | **0.9775** | 0.75 |
| Magic-square game (avg over 9 question pairs) | 4 | 2 Bell + ≤2 local (Alice row 3: CZ; Bob col 3: CNOT) | 1.000 | **0.979** (worst cell 0.967) | 8/9 = 0.889 |
| 1 DEJMPS round, F_in=0.90 Werner | 4 | 2 local CNOTs | 0.926 | **0.921** (no readout error) | ceiling ≈0.985 |

- **Swapping chain [Computed]**: end-to-end Φ+ fidelity with n links (2n qubits, 2n−1 CNOTs, noiseless Pauli-frame correction, no readout error):

  | Links | Qubits | F |
  |---|---|---|
  | 1 | 2 | 0.995 |
  | 2 | 4 | 0.985 |
  | 3 | 6 | 0.974 |
  | 4 | 8 | 0.964 |
  | 5 | 10 | 0.955 |
  | 8 | 16 | 0.928 (analytic) |
  | 10 | 20 | 0.911 (analytic) |
  | 12 | 24 | 0.893 (analytic) |
  | 14 | 28 | 0.876 (analytic) |

  - Simulations match the analytic Werner model F=(1+3(1−λ)^{2n−1})/4 to within 0.002.
- **GHZ fidelity vs n [Computed]** (log-depth fan-out, n−1 CNOTs). Fidelity F=(P₀ⁿ+P₁ⁿ)/2+⟨X^{⊗n}⟩/2, measured with 2 circuits:

  | n | With 0.5% readout error | Without readout error |
  |---|---|---|
  | 2 | 0.980 | 0.995 |
  | 3 | 0.966 | 0.990 |
  | 5 | 0.940 | 0.976 |
  | 8 | 0.903 | 0.958 |
  | 12 | 0.855 | 0.937 |
  | 16 | 0.812 | 0.915 |
  | 20 | 0.768 | 0.891 |
  | 24 | 0.734 | 0.872 |
  | 29 | 0.682 | 0.844 |

  - All values exceed the GME witness threshold of 0.5.
  - Readout error matters more than gate error at large n: the parity term decays roughly as (1−2p_ro)ⁿ.
- **QKD numbers [Computed]**, using Werner noise Q=(1−v)/2 and S=2√2v:
  - BB84 key rate 1−2h(Q): 0.909 at Q=0.5%, 0.789 at Q=1.38% (corresponding to S=2.75), 0.427 at Q=5%. It is zero at Q≈11%. Full intercept-resend gives Q=25%.
  - DI-QKD rate (Pironio formula): 0.874 at S=2.80, 0.710 at S=2.75, 0.541 at S=2.69, 0.225 at S=2.55.
  - Under intercept-resend in the Z or X basis, E91's CHSH value drops to S=√2 (analytic, standard settings).

### Inferences

**Concrete demos and design notes.** Gate counts assume one IonQ entangling gate per CNOT/CZ. IonQ's native entangling gates (ZZ on Forte, MS on Aria) are equivalent to CNOT/CZ up to single-qubit gates.

1. **"No-signaling microscope"** (2 qubits, 1 entangling gate). Alice randomly chooses her basis. Show that Bob's marginal stays 50/50 within shot noise for every Alice choice. Correlations appear only when the two records are joined. This directly targets the FTL misconception from Brang et al. A good refinement is to show the *conditional* histogram only after a "classical message" animation arrives at light speed.
2. **"Werner slider / hierarchy ladder"**:
   - Inject tunable noise inside a single *pure-state* circuit by purifying the Pauli channel with ancillas. An ancilla prepared as Ry(θ)|0⟩ controlling an X (or Z) on Bob's qubit, then ignored, realizes a flip with probability sin²(θ/2).
   - Two ancillas give exactly iQuHACK-style independent X/Z flips; three give a full Pauli or Werner channel.
   - This keeps simulation as a statevector, so it fits the 24-qubit browser simulator, where density matrices of more than ~10–12 qubits do not.
   - It also runs as-is on IonQ, with no classical randomness needed per shot.
   - Overlay the thresholds 1/3, 1/2, ~0.69, 0.7071 and F=0.8107.
3. **"Distillation workbench" (iQuHACK complement):**
   - N=2 pairs: 4 data qubits + 4 noise ancillas = 8 qubits, about 8 entangling gates.
   - N=4 pairs (2 rounds): about 16 qubits, about 18 entangling gates.
   - Show the Bell-diagonal vector (p_I, p_X, p_Y, p_Z) through each step; post-select in classical processing.
   - Contrast the Z-check, X-check and DEJMPS variants on biased noise, and show the ~0.985 ceiling under Forte gate noise. Fidelity readout fits in one circuit via a "referee" Bell measurement on the output pair: P(Φ+) is exactly F. It is a non-LOCC verification step, so label it as such.
4. **Teleportation three ways:**
   - (a) deferred-measurement controlled gates: 4 entangling gates, F≈0.981;
   - (b) Pauli-frame XOR in post-processing: 2 entangling gates, F≈0.988, honest LOCC;
   - (c) post-select m=00: keeps 25% of shots.
   - Teaching point: (a) is *not* physical teleportation because its correction gates act across the boundary.
   - Gate teleportation (nonlocal CNOT via 1 ebit) uses 4 qubits and about 3–5 entangling gates. It connects directly to Oxford's 2025 86% teleported CZ: our simulated noise-only number is much higher, and the difference is the photonic link's infidelity.
5. **"Repeater race":** a swapping chain of up to 14 links on Forte's 29 qubits (fidelity 0.995→0.876), compared with direct fiber transmission (PLOB curve). Insert a distillation round before swapping to show the nested BDCZ idea. Use the 2026 USTC numbers (550 ms vs 450 ms; 420 km crossover) as real-world anchors.
6. **Nonlocal-games arcade:** CHSH (0.844 noisy vs 0.75), GHZ (0.978 vs 0.75), magic square (0.979 vs 0.889).
   - Under "one job per run", each question pair is a separate circuit. A single-circuit variant can draw the settings from |+⟩ ancilla "quantum coins" with controlled rotations. My estimate is S≈2.68 for CHSH with 5 entangling gates; this is an extrapolation, not simulated.
7. **GHZ scaling on all-to-all hardware:** fidelity vs n up to 29, plus an arbitrary graph state at exactly |E| gates on IonQ. The contrast is SWAP overhead on heavy-hex IBM noise models. Show the GME witness F>1/2 and the Mermin value's exponential gap.
8. **Monogamy: GHZ vs W.** Trace out one qubit and compute concurrence: GHZ gives 0, W gives 2/3. The 3-tangle is 1 vs 0. Uses `qiskit.quantum_info.concurrence`.
9. **BB84 / E91 / DI-QKD with Eve:** QBER climbs to 25% under intercept-resend and S falls to √2. At the noisy baseline, the DI key rate is about 0.71 bits per round asymptotically. Wiesner money is a 1-qubit-per-bill side game in which a counterfeiter succeeds with probability (3/4)ⁿ.

**Rough rule of thumb** (for depolarizing noise): the verified fidelity of an m-gate Clifford entangling protocol is about (1−4ε2/3)^m on the Werner visibility, times about (1−2p_ro) per parity-relevant readout.

### Gaps
- I did not run the actual IonQ Forte or IBM device noise models, since qiskit-ionq noise models were not installed here. Absolute numbers will differ: real Forte figures and SPAM are not modelled, nor is idle/crosstalk noise. Treat the 0.5% depolarizing numbers as order-of-magnitude anchors.
- Whether a single IonQ "job" may contain multiple circuits (a multicircuit job) is unverified. This determines whether multi-setting demos (CHSH needs 4 circuits, tomography 3, the magic square 9) count as "one job".
- Readout-error effects on post-selected distillation were not simulated. Flag misfires would lower the ~0.985 ceiling.
- I did not do a systematic survey of existing visual teaching tools (QuVis, Quantum Flytrap, Quirk). The adjacent education-tools notes may cover these.
- The Qiskit-in-Pyodide performance limits for density-matrix simulation are my estimate, not measured.
