"""Scratch calibration: 6 marginal units x 2 hours (12 qubits) with startup coupling."""
import sys, time, numpy as np
from uc_calib import units, net, res, dispatch, lr_qaoa, metrics
from scipy.stats import spearmanr
rng=np.random.default_rng(3)
def run(h0, nu=6, H=2):
    n=nu*H
    order=sorted(range(len(units)), key=lambda i: units[i]['avg'])
    Dmax=max(net[h0:h0+H]+res[h0:h0+H]); cum=0;k=0
    while cum<Dmax: cum+=units[order[k]]['pmax']; k+=1
    lo=max(0,k-nu//2); win=[units[i] for i in order[lo:lo+nu]]; fixed=[units[i] for i in order[:lo]]
    xs=((np.arange(2**n)[:,None]>>np.arange(n-1,-1,-1))&1)
    cost=np.zeros(2**n)
    for x in range(2**n):
        b=xs[x].reshape(H,nu); tot=0
        for t in range(H):
            on=fixed+[dict(u, su=0.0) for j,u in enumerate(win) if b[t,j]]
            c=dispatch(on, net[h0+t], res[h0+t])
            # startup cost when a window unit turns on (t0 = off)
            prev=b[t-1] if t>0 else np.zeros(nu,int)
            c+=sum(win[j]['su'] for j in range(nu) if b[t,j] and not prev[j])
            tot+=c
        cost[x]=tot
    feas=np.isfinite(cost); opt=cost.min()
    # fit QUBO surrogate
    xsf=xs.astype(float); iu=np.triu_indices(n,1)
    F=np.hstack([np.ones((2**n,1)),xsf,xsf[:,iu[0]]*xsf[:,iu[1]]])
    tgt=np.where(feas,cost,cost[feas].max()*1.5)
    w=np.where(tgt<=np.quantile(tgt,0.25),4.0,1.0)
    coef,*_=np.linalg.lstsq(F*w[:,None],tgt*w,rcond=None); E=F@coef
    rho=spearmanr(E[feas],cost[feas]).statistic; gap=(cost[np.argmin(E)]/opt-1)*100
    best=None
    for p in [1,2,4,8,12]:
        for dg in np.linspace(0.5,10,20):
            for db in np.linspace(0.1,1.2,12):
                pr=lr_qaoa(E,n,p,dg,db); m=metrics(pr,cost,opt)
                if best is None or m[0]>best[0][0]: best=(m,p,dg,db,pr)
    (q1,q2,qf),p,dg,db,pr=best
    marg=(pr[:,None]*xsf).sum(0); prod=np.prod(np.where(xsf==1,marg,1-marg),axis=1)
    n1=metrics(prod,cost,opt); un=metrics(np.full(2**n,2.0**-n),cost,opt)
    # priority-list per hour (myopic)
    pl=0
    xpl=np.zeros((H,nu),int)
    for t in range(H):
        for kk in range(nu+1):
            on=fixed+[dict(u,su=0.0) for u in win[:kk]]
            if np.isfinite(dispatch(on,net[h0+t],res[h0+t])): xpl[t,:kk]=1; break
    idx=int(''.join(map(str,xpl.reshape(-1))),2); plgap=(cost[idx]/opt-1)*100
    print(f"h0={h0} n={n} opt=${opt:,.0f} good1%={int((cost<=opt*1.01).sum())}/{2**n} rho={rho:.2f} QUBOargmin gap={gap:.2f}% PL(myopic) gap={plgap:.2f}% | QAOA p={p} dg={dg:.1f} db={db:.2f} P1%={q1:.4f} feas={qf:.2f} | prod-null P1%={n1[0]:.4f} | uniform {un[0]:.4f} | ratio QAOA/prod={q1/max(n1[0],1e-12):.2f}")
for h0 in [int(x) for x in sys.argv[2].split(',')]:
    t=time.time(); run(h0); print(f'  ({time.time()-t:.0f}s)')
