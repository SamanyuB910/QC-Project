import numpy as np
exec(open("qrc_tune.py").read().split("rows=[]")[0])
rng=np.random.default_rng(5)
Q,n2q = qrc_features(u, n=8, w=w, npairs=8, h=0.3, scale=np.pi/4)
for label, F in [("ideal",1.0),("global-depol 0.5%/2q",0.995**n2q)]:
  for S in [None, 1000, 10000, 100000]:
    Qn = F*Q if S is None else F*Q + rng.normal(size=Q.shape)*np.sqrt(np.clip(1-(F*Q)**2,0,1)/S)
    Qa=np.hstack([Qn,Xw]); print(f"{label:22s} shots={S}: 1-step={ev(Qa,1,w-1)[0]:.2e} 5-step={ev(Qa,5,w-1)[0]:.2e}")
Qa=np.hstack([np.zeros_like(Q),Xw]); print("window only (linear):", ev(Xw,1,w-1)[0], ev(Xw,5,w-1)[0])
