"""Experiment 2b: the frozen auditor (exp3c rule) + geometric difference on the REAL labels at n = 4, 8, 12, including the
small bandwidths that nested CV actually selects.  Label-free global scaler+PCA (diagnostic only).
For each quantum kernel: top-30 task alignment A, g_min = min over classical {RBF grid, linear} of g(K_C||K_Q) (lam=0.01, 0.1),
off-diagonal mean/var.  Family maxima give the verdict."""
import os
os.environ.setdefault("OMP_NUM_THREADS", "4")
import json
import numpy as np
import qk_core as qc

X, y = qc.load_wdbc()
ypm = 2 * y - 1
N = len(y)
yc = ypm - ypm.mean()


def A30(K):
    w, V = np.linalg.eigh((K + K.T) / 2)
    V = V[:, ::-1][:, :30]
    return float(((V.T @ yc) ** 2).sum() / (yc @ yc))


out = {}
for n in [4, 8, 12]:
    Z = qc.fold_features(X, np.arange(N), n)
    classical = {f"RBF g={g}": qc.rbf_kernel_z(Z, g) for g in [0.003, 0.01, 0.03, 0.1, 0.3, 1.0, 3.0]}
    classical["Linear"] = Z @ Z.T + 1.0
    quantum = {}
    for c in [0.0025, 0.005, 0.01, 0.02, 0.05]:
        Sf = qc.zz_states(Z * c, 2, "full"); Sl = qc.zz_states(Z * c, 2, "linear")
        quantum[f"FQK-full c={c}"] = qc.fid_kernel(Sf)
        quantum[f"FQK-linear c={c}"] = qc.fid_kernel(Sl)
        quantum[f"SEP c={c}"] = qc.fid_kernel(qc.zz_states(Z * c, 2, "none"))
        quantum[f"PQK c={c} g=0.3"] = qc.pqk_from_bloch(qc.bloch(Sf, n), 0.3)
        quantum[f"PQK-linear c={c} g=0.3"] = qc.pqk_from_bloch(qc.bloch(Sl, n), 0.3)
    AC = {k: A30(K) for k, K in classical.items()}
    rows = {}
    for k, K in quantum.items():
        od = qc.offdiag(K)
        rows[k] = {"A30": A30(K), "g_min(lam=0.01)": min(qc.geo_diff(KC, K, 0.01) for KC in classical.values()),
                   "g_min(lam=0.1)": min(qc.geo_diff(KC, K, 0.1) for KC in classical.values()),
                   "offdiag_mean": float(od.mean()), "offdiag_var": float(od.var())}
    aq = {k: r["A30"] for k, r in rows.items() if not k.startswith("SEP")}
    A_C, A_Q = max(AC.values()), max(aq.values())
    verdict = ("quantum-favourable" if A_Q - A_C >= 0.10 and A_Q >= 0.20 else "classical-favourable" if A_C - A_Q >= 0.10 and A_C >= 0.20
               else "unlearnable" if max(A_C, A_Q) < 0.20 else "no clear edge")
    out[n] = {"A_C_by_kernel": AC, "quantum": rows, "A_C": A_C, "A_Q": A_Q, "verdict": verdict, "sqrtN": float(np.sqrt(N))}
    print(f"n={n}: A_C={A_C:.3f} ({max(AC, key=AC.get)}) A_Q={A_Q:.3f} ({max(aq, key=aq.get)}) verdict={verdict}", flush=True)
    for k, r in rows.items():
        print(f"   {k:24s} A30={r['A30']:.3f} g_min(.01)={r['g_min(lam=0.01)']:.2f} g_min(.1)={r['g_min(lam=0.1)']:.2f} od_mean={r['offdiag_mean']:.3f}", flush=True)
json.dump(out, open("results/exp2b_real_auditor.json", "w"), indent=1)
