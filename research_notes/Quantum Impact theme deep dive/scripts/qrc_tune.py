import numpy as np, importlib.util, sys
spec = importlib.util.spec_from_file_location("q", "qrc_mg.py")
src = open("qrc_mg.py").read().split("T = 1700")[0]
exec(src)
from sklearn.linear_model import Ridge
T=1700; x = mackey_glass(T, sub=3); u=(x-x.min())/(x.max()-x.min()); w=6; ntr=1000
Xw = np.array([u[t - w + 1:t + 1] for t in range(w - 1, len(u))])
def ev(F, horizon, offset):
    tt = np.arange(offset, offset+len(F)); valid = tt+horizon < len(u)
    F2, y2 = F[valid], u[tt[valid]+horizon]
    Ftr,Fte,ytr,yte = F2[:ntr],F2[ntr:],y2[:ntr],y2[ntr:]
    best=min(((nmse(Ridge(alpha=a).fit(Ftr[:800],ytr[:800]).predict(Ftr[800:]),ytr[800:]),a) for a in [1e-8,1e-6,1e-4,1e-2,1]))
    m=Ridge(alpha=best[1]).fit(Ftr,ytr); return nmse(m.predict(Fte),yte), best[0]
rows=[]
for scale in [np.pi/4, np.pi/2, np.pi]:
  for h in [0.3, 1.0]:
    for npairs in [8, 16]:
      Q,n2q = qrc_features(u, n=8, w=w, npairs=npairs, h=h, scale=scale)
      Qa = np.hstack([Q, Xw])
      r1,v1 = ev(Qa,1,w-1); r5,v5 = ev(Qa,5,w-1)
      rows.append((v1+v5, scale, h, npairs, n2q, r1, r5))
      print(f"scale={scale:.2f} h={h} pairs/layer={npairs//1} ZZ={n2q}: QRC+window NMSE 1-step={r1:.2e} 5-step={r5:.2e}", flush=True)
E = esn_features(u, N=36); Ea = np.hstack([E[w-1:], Xw])
print("ESN36+window:", ev(Ea,1,w-1)[0], ev(Ea,5,w-1)[0])
