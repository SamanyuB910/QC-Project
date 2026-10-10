import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import XXPlusYYGate
rng = np.random.default_rng(1)
basis = ['rzz','rz','rx','ry']
def cnt(qc): 
    t = transpile(qc, basis_gates=basis, optimization_level=2, seed_transpiler=1)
    return t.count_ops().get('rzz',0), t.depth(lambda g: g.operation.num_qubits==2)
# single Givens
qc = QuantumCircuit(2); qc.append(XXPlusYYGate(0.37, 0.0), [0,1]); print('Givens (XX+YY):', cnt(qc))
# density-density exp(i th n_p n_q)
qc = QuantumCircuit(2); qc.cp(0.41, 0, 1); print('n_p n_q phase (CPhase):', cnt(qc))
qc = QuantumCircuit(2); qc.cx(0,1); print('CNOT:', cnt(qc))
qc = QuantumCircuit(2); qc.swap(0,1); print('SWAP:', cnt(qc))
qc = QuantumCircuit(2); qc.rxx(0.3,0,1); qc.ryy(0.2,0,1); qc.rzz(0.1,0,1); print('Heisenberg bond XX+YY+ZZ:', cnt(qc))
qc = QuantumCircuit(4); 
from qiskit.circuit.library import PauliEvolutionGate
from qiskit.quantum_info import SparsePauliOp
qc.append(PauliEvolutionGate(SparsePauliOp(['XZZX','YZZY'],[0.5,0.5]), time=0.3), range(4)); print('JW hop with 2 Z-string (XZZX+YZZY):', cnt(qc))

def ucj_circuit(norb, nocc, full_jastrow=True, layers=1, compress_first=True):
    n = 2*norb  # alpha 0..norb-1, beta norb..2norb-1
    qc = QuantumCircuit(n)
    for i in range(nocc): qc.x(i); qc.x(norb+i)
    def orb_rot(nG_list):
        for (p,q) in nG_list:
            for off in (0, norb):
                qc.append(XXPlusYYGate(rng.uniform(0.1,1), 0.0), [off+p, off+q])
    # first rotation on HF: nocc*(norb-nocc) Givens, adjacent pairs network (Jiang et al.)
    def full_net(norb):
        pairs=[]
        for layer in range(norb):
            for p in range(layer%2, norb-1, 2): pairs.append((p,p+1))
        return pairs  # norb(norb-1)/2 givens
    def hf_net(norb,nocc):
        # nocc*(norb-nocc) givens on adjacent pairs
        pairs=[]
        for k in range(nocc):
            for p in range(nocc-1-k, norb-1-k): pairs.append((p,p+1))
        return pairs[:nocc*(norb-nocc)]
    for L in range(layers):
        orb_rot(hf_net(norb,nocc) if (L==0 and compress_first) else full_net(norb))
        # Jastrow
        if full_jastrow:
            for off in (0,norb):
                for p in range(norb):
                    for q in range(p+1,norb): qc.cp(rng.uniform(0.1,1), off+p, off+q)
            for p in range(norb):
                for q in range(norb): qc.cp(rng.uniform(0.1,1), p, norb+q)
        else:  # LUCJ-like: same-spin nearest neighbours, opposite-spin same orbital
            for off in (0,norb):
                for p in range(norb-1): qc.cp(rng.uniform(0.1,1), off+p, off+p+1)
            for p in range(norb): qc.cp(rng.uniform(0.1,1), p, norb+p)
        orb_rot(full_net(norb))
    qc.measure_all()
    return qc

for norb,nocc in [(4,2),(5,2),(6,3),(8,4)]:
    for fj in (True, False):
        qc = ucj_circuit(norb,nocc,full_jastrow=fj)
        print(f'UCJ 1 layer norb={norb} nocc={nocc} qubits={2*norb} jastrow={"full(all-to-all)" if fj else "LUCJ-local"}: rzz, 2q-depth =', cnt(qc))
