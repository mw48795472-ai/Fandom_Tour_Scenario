import json,csv,math,numpy as np
SD=['서울','부산','대구','인천','광주','대전','울산','세종','경기','강원','충북','충남','전북','전남','경북','경남','제주']
a=np.array(json.load(open('asym.json'))['a']); A=a.sum()
rows=[x for x in csv.DictReader(open('/root/.claude/uploads/453213c1-28c6-5903-952e-90318dd79866/5a233e5f-domestic_regional_index_v7.csv',encoding='utf-8-sig')) if x.get('팬덤')]
D=[{'n':x['팬덤'],'c':np.array([int(x[s]) for s in SD],float),'N':int(x['총지역언급']),'K':int(x['검출지역수'])} for x in rows]
pi=a/A
post=lambda d:(d['c']+a)/(d['N']+A)
LQ=np.array([post(d)/pi for d in D])          # 100 x 17
LQ[:, SD.index('세종')]=np.nan
mx=np.nanmax(LQ)
iy,ix=np.unravel_index(np.nanargmax(LQ),LQ.shape)
print('LQ_max %.3f  %s · %s'%(mx,D[iy]['n'],SD[ix]))
print('\n시도별 1위 (비대칭 사전)')
rep_seoul=0
for i,s in enumerate(SD):
    if s=='세종': print(f"  {s:>3}  측정 불가 — 코퍼스 내 언급 0건 (사전 농도 0)"); continue
    o=np.argsort(-LQ[:,i])[:3]
    print(f"  {s:>3}  "+' | '.join(f"{D[j]['n']} LQ {LQ[j,i]:.2f} A {LQ[j,i]/mx:.3f}" for j in o))
# 대표지역(최대 LQ 기준) 분포
best=[SD[int(np.nanargmax(LQ[k]))] for k in range(len(D))]
from collections import Counter
print('\n최대 LQ 지역 분포 (비대칭):',Counter(best).most_common())
# 대칭 비교
al=4.03
P2=np.array([(d['c']+al/17)/(d['N']+al) for d in D])
best2=[SD[int(np.argmax(P2[k]))] for k in range(len(D))]
print('최대 점유 지역 분포 (대칭)  :',Counter(best2).most_common())
json.dump({'LQ':[[None if math.isnan(v) else round(float(v),4) for v in r] for r in LQ],'mx':round(float(mx),4),
           'pi':[round(float(x),6) for x in pi],'a':[round(float(x),4) for x in a],'A':round(float(A),4),
           'names':[d['n'] for d in D]},open('asym_lq.json','w',encoding='utf-8'),ensure_ascii=False)
