# -*- coding: utf-8 -*-
import json, re
import poi_national as PN
from sgg import SGG

CATMAP={'h':'herit','s':'sea','e':'heal','a':'activity','f':'food'}
CITY2SGG={'gyeongju':'경북/경주시','geoje':'경남/거제시','suwon':'경기/수원시',
 'jeongseon':'강원/정선군','chungju':'충북/충주시','donghae':'강원/동해시'}
DJ={'na6':'대전/중구','nax5':'대전/중구','nax4':'대전/서구'}

old=json.load(open('data.json',encoding='utf-8'))
P=[]
for p in old['P']:
    key = DJ.get(p['id']) or CITY2SGG.get(p['ci'])
    if not key: raise SystemExit('unmapped '+p['id'])
    sd,sg=key.split('/')
    P.append({'id':p['id'],'sd':sd,'sg':sg,'k':p['k'],'c':p['c'],'t':p['t'],
              'h':p['h'],'s':p['s'],'b':p['b'],'la':p['la'],'ln':p['ln'],'v':1})
seen={(x['sd'],x['sg'],x['k']) for x in P}
i=0
for key,items in PN.N.items():
    if not items: continue
    sd,sg=key.rstrip('+').split('/')
    if sg not in SGG.get(sd,[]): raise SystemExit('bad sgg '+key)
    for (k,c,t) in items:
        if (sd,sg,k) in seen: continue
        i+=1
        P.append({'id':'L%03d'%i,'sd':sd,'sg':sg,'k':k,'c':CATMAP[c],'t':t,
                  'h':'','s':'','b':'','la':0,'ln':0,'v':0})
        seen.add((sd,sg,k))

S=[]
S2SGG={'sg1':'경북/경주시','sg2':'경북/경주시','sg3':'경북/경주시','sz1':'경남/거제시','sz2':'경남/거제시',
 'sz3':'경남/거제시','sn1':'강원/동해시','sn2':'강원/정선군','sn3':'경기/수원시','sn4':'충북/충주시'}
for s in old['S']:
    sd,sg=S2SGG[s['id']].split('/')
    S.append({'id':s['id'],'sd':sd,'sg':sg,'k':s['k'],'a':s['a'],'p':s['p'],'t':s['t']})

H={'경북/경주시':{'r':'신경주역 (KTX·SRT)','b':'경주고속버스터미널','m':['ktx','srt','bus']},
   '경남/거제시':{'r':None,'b':'고현버스터미널','m':['bus']},
   '경기/수원시':{'r':'수원역 (KTX)','b':'수원버스터미널','m':['ktx','bus']},
   '강원/정선군':{'r':'민둥산역','b':'정선버스터미널','m':['ktx','bus']},
   '대전/중구':{'r':'대전역 (KTX·SRT)','b':'대전복합터미널','m':['ktx','srt','bus']},
   '대전/서구':{'r':'대전역 (KTX·SRT)','b':'대전복합터미널','m':['ktx','srt','bus']},
   '충북/충주시':{'r':'충주역','b':'충주공용버스터미널','m':['ktx','bus']},
   '강원/동해시':{'r':'동해역','b':'동해종합버스터미널','m':['ktx','bus']}}

out={'F':old['F'],'P':P,'S':S,'H':H,'SGG':SGG,
     'LQ':{'경남/거제시':{'src':'거제','v':{'음식':2.230,'관광':1.710}},
           '경북/경주시':{'src':'경주','v':{'숙박':1.929,'쇼핑':0.208}},
           '경기/고양시':{'src':'고양','v':{'관광':1.423,'음식':0.159}},
           '부산/*':{'src':'부산','v':{'음식':1.394,'쇼핑':1.851}}}}
json.dump(out,open('data2.json','w',encoding='utf-8'),ensure_ascii=False,separators=(',',':'))
import collections
print('POI',len(P),'verified',sum(p['v'] for p in P),'시군구',len({(p['sd'],p['sg']) for p in P}))
print('bytes',len(json.dumps(out,ensure_ascii=False)))
