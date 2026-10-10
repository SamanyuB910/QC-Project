"""Follow-up to penalty_vs_xy.py:
 (1) XY mixer at p = 3..6 (equal-depth comparison with penalty p = 3..6)
 (2) penalty with P chosen WITHOUT knowing the optimum: a standard sufficient bound
     P_bound = max_i ( |r_i| + lam * sum_j c_ij )  (largest change in f from flipping one feature),
     plus 2x and 4x P_min, at p = 1..6. Angles tuned by expected energy (no oracle)."""
import json, math, time
src = open('penalty_vs_xy.py').read().split("if __name__ == '__main__':")[0]
exec(src)
KEPT = math.comb(13, 5) * (5 / 13)**5 * (8 / 13)**8

def pmin_of(f, opt_state):
    lo, hi = 0.0, 100.0
    for _ in range(60):
        mid = (lo + hi) / 2
        if (f + mid * (hw - K)**2)[~feas].min() > f[opt_state]: hi = mid
        else: lo = mid
    return hi

rows_all = []
for label, r, lam in [('prompt-like k=3 lam=0.2', relevance(3, [0]), 0.2),
                      ('ours k=10x20 lam=0.1', relevance(10, range(20)), 0.1)]:
    f = qubo_f(r, lam); f_feas = f[feas]
    opt_state = idx[feas][np.argmin(f_feas)]; opt_local = int(np.argmin(f_feas))
    Pmin = pmin_of(f, opt_state)
    Pbound = float(np.max(np.abs(r) + lam * C.sum(1)))
    print(f'\n== {label}: P_min={Pmin:.4f}  P_bound(no-oracle)={Pbound:.4f} ({Pbound/Pmin:.1f}x P_min)  Qiskit-auto=4.35 ({4.349/Pmin:.0f}x)', flush=True)
    print(f"{'method':38s} {'p':>2} {'2q':>4} {'P(opt|feas)':>11} {'P(opt)/raw':>10} {'P(feas)':>7} {'AR|feas':>7}")
    t0 = time.time()
    for p in range(1, 7):
        # XY
        v, g, b = tune(lambda g, b: run_xy(f_feas, g, b), lambda pr: (pr * f_feas).sum(), p, f_feas.std())
        pr = run_xy(f_feas, g, b); m = metrics_xy(pr, f_feas, opt_local, KEPT)
        row = dict(case=label, method='XY (free RY start)', p=p, twoq=234 * p, **m); rows_all.append(row)
        print(f"{row['method']:38s} {p:>2} {row['twoq']:>4} {m['P_opt_given_feas']:11.5f} {m['P_opt_raw']:10.5f} {m['P_feasible']:7.3f} {m['AR_feasible']:7.3f}", flush=True)
        for name, P in [('penalty P_bound (no oracle)', Pbound), ('penalty 2x P_min', 2 * Pmin), ('penalty 4x P_min', 4 * Pmin)]:
            E = f + P * (hw - K)**2
            v, g, b = tune(lambda g, b: run_x(E, g, b), lambda pr: (pr * E).sum(), p, E.std())
            pr = run_x(E, g, b); m = metrics_x(pr, f, opt_state, P)
            row = dict(case=label, method=name, p=p, twoq=78 * p, P=P, **m); rows_all.append(row)
            print(f"{name:38s} {p:>2} {row['twoq']:>4} {m['P_opt_given_feas']:11.5f} {m['P_opt_raw']:10.5f} {m['P_feasible']:7.3f} {m['AR_feasible']:7.3f}", flush=True)
    print(f'  ({time.time()-t0:.0f}s)')
json.dump(rows_all, open('followup_results.json', 'w'), indent=1, default=float)
