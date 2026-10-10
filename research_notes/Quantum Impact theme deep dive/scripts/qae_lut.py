"""Hand-built 'lookup-table' amplitude-estimation oracle: A = StatePreparation(sqrt p) on n qubits + uniformly-controlled RY on 1 objective qubit.
Compare 2Q counts with qiskit-finance's comparator/piecewise-linear construction. Then noisy MLAE with a simple depolarizing model.
"""
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import StatePreparation, UCRYGate, grover_operator
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error

BASIS = ["rz", "sx", "x", "cx"]
def tcx(qc):
    t = transpile(qc, basis_gates=BASIS, optimization_level=3, seed_transpiler=1)
    return t.count_ops().get("cx", 0), t

def build(n, S=2.0, vol=0.4, r=0.05, T=40/365, K=1.896):
    mu = (r - 0.5*vol**2)*T + np.log(S); sig = vol*np.sqrt(T)
    mean = np.exp(mu + sig**2/2); std = np.sqrt((np.exp(sig**2)-1)*np.exp(2*mu+sig**2))
    xs = np.linspace(max(0, mean-3*std), mean+3*std, 2**n)
    pdf = np.exp(-(np.log(xs)-mu)**2/(2*sig**2))/(xs*sig*np.sqrt(2*np.pi)); p = pdf/pdf.sum()
    f = np.maximum(xs-K, 0); fmax = f.max(); fn = f/fmax
    A = QuantumCircuit(n+1)
    A.append(StatePreparation(np.sqrt(p)), range(n))
    A.append(UCRYGate(list(2*np.arcsin(np.sqrt(fn)))), [n] + list(range(n)))
    oracle = QuantumCircuit(n+1); oracle.z(n)
    Q = grover_operator(oracle, state_preparation=A)
    a_true = float(np.dot(p, fn))
    return A, Q, a_true, fmax

print("=== Lookup-table oracle: CX counts (all-to-all) ===")
for n in [2, 3, 4]:
    A, Q, a, fmax = build(n)
    row = []
    for k in [0, 1, 2, 3, 4]:
        qc = QuantumCircuit(n+1); qc.compose(A, inplace=True)
        for _ in range(k): qc.compose(Q, inplace=True)
        row.append(f"k={k}:{tcx(qc)[0]}")
    print(f"n={n} (qubits {n+1}): A CX={tcx(A)[0]}  Q CX={tcx(Q)[0]}  Q^k A: " + ", ".join(row))

def mlae_fit(ms, hits, shots, decay=None):
    thetas = np.linspace(1e-4, np.pi/2-1e-4, 20001)
    ll = np.zeros_like(thetas)
    for m, h in zip(ms, hits):
        p = np.sin((2*m+1)*thetas)**2
        if decay is not None:  # depolarizing-aware likelihood: p -> e^{-g(2m+1)} p + (1-e^{-g(2m+1)})/2
            lam = np.exp(-decay*(2*m+1)); p = lam*p + (1-lam)/2
        p = np.clip(p, 1e-12, 1-1e-12)
        ll += h*np.log(p) + (shots-h)*np.log(1-p)
    return np.sin(thetas[np.argmax(ll)])**2

print("\n=== MLAE n=2 lookup-table oracle, schedule m=[0,1,2], 2Q depolarizing p2 per CX, 1Q p1=p2/10 ===")
n = 2; A, Q, a_true, fmax = build(n); ms = [0, 1, 2]; shots = 1000
circs = []
for m in ms:
    qc = QuantumCircuit(n+1, 1); qc.compose(A, inplace=True)
    for _ in range(m): qc.compose(Q, inplace=True)
    qc.measure(n, 0); circs.append(transpile(qc, basis_gates=BASIS, optimization_level=3, seed_transpiler=1))
print("true a =", round(a_true, 5), " CX per circuit:", [c.count_ops().get('cx', 0) for c in circs])
rng = np.random.default_rng(0)
for p2 in [0.0, 0.005, 0.01, 0.02]:
    nm = NoiseModel()
    if p2 > 0:
        nm.add_all_qubit_quantum_error(depolarizing_error(p2, 2), ["cx"])
        nm.add_all_qubit_quantum_error(depolarizing_error(p2/10, 1), ["sx", "x"])
    sim = AerSimulator(noise_model=nm if p2 > 0 else None, seed_simulator=11)
    errs_naive, errs_aware, errs_mc = [], [], []
    for rep in range(20):
        res = sim.run(circs, shots=shots, seed_simulator=int(rng.integers(1e9))).result()
        hits = [res.get_counts(i).get('1', 0) for i in range(len(ms))]
        errs_naive.append(abs(mlae_fit(ms, hits, shots) - a_true))
        # crude decay calibration: fit decay jointly by grid (stand-in for Tanaka et al. noise-aware MLAE)
        best = None
        for g in np.linspace(0, 0.3, 61):
            est = mlae_fit(ms, hits, shots, decay=g)
            th = np.arcsin(np.sqrt(est)); lam = np.exp(-g*(2*np.array(ms)+1))
            pp = np.clip(lam*np.sin((2*np.array(ms)+1)*th)**2 + (1-lam)/2, 1e-12, 1-1e-12)
            ll = np.sum(np.array(hits)*np.log(pp) + (shots-np.array(hits))*np.log(1-pp))
            if best is None or ll > best[0]: best = (ll, est)
        errs_aware.append(abs(best[1] - a_true))
        n_eq = shots*sum(2*m+1 for m in ms)  # oracle-call-equivalent classical samples
        errs_mc.append(abs(rng.binomial(n_eq, a_true)/n_eq - a_true))
    print(f"p2={p2:.3f}: MLAE naive RMSE={np.sqrt(np.mean(np.square(errs_naive))):.4f}  noise-aware RMSE={np.sqrt(np.mean(np.square(errs_aware))):.4f}  classical MC RMSE @ {shots*sum(2*m+1 for m in ms)} samples={np.sqrt(np.mean(np.square(errs_mc))):.4f}")
