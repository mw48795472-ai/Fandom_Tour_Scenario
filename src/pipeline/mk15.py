import json,math
SD=['서울','부산','대구','인천','광주','대전','울산','세종','경기','강원','충북','충남','전북','전남','경북','경남','제주']
d=json.load(open('data14.json',encoding='utf-8'))
S=json.load(open('show_lq.json',encoding='utf-8')); C=json.load(open('shows_clean.json',encoding='utf-8'))
X=json.load(open('xchan.json',encoding='utf-8'))
pool=set(S['pool']); empty=set(S['empty'])
# 레코드를 아티스트별로
byart={}
for r in C['clean']:
    byart.setdefault(r['artist'],[]).append({k:r[k] for k in ('title','venue','sido','sgg','start','end','n','type','conf','source')})
# 결합 LQ
G=[]
for f in d['F']:
    n=f['n']; slq=S['LQ'].get(n)
    f['slq']=slq
    f['sst']= 'have' if n in byart else ('empty' if n in empty else 'unsearched')
    f['srec']=byart.get(n,[])
    f['sm']=S['M'].get(n)
    comb=[]
    for j in range(17):
        a=f['lq'][j] if f.get('lq') else None
        b=slq[j] if slq else None
        v = math.sqrt(a*b) if (a is not None and b is not None) else (a if a is not None else b)
        comb.append(None if v is None else round(v,4))
        if v is not None: G.append(v)
    f['clq']=comb
mx=max(G)
for f in d['F']:
    f['ca']=[None if v is None else round(min(max(math.log(v)/math.log(mx),0),1),4) for v in f['clq']]
d['SHOWLQ']={'pi':S['pi'],'a':S['a'],'K':S['K'],'SD':SD,'max':S['mx'],'combmax':round(mx,3),
  'have':len(byart),'empty':sorted(empty,key=lambda n:[x['n'] for x in d['F']].index(n)),
  'unsearched':S['unsearched'],'nrec':len(C['clean']),
  'nshow':int(sum(sum(v) for v in S['M'].values())),
  'x':{'r':X['r'],'rho':X['rho'],'agree':X['agree'],'tot':X['tot']},
  'src':'웹 리서치 (2024-01-01 ~ 2026-09-18 국내 공연) · 레코드별 출처 URL 보유',
  'note':'KOPIS 오픈API는 data.go.kr 서비스키 발급이 필요해 이 세션에서 직접 조회하지 못했다. 공식 공연목록이 확보되면 이 행렬을 그대로 대체한다.'}
json.dump(d,open('data16.json','w',encoding='utf-8'),ensure_ascii=False,separators=(',',':'))
print('ok',len(open('data16.json',encoding='utf-8').read()))
print('결합 LQ 최대 %.2f'%mx)
for n in ['송가인','리센느(RESCENE)','이효리','임영웅','BTS','김호중']:
    f=[x for x in d['F'] if x['n']==n][0]
    t=sorted(((f['ca'][j],SD[j]) for j in range(17) if f['ca'][j] is not None),reverse=True)[:3]
    print(f"  {n:>16} [{f['sst']}] " + ' · '.join(f'{s} {v:.3f}' for v,s in t))
