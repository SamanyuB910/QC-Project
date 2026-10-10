import json,urllib.request,time
p={x['owner_username']+'/'+x['name']:x for x in json.load(open('now_popular.json',encoding='utf-8'))}
names='''Sitifar/quantum-game-pizza-race jamie/systemic-oracle alireza/quantum-regime-radar bawa27/qorbital hsadeghi/quantum-advantage-lab q-aad/quantum-market-game-theory-sim qollab/quantum-chemistry qollab/learn-app-race jonromero/collapsing-ai Rudra1x/qaip-hardware-ranking mirko/krylov-quantum-diagonalization WilliamDenyer/depth-independent-coherence akshayuttarkar/qupepfold qcat/qchemistry manish/qchemistry plamsoft/mejorruta plamsoft/distancia ndazeo/registration-vectors Sagar/data-analysis-with-python S0cra13s/quantum-automitigation SQuant/s2s-probe-size qollab/showcase-option-pricing qollab/showcase-portfolio-opt qollab/showcase-qaoa-qubo qollab/showcase-qubo-exact qollab/quantum-kernel-showcase-drag-t qollab/showcase-vqc-xor qollab/showcase-estimator-qnn qollab/quantum-chemistry-showcase-the qollab/quantum-chemistry-showcase-t-2 qollab/cross-framework-showcase-one-v qollab/showcase-vqe-ground-state qollab/showcase-h2-ground-state'''.split()
out={}
for n in names:
    x=p[n]
    for t in range(4):
        try:
            u=f"https://api.qollab.xyz/api/project/id/{x['id']}/versions/head"
            d=json.load(urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=30))
            break
        except Exception as e:
            d={'error':str(e)}; time.sleep(2)
    d['_meta']={k:x[k] for k in ['title','views_cnt','head_updated_at']}
    out[n]=d; time.sleep(0.6)
json.dump(out,open('apps_heads.json','w',encoding='utf-8'),ensure_ascii=False)
with open('apps_writeups.txt','w',encoding='utf-8') as f:
    for n,d in out.items():
        f.write(f"\n\n######## {n} | {d['_meta']} | tag={d.get('tag')} public_at={d.get('public_at')} err={d.get('error')}\n")
        f.write((d.get('content') or '')[:6000])
        code=d.get('code') or ''
        f.write(f"\n---- code len {len(code)}; first 1200:\n"+code[:1200])
print('done',sum(1 for d in out.values() if 'error' in d))
