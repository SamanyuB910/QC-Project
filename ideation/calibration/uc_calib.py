"""Calibration (scratch, not project code): does an LR-QAOA sampler beat
product-state / uniform nulls on a real RTS-GMLC unit-commitment window?"""
import json, itertools, time, sys
import numpy as np

rng = np.random.default_rng(7)
d = json.load(open(sys.argv[1] if len(sys.argv) > 1 else 'data/2020-07-06.json'))
T = d['time_periods']
tg = d['thermal_generators']; rg = d['renewable_generators']
ren = np.zeros(T)
for g in rg.values():
    ren += np.array(g['power_output_maximum'])
net = np.array(d['demand']) - ren
res = np.array(d['reserves'])

units = []
for name, g in tg.items():
    pts = g['piecewise_production']
    mw = np.array([p['mw'] for p in pts]); c = np.array([p['cost'] for p in pts])
    segs = []  # (marginal cost, width)
    for k in range(1, len(mw)):
        w = mw[k] - mw[k-1]
        if w > 0: segs.append(((c[k]-c[k-1])/w, w))
    su = g['startup'][0]['cost'] if g['unit_on_t0'] == 0 else 0.0
    units.append(dict(name=name, pmin=g['power_output_minimum'], pmax=g['power_output_maximum'],
                      c0=c[0], segs=segs, su=su, avg=c[-1]/max(mw[-1], 1e-9), must=g['must_run']))

def dispatch(on, D, R):
    """Economic dispatch (single bus, convex piecewise costs): greedy is optimal."""
    pmin = sum(u['pmin'] for u in on); pmax = sum(u['pmax'] for u in on)
    if pmax < D + R or pmin > D:
        return np.inf
    cost = sum(u['c0'] + u['su'] for u in on)
    rem = D - pmin
    segs = sorted(s for u in on for s in u['segs'])
    for mc, w in segs:
        if rem <= 0: break
        take = min(w, rem); cost += mc * take; rem -= take
    return cost

def make_window(h, n):
    D, R = net[h], res[h]
    order = sorted(range(len(units)), key=lambda i: units[i]['avg'])
    cum = 0; k = 0
    while cum < D + R:
        cum += units[order[k]]['pmax']; k += 1
    lo = max(0, k - n // 2)
    win = order[lo:lo + n]
    fixed = [units[i] for i in order[:lo]] + [units[i] for i in order if units[i]['must'] and i not in win]
    fixed = list({u['name']: u for u in fixed}.values())
    W = [units[i] for i in win]
    return D, R, fixed, W

def all_costs(D, R, fixed, W):
    n = len(W)
    out = np.empty(2**n)
    for x in range(2**n):
        on = fixed + [W[j] for j in range(n) if (x >> (n-1-j)) & 1]
        out[x] = dispatch(on, D, R)
    return out

def qubo(D, R, fixed, W):
    n = len(W)
    # linear surrogate cost per unit: startup + cost at Pmax, normalized; quadratic coverage penalty
    a = np.array([u['su'] + u['c0'] + sum(mc*w for mc, w in u['segs']) for u in W])
    P = np.array([u['pmax'] for u in W])
    target = D + R - sum(u['pmax'] for u in fixed)
    target = max(target, 0)
    lam = 2.0 * a.max() / (P.mean()**2)
    # E(x) = sum a x + lam (P.x - target)^2
    J = lam * np.outer(P, P); np.fill_diagonal(J, 0)
    hlin = a + lam * (P**2 - 2*target*P)
    return hlin, J, lam*target**2

def energies(hlin, J, const, n):
    xs = ((np.arange(2**n)[:, None] >> np.arange(n-1, -1, -1)) & 1).astype(float)
    return xs @ hlin + 0.5 * np.einsum('bi,ij,bj->b', xs, J, xs) + const, xs

def lr_qaoa(E, n, p, dg, db):
    En = (E - E.mean()) / (np.abs(E - E.mean()).max())
    psi = np.full(2**n, 2**(-n/2), dtype=complex)
    for k in range(p):
        g = (k+1)/p * dg; b = (1 - k/p) * db
        psi *= np.exp(-1j * g * En)
        # mixer exp(-i b X) on each qubit
        c, s = np.cos(b), 1j*np.sin(b)  # exp(+i b X): |+> is ground state of -X, anneal to MIN of E
        psi = psi.reshape([2]*n)
        for q in range(n):
            psi = np.moveaxis(psi, q, 0)
            a0, a1 = psi[0].copy(), psi[1].copy()
            psi[0] = c*a0 + s*a1; psi[1] = s*a0 + c*a1
            psi = np.moveaxis(psi, 0, q)
        psi = psi.reshape(-1)
    return np.abs(psi)**2

def metrics(prob, cost, opt):
    good1 = cost <= opt * 1.01; good2 = cost <= opt*1.02
    feas = np.isfinite(cost)
    return prob[good1].sum(), prob[good2].sum(), prob[feas].sum()

if __name__ == '__main__':
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 12
    hours = [int(x) for x in sys.argv[3].split(',')] if len(sys.argv) > 3 else [8, 14, 17, 20]
    for h in hours:
        t0 = time.time()
        D, R, fixed, W = make_window(h, n)
        cost = all_costs(D, R, fixed, W)
        opt = cost.min()
        hlin, J, const = qubo(D, R, fixed, W)
        E, xs = energies(hlin, J, const, n)
        uni = np.full(2**n, 2.0**-n)
        best = None
        for p in [1, 2, 3, 5, 8]:
            for dg in np.linspace(0.2, 3.0, 15):
                for db in np.linspace(0.1, 1.5, 15):
                    pr = lr_qaoa(E, n, p, dg, db)
                    m = metrics(pr, cost, opt)
                    if best is None or m[0] > best[0][0]:
                        best = (m, p, dg, db, pr)
        (q1, q2, qf), p, dg, db, pr = best
        # product-state null with QAOA's own marginals (removes correlations)
        marg = (pr[:, None] * xs).sum(0)
        prod = np.prod(np.where(xs == 1, marg, 1 - marg), axis=1)
        # product-state null with best uniform bias per qubit from surrogate (greedy warm start)
        n1 = metrics(prod, cost, opt)
        nu = metrics(uni, cost, opt)
        # priority list: commit window units in merit order until feasible
        pl = np.inf
        for k in range(n+1):
            x = sum(1 << (n-1-j) for j in range(k))
            if np.isfinite(cost[x]): pl = cost[x]; break
        gap_pl = (pl/opt - 1)*100
        ising_opt = cost[np.argmin(E)]
        print(f"h={h:2d} D={D:7.1f} R={R:5.1f} fixed={len(fixed)} | opt=${opt:,.0f} PL gap={gap_pl:.2f}% QUBO-argmin gap={(ising_opt/opt-1)*100:.2f}% | "
              f"QAOA p={p} dg={dg:.2f} db={db:.2f}: P1%={q1:.3f} P2%={q2:.3f} feas={qf:.2f} | "
              f"prod-null P1%={n1[0]:.3f} feas={n1[2]:.2f} | uniform P1%={nu[0]:.4f} feas={nu[2]:.2f} | n_opt1%={int((cost<=opt*1.01).sum())} | {time.time()-t0:.1f}s")
