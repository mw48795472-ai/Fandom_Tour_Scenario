import csv,json,math
P='/root/.claude/uploads/453213c1-28c6-5903-952e-90318dd79866/89f4a8fe-worldwide_language_index_v7.csv'
rows=[r for r in csv.DictReader(open(P,encoding='utf-8-sig')) if r.get('팬덤')]
LANGS=['한국어','영어','일본어','중국어','스페인어','프랑스어','태국어','인도네시아어','베트남어','러시아어','필리핀어','포르투갈어','튀르키예어','아랍어']
L={}
for r in rows:
    c=[int(r[l]) for l in LANGS]
    L[r['팬덤']]=dict(a=int(r['근거문장수']),N=int(r['총언어언급']),K=int(r['검출언어수']),
        div=float(r['언어다양성']),ov=int(r['해외근거문장수']),ovs=float(r['해외비중']),
        oK=int(r['검출해외언어수']),odiv=float(r['해외언어다양성']),top=r['대표해외언어'],
        tops=float(r['대표해외언어비중']),c=c)
json.dump(L,open('lang_v7.json','w',encoding='utf-8'),ensure_ascii=False)
print(len(L))
# identity checks
ok1=sum(1 for k,v in L.items() if v['N']==v['a'])
ok2=sum(1 for k,v in L.items() if v['N']==sum(v['c']))
ok3=sum(1 for k,v in L.items() if abs(v['ovs']-v['ov']/v['N'])<0.002)
ok4=sum(1 for k,v in L.items() if v['ov']==sum(v['c'][1:]))
ok5=sum(1 for k,v in L.items() if v['oK']==sum(1 for x in v['c'][1:] if x>0))
ok6=sum(1 for k,v in L.items() if v['K']==sum(1 for x in v['c'] if x>0))
print('N==근거문장수',ok1,'N==sum',ok2,'해외비중',ok3,'해외=비한국어합',ok4,'oK',ok5,'K',ok6)
# 언어다양성 = ? test K/14, shannon
import statistics
def sh(c):
    N=sum(c)
    if N==0: return 0
    ps=[x/N for x in c if x>0]
    return -sum(p*math.log(p) for p in ps)/math.log(len(c))
t1=sum(1 for k,v in L.items() if abs(v['div']-v['K']/14)<0.002)
t2=sum(1 for k,v in L.items() if abs(v['div']-sh(v['c']))<0.002)
t3=sum(1 for k,v in L.items() if abs(v['div']-(1-sum((x/v['N'])**2 for x in v['c'])))<0.002)
print('div=K/14',t1,'div=shannon14',t2,'div=gini',t3)
def sh2(c,n):
    N=sum(c)
    if N==0 or n<2: return 0
    ps=[x/N for x in c if x>0]
    return -sum(p*math.log(p) for p in ps)/math.log(n)
t4=sum(1 for k,v in L.items() if abs(v['odiv']-sh2(v['c'][1:],13))<0.003)
t5=sum(1 for k,v in L.items() if abs(v['odiv']-sh2(v['c'][1:],v['oK']))<0.003)
print('odiv=shannon13',t4,'odiv=shannon/oK',t5)

d=json.load(open('data10.json',encoding='utf-8'))
Fs=d['F']
def pear(x,y):
    n=len(x); mx=sum(x)/n; my=sum(y)/n
    sx=math.sqrt(sum((a-mx)**2 for a in x)); sy=math.sqrt(sum((b-my)**2 for b in y))
    return sum((a-mx)*(b-my) for a,b in zip(x,y))/(sx*sy) if sx and sy else 0
def rank(v):
    s=sorted(range(len(v)),key=lambda i:v[i]); r=[0]*len(v)
    i=0
    while i<len(s):
        j=i
        while j+1<len(s) and v[s[j+1]]==v[s[i]]: j+=1
        avg=(i+j)/2+1
        for k in range(i,j+1): r[s[k]]=avg
        i=j+1
    return r
def spear(x,y): return pear(rank(x),rank(y))
print('\n--- 언어지표 vs 기존 성과지표 (n=100) ---')
langvars={'해외비중':lambda v:v['ovs'],'검출언어수':lambda v:v['K'],'언어다양성':lambda v:v['div'],
  '해외언어다양성':lambda v:v['odiv'],'검출해외언어수':lambda v:v['oK'],'해외근거문장수':lambda v:v['ov'],
  '대표해외언어비중':lambda v:v['tops'],'근거문장수':lambda v:v['a']}
outs={'파급효과 S':lambda f:f['S'],'충성도 L':lambda f:f['L'],'D':lambda f:f['D'],'cv':lambda f:f['cv']}
print(f"{'':>16}"+''.join(f"{k:>14}" for k in outs))
for ln,lf in langvars.items():
    xs=[lf(L[f['n']]) for f in Fs]
    line=f"{ln:>16}"
    for on,of in outs.items():
        ys=[of(f) for f in Fs]
        line+=f"  r={pear(xs,ys):+.3f}/ρ={spear(xs,ys):+.3f}"
    print(line)

print('\n--- 근거문장수(코퍼스 분량) 통제 후 편상관 ---')
def partial(x,y,z):
    rxy,rxz,ryz=pear(x,y),pear(x,z),pear(y,z)
    den=math.sqrt((1-rxz**2)*(1-ryz**2))
    return (rxy-rxz*ryz)/den if den else 0
vol=[L[f['n']]['a'] for f in Fs]
for ln,lf in langvars.items():
    if ln=='근거문장수': continue
    xs=[lf(L[f['n']]) for f in Fs]
    out=[]
    for on,of in outs.items():
        ys=[of(f) for f in Fs]
        out.append(f"{on} r·z={partial(xs,ys,vol):+.3f}")
    print(f"{ln:>16}  "+'  '.join(out))
print('\n--- 4구획별 해외비중 평균 ---')
from collections import defaultdict
g=defaultdict(list)
for f in Fs: g[f['q']].append(L[f['n']])
for k,v in sorted(g.items(),key=lambda t:-len(t[1])):
    print(f"{k:>8} n={len(v):>3}  해외비중 {sum(x['ovs'] for x in v)/len(v):.3f}  검출언어수 {sum(x['K'] for x in v)/len(v):.1f}  근거문장수 {sum(x['a'] for x in v)/len(v):.0f}")
print('\n--- 페르소나별 ---')
g=defaultdict(list)
for f in Fs:
    if f.get('p'): g[f['p']].append(L[f['n']])
for k,v in sorted(g.items(),key=lambda t:-len(t[1])):
    print(f"{k:>8} n={len(v):>3}  해외비중 {sum(x['ovs'] for x in v)/len(v):.3f}  해외언어다양성 {sum(x['odiv'] for x in v)/len(v):.3f}  검출해외언어수 {sum(x['oK'] for x in v)/len(v):.1f}")
