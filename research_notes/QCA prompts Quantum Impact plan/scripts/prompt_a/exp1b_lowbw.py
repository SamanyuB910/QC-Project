"""Experiment 1b: same nested-CV protocol as exp1 (same outer/inner seeds), quantum kernels only, with the bandwidth grid
extended DOWNWARD because exp1/exp2 showed inner CV selecting the smallest bandwidth (0.02) at n = 8-12 for the
full-entanglement ZZ map.  Extending a grid whose edge is selected is standard grid design; selection stays nested.
Models: FQK-full, FQK-linear, SEP, PQK(full states), PQK-linear (linear states).
"""
import os
os.environ.setdefault("OMP_NUM_THREADS", "1"); os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
import time, pickle
import numpy as np
from multiprocessing import Pool
from sklearn.model_selection import StratifiedKFold
import qk_core as qc

BW = [0.0025, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.35, 0.75]
PQK_G = [0.1, 0.3, 1.0, 3.0]


def run_task(args):
    n, rep = args
    t0 = time.time()
    X, y = qc.load_wdbc()
    outer = StratifiedKFold(5, shuffle=True, random_state=1000 + rep)
    res = {}
    def put(name, te, r):
        d = res.setdefault(name, {"scores": np.full(len(y), np.nan), "pred": np.full(len(y), -1), "pred_cal": np.full(len(y), -1), "folds": []})
        d["scores"][te] = r["scores"]; d["pred"][te] = r["pred"]; d["pred_cal"][te] = r["pred_cal"]
        d["folds"].append({k: r[k] for k in ("key", "C", "inner_acc", "n_sv", "thr")})
    for f, (tr, te) in enumerate(outer.split(X, y)):
        seed = 10 * rep + f
        Z = qc.fold_features(X, tr, n, seed=0)
        for ent, tag in [("full", "FQK-full"), ("linear", "FQK-linear"), ("none", "SEP")]:
            Ks, pq = {}, {}
            for c in BW:
                S = qc.zz_states(Z * c, 2, ent)
                Ks[c] = qc.fid_kernel(S)
                if ent in ("full", "linear"):
                    R = qc.bloch(S, n)
                    for g in PQK_G:
                        pq[(c, g)] = qc.pqk_from_bloch(R, g, ref_idx=tr)
                del S
            put(tag + "*", te, qc.fit_eval_kernel(Ks, y, tr, te, seed, 0.98))
            if pq:
                put(("PQK*" if ent == "full" else "PQK-linear*"), te, qc.fit_eval_kernel(pq, y, tr, te, seed, 0.98))
        print(f"n={n} rep={rep} fold={f} {time.time()-t0:.0f}s", flush=True)
    return n, rep, res


if __name__ == "__main__":
    tasks = [(n, r) for n in [12, 8, 4] for r in range(5)]
    with Pool(8) as pool:
        out = pool.map(run_task, tasks, chunksize=1)
    allres = {}
    for n, rep, res in out:
        for name, d in res.items():
            allres[(name, n, rep)] = d
    pickle.dump(allres, open("results/exp1b_raw.pkl", "wb"))
    print("saved")
