"""Quick noisy-simulation estimates for QEC teaching demos (no feed-forward, no mid-circuit reuse).
Noise: depolarizing p2 on CX, p1 = p2/10 on 1q gates, symmetric readout error pm.
"""
import sys, time, itertools
import numpy as np
import networkx as nx
from collections import Counter, defaultdict
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error, ReadoutError, pauli_error

def noise_model(p2, p1=None, pm=None):
    p1 = p2/10 if p1 is None else p1
    pm = p2 if pm is None else pm
    nm = NoiseModel()
    if p2 > 0:
        nm.add_all_qubit_quantum_error(depolarizing_error(p2, 2), ['cx'])
    if p1 > 0:
        nm.add_all_qubit_quantum_error(depolarizing_error(p1, 1), ['h', 'x', 's', 'sdg', 'sx', 'rz', 'u', 'u1', 'u2', 'u3'])
    if pm > 0:
        nm.add_all_qubit_readout_error(ReadoutError([[1-pm, pm], [pm, 1-pm]]))
    return nm

def run(qc, nm, shots, method='stabilizer', seed=1):
    sim = AerSimulator(method=method, noise_model=nm, seed_simulator=seed)
    tqc = qc
    res = sim.run(tqc, shots=shots, memory=True).result()
    mem = res.get_memory()
    # convert to array of bits: memory strings are little-endian (clbit 0 is rightmost)
    arr = np.array([[int(ch) for ch in s.replace(' ', '')[::-1]] for s in mem], dtype=np.uint8)
    return arr

# ---------------------------------------------------------------- D1: 3-qubit bit-flip code
def d1(p2=0.005, qs=(0.0, 0.01, 0.05, 0.1, 0.2), shots=200000):
    print("\n=== D1: 3-qubit bit-flip code (encode |1>, inject X w.p. q per data qubit) ===")
    nm = noise_model(p2)
    for q in qs:
        inj = pauli_error([('X', q), ('I', 1-q)]) if q > 0 else None
        # (a) bare qubit
        qa = QuantumCircuit(1, 1); qa.x(0)
        if inj: qa.append(inj, [0])
        qa.measure(0, 0)
        a = run(qa, nm, shots, method='density_matrix')
        err_bare = np.mean(a[:, 0] != 1)
        # (b) encode, inject, measure syndrome with 2 ancillas, measure data, decode classically
        qb = QuantumCircuit(5, 5)
        qb.x(0); qb.cx(0, 1); qb.cx(0, 2)
        if inj:
            for k in range(3): qb.append(inj, [k])
        qb.cx(0, 3); qb.cx(1, 3); qb.cx(1, 4); qb.cx(2, 4)
        qb.measure(range(5), range(5))
        b = run(qb, nm, shots, method='density_matrix')
        data = b[:, :3]; s = b[:, 3:5]
        maj = (data.sum(1) >= 2).astype(int)
        err_maj = np.mean(maj != 1)
        # syndrome-only correction of data qubit 0 then read q0
        flip0 = (s[:, 0] == 1) & (s[:, 1] == 0)
        err_syn = np.mean((data[:, 0] ^ flip0) != 1)
        # (c) coherent (measurement-free) correction: decode circuit + Toffoli majority, read q0 only
        qc = QuantumCircuit(3, 1)
        qc.x(0); qc.cx(0, 1); qc.cx(0, 2)
        if inj:
            for k in range(3): qc.append(inj, [k])
        qc.cx(0, 1); qc.cx(0, 2); qc.ccx(1, 2, 0)
        qc.measure(0, 0)
        c = run(qc, nm, shots, method='density_matrix')
        err_coh = np.mean(c[:, 0] != 1)
        print(f"q={q:.3f}  bare={err_bare:.4f}  majority-vote(data)={err_maj:.4f}  syndrome-lookup(q0)={err_syn:.4f}  coherent-Toffoli={err_coh:.4f}  theory_codecap={3*q**2-2*q**3:.4f}")

# ---------------------------------------------------------------- D2: [[4,2,2]] logical Bell vs bare Bell
def d2(p2s=(0.001, 0.003, 0.005, 0.01), shots=400000):
    print("\n=== D2: [[4,2,2]] logical Bell state (two physical Bell pairs (0,3),(1,2)) vs bare Bell ===")
    for p2 in p2s:
        nm = noise_model(p2)
        out = {}
        for basis in ('Z', 'X'):
            # bare
            qa = QuantumCircuit(2, 2); qa.h(0); qa.cx(0, 1)
            if basis == 'X': qa.h([0, 1])
            qa.measure([0, 1], [0, 1])
            a = run(qa, nm, shots)
            out[('bare', basis)] = np.mean(a[:, 0] ^ a[:, 1])
            # encoded, FT-ish: Bell(0,3) x Bell(1,2)
            qb = QuantumCircuit(4, 4); qb.h(0); qb.cx(0, 3); qb.h(1); qb.cx(1, 2)
            if basis == 'X': qb.h(range(4))
            qb.measure(range(4), range(4))
            b = run(qb, nm, shots)
            par = b.sum(1) % 2
            acc = par == 0
            logical = b[:, 1] ^ b[:, 2]  # Zbar1 Zbar2 = Z1Z2 ; Xbar1 Xbar2 = X1X2
            out[('enc', basis)] = (np.mean(logical[acc]), np.mean(acc), np.mean(logical))
        bare = 0.5*(out[('bare', 'Z')] + out[('bare', 'X')])
        encZ, accZ, rawZ = out[('enc', 'Z')]; encX, accX, rawX = out[('enc', 'X')]
        print(f"p2={p2:.3f}: bare Bell err (avg ZZ,XX)={bare:.5f} | encoded post-selected err={0.5*(encZ+encX):.5f} "
              f"accept={0.5*(accZ+accX):.4f} | encoded no-postselect err={0.5*(rawZ+rawX):.5f}")

def d2b(p2=0.005, shots=400000):
    print("\n=== D2b: [[4,2,2]] |00>_L prep: non-FT GHZ encoder vs flagged (Linke-style 5th qubit) ===")
    nm = noise_model(p2)
    # non-FT: H0, CX01, CX02, CX03 ; measure Z on all; accept even parity; logical (Z0Z1, Z0Z2)
    qa = QuantumCircuit(4, 4); qa.h(0); qa.cx(0, 1); qa.cx(0, 2); qa.cx(0, 3); qa.measure(range(4), range(4))
    a = run(qa, nm, shots)
    acc = a.sum(1) % 2 == 0
    lerr = ((a[:, 0] ^ a[:, 1]) | (a[:, 0] ^ a[:, 2])).astype(bool)
    print(f"non-FT Z-basis: accept={acc.mean():.4f} post-selected logical err={lerr[acc].mean():.5f}")
    # X-basis check of the same state: XXXX parity and logical X1X3? (|00>_L is not an Xbar eigenstate) -> check XXXX stabilizer only
    qa2 = QuantumCircuit(4, 4); qa2.h(0); qa2.cx(0, 1); qa2.cx(0, 2); qa2.cx(0, 3); qa2.h(range(4)); qa2.measure(range(4), range(4))
    a2 = run(qa2, nm, shots)
    print(f"non-FT X-basis: XXXX-violation rate={np.mean(a2.sum(1) % 2):.5f}")
    # flagged: same encoder + ancilla 4 that checks Z0Z3 parity (catches the weight-2 X error from a fault on q0)
    qb = QuantumCircuit(5, 5); qb.h(0); qb.cx(0, 1); qb.cx(0, 2); qb.cx(0, 3); qb.cx(1, 4); qb.cx(3, 4)
    qb.measure(range(5), range(5))
    b = run(qb, nm, shots)
    acc = (b[:, :4].sum(1) % 2 == 0) & (b[:, 4] == 0)
    lerr = ((b[:, 0] ^ b[:, 1]) | (b[:, 0] ^ b[:, 2])).astype(bool)
    print(f"flagged Z-basis: accept={acc.mean():.4f} post-selected logical err={lerr[acc].mean():.5f}")

# ---------------------------------------------------------------- D3: repetition code, unrolled ancillas
def rep_circuit(d, R):
    n = d + R*(d-1)
    qc = QuantumCircuit(n, n)
    for r in range(R):
        for i in range(d-1):
            a = d + r*(d-1) + i
            qc.cx(i, a); qc.cx(i+1, a)
    qc.measure(range(n), range(n))
    return qc

def rep_detectors(bits, d, R):
    S = bits.shape[0]
    m = np.zeros((S, R, d-1), dtype=np.uint8)
    for r in range(R):
        m[:, r, :] = bits[:, d + r*(d-1): d + (r+1)*(d-1)]
    data = bits[:, :d]
    final = data[:, :-1] ^ data[:, 1:]
    layers = np.concatenate([m, final[:, None, :]], axis=1)  # (S, R+1, d-1)
    det = layers.copy(); det[:, 1:, :] ^= layers[:, :-1, :]
    return det.reshape(S, -1), data[:, 0]

def build_rep_graph(d, R):
    G = nx.Graph()
    L = R + 1
    node = lambda r, i: r*(d-1) + i
    B = 'B'
    for r in range(L):
        for i in range(d-2):
            G.add_edge(node(r, i), node(r, i+1), weight=1, obs=0)
        G.add_edge(node(r, 0), B, weight=1, obs=1)        # error on data qubit 0
        if (r, d-2) != None:
            # right boundary (error on data qubit d-1): connect to a separate boundary node to keep obs parity well-defined
            G.add_edge(node(r, d-2), 'BR', weight=1, obs=0)
        if r < L-1:
            for i in range(d-1):
                G.add_edge(node(r, i), node(r+1, i), weight=1, obs=0)
    # merge boundaries: B and BR are the same "boundary" but obs differs -> connect with weight 0, obs 0
    G.add_edge(B, 'BR', weight=0, obs=0)
    return G

def mwpm_decoder(G, ndet):
    dist, paths = nx.all_pairs_dijkstra(G, weight='weight'), None
    D = {}; P = {}
    for src, (dd, pp) in nx.all_pairs_dijkstra(G, weight='weight'):
        for tgt, path in pp.items():
            par = 0
            for u, v in zip(path[:-1], path[1:]):
                par ^= G[u][v]['obs']
            D[(src, tgt)] = dd[tgt]; P[(src, tgt)] = par
    cache = {}
    def decode(det_row):
        key = det_row.tobytes()
        if key in cache: return cache[key]
        defects = list(np.flatnonzero(det_row))
        if not defects:
            cache[key] = 0; return 0
        M = nx.Graph()
        BIG = 1000
        for a, b in itertools.combinations(defects, 2):
            M.add_edge(('d', a), ('d', b), weight=BIG - D[(a, b)], obs=P[(a, b)])
        for a in defects:
            M.add_edge(('d', a), ('b', a), weight=BIG - D[(a, 'B')], obs=P[(a, 'B')])
        for a, b in itertools.combinations(defects, 2):
            M.add_edge(('b', a), ('b', b), weight=BIG, obs=0)
        mt = nx.max_weight_matching(M, maxcardinality=True)
        par = 0
        for u, v in mt:
            par ^= M[u][v]['obs']
        cache[key] = par
        return par
    return decode

def d3(ds=(3, 5, 7), R=3, p2s=(0.001, 0.003, 0.005, 0.01, 0.02, 0.04, 0.08), shots=40000):
    print(f"\n=== D3: repetition code, R={R} rounds with fresh ancillas (no mid-circuit reuse), MWPM via networkx ===")
    for d in ds:
        qc = rep_circuit(d, R)
        nq = qc.num_qubits; ncx = sum(1 for i in qc.data if i.operation.name == 'cx')
        G = build_rep_graph(d, R)
        dec = mwpm_decoder(G, (R+1)*(d-1))
        row = []
        for p2 in p2s:
            bits = run(qc, noise_model(p2), shots, seed=7)
            det, obs = rep_detectors(bits, d, R)
            pred = np.array([dec(det[s]) for s in range(shots)], dtype=np.uint8)
            ler = np.mean(pred != obs)
            raw = np.mean(obs)  # no decoding: read data qubit 0
            maj = np.mean((bits[:, :d].sum(1) > d//2))
            row.append((p2, ler, raw, maj))
        print(f"d={d}: qubits={nq}, CX={ncx}")
        for p2, ler, raw, maj in row:
            print(f"   p2={p2:.3f}  MWPM logical err={ler:.5f}  final-majority-only={maj:.5f}  undecoded(q0)={raw:.5f}")

# ---------------------------------------------------------------- D4: d=3 rotated surface code, Z memory, unrolled
XST = [[0, 1, 3, 4], [4, 5, 7, 8], [1, 2], [6, 7]]
ZST = [[1, 4, 2, 5], [3, 6, 4, 7], [0, 3], [5, 8]]

def surf_circuit(R, xchecks=True):
    nanc = (8 if xchecks else 4)
    n = 9 + R*nanc
    qc = QuantumCircuit(n, n)
    a = 9
    zanc = []
    for r in range(R):
        if xchecks:
            for st in XST:
                qc.h(a)
                for q in st: qc.cx(a, q)
                qc.h(a); a += 1
        zr = []
        for st in ZST:
            for q in st: qc.cx(q, a)
            zr.append(a); a += 1
        zanc.append(zr)
    qc.measure(range(n), range(n))
    return qc, zanc

def surf_detectors(bits, R, zanc):
    S = bits.shape[0]
    layers = []
    for r in range(R):
        layers.append(bits[:, zanc[r]])
    data = bits[:, :9]
    fin = np.stack([np.bitwise_xor.reduce(data[:, st], axis=1) for st in ZST], axis=1)
    layers.append(fin)
    L = np.stack(layers, axis=1)
    det = L.copy(); det[:, 1:, :] ^= L[:, :-1, :]
    obs = data[:, 0] ^ data[:, 1] ^ data[:, 2]
    return det.reshape(S, -1), obs

def ml_lookup(det_tr, obs_tr, det_te, obs_te):
    cnt = defaultdict(lambda: [0, 0])
    keys_tr = [r.tobytes() for r in det_tr]
    for k, o in zip(keys_tr, obs_tr): cnt[k][o] += 1
    table = {k: int(v[1] > v[0]) for k, v in cnt.items()}
    pred = np.array([table.get(r.tobytes(), 0) for r in det_te], dtype=np.uint8)
    return np.mean(pred != obs_te)

def d4(Rs=(1, 2), p2s=(0.001, 0.003, 0.005, 0.01, 0.02), shots=400000):
    print("\n=== D4: d=3 rotated surface code (9 data), Z-memory, fresh ancillas each round, ML-lookup decoder learned from half the shots ===")
    for R in Rs:
        qc, zanc = surf_circuit(R, xchecks=True)
        ncx = sum(1 for i in qc.data if i.operation.name == 'cx')
        print(f"R={R}: qubits={qc.num_qubits}, CX={ncx}")
        for p2 in p2s:
            bits = run(qc, noise_model(p2), shots, seed=11)
            det, obs = surf_detectors(bits, R, zanc)
            h = shots//2
            ler = ml_lookup(det[:h], obs[:h], det[h:], obs[h:])
            # code-capacity-style decode using only final data (lookup of final Z-syndrome -> min weight X correction)
            fin = det.reshape(shots, R+1, 4)
            fin_layer = np.bitwise_xor.reduce(fin, axis=1)  # = final data syndrome
            ler_final = ml_lookup(fin_layer[:h], obs[:h], fin_layer[h:], obs[h:])
            raw = np.mean(obs)
            # post-selection: accept only all-zero detectors
            acc = det.sum(1) == 0
            ps = np.mean(obs[acc]) if acc.any() else float('nan')
            print(f"   p2={p2:.3f}  ML-decoded LER={ler:.5f}  final-data-only LER={ler_final:.5f}  undecoded={raw:.5f}  postselect: accept={acc.mean():.4f} err={ps:.5f}")

if __name__ == '__main__':
    which = sys.argv[1:] or ['d1', 'd2', 'd2b', 'd3', 'd4']
    t0 = time.time()
    for w in which:
        globals()[w]()
        print(f"[elapsed {time.time()-t0:.1f}s]")
