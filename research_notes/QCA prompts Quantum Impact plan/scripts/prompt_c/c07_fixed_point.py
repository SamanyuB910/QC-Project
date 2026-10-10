"""Prompt C, step 7: fixed-point amplitude amplification (Yoder, Low, Chuang, PRL 113, 210501, 2014)
vs plain Grover when M is unknown, on real slices. Exact simulation in the N-dim space (N<=64),
plus a Qiskit circuit for one case (gate count + statevector check).

YLC: G(a,b) = -S_s(a) S_t(b), S_s(a)=I-(1-e^{-ia})|s><s|, S_t(b)=I-(1-e^{ib})P_T,
L=2l+1, gamma^{-1}=T_{1/L}(1/delta), a_j = -b_{l-j+1} = 2 arccot(tan(2 pi j/L) sqrt(1-gamma^2)),
P_L = 1 - delta^2 T_L(T_{1/L}(1/delta) sqrt(1-lambda))^2 ; P_L >= 1-delta^2 for lambda >= w if L >= ln(2/delta)/sqrt(w).
"""
import json, os, math, warnings
import numpy as np
warnings.filterwarnings("ignore")
import gs_core as G

def cheb(L, x):
    x = complex(x)
    return np.cosh(L * np.arccosh(x)).real if abs(x) >= 1 else math.cos(L * math.acos(x.real))

def arccot(x):
    return math.pi / 2 - math.atan(x)

def ylc_phases(l, delta):
    L = 2 * l + 1
    gam_inv = cheb(1.0 / L, 1.0 / delta)
    g = 1.0 / gam_inv
    a = [2 * arccot(math.tan(2 * math.pi * j / L) * math.sqrt(1 - g * g)) for j in range(1, l + 1)]
    b = [-a[l - j] for j in range(1, l + 1)]   # b_j = -a_{l-j+1}
    return a, b

def run_fpaa(N, marked, l, delta):
    a, b = ylc_phases(l, delta)
    s = np.ones(N, complex) / math.sqrt(N)
    T = np.zeros(N); T[list(marked)] = 1
    psi = s.copy()
    for aj, bj in zip(a, b):
        psi = psi - (1 - np.exp(1j * bj)) * T * psi                     # S_t(b)
        psi = psi - (1 - np.exp(-1j * aj)) * s * (s.conj() @ psi)        # S_s(a)
        psi = -psi
    return float(np.sum(np.abs(psi[list(marked)]) ** 2))

def p_formula(N, M, l, delta):
    L = 2 * l + 1; lam = M / N
    return 1 - delta**2 * cheb(L, cheb(1.0 / L, 1.0 / delta) * math.sqrt(1 - lam)) ** 2

# check the implementation against the closed form
for (N, M, l, d) in [(64, 1, 6, 0.5), (64, 3, 6, 0.5), (32, 2, 4, 0.3), (16, 1, 3, 0.5)]:
    sim = run_fpaa(N, range(M), l, d); fm = p_formula(N, M, l, d)
    print(f"[check] N={N} M={M} l={l} delta={d}: simulated {sim:.6f}  closed-form {fm:.6f}")
    assert abs(sim - fm) < 1e-9

rows = G.load_catalog()
rng = np.random.default_rng(3)
out = {"curves": {}, "real": {}}
# design for "at least one match" (w = 1/N) with delta=0.5 (P>=0.75)
for n in (4, 5, 6):
    N = 2**n; w = 1 / N; delta = 0.5
    L = math.ceil(math.log(2 / delta) / math.sqrt(w)); L += (L % 2 == 0); l = (L - 1) // 2
    kG = G.k_opt(N, 1)   # Grover tuned for the rarest case M=1 (what you'd do without knowing M)
    Ms = list(range(1, 13))
    out["curves"][n] = dict(N=N, l_fpaa=l, delta=delta, grover_k=kG, M=Ms,
                            p_fpaa=[p_formula(N, M, l, delta) for M in Ms],
                            p_grover=[G.p_success_theory(N, M, kG) for M in Ms])
    print(f"\nn={n} N={N}: FPAA l={l} iterations (L={L}, delta={delta}) vs Grover k={kG} (tuned for M=1)")
    print("   M      : " + " ".join(f"{M:5d}" for M in Ms))
    print("   FPAA P : " + " ".join(f"{p:5.3f}" for p in out["curves"][n]["p_fpaa"]))
    print("   Grover : " + " ".join(f"{p:5.3f}" for p in out["curves"][n]["p_grover"]))
    # real slices (M>=1): expected cost (iterations+1 verification)/P with restarts
    costs_f, costs_g, ps_f, ps_g = [], [], [], []
    for _ in range(3000):
        sl = G.slice_events(rows, n, rng); M = len(G.marked_indices(sl))
        if M == 0: continue
        pf = p_formula(N, M, l, delta); pg = G.p_success_theory(N, M, kG)
        ps_f.append(pf); ps_g.append(pg)
        costs_f.append((l + 1) / pf); costs_g.append((kG + 1) / max(pg, 1e-9))
    out["real"][n] = dict(mean_P_fpaa=float(np.mean(ps_f)), min_P_fpaa=float(np.min(ps_f)),
                          mean_P_grover=float(np.mean(ps_g)), min_P_grover=float(np.min(ps_g)),
                          median_cost_fpaa=float(np.median(costs_f)), mean_cost_fpaa=float(np.mean(costs_f)),
                          median_cost_grover=float(np.median(costs_g)), mean_cost_grover=float(np.mean(costs_g)))
    r = out["real"][n]
    print(f"   real slices (M>=1): P_fpaa mean {r['mean_P_fpaa']:.3f} (min {r['min_P_fpaa']:.3f}); "
          f"P_grover(k={kG}) mean {r['mean_P_grover']:.3f} (min {r['min_P_grover']:.3f}); "
          f"mean expected evals with restarts: FPAA {r['mean_cost_fpaa']:.1f}, Grover {r['mean_cost_grover']:.1f}")

# Qiskit circuit for FPAA (n=4) using phase-oracle MCPhase and phase-reflection about |s>
from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import Statevector
from qiskit.circuit.library import MCPhaseGate
def fpaa_circuit(n, marked, l, delta):
    a, b = ylc_phases(l, delta)
    qc = QuantumCircuit(n); qc.h(range(n))
    for aj, bj in zip(a, b):
        for m in marked:                       # S_t(b): phase e^{ib} on each marked index
            z = [q for q in range(n) if not (m >> q) & 1]
            if z: qc.x(z)
            qc.append(MCPhaseGate(bj, n - 1), list(range(n)))
            if z: qc.x(z)
        qc.h(range(n)); qc.x(range(n))         # S_s(a) = H^n S_0(a) H^n, S_0(a)=I-(1-e^{-ia})|0><0|
        qc.append(MCPhaseGate(-aj, n - 1), list(range(n)))
        qc.x(range(n)); qc.h(range(n))
        qc.global_phase += math.pi             # the leading minus sign
    return qc
n, N = 4, 16
for M in (1, 3):
    mk = list(range(M)); l = 3
    qc = fpaa_circuit(n, mk, l, 0.5)
    p = float(sum(abs(Statevector(qc).data[i]) ** 2 for i in mk))
    tq = G.to_ionq(qc)
    print(f"[circuit] FPAA n=4 M={M} l={l}: statevector P={p:.6f} vs formula {p_formula(N, M, l, 0.5):.6f}; IonQ-like 2Q={G.twoq(tq)} "
          f"(plain Grover k=3 list oracle M={M}: {G.twoq(G.to_ionq(G.grover_circuit(n, G.list_oracle(n, mk), 3, measure=False)))})")
json.dump(out, open(os.path.join(G.HERE, "results_c07_fixed_point.json"), "w"), indent=1)
