import csv,json
P='/root/.claude/uploads/453213c1-28c6-5903-952e-90318dd79866/e4af4862-___2025_____LQ_EQ.csv'
rows=list(csv.DictReader(open(P,encoding='utf-8-sig')))
A5=['음식','관광/쇼핑','레저활동','공연/전시','숙박']
V={}; REG={}; NAT={}
for r in rows:
    sd=r['가맹점광역시도']; a=r['소비영역']
    V.setdefault(sd,{})[a]=float(r['VLM'])
    REG[sd]=float(r['지역전체소비']); NAT[a]=float(r['전국영역소비'])
NATTOT=float(rows[0]['전국전체소비'])
print('시도',len(V))
print('전국 소비영역별 (조원) ', {a:round(NAT[a]/1e12,1) for a in A5})
print('전국 전체 %.1f조 · 5영역 합 %.1f조 (%.1f%%)'%(NATTOT/1e12,sum(NAT.values())/1e12,sum(NAT.values())/NATTOT*100))
print('\n지역전체소비 상위')
for sd,v in sorted(REG.items(),key=lambda x:-x[1])[:6]:
    print(f'  {sd:>3} {v/1e12:7.1f}조  전국 대비 {v/NATTOT*100:5.2f}%')
print('\n영역별 전국 대비 지역 점유 상위')
for a in A5:
    t=sorted(((V[sd].get(a,0)/NAT[a],sd) for sd in V),reverse=True)[:3]
    print(f'  {a:>7} ' + ' · '.join(f'{s} {v*100:.1f}%' for v,s in t))
json.dump({'A5':A5,'V':{sd:[V[sd].get(a,0.0) for a in A5] for sd in V},
           'REG':REG,'NAT':[NAT[a] for a in A5],'NATTOT':NATTOT,'year':rows[0]['연도']},
          open('vlm.json','w',encoding='utf-8'),ensure_ascii=False)
