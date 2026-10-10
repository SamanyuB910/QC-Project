"""SQD under white-noise proxy for IonQ Forte, N2/cc-pVDZ active spaces.
Measures: LUCJ native-ZZ counts (all-to-all vs local), SQD energy error vs FCI for several fidelities, shots.
"""
import json, sys, time, warnings
import numpy as np
warnings.filterwarnings("ignore")
import pyscf
from pyscf import gto, scf, cc, mcscf, fci, ao2mo
import ffsim
from qiskit import QuantumCircuit, QuantumRegister
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit.primitives import BitArray
from qiskit_addon_sqd.fermion import diagonalize_fermionic_hamiltonian

R = float(sys.argv[1]) if len(sys.argv) > 1 else 1.1
NORBS = [int(x) for x in sys.argv[2].split(',')] if len(sys.argv) > 2 else [8, 10]
SHOTS = [int(x) for x in sys.argv[3].split(',')] if len(sys.argv) > 3 else [1000, 10000]
EPS2Q, SPAM = 0.005, 0.005
out = {"R": R, "systems": []}

mol = gto.M(atom=f"N 0 0 0; N 0 0 {R}", basis="cc-pvdz", symmetry="Dooh", verbose=0)
mf = scf.RHF(mol).run()
n_frozen = 2
for norb in NORBS:
    t0 = time.time()
    nelec = (5, 5)
    active = list(range(n_frozen, n_frozen + norb))
    mc = mcscf.CASCI(mf, norb, sum(nelec)); mc.frozen = None
    h1, ecore = mc.get_h1eff(); h2 = ao2mo.restore(1, mc.get_h2eff(), norb)
    e_fci, civec = fci.direct_spin1.kernel(h1, h2, norb, nelec, ecore=ecore, conv_tol=1e-10)
    frozen = [i for i in range(mol.nao) if i not in active]
    ccsd = cc.CCSD(mf, frozen=frozen).run()
    e_t = ccsd.ccsd_t()
    sysres = {"norb": norb, "qubits": 2 * norb, "nelec": nelec, "fci_dim": int(civec.size),
              "E_HF": mf.e_tot, "E_CCSD": ccsd.e_tot, "E_CCSD(T)": ccsd.e_tot + e_t, "E_FCI(CAS)": e_fci,
              "err_mHa": {"HF": 1e3 * (mf.e_tot - e_fci), "CCSD": 1e3 * (ccsd.e_tot - e_fci), "CCSD(T)": 1e3 * (ccsd.e_tot + e_t - e_fci)},
              "runs": []}
    pairs_local = ([(p, p + 1) for p in range(norb - 1)], [(p, p) for p in range(0, norb, 4)])
    for label, pairs in [("UCJ_all_to_all", None), ("LUCJ_heavyhex_like", pairs_local)]:
        op = ffsim.UCJOpSpinBalanced.from_t_amplitudes(ccsd.t2, t1=ccsd.t1, n_reps=1, interaction_pairs=pairs)
        # native ZZ count via Qiskit transpile into rzz basis (arbitrary-angle ZZ = IonQ Forte native)
        qubits = QuantumRegister(2 * norb)
        qc = QuantumCircuit(qubits)
        qc.append(ffsim.qiskit.PrepareHartreeFockJW(norb, nelec), qubits)
        qc.append(ffsim.qiskit.UCJOpSpinBalancedJW(op), qubits)
        pm = generate_preset_pass_manager(basis_gates=["rzz", "rz", "rx", "ry"], optimization_level=2, seed_transpiler=0)
        pm.pre_init = ffsim.qiskit.PRE_INIT
        tqc = pm.run(qc)
        nzz = tqc.count_ops().get("rzz", 0)
        F_est = (1 - EPS2Q) ** nzz * (1 - SPAM) ** (2 * norb)
        vec = ffsim.apply_unitary(ffsim.hartree_fock_state(norb, nelec), op, norb=norb, nelec=nelec)
        H = ffsim.linear_operator(ffsim.MolecularHamiltonian(h1, h2, ecore), norb=norb, nelec=nelec)
        e_ansatz = float(np.real(np.vdot(vec, H @ vec)))
        rng = np.random.default_rng(7)
        for shots in SHOTS:
            ideal = np.array(ffsim.sample_state_vector(vec, norb=norb, nelec=nelec, shots=shots,
                                                       bitstring_type=ffsim.BitstringType.INT, seed=rng), dtype=np.int64)
            for F in [1.0, round(F_est, 3), 0.05, 0.0]:
                samp = ideal.copy()
                mask = rng.random(shots) > F
                samp[mask] = rng.integers(0, 2 ** (2 * norb), size=mask.sum())
                hw_ok = np.mean([(bin(int(s) & ((1 << norb) - 1)).count("1") == 5) and (bin(int(s) >> norb).count("1") == 5) for s in samp])
                counts = {}
                for s in samp:
                    k = format(int(s), f"0{2*norb}b"); counts[k] = counts.get(k, 0) + 1
                ba = BitArray.from_counts(counts, num_bits=2 * norb)
                t1 = time.time()
                res = diagonalize_fermionic_hamiltonian(h1, h2, ba, samples_per_batch=min(shots, 1000), norb=norb, nelec=nelec,
                                                        num_batches=3, max_iterations=5, symmetrize_spin=True, seed=11)
                e_sqd = res.energy + ecore
                dim = int(np.prod(res.sci_state.amplitudes.shape))
                sysres["runs"].append({"ansatz": label, "native_ZZ": int(nzz), "F_est": round(F_est, 3), "E_ansatz_err_mHa": round(1e3 * (e_ansatz - e_fci), 2),
                                       "shots": shots, "F": F, "frac_correct_N": round(float(hw_ok), 3), "subspace_dim": dim,
                                       "subspace_frac_of_FCI": round(dim / civec.size, 3), "SQD_err_mHa": round(1e3 * (e_sqd - e_fci), 3),
                                       "sqd_s": round(time.time() - t1, 1)})
                print(json.dumps(sysres["runs"][-1]), flush=True)
    sysres["wall_s"] = round(time.time() - t0, 1)
    out["systems"].append(sysres)
    print(json.dumps({k: v for k, v in sysres.items() if k != "runs"}), flush=True)
json.dump(out, open(f"sqd_N2_R{R}.json", "w"), indent=1)
