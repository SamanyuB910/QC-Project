"""Step 10d: stronger classical baselines at matched evaluations on the E1 instances:
greedy + 1-swap best-improvement local search (deterministic) and random-restart 1-swap local search (budgeted)."""
import numpy as np
from common import *
from qsim import Inst
from s06_helpers import cost_vector
X, y, _ = load_data(); COST = cost_vector()
r = relevance(X, y, n_neighbors=10)[0]; C = redundancy(X)

def greedy(f):
    sel = []; ev = 0
    for _ in range(K):
        best = None
        for i in range(N):
            if i in sel: continue
            s = subset_to_state(sel + [i]); ev += 1  # partial subsets evaluated on the same polynomial
            if best is None or f[s] < best[0]: best = (f[s], i)
        sel.append(best[1])
    return sel, ev

def local_search(f, start, budget):
    cur = list(start); fc = f[subset_to_state(cur)]; ev = 1
    while ev < budget:
        best = None
        for a in range(K):
            for j in range(N):
                if j in cur: continue
                new = cur.copy(); new[a] = j; s = subset_to_state(new); ev += 1
                if best is None or f[s] < best[0]: best = (f[s], new)
                if ev >= budget: break
            if ev >= budget: break
        if best is None or best[0] >= fc: break
        cur, fc = best[1], best[0]
    return subset_to_state(cur), ev

rng = np.random.default_rng(1)
for mu in [0.0, 0.02, 0.05, 0.1, 0.2]:
    I = Inst(r, C, 0.1, extra=mu * COST / 100); f = I.f0.copy()
    g, evg = greedy(f)
    sl, evl = local_search(f, g, 10 ** 6)
    out = [f"greedy={'OPT' if subset_to_state(g)==I.opt else 'rank '+str(int(I.rank_f[np.flatnonzero(FEAS_IDX==subset_to_state(g))[0]])+1)} ({evg} evals)",
           f"greedy+1swap LS={'OPT' if sl==I.opt else 'not opt'} ({evg+evl} evals total)"]
    for budget in [44, 111, 222]:
        hits = 0
        for rep in range(300):
            used = 0; found = False
            while used < budget:
                st = list(rng.choice(N, K, replace=False))
                s, ev = local_search(f, st, budget - used); used += ev
                if s == I.opt: found = True; break
            hits += found
        out.append(f"RR-LS {budget} evals: P(opt)={hits/300:.2f}")
    print(f"mu={mu:4.2f}: " + " | ".join(out))
