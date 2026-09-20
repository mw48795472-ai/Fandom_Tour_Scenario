import json,math,numpy as np
d=json.load(open('data12.json',encoding='utf-8')); AD=json.load(open('ad_v7.json',encoding='utf-8'))
LG=json.load(open('lang_v7.json',encoding='utf-8')); A,IND=AD['A'],AD['IND']
F=d['F']; n=len(F)
vol=np.array([A[f['n']]['a'] for f in F],float)
S=np.array([f['S'] for f in F]); L=np.array([f['L'] for f in F])
def dR2(x,y,base):
    X0=np.c_[base,np.ones(n)]; X1=np.c_[base,x,np.ones(n)]
    f=lambda X: 1-((y-X@np.linalg.lstsq(X,y,rcond=None)[0])**2).sum()/((y-y.mean())**2).sum()
    return f(X1)-f(X0), f(X1)
COM=['식음료','쇼핑','패션/의류','미용','스포츠/레저','엔터테인먼트','여행']
cand=[('광고비중',[A[f['n']]['share'] for f in F]),
      ('광고 업종수',[sum(1 for x in A[f['n']]['c'] if x>0) for f in F]),
      ('복지/행정 점유',[(A[f['n']]['c'][IND.index('복지/행정')]/max(sum(A[f['n']]['c']),1)) for f in F]),
      ('관광소비 매핑 점유',[(sum(A[f['n']]['c'][IND.index(i)] for i in COM)/max(sum(A[f['n']]['c']),1)) for f in F]),
      ('해외비중 (언어)',[LG[f['n']]['ovs'] for f in F]),
      ('검출언어수 (언어)',[LG[f['n']]['K'] for f in F]),
      ('지역 검출지역수',[(f['rv'][1] if f.get('rv') else 0) for f in F])]
print('종속변수 = 파급효과 S    기저모형: S ~ 근거문장수  (R2 = %.3f)\n'%(1-((S-np.c_[vol,np.ones(n)]@np.linalg.lstsq(np.c_[vol,np.ones(n)],S,rcond=None)[0])**2).sum()/((S-S.mean())**2).sum()))
print(f"{'추가 변수':>18}{'ΔR²':>9}{'모형 R²':>10}{'편상관':>9}")
for nm,x in cand:
    x=np.array(x,float); dr,r2=dR2(x,S,vol)
    rxy=np.corrcoef(x,S)[0,1]; rxz=np.corrcoef(x,vol)[0,1]; ryz=np.corrcoef(S,vol)[0,1]
    pr=(rxy-rxz*ryz)/math.sqrt((1-rxz**2)*(1-ryz**2))
    print(f"{nm:>18}{dr:>+9.3f}{r2:>10.3f}{pr:>+9.3f}")
print('\n종속변수 = 충성도 L')
print(f"{'추가 변수':>18}{'ΔR²':>9}{'모형 R²':>10}{'편상관':>9}")
for nm,x in cand:
    x=np.array(x,float); dr,r2=dR2(x,L,vol)
    rxy=np.corrcoef(x,L)[0,1]; rxz=np.corrcoef(x,vol)[0,1]; ryz=np.corrcoef(L,vol)[0,1]
    pr=(rxy-rxz*ryz)/math.sqrt((1-rxz**2)*(1-ryz**2))
    print(f"{nm:>18}{dr:>+9.3f}{r2:>10.3f}{pr:>+9.3f}")
