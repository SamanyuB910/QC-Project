"""Step 10e: SA with several start temperatures at 222 evaluations (generous to SA: best schedule chosen on the test instances)."""
import numpy as np
from common import *
from qsim import Inst
from s06_helpers import cost_vector
exec(open("s10c_sa_matched.py").read().split("res = {}")[0].split("rng = np.random.default_rng(0)")[0])
rng = np.random.default_rng(3)
def sa(f, n_eval, T0, T1=1e-4):
    cur = list(rng.choice(N, K, replace=False)); s = subset_to_state(cur); fc = f[s]; best = (fc, s)
    for t in range(n_eval - 1):
        T = T0 * (T1 / T0) ** (t / max(1, n_eval - 2))
        i = rng.integers(K); j = rng.choice([q for q in range(N) if q not in cur])
        new = cur.copy(); new[i] = j; s2 = subset_to_state(new)
        if f[s2] <= fc or rng.random() < np.exp(-(f[s2] - fc) / T):
            cur, fc = new, f[s2]
            if fc < best[0]: best = (fc, s2)
    return best[1]
for T0 in [0.003, 0.01, 0.03, 0.1, 0.3]:
    ps = []
    for mu in [0.0, 0.02, 0.05, 0.1, 0.2]:
        I = Inst(r, C, 0.1, extra=mu * COST / 100)
        ps.append(np.mean([sa(I.f0, 222, T0) == I.opt for _ in range(200)]))
    print(f"T0={T0}: P(opt) per mu at 222 evals = {[round(p,2) for p in ps]}; product (all 5) = {np.prod(ps):.3f}")
