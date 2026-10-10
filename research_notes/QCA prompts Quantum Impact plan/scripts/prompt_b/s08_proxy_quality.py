"""Step 8: how good is each QUBO (relevance estimator x lambda x mu) as a proxy for downstream CV AUC at a given cost?
Uses the all-subsets CV AUCs from s05 (C). Regret = best AUC achievable at <= the panel's cost minus the panel's AUC."""
import numpy as np
from scipy.stats import spearmanr
from common import *
from qsim import Inst
from s06_helpers import cost_vector
from s07_robustness import binned_mi, perm_debiased  # noqa  (re-runs s07 prints; harmless)

X, y, _ = load_data()
z = np.load(os.path.join(OUT, "s05_all_subsets.npz"))
st, au, co = z["states"], z["aucs"], z["costs"]
m5 = np.array([bin(int(v)).count("1") == K for v in st])
auc5 = dict(zip(st[m5].tolist(), au[m5]))
COST = cost_vector()
C = redundancy(X)
ests = {
    "kNN-MI k=3 (sklearn default)": relevance(X, y, n_neighbors=3)[0],
    "kNN-MI k=10": relevance(X, y, n_neighbors=10)[0],
    "binned MI(5) - perm null": np.clip(perm_debiased(X, y, lambda X, y: binned_mi(X, y, 5))[0], 0, None),
}


def best_auc_at(cost):
    m = m5 & (co <= cost + 1e-9)
    return au[m].max()


res = {}
print("\nProxy quality: QUBO optimum's 5-panel CV-AUC vs the best 5-panel AUC at the same or lower cost")
for en, r in ests.items():
    for lam in [0.0, 0.1, 0.2, 0.5]:
        rel = BITS[st[m5]] @ r
        red = 0.5 * np.einsum("si,ij,sj->s", BITS[st[m5]].astype(float), C, BITS[st[m5]].astype(float))
        rho = spearmanr(-rel + lam * red, -au[m5]).correlation
        rows = []
        for mu in [0, 0.02, 0.05, 0.1, 0.2]:
            I = Inst(r, C, lam, extra=mu * COST / 100)
            s = int(I.opt)
            a = auc5[s]; c = COST[s]
            rows.append((mu, round(c, 2), round(a, 3), round(best_auc_at(c) - a, 3)))
        res[f"{en}|lam{lam}"] = {"spearman": rho, "rows": rows}
        print(f"  {en:30s} lam={lam:3.1f} Spearman(f,-AUC)={rho:+.2f} | (mu, cost, AUC, regret): {rows}")
save_json("s08_proxy_quality.json", res)
