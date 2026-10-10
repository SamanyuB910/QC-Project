"""Step 10f: fair matched-evaluation comparison for the 5-price-point frontier task.
QAOA's job yields a POOL of ~5 x 222 feasible samples, and every mu-optimum is searched for in the whole pool.
Here SA and random-restart local search run once per mu with B evaluations each, and ALL states they evaluate are pooled."""
import numpy as np
from common import *
from qsim import Inst
from s06_helpers import cost_vector
X, y, _ = load_data(); COST = cost_vector()
r = relevance(X, y, n_neighbors=10)[0]; C = redundancy(X)
MUS = [0.0, 0.02, 0.05, 0.1, 0.2]
insts = {mu: Inst(r, C, 0.1, extra=mu * COST / 100) for mu in MUS}
rng = np.random.default_rng(11)

def sa_pool(f, n_eval, T0=0.1, T1=1e-4):
    cur = list(rng.choice(N, K, replace=False)); s = subset_to_state(cur); fc = f[s]; pool = {s}
    for t in range(n_eval - 1):
        T = T0 * (T1 / T0) ** (t / max(1, n_eval - 2))
        i = rng.integers(K); j = rng.choice([q for q in range(N) if q not in cur])
        new = cur.copy(); new[i] = j; s2 = subset_to_state(new); pool.add(s2)
        if f[s2] <= fc or rng.random() < np.exp(-(f[s2] - fc) / T):
            cur, fc = new, f[s2]
    return pool

def rrls_pool(f, budget):
    pool = set(); used = 0
    while used < budget:
        cur = list(rng.choice(N, K, replace=False)); fc = f[subset_to_state(cur)]; pool.add(subset_to_state(cur)); used += 1
        improved = True
        while improved and used < budget:
            improved = False; best = None
            for a in range(K):
                for j in range(N):
                    if j in cur or used >= budget: continue
                    new = cur.copy(); new[a] = j; s = subset_to_state(new); pool.add(s); used += 1
                    if best is None or f[s] < best[0]: best = (f[s], new)
            if best is not None and best[0] < fc:
                cur, fc = best[1], best[0]; improved = True
    return pool

for B in [22, 44, 111, 222]:
    for name, fn in [("SA (T0=0.1)", lambda f: sa_pool(f, B)), ("SA (T0=0.3)", lambda f: sa_pool(f, B, T0=0.3)), ("random-restart 1-swap LS", lambda f: rrls_pool(f, B))]:
        found = []
        for rep in range(200):
            pool = set()
            for mu in MUS:
                pool |= fn(insts[mu].f0)
            found.append(sum(insts[mu].opt in pool for mu in MUS))
        found = np.array(found)
        print(f"{B:4d} evals per mu (pooled {5*B}): {name:26s} mu-optima found {found.mean():.2f}/5, all 5 in {100*(found==5).mean():.0f}% of runs")
print("compare (s10b): QAOA ideal / noisy forte-1 at 100,200,500,1000 raw shots per circuit (~22,44,111,222 feasible): all-5 = 8/2, 32/12, 78/66, 98/94 %; null|k 0/2/25/62 %; uniform 0/0/0/10 %")
