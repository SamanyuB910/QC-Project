"""Prompt C, step 5: unknown M. BBHT exponential search (Boyer, Brassard, Hoyer, Tapp 1998)
vs classical baselines, over many random real catalog slices (2024 USGS M>=5, contiguous windows).

Cost accounting (expensive-black-box model): every Grover iteration = 1 oracle call (1 predicate evaluation
in superposition); every measured candidate is VERIFIED classically = 1 predicate evaluation.
Classical random-order scan: checks until first match (expected (N+1)/(M+1)); M=0 needs N checks to certify.
Indexed baseline: B-tree on magnitude -> log2(N) comparisons + check depth of each row with mag>=thr.

Measurement outcomes are sampled from the exact Grover law P=sin^2((2j+1)theta) (ideal), or from the
global-depolarizing model P=F*P_ideal+(1-F)*M/N with F from transpiled 2Q counts at IonQ forte-1 rates
(validated against density-matrix sims in c04).
"""
import json, os, math, warnings
import numpy as np
warnings.filterwarnings("ignore")
import gs_core as G

rows = G.load_catalog()
LAM = 6 / 5

# per-n 2Q cost of one MCZ on n qubits and of the diffusion (IonQ-like transpile), for the noise model
mcz2q = {}
for n in range(3, 11):
    mcz2q[n] = G.twoq(G.to_ionq(G.list_oracle(n, [2**n - 1])))
print("2Q per n-qubit MCZ (Qiskit ancilla-free synthesis, rzz basis):", mcz2q)

def p_succ(N, M, j, noisy, n):
    if M == 0: return 0.0
    p = G.p_success_theory(N, M, j)
    if not noisy: return p
    g2 = j * (M + 1) * mcz2q[n]                  # M oracle MCZs + 1 diffusion MCZ per iteration
    F = (1 - 15 / 16 * G.P2) ** g2
    return F * p + (1 - F) * M / N

def bbht(N, M, n, rng, noisy=False, budget=None):
    """returns (oracle_calls, verify_checks, found:bool)"""
    m, calls, checks = 1.0, 0, 0
    while True:
        j = int(rng.integers(0, max(1, math.ceil(m))))   # uniform in [0, m)
        if budget is not None and calls + j > budget:
            return calls, checks, False
        calls += j; checks += 1
        if rng.random() < p_succ(N, M, j, noisy, n):
            return calls, checks, True
        m = min(LAM * m, math.sqrt(N))

def classical_first(N, M, rng):
    if M == 0: return N
    perm = rng.permutation(N)
    return int(np.argmax(perm < M)) + 1                  # positions of the M matches = labels < M

def boot_ci(x, rng, B=2000):
    x = np.asarray(x, float); bs = rng.choice(x, size=(B, len(x)), replace=True).mean(1)
    return float(x.mean()), float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))

rng = np.random.default_rng(42)
# 1) calibrate a stopping budget for the M=0 case: smallest c such that P(miss | M=1) <= 5% (ideal)
calib = {}
for n in range(3, 11):
    N = 2**n
    for c in np.arange(1.0, 12.01, 0.25):
        B = c * math.sqrt(N)
        miss = np.mean([not bbht(N, 1, n, rng, budget=B)[2] for _ in range(4000)])
        if miss <= 0.05: calib[n] = float(c); break
print("BBHT stop budget c*sqrt(N) giving P(miss|M=1)<=5%:", calib)

S, R = 3000, 1
summary = []
for n in range(3, 7):
    N = 2**n
    sl_list = [G.slice_events(rows, n, rng) for _ in range(S)]
    Ms = np.array([len(G.marked_indices(s)) for s in sl_list])
    q_id, q_ny, cl, idx_cost, ck_id, ck_ny, found_id, found_ny = [], [], [], [], [], [], [], []
    for s, M in zip(sl_list, Ms):
        B = calib[n] * math.sqrt(N)
        a = bbht(N, M, n, rng, noisy=False, budget=B); b = bbht(N, M, n, rng, noisy=True, budget=B)
        q_id.append(a[0] + a[1]); ck_id.append(a[1]); found_id.append(a[2] == (M > 0))
        q_ny.append(b[0] + b[1]); ck_ny.append(b[1]); found_ny.append(b[2] == (M > 0))
        cl.append(classical_first(N, M, rng))
        k_mag = sum(1 for r in s if r["mag"] >= G.MAG_THR)
        idx_cost.append(math.ceil(math.log2(N)) + k_mag)
    q_id, q_ny, cl, idx_cost = map(np.array, (q_id, q_ny, cl, idx_cost))
    pos = Ms > 0
    rec = dict(n=n, N=N, slices=S, frac_M0=float(np.mean(~pos)), mean_M=float(Ms.mean()))
    for name, arr in [("bbht_ideal_total_evals", q_id), ("bbht_noisy_total_evals", q_ny), ("classical_scan_checks", cl), ("indexed_rows_touched", idx_cost)]:
        rec[name + "_M>=1"] = boot_ci(arr[pos], rng)
        rec[name + "_M=0"] = boot_ci(arr[~pos], rng) if (~pos).any() else None
    rec["classical_theory_mean_M>=1"] = float(np.mean((N + 1) / (Ms[pos] + 1)))
    rec["bbht_correct_rate_ideal"] = float(np.mean(found_id)); rec["bbht_correct_rate_noisy"] = float(np.mean(found_ny))
    rec["ratio_classical_over_bbht_ideal_M>=1"] = float(cl[pos].mean() / q_id[pos].mean())
    rec["bbht_win_fraction_ideal_M>=1"] = float(np.mean(q_id[pos] < cl[pos]))
    summary.append(rec)
    f = lambda t: f"{t[0]:6.2f} [{t[1]:.2f},{t[2]:.2f}]" if t else "   n/a"
    print(f"\nn={n} N={N}: P(M=0)={rec['frac_M0']:.3f}, mean M={rec['mean_M']:.2f}")
    print(f"  M>=1: BBHT ideal evals {f(rec['bbht_ideal_total_evals_M>=1'])} | BBHT noisy {f(rec['bbht_noisy_total_evals_M>=1'])} | "
          f"classical scan {f(rec['classical_scan_checks_M>=1'])} (theory {rec['classical_theory_mean_M>=1']:.2f}) | indexed {f(rec['indexed_rows_touched_M>=1'])}")
    print(f"  M=0 : BBHT ideal {f(rec['bbht_ideal_total_evals_M=0'])} | classical {f(rec['classical_scan_checks_M=0'])} | indexed {f(rec['indexed_rows_touched_M=0'])}")
    print(f"  correct (find-or-certify-none) rate: ideal {rec['bbht_correct_rate_ideal']:.3f}, noisy {rec['bbht_correct_rate_noisy']:.3f}; "
          f"BBHT beats scan on {100*rec['bbht_win_fraction_ideal_M>=1']:.1f}% of M>=1 slices")

# 2) scaling with N at fixed M=1 (needle) and at the real rate, ideal & noisy (synthetic sizes up to n=10)
print("\nScaling at M=1 (needle): mean total evaluations over 4000 runs (calls + verification checks)")
scal = []
for n in range(3, 11):
    N = 2**n
    qi = [sum(bbht(N, 1, n, rng)[:2]) for _ in range(4000)]
    qn = [sum(bbht(N, 1, n, rng, noisy=True, budget=50 * math.sqrt(N))[:2]) for _ in range(4000)]
    rec = dict(n=n, N=N, bbht_ideal=float(np.mean(qi)), bbht_noisy=float(np.mean(qn)), classical=(N + 1) / 2,
               ratio_to_sqrtN=float(np.mean(qi) / math.sqrt(N)))
    scal.append(rec)
    print(f"  n={n:2d} N={N:5d}: BBHT ideal {rec['bbht_ideal']:7.2f} ({rec['ratio_to_sqrtN']:.2f} sqrtN) | BBHT noisy {rec['bbht_noisy']:7.2f} | classical (N+1)/2 = {rec['classical']:.1f}")

json.dump(dict(stop_budget_c=calib, per_n=summary, needle_scaling=scal, mcz2q=mcz2q),
          open(os.path.join(G.HERE, "results_c05_bbht.json"), "w"), indent=1)
