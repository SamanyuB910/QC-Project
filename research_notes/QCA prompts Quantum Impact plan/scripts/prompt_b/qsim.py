"""Small exact QAOA simulators for the 13-qubit Prompt B problem (numpy, statevector).

Conventions (match the Qiskit circuits built in s04):
  cost layer      exp(-i * gamma * E_norm)            (E_norm = (E - mean)/std over the mixer's reachable space)
  X mixer         prod_q exp(+i * beta * X_q)         (|+>^n is the ground state of -sum X; anneal towards MIN E)
                  == RX(-2*beta) on each qubit
  XY mixer        prod_(a,b) exp(+i * beta * (XX+YY)/2) applied pair by pair in a fixed order (Trotterised, as the
                  circuit does); == XXPlusYYGate(-2*beta) per pair. Preserves Hamming weight.
State index s: qubit/feature i is |1> (kept) iff bit i of s is set.
"""
import numpy as np
from common import N, K, BITS, HW, FEAS, FEAS_IDX, ALL

POS_IN_FEAS = -np.ones(2 ** N, dtype=int)
POS_IN_FEAS[FEAS_IDX] = np.arange(len(FEAS_IDX))


def ring_pairs(n=N):
    edges = [(i, (i + 1) % n) for i in range(n)]
    even = [e for e in edges if e[0] % 2 == 0 and e[0] != n - 1]
    odd = [e for e in edges if e[0] % 2 == 1]
    last = [e for e in edges if e[0] == n - 1]
    return even + odd + last


def complete_pairs(n=N):
    # round-robin (circle method) ordering so each round is a parallel layer of disjoint pairs
    m = n + 1 if n % 2 else n
    players = list(range(m))
    rounds = []
    for _ in range(m - 1):
        rnd = []
        for i in range(m // 2):
            a, b = players[i], players[m - 1 - i]
            if a < n and b < n:
                rnd.append((min(a, b), max(a, b)))
        rounds.append(rnd)
        players = [players[0]] + [players[-1]] + players[1:-1]
    return [p for rnd in rounds for p in rnd]


def _pair_maps_feasible(pairs):
    """For each pair (a,b): indices (within the 1287 feasible list) of states with a=1,b=0 and their partner a=0,b=1."""
    maps = []
    for a, b in pairs:
        sel = FEAS_IDX[(BITS[FEAS_IDX, a] == 1) & (BITS[FEAS_IDX, b] == 0)]
        partner = sel ^ (1 << a) ^ (1 << b)
        maps.append((POS_IN_FEAS[sel], POS_IN_FEAS[partner]))
    return maps


RING_MAPS = _pair_maps_feasible(ring_pairs())
COMPLETE_MAPS = _pair_maps_feasible(complete_pairs())


def apply_x_mixer(psi, beta):
    c, s = np.cos(beta), 1j * np.sin(beta)
    psi = psi.reshape([2] * N)
    for q in range(N):
        ax = N - 1 - q  # reshape is big-endian: axis 0 is the highest bit
        psi = np.moveaxis(psi, ax, 0)
        a0, a1 = psi[0].copy(), psi[1].copy()
        psi[0] = c * a0 + s * a1
        psi[1] = s * a0 + c * a1
        psi = np.moveaxis(psi, 0, ax)
    return psi.reshape(-1)


def apply_xy_feasible(phi, beta, maps):
    c, s = np.cos(beta), 1j * np.sin(beta)
    for i10, i01 in maps:
        a, b = phi[i10].copy(), phi[i01].copy()
        phi[i10] = c * a + s * b
        phi[i01] = s * a + c * b
    return phi


def normalise(E, mask=None):
    v = E if mask is None else E[mask]
    mu, sd = v.mean(), v.std()
    return (E - mu) / sd


def qaoa_x(E, gammas, betas, init=None):
    """Penalty QAOA with X mixer on the full 2^13 space. E must already be normalised. Returns probabilities."""
    psi = np.full(2 ** N, 2 ** (-N / 2), dtype=complex) if init is None else init.astype(complex).copy()
    for g, b in zip(gammas, betas):
        psi = psi * np.exp(-1j * g * E)
        psi = apply_x_mixer(psi, b)
    return np.abs(psi) ** 2


def qaoa_xy(Ef, gammas, betas, maps, init):
    """XY-mixer QAOA restricted to the 1287-dim Hamming-weight-5 subspace. Ef: normalised energies on FEAS_IDX order.
    init: complex amplitudes on the 1287 feasible states. Returns probabilities over the feasible list."""
    phi = init.astype(complex).copy()
    for g, b in zip(gammas, betas):
        phi = phi * np.exp(-1j * g * Ef)
        phi = apply_xy_feasible(phi, b, maps)
    return np.abs(phi) ** 2


def dicke_init():
    return np.full(len(FEAS_IDX), 1 / np.sqrt(len(FEAS_IDX)), dtype=complex)


def basis_init(state):
    v = np.zeros(len(FEAS_IDX), dtype=complex)
    v[POS_IN_FEAS[state]] = 1.0
    return v


def lr_schedule(p, dg, db):
    """Linear-ramp QAOA: gamma ramps up, beta ramps down (Montanez-Barrera et al. LR-QAOA style)."""
    ks = np.arange(1, p + 1)
    return (ks / p) * dg, (1 - (ks - 1) / p) * db


def marginals_full(prob):
    return prob @ BITS


def product_dist(m):
    """Independent-choice null: product distribution over all 2^13 states with marginals m."""
    m = np.clip(m, 1e-12, 1 - 1e-12)
    return np.exp(BITS @ np.log(m) + (1 - BITS) @ np.log(1 - m))


class Inst:
    """QUBO instance (prompt's objective) with exact enumeration."""

    def __init__(self, r, C, lam, P=0.0, k=K, extra=None):
        """extra: optional additional energy vector over all 2^13 states (e.g. mu * test cost, incl. cubic terms)."""
        self.r, self.C, self.lam, self.P = r, C, lam, P
        Xb = BITS.astype(float)
        self.f0 = -(Xb @ r) + lam * 0.5 * np.einsum("si,ij,sj->s", Xb, C, Xb)
        if extra is not None:
            self.f0 = self.f0 + extra
        self.E = self.f0 + P * (HW - k) ** 2
        ff = self.f0[FEAS_IDX]
        self.ff = ff
        o = np.argsort(ff)
        self.opt = FEAS_IDX[o[0]]
        self.fopt, self.fworst = ff[o[0]], ff[o[-1]]
        self.rank_f = np.empty(len(ff), int); self.rank_f[o] = np.arange(len(ff))  # rank of each feasible state

    def metrics_full(self, prob, shots=(100, 1000)):
        """prob over 2^13. Returns P(opt), P(feas), feasible-conditioned mean normalised AR, best-of-N stats."""
        pf = prob[FEAS_IDX]
        return self._metrics(pf, prob.sum(), shots)

    def metrics_feas(self, pf, shots=(100, 1000)):
        return self._metrics(pf, pf.sum(), shots)

    def _metrics(self, pf, total, shots):
        pfeas = pf.sum() / total
        popt = pf[POS_IN_FEAS[self.opt]] / total
        nar = (self.fworst - self.ff) / (self.fworst - self.fopt)
        mean_nar = (pf * nar).sum() / max(pf.sum(), 1e-300)
        out = {"P_opt": popt, "P_feas": pfeas, "mean_normAR_feas": mean_nar,
               "P_top5": pf[self.rank_f < 5].sum() / total, "P_top1pct": pf[self.rank_f < 13].sum() / total}
        # best-of-N normalised AR and prompt AR (f/f*), exact over the shot distribution
        o = np.argsort(self.ff)
        q = np.cumsum(pf[o] / total)  # P(sample has rank <= r)
        for n in shots:
            cdf = 1 - (1 - q) ** n
            pm = np.diff(np.concatenate([[0.0], cdf]))
            out[f"best_of_{n}_normAR"] = (pm * nar[o]).sum()
            if self.fopt < 0:
                out[f"best_of_{n}_promptAR"] = (pm * (self.ff[o] / self.fopt)).sum()
            out[f"P_opt_in_{n}"] = 1 - (1 - popt) ** n
        return out
