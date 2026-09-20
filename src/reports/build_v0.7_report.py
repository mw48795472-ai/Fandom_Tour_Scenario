import json
D=json.load(open('docdata2.json',encoding='utf-8'))
src=open('/home/claude/language-index.html',encoding='utf-8').read()
style=src[src.index('<style>'):src.rindex('</style>')+8]
J=lambda o: json.dumps(o,ensure_ascii=False,separators=(',',':'))
def tbl(head,rows,cls=''):
    h=''.join(f'<th>{c}</th>' for c in head)
    def cell(c):
        if isinstance(c,str) and c.startswith('@'): return '<td class="mono">'+c[1:]+'</td>'
        return '<td>'+str(c)+'</td>'
    b=''.join('<tr>'+''.join(cell(c) for c in r)+'</tr>' for r in rows)
    return f'<div class="tablewrap"><table class="{cls}"><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table></div>'
m=lambda v: f'<span class="mono">{v}</span>'
bd=lambda v: f'<span class="mono"><b>{v}</b></span>'

head=f'''<title>광고지수 유발계수 검증</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Gothic+A1:wght@500;700;800;900&family=Noto+Sans+KR:wght@400;500;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet">
{style}
<style>.pass{{color:var(--ok);font-weight:700;}} .fail{{color:var(--text-3);}}</style>
'''

body=f'''
<div class="wrap">

<header class="masthead">
  <p class="kicker">팬덤루트랩 · RegionFit 개정 보고 · v0.7</p>
  <h1>세 지수를 같은 저울에<br>올렸더니, 광고만 남았다</h1>
  <p class="deck">언어지수를 검정할 때 쓴 잣대를 광고지수·지역지수에도 똑같이 적용했습니다. 근거문장수를 기저로 둔 <b>증분 설명력 ΔR²</b>으로 보면 광고비중만 <span class="mono">+0.049</span>로 살아남고 나머지는 전부 <span class="mono">0.008</span> 이하입니다. 광고지수를 <b>강도(상업유발도)</b>와 <b>방향(업종정합도)</b>으로 나눠 적용했고, 방향 쪽은 지역 소비구조 LQ와 교차해 <b>지역 한쪽만 보던 업종 항을 지역 × 아티스트로</b> 바꿨습니다.</p>
  <div class="docmeta">
    <div><b>작성</b><span>팀 데이터오름 · 서목원</span></div>
    <div><b>일자</b><span class="mono">2026-09-18</span></div>
    <div><b>원천</b><span>광고 지수 v7 · 100 × 20 행렬</span></div>
    <div><b>적용</b><span>팬덤루트랩 스튜디오 v16</span></div>
  </div>
</header>

<section>
  <div class="sechead"><span class="secnum">00</span><h2>요약</h2></div>
  <div class="thesis">
    <span class="lab">Result</span>
    <p class="big">광고비중은 <span class="em">코퍼스 분량을 통제해도 파급효과와 남습니다</span> — 편상관 +0.512, 증분 설명력 +0.049. 언어지수(+0.008·부호 반전)와 갈린 유일한 지수입니다. 그래서 이 지표는 <span class="em">보조가 아니라 점수 항</span>으로 넣었고, 업종 분포는 지역 소비구조 LQ와 곱해 <span class="em">유발계수의 방향</span>을 정하는 데 썼습니다.</p>
  </div>
  <div class="stats">
    <div><span class="v mono">+0.512</span><span class="k">광고비중 ↔ 파급효과<br>분량 통제 후 편상관</span></div>
    <div><span class="v mono">ΔR² +0.049</span><span class="k">증분 설명력<br>(언어지수는 +0.008)</span></div>
    <div><span class="v mono">51.1%</span><span class="k">20개 업종 중<br>관광소비 매핑 커버리지</span></div>
    <div><span class="v mono">3 / 17</span><span class="k">광고 프로파일 반영으로<br>1위가 바뀐 시도</span></div>
    <div><span class="v mono">R² 0.813</span><span class="k">파급효과 ~ 근거문장수<br>(§07 참조)</span></div>
  </div>
  <p>구조는 <b>유발계수 = 강도 × 방향</b>입니다. 강도는 광고비중을 베타-이항 경험베이즈로 축소한 <b>상업유발도 C</b>(검정 통과), 방향은 아티스트 광고 업종 LQ와 지역 소비구조 LQ를 교차한 <b>업종정합도 B</b>(검정 불가 — 설계 가설)입니다. 둘을 하나로 합치지 않고 나눠 둔 이유는 <b>한쪽만 검증됐기 때문</b>입니다.</p>
</section>

<section>
  <div class="sechead"><span class="secnum">01</span><h2>원자료 구조 — 광고 태깅은 다중 라벨이었다</h2></div>
  <p class="seclede">정합성 검사 3종 중 2종은 100/100이었지만, 하나가 어긋났습니다. 그리고 그 어긋남이 자료 구조를 알려줬습니다.</p>

  {tbl(['검사','결과','해석'],
   [['광고비중 = 광고성문장수 ÷ 근거문장수',f'<span class="pass">100 / 100</span>','문장 단위 비율'],
    ['대표업종 = 업종 열 최댓값',f'<span class="pass">100 / 100</span>','동률은 첫 열 우선'],
    ['광고성문장수 = 업종 열 합계',f'<span class="fail">42 / 100</span>','<b>나머지 58건은 열 합계가 더 큼</b>'],
   ])}
  <p>열 합계가 광고성문장수보다 작은 경우는 <b>한 건도 없습니다</b>. 평균 배수는 <span class="mono">1.141</span>, 최대 <span class="mono">2.50</span>(김연자)입니다. 즉 <b>한 광고 문장에 업종 태그가 여러 개 붙습니다</b>. 실무적으로 중요한 함의가 있습니다 — <b>광고비중의 분모는 문장, 업종 분포의 분모는 태그</b>라서 두 지표를 같은 분모로 묶으면 안 됩니다. 이 보고서는 둘을 분리해 다룹니다.</p>

  {tbl(['업종','건수','기저 π','관광소비 매핑'],
   [[r[0],m(r[1]),m(f'{r[2]*100:.2f}%'),(f'<span class="pass">→ {r[4]}</span>' if r[3] else '<span class="fail">대응 없음</span>')] for r in D['IND20']])}
  <p class="cap">기저 π는 100×20 행렬에 비대칭 디리클레-다항 경험베이즈를 적합한 값(총 농도 {D['K20']})입니다. 매핑 대상 7개 업종의 합이 전체 광고 근거의 <b>{D['cov']*100:.1f}%</b>입니다. 나머지는 지역 관광소비와 대응항이 없어 매핑하지 않았습니다 — 억지로 끼워 넣으면 방향 신호가 아니라 잡음이 됩니다. 다만 그중 <b>복지/행정이 단일 최대 업종(15.3%)</b>이라는 점은 그 자체로 의미가 있어 §06에서 따로 다룹니다.</p>
</section>

<section>
  <div class="sechead"><span class="secnum">02</span><h2>검정 — 같은 저울에 올린 세 지수</h2></div>
  <p class="seclede">기저모형은 <span class="mono">파급효과 ~ 근거문장수</span>(R² = {D['base']})입니다. 각 변수를 추가했을 때의 설명력 증가분 ΔR²이 그 지표가 분량 말고 무엇을 더 알려주는지를 나타냅니다.</p>

  {tbl(['변수','지수','원상관<br>(vs S)','편상관<br>(분량 통제)','ΔR²<br>(vs S)','편상관<br>(vs 충성도)','ΔR²<br>(vs L)'],
   [[r[0],r[1],m(f'{r[2]:+.3f}'),(bd(f'{r[3]:+.3f}') if abs(r[3])>=0.3 else m(f'{r[3]:+.3f}')),
     (bd(f'{r[4]:+.3f}') if r[4]>=0.02 else m(f'{r[4]:+.3f}')),m(f'{r[5]:+.3f}'),m(f'{r[6]:+.3f}')] for r in D['TBL']])}
  <p class="cap">n = 100. 충성도 기저모형은 R² = {D['baseL']}입니다. 광고비중·광고 업종수만 ΔR²가 0.03을 넘고, 나머지는 전부 0.008 이하입니다.</p>

  <div class="figure">
    <h4>증분 설명력 ΔR² — 세 지수 비교</h4>
    <p class="sub">근거문장수만 쓴 기저모형에 각 변수를 더했을 때의 설명력 증가분. 광고 계열 두 개만 눈에 띈다</p>
    <svg class="chart" id="dr" viewBox="0 0 640 260" preserveAspectRatio="xMidYMid meet" role="img"
      aria-label="변수별 증분 설명력 막대그래프"></svg>
  </div>

  <h3>부호까지 읽으면 — 광고는 4구획의 대각선을 탄다</h3>
  <p>광고비중은 파급효과 쪽으로 <b>+0.512</b>, 충성도 쪽으로 <b>−0.288</b>입니다. 광고 업종수는 각각 <b>+0.438</b>, <b>−0.349</b>로 더 뚜렷합니다. 상업 담론이 두꺼운 팬덤은 파급효과 축으로 밀리고 충성도 축에서는 내려간다는 뜻이고, 이는 4구획의 <b>외부견인형 ↔ 내부결속형 대각선</b>과 정확히 같은 방향입니다. 광고지수는 기존 4구획 축과 독립된 새 정보가 아니라, <b>그 축을 외부에서 재확인해 주는 자료</b>로 읽는 편이 맞습니다.</p>

  <div class="figure">
    <h4>분량을 걷어낸 뒤에도 남는 관계</h4>
    <p class="sub">두 축 모두 근거문장수로 회귀한 잔차. 기울기가 살아 있다 — 언어지수의 잔차 산점도는 반대로 기울었다</p>
    <svg class="chart" id="rs" viewBox="0 0 640 330" preserveAspectRatio="xMidYMid meet" role="img"
      aria-label="광고비중 잔차와 파급효과 잔차의 산점도"></svg>
  </div>
</section>

<section>
  <div class="sechead"><span class="secnum">03</span><h2>강도 — 상업유발도 C</h2></div>
  <p class="seclede">광고비중을 그대로 쓰지 않고 베타-이항 최대우도로 축소 강도를 추정했습니다. 근거문장수가 68~227건이라 표본 자체는 두터운데, 광고성 문장은 0~47건으로 얇습니다.</p>

  <div class="formula">축소 광고비중(f) = ( <b>광고성문장수</b> + α<sub>C</sub>·m ) ÷ ( <b>근거문장수</b> + α<sub>C</sub> )

  α<sub>C</sub> = {D['Ca']},  m = {D['Cm']}      ← 베타-이항 최대우도 (경험베이즈)

<b>C</b>(f) = 축소 광고비중 ÷ {D['Cmax']}      {D['Cmax']} = 표본 최대 (이효리)</div>
  <p>α<sub>C</sub> = {D['Ca']}는 언어지수의 6.93보다 훨씬 큽니다 — 광고 태깅이 희소해 팬덤 간 관측 분산이 이항 잡음에 가깝기 때문에, 자료가 <b>강하게 축소하라</b>고 말합니다. 그 결과 광고 0건인 김동률·나훈아도 0이 아니라 사전평균 근처(C 0.073·0.083)에 놓입니다.</p>

  {tbl(['팬덤','광고성 / 근거','원 광고비중','축소','C','대표업종'],
   [[r[0],m(f'{r[1]} / {r[2]}'),m(f'{r[3]:.3f}'),m(f'{r[4]:.3f}'),bd(f'{r[5]:.3f}'),r[6]] for r in D['CTOP']]
   +[['<span style="color:var(--text-3)">…</span>','','','','','']]
   +[[r[0],m(f'{r[1]} / {r[2]}'),m(f'{r[3]:.3f}'),m(f'{r[4]:.3f}'),bd(f'{r[5]:.3f}'),r[6]] for r in D['CBOT']])}
</section>

<section>
  <div class="sechead"><span class="secnum">04</span><h2>방향 — 업종정합도 B</h2></div>
  <p class="seclede">기존 업종적합도는 지역 소비구조 LQ만 보고, 가중치는 페르소나 템플릿에서 가져왔습니다. 아티스트가 실제로 어떤 업종을 광고하는지는 들어가지 않았습니다.</p>

  <div class="formula">아티스트 업종 LQ(f, 영역) = 사후 점유 ÷ 기저 π      사후 = (광고 건수 + α<sub>영역</sub>) / (총 + κ),  κ = {D['K5']}

혼합 가중(f, 영역) ∝ <b>페르소나 템플릿</b>(영역) × <b>아티스트 업종 LQ</b>(f, 영역)      → 합이 1이 되도록 재정규화

<b>B</b>(f, r) = Σ 혼합 가중 × min( 지역 소비 LQ ÷ 2 , 1 )</div>

  <p>이 형태의 장점은 <b>되돌아가는 지점이 정확하다</b>는 것입니다. 광고 근거가 없는 팬덤은 아티스트 LQ가 전 영역에서 정확히 1.0이 되므로 혼합 가중이 페르소나 템플릿과 같아지고, v0.6과 동일한 값이 나옵니다. 김동률(광고 0건)이 실제로 그렇습니다.</p>

  {tbl(['소비영역','광고 건수','기저 π','α'],
   [[r[0],m(r[1]),m(f'{r[2]*100:.2f}%'),m(f'{r[3]:.4f}')] for r in D['AREA']])}

  <h3>적용 예 — 리센느 × 거제시</h3>
  <p>리센느의 광고는 식음료 8건 / 쇼핑·패션 2건입니다. 음식 영역 아티스트 LQ가 <span class="mono">2.30</span>인데, 거제시의 음식 소비 LQ도 <span class="mono">2.28</span>로 높습니다. 혼합 가중에서 음식이 <b>25% → 61%</b>로 올라가고, 업종정합도가 <span class="mono">0.748 → 0.851</span>이 됩니다. 반대로 숙박은 템플릿에서 45%였지만 리센느에 숙박·여행 광고가 없어 20%로 내려갑니다.</p>

  <div class="figure">
    <h4>혼합 가중의 이동 — 리센느 × 거제시</h4>
    <p class="sub">페르소나 템플릿(글로벌투어형)이 아티스트 광고 프로파일에 의해 재배분된다</p>
    <svg class="chart" id="mx" viewBox="0 0 640 230" preserveAspectRatio="xMidYMid meet" role="img"
      aria-label="리센느 거제시 혼합 가중 변화"></svg>
  </div>

  <div class="alert">
    <span class="atitle">방향은 검정하지 못했습니다</span>
    <p>강도(광고비중)는 팬덤 단위 변수라 팬덤 단위 성과(파급효과)와 대조할 수 있었습니다. 그러나 업종정합도는 <b>팬덤 × 지역</b> 단위라 대조할 성과 실측이 없습니다 — DID 실측은 3건뿐입니다. §04 전체가 <b>검정된 결과가 아니라 설계 가설</b>이며, 화면에도 그렇게 표기했습니다. 광고 업종과 지역 소비구조가 맞아야 소비로 전환된다는 가정 자체는 거제 사례(식음료 광고 · 음식 LQ 2.28 · DID 소비 +20.1%)와 어긋나지 않지만, n=1입니다.</p>
  </div>
</section>

<section>
  <div class="sechead"><span class="secnum">05</span><h2>적용 결과</h2></div>
  <p class="seclede">17개 시도 전체에서 광고 프로파일을 켜고 끈 결과를 비교했습니다.</p>
  {tbl(['시도','템플릿 전용 1위','광고 프로파일 반영 1위'],
   [['인천','TWICE','<b>BTS</b>'],['강원','BTS','<b>싸이</b>'],['세종','BTS','<b>이효리</b>']])}
  <p class="cap">나머지 14개 시도는 1위가 유지됐고, 업종정합도 값만 ±0.10 범위에서 움직였습니다 — 가장 큰 상승은 경남 리센느 <span class="mono">+0.103</span>, 가장 큰 하락은 울산 TWICE <span class="mono">−0.116</span>입니다. 판을 뒤엎지 않으면서 같은 점수대의 후보들 사이에서 순서를 가르는 정도로 작동합니다.</p>
</section>

<section>
  <div class="sechead"><span class="secnum">06</span><h2>복지/행정 — 점수에는 넣지 않았습니다</h2></div>
  <p class="seclede">20개 업종 중 가장 큰 항목(228건 · 15.3%)이고, 내용상 <b>지자체 위촉·공익 캠페인</b>입니다. 이 서비스가 만들려는 것과 정확히 같은 종류의 협업입니다.</p>

  {tbl(['팬덤','복지/행정 LQ','건수','광고 총건'],
   [[r[0],bd(f'{r[1]:.2f}'),m(r[2]),m(r[3])] for r in D['GOV']])}

  <p>그런데 검정에서는 <b>ΔR² = 0.000</b>, 편상관 −0.037이었습니다. 지자체 광고가 많다고 파급효과가 크지는 않습니다 — 오히려 수원 사례(연고 없는 기관 채널 중심 · 검색 −11.7%)가 보여준 패턴과 일관됩니다. 그래서 <b>점수 항으로 넣지 않고 협업 이력으로만 표기</b>합니다. 후보를 고르는 근거가 아니라, 고른 뒤 <b>위촉 실무가 수월한지</b>를 가늠하는 정보입니다.</p>
  <p class="cap">리센느의 복지/행정 LQ는 1.75(9건)로 상위 9위입니다 — 거제·경주 홍보대사 위촉이 실제로 코퍼스에 잡혀 있다는 뜻이고, 지표가 현실을 반영하고 있다는 간접 확인입니다.</p>
</section>

<section>
  <div class="sechead"><span class="secnum">07</span><h2>검정하면서 드러난 문제 — 파급효과 S</h2></div>
  <div class="alert">
    <span class="atitle">파급효과는 근거문장수로 81% 설명됩니다</span>
    <p><span class="mono">S ~ 근거문장수</span> 단일 회귀의 R²가 <b>{D['base']}</b>입니다. 충성도 L도 {D['baseL']}입니다. 이 자체가 이번 개정의 결과는 아니지만, 검정을 하려고 기저모형을 세우는 과정에서 드러났습니다. 함의는 두 가지입니다. <b>(1)</b> 파급효과 축은 상당 부분 "얼마나 많이 언급되는가"의 재진술이므로, 4구획의 가로축을 해석할 때 규모 효과를 분리해 설명해야 합니다. <b>(2)</b> 어떤 새 지표든 파급효과와의 단순 상관은 거의 자동으로 양수가 나오므로, 이 보고서가 쓴 <b>ΔR² 기준이 최소한의 방어선</b>입니다.</p>
  </div>
  <p>RegionFit에서 파급효과 항(w 0.20)과 상업유발도 항(w 0.086)은 원상관 +0.589로 겹칩니다. 두 항을 독립 근거로 읽으면 안 되고, 화면에도 그렇게 적었습니다.</p>
</section>

<section>
  <div class="sechead"><span class="secnum">08</span><h2>가중치 — 같은 기준으로 다시 맞췄습니다</h2></div>
  <p class="seclede">v0.6에서 해외확산도 상한을 0.08로 정할 때는 편상관 제곱(R² ≤ 0.05)을 기준으로 삼았습니다. 이번에 ΔR²이라는 더 정확한 잣대가 생겼으므로 그 기준으로 다시 맞춥니다.</p>

  {tbl(['항','근거','ΔR²','v0.6','v0.7'],
   [['상업유발도','광고비중 · 검정 통과',m('+0.049'),'—',bd('0.086')],
    ['해외확산도','해외비중 · 편상관 부호 반전',m('+0.008'),m('0.030~0.080'),bd('0.005~0.014')],
    ['업종정합도','지역 × 아티스트 · 검정 불가','—',m('0.250'),m('0.250')],
    ['연고밀착도','지역 LQ · 검정 불가','—',m('0.300'),m('0.300')],
    ['파급효과','성과지표 직접 투입','—',m('0.200'),m('0.200')],
    ['공연 수용력','시설 규모 · 검정 불가','—',m('0.10~0.20'),m('0.10~0.20')],
   ])}
  <p>팬덤 특성 항(상업유발도 + 해외확산도)의 예산을 0.10으로 두고 ΔR² 비율(0.049 : 0.008)로 나눴습니다. 해외확산도는 v0.6에서 내린 값을 <b>한 번 더 내렸고</b>, 이건 v0.6의 기준이 느슨했기 때문입니다 — 편상관 제곱은 기저모형 없이 계산되므로 분량이 이미 설명하는 부분을 빼지 못합니다.</p>
  <div class="note"><b>나머지 네 항은 여전히 설계값입니다.</b> 연고밀착도·업종정합도·공연 수용력은 <b>지역 조건부</b> 변수라 팬덤 단위 성과로는 검정할 수 없습니다. 이 항들의 0.30 / 0.25 / 0.10~0.20은 데이터가 아니라 판단이며, 이 문서는 그 판단을 정당화하지 않습니다. 팬덤 × 지역 단위 성과가 쌓이기 전까지는 그대로 둡니다.</div>
</section>

<section>
  <div class="sechead"><span class="secnum">09</span><h2>남은 과제</h2></div>
  {tbl(['#','과제','내용','상태'],
   [['@1','팬덤 × 지역 성과 실측','업종정합도·연고밀착도를 검정할 유일한 길. 현재 DID 3건','검정 불가'],
    ['@2','다중 라벨 원단위','업종 태그가 문장당 평균 1.141개. 태그-문장 대응표가 있으면 업종별 광고비중을 문장 단위로 재산출 가능','태그 합계만 보유'],
    ['@3','비매핑 업종 활용','금융·자동차·정보/통신 등 48.9%는 지역 관광소비와 대응항이 없음. 산업전이(F4) 쪽 지표로는 쓸 수 있는지 검토','미검토'],
    ['@4','파급효과 규모 보정','S에서 근거문장수 효과를 제거한 잔차 버전을 4구획에 병기할지 결정','§07 제기'],
    ['@5','복지/행정 세분','지자체 위촉과 공익 캠페인이 한 업종에 묶여 있음. 분리되면 위촉 실적 지표로 승격 가능','미분리'],
   ])}
</section>

<footer>
  <p><b>데이터 출처</b> — 광고 지수 v7(<span class="mono">ad_commercial_index_v7.csv</span>) 100개 팬덤 × 20개 업종, 광고성 문장 1,488건. 정합성 검사는 §01에 그대로 실었습니다. 파급효과·충성도·4구획·페르소나는 결과보고서의 실측 산출물이고, 소비구조 LQ는 제공받은 카드소비 실측(시도 17 · 시군구 229 · 5영역)입니다.</p>
  <p><b>추정 방법</b> — 베타-이항(광고비중)과 디리클레-다항(20개 업종 · 5개 영역)의 최대우도. scipy 1.17.1 · Nelder-Mead 및 L-BFGS-B. ΔR²은 <span class="mono">y ~ 근거문장수</span> 기저모형에 변수를 추가한 최소제곱 회귀의 결정계수 차이이며, 편상관은 근거문장수를 통제한 1차 편상관입니다. 이전 보고: 연고밀착도 v0.5 · 언어지수 v0.6.</p>
</footer>
</div>

<script>
const TBL={J(D['TBL'])}, RES={J(D['RES'])}, IND20={J(D['IND20'])};
const MIXB=[['음식',0.25,0.61],['관광/쇼핑',0.20,0.14],['레저활동',0.10,0.05],['숙박',0.45,0.20]];
const NS='http://www.w3.org/2000/svg';
const css=v=>getComputedStyle(document.documentElement).getPropertyValue(v).trim();
function mk(t,a){{const e=document.createElementNS(NS,t);for(const k in a)e.setAttribute(k,a[k]);return e;}}
function txt(x,y,s,o){{const e=mk('text',Object.assign({{x,y}},o||{{}}));e.textContent=s;return e;}}

function drawDR(){{
  const s=document.getElementById('dr'); s.innerHTML='';
  const W=640,H=260,L=124,R=42,T=26,B=30,w=W-L-R,rows=TBL.length,rh=(H-T-B)/rows;
  const mx=0.055,sx=v=>L+v/mx*w;
  const COL={{'광고':css('--primary'),'언어':css('--text-3'),'지역':css('--line-strong')}};
  [0,0.01,0.02,0.03,0.04,0.05].forEach(v=>{{
    s.appendChild(mk('line',{{x1:sx(v),y1:T-8,x2:sx(v),y2:H-B,stroke:css('--line'),'stroke-dasharray':'2 3'}}));
    s.appendChild(txt(sx(v),T-13,v.toFixed(2),{{'text-anchor':'middle',class:'axlbl',fill:css('--text-3')}}));
  }});
  TBL.forEach((r,i)=>{{
    const y=T+i*rh+rh/2, v=Math.max(r[4],0);
    s.appendChild(txt(L-8,y+4,r[0],{{'text-anchor':'end',class:'ptlbl',fill:css('--text-2')}}));
    s.appendChild(mk('rect',{{x:L,y:y-6,width:Math.max(sx(v)-L,1),height:12,fill:COL[r[1]],rx:1}}));
    s.appendChild(txt(sx(v)+5,y+4,r[4].toFixed(3),{{class:'axlbl',fill:css('--text-3')}}));
  }});
  let lx=L;
  [['광고','광고'],['언어','언어'],['지역','지역']].forEach(([k,lab])=>{{
    s.appendChild(mk('rect',{{x:lx,y:H-16,width:9,height:9,fill:COL[k],rx:1}}));
    s.appendChild(txt(lx+13,H-8,lab+' 지수',{{class:'axlbl',fill:css('--text-3')}})); lx+=76;
  }});
}}

function drawRS(){{
  const s=document.getElementById('rs'); s.innerHTML='';
  const W=640,H=330,L=54,R=16,T=20,B=40,w=W-L-R,h=H-T-B;
  const xs=RES.map(d=>d[1]), ys=RES.map(d=>d[2]);
  const x0=Math.min(...xs),x1=Math.max(...xs),y0=Math.min(...ys),y1=Math.max(...ys);
  const sx=v=>L+(v-x0)/(x1-x0)*w, sy=v=>T+h-(v-y0)/(y1-y0)*h;
  s.appendChild(mk('line',{{x1:L,y1:sy(0),x2:W-R,y2:sy(0),stroke:css('--line-strong')}}));
  s.appendChild(mk('line',{{x1:sx(0),y1:T,x2:sx(0),y2:T+h,stroke:css('--line-strong')}}));
  [-0.1,0,0.1,0.2].forEach(v=>{{ if(v<x0||v>x1)return;
    s.appendChild(txt(sx(v),H-22,v.toFixed(2),{{'text-anchor':'middle',class:'axlbl',fill:css('--text-3')}}));}});
  [-0.2,-0.1,0,0.1,0.2].forEach(v=>{{ if(v<y0||v>y1)return;
    s.appendChild(txt(L-7,sy(v)+4,v.toFixed(2),{{'text-anchor':'end',class:'axlbl',fill:css('--text-3')}}));}});
  s.appendChild(txt(L,T-6,'파급효과 잔차',{{class:'axlbl',fill:css('--text-3')}}));
  s.appendChild(txt(W-R,H-6,'광고비중 잔차 →',{{'text-anchor':'end',class:'axlbl',fill:css('--text-3')}}));
  RES.forEach(d=>s.appendChild(mk('circle',{{cx:sx(d[1]),cy:sy(d[2]),r:3.2,fill:css('--primary'),'fill-opacity':.3,stroke:css('--primary'),'stroke-width':.8,'stroke-opacity':.55}})));
  const n=RES.length,mx2=xs.reduce((a,b)=>a+b,0)/n,my=ys.reduce((a,b)=>a+b,0)/n;
  const bb=RES.reduce((a,d)=>a+(d[1]-mx2)*(d[2]-my),0)/RES.reduce((a,d)=>a+(d[1]-mx2)**2,0);
  s.appendChild(mk('line',{{x1:sx(x0),y1:sy(my+bb*(x0-mx2)),x2:sx(x1),y2:sy(my+bb*(x1-mx2)),stroke:css('--bad'),'stroke-width':1.8,'stroke-dasharray':'5 3'}}));
  s.appendChild(txt(sx(x1)-4,sy(my+bb*(x1-mx2))-8,'r = {D['rres']:+.3f}',{{'text-anchor':'end',class:'axlbl',fill:css('--bad')}}));
}}

function drawMX(){{
  const s=document.getElementById('mx'); s.innerHTML='';
  const W=640,H=230,L=88,R=56,T=24,B=28,w=W-L-R,rh=(H-T-B)/MIXB.length;
  const mx=0.7,sx=v=>L+v/mx*w;
  [0,0.2,0.4,0.6].forEach(v=>{{s.appendChild(mk('line',{{x1:sx(v),y1:T-8,x2:sx(v),y2:H-B,stroke:css('--line'),'stroke-dasharray':'2 3'}}));
    s.appendChild(txt(sx(v),T-13,(v*100)+'%',{{'text-anchor':'middle',class:'axlbl',fill:css('--text-3')}}));}});
  MIXB.forEach((r,i)=>{{
    const y=T+i*rh+rh/2, up=r[2]>=r[1];
    s.appendChild(txt(L-8,y+4,r[0],{{'text-anchor':'end',class:'ptlbl',fill:css('--text-2')}}));
    s.appendChild(mk('rect',{{x:L,y:y-9,width:Math.max(sx(r[1])-L,1),height:8,fill:css('--text-3'),'fill-opacity':.5,rx:1}}));
    s.appendChild(mk('rect',{{x:L,y:y+2,width:Math.max(sx(r[2])-L,1),height:8,fill:up?css('--ok'):css('--bad'),rx:1}}));
    s.appendChild(txt(Math.max(sx(r[1]),sx(r[2]))+6,y+4,((r[2]-r[1])*100>=0?'+':'')+((r[2]-r[1])*100).toFixed(0)+'%p',
      {{class:'axlbl',fill:up?css('--ok'):css('--bad')}}));
  }});
  s.appendChild(mk('rect',{{x:L,y:H-16,width:9,height:9,fill:css('--text-3'),'fill-opacity':.5,rx:1}}));
  s.appendChild(txt(L+13,H-8,'페르소나 템플릿',{{class:'axlbl',fill:css('--text-3')}}));
  s.appendChild(mk('rect',{{x:L+106,y:H-16,width:9,height:9,fill:css('--ok'),rx:1}}));
  s.appendChild(txt(L+119,H-8,'광고 프로파일 혼합 후',{{class:'axlbl',fill:css('--text-3')}}));
}}
function all(){{drawDR();drawRS();drawMX();}}
all();
matchMedia('(prefers-color-scheme: dark)').addEventListener('change',all);
</script>
'''
open('/home/claude/ad-inducement.html','w',encoding='utf-8').write(head+body)
print('written',len(head+body))
