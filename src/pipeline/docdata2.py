import json,math,numpy as np
d=json.load(open('data13.json',encoding='utf-8')); AD=json.load(open('ad_v7.json',encoding='utf-8'))
LG=json.load(open('lang_v7.json',encoding='utf-8')); PR=json.load(open('ad_prof.json',encoding='utf-8'))
NO=json.load(open('ad_norm.json',encoding='utf-8'))
F=d['F']; A,IND=AD['A'],AD['IND']; n=len(F)
vol=np.array([A[f['n']]['a'] for f in F],float); S=np.array([f['S'] for f in F]); L=np.array([f['L'] for f in F])
def fitR2(X,y):
    b=np.linalg.lstsq(X,y,rcond=None)[0]; p=X@b
    return 1-((y-p)**2).sum()/((y-y.mean())**2).sum()
def pr(x,y,z):
    rxy=np.corrcoef(x,y)[0,1];rxz=np.corrcoef(x,z)[0,1];ryz=np.corrcoef(y,z)[0,1]
    return (rxy-rxz*ryz)/math.sqrt((1-rxz**2)*(1-ryz**2))
COM=['식음료','쇼핑','패션/의류','미용','스포츠/레저','엔터테인먼트','여행']
gv=IND.index('복지/행정')
cand=[('광고비중','광고',[A[f['n']]['share'] for f in F]),
      ('광고 업종수','광고',[sum(1 for x in A[f['n']]['c'] if x>0) for f in F]),
      ('복지/행정 점유','광고',[(A[f['n']]['c'][gv]/max(sum(A[f['n']]['c']),1)) for f in F]),
      ('관광소비 매핑 점유','광고',[(sum(A[f['n']]['c'][IND.index(i)] for i in COM)/max(sum(A[f['n']]['c']),1)) for f in F]),
      ('해외비중','언어',[LG[f['n']]['ovs'] for f in F]),
      ('검출언어수','언어',[LG[f['n']]['K'] for f in F]),
      ('언어다양성','언어',[LG[f['n']]['div'] for f in F]),
      ('검출지역수','지역',[(f['rv'][1] if f.get('rv') else 0) for f in F])]
base=fitR2(np.c_[vol,np.ones(n)],S); baseL=fitR2(np.c_[vol,np.ones(n)],L)
TBL=[]
for nm,g,x in cand:
    x=np.array(x,float)
    TBL.append([nm,g,round(float(np.corrcoef(x,S)[0,1]),3),round(float(pr(x,S,vol)),3),
                round(float(fitR2(np.c_[vol,x,np.ones(n)],S)-base),3),
                round(float(pr(x,L,vol)),3),round(float(fitR2(np.c_[vol,x,np.ones(n)],L)-baseL),3)])
# 잔차 산점도: S와 광고비중을 각각 vol로 회귀한 잔차
def resid(y):
    X=np.c_[vol,np.ones(n)]; return y-X@np.linalg.lstsq(X,y,rcond=None)[0]
ad=np.array([A[f['n']]['share'] for f in F]); RS=resid(S); RA=resid(ad)
RES=[[F[i]['n'],round(float(RA[i]),4),round(float(RS[i]),4)] for i in range(n)]
print('잔차 상관 r=%.3f'%np.corrcoef(RA,RS)[0,1])
# 업종 기저 + 매핑
MAPPED=set(PR['MAP'])
tot=[sum(A[k]['c'][i] for k in A) for i in range(20)]
IND20=[[IND[i],tot[i],round(NO['pi20'][i],4),IND[i] in MAPPED, PR['MAP'].get(IND[i],'')] for i in range(20)]
IND20.sort(key=lambda r:-r[1])
# 상업유발도 상하위
Cs=sorted(F,key=lambda f:-f['ad']['C'])
CTOP=[[f['n'],f['ad']['n'],f['ad']['tot'],f['ad']['raw'],f['ad']['sh'],f['ad']['C'],f['ad']['top']] for f in Cs[:8]]
CBOT=[[f['n'],f['ad']['n'],f['ad']['tot'],f['ad']['raw'],f['ad']['sh'],f['ad']['C'],f['ad']['top'] or '없음'] for f in Cs[-5:]]
# 복지/행정 상위
gvs=sorted(F,key=lambda f:-f['ad']['gov'][0])[:10]
GOV=[[f['n'],f['ad']['gov'][0],f['ad']['gov'][1],f['ad']['n']] for f in gvs]
# 5영역 기저
A5=d['LQAREAS']
AREA=[[A5[i],int(np.array([f['ad']['cnt'][i] for f in F]).sum()),round(PR['pi'][i],4),round(PR['a'][i],4)] for i in range(5)]
json.dump({'TBL':TBL,'base':round(float(base),3),'baseL':round(float(baseL),3),'RES':RES,
  'rres':round(float(np.corrcoef(RA,RS)[0,1]),3),'IND20':IND20,'CTOP':CTOP,'CBOT':CBOT,'GOV':GOV,'AREA':AREA,
  'cov':PR['cov'],'K5':PR['K'],'K20':NO['K20'],'Cm':NO['Cm'],'Ca':NO['Ca'],'Cmax':NO['Cmax']},
  open('docdata2.json','w',encoding='utf-8'),ensure_ascii=False)
for r in TBL: print(r)
print('base S=%.3f  L=%.3f'%(base,baseL))
