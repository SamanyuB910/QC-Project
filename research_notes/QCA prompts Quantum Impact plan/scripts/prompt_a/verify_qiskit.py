"""Verify the NumPy zz_feature_map simulator against Qiskit 2.x + qiskit-machine-learning 0.9.1,
and time the 'plain' FidelityStatevectorKernel path (proxy for in-browser cost).
Run with the venv:  .venv/Scripts/python verify_qiskit.py
"""
import time, json, sys
import numpy as np
from qiskit.circuit.library import zz_feature_map
from qiskit.quantum_info import Statevector, partial_trace, DensityMatrix
from qiskit_machine_learning.kernels import FidelityStatevectorKernel
import qk_core as qc

rng = np.random.default_rng(1)
out = {}
for n in [2, 3, 4, 5]:
    for ent in ["full", "linear"]:
        fm = zz_feature_map(n, reps=2, entanglement=ent)
        X = rng.uniform(-1.5, 2.5, size=(6, n))
        S = qc.zz_states(X, reps=2, ent=ent)
        maxerr = 0.0
        for i in range(len(X)):
            sv = Statevector(fm.assign_parameters(X[i])).data
            ov = abs(np.vdot(sv, S[i])) ** 2
            ovc = abs(np.vdot(sv, S[i].conj())) ** 2
            maxerr = max(maxerr, 1 - max(ov, ovc))
        K_np = qc.fid_kernel(S)
        K_q = FidelityStatevectorKernel(feature_map=fm).evaluate(X)
        # bloch vs partial trace
        R = qc.bloch(S, n)
        bl_err = 0.0
        for i in range(2):
            dm = DensityMatrix(Statevector(fm.assign_parameters(X[i])))
            for k in range(n):
                rk = partial_trace(dm, [q for q in range(n) if q != k]).data
                bx, by, bz = 2 * rk[0, 1].real, 2 * rk[1, 0].imag, (rk[0, 0] - rk[1, 1]).real
                bl_err = max(bl_err, abs(abs(bx) - abs(R[i, k, 0])), abs(abs(by) - abs(R[i, k, 1])), abs(bz - R[i, k, 2]))
        out[f"n{n}_{ent}"] = {"state_infidelity_max": maxerr, "kernel_maxabs_diff": float(np.abs(K_np - K_q).max()),
                              "bloch_maxabs_diff": bl_err,
                              "gates": dict(fm.decompose().count_ops())}
        print(n, ent, out[f"n{n}_{ent}"])

# timing: plain qiskit-ML FidelityStatevectorKernel vs numpy for N=569
X, y = qc.load_wdbc()
timing = {}
for n in [4, 8, 12]:
    Z = qc.fold_features(X, np.arange(len(y)), n)
    Z = (Z - Z.min(0)) / (Z.max(0) - Z.min(0))
    fm = zz_feature_map(n, reps=2)
    t0 = time.time()
    K1 = FidelityStatevectorKernel(feature_map=fm).evaluate(Z)
    t1 = time.time()
    S = qc.zz_states(Z, reps=2, ent="full")
    K2 = qc.fid_kernel(S)
    t2 = time.time()
    timing[n] = {"qml_FidelityStatevectorKernel_569x569_s": t1 - t0, "numpy_569x569_s": t2 - t1,
                 "maxdiff": float(np.abs(K1 - K2).max())}
    print("timing", n, timing[n])
out["timing_native"] = timing
json.dump(out, open("results/verify_qiskit.json", "w"), indent=1)
