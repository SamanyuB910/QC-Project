"""Emulate the plain qiskit-optimization path exactly (penalty = qiskit auto value 4.3493 at lambda=0.2, X-mixer QAOA,
COBYLA(maxiter=100) on <E> of the instance itself, random initial angles, 1024 shots, return best sampled bitstring)
with the verified numpy simulator (the real library path is too slow at 13 qubits, see s02b)."""
import numpy as np
from scipy.optimize import minimize
from common import *
from qsim import *

X, y, _ = load_data()
r, _ = relevance(X, y); C = redundancy(X)
LAM, P = 0.2, 4.349349173722215
I = Inst(r, C, LAM, P)
# qiskit uses the raw (un-normalised) Ising energies; emulate both raw and normalised angle scales
rows = []
for scale_name, E in [("raw", I.E - I.E.mean()), ("normalised", normalise(I.E))]:
    for p in [1, 2, 3]:
        for seed in range(10):
            rng = np.random.default_rng(seed)
            x0 = rng.uniform(-np.pi, np.pi, 2 * p)  # qiskit-algorithms QAOA default: random initial point
            f = lambda th: float((qaoa_x(E, th[:p], th[p:]) * E).sum())
            res = minimize(f, x0, method="COBYLA", options={"maxiter": 100})
            prob = qaoa_x(E, res.x[:p], res.x[p:])
            m = I.metrics_full(prob, shots=(1024,))
            counts = rng.multinomial(1024, prob / prob.sum())
            seen = np.flatnonzero(counts)
            best = seen[np.argmin(I.E[seen])]
            rows.append((scale_name, p, seed, m["P_opt"], m["P_feas"], m["mean_normAR_feas"], best == I.opt, FEAS[best]))
        sub = [r_ for r_ in rows if r_[0] == scale_name and r_[1] == p]
        print(f"{scale_name:10s} p={p}: mean P(opt)/shot={np.mean([s[3] for s in sub]):.5f}  mean P(feas)={np.mean([s[4] for s in sub]):.3f}  "
              f"mean AR|feas={np.mean([s[5] for s in sub]):.3f}  best-of-1024 sample == optimum in {sum(s[6] for s in sub)}/10 runs "
              f"(feasible best in {sum(s[7] for s in sub)}/10)", flush=True)
print("uniform over all 8192: P(opt)=%.5f, P(feas)=%.3f; best-of-1024 uniform hits optimum w.p. %.3f" % (1 / 8192, 1287 / 8192, 1 - (1 - 1 / 8192) ** 1024))
save_json("s02c_plain_emulated.json", rows)
