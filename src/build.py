#!/usr/bin/env python3
"""템플릿 + 데이터 → 배포용 단일 HTML.

    python src/build.py            # data/studio.json 을 src/studio.tpl.html 에 주입
                                   # → web/studio.html

템플릿의 __DATA__ 자리에 JSON 전체가 인라인된다. 외부 요청은 Google Fonts뿐이라
생성된 파일 하나만 열어도 전부 동작한다.
"""
import json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
tpl  = (ROOT / "src" / "studio.tpl.html").read_text(encoding="utf-8")
data = (ROOT / "data" / "studio.json").read_text(encoding="utf-8")

json.loads(data)                       # 깨진 JSON을 그대로 굽지 않는다
if "__DATA__" not in tpl:
    sys.exit("템플릿에 __DATA__ 자리표시자가 없습니다.")

out = ROOT / "web" / "studio.html"
out.write_text(tpl.replace("__DATA__", data), encoding="utf-8")
print(f"{out.relative_to(ROOT)}  {out.stat().st_size/1024:.0f} KB")
