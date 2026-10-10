"""Experiment 4b: noise + shots at the SMALL bandwidths that nested CV actually selects (n = 8).
PQK: exact Forte-like-noise Bloch vectors from Aer density-matrix simulation (same noise model as exp4), c in {0.01..0.1}.
FQK: the global-depolarising model validated in exp4 part B (K_noisy = a K + b, residual sd ~3e-4), a,b from exp4 fits,
     binomial shots, optional diagonal-based mitigation + PSD projection.
Shots S in {100, 1000, 10000}.  Nested CV (1 x 5 outer, 3 inner), label-free global PCA (sensitivity analysis).
Also records the per-feature signal-to-shot-noise ratio: sd of exact Bloch components across patients vs 1/sqrt(S).
"""
import os
os.environ.setdefault("OMP_NUM_THREADS", "2"); os.environ.setdefault("OPENBLAS_NUM_THREADS", "2")
import json, time
import numpy as np
from multiprocessing import Pool
import qk_core as qc
from exp4_noise import par_noisy_bloch, shots_bloch, nested_cv, pqk_kernels, mixed_pqk

if __name__ == "__main__":
    t0 = time.time()
    X, y = qc.load_wdbc()
    N, n = len(y), 8
    rng = np.random.default_rng(21)
    Z = qc.fold_features(X, np.arange(N), n)
    fits = json.load(open("results/exp4_noise.json"))["B"]
    out = {"PQK": {}, "FQK": {}}
    pool = Pool(6)
    CB = [0.01, 0.02, 0.05, 0.1]
    for ent in ["linear", "full"]:
        Rex = {c: qc.bloch(qc.zz_states(Z * c, 2, ent), n) for c in CB}
        Rno = {c: par_noisy_bloch(pool, Z * c, ent) for c in CB}
        row = {"bloch_signal_sd": {c: float(Rex[c].std(axis=0).mean()) for c in CB},
               "bloch_shrink": {c: float((Rno[c] * Rex[c]).sum() / (Rex[c] ** 2).sum()) for c in CB},
               "exact": nested_cv(pqk_kernels(Rex), y), "noise_inf_shots": nested_cv(pqk_kernels(Rno), y)}
        for S in [100, 1000, 10000]:
            Rs = {c: shots_bloch(R, S, rng) for c, R in Rno.items()}
            row[f"noise_{S}shots_all"] = nested_cv(pqk_kernels(Rs), y)
            row[f"train_noisesim_test_noise_{S}"] = nested_cv(pqk_kernels(Rno), y, mixed_pqk(Rno, Rs))
        out["PQK"][ent] = row
        print("PQK", ent, {k: v["acc"] for k, v in row.items() if isinstance(v, dict) and "acc" in v}, row["bloch_signal_sd"], f"{time.time()-t0:.0f}s", flush=True)
        # FQK with calibrated global-depolarising model
        a, b = fits[f"n8_{ent}_c0.35"]["fit_a"], fits[f"n8_{ent}_c0.35"]["fit_b"]
        BWF = [0.005, 0.01, 0.02, 0.05, 0.1]
        Kf = {c: qc.fid_kernel(qc.zz_states(Z * c, 2, ent)) for c in BWF}
        frow = {"a": a, "b": b, "exact": nested_cv(Kf, y),
                "offdiag_sd": {c: float(qc.offdiag(K).std()) for c, K in Kf.items()},
                "offdiag_mean": {c: float(qc.offdiag(K).mean()) for c, K in Kf.items()}}
        for S in [100, 1000, 10000]:
            Ks, Km = {}, {}
            for c, K in Kf.items():
                Kn = rng.binomial(S, np.clip(a * K + b, 0, 1)) / S
                Kn = np.triu(Kn, 1); Kn = Kn + Kn.T; np.fill_diagonal(Kn, 1.0)
                Ks[c] = Kn
                M = (Kn - b) / a; np.fill_diagonal(M, 1.0)
                w, V = np.linalg.eigh(M); Km[c] = (V * np.clip(w, 0, None)) @ V.T
            frow[f"noise_{S}shots"] = nested_cv(Ks, y)
            frow[f"noise_{S}shots_mitigated"] = nested_cv(Km, y)
        out["FQK"][ent] = frow
        print("FQK", ent, {k: v["acc"] for k, v in frow.items() if isinstance(v, dict) and "acc" in v}, f"{time.time()-t0:.0f}s", flush=True)
        json.dump(out, open("results/exp4b_noise_lowbw.json", "w"), indent=1, default=float)
    pool.close()
    print("saved")
