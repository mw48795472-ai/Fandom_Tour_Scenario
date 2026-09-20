import json
d=json.load(open('data12.json',encoding='utf-8'))
PR=json.load(open('ad_prof.json',encoding='utf-8'))
NO=json.load(open('ad_norm.json',encoding='utf-8'))
AD=json.load(open('ad_v7.json',encoding='utf-8'))
IND=NO['IND']; gi=IND.index('복지/행정')
for f in d['F']:
    n=f['n']; p=PR['prof'][n]; a=AD['A'][n]
    order=sorted(range(20),key=lambda i:-NO['ind20'][n]['lq'][i])
    tg=[[IND[i],NO['ind20'][n]['lq'][i],a['c'][i]] for i in order if a['c'][i]>0][:3]
    f['ad']={'C':NO['C'][n]['C'],'sh':NO['C'][n]['sh'],'n':a['ad'],'tot':a['a'],
             'raw':round(a['share'],4),'top':a['top'],'w':p['w'],'lq':p['lq'],'cnt':p['n'],
             'gov':[NO['ind20'][n]['lq'][gi],a['c'][gi]],'tg':tg,'cat':a['cat']}
# 해외확산도 가중치 재조정: ΔR² 기준 (0.008 vs 0.049), 팬덤특성 항 예산 0.10
old=d['LGW']; cap_old=0.08; cap_new=0.014
d['LGW']={k:round(v/cap_old*cap_new,4) for k,v in old.items()}
d['LGMETA']['CAP']=cap_new; d['LGMETA']['CAP_OLD']=cap_old
d['ADM']={'MAP':PR['MAP'],'pi5':PR['pi'],'K5':PR['K'],'a5':PR['a'],'cov':PR['cov'],
          'pi20':NO['pi20'],'K20':NO['K20'],'IND':IND,
          'Cm':NO['Cm'],'Ca':NO['Ca'],'Cmax':NO['Cmax'],'WC':0.086,
          'dR2':{'광고비중':0.049,'해외비중':0.008,'광고업종수':0.036},
          'pr':{'광고비중':0.512,'해외비중':-0.203},'base':0.813}
json.dump(d,open('data13.json','w',encoding='utf-8'),ensure_ascii=False,separators=(',',':'))
print('ok',len(open('data13.json',encoding='utf-8').read()))
print(json.dumps(d['LGW'],ensure_ascii=False))
print(json.dumps(d['F'][0]['ad'],ensure_ascii=False))
