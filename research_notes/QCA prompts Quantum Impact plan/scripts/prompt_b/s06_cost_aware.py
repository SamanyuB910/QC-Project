"""Step 6: cost-aware screening panel with Turney's real test costs and shared-procedure discounts.

cost(x) = sum_i d_i x_i + sum_g s_g * OR_g(x)          (d = discount cost, s_g = shared cost of procedure g)
OR_A = x_chol + x_fbs - x_chol x_fbs                     (blood draw, s_A = 2.10)
OR_B = x_thalach + x_thal - x_thalach x_thal             (s_B = 101.90)
OR_C = x_ex + x_op + x_sl - x_ex x_op - x_ex x_sl - x_op x_sl + x_ex x_op x_sl   (exercise ECG, s_C = 86.30) -> CUBIC
Objective (k = 5 via XY mixer):  f_mu(x) = -sum r_i x_i + lam sum c_ij x_i x_j + mu * cost(x)/100
"""
import sys, time
import numpy as np
from scipy.optimize import minimize
from common import *
from qsim import *

LAM = 0.2
X, y, _ = load_data()
r_full, _ = relevance(X, y); C_full = redundancy(X)
fi = {f: i for i, f in enumerate(FEATURES)}
d = np.array([EXPENSE[f][1] for f in FEATURES])
s = {g: EXPENSE[m[0]][0] - EXPENSE[m[0]][1] for g, m in GROUPS.items()}
B = BITS.astype(float)


def cost_poly():
    c = B @ d
    for g, mem in GROUPS.items():
        idx = [fi[f] for f in mem]
        orv = 1 - np.prod(1 - B[:, idx], axis=1)
        c = c + s[g] * orv
    return c


COST = cost_poly()
chk = all_costs()
print("cost polynomial == table-driven Turney cost for all 8192 states:", np.allclose(COST, chk), " max |diff|", np.abs(COST - chk).max())
print("shared costs:", s, " discount costs:", dict(zip(FEATURES, d)))
c5 = COST[FEAS_IDX]
print(f"5-panel cost range ${c5.min():.2f} .. ${c5.max():.2f}; cheapest 5-panel {state_to_names(int(FEAS_IDX[np.argmin(c5)]))}")
# Ising expansion term count (for gate cost)
print("HUBO terms added by cost: linear 13, quadratic 1 (A) + 1 (B) + 3 (C) = 5 pairs (all already present in the dense c_ij graph), cubic 1 (exang,oldpeak,slope)")

res = {"cost_matches_table": bool(np.allclose(COST, chk))}


def greedy_cost(r, C, lam, mu):
    sel = []
    for _ in range(K):
        best = None
        for i in range(N):
            if i in sel:
                continue
            st = subset_to_state(sel + [i]); st0 = subset_to_state(sel)
            delta = -r[i] + lam * sum(C[i, j] for j in sel) + mu * (COST[st] - COST[st0]) / 100
            if best is None or delta < best[0]:
                best = (delta, i)
        sel.append(best[1])
    return subset_to_state(sel)


def inst_mu(r, C, mu):
    return Inst(r, C, LAM, 0.0, extra=mu * COST / 100)


# ---- mu sweep: exact optimum vs greedy ----
print("\nmu sweep (lam=0.2): exact optimum over 1287 vs cost-aware greedy")
sweep = []
for mu in [0, 0.005, 0.01, 0.015, 0.02, 0.03, 0.04, 0.05, 0.06, 0.08, 0.1, 0.12, 0.15, 0.2, 0.3, 0.5, 1.0, 2.0]:
    I = inst_mu(r_full, C_full, mu)
    g = greedy_cost(r_full, C_full, LAM, mu)
    rank_g = int(I.rank_f[POS_IN_FEAS[g]]) + 1
    nar_g = (I.fworst - I.f0[g]) / (I.fworst - I.fopt)
    o = np.argsort(I.ff)
    sweep.append({"mu": mu, "opt": state_to_names(int(I.opt)), "opt_cost": COST[I.opt], "opt_rel": float(B[I.opt] @ r_full),
                  "greedy": state_to_names(g), "greedy_cost": COST[g], "greedy_rank": rank_g, "greedy_normAR": nar_g,
                  "gap2": float(I.ff[o[1]] - I.ff[o[0]])})
    print(f"  mu={mu:4.2f}: opt={state_to_names(int(I.opt))} ${COST[I.opt]:.2f} | greedy rank {rank_g} normAR={nar_g:.3f} {state_to_names(g)} ${COST[g]:.2f}")
res["mu_sweep"] = sweep

# ---- Pareto analysis with downstream AUC (from s05 part C) ----
pz = os.path.join(OUT, "s05_all_subsets.npz")
if os.path.exists(pz):
    z = np.load(pz); st, au, co = z["states"], z["aucs"], z["costs"]
    def pareto(stx, aux, cox):
        o = np.lexsort((-aux, cox)); front = []; best = -1
        for i in o:
            if aux[i] > best + 1e-12:
                front.append(i); best = aux[i]
        return front
    for label, mask in [("size<=5", np.ones(len(st), bool)), ("size==5", np.array([bin(int(v)).count('1') == K for v in st]))]:
        fr = pareto(st[mask], au[mask], co[mask])
        S = st[mask]; A = au[mask]; Co = co[mask]
        print(f"\nExact cost-vs-CV-AUC Pareto front ({label}): {len(fr)} panels")
        for i in fr:
            print(f"   ${Co[i]:7.2f}  AUC={A[i]:.3f}  {state_to_names(int(S[i]))}")
        res[f"pareto_{label}"] = [(float(Co[i]), float(A[i]), state_to_names(int(S[i]))) for i in fr]
    # where do the QUBO optima at each mu sit?
    aucmap = {int(a): b for a, b in zip(st, au)}
    print("\nQUBO(mu) optimum vs AUC:")
    for row in sweep:
        stt = subset_to_state([fi[f] for f in row["opt"]])
        row["opt_auc"] = aucmap[stt]
        print(f"   mu={row['mu']:4.2f} ${row['opt_cost']:7.2f} AUC={aucmap[stt]:.3f} {row['opt']}")
    # how much AUC per dollar: best AUC at each budget
    for budget in [10, 20, 50, 110, 200, 400]:
        m = co <= budget
        i = np.argmax(np.where(m, au, -1))
        print(f"   budget ${budget}: best AUC={au[i]:.3f} with {state_to_names(int(st[i]))} (${co[i]:.2f})")
        res[f"best_auc_budget_{budget}"] = (float(au[i]), state_to_names(int(st[i])), float(co[i]))

# ---- QAOA on the cost-aware instance (XY mixers), tuned on bootstrap resamples, frozen ----
MUS = [0.02, 0.05]
rng = np.random.default_rng(999)
boot = [rng.choice(len(y), int(0.8 * len(y)), replace=False) for _ in range(24)]  # 80% subsamples (bootstrap duplicates inflate kNN-MI)
RC = [(relevance(X[b], y[b], seeds=range(5))[0], redundancy(X[b])) for b in boot]
for mu in MUS:
    print(f"\nQAOA on cost-aware instance mu={mu}")
    gi_test = [greedy_cost(*RC[i], LAM, mu) == inst_mu(*RC[i], mu).opt for i in range(12, 24)]
    print(f"  greedy optimal on held-out resamples: {np.mean(gi_test):.2f}")
    for mixer, maps in [("ring", RING_MAPS), ("complete", COMPLETE_MAPS)]:
        for init in ["dicke", "greedy"]:
            def setup(r, C):
                I = inst_mu(r, C, mu)
                v0 = dicke_init() if init == "dicke" else basis_init(greedy_cost(r, C, LAM, mu))
                return I, normalise(I.ff), v0
            tr = [setup(*RC[i]) for i in range(12)]
            te = [setup(*RC[i]) for i in range(12, 24)]
            full = setup(r_full, C_full)
            for p in [1, 2]:
                def loss(th):
                    return -np.mean([I.metrics_feas(qaoa_xy(Ef, th[:p], th[p:], maps, v0))["P_opt"] for I, Ef, v0 in tr])
                best = None
                for dg in [0.3, 0.7, 1.5]:
                    for db in [0.1, 0.3, 0.6]:
                        g0, b0 = lr_schedule(p, dg, db)
                        rr = minimize(loss, np.concatenate([g0, b0]), method="Nelder-Mead", options={"maxiter": 200 * p})
                        if best is None or rr.fun < best.fun:
                            best = rr
                g, b = best.x[:p], best.x[p:]
                I, Ef, v0 = full
                pf = qaoa_xy(Ef, g, b, maps, v0)
                met = I.metrics_feas(pf)
                fullp = np.zeros(2 ** N); fullp[FEAS_IDX] = pf
                prod = product_dist(marginals_full(fullp)); pc = prod[FEAS_IDX] / prod[FEAS_IDX].sum()
                nm = I.metrics_feas(pc)
                gstate = greedy_cost(r_full, C_full, LAM, mu)
                p_better = pf[I.ff < I.f0[gstate] - 1e-12].sum()
                p_better_null = pc[I.ff < I.f0[gstate] - 1e-12].sum()
                tm = [Ii.metrics_feas(qaoa_xy(Efi, g, b, maps, v0i)) for Ii, Efi, v0i in te]
                key = f"mu{mu}_{mixer}_{init}_p{p}"
                res[key] = {"g": g, "b": b, "P_opt": met["P_opt"], "null_k_P_opt": nm["P_opt"], "mean_normAR": met["mean_normAR_feas"],
                            "null_k_mean_normAR": nm["mean_normAR_feas"], "P_better_than_greedy": p_better,
                            "null_P_better_than_greedy": p_better_null, "test_mean_P_opt": float(np.mean([t_["P_opt"] for t_ in tm])),
                            "test_min_P_opt": float(np.min([t_["P_opt"] for t_ in tm]))}
                print(f"  {mixer:8s} init={init:6s} p={p}: P(opt)={met['P_opt']:.4f} vs product-null|k {nm['P_opt']:.4f} vs uniform {1/1287:.5f}; "
                      f"meanAR {met['mean_normAR_feas']:.3f} (null {nm['mean_normAR_feas']:.3f}); P(better than greedy)={p_better:.4f} (null {p_better_null:.4f}); "
                      f"held-out mean P(opt)={res[key]['test_mean_P_opt']:.4f} min {res[key]['test_min_P_opt']:.4f}", flush=True)
save_json("s06_cost_aware.json", res)
