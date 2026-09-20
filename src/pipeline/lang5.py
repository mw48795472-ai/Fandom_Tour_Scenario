import json,math
d=json.load(open('data10.json',encoding='utf-8'))
SD=d['SIDO']; Fs=d['F']
def build(alpha):
    out={}; mx=0
    for f in Fs:
        rv=f.get('rv') or [0,0,[0]*17]; N=rv[0]; c=rv[2]
        sh=[(c[i]+alpha/17)/(N+alpha) for i in range(17)]
        out[f['n']]=sh
        if N: mx=max(mx,max(sh))
    return out,mx
for a in (10,4.03):
    sh,mx=build(a)
    r=sorted(Fs,key=lambda f:-sh[f['n']][SD.index('경남')])[:5]
    print(f"alpha={a}: RAWMAX={mx:.4f}  경남 top5 " + ', '.join(f"{f['n']} {sh[f['n']][SD.index('경남')]/mx:.3f}" for f in r))
    z=[f for f in Fs if not (f.get('rv') and f['rv'][0])]
    print(f"   지역언급0 팬덤 A값 = {sh[z[0]['n']][0]/mx:.3f} (n={len(z)})   전국균등 LQ=1 지점 A = {(1/17)/mx:.3f}")
# 순위 상관
sh10,m10=build(10); sh4,m4=build(4.03)
import statistics
tot=0;chg=0
for s in SD:
    i=SD.index(s)
    r1=[f['n'] for f in sorted(Fs,key=lambda f:-sh10[f['n']][i])]
    r2=[f['n'] for f in sorted(Fs,key=lambda f:-sh4[f['n']][i])]
    tot+=1
    if r1[:10]!=r2[:10]: chg+=1
print('시도별 상위10 순서가 바뀐 시도 수:',chg,'/',tot)
