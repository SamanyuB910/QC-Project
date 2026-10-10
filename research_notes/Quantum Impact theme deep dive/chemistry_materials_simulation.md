# Quantum chemistry, materials science and physical simulation: knowledge base for a "Quantum Impact" project (Qollab x IonQ, Oct 9–11, 2026)

Scope: the electronic-structure pipeline, IonQ and trapped-ion chemistry results from 2019 to 2026, materials and physics simulation targets, public datasets, honest classical baselines, and 3–5 project designs that fit the build constraints. The constraints are Qiskit 2.x in Pyodide; qiskit-nature 0.8.0 plus a PySCF preset; IonQ GPi/GPi2/ZZ(θ) with all-to-all connectivity; Forte noise models up to 29 qubits; about 100 two-qubit gates at about 0.5% error; one job per run; no dynamic circuits; and a Run button that has to finish fast.

**Labels:** **[2025]** and **[2026]** mark recent results. **[vendor]** marks a company claim with no independent check. **[own test]** marks something I measured in this session:
- Browser tests ran in stock Pyodide 314.0.7 in the Claude desktop browser pane.
- Chemistry runs used PySCF 2.14.0, ffsim 0.0.84, qiskit-addon-sqd 0.14.0 and Qiskit 2.5.2 in a temporary WSL Ubuntu 24.04 venv, which I deleted afterwards.
- Every script and raw JSON result is in `research_notes/Quantum Impact theme deep dive/scripts/chemistry/`.

---

## Q1. The electronic-structure pipeline: what each stage is, which variants fit IonQ hardware, and what actually runs in the browser

### Takeaway
The standard pipeline runs geometry → Hartree–Fock → active space → second-quantized Hamiltonian → qubit mapping → state preparation → measurement → mitigation → classical post-processing.

On IonQ, the only pre-fault-tolerant variant that needs exactly **one circuit per job** is sample-based diagonalization (QSCI/SQD/SKQD). It measures only in the Z basis and comes with built-in particle-number post-selection. That makes it the best structural fit for the "one job per run" rule.

The catch, which I measured: **at ≤24 qubits, SQD's classical machinery recovers the exact answer even from pure noise.** A credible project therefore has to cap the subspace and compare against classical selection heuristics.

PySCF does **not** install in stock Pyodide. Most of qiskit-addon-sqd is pure numpy, but it hard-depends on jax and pyscf. A numpy FCI/SCI solver of about 60 lines runs in the browser up to about 5,000 determinants in a few seconds.

### Cited Findings

**Reviews to anchor the theory**
- McArdle, Endo, Aspuru-Guzik, Benjamin, Yuan, "Quantum computational chemistry", Rev. Mod. Phys. 92, 015003 (2020) — [arXiv:1808.10402](https://arxiv.org/abs/1808.10402)
- Cao et al., "Quantum Chemistry in the Age of Quantum Computing", Chem. Rev. 2019 — [arXiv:1812.09976](https://arxiv.org/abs/1812.09976)
- Bauer, Bravyi, Motta, Chan, "Quantum algorithms for quantum chemistry and quantum materials science", Chem. Rev. 2020 — [arXiv:2001.03685](https://arxiv.org/abs/2001.03685)
- Tilly et al., "The Variational Quantum Eigensolver: a review of methods and best practices" (2021/2022) — [arXiv:2111.05176](https://arxiv.org/abs/2111.05176)

**Fermion-to-qubit mappings and qubit reduction**
- The Bravyi–Kitaev transformation for electronic structure was introduced to chemistry by Seeley, Richard and Love (2012) — [arXiv:1208.5986](https://arxiv.org/abs/1208.5986)
- Symmetry tapering removes qubits using Z2 symmetries, for example the parity-mapping two-qubit reduction — Bravyi, Gambetta, Mezzacapo, Temme, "Tapering off qubits to simulate fermionic Hamiltonians" (2017) — [arXiv:1701.08213](https://arxiv.org/abs/1701.08213)
- Under Jordan–Wigner (JW), a Givens rotation between JW-adjacent spin-orbitals has no Z string. Kivlichan et al. show that a full orbital rotation fits in linear depth on a line — [PRL 120, 110501 (2018), arXiv:1711.04789](https://arxiv.org/abs/1711.04789). Jiang et al. give Givens-rotation algorithms for preparing Slater determinants and fermionic Gaussian states — [Phys. Rev. Applied 9, 044036 (2018), arXiv:1711.05395](https://arxiv.org/abs/1711.05395)

**Native IonQ cost of fermionic building blocks [own test]**
Method: Qiskit 2.3 transpile to basis {rzz, rz, rx, ry}, where rzz stands in for IonQ Forte's arbitrary-angle ZZ(θ).

| Building block | Native ZZ count |
|---|---|
| Givens rotation (XX+YY type) | **2** |
| Density–density phase exp(iθ n_p n_q), the Jastrow term | **1** |
| CNOT | 1 |
| Heisenberg bond XX+YY+ZZ | **3** |
| JW hopping across a 2-qubit Z string (XZZX+YZZY) | 9 |

Source: [scripts/chemistry/gatecount.py](https://pypi.org/project/qiskit/). Forte's native gate set is `gpi, gpi2, zz`, per the [IonQ API backend record](https://api.ionq.co/v0.4/backends/qpu.forte-enterprise-1) (cited in the earlier note `ionq_hardware_and_sdk.md`).

**Ansätze**
- **UCCSD and its problems:** the IonQ authors note that the CNOT count of uCCSD scales as O(N⁴) and that "even the most efficient implementations... contain thousands of entangling gates for small systems" — [Zhao et al., arXiv:2212.02482](https://arxiv.org/abs/2212.02482)
- **k-UpCCGSD:** Lee, Huggins, Head-Gordon, Whaley, "Generalized Unitary Coupled Cluster Wavefunctions for Quantum Computation" — [arXiv:1810.02327](https://arxiv.org/abs/1810.02327)
- **ADAPT-VQE** grows the ansatz operator by operator using energy gradients — [Grimsley et al., Nat. Commun. 10, 3007 (2019), arXiv:1812.11173](https://arxiv.org/abs/1812.11173). qubit-ADAPT uses Pauli-string operators for hardware-efficient ansätze — [Tang et al., PRX Quantum 2, 020310 (2021), arXiv:1911.10205](https://arxiv.org/abs/1911.10205)
- **Hardware-efficient ansatz:** BeH₂ on 6 qubits — [Kandala et al., Nature 549, 242 (2017), arXiv:1704.05018](https://arxiv.org/abs/1704.05018)
- **Pair or seniority-zero ansätze**
  - The pUCCD hard-core-boson mapping halves the qubit count.
  - IonQ ran orbital-optimized upCCD end-to-end on Harmony and Aria with "up to 12 qubits and 72 variational parameters". Aria's better fidelity cut energy error by 38% versus Harmony — [Zhao et al., npj Quantum Inf. 2023, arXiv:2212.02482](https://arxiv.org/abs/2212.02482)
  - Google ran pair-correlated simulations on up to 20 qubits with purification-based mitigation — [O'Brien et al., Nat. Phys. 2023, arXiv:2210.10799](https://arxiv.org/abs/2210.10799)
- **Orbital rotations only:** Hartree–Fock on 12 qubits (H₁₂) — [Arute et al., Science 369, 1084 (2020), arXiv:2004.04174](https://arxiv.org/abs/2004.04174)
- **LUCJ (local unitary cluster Jastrow)**
  - Form: orbital rotations alternating with density–density (Jastrow) layers. "Local" variants keep only interactions that the qubit topology allows (square, hex, heavy-hex) and so need no SWAPs. The authors argue it describes strong correlation better than qUCCSD with "vastly reduced quantum resource requirements" — [Motta, Sung, Whaley, Head-Gordon, Shee, Chem. Sci. 14, 11213 (2023)](https://pubs.rsc.org/en/Content/ArticleLanding/2023/SC/D3SC02516K)
  - In IBM's SQD experiments, parameters came from classical CCSD, with no quantum optimization. "Local" means opposite-spin density–density terms only between heavy-hex-adjacent qubits. The authors flag a limit: no more than about six opposite-spin pairs can couple when N_MO > 21 — [Robledo-Moreno et al., arXiv:2405.05068](https://arxiv.org/html/2405.05068v3)

**[own test] Native-ZZ counts for one UCJ circuit on IonQ** (ffsim UCJOpSpinBalanced from CCSD t-amplitudes, N₂/cc-pVDZ active spaces, transpiled to the rzz basis with ffsim's PRE_INIT pass merging the first orbital rotation into HF prep). The last column is a white-noise fidelity estimate, F ≈ 0.995^(#ZZ) × 0.995^(#qubits).

| Active space | Qubits | UCJ, all-to-all Jastrow: ZZ (2q depth) | Heavy-hex-pattern LUCJ: ZZ | F (all-to-all / LUCJ) |
|---|---|---|---|---|
| (4e,4o) | 8 | 60 (20) | 39 | 0.71 / 0.79 |
| (6e,5o) | 10 | 76 (24) | 54 | 0.65 / 0.73 |
| (10e,6o) | 12 | 58 (23) | 53 | 0.70 / 0.72 |
| (6e,6o) | 12 | 146 (37) | 92 | 0.45 / 0.59 |
| (8e,8o) | 16 | 264 (49) | 157 | 0.25 / 0.42 |
| (10e,8o) | 16 | 206 (44) | 149 | 0.33 / 0.44 |
| (10e,10o) | 20 | 314–348 | 242–258 | 0.16–0.19 / 0.25–0.27 |
| (10e,12o) | 24 | 484 | 378 | 0.08 / 0.13 |

- Two layers (n_reps=2) roughly double these counts, for example (10e,8o) all-to-all goes to 380 ZZ.
- Sources: [scripts/chemistry/small_counts.py and sqd_capped_study.py](https://pypi.org/project/ffsim/), using [ffsim 0.0.84](https://pypi.org/project/ffsim/)

**Measurement reduction**
- Low-rank (double) factorization of the two-electron tensor gives "a cubic reduction in term groupings over prior state-of-the-art", at the cost of a linear-depth basis-rotation circuit before measurement, and enables post-selection-based mitigation — [Huggins et al., npj Quantum Inf. 7, 23 (2021), arXiv:1907.13117](https://arxiv.org/abs/1907.13117)
- Classical shadows predict many properties from few randomized measurements — [Huang, Kueng, Preskill, Nat. Phys. 16, 1050 (2020), arXiv:2002.08953](https://arxiv.org/abs/2002.08953). The fermionic (matchgate) version handles k-RDMs — [Zhao, Rubin, Miyake, PRL 127, 110504 (2021), arXiv:2010.16094](https://arxiv.org/abs/2010.16094)
- **[own test] Pauli terms and grouping, N₂/cc-pVDZ, JW:**

  | Active space | Qubits | Pauli terms | QWC groups | General-commuting groups |
  |---|---|---|---|---|
  | (6e,4o) | 8 | 61 | 17 | 3 |
  | (10e,6o) | 12 | 287 | 92 | 15 |
  | (10e,8o) | 16 | 825 | 226 | 27 |
  | (10e,10o) | 20 | 2,063 | 450 | 81 |
  | (10e,12o) | 24 | 4,201 | 878 | 114 |

  Source: [scripts/chemistry/grouping_and_fcidump.py](https://pypi.org/project/pyscf/)
- So a single VQE energy evaluation needs 17–878 distinct measurement circuits, while SQD/QSCI needs one.

**Error mitigation for chemistry**
- **Symmetry verification**
  - Measure a conserved quantity, such as particle number or parity, and discard violating shots — [Bonet-Monroig et al., PRA 98, 062339 (2018), arXiv:1807.10050](https://arxiv.org/abs/1807.10050)
  - Related: [McArdle, Yuan, Benjamin, PRL 122, 180501 (2019), arXiv:1807.02467](https://arxiv.org/abs/1807.02467)
- **McWeeny purification of noisy reduced density matrices "dramatically improves accuracy"**
  - Applied to NaH, KH and RbH, using 4 qubits on IBM Tokyo and Rigetti Aspen — [McCaskey et al., npj Quantum Inf. 5, 99 (2019), arXiv:1905.01534](https://arxiv.org/abs/1905.01534)
- **Reference-state error mitigation (REM)**
  - Method: measure a classically solvable reference state, such as Hartree–Fock, on the same hardware and subtract its error.
  - Cost: "only one or no additional measurements".
  - Results: "two orders-of-magnitude improvement" for H₂, HeH⁺ and LiH on superconducting hardware, plus simulations above 1,000 two-qubit gates — [Lolur et al., JCTC 19, 783 (2023), arXiv:2203.14756](https://arxiv.org/abs/2203.14756)
- **Echo verification and virtual distillation**
  - Error reduced "by one to two orders of magnitude below less sophisticated techniques (e.g. post-selection)", on up to 20 qubits.
  - The same paper concludes that "significant hardware improvements will be required for classically intractable variational chemistry simulations" — [O'Brien et al., arXiv:2210.10799](https://arxiv.org/abs/2210.10799)
- IonQ's QC-AFQMC run used leakage-detection gadgets: two ZZ gates plus one ancilla on half the qubits, which added 8 ancillas, with flagged shots discarded. The target was spontaneous emission during Raman ZZ gates — [Zhao et al., arXiv:2506.22408](https://arxiv.org/html/2506.22408v1)

**QSCI, SQD and SKQD: the sample-then-diagonalize family**
- **QSCI** [2023; journal 2026]
  - Method: prepare an approximate state, sample in the Z basis to pick important configurations, then project and diagonalize classically. The energy "strictly satisfies the variational principle" even with noise.
  - Hardware demonstration: an 8-qubit molecular Hamiltonian — [Kanno et al., arXiv:2302.11320; Phys. Rev. Research 8, 023268 (2026)](https://arxiv.org/abs/2302.11320)
- **SQD** [2024 preprint; Science Advances 11, eadu9991, June 2025] — [Robledo-Moreno et al., arXiv:2405.05068](https://arxiv.org/html/2405.05068v3)
  - Hardware: IBM Heron plus up to 6,400 Fugaku nodes.

    | System | Active space | Qubits | Two-qubit gates |
    |---|---|---|---|
    | N₂, cc-pVDZ | (10e,26o) | 58 | ~1–1.5k |
    | [2Fe-2S] | (30e,20o) | 45 | ~1–1.5k |
    | [4Fe-4S] | (54e,36o) | 77 | ~3.5k |

  - Each system got about 10⁵–2.5×10⁶ shots and about 45 min of QPU time.
  - Self-consistent "configuration recovery" flips bits of wrong-particle-number shots using average orbital occupancies, converging in about 3 iterations. In an N₂/6-31G numerical test, raw samples needed about 20% signal for about 10 mHa error; with recovery, about 2% signal was enough.
  - Results: N₂ energies were "within tens of mE_h of HCI". [4Fe-4S] energies were worse than classical methods, though better than random bitstrings of the same subspace size. The authors state quantum advantage is not established.
- **SKQD (sample-based Krylov)** [2025]
  - Samples come from time-evolved states, with convergence guarantees under QPE-like overlap assumptions.
  - Largest run: the single-impurity Anderson model with 41 bath sites on **85 qubits with up to 6×10³ two-qubit gates** on ibm_fez, closely matching DMRG — [Yu et al., arXiv:2501.09702](https://arxiv.org/abs/2501.09702)
  - The revised version adds a four-impurity model on 70 qubits — [UChicago seminar and arXiv summary](https://arxiv.org/html/2501.09702v3)
- **SqDRIFT** [2025] combines SKQD with qDRIFT randomized compilation to keep convergence guarantees on today's devices — [Piccinelli et al., arXiv:2508.02578](https://arxiv.org/abs/2508.02578)
- **Scale-up** [2025–2026]
  - A closed-loop Heron + full-Fugaku (152,064 nodes) electronic-structure workflow — [Shirakawa et al., arXiv:2511.00224](https://arxiv.org/abs/2511.00224)
  - GPU (OpenMP offload) diagonalization at about 100× per node over CPU — [Walkup et al., arXiv:2601.16169](https://arxiv.org/abs/2601.16169)
- **Critiques (independent)**
  - Reinholdt et al. [2025] find QSCI "wastes effort by repeatedly sampling configurations it has already found", and that this gets worse at high accuracy or with approximate ansätze. Earlier versions were titled "Exposing a Fatal Flaw…" — [JCTC 21, 6811 (2025), arXiv:2501.07231](https://arxiv.org/abs/2501.07231)
  - Gaberle & Jattana [May 2026] built SQD subspaces directly from exact Heisenberg and Hubbard ground states. The number of configurations needed for fixed accuracy "grows exponentially with the system size", even when ordered optimally — [arXiv:2605.02494](https://arxiv.org/abs/2605.02494)
- **SQD on trapped ions**
  - BlueQubit ran SQD on Quantinuum H2 for a 2–6-plaquette copper-oxide chain [Dec 2025]. They found SQD "does not always converge on a practical timescale", that all-to-all connectivity is one lever against sampling bottlenecks, and that "noise on the… H2 device improved energy convergence beyond what noise-free statevector simulations predicted" — [Wray et al., arXiv:2512.04962](https://arxiv.org/abs/2512.04962)
  - SKQD for the Schwinger model ran on a trapped-ion processor (4-qubit proof of principle) and on IBM devices [Oct 2025] — [Rosanowski et al., arXiv:2510.26951](https://arxiv.org/abs/2510.26951)
  - I found no IonQ SQD paper.

**qiskit-addon-sqd packaging [own test, 2026-10-09]**
- v0.14.0 is a pure-Python wheel (`py3-none-any`), but it declares `jax>=0.4.30`, `jaxlib>=0.4.30` and `pyscf>=2.9` (non-win32) — [PyPI JSON](https://pypi.org/pypi/qiskit-addon-sqd/json)
- Which modules are portable:
  - Pure numpy + qiskit: `configuration_recovery.py` (`recover_configurations`), `subsampling.py` (`postselect_by_hamming_right_and_left`, `subsample`), `counts.py` and `trim.py`.
  - Not portable: `fermion.py` imports `jax` and `pyscf.fci.selected_ci` (the SCI solver behind `diagonalize_fermionic_hamiltonian`), and `qubit.py` imports jax.
  - Source: [qiskit_addon_sqd-0.14.0 wheel, inspected](https://pypi.org/project/qiskit-addon-sqd/)
- Pyodide 314.0.7's lockfile (357 packages) has no pyscf, jax or jaxlib. It does have h5py 3.13.0, sympy 1.14.0, scipy 1.18.0 and numpy 2.4.6 — [pyodide-lock.json v314.0.7](https://cdn.jsdelivr.net/pyodide/v314.0.7/full/pyodide-lock.json)

**PySCF in the browser [own test, 2026-10-09]**
- `await micropip.install('pyscf')` in stock Pyodide 314.0.7 fails with `ValueError: Can't find a pure Python 3 wheel for 'pyscf'` — [own test, Pyodide console](https://pyodide.org/en/stable/console.html)
- PyPI pyscf 2.14.0 ships only macOS and manylinux wheels plus an sdist. There is **no Windows and no Emscripten wheel**, so offline precomputation on the user's Windows machine needs WSL, Linux, macOS or Colab — [PyPI JSON](https://pypi.org/pypi/pyscf/json)
- The Qollab "Qiskit Nature (+ PySCF)" preset adds `qiskit-nature==0.8.0` and `pyscf>=2.14.0,<3.0.0` to requirements.txt. Qollab installs only pure-Python wheels and Pyodide-built packages. A package "that need[s] compiled code with no Pyodide build stop[s] the run" with "Could not install every package listed in requirements.txt". The docs say nothing about custom wheels — [Qollab runtime docs](https://qollab.xyz/learn/docs/runtime-environment)
- Qollab's own H2 showcase says its Hamiltonians were "precomputed using qiskit-nature + PySCF" — [earlier note, theme_brief_and_qollab_platform.md](https://qollab.xyz/u/qollab/quantum-chemistry-showcase-t-2)

**qiskit-nature 0.8.0 without PySCF [own test]**
- The wheel was uploaded to PyPI on **2026-06-01**. It requires `qiskit>=1.4,<3`, `qiskit-algorithms>=0.4`, h5py, rustworkx and sympy. pyscf is only an optional extra — [PyPI JSON](https://pypi.org/pypi/qiskit-nature/json)
- `second_q/formats/fcidump` (`FCIDump.from_file`) and `fcidump_translator.fcidump_to_problem` exist. The pyscf imports in `symmetric_two_body.py` sit inside `try:` blocks with a numpy fallback — [qiskit_nature-0.8.0 wheel, inspected](https://pypi.org/project/qiskit-nature/)
- **Conflict:** a web search summary said 0.7.2 (2024-02-23) was the latest qiskit-nature and that the package looked "Inactive" — [snyk/piwheels via search](https://github.com/qiskit-community/qiskit-nature/releases). PyPI shows 0.8.0 (2026-06-01).

**[own test] Browser compute budget (Pyodide 314.0.7, numpy 2.4.6, scipy 1.18.0)**

| Workload | Time |
|---|---|
| Dense `numpy.linalg.eigh`, n = 400 / 1,225 / 2,000 | 0.39 s / 9.2 s / 37 s |
| Sparse Fermi-Hubbard ED (open 2×L ladder, U = 4t, half filling, scipy `eigsh`): 2×4, 16 qubits, dim 4,900 | 0.06 s build + 0.16 s solve |
| Same, 2×5, 20 qubits, dim 63,504 | 0.19 s + 1.87 s |
| Same, 2×6, 24 qubits, dim 853,776, 15.8M nonzeros | 1.9 s + 28.4 s |
| numpy Knowles–Handy-style direct FCI (`kh_fci.py`, ~60 lines, validated to 10⁻⁶ against the sparse-ED Hubbard energy −5.012503), (8e,8o), dim 4,900 | **4.0 s** (1.05 s in desktop CPython) |
| Same, (10e,10o), dim 63,504 | **189 s** (23 s in CPython) |
| numpy statevector, 100 random two-qubit gates, 12 / 16 / 20 qubits | 0.05 / 0.08 / 1.1 s |
| Sampling 2×10⁴ shots from a 20-qubit state | 0.06 s |

Source for all rows: [own test, Pyodide console](https://pyodide.org/en/stable/console.html)

### Inferences
- **Hardware fit:** SQD/QSCI is the natural IonQ algorithm. It needs one circuit and Z-basis measurement only, and its parameters come from CCSD with no VQE loop. Particle-number post-selection or recovery is built in. That matches "one job per run" and "judges press Run", whereas VQE needs 17–878 measurement circuits per energy evaluation at these sizes.
- **Where all-to-all helps:** on IonQ, every Jastrow term n_p·n_q, including any opposite-spin pair (p↑, q↓), is a single native ZZ(θ) with no SWAPs. Heavy-hex LUCJ must drop most of these pairs. The IonQ-native story is "full UCJ instead of local UCJ", and it is testable as an ablation: same circuit family, Jastrow pairs restricted versus unrestricted.
- **Browser architecture:**
  1. Vendor `configuration_recovery.py`, `subsampling.py` and `counts.py`, which are Apache-2.0 and import only numpy and qiskit.
  2. Replace the pyscf SCI solver with the numpy direct-CI code restricted to the sampled α/β string sets.
  3. Keep live subspaces at or below about 5×10³–10⁴ determinants (seconds). Precompute anything bigger, plus all FCI references, offline and ship them as JSON.
- **First thing to check on Oct 9–10:** whether the Qollab PySCF preset actually imports, with a 3-line `from pyscf import gto, scf` test. My stock-Pyodide test and the "precomputed" wording on Qollab's own showcase suggest it may not.

### Gaps
- I could not verify inside Qollab itself whether its preset ships a custom PySCF WebAssembly build, because that needs a signed-in Qollab run. If it works, which basis sets and molecule sizes are feasible is unknown. A guess: an STO-3G/6-31G SCF for under ~10 atoms would be seconds in WASM, but this is not measured.
- I found no per-circuit two-qubit gate count for IonQ's oo-upCCD hardware runs, only "up to 12 qubits, 72 parameters".
- I did not benchmark classical-shadow or double-factorized measurement costs for these active spaces.

---

## Q2. IonQ and trapped-ion chemistry results, 2018–2026: what was computed, at what size, and what the claims rest on

### Takeaway
Chemistry runs on IonQ hardware have stayed small:
- 2019–2020: water VQE executed with 3 parameters, with errors of about 27–35 mHa against FCI.
- 2022: 12-qubit pair-correlated VQE.
- 2025: a 24-qubit (16 system + 8 ancilla) QC-AFQMC trial state on an (8e,8o) active space.

The ">20×" AstraZeneca/AWS/NVIDIA number is a **time-to-solution** claim against IonQ's own earlier 4-qubit benchmark. It is **not** an accuracy or quantum-advantage claim. On the QPU the reaction barriers were about 10 kcal/mol off CCSD(T).

Quantinuum leads on trapped-ion chemistry fidelity, with QPE on [[7,1,3]] logical qubits for H₂ and Helios Fermi-Hubbard pairing on up to 90 qubits.

### Cited Findings

**Early trapped-ion chemistry**
- Innsbruck's trapped-ion chemistry calculations (Hempel et al., 2018) — [PRX 8, 031022, arXiv:1803.10238](https://arxiv.org/abs/1803.10238)

**IonQ water VQE (Nam et al., arXiv Feb 2019; npj Quantum Inf. 2020)** — [arXiv:1902.10171](https://ar5iv.labs.arxiv.org/html/1902.10171); [DOI 10.1038/s41534-020-0259-3](https://www.doi.org/10.1038/S41534-020-0259-3)
- Basis: STO-3G with 7 spatial orbitals.
- The full UCC circuit (HF+17) needs 11 qubits and **143 entangling gates** (89 CNOT + 54 small-angle XX).
- Hardware ran only HF+1, HF+2 and HF+3, i.e. three parameters, at one geometry (O–H ≈ 1.8 a₀).
- Energies were −74.977, −74.979 and −74.985 Ha against FCI −75.0116 Ha, i.e. **35, 33 and 27 mHa errors**.
- "Chemical accuracy" in the paper means agreement with the in-silico VQE at the same ansatz level, not with FCI.
- No error mitigation apart from SPAM correction.

**IonQ pair-correlated VQE (Zhao et al., Dec 2022; npj QI 2023)** — [arXiv:2212.02482](https://arxiv.org/abs/2212.02482)
- Orbital-optimized upCCD on Harmony and Aria, with up to 12 qubits and 72 parameters, end-to-end.
- The paper's comparison table lists **Li₂O, 12 qubits, 72 parameters, full VQE, IonQ (2022)**.
- Relative energies across geometries were in "excellent agreement with noise-free simulators".
- Aria had 38% less energy error than Harmony.

**IonQ + Hyundai battery chemistry**
- Announced January 19, 2022: new VQE algorithms for lithium compounds, aiming to simulate lithium oxide, "the largest battery chemistry model yet to be run on a quantum computer" — [IonQ IR](https://investors.ionq.com/news/news-details/2022/IonQ-and-Hyundai-Motor-Partner-to-Use-Quantum-Computing-to-Advance-Effectiveness-of-Next-gen-Batteries/default.aspx)
- An interview-sourced plan of "at least 12 qubits and over 100 gate operations" — [statnano summary](https://statnano.com/world-news/90454/How-Quantum-Computers-Can-Make-Batteries-Better)
- Inference: the Li₂O 12-qubit oo-upCCD row in Zhao et al. is the published outcome.

**IonQ + AstraZeneca + AWS + NVIDIA [2025]**
- **Press release, June 9, 2025** [vendor] — [IonQ news](https://ionq.com/news/ionq-speeds-quantum-accelerated-drug-development-application-with); [The Quantum Insider](https://thequantuminsider.com/2025/06/09/ionq-speeds-quantum-accelerated-drug-development-application-in-partnership-with-astrazeneca-aws-and-nvidia/)
  - Claims: "more than a 20x speedup in time-to-solution compared to prior benchmarks" and runtime cut "from months to days".
  - Setup: Forte + CUDA-Q on Amazon Braket with H200 GPUs on ParallelCluster, targeting the Suzuki–Miyaura reaction.
- **Paper, June 27, 2025** — [arXiv:2506.22408](https://arxiv.org/html/2506.22408v1)
  - Method: QC-AFQMC with matchgate shadows.
  - Target: the **oxidative-addition step** of the Ni-catalysed Suzuki–Miyaura reaction, using 41-atom reduced models truncated from 77 atoms.
  - Active space and trial state: **(8e,8o)**, with a VQE-optimized upCCD trial state (optimized on an ideal simulator with COBYLA).
  - Qubits: **24 on Forte (16 trial + 8 leakage-detection ancillas)**.
  - QPU load: about 300,983 circuits in total, with about 58–61k single-shot shadows per structure.
  - Barriers (kcal/mol):

    | Barrier | CCSD(T) | QPU | Ideal simulator |
    |---|---|---|---|
    | B → TS | 53.3 | 43±3 | 57±4 |
    | C → TS | 45.4 | 55±3 | 44±4 |

  - So the QPU results are about 10 kcal/mol off and the ideal simulator about 4 kcal/mol off.
  - The **9×** speedup is QPU circuit time (median 9.9 s → 1.1 s). The **656×** is GPU post-processing versus the prior state of the art: Huang et al.'s 4-qubit, (4,3)-active-space, 4,000-shadow Aria run.
  - Costs: about 13–17k GPU-hours per molecule. QPU collection was projected at 34.5 days untuned versus 3.8 days tuned.
  - AstraZeneca co-authors are listed (Kovyrshin, Tornberg, Broo).

**IonQ QC-AFQMC atomic forces [Oct 13, 2025; vendor framing]**
- Claim: forces "more accurate than those derived using classical methods", with an unnamed Global-1000 automaker, framed around carbon capture — [IonQ news](https://ionq.com/news/ionq-quantum-computing-achieves-greater-accuracy-simulating-complex-chemical)
- The linked paper treats H-chains, N₂, stretched H₄, stretched CO₂ and the **MEA–CO₂ carbon-capture reaction** using correlated sampling with one reused shadow ensemble. The abstract compares against single-reference and coupled-cluster methods, which "qualitatively fail" in strong correlation. It does not state whether any run was on a QPU — [Goings et al., arXiv:2507.17992](https://arxiv.org/abs/2507.17992)
- Quantum Computing Report names Hyundai — [QCR](https://quantumcomputingreport.com/ionq-and-hyundai-utilize-qc-afqmc-to-advance-accurate-nuclear-force-computations-for-materials-modeling/)

**IonQ materials quantum GAN [Apr–May 2025]**
- A hybrid quantum-classical Wasserstein GAN generating 5-channel EBSD steel-microstructure images (ferrite and bainite), with Hyundai.
- It improved over classical Bernoulli GANs "in 70% of samples" on MMD — [Sekwao et al., arXiv:2504.08728](https://arxiv.org/abs/2504.08728); [IonQ news](https://ionq.com/news/ionq-demonstrates-quantum-enhanced-applications-advancing-ai)
- This is generative ML, not electronic structure.

**IonQ + Ansys "CFD" [Mar 20, 2025]** — [IonQ news](https://www.ionq.com/news/ionq-and-ansys-achieve-major-quantum-computing-milestone-demonstrating); [arXiv:2503.13128](https://arxiv.org/abs/2503.13128); [critique](https://wkirkpatrick.substack.com/p/ionq-and-ansys); [TQI](https://thequantuminsider.com/2025/03/20/ionqs-devices-boost-ansys-simulations-achieving-up-to-12-faster-processing-over-classical-computers/)
- What it actually was: **not a fluid simulation on a QPU**. VarQITE did graph partitioning to reduce fill-in in the sparse factorization inside LS-DYNA, for a blood-pump model with up to 2.6M vertices and 40M edges.
- The 12% is end-to-end wall-clock "up to 12% on certain problems", against industry heuristic partitioners.
- Criticisms: the large instances were classically simulated, and the mesh was refined about 100× so that factorization time mattered.
- A 2026 follow-up switched to iterative QAOA and reports up to 15% (at least 7%) amortized gains — [arXiv:2603.15515](https://arxiv.org/html/2603.15515)

**Quantinuum chemistry**
- **Protein–ligand binding** (Kirsopp et al., Cambridge Quantum + Roche): DMET+VQE for 12 BACE1 inhibitors, with Partition Measurement Symmetry Verification, on superconducting and trapped-ion hardware — [arXiv:2110.08163](https://arxiv.org/abs/2110.08163)
- **Bayesian QPE with error detection** for H₂ — [Yamamoto et al., arXiv:2306.16608](https://arxiv.org/abs/2306.16608)
- **QEC chemistry [2025]** — [Yamamoto et al., arXiv:2505.09133](https://arxiv.org/abs/2505.09133); [TQI](https://thequantuminsider.com/2025/05/22/quantum-chemistry-gets-error-corrected-boost-from-quantinuums-trapped-ion-computer/)
  - QPE for H₂ on H2-2 with the [[7,1,3]] color code and mid-circuit Steane QEC.
  - v1: 22 qubits, up to 2,185 two-qubit gates and 760 mid-circuit measurements, with E−E_FCI = 0.018(10) Ha.
  - v2: E−E_FCI = 0.001(13) Ha.
  - Memory noise was the dominant error.
- **Helios hardware:** 98 qubits; two-qubit error 7.9×10⁻⁴, one-qubit error 2.5×10⁻⁵, SPAM error 4.8×10⁻⁴ — [Helios paper abstract via search](https://www.quantinuum.com/blog/helios-delivers-quantum-advantage-with-real-world-impact)
- **Superconducting pairing in Fermi-Hubbard models on Helios** — [Granet et al., arXiv:2511.02125](https://arxiv.org/abs/2511.02125); [Quantinuum blog](https://www.quantinuum.com/blog/helios-delivers-quantum-advantage-with-real-world-impact)
  - Three settings: light-driven pairing on a half-filled square lattice, d-wave pairing in a checkerboard model at 1/6 doping, and s-wave pairing in a bilayer nickelate model.
  - Scale: up to 90 qubits (72 system + 18 ancilla) on a 6×6 lattice [vendor framing on classical hardness].
- **Digital quantum magnetism** on H2 (56 qubits): 2D transverse-field Ising Floquet prethermalization, 99.94% partial-entangler fidelity, over 2,000 two-qubit gates — [Haghshenas et al., Nature 653, 56–62 (2026), arXiv:2503.20870](https://arxiv.org/abs/2503.20870)
- **Q2-2026 earnings [vendor]:** a "new parallel quantum phase-estimation algorithm" for molecular properties and "near five-nines logical fidelity on Helios" — [Quantinuum press release](https://www.quantinuum.com/press-releases/quantinuum-reports-second-quarter-2026-results)

**The IonQ Forte devices you can use (from the earlier note)**
- 36 qubits, 99.6% two-qubit fidelity, native gates gpi/gpi2/zz.
- Simulator noise models: forte-1 and forte-enterprise-1, up to 29 qubits.
- Sources: [IonQ – Forte](https://www.ionq.com/quantum-systems/forte); [IonQ API backends](https://api.ionq.co/v0.4/backends/qpu.forte-enterprise-1)

### Inferences
- **What has worked on IonQ hardware for chemistry:**
  - About 10–16 system qubits with about 50–150 two-qubit gates and shallow pair or upCCD circuits.
  - Accuracy comes mainly from error cancellation in relative energies, plus heavy classical post-processing.
- **Pitching the hackathon project:** "24 qubits on Forte" (the AstraZeneca work) is the high-water mark to cite. Avoid repeating the ">20×" as a quantum speedup; it is a workflow and GPU engineering result.
- **Uncontested space:** nobody has published SQD on IonQ. Quantinuum (Wray et al.) and IBM own the trapped-ion and superconducting SQD literature, so "SQD on IonQ-native all-to-all UCJ" is open.

### Gaps
- I did not obtain exact two-qubit gate counts for the QC-AFQMC upCCD trial circuit ("O(N²) entangling gates" only), or the AFQMC shadow-circuit depth.
- I could not confirm whether the Oct 2025 force results used Forte hardware or a simulator.
- I found no 2026 IonQ chemistry hardware paper.

---

## Q3. Materials and physics simulation targets: which are credible, and what has actually been shown

### Takeaway
The credible near-term physics targets on all-to-all trapped ions are:
- lattice models with exact classical references at hackathon size: Fermi-Hubbard (cuprate-motivated parameters), Heisenberg/Ising magnetism, and the Schwinger model;
- small active-space "slices" of real chemistry: N≡N cleavage, Ni/Ru/Fe catalysis, Li-ion electrolytes and cathodes, MEA–CO₂ capture, covalent drug binding.

Fault-tolerant resource estimates exist for catalysis (FeMoco, Ru–CO₂, P450) and batteries (LiNiO₂, Li₂FeSiO₄, electrolytes). Pairing a tiny hardware slice with that estimate is the honest "impact" narrative.

### Cited Findings

**Hubbard model and cuprates**
- **One-band parameter evidence:**
  - DQMC with U = 8t, t′/t = −0.3 at T = t/3 matched neutron-scattering χ″(q,ω) — [LeBlanc et al., PRB 100, 075123 (2019), arXiv:1904.10782](https://arxiv.org/abs/1904.10782)
  - Fits to spin waves and dispersions give t ≈ 0.33–0.34 eV, t′/t ≈ −0.25 to −0.28, U/t ≈ 6–6.2 — [search snippet, likely Markiewicz et al., arXiv:cond-mat/0308469](https://arxiv.org/pdf/cond-mat/0308469)
  - Downfolding from three-band models gives a larger effective U/t and density-assisted hopping. An ab-initio static Ũ ≈ 3.65 eV for La₂CuO₄ — [Sheshadri et al., arXiv:2211.14019](https://arxiv.org/abs/2211.14019)
- **Benchmarks for 2D Hubbard across many numerical methods:** [LeBlanc et al., PRX 5, 041041 (2015), arXiv:1505.02290](https://arxiv.org/abs/1505.02290)
- **Helios pairing-correlation experiments, including light-induced pairing:** see Q2 — [arXiv:2511.02125](https://arxiv.org/abs/2511.02125)

**Spin models and magnetism**
- Quantinuum H2, 56-qubit 2D Ising Floquet prethermalization — [Nature 653, 56 (2026)](https://arxiv.org/abs/2503.20870)
- The SQD critique for Heisenberg and Hubbard models shows exponential subspace growth — [arXiv:2605.02494](https://arxiv.org/abs/2605.02494)

**Lattice gauge theory**
- First digital simulation of Schwinger-model pair creation on 4 trapped-ion qubits — [Martinez et al., Nature 534, 516 (2016), arXiv:1605.04570](https://arxiv.org/abs/1605.04570)
- SKQD for the Schwinger model on a trapped-ion device and on IBM devices [2025] — [arXiv:2510.26951](https://arxiv.org/abs/2510.26951)

**Catalysis and nitrogen fixation**
- FeMoco reaction-mechanism estimate — [Reiher et al., PNAS 114, 7555 (2017), arXiv:1605.03590](https://arxiv.org/abs/1605.03590)
- Ru catalyst for CO₂ → methanol with double factorization — [von Burg et al., PRR 3, 033055 (2021), arXiv:2007.14460](https://arxiv.org/abs/2007.14460)
- Cytochrome P450 — [Goings et al., PNAS 2022, arXiv:2202.01244](https://arxiv.org/abs/2202.01244)
- Numbers are in Q5.

**Batteries**
- Electrolyte molecules, including fluoroethylene carbonate, on a fusion-based photonic machine — [Kim et al. (PsiQuantum + Mercedes-Benz), PRR 4, 023019 (2022), arXiv:2104.10653](https://arxiv.org/abs/2104.10653)
- LiNiO₂-relevant cathode models with Bloch-orbital THC — [Rubin et al. (Google + BASF), PRX Quantum 4, 040303 (2023), arXiv:2302.05531](https://arxiv.org/abs/2302.05531)
- Li₂FeSiO₄ cathode, first-quantized — [Delgado et al. (Xanadu + VW), PRA 106, 032428 (2022), arXiv:2204.11890](https://arxiv.org/abs/2204.11890)
- IonQ/Hyundai Li₂O (Q2)

**Carbon capture**
- IonQ's MEA–CO₂ reaction-force study — [arXiv:2507.17992](https://arxiv.org/abs/2507.17992)

**Drug discovery**
- **BACE1 protein–ligand binding energies** with DMET+VQE — [Kirsopp et al., arXiv:2110.08163](https://arxiv.org/abs/2110.08163)
- **Covalent KRAS G12C inhibition by sotorasib**, plus Gibbs free-energy profiles for prodrug C–C bond cleavage — [Li et al., "A Hybrid Quantum Computing Pipeline for Real World Drug Discovery", arXiv:2401.03759](https://arxiv.org/abs/2401.03759)
  - Method: QM/MM with the QM region covering the covalent-bond atoms.
  - Active space: **(2e,2o) on 2 qubits**. The quantum part is tiny.
- **KRAS inhibitor generation:** a separate 2024–2025 study used a QCBM + LSTM generative model to screen over 1M molecules. Candidates showed micromolar SPR binding to KRAS G12D, G12C and G12V. This is generative ML, not electronic structure — [PMC commentary](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12075789/)

**Photophysics and materials VQE on hardware**
- Earlier hardware runs include a 2-qubit HEA for TADF emitters (IBM, 2021) and a 2-qubit HEA for a Li₂O₄ model (IonQ, 2021), per the comparison table in [arXiv:2212.02482](https://arxiv.org/abs/2212.02482)

**Engineering "CFD" on IonQ**
- This is the Ansys LS-DYNA graph-partitioning work (Q2). It is not quantum fluid dynamics — [arXiv:2503.13128](https://arxiv.org/abs/2503.13128)

### Inferences
- **Real all-to-all benefits for Hamiltonian simulation:**
  - The Hubbard on-site term n↑n↓ couples qubit i to qubit i+L under JW block ordering, which is one native ZZ on Forte but a long-range interaction on a line or heavy-hex.
  - Schwinger-model gauge elimination yields long-range Z_iZ_j couplings, which are all native on Forte.
- **Trotter cost per step on Forte**, from my measured building-block costs:
  - 1D Hubbard, L sites: 4(L−1) ZZ for hopping + L for on-site, i.e. **5L−4**. That is 36 ZZ for L = 8 (16 qubits).
  - Heisenberg chain, N spins: 3(N−1) ZZ, i.e. 33 for N = 12.
  - Schwinger, N sites: about 2(N−1) for hopping + N(N−1)/2 long-range ZZ. That is about 63 for N = 10.
  - These are my inference from the measured costs, not published counts.
- **Most credible "real problem" framing:** a reaction where CCSD(T) fails, such as triple-bond cleavage or multireference transition-metal steps, with a small active space computed classically exactly. The quantum part is then a scaled-down but structurally identical step.

### Gaps
- I found no hardware demonstrations or sources for MOF carbon-capture or photovoltaic electronic structure on quantum hardware.
- I did not research linear-response or spectroscopy algorithms (Green's functions, dynamical correlation functions) in this pass.
- I did not verify the exact paper behind the "t = 0.34 eV, U/t = 6.2" snippet.

---

## Q4. Public datasets, browser accessibility, and shipping integrals under 2 MB

### Takeaway
- **Fetchable from a browser page (CORS):** PubChem PUG REST (3D SDF), RCSB PDB, PDBe, NCI CACTUS and GitHub raw.
- **Not fetchable from a browser:** NIST CCCBDB (HTML only), Materials Project (API key; unauthenticated calls fail) and its OPTIMADE endpoint, OQMD and COD.
- **Recommended route:** precompute active-space integrals offline (PySCF on Linux, WSL or Colab) and ship FCIDUMP or JSON.
  - D2h-symmetric N₂ with up to 26 active orbitals fits in 633 KB.
  - A no-symmetry molecule stays under 2 MB up to about 26 active orbitals in text format.

### Cited Findings

**[own test, 2026-10-09] Browser `fetch()` CORS results**
- Succeeded:
  - `pubchem.ncbi.nlm.nih.gov/rest/pug/.../SDF?record_type=3d` (200, ACAO `*`)
  - `files.rcsb.org/download/*.pdb` and `data.rcsb.org/rest/v1/core/entry/*` (ACAO `*`)
  - `www.ebi.ac.uk/pdbe/api/...` (ACAO `*`)
  - `cactus.nci.nih.gov/chemical/structure/<name>/file?format=xyz` (ACAO `*`)
  - `raw.githubusercontent.com` (ACAO `*`)
  - `figshare.com/ndownloader` (ACAO `*`, but returned 202)
- Failed with "Failed to fetch":
  - `api.materialsproject.org` without a key (401, no ACAO; preflight allows `X-Api-Key`, untested with a key)
  - `optimade.materialsproject.org`
  - `cccbdb.nist.gov`
  - `oqmd.org/optimade`
  - `crystallography.net/cod`
- Sources: own test, with curl `Origin` headers plus a browser `fetch()` from a pyodide.org/example.com page — [example PubChem URL](https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/aspirin/SDF?record_type=3d); [example GitHub raw URL](https://raw.githubusercontent.com/quantumlib/OpenFermion/master/src/openfermion/testing/data/H2_sto-3g_singlet_0.7414.hdf5)

**Ready-made integral files**
- OpenFermion's repo ships HDF5 molecular data:
  - an H₂/STO-3G bond scan from 0.1 to 3.0 Å
  - LiH/STO-3G at 1.45 Å
  - H₂/6-31G at 0.75 Å
- These are readable with h5py, which is in the Pyodide lock, and fetchable via GitHub raw with CORS — [GitHub API listing](https://api.github.com/repos/quantumlib/OpenFermion/contents/src/openfermion/testing/data)
- H₂ and LiH are "tutorial-level" for scoring.

**FCIDUMP sizes [own test]** (PySCF `tools.fcidump.from_integrals`, N₂/cc-pVDZ, D2h, tol 10⁻¹²)

| Active space | Size |
|---|---|
| (6e,4o) | 0.9 KB |
| (10e,8o) | 5.4 KB |
| (10e,12o) | 22 KB |
| 16 orbitals | 116 KB |
| 20 orbitals | 240 KB |
| 26 orbitals | 633 KB |

- Source: [scripts/chemistry/grouping_and_fcidump.py](https://pypi.org/project/pyscf/)
- qiskit-nature 0.8.0 parses FCIDUMP without PySCF (Q1) — [PyPI](https://pypi.org/project/qiskit-nature/)
- Qollab storage limits: "up to 100 files of up to 2 MB each, and all your projects together can use 200 MB". Data files are loaded into memory before the run, and large datasets should be streamed over GET — [Qollab runtime docs](https://qollab.xyz/learn/docs/runtime-environment)

**Benchmark systems with published references**
- N₂ dissociation (cc-pVDZ, used in IBM SQD), plus [2Fe-2S] and [4Fe-4S] — [arXiv:2405.05068](https://arxiv.org/html/2405.05068v3)
- Hydrogen-chain equation of state across many methods — [Motta et al., PRX 7, 031059 (2017), arXiv:1705.01608](https://arxiv.org/abs/1705.01608)
- 2D Hubbard benchmarks — [LeBlanc et al., PRX 5, 041041 (2015)](https://arxiv.org/abs/1505.02290)
- LiH STO-3G dissociation — [Zhao et al. Fig. 1, arXiv:2212.02482](https://arxiv.org/abs/2212.02482)
- BACE1 ligands — [arXiv:2110.08163](https://arxiv.org/abs/2110.08163)
- The Suzuki–Miyaura Ni oxidative-addition structures (B, TS, C) — [arXiv:2506.22408](https://arxiv.org/html/2506.22408v1)

### Inferences
- **Pattern to use:**
  1. Fetch a real geometry live, for example a PubChem 3D SDF or a PDB ligand pocket, for the narrative and the 3D view.
  2. Load precomputed FCIDUMP and JSON for the active space you actually solve: integrals, CCSD t-amplitudes, UCJ parameters, and FCI/CCSD(T) references.
  3. Keep each file at or below 2 MB.
- Materials Project data must be pre-downloaded with a key and shipped as a file.
- For a no-symmetry molecule the FCIDUMP has about M(M+1)/2 unique two-electron entries, with M = n(n+1)/2. That is about 22k entries for n = 20 and about 62k for n = 26, so about 0.7 MB and 1.9 MB at about 30 bytes per line. This is my arithmetic, not a measurement.

### Gaps
- I did not test the Materials Project API with a key. Its CORS behaviour on authenticated GET is unknown.
- I did not verify QM9, GDB or MoleculeNet download URLs or CORS in this pass.
- NIST CCCBDB has no API that I found, so scrape offline.

---

## Q5. Classical baselines and honest benchmarking: when classical methods fail, and what "advantage in chemistry" would require

### Takeaway
At equilibrium, CCSD(T) is already within chemical accuracy for my N₂ active spaces (0.70–0.81 mHa error). At 2.0 Å it fails non-variationally (CCSD −35.6 mHa, CCSD(T) −77.3 mHa), and that is where a quantum step can be meaningful.

Lee et al. (2023) argue that exponential advantage for ground-state chemistry is not generically expected. Fault-tolerant estimates for the flagship targets have dropped from about 10¹⁴–10¹⁵ T gates (2017) to about 10⁹–10¹⁰ Toffolis on about 1.5–4k logical qubits, with runtimes of about 1 day to a few days.

The honest benchmark for any NISQ chemistry demo is (a) exact FCI in the same active space, (b) CCSD(T), and (c) a classical selection heuristic at equal subspace budget, not random sampling.

### Cited Findings

**Chemical accuracy**
- About 1.6 mHa (4 kJ/mol, about 1 kcal/mol), "the target accuracy necessary to estimate chemical reaction rates at room temperature" — [Nam et al.](https://arxiv.org/pdf/1902.10171)

**[own test] N₂/cc-pVDZ errors versus CASCI/FCI in the same active space**

| Case | HF | CCSD | CCSD(T) |
|---|---|---|---|
| R = 1.1 Å, (10e,8o) | 80.8 mHa | 1.62 | **0.70** |
| R = 1.1 Å, (10e,10o) | 94.4 | 1.98 | **0.73** |
| R = 1.1 Å, (10e,12o) | 122.9 | 2.51 | **0.81** |
| **R = 2.0 Å, (10e,10o)** | 445 | **−35.6** | **−77.3** (CCSD converged; below FCI, i.e. non-variational failure) |

Source: [scripts/chemistry/sqd_capped_study.py, JSON in same folder](https://pypi.org/project/pyscf/)

**Evidence on quantum advantage**
- Lee et al. (Chan group, Nat. Commun. 14, 1952, Apr 2023): they find "no evidence of exponential quantum advantage" across chemical space for ground-state energy estimation, while "quantum computers may still prove useful… through polynomial speedups". The key question they pose is whether features enabling efficient quantum state preparation also enable efficient classical heuristics — [PMC](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10082187/); [arXiv:2208.02199](https://arxiv.org/abs/2208.02199)

**Fault-tolerant resource estimates**
- **Reiher et al. (2017), FeMoco** — [arXiv:1605.03590](https://arxiv.org/abs/1605.03590)
  - The original estimate was about 10¹⁴–10¹⁵ T gates.
  - Per the von Burg summary below, the original was 1.5×10¹⁴ Toffoli-equivalent, later 6.0×10¹⁴ T on 142 qubits.
- **von Burg et al. (2021), double factorization** — [PRR 3, 033055, arXiv:2007.14460](https://arxiv.org/abs/2007.14460)
  - FeMoco (54 orbitals): 1.2×10¹⁰ Toffolis at Berry's rank, or 2.3×10¹⁰ at 1 mHa, on about 3,600 logical qubits.
  - Ru CO₂ → methanol catalyst (52–65 orbitals): about 10¹⁰ Toffolis on about 4,000 qubits.
  - At 10 µs per Toffoli, 10¹⁰ Toffolis is "28 hours or about a day".
- **Lee et al. (2021), THC** — [PRX Quantum 2, 030305, arXiv:2011.03494](https://arxiv.org/abs/2011.03494)
  - The paper reports the "least fault-tolerant resources" for FeMoco.
  - **Conflict between secondary sources** on the numbers: 2,142 logical qubits and 5.3×10⁹ Toffolis ([postquantum.com](https://postquantum.com/quantum-utility-map/quantum-chemistry-drug-discovery-catalysis/)) versus 2,196 and 6.7×10⁹ ([arXiv:2108.12371 via search](https://arxiv.org/pdf/2108.12371)). Accounting differences are likely.
- **Low et al. (2025), spectrum amplification** — [PRX 15, 041016, arXiv:2502.15882](https://arxiv.org/abs/2502.15882)
  - Reports a "factor of 4 to 195 speedup over the state of the art" for iron–sulfur complexes and a CO₂-fixation catalyst.
  - A 2026 benchmarking paper quotes Low et al. at 1,459 logical qubits and 9.99×10⁸ Toffolis for 76-orbital FeMoco (secondary) — [arXiv:2609.12146 via search](https://arxiv.org/pdf/2609.12146)
- **Goings et al. (2022), cytochrome P450** — [arXiv:2202.01244](https://arxiv.org/abs/2202.01244) (own PDF extraction)
  - The largest Cpd I active space needs about 4.6M physical qubits and 73 hours at 0.1% physical error, or about 500k physical qubits and 25 hours at 0.001%.
  - Classical DMRG+NEVPT2 and CCSD(T) convergence is used to define the advantage boundary.

**Critiques of sample-based methods and classical competition**
- Reinholdt et al. (QSCI), Gaberle & Jattana (SQD), and IBM's own statement that [4Fe-4S] SQD energies were worse than classical methods (Q1) — [arXiv:2501.07231](https://arxiv.org/abs/2501.07231); [arXiv:2605.02494](https://arxiv.org/abs/2605.02494); [arXiv:2405.05068](https://arxiv.org/html/2405.05068v3)

**The "Grand Challenge" perspective**
- Babbush et al. (Google; arXiv Nov 12, 2025; PRX Quantum Perspective, June 15, 2026) lay out a five-stage path for applications. They stress that two stages are under-resourced: finding concrete problem instances with likely advantage, and connecting them to real-world use cases. They also discuss what makes a convincing advantage demonstration — [arXiv:2511.09124](https://arxiv.org/abs/2511.09124); [Google Research](https://research.google/pubs/the-grand-challenge-of-quantum-applications/)

**[own test] What sample-based methods look like next to honest baselines** (N₂/cc-pVDZ (10e,10o), 20 qubits, 20,000 shots; uncapped runs used 1,000 and 10,000 shots)
- **Uncapped qiskit-addon-sqd** (`diagonalize_fermionic_hamiltonian`, 3 batches, 5 recovery iterations, spin-symmetrized):
  - Ideal UCJ samples (348 ZZ) gave subspaces of only 16–64 determinants and **27–31 mHa** error.
  - With white noise at the Forte-estimated fidelity F = 0.16, **and even with pure-noise samples (F = 0)**, the α×β product space plus configuration recovery filled 98–100% of the 63,504-dimensional FCI space and returned the **exact** FCI energy.
  - The same happened at 16 qubits ((10e,8o), dim 3,136) with 1,000 shots.
  - Source: [scripts/chemistry/sqd_noise_study.py, sqd_N2_R1.1.json](https://pypi.org/project/qiskit-addon-sqd/)
- **Capped subspace (equal determinant budget), equilibrium R = 1.1 Å**

  | Budget (strings per spin) | Ideal UCJ samples | White-noise UCJ (F = 0.16) | Classical excitation-level heuristic | Oracle (exact FCI ranking) | Uniform random |
  |---|---|---|---|---|---|
  | 20 / 40 / 80 | 27.7 (only 7 distinct strings in 20k shots, dim 49) | 30.1 / 30.0 / 22.4 | 18.6 / 5.2 / **3.1** | 8.2 / 1.7 / 0.26 | 65–852 |

  All values are errors in mHa.
- **Capped subspace, stretched R = 2.0 Å**

  | Budget | Ideal all-to-all UCJ | White noise (F = 0.19) | Ideal heavy-hex-pattern LUCJ | Classical heuristic | Oracle |
  |---|---|---|---|---|---|
  | 20 strings (dim 400) | 19.8 | 35.8 | 72.5 | 133.5 | 34.7 |
  | 40 strings | 17.7 (dim 529; saturates at 23 strings) | 34.8 | — | 46.4 | 9.2 |
  | 80 strings (dim 6,400) | — | 31.8 | — | **21.4** | 2.3 |

  All values are errors in mHa. Source: [scripts/chemistry/sqd_capped_study.py, sqd_capped_R*.json](https://pypi.org/project/ffsim/)
- At 24 qubits ((10e,12o), R = 1.1 Å), ideal UCJ (484 ZZ) gave 16 distinct strings and 38 mHa. The classical heuristic gave 11.5 mHa at dim 14,400 — [same script](https://pypi.org/project/ffsim/)

### Inferences
- **Never report "SQD reached FCI" at ≤24 qubits as a quantum result.** At these sizes the classical post-processing reconstructs the full space from any samples, including noise, which is exactly the Reinholdt critique. The quantum contribution only shows when the subspace budget is capped well below the FCI dimension and compared with classical selection at the same budget.
- **Where quantum samples beat a simple classical heuristic:** in my white-noise proxy this happened only for the strongly correlated geometry (2.0 Å) at small budgets, 400–1,600 determinants. All-to-all UCJ clearly beat heavy-hex-pattern LUCJ there (19.8 versus 72.5 mHa ideal).
- **Caveats on that comparison:**
  - A stronger classical baseline, such as CISD-amplitude ranking or heat-bath CI, would likely win.
  - White noise is pessimistic in some respects and optimistic in others relative to the Forte model.
  - Both points have to be disclosed.
- **CCSD amplitudes at stretched geometries** make poor UCJ parameters. CCSD converged, but its energy was 35.6 mHa below FCI, so orbital or parameter optimization (for example ffsim's `optimize=True`) is a natural improvement.

### Gaps
- I did not run the actual IonQ Forte noise model, which needs Qollab or IonQ cloud. All noisy numbers above use a white-noise proxy, F = 0.995^(#ZZ + #qubits).
- I did not run heat-bath CI or DMRG baselines.
- I did not verify the primary-paper FeMoco THC numbers.

---

## Q6. What a "measurable quantum step" can honestly be in 48 h: concrete designs with qubits, native-ZZ counts, expected accuracy and browser runtime

### Takeaway
The strongest IonQ-specific, non-tutorial design is an SQD study at a **fixed determinant budget**. It compares IonQ-native all-to-all UCJ samples against heavy-hex-pattern LUCJ, a classical selection heuristic, random sampling and an oracle, on a bond-breaking problem where CCSD(T) fails, with a single circuit per run.

The circuits that matter (20 qubits, about 250–350 ZZ) exceed the ~100-gate budget. So pair it with a within-budget tier: 8–12 qubits, 39–76 ZZ, F ≈ 0.65–0.79.

Two robust alternatives are Hubbard quench dynamics (on-site terms are native ZZ on all-to-all hardware) and a reality-check project that pairs a fault-tolerant resource estimate with a small hardware slice.

### Cited Findings
These are the numbers the designs rest on. All counts are on IonQ-native ZZ (Q1 table); fidelities use F = 0.995^(#ZZ) × 0.995^(#qubits).

| Fact | Source |
|---|---|
| (4e,4o) UCJ is 60 ZZ (all-to-all) / 39 (LUCJ); (6e,5o) is 76/54; (10e,6o) is 58/53; (10e,8o) is 206/149; (10e,10o) is 314–348/242–258 | [own test, small_counts.py](https://pypi.org/project/ffsim/) |
| VQE would need 17–878 QWC measurement circuits per energy at 8–24 qubits; SQD needs 1 | [own test](https://pypi.org/project/qiskit/) |
| Browser FCI: (8e,8o) in 4 s; (10e,10o) in 189 s. Browser ED: 20-qubit Hubbard in about 2 s, 24-qubit in about 30 s | [own test, Pyodide console](https://pyodide.org/en/stable/console.html) |
| Forte two-qubit fidelity 99.6%; simulator noise models up to 29 qubits; Braket on-demand cap of 2,000 gates per circuit | [IonQ Forte](https://www.ionq.com/quantum-systems/forte); [earlier note ionq_hardware_and_sdk.md](https://docs.ionq.com/features/simulation-with-noise-models) |
| IonQ debiasing needs ≥500 shots | [IonQ API v0.4 create job](https://docs.ionq.com/api-reference/v0.4/jobs/create-job) |
| SQD configuration recovery tolerates about 2% signal in N₂ numerics | [arXiv:2405.05068](https://arxiv.org/html/2405.05068v3) |
| Qollab already hosts an H₂ bond-length VQE, a cross-framework H₂ VQE and a methanol VQE example | [earlier note, theme_brief_and_qollab_platform.md](https://qollab.xyz/u/qollab/quantum-chemistry) |

### Inferences (the designs)

**Design A (recommended headline): "Does all-to-all buy better chemistry samples? SQD on a fixed budget, for N≡N bond breaking"**

*Problem.* N₂ dissociation is the chemistry behind nitrogen fixation, the FeMoco motivation in Reiher et al. Compute the energy at R = 1.1, 1.5 and 2.0 Å in N₂/cc-pVDZ.

*Tiers*

| Tier | Active space | Qubits | Gates | F | Role |
|---|---|---|---|---|---|
| Within budget, live | (6e,5o) or (10e,6o) | 10–12 | 58–76 ZZ (UCJ, 1 layer) | 0.65–0.70 | FCI dims 100–225 are trivially saturated, so report **shots-to-chemical-accuracy at a capped budget** and the **correct-(Nα,Nβ) post-selection rate** under the Forte noise model against ideal |
| Science tier | (10e,10o) | 20 | 314 ZZ all-to-all vs 258 ZZ heavy-hex-pattern LUCJ | ~0.19 / 0.25 | Run on the IonQ simulator with the forte-1 noise model |

*Metric.* Energy error versus subspace budget, d = 400 / 1,600 / 6,400 determinants, for five sources:
- noisy all-to-all UCJ samples
- LUCJ samples
- a classical excitation-level heuristic, ideally also CISD-amplitude ranking
- uniform random
- the oracle

*Expected results* (my white-noise proxy at 2.0 Å):
- All-to-all ideal: 19.8 mHa at d = 400.
- Noisy: about 35 mHa at d = 400–1,600.
- Heuristic: 133 mHa at d = 400 and 46 mHa at 1,600.
- LUCJ ideal: 72.5 mHa.
- So the quantum samples win at small budgets and lose at d = 6,400 (31.8 versus 21.4 mHa).
- At 1.1 Å the classical heuristic wins outright.
- Report this honestly. The "quantum step" is the measured crossover budget, not an advantage claim.

*Browser work*
- Load FCIDUMP plus precomputed CCSD t1/t2 and UCJ parameters as JSON (about 12 KB per geometry).
- Build the circuit with Qiskit from Givens rotations and `rzz`, or export QASM from ffsim offline.
- Make one IonQ job.
- Run vendored `recover_configurations` and `postselect_by_hamming_right_and_left`, then the numpy direct-CI solver on capped subspaces with d ≤ 6,400 (seconds).
- Show precomputed FCI, CCSD and CCSD(T) for comparison.

*Risks*
- 250–350 ZZ is well over the ~100-gate guidance.
- A 20-qubit Forte-noise simulation may be slow or fail near the limits, since the IonQ docs warn about that.
- Precompute a fallback result.

**Design B: "Cuprate-parameter Hubbard quench on all-to-all ions" (dynamics versus exact)**

*System*
- 1D Fermi-Hubbard chain, L = 8 at half filling: 16 qubits under JW with an up block and a down block.
- Parameters t ≈ 0.35 eV, U/t = 6–8, motivated by Q3.
- Quench from a Néel or charge-density-wave product state.

*Cost per Trotter step*
- Hopping: 7 bonds × 2 spins × 2 ZZ = 28.
- On-site U: 8 ZZ, each coupling qubit i to qubit i+8, which is free on Forte but needs SWAP networks on a line.
- Total **36 ZZ per step**. Two steps make 72 ZZ, with F ≈ 0.995^88 ≈ 0.64.

*Observables*
- Double occupancy, staggered magnetization and spin–charge separation.
- Mitigation: post-select on conserved N↑ and N↓ (free from Z-basis shots); readout debiasing.

*Baseline.* Exact time evolution in the browser on the (4,4) sector, dimension 4,900, via `scipy.sparse.linalg.expm_multiply`, well under 1 s by extension of the measured ED timing. The Trotter error is computed exactly too.

*Measurable step*
- The observable error versus Trotter steps under the Forte noise model, before and after post-selection.
- A SWAP-count comparison against an IBM heavy-hex transpile of the same circuit.

*Honesty.* Classically trivial at L = 8. The impact framing is "a validated pipeline whose cost grows linearly in L on all-to-all hardware".

**Design C: "Schwinger-model pair production with long-range ZZ" (lattice gauge theory)**

*System*
- N = 8–10 staggered sites with the gauge field eliminated.
- Cost per Trotter step: about 2(N−1) ZZ for hopping + N(N−1)/2 long-range ZZ. That is about 42 ZZ for N = 8 and about 63 for N = 10.
- One or two steps fit the budget.

*Comparisons.* The 4-qubit trapped-ion results of 2016 and 2025 (Martinez; Rosanowski SKQD).

*Option.* SKQD: sample time-evolved states at 2–4 times in one job and diagonalize in the sampled subspace. The exact baseline is a 2¹⁰ ED in milliseconds.

*Measurable step.* Particle-number density versus time against exact. The counts are my inference from the Hamiltonian structure.

**Design D: "Impact reality check: a real reaction, its fault-tolerant cost, and the slice we can run today"**

*Pick.* MEA–CO₂ capture (IonQ 2025), the Ru CO₂-hydrogenation catalyst (von Burg), the Ni Suzuki–Miyaura oxidative addition (IonQ/AstraZeneca), or a Li-ion electrolyte decomposition step (PsiQuantum/Mercedes).

*Offline.* PySCF on Linux/WSL/Colab: AVAS or CASSCF active spaces of increasing size, FCIDUMPs, CCSD(T) and FCI or DMRG references, and the Hamiltonian 1-norm λ.

*In the browser*
- Show λ and published fault-tolerant scalings: about 10⁹–10¹⁰ Toffolis and about 1.5–4k logical qubits for 54–76-orbital FeMoco-class problems, about 1 day at 10 µs per Toffoli.
- Next to that, a live within-budget (6e,5o) or (10e,6o) SQD/QSCI slice: 58–76 ZZ, F ≈ 0.65–0.70, one job, exact answer reachable.
- Report the slice error versus FCI and versus CCSD(T).

*Measurable step.* The slice's hardware or noisy-simulator error with and without post-selection and REM.
- REM needs a second, Hartree–Fock reference circuit.
- Under "one job per run", run that reference as a separate, precomputed noisy-simulator job.

**Design E (optional add-on): "VQE versus single-job QSCI measurement economics"**
- Compare, for the same (10e,6o) state, the number of IonQ jobs, circuits and shots needed for an energy to ±1.6 mHa.
- VQE: 92 QWC groups × optimizer iterations.
- QSCI: 1 circuit + classical diagonalization.
- Runs entirely on simulators. Useful as a slide, weak as a standalone project.

**Cross-cutting recommendations**
1. Every chart pairs the quantum result with FCI (exact), CCSD(T) (gold standard) and a classical heuristic at equal cost.
2. Flag every vendor number.
3. Precompute anything above about 5k determinants.
4. Keep the Run path under about 10 s: load JSON → one IonQ job (or cached counts) → recovery → SCI at d ≤ 6,400.
5. Expected accuracy at 0.5% two-qubit error:
   - Within-budget circuits (F ≈ 0.65–0.79) give recovered subspaces with chemical accuracy only because the spaces are tiny.
   - 20-qubit circuits (F ≈ 0.16–0.25) in my proxy give 20–35 mHa at d ≤ 6,400 for stretched N₂. That is not chemical accuracy, and it should be presented as a measured crossover, not a success.

### Gaps
- I did not run any design on the real Forte noise model or on QPU hardware. IonQ simulator runtimes at 16–24 qubits with 100–350 ZZ are unknown.
- Trotter and Schwinger gate counts are analytic from the measured building blocks; I did not transpile them.
- I did not run a stronger classical selection baseline (CISD-ranked or heat-bath CI) for Design A.
- Whether the Qollab Run button can reuse cached IonQ results, instead of resubmitting, is unverified here.
