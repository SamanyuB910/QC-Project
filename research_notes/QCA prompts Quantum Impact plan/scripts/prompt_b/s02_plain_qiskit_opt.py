"""Step 2: the 'plain version' every team will build, run with qiskit-optimization 0.7.0 / qiskit-algorithms 0.4.0
(the Qollab presets). Checks the auto-penalty and what MinimumEigenOptimizer(QAOA) actually returns.
Run with a Python that has qiskit-optimization 0.7.0 installed (a venv here). Reads r, C from s01 results."""
import json, os, sys, time, warnings, logging
import numpy as np
warnings.filterwarnings("ignore")
logging.basicConfig(level=logging.WARNING)
from qiskit_optimization import QuadraticProgram
from qiskit_optimization.converters import QuadraticProgramToQubo, LinearEqualityToPenalty
from qiskit_optimization.algorithms import MinimumEigenOptimizer
from qiskit_algorithms import QAOA, NumPyMinimumEigensolver
from qiskit_algorithms.optimizers import COBYLA
from qiskit_algorithms.utils import algorithm_globals
from qiskit.primitives import StatevectorSampler

HERE = os.path.dirname(os.path.abspath(__file__))
d = json.load(open(os.path.join(HERE, "results", "s01_data_qubo.json")))
r = np.array(d["r"]); C = np.array(d["C"]); F = d["features"]; n = len(F); k = 5
out = {}
for lam in [0.2]:
    qp = QuadraticProgram("heart_k5")
    for f in F:
        qp.binary_var(f)
    quad = {(F[i], F[j]): lam * C[i, j] for i in range(n) for j in range(i + 1, n)}
    qp.minimize(linear={F[i]: -r[i] for i in range(n)}, quadratic=quad)
    qp.linear_constraint(linear={f: 1 for f in F}, sense="==", rhs=k, name="k_features")
    conv = QuadraticProgramToQubo()
    qubo = conv.convert(qp)
    # recover the penalty actually used
    lep = LinearEqualityToPenalty()
    _ = lep.convert(qp)
    pen = lep.penalty
    print(f"lam={lam}: auto penalty chosen by LinearEqualityToPenalty = {pen}", flush=True)
    # also: what if the constraint had a fractional coefficient (e.g. a normalised constraint sum x_i/5 == 1)?
    qp2 = QuadraticProgram("frac")
    for f in F:
        qp2.binary_var(f)
    qp2.minimize(linear={F[i]: -r[i] for i in range(n)}, quadratic=quad)
    qp2.linear_constraint(linear={f: 0.2 for f in F}, sense="==", rhs=1.0, name="k_frac")
    lep2 = LinearEqualityToPenalty(); _ = lep2.convert(qp2)
    print(f"   same constraint written as sum(0.2 x_i) == 1  -> auto penalty = {lep2.penalty}")
    # exact optimum by enumerating the 1287 feasible subsets (NumPyMinimumEigensolver builds an 8192x8192 matrix: slow, 1+ GB)
    from itertools import combinations
    best = min(combinations(range(n), k), key=lambda S: -sum(r[i] for i in S) + lam * sum(C[i, j] for a, i in enumerate(S) for j in S[a + 1:]))
    xopt = tuple(1 if i in best else 0 for i in range(n))
    print(f"   exact (enumeration): {[F[i] for i in range(n) if xopt[i]]}", flush=True)
    res = {"auto_penalty": pen, "frac_penalty": lep2.penalty, "exact": [F[i] for i in range(n) if xopt[i]], "runs": []}
    for reps in [1, 2, 3]:
        for seed in range(5):
            algorithm_globals.random_seed = seed
            t = time.time()
            qaoa = QAOA(sampler=StatevectorSampler(seed=seed), optimizer=COBYLA(maxiter=100), reps=reps)
            rr = MinimumEigenOptimizer(qaoa).solve(qp)
            dt = time.time() - t
            p_opt = sum(s.probability for s in rr.samples if tuple(int(v) for v in s.x) == xopt)
            p_feas = sum(s.probability for s in rr.samples if s.status.name == "SUCCESS")
            hit = tuple(int(v) for v in rr.x) == xopt
            nfev = qaoa.optimizer  # placeholder
            print(f"   QAOA reps={reps} seed={seed}: returned={[F[i] for i in range(n) if rr.x[i]]} hit_opt={hit} "
                  f"P(opt in samples)={p_opt:.4f} P(feasible)={p_feas:.3f} time={dt:.1f}s", flush=True)
            res["runs"].append({"reps": reps, "seed": seed, "hit": hit, "p_opt": p_opt, "p_feas": p_feas, "time": dt,
                                "returned": [F[i] for i in range(n) if rr.x[i]]})
        json.dump(out | {str(lam): res}, open(os.path.join(HERE, "results", "s02_plain_qiskit_opt.json"), "w"), indent=1)
    out[str(lam)] = res
json.dump(out, open(os.path.join(HERE, "results", "s02_plain_qiskit_opt.json"), "w"), indent=1)
