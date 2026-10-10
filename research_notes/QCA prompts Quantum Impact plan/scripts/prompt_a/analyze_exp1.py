"""Summarise exp1: metrics on pooled out-of-fold predictions (averaged over 5 repeats), 95% CIs by patient-level
bootstrap (2,000 resamples; the same resample applied to every repeat), paired differences vs reference models
(bootstrap CI + Nadeau-Bengio corrected repeated-CV t interval over the 25 outer folds)."""
import pickle, json
from collections import Counter
import numpy as np
from scipy import stats
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_auc_score
import qk_core as qc

raw = pickle.load(open("results/exp1_raw.pkl", "rb"))
import os
if os.path.exists("results/exp1b_raw.pkl"):
    raw.update(pickle.load(open("results/exp1b_raw.pkl", "rb")))
X, y = qc.load_wdbc()
N = len(y)
REPS = 5
folds = {rep: [te for _, te in StratifiedKFold(5, shuffle=True, random_state=1000 + rep).split(X, y)] for rep in range(REPS)}
models = sorted({(m, n) for (m, n, r) in raw}, key=lambda t: (t[1], t[0]))
rng = np.random.default_rng(0)
B = 2000
boot = [rng.integers(0, N, N) for _ in range(B)]


def fast_auc(yb, sb):
    pos = yb == 1
    npos, nneg = pos.sum(), (~pos).sum()
    r = stats.rankdata(sb)
    return (r[pos].sum() - npos * (npos + 1) / 2) / (npos * nneg)


def metrics_rep(d, idx=None):
    yy, s, p, pc = y, d["scores"], d["pred"], d["pred_cal"]
    if idx is not None:
        yy, s, p, pc = yy[idx], s[idx], p[idx], pc[idx]
    return {"acc": (p == yy).mean(), "auc": fast_auc(yy, s), "sens@spec95": qc.sens_at_spec(yy, s, 0.95),
            "cal_sens": pc[yy == 1].mean(), "cal_spec": 1 - pc[yy == 0].mean(),
            "sens": p[yy == 1].mean(), "spec": 1 - p[yy == 0].mean()}


summary = {}
point = {}
bootvals = {}
for (m, n) in models:
    reps = [raw[(m, n, r)] for r in range(REPS) if (m, n, r) in raw]
    pm = [metrics_rep(d) for d in reps]
    est = {k: float(np.mean([x[k] for x in pm])) for k in pm[0]}
    bv = {k: np.empty(B) for k in ("acc", "auc", "sens@spec95", "cal_sens", "cal_spec")}
    for b, idx in enumerate(boot):
        mb = [metrics_rep(d, idx) for d in reps]
        for k in bv:
            bv[k][b] = np.mean([x[k] for x in mb])
    ci = {k: [float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))] for k, v in bv.items()}
    fold_acc = np.array([[(d["pred"][te] == y[te]).mean() for te in folds[r]] for r, d in enumerate(reps)]).ravel()
    keys = Counter(str(f["key"]) for d in reps for f in d["folds"])
    Cs = Counter(str(f["C"]) for d in reps for f in d["folds"])
    nsv = [f["n_sv"] for d in reps for f in d["folds"] if f["n_sv"] is not None]
    extra = {}
    for kx in ("x_kta_init", "x_kta_final", "x_loss_init", "x_loss_final", "x_offdiag_mean"):
        v = [f[kx] for d in reps for f in d["folds"] if kx in f]
        if v:
            extra[kx] = float(np.mean(v))
    summary[f"{m}|{n}"] = {"model": m, "n": n, **est, "CI95": ci, "fold_acc_mean": float(fold_acc.mean()),
                           "fold_acc_sd": float(fold_acc.std()), "selected_keys": dict(keys.most_common(6)),
                           "selected_C": dict(Cs.most_common(6)), "n_sv_mean": float(np.mean(nsv)) if nsv else None, **extra}
    point[(m, n)] = fold_acc
    bootvals[(m, n)] = bv
    print(f"{m:12s} n={n:2d} acc={est['acc']:.4f} [{ci['acc'][0]:.3f},{ci['acc'][1]:.3f}] auc={est['auc']:.4f} "
          f"sens@spec95={est['sens@spec95']:.3f} cal_sens={est['cal_sens']:.3f} cal_spec={est['cal_spec']:.3f} keys={dict(keys.most_common(3))}")


def nb_ci(a, b, k=25, ratio=0.25):
    d = a - b
    var = d.var(ddof=1) * (1 / k + ratio)
    t = stats.t.ppf(0.975, k - 1)
    return [float(d.mean() - t * np.sqrt(var)), float(d.mean() + t * np.sqrt(var))]


diffs = {}
refs = [("RBF-30", 30), ("LR-30", 30)]
for (m, n) in models:
    for ref in refs + [("RBF-PCA", n)]:
        if ref not in bootvals or ref == (m, n):
            continue
        dacc = bootvals[(m, n)]["acc"] - bootvals[ref]["acc"]
        dauc = bootvals[(m, n)]["auc"] - bootvals[ref]["auc"]
        diffs[f"{m}|{n} - {ref[0]}|{ref[1]}"] = {
            "d_acc": float(summary[f'{m}|{n}']['acc'] - summary[f'{ref[0]}|{ref[1]}']['acc']),
            "d_acc_boot_CI95": [float(np.percentile(dacc, 2.5)), float(np.percentile(dacc, 97.5))],
            "d_acc_NB_CI95": nb_ci(point[(m, n)], point[ref]),
            "d_auc": float(summary[f'{m}|{n}']['auc'] - summary[f'{ref[0]}|{ref[1]}']['auc']),
            "d_auc_boot_CI95": [float(np.percentile(dauc, 2.5)), float(np.percentile(dauc, 97.5))]}

json.dump({"summary": summary, "diffs": diffs}, open("results/exp1_summary.json", "w", encoding="utf-8"), indent=1)

# markdown table
lines = ["| n | Model | Accuracy [95% CI] | AUC [95% CI] | Sens @ 95% spec | Deployable sens / spec (thr. for 98% sens) | Most-selected hyperparams |",
         "|---|---|---|---|---|---|---|"]
for (m, n) in models:
    s = summary[f"{m}|{n}"]
    c = s["CI95"]
    lines.append(f"| {n} | {m} | {s['acc']:.3f} [{c['acc'][0]:.3f}, {c['acc'][1]:.3f}] | {s['auc']:.4f} [{c['auc'][0]:.3f}, {c['auc'][1]:.3f}] | "
                 f"{s['sens@spec95']:.3f} | {s['cal_sens']:.3f} / {s['cal_spec']:.3f} | {list(s['selected_keys'].items())[:2]} |")
open("results/exp1_table.md", "w", encoding="utf-8").write("\n".join(lines) + "\n")
lines = ["| Comparison | Δacc | bootstrap 95% CI | Nadeau-Bengio 95% CI | ΔAUC [boot CI] |", "|---|---|---|---|---|"]
for k, v in diffs.items():
    lines.append(f"| {k} | {v['d_acc']:+.4f} | [{v['d_acc_boot_CI95'][0]:+.3f}, {v['d_acc_boot_CI95'][1]:+.3f}] | "
                 f"[{v['d_acc_NB_CI95'][0]:+.3f}, {v['d_acc_NB_CI95'][1]:+.3f}] | {v['d_auc']:+.4f} [{v['d_auc_boot_CI95'][0]:+.3f}, {v['d_auc_boot_CI95'][1]:+.3f}] |")
open("results/exp1_diffs.md", "w", encoding="utf-8").write("\n".join(lines) + "\n")
print("saved")
