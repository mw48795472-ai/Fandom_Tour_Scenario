import json,csv,math
SD=['서울','부산','대구','인천','광주','대전','울산','세종','경기','강원','충북','충남','전북','전남','경북','경남','제주']
rows=[x for x in csv.DictReader(open('/root/.claude/uploads/453213c1-28c6-5903-952e-90318dd79866/5a233e5f-domestic_regional_index_v7.csv',encoding='utf-8-sig')) if x.get('팬덤')]
A=4.03
D=[]
for x in rows:
    c=[int(x[s]) for s in SD]; N=int(x['총지역언급']); K=int(x['검출지역수'])
    D.append({'n':x['팬덤'],'c':c,'N':N,'K':K})
sh=lambda d,i:(d['c'][i]+A/17)/(d['N']+A)
mx=max(sh(d,d['c'].index(max(d['c']))) for d in D if d['N'])
top=[d for d in D if d['N'] and sh(d,d['c'].index(max(d['c'])))==mx][0]
print('raw_max %.4f (%s · %s)'%(mx,top['n'],SD[top['c'].index(max(top['c']))]))
RANK=[]
for d in D:
    if not d['N']: continue
    i=d['c'].index(max(d['c'])); s=sh(d,i)
    RANK.append([d['n'],SD[i],d['c'][i],d['N'],d['K'],round(s*17,2),round(s/mx,3)])
RANK.sort(key=lambda r:-r[6]); RANK=RANK[:20]
CONC=[]
for i,s in enumerate(SD):
    vals=sorted(((sh(d,i)/mx,d['n']) for d in D),reverse=True)
    tot=sum(v for v,_ in vals)
    rep=sum(1 for d in D if d['N'] and d['c'].index(max(d['c']))==i)
    det=sum(1 for d in D if d['c'][i]>0)
    CONC.append([s,rep,det,round(vals[0][0]/tot*100,1),round(sum(v for v,_ in vals[:5])/tot*100,1),vals[0][1],round(vals[0][0],3)])
print(json.dumps(RANK,ensure_ascii=False)[:200])
for r in CONC: print(r)
zero=[d for d in D if not d['N']]
print('A for zero-mention:',round((A/17)/(0+A)/mx,3),'n=',len(zero))
json.dump({'RANK':RANK,'CONC':CONC,'mx':round(mx,4)},open('regen403.json','w',encoding='utf-8'),ensure_ascii=False)
# 예시표 값
for name,reg in [('송가인','전남'),('리센느(RESCENE)','경남'),('여자친구','서울'),('GOT7','서울'),('투어스(TWS)','서울'),('리센느(RESCENE)','경북')]:
    d=[x for x in D if x['n']==name][0]; i=SD.index(reg); s=sh(d,i)
    print(f"{name} {reg}: {d['c'][i]}/{d['N']} 관측{(d['c'][i]/d['N']*100 if d['N'] else 0):.1f}% 축소{s*100:.1f}% LQ{s*17:.2f} A{s/mx:.3f}")
