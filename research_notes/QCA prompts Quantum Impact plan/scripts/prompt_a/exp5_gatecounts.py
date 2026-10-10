"""Experiment 5: two-qubit gate counts of the ZZ feature map (full vs linear entanglement) for
U(x) (PQK / projected circuit) and the fidelity-test circuit U(x') ^dagger U(x),
transpiled to (a) an IonQ-like all-to-all target with native RZZ (ZZ(theta)) and
(b) an IBM heavy-hex coupling map (distance-5, 57 qubits) with CZ basis.

Key identity: CX(i,j) P(l)_j CX(i,j) == exp(i l/2) RZZ(l) on (i,j), so each ZZ term is ONE native ZZ on IonQ.
"""
import json, numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import zz_feature_map
from qiskit.transpiler import CouplingMap
from qiskit.quantum_info import Operator

def zz_native(x, reps=2, ent="full"):
    """IonQ-native-friendly construction: H, P(2x_i), RZZ(2(pi-x_i)(pi-x_j)). Same unitary as zz_feature_map up to global phase."""
    n = len(x)
    pairs = [(i, i + 1) for i in range(n - 1)] if ent == "linear" else [(i, j) for i in range(n) for j in range(i + 1, n)]
    qc = QuantumCircuit(n)
    for _ in range(reps):
        qc.h(range(n))
        for i in range(n):
            qc.p(2 * x[i], i)
        for i, j in pairs:
            qc.rzz(2 * (np.pi - x[i]) * (np.pi - x[j]), i, j)
    return qc

def count2q(qc):
    return sum(1 for ins in qc.data if ins.operation.num_qubits == 2)

def count1q_nonvirtual(qc):
    return sum(1 for ins in qc.data if ins.operation.num_qubits == 1 and ins.operation.name not in ("rz", "measure", "barrier", "p"))

rng = np.random.default_rng(0)
# sanity: native construction equals qiskit zz_feature_map up to global phase
x = rng.uniform(0, 1, 4)
U1 = Operator(zz_feature_map(4, reps=2, entanglement="full").assign_parameters(x))
U2 = Operator(zz_native(x, 2, "full"))
ov = abs(np.trace(U1.data.conj().T @ U2.data)) / 16
print("native == zz_feature_map (|Tr U1^dag U2|/d):", ov)

hh = CouplingMap.from_heavy_hex(5)
out = {"native_equivalence_overlap": float(ov), "heavy_hex_qubits": hh.size()}
for n in [4, 8, 12, 16]:
    for ent in ["linear", "full"]:
        x = rng.uniform(0.05, 0.3, n); x2 = rng.uniform(0.05, 0.3, n)
        U = zz_native(x, 2, ent)
        Fc = U.compose(zz_native(x2, 2, ent).inverse())
        row = {"ZZ_terms_per_U": count2q(U)}
        for name, circ in [("U", U), ("fid", Fc)]:
            ion = transpile(circ, basis_gates=["rz", "sx", "x", "rzz"], optimization_level=3, seed_transpiler=1)
            row[f"{name}_ionq_2q"] = count2q(ion)
            row[f"{name}_ionq_1q_nonvirtual"] = count1q_nonvirtual(ion)
            row[f"{name}_ionq_total"] = len(ion.data)
            cxc = transpile(circ, basis_gates=["rz", "sx", "x", "cx"], optimization_level=3, seed_transpiler=1)
            row[f"{name}_alltoall_cx"] = count2q(cxc)
            best = None
            for s in range(3):
                h = transpile(circ, coupling_map=hh, basis_gates=["rz", "sx", "x", "cz"], optimization_level=3, seed_transpiler=s)
                c2, d = count2q(h), h.depth(lambda ins: ins.operation.num_qubits == 2)
                if best is None or c2 < best[0]:
                    best = (c2, d)
            row[f"{name}_heavyhex_cz"] = best[0]
            row[f"{name}_heavyhex_2q_depth"] = best[1]
            row[f"{name}_ionq_2q_depth"] = ion.depth(lambda ins: ins.operation.num_qubits == 2)
        out[f"n{n}_{ent}"] = row
        print(n, ent, row, flush=True)
json.dump(out, open("results/exp5_gatecounts.json", "w"), indent=1)
