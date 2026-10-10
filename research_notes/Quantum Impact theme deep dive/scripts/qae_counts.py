"""2Q-gate counts for qiskit-finance amplitude-estimation circuits (European call, credit-risk expected loss).
Counts CX after transpiling to {rz, sx, x, cx} at optimization_level=3, no coupling map (all-to-all, like IonQ Forte).
On IonQ, one CX ~ one native ZZ/MS entangler, so CX count ~ native 2Q count.
"""
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import WeightedAdder, LinearAmplitudeFunction
from qiskit_finance.circuit.library import LogNormalDistribution, GaussianConditionalIndependenceModel as GCI
from qiskit_finance.applications.estimation import EuropeanCallPricing
from qiskit_algorithms import MaximumLikelihoodAmplitudeEstimation, EstimationProblem
from qiskit.primitives import StatevectorSampler

BASIS = ["rz", "sx", "x", "cx"]

def cx(qc):
    t = transpile(qc, basis_gates=BASIS, optimization_level=3, seed_transpiler=1)
    return t.count_ops().get("cx", 0), t.num_qubits, t.depth()

def grover_power_circuit(A, Q, k, obj):
    qc = QuantumCircuit(A.num_qubits, 1)
    qc.compose(A, inplace=True)
    for _ in range(k):
        qc.compose(Q, inplace=True)
    return qc

def european(n):
    S, vol, r, T = 2.0, 0.4, 0.05, 40/365
    mu = (r - 0.5*vol**2)*T + np.log(S); sigma = vol*np.sqrt(T)
    mean = np.exp(mu + sigma**2/2); var = (np.exp(sigma**2)-1)*np.exp(2*mu+sigma**2); std = np.sqrt(var)
    low, high = max(0, mean-3*std), mean+3*std
    unc = LogNormalDistribution(n, mu=mu, sigma=sigma**2, bounds=(low, high))
    ecp = EuropeanCallPricing(num_state_qubits=n, strike_price=1.896, rescaling_factor=0.25, bounds=(low, high), uncertainty_model=unc)
    prob = ecp.to_estimation_problem()
    return ecp, prob, unc

print("=== European call (LogNormal on n uncertainty qubits + 1 objective qubit + comparator ancillas) ===")
for n in [2, 3, 4]:
    ecp, prob, unc = european(n)
    A, Q = prob.state_preparation, prob.grover_operator
    a_cx, a_q, a_d = cx(A)
    u_cx, _, _ = cx(unc)
    q_cx, q_q, q_d = cx(Q)
    ks = [1, 2, 4]
    tot = {k: cx(grover_power_circuit(A, Q, k, prob.objective_qubits))[0] for k in ks}
    print(f"n={n}: qubits={a_q}  loader CX={u_cx}  A CX={a_cx} (depth {a_d})  Q CX={q_cx}  Q^k A CX: " + ", ".join(f"k={k}:{v}" for k, v in tot.items()))

print("\n=== Credit risk expected loss (GCI model n_z=2, K assets, WeightedAdder + LinearAmplitudeFunction) ===")
def credit(K):
    n_z, z_max = 2, 2
    p_zeros = list(np.linspace(0.15, 0.25, K)); rhos = list(np.linspace(0.1, 0.05, K)); lgd = [1, 2, 1, 2, 1, 2][:K]
    u = GCI(n_z, z_max, p_zeros, rhos)
    agg = WeightedAdder(n_z + K, [0]*n_z + lgd)
    obj = LinearAmplitudeFunction(agg.num_sum_qubits, slope=[1], offset=[0], domain=(0, 2**agg.num_sum_qubits - 1), image=(0, sum(lgd)), rescaling_factor=0.25, breakpoints=[0])
    qr_state = u.num_qubits; nq = agg.num_qubits + 1
    sp = QuantumCircuit(max(u.num_qubits, agg.num_qubits) + 1)
    sp.append(u.to_gate(), range(u.num_qubits))
    sp.append(agg.to_gate(), range(agg.num_qubits))
    sp.append(obj.to_gate(), list(range(n_z+K, n_z+K+agg.num_sum_qubits)) + [agg.num_qubits])
    sp.append(agg.to_gate().inverse(), range(agg.num_qubits))
    return u, sp
for K in [2, 3, 4]:
    u, sp = credit(K)
    print(f"K={K}: qubits={sp.num_qubits}  GCI CX={cx(u)[0]}  A(expected loss) CX={cx(sp)[0]}")

print("\n=== Ideal MLAE vs exact, European call n=3 (statevector sampler) ===")
ecp, prob, unc = european(3)
# exact value
from qiskit.quantum_info import Statevector
sv = Statevector(prob.state_preparation)
p_exact = sum(pr for idx, pr in enumerate(sv.probabilities()) if (idx >> prob.objective_qubits[0]) & 1)
print("exact amplitude a =", round(p_exact, 6), " -> price", round(ecp.interpret(type("R", (), {"estimation_processed": prob.post_processing(p_exact)})()) if False else prob.post_processing(p_exact), 6))
for shots in [100, 1000]:
    mlae = MaximumLikelihoodAmplitudeEstimation(evaluation_schedule=[0, 1, 2, 4], sampler=StatevectorSampler(default_shots=shots, seed=7))
    res = mlae.estimate(prob)
    oracle_calls = res.num_oracle_queries
    print(f"shots/circuit={shots}: a_est={res.estimation:.6f} |err|={abs(res.estimation-p_exact):.2e} oracle_queries={oracle_calls}  MC std err at same #samples ~ {np.sqrt(p_exact*(1-p_exact)/oracle_calls):.2e}")
