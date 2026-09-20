import csv,json,math,numpy as np
P='/root/.claude/uploads/453213c1-28c6-5903-952e-90318dd79866/ffdec037-ad_commercial_index_v7.csv'
rows=[r for r in csv.DictReader(open(P,encoding='utf-8-sig')) if r.get('팬덤')]
IND=['건강/의료','식음료','가정/생활','금융','자동차','미용','스포츠/레저','정보/통신','여행','비즈니스/산업','쇼핑','엔터테인먼트','복지/행정','부동산','교육','게임','패션/의류','뉴스','도서/참고자료','기타']
A={}
for r in rows:
    c=[int(r[i]) for i in IND]
    A[r['팬덤']]={'cat':r['구분'],'a':int(r['근거문장수']),'ad':int(r['광고성문장수']),
      'share':float(r['광고비중']),'top':r['대표업종'],'c':c}
print('n=',len(A))
ok1=sum(1 for v in A.values() if abs(v['share']-v['ad']/v['a'])<0.0006)
ok2=sum(1 for v in A.values() if v['ad']==sum(v['c']))
ok3=sum(1 for v in A.values() if (not v['top'] and sum(v['c'])==0) or (v['top'] and v['c'][IND.index(v['top'])]==max(v['c'])))
print('광고비중=광고성/근거',ok1,' 광고성=열합계',ok2,' 대표업종=최대열',ok3)
bad=[(k,v['ad'],sum(v['c'])) for k,v in A.items() if v['ad']!=sum(v['c'])]
print('불일치:',bad[:10])
json.dump({'IND':IND,'A':A},open('ad_v7.json','w',encoding='utf-8'),ensure_ascii=False)
# 풀 분포
tot=np.array([sum(v['c'][i] for v in A.values()) for i in range(20)],float)
print('\n전체 광고 업종 분포 (건수 / 점유)')
for i,n in sorted(enumerate(IND),key=lambda t:-tot[t[0]]):
    print(f"  {n:>12} {int(tot[i]):>4}  {tot[i]/tot.sum()*100:5.2f}%")
print('총 광고성 문장', int(tot.sum()))
