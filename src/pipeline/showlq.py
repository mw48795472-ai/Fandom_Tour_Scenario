import json,math,numpy as np
from scipy.special import gammaln
from scipy.optimize import minimize,minimize_scalar
SD=['서울','부산','대구','인천','광주','대전','울산','세종','경기','강원','충북','충남','전북','전남','경북','경남','제주']
C=json.load(open('shows_clean.json',encoding='utf-8'))
d=json.load(open('data14.json',encoding='utf-8')); NAMES=[f['n'] for f in d['F']]
SEARCHED=set(NAMES)                 # b1~b11 — 100팀 전원 조사 완료
have=set(C['have'])
empty=sorted(SEARCHED-have,key=NAMES.index)
unsearched=[n for n in NAMES if n not in SEARCHED]
print('수집 %d · 조사했으나 무기록 %d · 미조사 %d'%(len(have),len(empty),len(unsearched)))
print('무기록:',', '.join(empty))
pool=sorted(SEARCHED,key=NAMES.index)
M=np.zeros((len(pool),17)); Mn=np.zeros((len(pool),17))
idx={n:i for i,n in enumerate(pool)}
for r in C['clean']:
    i=idx[r['artist']]; j=SD.index(r['sido'])
    M[i,j]+=r['n']; Mn[i,j]+=1
print('총 회차 %d · 총 건수 %d'%(M.sum(),Mn.sum()))
print('시도별 회차:',{SD[j]:int(M[:,j].sum()) for j in range(17) if M[:,j].sum()})
nz=M[M.sum(1)>0]
def dm(th,Cm):
    a=np.exp(th); N=Cm.sum(1)
    return -np.sum(gammaln(a.sum())-gammaln(N+a.sum())+np.sum(gammaln(Cm+a)-gammaln(a),axis=1))
p0=nz.sum(0)/nz.sum()
r=minimize(dm,np.log(np.maximum(p0,1e-4)*5),args=(nz,),method='L-BFGS-B',options={'maxiter':40000})
a=np.exp(r.x); K=a.sum(); pi=a/K
rs=minimize_scalar(lambda la: dm(np.log(np.full(17,math.exp(la)/17)),nz),bounds=(-3,6),method='bounded')
print('\n비대칭 디리클레 총 농도 κ=%.3f   대칭 α=%.2f ΔlogL=%.1f'%(K,math.exp(rs.x),dm(np.log(np.full(17,math.exp(rs.x)/17)),nz)-r.fun))
for j in np.argsort(-pi):
    if a[j]<1e-4 and M[:,j].sum()==0: continue
    print(f'  {SD[j]:>3} π={pi[j]*100:5.2f}%  α={a[j]:.4f}  실회차 {int(M[:,j].sum()):>3}')
LQ={}
for n in pool:
    i=idx[n]; post=(M[i]+a)/(M[i].sum()+K)
    LQ[n]=[(None if pi[j]<=0 else round(float(post[j]/pi[j]),3)) for j in range(17)]
mx=max(v for n in pool for v in LQ[n] if v)
print('\nLQ 최대 %.2f'%mx)
for n in ['임영웅','BTS','이찬원','영탁','정동원','송가인','싸이','리센느(RESCENE)','김호중','QWER']:
    if n in LQ:
        top=sorted(((LQ[n][j],SD[j]) for j in range(17) if LQ[n][j]),reverse=True)[:3]
        print(f"  {n:>16} " + ' · '.join(f'{s} {v:.2f}' for v,s in top) + f"   회차 {int(M[idx[n]].sum())}")
json.dump({'pool':pool,'empty':empty,'unsearched':unsearched,'a':[round(float(x),4) for x in a],
  'K':round(float(K),3),'pi':[round(float(x),6) for x in pi],'LQ':LQ,'mx':round(float(mx),3),
  'M':{n:[int(x) for x in M[idx[n]]] for n in pool},'Mn':{n:[int(x) for x in Mn[idx[n]]] for n in pool}},
  open('show_lq.json','w',encoding='utf-8'),ensure_ascii=False)
