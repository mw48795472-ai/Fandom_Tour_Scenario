import json,math,numpy as np
from scipy.special import gammaln
from scipy.optimize import minimize,minimize_scalar
AD=json.load(open('ad_v7.json',encoding='utf-8')); A,IND=AD['A'],AD['IND']
d=json.load(open('data12.json',encoding='utf-8')); F=d['F']; A5=d['LQAREAS']
MAP={'식음료':'음식','쇼핑':'관광/쇼핑','패션/의류':'관광/쇼핑','미용':'관광/쇼핑',
     '스포츠/레저':'레저활동','엔터테인먼트':'공연/전시','여행':'숙박'}
M=np.zeros((len(F),5))
for k,f in enumerate(F):
    c=A[f['n']]['c']
    for i,ind in enumerate(IND):
        if ind in MAP: M[k,A5.index(MAP[ind])]+=c[i]
cov=M.sum()/sum(sum(v['c']) for v in A.values())
print('매핑 커버리지 %.1f%% (%d / %d건)'%(cov*100,M.sum(),sum(sum(v['c']) for v in A.values())))
print('영역별 합계',dict(zip(A5,M.sum(0).astype(int))))
nz=M[M.sum(1)>0]
def dm(th,C,K):
    a=np.exp(th); ak=a if len(np.atleast_1d(a))>1 else np.full(K,a/K); N=C.sum(1)
    return -np.sum(gammaln(ak.sum())-gammaln(N+ak.sum())+np.sum(gammaln(C+ak)-gammaln(ak),axis=1))
pool=nz.sum(0)/nz.sum()
r=minimize(dm,np.log(np.maximum(pool,1e-3)*5),args=(nz,5),method='L-BFGS-B',options={'maxiter':20000})
a=np.exp(r.x); K=a.sum()
print('\n비대칭 디리클레 (관광소비 5영역 광고 프로파일)  총 농도 κ=%.3f'%K)
for i,s in enumerate(A5): print(f"  {s:>7} α={a[i]:.4f}  기저 π={a[i]/K*100:5.2f}%  풀 점유={pool[i]*100:5.2f}%")
rs=minimize_scalar(lambda la: dm(np.log(np.full(5,math.exp(la)/5)),nz,5),bounds=(-3,6),method='bounded')
print('대칭 α=%.2f  ΔlogL=%.1f'%(math.exp(rs.x),dm(np.log(np.full(5,math.exp(rs.x)/5)),nz,5)-r.fun))
# 팬덤별 5영역 사후 프로파일
prof={}
for k,f in enumerate(F):
    n=M[k]; post=(n+a)/(n.sum()+K)
    prof[f['n']]={'n':[int(x) for x in n],'w':[round(float(x),4) for x in post],
                  'lq':[round(float(post[i]/(a[i]/K)),3) for i in range(5)]}
print('\n사례')
for nm in ['이효리','리센느(RESCENE)','BTS','TWICE','임영웅','송가인','이찬원','조용필','김동률']:
    p=prof[nm]; print(f"  {nm:>16} 건수 {p['n']}  가중 {[round(x,3) for x in p['w']]}  LQ {p['lq']}")
json.dump({'MAP':MAP,'A5':A5,'a':[round(float(x),4) for x in a],'K':round(float(K),4),
           'pi':[round(float(x/K),5) for x in a],'prof':prof,'cov':round(float(cov),4)},
          open('ad_prof.json','w',encoding='utf-8'),ensure_ascii=False)
