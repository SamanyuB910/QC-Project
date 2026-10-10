import json,urllib.request,sys
def get(u):
    r=urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'})
    return json.load(urllib.request.urlopen(r,timeout=30))
for kind in ['popular','recent']:
    items=[];nxt=None;seen=set()
    for i in range(60):
        u=f'https://api.qollab.xyz/api/project/{kind}?limit=30'+(f'&next={nxt}' if nxt else '')
        d=get(u)
        new=[x for x in d['items'] if x['id'] not in seen]
        if not new: break
        for x in new: seen.add(x['id'])
        items+=new
        nxt=d.get('next')
        if not nxt: break
    print(kind,len(items))
    json.dump(items,open(f'now_{kind}.json','w',encoding='utf-8'),ensure_ascii=False,indent=0)
old={x['id'] for x in json.load(open('../qollab/all_popular.json',encoding='utf-8'))}
now=json.load(open('now_recent.json',encoding='utf-8'))
print('keys',list(now[0].keys()))
for x in now:
    if x['id'] not in old:
        print('NEW',x['owner_username'],x['name'],'|',x['title'],'|',(x.get('description') or '')[:150],'|',x.get('created_at') or x.get('public_at'))
