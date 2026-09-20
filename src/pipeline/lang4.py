import json,math,csv,numpy as np
from scipy.special import gammaln
from scipy.optimize import minimize_scalar
SD=['서울','부산','대구','인천','광주','대전','울산','세종','경기','강원','충북','충남','전북','전남','경북','경남','제주']
rows=[x for x in csv.DictReader(open('/root/.claude/uploads/453213c1-28c6-5903-952e-90318dd79866/5a233e5f-domestic_regional_index_v7.csv',encoding='utf-8-sig')) if x.get('팬덤')]
C=np.array([[int(x[s]) for s in SD] for x in rows],float); C=C[C.sum(1)>0]
def dmnll(la,C,K):
    a=math.exp(la); ak=a/K; N=C.sum(1)
    return -np.sum(gammaln(a)-gammaln(N+a)+np.sum(gammaln(C+ak)-gammaln(ak),axis=1))
r=minimize_scalar(dmnll,args=(C,17),bounds=(-3,6),method='bounded')
print('국내 17개 시도 대칭 디리클레-다항 경험베이즈  alpha = %.2f  (현재 채택 10)  n=%d'%(math.exp(r.x),len(C)))
# 언어: 14종 대칭이 아니라 한국어/해외 2항이 관심 → 해외 13종 대칭 디리클레
L=json.load(open('lang_v7.json',encoding='utf-8'))
CL=np.array([v['c'][1:] for v in L.values()],float); CL=CL[CL.sum(1)>0]
r3=minimize_scalar(dmnll,args=(CL,13),bounds=(-3,6),method='bounded')
print('해외 13개 언어 대칭 디리클레-다항 경험베이즈  alpha = %.2f  n=%d'%(math.exp(r3.x),len(CL)))
