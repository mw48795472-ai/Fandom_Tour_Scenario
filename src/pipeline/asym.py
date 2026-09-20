import json,csv,math,numpy as np
from scipy.special import gammaln
from scipy.optimize import minimize
SD=['서울','부산','대구','인천','광주','대전','울산','세종','경기','강원','충북','충남','전북','전남','경북','경남','제주']
rows=[x for x in csv.DictReader(open('/root/.claude/uploads/453213c1-28c6-5903-952e-90318dd79866/5a233e5f-domestic_regional_index_v7.csv',encoding='utf-8-sig')) if x.get('팬덤')]
C=np.array([[int(x[s]) for s in SD] for x in rows],float); C=C[C.sum(1)>0]
N=C.sum(1)
def nll(th):
    a=np.exp(th)
    return -np.sum(gammaln(a.sum())-gammaln(N+a.sum())+np.sum(gammaln(C+a)-gammaln(a),axis=1))
pool=C.sum(0)/C.sum(); x0=np.log(np.maximum(pool,1e-3)*4.03)
r=minimize(nll,x0,method='L-BFGS-B',options={'maxiter':20000})
a=np.exp(r.x); A=a.sum()
print('비대칭 디리클레: 총 농도 α = %.2f   -logL %.1f'%(A,r.fun))
print('   기저분포 π (전국 언급 분포 대비)')
for i,s in enumerate(SD):
    print(f"     {s:>3}  α_r={a[i]:6.3f}  π={a[i]/A*100:5.2f}%   실제 풀 점유={pool[i]*100:5.2f}%")
# 대칭 비교
def nlls(la):
    aa=math.exp(la); ak=aa/17
    return -np.sum(gammaln(aa)-gammaln(N+aa)+np.sum(gammaln(C+ak)-gammaln(ak),axis=1))
from scipy.optimize import minimize_scalar
rs=minimize_scalar(nlls,bounds=(-3,6),method='bounded')
print('대칭 α=%.2f  -logL %.1f   ΔlogL=%.1f  (자유도 +16)'%(math.exp(rs.x),rs.fun,rs.fun-r.fun))
import scipy.stats as ss
print('LR p =',ss.chi2.sf(2*(rs.fun-r.fun),16))
np.save('asym_a.npy',a)
json.dump({'a':[round(float(x),4) for x in a],'A':round(float(A),3)},open('asym.json','w'))
