import json,math,numpy as np
SD=['서울','부산','대구','인천','광주','대전','울산','세종','경기','강원','충북','충남','전북','전남','경북','경남','제주']
S=json.load(open('show_lq.json',encoding='utf-8'))
d=json.load(open('data14.json',encoding='utf-8'))
F={f['n']:f for f in d['F']}
pairs=[]
for n in S['pool']:
    f=F[n]
    if not f.get('lq'): continue
    for j in range(17):
        a=f['lq'][j]; b=S['LQ'][n][j]
        if a is None or b is None: continue
        pairs.append((n,SD[j],a,b))
A=np.array([p[2] for p in pairs]); B=np.array([p[3] for p in pairs])
print('셀 %d개 (팬덤 %d × 유효시도)'%(len(pairs),len(S['pool'])))
print('언급LQ ↔ 공연LQ  피어슨 r=%.3f'%np.corrcoef(A,B)[0,1])
la,lb=np.log(A),np.log(B)
print('  log-log r=%.3f'%np.corrcoef(la,lb)[0,1])
def rank(v):
    o=np.argsort(v); r=np.empty(len(v)); r[o]=np.arange(len(v)); return r
print('  스피어만 ρ=%.3f'%np.corrcoef(rank(A),rank(B))[0,1])
# 최고 LQ 지역 일치
agree=0;tot=0;dis=[]
for n in S['pool']:
    f=F[n]
    if not f.get('lq'): continue
    va=[(f['lq'][j],SD[j]) for j in range(17) if f['lq'][j] is not None]
    vb=[(S['LQ'][n][j],SD[j]) for j in range(17) if S['LQ'][n][j] is not None]
    if not va or not vb: continue
    ta=max(va)[1]; tb=max(vb)[1]; tot+=1
    if ta==tb: agree+=1
    else: dis.append((n,ta,tb,round(max(va)[0],2),round(max(vb)[0],2)))
print('\n최고 LQ 지역 일치 %d/%d (%.0f%%)'%(agree,tot,agree/tot*100))
print('일치 사례:',', '.join(n for n in S['pool'] if F[n].get('lq') and
   max((F[n]['lq'][j],SD[j]) for j in range(17) if F[n]['lq'][j] is not None)[1]==
   max((S['LQ'][n][j],SD[j]) for j in range(17) if S['LQ'][n][j] is not None)[1]))
print('\n불일치 상위 10 (언급 top / 공연 top)')
for x in dis[:10]: print('  ',x)
json.dump({'r':round(float(np.corrcoef(A,B)[0,1]),3),'rlog':round(float(np.corrcoef(la,lb)[0,1]),3),
 'rho':round(float(np.corrcoef(rank(A),rank(B))[0,1]),3),'agree':agree,'tot':tot,
 'pairs':[[p[0],p[1],round(p[2],3),round(p[3],3)] for p in pairs]},open('xchan.json','w',encoding='utf-8'),ensure_ascii=False)
