import numpy as np, itertools, time, json
import scipy.sparse as sp
from scipy.sparse.linalg import eigsh, LinearOperator

def strings(norb, n):
    return [sum(1 << i for i in c) for c in itertools.combinations(range(norb), n)]

def link_mats(norb, n):
    S = strings(norb, n); idx = {s: k for k, s in enumerate(S)}; N = len(S)
    rows_D, cols_D, vals = [], [], []
    for k, s in enumerate(S):
        for q in range(norb):
            if not (s >> q) & 1: continue
            s1 = s ^ (1 << q)
            sg1 = -1 if bin(s1 & ((1 << q) - 1)).count('1') % 2 else 1
            for p in range(norb):
                if (s1 >> p) & 1: continue
                sg2 = -1 if bin(s1 & ((1 << p) - 1)).count('1') % 2 else 1
                s2 = s1 | (1 << p)
                rows_D.append((p * norb + q) * N + idx[s2]); cols_D.append(k); vals.append(sg1 * sg2)
    A = sp.csr_matrix((vals, (rows_D, cols_D)), shape=(norb * norb * N, N))  # D_flat = A @ C
    # B[dst, pq*N+src] = sgn  -> sigma = B @ G_flat
    r = np.array(rows_D); pq = r // N; dst = r % N
    B = sp.csr_matrix((vals, (dst, pq * N + np.array(cols_D))), shape=(N, norb * norb * N))
    return A, B, N

def fci(h1, eri, norb, na, nb, ecore=0.0):
    Aa, Ba, Na = link_mats(norb, na)
    Ab, Bb, Nb = link_mats(norb, nb)
    k = h1 - 0.5 * np.einsum('pqqs->ps', eri)
    n2 = norb * norb
    W = 0.5 * eri.reshape(n2, n2)
    def sigma(c):
        C = c.reshape(Na, Nb)
        Da = (Aa @ C).reshape(n2, Na, Nb)
        Db = (Ab @ C.T).reshape(n2, Nb, Na).transpose(0, 2, 1)
        D = Da + Db
        out = np.einsum('pq,pqij->ij', k.reshape(norb, norb), D.reshape(norb, norb, Na, Nb)) if False else np.tensordot(k.reshape(-1), D, axes=(0, 0))
        G = (W @ D.reshape(n2, -1)).reshape(n2, Na, Nb)
        out += Ba @ G.reshape(n2 * Na, Nb)
        out += (Bb @ G.transpose(0, 2, 1).reshape(n2 * Nb, Na)).T
        return out.reshape(-1)
    H = LinearOperator((Na * Nb, Na * Nb), matvec=sigma, dtype=float)
    e, v = eigsh(H, k=1, which='SA', tol=1e-9)
    return e[0] + ecore, Na * Nb

def hubbard_ints(Lx, Ly, t=1.0, U=4.0):
    L = Lx * Ly; h1 = np.zeros((L, L))
    for x in range(Lx):
        for y in range(Ly):
            i = x * Ly + y
            if y + 1 < Ly: h1[i, i + 1] = h1[i + 1, i] = -t
            if x + 1 < Lx: h1[i, i + Ly] = h1[i + Ly, i] = -t
    eri = np.zeros((L, L, L, L))
    for i in range(L): eri[i, i, i, i] = U
    return h1, eri, L

def random_mol_ints(norb, seed=0):
    rng = np.random.default_rng(seed)
    h1 = rng.standard_normal((norb, norb)) * 0.3; h1 = h1 + h1.T - np.diag(np.arange(norb)[::-1] * 0.5)
    X = rng.standard_normal((norb, norb, 3)) * 0.2
    L = np.einsum('pqx->xpq', X + X.transpose(1, 0, 2))  # Cholesky-like vectors -> positive semidefinite, 8-fold symmetric
    eri = np.einsum('xpq,xrs->pqrs', L, L)
    return h1, eri

if __name__ == '__main__':
    res = {}
    h1, eri, L = hubbard_ints(2, 4)
    t = time.time(); e, d = fci(h1, eri, L, 4, 4); res['hubbard2x4_KH'] = [round(e, 6), d, round(time.time() - t, 2)]
    for norb in [8, 10]:
        h1, eri = random_mol_ints(norb)
        t = time.time(); e, d = fci(h1, eri, norb, norb // 2, norb // 2); res[f'random_{norb}e{norb}o'] = [round(e, 6), d, round(time.time() - t, 2)]
    print(json.dumps(res))
