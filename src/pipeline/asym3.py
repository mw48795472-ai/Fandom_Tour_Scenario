import json,math,numpy as np
d=json.load(open('asym_lq.json',encoding='utf-8'))
SD=['서울','부산','대구','인천','광주','대전','울산','세종','경기','강원','충북','충남','전북','전남','경북','경남','제주']
LQ=np.array([[np.nan if v is None else v for v in r] for r in d['LQ']]); names=d['names']
mx=d['mx']; LM=math.log(mx)
A=np.clip(np.log(np.maximum(LQ,1e-9))/LM,0,1)
A[:,SD.index('세종')]=np.nan
fin=A[~np.isnan(A)]
print('셀 %d개  LQ>=1 비율 %.1f%%  A>0 %.1f%%'%(fin.size,np.nanmean(LQ>=1)*100,(fin>0).mean()*100))
print('A 분포: 평균 %.3f 중앙 %.3f 90%%분위 %.3f'%(fin.mean(),np.median(fin),np.quantile(fin,.9)))
print('\n시도별 상위3 (로그 정규화)')
for i,s in enumerate(SD):
    if s=='세종': print(f"  {s:>3}  측정 불가"); continue
    o=np.argsort(-A[:,i])[:3]
    print(f"  {s:>3}  "+' | '.join(f"{names[j]} {A[j,i]:.3f}(LQ {LQ[j,i]:.1f})" for j in o))
print('\n주요 사례')
for n,r in [('송가인','전남'),('리센느(RESCENE)','경남'),('이효리','제주'),('여자친구','서울'),('김재중','서울'),('GOT7','서울'),('투어스(TWS)','서울'),('BTS','서울'),('TWICE','울산')]:
    j=names.index(n); i=SD.index(r)
    print(f"  {n:>16} · {r}  LQ {LQ[j,i]:6.2f}  A {A[j,i]:.3f}")
json.dump({'A':[[None if math.isnan(v) else round(float(v),4) for v in r] for r in A],
           'LQ':d['LQ'],'names':names,'pi':d['pi'],'a':d['a'],'Aconc':d['A'],'LQMAX':mx},
          open('aff_asym.json','w',encoding='utf-8'),ensure_ascii=False)
