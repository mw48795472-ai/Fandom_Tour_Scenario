import json,math,numpy as np
SD=['서울','부산','대구','인천','광주','대전','울산','세종','경기','강원','충북','충남','전북','전남','경북','경남','제주']
AF=json.load(open('aff_asym.json',encoding='utf-8'))
LF=json.load(open('lang_final.json',encoding='utf-8'))
d=json.load(open('data12.json',encoding='utf-8'))
names=AF['names']; A=np.array([[np.nan if v is None else v for v in r] for r in AF['A']])
LQ=np.array([[np.nan if v is None else v for v in r] for r in AF['LQ']])
pi=np.array(AF['pi']); al=np.array(AF['a'])
TOP=[]
for i,s in enumerate(SD):
    if s=='세종': TOP.append([s,round(pi[i]*100,2),round(al[i],3),None,None,None,0]); continue
    o=int(np.argsort(-A[:,i])[0]); n5=int((LQ[:,i]>1).sum())
    TOP.append([s,round(pi[i]*100,2),round(al[i],3),names[o],round(float(LQ[o,i]),2),round(float(A[o,i]),3),n5])
best=[SD[int(np.nanargmax(A[k]))] if np.nanmax(A[k])>0 else None for k in range(len(names))]
from collections import Counter
cnt=Counter(x for x in best if x)
# 언어 상위/하위
L=LF['lang']; G=sorted(L.items(),key=lambda t:-t[1]['G'])
LANGTOP=[[k,v['ov'],v['N'],round(v['ovs'],3),round(v['sh'],3),round(v['G'],3),v['tg'][0][0]] for k,v in G[:8]]
LANGBOT=[[k,v['ov'],v['N'],round(v['ovs'],3),round(v['sh'],3),round(v['G'],3),v['tg'][0][0]] for k,v in G[-6:]]
SCAT=[[k,v['N'],round(v['ovs'],3)] for k,v in L.items()]
Fm={f['n']:f for f in d['F']}
SCAT=[[k,round(L[k]['ovs'],3),round(Fm[k]['S'],3),Fm[k]['a']] for k in L]
TG=[[k,L[k]['tg']] for k in ['BTS','투어스(TWS)','에픽하이','김연자','잔나비','송가인','이효리','리센느(RESCENE)']]
json.dump({'TOP':TOP,'cnt':cnt.most_common(),'LANGTOP':LANGTOP,'LANGBOT':LANGBOT,'SCAT':SCAT,'TG':TG,
  'W':LF['W'],'means':LF['means'],'pi':[round(float(x),5) for x in pi],'a':[round(float(x),4) for x in al]},
  open('docdata.json','w',encoding='utf-8'),ensure_ascii=False)
print(json.dumps(TOP,ensure_ascii=False))
print(cnt.most_common())
print('언급 없음/기저이하로 최고 LQ 없음:',sum(1 for x in best if not x))
