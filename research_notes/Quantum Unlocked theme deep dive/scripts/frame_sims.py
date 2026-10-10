"""Pure-numpy Pauli-frame simulator (Stim-style error propagation) for QEC teaching demos.
Only numpy + networkx -> both ship with Pyodide. Noise: depolarizing p2 after each CX (15 Paulis),
p1 = p2/10 after each 1q gate, symmetric measurement flip pm = p2 (unless set).
Detectors/observables are parities of measurement *flips* relative to the noiseless circuit,
which is valid whenever the noiseless parity is deterministic (true for all detectors here).
"""
import sys, time, itertools
import numpy as np
import networkx as nx
from collections import defaultdict

class Frame:
    def __init__(self, n, S, p2, p1=None, pm=None, seed=0):
        self.S, self.n = S, n
        self.x = np.zeros((S, n), dtype=bool); self.z = np.zeros((S, n), dtype=bool)
        self.p2 = p2; self.p1 = p2/10 if p1 is None else p1; self.pm = p2 if pm is None else pm
        self.rng = np.random.default_rng(seed); self.meas = []
    def _n1(self, q):
        if self.p1 <= 0: return
        m = self.rng.random(self.S) < self.p1; r = self.rng.integers(1, 4, self.S)
        self.x[:, q] ^= m & (r & 1).astype(bool); self.z[:, q] ^= m & ((r >> 1) & 1).astype(bool)
    def _n2(self, a, b):
        if self.p2 <= 0: return
        m = self.rng.random(self.S) < self.p2; r = self.rng.integers(1, 16, self.S)
        self.x[:, a] ^= m & (r & 1).astype(bool); self.z[:, a] ^= m & ((r >> 1) & 1).astype(bool)
        self.x[:, b] ^= m & ((r >> 2) & 1).astype(bool); self.z[:, b] ^= m & ((r >> 3) & 1).astype(bool)
    def h(self, q):
        self.x[:, q], self.z[:, q] = self.z[:, q].copy(), self.x[:, q].copy(); self._n1(q)
    def xgate(self, q): self._n1(q)          # Paulis commute through the frame up to sign
    def cx(self, c, t):
        self.x[:, t] ^= self.x[:, c]; self.z[:, c] ^= self.z[:, t]; self._n2(c, t)
    def inject_x(self, q, prob):
        self.x[:, q] ^= self.rng.random(self.S) < prob
    def m(self, q):
        f = self.x[:, q] ^ (self.rng.random(self.S) < self.pm); self.meas.append(f); return f
    def mx(self, q):
        self.h(q); return self.m(q)
    def bits(self): return np.stack(self.meas, axis=1).astype(np.uint8)

# ---------------------------------------------------------------- D1: 3-qubit bit-flip code (Clifford parts)
def d1(p2=0.005, qs=(0.0, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2), S=2_000_000):
    print("\n=== D1: 3-qubit bit-flip code, inject X w.p. q per data qubit, p2=%.3f ===" % p2)
    for q in qs:
        f = Frame(1, S, p2, seed=1); f.xgate(0); f.inject_x(0, q); f.m(0); bare = f.bits()[:, 0].mean()
        f = Frame(5, S, p2, seed=2)
        f.xgate(0); f.cx(0, 1); f.cx(0, 2)
        for k in range(3): f.inject_x(k, q)
        f.cx(0, 3); f.cx(1, 3); f.cx(1, 4); f.cx(2, 4)
        for k in range(5): f.m(k)
        b = f.bits(); data = b[:, :3]; s = b[:, 3:]
        maj = (data.sum(1) >= 2).mean()
        flip0 = (s[:, 0] == 1) & (s[:, 1] == 0)
        syn = ((data[:, 0] ^ flip0) == 1).mean()
        print(f"q={q:.3f} bare={bare:.5f} | encoded+majority(data)={maj:.5f} | encoded+ancilla-syndrome-lookup(q0)={syn:.5f} | code-capacity theory 3q^2-2q^3={3*q*q-2*q**3:.5f}")

def d1_coherent(p2=0.005, qs=(0.0, 0.01, 0.05, 0.1, 0.2)):
    """Exact density-matrix calc of measurement-free (Toffoli) correction, using qiskit-aer if available."""
    try:
        from qiskit import QuantumCircuit
        from qiskit_aer import AerSimulator
        from qiskit_aer.noise import NoiseModel, depolarizing_error, pauli_error
    except Exception as e:
        print("skip coherent:", e); return
    p1 = p2/10; pm = p2
    nm = NoiseModel()
    nm.add_all_qubit_quantum_error(depolarizing_error(p2, 2), ['cx'])
    nm.add_all_qubit_quantum_error(depolarizing_error(p1, 1), ['h', 't', 'tdg', 'x'])
    sim = AerSimulator(method='density_matrix', noise_model=nm)
    print("\n=== D1c: coherent (measurement-free) correction via Toffoli majority, exact density matrix ===")
    dec = QuantumCircuit(3); dec.cx(0, 1); dec.cx(0, 2); dec.ccx(1, 2, 0)
    dec = dec.decompose(gates_to_decompose=['ccx'])
    ncx = sum(1 for i in dec.data if i.operation.name == 'cx')
    for q in qs:
        qc = QuantumCircuit(3)
        qc.x(0); qc.cx(0, 1); qc.cx(0, 2)
        if q > 0:
            for k in range(3): qc.append(pauli_error([('X', q), ('I', 1-q)]), [k])
        qc.compose(dec, inplace=True)
        qc.save_probabilities([0])
        pr = sim.run(qc, shots=1).result().data()['probabilities']
        p_wrong = pr[0]  # q0 should be |1>
        p_wrong = p_wrong*(1-pm) + (1-p_wrong)*pm
        print(f"q={q:.3f} coherent-correction error={p_wrong:.5f}  (decoder uses {ncx} CX incl. Toffoli)")

# ---------------------------------------------------------------- D2: [[4,2,2]] logical Bell vs bare Bell
def d2(p2s=(0.001, 0.003, 0.005, 0.01, 0.02), S=4_000_000):
    print("\n=== D2: [[4,2,2]] logical Bell = Bell(0,3) x Bell(1,2) vs bare Bell; no mid-circuit meas ===")
    for p2 in p2s:
        res = {}
        for basis in 'ZX':
            f = Frame(2, S, p2, seed=3); f.h(0); f.cx(0, 1)
            (f.mx if basis == 'X' else f.m)(0); (f.mx if basis == 'X' else f.m)(1)
            b = f.bits(); res[('b', basis)] = (b[:, 0] ^ b[:, 1]).mean()
            f = Frame(4, S, p2, seed=4); f.h(0); f.cx(0, 3); f.h(1); f.cx(1, 2)
            for k in range(4): (f.mx if basis == 'X' else f.m)(k)
            b = f.bits(); acc = b.sum(1) % 2 == 0; lg = b[:, 1] ^ b[:, 2]
            res[('e', basis)] = (lg[acc].mean(), acc.mean(), lg.mean())
        bare = (res[('b', 'Z')] + res[('b', 'X')])/2
        e = [(res[('e', 'Z')][i] + res[('e', 'X')][i])/2 for i in range(3)]
        print(f"p2={p2:.3f}: bare Bell parity err={bare:.5f} | encoded post-selected={e[0]:.6f} (accept {e[1]:.4f}) | encoded w/o post-selection={e[2]:.5f} | ratio bare/encPS={bare/max(e[0],1e-9):.1f}x")

def d2b(p2=0.005, S=4_000_000):
    print("\n=== D2b: [[4,2,2]] |00>_L: non-FT GHZ encoder vs flag-qubit encoder (Z-basis readout) ===")
    f = Frame(4, S, p2, seed=5); f.h(0); f.cx(0, 1); f.cx(0, 2); f.cx(0, 3)
    for k in range(4): f.m(k)
    b = f.bits(); acc = b.sum(1) % 2 == 0; lg = ((b[:, 0] ^ b[:, 1]) | (b[:, 0] ^ b[:, 2])).astype(bool)
    print(f"non-FT: accept={acc.mean():.4f} post-selected logical err={lg[acc].mean():.6f}")
    f = Frame(5, S, p2, seed=6); f.h(0); f.cx(0, 1); f.cx(0, 2); f.cx(0, 3); f.cx(1, 4); f.cx(3, 4)
    for k in range(5): f.m(k)
    b = f.bits(); acc = (b[:, :4].sum(1) % 2 == 0) & (b[:, 4] == 0)
    lg = ((b[:, 0] ^ b[:, 1]) | (b[:, 0] ^ b[:, 2])).astype(bool)
    print(f"flagged (ancilla q4 checks Z1Z3): accept={acc.mean():.4f} post-selected logical err={lg[acc].mean():.6f}")
    f = Frame(2, S, p2, seed=7); f.m(0); f.m(1); b = f.bits()
    print(f"bare |00> (prep+measure only): err={(b.sum(1) > 0).mean():.5f}")

# ---------------------------------------------------------------- D3: repetition code memory, unrolled ancillas
def rep_sample(d, R, p2, S, seed):
    n = d + R*(d-1); f = Frame(n, S, p2, seed=seed)
    for r in range(R):
        for i in range(d-1):
            a = d + r*(d-1) + i; f.cx(i, a); f.cx(i+1, a)
    for k in range(n): f.m(k)
    bits = f.bits()
    m = np.stack([bits[:, d + r*(d-1): d + (r+1)*(d-1)] for r in range(R)], axis=1)
    data = bits[:, :d]; fin = data[:, :-1] ^ data[:, 1:]
    L = np.concatenate([m, fin[:, None, :]], axis=1); det = L.copy(); det[:, 1:] ^= L[:, :-1]
    return det.reshape(S, -1), data[:, 0], data

def rep_graph(d, R):
    G = nx.Graph(); node = lambda r, i: r*(d-1) + i
    for r in range(R+1):
        for i in range(d-2): G.add_edge(node(r, i), node(r, i+1), weight=1.0, obs=0)
        G.add_edge(node(r, 0), 'B', weight=1.0, obs=1)
        G.add_edge(node(r, d-2), 'BR', weight=1.0, obs=0)
        if r < R:
            for i in range(d-1): G.add_edge(node(r, i), node(r+1, i), weight=1.0, obs=0)
            # diagonal edge from an error on data qubit i+1 between the two CXs of round r (hook-like)
    G.add_edge('B', 'BR', weight=0.0, obs=0)
    return G

def make_mwpm(G):
    D, P = {}, {}
    for src, (dd, pp) in nx.all_pairs_dijkstra(G, weight='weight'):
        for tgt, path in pp.items():
            par = 0
            for u, v in zip(path[:-1], path[1:]): par ^= G[u][v]['obs']
            D[(src, tgt)] = dd[tgt]; P[(src, tgt)] = par
    cache = {}
    def decode(row):
        k = row.tobytes()
        if k in cache: return cache[k]
        dfs = [int(i) for i in np.flatnonzero(row)]
        if not dfs: cache[k] = 0; return 0
        M = nx.Graph(); BIG = 1e4
        for a, b in itertools.combinations(dfs, 2):
            M.add_edge(('d', a), ('d', b), weight=BIG - D[(a, b)], obs=P[(a, b)])
            M.add_edge(('b', a), ('b', b), weight=BIG, obs=0)
        for a in dfs: M.add_edge(('d', a), ('b', a), weight=BIG - D[(a, 'B')], obs=P[(a, 'B')])
        par = 0
        for u, v in nx.max_weight_matching(M, maxcardinality=True): par ^= M[u][v]['obs']
        cache[k] = par; return par
    return decode

def d3(ds=(3, 5, 7), R=3, p2s=(0.001, 0.003, 0.005, 0.01, 0.02, 0.04, 0.08), S=100_000):
    print(f"\n=== D3: repetition code (bit-flip), R={R} rounds, fresh ancilla per check (no reuse), MWPM(networkx) ===")
    for d in ds:
        n = d + R*(d-1); ncx = 2*R*(d-1)
        dec = make_mwpm(rep_graph(d, R))
        print(f"d={d}: qubits={n}, CX={ncx}, detectors={(R+1)*(d-1)}")
        for p2 in p2s:
            det, obs, data = rep_sample(d, R, p2, S, seed=int(p2*1e5)+d)
            t = time.time()
            pred = np.fromiter((dec(det[s]) for s in range(S)), dtype=np.uint8, count=S)
            ler = (pred != obs).mean(); maj = (data.sum(1) > d//2).mean()
            print(f"   p2={p2:.3f}  MWPM LER={ler:.5f}  final-majority-only={maj:.5f}  bare q0 flip={obs.mean():.5f}  [{time.time()-t:.1f}s]")

# ---------------------------------------------------------------- D4: d=3 rotated surface code Z-memory
XST = [[0, 1, 3, 4], [4, 5, 7, 8], [1, 2], [6, 7]]
ZST = [[1, 4, 2, 5], [3, 6, 4, 7], [0, 3], [5, 8]]

def surf_sample(R, p2, S, seed, xchecks=True):
    nanc = 8 if xchecks else 4; n = 9 + R*nanc
    f = Frame(n, S, p2, seed=seed); a = 9; zanc = []
    for r in range(R):
        if xchecks:
            for st in XST:
                f.h(a)
                for q in st: f.cx(a, q)
                f.h(a); a += 1
        zr = []
        for st in ZST:
            for q in st: f.cx(q, a)
            zr.append(a); a += 1
        zanc.append(zr)
    for k in range(n): f.m(k)
    bits = f.bits()
    L = [bits[:, zanc[r]] for r in range(R)]
    data = bits[:, :9]
    L.append(np.stack([np.bitwise_xor.reduce(data[:, st], axis=1) for st in ZST], axis=1))
    L = np.stack(L, axis=1); det = L.copy(); det[:, 1:] ^= L[:, :-1]
    obs = data[:, 0] ^ data[:, 1] ^ data[:, 2]
    ncx = R*(24 if xchecks else 12)
    return det.reshape(S, -1), obs, n, ncx

def ml_lookup(dtr, otr, dte, ote):
    c = defaultdict(lambda: [0, 0])
    for k, o in zip(map(bytes, dtr), otr): c[k][o] += 1
    tab = {k: int(v[1] > v[0]) for k, v in c.items()}
    pred = np.fromiter((tab.get(bytes(r), 0) for r in dte), dtype=np.uint8, count=len(dte))
    return (pred != ote).mean()

def d4(Rs=(1, 2, 3), p2s=(0.001, 0.002, 0.003, 0.005, 0.01, 0.02), S=1_000_000):
    print("\n=== D4: d=3 rotated surface code, Z-memory, fresh ancillas per round, ML-lookup decoder (train/test split) ===")
    for R in Rs:
        for p2 in p2s:
            det, obs, n, ncx = surf_sample(R, p2, S, seed=int(p2*1e5)+R)
            h = S//2
            ler = ml_lookup(det[:h], obs[:h], det[h:], obs[h:])
            fin = np.bitwise_xor.reduce(det.reshape(S, R+1, 4), axis=1)
            ler_fin = ml_lookup(fin[:h], obs[:h], fin[h:], obs[h:])
            acc = det.sum(1) == 0
            print(f"R={R} qubits={n} CX={ncx} p2={p2:.3f}: ML LER={ler:.5f} | final-data-only LER={ler_fin:.5f} | undecoded={obs.mean():.5f} | post-select-all-trivial: accept={acc.mean():.4f}, err={obs[acc].mean():.6f}")

if __name__ == '__main__':
    t0 = time.time()
    for w in (sys.argv[1:] or ['d1', 'd1_coherent', 'd2', 'd2b', 'd3', 'd4']):
        globals()[w](); print(f"[t={time.time()-t0:.0f}s]", flush=True)
