import json
d=json.load(open('data16.json',encoding='utf-8'))
AD=json.load(open('ad_v7.json',encoding='utf-8')); A,IND=AD['A'],AD['IND']
VL=json.load(open('vlm.json',encoding='utf-8')); A5=VL['A5']
MAP={'식음료':'음식','쇼핑':'관광/쇼핑','패션/의류':'관광/쇼핑','미용':'관광/쇼핑',
     '스포츠/레저':'레저활동','엔터테인먼트':'공연/전시','여행':'숙박'}
for f in d['F']:
    c=A[f['n']]['c']; tot=sum(c) or 1
    w=[0.0]*5; cnt=[0]*5
    for i,ind in enumerate(IND):
        if ind in MAP:
            j=A5.index(MAP[ind]); w[j]+=c[i]/tot; cnt[j]+=c[i]
    unl=[[IND[i],c[i]] for i in range(20) if IND[i] not in MAP and c[i]>0]
    unl.sort(key=lambda x:-x[1])
    f['adx']={'w':[round(x,4) for x in w],'cnt':cnt,'link':round(sum(w),4),
              'tot':tot,'unl':unl[:5],'unlsum':tot-sum(cnt)}
d['VLM']={'A5':A5,'V':VL['V'],'REG':VL['REG'],'NAT':VL['NAT'],'NATTOT':VL['NATTOT'],'year':VL['year'],
  'MAP':MAP,
  'test':{'share':{'pr':0.512,'dr':0.049},'link':{'pr':-0.136,'dr':0.003},
          'linked':{'pr':0.307,'dr':0.018},'unlinked':{'pr':0.458,'dr':0.039},'both':0.050,'base':0.813},
  'note':'광고 강도를 관광소비 연결률로 깎는 안은 검정이 지지하지 않았다 — 연결분(ΔR² +0.018)보다 비연결분(+0.039)이 파급효과를 더 설명한다. 그래서 상업유발도 C의 정의는 그대로 두고, 광고가 실제로 어느 소비영역에 얼마를 겨냥하는지는 소비액으로 따로 표기한다.'}
json.dump(d,open('data17.json','w',encoding='utf-8'),ensure_ascii=False,separators=(',',':'))
print('ok',len(open('data17.json',encoding='utf-8').read()))
for n in ['리센느(RESCENE)','임영웅','BTS','이효리','조용필']:
    f=[x for x in d['F'] if x['n']==n][0]; x=f['adx']
    print(f"  {n:>16} 연결률 {x['link']:.2f} · 태그 {x['tot']}  영역 {dict(zip(A5,x['cnt']))}  비연결 {x['unl'][:3]}")
