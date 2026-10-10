"""Prototype of what a Qollab 'Run' would execute for the recommended Prompt A build (pure NumPy + scikit-learn +
Qiskit circuit construction; no multiprocessing, no Aer -> Pyodide-compatible).  Timed single-threaded natively so
in-browser time can be estimated (Pyodide is ~3-10x slower than native CPython for NumPy-bound code; see notes).

Blocks:
  1. 5-fold CV (fixed seed, fold-internal scaler+PCA) at n=8 with hyperparameters FIXED to the offline nested-CV choices
     (shipped as constants); accuracy, AUC, sensitivity at the inner-calibrated 98%-sensitivity threshold.
  2. Auditor on the real labels: g_CQ, s_C/s_Q, KTA, task-alignment.
  3. Positive control: Huang-engineered labels -> the same auditor + CV must flag a quantum win.
  4. Concentration mini-curve: off-diagonal variance vs n (2..10) on 120 patients.
  5. IonQ one-job PQK builder: 3 x B circuits for B test patients, run on a local simulator stand-in, counts -> Bloch
     vectors -> PQK rows -> predictions.  (On Qollab: pass the list to ONE backend.run call; read counts, not Sampler.)
"""
import os
os.environ.setdefault("OMP_NUM_THREADS", "1"); os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
import time, json
import numpy as np
from sklearn.model_selection import StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import roc_auc_score
import qk_core as qc

T = {}
t0 = time.time()
X, y = qc.load_wdbc()
N, n = len(y), 8
# offline nested-CV choices (update from exp1_summary.json)
HP = {"RBF_g": 0.03, "RBF_C": 1000.0, "FQK_c": 0.005, "FQK_C": 1000.0, "PQK_c": 0.005, "PQK_g": 0.1, "PQK_C": 100.0, "LR_C": 1.0,
      "JOB_c": 0.05, "JOB_g": 1.0, "JOB_C": 100.0}  # from exp1/exp1b nested-CV modes (n=8); JOB_* = noise-aware choice (exp4/4b)
TARGET = 0.98

# ---------------------------------------------------------------- 1. CV with fixed hyperparameters
rows = {m: {"s": np.zeros(N), "pc": np.zeros(N, int)} for m in ["LR", "RBF", "FQK-full", "PQK"]}
for tr, te in StratifiedKFold(5, shuffle=True, random_state=0).split(X, y):
    Z = qc.fold_features(X, tr, n)
    S = qc.zz_states(Z * HP["FQK_c"], 2, "full")
    Sp = S if HP["PQK_c"] == HP["FQK_c"] else qc.zz_states(Z * HP["PQK_c"], 2, "full")
    Ks = {"RBF": (qc.rbf_kernel_z(Z, HP["RBF_g"]), HP["RBF_C"]), "FQK-full": (qc.fid_kernel(S), HP["FQK_C"]),
          "PQK": (qc.pqk_from_bloch(qc.bloch(Sp, n), HP["PQK_g"], ref_idx=tr), HP["PQK_C"])}
    inner = list(StratifiedKFold(3, shuffle=True, random_state=1).split(np.zeros(len(tr)), y[tr]))
    for m, (K, C) in Ks.items():
        mdl = SVC(kernel="precomputed", C=C).fit(K[np.ix_(tr, tr)], y[tr])
        s = mdl.decision_function(K[np.ix_(te, tr)])
        thr = qc.calib_threshold(y[tr], qc.oof_scores_kernel(K, y, tr, C, inner), TARGET)
        rows[m]["s"][te] = s; rows[m]["pc"][te] = (s >= thr)
    lr = LogisticRegression(C=HP["LR_C"], max_iter=5000)
    s = lr.fit(Z[tr], y[tr]).decision_function(Z[te])
    oof = np.empty(len(tr))
    for a, b in inner:
        oof[b] = LogisticRegression(C=HP["LR_C"], max_iter=5000).fit(Z[tr][a], y[tr][a]).decision_function(Z[tr][b])
    rows["LR"]["s"][te] = s; rows["LR"]["pc"][te] = (s >= qc.calib_threshold(y[tr], oof, TARGET))
res1 = {m: {"acc": float(((r["s"] > 0) == y).mean()), "auc": float(roc_auc_score(y, r["s"])),
            "cal_sens": float(r["pc"][y == 1].mean()), "cal_spec": float(1 - r["pc"][y == 0].mean())} for m, r in rows.items()}
T["1_cv_4models_n8"] = time.time() - t0
print("1.", res1, f"{T['1_cv_4models_n8']:.1f}s", flush=True)

# ---------------------------------------------------------------- 2. auditor on real labels
t1 = time.time()
Z = qc.fold_features(X, np.arange(N), n)
ypm = 2 * y - 1
KC = qc.rbf_kernel_z(Z, HP["RBF_g"])
KQ = qc.fid_kernel(qc.zz_states(Z * HP["FQK_c"], 2, "full"))
aud = {"g_CQ": qc.geo_diff(KC, KQ, 0.1), "sqrtN": float(np.sqrt(N)),
       "s_C/s_Q": qc.model_complexity(KC, ypm, 0.1) / qc.model_complexity(KQ, ypm, 0.1),
       "KTA_C": qc.kta(KC, ypm), "KTA_Q": qc.kta(KQ, ypm)}
T["2_auditor_real"] = time.time() - t1
print("2.", aud, f"{T['2_auditor_real']:.1f}s", flush=True)

# ---------------------------------------------------------------- 3. positive control
t1 = time.time()
KQ2 = qc.fid_kernel(qc.zz_states(Z * 0.75, 2, "full"))
KC2 = qc.rbf_kernel_z(Z, 0.3)
g, v, sQ = qc.geo_diff_vec(KC2, KQ2, 0.1)
f = sQ @ v
yp = (f > np.median(f)).astype(int)
ypp = 2 * yp - 1
pc = {"g_CQ": g, "s_C/s_Q": qc.model_complexity(KC2, ypp, 0.1) / qc.model_complexity(KQ2, ypp, 0.1)}
acc = {"RBF": [], "FQK": []}
for tr, te in StratifiedKFold(5, shuffle=True, random_state=0).split(Z, yp):
    for m, K in [("RBF", KC2), ("FQK", KQ2)]:
        best = max((np.mean([SVC(kernel="precomputed", C=C).fit(K[np.ix_(tr[a], tr[a])], yp[tr[a]]).score(K[np.ix_(tr[b], tr[a])], yp[tr[b]])
                             for a, b in StratifiedKFold(3, shuffle=True, random_state=1).split(tr, yp[tr])]), C) for C in (1, 10, 100))
        acc[m].append(SVC(kernel="precomputed", C=best[1]).fit(K[np.ix_(tr, tr)], yp[tr]).score(K[np.ix_(te, tr)], yp[te]))
pc.update({k: float(np.mean(v_)) for k, v_ in acc.items()})
T["3_positive_control"] = time.time() - t1
print("3.", pc, f"{T['3_positive_control']:.1f}s", flush=True)

# ---------------------------------------------------------------- 4. concentration mini-curve
t1 = time.time()
sub = np.random.default_rng(0).choice(N, 120, replace=False)
conc = {}
for nn in [2, 4, 6, 8, 10]:
    Zn = qc.fold_features(X, np.arange(N), nn)[sub]
    conc[nn] = float(qc.offdiag(qc.fid_kernel(qc.zz_states(Zn, 2, "full"))).var())
T["4_concentration"] = time.time() - t1
print("4.", conc, f"{T['4_concentration']:.1f}s", flush=True)

# ---------------------------------------------------------------- 5. one-job PQK inference (simulator stand-in)
t1 = time.time()
from qiskit import QuantumCircuit
from qiskit.providers.basic_provider import BasicSimulator


def pqk_circuits(x, ent="linear"):
    out = []
    for basis in "XYZ":
        c = QuantumCircuit(n, n)
        pairs = qc.pairs_for(n, ent)
        for _ in range(2):
            c.h(range(n))
            for q in range(n):
                c.p(2 * x[q], q)
            for i, j in pairs:
                c.rzz(2 * (np.pi - x[i]) * (np.pi - x[j]), i, j)
        if basis == "X":
            c.h(range(n))
        elif basis == "Y":
            c.sdg(range(n)); c.h(range(n))
        c.measure(range(n), range(n))
        out.append(c)
    return out


B, SHOTS, ENT = 20, 1000, "linear"
tr, te = next(StratifiedKFold(5, shuffle=True, random_state=0).split(X, y))
Z = qc.fold_features(X, tr, n)
c_ = HP["JOB_c"]
batch = te[:B]
circs = [c for i in batch for c in pqk_circuits(Z[i] * c_, ENT)]
t2 = time.time()
job = BasicSimulator().run(circs, shots=SHOTS, seed_simulator=7)   # on Qollab: backend.run(circs, shots=SHOTS)
counts = job.result().get_counts()
T["5_sim_job_seconds"] = time.time() - t2
Rb = np.zeros((B, n, 3))
for k in range(B):
    for a in range(3):
        cnt = counts[3 * k + a]
        tot = sum(cnt.values())
        for bitstr, m in cnt.items():
            bits = bitstr[::-1]  # little-endian: bits[q] is qubit q
            for q in range(n):
                Rb[k, q, a] += (1 if bits[q] == "0" else -1) * m / tot
Rtr = qc.bloch(qc.zz_states(Z[tr] * c_, 2, ENT), n)
Rte_exact = qc.bloch(qc.zz_states(Z[batch] * c_, 2, ENT), n)
F_tr = Rtr.reshape(len(tr), -1)
d_tr = 0.5 * qc.sqdist(F_tr); med = np.median(qc.offdiag(d_tr))
Ktr = np.exp(-HP["JOB_g"] / med * d_tr)
mdl = SVC(kernel="precomputed", C=HP["JOB_C"]).fit(Ktr, y[tr])
pred_job = mdl.predict(np.exp(-HP["JOB_g"] / med * 0.5 * qc.sqdist(Rb.reshape(B, -1), F_tr)))
pred_exact = mdl.predict(np.exp(-HP["JOB_g"] / med * 0.5 * qc.sqdist(Rte_exact.reshape(B, -1), F_tr)))
T["5_one_job_total"] = time.time() - t1
res5 = {"B": B, "shots": SHOTS, "circuits": len(circs), "acc_job": float((pred_job == y[batch]).mean()),
        "acc_exact": float((pred_exact == y[batch]).mean()), "agree": float((pred_job == pred_exact).mean()),
        "bloch_mae": float(np.abs(Rb - Rte_exact).mean())}
print("5.", res5, f"{T['5_one_job_total']:.1f}s (sim {T['5_sim_job_seconds']:.1f}s)", flush=True)
T["total"] = time.time() - t0
json.dump({"timings_native_1thread_s": T, "cv": res1, "auditor": aud, "positive_control": pc, "concentration": conc, "one_job": res5},
          open("results/judge_run_prototype.json", "w"), indent=1)
print("total", T["total"])
