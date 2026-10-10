"""Experiment 3c: OUT-OF-SAMPLE validation of the auditor rule, frozen (written into this file) BEFORE running it on
fresh label sets.  The rule was calibrated on the exp3 label sets (exp3b); here it predicts, then nested CV judges.

FROZEN RULE (top-30 spectral task-model alignment, family maxima, centred labels):
  A_C = max over {RBF grid, linear} of fraction of label power in the top-30 kernel eigenvectors
  A_Q = max over {FQK-full grid, FQK-linear grid, PQK grid}
  'quantum-favourable'   if A_Q - A_C >= 0.10 and A_Q >= 0.20
  'classical-favourable' if A_C - A_Q >= 0.10 and A_C >= 0.20
  'unlearnable'          if max(A_C, A_Q) < 0.20
  'no clear edge'        otherwise
Fresh label sets (n = 8, same global features as exp3):
  HUANG-lin(c=0.35)  Huang construction against the LINEAR-entanglement kernel (K_C = RBF g=1)
  HUANG(c=0.1)       Huang construction, full map, K_C = RBF g=0.1
  OBS-1q5(c=0.35)    sign of <Z_5> at c=0.35
  OBS-2(c=0.1)       sign of <Z_1 Z_4> at c=0.1
  REVERSE-HUANG      classical-favourable: top eigvec of sqrt(K_C)(K_Q+lam)^-1 sqrt(K_C), K_C=RBF g=1, K_Q=FQK c=0.35
  SHUFFLED           permuted real labels
  REAL+20%flip       real labels with 20% flipped
"""
import os
os.environ.setdefault("OMP_NUM_THREADS", "4")
import json, time
import numpy as np
from sklearn.model_selection import StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
import qk_core as qc
import exp3_positive_control as e3
from exp1_nested_cv import fit_eval_feat

t0 = time.time()
Z, n, N = e3.Z, e3.n, len(e3.yreal)
FQKL, PQK = e3.extra()
classical = {f"RBF g={g}": K for g, K in e3.RBF.items()}
classical["Linear"] = Z @ Z.T + 1.0
quantum = {f"FQK c={c}": K for c, K in e3.FQK.items()}
quantum.update({f"FQK-linear c={c}": K for c, K in FQKL.items()})
quantum.update({f"PQK c={c} g={g}": K for (c, g), K in PQK.items()})
EIG = {k: np.linalg.eigh((K + K.T) / 2)[1][:, ::-1][:, :30] for k, K in {**classical, **quantum}.items()}


def align30(keys, ypm):
    yc = ypm - ypm.mean()
    best = (-1, None)
    for k in keys:
        a = float(((EIG[k].T @ yc) ** 2).sum() / (yc @ yc))
        if a > best[0]:
            best = (a, k)
    return best


def verdict(AC, AQ):
    if AQ - AC >= 0.10 and AQ >= 0.20:
        return "quantum-favourable"
    if AC - AQ >= 0.10 and AC >= 0.20:
        return "classical-favourable"
    if max(AC, AQ) < 0.20:
        return "unlearnable"
    return "no clear edge"


rng = np.random.default_rng(99)
labels = {}
g_, v, sQ = qc.geo_diff_vec(qc.rbf_kernel_z(Z, 1.0), FQKL[0.35], 0.1); f = sQ @ v
labels["HUANG-lin(c=0.35)"] = (f > np.median(f)).astype(int)
g_, v, sQ = qc.geo_diff_vec(e3.RBF[0.1], e3.FQK[0.1], 0.1); f = sQ @ v
labels["HUANG(c=0.1)"] = (f > np.median(f)).astype(int)
f = e3.zstring_expect(e3.states[0.35], [5]); labels["OBS-1q5(c=0.35)"] = (f > np.median(f)).astype(int)
f = e3.zstring_expect(e3.states[0.1], [1, 4]); labels["OBS-2(c=0.1)"] = (f > np.median(f)).astype(int)
g_, v, sC = qc.geo_diff_vec(e3.FQK[0.35], qc.rbf_kernel_z(Z, 1.0), 0.1); f = sC @ v   # roles swapped
labels["REVERSE-HUANG"] = (f > np.median(f)).astype(int)
labels["SHUFFLED"] = rng.permutation(e3.yreal)
yy = e3.yreal.copy(); fl = rng.choice(N, int(0.2 * N), replace=False); yy[fl] = 1 - yy[fl]
labels["REAL+20%flip"] = yy

RBFx = dict(e3.RBF); RBFx[1.0] = qc.rbf_kernel_z(Z, 1.0)
out = {}
for name, y in labels.items():
    ypm = 2 * y - 1
    AC, kc = align30(classical, ypm)
    AQ, kq = align30(quantum, ypm)
    pred = verdict(AC, AQ)
    accs = {m: [] for m in ["LR", "RBF", "FQK-full", "FQK-linear", "PQK"]}
    for tr, te in StratifiedKFold(5, shuffle=True, random_state=4000).split(Z, y):
        splits = list(StratifiedKFold(3, shuffle=True, random_state=1).split(np.zeros(len(tr)), y[tr]))
        r = fit_eval_feat(lambda C: LogisticRegression(C=C, max_iter=5000), [{"C": c} for c in [0.01, 0.1, 1, 10, 100]], Z, y, tr, te, splits)
        accs["LR"].append((r["pred"] == y[te]).mean())
        for m, Ks in [("RBF", RBFx), ("FQK-full", e3.FQK), ("FQK-linear", FQKL), ("PQK", PQK)]:
            r = qc.fit_eval_kernel(Ks, y, tr, te, 1, Cs=(1.0, 10.0, 100.0, 1000.0))
            accs[m].append((r["pred"] == y[te]).mean())
    acc = {m: float(np.mean(v)) for m, v in accs.items()}
    bc = max(acc["LR"], acc["RBF"]); bq = max(acc["FQK-full"], acc["FQK-linear"], acc["PQK"])
    observed = ("quantum-favourable" if bq - bc >= 0.05 else "classical-favourable" if bc - bq >= 0.05
                else ("unlearnable" if max(bc, bq) < 0.6 else "no clear edge"))
    out[name] = {"A_C": AC, "A_C_kernel": kc, "A_Q": AQ, "A_Q_kernel": kq, "predicted": pred, "acc": acc,
                 "observed(5pt rule)": observed, "match": pred == observed}
    print(name, f"A_C={AC:.3f} A_Q={AQ:.3f} predicted={pred} | acc={ {k: round(v, 3) for k, v in acc.items()} } observed={observed}",
          f"{time.time()-t0:.0f}s", flush=True)
json.dump(out, open("results/exp3c_auditor_validation.json", "w"), indent=1)
print("matches:", sum(v["match"] for v in out.values()), "/", len(out))
