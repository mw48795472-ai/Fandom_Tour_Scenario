# 팬덤루트랩 (FandomRouteLab)

K-팬덤의 지역관광 파급효과 분석을 **지자체가 실제로 쓸 수 있는 관광상품 개발 도구**로 옮긴 프로토타입입니다.
지역을 고르면 100개 팬덤을 `RegionFit`으로 스코어링하고, 고른 팬덤의 소비성향에 맞춰 일정을 짜고,
상품 명세서까지 내려갑니다.

> 2026 문화체육관광 통계 활용대회 · 팀 데이터오름 · 서목원

---

## 바로 열어보기

| 파일 | 내용 |
|---|---|
| [`web/studio.html`](web/studio.html) | **관광상품 개발 콘솔** — 지역 선택 → 팬덤 후보 → 상품 설계 → 명세서 (4단계) |
| [`web/plan.html`](web/plan.html) | 서비스 실현방안 보고서 — 3개 모듈(매칭 / 루트 스튜디오 / 전환 원장) |
| [`web/spec.html`](web/spec.html) | 상세명세서 — 테이블 스키마 14종, 산식, API 규격, 화면 명세 |
| [`web/reports/v0.5-affinity-redesign.html`](web/reports/v0.5-affinity-redesign.html) | 연고밀착도 재설계 보고 |
| [`web/reports/v0.6-language-index.html`](web/reports/v0.6-language-index.html) | 언어지수 검정 — 보조지표 강등 |
| [`web/reports/v0.7-ad-inducement.html`](web/reports/v0.7-ad-inducement.html) | 광고지수 유발계수 검증 |

모두 **단일 HTML**입니다. 빌드 없이 브라우저로 바로 열립니다 (외부 요청은 Google Fonts 하나뿐).

---

## 이 저장소가 지키려 한 원칙

이 프로젝트는 지표를 만들 때마다 같은 절차를 밟았습니다.

1. **임의 상수를 쓰지 않는다.** 축소 강도(α)·사전분포(π) 같은 모수는 전부 자료에서 경험베이즈로 추정합니다.
   "중앙값을 쓴다" 같은 관례도 추정값으로 대체했습니다.
2. **새 지표는 먼저 검정한다.** 기저모형 `성과 ~ 근거문장수`에 변수를 더했을 때의 증분 설명력(ΔR²)을 봅니다.
   코퍼스 분량이 성과의 81%를 설명하므로, 단순 상관은 거의 자동으로 양수가 나옵니다.
3. **검정을 통과하지 못한 지표는 강등한다.** 언어지수는 이 절차에서 가중치가 0.150 → 0.014로 내려갔습니다.
4. **모르는 것은 0으로 채우지 않는다.** 미수집과 0건을 구분하고, 산출 불가 지역은 항을 제외한 뒤 재정규화합니다.
5. **실존 인물의 사실을 지어내지 않는다.** 멤버 연고는 결과보고서에 명시된 2건만, 공연 이력은 출처 URL이 있는 것만 등록했습니다.

자세한 내용: [`docs/MODEL.md`](docs/MODEL.md) · [`docs/DATA.md`](docs/DATA.md) · [`docs/VALIDATION.md`](docs/VALIDATION.md)

---

## 저장소 구조

```
web/                    배포용 단일 HTML (그대로 열면 됨)
  studio.html           콘솔 — src/build.py 로 생성
  plan.html  spec.html  보고서 예시 · 상세명세서
  reports/              모델 개정 보고 v0.5 ~ v0.7

src/
  studio.tpl.html       콘솔 템플릿 (__DATA__ 자리에 데이터 주입)
  build.py              템플릿 + data/studio.json → web/studio.html
  pipeline/             지표 산출 스크립트
  reports/              개정 보고서 생성 스크립트

data/
  studio.json           콘솔에 주입되는 통합 데이터
  artist_show_history_v1.csv   공연이력 리서치 결과 (713건 + 무기록 6팀)
  raw/                  원자료 (지역·언어·광고 지수 v7, 카드소비 LQ·EQ)
  research/             공연이력 리서치 원본 TSV (배치 b1~b11) + 수집 규격
  derived/              중간 산출물 (경험베이즈 추정 결과 등)

docs/
  MODEL.md              RegionFit 산식과 버전 이력
  DATA.md               데이터 계보와 정합성 검사 결과
  VALIDATION.md         검정 결과 모음
```

## 다시 빌드하기

```bash
python3 src/build.py          # data/studio.json → web/studio.html
```

파이프라인 스크립트는 `data/raw/` 를 읽어 `data/derived/` 를 만들고,
`src/pipeline/mk17.py` 가 최종적으로 `data/studio.json` 을 조립합니다.
스크립트 안의 경로는 작업 당시 기준이라 그대로 돌리려면 경로 조정이 필요합니다 —
산출물은 `data/derived/` 에 모두 들어 있으므로 재현 없이도 검증할 수 있습니다.

필요 패키지: `numpy`, `scipy` (경험베이즈 추정). 콘솔 자체는 의존성이 없습니다.

## 원자료 출처

- **지역·언어·광고 지수 v7** — 결과보고서의 LDA 토픽모델링 산출물 (100개 팬덤)
- **카드소비 LQ·EQ** — 한국관광 데이터랩 계열 카드소비 실측 (시도 17 · 시군구 229 · 5개 소비영역, 2024~2025)
- **공연 이력** — 웹 리서치 (2024-01-01 ~ 2026-09-18 국내 공연). 레코드마다 출처 URL·신뢰도 등급 보유.
  KOPIS 오픈API는 서비스키 발급이 필요해 직접 조회하지 못했습니다 — 공식 공연목록이 확보되면 동일 규격으로 대체됩니다.
- **DID 실측** — 결과보고서 4장 (BTS·임영웅 콘서트 6건)

결과보고서 PDF 원본은 이 저장소에 포함하지 않았습니다.

## 연계 계획 (미수집)

- **TourAPI 4.0** (한국관광공사) — 관광지 상세·좌표·운영시간. 콘솔에 수집 대기 상태로 표기됨
- **KOPIS** (예술경영지원센터) — 공연목록·공연통계·공연시설 좌석수
- **외래관광객 조사** — 지역별 국적 구성. 해외확산도를 실제 언어적합도로 승격하는 데 필요

각 항목의 현재 수집 상태는 콘솔 1단계 화면에 그대로 표시됩니다.
