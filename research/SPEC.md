# 출력 규격 (TSV, 탭 구분, 헤더 포함)
artist	title	venue	sido	sgg	start	end	n	type	conf	source

- artist : 지시받은 표기 그대로 (예: "리센느(RESCENE)", "지드래곤 (G-Dragon)")
- title  : 공연명 원문
- venue  : 공연장명 (모르면 빈칸)
- sido   : 서울/부산/대구/인천/광주/대전/울산/세종/경기/강원/충북/충남/전북/전남/경북/경남/제주 중 하나
- sgg    : 시군구 (모르면 빈칸)
- start,end : YYYY-MM-DD (하루면 둘 다 같은 값, 모르면 빈칸)
- n      : 해당 지역 공연 회차(일수). 모르면 빈칸
- type   : 콘서트 / 팬미팅 / 페스티벌출연 / 단독공연 / 기타
- conf   : A = 공연명·도시·날짜가 공식 발표·티켓처·위키 투어문서에 명시
           B = 언론 보도로 도시와 시기 확인, 날짜 일부 불명
           C = 도시만 확인, 날짜 불명
- source : URL 하나 (필수)
