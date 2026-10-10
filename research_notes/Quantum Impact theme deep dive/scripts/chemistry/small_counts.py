import json, warnings
warnings.filterwarnings("ignore")
import numpy as np
from pyscf import gto, scf, cc, mcscf, fci, ao2mo
import ffsim
from qiskit import QuantumCircuit, QuantumRegister
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

mol = gto.M(atom="N 0 0 0; N 0 0 1.1", basis="cc-pvdz", symmetry="Dooh", verbose=0)
mf = scf.RHF(mol).run()
for (nel, norb) in [(4, 4), (6, 6), (6, 5), (10, 6), (8, 8), (10, 8)]:
    nelec = (nel // 2, nel // 2)
    ncore = (14 - nel) // 2
    active = list(range(ncore, ncore + norb)); frozen = [i for i in range(mol.nao) if i not in active]
    mycc = cc.CCSD(mf, frozen=frozen).run()
    for nreps in (1, 2):
        for label, pairs in [("all_to_all", None), ("heavyhex_like", ([(p, p + 1) for p in range(norb - 1)], [(p, p) for p in range(0, norb, 4)]))]:
            op = ffsim.UCJOpSpinBalanced.from_t_amplitudes(mycc.t2, t1=mycc.t1, n_reps=nreps, interaction_pairs=pairs)
            q = QuantumRegister(2 * norb); qc = QuantumCircuit(q)
            qc.append(ffsim.qiskit.PrepareHartreeFockJW(norb, nelec), q); qc.append(ffsim.qiskit.UCJOpSpinBalancedJW(op), q)
            pm = generate_preset_pass_manager(basis_gates=["rzz", "rz", "rx", "ry"], optimization_level=2, seed_transpiler=0); pm.pre_init = ffsim.qiskit.PRE_INIT
            t = pm.run(qc)
            nzz = t.count_ops().get("rzz", 0)
            d2 = t.depth(lambda g: g.operation.num_qubits == 2)
            print(json.dumps({"active": f"({nel}e,{norb}o)", "qubits": 2 * norb, "n_reps": nreps, "jastrow": label, "native_ZZ": nzz, "2q_depth": d2,
                              "F_est(0.5%2q+0.5%SPAM)": round(0.995 ** nzz * 0.995 ** (2 * norb), 3)}), flush=True)
