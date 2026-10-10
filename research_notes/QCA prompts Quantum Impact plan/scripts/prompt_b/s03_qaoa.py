"""Step 3: QAOA experiments with NO oracle tuning.
Angles are tuned on TRAINING instances (bootstrap resamples of the Cleveland rows, disjoint seeds from the test
resamples), frozen, then evaluated on the full-data instance and on held-out resamples.
Methods: (a) penalty QAOA (X mixer), (b) XY ring / complete mixers from Dicke or a k-hot basis start,
(c) independent-choice (product-of-marginals) null, (d) uniform k-subset; SA at matched evaluations lives in s01.
"""
import sys, time, json
import numpy as np
from scipy.optimize import minimize
from common import *
from qsim import *

LAM = float(sys.argv[1]) if len(sys.argv) > 1 else 0.2
NTRAIN, NTEST = 12, 12
SHOTS = 1000
X, y, _ = load_data()
n_rows = len(y)


def make_rc(idx, mi_seeds=range(5)):
    Xb, yb = X[idx], y[idx]
    r, _ = relevance(Xb, yb, seeds=mi_seeds)
    return r, redundancy(Xb)


rng = np.random.default_rng(12345)
SCHEME = os.environ.get("SCHEME", "bootstrap")
if SCHEME == "bootstrap":
    boot = [rng.integers(0, n_rows, n_rows) for _ in range(NTRAIN + NTEST)]
else:  # 80% subsamples without replacement (bootstrap duplicates inflate kNN-MI of continuous features)
    boot = [rng.choice(n_rows, int(0.8 * n_rows), replace=False) for _ in range(NTRAIN + NTEST)]
t0 = time.time()
RC = [make_rc(b) for b in boot]
r_full, C_full = relevance(X, y)[0], redundancy(X)
print(f"lambda={LAM}; built {len(RC)} bootstrap instances in {time.time()-t0:.1f}s")


def p_safe(r, C, lam):
    # flipping one bit changes the objective by at most |r_i| + lam*sum_j c_ij; P above this makes every
    # infeasible state worse than its nearest feasible neighbour (sufficient, not tight)
    return float(np.max(np.abs(r) + lam * C.sum(1)))


def p_auto_qiskit(r, C, lam):
    # filled from s02 if available, else None
    return None


def build(r, C, P):
    return Inst(r, C, LAM, P)


def greedy_state(r, C):
    sel = []
    for _ in range(K):
        cand = [(-r[i] + LAM * sum(C[i, j] for j in sel), i) for i in range(N) if i not in sel]
        sel.append(min(cand)[1])
    return subset_to_state(sel)


def topk_state(r):
    return subset_to_state(np.argsort(-r)[:K])


class Method:
    def __init__(self, name, kind, mixer=None, init=None, Pmult=None):
        self.name, self.kind, self.mixer, self.init, self.Pmult = name, kind, mixer, init, Pmult

    def setup(self, r, C):
        if self.kind == "x":
            P = self.Pmult * p_safe(r, C, LAM)
            inst = Inst(r, C, LAM, P)
            En = normalise(inst.E)
            return inst, En, None
        inst = Inst(r, C, LAM, 0.0)
        Ef = normalise(inst.ff)
        if self.init == "dicke":
            v0 = dicke_init()
        elif self.init == "greedy":
            v0 = basis_init(greedy_state(r, C))
        elif self.init == "topk":
            v0 = basis_init(topk_state(r))
        return inst, Ef, v0

    def run(self, setup, gammas, betas):
        inst, En, v0 = setup
        if self.kind == "x":
            prob = qaoa_x(En, gammas, betas)
            return prob, inst.metrics_full(prob, shots=(100, SHOTS))
        maps = RING_MAPS if self.mixer == "ring" else COMPLETE_MAPS
        pf = qaoa_xy(En, gammas, betas, maps, v0)
        return pf, inst.metrics_feas(pf, shots=(100, SHOTS))


def expected_energy_norm(method, setup, gammas, betas):
    inst, En, v0 = setup
    prob, _ = method.run(setup, gammas, betas)
    return float((prob * En).sum())


def tune(method, setups, p, objective="E", seed=0):
    """Tune 2p angles on training setups. objective 'E' = mean normalised <E> (no optimum knowledge needed);
    'Popt' = -mean P(opt) of each TRAINING instance's own optimum."""
    def loss(th):
        g, b = th[:p], th[p:]
        if objective == "E":
            return np.mean([expected_energy_norm(method, s, g, b) for s in setups])
        return -np.mean([method.run(s, g, b)[1]["P_opt"] for s in setups])
    best = None
    starts = []
    for dg in [0.2, 0.5, 1.0, 2.0]:
        for db in [0.2, 0.4, 0.7, 1.0]:
            g0, b0 = lr_schedule(p, dg, db)
            starts.append(np.concatenate([g0, b0]))
    # coarse screen, then Nelder-Mead from the 3 best
    scored = sorted(starts, key=loss)[:3]
    for s0 in scored:
        res = minimize(loss, s0, method="Nelder-Mead", options={"maxiter": 250 * p, "xatol": 1e-3, "fatol": 1e-5})
        if best is None or res.fun < best.fun:
            best = res
    return best.x[:p], best.x[p:], best.fun


methods = [
    Method("penalty_X_P1xsafe", "x", Pmult=1.0),
    Method("penalty_X_P0.3xsafe", "x", Pmult=0.3),
    Method("XY_ring_dicke", "xy", "ring", "dicke"),
    Method("XY_complete_dicke", "xy", "complete", "dicke"),
    Method("XY_ring_topk", "xy", "ring", "topk"),
    Method("XY_complete_topk", "xy", "complete", "topk"),
    Method("XY_ring_greedy", "xy", "ring", "greedy"),
    Method("XY_complete_greedy", "xy", "complete", "greedy"),
]
only = sys.argv[2].split(",") if len(sys.argv) > 2 else None
P_LIST = [int(v) for v in os.environ.get("PLIST", "1,2,3").split(",")]
OBJ = sys.argv[3].split(",") if len(sys.argv) > 3 else ["E", "Popt"]
results = {"lambda": LAM, "methods": {}}
full_inst0 = Inst(r_full, C_full, LAM, 0.0)
print("full-data optimum:", state_to_names(int(full_inst0.opt)), "greedy:", state_to_names(greedy_state(r_full, C_full)),
      "topk:", state_to_names(topk_state(r_full)))
results["full_opt"] = state_to_names(int(full_inst0.opt))
results["greedy_is_opt_full"] = greedy_state(r_full, C_full) == full_inst0.opt
results["greedy_is_opt_test"] = float(np.mean([greedy_state(*RC[i]) == Inst(*RC[i], LAM, 0).opt for i in range(NTRAIN, NTRAIN + NTEST)]))
results["topk_is_opt_test"] = float(np.mean([topk_state(RC[i][0]) == Inst(*RC[i], LAM, 0).opt for i in range(NTRAIN, NTRAIN + NTEST)]))
print("greedy optimal on held-out resamples:", results["greedy_is_opt_test"], " top-k optimal:", results["topk_is_opt_test"])
results["opt_identity_test"] = [state_to_names(int(Inst(*RC[i], LAM, 0).opt)) for i in range(NTRAIN, NTRAIN + NTEST)]
rs = np.random.default_rng(7)
for m in methods:
    if only and m.name not in only:
        continue
    t = time.time()
    tr = [m.setup(*RC[i]) for i in range(NTRAIN)]
    te = [m.setup(*RC[i]) for i in range(NTRAIN, NTRAIN + NTEST)]
    full = m.setup(r_full, C_full)
    mres = {}
    for obj in OBJ:
        for p in P_LIST:
            g, b, fl = tune(m, tr, p, obj)
            prob, met = m.run(full, g, b)
            # independent-choice null with QAOA's own marginals
            if m.kind == "x":
                marg = marginals_full(prob)
            else:
                full_prob = np.zeros(2 ** N); full_prob[FEAS_IDX] = prob; marg = marginals_full(full_prob)
            prod = product_dist(marg)
            nullmet = full[0].metrics_full(prod, shots=(100, SHOTS))
            prod_feas = prod[FEAS_IDX] / prod[FEAS_IDX].sum()
            nullmet_cond = full[0].metrics_feas(prod_feas, shots=(100, SHOTS))
            # finite-shot estimate with Wilson CI
            pf_full = prob if m.kind == "x" else full_prob
            counts = rs.multinomial(SHOTS, pf_full / pf_full.sum())
            hits = counts[full[0].opt]
            ci = wilson(hits, SHOTS)
            # held-out resamples
            tmet = [m.run(s, g, b)[1] for s in te]
            row = {"gammas": g, "betas": b, "train_loss": fl, "full": met, "null_product": nullmet,
                   "null_product_conditioned_k": nullmet_cond, "shots": SHOTS, "hits_opt": int(hits), "wilson95": ci,
                   "test_mean": {k_: float(np.mean([tm[k_] for tm in tmet])) for k_ in ["P_opt", "P_feas", "mean_normAR_feas", f"best_of_{SHOTS}_normAR"]},
                   "test_min_Popt": float(np.min([tm["P_opt"] for tm in tmet]))}
            mres[f"{obj}_p{p}"] = row
            print(f"[{m.name:22s}] tuned-on={obj:4s} p={p}: FULL P(opt)={met['P_opt']:.4f} ({hits}/{SHOTS} shots, CI {ci[0]:.4f}-{ci[1]:.4f}) "
                  f"P(feas)={met['P_feas']:.3f} meanAR|feas={met['mean_normAR_feas']:.3f} | product-null P(opt)={nullmet['P_opt']:.4f} "
                  f"P(feas)={nullmet['P_feas']:.3f}; null|k P(opt)={nullmet_cond['P_opt']:.4f} | "
                  f"held-out mean P(opt)={row['test_mean']['P_opt']:.4f} (min {row['test_min_Popt']:.4f}) | uniform-k {1/1287:.5f}", flush=True)
    results["methods"][m.name] = mres
    print(f"   ({time.time()-t:.0f}s)", flush=True)
results["scheme"] = SCHEME
save_json(f"s03_qaoa_lam{LAM}{'_' + '_'.join(only) if only else ''}{'' if SCHEME == 'bootstrap' else '_' + SCHEME}.json", results)
