"""Scratch calibration: SPOT5 instance -> exact MILP optimum, greedy, and QAOA on extracted windows."""
import sys, zipfile, time, numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import lil_matrix
z=zipfile.ZipFile('data/spot5/spot5.zip')
def parse(name):
    toks=z.read(f'SPOT5 benchmarks/{name}.spot').decode().split('\n')
    lines=[l.split() for l in toks if l.strip()]
    nv=int(lines[0][0]); V=[]; i=1
    for _ in range(nv):
        l=list(map(int,lines[i])); i+=1
        vid,w,ds=l[0],l[1],l[2]; vals=[(l[3+2*k],l[4+2*k]) for k in range(ds)]
        V.append((vid,w,vals))
    nc=int(lines[i][0]); i+=1; C=[]
    for _ in range(nc):
        l=list(map(int,lines[i])); i+=1
        ar=l[0]; vs=l[1:1+ar]; rest=l[1+ar:]; tups=[tuple(rest[k:k+ar]) for k in range(0,len(rest),ar)]
        C.append((vs,tups))
    cap=int(lines[i][0]) if i<len(lines) else None
    return V,C,cap
name=sys.argv[1]
V,C,cap=parse(name)
bid={}; W=[]
for vid,w,vals in V:
    for val,mem in vals: bid[(vid,val)]=len(W); W.append(w)
nb=len(W); W=np.array(W,float)
rows=[]
for vid,w,vals in V:
    rows.append(([bid[(vid,val)] for val,_ in vals],1))
pairs=[];triples=[]
for vs,tups in C:
    for t in tups:
        idx=[bid[(v,a)] for v,a in zip(vs,t) if (v,a) in bid]
        if len(idx)!=len(vs): continue
        (pairs if len(vs)==2 else triples).append(tuple(idx))
        rows.append((idx,len(idx)-1))
A=lil_matrix((len(rows),nb)); ub=np.zeros(len(rows))
for r,(idx,u) in enumerate(rows):
    for j in idx: A[r,j]+=1
    ub[r]=u
t=time.time()
res=milp(-W,constraints=LinearConstraint(A.tocsr(),-np.inf,ub),integrality=np.ones(nb),bounds=Bounds(0,1))
xopt=np.round(res.x).astype(int); opt=W@xopt
print(f"instance {name}: photos={len(V)} binaries={nb} pairs={len(pairs)} triples={len(triples)} cap={cap} | MILP opt={opt:.0f} in {time.time()-t:.2f}s status={res.status}")
def feasible(x):
    for idx,u in rows:
        if x[list(idx)].sum()>u: return False
    return True
# greedy by weight
order=np.argsort(-W, kind='stable'); xg=np.zeros(nb,int)
for j in order:
    xg[j]=1
    if not feasible(xg): xg[j]=0
print(f"greedy={W@xg:.0f} gap={(1-(W@xg)/opt)*100:.2f}%")
# windows: free n binaries around a seed in the constraint graph, rest fixed to greedy incumbent
import collections
adj=collections.defaultdict(set)
for idx,u in rows:
    for a in idx:
        for b in idx:
            if a!=b: adj[a].add(b)
from qaoa_sim import lr_qaoa
rng=np.random.default_rng(1)
n=int(sys.argv[2]); out=[]
import os; PLIST=[int(x) for x in os.environ.get("PLIST","1,2,4,8").split(",")]
for trial in range(int(sys.argv[3])):
    seed=rng.integers(nb); win=[seed]; q=collections.deque([seed]); seen={seed}
    while q and len(win)<n:
        a=q.popleft()
        for b in sorted(adj[a], key=lambda _: rng.random()):
            if b not in seen and len(win)<n: seen.add(b); win.append(b); q.append(b)
    if len(win)<n: continue
    win=np.array(win); xs=((np.arange(2**n)[:,None]>>np.arange(n-1,-1,-1))&1)
    base=xg.copy(); base[win]=0
    # exact window objective (with all constraints) via enumeration
    val=np.full(2**n,-np.inf)
    rel=[(idx,u) for idx,u in rows if any(j in set(win) for j in idx)]
    for k in range(2**n):
        x=base.copy(); x[win]=xs[k]
        if all(x[list(idx)].sum()<=u for idx,u in rel): val[k]=W[win]@xs[k]
    best=val.max()
    # penalty Hamiltonian (exact HUBO): -sum w x + P * sum violations (pair: x_a x_b ; triple: x_a x_b x_c ; at-most-one handled as pairs)
    Pp=W[win].max()*1.5+1
    E=-(xs@W[win]).astype(float)
    pos={j:i for i,j in enumerate(win)}
    nterm2=0;nterm3=0
    for idx,u in rel:
        inw=[pos[j] for j in idx if j in pos]; outon=[j for j in idx if j not in pos and base[j]]
        if len(idx)==2 or (u==1 and len(idx)>2):  # at-most-one groups or pairs
            if len(idx)==2:
                if len(inw)==2: E+=Pp*xs[:,inw[0]]*xs[:,inw[1]]; nterm2+=1
                elif len(inw)==1 and outon: E+=Pp*xs[:,inw[0]]
            else:
                for a in range(len(inw)):
                    for b in range(a+1,len(inw)): E+=Pp*xs[:,inw[a]]*xs[:,inw[b]]; nterm2+=1
                if outon:
                    for a in inw: E+=Pp*xs[:,a]
        else:  # triple forbidden: violated iff all 3 on
            k_on=len(outon)
            if len(inw)+k_on==3:
                term=np.ones(2**n)
                for a in inw: term=term*xs[:,a]
                E+=Pp*term; nterm3+= (len(inw)==3); nterm2+=(len(inw)==2)
    good=(val>=best)&np.isfinite(val)
    bp=None
    for p in PLIST:
        for dg in np.linspace(0.3,8,16):
            for db in np.linspace(0.1,1.2,12):
                pr=lr_qaoa(E,n,p,dg,db); s=pr[good].sum()
                if bp is None or s>bp[0]: bp=(s,p,dg,db,pr)
    s,p,dg,db,pr=bp
    xsf=xs.astype(float); marg=(pr[:,None]*xsf).sum(0); prod=np.prod(np.where(xs==1,marg,1-marg),axis=1)
    ok=np.isfinite(val)
    out.append((s,prod[good].sum(),good.sum()/2**n,pr[ok].sum(),prod[ok].sum(),ok.mean()))
    print(f" win{trial}: n={n} 2-body={nterm2} 3-body={nterm3} n_opt={good.sum()} | QAOA p={p} P(opt)={s:.3f} P(feas)={pr[ok].sum():.2f} | prod-null P(opt)={prod[good].sum():.3f} P(feas)={prod[ok].sum():.2f} | uniform P(opt)={good.mean():.4f} P(feas)={ok.mean():.3f} | ratio={s/max(prod[good].sum(),1e-12):.2f}")
o=np.array(out); print('mean ratio QAOA/prod', (o[:,0]/o[:,1]).mean(), 'median', np.median(o[:,0]/o[:,1]))
# noise estimate: global depolarizing proxy F = 0.995^(#2q gates), 2q gates ~= p*(n_pairs + 3*n_triples)
