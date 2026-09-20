import re,json
A='/tmp/claude-0/-home-claude/453213c1-28c6-5903-952e-90318dd79866/scratchpad/artifact-files/'
h=open(A+'f23c02c5-8586-4265-bcf7-8e333b117b26/index.html',encoding='utf-8').read()
rows=json.loads(re.search(r'const payload = (\{.*?\});',h,re.S).group(1))['rows']
h2=open(A+'654cb2c0-3558-4856-b92a-8a3f35dc9876/index.html',encoding='utf-8').read()
pf=json.loads(re.search(r'const DATA = (\{.*?\});',h2,re.S).group(1))['pca']['fandoms']
pmap={x['name']:x for x in pf}

F=[]
for r in rows:
    p=pmap.get(r['fandom'])
    F.append({
      'n':r['fandom'],'c':r['category'],'L':r['loyalty'],'S':r['spillover'],
      'D':r['diversity'],'cv':r['coverage'],'a':r['activity'],'q':r['quadrant'],
      'p':(p['persona'] if p else None),
      'f':([round(p['shares']['F%d'%i],4) for i in range(1,6)] if p else None)
    })

# 표 15 지역 언급 상위 20
REG={
 '싸이':['강원',0.20,0.59],'이승철':['서울',0.13,0.53],'임영웅':['서울',0.21,0.71],
 '송가인':['전남',0.74,0.35],'박서진':['서울',0.21,0.65],'악동뮤지션':['서울',0.33,0.53],
 '김연자':['광주',0.33,0.47],'나훈아':['서울',0.35,0.47],'조용필':['서울',0.30,0.35],
 '리센느(RESCENE)':['경남',0.58,0.29],'이영지':['서울',0.39,0.59],'다이나믹듀오':['서울',0.28,0.35],
 '영탁':['서울',0.33,0.41],'지드래곤 (G-Dragon)':['서울',0.47,0.23],'BTS':['서울',0.47,0.29],
 'god':['서울',0.50,0.23],'젝스키스':['부산',0.53,0.29],'로이킴':['서울',0.53,0.35],
 '김호중':['경북',0.43,0.35],'엄정화':['부산',0.36,0.18]}
# 표 16 (확실히 판독된 행만)
LANG={'BTS':[0.60,['영어 53%','스페인어 12%','일본어 11%'],0.66],
 'BLACKPINK':[0.69,['영어 41%','중국어 11%','스페인어 11%'],0.77],
 'Stray Kids':[0.79,['영어 59%','스페인어 9%','일본어 7%'],0.60],
 'TWICE':[0.61,['영어 38%','일본어 22%','중국어 17%'],0.70],
 'SEVENTEEN':[0.71,['영어 68%','중국어 9%','일본어 5%'],0.50],
 'NewJeans':[0.70,['영어 59%','중국어 11%','스페인어 8%'],0.59],
 'LE SSERAFIM':[0.62,['영어 49%','중국어 11%','일본어 11%'],0.72]}
MCI={'FTISLAND':0.660,'동방신기':0.512,'CNBLUE':0.504,'CORTIS':0.459,'빅뱅':0.364,
 '소녀시대':0.134,'워너원':0.123,'EXO':0.122,'SEVENTEEN':0.112,'NCT':0.111}
for f in F:
    n=f['n']
    if n in REG: f['r']=REG[n]
    if n in LANG: f['lg']=LANG[n]
    if n in MCI: f['m']=MCI[n]

# POI
hm=open('/mnt/user-data/uploads/RESCENE_Route__standalone_.html',encoding='utf-8').read().replace('\\u002F','/')
objs=re.findall(r"\{(?:n:\d+,)?id:'[a-z0-9]+',[^{}]*?cat:'[a-z]+',[^{}]*?\}",hm)
CITY={'na1':'suwon','na22':'suwon','na23':'suwon','na2':'suwon','na3':'suwon','nax1':'suwon',
 'na4':'jeongseon','na5':'jeongseon','nax2':'jeongseon','nax3':'jeongseon',
 'na6':'daejeon','nax4':'daejeon','nax5':'daejeon',
 'na8':'chungju','na9':'chungju','nax6':'chungju','nax7':'chungju',
 'na10':'donghae','na11':'donghae','nax8':'donghae','nax9':'donghae','nax10':'donghae',
 'nax11':'donghae','nax12':'donghae','nax14':'donghae','nax15':'donghae','nax16':'donghae'}
P=[]
for o in objs:
    g=lambda k:(re.search(k+r":\s*'([^']*)'",o) or re.search(k+r':\s*"([^"]*)"',o))
    d={k:(g(k).group(1) if g(k) else '') for k in ['id','ko','en','cat','srcKo','hrs']}
    for k in ['lat','lng','min']:
        mm=re.search(k+r":\s*(-?[\d.]+)",o); d[k]=float(mm.group(1)) if mm else 0
    mm=re.search(r"bKo:\s*'([^']*)'",o) or re.search(r'bKo:\s*"([^"]*)"',o)
    d['b']=mm.group(1) if mm else ''
    i=d['id']
    d['city']='gyeongju' if i.startswith('gj') else 'geoje' if i.startswith('gz') else CITY.get(i)
    if not d['city']: continue
    d['min']=int(d['min'])
    P.append({'id':d['id'],'ci':d['city'],'k':d['ko'],'c':d['cat'],'t':d['min'],
              'h':d['hrs'],'s':d['srcKo'],'b':d['b'],'la':d['lat'],'ln':d['lng']})

# STAYS
st=re.findall(r"\{id:'s[a-z0-9]+',[^{}]*typeKo:'[^']*'\}",hm)
S=[]
CS={'sg':'gyeongju','sz':'geoje','sd':'donghae','sj':'jeongseon','ss':'suwon','sc':'chungju','sn':'daejeon'}
for o in st:
    g=lambda k:re.search(k+r":\s*'([^']*)'",o)
    d={k:(g(k).group(1) if g(k) else '') for k in ['id','ko','areaKo','price','typeKo']}
    la=re.search(r"lat:\s*([\d.]+)",o); ln=re.search(r"lng:\s*([\d.]+)",o)
    pre=d['id'][:2]
    S.append({'id':d['id'],'ci':CS.get(pre,'etc'),'k':d['ko'],'a':d['areaKo'],'p':d['price'],'t':d['typeKo'],
              'la':float(la.group(1)),'ln':float(ln.group(1))})
print('stay cities',sorted({s['ci'] for s in S}), len(S))
for s in S: print(s['id'],s['ci'],s['k'])
out={'F':F,'P':P,'S':S}
open('data.json','w',encoding='utf-8').write(json.dumps(out,ensure_ascii=False,separators=(',',':')))
print('poi',len(P),'fandom',len(F))
import collections; print(collections.Counter(p['ci'] for p in P))
