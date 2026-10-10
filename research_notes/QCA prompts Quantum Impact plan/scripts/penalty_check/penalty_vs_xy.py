"""Independent check (fresh code, no reuse of prompt_b/qsim.py):
Penalty-QAOA (X mixer, |+> start) vs constraint-preserving XY-QAOA (Dicke start)
on the Prompt B heart-disease QUBO, choose exactly k=5 of 13.

Fairness rules:
  * penalty P swept from the smallest value that makes the true optimum the global
    minimum (P_min) up to 10x P_min, plus ~4.35 (Qiskit's auto value found earlier)
  * angles tuned two ways for BOTH methods:
      (a) standard QAOA practice: minimise expected energy (no knowledge of the optimum)
      (b) oracle best case: maximise P(optimum) directly (generous upper bound)
  * comparisons at equal depth p AND at equal two-qubit-gate budget
  * per-raw-shot accounting: XY with the free RY start keeps only weight-5 shots (22.3%)
"""
import json, sys, time, itertools
import numpy as np, pandas as pd
from scipy.optimize import minimize
from sklearn.feature_selection import mutual_info_classif

df = pd.read_csv(r'C:\VS Code Projects\QC Hackathon\research_notes\QCA prompts Quantum Impact plan\scripts\prompt_b\heart_cleveland_297.csv')
FEATS = ['age','sex','cp','trestbps','chol','fbs','restecg','thalach','exang','oldpeak','slope','ca','thal']
X = df[FEATS].to_numpy(float); y = df['target'].to_numpy(int)
n, K = 13, 5
N = 2**n
idx = np.arange(N)
bits = ((idx[:, None] >> np.arange(n)) & 1).astype(float)      # x_i = bit i (Qiskit little-endian)
hw = bits.sum(1).astype(int)
feas = hw == K
C = np.abs(np.corrcoef(X.T)); np.fill_diagonal(C, 0)

def relevance(nn, seeds):
    return np.mean([mutual_info_classif(X, y, n_neighbors=nn, random_state=s) for s in seeds], axis=0)

def qubo_f(r, lam):
    return -(bits @ r) + lam * 0.5 * np.einsum('si,ij,sj->s', bits, C, bits)

# ---------- simulators ----------
P0 = [idx[((idx >> q) & 1) == 0] for q in range(n)]
P1 = [p0 | (1 << q) for q, p0 in enumerate(P0)]

def run_x(E, gammas, betas):
    psi = np.full(N, N**-0.5, complex)
    for g, b in zip(gammas, betas):
        psi = psi * np.exp(-1j * g * E)
        c, s = np.cos(b), -1j * np.sin(b)              # exp(-i b X) per qubit
        for q in range(n):
            a0, a1 = psi[P0[q]], psi[P1[q]]
            psi[P0[q]], psi[P1[q]] = c * a0 + s * a1, s * a0 + c * a1
    return np.abs(psi)**2

FE = idx[feas]                                       # 1287 weight-5 states
pos = {s: i for i, s in enumerate(FE)}
PAIRS = list(itertools.combinations(range(n), 2))    # 78 pairs, fixed order
SWAP = []
for i, j in PAIRS:
    a, b = [], []
    for s in FE:
        if ((s >> i) & 1) == 1 and ((s >> j) & 1) == 0:
            t = s ^ (1 << i) ^ (1 << j); a.append(pos[s]); b.append(pos[t])
    SWAP.append((np.array(a), np.array(b)))

def run_xy(f_feas, gammas, betas):
    psi = np.full(len(FE), len(FE)**-0.5, complex)   # Dicke state
    for g, b in zip(gammas, betas):
        psi = psi * np.exp(-1j * g * f_feas)
        c, s = np.cos(b), -1j * np.sin(b)            # XXPlusYY on each pair, restricted to subspace
        for a_, b_ in SWAP:
            u, v = psi[a_], psi[b_]
            psi[a_], psi[b_] = c * u + s * v, s * u + c * v
    return np.abs(psi)**2

# ---------- metrics ----------
def metrics_x(prob, f, opt_state, P):
    pf = prob[feas].sum()
    fv = f[feas]; fmin, fmax = fv.min(), fv.max()
    ar = ((fmax - f[feas]) / (fmax - fmin) * prob[feas]).sum() / max(pf, 1e-15)
    top10 = idx[feas][np.argsort(f[feas])[:10]]
    return dict(P_feasible=pf, P_opt_raw=prob[opt_state], P_opt_given_feas=prob[opt_state] / max(pf, 1e-15),
                AR_feasible=ar, P_top10_raw=prob[top10].sum())

def metrics_xy(prob, f_feas, opt_local, kept=1.0):
    fmin, fmax = f_feas.min(), f_feas.max()
    ar = ((fmax - f_feas) / (fmax - fmin) * prob).sum()
    top10 = np.argsort(f_feas)[:10]
    return dict(P_feasible=kept, P_opt_raw=kept * prob[opt_local], P_opt_given_feas=prob[opt_local],
                AR_feasible=ar, P_top10_raw=kept * prob[top10].sum())

# ---------- tuning (linear-ramp schedule, 2 params, then full refine for p<=3) ----------
def schedule(dg, db, p):
    return [(k + 1) / p * dg for k in range(p)], [(1 - k / p) * db for k in range(p)]

def tune(sim, score, p, gscale):
    best = None
    for dg in np.concatenate([-np.geomspace(1e-2, 1e2, 30), np.geomspace(1e-2, 1e2, 30)]) / gscale:
        for db in np.linspace(-np.pi / 2, np.pi / 2, 25):
            g, b = schedule(dg, db, p); v = score(sim(g, b))
            if best is None or v < best[0]: best = (v, g, b)
    if p <= 3:   # full-parameter refinement from the best ramp point
        x0 = np.array(best[1] + best[2])
        res = minimize(lambda x: score(sim(x[:p], x[p:])), x0, method='Nelder-Mead',
                       options=dict(maxiter=600 * p, xatol=1e-6, fatol=1e-10))
        if res.fun < best[0]: best = (res.fun, list(res.x[:p]), list(res.x[p:]))
    return best

import math; KEPT_RY = math.comb(13, 5) * (5 / 13)**5 * (8 / 13)**8

def study(label, r, lam, pmax=6):
    f = qubo_f(r, lam)
    opt_state = idx[feas][np.argmin(f[feas])]
    f_feas = f[feas]; opt_local = int(np.argmin(f_feas))
    # P_min: smallest P so that every infeasible state has E_P > f(opt)
    lo, hi = 0.0, 100.0
    for _ in range(60):
        mid = (lo + hi) / 2
        Ep = f + mid * (hw - K)**2
        if Ep[~feas].min() > f[opt_state]: hi = mid
        else: lo = mid
    Pmin = hi
    gs_xy = f_feas.std()
    out = dict(label=label, lam=lam, optimum=[FEATS[i] for i in range(n) if (opt_state >> i) & 1],
               f_opt=float(f[opt_state]), f_spread_feasible=float(f_feas.max() - f_feas.min()),
               P_min=Pmin, uniform_k_subset_P_opt=1 / 1287, KEPT_RY=KEPT_RY, rows=[])
    t0 = time.time()
    for p in range(1, pmax + 1):
        # XY (only up to p=2: gate budget 234/layer)
        if p <= 2:
            for mode in ['energy', 'oracle']:
                sim = lambda g, b: run_xy(f_feas, g, b)
                score = (lambda pr: (pr * f_feas).sum()) if mode == 'energy' else (lambda pr: -pr[opt_local])
                v, g, b = tune(sim, score, p, gs_xy)
                pr = sim(g, b)
                m_dicke = metrics_xy(pr, f_feas, opt_local, 1.0)
                m_ry = metrics_xy(pr, f_feas, opt_local, KEPT_RY)
                out['rows'].append(dict(method='XY mixer, exact Dicke start', p=p, twoq=234 * p + 290, tune=mode, **m_dicke))
                out['rows'].append(dict(method='XY mixer, free RY start + keep weight-5', p=p, twoq=234 * p, tune=mode, **m_ry))
        for mult in ([0.5, 1, 2, 10, 'qiskit~4.35'] if p <= 2 else [1, 'qiskit~4.35']):
            P = 4.349 if mult == 'qiskit~4.35' else mult * Pmin
            E = f + P * (hw - K)**2
            sim = lambda g, b: run_x(E, g, b)
            for mode in (['energy', 'oracle'] if mult in (1, 2) else ['energy']):
                score = (lambda pr: (pr * E).sum()) if mode == 'energy' else (lambda pr: -pr[opt_state])
                v, g, b = tune(sim, score, p, E.std())
                pr = sim(g, b)
                out['rows'].append(dict(method=f'penalty P={mult}xPmin' if mult != 'qiskit~4.35' else 'penalty P=4.35 (Qiskit auto)',
                                        p=p, twoq=78 * p, tune=mode, P=P, **metrics_x(pr, f, opt_state, P)))
        print(f'  {label}: p={p} done ({time.time()-t0:.0f}s)', flush=True)
    return out

if __name__ == '__main__':
    cases = [('prompt-like: kNN-MI k=3 seed0, lambda=0.2', relevance(3, [0]), 0.2),
             ('ours: kNN-MI k=10 avg 20 seeds, lambda=0.1', relevance(10, range(20)), 0.1)]
    results = [study(*c) for c in cases]
    json.dump(results, open(r'C:\VS Code Projects\QC Hackathon\research_notes\QCA prompts Quantum Impact plan\scripts\penalty_check\results.json', 'w'), indent=1, default=float)
    for R in results:
        print('\n==', R['label'], '| optimum', R['optimum'], '| P_min=%.4f' % R['P_min'], '| random 5-subset P(opt)=%.5f' % R['uniform_k_subset_P_opt'])
        print(f"{'method':44s} {'p':>2} {'2q':>4} {'tune':6s} {'P(feas)':>7} {'P(opt)/raw shot':>15} {'P(opt|feas)':>11} {'AR|feas':>7} {'top10/raw':>9}")
        for row in R['rows']:
            if row['tune'] == 'energy' or 'Pmin' not in row['method'] or row['method'].startswith('penalty P=1x') or row['method'].startswith('XY'):
                print(f"{row['method']:44s} {row['p']:>2} {row['twoq']:>4} {row['tune']:6s} {row['P_feasible']:7.3f} {row['P_opt_raw']:15.5f} {row['P_opt_given_feas']:11.5f} {row['AR_feasible']:7.3f} {row['P_top10_raw']:9.4f}")
