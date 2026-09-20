import json,math,numpy as np
from scipy.special import gammaln
from scipy.optimize import minimize
L=json.load(open('lang_v7.json',encoding='utf-8'))
N=np.array([v['N'] for v in L.values()],float); k=np.array([v['ov'] for v in L.values()],float)
def nll(th,N,k):
    m,s=1/(1+math.exp(-th[0])), math.exp(th[1]); a,b=m*s,(1-m)*s
    return -np.sum(gammaln(N+1)-gammaln(k+1)-gammaln(N-k+1)+gammaln(k+a)+gammaln(N-k+b)-gammaln(N+a+b)+gammaln(a+b)-gammaln(a)-gammaln(b))
r=minimize(nll,[0,math.log(20)],args=(N,k),method='Nelder-Mead',options={'xatol':1e-8,'fatol':1e-10,'maxiter':5000})
m=1/(1+math.exp(-r.x[0])); s=math.exp(r.x[1])
print('해외비중 경험베이즈  m=%.4f  alpha_L=s=%.2f  (a=%.2f b=%.2f)  -logL=%.1f'%(m,s,m*s,(1-m)*s,r.fun))
# 도메스틱 비교: 대표지역 비중에 같은 추정기
import csv
P='/root/.claude/uploads/453213c1-28c6-5903-952e-90318dd79866/5a233e5f-domestic_regional_index_v7.csv'
rows=[x for x in csv.DictReader(open(P,encoding='utf-8-sig')) if x.get('팬덤')]
SD=['서울','부산','대구','인천','광주','대전','울산','세종','경기','강원','충북','충남','전북','전남','경북','경남','제주']
Nd=[];kd=[]
for x in rows:
    n=int(x['총지역언급'])
    if n==0: continue
    c=[int(x[s]) for s in SD]
    Nd.append(n); kd.append(max(c))
Nd=np.array(Nd,float);kd=np.array(kd,float)
r2=minimize(nll,[0,math.log(10)],args=(Nd,kd),method='Nelder-Mead',options={'maxiter':5000})
print('국내 대표지역비중 경험베이즈 m=%.4f alpha=%.2f (n=%d)'%(1/(1+math.exp(-r2.x[0])),math.exp(r2.x[1]),len(Nd)))
json.dump({'m':m,'s':s},open('lang_eb.json','w'))
