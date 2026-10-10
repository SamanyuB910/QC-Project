"""Restart-protocol quantum reservoir (no mid-circuit measurement) vs classical reservoirs on Mackey-Glass.
Each prediction time t: fresh circuit encodes window u_{t-w+1..t}; layer = input RY on all qubits + fixed random ZZ(all-to-all subset) + RX mixing.
Features: <Z_i>, <Z_i Z_j>. Readout: ridge. Pure numpy statevector.
"""
import numpy as np, time
from sklearn.linear_model import Ridge
from sklearn.preprocessing import PolynomialFeatures

rng = np.random.default_rng(1)

def mackey_glass(T, tau=17, dt=1.0, beta=0.2, gamma=0.1, nexp=10, sub=1):
    hist = int(tau / dt)
    x = np.zeros(T * sub + hist + 1000); x[:hist + 1] = 1.2
    for t in range(hist, len(x) - 1):
        x[t + 1] = x[t] + dt * (beta * x[t - hist] / (1 + x[t - hist] ** nexp) - gamma * x[t])
    return x[hist + 1000::sub][:T]

def rx_all(psi, n, th):
    t = psi.reshape([2] * n)
    c, s = np.cos(th / 2), np.sin(th / 2)
    U = np.array([[c, -1j * s], [-1j * s, c]])
    for ax in range(n):
        t = np.moveaxis(np.tensordot(U, t, axes=([1], [ax])), 0, ax)
    return t.reshape(-1)

def ry_all(psi, n, th):
    t = psi.reshape([2] * n)
    c, s = np.cos(th / 2), np.sin(th / 2)
    U = np.array([[c, -s], [s, c]])
    for ax in range(n):
        t = np.moveaxis(np.tensordot(U, t, axes=([1], [ax])), 0, ax)
    return t.reshape(-1)

def qrc_features(u, n=8, w=6, npairs=8, h=1.0, scale=np.pi, seed=0):
    r = np.random.default_rng(seed)
    idx = np.arange(2 ** n); bits = (idx[:, None] >> np.arange(n)[::-1]) & 1; z = 1 - 2 * bits
    allp = [(i, j) for i in range(n) for j in range(i + 1, n)]
    P = [allp[k] for k in r.choice(len(allp), npairs, replace=False)]
    J = r.uniform(0.5, 1.5, npairs) * np.pi / 2
    ph = sum(J[k] * z[:, i] * z[:, j] for k, (i, j) in enumerate(P))
    D = np.exp(-1j * ph)
    # per-qubit input weights (random), so qubits see different nonlinearity
    win = r.uniform(0.5, 1.5, n)
    feats = []
    zz = np.array([z[:, i] * z[:, j] for i, j in allp]).T
    for t in range(w - 1, len(u)):
        psi = np.zeros(2 ** n, complex); psi[0] = 1
        for k in range(w):
            val = u[t - w + 1 + k]
            tt = psi.reshape([2] * n)
            for ax in range(n):
                th = scale * win[ax] * val
                c, s = np.cos(th / 2), np.sin(th / 2)
                tt = np.moveaxis(np.tensordot(np.array([[c, -s], [s, c]]), tt, axes=([1], [ax])), 0, ax)
            psi = tt.reshape(-1)
            psi = D * psi
            psi = rx_all(psi, n, h)
        p = np.abs(psi) ** 2
        feats.append(np.concatenate([p @ z, p @ zz]))
    return np.array(feats), npairs * w

def esn_features(u, N=100, rho=0.9, leak=1.0, insc=1.0, seed=0):
    r = np.random.default_rng(seed)
    W = r.normal(size=(N, N)) * (r.random((N, N)) < 0.1)
    W *= rho / np.max(np.abs(np.linalg.eigvals(W)))
    Win = r.uniform(-insc, insc, N)
    x = np.zeros(N); out = []
    for v in u:
        x = (1 - leak) * x + leak * np.tanh(W @ x + Win * v)
        out.append(x.copy())
    return np.array(out)

def nmse(yp, yt):
    return np.mean((yp - yt) ** 2) / np.var(yt)

T = 1700
x = mackey_glass(T, sub=3)
u = (x - x.min()) / (x.max() - x.min())  # in [0,1]
H = 1  # horizon (steps of 3 time units)
w = 6
ntr, nwash = 1000, 0
targets = u[w - 1 + H:]
for horizon in [1, 5]:
    print(f"\n=== Mackey-Glass (tau=17, sampled every 3 time units), predict {horizon} step(s) ahead ===")
    def evaluate(F, name, offset):
        # F row i corresponds to time index offset+i; target u[t+horizon]
        tt = np.arange(offset, offset + len(F))
        valid = tt + horizon < len(u)
        F2, y2 = F[valid], u[tt[valid] + horizon]
        Ftr, Fte, ytr, yte = F2[:ntr], F2[ntr:], y2[:ntr], y2[ntr:]
        best = min(((nmse(Ridge(alpha=a).fit(Ftr[:800], ytr[:800]).predict(Ftr[800:]), ytr[800:]), a) for a in [1e-8, 1e-6, 1e-4, 1e-2, 1]))
        m = Ridge(alpha=best[1]).fit(Ftr, ytr)
        print(f"  {name:45s} test NMSE = {nmse(m.predict(Fte), yte):.2e}  (features={F.shape[1]})")
    # linear AR(w)
    Xw = np.array([u[t - w + 1:t + 1] for t in range(w - 1, len(u))])
    evaluate(Xw, f"Linear AR({w}) ridge", w - 1)
    Xp = PolynomialFeatures(2).fit_transform(Xw)
    evaluate(Xp, f"NVAR: quadratic poly of window w={w}", w - 1)
    Xp3 = PolynomialFeatures(3).fit_transform(Xw)
    evaluate(Xp3, f"NVAR: cubic poly of window w={w}", w - 1)
    for N in [36, 300]:
        E = esn_features(u, N=N)
        evaluate(E[50:], f"ESN N={N}", 50)
    t0 = time.time()
    Q, n2q = qrc_features(u, n=8, w=w, npairs=8)
    t1 = time.time()
    evaluate(Q, f"QRC 8q, w={w}, {n2q} ZZ gates, <Z>,<ZZ> (exact)", w - 1)
    # finite shots: estimate features from S shots (approx: Gaussian noise with binomial var)
    for S in [1000, 10000]:
        Qn = Q + rng.normal(size=Q.shape) * np.sqrt(np.clip(1 - Q ** 2, 0, 1) / S)
        evaluate(Qn, f"QRC same, {S} shots/circuit (sampled noise)", w - 1)
    # global depolarizing approx: expectation values shrink by F
    F = 0.995 ** n2q
    Qd = F * Q + rng.normal(size=Q.shape) * np.sqrt(np.clip(1 - (F * Q) ** 2, 0, 1) / 1000)
    evaluate(Qd, f"QRC, global-depol F={F:.2f} + 1000 shots", w - 1)
    print(f"  QRC feature time: {t1 - t0:.1f}s for {len(Q)} circuits (native numpy)")
