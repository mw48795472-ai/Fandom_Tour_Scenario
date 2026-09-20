import json,math,re
D=json.load(open('docdata.json',encoding='utf-8'))
LGD=json.load(open('lang_final.json',encoding='utf-8'))['lang']
src=open('/home/claude/affinity-redesign.html',encoding='utf-8').read()
style=src[src.index('<style>'):src.index('</style>')+8]
SD=['서울','부산','대구','인천','광주','대전','울산','세종','경기','강원','충북','충남','전북','전남','경북','경남','제주']
J=lambda o: json.dumps(o,ensure_ascii=False,separators=(',',':'))

corr=[['해외비중','해당 팬덤 근거문장 중 한국어가 아닌 비율',0.359,-0.203],
      ['검출언어수','언급이 한 건이라도 잡힌 언어 종 수 (14종 중)',0.446,-0.145],
      ['언어다양성','14개 언어 분포의 정규화 섀넌 엔트로피',0.374,-0.182],
      ['해외언어다양성','한국어 제외 13종 분포의 정규화 엔트로피',0.310,-0.145],
      ['해외근거문장수','해외 언어 근거문장 절대 건수',0.709,-0.226],
      ['대표해외언어비중','가장 많이 잡힌 해외 언어 1종의 점유',-0.192,0.141]]

persona=[['글로벌투어형',40,0.509,0.080],['원정소비형',17,0.491,0.077],
         ['현장상업형',31,0.321,0.051],['집단동원형',9,0.190,0.030]]

head=f'''<title>언어지수 검증과 정규화</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Gothic+A1:wght@500;700;800;900&family=Noto+Sans+KR:wght@400;500;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet">
{style}
<style>
.badrow td:first-child{{ color:var(--bad); }}
.wt{{ display:inline-block; min-width:52px; }}
</style>
'''

def tbl(head,rows,cls=''):
    h=''.join(f'<th>{c}</th>' for c in head)
    def cell(c):
        if isinstance(c,str) and c.startswith('@'):
            return '<td class="mono">'+c[1:]+'</td>'
        return '<td>'+str(c)+'</td>'
    b=''.join('<tr>'+''.join(cell(c) for c in r)+'</tr>' for r in rows)
    return f'<div class="tablewrap"><table class="{cls}"><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table></div>'

body=f'''
<div class="wrap">

<header class="masthead">
  <p class="kicker">팬덤루트랩 · RegionFit 개정 보고 · v0.6</p>
  <h1>언어는 규모를 예측하지<br>못했다 — 보조지표로 내린다</h1>
  <p class="deck">전 세계 언어지수 v7 실측을 RegionFit에 넣기 전에, 먼저 <b>이 지표가 관광수요와 상관이 있는지</b>부터 검정했습니다. 원상관은 <span class="mono">r = +0.36</span>으로 보이지만 <b>근거문장수(코퍼스 분량)를 통제하면 −0.15 ~ −0.23으로 사라집니다.</b> 언어 확산은 규모가 아니라 <b>구성</b>을 알려주는 지표였습니다. 가중치를 0.150에서 0.030~0.080으로 내리고, 같은 경험베이즈 정규화를 연고밀착도에도 병행 적용했습니다.</p>
  <div class="docmeta">
    <div><b>작성</b><span>팀 데이터오름 · 서목원</span></div>
    <div><b>일자</b><span class="mono">2026-09-18</span></div>
    <div><b>원천</b><span>전 세계 언어지수 v7 · 100 × 14 행렬</span></div>
    <div><b>적용</b><span>팬덤루트랩 스튜디오 v15</span></div>
  </div>
</header>

<section>
  <div class="sechead"><span class="secnum">00</span><h2>요약</h2></div>
  <div class="thesis">
    <span class="lab">Result</span>
    <p class="big">"다양한 언어권에서 주목받는다"는 신호는 <span class="em">근거 코퍼스가 크다는 사실의 부산물</span>이었습니다. 분량을 통제하면 파급효과와의 상관이 0 또는 음(−)으로 바뀝니다. 그래서 점수를 <span class="em">올리는 근거로는 쓰지 않고</span>, 어느 언어권을 대상으로 설계할지 알려주는 <span class="em">보조지표</span>로 재배치했습니다.</p>
  </div>
  <div class="stats">
    <div><span class="v mono">+0.36 → −0.20</span><span class="k">해외비중 ↔ 파급효과<br>(분량 통제 전 → 후)</span></div>
    <div><span class="v mono">0.150 → 0.030~0.080</span><span class="k">언어 항 가중치</span></div>
    <div><span class="v mono">+0.90</span><span class="k">근거문장수 ↔ 파급효과<br>(실제 교란 변수)</span></div>
    <div><span class="v mono">76 → 3</span><span class="k">최고 LQ 지역이 서울인 팬덤<br>(사전분포 비대칭화 후)</span></div>
    <div><span class="v mono">Δ logL 312</span><span class="k">비대칭 사전의 우도 개선<br>LR p &lt; 10⁻¹⁰⁰</span></div>
  </div>
  <p>이번 개정은 두 갈래입니다. <b>(1) 언어지표의 지위 재조정</b> — 검정 결과에 맞춰 가중치를 내리고 이름을 <b>해외확산도</b>로 바꿨습니다(뒤에 설명하듯 현재 구조는 '적합도'가 아닙니다). <b>(2) 정규화 병행</b> — 언어 쪽에 경험베이즈 축소를 새로 적용하면서, 같은 추정기를 국내 연고밀착도에도 돌려 <span class="mono">α=10</span>이라는 임의 상수를 걷어냈습니다.</p>
</section>

<section>
  <div class="sechead"><span class="secnum">01</span><h2>검정 — 상관은 분량의 착시였다</h2></div>
  <p class="seclede">언어지수 7개 변수를 4구획 산출에 쓰인 성과지표와 대조했습니다. 통제변수는 근거문장수(팬덤별 코퍼스 분량)입니다.</p>

  {tbl(['언어 변수','정의','원상관 r<br>(vs 파급효과)','분량 통제 후<br>편상관 r·z'],
    [[c[0],c[1],f'<span class="mono">{c[2]:+.3f}</span>',f'<span class="mono"><b>{c[3]:+.3f}</b></span>'] for c in corr])}
  <p class="cap">n = 100. 편상관은 근거문장수를 통제한 1차 편상관입니다. 마지막 행(대표해외언어비중)은 다른 변수와 부호가 반대인데, 이 변수만 "언어가 하나로 쏠렸다"를 뜻하기 때문입니다 — 즉 <b>확산 방향의 변수는 전부 0 근처로 붕괴합니다.</b></p>

  <div class="figure">
    <h4>원상관과 편상관</h4>
    <p class="sub">왼쪽이 그대로 본 상관, 오른쪽이 근거문장수를 통제한 상관. 통제하면 전부 0선을 넘어 음으로 떨어진다</p>
    <svg class="chart" id="cc" viewBox="0 0 640 260" preserveAspectRatio="xMidYMid meet" role="img"
      aria-label="언어 변수별 원상관과 편상관 비교 막대그래프"></svg>
  </div>

  <h3>교란 변수는 코퍼스 분량이었다</h3>
  <p>근거문장수와 파급효과의 상관은 <span class="mono">r = +0.902</span>입니다. 많이 언급되는 팬덤은 (a) 파급효과가 크고 (b) 자연히 더 많은 언어에서 잡힙니다. 언어지표가 파급효과와 같이 움직인 것은 <b>둘 다 분량을 타고 있었기</b> 때문입니다.</p>

  <div class="figure">
    <h4>해외비중 ↔ 파급효과, 점 크기 = 근거문장수</h4>
    <p class="sub">오른쪽 위로 가는 흐름은 큰 점(분량이 많은 팬덤)이 만들고 있다. 같은 크기의 점끼리 보면 기울기가 사라진다</p>
    <svg class="chart" id="sc" viewBox="0 0 640 330" preserveAspectRatio="xMidYMid meet" role="img"
      aria-label="해외비중과 파급효과 산점도"></svg>
  </div>

  <div class="alert">
    <span class="atitle">직접 검증은 아직 불가능합니다</span>
    <p>엄밀히 말하면 여기서 쓴 종속변수 <b>파급효과</b>는 관광수요의 대리지표입니다. 팬덤 단위로 실제 관광수요(외래객 방문·소비)를 붙인 자료가 없습니다 — DID로 실측 등급이 나온 사례는 거제·경주·수원 3건뿐이고 전부 리센느 관련이라 언어지표 검정에 쓸 표본이 되지 못합니다. <b>"상관이 뚜렷하지 않다"가 아니라 "상관을 확인할 근거 자체가 없다"</b>는 것이 정확한 상태이고, 그래서 주요 항으로 둘 수 없다는 판단은 더 강해집니다.</p>
  </div>
</section>

<section>
  <div class="sechead"><span class="secnum">02</span><h2>정규화 — 해외확산도 G</h2></div>
  <p class="seclede">원래는 해외비중 원값을 그대로 항에 넣었습니다. 근거가 얇은 팬덤의 비중이 과장되는 문제가 있어 베이즈 축소를 적용했고, 축소 강도는 임의로 정하지 않고 데이터에서 추정했습니다.</p>

  <div class="formula">축소 해외점유(f) = ( <b>해외언급</b> + α<sub>L</sub>·m ) ÷ ( <b>총언급</b> + α<sub>L</sub> )

  α<sub>L</sub> = 6.93, m = 0.4201      ← 베타-이항 최대우도로 추정 (경험베이즈)

<b>G</b>(f) = 축소 해외점유 ÷ 0.7763       0.7763 = 표본 최대 (Stray Kids)</div>
  <p>α를 "중앙값 표본크기" 같은 관례로 잡으면 <span class="mono">α = 93</span>이 나오는데, 총언급이 68~227건으로 두터운 이 자료에서는 사전분포가 관측을 이겨버립니다(카더가든 9.5% → 29.0%). 베타-이항 우도를 직접 최대화하면 <span class="mono">α<sub>L</sub> = 6.93</span>으로, <b>팬덤 간 실제 분산이 커서 축소가 약해야 한다</b>고 자료가 말합니다.</p>

  {tbl(['팬덤','해외 / 총','원 해외비중','축소 점유','G','1순위 언어'],
    [[r[0],f'<span class="mono">{r[1]} / {r[2]}</span>',f'<span class="mono">{r[3]:.3f}</span>',f'<span class="mono">{r[4]:.3f}</span>',f'<span class="mono"><b>{r[5]:.3f}</b></span>',r[6]] for r in D['LANGTOP']]
    +[['<span style="color:var(--text-3)">…</span>','','','','','']]
    +[[r[0],f'<span class="mono">{r[1]} / {r[2]}</span>',f'<span class="mono">{r[3]:.3f}</span>',f'<span class="mono">{r[4]:.3f}</span>',f'<span class="mono"><b>{r[5]:.3f}</b></span>',r[6]] for r in D['LANGBOT']])}
</section>

<section>
  <div class="sechead"><span class="secnum">03</span><h2>가중치 — 0.150에서 0.030~0.080으로</h2></div>
  <p class="seclede">편상관이 0 근처라면 설명력도 0 근처입니다. 상한을 R² 수준에 맞춰 내리고, 페르소나별로는 실측 해외비중에 비례해 차등했습니다.</p>

  <p>상한 <b>0.08</b>은 판단이 들어간 값입니다 — 편상관 절대값이 최대 0.226이므로 설명력 R²는 0.05를 넘지 않는데, 기존 0.150은 그 3배였습니다. 상한 아래에서는 데이터가 결정합니다: <span class="mono">w<sub>L</sub>(페르소나) = 0.08 × (해당 페르소나 평균 해외비중 ÷ 최댓값)</span>.</p>

  {tbl(['페르소나','n','측정 해외비중','최댓값 대비','w<sub>L</sub>','기존'],
    [[p[0],p[1],f'<span class="mono">{p[2]:.3f}</span>',f'<span class="mono">{p[2]/0.509:.3f}</span>',f'<span class="mono"><b>{p[3]:.3f}</b></span>',f'<span class="mono" style="color:var(--text-3)">0.150</span>'] for p in persona])}

  <div class="figure">
    <h4>페르소나별 해외비중과 가중치</h4>
    <p class="sub">집단동원형(임영웅형 단체 이동)은 해외비중 19% — 해외 언어권 확산이 상품 설계에 거의 들어가지 않는다</p>
    <svg class="chart" id="pw" viewBox="0 0 640 220" preserveAspectRatio="xMidYMid meet" role="img"
      aria-label="페르소나별 해외비중과 언어 항 가중치"></svg>
  </div>

  <div class="note"><b>이름도 바꿨습니다 — 언어적합도 → 해외확산도.</b> '적합도'라면 지역 쪽 대응항이 있어야 하는데, 이 지표는 팬덤 측 특성만 잽니다. 지역별 외래객 국적 구성(한국관광 데이터랩 외래관광객 조사)을 확보해 <span class="mono">팬덤 언어 프로파일 × 지역 외래객 구성</span>의 코사인 유사도로 바꿔야 비로소 적합도가 됩니다. 그 전까지는 확산도일 뿐이며, 이름이 실제보다 더 많은 것을 약속하지 않도록 고쳤습니다.</div>
</section>

<section>
  <div class="sechead"><span class="secnum">04</span><h2>대신 이 지표가 답하는 것 — 언어 대응 우선순위</h2></div>
  <p class="seclede">규모는 못 맞히지만 구성은 맞힙니다. 해외 13개 언어에 대칭 디리클레(α = 5.93, 경험베이즈)를 적용해 축소 점유 상위 3종을 상품 명세의 다국어 대응 항목으로 내보냅니다.</p>

  {tbl(['팬덤','1순위 언어','2순위','3순위','G','해외 / 총'],
    [[t[0]]+[f'<span class="mono">{x[0]} {round(x[1]*100)}%</span>' for x in t[1]]
      +[f'<span class="mono">{LGD[t[0]]["G"]:.3f}</span>', f'<span class="mono">{LGD[t[0]]["ov"]} / {LGD[t[0]]["N"]}</span>'] for t in D['TG']])}
  <p class="cap">1순위가 영어가 아닌 팬덤은 <b>100개 중 8개</b>입니다 — 김연자·나훈아·박서진·몬스타엑스(일본어), 김재중·잔나비(중국어), 에픽하이(인도네시아어), 영탁(필리핀어). 원자료의 대표해외언어 열로는 5개만 잡히는데, 축소 점유로 보면 몬스타엑스·영탁·박서진이 추가로 드러납니다. 영어 안내만 붙이는 기본값으로는 이 8건의 실제 유입 언어권을 놓칩니다 — <b>지표의 값어치는 순위를 매기는 데가 아니라 여기에 있습니다.</b></p>
</section>

<section>
  <div class="sechead"><span class="secnum">05</span><h2>병행 정규화 — 연고밀착도의 사전분포를 비대칭으로</h2></div>
  <p class="seclede">언어 쪽 경험베이즈 추정기를 국내 100×17 행렬에도 돌렸습니다. v0.5의 <span class="mono">α = 10</span>(총지역언급 중앙값)은 추정값이 아니라 관례였고, 더 큰 문제는 <b>17개 시도에 균등 배분</b>했다는 점이었습니다.</p>

  <p>균등 사전은 "모든 시도가 똑같이 언급될 법하다"를 가정합니다. 실제 전국 언급의 <b>39.9%가 서울</b>입니다. 그래서 v0.5에서는 100개 팬덤 중 <b>76개의 대표지역이 서울</b>로 잡혔고, 이는 연고가 아니라 기저율이었습니다.</p>

  <div class="formula">사후 점유(f, r) = ( <b>n</b> + α<sub>r</sub> ) ÷ ( <b>N</b> + α )      α = Σα<sub>r</sub> = 13.79
  α<sub>r</sub> : 비대칭 디리클레-다항 최대우도 (17개 자유 모수)

지역언급 <b>LQ</b>(f, r) = 사후 점유 ÷ π<sub>r</sub>        π<sub>r</sub> = α<sub>r</sub> / α  (전국 기저분포)
        LQ = 1  →  전국 기저와 동일       LQ &gt; 1  →  이 지역에 특화

<b>A</b>(f, r) = log LQ ÷ log 37.72        37.72 = 표본 최대 (송가인 · 전남), LQ&lt;1 은 0으로 절단</div>

  <p>대칭 사전(α=4.03이 최대우도) 대비 로그우도가 <b>312.4</b> 개선됩니다. 자유도 16 증가에 대한 우도비 검정 p는 <span class="mono">1.2 × 10⁻¹²²</span>로, 지역별 기저가 다르다는 것은 사실상 확정입니다.</p>

  {tbl(['시도','기저 π<sub>r</sub>','α<sub>r</sub>','LQ&gt;1 팬덤','1위 팬덤','LQ','A'],
    [[t[0],f'<span class="mono">{t[1]:.2f}%</span>',f'<span class="mono">{t[2]:.3f}</span>',
      f'<span class="mono">{t[6]}</span>',t[3] or '<span style="color:var(--warn)">측정 불가</span>',
      f'<span class="mono">{t[4]:.2f}</span>' if t[4] else '—',
      f'<span class="mono"><b>{t[5]:.3f}</b></span>' if t[5] is not None else '—'] for t in D['TOP']])}

  <div class="figure">
    <h4>최고 LQ 지역의 분포 — 사전분포를 바꾸기 전과 후</h4>
    <p class="sub">균등 사전에서는 77개 팬덤이 서울로 몰렸다. 기저를 실제 분포로 두면 3개만 남고 나머지가 전국에 흩어진다</p>
    <svg class="chart" id="cv" viewBox="0 0 640 300" preserveAspectRatio="xMidYMid meet" role="img"
      aria-label="사전분포 변경 전후 최고 LQ 지역 분포 비교"></svg>
  </div>

  <h3>같이 걷어낸 것 — 시군구 균등 배분</h3>
  <p>v0.5는 시군구를 고르면 시도 값을 <span class="mono">1 ÷ 시군구수</span>로 나눴습니다. 그런데 이 상수는 <b>그 지역의 모든 후보에 똑같이 곱해지므로 순위 정보가 전혀 없고</b>, 대신 연고밀착도 항만 1/22로 줄여 다른 항과의 균형을 무너뜨립니다. 실제로 전남 여수시에서 송가인이 4위로 밀리는 현상이 이 때문이었습니다. 제거하고, 측정 해상도가 시도 단위임을 화면에 명시하되 <b>멤버 연고가 그 시군구를 지목한 후보만 앞세우는</b> 방식으로 바꿨습니다.</p>

  <div class="alert">
    <span class="atitle">세종은 산출 불가로 바뀌었습니다</span>
    <p>100개 팬덤 전부의 세종 언급이 0건이라 α<sub>세종</sub> = 0, 기저 π = 0이 추정됩니다. 0으로 나눌 수 없으므로 LQ가 정의되지 않습니다. v0.5는 모든 후보에게 똑같은 0.102를 주어 <b>측정된 것처럼 보이게</b> 했는데, 이제는 연고밀착도 항을 빼고 남은 가중치로 재정규화합니다 — 모든 후보에 동일하게 적용되므로 세종 내부 순위는 왜곡되지 않습니다. 근본 원인은 아직 미확인이며, <b>코퍼스의 지역명 사전에 세종 표기가 들어 있는지</b>부터 확인해야 합니다.</p>
  </div>
</section>

<section>
  <div class="sechead"><span class="secnum">06</span><h2>버전 대조</h2></div>
  {tbl(['항목','v0.5','v0.6'],
   [['언어 항 이름','언어적합도','해외확산도 <span style="color:var(--text-3)">(보조)</span>'],
    ['언어 항 값','해외비중 원값','경험베이즈 축소 후 표본 최대 정규화'],
    ['언어 항 가중치','<span class="mono">0.150</span> 고정','<span class="mono">0.030 ~ 0.080</span> 페르소나별'],
    ['언어 항 근거','없음 — 관례적 배분','편상관 검정 (분량 통제 후 −0.15~−0.23)'],
    ['연고 사전분포','대칭 <span class="mono">α/17</span> · α=10 (중앙값)','비대칭 <span class="mono">α<sub>r</sub></span> · 경험베이즈 17개 모수'],
    ['연고 척도','축소 점유 ÷ 표본 최대','지역언급 <b>LQ</b> ÷ 기저 → 로그 정규화'],
    ['서울 대표 팬덤','<span class="mono">76 / 100</span>','<span class="mono">3 / 100</span>'],
    ['시군구 처리','<span class="mono">× 1/시군구수</span> (정보 없는 상수)','제거 — 시도 해상도 명시 + 멤버 연고 우선'],
    ['세종','전원 동률 <span class="mono">0.102</span>','산출 불가 — 항 제외 후 재정규화'],
    ['임의 상수','α=10, 가중치 0.15','상한 0.08 하나'],
   ])}
</section>

<section>
  <div class="sechead"><span class="secnum">07</span><h2>남은 과제</h2></div>
  {tbl(['#','과제','내용','현재 상태'],
   [['@1','지역별 외래객 국적 구성','한국관광 데이터랩 외래관광객 조사로 시도별 언어권 구성 확보 → 해외확산도를 코사인 유사도 기반 <b>언어적합도</b>로 승격','지역 측 대응항 없음'],
    ['@2','팬덤 단위 관광수요 실측','언어지표를 파급효과 대리지표가 아닌 실제 방문·소비로 검정. 현재 DID 실측은 3건뿐','검정 자체가 불가'],
    ['@3','세종 0건 원인','코퍼스 지역명 사전에 세종·세종시·행정중심복합도시 표기가 포함됐는지 확인','미확인'],
    ['@4','시군구 언급 행렬','시도 해상도를 시군구로 내리면 마지막 추정(지리 귀속)이 사라짐','시도 단위'],
    ['@5','LQ 상한 민감도','A 정규화 분모가 표본 최대(송가인 37.72) 한 점에 걸려 있음. 이 팬덤이 빠지면 전체 척도가 바뀜','단일점 의존'],
    ['@6','영어 1순위 편중','100개 중 92개의 1순위가 영어. 실무에서는 영어를 기본 제공으로 두고 2순위부터 배치하는 편이 유용할 수 있음','검토 필요'],
   ])}
</section>

<footer>
  <p><b>데이터 출처</b> — 전 세계 언어지수 v7(<span class="mono">worldwide_language_index_v7.csv</span>) 100개 팬덤 × 14개 언어, 국내 지역지수 v7(<span class="mono">domestic_regional_index_v7.csv</span>) 100 × 17. 두 파일 모두 내부 정합성 검사를 통과했습니다 — 언어지수는 6종(총언급=근거문장수, 열 합계, 해외비중, 해외=비한국어 합, 검출언어수, 검출해외언어수) 전부 100/100 일치이며, <b>언어다양성은 14개 언어 분포의 정규화 섀넌 엔트로피</b>(100/100), <b>해외언어다양성은 13종 기준 정규화 엔트로피</b>(100/100)임을 역산으로 확인했습니다. 국내 지역지수의 지역다양성이 <span class="mono">검출지역수 ÷ 17</span>이었던 것과 달리 언어 쪽은 엔트로피를 쓰고 있어, 두 지수의 '다양성' 정의가 서로 다릅니다 — 문서화가 필요합니다.</p>
  <p><b>추정 방법</b> — 베타-이항(해외비중)과 디리클레-다항(언어별·지역별 분포)의 최대우도. scipy 1.17.1 · Nelder-Mead 및 L-BFGS-B. 우도비 검정은 자유도 16의 χ² 근사. 멤버 연고는 결과보고서 3장에 명시된 리센느 2건(원이–거제, 제나–경주)만 등록했으며 실존 인물의 출신지를 추정해 채우지 않았습니다.</p>
</footer>
</div>

<script>
const CORR={J([[c[0],c[2],c[3]] for c in corr])};
const SCAT={J(D['SCAT'])};
const PW={J(persona)};
const CVOLD={J([['서울',77],['경기',3],['부산',3],['경남',3],['인천',3],['강원',2],['광주',2],['제주',2],['대구',2],['전남',1],['경북',1],['울산',1]])};
const CVNEW={J(D['cnt'])};
const SD={J(SD)};
const NS='http://www.w3.org/2000/svg';
const css=v=>getComputedStyle(document.documentElement).getPropertyValue(v).trim();
function mk(t,a){{const e=document.createElementNS(NS,t);for(const k in a)e.setAttribute(k,a[k]);return e;}}
function txt(x,y,s,o){{const e=mk('text',Object.assign({{x,y}},o||{{}}));e.textContent=s;return e;}}

function drawCorr(){{
  const s=document.getElementById('cc'); s.innerHTML='';
  const W=640,H=260,L=118,R=18,T=26,B=30, w=W-L-R, rows=CORR.length, rh=(H-T-B)/rows;
  const mx=0.75, x0=L+w*0.5, sx=v=>x0+v/mx*(w*0.5);
  [-0.5,-0.25,0,0.25,0.5].forEach(v=>{{
    s.appendChild(mk('line',{{x1:sx(v),y1:T-8,x2:sx(v),y2:H-B,stroke:css(v===0?'--line-strong':'--line'),'stroke-width':1,...(v?{{'stroke-dasharray':'2 3'}}:{{}})}}));
    s.appendChild(txt(sx(v),T-13,v.toFixed(2),{{'text-anchor':'middle',class:'axlbl',fill:css('--text-3')}}));
  }});
  CORR.forEach((c,i)=>{{
    const y=T+i*rh+rh/2;
    s.appendChild(txt(L-8,y+4,c[0],{{'text-anchor':'end',class:'ptlbl',fill:css('--text-2')}}));
    [[c[1],css('--text-3'),-7],[c[2],css('--primary'),5]].forEach(([v,col,dy])=>{{
      const a=Math.min(sx(0),sx(v)),b=Math.abs(sx(v)-sx(0));
      s.appendChild(mk('rect',{{x:a,y:y+dy-5,width:Math.max(b,1),height:10,fill:col,rx:1}}));
      s.appendChild(txt(v<0?a-4:a+b+4,y+dy+3,v.toFixed(3),{{'text-anchor':v<0?'end':'start',class:'axlbl',fill:css('--text-3')}}));
    }});
  }});
  s.appendChild(mk('rect',{{x:L,y:H-16,width:9,height:9,fill:css('--text-3'),rx:1}}));
  s.appendChild(txt(L+13,H-8,'원상관',{{class:'axlbl',fill:css('--text-3')}}));
  s.appendChild(mk('rect',{{x:L+62,y:H-16,width:9,height:9,fill:css('--primary'),rx:1}}));
  s.appendChild(txt(L+75,H-8,'근거문장수 통제 후 편상관',{{class:'axlbl',fill:css('--text-3')}}));
}}

function drawScat(){{
  const s=document.getElementById('sc'); s.innerHTML='';
  const W=640,H=330,L=48,R=16,T=18,B=40, w=W-L-R, h=H-T-B;
  const sx=v=>L+v*w, sy=v=>T+h-v*h;
  [0,.25,.5,.75,1].forEach(v=>{{
    s.appendChild(mk('line',{{x1:L,y1:sy(v),x2:W-R,y2:sy(v),stroke:css('--line'),'stroke-dasharray':'2 3'}}));
    s.appendChild(txt(L-7,sy(v)+4,v.toFixed(2),{{'text-anchor':'end',class:'axlbl',fill:css('--text-3')}}));
    s.appendChild(txt(sx(v),H-22,v.toFixed(2),{{'text-anchor':'middle',class:'axlbl',fill:css('--text-3')}}));
  }});
  s.appendChild(txt(L,T-4,'파급효과 S',{{class:'axlbl',fill:css('--text-3')}}));
  s.appendChild(txt(W-R,H-6,'해외비중 →',{{'text-anchor':'end',class:'axlbl',fill:css('--text-3')}}));
  const amin=Math.min(...SCAT.map(d=>d[3])), amax=Math.max(...SCAT.map(d=>d[3]));
  SCAT.forEach(d=>{{
    const r=2.4+(d[3]-amin)/(amax-amin)*6.6;
    s.appendChild(mk('circle',{{cx:sx(d[1]),cy:sy(d[2]),r,fill:css('--primary'),'fill-opacity':.28,stroke:css('--primary'),'stroke-width':.8,'stroke-opacity':.5}}));
  }});
  const n=SCAT.length, mx=SCAT.reduce((a,d)=>a+d[1],0)/n, my=SCAT.reduce((a,d)=>a+d[2],0)/n;
  const b=SCAT.reduce((a,d)=>a+(d[1]-mx)*(d[2]-my),0)/SCAT.reduce((a,d)=>a+(d[1]-mx)**2,0);
  s.appendChild(mk('line',{{x1:sx(0),y1:sy(my+b*(0-mx)),x2:sx(.85),y2:sy(my+b*(.85-mx)),stroke:css('--bad'),'stroke-width':1.6,'stroke-dasharray':'5 3'}}));
  s.appendChild(txt(sx(.86),sy(my+b*(.86-mx))+4,'r = +0.36',{{class:'axlbl',fill:css('--bad')}}));
  [70,140,220].forEach((v,i)=>{{
    const r=2.4+(v-amin)/(amax-amin)*6.6, cx=L+18+i*54, cy=T+16;
    s.appendChild(mk('circle',{{cx,cy,r,fill:'none',stroke:css('--text-3'),'stroke-width':.9}}));
    s.appendChild(txt(cx+r+4,cy+3,v+'건',{{class:'axlbl',fill:css('--text-3')}}));
  }});
}}

function drawPW(){{
  const s=document.getElementById('pw'); s.innerHTML='';
  const W=640,H=220,L=92,R=52,T=22,B=28, w=W-L-R, rh=(H-T-B)/PW.length;
  const mx=0.55, sx=v=>L+v/mx*w;
  [0,.2,.4].forEach(v=>{{s.appendChild(mk('line',{{x1:sx(v),y1:T-8,x2:sx(v),y2:H-B,stroke:css('--line'),'stroke-dasharray':'2 3'}}));
    s.appendChild(txt(sx(v),T-13,v.toFixed(1),{{'text-anchor':'middle',class:'axlbl',fill:css('--text-3')}}));}});
  PW.forEach((p,i)=>{{
    const y=T+i*rh+rh/2;
    s.appendChild(txt(L-8,y+4,p[0]+' ('+p[1]+')',{{'text-anchor':'end',class:'ptlbl',fill:css('--text-2')}}));
    s.appendChild(mk('rect',{{x:L,y:y-9,width:sx(p[2])-L,height:11,fill:css('--primary'),rx:1,'fill-opacity':.85}}));
    s.appendChild(txt(sx(p[2])+5,y+1,'해외비중 '+(p[2]*100).toFixed(1)+'%',{{class:'axlbl',fill:css('--text-3')}}));
    s.appendChild(mk('rect',{{x:L,y:y+4,width:Math.max(sx(p[3])-L,1.5),height:7,fill:css('--warn'),rx:1}}));
    s.appendChild(txt(sx(p[3])+5,y+11,'w '+p[3].toFixed(3),{{class:'axlbl',fill:css('--warn')}}));
  }});
  s.appendChild(txt(L,H-8,'위: 측정 해외비중   아래: 적용 가중치 w',{{class:'axlbl',fill:css('--text-3')}}));
}}

function drawCV(){{
  const s=document.getElementById('cv'); s.innerHTML='';
  const W=640,H=300,L=40,R=12,T=26,B=46, w=W-L-R, h=H-T-B;
  const o=Object.fromEntries(CVOLD), nw=Object.fromEntries(CVNEW);
  const mx=80, sy=v=>T+h-v/mx*h, bw=w/SD.length;
  [0,20,40,60,80].forEach(v=>{{s.appendChild(mk('line',{{x1:L,y1:sy(v),x2:W-R,y2:sy(v),stroke:css('--line'),'stroke-dasharray':'2 3'}}));
    s.appendChild(txt(L-6,sy(v)+4,v,{{'text-anchor':'end',class:'axlbl',fill:css('--text-3')}}));}});
  SD.forEach((sd,i)=>{{
    const x=L+i*bw, a=o[sd]||0, b=nw[sd]||0;
    s.appendChild(mk('rect',{{x:x+bw*0.13,y:sy(a),width:bw*0.33,height:Math.max(h-(sy(a)-T),0),fill:css('--text-3'),'fill-opacity':.55,rx:1}}));
    s.appendChild(mk('rect',{{x:x+bw*0.52,y:sy(b),width:bw*0.33,height:Math.max(h-(sy(b)-T),0),fill:css('--primary'),rx:1}}));
    const g=mk('g',{{transform:'translate('+(x+bw/2)+','+(H-B+13)+') rotate(-38)'}});
    g.appendChild(txt(0,0,sd,{{'text-anchor':'end',class:'axlbl',fill:css('--text-3')}}));
    s.appendChild(g);
    if(a>=20) s.appendChild(txt(x+bw*0.30,sy(a)-4,a,{{'text-anchor':'middle',class:'axlbl',fill:css('--text-3')}}));
  }});
  s.appendChild(mk('rect',{{x:W-R-176,y:T-18,width:9,height:9,fill:css('--text-3'),'fill-opacity':.55,rx:1}}));
  s.appendChild(txt(W-R-163,T-10,'균등 사전 (v0.5)',{{class:'axlbl',fill:css('--text-3')}}));
  s.appendChild(mk('rect',{{x:W-R-72,y:T-18,width:9,height:9,fill:css('--primary'),rx:1}}));
  s.appendChild(txt(W-R-59,T-10,'비대칭 (v0.6)',{{class:'axlbl',fill:css('--text-3')}}));
}}
function all(){{drawCorr();drawScat();drawPW();drawCV();}}
all();
matchMedia('(prefers-color-scheme: dark)').addEventListener('change',all);
</script>
'''
open('/home/claude/language-index.html','w',encoding='utf-8').write(head+body)
print('written',len(head+body))
