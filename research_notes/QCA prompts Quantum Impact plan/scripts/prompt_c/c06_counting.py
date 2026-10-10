"""Prompt C, step 6: HOW MANY events match? Quantum counting (QPE on the Grover operator) and
QPE-free maximum-likelihood amplitude estimation (MLAE, Suzuki et al. 2020), on real slices.

Budget accounting: one MLAE shot of circuit Q^m costs m oracle calls + 1 predicate evaluation to label
the shot good/bad (either a classical check of the measured event or an in-circuit flag computation).
Classical baselines at equal budget B: (a) sample B events uniformly with replacement, check each,
M_hat = N*hits/B; (b) exact count needs B=N checks (unbeatable once B>=N).
Noise: global-depolarizing model P_k = F_k*P_ideal + (1-F_k)*M/N with F from IonQ forte-1 rates and
transpiled 2Q counts; noise-aware MLE fits (theta, gamma) with F_k = exp(-gamma*m_k).
"""
import json, os, math, warnings, time
import numpy as np
warnings.filterwarnings("ignore")
from qiskit import QuantumCircuit
from qiskit.circuit.library import QFTGate
from qiskit_aer import AerSimulator
import gs_core as G

rows = G.load_catalog()
rng = np.random.default_rng(99)
TH = np.linspace(1e-4, math.pi / 2 - 1e-4, 4001)

def mle_theta(ms, shots, hits, gamma=None, grid=None):
    TH = grid if grid is not None else globals()["TH"]
    ll = np.zeros_like(TH)
    for m, s, h in zip(ms, shots, hits):
        p = np.sin((2 * m + 1) * TH) ** 2
        if gamma is not None:
            F = math.exp(-gamma * m); p = F * p + (1 - F) * np.sin(TH) ** 2
        p = np.clip(p, 1e-12, 1 - 1e-12)
        ll += h * np.log(p) + (s - h) * np.log(1 - p)
    return TH[np.argmax(ll)], ll

def mle_theta_gamma(ms, shots, hits, gammas=np.linspace(0, 1.0, 21)):
    best = (-np.inf, None, None)
    for g in gammas:
        t, ll = mle_theta(ms, shots, hits, gamma=g)
        if ll.max() > best[0]: best = (ll.max(), t, g)
    return best[1], best[2]

# ---------------------------------------------------------------- 1) MLAE on real slices, small budgets
mcz2q = {n: G.twoq(G.to_ionq(G.list_oracle(n, [2**n - 1]))) for n in range(3, 21) if n <= 10}
def F_noise(n, M, m):
    c = mcz2q.get(n, None)
    if c is None: c = mcz2q[10] * (n / 10) ** 2       # rough extrapolation beyond n=10 (not used for real slices)
    return (1 - 15 / 16 * G.P2) ** (m * (M + 1) * c)

res_real = []
print("MLAE on real slices (schedule m=0,1,2,4; equal shots), RMSE of M_hat over 200 repeats per slice")
for n in (4, 5, 6):
    N = 2**n
    for trial in range(2):
        while True:
            sl = G.slice_events(rows, n, rng); M = len(G.marked_indices(sl))
            if M >= 1: break
        th0 = math.asin(math.sqrt(M / N))
        for shots_each in (2, 4, 16):
            ms = [0, 1, 2, 4]; budget = sum(shots_each * (m + 1) for m in ms)
            est_q, est_qn, est_qn_aw, est_c = [], [], [], []
            for _ in range(200):
                hits = [rng.binomial(shots_each, math.sin((2 * m + 1) * th0) ** 2) for m in ms]
                est_q.append(N * math.sin(mle_theta(ms, [shots_each] * 4, hits)[0]) ** 2)
                pn = [F_noise(n, M, m) * math.sin((2 * m + 1) * th0) ** 2 + (1 - F_noise(n, M, m)) * M / N for m in ms]
                hn = [rng.binomial(shots_each, p) for p in pn]
                est_qn.append(N * math.sin(mle_theta(ms, [shots_each] * 4, hn)[0]) ** 2)
                if shots_each == 16:
                    t, g = mle_theta_gamma(ms, [shots_each] * 4, hn); est_qn_aw.append(N * math.sin(t) ** 2)
                cb = min(budget, 10**9)
                est_c.append(N * rng.binomial(cb, M / N) / cb)
            r = lambda e: float(np.sqrt(np.mean((np.array(e) - M) ** 2))) if e else None
            rec = dict(n=n, N=N, M=M, shots_each=shots_each, budget=budget, rmse_mlae_ideal=r(est_q),
                       rmse_mlae_noisy_naive=r(est_qn), rmse_mlae_noisy_aware=r(est_qn_aw),
                       rmse_classical_sampling=r(est_c), classical_exact_budget=N)
            res_real.append(rec)
            print(f"  n={n} N={N:3d} M={M}: budget {budget:4d} ({'<' if budget<N else '>='} N) | RMSE(M_hat): MLAE ideal {rec['rmse_mlae_ideal']:.2f}, "
                  f"noisy-naive {rec['rmse_mlae_noisy_naive']:.2f}" + (f", noisy-aware {rec['rmse_mlae_noisy_aware']:.2f}" if est_qn_aw else "") +
                  f" | classical sampling {rec['rmse_classical_sampling']:.2f} | exact count costs {N}")

# ---------------------------------------------------------------- 2) asymptotic sweep (ideal): budget for 10% relative error
print("\nBudget (oracle calls + labels) to reach 10% relative RMSE on M, real rate p=M/N (ideal MLAE vs classical sampling)")
sweep = []
for p_rate, lab in ((0.0479, "shallow&M>=6 rate"), (0.0053, "shallow&M>=7 rate")):
    th0 = math.asin(math.sqrt(p_rate))
    for K in range(1, 10):
        ms = [0] + [2**j for j in range(K)]; shots = 32
        est = []
        for _ in range(200):
            hits = [rng.binomial(shots, math.sin((2 * m + 1) * th0) ** 2) for m in ms]
            grid = np.linspace(1e-5, math.pi / 2 - 1e-5, 60 * (2 * ms[-1] + 1) + 1)   # resolve the narrowest likelihood peak
            est.append(math.sin(mle_theta(ms, [shots] * len(ms), hits, grid=grid)[0]) ** 2)
        rel = float(np.sqrt(np.mean((np.array(est) / p_rate - 1) ** 2)))
        budget = sum(shots * (m + 1) for m in ms)
        cl_budget = (1 - p_rate) / (p_rate * rel**2)   # classical sampling budget for the same relative RMSE
        sweep.append(dict(rate=p_rate, label=lab, max_m=ms[-1], budget_mlae=budget, rel_rmse=rel, classical_budget_same_rmse=cl_budget))
        print(f"  {lab:20s} max m={ms[-1]:4d}: MLAE budget {budget:6d} -> rel RMSE {rel:.3f}; classical sampling needs {cl_budget:9.0f} for same RMSE")

# ---------------------------------------------------------------- 3) QPE quantum counting circuit (n=4, t=4), ideal + noisy DM
def counting_circuit(n, marked, t):
    O = G.list_oracle(n, marked); D = G.diffusion(n)
    Gop = QuantumCircuit(n, name="G"); Gop.compose(O, inplace=True); Gop.compose(D, inplace=True)
    Gop.global_phase += math.pi   # FIX (see c06b): D = I-2|s><s| makes G = -G_std; without this, M_hat decodes as N-M
    cG = Gop.to_gate().control(1)
    qc = QuantumCircuit(t + n, t)
    qc.h(range(t + n))
    for j in range(t):
        for _ in range(2**j):
            qc.append(cG, [j] + list(range(t, t + n)))
    qc.append(QFTGate(t).inverse(), range(t))
    qc.measure(range(t), range(t))
    return qc

qpe = []
for n, t in ((4, 4), (4, 5)):
    N = 2**n
    while True:
        sl = G.slice_events(rows, n, rng); mk = G.marked_indices(sl)
        if len(mk) >= 1: break
    M = len(mk)
    qc = counting_circuit(n, mk, t)
    tq = G.to_ionq(qc)
    for label, sim in (("ideal", AerSimulator()), ("noisy_forte1", AerSimulator(method="density_matrix", noise_model=G.ionq_noise_model()))):
        t0 = time.time()
        counts = sim.run(tq, shots=4000, seed_simulator=5).result().get_counts()
        ests = {}
        for bs, c in counts.items():
            y = int(bs, 2); phi = y / 2**t
            Mh = N * math.sin(math.pi * phi) ** 2      # eigenphase +-2theta -> M = N sin^2(pi*y/2^t)
            ests[round(Mh, 2)] = ests.get(round(Mh, 2), 0) + c
        top = sorted(ests.items(), key=lambda kv: -kv[1])[:4]
        mode = top[0][0]
        p_within_half = sum(c for v, c in ests.items() if abs(v - M) <= 0.5) / 4000
        rec = dict(n=n, t=t, N=N, M=M, mode=label, twoq=G.twoq(tq), twoq_depth=G.twoq_depth(tq), qubits=t + n,
                   oracle_calls=2**t - 1, top_estimates=top, p_estimate_within_half=p_within_half, sec=time.time() - t0)
        qpe.append(rec)
        print(f"QPE counting n={n} t={t} N={N} true M={M} [{label}]: 2Q={rec['twoq']} (depth {rec['twoq_depth']}), "
              f"controlled-G calls {2**t-1}; top M_hat {top}; P(|M_hat-M|<=0.5)={p_within_half:.3f}")

json.dump(dict(mlae_real=res_real, mlae_sweep=sweep, qpe_counting=qpe), open(os.path.join(G.HERE, "results_c06_counting.json"), "w"), indent=1)
