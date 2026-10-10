import numpy as np, itertools, time
from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import UnitaryGate
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error, ReadoutError, pauli_error
from qiskit.quantum_info import DensityMatrix, partial_trace, state_fidelity, Statevector

E2 = 0.005   # average 2q gate error
E1 = 0.0002  # average 1q gate error
RO = 0.005   # readout flip prob
lam2 = E2/0.75
lam1 = E1/0.5

def noise(ro=True):
    nm = NoiseModel()
    nm.add_all_qubit_quantum_error(depolarizing_error(lam2,2), ['cx','cz'])
    nm.add_all_qubit_quantum_error(depolarizing_error(lam1,1), ['h','rx','ry','rz','sdg','s','x','z','y','sx'])
    if ro:
        nm.add_all_qubit_readout_error(ReadoutError([[1-RO,RO],[RO,1-RO]]))
    return nm

BASIS = ['cx','cz','h','rx','ry','rz','sdg','s','x','z','y','sx','unitary','measure','save_density_matrix','save_probabilities']
dm_sim = AerSimulator(method='density_matrix', noise_model=noise())
dm_sim_noro = AerSimulator(method='density_matrix', noise_model=noise(False))
ideal = AerSimulator(method='density_matrix')

def probs(qc, sim):
    qc2 = qc.copy(); qc2.save_probabilities(label='p')
    r = sim.run(qc2).result()
    return r.data()['p']

def probs_meas(qc, sim, shots=200000):
    r = sim.run(qc, shots=shots).result()
    return r.get_counts()

# ---------- CHSH ----------
print("=== CHSH on Phi+ ===")
def chsh(sim):
    angA=[0,np.pi/2]; angB=[np.pi/4,-np.pi/4]
    E={}
    for i,a in enumerate(angA):
        for j,b in enumerate(angB):
            qc=QuantumCircuit(2,2); qc.h(0); qc.cx(0,1)
            qc.ry(-a,0); qc.ry(-b,1); qc.measure([0,1],[0,1])
            c=probs_meas(qc,sim,shots=400000); tot=sum(c.values())
            e=sum(v*(1 if k.count('1')%2==0 else -1) for k,v in c.items())/tot
            E[(i,j)]=e
    return E[(0,0)]+E[(0,1)]+E[(1,0)]-E[(1,1)]
for name,sim in [('ideal',ideal),('0.5% 2q + 0.5% RO',dm_sim)]:
    S=chsh(sim); print(f"{name}: S={S:.4f}  CHSH game win={0.5+S/8:.4f}")

# ---------- Teleportation ----------
print("\n=== Teleportation (avg over 6 cardinal input states) ===")
cards = {'0':[], '1':['x'], '+':['h'], '-':['x','h'], '+i':['h','s'], '-i':['h','sdg']}
CXu = UnitaryGate(np.array([[1,0,0,0],[0,0,0,1],[0,0,1,0],[0,1,0,0]]),label='cx_free')  # qiskit little-endian: control q0(first arg)
CZu = UnitaryGate(np.diag([1,1,1,-1]),label='cz_free')
def prep(qc,q,ops):
    for o in ops: getattr(qc,o)(q)
def tele_fid(mode, sim):
    fs=[]
    for k,ops in cards.items():
        qc=QuantumCircuit(3,1)
        prep(qc,0,ops)
        qc.h(1); qc.cx(1,2)
        qc.cx(0,1); qc.h(0)
        if mode=='deferred':      # physical controlled corrections (noisy)
            qc.cx(1,2); qc.cz(0,2)
        else:                      # Pauli-frame / noiseless classical correction equivalent
            qc.append(CXu,[1,2]); qc.append(CZu,[0,2])
        # undo prep on q2 and measure overlap
        inv=QuantumCircuit(1); prep(inv,0,ops); qc.compose(inv.inverse(),[2],inplace=True)
        qc.measure(2,0)
        c=probs_meas(qc,sim,shots=200000); fs.append(c.get('0',0)/sum(c.values()))
    return np.mean(fs)
for mode in ['deferred','pauli_frame']:
    print(f"{mode}: ideal {tele_fid(mode,ideal):.4f}, noisy {tele_fid(mode,dm_sim):.4f}  (classical bound 0.6667)")

# ---------- Superdense coding ----------
print("\n=== Superdense coding success ===")
succ=[]
for bits in ['00','01','10','11']:
    qc=QuantumCircuit(2,2); qc.h(0); qc.cx(0,1)
    if bits[1]=='1': qc.x(0)
    if bits[0]=='1': qc.z(0)
    qc.cx(0,1); qc.h(0); qc.measure([0,1],[1,0])
    c=probs_meas(qc,dm_sim,shots=200000); succ.append(c.get(bits,0)/sum(c.values()))
print("noisy success per message:",[round(s,4) for s in succ],"mean",round(np.mean(succ),4))

# ---------- Swapping chain ----------
print("\n=== Entanglement swapping chain (end-to-end Phi+ fidelity, noiseless frame correction, no readout err) ===")
def chain(n, sim):
    q=2*n; qc=QuantumCircuit(q)
    for l in range(n):
        qc.h(2*l); qc.cx(2*l,2*l+1)
    last=q-1
    for l in range(n-1):
        b,c=2*l+1,2*l+2
        qc.cx(b,c); qc.h(b)
        qc.append(CXu,[c,last]); qc.append(CZu,[b,last])
    qc.save_density_matrix(qubits=[0,last],label='rho')
    r=sim.run(qc).result()
    rho=DensityMatrix(r.data()['rho'])
    bell=Statevector(np.array([1,0,0,1])/np.sqrt(2))
    return state_fidelity(rho,bell)
for n in range(1,6):
    t=time.time(); F=chain(n,dm_sim_noro)
    v=(1-lam2)**(2*n-1)
    print(f"links={n} qubits={2*n} 2q gates={2*n-1}: sim F={F:.4f}; analytic Werner (1+3(1-lam)^(2n-1))/4={(1+3*v)/4:.4f}")
for n in [8,10,12,14]:
    v=(1-lam2)**(2*n-1); print(f"links={n} qubits={2*n}: analytic F={(1+3*v)/4:.4f}")

# ---------- GHZ scaling (stabilizer sim) ----------
print("\n=== GHZ fidelity vs n (stabilizer sim, 0.5% 2q depol, 0.02% 1q, 0.5% RO) ===")
stab=AerSimulator(method='stabilizer', noise_model=noise())
stab_nro=AerSimulator(method='stabilizer', noise_model=noise(False))
def ghz(n, sim, shots=40000):
    def base():
        qc=QuantumCircuit(n,n); qc.h(0)
        # log-depth fan-out tree
        have=[0]
        while len(have)<n:
            new=[]
            for a in have:
                t=len(have)+len(new)
                if t<n: qc.cx(a,t); new.append(t)
            have+=new
        return qc
    qa=base(); qa.measure(range(n),range(n))
    c=sim.run(qa,shots=shots).result().get_counts()
    pop=(c.get('0'*n,0)+c.get('1'*n,0))/shots
    qb=base(); qb.h(range(n)); qb.measure(range(n),range(n))
    c=sim.run(qb,shots=shots).result().get_counts()
    par=sum(v*(1 if k.count('1')%2==0 else -1) for k,v in c.items())/shots
    return pop/2+par/2, pop, par
for n in [2,3,4,5,8,12,16,20,24,29]:
    F,pop,par=ghz(n,stab); F2,_,_=ghz(n,stab_nro)
    print(f"n={n:2d}: F={F:.3f} (pop {pop:.3f}, <X^n> {par:.3f}); without readout err F={F2:.3f}; (1-E2)^(n-1)={(1-E2)**(n-1):.3f}")

# ---------- GHZ game ----------
print("\n=== GHZ game (3 players) ===")
wins=[]
for xyz in ['000','011','101','110']:
    qc=QuantumCircuit(3,3); qc.h(0); qc.cx(0,1); qc.cx(0,2)
    for i,b in enumerate(xyz):
        if b=='1': qc.sdg(i)
        qc.h(i)
    qc.measure(range(3),range(3))
    c=probs_meas(qc,dm_sim,shots=200000); tot=sum(c.values())
    target=1 if '1' in xyz else 0
    wins.append(sum(v for k,v in c.items() if k.count('1')%2==target)/tot)
print("per question:",[round(w,4) for w in wins],"avg",round(np.mean(wins),4),"(classical 0.75)")

# ---------- Mermin-Peres magic square ----------
print("\n=== Magic square game (2 Phi+ pairs: (a1,b1),(a2,b2)) ===")
# qubits: a1=0,a2=1,b1=2,b2=3
def alice_row(qc,r):
    a1,a2=0,1
    if r==0: qc.h(a1); qc.h(a2)            # XI, IX
    elif r==1: pass                         # IZ? we read ZI from a1, IZ from a2
    else: qc.cz(a1,a2); qc.h(a1); qc.h(a2)  # XZ, ZX
def bob_col(qc,c):
    b1,b2=2,3
    if c==0: qc.h(b1)                      # XI (b1 X), IZ (b2 Z)
    elif c==1: qc.h(b2)                    # IX (b2 X), ZI (b1 Z)
    else: qc.cx(b1,b2); qc.h(b1)           # XX on b1, ZZ on b2
def cell_values_alice(r,m):  # m=(m_a1,m_a2) as +-1 eigenvalues
    s1,s2=m
    if r==0: return [s1, s2, s1*s2]               # XI, IX, XX
    if r==1: return [s2, s1, s1*s2]               # IZ, ZI, ZZ
    return [-s1, -s2, s1*s2]                       # -XZ, -ZX, YY
def cell_values_bob(c,m):
    s1,s2=m
    if c==0: return [s1, s2, -s1*s2]              # XI, IZ, -XZ
    if c==1: return [s2, s1, -s1*s2]              # IX, ZI, -ZX
    return [s1, s2, -s1*s2]                        # XX, ZZ, YY
def ms_win(sim):
    tot_w=[]
    for r in range(3):
        for c in range(3):
            qc=QuantumCircuit(4,4); qc.h(0); qc.cx(0,2); qc.h(1); qc.cx(1,3)
            alice_row(qc,r); bob_col(qc,c); qc.measure(range(4),range(4))
            cnt=probs_meas(qc,sim,shots=100000); tot=sum(cnt.values()); w=0
            for k,v in cnt.items():
                bits=k[::-1]  # bits[i] = qubit i
                sa=(1-2*int(bits[0]),1-2*int(bits[1])); sb=(1-2*int(bits[2]),1-2*int(bits[3]))
                A=cell_values_alice(r,sa); B=cell_values_bob(c,sb)
                if A[c]==B[r]: w+=v
            tot_w.append(w/tot)
    return np.mean(tot_w), tot_w
for name,sim in [('ideal',ideal),('noisy',dm_sim)]:
    m,all_=ms_win(sim); print(f"{name}: avg win {m:.4f} (classical 8/9=0.8889); per-cell min {min(all_):.4f}")

# ---------- Distillation circuit with gate noise ----------
print("\n=== One DEJMPS round on two Werner pairs, noisy local gates (density matrix, no RO) ===")
def werner_channel(F):
    q=(1-F)/3
    return pauli_error([('I',F),('X',q),('Y',q),('Z',q)])
def dejmps_round(F, gate_noise=True):
    # pairs: (0,3) and (1,2); Alice 0,1 ; Bob 2,3 (iQuHACK outside-in layout for N=2)
    nm=NoiseModel()
    if gate_noise:
        nm.add_all_qubit_quantum_error(depolarizing_error(lam2,2),['cx'])
        nm.add_all_qubit_quantum_error(depolarizing_error(lam1,1),['rx','h'])
    sim=AerSimulator(method='density_matrix',noise_model=nm)
    qc=QuantumCircuit(4,2)
    for a,b in [(0,3),(1,2)]:
        qc.h(a); qc.cx(a,b)
    # apply Werner noise noiselessly via unitary-free channel
    qc2=QuantumCircuit(4,2); qc2.compose(qc,inplace=True)
    sv=Statevector.from_instruction(qc)
    rho=DensityMatrix(sv)
    from qiskit.quantum_info import Kraus
    K=Kraus(werner_channel(F))
    rho=rho.evolve(K,[3]).evolve(K,[2])
    qc=QuantumCircuit(4,2)
    qc.set_density_matrix(rho)
    qc.rx(np.pi/2,0); qc.rx(np.pi/2,1); qc.rx(-np.pi/2,2); qc.rx(-np.pi/2,3)
    qc.cx(1,0); qc.cx(2,3)   # keep pair (1,2) controls; sacrificial pair (0,3) targets
    qc.measure(0,0); qc.measure(3,1)
    qc.save_density_matrix(qubits=[1,2],label='rho',conditional=True)
    r=sim.run(qc).result()
    d=r.data()['rho']
    bell=Statevector(np.array([1,0,0,1])/np.sqrt(2))
    psucc=0; Fnum=0
    for key,mat in d.items():
        k=int(key,16) if isinstance(key,str) else key
        b0=k&1; b1=(k>>1)&1
        m=DensityMatrix(mat); p=np.real(np.trace(m.data))
        if b0==b1:
            psucc+=p; Fnum+=np.real(bell.data.conj()@m.data@bell.data)
    return Fnum/psucc, psucc
for F in [0.6,0.7,0.8,0.9,0.95,0.98,0.99,0.995]:
    Fi,pi=dejmps_round(F,False); Fn,pn=dejmps_round(F,True)
    print(f"F_in={F}: ideal gates F_out={Fi:.4f} (p={pi:.3f}); 0.5% CNOT F_out={Fn:.4f} (p={pn:.3f})")
