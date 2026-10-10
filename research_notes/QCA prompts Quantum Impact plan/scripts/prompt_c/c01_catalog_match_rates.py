"""Prompt C, step 1: real match rates M/N in the USGS 2024 catalog.

Reads data/usgs_2024_m5.geojson (fetched 2026-10-10 from
https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=2024-01-01&endtime=2024-12-31&minmagnitude=5)
and data/usgs_2024_m45.csv (M>=4.5, endtime=2025-01-01).

Prints match counts for several seismologically meaningful predicates and the
product types attached to events (moment-tensor, shakemap, losspager, finite-fault...).
"""
import json, csv, collections, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(HERE, "data")

with open(os.path.join(D, "usgs_2024_m5.geojson"), encoding="utf-8") as f:
    gj = json.load(f)
feats = [ft for ft in gj["features"] if ft["properties"].get("type") == "earthquake"]
print("GeoJSON M>=5 features:", len(gj["features"]), " type==earthquake:", len(feats))

rows = []
for ft in feats:
    p = ft["properties"]; lon, lat, dep = ft["geometry"]["coordinates"]
    types = set(t for t in (p.get("types") or "").split(",") if t)
    rows.append(dict(id=ft["id"], mag=p["mag"], depth=dep, lat=lat, lon=lon,
                     alert=p.get("alert"), tsunami=p.get("tsunami"), felt=p.get("felt"),
                     sig=p.get("sig"), mmi=p.get("mmi"), magType=p.get("magType"),
                     place=p.get("place"), types=types, time=p["time"]))
N = len(rows)

def count(name, pred):
    m = sum(1 for r in rows if pred(r))
    print(f"{name:55s} M={m:5d}  M/N={m/N:8.5f}  1/rate={N/max(m,1):8.1f}")
    return m

print(f"\nN = {N} (2024, M>=5, earthquakes)")
count("shallow (<70 km) & M>=7", lambda r: r["depth"] < 70 and r["mag"] >= 7)
count("M>=7 (any depth)", lambda r: r["mag"] >= 7)
count("shallow (<70 km) & M>=6.5", lambda r: r["depth"] < 70 and r["mag"] >= 6.5)
count("shallow (<70 km) & M>=6", lambda r: r["depth"] < 70 and r["mag"] >= 6)
count("shallow (<70 km) & M>=7.5 (tsunamigenic-class)", lambda r: r["depth"] < 70 and r["mag"] >= 7.5)
count("USGS tsunami flag == 1", lambda r: r["tsunami"] == 1)
count("tsunami flag & shallow & M>=6.5", lambda r: r["tsunami"] == 1 and r["depth"] < 70 and r["mag"] >= 6.5)
count("PAGER alert not null", lambda r: r["alert"] is not None)
for lvl in ("green", "yellow", "orange", "red"):
    count(f"PAGER alert == {lvl}", lambda r, l=lvl: r["alert"] == l)
count("PAGER alert in {yellow,orange,red}", lambda r: r["alert"] in ("yellow", "orange", "red"))
count("PAGER alert in {orange,red}", lambda r: r["alert"] in ("orange", "red"))
count("felt reports >= 100 (DYFI)", lambda r: (r["felt"] or 0) >= 100)
count("felt reports >= 1000 (DYFI)", lambda r: (r["felt"] or 0) >= 1000)
count("significance sig >= 600 (USGS 'significant' feed)", lambda r: (r["sig"] or 0) >= 600)
count("deep (>=300 km)", lambda r: r["depth"] >= 300)
count("shallow (<70 km)", lambda r: r["depth"] < 70)

print("\nProduct types present on events (fraction of N):")
tc = collections.Counter(t for r in rows for t in r["types"])
for t, c in tc.most_common():
    print(f"  {t:28s} {c:5d}  {c/N:.3f}")

print("\nM>=7 events in 2024:")
for r in sorted(rows, key=lambda r: -r["mag"]):
    if r["mag"] >= 7:
        print(f"  M{r['mag']:.1f} depth={r['depth']:6.1f} alert={r['alert']} tsunami={r['tsunami']} felt={r['felt']} {r['place']}")

# M>=4.5 CSV for the larger N regime
with open(os.path.join(D, "usgs_2024_m45.csv"), encoding="utf-8") as f:
    rr = [r for r in csv.DictReader(f) if r["type"] == "earthquake"]
N2 = len(rr)
m2 = sum(1 for r in rr if float(r["depth"]) < 70 and float(r["mag"]) >= 7)
m3 = sum(1 for r in rr if float(r["depth"]) < 70 and float(r["mag"]) >= 6)
print(f"\nM>=4.5 2024 CSV: N={N2}; shallow&M>=7: {m2} (rate {m2/N2:.5f}); shallow&M>=6: {m3} (rate {m3/N2:.5f})")
# bits needed per field
import math
print("\nIndex bits: N=%d -> n=%d ; N=%d -> n=%d" % (N, math.ceil(math.log2(N)), N2, math.ceil(math.log2(N2))))
json.dump([{k: (sorted(v) if isinstance(v, set) else v) for k, v in r.items()} for r in rows],
          open(os.path.join(D, "catalog_2024_m5_slim.json"), "w", encoding="utf-8"))
print("wrote data/catalog_2024_m5_slim.json")
