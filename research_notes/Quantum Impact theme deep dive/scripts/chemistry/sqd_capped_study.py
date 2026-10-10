"""SQD with a CAPPED subspace: is the quantum sample better than random / classical ranking at equal subspace dimension?
N2 cc-pVDZ, (10e, norb) active space, white-noise proxy for IonQ Forte (eps2q=0.005, SPAM 0.005/qubit).
"""
import json, sys, time, warnings, itertools
import numpy as np
warnings.filterwarnings("ignore")
from pyscf import gto, scf, cc, mcscf, fci, ao2mo
import ffsim
from qiskit import QuantumCircuit, QuantumRegister
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit.primitives import BitArray
from qiskit_addon_sqd.fermion import diagonalize_fermionic_hamiltonian, solve_sci_batch

R = float(sys.argv[1]); norb = int(sys.argv[2]); NREPS = int(sys.argv[3]) if len(sys.argv) > 3 else 1
CAPS = [int(x) for x in sys.argv[4].split(',')] if len(sys.argv) > 4 else [20, 40, 80]
SHOTS = 20000
nelec = (5, 5)
mol = gto.M(atom=f"N 0 0 0; N 0 0 {R}", basis="cc-pvdz", symmetry="Dooh", verbose=0)
mf = scf.RHF(mol).run()
mc = mcscf.CASCI(mf, norb, 10)
h1, ecore = mc.get_h1eff(); h2 = ao2mo.restore(1, mc.get_h2eff(), norb)
e_fci, civec = fci.direct_spin1.kernel(h1, h2, norb, nelec, ecore=ecore, conv_tol=1e-10, max_space=30, max_cycle=200)
active = list(range(2, 2 + norb)); frozen = [i for i in range(mol.nao) if i not in active]
ccsd = cc.CCSD(mf, frozen=frozen); ccsd.max_cycle = 200; ccsd.run(); et = ccsd.ccsd_t()
info = {"R": R, "norb": norb, "qubits": 2 * norb, "n_reps": NREPS, "fci_dim": int(civec.size), "E_FCI": e_fci,
        "err_mHa": {"HF": 1e3 * (mf.e_tot - e_fci), "CCSD": 1e3 * (ccsd.e_tot - e_fci), "CCSD(T)": 1e3 * (ccsd.e_tot + et - e_fci)},
        "ccsd_converged": bool(ccsd.converged)}
print(json.dumps(info), flush=True)

# "Oracle" classical ranking: strings ranked by marginal weight in the exact FCI vector (upper bound on any sampler)
ci = civec.reshape(int(np.sqrt(civec.size)), -1) if civec.ndim == 1 else civec
from pyscf.fci import cistring
strs = cistring.make_strings(range(norb), 5)
w_a = (np.abs(ci) ** 2).sum(axis=1); w_b = (np.abs(ci) ** 2).sum(axis=0)

def sci_energy(a_strs, b_strs):
    a = np.array(sorted(set(a_strs) | set(b_strs)), dtype=np.int64)  # spin-symmetrized
    res = solve_sci_batch([(a, a)], h1, h2, norb=norb, nelec=nelec)[0]
    return res.energy + ecore, len(a) ** 2

def bitstrings_to_ab(samples):
    a = [int(s) & ((1 << norb) - 1) for s in samples]; b = [int(s) >> norb for s in samples]
    return a, b

def top_k_strings(samples, k):
    # keep only correct-hamming strings, rank by frequency (alpha and beta pooled)
    a, b = bitstrings_to_ab(samples)
    cnt = {}
    for x in a + b:
        if bin(x).count("1") == 5: cnt[x] = cnt.get(x, 0) + 1
    ranked = sorted(cnt, key=lambda x: -cnt[x])
    return ranked[:k]

rng = np.random.default_rng(3)
results = []
for label, pairs in [("UCJ_all_to_all", None), ("LUCJ_heavyhex_like", ([(p, p + 1) for p in range(norb - 1)], [(p, p) for p in range(0, norb, 4)]))]:
    op = ffsim.UCJOpSpinBalanced.from_t_amplitudes(ccsd.t2, t1=ccsd.t1, n_reps=NREPS, interaction_pairs=pairs)
    q = QuantumRegister(2 * norb); qc = QuantumCircuit(q)
    qc.append(ffsim.qiskit.PrepareHartreeFockJW(norb, nelec), q); qc.append(ffsim.qiskit.UCJOpSpinBalancedJW(op), q)
    pm = generate_preset_pass_manager(basis_gates=["rzz", "rz", "rx", "ry"], optimization_level=2, seed_transpiler=0); pm.pre_init = ffsim.qiskit.PRE_INIT
    nzz = pm.run(qc).count_ops().get("rzz", 0)
    F_est = (1 - 0.005) ** nzz * (1 - 0.005) ** (2 * norb)
    vec = ffsim.apply_unitary(ffsim.hartree_fock_state(norb, nelec), op, norb=norb, nelec=nelec)
    ideal = np.array(ffsim.sample_state_vector(vec, norb=norb, nelec=nelec, shots=SHOTS, bitstring_type=ffsim.BitstringType.INT, seed=rng), dtype=np.int64)
    n_unique_ideal = len(set(top_k_strings(ideal, 10 ** 9)))
    for F in [1.0, round(F_est, 3)]:
        samp = ideal.copy(); mask = rng.random(SHOTS) > F
        samp[mask] = rng.integers(0, 2 ** (2 * norb), size=mask.sum())
        for k in CAPS:
            ks = top_k_strings(samp, k)
            e, d = sci_energy(ks, ks)
            results.append({"source": f"{label} F={F}", "native_ZZ": int(nzz), "cap_strings": k, "n_strings_used": len(ks), "dim": d, "err_mHa": round(1e3 * (e - e_fci), 3)})
            print(json.dumps(results[-1]), flush=True)
    results.append({"source": f"{label} unique correct-N strings in {SHOTS} ideal shots", "value": n_unique_ideal}); print(json.dumps(results[-1]), flush=True)
for k in CAPS:
    # uniform random correct-N strings
    pool = [int(s) for s in strs]
    rs = list(rng.choice(pool, size=min(k, len(pool)), replace=False))
    e, d = sci_energy(rs, rs); results.append({"source": "uniform random strings", "cap_strings": k, "dim": d, "err_mHa": round(1e3 * (e - e_fci), 3)})
    # oracle ranking from exact FCI marginals
    order = np.argsort(-(w_a + w_b)); os_ = [int(strs[i]) for i in order[:k]]
    e, d = sci_energy(os_, os_); results.append({"source": "oracle (exact-FCI marginal ranking)", "cap_strings": k, "dim": d, "err_mHa": round(1e3 * (e - e_fci), 3)})
    # classical heuristic: CISD-like ranking = HF + all strings within single/double excitation of HF string ranked by |CCSD t-amplitude|-free proxy: excitation level then orbital energy
    hf = (1 << 5) - 1
    exc = sorted(pool, key=lambda s: (bin(s ^ hf).count("1"), sum(i for i in range(norb) if (s >> i) & 1)))
    cs = exc[:k]; e, d = sci_energy(cs, cs); results.append({"source": "classical heuristic (excitation-level ordering)", "cap_strings": k, "dim": d, "err_mHa": round(1e3 * (e - e_fci), 3)})
    for r in results[-3:]: print(json.dumps(r), flush=True)
json.dump({"info": info, "results": results}, open(f"sqd_capped_R{R}_n{norb}_reps{NREPS}.json", "w"), indent=1)
