import json,math,statistics
L=json.load(open('lang_v7.json',encoding='utf-8'))
d=json.load(open('data10.json',encoding='utf-8'))
Fs=d['F']; LANGS=['한국어','영어','일본어','중국어','스페인어','프랑스어','태국어','인도네시아어','베트남어','러시아어','필리핀어','포르투갈어','튀르키예어','아랍어']
Ns=[v['N'] for v in L.values()]
aL=statistics.median(Ns)
p0=sum(v['ov'] for v in L.values())/sum(v['N'] for v in L.values())
print('alpha_L(중앙값 총언어언급) =',aL,' pooled 해외비중 p0 =',round(p0,4))
print('총언어언급 min/max',min(Ns),max(Ns))
for k,v in L.items():
    v['sh']=(v['ov']+aL*p0)/(v['N']+aL)              # 축소 해외점유
    v['shl']=[(c+aL*p0/13)/(v['N']+aL) for c in v['c'][1:]]  # 언어별 축소 점유(해외 13종)
mx=max(v['sh'] for v in L.values())
mn=min(v['sh'] for v in L.values())
for v in L.values(): v['G']=v['sh']/mx
print('축소 해외점유 max %.4f (%s)  min %.4f (%s)'%(mx,[k for k,v in L.items() if v['sh']==mx][0],mn,[k for k,v in L.items() if v['sh']==mn][0]))
print('\n--- 원 해외비중 vs 축소 해외점유 (변화 큰 순 10) ---')
rows=sorted(L.items(),key=lambda t:-abs(t[1]['ovs']-t[1]['sh']))[:10]
for k,v in rows: print(f"{k:>16} N={v['N']:>3} 해외 {v['ov']:>3}  원 {v['ovs']:.3f} → 축소 {v['sh']:.3f} (Δ{v['sh']-v['ovs']:+.3f})  G={v['G']:.3f}")
print('\n--- 상위/하위 8 (축소 기준) ---')
s=sorted(L.items(),key=lambda t:-t[1]['sh'])
for k,v in s[:8]: print(f"  {k:>16} 축소 {v['sh']:.3f} G {v['G']:.3f}  (원 {v['ovs']:.3f})")
print('  ...')
for k,v in s[-6:]: print(f"  {k:>16} 축소 {v['sh']:.3f} G {v['G']:.3f}  (원 {v['ovs']:.3f})")
# 순위 변동
def rk(key):
    s=sorted(L,key=lambda k:-L[k][key]); return {k:i+1 for i,k in enumerate(s)}
r1,r2=rk('ovs'),rk('sh')
mv=sorted(L,key=lambda k:-abs(r1[k]-r2[k]))[:6]
print('\n--- 순위 변동 큰 팬덤 ---')
for k in mv: print(f"  {k:>16} {r1[k]:>3}위 → {r2[k]:>3}위 ({r2[k]-r1[k]:+d})  N={L[k]['N']}")
json.dump({'aL':aL,'p0':round(p0,4),'max':mx},open('lang_meta.json','w'))
