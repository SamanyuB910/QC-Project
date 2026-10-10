import sys, time, numpy as np
from uc_calib import *
n = int(sys.argv[2]); hours=[int(x) for x in sys.argv[3].split(',')]
for h in hours:
    t0=time.time()
    D,R,fixed,W = make_window(h,n)
    cost = all_costs(D,R,fixed,W); opt=cost.min(); feas=np.isfinite(cost)
    xs = ((np.arange(2**n)[:,None] >> np.arange(n-1,-1,-1)) & 1).astype(float)
    # shortfall for infeasible
    P=np.array([u['pmax'] for u in W]); Pm=np.array([u['pmin'] for u in W])
    capfix=sum(u['pmax'] for u in fixed)
    short = np.maximum(0, D+R - (capfix + xs@P))
    tgt = np.where(feas, cost, cost[feas].max() + (cost[feas].max()-opt)*(1+short/ max(P.mean(),1)))
    # least-squares QUBO fit: const + linear + pairwise
    iu = np.triu_indices(n,1)
    F = np.hstack([np.ones((2**n,1)), xs, (xs[:,iu[0]]*xs[:,iu[1]])])
    w = np.where(tgt <= np.quantile(tgt, 0.25), 4.0, 1.0)  # weight the low-cost region
    coef,*_ = np.linalg.lstsq(F*w[:,None], tgt*w, rcond=None)
    E = F@coef
    am = np.argmin(E); gapq=(cost[am]/opt-1)*100
    # spearman
    from scipy.stats import spearmanr
    rho = spearmanr(E[feas], cost[feas]).statistic
    best=None
    for p in [1,2,3,5,8,12]:
        for dg in np.linspace(0.2,4.0,20):
            for db in np.linspace(0.1,1.5,15):
                pr = lr_qaoa(E,n,p,dg,db); m=metrics(pr,cost,opt)
                if best is None or m[0]>best[0][0]: best=(m,p,dg,db,pr)
    (q1,q2,qf),p,dg,db,pr = best
    marg=(pr[:,None]*xs).sum(0); prod=np.prod(np.where(xs==1,marg,1-marg),axis=1)
    n1=metrics(prod,cost,opt); nu=metrics(np.full(2**n,2.0**-n),cost,opt)
    # Boltzmann-on-surrogate classical null at matched entropy? skip; SA on true cost w/ 200 evals
    def sa(evals):
        hits=0; R_=200
        for r in range(R_):
            x=rng.integers(0,2,n); c=cost[int(''.join(map(str,x)),2)]; bestc=c; Tm=(cost[feas].std())
            for e in range(evals):
                j=rng.integers(n); x[j]^=1; c2=cost[int(''.join(map(str,x)),2)]
                tt=Tm*(1-e/evals)+1e-9
                if c2<=c or (np.isfinite(c2) and np.isfinite(c) and rng.random()<np.exp(-(c2-c)/tt)): c=c2; bestc=min(bestc,c)
                else: x[j]^=1
            hits += bestc<=opt*1.01
        return hits/R_
    sa20=sa(20); sa50=sa(50)
    shots_tts = lambda q: np.log(0.01)/np.log(1-q) if 0<q<1 else (1 if q>=1 else np.inf)
    print(f"h={h:2d} n={n} opt=${opt:,.0f} n_good1%={int((cost<=opt*1.01).sum())}/{2**n} rho={rho:.2f} QUBOfit-argmin gap={gapq:.2f}% | QAOA p={p} dg={dg:.2f} db={db:.2f} P1%={q1:.3f} feas={qf:.2f} TTS99={shots_tts(q1):.0f} shots | prod-null P1%={n1[0]:.3f} TTS99={shots_tts(n1[0]):.0f} | uniform {nu[0]:.4f} TTS99={shots_tts(nu[0]):.0f} | SA P(hit in 20 evals)={sa20:.2f} 50 evals={sa50:.2f} | {time.time()-t0:.1f}s")
