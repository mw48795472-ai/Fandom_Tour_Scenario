import json
d=json.load(open('data13.json',encoding='utf-8'))
S=json.load(open('shows.json',encoding='utf-8'))
d['SHOW']=S['SHOW']; d['SHOWD']=S['DUMMY']
# 아티스트별 집계
agg={}
for r in S['SHOW']:
    a=agg.setdefault(r['f'],{'n':0,'shows':0,'sd':{},'sg':{}})
    a['n']+=1; a['shows']+=r['n']
    a['sd'][r['sd']]=a['sd'].get(r['sd'],0)+r['n']
    a['sg'][r['sd']+'/'+r['sg']]=a['sg'].get(r['sd']+'/'+r['sg'],0)+r['n']
d['SHOWAGG']=agg
d['SHOWMETA']={
 'src':'공연예술통합전산망(KOPIS) 공연목록·공연통계',
 'have':len(agg),'tot':len(d['F']),
 'need':[['아티스트 × 17개 시도 공연 건수·상연 회차','KOPIS 공연목록을 기간·지역으로 조회한 뒤 공연명을 100개 아티스트명과 매칭','미수집'],
         ['지역별 공연건수 전국 분포','공연 LQ의 기저 π. KOPIS 공연통계 지역별 집계','미수집'],
         ['공연시설 정확 좌석수','현재 규모 구간(XL/L/M/S)만 등록','부분 수집']],
 'note':'현재 등록된 공연 이력은 결과보고서 4장 DID 분석 대상 6건뿐이다. 100개 아티스트 전체의 공연 행렬과 전국 기저가 확보돼야 공연 LQ를 산출할 수 있고, 그 전까지는 개최 이력과 실측 성과만 표기한다.'}
json.dump(d,open('data14.json',encoding='utf-8' if False else 'w',encoding2=None) if False else open('data14.json','w',encoding='utf-8'),ensure_ascii=False,separators=(',',':'))
print('ok',len(open('data14.json',encoding='utf-8').read()))
print(json.dumps(agg,ensure_ascii=False))
