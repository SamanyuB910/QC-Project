"""Step 10b: frontier recovery vs shot budget, ideal and NOISY. The noisy distributions are estimated once from a large
Aer run (forte-1 depolarizing rates) and then resampled at matched shot budgets (200 repeats each)."""
import numpy as np
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "s10_pareto_onejob.py")).read() if False else None
import os
HERE = os.path.dirname(os.path.abspath(__file__))
code = open(os.path.join(HERE, "s10_pareto_onejob.py")).read()
top, rest = code.split("# matched-sample comparison")
exec(top)
# circuit builder + noise model from s10 (definitions only)
defs = rest.split("noise = NoiseModel()")[0]
defs = defs[defs.index("from qiskit import QuantumCircuit"):]
exec(defs)
noise = NoiseModel()
noise.add_all_qubit_quantum_error(depolarizing_error(2.67e-4, 1), ["rx", "rz"])
noise.add_all_qubit_quantum_error(depolarizing_error(4.95e-3, 2), ["rzz"])
sim = AerSimulator(noise_model=noise, method="statevector", seed_simulator=17)
BIG = 10000
circs = [transpile(circuit(mu)[0], basis_gates=["rzz", "rx", "rz"], optimization_level=2, seed_transpiler=1) for mu in MU_GRID]
t = time.time()
job = sim.run(circs, shots=BIG).result()
print(f"noisy reference run: {BIG} shots x {len(circs)} circuits in {time.time()-t:.0f}s", flush=True)
noisy_feas, noisy_phw5 = {}, {}
for i, mu in enumerate(MU_GRID):
    cnt = job.get_counts(i)
    v = np.zeros(1287)
    for k_, c in cnt.items():
        s_ = int(k_, 2)
        if k_.count("1") == K:
            v[POS_IN_FEAS[s_]] += c
    noisy_phw5[mu] = v.sum() / BIG
    noisy_feas[mu] = v / v.sum()
    I = inst(r_full, C_full, mu)
    print(f"  mu={mu:4.2f}: noisy P(HW5)={noisy_phw5[mu]:.3f}  noisy P(opt|HW5)={noisy_feas[mu][POS_IN_FEAS[I.opt]]:.4f} "
          f"(ideal {dists[mu][POS_IN_FEAS[I.opt]]:.4f}, null|k {nulls[mu][POS_IN_FEAS[I.opt]]:.4f}, uniform {1/1287:.5f})", flush=True)
out = {}
for shots in [100, 200, 500, 1000]:
    for name in ["QAOA_ideal", "QAOA_noisy_forte1", "product_null_k", "uniform_k"]:
        qs = []
        for rep in range(200):
            rs = np.random.default_rng(rep)
            samp = []
            for mu in MU_GRID:
                ph = noisy_phw5[mu] if name == "QAOA_noisy_forte1" else P_HW5
                nf = rs.binomial(shots, ph)
                pr = {"QAOA_ideal": dists[mu], "QAOA_noisy_forte1": noisy_feas[mu], "product_null_k": nulls[mu]}.get(name, np.full(1287, 1 / 1287))
                samp += FEAS_IDX[rs.choice(1287, nf, p=pr)].tolist()
            qs.append(front_quality(samp))
        qs = np.array(qs)
        out[f"{name}_{shots}"] = {"mu_opt_found": qs[:, 0].mean(), "all5": (qs[:, 0] == 5).mean(), "pareto_found": qs[:, 1].mean(),
                                  "auc_front_found": qs[:, 2].mean(), "hv": qs[:, 3].mean(), "hv_p5": np.percentile(qs[:, 3], 5)}
        print(f"shots/circuit={shots:5d} {name:18s}: mu-optima {qs[:,0].mean():.2f}/5 (all 5: {100*(qs[:,0]==5).mean():3.0f}%)  "
              f"score-Pareto {qs[:,1].mean():5.1f}/{len(pareto_states)}  AUC-front {qs[:,2].mean():.2f}/{len(auc_front_states)}  "
              f"HV {qs[:,3].mean():.3f} (p5 {np.percentile(qs[:,3],5):.3f})", flush=True)
save_json("s10b_pareto_shots.json", {"noisy_phw5": noisy_phw5, "rows": out})
