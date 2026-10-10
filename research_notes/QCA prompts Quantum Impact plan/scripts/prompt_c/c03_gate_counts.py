"""Prompt C, step 3: gate counts per oracle call and per full Grover run.
Compares: tutorial list oracle (needs answer), honest QROM(ucry or select)+comparator oracle, diffusion.
Targets: IonQ-like all-to-all {rz,rx,rzz} and an IBM-style heavy-hex GenericBackendV2 {cz,rz,sx,x}.
"""
import json, os, time, warnings
import numpy as np
warnings.filterwarnings("ignore")
import gs_core as G

rows = G.load_catalog()
rng = np.random.default_rng(7)
res = []
for n in range(3, 7):
    N = 2**n
    while True:  # same slice-selection rule/seed as c02
        sl = G.slice_events(rows, n, rng); mk = G.marked_indices(sl)
        if 1 <= len(mk) <= max(1, N // 8): break
    M = len(mk); k = G.k_opt(N, M)
    t0 = time.time()
    OL = G.list_oracle(n, mk); OHu = G.honest_oracle(n, sl, qrom="ucry"); OHs = G.honest_oracle(n, sl, qrom="select")
    D = G.diffusion(n)
    rec = dict(n=n, N=N, M=M, k_opt=k, qubits_list=n, qubits_honest_ucry=OHu.num_qubits, qubits_honest_select=OHs.num_qubits)
    for name, qc in [("list_oracle", OL), ("honest_oracle_ucry", OHu), ("honest_oracle_select", OHs), ("diffusion", D)]:
        ti = G.to_ionq(qc); th = G.to_heavyhex(qc)
        rec[name] = dict(ionq_2q=G.twoq(ti), ionq_2q_depth=G.twoq_depth(ti), ionq_1q=len(ti.data) - G.twoq(ti),
                         hh_2q=G.twoq(th), hh_2q_depth=G.twoq_depth(th))
    # full Grover circuits at k_opt
    for name, O in [("grover_list", OL), ("grover_honest_ucry", OHu)]:
        qc = G.grover_circuit(n, O, k)
        ti = G.to_ionq(qc); th = G.to_heavyhex(qc)
        rec[name] = dict(ionq_2q=G.twoq(ti), ionq_2q_depth=G.twoq_depth(ti), hh_2q=G.twoq(th), hh_2q_depth=G.twoq_depth(th))
    # IonQ billing rule: n-qubit MC gate = 6(n-2) 2Q gates
    rec["ionq_billed"] = dict(list_oracle=M * G.ionq_billed_mcx(n), diffusion=G.ionq_billed_mcx(n),
                              grover_list=k * (M + 1) * G.ionq_billed_mcx(n))
    rec["sec"] = time.time() - t0
    res.append(rec)
    print(f"\nn={n} N={N} M={M} k_opt={k}  (qubits: list {n}, honest-ucry {OHu.num_qubits}, honest-select {OHs.num_qubits}) [{rec['sec']:.1f}s]")
    for key in ["list_oracle", "honest_oracle_ucry", "honest_oracle_select", "diffusion", "grover_list", "grover_honest_ucry"]:
        r = rec[key]
        print(f"  {key:22s} IonQ-like 2Q={r['ionq_2q']:6d} (2Q-depth {r['ionq_2q_depth']:6d}) | heavy-hex 2Q={r['hh_2q']:6d} (2Q-depth {r['hh_2q_depth']:6d})")
    print(f"  IonQ billed (6(n-2) per MC gate): list oracle {rec['ionq_billed']['list_oracle']}, diffusion {rec['ionq_billed']['diffusion']}, full list-Grover {rec['ionq_billed']['grover_list']}")

# scaling of honest QROM (ucry) cost with bits per field, at fixed n (no comparator): 2Q = 2*b*N expected
print("\nQROM(ucry) load+unload 2Q count vs data bits b (IonQ-like basis), random data:")
scal = []
for n in (3, 4, 5, 6):
    for b in (1, 4, 9, 16):
        vals = [int(v) for v in np.random.default_rng(n * 100 + b).integers(0, 2**b, size=2**n)]
        q = G.qrom_ucry(n, vals, b)
        c = G.twoq(G.to_ionq(q.compose(q.inverse())))
        scal.append(dict(n=n, b=b, N=2**n, twoq_load_unload=c, formula_2bN=2 * b * 2**n))
        print(f"  n={n} N={2**n:3d} b={b:2d}: 2Q={c:5d}  (2bN={2*b*2**n})")
json.dump(dict(per_n=res, qrom_scaling=scal), open(os.path.join(G.HERE, "results_c03_gate_counts.json"), "w"), indent=1)
