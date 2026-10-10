"""Quick numerical check: quantum kernels vs classical baselines on sklearn breast cancer.
Pure numpy statevector simulation of an IQP/ZZ-style feature map (IonQ-friendly: each ZZ term = 1 native ZZ gate).
"""
import numpy as np, time, sys
from sklearn.datasets import load_breast_cancer
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.svm import SVC
from sklearn.model_selection import StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, HistGradientBoostingClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics.pairwise import rbf_kernel

rng = np.random.default_rng(0)

def had_all(psi, n):
    t = psi.reshape([2] * n)
    H = np.array([[1, 1], [1, -1]]) / np.sqrt(2)
    for ax in range(n):
        t = np.moveaxis(np.tensordot(H, t, axes=([1], [ax])), 0, ax)
    return t.reshape(-1)

def states(X, reps=2, pairs="chain"):
    N, n = X.shape
    idx = np.arange(2 ** n)
    bits = (idx[:, None] >> np.arange(n)[::-1]) & 1
    z = 1 - 2 * bits
    P = [(i, i + 1) for i in range(n - 1)] if pairs == "chain" else [(i, j) for i in range(n) for j in range(i + 1, n)]
    out = np.empty((N, 2 ** n), complex)
    for a, x in enumerate(X):
        ph = z @ x + sum(x[i] * x[j] * z[:, i] * z[:, j] for i, j in P)
        D = np.exp(-1j * ph)
        psi = np.zeros(2 ** n, complex); psi[0] = 1
        for _ in range(reps):
            psi = D * had_all(psi, n)
        out[a] = psi
    return out, len(P) * reps

def bloch(S, n):
    N = S.shape[0]
    R = np.empty((N, n, 3))
    for k in range(n):
        t = S.reshape(N, 2 ** k, 2, 2 ** (n - k - 1))
        rho = np.einsum("aibj,aicj->abc", t, t.conj())  # N x 2 x 2
        R[:, k, 0] = 2 * rho[:, 0, 1].real
        R[:, k, 1] = -2 * rho[:, 0, 1].imag
        R[:, k, 2] = (rho[:, 0, 0] - rho[:, 1, 1]).real
    return R

def fid_kernel(S):
    return np.abs(S.conj() @ S.T) ** 2

def pqk(R, gamma):
    d = ((R[:, None, :, :] - R[None, :, :, :]) ** 2).sum(axis=(2, 3)) / 2.0
    return np.exp(-gamma * d)

def geo_diff(KC, KQ, lam):
    N = KC.shape[0]
    KC = KC * N / np.trace(KC); KQ = KQ * N / np.trace(KQ)
    w, V = np.linalg.eigh(KQ); w = np.clip(w, 0, None)
    sQ = (V * np.sqrt(w)) @ V.T
    M = sQ @ np.linalg.inv(KC + lam * np.eye(N)) @ sQ
    return np.sqrt(np.max(np.linalg.eigvalsh((M + M.T) / 2)))

def model_complexity(K, y, lam):
    N = K.shape[0]; K = K * N / np.trace(K)
    return float(y @ np.linalg.solve(K + lam * np.eye(N), y))

def nested_cv_kernel(Ks, y, Cs=(0.1, 1, 10, 100), seed=0):
    """Ks: dict name->precomputed kernel. Inner 3-fold picks (kernel, C); outer 5-fold reports."""
    outer = StratifiedKFold(5, shuffle=True, random_state=seed)
    accs = []
    for tr, te in outer.split(np.zeros(len(y)), y):
        inner = StratifiedKFold(3, shuffle=True, random_state=seed + 1)
        best, bestacc = None, -1
        for name, K in Ks.items():
            for C in Cs:
                a = []
                for itr, ite in inner.split(np.zeros(len(tr)), y[tr]):
                    A, B = tr[itr], tr[ite]
                    m = SVC(kernel="precomputed", C=C).fit(K[np.ix_(A, A)], y[A])
                    a.append(m.score(K[np.ix_(B, A)], y[B]))
                if np.mean(a) > bestacc:
                    bestacc, best = np.mean(a), (name, C)
        name, C = best
        K = Ks[name]
        m = SVC(kernel="precomputed", C=C).fit(K[np.ix_(tr, tr)], y[tr])
        accs.append(m.score(K[np.ix_(te, tr)], y[te]))
    return np.mean(accs), np.std(accs)

def cv_model(make, Z, y, seed=0):
    outer = StratifiedKFold(5, shuffle=True, random_state=seed)
    return np.mean([make().fit(Z[tr], y[tr]).score(Z[te], y[te]) for tr, te in outer.split(Z, y)])

X, y01 = load_breast_cancer(return_X_y=True)
y = 2 * y01 - 1
Xs = StandardScaler().fit_transform(X)
print("N =", len(y), "features =", X.shape[1])

for n in [4, 8, 12]:
    # NOTE: PCA/scaler fit on all data (transductive, slight leak, same for all models)
    Z = PCA(n).fit_transform(Xs)
    Z = Z / Z.std(axis=0)
    print(f"\n===== n = {n} qubits (PCA-{n}) =====")
    # classical baselines on same PCA features
    res = {}
    res["LogReg"] = cv_model(lambda: LogisticRegression(max_iter=2000), Z, y01)
    res["RF"] = cv_model(lambda: RandomForestClassifier(300, random_state=0), Z, y01)
    res["HistGB"] = cv_model(lambda: HistGradientBoostingClassifier(random_state=0), Z, y01)
    res["MLP(32)"] = cv_model(lambda: MLPClassifier((32,), max_iter=3000, random_state=0), Z, y01)
    rbfK = {f"rbf_g{g}": rbf_kernel(Z, gamma=g / n) for g in [0.1, 0.3, 1, 3]}
    res["RBF-SVM (nested)"] = nested_cv_kernel(rbfK, y)[0]
    t0 = time.time()
    fidK, pqK, info = {}, {}, {}
    for bw in [0.1, 0.25, 0.5, 1.0]:
        S, n2q = states(Z * bw, reps=2, pairs="chain")
        K = fid_kernel(S)
        fidK[f"fid_bw{bw}"] = K
        R = bloch(S, n)
        for g in [0.1, 0.3, 1.0]:
            pqK[f"pqk_bw{bw}_g{g}"] = pqk(R, g)
        off = K[~np.eye(len(K), dtype=bool)]
        info[bw] = (off.mean(), off.var(), n2q)
    t1 = time.time()
    res["Fidelity QK (nested bw,C)"] = nested_cv_kernel(fidK, y)[0]
    res["Projected QK (nested bw,g,C)"] = nested_cv_kernel(pqK, y)[0]
    for k, v in res.items():
        print(f"  {k:32s} acc = {v:.4f}")
    print(f"  statevector+kernel build time (4 bandwidths, numpy native): {t1 - t0:.2f}s")
    for bw, (m, v, n2q) in info.items():
        print(f"  bw={bw}: fidelity-kernel off-diag mean={m:.4f} var={v:.5f}; ZZ gates per U(x)={n2q} (kernel circuit U(x)U^dag(x') = {2*n2q}), F~0.995^2q = {0.995**(2*n2q):.3f}")
    KC = rbf_kernel(Z, gamma=1.0 / n)
    for bw in [0.25, 1.0]:
        for lam in [0.01, 0.1]:
            gF = geo_diff(KC, fidK[f"fid_bw{bw}"], lam)
            gP = geo_diff(KC, pqK[f"pqk_bw{bw}_g0.3"], lam)
            print(f"  geometric difference vs RBF (lam={lam}) bw={bw}: g(fid)={gF:.2f}  g(pqk)={gP:.2f}  [sqrt(N)={np.sqrt(len(y)):.1f}]")
        sC = model_complexity(KC, y, 0.1); sF = model_complexity(fidK[f"fid_bw{bw}"], y, 0.1); sP = model_complexity(pqK[f"pqk_bw{bw}_g0.3"], y, 0.1)
        print(f"  model complexity s_K (lam=0.1, real labels) bw={bw}: s_RBF={sC:.1f}  s_fid={sF:.1f}  s_pqk={sP:.1f}  (N={len(y)})")

# Concentration with fixed bandwidth vs qubits (all-pairs ZZ, reps=2), random subset
print("\n===== concentration: off-diagonal fidelity-kernel variance vs n (bw=1, all-pairs, 150 pts) =====")
sub = rng.choice(len(y), 150, replace=False)
for n in [2, 4, 6, 8, 10, 12]:
    Z = PCA(n).fit_transform(Xs)[sub]; Z = Z / Z.std(axis=0)
    for pairs in ["all"]:
        S, n2q = states(Z, reps=2, pairs=pairs)
        K = fid_kernel(S); off = K[~np.eye(len(K), dtype=bool)]
        R = bloch(S, n); KP = pqk(R, 1.0 / n); offp = KP[~np.eye(len(KP), dtype=bool)]
        print(f"  n={n:2d} pairs={pairs}: fid mean={off.mean():.4f} var={off.var():.2e} | 2^-n={2**-n:.4f} | PQK(g=1/n) var={offp.var():.2e} | 2q/U={n2q}")

# Shot noise + global depolarizing on fidelity kernel at n=8
print("\n===== finite shots + global depolarizing on fidelity kernel, n=8, bw=0.5, chain reps2 =====")
Z = PCA(8).fit_transform(Xs); Z = Z / Z.std(axis=0)
S, n2q = states(Z * 0.5, reps=2, pairs="chain")
K = fid_kernel(S)
for p2 in [0.0, 0.005, 0.01]:
    F = (1 - p2) ** (2 * n2q)
    Kn = F * K + (1 - F) / 2 ** 8
    for shots in [None, 100, 1000]:
        if shots is None:
            Ke = Kn.copy()
        else:
            Ke = rng.binomial(shots, np.clip(Kn, 0, 1)) / shots
            Ke = np.triu(Ke, 1); Ke = Ke + Ke.T; np.fill_diagonal(Ke, 1.0)
        a, s = nested_cv_kernel({"k": Ke}, y)
        print(f"  p2q={p2} (F={F:.3f}) shots={shots}: acc={a:.4f} +- {s:.3f}")
