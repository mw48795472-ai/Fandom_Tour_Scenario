import json,math,numpy as np
d=json.load(open('data12.json',encoding='utf-8')); AD=json.load(open('ad_v7.json',encoding='utf-8'))
A,IND=AD['A'],AD['IND']; F=d['F']
def pear(x,y):
    x=np.array(x,float);y=np.array(y,float)
    return float(np.corrcoef(x,y)[0,1])
def part(x,y,z):
    rxy,rxz,ryz=pear(x,y),pear(x,z),pear(y,z)
    den=math.sqrt((1-rxz**2)*(1-ryz**2)); return (rxy-rxz*ryz)/den if den else 0
vol=[A[f['n']]['a'] for f in F]
FN=['F1 팬덤결속','F2 직접소비','F3 현장경제','F4 산업전이','F5 대중글로벌확산']
outs=[('파급효과 S',lambda f:f['S']),('충성도 L',lambda f:f['L'])]+[(FN[i],(lambda i: (lambda f: f['f'][i] if f.get('f') else None))(i)) for i in range(5)]
adv=[('광고비중',lambda v:v['share']),('광고성문장수',lambda v:v['ad']),
     ('광고 업종수',lambda v:sum(1 for x in v['c'] if x>0)),
     ('복지/행정 건수',lambda v:v['c'][IND.index('복지/행정')]),
     ('복지/행정 점유',lambda v:(v['c'][IND.index('복지/행정')]/sum(v['c'])) if sum(v['c']) else 0),
     ('상업5영역 점유',lambda v:(sum(v['c'][IND.index(i)] for i in ['식음료','쇼핑','패션/의류','미용','스포츠/레저','엔터테인먼트','여행'])/sum(v['c'])) if sum(v['c']) else 0)]
print(f"{'':>14}"+''.join(f"{n:>17}" for n,_ in outs))
for an,af in adv:
    xs=[af(A[f['n']]) for f in F]
    line=f"{an:>14}"
    for on,of in outs:
        idx=[i for i,f in enumerate(F) if of(f) is not None]
        xs2=[xs[i] for i in idx]; ys=[of(F[i]) for i in idx]; v2=[vol[i] for i in idx]
        line+=f"  {pear(xs2,ys):+.3f}/{part(xs2,ys,v2):+.3f}"
    print(line)
print("\n(원상관 / 근거문장수 통제 후 편상관)  n=100")
