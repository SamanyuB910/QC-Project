"""Experiment 4: shot noise and Forte-like depolarising noise on kernel entries and on accuracy; IonQ one-job design.

Noise model (Aer, density-matrix, exact expectations): depolarising p1 = 2.67e-4 on every non-virtual 1Q gate (sx, x),
p2 = 4.95e-3 on every native ZZ (rzz).  RZ is virtual (no error), as on IonQ.  No SPAM/readout error (assumption).
Circuits are the IonQ-native construction of zz_feature_map: H = rz.sx.rz, P = rz, ZZ term = 1 rzz.

A. PQK: exact noisy 1-qubit Bloch vectors for all 569 patients (n = 4, 8; linear and full; bandwidth grid),
   then binomial shot noise per basis.  Nested CV (3x5, inner 3) with hyperparameters chosen INSIDE on the same noisy data.
   Scenarios: exact / noise / noise+S shots (all rows) / train-exact,test-noisy / train-noise-simulated,test-noisy.
B. Fidelity kernel: exact noisy return probabilities for a 60-patient block (1,770 pairs) at n = 8 to validate a
   global-depolarising fit K_noisy ~ a K + b; then that calibrated model + binomial shots on the full 569 kernel.
C. Timing proxy: Aer per-shot trajectory simulation of one PQK circuit (each shot simulated separately, as IonQ's noisy sim).
Features: label-free global scaler + PCA (all rows), unit variance (sensitivity analysis, not the headline protocol).
"""
import os
os.environ.setdefault("OMP_NUM_THREADS", "2"); os.environ.setdefault("OPENBLAS_NUM_THREADS", "2")
import json, time
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Pauli
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_auc_score
import qk_core as qc

P1, P2 = 2.67e-4, 4.95e-3
nm = NoiseModel(basis_gates=["rz", "sx", "x", "rzz"])
nm.add_all_qubit_quantum_error(depolarizing_error(P1, 1), ["sx", "x"])
nm.add_all_qubit_quantum_error(depolarizing_error(P2, 2), ["rzz"])
sim_dm = AerSimulator(method="density_matrix", noise_model=nm, max_parallel_threads=1)


def _bloch_chunk(args):
    Zc, ent = args
    return noisy_bloch(Zc, ent)


def _fid_chunk(args):
    Zc_i, Zc_j, ent = args
    n = Zc_i.shape[1]
    circs = []
    for xi, xj in zip(Zc_i, Zc_j):
        cc = QuantumCircuit(n)
        zz_native(cc, xi, ent); zz_native(cc, xj, ent, inverse=True)
        cc.save_probabilities()
        circs.append(cc)
    res = sim_dm.run(circs).result()
    return np.array([res.data(k)["probabilities"][0] for k in range(len(circs))])


def par_noisy_bloch(pool, Zc, ent, chunk=40):
    parts = [(Zc[i:i + chunk], ent) for i in range(0, len(Zc), chunk)]
    return np.concatenate(pool.map(_bloch_chunk, parts), axis=0)


def h(qc_, q):
    qc_.rz(np.pi / 2, q); qc_.sx(q); qc_.rz(np.pi / 2, q)


def zz_native(qc_, x, ent, inverse=False):
    n = len(x)
    pairs = qc.pairs_for(n, ent)
    if not inverse:
        for _ in range(2):
            for q in range(n): h(qc_, q)
            for q in range(n): qc_.rz(2 * x[q], q)
            for i, j in pairs: qc_.rzz(2 * (np.pi - x[i]) * (np.pi - x[j]), i, j)
    else:
        for _ in range(2):
            for i, j in reversed(pairs): qc_.rzz(-2 * (np.pi - x[i]) * (np.pi - x[j]), i, j)
            for q in range(n): qc_.rz(-2 * x[q], q)
            for q in range(n): h(qc_, q)


def noisy_bloch(Zc, ent):
    N, n = Zc.shape
    circs = []
    for x in Zc:
        c = QuantumCircuit(n)
        zz_native(c, x, ent)
        for k in range(n):
            for P in "XYZ":
                lab = ["I"] * n; lab[n - 1 - k] = P
                c.save_expectation_value(Pauli("".join(lab)), list(range(n)), label=f"{P}{k}")
        circs.append(c)
    res = sim_dm.run(circs).result()
    R = np.empty((N, n, 3))
    for i in range(N):
        d = res.data(i)
        for k in range(n):
            for a, P in enumerate("XYZ"):
                R[i, k, a] = d[f"{P}{k}"]
    return R


def shots_bloch(R, S, rng):
    p = np.clip((1 + R) / 2, 0, 1)
    return 2 * rng.binomial(S, p) / S - 1


def nested_cv(Ks_train, y, Ks_test=None, reps=1):
    """Ks_train: dict key->kernel used for training/selection; Ks_test (optional): kernels whose TEST rows replace the
    training kernel's test rows (train on one representation, test on another)."""
    accs, aucs = [], []
    for rep in range(reps):
        outer = StratifiedKFold(5, shuffle=True, random_state=3000 + rep)
        for f, (tr, te) in enumerate(outer.split(np.zeros(len(y)), y)):
            seed = 10 * rep + f
            (key, C), _, _ = qc.inner_select_kernel(Ks_train, y, tr, seed, Cs=(1.0, 10.0, 100.0, 1000.0))
            from sklearn.svm import SVC
            K = Ks_train[key]
            m = SVC(kernel="precomputed", C=C).fit(K[np.ix_(tr, tr)], y[tr])
            Kt = K if Ks_test is None else Ks_test[key]
            s = m.decision_function(Kt[np.ix_(te, tr)])
            accs.append(((s > 0).astype(int) == y[te]).mean()); aucs.append(roc_auc_score(y[te], s))
    return {"acc": float(np.mean(accs)), "acc_sd": float(np.std(accs)), "auc": float(np.mean(aucs))}


def pqk_kernels(Rdict, gammas=(0.3, 1.0, 3.0)):
    return {(c, g): qc.pqk_from_bloch(R, g) for c, R in Rdict.items() for g in gammas}


def mixed_pqk(Rtrain, Rtest, gammas=(0.3, 1.0, 3.0)):
    """Kernel matrices where rows use Rtest features and columns use Rtrain features (for test rows) — we build the
    full matrix from a stacked representation: entry (i,j) = k(Rtest_i, Rtrain_j); median from train-train distances."""
    out = {}
    for c in Rtrain:
        A = Rtrain[c].reshape(len(Rtrain[c]), -1); B = Rtest[c].reshape(len(Rtest[c]), -1)
        d_tr = 0.5 * qc.sqdist(A); med = np.median(qc.offdiag(d_tr))
        d_x = 0.5 * qc.sqdist(B, A)
        for g in gammas:
            out[(c, g)] = np.exp(-g / med * d_x)
    return out


if __name__ == "__main__":
    t0 = time.time()
    X, y = qc.load_wdbc()
    N = len(y)
    rng = np.random.default_rng(11)
    out = {"noise_model": {"p1": P1, "p2": P2, "rz_virtual": True, "spam": "not modelled"}, "A": {}, "B": {}, "C": {}}
    from multiprocessing import Pool
    pool = Pool(6)
    CB = [0.05, 0.1, 0.2, 0.35, 0.5, 0.75]
    CONF = [(4, "linear", CB), (4, "full", CB), (8, "linear", [0.1, 0.2, 0.35, 0.5]), (8, "full", [0.1, 0.2, 0.35])]
    # ---------------- A. PQK
    for n, ent, CBx in CONF:
        Z = qc.fold_features(X, np.arange(N), n)
        if True:
            CB_ = CBx
            Rex = {c: qc.bloch(qc.zz_states(Z * c, 2, ent), n) for c in CB_}
            Rno = {}
            cache = f"results/exp4_bloch_n{n}_{ent}.npz"
            if os.path.exists(cache):
                dat = np.load(cache)
                Rno = {c: dat[f"no_{c}"] for c in CB_}
            for c in CB_:
                if c in Rno:
                    continue
                tt = time.time()
                Rno[c] = par_noisy_bloch(pool, Z * c, ent)
                print(f"  noisy bloch n={n} {ent} c={c}: {time.time()-tt:.0f}s", flush=True)
            dev = {c: float(np.abs(Rno[c] - Rex[c]).mean()) for c in CB_}
            shrink = {c: float((Rno[c] * Rex[c]).sum() / (Rex[c] ** 2).sum()) for c in CB_}
            row = {"mean_abs_bloch_err_noise": dev, "bloch_shrink_factor": shrink,
                   "bloch_signal_sd": {c: float(Rex[c].std(axis=0).mean()) for c in CB_}}
            np.savez_compressed(f"results/exp4_bloch_n{n}_{ent}.npz", **{f"ex_{c}": Rex[c] for c in CB_}, **{f"no_{c}": Rno[c] for c in CB_})
            row["exact"] = nested_cv(pqk_kernels(Rex), y)
            row["noise_inf_shots"] = nested_cv(pqk_kernels(Rno), y)
            for S in [100, 300, 1000, 3000]:
                Rs = {c: shots_bloch(R, S, rng) for c, R in Rno.items()}
                row[f"noise_{S}shots_all"] = nested_cv(pqk_kernels(Rs), y)
                if S == 1000:
                    Rs0 = {c: shots_bloch(R, S, rng) for c, R in Rex.items()}
                    row[f"noiseless_{S}shots_all"] = nested_cv(pqk_kernels(Rs0), y)
                if S in (300, 1000):
                    # train exact / test noisy+shots (offline training, IonQ inference)
                    row[f"train_exact_test_noise_{S}"] = nested_cv(pqk_kernels(Rex), y, mixed_pqk(Rex, Rs))
                    # noise-aware: train on noise-simulated expectations, test on noisy+shots
                    row[f"train_noisesim_test_noise_{S}"] = nested_cv(pqk_kernels(Rno), y, mixed_pqk(Rno, Rs))
            out["A"][f"n{n}_{ent}"] = row
            print(f"A n={n} {ent}", {k: (v["acc"] if isinstance(v, dict) and "acc" in v else None) for k, v in row.items()},
                  f"{time.time()-t0:.0f}s", flush=True)
            json.dump(out, open("results/exp4_noise.json", "w"), indent=1, default=float)

    # ---------------- B. fidelity kernel block (n = 8)
    n = 8
    Z = qc.fold_features(X, np.arange(N), n)
    blk = np.sort(rng.choice(N, 30, replace=False))
    for ent in ["linear", "full"]:
        for c in [0.35]:
            Zc = Z[blk] * c
            idx = [(i, j) for i in range(len(blk)) for j in range(i, len(blk))]
            I = np.array([a for a, b in idx]); J = np.array([b for a, b in idx])
            tt = time.time()
            parts = [(Zc[I[k:k + 20]], Zc[J[k:k + 20]], ent) for k in range(0, len(idx), 20)]
            vals = np.concatenate(pool.map(_fid_chunk, parts))
            tsim = time.time() - tt
            circs = idx
            Kn = np.zeros((len(blk), len(blk)))
            for k, (i, j) in enumerate(idx):
                Kn[i, j] = Kn[j, i] = vals[k]
            Ke = qc.fid_kernel(qc.zz_states(Zc, 2, ent))
            iu = np.triu_indices(len(blk), 1)
            a, b = np.polyfit(Ke[iu], Kn[iu], 1)
            resid = Kn[iu] - (a * Ke[iu] + b)
            diag = float(np.mean(np.diag(Kn)))
            n2q = 2 * len(qc.pairs_for(n, ent)) * 2
            out["B"][f"n8_{ent}_c{c}"] = {"fit_a": float(a), "fit_b": float(b), "resid_sd": float(resid.std()),
                                         "exact_offdiag_sd": float(Ke[iu].std()), "noisy_diag_mean": diag,
                                         "global_depol_pred_F(0.995^n2q)": float((1 - P2) ** n2q), "n2q_fid_circuit": n2q,
                                         "aer_dm_seconds_6proc": tsim, "n_circuits": len(circs)}
            print("B", ent, c, out["B"][f"n8_{ent}_c{c}"], flush=True)
        Kfull = {cc: qc.fid_kernel(qc.zz_states(Z * cc, 2, ent)) for cc in CB}
        accs = {"exact": nested_cv(Kfull, y)}
        fitted = out["B"][f"n8_{ent}_c0.35"]
        accs["noise_inf_shots"] = nested_cv({cc: np.clip(fitted["fit_a"] * K + fitted["fit_b"], 0, 1) for cc, K in Kfull.items()}, y)
        for S in [100, 1000]:
            Ks = {}
            Ksm = {}
            for cc, K in Kfull.items():
                Kn = np.clip(fitted["fit_a"] * K + fitted["fit_b"], 0, 1)
                Ke = rng.binomial(S, Kn) / S
                Ke = np.triu(Ke, 1); Ke = Ke + Ke.T; np.fill_diagonal(Ke, 1.0)
                Ks[cc] = Ke
                # mitigation: invert global model using the measured diagonal, then PSD-project
                Km = (Ke - fitted["fit_b"]) / fitted["fit_a"]; np.fill_diagonal(Km, 1.0)
                w, V = np.linalg.eigh(Km); Ksm[cc] = (V * np.clip(w, 0, None)) @ V.T
            accs[f"noise_{S}shots"] = nested_cv(Ks, y)
            accs[f"noise_{S}shots_mitigated_psd"] = nested_cv(Ksm, y)
        out["B"][f"n8_{ent}_accuracy"] = accs
        print("B acc", ent, {k: v["acc"] for k, v in accs.items()}, f"{time.time()-t0:.0f}s", flush=True)
        json.dump(out, open("results/exp4_noise.json", "w"), indent=1, default=float)

    pool.close()
    # ---------------- C. per-shot trajectory timing proxy (each shot simulated separately)
    sim_traj = AerSimulator(method="statevector", noise_model=nm, max_parallel_threads=1, max_parallel_shots=1)
    for n, ent in [(4, "linear"), (8, "linear"), (8, "full"), (12, "linear")]:
        Z = qc.fold_features(X, np.arange(N), n)
        cc = QuantumCircuit(n, n)
        zz_native(cc, Z[0] * 0.2, ent)
        for q in range(n): h(cc, q)  # X-basis measurement
        cc.measure(range(n), range(n))
        for S in [300, 1000]:
            tt = time.time(); sim_traj.run(cc, shots=S, seed_simulator=1).result(); dt = time.time() - tt
            out["C"][f"n{n}_{ent}_{S}shots_s"] = dt
            print("C", n, ent, S, dt, flush=True)
    json.dump(out, open("results/exp4_noise.json", "w"), indent=1, default=float)
    print("saved", time.time() - t0)
