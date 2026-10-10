# Technical Playbook: Building a Winning IonQ Trapped-Ion Hackathon Project (24–48 h, as of Oct 2026)

Research date: 2026-10-07. Sources are tagged by date. "[Quantinuum]" marks trapped-ion evidence that is NOT from IonQ hardware. Vendor press releases are flagged as vendor claims.

> **Critical context for the Qollab x IonQ event (SESSION 2026.10.09).** A secondary summary of the official page says code runs on an **IonQ simulator, not a QPU**, and that compute prizes are **IonQ hardware time** spent later through the platform. The official Qollab page I fetched does not mention simulator or QPU access at all. Verify this with the organizers. If it holds, "how well it runs" will be judged on the simulator, ideally with IonQ's noise models. Debiasing, IonQ's main mitigation, is **not available** in IonQ simulation, so any mitigation shown must run client-side. — [Quantum Zeitgeist, Sep 2026](https://quantumzeitgeist.com/ionq-quantum-hackathon-qollab-host/); [Qollab hackathon page](https://qollab.xyz/programs/hackathon); [IonQ noise-model docs](https://docs.ionq.com/guides/simulation-with-noise-models)

---

## Key Question 1: Which project archetypes most reliably produce a working, impressive result on ~10–36 trapped-ion qubits within hours?

### Takeaway
The archetype with the strongest hardware evidence for 2024–2026 is **peaked-output combinatorial optimization**: QAOA variants (multi-angle, linear-ramp, or iterative/warm-started) on a dense QUBO built from a real dataset. On IonQ Aria and Forte these runs returned optimal or near-optimal bitstrings at 12–36 qubits. They work because the optimum only has to *appear in the samples*; accurate expectation values are not needed. Good second tier, for different reasons: small quantum kernels and re-uploading classifiers (4–8 qubits) and short Trotterized dynamics with symmetry post-selection, which are cheap and robust; GHZ, entanglement, or [[4,2,2]] error-detection demos, which are easy and fit "teach a hard topic"; and hybrid generative models, which are impressive but heavy to build. VQE on real chemistry is the most shot- and time-expensive, so it is risky in 48 h.

### Cited Findings

**Optimization / QAOA (IonQ hardware, strongest evidence)**
- **Airbus aircraft loading (arXiv, Apr 2025):** a multi-angle QAOA variant that "utilize[s] a smaller number of two qubit gates" than standard QAOA, plus a cost function that handles inequality constraints *without slack qubits*. It ran on IonQ Aria and Forte, and the authors report it found "the optimal solutions for all the problem instances studied ranging from 12 qubits to 28 qubits." In the 12-qubit case (4 containers, 3 slots) the optimum's final probability was about 70%, with 1000 shots, COBYLA, and at most 100 iterations. No classical speed comparison was given. — [arXiv:2504.01567](https://arxiv.org/abs/2504.01567)
- **Iterative-QAOA for job-shop scheduling (IonQ + Clemson, arXiv Oct 2025):** non-variational, fixed-parameter shallow circuits with iterative warm-starting. On hardware it "sample[d] the optimal solution for the 32 qubits and 33 qubits problem instances and the first excited state in the 36 qubit problem instance." These are vendor-authored results. — [arXiv:2510.26859](https://arxiv.org/abs/2510.26859)
- **Shipment selection (arXiv, Apr 2026):** Iterative-QAOA on Forte at 20–35 qubits, using "only IonQ's default debiasing setting, with no further error mitigation." The main results come from noiseless simulation. — [arXiv:2604.11758](https://arxiv.org/abs/2604.11758)
- **Feature selection with higher-order binary optimization (arXiv, Apr 2026):** 32-qubit circuits (one qubit per feature) with ~1,000 two-qubit gates and 2,000 shots per circuit on IonQ hardware. "Results after 1 iteration [are] already competitive with the classical benchmarks." The excerpt does not label this QAOA. — [arXiv:2604.26834](https://arxiv.org/abs/2604.26834)
- **Network routing under link failures (arXiv, Feb 2026):** the team cut QAOA layers from 20 to 8 on Forte "to improve the fidelity," and ran only 3 cases because of cost. The best valid solution appeared 2, 5, and 16 times, while most other bitstrings appeared once. This is an honest example of weak-but-present signal. — [arXiv:2602.04495](https://arxiv.org/abs/2602.04495)
- **Linear-ramp QAOA (Montanez-Barrera & Michielsen, npj QI 2025):** fixed linear-ramp schedule (no variational loop), tested on IonQ Aria, Quantinuum H2-1 and IBM, with up to 109 qubits and p=100 (circuits up to 21,200 CNOTs across platforms). The per-device signal-loss threshold was not in the abstract. — [arXiv:2405.09169](https://arxiv.org/abs/2405.09169)
- **IonQ + ORNL power-grid unit commitment (Jul 2025, vendor PR):** hybrid method on 36-qubit Forte Enterprise for 26 generators over 24 time periods. It is compared against other quantum algorithms, not classical ones, and no advantage is claimed. — [IonQ news](https://ionq.com/news/ionq-partners-with-oak-ridge-national-laboratory-demonstrating-quantum-power)

**IonQ application showcases (useful as "industry framing" slides; all vendor claims)**
- **AstraZeneca + AWS + NVIDIA (Jun 2025):** end-to-end Suzuki–Miyaura reaction step using IonQ Forte, NVIDIA CUDA-Q, AWS Braket and ParallelCluster with H200 GPUs. The partners claim a ">20x" time-to-solution speedup over prior benchmarks. The baseline is unspecified and there is no independent validation. — [IonQ news](https://ionq.com/news/ionq-speeds-quantum-accelerated-drug-development-application-with)
- **Ansys LS-DYNA blood pump (Mar 2025):** "up to 12%" faster than classical. Meshes up to 2.6M vertices and 40M edges. The Quantum Insider reports the 12% figure came from *simulating* the hybrid algorithm, with Forte used only to validate small instances. — [IonQ news](https://www.ionq.com/news/ionq-and-ansys-achieve-major-quantum-computing-milestone-demonstrating); [The Quantum Insider](https://thequantuminsider.com/?p=2376655)
- **Hyundai road-sign classification:** the press release says IonQ was classifying 43 road-sign types (Apr 2022). The APS March 2023 abstract describes a hybrid QCNN trained end-to-end on up to 8 qubits, with inference on a 16-qubit processor for up to 10 classes. No accuracy figure is published. — [Hyundai news](https://www.hyundai.com/au/en/news/mobility/IonQ-and-Hyundai-Motor-Expand-Partnership-to-Use-Quantum-Computing-for-Object-Detection); [APS 2023 abstract](https://meetings-archive.aps.org/mar/2023/m64/3)
- **Quantum-enhanced AI (May 2025, vendor PR):** a PQC layer added to an open-source LLM for sentiment classification beat similar-size classical models by a "meaningful margin," with no figures released. A hybrid QGAN for steel microstructure images scored higher in "up to 70%" of cases. — [IonQ IR](https://investors.ionq.com/news/news-details/2025/IonQ-Demonstrates-Quantum-Enhanced-Applications-Advancing-AI/default.aspx). The QGAN paper puts a quantum circuit at the input of a classical Wasserstein GAN and reports beating classical Bernoulli GANs on 70% of samples by MMD. — [arXiv:2504.08728, Apr 2025](https://arxiv.org/abs/2504.08728)

**Hamiltonian simulation**
- **Neutrinoless double-beta decay on IonQ Forte Enterprise (arXiv Jun 2025; Nat. Commun. 2026):** 32 qubits for the physics plus 4 flag qubits for "flag-based error mitigation" (36 total), with benchmarking circuits up to 2,356 two-qubit gates. Lepton-number violation was observed in real time. Co-authors include IonQ staff. — [arXiv:2506.05757](https://arxiv.org/abs/2506.05757)
- **IonQ guidance for Trotter circuits:** use the same number of Trotter steps for every sample time, rather than a fixed step size, so "experimental error [is] easier to correct." Prefer bases with many Z rotations, which are virtual, e.g. write a TFIM as XX coupling with Z fields rather than ZZ coupling with an X field. — [IonQ best practices](https://ionq.com/best-practices)

**QML**
- **Quantum kernel (QSVC on Fashion-MNIST), IonQ Harmony vs Aria (2024, Springer QMI supplement):** kernel alignment rose from 0.993 on Harmony to 0.998 on Aria, with 2Q error 2.7% vs 0.4%. — [Springer supplement](https://media.springernature.com/original/springer-static/esm/art%3A10.1007%2Fs42484-024-00165-0/MediaObjects/42484_2024_165_MOESM1_ESM.pdf)
- **QSVC/QSVR on IonQ Harmony (2023/2024):** 4-qubit classification on hardware was comparable to noiseless simulation. — [arXiv:2307.02091](https://arxiv.org/abs/2307.02091)
- **Data re-uploading:** a single qubit with repeated data re-uploading is a universal classifier, which makes for very shallow hardware circuits. — [Pérez-Salinas et al., Quantum 2020](https://arxiv.org/abs/1907.02085). A 2025 trapped-ion re-uploading classifier for adversarial defense exists, but the vendor is unverified. — [arXiv:2503.02436](https://arxiv.org/abs/2503.02436)
- **QCBM on IonQ (pre-window, 2020):** to raise state fidelity, the authors *reduced* all-to-all XX connectivity to a linear chain of entanglers. Even with all-to-all hardware, fewer 2Q gates beat more connectivity. — [arXiv:2012.03924](https://arxiv.org/abs/2012.03924)

**Entanglement / GHZ / error detection**
- **GHZ on IonQ Aria-1 (third-party, Jan 2026):** fidelity ≈0.96 at 6 qubits and ≈0.84 at 10 qubits, the strongest of the devices tested. IQM Garnet and Rigetti Ankaa-3 fell to ≈0.12 and ≈0.09 at 10 qubits. The estimation method was not visible in the snippet. — [arXiv:2601.05286](https://arxiv.org/abs/2601.05286)
- **[Quantinuum, 2022]** 20-qubit GHZ fidelity lower bound of 0.73 on H1. — [arXiv:2210.03048](https://arxiv.org/abs/2210.03048)
- **[[4,2,2]] on IonQ (arXiv Dec 2024):** the encoding helped on 11-qubit Harmony. On 21-qubit Aria (lower gate error) there was "no conclusive improvement," possibly from correlated errors the assumed error model misses. — [arXiv:2412.20736](https://arxiv.org/abs/2412.20736). The original trapped-ion [[4,2,2]] fault-tolerant error detection (2016, academic trap) found the logical qubit more robust than the bare qubit. — [arXiv:1611.06946](https://arxiv.org/abs/1611.06946)
- **[Quantinuum, 2024]** 3-qubit logical QFT in the Steane [[7,1,3]] code on H2-1, including transversal logical CNOT and logical T via magic states. That was the largest QFT that fit the device. — [arXiv:2404.08616](https://arxiv.org/abs/2404.08616)
- **[Quantinuum, 2023]** Bayesian QPE with an error-detection code on H1 for a chemistry calculation, discarding runs when errors were detected. — [Quantinuum news](https://www.quantinuum.com/news/quantum-chemistry-progresses-meaningfully-towards-a-fault-tolerant-regime-using-logical-qubits)
- **[Quantinuum, 2025]** [[4,2,2]]-based error detection *without* post-selection in adaptive circuits. — [arXiv:2509.25326](https://arxiv.org/abs/2509.25326)

**VQE (small molecules)**
- **Qedma QESEM on IonQ Aria (arXiv Aug 2025):** NaH VQE used 6 qubits and 94 MS gates (using all-to-all connectivity). O2 used 12 qubits and 99 MS gates, with dedicated access through Braket Direct. — [arXiv:2508.10997](https://arxiv.org/abs/2508.10997); [AWS blog](https://aws.amazon.com/blogs/quantum-computing/enabling-state-of-the-art-quantum-algorithms-with-qedmas-error-mitigation-and-ionq-using-braket-direct)
- **Relativistic VQE for molecular dipole moments on IonQ Aria (2024):** debiasing followed by post-selection. — [arXiv:2406.04992](https://arxiv.org/abs/2406.04992)

### Inferences
- **Archetype ranking for a 48-h build (most to least reliable):**
  1. *QUBO/HUBO optimization from a real public dataset, solved with a fixed-schedule QAOA* (linear-ramp or iterative warm-start), so there is no long variational loop. Benchmark it against brute force, simulated annealing, or Gurobi. Report P(optimum) and approximation ratio vs qubits. This fits Qollab's "Quantum Impact" theme, which asks for a strong classical baseline plus a measurable quantum subroutine.
  2. *Shallow QML* (4–8-qubit fidelity kernel or 1–2-qubit re-uploading classifier) with an honest classical SVM/MLP baseline.
  3. *Short Trotter dynamics* (TFIM/Heisenberg, 6–16 qubits) with a conserved quantity used for post-selection, compared to exact diagonalization.
  4. *Teaching demos* (GHZ scaling curve, [[4,2,2]] detect-and-discard, teleportation/entanglement swapping), which fit "Quantum Unlocked."
  5. *Hybrid generative* (QCBM prior or QGAN latent), which is impressive but costly to train.
  6. *VQE for molecules*, which is costly and easy to get wrong in 48 h.
- All-to-all connectivity "looks impressive" most clearly on **dense graphs and higher-order terms**. On a nearest-neighbor device those would need SWAP networks, so show the 2Q-gate count compiled for IonQ vs. for a heavy-hex/linear topology as a slide.
- The vendor demos (AstraZeneca, Ansys, ORNL, Airbus) all use a **hybrid "quantum as accelerator subroutine"** framing. Mirroring that framing matches what IonQ itself promotes. Avoid quoting their headline speedups as validated advantage.

### Gaps
- No 2023–2026 IonQ hardware papers were found for quantum walks, random-circuit sampling, QCNN (beyond the Hyundai abstract), or amplitude estimation / quantum Monte Carlo for finance. Searches did not cover these specifically.
- The EPB partnership was not researched.
- Accuracy numbers for the Hyundai work and the May 2025 LLM fine-tuning are unpublished in the sources I found.
- The Ansys and AstraZeneca speedup baselines are not independently verified.

---

## Key Question 2: What are concrete fidelity/depth limits on IonQ Aria/Forte (how many 2-qubit gates before signal is lost)?

### Takeaway
Two-qubit error is the dominant cost. Vendor figures are ~0.4% (Forte) and ~0.6% (Aria), while measured or independent figures run 0.7–0.9% on Forte-class systems. A naive (1−e₂q)^N model therefore puts the 1/e point at **~100–250 two-qubit gates** on Forte-class hardware and **~75–165** on Aria. Output types where only the answer must *appear* in the samples (peaked optimization, flag/symmetry post-selected observables) have survived **~1,000–2,400 two-qubit gates** at 32–36 qubits. Budget roughly 50–150 2Q gates for expectation-value tasks and up to several hundred for peaked-output tasks, and always verify on the forte-1 noise model first.

### Cited Findings
- **IonQ vendor specs (comparison page):** Aria has #AQ 25, 99.4% 2Q fidelity and 99.94% 1Q fidelity. Forte has #AQ 36, 99.6% 2Q and 99.98% 1Q. The Forte product page shows #AQ 35 in one block, so the vendor figures are internally inconsistent. — [IonQ compare](https://www.ionq.com/quantum-systems/compare); [IonQ Forte](https://ionq.com/quantum-systems/forte)
- **Forte Enterprise targets:** 1Q error ~0.02%, 2Q error ~0.4%, SPAM ~0.5%, T1/T2 "10–100 s, ~1 s." — [IonQ Forte Enterprise](https://ionq.com/quantum-systems/forte-enterprise)
- **Measured Forte Enterprise 1 at job submission (third-party, arXiv Mar 2026):** 2Q fidelity 0.9915, 1Q 0.9998, SPAM fidelity 0.9939, T2 0.95 s. 2Q gate duration 650 µs, 1Q 63 µs. — [arXiv:2603.03801](https://arxiv.org/abs/2603.03801)
- **Forte benchmarking paper (Quantum, Nov 2024):** direct randomized benchmarking across all 435 pairs of a 30-ion chain. Per the search excerpt, median 2Q fidelity was ~99.3% and 2Q gate time ~950 µs. Another Forte paper notes a 36-ion chain where "only 30 … serve as the computational qubits." — [Quantum q-2024-11-07-1516](https://quantum-journal.org/papers/q-2024-11-07-1516/)
- **Third-party aggregator:** Aria 99.4%, Forte 99.6% 2Q. A separate write-up gives a Forte range of 99.35–99.6% "depending on benchmarking methodology." — [Open Quantum](https://www.openquantum.com/providers/ionq); [Jared Watkins write-up](https://www.jaredwatkins.com/research/quantum-computing/ionq/)
- **Azure lists Aria-1 2Q at 99.6% "(not SPAM corrected)".** This differs from IonQ's 99.4% for Aria. — [Azure IonQ provider](https://learn.microsoft.com/azure/quantum/provider-ionq)
- **IonQ simulator noise-model parameters (aggregated depolarizing; "shouldn't be compared directly to experimental error rates"):** Aria-1 r1q=0.0005, r2q=0.0133. Aria-2 r1q≈0.000657, r2q≈0.01856. Forte-1 r1q≈0.000267, r2q≈0.004949. A forte-enterprise-1 model was added Sep 2025. Aria models are now "retired QPUs." — [IonQ noise-model docs](https://docs.ionq.com/guides/simulation-with-noise-models)
- **Simulator limits:** the ideal and Forte-class noise models handle up to 29 qubits, and Aria-class models up to 25. Simulation runs one trajectory per shot, so runtime grows with shots. Noise simulation is free for direct IonQ users. IonQ advises against using the models to predict whether a specific system can run a circuit. — [IonQ noise-model docs](https://docs.ionq.com/guides/simulation-with-noise-models)
- **#AQ definition:** #AQ = N means structured algorithmic circuits of width ≤ N and roughly N² CX gates pass with success − statistical error > 1/e ≈ 0.37. — [IonQ AQ resource](https://ionq.com/resources/algorithmic-qubits-a-better-single-number-metric); [Quantum Benchmark Zoo](https://quantumbenchmarkzoo.org/content/application-level-benchmark/algorithmic-qubit). **[Quantinuum critique]** Quantinuum argues AQ is "very susceptible to tricks" such as compilation and plurality voting. That is a competitor's view. — [Quantinuum blog](https://www.quantinuum.com/blog/debunking-algorithmic-qubits)
- **Hardware data points where signal survived:** ~1,000 2Q gates at 32 qubits, competitive with classical after one iteration ([arXiv:2604.26834](https://arxiv.org/abs/2604.26834)). Up to 2,356 2Q gates in 36-qubit benchmarking circuits with flag-based mitigation ([arXiv:2506.05757](https://arxiv.org/abs/2506.05757)). 94–99 MS gates for VQE at 6–12 qubits with QESEM ([arXiv:2508.10997](https://arxiv.org/abs/2508.10997)). GHZ fidelity ≈0.84 at 10 qubits on Aria-1 ([arXiv:2601.05286](https://arxiv.org/abs/2601.05286)).
- **Data points where signal degraded:** Iterative-QAOA reached only the first excited state at 36 qubits vs the optimum at 32–33 ([arXiv:2510.26859](https://arxiv.org/abs/2510.26859)). In a routing QAOA on Forte, depth had to be cut from 20 to 8 layers, and the best solution was barely above the noise floor ([arXiv:2602.04495](https://arxiv.org/abs/2602.04495)).
- **Small-angle MS gates are higher fidelity.** On a decommissioned system, 2Q fidelity improved from ~97.5% at π/2 to ~99.6% at π/100. Partially entangling MS is available on Aria, and Forte exposes a native ZZ(θ). — [IonQ native gates](https://docs.ionq.com/guides/getting-started-with-native-gates)
- **Access route matters:** a QFT benchmark on Aria-1 was limited to 16 qubits on AWS Braket vs 25 on Azure, because Braket's gate set produced larger circuits. — [arXiv:2601.09943](https://arxiv.org/abs/2601.09943)
- **Roadmap / prototype numbers (not available to users):** 99.99% 2Q fidelity with Electronic Qubit Control was shown on prototype hardware in Oct 2025. — [HPCwire](https://www.hpcwire.com/off-the-wire/ionq-demonstrates-99-99-two-qubit-gate-fidelity-using-electronic-qubit-control-tech/). An IonQ page reports Tempo #AQ 64. — [IonQ benchmarking page](https://ionq.co/algorithmic-qubits)

### Inferences
- **Rule-of-thumb gate budget** (my calculation, simple multiplicative model F ≈ (1−e)^N, ignoring 1Q/SPAM):
  - Forte-1 noise model (e=0.00495): F=0.5 at N≈140 and F=1/e at N≈200.
  - Measured Forte Ent. (e=0.0085): F=0.5 at N≈80 and 1/e at N≈117.
  - Vendor Forte (e=0.004): 1/e at N≈250.
  - Aria-1 model (e=0.0133): 1/e at N≈75.
  - So **target ≤100 two-qubit gates for expectation-value or distribution-fidelity tasks.** Peaked-output tasks can go further because the correct bitstring only needs to beat the uniform background (2⁻ⁿ).
- **Wall-clock:** at 650–950 µs per 2Q gate, a 200-2Q-gate circuit spends ~0.13–0.19 s in 2Q gates per shot. That means minutes per 1,000-shot job before queueing. Variational loops with hundreds of iterations are infeasible on QPU in a 48-h window, so do the optimization in simulation and run only final or fixed-schedule circuits on hardware.
- **Practical qubit ceiling for prototyping is 29** (the simulator limit), even though Forte has 36. Plan the scaling study at 4–28 qubits.
- The #AQ figure (~N² gates passing at N=36, i.e. ~1,300 CX) is much more optimistic than the per-gate model. Don't use #AQ to size circuits for expectation-value tasks.

### Gaps
- No official IonQ page gives a "max useful depth" recommendation. IonQ's best-practices page explicitly gives no gate-count limits.
- No live per-qubit calibration numbers for Forte/Forte Enterprise were found publicly. They are in the IonQ Cloud Console/API per the docs.
- The Forte 1 vs Forte Enterprise noise-model parameters for forte-enterprise-1 are not published.
- No IonQ-authored GHZ scaling result was found for 2024–2026.

---

## Key Question 3: Which error-mitigation and circuit-engineering techniques give the biggest gain per effort on IonQ (and with which tooling)?

### Takeaway
In rough order of gain per hour of work:
1. **Cut 2Q gate count**, using all-to-all connectivity, no SWAPs, fixed-schedule ansätze, and partially entangling or native ZZ gates where you control compilation.
2. **Debiasing** on hardware: free and on by default at ≥500 shots. Use *sharpening* for peaked outputs and *averaging* otherwise.
3. **Symmetry or constraint post-selection**: discard forbidden bitstrings and renormalize. Cheap, and IonQ recommends it.
4. **ZNE via identity insertion or unitary folding** (Mitiq/PennyLane): modest gains, and the triple-shot cost needs controls.
5. **Unbiased quasi-probabilistic methods** (Qedma QESEM): strong but requires a commercial tool and dedicated access.

On the simulator, only #1, #3 and #4 apply, since debiasing is not simulated.

### Cited Findings

**Native gates & compilation**
- **Native gates:** GPi(φ) and GPi2(φ), with angles in *turns* (1 turn = 2π). Z rotations are *virtual* (absorbed into later phases). MS(φ₀,φ₁[,θ]) on Aria, where θ ∈ [0, 0.25] turns is partially entangling with ~3-decimal precision. ZZ(θ) on Forte only. One arbitrary-angle MS "can require up to two fully entangling MS gates plus four single-qubit rotations" if decomposed, so native partial gates reduce depth. — [IonQ native gates](https://docs.ionq.com/guides/getting-started-with-native-gates)
- **Native-gate submissions:** the compiler, optimizer and error mitigation are *off*, debiasing can be re-enabled, and native and abstract gates cannot be mixed. IonQ advises against native gates for general algorithm runs: "Abstract gates usually give better results because the compiler and optimizer are used." — [IonQ native gates](https://docs.ionq.com/guides/getting-started-with-native-gates)
- **CNOT → XX:** RY(π/2) on the control, then XX(π/4), then RX(−π/2) and RY(−π/2) on the control and RX(−π/2) on the target. Use KAK (Qiskit `TwoQubitBasisDecomposer`, Cirq `kak_decomposition`) for general 2Q unitaries. — [IonQ native gates](https://docs.ionq.com/guides/getting-started-with-native-gates)
- **IonQ best practices:**
  - Logical-to-physical mapping is chosen at runtime.
  - Replace CX(a,b)·CX(b,a) with a CX plus a SWAP that can be commuted away.
  - Arbitrary-angle XX/YY/ZZ (abstract gates) cost two fixed-angle MS gates plus 1Q rotations.
  - Maximize virtual RZ.
  - RX/RY angles finer than ~10⁻³·π give no benefit.
  - Tailor shots to the output distribution, since too many waste money and too few look like noise.
  - Post-select on theory-forbidden outcomes and renormalize ("a cheap way to improve fidelity").
  - [IonQ best practices](https://ionq.com/best-practices)
- **Conflict to note:** the best-practices page says arbitrary-angle XX/YY/ZZ run as two fixed-angle MS gates. The native-gate guide says partially entangling MS is directly available on Aria with higher fidelity at small angles. The best-practices page likely describes the abstract-gate path or an older system, but this is not reconciled in the sources. — [IonQ best practices](https://ionq.com/best-practices); [IonQ native gates](https://docs.ionq.com/guides/getting-started-with-native-gates)

**Debiasing (IonQ-specific symmetrization)**
- **Mechanism:** many symmetric circuit variants (qubit assignment, gate decomposition, pulse sequence) are run and aggregated, so systematic errors cancel. Debiasing requires ≥500 shots, split into 25 executions. It is default-on for QIS-gate jobs ≥500 shots, off for native-gate jobs (can be enabled), and available on all IonQ QPUs but **not on the simulator, including noise models**. It adds no circuits, shots, qubits or gates, but adds classical overhead that raises the minimum cost for small jobs. IonQ recommends turning it off for shallow circuits and small tests to save credits. — [IonQ debiasing docs](https://docs.ionq.com/guides/error-mitigation-debiasing)
- **Aggregation:** averaging (default) merges histograms and suits distributions where relative probabilities matter. Sharpening (plurality vote per execution) suits "one or a few expected high-probability states" and can distort complex distributions. Sharpening is a *retrieval* option on a debiased job, so you can fetch both versions from one job and compare. — [IonQ debiasing docs](https://docs.ionq.com/guides/error-mitigation-debiasing)
- **API and SDK switches:** Qiskit `ErrorMitigation.DEBIASING` / `NO_DEBIASING`; v0.4 API `settings.error_mitigation.debiasing`. — [IonQ debiasing docs](https://docs.ionq.com/guides/error-mitigation-debiasing); [IonQ Qiskit error-mitigation docs](https://docs.ionq.com/sdks/qiskit/error-mitigation-qiskit)
- **Paper claim:** improves "multiple practical algorithms by 100x with no qubit or gate overhead" on a commercial trapped-ion computer (Maksymov, Nguyen, Nam, Markov; IonQ; Jan 2023). This is the vendor's own paper, and the benchmark method was not checked. — [arXiv:2301.07233](https://arxiv.org/abs/2301.07233)
- **Braket requires a minimum of 2,500 shots** for error-mitigation tasks on on-demand access, a higher floor than IonQ direct. Azure notes debiasing is default on Forte and priced accordingly. — [AWS Braket docs](https://docs.aws.amazon.com/braket/latest/developerguide/error-mitigation-aria.html); [Azure IonQ provider](https://learn.microsoft.com/azure/quantum/provider-ionq)
- **Typical practice in 2025–26 papers:** Iterative-QAOA on Forte used "only IonQ's default debiasing … no further error mitigation" ([arXiv:2604.11758](https://arxiv.org/abs/2604.11758)). Relativistic VQE on Aria used debiasing plus post-selection ([arXiv:2406.04992](https://arxiv.org/abs/2406.04992)).

**ZNE / folding**
- **AWS blog:** ZNE on IonQ by inserting identity layers at three noise levels improved VQE accuracy by "up to 12%" vs unmitigated. — [AWS blog](https://aws.amazon.com/blogs/quantum-computing/amazon-braket-now-supports-verbatim-compilation-and-native-gates-with-ionq)
- **Mitiq** has a step-by-step ZNE tutorial for IonQ via Braket. A real-device run needs AWS credits. — [Mitiq IonQ tutorial](https://mitiq.readthedocs.io/en/stable/examples/zne-braket-ionq.html). Unitary folding G→G G† G, local vs global, and fold order affect results. — [Mitiq scaling docs](https://mitiq.readthedocs.io/en/stable/examples/scaling.html). PennyLane offers a native `mitigate_with_zne` transform. — [PennyLane docs](https://docs.pennylane.ai/en/stable/code/api/pennylane.transforms.mitigate_with_zne.html)
- **[Trapped ion, Sandia QSCOUT, not IonQ, 2023]:** stretching 2Q gate duration did *not* scale noise enough for ZNE. Inserting identity 2Q gates (unitary folding) worked, with 96.8% error suppression on a HeH+ VQE. — [arXiv:2307.07027](https://arxiv.org/abs/2307.07027); [APS 2024 abstract](https://meetings-archive.aps.org/mar/2024/k51/5)
- **Cross-platform (IBM/IonQ/Rigetti, IEEE TQE 2023):** ZNE/PEC were "on average more beneficial than no error mitigation, even when normalized by the additional resources," but the gain was device-dependent. — [arXiv:2210.07194](https://arxiv.org/abs/2210.07194)
- **Caution [superconducting IQM, not trapped ion, 2026]:** a deliberately flawed folding control produced a *larger* apparent ZNE "improvement" than real folding, with overshoots beyond the ideal value. Always include controls. — [arXiv:2607.09360](https://arxiv.org/abs/2607.09360)

**Unbiased PEC-style mitigation**
- **Qedma QESEM** ran on IonQ Aria (VQE for NaH and O2). It "consistently beats several variants of zero-noise extrapolation." The authors claim it is the first large-scale unbiased mitigation on trapped ions. It needs device characterization plus dedicated access. — [arXiv:2508.10997](https://arxiv.org/abs/2508.10997)

**Error detection as mitigation**
- **Flag qubits:** 4 extra flag qubits for "flag-based error mitigation" on Forte Enterprise. — [arXiv:2506.05757](https://arxiv.org/abs/2506.05757)
- **[[4,2,2]] post-selection:** helped on Harmony, inconclusive on Aria. — [arXiv:2412.20736](https://arxiv.org/abs/2412.20736)

**Tooling**
- **Qiskit:** `qiskit-ionq` provides `IonQProvider` (env var `IONQ_API_TOKEN`). The simulator `noise_model` option accepts aria-1, aria-2 and forte-1, e.g. `backend.run(qc, shots=1000, noise_model="forte-1")` with `sampler_seed` for reproducibility. — [IonQ Qiskit docs](https://docs.ionq.com/sdks/qiskit); [IonQ noise-model docs](https://docs.ionq.com/guides/simulation-with-noise-models)
- **PennyLane:** `pennylane-ionq` exposes `ionq.simulator` and `ionq.qpu` (backend e.g. "aria-1") with custom XX/YY/ZZ gates. Env var: `IONQ_API_KEY`. — [PennyLane-IonQ devices](https://docs.pennylane.ai/projects/ionq/en/latest/devices.html)
- **CUDA-Q:** `cudaq.set_target('ionq')`, with `qpu=…`, `noise` (aria-1/aria-2 legacy, forte-1, forte-enterprise-1), and `emulate=True` for local runs. Default 1,000 shots. — [CUDA-Q ion-trap backend docs](https://nvidia.github.io/cuda-quantum/0.12.0/using/backends/hardware/iontrap.html). CUDA-Q was the orchestration layer in the IonQ/AstraZeneca/AWS/NVIDIA demo. — [IonQ news](https://ionq.com/news/ionq-speeds-quantum-accelerated-drug-development-application-with)

### Inferences
- **Highest ROI for a simulator-based hackathon:**
  1. Design low-2Q-count circuits and *report the 2Q count* prominently.
  2. Use **constraint/symmetry post-selection**. QUBO feasibility, Hamming weight and parity are cheap, and IonQ recommends it.
  3. Show **ideal vs forte-1 noisy vs noisy + post-selection (+ ZNE)** side by side, with a folding control as in arXiv:2607.09360 so the ZNE gain is credible.
  4. If you get real QPU time, keep debiasing on (≥500 shots) and present *both* averaged and sharpened results from the same job.
- **Shot budgeting (inference):** standard error of a probability p from S shots is √(p(1−p)/S). With 1,000 shots, ±1.6% at p=0.5. Parameter-shift needs 2 circuit evaluations per parameter per gradient step, so a 20-parameter ansatz costs 40 jobs per step. Train in simulation; reserve QPU shots for final evaluation at 500–2,000 shots, consistent with the hardware papers above (1,000–2,000 shots).
- **Native-gate hand-compilation is usually not worth it in 48 h:** IonQ itself says the optimizer does better. The exception is when the project's *point* is gate-level (e.g., showing partial-MS/ZZ depth savings).

### Gaps
- No source quantifying **readout-error mitigation** (confusion-matrix inversion) gains specifically on IonQ was found. SPAM is ~0.5–0.6% per the specs above, so its relative value is modest.
- No IonQ-specific **classical shadows** experiments were found in this search.
- No independent replication of the 100x debiasing claim was found.
- No IonQ-specific data was found on parameter-shift shot budgets (the inference above is generic statistics).

---

## Key Question 4: What do hackathon judges (especially industry quantum judges) look for, and how should a 24–48-h project be scoped and presented?

### Takeaway
Across the quantum hackathons surveyed (Qollab x IonQ 2026, iQuHACK Microsoft/IonQ 2022, QHack 2024, Qiskit Summer Jam, Berlin 2026), rubrics converge on four things:
- **novelty/creativity**
- **technical execution and rigor ("how well it runs")**
- **impact/relevance to the challenge**
- **clarity of presentation and documentation**

Organizers explicitly reward honest critical analysis over flashy unsupported numbers, and they penalize drifting off-challenge and undocumented repositories. For Qollab specifically, the "Quantum Impact" theme asks for a public dataset, a *strong classical baseline*, and a measurable quantum contribution.

### Cited Findings

**Qollab x IonQ SESSION 2026.10.09 (the target event)**
- **Format:** 48-hour remote build in the browser on Qollab, from 19:00 ET Oct 9 to 19:00 ET Oct 11, 2026. Python with Qiskit. Teams of up to 4. Projects are published under an MIT license with an explainer page. Local panels judge first, then a global panel. — [Quantum Zeitgeist](https://quantumzeitgeist.com/ionq-quantum-hackathon-qollab-host/); [Qollab](https://qollab.xyz/programs/hackathon)
- **Judging criteria (secondary summary):** "Novelty of the work; How well it runs; What it changes; How clearly it is written," with the same score sheet at every node. Weights are not published on the main page. — [Quantum Zeitgeist](https://quantumzeitgeist.com/ionq-quantum-hackathon-qollab-host/)
- **Themes:**
  - *Quantum Impact:* a public dataset plus a strong classical baseline, then show where a quantum subroutine makes a measurable difference.
  - *Quantum Playground:* game, music or art where superposition, interference, entanglement or measurement is essential, "not just a source of randomness."
  - *Quantum Unlocked:* teach error correction, fault tolerance, networking or algorithms interactively.
  - [Qollab](https://qollab.xyz/programs/hackathon)
- **Prizes:** 1st $10k + $20k compute, 2nd $5k + $15k, 3rd $2.5k + $10k. Specialty awards ($500 + $5k compute) cover most novel, best documentation, greatest impact, and best per theme. The global top 3 get IonQ engineer mentorship and expedited interviews. — [Quantum Zeitgeist](https://quantumzeitgeist.com/ionq-quantum-hackathon-qollab-host/); [Qollab](https://qollab.xyz/programs/hackathon)
- **Source conflicts:**
  - Registration close: Oct 6 per Quantum Zeitgeist vs Oct 8 11:00 ET per the Qollab page.
  - Node count: "21 university nodes in 10 countries" vs "24 nodes across 25 locations in 10 countries."
  - Simulator-only access: stated in the secondary source, absent from the fetched Qollab page.
  - [Quantum Zeitgeist](https://quantumzeitgeist.com/ionq-quantum-hackathon-qollab-host/); [Qollab](https://qollab.xyz/programs/hackathon)
- **Related:** IonQ also backs Qollab's Creative Challenge (Mar 2026), which offers $50k in IonQ credits for open-source quantum experiments. This signals IonQ's interest in creative, open, forkable projects. — [IonQ news](https://ionq.com/news/ionq-partners-with-qollabs-creative-challenge-advancing-creative-quantum-innovation)

**Other rubrics and organizer advice**
- **Microsoft/IonQ challenge at iQuHACK 2022:** judged on lightning presentations plus code, on 5 scales: utility of concept, technical merit, creativity, relevance, and communication. Each judge saw only a subset of teams. The winner, "Opti-maze," was a *game teaching QAOA* where the player competes or cooperates with the quantum computer. — [Microsoft Q# blog](https://devblogs.microsoft.com/qsharp/?p=1707)
- **QHack 2024 organizers (PennyLane/Xanadu, Feb 2024):**
  - "Don't start programming before you are clear about what you want to do and how to do it."
  - Re-check daily that you're still on-challenge, since off-topic projects can be discarded early.
  - Rigor and honest reporting count, and "a simpler result with clear critical thinking can outscore a flashier one."
  - Use mixed-skill teams.
  - README explaining each file, comments at critical sections, and a report a newcomer can retrace: "please don't make us do code archaeology."
  - Pitfalls: unexplained notebook sprawl, impressive numbers without analysis, too little planning, missed deadlines.
  - Multiple judges score each project, and the scores are averaged.
  - [PennyLane blog](https://pennylane.ai/blog/2024/02/how-to-do-a-great-hackathon-project)
- **Qiskit Community Summer Jam:** 25% each for originality, usefulness/complexity, community benefit, and digital presentation. — [HackerEarth](https://www.hackerearth.com/challenges/hackathon/qiskit-community-summer-jam-north-carolina/)
- **Berlin Quantum Hackathon 2026:** innovation, technical execution, real-world impact, and clarity of presentation. — [Quantum Zeitgeist](https://quantumzeitgeist.com/quantum-computing-quantum-hackathon/)
- **Unverified secondary claim (Aug 2026 blog):** at iQuHACK, the hardware sponsor writes challenges, its engineers score them, and "documentation [is weighted] about as heavily as code." — [Litslink blog](https://litslink.com/blog/what-is-quantum-hackathon)
- **Past IonQ-track winners show a creative/educational bias:**
  - iQuHACK 2023 IonQ 1st place: "Entanglement5." A UMass team won with "Game of Finches," an interactive evolution model. — [iQuHACK 2023](https://www.iquise.mit.edu/iquhack/2023-01-27); [UMass CICS](https://www.cics.umass.edu/news/cics-student-wins-iquhack-2023)
  - iQuHACK 2024 IonQ: 1st fATCAT, 2nd FalQon. — [iQuHACK 2024](https://www.iquise.mit.edu/iquhack/2024-02-02)
  - iQuHACK 2026 IonQ challenge: gamified entanglement distillation on a quantum-network graph. — [The Tech, Feb 2026](https://thetech.com/2026/02/19/iquhack-2026)

### Inferences
- **Scoping for 48 h (suggested timeline):**
  - **H0–4:** pick the theme. Write a one-paragraph problem statement plus the success metric. Choose the dataset and the classical baseline.
  - **H4–16:** classical baseline and ideal-simulator prototype at 4–12 qubits.
  - **H16–30:** forte-1 noisy simulation, a scaling sweep (qubits and 2Q count), and mitigation (post-selection, ZNE with controls).
  - **H30–40:** UI/visualization or demo notebook, README, and explainer page.
  - **H40–48:** slides or video, buffer, and a frozen submission.
  - Freeze scope at ~H24. No new algorithms after that.
- **Team roles (4 people):**
  1. Quantum circuit lead (ansatz, compilation, 2Q-count minimization).
  2. Classical baseline and data lead (dataset, solver, metrics).
  3. Noise and benchmarking lead (noise-model sweeps, mitigation, error bars, plots).
  4. Product and communication lead (UI or demo, README, explainer, pitch).
- **Slide/demo structure that maps to the Qollab rubric:**
  1. Problem and why it matters ("what it changes").
  2. Why quantum, and why IonQ specifically (all-to-all connectivity → 2Q-count comparison vs nearest-neighbor topology).
  3. Method (circuit diagram with qubit count, 2Q count, shots).
  4. Results: ideal vs noisy (forte-1) vs mitigated vs classical baseline, with error bars.
  5. Honest limits: no advantage claimed, where noise breaks it, and the scaling curve.
  6. What changes with better hardware or a QPU run (tie-in to the compute prize).
  7. Repo/README and live demo.
- **Common point-losers inferred from the sources:**
  - Claiming quantum advantage or quoting vendor speedups (Ansys 12%, AstraZeneca 20x) as validated.
  - No classical baseline, which is explicitly required in Quantum Impact.
  - Randomness-only "quantum" art in Playground.
  - Results only from the ideal simulator.
  - ZNE improvements without controls.
  - Notebook sprawl with no README.
  - Going off-theme.
  - Circuits sized beyond the ~29-qubit simulator limit or a ~100–200 2Q-gate noise budget.

### Gaps
- No published interviews or blog posts from **IonQ engineers acting as hackathon judges** stating their preferences were found.
- The weights for the Qollab rubric and its full "How it works" and Rules pages could not be retrieved (the fetch returned only a title).
- IonQ-track rubrics for iQuHACK 2023–2026 were not found. Only the 2022 Microsoft/IonQ rubric is documented.
- Whether Qollab participants get *any* QPU shots during the build is unconfirmed. It needs organizer confirmation (hello@qollab.xyz, per the Qollab page).
