"""Prompt C, step 11: noise horizon under two 2Q-cost assumptions for an n-qubit MCZ:
 (q) Qiskit ancilla-free synthesis to rzz (measured, c05 table) and (b) IonQ billing 6(n-2).
Global-depolarizing model at forte-1 rates (validated vs density matrix in c04, within ~0.01-0.04).
Needle case M=1. Reports P at k_opt, classical P with k+1 checks, and noise-aware expected cost (k+1)/P(k) vs (N+1)/2."""
import math, json
P2, P1 = 4.95e-3, 2.67e-4
qiskit_mcz = {3: 5, 4: 13, 5: 27, 6: 73, 7: 113, 8: 165, 9: 231, 10: 305}
out = []
for n in range(3, 13):
    N = 2**n; th = math.asin(1 / math.sqrt(N)); kopt = math.floor(math.pi / (4 * th))
    row = dict(n=n, N=N, k_opt=kopt)
    for lab, c in (("qiskit", qiskit_mcz.get(n)), ("ionq_billed", 6 * (n - 2))):
        if c is None: continue
        best = None
        for k in range(0, kopt + 1):
            F = (1 - 15 / 16 * P2) ** (2 * c * k)
            p = F * math.sin((2 * k + 1) * th) ** 2 + (1 - F) / N
            cost = (k + 1) / p
            if best is None or cost < best[1]: best = (k, cost, p)
        F = (1 - 15 / 16 * P2) ** (2 * c * kopt)
        pk = F * math.sin((2 * kopt + 1) * th) ** 2 + (1 - F) / N
        pcl = 1 - (N - (kopt + 1)) / N
        row[lab] = dict(twoq_per_iter=2 * c, p_at_kopt=pk, p_classical_same_budget=pcl, best_k=best[0], best_cost=best[1], classical_cost=(N + 1) / 2)
    out.append(row)
    s = f"n={n:2d} N={N:5d} k_opt={kopt:3d} | "
    for lab in ("qiskit", "ionq_billed"):
        if lab in row:
            r = row[lab]; s += f"{lab}: 2Q/iter={r['twoq_per_iter']:4d} P(k_opt)={r['p_at_kopt']:.3f} vs cl {r['p_classical_same_budget']:.3f}; best k={r['best_k']:2d} E={r['best_cost']:7.1f} vs cl {r['classical_cost']:7.1f} | "
    print(s)
json.dump(out, open("results_c11_billed_noise_horizon.json", "w"), indent=1)
