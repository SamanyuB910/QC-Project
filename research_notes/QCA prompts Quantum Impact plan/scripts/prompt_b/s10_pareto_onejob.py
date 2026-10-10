"""Step 10: the recommended build, end to end, as ONE IonQ job.
Formulation: debiased relevance (kNN-MI k=10, 20 seeds), lam=0.1, Turney cost HUBO (cubic exercise-ECG term), k=5 via XY
complete mixer, product-RY start + post-selection on Hamming weight 5 (== Dicke start, 0 extra 2Q gates).
One schedule (gamma, beta), p=1, tuned on 80% subsamples (no oracle), shared by 5 circuits mu in MU_GRID -> one
backend.run([5 circuits]). Measures: recovery of the exact cost-vs-score Pareto set and the cost-vs-CV-AUC front from the
union of samples, against uniform k-subsets and the product-of-marginals null at matched feasible-sample counts.
Also runs the 5 circuits under Aer depolarizing noise at IonQ forte-1 rates."""
import sys, time
import numpy as np
from scipy.optimize import minimize
from common import *
from qsim import *
from s06_helpers import cost_vector

KNN, LAM = 10, 0.1
MU_GRID = [0.0, 0.02, 0.05, 0.1, 0.2]
SHOTS = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
X, y, _ = load_data()
COST = cost_vector()
r_full = relevance(X, y, n_neighbors=KNN)[0]; C_full = redundancy(X)
rng = np.random.default_rng(4242)
subs = [rng.choice(len(y), int(0.8 * len(y)), replace=False) for _ in range(12)]
RC = [(relevance(X[s], y[s], seeds=range(5), n_neighbors=KNN)[0], redundancy(X[s])) for s in subs]
P_HW5 = 0.2227844551478433


def inst(r, C, mu):
    return Inst(r, C, LAM, extra=mu * COST / 100)


train = [(I, normalise(I.ff)) for (r, C) in RC for I in [inst(r, C, mu) for mu in MU_GRID]]


def loss(th, p=1):
    return -np.mean([I.metrics_feas(qaoa_xy(Ef, th[:p], th[p:], COMPLETE_MAPS, dicke_init()))["P_opt"] for I, Ef in train])


best = None
for g0 in [0.3, 0.6, 1.0, 1.5]:
    for b0 in [0.05, 0.1, 0.2, 0.4]:
        rr = minimize(loss, [g0, b0], method="Nelder-Mead", options={"maxiter": 200})
        if best is None or rr.fun < best.fun:
            best = rr
g, b = best.x[:1], best.x[1:]
print(f"frozen schedule (tuned on {len(train)} training instances = 12 subsamples x 5 mu): gamma={g[0]:.4f} beta={b[0]:.4f}, "
      f"train mean P(opt|HW5)={-best.fun:.4f}", flush=True)

# exact frontier of the QUBO family on the full data: union of optima over the mu grid, and the full (cost, score) Pareto set
score = np.array([Inst(r_full, C_full, LAM).f0[s] for s in FEAS_IDX])  # relevance-redundancy score (lower better)
cost5 = COST[FEAS_IDX]
o = np.lexsort((score, cost5)); pareto = []; bestf = np.inf
for i in o:
    if score[i] < bestf - 1e-12:
        pareto.append(i); bestf = score[i]
pareto_states = set(FEAS_IDX[pareto].tolist())
mu_opts = {mu: int(inst(r_full, C_full, mu).opt) for mu in MU_GRID}
print(f"exact (cost, score) Pareto set: {len(pareto_states)} panels; mu-grid optima: " +
      "; ".join(f"mu={mu}: {state_to_names(s)} ${COST[s]:.2f}" for mu, s in mu_opts.items()), flush=True)
z = np.load(os.path.join(OUT, "s05_all_subsets.npz"))
auc = dict(zip(z["states"].tolist(), z["aucs"]))
auc5 = np.array([auc[int(s)] for s in FEAS_IDX])
oa = np.lexsort((-auc5, cost5)); auc_front = []; ba = -1
for i in oa:
    if auc5[i] > ba + 1e-12:
        auc_front.append(i); ba = auc5[i]
auc_front_states = set(FEAS_IDX[auc_front].tolist())


def front_quality(states):
    """states: iterable of sampled feasible states. Returns (#mu-optima found, #exact score-Pareto panels found,
    #AUC-front panels found, AUC-front hypervolume ratio over cost in [0, 320], AUC baseline 0.5)."""
    S = set(int(s) for s in states)
    def hv(stset):
        pts = sorted((COST[s], auc[s]) for s in stset)
        area, cur, last = 0.0, 0.5, 0.0
        # staircase: best AUC achievable at cost <= c, integrated over c in [0, 320]
        grid = np.linspace(0, 320, 3201)
        bestv = np.full(len(grid), 0.5)
        for c, a in pts:
            bestv[grid >= c] = np.maximum(bestv[grid >= c], a)
        return np.trapz(bestv - 0.5, grid)
    ref = hv(auc_front_states)
    return (sum(1 for s in mu_opts.values() if s in S), len(S & pareto_states), len(S & auc_front_states), hv(S) / ref if S else 0.0)


# ideal QAOA distributions per mu (HW5-conditional) + product null|k
dists, nulls = {}, {}
for mu in MU_GRID:
    I = inst(r_full, C_full, mu)
    pf = qaoa_xy(normalise(I.ff), g, b, COMPLETE_MAPS, dicke_init())
    dists[mu] = pf / pf.sum()
    fullp = np.zeros(2 ** N); fullp[FEAS_IDX] = pf
    prod = product_dist(marginals_full(fullp))[FEAS_IDX]; nulls[mu] = prod / prod.sum()
    print(f"  mu={mu:4.2f}: ideal P(opt|HW5)={dists[mu][POS_IN_FEAS[I.opt]]:.4f}  null|k={nulls[mu][POS_IN_FEAS[I.opt]]:.4f}  uniform={1/1287:.5f}", flush=True)

# matched-sample comparison: each circuit gets SHOTS raw shots -> Binomial(SHOTS, P_HW5) feasible samples
R = 200
res = {"gamma": g, "beta": b, "pareto_size": len(pareto_states), "auc_front_size": len(auc_front_states), "rows": {}}
for name in ["QAOA_ideal", "product_null_k", "uniform_k"]:
    qs = []
    for rep in range(R):
        rs = np.random.default_rng(rep)
        samp = []
        for mu in MU_GRID:
            nf = rs.binomial(SHOTS, P_HW5)
            if name == "QAOA_ideal":
                pr = dists[mu]
            elif name == "product_null_k":
                pr = nulls[mu]
            else:
                pr = np.full(1287, 1 / 1287)
            samp += FEAS_IDX[rs.choice(1287, nf, p=pr)].tolist()
        qs.append(front_quality(samp))
    qs = np.array(qs)
    res["rows"][name] = {"mu_optima_found_mean": qs[:, 0].mean(), "pareto_found_mean": qs[:, 1].mean(),
                         "auc_front_found_mean": qs[:, 2].mean(), "auc_hv_ratio_mean": qs[:, 3].mean(),
                         "auc_hv_ratio_p5": np.percentile(qs[:, 3], 5), "all5_mu_optima_rate": (qs[:, 0] == 5).mean()}
    print(f"{name:15s} ({SHOTS} raw shots x 5 circuits, ~{int(SHOTS*P_HW5)} feasible each): mu-optima found {qs[:,0].mean():.2f}/5 "
          f"(all 5 in {100*(qs[:,0]==5).mean():.0f}% of runs); exact score-Pareto panels found {qs[:,1].mean():.1f}/{len(pareto_states)}; "
          f"AUC-front panels {qs[:,2].mean():.2f}/{len(auc_front_states)}; AUC hypervolume ratio {qs[:,3].mean():.3f} (5th pct {np.percentile(qs[:,3],5):.3f})", flush=True)

# noisy run of the actual 5-circuit job (Aer, forte-1 depolarizing rates)
from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import XXPlusYYGate
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error


def circuit(mu):
    I = inst(r_full, C_full, mu)
    E = I.f0  # full 2^13 energy incl. cost polynomial (HUBO)
    sd, mean = I.ff.std(), I.ff.mean()
    # exact Walsh-Hadamard expansion of the diagonal into Z-strings (keeps the cubic term exactly)
    Bm = BITS.astype(float); Zs = 1 - 2 * Bm
    terms = {}
    from itertools import combinations
    for order in [1, 2, 3]:
        for S in combinations(range(N), order):
            c = float((E * np.prod(Zs[:, list(S)], axis=1)).mean())
            if abs(c) > 1e-10:
                terms[S] = c
    qc = QuantumCircuit(N)
    th = 2 * np.arcsin(np.sqrt(K / N))
    for q in range(N):
        qc.ry(th, q)
    for S, c in terms.items():
        ang = 2 * g[0] * c / sd
        if len(S) == 1:
            qc.rz(ang, S[0])
        elif len(S) == 2:
            qc.rzz(ang, *S)
        else:
            a, b_, c_ = S
            qc.cx(a, c_); qc.cx(b_, c_); qc.rz(ang, c_); qc.cx(b_, c_); qc.cx(a, c_)
    for (i, j) in complete_pairs():
        qc.append(XXPlusYYGate(-2 * b[0]), [i, j])
    qc.measure_all()
    # check that the term expansion reproduces E up to a constant
    return qc, terms


noise = NoiseModel()
noise.add_all_qubit_quantum_error(depolarizing_error(2.67e-4, 1), ["rx", "rz"])
noise.add_all_qubit_quantum_error(depolarizing_error(4.95e-3, 2), ["rzz"])
sim = AerSimulator(noise_model=noise, method="statevector", seed_simulator=5)
circs = []
for mu in MU_GRID:
    qc, terms = circuit(mu)
    circs.append(transpile(qc, basis_gates=["rzz", "rx", "rz"], optimization_level=2, seed_transpiler=1))
n2 = [c.count_ops().get("rzz", 0) for c in circs]
print(f"\nOne job = {len(circs)} circuits; 2Q (rzz) per circuit: {n2}; total 2Q in job {sum(n2)}; cubic terms per circuit: "
      f"{sum(1 for S in terms if len(S) == 3)}", flush=True)
t = time.time()
job = sim.run(circs, shots=SHOTS).result()
print(f"Aer noisy run of the whole job: {time.time()-t:.1f}s", flush=True)
samp = []; hw5_frac = []
for i, mu in enumerate(MU_GRID):
    cnt = job.get_counts(i)
    tot = sum(cnt.values())
    keep = {int(k_, 2): v for k_, v in cnt.items() if k_.count("1") == K}
    hw5_frac.append(sum(keep.values()) / tot)
    I = inst(r_full, C_full, mu)
    hits = keep.get(int(I.opt), 0); nf = sum(keep.values())
    print(f"  noisy mu={mu:4.2f}: P(HW5)={nf/tot:.3f}  P(opt|HW5)={hits/max(nf,1):.4f} {wilson(hits, max(nf,1))}", flush=True)
    for s_, v in keep.items():
        samp += [s_] * v
qn = front_quality(samp)
print(f"QAOA noisy (forte-1 depolarizing): mu-optima found {qn[0]}/5; score-Pareto panels {qn[1]}/{len(pareto_states)}; "
      f"AUC-front panels {qn[2]}/{len(auc_front_states)}; AUC hypervolume ratio {qn[3]:.3f}", flush=True)
res["noisy"] = {"P_HW5": hw5_frac, "front_quality": qn, "rzz_per_circuit": n2}
save_json("s10_pareto_onejob.json", res)
