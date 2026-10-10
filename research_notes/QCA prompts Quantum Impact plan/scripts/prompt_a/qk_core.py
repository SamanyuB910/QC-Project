"""Core utilities for Prompt A experiments (quantum-kernel SVM on WDBC).

Vectorised NumPy statevector simulation of Qiskit's `zz_feature_map`
(H, P(alpha*x_i), CX-P(alpha*(pi-x_i)(pi-x_j))-CX per pair, `reps` repetitions),
verified against qiskit.quantum_info.Statevector in verify_qiskit.py.

Kernels: fidelity |<psi(x)|psi(x')>|^2, projected (1-RDM Bloch RBF, Huang et al. 2021),
separable (no entanglers), RBF.  Diagnostics: geometric difference g_CQ, model
complexity s_K, centred kernel-target alignment, spectra / effective dimension,
task-model alignment.  Metrics: accuracy, AUC, sensitivity at fixed specificity,
deployable sensitivity/specificity at an inner-CV-calibrated threshold.
"""
import numpy as np
from sklearn.svm import SVC
from sklearn.metrics import roc_auc_score, roc_curve
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.datasets import load_breast_cancer

# ----------------------------------------------------------------------------- data

def load_wdbc():
    X, y = load_breast_cancer(return_X_y=True)
    y_mal = (y == 0).astype(int)  # sklearn: 0 = malignant. We use 1 = malignant (positive class)
    return X, y_mal


def fold_features(X, tr, n, seed=0):
    """Scaler + PCA fit on the training rows only; returns unit-variance (on train) PCA scores for ALL rows."""
    sc = StandardScaler().fit(X[tr])
    Xs = sc.transform(X)
    if n >= X.shape[1]:
        Z = Xs
    else:
        pca = PCA(n, random_state=seed).fit(Xs[tr])
        Z = pca.transform(Xs)
    Z = Z / Z[tr].std(axis=0)
    return Z

# ----------------------------------------------------------------------------- feature maps

_BITS = {}

def bits_matrix(n):
    if n not in _BITS:
        idx = np.arange(2 ** n)
        _BITS[n] = ((idx[:, None] >> np.arange(n)[None, :]) & 1).astype(np.float64)  # little-endian
    return _BITS[n]


def pairs_for(n, ent):
    if ent == "linear":
        return [(i, i + 1) for i in range(n - 1)]
    if ent == "circular":
        return [(i, i + 1) for i in range(n - 1)] + ([(n - 1, 0)] if n > 2 else [])
    if ent == "full":
        return [(i, j) for i in range(n) for j in range(i + 1, n)]
    if ent == "none":
        return []
    raise ValueError(ent)


def wht(psi, n):
    """Apply H on every qubit to a batch of statevectors psi (N, 2^n)."""
    N = psi.shape[0]
    s = 1 / np.sqrt(2)
    for k in range(n):
        t = psi.reshape(N, 2 ** (n - k - 1), 2, 2 ** k)
        a = t[:, :, 0, :]
        b = t[:, :, 1, :]
        psi = np.stack([(a + b) * s, (a - b) * s], axis=2)
    return psi.reshape(N, 2 ** n)


def zz_states(Z, reps=2, ent="full", alpha=2.0, pre_ry=None):
    """Batch statevectors of Qiskit's zz_feature_map(n, reps, ent, alpha) for angle matrix Z (N, n).
    pre_ry: optional length-n array of RY angles applied to |0> before the map (tutorial-08 style trainable layer)."""
    Z = np.asarray(Z, dtype=np.float64)
    N, n = Z.shape
    B = bits_matrix(n)
    phase = (alpha * Z) @ B.T
    P = pairs_for(n, ent)
    if P:
        I = np.array([p[0] for p in P])
        J = np.array([p[1] for p in P])
        XOR = (B[:, I] != B[:, J]).astype(np.float64)
        phi = alpha * (np.pi - Z[:, I]) * (np.pi - Z[:, J])
        phase += phi @ XOR.T
    D = np.exp(1j * phase)
    if pre_ry is None:
        psi = np.full((N, 2 ** n), 2 ** (-n / 2), dtype=np.complex128) * D
    else:
        # product state prod_k RY(theta_k)|0>, then H^n, then D
        v = np.ones(1, dtype=np.complex128)
        for k in range(n):  # little-endian: qubit k is the k-th least significant bit
            q = np.array([np.cos(pre_ry[k] / 2), np.sin(pre_ry[k] / 2)], dtype=np.complex128)
            v = np.kron(q, v)
        psi0 = wht(v[None, :], n)
        psi = psi0 * D
    for _ in range(reps - 1):
        psi = D * wht(psi, n)
    return psi


def bloch(S, n):
    """Single-qubit Bloch vectors (N, n, 3) of batch statevectors S (N, 2^n)."""
    N = S.shape[0]
    R = np.empty((N, n, 3))
    for k in range(n):
        t = S.reshape(N, 2 ** (n - k - 1), 2, 2 ** k)
        a = t[:, :, 0, :]
        b = t[:, :, 1, :]
        r01 = (a * b.conj()).sum(axis=(1, 2))
        R[:, k, 0] = 2 * r01.real
        R[:, k, 1] = -2 * r01.imag
        R[:, k, 2] = (np.abs(a) ** 2).sum(axis=(1, 2)) - (np.abs(b) ** 2).sum(axis=(1, 2))
    return R

# ----------------------------------------------------------------------------- kernels

def fid_kernel(Sa, Sb=None):
    Sb = Sa if Sb is None else Sb
    return np.abs(Sa.conj() @ Sb.T) ** 2


def sqdist(A, B=None):
    B = A if B is None else B
    d = (A * A).sum(1)[:, None] + (B * B).sum(1)[None, :] - 2 * A @ B.T
    return np.maximum(d, 0)


def pqk_from_bloch(R, gamma, ref_idx=None):
    """Projected quantum kernel exp(-gamma_eff * sum_k ||rho_k - rho_k'||_F^2) with gamma normalised by the
    median pairwise distance over ref_idx (training rows) so the grid is dimension-free."""
    F = R.reshape(R.shape[0], -1)
    d = 0.5 * sqdist(F)  # ||rho-rho'||_F^2 = 0.5 ||r-r'||^2
    ref = np.arange(len(F)) if ref_idx is None else ref_idx
    sub = d[np.ix_(ref, ref)]
    med = np.median(sub[~np.eye(len(ref), dtype=bool)])
    return np.exp(-gamma / max(med, 1e-12) * d)


def rbf_kernel_z(Z, g):
    """RBF on unit-variance features with gamma = g / n (so g is dimension-free)."""
    n = Z.shape[1]
    return np.exp(-(g / n) * sqdist(Z))


def ard_rbf(Z, w):
    Zw = Z * np.sqrt(w)[None, :]
    return np.exp(-sqdist(Zw))

# ----------------------------------------------------------------------------- diagnostics

def normalize_trace(K):
    return K * K.shape[0] / np.trace(K)


def psd_sqrt(K):
    w, V = np.linalg.eigh((K + K.T) / 2)
    w = np.clip(w, 0, None)
    return (V * np.sqrt(w)) @ V.T


def geo_diff(KC, KQ, lam=0.0):
    """Huang et al. 2021 g(K^C || K^Q) = sqrt(|| sqrt(KQ) (KC+lam I)^-1 sqrt(KQ) ||_inf), Tr K = N."""
    N = KC.shape[0]
    KC = normalize_trace(KC)
    KQ = normalize_trace(KQ)
    sQ = psd_sqrt(KQ)
    M = sQ @ np.linalg.solve(KC + lam * np.eye(N), sQ)
    return float(np.sqrt(max(np.linalg.eigvalsh((M + M.T) / 2).max(), 0)))


def geo_diff_vec(KC, KQ, lam=0.0):
    """Returns (g, v) where v is the top eigenvector of sqrt(KQ)(KC+lam)^-1 sqrt(KQ) (for engineered labels)."""
    N = KC.shape[0]
    KC = normalize_trace(KC)
    KQ = normalize_trace(KQ)
    sQ = psd_sqrt(KQ)
    M = sQ @ np.linalg.solve(KC + lam * np.eye(N), sQ)
    w, V = np.linalg.eigh((M + M.T) / 2)
    return float(np.sqrt(max(w[-1], 0))), V[:, -1], sQ


def model_complexity(K, y_pm, lam=0.1):
    """s_K = y^T (K + lam I)^-1 y with Tr K = N (Huang et al.)."""
    K = normalize_trace(K)
    return float(y_pm @ np.linalg.solve(K + lam * np.eye(len(y_pm)), y_pm))


def center(K):
    r = K.mean(0)
    return K - r[None, :] - r[:, None] + K.mean()


def kta(K, y_pm, centered=True):
    Y = np.outer(y_pm, y_pm).astype(float)
    if centered:
        Kc = center(K)
        Yc = center(Y)
    else:
        Kc, Yc = K, Y
    return float((Kc * Yc).sum() / (np.linalg.norm(Kc) * np.linalg.norm(Yc) + 1e-300))


def spectrum_stats(K, y_pm=None):
    K = normalize_trace(K)
    w, V = np.linalg.eigh((K + K.T) / 2)
    w = np.clip(w[::-1], 0, None)
    V = V[:, ::-1]
    p = w / w.sum()
    out = {
        "participation_ratio": float(w.sum() ** 2 / (w ** 2).sum()),
        "n_eig_90pct": int(np.searchsorted(np.cumsum(p), 0.90) + 1),
        "n_eig_99pct": int(np.searchsorted(np.cumsum(p), 0.99) + 1),
        "top_eig_frac": float(p[0]),
        "eigs_top20": [float(x) for x in p[:20]],
    }
    if y_pm is not None:
        yc = y_pm - y_pm.mean()
        proj = (V.T @ yc) ** 2 / (yc @ yc)
        cum = np.cumsum(proj)
        out["task_alignment_top5"] = float(cum[4])
        out["task_alignment_top20"] = float(cum[19])
        out["task_alignment_top50"] = float(cum[49])
    return out


def offdiag(K):
    return K[~np.eye(K.shape[0], dtype=bool)]

# ----------------------------------------------------------------------------- metrics

def sens_at_spec(y, s, spec=0.95):
    fpr, tpr, _ = roc_curve(y, s)
    ok = fpr <= 1 - spec + 1e-12
    return float(tpr[ok].max()) if ok.any() else 0.0


def spec_at_sens(y, s, sens=0.98):
    fpr, tpr, _ = roc_curve(y, s)
    ok = tpr >= sens - 1e-12
    return float(1 - fpr[ok].min()) if ok.any() else 0.0


def calib_threshold(y, s, target_sens):
    """Largest threshold t s.t. fraction of positives with s >= t is >= target_sens."""
    pos = np.sort(s[y == 1])
    k = int(np.floor((1 - target_sens) * len(pos)))
    k = min(max(k, 0), len(pos) - 1)
    return float(pos[k])


def metric_block(y, s, pred, pred_cal=None):
    out = {
        "acc": float((pred == y).mean()),
        "auc": float(roc_auc_score(y, s)),
        "sens": float(pred[y == 1].mean()),
        "spec": float(1 - pred[y == 0].mean()),
        "sens@spec95": sens_at_spec(y, s, 0.95),
        "spec@sens98": spec_at_sens(y, s, 0.98),
    }
    if pred_cal is not None:
        out["cal_sens"] = float(pred_cal[y == 1].mean())
        out["cal_spec"] = float(1 - pred_cal[y == 0].mean())
        out["cal_acc"] = float((pred_cal == y).mean())
    return out

# ----------------------------------------------------------------------------- nested CV over precomputed kernels

CS = (0.1, 1.0, 10.0, 100.0, 1000.0, 10000.0)


def inner_select_kernel(Ks, y, tr, seed, Cs=CS, n_inner=3):
    """Ks: dict key -> full kernel (all rows). Inner stratified CV on tr selects (key, C) by accuracy (AUC tiebreak)."""
    inner = StratifiedKFold(n_inner, shuffle=True, random_state=seed)
    splits = list(inner.split(np.zeros(len(tr)), y[tr]))
    best, best_score = None, (-1, -1)
    for key, K in Ks.items():
        Ktr = K[np.ix_(tr, tr)]
        for C in Cs:
            accs, aucs = [], []
            for a, b in splits:
                m = SVC(kernel="precomputed", C=C).fit(Ktr[np.ix_(a, a)], y[tr][a])
                d = m.decision_function(Ktr[np.ix_(b, a)])
                accs.append(((d > 0).astype(int) == y[tr][b]).mean())
                aucs.append(roc_auc_score(y[tr][b], d))
            sc = (round(np.mean(accs), 6), np.mean(aucs))
            if sc > best_score:
                best_score, best = sc, (key, C)
    return best, best_score, splits


def oof_scores_kernel(K, y, tr, C, splits):
    """Inner out-of-fold decision values on the training rows (for threshold calibration)."""
    Ktr = K[np.ix_(tr, tr)]
    s = np.empty(len(tr))
    for a, b in splits:
        m = SVC(kernel="precomputed", C=C).fit(Ktr[np.ix_(a, a)], y[tr][a])
        s[b] = m.decision_function(Ktr[np.ix_(b, a)])
    return s


def fit_eval_kernel(Ks, y, tr, te, seed, target_sens=0.98, Cs=CS):
    (key, C), sc, splits = inner_select_kernel(Ks, y, tr, seed, Cs)
    K = Ks[key]
    m = SVC(kernel="precomputed", C=C).fit(K[np.ix_(tr, tr)], y[tr])
    s = m.decision_function(K[np.ix_(te, tr)])
    oof = oof_scores_kernel(K, y, tr, C, splits)
    t = calib_threshold(y[tr], oof, target_sens)
    return {
        "key": key, "C": C, "inner_acc": sc[0], "n_sv": int(m.n_support_.sum()),
        "scores": s, "pred": (s > 0).astype(int), "pred_cal": (s >= t).astype(int), "thr": t,
    }

# ----------------------------------------------------------------------------- SPSA kernel alignment

def spsa_maximize(f, theta0, iters=60, seed=0, c=0.1, target_step=0.15, eval_every=10):
    """Maximise f with SPSA (qiskit-style calibration of a). Returns best evaluated theta."""
    rng = np.random.default_rng(seed)
    th = np.array(theta0, dtype=float)
    A, alpha, gam = 0.1 * iters, 0.602, 0.101
    # calibration
    mags = []
    for _ in range(6):
        d = rng.choice([-1.0, 1.0], size=th.size)
        mags.append(abs(f(th + c * d) - f(th - c * d)) / (2 * c))
    g0 = np.mean(mags) + 1e-12
    a = target_step * (A + 1) ** alpha / g0
    best_th, best_f = th.copy(), f(th)
    hist = [best_f]
    for k in range(iters):
        ak = a / (k + 1 + A) ** alpha
        ck = c / (k + 1) ** gam
        d = rng.choice([-1.0, 1.0], size=th.size)
        gk = (f(th + ck * d) - f(th - ck * d)) / (2 * ck) * d
        th = th + ak * gk
        if (k + 1) % eval_every == 0 or k == iters - 1:
            fv = f(th)
            hist.append(fv)
            if fv > best_f:
                best_f, best_th = fv, th.copy()
    return best_th, best_f, hist
