import json, os, time, warnings
warnings.filterwarnings("ignore")
import numpy as np
from pyscf import gto, scf, mcscf, ao2mo, tools
import ffsim

out = {}
mol = gto.M(atom="N 0 0 0; N 0 0 1.1", basis="cc-pvdz", symmetry="Dooh", verbose=0)
mf = scf.RHF(mol).run()
for norb in [4, 6, 8, 10, 12]:
    nel = 10 if norb >= 6 else 6
    mc = mcscf.CASCI(mf, norb, nel)
    h1, ecore = mc.get_h1eff(); h2 = ao2mo.restore(1, mc.get_h2eff(), norb)
    ham = ffsim.MolecularHamiltonian(h1, h2, ecore)
    t = time.time()
    op = ffsim.qiskit.jordan_wigner(ffsim.fermion_operator(ham), norb=norb).simplify(atol=1e-10)
    groups = op.group_commuting(qubit_wise=True)
    gfull = op.group_commuting(qubit_wise=False)
    fn = f"fcidump_N2_ccpvdz_{nel}e{norb}o.txt"
    tools.fcidump.from_integrals(fn, h1, h2, norb, nel, nuc=ecore, tol=1e-12)
    out[f"({nel}e,{norb}o)"] = {"qubits": 2 * norb, "pauli_terms": len(op), "QWC_groups": len(groups),
                               "GC_groups(full commuting)": len(gfull), "fcidump_bytes": os.path.getsize(fn),
                               "s": round(time.time() - t, 1)}
    print(json.dumps(out), flush=True)
    os.remove(fn)
# FCIDUMP size scaling (8-fold symmetric eri) for larger norb using random-free estimate from actual N2 cc-pVDZ (28 orbitals total)
for norb in [16, 20, 26]:
    mc = mcscf.CASCI(mf, norb, 10)
    h1, ecore = mc.get_h1eff(); h2 = mc.get_h2eff()
    fn = f"fcidump_tmp_{norb}.txt"
    tools.fcidump.from_integrals(fn, h1, h2, norb, 10, nuc=ecore, tol=1e-12)
    out[f"fcidump_bytes_norb{norb}"] = os.path.getsize(fn)
    os.remove(fn)
print(json.dumps(out, indent=1))
