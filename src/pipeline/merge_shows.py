import csv,json,os,re
SD=['서울','부산','대구','인천','광주','대전','울산','세종','경기','강원','충북','충남','전북','전남','경북','경남','제주']
d=json.load(open('data14.json',encoding='utf-8')); NAMES=[f['n'] for f in d['F']]
BATCH={1:NAMES[0:10],2:NAMES[10:20],3:NAMES[20:30],4:NAMES[30:40],5:NAMES[40:50],
       6:NAMES[50:60],7:NAMES[60:70],8:NAMES[70:80],9:NAMES[80:90],10:NAMES[90:100],
       11:['소녀시대','이효리','잭스키스','브라운아이즈']}
rows=[];bad=[]
for i in list(range(1,12)):
    p=f'shows/b{i}.tsv'
    if not os.path.exists(p): continue
    for r in csv.DictReader(open(p,encoding='utf-8'),delimiter='\t'):
        if not r.get('artist'): continue
        r['_b']=i; rows.append(r)
print('원시 레코드',len(rows))
# 검증
seen=set()
clean=[]
for r in rows:
    a=r['artist'].strip()
    if a not in NAMES: bad.append(('unknown artist',a)); continue
    if a not in BATCH[r['_b']]: bad.append(('wrong batch',a,r['_b'])); continue
    sd=r['sido'].strip()
    if sd not in SD: bad.append(('bad sido',a,sd)); continue
    if not r['source'].strip().startswith('http'): bad.append(('no source',a,r['title'][:20])); continue
    for k in ('start','end'):
        v=r[k].strip()
        if v and not re.fullmatch(r'\d{4}-\d{2}-\d{2}',v): bad.append(('bad date',a,v)); r[k]=''
    if r['start'] and not ('2024-01-01'<=r['start']<='2026-09-18'): bad.append(('out of range',a,r['start'])); continue
    if r['conf'].strip() not in ('A','B','C'): r['conf']='C'
    key=(a,r['title'].strip(),sd,r['start'].strip())
    if key in seen: bad.append(('dup',a,r['title'][:24])); continue
    seen.add(key)
    n=r['n'].strip()
    r['n']=int(n) if n.isdigit() and int(n)>0 else 1
    r['artist']=a; r['sido']=sd
    clean.append(r)
print('검증 통과',len(clean),' 제외',len(bad))
from collections import Counter
print('제외 사유',Counter(b[0] for b in bad))
for b in bad[:12]: print('  ',b)
COLS=['artist','title','venue','sido','sgg','start','end','n','type','conf','source']
with open('/home/claude/artist_show_history_v1.csv','w',encoding='utf-8-sig',newline='') as fp:
    w=csv.DictWriter(fp,fieldnames=COLS,extrasaction='ignore'); w.writeheader()
    for r in sorted(clean,key=lambda x:(NAMES.index(x['artist']),x['start'] or '9999')): w.writerow(r)
have=sorted({r['artist'] for r in clean},key=NAMES.index)
miss=[n for n in NAMES if n not in have]
print('\n수집된 아티스트',len(have),' 미수집',len(miss))
print('미수집:',', '.join(miss))
json.dump({'clean':clean,'have':have,'miss':miss},open('shows_clean.json','w',encoding='utf-8'),ensure_ascii=False)
