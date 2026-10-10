"""Experiment 6: exact gate counts for the single-IonQ-job designs (IonQ-like basis rz,sx,x,rzz; rz virtual) and the
largest batch that fits IonQ's per-job limits (5,000 circuits; 150,000 gates), plus a shot-time proxy from exp4 part C."""
import json, numpy as np
from qiskit import QuantumCircuit, transpile
from exp5_gatecounts import zz_native

def pqk_circ(x, ent, basis):
    c = zz_native(x, 2, ent)
    n = len(x)
    if basis == "X": c.h(range(n))
    if basis == "Y": c.sdg(range(n)); c.h(range(n))
    c.measure_all()
    return c

rng = np.random.default_rng(0)
proxy = json.load(open("results/exp4_noise.json"))["C"]  # Aer per-shot trajectory seconds for 1000 shots
out = {}
for n in [4, 8, 12]:
    for ent in ["linear", "full"]:
        x, x2 = rng.uniform(0.0, 0.3, n), rng.uniform(0.0, 0.3, n)
        cnt = []
        for b in "XYZ":
            t = transpile(pqk_circ(x, ent, b), basis_gates=["rz", "sx", "x", "rzz", "measure"], optimization_level=3, seed_transpiler=1)
            ops = t.count_ops(); cnt.append(sum(v for k, v in ops.items() if k not in ("measure", "barrier")))
        g_pqk = float(np.mean(cnt))
        f = zz_native(x, 2, ent).compose(zz_native(x2, 2, ent).inverse()); f.measure_all()
        t = transpile(f, basis_gates=["rz", "sx", "x", "rzz", "measure"], optimization_level=3, seed_transpiler=1)
        g_fid = sum(v for k, v in t.count_ops().items() if k not in ("measure", "barrier"))
        B_pqk = int(min(5000 // 3, 150000 // (3 * g_pqk)))
        pairs_fid = int(min(5000, 150000 // g_fid))
        out[f"n{n}_{ent}"] = {"gates_per_pqk_circuit": g_pqk, "gates_per_fid_circuit": g_fid,
                              "max_patients_pqk_one_job": B_pqk, "max_fid_circuits_one_job": pairs_fid,
                              "fid_test_patients_one_job_at_60_SV": pairs_fid // 60}
        print(n, ent, out[f"n{n}_{ent}"])
# shot-time proxy: Aer noisy trajectories, native single thread (IonQ cloud speed unknown)
per_shot = {"n4_linear": proxy["n4_linear_1000shots_s"] / 1000, "n8_linear": proxy["n8_linear_1000shots_s"] / 1000,
            "n8_full": proxy["n8_full_1000shots_s"] / 1000, "n12_linear": proxy["n12_linear_1000shots_s"] / 1000}
designs = {"PQK test fold n8 linear (114 pts x 3 bases, 1000 shots)": (342, 1000, "n8_linear"),
           "PQK test fold n8 linear (114 x 3, 300 shots)": (342, 300, "n8_linear"),
           "PQK all 569 pts n8 linear (1707 circuits, 300 shots)": (1707, 300, "n8_linear"),
           "PQK 20-patient demo n8 linear (60 circuits, 1000 shots)": (60, 1000, "n8_linear"),
           "FQK block n8 linear (16 test x 60 SV = 960 circuits, 300 shots)": (960, 300, "n8_linear"),
           "PQK test fold n12 linear (342 circuits, 1000 shots)": (342, 1000, "n12_linear")}
out["time_proxy_aer_native_1thread_s"] = {k: c * s * per_shot[key] for k, (c, s, key) in designs.items()}
out["per_shot_s"] = per_shot
for k, v in out["time_proxy_aer_native_1thread_s"].items():
    print(f"{k}: {v:.0f} s")
json.dump(out, open("results/exp6_job_sizing.json", "w"), indent=1)
