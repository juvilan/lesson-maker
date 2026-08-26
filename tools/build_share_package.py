"""공유용 오프라인 패키지를 만든다.

덱 HTML은 공유 CSS(상대경로)와 CDN 자원 6개에 의존한다. HTML만 건네면
디자인이 전부 죽고, 학교 망이 CDN을 막으면 수식도 깨진다.
이 스크립트는 그 의존을 전부 폴더 안으로 끌어와 인터넷 없이 열리게 만든다.

출력 구조 (dist/공유용/):
    _assets/templates/design-tokens.css
    _assets/templates/slide-system.css
    _assets/fonts/PretendardVariable.woff2   <- design-tokens.css 가 ../fonts/ 로 찾는다
    _assets/reveal/{reset.css,reveal.css,reveal.js,notes.js}
    _assets/gsap.min.js
    _assets/mathjax/tex-chtml.js
    _assets/mathjax/output/chtml/fonts/woff-v2/*.woff
    슬라이드_*.html
    읽어보세요.txt

CSS 를 _assets/templates/ 에 두는 것이 핵심이다. 평평하게 펴면
design-tokens.css 의 url('../fonts/...') 가 깨져 폰트가 404 난다.

실행: powershell.exe -NoProfile -Command "python tools/build_share_package.py"
(Git Bash 셸은 네트워크가 막혀 있어 PowerShell 로 실행해야 한다.)
"""
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "dist", "공유용")
ASSETS = os.path.join(OUT, "_assets")

CDN = "https://cdn.jsdelivr.net"
MJ_VER = "3.2.2"

# (원본 URL, 패키지 안 경로)
DOWNLOADS = [
    (CDN + "/npm/reveal.js@4.6.1/dist/reset.css", "reveal/reset.css"),
    (CDN + "/npm/reveal.js@4.6.1/dist/reveal.css", "reveal/reveal.css"),
    (CDN + "/npm/reveal.js@4.6.1/dist/reveal.js", "reveal/reveal.js"),
    (CDN + "/npm/reveal.js@4.6.1/plugin/notes/notes.js", "reveal/notes.js"),
    (CDN + "/npm/gsap@3.12.5/dist/gsap.min.js", "gsap.min.js"),
    (CDN + "/npm/mathjax@3/es5/tex-chtml.js", "mathjax/tex-chtml.js"),
]

# HTML 안의 참조를 패키지 경로로 바꾼다
REWRITES = [
    ("../../../_shared/templates/design-tokens.css", "_assets/templates/design-tokens.css"),
    ("../../../_shared/templates/slide-system.css", "_assets/templates/slide-system.css"),
    (CDN + "/npm/reveal.js@4.6.1/dist/reset.css", "_assets/reveal/reset.css"),
    (CDN + "/npm/reveal.js@4.6.1/dist/reveal.css", "_assets/reveal/reveal.css"),
    (CDN + "/npm/reveal.js@4.6.1/dist/reveal.js", "_assets/reveal/reveal.js"),
    (CDN + "/npm/reveal.js@4.6.1/plugin/notes/notes.js", "_assets/reveal/notes.js"),
    (CDN + "/npm/gsap@3.12.5/dist/gsap.min.js", "_assets/gsap.min.js"),
    (CDN + "/npm/mathjax@3/es5/tex-chtml.js", "_assets/mathjax/tex-chtml.js"),
]

MJ_FONT_DIR = "_assets/mathjax/output/chtml/fonts/woff-v2"

DECK_GLOBS = [
    ("ai-math/output/slides", re.compile(r"^슬라이드_III-1-.*\.html$")),
    ("ai-math/output/slides", re.compile(r"^슬라이드_III-2-.*\.html$")),
    ("ai-math-2022/output/slides", re.compile(r"^슬라이드_[12]-.*\.html$")),
]


def fetch(url):
    """urllib 을 먼저 쓰고, 실패하면 PowerShell 로 넘긴다.

    맥에서는 urllib 이 그대로 된다.
    윈도우 업무용 노트북에서는 urllib 이 SSL 검증에 실패하므로
    (CERTIFICATE_VERIFY_FAILED: Missing Authority Key Identifier)
    Windows 인증서 저장소를 쓰는 PowerShell 로 넘긴다.
    **검증을 끄지는 않는다** — 남에게 배포할 파일이다.
    """
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "lesson-maker-bundler"})
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.read()
    except Exception as e:
        if os.name != "nt":
            raise RuntimeError("다운로드 실패: %s\n%s" % (url, e))
    return fetch_via_powershell(url)


def fetch_via_powershell(url):
    fd, tmp = tempfile.mkstemp(suffix=".bin")
    os.close(fd)
    try:
        cmd = [
            "powershell.exe", "-NoProfile", "-Command",
            "$ProgressPreference='SilentlyContinue'; "
            "Invoke-WebRequest -Uri '%s' -OutFile '%s' -TimeoutSec 60 -UseBasicParsing"
            % (url, tmp.replace("\\", "\\\\")),
        ]
        r = subprocess.run(cmd, capture_output=True)
        if r.returncode != 0 or not os.path.getsize(tmp):
            raise RuntimeError(
                "다운로드 실패: %s\n%s" % (url, r.stderr.decode("utf-8", "replace"))
            )
        with open(tmp, "rb") as f:
            return f.read()
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)


def write_bytes(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(data)


def mathjax_font_list():
    """jsdelivr API 로 MathJax CHTML 폰트 파일 목록을 받는다."""
    url = "https://data.jsdelivr.com/v1/packages/npm/mathjax@%s?structure=flat" % MJ_VER
    data = json.loads(fetch(url).decode("utf-8"))
    return [f["name"] for f in data["files"]
            if "output/chtml/fonts/woff-v2/" in f["name"]]


def collect_decks():
    out = []
    for rel, pat in DECK_GLOBS:
        d = os.path.join(ROOT, rel)
        for name in sorted(os.listdir(d)):
            if pat.match(name):
                out.append(os.path.join(d, name))
    return out


def rewrite_html(raw):
    """참조 경로를 바꾸고 MathJax 에 로컬 폰트 위치를 알려 준다."""
    notes = []
    for src, dst in REWRITES:
        if src in raw:
            raw = raw.replace(src, dst)
        else:
            notes.append("참조 없음: " + src)

    # MathJax 스크립트에서 async 를 뗀다.
    #
    # 덱의 safeTypeset() 은 MathJax 가 아직 없으면 조용히 아무 일도 안 하고
    # 끝난다. 원본은 CDN 에서 받느라 느려 Reveal 의 ready 보다 MathJax 가 먼저
    # 준비됐지만, 자원을 전부 로컬로 옮기면 순서가 뒤바뀌어 수식이 하나도
    # 조판되지 않는다(실제로 2-3-3 에서 mjx-container 0개로 확인). 오류도
    # 경고도 없이 수식만 사라지므로 알아채기 어렵다.
    # 로컬 파일이라 동기 로드해도 체감 지연이 없다.
    raw = raw.replace('id="MathJax-script" async>', 'id="MathJax-script">')

    # MathJax 는 폰트를 따로 받아간다. fontURL 을 주지 않으면 조용히 CDN 으로 간다
    # — 온라인에서는 멀쩡해 보이고 막힌 망에서만 깨지므로 반드시 확인해야 한다.
    if "fontURL" in raw:
        notes.append("fontURL 이미 있음 — 건드리지 않음")
    else:
        new, n = re.subn(
            r"chtml:\s*\{\s*scale:\s*1\.0\s*\}",
            "chtml: { scale: 1.0, fontURL: '%s' }" % MJ_FONT_DIR,
            raw,
        )
        if n == 1:
            raw = new
        else:
            notes.append("!! chtml 설정을 못 찾음 (치환 %d건) — 수식 폰트가 CDN 으로 샌다" % n)
    return raw, notes


def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT, exist_ok=True)

    print("== 공유 CSS·폰트 복사 ==")
    for src, dst in [
        ("_shared/templates/design-tokens.css", "templates/design-tokens.css"),
        ("_shared/templates/slide-system.css", "templates/slide-system.css"),
        ("_shared/fonts/PretendardVariable.woff2", "fonts/PretendardVariable.woff2"),
        ("_shared/fonts/LICENSE", "fonts/LICENSE"),
    ]:
        s = os.path.join(ROOT, src)
        d = os.path.join(ASSETS, dst)
        os.makedirs(os.path.dirname(d), exist_ok=True)
        shutil.copy2(s, d)
        print("   %-46s %8d bytes" % (dst, os.path.getsize(d)))

    print("== CDN 자원 내려받기 ==")
    for url, dst in DOWNLOADS:
        data = fetch(url)
        write_bytes(os.path.join(ASSETS, dst), data)
        print("   %-46s %8d bytes" % (dst, len(data)))

    print("== MathJax 폰트 ==")
    names = mathjax_font_list()
    total = 0
    for name in names:
        data = fetch(CDN + "/npm/mathjax@" + MJ_VER + name)
        base = os.path.basename(name)
        write_bytes(os.path.join(ASSETS, "mathjax/output/chtml/fonts/woff-v2", base), data)
        total += len(data)
    print("   %d개 파일, 합계 %d bytes" % (len(names), total))

    print("== 덱 변환 ==")
    decks = collect_decks()
    problems = []
    for path in decks:
        raw = io.open(path, encoding="utf-8").read()
        new, notes = rewrite_html(raw)
        name = os.path.basename(path)
        io.open(os.path.join(OUT, name), "w", encoding="utf-8", newline="").write(new)
        left = re.findall(r"https://cdn\.jsdelivr\.net[^\"'\s)]*", new)
        if left:
            problems.append((name, "CDN 참조 잔존: " + ", ".join(sorted(set(left)))))
        for n in notes:
            if n.startswith("!!"):
                problems.append((name, n))
    print("   %d개 덱 변환" % len(decks))

    print("== 사용설명서 ==")
    metas = [read_meta(p) for p in decks]
    manual = build_manual(metas)
    io.open(os.path.join(OUT, "사용설명서.html"), "w",
            encoding="utf-8", newline="").write(manual)
    print("   사용설명서.html (%d개 차시 수록)" % len(metas))

    io.open(os.path.join(OUT, "읽어보세요.txt"), "w",
            encoding="utf-8", newline="").write(README)

    print("== 결과 ==")
    size = sum(os.path.getsize(os.path.join(dp, f))
               for dp, _, fs in os.walk(OUT) for f in fs)
    print("   %s" % OUT)
    print("   전체 %.1f MB" % (size / 1024.0 / 1024.0))
    if problems:
        print("== 확인 필요 ==")
        for name, msg in problems:
            print("   %s — %s" % (name, msg))
    else:
        print("   외부 참조 0건 — 인터넷 없이 열립니다")


RE_TITLE = re.compile(r"<title>(.*?)</title>", re.S)
RE_TAG = re.compile(r'<div class="chapter-tag">(.*?)</div>', re.S)
RE_SUB = re.compile(r'<p class="slide-sub">(.*?)</p>', re.S)
RE_META = re.compile(r'<div class="title-meta">(.*?)</div>', re.S)
RE_SPAN = re.compile(r"<span[^>]*>(.*?)</span>", re.S)
RE_TAGS = re.compile(r"<[^>]+>")


def plain(s):
    return re.sub(r"\s+", " ", RE_TAGS.sub("", s)).strip()


def read_meta(path):
    raw = io.open(path, encoding="utf-8").read()
    t = RE_TITLE.search(raw)
    title, grade = "", ""
    if t:
        parts = plain(t.group(1)).split("|")
        title = parts[0].strip()
        grade = parts[1].strip() if len(parts) > 1 else ""
    tag = RE_TAG.search(raw)
    sub = RE_SUB.search(raw)
    book = ""
    mm = RE_META.search(raw)
    if mm:
        spans = [plain(x) for x in RE_SPAN.findall(mm.group(1))]
        book = next((s for s in spans if "교과서" in s), "")
    return {
        "file": os.path.basename(path),
        "title": title,
        "grade": grade,
        "tag": plain(tag.group(1)) if tag else "",
        "sub": plain(sub.group(1)) if sub else "",
        "book": book,
        "n": len(re.findall(r"<section\b", raw)),
    }


# 파일 이름 앞부분 -> (묶음 제목, 설명)
GROUPS = [
    ("슬라이드_1-", "2학년 · Ⅰ단원 인공지능과 빅데이터",
     "인공지능이 무엇인지, 어떻게 배우는지, 그 재료인 빅데이터는 무엇인지"),
    ("슬라이드_2-", "2학년 · Ⅱ단원 텍스트 데이터 처리",
     "말을 수로 바꾸고, 세고, 견주는 방법 — 표현에서 분석까지"),
    ("슬라이드_III-1-", "3학년 · Ⅲ-1 자료의 분류",
     "닮음을 재는 잣대와 퍼셉트론, 그리고 이미지 분류"),
    ("슬라이드_III-2-", "3학년 · Ⅲ-2 경향성과 예측",
     "확률로 예측하기, 산점도와 추세선, 그리고 오차"),
]


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def build_manual(metas):
    blocks = []
    for prefix, heading, desc in GROUPS:
        rows = [m for m in metas if m["file"].startswith(prefix)]
        if not rows:
            continue
        tr = []
        for m in rows:
            tr.append(
                '<tr><td class="lesson"><a href="{f}">{t}</a>'
                '<span class="sub">{s}</span></td>'
                '<td class="book">{b}</td><td class="cnt">{n}장</td></tr>'.format(
                    f=esc(m["file"]), t=esc(m["title"]),
                    s=esc(m["sub"]), b=esc(m["book"]), n=m["n"])
            )
        blocks.append(
            '<section class="unit"><h2>{h}</h2><p class="udesc">{d}</p>'
            '<table class="lessons"><thead><tr><th>차시</th><th>교과서</th>'
            '<th>분량</th></tr></thead><tbody>{rows}</tbody></table></section>'.format(
                h=esc(heading), d=esc(desc), rows="".join(tr))
        )
    total_slides = sum(m["n"] for m in metas)
    return (MANUAL
            .replace("{{BLOCKS}}", "".join(blocks))
            .replace("{{NDECK}}", str(len(metas)))
            .replace("{{NSLIDE}}", str(total_slides)))


README = """인공지능수학 수업 슬라이드 — 공유용 꾸러미
==========================================

■ 먼저 '사용설명서.html' 을 여세요
   수업 목록, 조작법, 문제 해결이 전부 정리돼 있습니다.

■ 여는 법
   폴더를 통째로 푼 다음, 원하는 '슬라이드_....html' 을 더블클릭하면 됩니다.
   크롬으로 여는 것을 권합니다.

■ 인터넷이 필요 없습니다
   글꼴, 수식(MathJax), 슬라이드 엔진(reveal.js)까지 모두 이 폴더 안에
   들어 있습니다. 학교 망이 외부 사이트를 막아도 그대로 열립니다.

■ 폴더를 통째로 두세요  ★중요★
   '_assets' 폴더에 디자인과 글꼴이 들어 있습니다.
   HTML 파일만 따로 빼내면 글꼴과 색이 전부 사라지고
   맹숭맹숭한 기본 글씨로 보입니다. 옮길 때는 폴더째 옮겨 주세요.

■ 슬라이드 조작
   →, ←  또는  Space   다음/이전
   F                   전체 화면
   S                   발표자 노트 창 (수업 진행 설명이 들어 있습니다)
   Esc                 전체 슬라이드 한눈에 보기
   화면 안의 버튼·문항은 눌러야 다음 단계가 나옵니다.

■ 화면 크기
   1920x1080 기준으로 만들었습니다. 창 크기에 맞춰 자동으로 줄어듭니다.
"""


MANUAL = """<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>사용설명서 | 인공지능수학 수업 슬라이드</title>
<link rel="stylesheet" href="_assets/templates/design-tokens.css">
<style>
  :root { color-scheme: light; }
  body { margin: 0; background: var(--lm-paper); color: var(--lm-ink);
         font-family: var(--lm-font-sans);
         word-break: keep-all; overflow-wrap: break-word; text-wrap: pretty;
         line-height: 1.75; }
  .wrap { max-width: 860px; margin: 0 auto; padding: 64px 28px 96px; }
  header { border-bottom: 3px solid var(--lm-accent); padding-bottom: 28px; margin-bottom: 44px; }
  .eyebrow { color: var(--lm-accent); font-weight: 700; letter-spacing: .04em; font-size: 15px; }
  h1 { font-size: 40px; margin: 10px 0 8px; letter-spacing: -0.02em; font-weight: 700; }
  .lead { color: var(--lm-ink-2); font-size: 18px; margin: 0; }
  .scale { margin-top: 18px; color: var(--lm-ink-3); font-size: 15px; }
  h2 { font-size: 25px; margin: 48px 0 14px; padding-bottom: 8px;
       border-bottom: 1px solid var(--lm-rule); text-wrap: balance; }
  h3 { font-size: 19px; margin: 28px 0 8px; }
  p, li { font-size: 16.5px; color: var(--lm-ink-2); }
  ol, ul { padding-left: 22px; }
  li { margin: 6px 0; }
  b, strong { color: var(--lm-ink); }
  code { background: var(--lm-paper-tint); border: 1px solid var(--lm-rule);
         border-radius: 5px; padding: 1px 6px; font-size: 14.5px;
         font-family: Consolas, "D2Coding", monospace; }
  .callout { border-left: 5px solid var(--lm-accent); background: var(--lm-accent-tint);
             padding: 18px 22px; border-radius: 0 8px 8px 0; margin: 22px 0; }
  .callout.warn { border-color: var(--lm-danger, #b4413c); background: var(--lm-danger-tint, #fbeceb); }
  .callout p:first-child { margin-top: 0; }
  .callout p:last-child { margin-bottom: 0; }
  .callout .h { display: block; font-weight: 700; color: var(--lm-ink); margin-bottom: 6px; }
  table { width: 100%; border-collapse: collapse; margin: 16px 0 8px; }
  th { text-align: left; font-size: 14px; color: var(--lm-ink-3); font-weight: 600;
       border-bottom: 2px solid var(--lm-rule-strong); padding: 8px 10px; }
  td { border-bottom: 1px solid var(--lm-rule); padding: 11px 10px;
       vertical-align: top; font-size: 16px; color: var(--lm-ink-2); }
  .keys td:first-child { width: 210px; }
  .keys kbd { display: inline-block; background: var(--lm-page);
              border: 1px solid var(--lm-rule-strong); border-bottom-width: 2px;
              border-radius: 6px; padding: 2px 9px; font-size: 14px;
              font-family: inherit; color: var(--lm-ink); }
  .unit { margin-top: 40px; }
  .udesc { color: var(--lm-ink-3); font-size: 15px; margin: 2px 0 4px; }
  .lessons td.lesson { width: auto; }
  .lessons td.book { width: 130px; color: var(--lm-ink-3); font-size: 14.5px; white-space: nowrap; }
  .lessons td.cnt { width: 62px; color: var(--lm-ink-3); font-size: 14.5px; text-align: right; }
  .lessons a { color: var(--lm-accent); font-weight: 700; text-decoration: none;
               font-size: 17px; }
  .lessons a:hover { text-decoration: underline; }
  .lessons .sub { display: block; color: var(--lm-ink-3); font-size: 14.5px;
                  margin-top: 3px; font-weight: 400; }
  .fix td:first-child { width: 240px; color: var(--lm-ink); font-weight: 600; }
  footer { margin-top: 64px; padding-top: 22px; border-top: 1px solid var(--lm-rule);
           color: var(--lm-ink-3); font-size: 14px; }
  @media print { .wrap { max-width: none; padding: 0; } a { color: inherit; } }
</style>
</head>
<body>
<div class="wrap">

<header>
  <div class="eyebrow">사용설명서</div>
  <h1>인공지능수학 수업 슬라이드</h1>
  <p class="lead">교실에서 바로 띄워 쓰는 수업용 슬라이드 꾸러미입니다.</p>
  <p class="scale">{{NDECK}}개 차시 · 슬라이드 {{NSLIDE}}장 · 인터넷 연결이 필요하지 않습니다</p>
</header>

<h2>1. 여는 법</h2>
<ol>
  <li>받은 압축 파일을 <b>폴더째 풀어 주세요.</b></li>
  <li>아래 <b>수업 목록</b>에서 원하는 차시를 누르거나,
      폴더에서 <code>슬라이드_....html</code> 파일을 더블클릭합니다.</li>
  <li><b>크롬(Chrome)</b>을 권합니다. 다른 브라우저에서도 열리지만
      화면이 조금 다르게 보일 수 있습니다.</li>
</ol>

<div class="callout warn">
  <span class="h">★ 폴더를 통째로 두세요</span>
  <p><code>_assets</code> 폴더에 글꼴과 디자인, 수식 엔진이 들어 있습니다.
  <b>HTML 파일 하나만 따로 빼내면</b> 글꼴과 색이 모두 사라지고
  밋밋한 기본 글씨로 보입니다. 옮기거나 다시 보낼 때는 반드시 폴더째 옮겨 주세요.</p>
</div>

<h2>2. 인터넷이 없어도 됩니다</h2>
<p>글꼴, 수식 엔진(MathJax), 슬라이드 엔진(reveal.js)을 모두 폴더 안에 넣어 두었습니다.
학교 망이 외부 사이트를 막고 있어도, 인터넷이 끊겨 있어도 그대로 열립니다.
USB에 담아 다녀도 됩니다.</p>

<h2>3. 슬라이드 조작</h2>
<table class="keys">
  <thead><tr><th>키</th><th>하는 일</th></tr></thead>
  <tbody>
    <tr><td><kbd>→</kbd> <kbd>←</kbd> 또는 <kbd>Space</kbd></td><td>다음 / 이전 슬라이드</td></tr>
    <tr><td><kbd>F</kbd></td><td>전체 화면 (수업할 때는 이 상태로)</td></tr>
    <tr><td><kbd>S</kbd></td><td><b>발표자 노트 창</b> — 아래 4번 참고</td></tr>
    <tr><td><kbd>Esc</kbd> 또는 <kbd>O</kbd></td><td>전체 슬라이드를 한눈에 보기 · 원하는 장으로 건너뛰기</td></tr>
    <tr><td><kbd>B</kbd> 또는 <kbd>.</kbd></td><td>화면을 잠시 까맣게 (칠판으로 시선을 돌릴 때)</td></tr>
  </tbody>
</table>
<p>슬라이드 안의 <b>버튼과 문항은 눌러야 다음 내용이 나옵니다.</b>
단계별 풀이는 버튼을 눌러 한 단계씩 열고, 확인 활동의 문항은 문항을 누르면 답이 나타납니다.
답이 나올 자리는 미리 비워 두었으므로 눌러도 화면이 밀리지 않습니다.</p>

<h2>4. 발표자 노트에 수업 진행이 들어 있습니다</h2>
<p><kbd>S</kbd>를 누르면 창이 하나 더 열립니다. 거기에는 그 장에서
<b>무엇을 강조할지, 학생들이 어디서 틀리는지, 어떤 질문을 던질지</b>가 적혀 있습니다.
슬라이드 화면에는 나오지 않으니 수업 전에 한 번 훑어보시길 권합니다.</p>
<div class="callout">
  <p>노트 창이 안 열리면 브라우저의 <b>팝업 차단</b> 때문입니다.
  주소창 오른쪽 끝의 팝업 차단 아이콘을 눌러 허용해 주세요.</p>
</div>

<h2>5. 수업 목록</h2>
<p>차시 제목을 누르면 바로 열립니다.</p>
{{BLOCKS}}

<h2>6. 이럴 때는</h2>
<table class="fix">
  <thead><tr><th>증상</th><th>이유와 해결</th></tr></thead>
  <tbody>
    <tr><td>글씨체가 밋밋하고<br>색이 안 나온다</td>
        <td>HTML 파일만 따로 옮긴 경우입니다. <code>_assets</code> 폴더가 같은 자리에
            있어야 합니다. 압축 파일을 폴더째 다시 풀어 주세요.</td></tr>
    <tr><td>수식이 <code>\\(x^2\\)</code> 처럼<br>글자로 보인다</td>
        <td>수식 엔진이 아직 다 안 읽힌 것입니다. 잠시 기다렸다가
            <kbd>F5</kbd>로 새로 고쳐 주세요.</td></tr>
    <tr><td>글씨가 너무 작다</td>
        <td>창 크기에 맞춰 자동으로 줄어듭니다. <kbd>F</kbd>로 전체 화면을 켜면
            가장 크게 보입니다.</td></tr>
    <tr><td>발표자 노트가 안 열린다</td>
        <td>팝업 차단을 해제해 주세요.</td></tr>
    <tr><td>내용을 고치고 싶다</td>
        <td>HTML 파일이라 메모장으로도 열립니다. 다만 <b>원본을 복사해 두고</b>
            고치시길 권합니다.</td></tr>
  </tbody>
</table>

<h2>7. 인쇄 · PDF로 만들기</h2>
<p>주소 끝에 <code>?print-pdf</code>를 붙이고 (예:
<code>슬라이드_2-1-1차시_....html?print-pdf</code>)
<kbd>Ctrl</kbd>+<kbd>P</kbd>를 누르면 슬라이드가 한 장씩 인쇄됩니다.
용지 방향은 <b>가로</b>, 여백은 <b>없음</b>, <b>배경 그래픽</b>을 켜 주세요.</p>

<footer>
  이 꾸러미의 슬라이드는 1920&times;1080 기준으로 만들어졌고, 창 크기에 맞춰 자동으로 축소됩니다.<br>
  본문 글꼴은 Pretendard (SIL Open Font License 1.1) —
  라이선스 전문은 <code>_assets/fonts/LICENSE</code> 에 함께 넣어 두었습니다.
</footer>

</div>
</body>
</html>
"""


if __name__ == "__main__":
    main()
