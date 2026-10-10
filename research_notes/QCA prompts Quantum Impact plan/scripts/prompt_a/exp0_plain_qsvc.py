"""Experiment 0: what the 'plain' tutorial-level Prompt A submission looks like, using the REAL qiskit-machine-learning
0.9.1 API (venv).  Pipeline: StandardScaler -> PCA(n) -> angle scaling, fit on ALL data (as most tutorials/repos do),
zz_feature_map(n, reps=2) [default entanglement='full'], FidelityStatevectorKernel, QSVC (default C=1),
single stratified 80/20 train_test_split.  Repeated over 25 split seeds to show the spread a team might report.

Angle-scaling variants: minmax01 (tutorial-02a style MinMaxScaler), minmax0pi, zscore (no MinMax).
For speed the kernel over all 569 rows is computed once per (n, variant) with qiskit-ML's FidelityStatevectorKernel and
the splits use sklearn SVC(kernel='precomputed') -- identical to QSVC; verified by one real QSVC.fit/score per config.
Also: faithful tutorial-08 QuantumKernelTrainer (shared RY training parameter, SVCLoss, SPSA maxiter=10, lr=0.05,
perturbation=0.05, initial_point=[pi/2]) on n=4 minmax01.
"""
import time, json
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import balanced_accuracy_score
from qiskit import QuantumCircuit
from qiskit.circuit import ParameterVector
from qiskit.circuit.library import zz_feature_map
from qiskit_machine_learning.kernels import FidelityStatevectorKernel, TrainableFidelityStatevectorKernel
from qiskit_machine_learning.algorithms import QSVC
from qiskit_machine_learning.kernels.algorithms import QuantumKernelTrainer
from qiskit_machine_learning.optimizers import SPSA
from qiskit_machine_learning.utils import algorithm_globals
import qk_core as qc

algorithm_globals.random_seed = 123
X, y = qc.load_wdbc()
out = {}
t00 = time.time()
for n in [2, 4, 8]:
    Zs = PCA(n).fit_transform(StandardScaler().fit_transform(X))  # leaky: fit on all rows
    variants = {"minmax01": MinMaxScaler((0, 1)).fit_transform(Zs),
                "minmax0pi": MinMaxScaler((0, np.pi)).fit_transform(Zs),
                "zscore": StandardScaler().fit_transform(Zs)}
    for vname, A in variants.items():
        fm = zz_feature_map(n, reps=2)
        t0 = time.time()
        K = FidelityStatevectorKernel(feature_map=fm).evaluate(A)
        tk = time.time() - t0
        accs, baccs = [], []
        for s in range(25):
            tr, te = train_test_split(np.arange(len(y)), test_size=0.2, stratify=y, random_state=s)
            m = SVC(kernel="precomputed", C=1.0).fit(K[np.ix_(tr, tr)], y[tr])
            p = m.predict(K[np.ix_(te, tr)])
            accs.append((p == y[te]).mean()); baccs.append(balanced_accuracy_score(y[te], p))
        # one real QSVC run (seed 0) to confirm equivalence + timing
        tr, te = train_test_split(np.arange(len(y)), test_size=0.2, stratify=y, random_state=0)
        t1 = time.time()
        q = QSVC(quantum_kernel=FidelityStatevectorKernel(feature_map=fm)).fit(A[tr], y[tr])
        qacc = q.score(A[te], y[te])
        tq = time.time() - t1
        od = qc.offdiag(K)
        out[f"n{n}_{vname}"] = {"acc_mean": float(np.mean(accs)), "acc_min": float(np.min(accs)), "acc_max": float(np.max(accs)),
                                "acc_sd": float(np.std(accs)), "bacc_mean": float(np.mean(baccs)),
                                "frac_pred_benign_seed0": float((SVC(kernel="precomputed", C=1.0).fit(K[np.ix_(tr, tr)], y[tr]).predict(K[np.ix_(te, tr)]) == 0).mean()),
                                "qsvc_seed0_acc": float(qacc), "precomputed_seed0_acc": float(accs[0]),
                                "kernel_offdiag_mean": float(od.mean()), "kernel_offdiag_var": float(od.var()),
                                "qml_kernel_569_seconds": tk, "qsvc_fit_score_seconds": tq}
        print(n, vname, out[f"n{n}_{vname}"], flush=True)
        json.dump(out, open("results/exp0_plain_qsvc.json", "w"), indent=1)

# ---------------- faithful tutorial-08 QKA on WDBC (n=4, minmax01, single split seed 0)
n = 4
Zs = PCA(n).fit_transform(StandardScaler().fit_transform(X))
A = MinMaxScaler((0, 1)).fit_transform(Zs)
tr, te = train_test_split(np.arange(len(y)), test_size=0.2, stratify=y, random_state=0)
tp = ParameterVector("θ", 1)
fm0 = QuantumCircuit(n)
for q in range(n):
    fm0.ry(tp[0], q)
fm = fm0.compose(zz_feature_map(n))
qk = TrainableFidelityStatevectorKernel(feature_map=fm, training_parameters=tp)
log = []
spsa = SPSA(maxiter=10, learning_rate=0.05, perturbation=0.05, callback=lambda *a: log.append(float(a[2])))
qkt = QuantumKernelTrainer(quantum_kernel=qk, loss="svc_loss", optimizer=spsa, initial_point=[np.pi / 2])
t0 = time.time()
res = qkt.fit(A[tr], y[tr])
tfit = time.time() - t0
qsvc = QSVC(quantum_kernel=res.quantum_kernel).fit(A[tr], y[tr])
acc_after = qsvc.score(A[te], y[te])
qk0 = TrainableFidelityStatevectorKernel(feature_map=fm, training_parameters=tp)
qk0.assign_training_parameters([np.pi / 2])
acc_before = QSVC(quantum_kernel=qk0).fit(A[tr], y[tr]).score(A[te], y[te])
out["tutorial08_QKA_n4"] = {"theta_opt": [float(v) for v in res.optimal_point], "loss_final": float(res.optimal_value),
                            "loss_trace": log, "acc_before(theta=pi/2)": float(acc_before), "acc_after": float(acc_after),
                            "fit_seconds": tfit, "n_train": int(len(tr))}
print("QKA", out["tutorial08_QKA_n4"], flush=True)
json.dump(out, open("results/exp0_plain_qsvc.json", "w"), indent=1)
print("total", time.time() - t00)
