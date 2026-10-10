"""Shared helpers for Prompt C ("Grover the Seismologist") experiments.

- catalog loading + real slices of the 2024 USGS M>=5 catalog
- predicate (shallow & M>=6 by default) and its honest bit-level encoding
- oracles: (a) list oracle (tutorial style: one MCZ per KNOWN marked index),
           (b) honest QROM + comparator oracle (loads raw depth/mag codes per index,
               evaluates the predicate in superposition, phase-kicks, uncomputes)
- diffusion, Grover circuits, transpile targets (IonQ-like all-to-all rz/rx/rzz; IBM heavy-hex)
- IonQ forte-1-like depolarizing noise model
All seeds fixed for reproducibility.
"""
import json, os, math
import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, transpile
import warnings
from qiskit.circuit.library import MCMTGate, ZGate, UCRYGate, IntegerComparator
from qiskit.transpiler import CouplingMap
from qiskit.providers.fake_provider import GenericBackendV2

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")

# ---------------------------------------------------------------- catalog
def load_catalog():
    rows = json.load(open(os.path.join(DATA, "catalog_2024_m5_slim.json"), encoding="utf-8"))
    rows.sort(key=lambda r: r["time"])          # chronological
    return rows

MAG_BITS, DEPTH_BITS = 5, 4          # mag code: 0.1-mag steps above 5.0 (5.0..8.1); depth code: 10-km bins (0..150 km)
MAG_THR, DEPTH_THR = 6.0, 70.0       # default rare condition: shallow (<70 km) and M>=6.0

def predicate(r, mag_thr=MAG_THR, depth_thr=DEPTH_THR):
    return (r["depth"] < depth_thr) and (r["mag"] >= mag_thr)

def mag_code(mag, bits=MAG_BITS):
    return int(min(max(math.floor((mag - 5.0) * 10 + 1e-6), 0), 2**bits - 1))

def depth_code(depth, bits=DEPTH_BITS):
    return int(min(max(math.floor(depth / 10.0 + 1e-9), 0), 2**bits - 1))

def slice_events(rows, n, rng, contiguous=True):
    N = 2**n
    if contiguous:
        s = int(rng.integers(0, len(rows) - N + 1))
        return rows[s:s + N]
    idx = rng.choice(len(rows), size=N, replace=False)
    return [rows[i] for i in idx]

def marked_indices(sl, pred=predicate):
    return [i for i, r in enumerate(sl) if pred(r)]

# ---------------------------------------------------------------- oracles
def list_oracle(n, marked):
    """Tutorial-style phase oracle: needs the list of marked indices (i.e. the answer)."""
    qc = QuantumCircuit(n, name="O_list")
    for m in marked:
        zeros = [q for q in range(n) if not (m >> q) & 1]
        if zeros: qc.x(zeros)
        if n == 1: qc.z(0)
        else: qc.append(MCMTGate(ZGate(), n - 1, 1), list(range(n)))
        if zeros: qc.x(zeros)
    return qc

def qrom_ucry(n, values, bits):
    """|i>|0> -> |i>|values[i]> using one multiplexed RY(0 or pi) per data bit (ancilla-free, N CNOTs/bit)."""
    qc = QuantumCircuit(n + bits, name="QROM")
    for b in range(bits):
        angles = [math.pi if (v >> b) & 1 else 0.0 for v in values]
        if any(angles):
            qc.append(UCRYGate(angles), [n + b] + list(range(n)))  # target first, then controls
    return qc

def qrom_select(n, values, bits):
    """Naive SELECT-style QROM: for each index, compute flag=[idx==i] with an MCX, fan out CNOTs, uncompute."""
    qc = QuantumCircuit(n + bits + 1, name="QROM_sel")
    flag = n + bits
    from qiskit.circuit.library import MCXGate
    for i, v in enumerate(values):
        if v == 0: continue
        zeros = [q for q in range(n) if not (i >> q) & 1]
        if zeros: qc.x(zeros)
        qc.append(MCXGate(n), list(range(n)) + [flag])
        for b in range(bits):
            if (v >> b) & 1: qc.cx(flag, n + b)
        qc.append(MCXGate(n), list(range(n)) + [flag])
        if zeros: qc.x(zeros)
    return qc

def honest_oracle(n, sl, mag_thr=MAG_THR, depth_thr=DEPTH_THR, qrom="ucry"):
    """QROM(raw mag code, raw depth code) + two reversible comparators + CZ phase + uncompute.
    Qubit layout: [idx(n)] [mag(MB)] [dep(DB)] [cm] [cd] [anc(max(MB,DB)-1)] (+1 flag if qrom='select')."""
    MB, DB = MAG_BITS, DEPTH_BITS
    mvals = [mag_code(r["mag"]) for r in sl]
    dvals = [depth_code(r["depth"]) for r in sl]
    vals = [m | (d << MB) for m, d in zip(mvals, dvals)]
    mthr = mag_code(mag_thr)                           # M>=6.0 -> code >= 10
    dthr = int(round(depth_thr / 10.0))                # depth<70 -> code < 7
    na = max(MB, DB) - 1
    nq = n + MB + DB + 2 + na + (1 if qrom == "select" else 0)
    qc = QuantumCircuit(nq, name="O_honest")
    idx = list(range(n)); mag = list(range(n, n + MB)); dep = list(range(n + MB, n + MB + DB))
    cm, cd = n + MB + DB, n + MB + DB + 1
    anc = list(range(n + MB + DB + 2, n + MB + DB + 2 + na))
    if qrom == "ucry":
        load = qrom_ucry(n, vals, MB + DB); load_q = idx + mag + dep
    else:
        load = qrom_select(n, vals, MB + DB); load_q = idx + mag + dep + [nq - 1]
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        # explicit-ancilla comparator circuits: [state bits][result][state_bits-1 ancillas]
        cmpm = IntegerComparator(MB, mthr, geq=True).decompose().to_gate(label="cmp_mag>=%d" % mthr)
        cmpd = IntegerComparator(DB, dthr, geq=False).decompose().to_gate(label="cmp_dep<%d" % dthr)
    qc.compose(load, load_q, inplace=True)
    qc.append(cmpm, mag + [cm] + anc[:MB - 1])
    qc.append(cmpd, dep + [cd] + anc[:DB - 1])
    qc.cz(cm, cd)
    qc.append(cmpd.inverse(), dep + [cd] + anc[:DB - 1])
    qc.append(cmpm.inverse(), mag + [cm] + anc[:MB - 1])
    qc.compose(load.inverse(), load_q, inplace=True)
    return qc

def diffusion(n):
    qc = QuantumCircuit(n, name="D")
    qc.h(range(n)); qc.x(range(n))
    if n == 1: qc.z(0)
    else: qc.append(MCMTGate(ZGate(), n - 1, 1), list(range(n)))
    qc.x(range(n)); qc.h(range(n))
    return qc

def grover_circuit(n, oracle, k, measure=True):
    nq = oracle.num_qubits
    qc = QuantumCircuit(nq, n if measure else 0)
    qc.h(range(n))
    D = diffusion(n)
    for _ in range(k):
        qc.compose(oracle, range(nq), inplace=True)
        qc.compose(D, range(n), inplace=True)
    if measure: qc.measure(range(n), range(n))
    return qc

def p_success_theory(N, M, k):
    if M == 0: return 0.0
    th = math.asin(math.sqrt(M / N))
    return math.sin((2 * k + 1) * th) ** 2

def k_opt(N, M):
    if M == 0: return 0
    return int(math.floor(math.pi / (4 * math.asin(math.sqrt(M / N)))))

# ---------------------------------------------------------------- targets
IONQ_BASIS = ["rz", "rx", "rzz"]          # all-to-all stand-in for GPi/GPi2/ZZ (Z is virtual on IonQ)
_HH = None
def heavy_hex_backend():
    global _HH
    if _HH is None:
        cm = CouplingMap.from_heavy_hex(7)  # 115 qubits, IBM-style heavy-hex
        _HH = GenericBackendV2(num_qubits=cm.size(), basis_gates=["cz", "rz", "sx", "x", "id"],
                               coupling_map=cm, seed=7)
    return _HH

def to_ionq(qc, opt=3, seed=11):
    return transpile(qc, basis_gates=IONQ_BASIS, optimization_level=opt, seed_transpiler=seed)

def to_heavyhex(qc, opt=3, seed=11):
    return transpile(qc, backend=heavy_hex_backend(), optimization_level=opt, seed_transpiler=seed)

def twoq(qc):
    return sum(1 for ins in qc.data if ins.operation.num_qubits == 2)

def twoq_depth(qc):
    return qc.depth(lambda ins: ins.operation.num_qubits == 2)

def ionq_billed_mcx(nq_gate):
    """IonQ billing rule given by organizers: an n-qubit multi-controlled gate = 6(n-2) two-qubit gates."""
    return 6 * (nq_gate - 2) if nq_gate > 2 else 1

# ---------------------------------------------------------------- noise
P1, P2 = 2.67e-4, 4.95e-3   # IonQ forte-1 rates given in the brief
def ionq_noise_model(p1=P1, p2=P2, readout=0.0):
    from qiskit_aer.noise import NoiseModel, depolarizing_error, ReadoutError
    nm = NoiseModel(basis_gates=IONQ_BASIS)
    nm.add_all_qubit_quantum_error(depolarizing_error(p1, 1), ["rx"])   # rz virtual
    nm.add_all_qubit_quantum_error(depolarizing_error(p2, 2), ["rzz"])
    if readout > 0:
        nm.add_all_qubit_readout_error(ReadoutError([[1 - readout, readout], [readout, 1 - readout]]))
    return nm
