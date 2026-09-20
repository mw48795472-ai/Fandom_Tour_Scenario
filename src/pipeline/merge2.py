# -*- coding: utf-8 -*-
import json
import poi_add as A
from sgg import SGG
CATMAP={'h':'herit','s':'sea','e':'heal','a':'activity','f':'food'}
d=json.load(open('data2.json',encoding='utf-8'))
P=d['P']
# 1) 소재지 정정 — 잘못 등록된 레코드 제거
before=len(P)
rm={(sd,sg,k) for sd,sg,k in A.FIX_REMOVE}
P=[p for p in P if (p['sd'],p['sg'],p['k']) not in rm]
print('정정 제거', before-len(P))
seen={(p['sd'],p['sg'],p['k']) for p in P}
nmax=max([int(p['id'][1:]) for p in P if p['id'].startswith('L')]+[0])
i=nmax
for k,items in A.ADD.items():
    sd,sg=k.split('/')
    for (nm,c,t) in items:
        if (sd,sg,nm) in seen: continue
        i+=1
        P.append({'id':'L%03d'%i,'sd':sd,'sg':sg,'k':nm,'c':CATMAP[c],'t':t,
                  'h':'','s':'','b':'','la':0,'ln':0,'v':0})
        seen.add((sd,sg,nm))
d['P']=P
json.dump(d,open('data3.json','w',encoding='utf-8'),ensure_ascii=False,separators=(',',':'))
cnt={}
for p in P: cnt[(p['sd'],p['sg'])]=cnt.get((p['sd'],p['sg']),0)+1
empty=[sd+'/'+sg for sd,l in SGG.items() for sg in l if cnt.get((sd,sg),0)==0]
thin=[sd+'/'+sg for sd,l in SGG.items() for sg in l if 0<cnt.get((sd,sg),0)<3]
print('POI 총',len(P),'검증',sum(p['v'] for p in P))
print('커버 시군구',len(cnt),'/ 229 · 미등록',len(empty),'· 3건 미만',len(thin))
print('미등록:',empty); print('얇음:',thin)
print('bytes',len(json.dumps(d,ensure_ascii=False)))
