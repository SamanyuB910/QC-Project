"""Prompt C, step 6b: QPE quantum counting with the global phase fixed.
gs_core.diffusion implements I-2|s><s| = -(2|s><s|-I), so G = D*O has eigenphases pi +- 2theta.
Under control this phase is physical; we add global_phase=pi to G so eigenphases are +-2theta and M = N sin^2(pi*y/2^t)."""
import math, json, time, warnings
import numpy as np
warnings.filterwarnings("ignore")
from qiskit import QuantumCircuit
from qiskit.circuit.library import QFTGate
from qiskit_aer import AerSimulator
import gs_core as G
rows = G.load_catalog(); rng = np.random.default_rng(99)
def counting_circuit(n, marked, t):
    Gop = QuantumCircuit(n, name="G"); Gop.compose(G.list_oracle(n, marked), inplace=True); Gop.compose(G.diffusion(n), inplace=True)
    Gop.global_phase += math.pi
    cG = Gop.to_gate().control(1)
    qc = QuantumCircuit(t + n, t); qc.h(range(t + n))
    for j in range(t):
        for _ in range(2**j): qc.append(cG, [j] + list(range(t, t + n)))
    qc.append(QFTGate(t).inverse(), range(t)); qc.measure(range(t), range(t))
    return qc
out = []
for n, t in ((4, 4), (4, 5)):
    N = 2**n
    while True:
        sl = G.slice_events(rows, n, rng); mk = G.marked_indices(sl)
        if len(mk) >= 1: break
    M = len(mk); tq = G.to_ionq(counting_circuit(n, mk, t))
    for label, sim in (("ideal", AerSimulator()), ("noisy_forte1", AerSimulator(method="density_matrix", noise_model=G.ionq_noise_model()))):
        t0 = time.time(); counts = sim.run(tq, shots=4000, seed_simulator=5).result().get_counts()
        est = {}
        for bs, c in counts.items():
            Mh = round(N * math.sin(math.pi * int(bs, 2) / 2**t) ** 2, 2); est[Mh] = est.get(Mh, 0) + c
        top = sorted(est.items(), key=lambda kv: -kv[1])[:4]
        pw = sum(c for v, c in est.items() if abs(v - M) <= 0.5) / 4000
        mean_est = sum(v * c for v, c in est.items()) / 4000
        rec = dict(n=n, t=t, N=N, M=M, mode=label, twoq=G.twoq(tq), qubits=n + t, controlled_G_calls=2**t - 1, top=top, p_within_half=pw, mean_Mhat=mean_est, sec=time.time() - t0)
        out.append(rec)
        print(f"QPE counting n={n} t={t} N={N} true M={M} [{label}]: {n+t} qubits, 2Q={rec['twoq']}, controlled-G calls {2**t-1}; "
              f"top M_hat {top}; P(|M_hat-M|<=0.5)={pw:.3f}; mean M_hat={mean_est:.2f} [{rec['sec']:.0f}s]", flush=True)
json.dump(out, open("results_c06b_qpe_counting.json", "w"), indent=1)
