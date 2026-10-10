# IonQ Hardware, Software Stack, and Developer Access (state as of 2026-10-07)

Research date: 2026-10-07. Live API data was pulled from `https://api.ionq.co/v0.4/backends` on 2026-10-07 (timestamps ~19:45-19:51 UTC). PyPI and GitHub data were pulled on the same day. Every spec below carries the date of its source. "Undated" means the page carries no date (only a 2017-2026 copyright), and I read it on 2026-10-07.

---

## Q1. Which IonQ systems can a hackathon participant actually use in Oct 2026, and what are their specs and limits (max qubits, max shots, queue times, circuit limits)?

### Takeaway
As of 2026-10-07, the only public IonQ QPUs are the **36-qubit Forte-class systems**: `qpu.forte-1` (College Park, MD) and `qpu.forte-enterprise-1` (Basel, Switzerland). Both use the native **GPi/GPi2/ZZ** gate set and have all-to-all connectivity. **Aria-1, Aria-2 and Harmony are retired.** **Tempo (100 qubits, #AQ 64) does not appear in the public backend list.** In practice you get a free 29-qubit cloud simulator (ideal plus Forte noise models) and, if credits are provided, Forte / Forte Enterprise with queue waits of hours.

### Cited Findings

**Live backend snapshot (IonQ API v0.4, 2026-10-07)**
- `GET /v0.4/backends` returned the backends below. Every QPU entry lists supported error mitigations "Debias" and "Sharpen" — [IonQ API /v0.4/backends, fetched 2026-10-07](https://api.ionq.co/v0.4/backends)

  | Backend | Status (2026-10-07) | Qubits | average_queue_time (raw) | Native gates |
  |---|---|---|---|---|
  | qpu.harmony | **retired** | 11 | 0 | gpi, gpi2, ms |
  | qpu.aria-1 | **retired** | 25 | 0 | gpi, gpi2, ms |
  | qpu.aria-2 | **retired** | 25 | 0 | gpi, gpi2, ms |
  | qpu.forte-1 | unavailable (at snapshot time) | 36 | 21,996,253 | gpi, gpi2, zz |
  | qpu.forte-enterprise-1 | **available** | 36 | 6,870,772 | gpi, gpi2, zz |
  | qpu.forte-enterprise-3 | unavailable | 36 | 55,978,632 | gpi, gpi2, zz |
  | simulator | available | 29 | 0 | gpi, gpi2, zz; noise models aria-1, aria-2, forte-1, forte-enterprise-1, ideal |

- The `qpu.forte-enterprise-1` detail record (2026-10-07) lists:
  - QIS `supported_gates`: x, y, z, h, s, si, t, ti, v, vi, rx, ry, rz, cnot, swap, xx, yy, zz, not
  - `supported_native_gates`: gpi, gpi2, zz
  - `supported_error_mitigations`: Debias, Sharpen
  - reported power draw `kw: 4.60929`
  - Source: [IonQ API /v0.4/backends/qpu.forte-enterprise-1](https://api.ionq.co/v0.4/backends/qpu.forte-enterprise-1)
- IonQ's docs backend table (undated, read 2026-10-07) lists:
  - Forte Enterprise 1: Available, 36 qubits, Basel, Switzerland
  - Forte 1: Available, 36 qubits, College Park, MD
  - Aria 1 / Aria 2: Retired, 25 qubits
  - Harmony: Retired, 11 qubits
  - All simulators are hosted on Google Cloud under the backend name `simulator`
  - Source: [IonQ Docs – Backends](https://docs.ionq.com/user-manual/backends)
- Harmony QPU retired September 2024; its noise model retired July 2025 — [IonQ Docs – Simulation with Noise Models](https://docs.ionq.com/features/simulation-with-noise-models)
- Amazon Braket removed IonQ Aria-2 on **2025-10-27** and IonQ Aria-1 on **2026-03-02** — [Braket developer guide document history](https://docs.aws.amazon.com/braket/latest/developerguide/doc-history.html)
- Braket's current QPU list contains only two IonQ devices, `arn:aws:braket:us-east-1::device/qpu/ionq/Forte-1` and `arn:aws:braket:us-east-1::device/qpu/ionq/Forte-Enterprise-1` — [Braket: Submitting quantum tasks to QPUs](https://docs.aws.amazon.com/braket/latest/developerguide/braket-qpu-partner-ionq.html)
- Braket added Forte Enterprise on 2025-03-20 (us-east-1). The hardware sits in Switzerland, but traffic routes through US East — [AWS What's New, 2025-03-20 (German)](https://aws.amazon.com/de/about-aws/whats-new/2025/03/ionq-forte-enterprise-amazon-braket/)
- IonQ announced global availability of Forte Enterprise via Braket and IonQ Quantum Cloud on 2025-04-01 — [IonQ IR, 2025-04-01](https://investors.ionq.com/news/news-details/2025/IonQ-Announces-Global-Availability-of-Forte-Enterprise-Through-Amazon-Braket-and-IonQ-Quantum-Cloud/default.aspx)
- **Conflict:** Azure Quantum's IonQ provider page (metadata updated 2026-08-29) still lists `ionq.qpu.aria-1` (25 qubits), next to `ionq.qpu.forte-1`, `ionq.qpu.forte-enterprise-1`, and `ionq.simulator` (29 qubits, free). This conflicts with IonQ's own API, which shows Aria-1 as retired — [Microsoft Learn – IonQ provider](https://learn.microsoft.com/en-us/azure/quantum/provider-ionq)

**Published specs, Forte / Forte Enterprise (IonQ product pages, undated, read 2026-10-07)**
- Forte:
  - 36 qubits
  - 1Q gate error 0.02% (Clifford RB)
  - 2Q gate error 0.4% (direct RB)
  - SPAM error 0.5%
  - T1 "10–100s", T2 "~1s"
  - "Available since 2022"
  - The page also says a newer barium system reaches about 0.04% SPAM error
  - Source: [IonQ – Forte](https://www.ionq.com/quantum-systems/forte)
- Forte Enterprise: 36 qubits, #AQ 36, and the same error figures (0.02% / 0.4% / 0.5%, T1 10–100 s, T2 ~1 s). It is rack-mountable for data-center deployment — [IonQ – Forte Enterprise](https://www.ionq.com/quantum-systems/forte-enterprise)
- Compare page:
  - Forte: 36 qubits, 99.6% 2Q, 99.98% 1Q, all-to-all, AOD gate control, #AQ 36
  - Forte Enterprise: 36 qubits, 99.6% 2Q, 99.98% 1Q
  - Tempo: 100 qubits, 99.9% 2Q, 99.99% 1Q, **"Many-to-many" connectivity**, "Late 2026"
  - Source: [IonQ – Compare systems](https://www.ionq.com/quantum-systems/compare)
- Microsoft says Forte and Forte Enterprise share the same core hardware and performance and differ only in deployment (data-center ruggedization) — [Microsoft Learn – IonQ provider](https://learn.microsoft.com/en-us/azure/quantum/provider-ionq)
- Gate timing exists only for the retired **Aria**: T1 10–100 s, T2 1 s, 1Q gate 135 µs, 2Q gate 600 µs. Fidelities: 1Q 99.95% (SPAM-corrected), 2Q 99.6%, SPAM 99.61% — [Microsoft Learn – IonQ provider](https://learn.microsoft.com/en-us/azure/quantum/provider-ionq)
- Live per-backend characterization data (fidelities, timings) is in the Cloud Console "Backends" tab and the v0.4 characterization endpoints. Those need an authenticated API key: my unauthenticated calls returned 401/403 on 2026-10-07 — [IonQ Docs – Backends](https://docs.ionq.com/user-manual/backends)

**Tempo and newer systems**
- On 2025-09-25 IonQ announced #AQ 64 on a Tempo system, "three months ahead of schedule". No fidelity numbers and no cloud rollout plan were given — [IonQ news, 2025-09-25](https://www.ionq.com/news/ionq-achieves-record-breaking-quantum-performance-milestone-of-aq-64)
  - Coverage disagrees on the qubit count behind the AQ 64 result (100-qubit system vs. a 64-qubit computational register) — [Quantum Computing Report](https://quantumcomputingreport.com/ionq-reaches-aq-64-milestone-on-100-qubit-tempo-system-ahead-of-schedule/)
- The Tempo product page (undated) says "100-Qubit Quantum Computer (#AQ 64)", 99.9% target fidelity, and lists mid-circuit measurement as a capability. Its CTA is "Inquire about IonQ Tempo" (pre-sales), not self-serve — [IonQ – Tempo](https://www.ionq.com/quantum-systems/tempo)
- qiskit-ionq PR #263 (merged 2026-07-16) builds backend targets from the API, including connectivity mapped to a coupling map. It describes itself as "groundwork for Tempo (`qpu.tempo-1` now resolves...)" and mentions testing against "staging tempo-1" — [qiskit-ionq PR #263](https://github.com/qiskit-community/qiskit-ionq/pull/263)
- KISTI (South Korea) finalized a deal for a 100-qubit Tempo system on 2025-12-23. Access will be through a private cloud (Megazone Cloud) for Korean users, and the release calls delivery "forthcoming" — [The Quantum Insider, 2025-12-23](https://thequantuminsider.com/2025/12/23/ionq-and-kisti-finalize-agreement-to-deliver-100-qubit-quantum-system-in-south-korea/)
- In Q2 2026 (reported 2026-08-07), IonQ credited growth to "global deployments of our IonQ Tempo quantum computers", but no public-cloud availability was stated — [Futurum, 2026-08-07](https://futurumgroup.com/insights/ionq-q2-fy-2026-tempo-quantum-computers-drive-growth-ahead-of-skywater-integration/)
- Superion 256 (256 qubits, Electronic Qubit Control, fabricated at SkyWater) was introduced at Investor Day on 2026-09-08. Customer deliveries are planned for 2027 and cloud access later, with no date — [The Quantum Insider, 2026-09-08](https://thequantuminsider.com/2026/09/08/ionq-uses-investor-day-to-detail-superion-roadmap-skywater-strategy-and-quantum-security-plans/)

**Job limits and queueing (IonQ API v0.4)**
- `shots`:
  - minimum 1, maximum **1,000,000**
  - ignored by the ideal simulator
  - debiasing requires ≥500 shots
  - Source: [IonQ API v0.4 – Create job](https://docs.ionq.com/api-reference/v0.4/jobs/create-job)
- Multi-circuit jobs (`ionq.multi-circuit.v1`) allow at most **5,000 circuits and 150,000 gates in total**. The request body must be ≤ **10 MB**. HTTP 429 means you hit a rate limit (contact support to raise it) — [IonQ API v0.4 – Create job](https://docs.ionq.com/api-reference/v0.4/jobs/create-job)
- Job types: `ionq.circuit.v1` (JSON gate list), `ionq.qasm3.v1` (OpenQASM 3), `ionq.multi-circuit.v1` — [IonQ API v0.4 – Create job](https://docs.ionq.com/api-reference/v0.4/jobs/create-job)
- On Amazon Braket (on-demand), IonQ devices allow at most **2,000 gates per circuit** and need ≥2,500 shots for error-mitigation tasks. With a direct reservation the limits are 5,000 gates per circuit and 500 shots — [Braket – Error mitigation on IonQ](https://docs.aws.amazon.com/braket/latest/developerguide/error-mitigation-ionq.html)
- IonQ queues use a **fair-share weighted scheduler** by organization allocation group. Reservations give exclusive QPU time in blocks of at least 1 hour, are open only to contract customers, and are booked through support@ionq.co. Braket users can reserve via Braket Direct — [IonQ Docs – Platform Systems](https://docs.ionq.com/user-manual/platform-systems)
- Simulator qubit limits:
  - ideal and Forte-class noise models: up to **29 qubits**
  - Aria noise models: 25 qubits
  - the docs warn that "simulations approaching the ideal and Forte-class qubit limits may still fail"
  - Source: [IonQ Docs – Backends](https://docs.ionq.com/user-manual/backends)
- A free IonQ account includes the simulators (up to 29 qubits) and the noise-model simulators — [IonQ Docs home](https://docs.ionq.com/)
- System status lives at status.ionq.co, with states Operational, Degraded, and Under Maintenance — [IonQ Docs – Backends](https://docs.ionq.com/user-manual/backends)

### Inferences
- **Realistic hackathon target (Oct 2026):**
  - Develop on `simulator` (ideal) and `simulator` with `noise_model="forte-enterprise-1"` or `"forte-1"`, keeping circuits ≤29 qubits.
  - Run final QPU jobs on **`qpu.forte-enterprise-1`**, the only QPU "available" in the live snapshot, or `qpu.forte-1` if it comes back.
  - Do not plan around Aria (retired) or Tempo (not public; the SDK groundwork points to an upcoming `qpu.tempo-1`).
- **Queue times:**
  - The raw `average_queue_time` values are most likely **milliseconds**. IonQ's earlier API docs defined this field in ms, but the v0.4 response I fetched states no unit.
  - Read as ms, the waits are about **1.9 h** (Forte Enterprise 1), **6.1 h** (Forte 1), and **15.6 h** (Forte Enterprise 3).
  - Submit asynchronously, save job IDs, and expect hackathon QPU jobs to return hours later.
- **`qpu.forte-enterprise-3`:** it appears in the live API but in no IonQ doc I found. It is probably a newly deployed Forte Enterprise unit not yet generally listed.
- **Tempo connectivity:** Tempo is listed as "many-to-many", not "all-to-all", and the SDK now builds a coupling map from the API. Circuits written for Tempo may need routing, unlike Forte.
- **Depth limits:** IonQ publishes no explicit circuit-depth limit. The practical limits are fidelity (99.6% 2Q means about 0.4% error per 2Q gate, so about 100 two-qubit gates in sequence already costs about 33% of fidelity), the Braket 2,000-gate on-demand cap, and the 150,000-gate cap per multi-circuit job.

### Gaps
- Forte / Forte Enterprise **gate durations** (1Q/2Q), readout and reset times, and current measured characterization values: the characterization endpoints need an authenticated key, and no public 2026 page lists Forte gate times. Only the retired Aria's timings (135 µs / 600 µs) are published.
- Whether Tempo is on any public cloud as of Oct 2026: I found no evidence that it is.
- What `forte-enterprise-3` is, and where it is deployed: no source.
- The unit of `average_queue_time` in v0.4 is not documented on the pages I retrieved (ms is inferred).
- Whether IonQ still publishes #AQ for Forte Enterprise or has replaced it with logical-qubit metrics: the 2025-09-25 release says IonQ will report logical qubits and error rates "going forward".

---

## Q2. What is the native gate set, how do you write native-gate circuits in Qiskit / Cirq / PennyLane (and Braket / API), and how do you minimize 2-qubit gate count?

### Takeaway
IonQ's native gates are single-qubit **GPi(φ)** and **GPi2(φ)**, plus one entangling gate per system family: **MS(φ0, φ1[, θ])** on Aria-class (retired) and **ZZ(θ)** on Forte-class (all current QPUs). All parameters are in **turns** (1 turn = 2π). Native circuits **bypass IonQ's compiler and optimizer**, and debiasing is **off by default** for them. For most hackathon work, submit abstract (QIS) gates and let IonQ compile. If you pre-transpile with Qiskit, use optimization level 0 or 1. Use native ZZ only when you need exact control.

### Cited Findings

**Gate definitions** (all from [IonQ Docs – Getting started with native gates](https://docs.ionq.com/features/getting-started-with-native-gates))
- **GPi(φ):**
  - π rotation about an equatorial axis set by φ; φ=0 gives X, φ=0.25 gives Y
  - Matrix [[0, e^(−2πiφ)], [e^(2πiφ), 0]]
- **GPi2(φ):**
  - π/2 rotation; φ=0.5 gives RX(π/2), φ=0.25 gives RY(π/2)
  - Matrix (1/√2)[[1, −i e^(−2πiφ)], [−i e^(2πiφ), 1]]
- **Virtual Z:** not a physical gate. It is applied by shifting the phases of later gates (phase tracking), so it is free.
- **MS(φ0, φ1)** (Aria only): fully entangling XX-type gate.
  - **Partial MS** takes an optional θ in [0, 0.25] (0.25 = fully entangling), with hardware precision of about 3 decimal places.
  - One arbitrary-angle MS replaces "up to two fully-entangling MS gates plus four single-qubit rotations".
  - Small-angle MS used lower-power pulses; on one earlier system, fidelity rose from about 97.5% (π/2) to 99.6% (π/100).
- **ZZ(θ)** (Forte only): ZZ(θ) = exp(−iπθ Z⊗Z), one parameter.
- Each circuit must use a single gateset; native and abstract gates cannot be mixed in one circuit.
- Native submission "turns off the compilation and optimization toolchain".

**System gate sets**
- Aria: GPi, GPi2, MS. Forte: GPi, GPi2, ZZ — [IonQ Docs – native gates](https://docs.ionq.com/features/getting-started-with-native-gates)
- The live API (2026-10-07) shows Forte / Forte Enterprise / simulator native gates as `gpi, gpi2, zz` — [IonQ API /v0.4/backends](https://api.ionq.co/v0.4/backends)

**Native JSON (IonQ API)**
- Set `"gateset": "native"` in `input`. Gates are `gpi` (`phase`, `target`), `gpi2` (`phase`, `target`), `ms` (`phases`, optional `angle` 0–0.25, `targets`), and `zz` (`angle`, `targets`). Phases are floats in [−1, 1] turns — [IonQ Docs – Native gates via API](https://docs.ionq.com/api-reference/v0.3/native-gates-api)
- A Forte-compatible example (adapted to `zz`):
  ```json
  {"type":"ionq.circuit.v1","backend":"simulator","shots":1024,
   "input":{"gateset":"native","qubits":2,"circuit":[
     {"gate":"gpi2","phase":0,"target":0},
     {"gate":"zz","angle":0.25,"targets":[0,1]},
     {"gate":"gpi","phase":0.25,"target":1}]}}
  ```
  The schema follows [native gates API](https://docs.ionq.com/api-reference/v0.3/native-gates-api) and the [v0.4 create job](https://docs.ionq.com/api-reference/v0.4/jobs/create-job) pages. The specific gate sequence is illustrative.

**Qiskit** (from [IonQ Docs – Compilation and native gates with Qiskit](https://docs.ionq.com/sdks/qiskit/native-gates-qiskit))
- `from qiskit_ionq import GPIGate, GPI2Gate, MSGate, ZZGate`. MSGate is marked "for Aria systems (retired)"; ZZGate is for Forte. Qiskit's own `qiskit.circuit.library` MS/ZZ gates are **not** the same as IonQ's native gates.
- Declare a native backend with `provider.get_backend("simulator", gateset="native")` (or a QPU). Then call `qc_native = transpile(qc_abstract, backend=backend_native)`, which transpiles to Forte (ZZ) or Aria (MS) native gates. This has been supported since qiskit-ionq v1.0.0.
- Minimal example:
  ```python
  from qiskit import QuantumCircuit, transpile
  from qiskit_ionq import IonQProvider, GPIGate, GPI2Gate, ZZGate
  provider = IonQProvider()                      # reads IONQ_API_KEY
  backend = provider.get_backend("simulator", gateset="native")
  qc = QuantumCircuit(2)
  qc.append(GPI2Gate(0), [0]); qc.append(ZZGate(0.25), [0, 1]); qc.append(GPIGate(0.25), [1])
  qc.measure_all()
  print(backend.run(qc, shots=1000).get_counts())
  ```
  Gate names follow the docs page; the circuit itself is illustrative.
- Transpile to QIS at optimization levels 0/1: "With an optimization level of 2 or 3, Qiskit may perform transpiler passes that are not compatible with the further optimization performed by IonQ's compiler." Qiskit ≥1.3 defaults to level 2, and qiskit-ionq >1.0.2 emits `IonQTranspileLevelWarning`. You can set `transpile_optimization_level = 1` in `~/.qiskit/settings.conf` — [IonQ Docs – Qiskit native gates](https://docs.ionq.com/sdks/qiskit/native-gates-qiskit), [IonQ Docs – Qiskit getting started](https://docs.ionq.com/sdks/qiskit/index)
- Unsupported Qiskit ops (for example `UnitaryGate`, `u`, `iswap`) raise `IonQGateError`. Transpile them with `transpile(qc, backend=ionq_backend, optimization_level=0)` — [IonQ Docs – Qiskit native gates](https://docs.ionq.com/sdks/qiskit/native-gates-qiskit)

**Cirq**
- `from cirq_ionq.ionq_native_gates import GPIGate, GPI2Gate, MSGate`. Cirq auto-detects the native gateset, so no flag is needed. To transpile, use `cirq.optimize_for_target_gateset(circuit, gateset=AriaNativeGateset())` from `cirq_ionq.ionq_native_target_gateset`. IonQ's docs say the ZZ gate "is currently not available in cirq-ionq" and that Forte transpilation is "in progress" — [IonQ Docs – Native gates with Cirq](https://docs.ionq.com/sdks/cirq/native-gates-cirq)
- **Conflict / newer:** the released **cirq-ionq v1.7.0** source already has `class ZZGate` in `ionq_native_gates.py` and `class ForteNativeGateset` in `ionq_native_target_gateset.py`, so IonQ's doc page is stale — [Cirq v1.7.0 cirq-ionq source](https://github.com/quantumlib/Cirq/tree/v1.7.0/cirq-ionq/cirq_ionq)
- QIS gates accepted through Cirq: `XPowGate`/`YPowGate`/`ZPowGate` (rx, ry, rz, X, Y, Z), `H`, `XXPowGate`/`YYPowGate`/`ZZPowGate`, `CNOT`, `SWAP`, and measurement. Decompose others with `cirq.optimize_for_target_gateset(circuit, gateset=cirq_ionq.ionq_gateset.IonQTargetGateset())` — [IonQ Docs – Cirq](https://docs.ionq.com/sdks/cirq/index)

**PennyLane**
- `from pennylane_ionq.ops import GPI, GPI2, MS` and `qp.device('ionq.simulator', wires=3, gateset="native")`. Native support dates from plugin v0.28.0. There is **no automatic abstract-to-native transpilation** in pennylane-ionq — [IonQ Docs – Native gates with PennyLane](https://docs.ionq.com/sdks/pennylane/native-gates-pennylane)
- The pennylane-ionq `ZZ` op is the **Ising** ZZ, exp(−iφ/2 Z⊗Z), part of the QIS set. It is not the native Forte ZZ in turns. v0.45.0 added `IsingXX`/`IsingYY`/`IsingZZ` support — [pennylane-ionq ops.py](https://github.com/PennyLaneAI/PennyLane-IonQ/blob/master/pennylane_ionq/ops.py), [pennylane-ionq releases](https://github.com/PennyLaneAI/PennyLane-IonQ/releases)

**Braket and Azure**
- Braket IonQ QIS gates: 'x','y','z','rx','ry','rz','h','cnot','s','si','t','ti','v','vi','xx','yy','zz','swap'. Native gates 'gpi','gpi2','zz' work **only inside verbatim compilation** (verbatim boxes) — [Braket – IonQ](https://docs.aws.amazon.com/braket/latest/developerguide/braket-qpu-partner-ionq.html)
- Azure + Qiskit native: `provider.get_backend("ionq.qpu.<target>", gateset="native")`, where `gateset` is `qis` (default) or `native` — [Microsoft Learn – IonQ provider](https://learn.microsoft.com/en-us/azure/quantum/provider-ionq)

**OpenQASM 3 (API v0.4) supported subset**
- Gates: x, y, z, h, s, t, sx, rx, ry, rz, p, and the IonQ extensions `xphase` / `yphase`. Two-qubit gates: cx, cy, cz, swap.
- `ctrl @` is allowed only on x, z, rz, xphase, yphase. Use `ctrl(2) @ x` instead of `ccx`.
- Gate angles must be constant; `pi` is the only named constant.
- No `def`, no scalar `qubit`/`bit`.
- Source: [IonQ API v0.4 – OpenQASM 3](https://docs.ionq.com/api-reference/v0.4/openqasm3)

**Cost / 2Q accounting hints**
- IonQ's estimator counts an N-qubit gate (N ≥ 3) as **6(N−2)** two-qubit gates — [IonQ Docs – Job Cost and Usage](https://docs.ionq.com/guides/job-cost-and-usage). Azure bills the same way: "a NOT gate with three controls would be billed as … 12 two-qubit gates" — [Azure Quantum pricing](https://learn.microsoft.com/en-us/azure/quantum/pricing)
- v0.4 job objects report `stats.gate_counts` (1q/2q submitted) and `output.compilation` diagnostics — [IonQ API v0.4 migration](https://docs.ionq.com/api-reference/v0.4/migration-from-v0.3)
- `dry_run=True` (qiskit-ionq ≥1.0.3) compiles the circuit without running it. With `job_settings={"compilation": {"service_version": "v0.4"}}`, `job.compiled_circuit(lang="native")` returns the IonQ-native compiled circuit — [qiskit-ionq README (main)](https://github.com/qiskit-community/qiskit-ionq/blob/main/README.md)
- v0.4 `settings.compilation` accepts `gate_basis`, `precision`, and `opt` (number) — [IonQ API v0.4 – Create job](https://docs.ionq.com/api-reference/v0.4/jobs/create-job)

### Inferences
- **Best practices to minimize 2Q gates on Forte:**
  1. **Do not insert SWAPs.** Connectivity is all-to-all, so don't let a generic transpiler route on a line or grid. Keep Qiskit at optimization level 0/1, or transpile with the IonQ backend so no restrictive coupling map is applied.
  2. **Express interactions as ZZ/XX/YY rotations directly** (QIS `zz`/`xx`/`yy`, or Qiskit `rzz`, which then compiles). On Forte, an arbitrary ZZ(θ) is a single native 2Q gate. RZZ(φ) = exp(−iφ/2 Z⊗Z) equals native ZZ(θ) with θ = φ/(2π) turns, so ZZ-type Hamiltonian terms (QAOA, Ising, Trotter steps) cost one 2Q gate each instead of the 2 CNOTs used on CNOT-native hardware. (Derived from the ZZ(θ) definition above.)
  3. **Avoid multi-controlled gates.** Each counts as 6(N−2) 2Q gates for cost and probably close to that for depth.
  4. **Treat Z rotations as free** (virtual Z). Put the work into Z-type phases where possible.
  5. **Use `dry_run` to read the compiled 2Q count** before spending credits, and compare ansätze.
  6. Prefer **shallow, wide circuits**. 29-qubit simulation is the ceiling for checking results anyway.
- Native gates are worth it in a hackathon mainly for noise-characterization or "hardware-aware" narratives. For scoring, abstract gates plus IonQ's compiler plus debiasing usually do better, per IonQ's own warnings.
- **MS vs ZZ:** most public examples (Cirq/PennyLane docs) still use **MS**, which is retired with Aria. The live API lists the simulator's native set as `gpi, gpi2, zz`, so MS-based native examples may be rejected even on the simulator. Port MS examples to ZZ and test.

### Gaps
- Exact ZZ(θ) angle range and precision on Forte: the docs state MS precision (about 3 decimals) but not ZZ precision or allowed range.
- Whether `ms` native circuits are still accepted on the simulator: the docs show MS examples, but the live API lists only zz.
- No IonQ document lists Braket verbatim-box code for gpi/gpi2/zz, or Braket's angle units (radians vs turns) for these gates. Verify in the Braket SDK before use.
- No published IonQ guide on the compiler's internal passes beyond the `opt` / `precision` / `gate_basis` settings.

---

## Q3. What noise models does the IonQ simulator support, and how do you invoke them in each SDK?

### Takeaway
The cloud `simulator` offers **`ideal`** (default) plus hardware noise models **`forte-1`** and **`forte-enterprise-1`** (both updated or added September 2025), and legacy **`aria-1`** and **`aria-2`**, whose QPUs are retired. `harmony` has been removed. Forte-class noise simulations are capped at **29 qubits** and Aria models at 25. Noisy simulation is free, shot-aware, seedable, and does **not** include debiasing.

### Cited Findings
- **Model list:**
  - `forte-1` (updated September 2025)
  - `forte-enterprise-1` (added September 2025)
  - `aria-1`, `aria-2` (QPUs retired; models still available)
  - `harmony` (model retired July 2025)
  - `ideal` (default)
  - Source: [IonQ Docs – Simulation with Noise Models](https://docs.ionq.com/features/simulation-with-noise-models)
- The live API simulator entry (2026-10-07) lists noise models `aria-1, aria-2, forte-1, forte-enterprise-1, ideal` — [IonQ API /v0.4/backends](https://api.ionq.co/v0.4/backends)
- **Model physics:**
  - Aria models, and Forte jobs before mid-September 2025, use a single depolarizing channel applied after each 1Q/2Q gate. Parameters: Aria 1 r1q=0.0005, r2q=0.0133; Aria 2 r1q≈0.000657, r2q=0.01856; old Forte 1 r1q≈0.000267, r2q≈0.004949.
  - The September 2025 Forte and Forte Enterprise models are "more complex than the approach described", and their documentation is "in preparation".
  - IonQ offers "no specific guarantees of accuracy".
  - Source: [IonQ Docs – Simulation with Noise Models](https://docs.ionq.com/features/simulation-with-noise-models)
- **Behavior:**
  - Noisy simulation is shot-aware: one simulation per shot, so the count total equals the shots.
  - Seed: an integer from 1 to 2^31. If omitted, a random seed is chosen and returned.
  - Abstract-gate circuits are compiled and optimized before simulation; native-gate circuits are not modified.
  - Debiasing is not applied in noisy simulation.
  - Source: [IonQ Docs – Simulation with Noise Models](https://docs.ionq.com/features/simulation-with-noise-models)
- The ideal simulator returns probabilities. Via Azure, it returns "the distribution scaled to the number of shots" rather than sampling — [Microsoft Learn – IonQ provider](https://learn.microsoft.com/en-us/azure/quantum/provider-ionq). Via CUDA-Q, ideal results are probabilities × shots, so the counts are exact (for example exactly 500/500) — [IonQ Docs – CUDA-Q](https://docs.ionq.com/sdks/cuda-q)
- Noise model simulations are free for all direct-IonQ users, "including through Google Cloud Marketplace or simulator-only accounts" — [IonQ Docs – Simulation with Noise Models](https://docs.ionq.com/features/simulation-with-noise-models)

**Invocation**
- **REST API:** `"backend": "simulator"` (v0.4; v0.3 used `"target"`) with `"noise": {"model": "forte-1", "seed": 481516}` — [IonQ Docs – noise models](https://docs.ionq.com/features/simulation-with-noise-models), [v0.4 create job](https://docs.ionq.com/api-reference/v0.4/jobs/create-job)
- **Qiskit:** use `backend.set_options(noise_model="forte-1", sampler_seed=8151623)` for a backend-wide default, or `backend.run(qc, shots=1000, noise_model="forte-1")` per job. Available models: `aria-1` (legacy), `aria-2` (legacy), `forte-1`, `forte-enterprise-1` — [IonQ Docs – Qiskit](https://docs.ionq.com/sdks/qiskit/index)
- **Cirq:** `service.run(circuit=c, target="simulator", repetitions=1000, extra_query_params={"noise": {"model": "forte-1"}})` — [IonQ Docs – Cirq](https://docs.ionq.com/sdks/cirq/index)
- **PennyLane (pennylane-ionq v0.45.0):** the device accepts `noise_model=` (only with `target="simulator"`) and `noise_seed=` (1 to 2^31−1). `noise_seed` requires `noise_model` — [pennylane-ionq v0.45.0 device.py](https://github.com/PennyLaneAI/PennyLane-IonQ/blob/v0.45.0/pennylane_ionq/device.py)
- **CUDA-Q:** `cudaq.set_target('ionq', noise='forte-1')`, then `cudaq.sample(kernel, shots_count=1000)` — [IonQ Docs – CUDA-Q](https://docs.ionq.com/sdks/cuda-q)
- **Azure Quantum:**
  - `option_params = {"noise": {"model": "aria-1", "seed": 1000}}`, passed as `input_params=` (Q#) or `backend.options.update_options(**option_params)` (Qiskit).
  - Azure's page documents only `ideal` and `aria-1` as model values.
  - Shots default to 1000 for noise models.
  - Source: [Microsoft Learn – IonQ provider](https://learn.microsoft.com/en-us/azure/quantum/provider-ionq)
- **Per-shot memory:** QPU and noisy-simulator jobs can return per-shot bitstrings with `backend.run(qc, shots=1000, memory=True)` and `job.get_memory()`. The ideal simulator cannot — [qiskit-ionq README (main)](https://github.com/qiskit-community/qiskit-ionq/blob/main/README.md)

### Inferences
- For a hackathon, `forte-enterprise-1` is the most relevant noise model, because Forte Enterprise 1 was the only "available" QPU in the live snapshot.
- Run the ideal sim to check correctness, then the noisy sim with a fixed seed so results are reproducible. Present ideal vs noisy vs QPU side by side.
- Noisy-sim output is only a rough proxy (IonQ disclaims accuracy), so judges should not treat a noisy-sim result as a hardware claim.
- Azure's noise documentation is stale (it mentions only aria-1). Assume `forte-1` / `forte-enterprise-1` pass through but verify.

### Gaps
- The parameters and structure of the post-September-2025 Forte / Forte Enterprise noise models are undocumented ("in preparation").
- The maximum shots for noisy simulation are not stated. Runtime grows with shots × qubits.
- Whether Azure Quantum accepts `forte-1` / `forte-enterprise-1` noise model strings is not documented.

---

## Q4. What error mitigation does IonQ offer, and how do you turn it on or off in the API and each SDK?

### Takeaway
IonQ's built-in mitigation is **debiasing** (symmetrization): the job is split into **25 executions** of equivalent circuit variants (qubit assignments, decompositions, pulse solutions), and results are aggregated by **averaging** (default) or **sharpening** (plurality voting, for sparse outputs). It is **on by default for QIS jobs with ≥500 shots** on the IonQ cloud, off by default for native-gate jobs, unavailable on simulators, and requires ≥2,500 shots on Braket on-demand. Newer options include **symmetry verification** (API v0.4 field), and on qiskit-ionq's unreleased main branch, a **"dnl" (debiasing with non-linear filtering)** aggregation.

### Cited Findings
- **How debiasing works and its defaults** (all from [IonQ Docs – Error Mitigation: Debiasing](https://docs.ionq.com/features/error-mitigation-debiasing)):
  - ≥500 shots are required and are "automatically divided into 25 executions", each a different but equivalent implementation.
  - On by default for QIS jobs with ≥500 shots; off by default for native-gate jobs, but can be turned on.
  - Unavailable on IonQ simulators, including noisy ones.
  - It does not add circuits, shots, qubits, or gates (aside from small decomposition changes).
  - It raises the **minimum per-circuit cost**, so it can raise the cost of small jobs.
  - Original paper: [arXiv:2301.07233](https://arxiv.org/abs/2301.07233) ("symmetrization").
- **Sharpening** is chosen at **result retrieval**, not at submission (from the same debiasing page):
  - All counts from each execution go to that execution's top bitstring.
  - If no clear winner exists, that execution's shots are kept as-is.
  - Requesting sharpened results for a non-debiased job returns an error.
  - Use it only for sparse or peaked distributions.
- **API v0.3:** `"error_mitigation": {"debias": true|false}`; sharpening via query param `sharpen=true` on `/jobs/{id}/results` — [IonQ Docs – Debiasing](https://docs.ionq.com/features/error-mitigation-debiasing)
- **API v0.4:**
  - Submission: `"settings": {"error_mitigation": {"debiasing": false}}`. The schema also has `"symmetry_verification": bool`.
  - Sharpening: `GET https://api.ionq.co/v0.4/jobs/{id}/results/probabilities?sharpen=true`.
  - Sources: [IonQ Docs – Debiasing](https://docs.ionq.com/features/error-mitigation-debiasing), [IonQ API v0.4 – Create job](https://docs.ionq.com/api-reference/v0.4/jobs/create-job)
- **Qiskit (released qiskit-ionq ≤1.1.1):**
  - Submit with `from qiskit_ionq import ErrorMitigation; backend.run(qc, shots=1000, error_mitigation=ErrorMitigation.DEBIASING | ErrorMitigation.NO_DEBIASING)`.
  - Retrieve with `job.result(sharpen=True).get_counts()`.
  - Sources: [IonQ Docs – Debiasing with Qiskit](https://docs.ionq.com/sdks/qiskit/error-mitigation-qiskit), [PyPI qiskit-ionq 1.1.1](https://pypi.org/project/qiskit-ionq/)
- **Qiskit (main branch, unreleased as of 2026-10-07):**
  - Submit with `backend.run(qc, shots=1000, debiasing=True, symmetry_verification=True)`.
  - Retrieve with `job.result(aggregation="average"|"voting"|"dnl")`. `voting` "replaces the deprecated `sharpen=True`"; `dnl` = debiasing with non-linear filtering, [arXiv:2506.05757](https://arxiv.org/abs/2506.05757).
  - The aggregation-fetch fix was committed 2026-09-02.
  - Sources: [qiskit-ionq README (main)](https://github.com/qiskit-community/qiskit-ionq/blob/main/README.md), [qiskit-ionq commits](https://github.com/qiskit-community/qiskit-ionq/commits/main)
- **Cirq:** `service.create_job(..., error_mitigation={"debias": False})`; `job.results(sharpen=True)`. Cirq's `Service.run` also takes `compilation=`, `dry_run=`, and `sharpen=` — [IonQ Docs – Debiasing](https://docs.ionq.com/features/error-mitigation-debiasing), [cirq-ionq service.py](https://github.com/quantumlib/Cirq/blob/main/cirq-ionq/cirq_ionq/service.py)
- **PennyLane:** device kwargs `error_mitigation={"debiasing": True}` and `sharpen=True` — [pennylane-ionq device.py](https://github.com/PennyLaneAI/PennyLane-IonQ/blob/v0.45.0/pennylane_ionq/device.py)
- **Amazon Braket:**
  - Submit with `from braket.error_mitigation import Debias; device.run(circuit, shots=2500, device_parameters={"errorMitigation": Debias()})`.
  - Read sharpened probabilities from `result.additional_metadata.ionqMetadata.sharpenedProbabilities` (renormalized probabilities, not counts).
  - Minimums: 2,500 shots on-demand, 500 with a reservation.
  - Source: [Braket – Error mitigation on IonQ](https://docs.aws.amazon.com/braket/latest/developerguide/error-mitigation-ionq.html)
- **Azure Quantum:**
  - `option_params = {"error-mitigation": {"debias": True|False}}`, passed via `input_params=` (Q#) or `backend.options.update_options(**option_params)` (Qiskit).
  - Debiasing is on by default for Aria and Forte, and those jobs "are subject to debiasing-based pricing".
  - Source: [Microsoft Learn – IonQ provider](https://learn.microsoft.com/en-us/azure/quantum/provider-ionq)
- **Mid-circuit-measurement (qasm3) jobs:** debiasing and `symmetry_verification` also work there (main-branch README). Released v1.1.1 passes them via `job_settings` — [qiskit-ionq README](https://github.com/qiskit-community/qiskit-ionq/blob/main/README.md), [PyPI qiskit-ionq](https://pypi.org/project/qiskit-ionq/)

### Inferences
- **Budget-aware default for a hackathon:**
  - For small or shallow demo circuits (Bell, GHZ ≤ ~10 qubits), **turn debiasing off**. The mitigated minimum price is roughly 6.5× the unmitigated one on Azure Forte ($168.20 vs $25.79).
  - For the headline result (medium/large circuit, ≥500 shots on IonQ direct, ≥2,500 on Braket), leave it on.
  - Retrieve both averaged and sharpened results for peaked outputs (Grover, QAOA argmax), since retrieval costs nothing extra.
- Debiasing changes the qubit mapping between executions. Experiments that need a fixed physical-qubit mapping (noise characterization) should disable it.
- Expect the Qiskit API to change at the next qiskit-ionq release (`error_mitigation=` → `debiasing=`, `sharpen=` → `aggregation=`). Pin the version you test with.

### Gaps
- No public IonQ documentation explains what "symmetry_verification" checks (which symmetries, how it is specified) beyond "discard measurement outcomes that violate the circuit's symmetries".
- Whether the `dnl` aggregation is enabled server-side for all users is unconfirmed (it appears only on the qiskit-ionq main branch).
- No IonQ-provided ZNE/PEC or readout-error-mitigation service was found. Users would implement those client-side.

---

## Q5. What are the current SDK versions, install commands, minimal code paths (simulator and QPU), and known breaking changes?

### Takeaway
As of 2026-10-07:
- **qiskit-ionq 1.1.1** (2026-06-05; requires Qiskit ≥2.0)
- **cirq-ionq 1.7.0** (2026-06-29)
- **pennylane-ionq 0.45.0** (2026-05-12)
- **cudaq 0.16.0.post1** (2026-09-17)
- **amazon-braket-sdk 1.127.3.post0** (2026-09-30)
- **azure-quantum 3.13.0** (2026-10-01)
- **qiskit 2.5.2** (2026-08-13)

All current IonQ plugins talk to **API v0.4**. Key breaking changes:
- Qiskit 2.x needs qiskit-ionq ≥1.0.
- pennylane-ionq 0.45 moved to the v0.4 payload and still defaults the QPU device to the **retired `aria-1`**.
- azure-quantum and qbraid pin `cirq-ionq <1.7`.

Use Python 3.11 or 3.12.

### Cited Findings

**Versions (PyPI, read 2026-10-07)**
| Package | Latest | Released | Python | Key pins |
|---|---|---|---|---|
| qiskit-ionq | 1.1.1 | 2026-06-05 | ≥3.10 | qiskit>=2.0.0 |
| cirq-ionq | 1.7.0 | 2026-06-29 | ≥3.11 | cirq-core==1.7.0 |
| pennylane-ionq | 0.45.0 | 2026-05-12 | – | pennylane>=0.44 |
| cudaq | 0.16.0.post1 | 2026-09-17 | ≥3.11 | – |
| amazon-braket-sdk | 1.127.3.post0 | 2026-09-30 | ≥3.11 | – |
| qiskit-braket-provider | 0.25.0 | 2026-09-10 | – | – |
| azure-quantum | 3.13.0 | 2026-10-01 | ≥3.10 | [cirq] extra: cirq-core<1.7,>=1.6.1; cirq-ionq<1.7; [qiskit] extra: qsharp[qiskit]<2.0,>=1.29.1 |
| qbraid | 0.13.0 | 2026-10-02 | ≥3.10 | cirq-ionq<1.7 (cirq extra) |
| qiskit | 2.5.2 | 2026-08-13 | ≥3.10 | – |
| pennylane | 0.45.1 | 2026-06-26 | ≥3.11 | – |
| ionq (IonQ SDK) | 0.0.0a15 (alpha) | 2025-12-02 | – | – |
Sources: [PyPI qiskit-ionq](https://pypi.org/project/qiskit-ionq/), [PyPI cirq-ionq](https://pypi.org/project/cirq-ionq/), [PyPI pennylane-ionq](https://pypi.org/project/pennylane-ionq/), [PyPI cudaq](https://pypi.org/project/cudaq/), [PyPI amazon-braket-sdk](https://pypi.org/project/amazon-braket-sdk/), [PyPI qiskit-braket-provider](https://pypi.org/project/qiskit-braket-provider/), [PyPI azure-quantum](https://pypi.org/project/azure-quantum/), [PyPI qbraid](https://pypi.org/project/qbraid/), [PyPI qiskit](https://pypi.org/project/qiskit/), [PyPI pennylane](https://pypi.org/project/pennylane/), [PyPI ionq](https://pypi.org/project/ionq/)

**qiskit-ionq**
- Compatibility:
  - qiskit-ionq ≥1.0 is compatible with Qiskit 2.0; Qiskit 1.x/0.x needs an older qiskit-ionq.
  - qiskit-ionq ≥0.6 uses API v0.4; earlier versions use v0.3.
  - IonQ's guide assumes Python 3.11.
  - Source: [IonQ Docs – Qiskit](https://docs.ionq.com/sdks/qiskit/index)
- Release history:
  - v1.0.0 (2025-08-25): "Qiskit v2"
  - v1.0.3 (2026-06-01): retries on HTTP 429, QASM3 export of native gates
  - v1.1.0 (2026-06-05): "mid-circuit measurement via ionq.qasm3.v1"
  - v1.1.1 (2026-06-05): pins `compilation.service_version v0.4` for OpenQASM 3 jobs
  - Source: [qiskit-ionq releases](https://github.com/qiskit-community/qiskit-ionq/releases)
- Unreleased main-branch commits:
  - 2026-07-16: API-driven backend target / Tempo support
  - 2026-08-18: "Validate circuit qubit count using qubit capacity of the target backend"
  - 2026-08-18: "Remove previous qiskit <2.5.0 limitation (but disallow 2.5.0)"
  - 2026-09-25: "Drop the 4-qubit fallback for unlisted backends"
  - Source: [qiskit-ionq commits](https://github.com/qiskit-community/qiskit-ionq/commits/main)
- Auth: the env var `IONQ_API_KEY` (docs), or `QISKIT_IONQ_API_TOKEN` / `IONQ_API_TOKEN` (provider fallback order), or `IonQProvider("key")` — [PyPI qiskit-ionq](https://pypi.org/project/qiskit-ionq/), [IonQ Docs – Qiskit](https://docs.ionq.com/sdks/qiskit/index)
- Backend names: `"simulator"` / `"ionq_simulator"`, `"qpu.forte-1"` / `"ionq_qpu.forte-1"`, `"qpu.forte-enterprise-1"` — [IonQ Docs – Qiskit](https://docs.ionq.com/sdks/qiskit/index)
- Minimal example (adapted from [IonQ Docs – Qiskit](https://docs.ionq.com/sdks/qiskit/index)):
  ```bash
  pip install qiskit qiskit-ionq
  ```
  ```python
  from qiskit import QuantumCircuit
  from qiskit_ionq import IonQProvider
  provider = IonQProvider()                                  # IONQ_API_KEY
  sim = provider.get_backend("simulator")
  qc = QuantumCircuit(2, name="bell"); qc.h(0); qc.cx(0, 1); qc.measure_all()   # explicit measurement required
  print(sim.run(qc, shots=10000).get_counts())               # ideal
  print(sim.run(qc, shots=10000, noise_model="forte-enterprise-1").get_counts())  # noisy
  qpu = provider.get_backend("qpu.forte-enterprise-1")
  job = qpu.run(qc, shots=1000); print(job.job_id())          # retrieve later: qpu.retrieve_job(id)
  ```
- Multiple circuits go in one job with `backend.run([qc1, qc2])`. Use `dry_run=True` (≥1.0.3; older versions use `extra_query_params={'dry_run': True}`) to predict cost, then read the cost via `GET /v0.4/jobs/{id}/cost` — [IonQ Docs – Qiskit](https://docs.ionq.com/sdks/qiskit/index), [IonQ Docs – Job Cost](https://docs.ionq.com/guides/job-cost-and-usage)
- **Warning:** passing `dry_run=True` to qiskit-ionq <1.0.3 is silently ignored, and the job runs on the QPU and consumes credit — [IonQ Docs – Job Cost](https://docs.ionq.com/guides/job-cost-and-usage)
- Common errors:
  - `IonQCredentialsError`: no key found
  - `IonQAPIError` "Insufficient scope": invalid key
  - "Unable to run jobs on IonQ QPU": no project permission, or the backend is "Out of Plan"
  - Source: [IonQ Docs – Qiskit](https://docs.ionq.com/sdks/qiskit/index)

**cirq-ionq**
- `pip install cirq-ionq` (Python ≥3.11) — [IonQ Docs – Cirq](https://docs.ionq.com/sdks/cirq/index). `cirq_ionq.Service(api_key=..., api_version='v0.4')` defaults to v0.4 — [cirq-ionq service.py](https://github.com/quantumlib/Cirq/blob/main/cirq-ionq/cirq_ionq/service.py)
- Usage:
  - simulator: `service.run(circuit=c, target="simulator", repetitions=1000)`
  - QPU (non-blocking): `job = service.create_job(circuit=c, target="qpu.forte-1", repetitions=1000)`, then `job.results().to_cirq_result()`
  - Source: [IonQ Docs – Cirq](https://docs.ionq.com/sdks/cirq/index)
- Before cirq-ionq v0.15 the decomposition call was `cirq_ionq.decompose_to_device(qc)`; it is now `cirq.optimize_for_target_gateset(..., IonQTargetGateset())` — [IonQ Docs – Cirq](https://docs.ionq.com/sdks/cirq/index)

**pennylane-ionq**
- Install with `pip install pennylane pennylane-ionq`. Devices are `ionq.simulator` and `ionq.qpu`. IonQ's docs now use the `qp` alias and the `@qp.set_shots(100)` decorator — [IonQ Docs – PennyLane](https://docs.ionq.com/sdks/pennylane/index)
- **v0.45.0 breaking change (2026-05-12):** moved to API v0.4. The payload uses `backend` instead of `target`, `type` instead of `format`, and `error_mitigation`/`compilation` nested under `settings`. Also new in v0.45.0: retries/timeouts, plus IsingXX/YY/ZZ support — [pennylane-ionq releases](https://github.com/PennyLaneAI/PennyLane-IonQ/releases)
- **v0.43.0 breaking changes (2025-10-15):** minimum PennyLane 0.43; default `shots` changed from 1024 to `None`; Python 3.10 dropped — [pennylane-ionq releases](https://github.com/PennyLaneAI/PennyLane-IonQ/releases)
- **Gotcha:** in v0.45.0, `QPUDevice` (`ionq.qpu`) has default `backend="aria-1"`, a retired QPU — [pennylane-ionq v0.45.0 device.py](https://github.com/PennyLaneAI/PennyLane-IonQ/blob/v0.45.0/pennylane_ionq/device.py)
- Unreleased 0.46.0-dev: mid-circuit measurement and reset via `qp.measure` (submitted as `ionq.qasm3.v1`), a `memory=True` per-shot kwarg, and native `Toffoli` in the QIS set — [pennylane-ionq CHANGELOG](https://github.com/PennyLaneAI/PennyLane-IonQ/blob/master/CHANGELOG.md)

**NVIDIA CUDA-Q**
- `pip install cudaq`. IonQ support is built in. The key must be in the env var `IONQ_API_KEY` (it cannot be passed in code) — [IonQ Docs – CUDA-Q](https://docs.ionq.com/sdks/cuda-q)
- Targets:
  - ideal simulator: `cudaq.set_target('ionq')`
  - noisy simulator: `cudaq.set_target('ionq', noise='forte-1')`
  - QPU: `cudaq.set_target('ionq', qpu='qpu.forte-1')`, with `cudaq.sample_async(kernel, shots_count=1000)` and `cudaq.AsyncSampleResult(saved_str).get()` to retrieve
  - The kernel function name becomes the job name. The saved async-result file contains the API key.
  - Source: [IonQ Docs – CUDA-Q](https://docs.ionq.com/sdks/cuda-q)

**Amazon Braket**
- Devices: `arn:aws:braket:us-east-1::device/qpu/ionq/Forte-1` and `.../Forte-Enterprise-1`. Native gates need verbatim compilation. The Qiskit-Braket provider is an alternative route — [Braket – IonQ](https://docs.aws.amazon.com/braket/latest/developerguide/braket-qpu-partner-ionq.html), [IonQ Docs – Amazon Braket](https://docs.ionq.com/partners/amazon-braket)
- Debiasing example: `AwsDevice("arn:aws:braket:us-east-1::device/qpu/ionq/Forte-Enterprise-1").run(Circuit().h(0).cnot(0,1), shots=2500, device_parameters={"errorMitigation": Debias()})` — [Braket – Error mitigation on IonQ](https://docs.aws.amazon.com/braket/latest/developerguide/error-mitigation-ionq.html)

**Azure Quantum**
- Target IDs: `ionq.simulator`, `ionq.qpu.aria-1` (still listed), `ionq.qpu.forte-1`, `ionq.qpu.forte-enterprise-1`.
- Data format is `ionq.circuit.v1` under the **QIR Base profile**, so measurement results cannot control program flow.
- Q# programs must return `Result` values.
- Source: [Microsoft Learn – IonQ provider](https://learn.microsoft.com/en-us/azure/quantum/provider-ionq)

**Google Cloud**
- IonQ hardware has been on Google Cloud Marketplace since 2021-06-17 — [IonQ IR, 2021-06-17](https://investors.ionq.com/news/news-details/2021/IonQs-Leading-Trapped-Ion-Quantum-Hardware-Now-Available-on-Google-Cloud-Marketplace/default.aspx). IonQ's 2026 docs still mention access "through Google Cloud Marketplace" — [IonQ Docs – noise models](https://docs.ionq.com/features/simulation-with-noise-models)

**qBraid**
- IonQ maintains qBraid getting-started and native-gate guides, and qBraid Lab is suggested as a hosted CUDA-Q environment — [IonQ docs index](https://docs.ionq.com/llms.txt), [IonQ Docs – CUDA-Q](https://docs.ionq.com/sdks/cuda-q)

**REST API v0.4**
- Base `https://api.ionq.co/v0.4`; header `Authorization: apiKey <key>`.
- Key endpoints:
  - `POST /jobs`
  - `GET /jobs/{id}`
  - `GET /jobs/{id}/results/probabilities` (replaces v0.3 `/results`)
  - `GET /jobs/{id}/cost`
  - `GET /jobs/estimate`
  - `GET /backends`, `GET /backends/{b}/characterizations`
  - sessions endpoints
- v0.4 breaking changes:
  - result URL `results.probabilities.url`
  - characterization endpoints nested under `/backends/`
  - ISO dates instead of Unix timestamps
  - job names restricted to `[a-zA-Z0-9 _-]`
  - new `output`, `results`, and `stats` fields (`stats.gate_counts`, `kwh`)
- Sources: [IonQ – Migrating to API v0.4](https://docs.ionq.com/api-reference/v0.4/migration-from-v0.3), [IonQ Docs – Direct API submission](https://docs.ionq.com/guides/direct-api-submission), [IonQ Docs – Job cost](https://docs.ionq.com/guides/job-cost-and-usage)
- Health check: `https://api.ionq.co/v0.4/health` should return `{"status": "pass"}` — [qiskit-ionq README](https://github.com/qiskit-community/qiskit-ionq/blob/main/README.md)
- **Mid-circuit measurement and dynamic circuits:**
  - MCM uses `ionq.qasm3.v1` and is supported "on some targets", including the simulator.
  - Unsupported targets fail with `UnsupportedFeature` before execution, at no cost.
  - Single-qubit `reset q[j];` is allowed.
  - **Dynamic circuits (if/else/while/for/switch) are not supported on any target, including the simulator, and are "not planned for any live system".**
  - Source: [IonQ API v0.4 – OpenQASM 3](https://docs.ionq.com/api-reference/v0.4/openqasm3)
  - qiskit-ionq says MCM jobs "Today … execute on the simulator (mid-circuit-measurement QPU support is rolling out)". Per-register results need a noisy simulator or a QPU — [qiskit-ionq README (main)](https://github.com/qiskit-community/qiskit-ionq/blob/main/README.md)
- **IonQ SDK / Hosted Hybrid:**
  - `pip install 'ionq[all]'`, with `from ionq.client import Client; from ionq import Backend`.
  - Hosted Hybrid "Quantum Functions" (Hamiltonian Energy, QCQP) plus "Optimizations" run classical loops server-side.
  - It is "in a limited preview and only available to customers with an active contract".
  - Sources: [IonQ Docs – Hosted Hybrid Service](https://docs.ionq.com/guides/hosted-hybrid-service), [PyPI ionq](https://pypi.org/project/ionq/)
- A conflicting search snippet claimed API v0.4 is "beta … only available to select customers". The SDKs default to v0.4 (cirq-ionq `api_version='v0.4'`, qiskit-ionq ≥0.6, pennylane-ionq 0.45), so that snippet is probably stale — [IonQ API v0.4 intro](https://docs.ionq.com/api-reference/v0.4/introduction), [cirq-ionq service.py](https://github.com/quantumlib/Cirq/blob/main/cirq-ionq/cirq_ionq/service.py)

### Inferences
- **Recommended environment:**
  - Python 3.11/3.12 with `qiskit>=2.0,!=2.5.0` + `qiskit-ionq==1.1.1`, `cirq-ionq==1.7.0`, `pennylane-ionq==0.45.0`, and `cudaq`.
  - Put `azure-quantum[cirq]` or `qbraid[cirq]` in a **separate venv**, because their `cirq-ionq<1.7` pin conflicts with cirq-ionq 1.7.0.
  - The "disallow 2.5.0" commit suggests avoiding exactly Qiskit 2.5.0 (2.5.2 is current).
- **PennyLane users must pass `backend="forte-1"` or `backend="forte-enterprise-1"`** to `qp.device("ionq.qpu", ...)`. Otherwise jobs target the retired `aria-1`.
- Because dynamic circuits are explicitly unplanned, any hackathon idea that needs feed-forward (teleportation with classical correction, adaptive VQE, repeat-until-success) must use deferred measurement or classical post-processing. MCM plus reset (qubit reuse) is the most IonQ supports, and only on the simulator, with QPU support "rolling out".

### Gaps
- No released qiskit-ionq version yet includes the `debiasing=` / `aggregation=` / Tempo changes on main. The release date of the next version (1.2?) is unknown.
- Which QPUs (if any) accepted MCM jobs as of 2026-10-07 is undocumented.
- No current Google Cloud Marketplace IonQ listing details (which QPUs, pricing) were found for 2026.
- CUDA-Q's own IonQ backend page URL returned 404; the CUDA-Q details come from IonQ's docs only.

---

## Q6. What does running on IonQ cost, what credit programs exist, and what is typical for hackathons?

### Takeaway
QPU time is expensive and has per-circuit minimums:
- **Azure:** Forte / Forte Enterprise charge $0.0001645 per 1Q-gate-shot and $0.001121 per 2Q-gate-shot. The minimum is **$168.195 per circuit with debiasing** and **$25.79 without**.
- **Braket:** Forte is **$0.30/task + $0.08/shot**, with reservations at **$7,000/hour**.
- **IonQ direct:** priced per organization contract. `GET /v0.4/jobs/estimate` and dry runs give circuit-specific estimates.
- **Simulators** (ideal and noisy) are free.

IonQ's Research Credits program offers up to **$10,000** per accepted academic proposal, but I found no evidence of a 2026 cohort and no public hackathon credit norms.

### Cited Findings
- **Azure Quantum** (page updated 2026-04-23):
  - Aria 1: $0.000220 per 1Q-gate-shot and $0.000975 per 2Q-gate-shot; minimum $97.50 with error mitigation, $12.4166 without.
  - Forte 1 and Forte Enterprise 1: $0.0001645 and $0.001121; minimum **$168.195 (EM on, default)** and **$25.7899 (EM off)**.
  - Aria-Forte subscription: $25,000/month.
  - Simulator: free.
  - Multi-controlled gates are billed as 6(N−2) 2Q gates.
  - Source: [Microsoft Learn – Azure Quantum pricing](https://learn.microsoft.com/en-us/azure/quantum/pricing)
- **Amazon Braket:**
  - IonQ Forte: per-task $0.30, per-shot $0.08, reservation $7,000/hour.
  - IonQ error-mitigation tasks need ≥2,500 shots; tasks with fewer fail and are not charged.
  - The free tier covers only 1 hour/month of simulator time for 12 months, not QPUs.
  - Source: [AWS – Braket pricing](https://aws.amazon.com/braket/pricing/)
- **IonQ direct:**
  - Credit is reserved at submission and charged at run; it is released if the job fails or is canceled.
  - Cost is estimated from 1Q/2Q gate counts and shots via `/v0.4/jobs/estimate`.
  - Example: forte-enterprise-1, 25 qubits, 1,000 shots, 400 1Q, 150 2Q, debiasing on → **$233.75** "at IonQ's standard rates".
  - A dry-run cost example returned $168.2.
  - Minimum per-circuit cost applies, and it is higher with debiasing.
  - `QuotaExhaustedError` means the project budget is exceeded. Reserved credit for queued jobs counts against the budget.
  - Source: [IonQ Docs – Job Cost and Usage](https://docs.ionq.com/guides/job-cost-and-usage)
- IonQ's guidance: keep debiasing on for medium/large circuits (no cost impact), and turn it off for "very shallow circuits or small test jobs" to conserve credit — [IonQ Docs – Debiasing](https://docs.ionq.com/features/error-mitigation-debiasing)
- **Research Credits Program:**
  - "Up to $10,000 in free credits … to qualified academics".
  - Proposal of 500 words or fewer, from an accredited academic or government research institution in served countries.
  - Uses a resource estimator at ionq.com/programs/research-credits/resource-estimator.
  - Rolling submissions in periodic cohorts. The last explicit deadline I saw was 2023-12-31, and no 2026 cohort dates were found.
  - Sources: [IonQ – Research Credits](https://ionq.com/programs/research-credits), [IonQ – Call for proposals](https://ionq.com/programs/research-credits/call-for-proposals), [IonQ – Application](https://ionq.com/programs/research-credits/application), [IonQ Docs – Debiasing (estimator link)](https://docs.ionq.com/features/error-mitigation-debiasing)
- Projects without plan access see QPUs marked "Out of Plan" in the console. Org admins request access from sales@ionq.co — [IonQ Docs – Qiskit](https://docs.ionq.com/sdks/qiskit/index)

### Inferences
- **Worked cost examples (computed from the cited rates):**
  - Braket, Bell circuit, 1,000 shots, no EM: $0.30 + 1,000 × $0.08 = **$80.30**.
  - Braket, debiased at the 2,500-shot minimum: **$200.30**.
  - Azure Forte, 20-qubit circuit with 200 1Q and 100 2Q gates at 1,000 shots: 200,000 × 0.0001645 + 100,000 × 0.001121 = $32.90 + $112.10 = **$145.00**. That is above the $25.79 no-EM minimum, so about $145. With EM on, the $168.195 minimum applies.
  - Azure's formula is written AQT = m + …, which reads as additive, but the table calls m a "minimum price per program execution". The cited example of $168.2 for a dry run supports the "minimum" reading.
  - Fewer shots matter far more on Braket (per-shot pricing). Fewer 2Q gates matter far more on Azure and IonQ direct (2Q gate-shots cost about 6.8× 1Q gate-shots on Forte).
- Hackathon teams will likely get a fixed IonQ credit allocation per team, enough for only a handful of QPU circuits (each costing roughly $25–$170 or more). Run everything on the free simulator first, use `dry_run` and `/jobs/estimate`, and reserve the QPU for one or two headline experiments.

### Gaps
- Braket per-shot pricing for **Forte-Enterprise-1** specifically: the pricing page lists only "IonQ Forte".
- IonQ direct list prices: contract-specific, not public.
- Typical IonQ credit amounts at hackathons (e.g., Qollab, iQuHACK, MIT/Yale events): no public source found.
- Whether the Research Credits program is active in 2026: no 2026 cohort information found.

---

## Q7. What 2025–2026 company developments (acquisitions, roadmap, new hardware and software) matter for participants?

### Takeaway
IonQ spent 2025–2026 buying its way into networking, sensing, space, and chip manufacturing. Completed deals include Qubitekk, ID Quantique (controlling stake), Lightsynq, Capella, **Oxford Ionics ($1.075B, closed 2025-09-17)**, Vector Atomic, Skyloom, and **SkyWater Technology (closed 2026-07-31)**. The hardware roadmap moved to Oxford Ionics' **Electronic Qubit Control (EQC)** chips:
- 99.99% 2Q fidelity on a lab prototype (2025-10-21)
- **Superion 256**: deliveries in 2027
- Superion 10K: a 2027 fault-tolerance demo and a 2028 commercial target

Tempo (100 qubits, #AQ 64) is being sold and deployed on-premises (for example KISTI), but is not on public clouds.

### Cited Findings
- **Qubitekk:** completion announced 2025-01-06. IonQ's FY2025 10-K dates the Qubitekk Federal purchase 2024-12-27, at about $22.1M — [IonQ IR, 2025-01-06](https://investors.ionq.com/news/news-details/2025/IonQ-Completes-Acquisition-of-Qubitekk-Solidifying-Leadership-in-Quantum-Networking/default.aspx), [IonQ 10-K FY2025](https://www.sec.gov/Archives/edgar/data/1824920/000119312526071562/ionq-20251231.htm)
- **ID Quantique** (controlling stake, 2025-05-06), **Lightsynq** (photonic interconnects / quantum memory, 2025-06-03), and **Capella Space** (SAR satellites, 2025-07-15) — completion dates as summarized from IonQ's Q3 2025 10-Q search result: [IonQ 10-Q Q3 2025](https://www.sec.gov/Archives/edgar/data/1824920/000119312525266942/ionq-20250930.htm)
- **Oxford Ionics:**
  - Announced 2025-06-09 at $1.075B ($1.065B in stock plus $10M cash) — [Converge Digest](https://convergedigest.com/ionq-to-acquire-oxford-ionics-in-1-075-billion-deal/)
  - Completed 2025-09-17 — [IonQ IR, 2025-09-17](https://investors.ionq.com/news/news-details/2025/IonQ-Completes-Acquisition-of-Oxford-Ionics-Rapidly-Accelerating-Its-Quantum-Computing-Roadmap/default.aspx)
- **Vector Atomic** (quantum sensing):
  - Completion announced 2025-10-07 — [IonQ IR](https://investors.ionq.com/news/news-details/2025/IonQ-Completes-Acquisition-of-Vector-Atomic-the-Global-Leader-in-Advanced-Quantum-Sensing/default.aspx)
  - The annual report gives an acquisition date of 2025-10-02 and about $181.5M in stock, and says IonQ completed six acquisitions in 2025 — [IonQ ARS FY2025](https://www.sec.gov/Archives/edgar/data/0001824920/000119312526197584/d938156dars.pdf)
- **SkyWater Technology:**
  - Agreed in late January 2026 at $35/share (about $1.8B equity value).
  - Final regulatory approval 2026-07-28; completed 2026-07-31.
  - IonQ raised its 2026 revenue outlook to $450–460M.
  - Source: [IonQ IR – 2026 outlook after SkyWater](https://investors.ionq.com/news/news-details/2026/IonQ-Announces-Increased-Full-Year-2026-Financial-Outlook-Following-SkyWater-Acquisition/default.aspx)
- **Skyloom Global** (free-space optical comms): completed 2026-01-28. **Seed Innovations** agreed, terms undisclosed. Both come from search summaries of IonQ FY2026 8-K exhibits — [IonQ 8-K exhibit (FY2026)](https://www.sec.gov/Archives/edgar/data/1824920/000119312526032000/ionq-ex99_1.htm)
- **#AQ 64** on Tempo, 2025-09-25. IonQ claims the record and benchmark gains vs IBM of 35% (QAOA), 74% (QFT), and 182% (FAA) — [IonQ news](https://www.ionq.com/news/ionq-achieves-record-breaking-quantum-performance-milestone-of-aq-64)
- **99.99% two-qubit gate fidelity:**
  - Technical papers released 2025-10-21, on an EQC prototype in R&D labs, not a commercial system.
  - It beats the previous 99.97% record (Oxford Ionics, 2024).
  - The result is not independently verified.
  - Source: [The Quantum Insider, 2025-10-21](https://thequantuminsider.com/2025/10/21/ionq-achieves-99-99-two-qubit-gate-performance/)
- **Investor Day (2026-09-08):**
  - **Superion 256**: EQC, fabricated at SkyWater, ions trapped in prototypes, six tapeouts in H1 2026, deliveries from 2027. The University of Cambridge bought the first unit in Q1 2026.
  - **Superion 10K**: cryo-CMOS, aimed at the "Walking Cat" fault-tolerant architecture published April 2026. Fault-tolerance lab demo targeted for 2027, commercial system for 2028.
  - A photonic interconnect demo between commercial systems happened in April 2026.
  - A secp256k1 resource estimate needs 19,397 physical / 1,457 logical qubits.
  - No Superion fidelities were disclosed.
  - Source: [The Quantum Insider, 2026-09-08](https://thequantuminsider.com/2026/09/08/ionq-uses-investor-day-to-detail-superion-roadmap-skywater-strategy-and-quantum-security-plans/)
- **Longer-range targets:**
  - IonQ states a path to 2 million physical qubits and 80,000 logical qubits by 2030 — [arXiv 2604.04761 (2026)](https://arxiv.org/html/2604.04761v1)
  - The SkyWater announcement cites 200,000-qubit QPUs and 8,000 logical qubits, with functional testing from 2028 — [IonQ IR – SkyWater outlook](https://investors.ionq.com/news/news-details/2026/IonQ-Announces-Increased-Full-Year-2026-Financial-Outlook-Following-SkyWater-Acquisition/default.aspx)
- **Q2 2026 revenue:** $80.1M (+287% YoY). Growth was credited to global Tempo deployments, and QEC progress was reported on a Tempo engineering test system — [Futurum, 2026-08-07](https://futurumgroup.com/insights/ionq-q2-fy-2026-tempo-quantum-computers-drive-growth-ahead-of-skywater-integration/)
- **Software:**
  - An alpha `ionq` Python SDK (0.0.0a15, 2025-12-02).
  - Hosted Hybrid Service (Quantum Functions / Optimizations, limited preview).
  - Fire Opal QAOA solver guide, API v0.4 sessions.
  - Sources: [PyPI ionq](https://pypi.org/project/ionq/), [IonQ Docs – Hosted Hybrid](https://docs.ionq.com/guides/hosted-hybrid-service), [IonQ docs index](https://docs.ionq.com/llms.txt)

### Inferences
- For participants, the developments that matter technically are:
  - Hardware has consolidated on **Forte-class (ZZ native)**, so legacy Aria/MS tutorials are outdated.
  - **Tempo** is a 100-qubit, "many-to-many" system with MCM. A `qpu.tempo-1` backend is already wired into the SDK and could appear on cloud by the "Late 2026" date.
  - The EQC/Superion roadmap makes a good narrative for scalability slides, but it does not affect what can be run in Oct 2026.
- The many acquisitions (networking, sensing, QKD) suggest IonQ judges may value quantum-networking or quantum-security angles alongside computing.

### Gaps
- Exact Tempo cloud-launch timing, and whether hackathon participants could get Tempo time.
- Exact closing dates for ID Quantique, Lightsynq, and Capella from primary press releases (I relied on a search summary of the 10-Q).
- Details of "Seed Innovations" and the Anduril MOU.

---

## Q8. What published IonQ application work might impress judges (chemistry, QML, optimization, finance, engineering)?

### Takeaway
IonQ's flagship application results are hybrid quantum-classical workflows on Forte/Aria, and almost all are self-reported:
- **AstraZeneca/AWS/NVIDIA** chemistry: >20× time-to-solution speedup, Suzuki-Miyaura reaction, June 2025
- **Ansys** LS-DYNA blood-pump simulation: "up to 12%" faster than classical, March 2025, with disputed hardware scope
- **Airbus** aircraft loading: multi-angle QAOA reaching optimal solutions for 12–28-qubit instances on Aria/Forte, April 2025
- **Hyundai** quantum image classification and object detection, 2022–2023
- 2025 **QML** work: quantum-layer LLM fine-tuning and a quantum GAN for steel microstructures

### Cited Findings
- **AstraZeneca/AWS/NVIDIA** (2025-06-09):
  - Hybrid workflow on IonQ Forte with CUDA-Q, Braket, and AWS ParallelCluster (H200 GPUs).
  - Simulated a Suzuki-Miyaura reaction, "the most complex chemical simulation run on IonQ hardware to date".
  - "More than a 20x speedup in time-to-solution compared to prior benchmarks" — that is, against earlier IonQ-stack implementations, not a purely classical baseline.
  - Source: [IonQ IR, 2025-06-09](https://investors.ionq.com/news/news-details/2025/IonQ-Speeds-Quantum-Accelerated-Drug-Development-Application-With-AstraZeneca-AWS-and-NVIDIA/default.aspx)
- **Ansys** (2025-03-20):
  - IonQ Forte assisted a graph-optimization subroutine in LS-DYNA for blood-pump dynamics, on a 2.6M-vertex / 40M-edge model.
  - "Up to 12 percent" faster than classical — [IonQ news](https://www.ionq.com/news/ionq-and-ansys-achieve-major-quantum-computing-milestone-demonstrating)
  - The Quantum Insider reports the full-scale hybrid result was **simulated**, with Forte validating only smaller instances — [The Quantum Insider, 2025-03-20](https://thequantuminsider.com/2025/03/20/ionqs-devices-boost-ansys-simulations-achieving-up-to-12-faster-processing-over-classical-computers/)
- **Airbus** ([arXiv:2504.01567, April 2025](https://arxiv.org/abs/2504.01567)):
  - Multi-angle QAOA designed to use fewer 2Q gates.
  - Run on Aria and Forte, obtaining optimal solutions for all instances from 12 to 28 qubits.
  - The 12-qubit Aria run (4 containers × 3 slots, 1,000 shots, COBYLA) reached about 70% probability of the optimal solution.
- **Hyundai:**
  - Road-sign classification (43 types), expanding to 3D object detection, announced 2022-04-19 — [The Quantum Insider](https://thequantuminsider.com/2022/04/19/ionq-and-hyundai-motor-expand-partnership-to-study-using-quantum-computers-for-object-detection)
  - APS March 2023 abstract: a hybrid QCNN trained on up to 8 qubits, with inference on 16 qubits across up to 10 classes — [APS abstract](https://meetings-archive.aps.org/mar/2023/m64/3)
- **QML / AI** (2025-05-01):
  - A parameterized quantum circuit layer added to an open-source LLM for sentiment fine-tuning, reported to beat classical baselines of similar parameter count, with projected energy advantages beyond 46 qubits.
  - A quantum GAN for synthetic steel-microstructure images, rated higher quality in up to 70% of comparisons, done with an automaker.
  - Source: [IonQ news](https://ionq.com/news/ionq-demonstrates-quantum-enhanced-applications-advancing-ai)
- **Tempo application claims** (2025-09-25): #AQ 64 tied to grid distribution, drug discovery, engineering simulation, supply chain, and fraud detection, plus the QAOA/QFT/FAA benchmark gains vs IBM — [IonQ news](https://www.ionq.com/news/ionq-achieves-record-breaking-quantum-performance-milestone-of-aq-64)
- **Investor Day 2026-09-08:** application work in computational engineering, logistics, pharma, and image-change detection; oncology and personalized medicine are named priorities — [The Quantum Insider](https://thequantuminsider.com/2026/09/08/ionq-uses-investor-day-to-detail-superion-roadmap-skywater-strategy-and-quantum-security-plans/)

### Inferences
- Hackathon projects that mirror these patterns line up with IonQ's own narrative, which judges may reward:
  - **Hybrid VQE/chemistry with CUDA-Q + IonQ**
  - **Multi-angle QAOA with low 2Q count** (logistics, loading)
  - **Quantum layers in classical ML**
- Present honest baselines, because IonQ's own claims are often relative to prior quantum implementations or partly simulated.
- The Airbus paper's emphasis on reducing 2Q gate count matches the Q2 best practices (ZZ-native interactions on Forte) and is a useful template.

### Gaps
- No finance-specific IonQ application result from 2025–2026 was found (searched only lightly).
- Accuracy figures for the LLM fine-tuning work and the underlying papers were not retrieved.
- No independent replication of any IonQ application claim was found.
