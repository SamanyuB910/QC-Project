"""Step 10c: simulated annealing at matched evaluations on the E1 (cost-aware, k=10 MI, lam=0.1) instances."""
import numpy as np
from common import *
from qsim import Inst
from s06_helpers import cost_vector
X, y, _ = load_data(); COST = cost_vector()
r = relevance(X, y, n_neighbors=10)[0]; C = redundancy(X)
rng = np.random.default_rng(0)
def sa(f, n_eval, T0=0.1, T1=1e-4):
    cur = list(rng.choice(N, K, replace=False)); s = subset_to_state(cur); fc = f[s]; best = (fc, s)
    for t in range(n_eval - 1):
        T = T0 * (T1 / T0) ** (t / max(1, n_eval - 2))
        i = rng.integers(K); j = rng.choice([q for q in range(N) if q not in cur])
        new = cur.copy(); new[i] = j; s2 = subset_to_state(new)
        if f[s2] <= fc or rng.random() < np.exp(-(f[s2] - fc) / T):
            cur, fc = new, f[s2]
            if fc < best[0]: best = (fc, s2)
    return best[1]
res = {}
for mu in [0.0, 0.02, 0.05, 0.1, 0.2]:
    I = Inst(r, C, 0.1, extra=mu * COST / 100)
    row = []
    for budget in [22, 44, 111, 222]:
        hits = sum(sa(I.f0, budget) == I.opt for _ in range(300))
        row.append((budget, hits / 300, wilson(hits, 300)))
    res[mu] = row
    print(f"mu={mu:4.2f}: " + "  ".join(f"SA {b} evals: P(opt)={p:.2f} [{ci[0]:.2f},{ci[1]:.2f}]" for b, p, ci in row))
p_all = {b: np.prod([dict((bb, pp) for bb, pp, _ in res[mu])[b] for mu in res]) for b in [22, 44, 111, 222]}
print("P(SA finds all 5 mu-optima) assuming independence:", {b: round(v, 3) for b, v in p_all.items()})
print("(QAOA 100/200/500/1000 raw shots per circuit ~ 22/44/111/222 feasible evaluations)")
save_json("s10c_sa_matched.json", {str(k): v for k, v in res.items()})
