"""Prompt C, step 9: fault-tolerant resource / crossover model for 'Grover the Seismologist'.

Quantum time  T_q = (pi/4) sqrt(N/M) * Toff_per_iter * t_toff
  Toff_per_iter = 2*Lookup(N,b) + 4*b (two comparators, compute+uncompute) + 2*n (diffusion ladder) [+ W_q for an expensive check]
  Lookup: unary-iteration QROM ~ N Toffoli-equivalents (Babbush et al. 2018: 4N T gates), or select-swap QROAM ~ 2*sqrt(N*b)
          (balanced N/lam + b*lam; Low-Kliuchnikov-Schaeffer 2018 style trade-off, needs ~b*sqrt(N/b) extra qubits)
  t_toff: 170 us (Babbush et al. 2021 superconducting surface code), 17 ms (their 10 kHz ion-trap cycle), 1.7 us (100x faster distillation)
Classical:
  cheap check (data in RAM): measured numpy filter ~3 ns/row (c08) -> scan N/(M+1) * t_row, or index ~ (log2 N + M) * t_row
  expensive check: W classical ops at t_op = 0.33 ns (3 GHz core); reversible version W_q = W Toffolis (optimistic 1:1)
"""
import math, json, os
HERE = os.path.dirname(os.path.abspath(__file__))
T_TOFF = {"SC surface code 170us (Babbush'21)": 170e-6, "ion trap 17ms (Babbush'21 10kHz)": 17e-3, "100x faster distillation 1.7us": 1.7e-6}
T_ROW = 3e-9; T_OP = 0.33e-9; b = 9

def toff_iter(N, lookup="unary", Wq=0.0):
    n = math.ceil(math.log2(N))
    L = N if lookup == "unary" else 2 * math.sqrt(N * b)
    return 2 * L + 4 * b + 2 * n + Wq

out = {"cheap": [], "expensive": []}
print("A) Cheap check (depth/mag compare on data in memory). Quantum/classical time ratio (M=1):")
for N in (64, 1504, 155_899, 10**7, 10**9):
    for lk in ("unary", "qroam"):
        Tq = math.pi / 4 * math.sqrt(N) * toff_iter(N, lk) * 170e-6
        Tc = (N + 1) / 2 * T_ROW; Ti = (math.log2(N) + 1) * T_ROW
        out["cheap"].append(dict(N=N, lookup=lk, Tq_s=Tq, T_scan_s=Tc, T_index_s=Ti))
        print(f"  N={N:>13,d} {lk:5s}: T_quantum(170us Toffoli)={Tq:10.3e} s | classical scan {Tc:9.2e} s | indexed {Ti:9.2e} s | ratio q/scan={Tq/Tc:9.2e}")

print("\nB) Expensive black-box check: crossover N* where (pi/4)sqrt(N)(W*t_toff + lookup) = (N/2) W t_op  (M=1, 1 classical core)")
for W_label, W in (("1 s of CPU (3e9 ops)", 3e9), ("1 core-hour (1.1e13 ops)", 1.08e13), ("CyberShake-site 55k core-h (6e17 ops)", 55e3 * 1.08e13)):
    for tl, tt in T_TOFF.items():
        # ignore lookup when W dominates; solve sqrt(N*) = (pi/2) * t_toff/t_op  (from (pi/4)sqrtN W t_toff = (N/2) W t_op)
        sN = (math.pi / 2) * tt / T_OP
        Nstar = sN**2
        T_class_at = Nstar / 2 * W * T_OP
        out["expensive"].append(dict(check=W_label, t_toff=tl, N_star=Nstar, classical_time_at_crossover_s=T_class_at))
        print(f"  {W_label:38s} | {tl:34s}: N* = {Nstar:9.2e} events; classical time at N* = {T_class_at/3.15e7:9.2e} core-years")
print("\n  (N* is independent of W when the check dominates; parallel classical with P cores multiplies N* by ~P^2.)")
print("  Reference sizes: 2024 USGS ComCat all magnitudes = 155,899 events (FDSN count, fetched 2026-10-10); M>=5: 1,507.")

# C) per-query logical Toffolis for the honest oracle at catalog sizes, and the Grover total
print("\nC) Honest-oracle logical cost at catalog sizes (b=9 bits/event, M = real shallow&M>=6 rate 4.8% and M=1):")
for N in (1504, 155_899):
    for M in (1, round(0.0479 * N)):
        k = math.floor(math.pi / 4 * math.sqrt(N / M))
        for lk in ("unary", "qroam"):
            tot = k * toff_iter(N, lk)
            print(f"  N={N:>7,d} M={M:5d}: k={k:4d} iterations x {toff_iter(N, lk):10.0f} Toffoli/iter ({lk}) = {tot:10.3e} Toffolis "
                  f"= {tot*170e-6:9.3e} s at 170us | classical scan ~{(N+1)/(M+1):8.1f} checks x 3 ns = {(N+1)/(M+1)*3e-9:8.1e} s")
json.dump(out, open(os.path.join(HERE, "results_c09_ft_crossover.json"), "w"), indent=1)
