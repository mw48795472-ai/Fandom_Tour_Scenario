import json
d=json.load(open('data11.json',encoding='utf-8'))
AF=json.load(open('aff_asym.json',encoding='utf-8'))
idx={n:i for i,n in enumerate(AF['names'])}
SD=d['SIDO']
miss=[f['n'] for f in d['F'] if f['n'] not in idx]
assert not miss, miss
for f in d['F']:
    i=idx[f['n']]
    f['aa']=AF['A'][i]          # 17개 시도 A_sido (세종 null)
    f['lq']=AF['LQ'][i]         # 17개 시도 LQ
d['AFF']={'a':AF['a'],'pi':AF['pi'],'conc':AF['Aconc'],'LQMAX':AF['LQMAX'],
          'na':'세종','method':'비대칭 디리클레-다항 경험베이즈'}
d.pop('ALPHA',None); d.pop('RAWMAX',None)
json.dump(d,open('data12.json','w',encoding='utf-8'),ensure_ascii=False,separators=(',',':'))
print('ok',len(open('data12.json',encoding='utf-8').read()))
