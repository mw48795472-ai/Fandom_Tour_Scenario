import json,math
from collections import defaultdict
L=json.load(open('lang_v7.json',encoding='utf-8'))
d=json.load(open('data10.json',encoding='utf-8'))
Fs=d['F']
AL,M0=6.93,0.4201; ALG=5.93
FL=['영어','일본어','중국어','스페인어','프랑스어','태국어','인도네시아어','베트남어','러시아어','필리핀어','포르투갈어','튀르키예어','아랍어']
for k,v in L.items():
    v['sh']=(v['ov']+AL*M0)/(v['N']+AL)
mx=max(v['sh'] for v in L.values())
print('G_max = %.4f (%s)'%(mx,[k for k,v in L.items() if v['sh']==mx][0]))
# 페르소나 가중치
g=defaultdict(list)
for f in Fs:
    if f.get('p'): g[f['p']].append(L[f['n']]['ovs'])
means={k:sum(v)/len(v) for k,v in g.items()}
top=max(means.values()); CAP=0.08
W={k:round(CAP*v/top,3) for k,v in means.items()}
print('\n페르소나별 측정 해외비중 → 가중치 (상한 %.2f)'%CAP)
for k in sorted(means,key=lambda k:-means[k]):
    print(f"  {k:>8} n={len(g[k]):>3}  해외비중 {means[k]:.3f}  비율 {means[k]/top:.3f}  w_L = {W[k]:.3f}  (기존 0.150)")
# 언어별 축소 점유 top3
tg={}
for k,v in L.items():
    sl=[( (v['c'][1:][i]+ALG/13)/(v['N']+ALG), FL[i]) for i in range(13)]
    s=sum(x for x,_ in sl); sl=[(x/s,n) for x,n in sl]
    sl.sort(reverse=True); tg[k]=[[n,round(x,4)] for x,n in sl[:3]]
print('\n언어 대응 우선순위 예시')
for k in ['BTS','리센느(RESCENE)','송가인','김연자','잔나비','에픽하이','이효리','투어스(TWS)']:
    print(f"  {k:>16} " + ' · '.join(f"{n} {x*100:.0f}%" for n,x in tg[k]) + f"   G={L[k]['sh']/mx:.3f}")
out={n:{'G':round(L[n]['sh']/mx,4),'sh':round(L[n]['sh'],4),'ovs':L[n]['ovs'],'ov':L[n]['ov'],'N':L[n]['N'],
        'K':L[n]['K'],'oK':L[n]['oK'],'div':L[n]['div'],'odiv':L[n]['odiv'],'tg':tg[n]} for n in L}
json.dump({'lang':out,'W':W,'AL':AL,'M0':M0,'ALG':ALG,'GMAX':round(mx,4),'means':{k:round(v,4) for k,v in means.items()}},
          open('lang_final.json','w',encoding='utf-8'),ensure_ascii=False)
