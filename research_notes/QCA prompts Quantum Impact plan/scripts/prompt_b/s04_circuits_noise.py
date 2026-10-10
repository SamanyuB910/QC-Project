"""Step 4: real Qiskit circuits for the frozen QAOA schedules; cross-check against the numpy simulator;
2Q-gate counts all-to-all (rzz/rx/rz) vs heavy-hex; Aer depolarizing noise at IonQ forte-1 noise-model rates
(1q 2.67e-4, 2q 4.95e-3, one depolarizing channel after every gate, as in IonQ's simulator docs)."""
import sys, json, time
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import XXPlusYYGate, RYGate
from qiskit.quantum_info import Statevector
from qiskit.transpiler import CouplingMap
from qiskit.providers.fake_provider import GenericBackendV2
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error
from common import *
from qsim import *

LAM = 0.2
X, y, _ = load_data()
r, _ = relevance(X, y); C = redundancy(X)


def ising_terms(E_lin, E_quad, const=0.0):
    """x-QUBO  sum_i h_i x_i + sum_{i<j} J_ij x_i x_j  ->  Ising coefficients a_i Z_i + b_ij Z_i Z_j (+const)."""
    a = np.zeros(N); b = {}
    for i in range(N):
        a[i] += -E_lin[i] / 2
    for (i, j), J in E_quad.items():
        a[i] += -J / 4; a[j] += -J / 4
        b[(i, j)] = b.get((i, j), 0) + J / 4
    return a, b


def qubo_coeffs(P):
    h = -r.copy(); Jq = {}
    for i in range(N):
        for j in range(i + 1, N):
            Jq[(i, j)] = LAM * C[i, j]
    if P:
        # P (sum x - k)^2 = P[(1-2k) sum x + 2 sum_{i<j} x_i x_j + k^2]
        h += P * (1 - 2 * K)
        for key in Jq:
            Jq[key] += 2 * P
    return h, Jq


def cost_layer(qc, a, b, gamma, scale):
    # exp(-i gamma E/scale): RZ(theta) = exp(-i theta Z/2), RZZ(theta) = exp(-i theta ZZ/2)
    for i in range(N):
        if abs(a[i]) > 1e-12:
            qc.rz(2 * gamma * a[i] / scale, i)
    for (i, j), v in b.items():
        if abs(v) > 1e-12:
            qc.rzz(2 * gamma * v / scale, i, j)


def scs(qc, qubits, l):
    """Split-and-cyclic-shift block of Baertschi & Eidenbenz (deterministic Dicke state preparation)."""
    n = len(qubits)
    q = qubits
    qc.cx(q[n - 2], q[n - 1])
    qc.cry(2 * np.arccos(np.sqrt(1 / n)), q[n - 1], q[n - 2])
    qc.cx(q[n - 2], q[n - 1])
    for i in range(2, l + 1):
        qc.cx(q[n - i - 1], q[n - 1])
        qc.append(RYGate(2 * np.arccos(np.sqrt(i / n))).control(2), [q[n - 1], q[n - i], q[n - i - 1]])
        qc.cx(q[n - i - 1], q[n - 1])


def dicke_circuit(n, k):
    qc = QuantumCircuit(n)
    for i in range(n - k, n):
        qc.x(i)
    for m in range(n, k, -1):
        scs(qc, list(range(m)), k)
    for m in range(k, 1, -1):
        scs(qc, list(range(m)), m - 1)
    return qc


def build(method, gammas, betas, init_state=None, measure=True, init_mode="dicke"):
    qc = QuantumCircuit(N)
    if method.startswith("penalty"):
        P = (0.3 if "0.3" in method else 1.0) * float(np.max(np.abs(r) + LAM * C.sum(1)))
        inst = Inst(r, C, LAM, P)
        scale = inst.E.std()
        h, Jq = qubo_coeffs(P)
        a, b = ising_terms(h, Jq)
        qc.h(range(N))
        for g, bt in zip(gammas, betas):
            cost_layer(qc, a, b, g, scale)
            for q in range(N):
                qc.rx(-2 * bt, q)
    else:
        inst = Inst(r, C, LAM, 0.0)
        scale = inst.ff.std()
        h, Jq = qubo_coeffs(0.0)
        a, b = ising_terms(h, Jq)
        if "dicke" in method and init_mode == "product":
            # product RY start with P(1)=k/n on every qubit: its HW=k component IS the Dicke state, and cost+XY layers
            # never mix Hamming-weight sectors, so post-selecting HW=k reproduces Dicke-start QAOA exactly (0 two-qubit gates)
            th = 2 * np.arcsin(np.sqrt(K / N))
            for q in range(N):
                qc.ry(th, q)
        elif "dicke" in method:
            qc.compose(dicke_circuit(N, K), inplace=True)
        else:
            for i in range(N):
                if (init_state >> i) & 1:
                    qc.x(i)
        pairs = ring_pairs() if "ring" in method else complete_pairs()
        for g, bt in zip(gammas, betas):
            cost_layer(qc, a, b, g, scale)
            for (i, j) in pairs:
                qc.append(XXPlusYYGate(-2 * bt), [i, j])
    if measure:
        qc.measure_all()
    return qc, inst


def count2q(qc):
    ops = qc.count_ops()
    return sum(v for k_, v in ops.items() if k_ in ("rzz", "cx", "cz", "ecr", "rxx", "ryy", "swap", "ms")), dict(ops), qc.depth()


def load_angles(method, key):
    for fn in [f"s03_qaoa_lam{LAM}_{method}_subsample.json", f"s03_qaoa_lam{LAM}_{method}.json"]:
        p = os.path.join(OUT, fn)
        if os.path.exists(p):
            d = json.load(open(p))
            row = d["methods"][method][key]
            return np.array(row["gammas"]), np.array(row["betas"]), row
    return None


heavy = GenericBackendV2(num_qubits=57, coupling_map=CouplingMap.from_heavy_hex(5), basis_gates=["cz", "rz", "sx", "x"], seed=1)
out = {}
# 1) verify the Dicke circuit
dq = dicke_circuit(N, K)
sv = Statevector(dq).probabilities()
print("Dicke check: mass on HW=5 =", sv[FEAS_IDX].sum().round(6), " max dev from uniform =", np.abs(sv[FEAS_IDX] - 1 / 1287).max())
d_a2a = transpile(dq, basis_gates=["rzz", "rx", "rz"], optimization_level=2, seed_transpiler=1)
print("Dicke(13,5) prep: 2Q (rzz) all-to-all =", count2q(d_a2a)[0], " original ops", dq.count_ops())
out["dicke_prep_2q_all2all"] = count2q(d_a2a)[0]

noise = NoiseModel()
noise.add_all_qubit_quantum_error(depolarizing_error(2.67e-4, 1), ["rx", "rz"])
noise.add_all_qubit_quantum_error(depolarizing_error(4.95e-3, 2), ["rzz"])
sim_noisy = AerSimulator(noise_model=noise, method="statevector", seed_simulator=11)
SHOTS = int(sys.argv[1]) if len(sys.argv) > 1 else 4000

configs = [("penalty_X_P1xsafe", None, "-", ["E_p1", "E_p2"]),
           ("XY_ring_dicke", None, "product", ["Popt_p1", "Popt_p2"]),
           ("XY_complete_dicke", None, "product", ["Popt_p1", "Popt_p2"]),
           ("XY_complete_dicke", None, "dicke", ["Popt_p1"])]
for method, init_state, init_mode, keys in configs:
    for key in keys:
        ang = load_angles(method, key)
        if ang is None:
            print("no angles yet for", method, key); continue
        g, b, row = ang
        qc, inst = build(method, g, b, init_state, init_mode=init_mode)
        # cross-check: circuit statevector vs numpy simulator
        qc_nm = qc.remove_final_measurements(inplace=False)
        p_circ = Statevector(qc_nm).probabilities()
        if method.startswith("penalty"):
            p_np = qaoa_x(normalise(inst.E), g, b)
        else:
            maps = RING_MAPS if "ring" in method else COMPLETE_MAPS
            v0 = dicke_init() if "dicke" in method else basis_init(init_state)
            pf = qaoa_xy(normalise(inst.ff), g, b, maps, v0); p_np = np.zeros(2 ** N); p_np[FEAS_IDX] = pf
        if init_mode == "product":  # compare the HW=5-conditional distribution with the Dicke-start simulator
            pc = np.zeros(2 ** N); pc[FEAS_IDX] = p_circ[FEAS_IDX]; p_hw5 = pc.sum(); p_circ = pc / p_hw5
        else:
            p_hw5 = p_circ[FEAS_IDX].sum()
        tvd = 0.5 * np.abs(p_circ - p_np).sum()
        a2a = transpile(qc, basis_gates=["rzz", "rx", "rz"], optimization_level=2, seed_transpiler=1)
        n2_a2a, ops_a2a, depth_a2a = count2q(a2a)
        hh = min((transpile(qc, backend=heavy, optimization_level=3, seed_transpiler=s) for s in range(3)), key=lambda c: count2q(c)[0])
        n2_hh, ops_hh, depth_hh = count2q(hh)
        # noisy simulation of the all-to-all circuit
        t = time.time()
        counts = sim_noisy.run(a2a, shots=SHOTS).result().get_counts()
        dt = time.time() - t
        tot = sum(counts.values())
        hits = sum(c for bs, c in counts.items() if int(bs.replace(" ", ""), 2) == inst.opt)
        feas = sum(c for bs, c in counts.items() if bin(int(bs.replace(" ", ""), 2)).count("1") == K)
        F_proxy = (1 - 4.95e-3) ** n2_a2a * (1 - 2.67e-4) ** sum(v for k_, v in ops_a2a.items() if k_ in ("rx", "rz"))
        ideal = row["full"]["P_opt"]
        res = {"tvd_circuit_vs_numpy": tvd, "2q_all2all": n2_a2a, "depth_all2all": depth_a2a, "ops_all2all": ops_a2a,
               "2q_heavyhex": n2_hh, "depth_heavyhex": depth_hh, "ideal_P_opt": ideal, "ideal_P_feas": row["full"]["P_feas"],
               "noisy_P_opt": hits / tot, "noisy_P_opt_ci": wilson(hits, tot), "noisy_P_feas": feas / tot,
               "noisy_P_opt_given_feas": hits / max(feas, 1), "fidelity_proxy": F_proxy, "shots": tot, "aer_seconds": dt,
               "init_mode": init_mode, "ideal_P_HW5_raw": p_hw5, "ideal_P_opt_per_raw_shot": ideal * (p_hw5 if init_mode == "product" else 1.0),
               "noisy_P_opt_given_feas_ci": wilson(hits, max(feas, 1))}
        out[f"{method}_{init_mode}_{key}"] = res
        print(f"{method:20s} init={init_mode:7s} {key}: P(HW5) ideal={p_hw5:.3f} TVD(circ,numpy)={tvd:.2e} | 2Q all-to-all={n2_a2a} (depth {depth_a2a}) heavy-hex={n2_hh} (depth {depth_hh}) "
              f"| ideal P(opt)={ideal:.4f} noisy P(opt)={hits/tot:.4f} [{res['noisy_P_opt_ci'][0]:.4f},{res['noisy_P_opt_ci'][1]:.4f}] "
              f"P(feas) noisy={feas/tot:.3f} P(opt|HW=5) noisy={hits/max(feas,1):.4f} {res['noisy_P_opt_given_feas_ci']} F~{F_proxy:.2f} ({dt:.1f}s/{tot} shots)", flush=True)
save_json("s04_circuits_noise.json", out)
