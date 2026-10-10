"""Cross-check penalty_vs_xy.py simulators against real Qiskit circuits (Statevector):
  - penalty QAOA built from RZ/RZZ (Ising expansion of the QUBO + penalty) and RX mixer
  - XY QAOA built from RZ/RZZ cost and XXPlusYYGate mixer (round-robin pairs), Dicke start
Prints total variation distance between the numpy simulator and Qiskit."""
import itertools, numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import XXPlusYYGate, StatePreparation
from qiskit.quantum_info import Statevector
src = open('penalty_vs_xy.py').read().split("if __name__ == '__main__':")[0]
exec(src)

def ising_terms(E_qubo_lin, E_qubo_quad):
    """E = sum h_i x_i + sum_{i<j} J_ij x_i x_j  ->  a_i Z_i + b_ij Z_i Z_j (+ const)."""
    a = np.zeros(n); b = {}
    for i in range(n): a[i] += -E_qubo_lin[i] / 2
    for (i, j), Jij in E_qubo_quad.items():
        a[i] += -Jij / 4; a[j] += -Jij / 4; b[(i, j)] = Jij / 4
    return a, b

def cost_layer(qc, a, b, gamma):
    for i in range(n): qc.rz(2 * gamma * a[i], i)
    for (i, j), bij in b.items(): qc.rzz(2 * gamma * bij, i, j)

r = relevance(3, [0]); lam = 0.2
f = qubo_f(r, lam)
# QUBO coefficients of f
lin = -r.copy(); quad = {(i, j): lam * C[i, j] for i, j in itertools.combinations(range(n), 2)}
# penalty P (sum x - K)^2 = P[(1-2K) sum x + 2 sum_{i<j} x_i x_j + K^2]
P = 0.05
linP = lin + P * (1 - 2 * K); quadP = {k: v + 2 * P for k, v in quad.items()}
gamma, beta = 3.0, 0.4

# --- penalty circuit ---
aP, bP = ising_terms(linP, quadP)
qc = QuantumCircuit(n); qc.h(range(n)); cost_layer(qc, aP, bP, gamma); qc.rx(2 * beta, range(n))
p_qiskit = Statevector(qc).probabilities()
E = f + P * (hw - K)**2
p_mine = run_x(E, [gamma], [beta])
print('penalty QAOA  TVD(numpy, qiskit) =', 0.5 * np.abs(p_qiskit - p_mine).sum())

# --- XY circuit ---
a, b = ising_terms(lin, quad)
amp = np.zeros(N, complex); amp[feas] = 1 / np.sqrt(feas.sum())
qc = QuantumCircuit(n); qc.append(StatePreparation(amp), range(n))
cost_layer(qc, a, b, gamma)
for (i, j) in PAIRS: qc.append(XXPlusYYGate(2 * beta), [i, j])   # exp(-i beta/2 (XX+YY)) = cos b I - i sin b swap on |01>,|10>
p_q = Statevector(qc).probabilities()
p_mine_xy = np.zeros(N); p_mine_xy[feas] = run_xy(f[feas], [gamma], [beta])
print('XY QAOA       TVD(numpy, qiskit) =', 0.5 * np.abs(p_q - p_mine_xy).sum(), '| weight-5 mass in qiskit =', p_q[feas].sum())
