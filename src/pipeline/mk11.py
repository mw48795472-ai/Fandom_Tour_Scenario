import json
d=json.load(open('data10.json',encoding='utf-8'))
LF=json.load(open('lang_final.json',encoding='utf-8'))
d['ALPHA']=4.03
d['LG']=LF['lang']; d['LGW']=LF['W']
d['LGMETA']={'AL':LF['AL'],'M0':LF['M0'],'ALG':LF['ALG'],'GMAX':LF['GMAX'],'CAP':0.08,
             'means':LF['means'],'base':0.15,
             'pr':{'해외비중':-0.203,'검출언어수':-0.145,'언어다양성':-0.182,'해외언어다양성':-0.145,'해외근거문장수':-0.226},
             'r0':{'해외비중':0.359,'검출언어수':0.446,'언어다양성':0.374,'해외언어다양성':0.310,'해외근거문장수':0.709},
             'vol':0.902}
for f in d['F']:
    f.pop('lg',None)
    g=LF['lang'].get(f['n'])
    f['lg']=[g['G'],[x[0] for x in g['tg']],g['odiv']] if g else None
# RAWMAX recompute
SIDO=d['SIDO']; a=d['ALPHA']; mx=0
for f in d['F']:
    rv=f.get('rv')
    if not rv or not rv[0]: continue
    c=rv[2]; i=c.index(max(c)); v=(c[i]+a/17)/(rv[0]+a)
    mx=max(mx,v)
d['RAWMAX']=round(mx,4)
json.dump(d,open('data11.json','w',encoding='utf-8'),ensure_ascii=False,separators=(',',':'))
print('RAWMAX',d['RAWMAX'],'ALPHA',d['ALPHA'],'size',len(open('data11.json',encoding='utf-8').read()))
