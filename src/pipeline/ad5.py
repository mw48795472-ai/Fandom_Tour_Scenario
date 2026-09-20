import json,math,numpy as np
from scipy.special import gammaln
from scipy.optimize import minimize
AD=json.load(open('ad_v7.json',encoding='utf-8')); A,IND=AD['A'],AD['IND']
d=json.load(open('data12.json',encoding='utf-8')); F=d['F']
C=np.array([A[f['n']]['c'] for f in F],float); nz=C[C.sum(1)>0]
def dm(th,Cm):
    a=np.exp(th); N=Cm.sum(1)
    return -np.sum(gammaln(a.sum())-gammaln(N+a.sum())+np.sum(gammaln(Cm+a)-gammaln(a),axis=1))
pool=nz.sum(0)/nz.sum()
r=minimize(dm,np.log(np.maximum(pool,1e-4)*6),args=(nz,),method='L-BFGS-B',options={'maxiter':40000})
a=np.exp(r.x); K=a.sum(); pi=a/K
print('20개 업종 비대칭 디리클레  총 농도 = %.3f'%K)
for i in np.argsort(-pi)[:8]: print(f"  {IND[i]:>12} π={pi[i]*100:5.2f}%  α={a[i]:.4f}")
ind20={}
for k,f in enumerate(F):
    n=C[k]; post=(n+a)/(n.sum()+K)
    lq=post/pi
    ind20[f['n']]={'lq':[round(float(x),3) for x in lq],'n':[int(x) for x in n]}
gi=IND.index('복지/행정')
top=sorted(F,key=lambda f:-ind20[f['n']]['lq'][gi])[:12]
print('\n복지/행정 광고 LQ 상위 (지자체·공익 캠페인 노출)')
for f in top: print(f"  {f['n']:>16} LQ {ind20[f['n']]['lq'][gi]:5.2f}  {ind20[f['n']]['n'][gi]:>2}건 / 광고 {A[f['n']]['ad']}건")
# 광고비중 정규화 (베타-이항 경험베이즈)
ad=np.array([A[f['n']]['ad'] for f in F],float); tot=np.array([A[f['n']]['a'] for f in F],float)
def bb(th):
    m=1/(1+math.exp(-th[0])); s=math.exp(th[1]); aa,bb_=m*s,(1-m)*s
    return -np.sum(gammaln(tot+1)-gammaln(ad+1)-gammaln(tot-ad+1)+gammaln(ad+aa)+gammaln(tot-ad+bb_)-gammaln(tot+aa+bb_)+gammaln(aa+bb_)-gammaln(aa)-gammaln(bb_))
r2=minimize(bb,[0,math.log(20)],method='Nelder-Mead',options={'maxiter':8000,'xatol':1e-9,'fatol':1e-11})
m=1/(1+math.exp(-r2.x[0])); s=math.exp(r2.x[1])
sh=(ad+s*m)/(tot+s); mx=sh.max()
print('\n광고비중 경험베이즈  m=%.4f  α_C=%.2f  축소 최대=%.4f (%s)'%(m,s,mx,F[int(sh.argmax())]['n']))
Cn={F[k]['n']:{'sh':round(float(sh[k]),4),'C':round(float(sh[k]/mx),4)} for k in range(len(F))}
for nm in ['이효리','aespa','리센느(RESCENE)','BTS','임영웅','송가인','김동률','나훈아','투어스(TWS)','잔나비']:
    k=[i for i,f in enumerate(F) if f['n']==nm][0]
    print(f"  {nm:>16} {int(ad[k]):>2}/{int(tot[k]):>3} 원 {ad[k]/tot[k]:.3f} → 축소 {sh[k]:.4f}  C {Cn[nm]['C']:.3f}")
json.dump({'IND':IND,'a20':[round(float(x),4) for x in a],'pi20':[round(float(x),5) for x in pi],
  'K20':round(float(K),3),'ind20':ind20,'C':Cn,'Cm':round(m,4),'Ca':round(s,3),'Cmax':round(float(mx),4)},
  open('ad_norm.json','w',encoding='utf-8'),ensure_ascii=False)
