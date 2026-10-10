import numpy as np
from math import log2, sqrt

def h(x):
    return 0 if x<=0 or x>=1 else -x*log2(x)-(1-x)*log2(1-x)

print("=== Werner table (Phi+ fidelity F, visibility v, F=(1+3v)/4) ===")
print("v      F      C      Neg    E_N    E_F    hash   S_CHSH  CHSHgame  tele_f")
for v in [0.2,1/3,0.4,0.5,0.6,0.6875,0.7071,0.75,0.8,0.9,0.95,0.99,1.0]:
    F=(1+3*v)/4
    C=max(0,2*F-1)
    N=max(0,(3*v-1)/4)
    EN=log2(2*F) if F>0.5 else 0
    EF=h((1+sqrt(1-C**2))/2) if C>0 else 0
    p=[F]+[(1-F)/3]*3
    S=-sum(x*log2(x) for x in p if x>0)
    hashing=max(0,1-S)
    Schsh=2*sqrt(2)*v
    game=0.5+Schsh/8
    tele=(2*F+1)/3
    print(f"{v:.4f} {F:.4f} {C:.4f} {N:.4f} {EN:.4f} {EF:.4f} {hashing:.4f} {Schsh:.4f} {game:.4f} {tele:.4f}")

# find hashing threshold
from scipy.optimize import brentq
def hy(F):
    p=[F]+[(1-F)/3]*3
    return 1+sum(x*log2(x) for x in p if x>0)
print("hashing threshold F* =", brentq(hy,0.6,0.95))

print("\n=== BBPSSW (twirled) vs DEJMPS recurrence, Werner input ===")
def bbpssw(F):
    q=(1-F)/3
    N=F*F+2*F*q+5*q*q  # = F^2 + 2F(1-F)/3 + 5((1-F)/3)^2
    return (F*F+q*q)/N, N
def dejmps(A,B,C,D):
    N=(A+B)**2+(C+D)**2
    return (A*A+B*B)/N,2*C*D/N,(C*C+D*D)/N,2*A*B/N,N
for F0 in [0.55,0.6,0.7,0.8,0.9]:
    F=F0; A,B,C,D=F0,(1-F0)/3,(1-F0)/3,(1-F0)/3
    pb=1; pd=1
    row=[]
    for r in range(1,6):
        F,ps=bbpssw(F); pb*=ps
        A,B,C,D,N=dejmps(A,B,C,D); pd*=N
        # expected raw pairs consumed per output pair: recursive 2/p each level
        row.append((r,F,A,ps,N))
    print(f"F0={F0}: "+"; ".join(f"r{r}: BBPSSW {f:.4f}(p={ps:.3f}) DEJMPS {a:.4f}(p={n:.3f})" for r,f,a,ps,n in row))

# expected raw pairs per output with recurrence: cost_k = 2*cost_{k-1}/p_k
print("\nExpected raw pairs per final pair (DEJMPS, F0=0.8):")
A,B,C,D=0.8,0.2/3,0.2/3,0.2/3; cost=1
for r in range(1,5):
    A,B,C,D,N=dejmps(A,B,C,D); cost=2*cost/N
    print(f" round {r}: F={A:.5f}  expected raw pairs ~{cost:.2f}")

print("\n=== iQuHACK-style X/Z flip noise: single bilateral-CNOT round ===")
# Bell-diagonal from independent X flip px and Z flip pz on one half of Phi+
def pauli_probs(px,pz):
    return {'I':(1-px)*(1-pz),'X':px*(1-pz),'Z':(1-px)*pz,'Y':px*pz}
def round_zcheck(P):
    # bilateral CNOT control=keep pair, target=sacrificial; measure targets in Z, keep if equal.
    # error (x,z): x-bit propagates c->t, z-bit propagates t->c
    out={'I':0,'X':0,'Z':0,'Y':0}; acc=0
    lab={(0,0):'I',(1,0):'X',(0,1):'Z',(1,1):'Y'}
    inv={v:k for k,v in lab.items()}
    for a,pa in P.items():
        for b,pb in P.items():
            xa,za=inv[a]; xb,zb=inv[b]
            if (xa^xb)==0:
                acc+=pa*pb
                out[lab[(xa,za^zb)]]+=pa*pb
    return {k:v/acc for k,v in out.items()},acc
def hadamard_both(P):
    # H x H on a Bell pair maps Phi+->Phi+, X-error <-> Z-error (Psi+ <-> Phi-), Y->Y (Psi- ->Psi- up to sign)
    return {'I':P['I'],'X':P['Z'],'Z':P['X'],'Y':P['Y']}
for px,pz in [(0.1,0.0),(0.0,0.1),(0.1,0.1),(0.05,0.2),(0.2,0.05)]:
    P=pauli_probs(px,pz)
    z1,az=round_zcheck(P)
    x1,ax=round_zcheck(hadamard_both(P)); x1=hadamard_both(x1)
    # two rounds alternating: X-check then Z-check (4 pairs)
    a1,_=round_zcheck(P); a2,acc2=round_zcheck(hadamard_both(a1)); a2=hadamard_both(a2)
    b1,_=round_zcheck(hadamard_both(P)); b1=hadamard_both(b1); b2,acc2b=round_zcheck(b1)
    print(f"px={px},pz={pz}: F0={P['I']:.4f} | Z-basis check(detects X flips): F={z1['I']:.4f} p={az:.3f} | X-basis check (detects Z flips): F={x1['I']:.4f} p={ax:.3f} | 2 rounds alt: F={a2['I']:.4f}/{b2['I']:.4f}")
