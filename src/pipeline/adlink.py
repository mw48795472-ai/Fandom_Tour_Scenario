import json,csv,math,numpy as np
AD=json.load(open('ad_v7.json',encoding='utf-8')); A,IND=AD['A'],AD['IND']
d=json.load(open('data16.json',encoding='utf-8')); F=d['F']; n=len(F)
MAP={'식음료':'음식','쇼핑':'관광/쇼핑','패션/의류':'관광/쇼핑','미용':'관광/쇼핑',
     '스포츠/레저':'레저활동','엔터테인먼트':'공연/전시','여행':'숙박'}
vol=np.array([A[f['n']]['a'] for f in F],float); S=np.array([f['S'] for f in F]); L=np.array([f['L'] for f in F])
def R2(X,y):
    b=np.linalg.lstsq(X,y,rcond=None)[0]; return 1-((y-X@b)**2).sum()/((y-y.mean())**2).sum()
def part(x,y,z):
    rxy,rxz,ryz=[float(np.corrcoef(u,v)[0,1]) for u,v in ((x,y),(x,z),(y,z))]
    return (rxy-rxz*ryz)/math.sqrt((1-rxz**2)*(1-ryz**2))
share=np.array([A[f['n']]['share'] for f in F])
link=np.array([ (sum(A[f['n']]['c'][IND.index(i)] for i in MAP)/max(sum(A[f['n']]['c']),1)) for f in F])
# 관광소비 연결 광고비중 = 광고비중 × 연결률 (문장 기준 근사)
linked=share*link
base=R2(np.c_[vol,np.ones(n)],S); baseL=R2(np.c_[vol,np.ones(n)],L)
print('기저 R²  S %.3f · L %.3f\n'%(base,baseL))
print(f"{'변수':>26}{'편상관(S)':>11}{'ΔR²(S)':>9}{'편상관(L)':>11}{'ΔR²(L)':>9}")
for nm,x in [('광고비중 (현재 C의 원값)',share),('관광소비 연결률',link),('연결 광고비중 = 비중×연결률',linked),
             ('비연결 광고비중',share*(1-link))]:
    print(f"{nm:>26}{part(x,S,vol):>+11.3f}{R2(np.c_[vol,x,np.ones(n)],S)-base:>+9.3f}{part(x,L,vol):>+11.3f}{R2(np.c_[vol,x,np.ones(n)],L)-baseL:>+9.3f}")
# 둘 다 넣으면?
r2=R2(np.c_[vol,linked,share*(1-link),np.ones(n)],S)
print('\nS ~ 근거문장수 + 연결광고 + 비연결광고  R²=%.3f (ΔR²=%.3f)'%(r2,r2-base))
b=np.linalg.lstsq(np.c_[vol,linked,share*(1-link),np.ones(n)],S,rcond=None)[0]
print('  계수: 연결 %.3f · 비연결 %.3f'%(b[1],b[2]))
print('\n연결률 분포: 중앙 %.3f 평균 %.3f 최소 %.3f 최대 %.3f'%(np.median(link),link.mean(),link.min(),link.max()))
hi=sorted(zip(link,[f['n'] for f in F]),reverse=True)
print('연결률 상위:',', '.join(f'{x[1]} {x[0]:.2f}' for x in hi[:6]))
print('연결률 하위:',', '.join(f'{x[1]} {x[0]:.2f}' for x in hi[-6:]))
