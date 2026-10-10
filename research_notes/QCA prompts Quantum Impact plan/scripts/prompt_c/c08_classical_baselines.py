"""Prompt C, step 8: the realistic classical baselines (and their wall-clock).
- numpy vectorised filter on the real 2024 catalog and on synthetic catalogs up to 1e7 rows
- sqlite (in Pyodide too) with a B-tree index on magnitude: SELECT ... WHERE mag>=6 AND depth<70
- random-order scan expectation (N+1)/(M+1) and variance
- server-side: the FDSN service itself answers the query (minmagnitude/maxdepth) -> count endpoint
"""
import json, os, time, sqlite3, math, urllib.request
import numpy as np
import gs_core as G

rows = G.load_catalog()
mag = np.array([r["mag"] for r in rows]); dep = np.array([r["depth"] for r in rows])
out = {}
def timeit(f, reps=50):
    f(); t = time.perf_counter()
    for _ in range(reps): f()
    return (time.perf_counter() - t) / reps

t = timeit(lambda: np.flatnonzero((mag >= 6) & (dep < 70)), 2000)
out["numpy_real_1504"] = t
print(f"numpy filter, real N=1504: {t*1e6:.1f} us  ({t/1504*1e9:.2f} ns/row), matches={int(((mag>=6)&(dep<70)).sum())}")
rng = np.random.default_rng(0)
for N in (10**5, 10**6, 10**7):
    m = rng.choice(mag, N); d = rng.choice(dep, N)
    t = timeit(lambda: np.flatnonzero((m >= 6) & (d < 70)), 5)
    out[f"numpy_synth_{N}"] = t
    print(f"numpy filter, synthetic N={N:>9,d}: {t*1e3:8.2f} ms ({t/N*1e9:.2f} ns/row)")

# sqlite with index
con = sqlite3.connect(":memory:")
con.execute("create table ev(id text, mag real, depth real)")
N = 10**6
m = rng.choice(mag, N); d = rng.choice(dep, N)
con.executemany("insert into ev values (?,?,?)", ((str(i), float(a), float(b)) for i, (a, b) in enumerate(zip(m, d))))
q = "select count(*) from ev where mag>=7.0 and depth<70"
t_noidx = timeit(lambda: con.execute(q).fetchone(), 5)
con.execute("create index ix_mag on ev(mag)")
t_idx = timeit(lambda: con.execute(q).fetchone(), 50)
plan = con.execute("explain query plan " + q).fetchall()
out.update(sqlite_noindex_1e6=t_noidx, sqlite_index_1e6=t_idx, sqlite_plan=str(plan))
print(f"sqlite N=1e6, '{q}': no index {t_noidx*1e3:.1f} ms; B-tree index on mag {t_idx*1e3:.3f} ms; plan={plan}")

# random-order scan statistics (exact): first-match position in a random permutation
def scan_stats(N, M):
    if M == 0: return N, 0.0
    mean = (N + 1) / (M + 1)
    var = (N + 1) * (N - M) * M / ((M + 1) ** 2 * (M + 2))
    return mean, var
for (N, M) in [(8, 1), (16, 1), (32, 1), (64, 1), (64, 3), (1504, 72), (1504, 8)]:
    mu, v = scan_stats(N, M)
    sim = [int(np.argmax(rng.permutation(N) < M)) + 1 for _ in range(20000)]
    print(f"scan N={N:5d} M={M:3d}: E={mu:8.2f} (sim {np.mean(sim):8.2f}), SD={math.sqrt(v):7.2f} (sim {np.std(sim):7.2f}); Grover (pi/4)sqrt(N/M)={math.pi/4*math.sqrt(N/M):6.2f}")

# server-side: FDSN does the filtered search for you
def get(url):
    with urllib.request.urlopen(url, timeout=60) as r: return r.read().decode()
base = "https://earthquake.usgs.gov/fdsnws/event/1/count?starttime=2024-01-01&endtime=2025-01-01"
for qs in ("&minmagnitude=5", "&minmagnitude=6&maxdepth=70", "&minmagnitude=7&maxdepth=70", "&minmagnitude=5&alertlevel=yellow"):
    t0 = time.perf_counter(); c = get(base + qs).strip(); dt = time.perf_counter() - t0
    out["fdsn" + qs] = dict(count=c, seconds=dt)
    print(f"FDSN count{qs}: {c}  ({dt*1e3:.0f} ms round trip)")
try:
    t0 = time.perf_counter(); c = get("https://earthquake.usgs.gov/fdsnws/event/1/count?starttime=1900-01-01&endtime=2026-10-10").strip()
    out["fdsn_all_comcat"] = dict(count=c, seconds=time.perf_counter() - t0)
    print(f"FDSN count, whole ComCat 1900-2026-10-10 (all magnitudes): {c}")
except Exception as e:
    print("whole-ComCat count failed:", e)
json.dump(out, open(os.path.join(G.HERE, "results_c08_classical.json"), "w"), indent=1)
