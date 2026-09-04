#!/usr/bin/env python3
"""시험지 그림 생성 — 전광판/픽셀 격자(SVG)와 다층 퍼셉트론 구조도(SVG).
클래스 기반 스타일: 미리보기에서는 hex, 시험지 HTML에서는 --lm-* 토큰으로 매핑.
시험지 단 폭: (210 − 15 − 15 − 6) / 2 = 87mm → 그림 폭 ≤ 82mm."""
from pathlib import Path

OUT = Path(__file__).parent
COL_MM = 87  # 시험지 한 단의 실제 폭

# 미리보기용 hex (시험지에서는 같은 클래스명에 --lm-* 토큰을 대응)
STYLE_PREVIEW = """
<style>
  /* 격자 */
  .fg-board { fill:#D0D0D0; }                                        /* --lm-page-rule : 밝은 판 (갱지 인쇄 대비) */
  .fg-off   { fill:#1A1A1A; stroke:#FFFFFF; stroke-width:0.35; }     /* --lm-page-ink / 흰 테두리 */
  .fg-on    { fill:#FFFFFF; stroke:#1A1A1A; stroke-width:0.35; }     /* --lm-page / 검정 테두리 */
  .fg-title { font-family:'Pretendard Variable',Pretendard,'Malgun Gothic',sans-serif; font-weight:700; fill:#8F6A1F; text-anchor:middle; }  /* --lm-accent */
  .fg-title-tex { color:#8F6A1F; overflow:visible; }
  .fg-cap   { font-family:'Pretendard Variable',Pretendard,'Malgun Gothic',sans-serif; fill:#555555; text-anchor:middle; }  /* --lm-page-ink-2 */
  /* 다층 퍼셉트론 */
  .fg-node-x { fill:#EDEBD2; }   /* accent-ai-math tint */
  .fg-node-z1{ fill:#D9D5E2; }   /* accent-math2 tint */
  .fg-node-z2{ fill:#D2E0D5; }   /* accent-statistics tint */
  .fg-node-y { fill:#F0DBD4; }   /* accent-calculus tint */
  .fg-node-text{ color:#1A1A1A; overflow:visible; }
  .fg-edge-z1{ stroke:#6B4C8A; stroke-width:0.55; fill:none; stroke-linecap:round; }  /* --lm-accent-math2 */
  .fg-edge-z2{ stroke:#3F6B3E; stroke-width:0.55; fill:none; stroke-linecap:round; }  /* --lm-accent-statistics */
  .fg-edge-y { stroke:#555555; stroke-width:0.55; fill:none; stroke-linecap:round; }  /* --lm-page-ink-2 */
  .fg-w-z1{ color:#6B4C8A; overflow:visible; } .fg-w-z2{ color:#3F6B3E; overflow:visible; } .fg-w-y{ color:#1A1A1A; overflow:visible; }
</style>
"""

# ───────────────────────── 픽셀 격자 ─────────────────────────
def grid_svg(mats, titles, captions=None, cell=3.9, gap=0.65, pad=1.3, group_gap=3.5,
             title_h=5.0, cap_h=4.5, unit="mm"):
    rows = len(mats[0]); cols = len(mats[0][0])
    gw = pad*2 + cols*cell + (cols-1)*gap
    gh = pad*2 + rows*cell + (rows-1)*gap
    W = len(mats)*gw + (len(mats)-1)*group_gap
    H = title_h + gh + (cap_h if captions else 0.8)
    assert W <= COL_MM - 5, f"too wide: {W:.1f}mm"
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W:.2f}{unit}" height="{H:.2f}{unit}" viewBox="0 0 {W:.2f} {H:.2f}" role="img">']
    for gi, m in enumerate(mats):
        ox = gi*(gw+group_gap); oy = title_h
        t = titles[gi]
        if len(t) >= 2 and t[-1].isalpha() and t[-1].isupper() and t[-2] == " ":
            word, letter = t[:-1].rstrip(), t[-1]
            cxm = ox + gw/2 + 1.6   # 글자와 문자 사이 경계
            p.append(f'<text class="fg-title" x="{cxm-0.9:.2f}" y="{title_h-1.6:.2f}" style="font-size:3.4px;text-anchor:end">{word}</text>')
            svg_l, wl, hl = tex_place(letter, cxm+0.2, title_h-2.8, 3.6, "fg-title-tex", anchor="start")
            p.append(svg_l)
        else:
            p.append(f'<text class="fg-title" x="{ox+gw/2:.2f}" y="{title_h-1.6:.2f}" style="font-size:3.4px">{t}</text>')
        p.append(f'<rect class="fg-board" x="{ox:.2f}" y="{oy:.2f}" width="{gw:.2f}" height="{gh:.2f}" rx="1.0"/>')
        for r, row in enumerate(m):
            for c, ch in enumerate(row):
                x = ox + pad + c*(cell+gap); y = oy + pad + r*(cell+gap)
                cls = "fg-on" if ch == "1" else "fg-off"
                p.append(f'<rect class="{cls}" x="{x:.2f}" y="{y:.2f}" width="{cell}" height="{cell}" rx="0.45"/>')
        if captions:
            p.append(f'<text class="fg-cap" x="{ox+gw/2:.2f}" y="{oy+gh+cap_h-1.3:.2f}" style="font-size:2.8px">{captions[gi]}</text>')
    p.append('</svg>')
    return "\n".join(p)

A16 = ["01110","10000","10000","11110","10001","10001","01110"]
B16 = ["01110","10001","10001","01111","00001","00001","01110"]
P16 = ["01110","10000","00000","11110","10001","00001","01110"]
A23 = ["111","010","010"]; B23 = ["101","000","101"]; C23 = ["111","000","100"]
A24 = ["111","111","000"]; B24 = ["000","000","101"]; C24 = ["111","110","101"]

def hamming(a, b): return sum(x != y for ra, rb in zip(a, b) for x, y in zip(ra, rb))
def overlap(a, b): return sum(x == "1" and y == "1" for ra, rb in zip(a, b) for x, y in zip(ra, rb))
def ones(a): return sum(ch == "1" for r in a for ch in r)

# ───────────────────────── MathJax 라벨 (TeX → SVG 경로, 폰트 독립) ─────────────────────────
import json, subprocess, re
_TEX_CACHE = {}
def tex_svgs(texs):
    need = [t for t in texs if t not in _TEX_CACHE]
    if need:
        out = subprocess.run(["node", str(OUT / "tex2svg.mjs")], input=json.dumps(need), capture_output=True, text=True, check=True).stdout
        for k, v in json.loads(out).items():
            m = re.search(r'<svg[^>]*viewBox="([^"]+)"[^>]*>(.*)</svg>', v, flags=re.S)
            vb = [float(x) for x in m.group(1).split()]
            _TEX_CACHE[k] = (vb, m.group(2))
    return [_TEX_CACHE[t] for t in texs]

def tex_box(tex, em_mm):
    """(width_mm, height_mm, inner, viewBox) — MathJax 단위 1000 = 1em"""
    (vb, inner), = tex_svgs([tex])
    return vb[2]*em_mm/1000, vb[3]*em_mm/1000, inner, vb

def tex_place(tex, cx, cy, em_mm, cls, anchor="middle"):
    w, h, inner, vb = tex_box(tex, em_mm)
    x = cx - w/2 if anchor == "middle" else cx
    return (f'<svg class="{cls}" x="{x:.2f}" y="{cy-h/2:.2f}" width="{w:.2f}" height="{h:.2f}" '
            f'viewBox="{vb[0]} {vb[1]} {vb[2]} {vb[3]}">{inner}</svg>'), w, h

# ───────────────────────── 다층 퍼셉트론 구조도 ─────────────────────────
def mlp_svg(w_hidden, w_out, unit="mm", W=80, H=44):
    """w_hidden: [(w1,w2) for z1, (w1,w2) for z2], w_out: (w1,w2) for y. 간선 색은 도착 노드 기준.
    라벨 배치(샘플 캡처): 직선 간선은 중앙 바깥쪽, 교차 간선 두 개는 교차점 오른쪽 쐐기 안
    (z1·z2 사이)에 위아래로 — 각각 자기 선의 안쪽에 붙임."""
    xs = {"x1": (9, 8), "x2": (9, 34)}
    zs = {"z1": (38, 8), "z2": (38, 34)}
    ys = {"y": (71, 21)}
    r = 4.4; EM = 3.4; CLR = 0.7
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}{unit}" height="{H}{unit}" viewBox="0 0 {W} {H}" role="img">']

    def edge(a, b, cls):
        (x1, y1), (x2, y2) = a, b
        dx, dy = x2-x1, y2-y1; L = (dx*dx+dy*dy)**0.5; ux, uy = dx/L, dy/L
        p.append(f'<line class="fg-edge-{cls}" x1="{x1+ux*r:.2f}" y1="{y1+uy*r:.2f}" x2="{x2-ux*r:.2f}" y2="{y2-uy*r:.2f}"/>')
    def line_y(a, b, x):
        (x1, y1), (x2, y2) = a, b
        return y1 + (y2-y1)*(x-x1)/(x2-x1)
    def wtex(sub, val): return f"w_{sub}={val}"
    def label_mid(a, b, tex, cls, side, t=0.5):
        """직선/완만한 간선: 중앙에서 법선 방향으로 띄움 (수평 상자가 선을 넘지 않게 자동 계산)"""
        (x1, y1), (x2, y2) = a, b
        dx, dy = x2-x1, y2-y1; L = (dx*dx+dy*dy)**0.5; ux, uy = dx/L, dy/L
        w, h, _, _ = tex_box(tex, EM)
        off = (w/2)*abs(uy) + (h/2)*abs(ux) + CLR
        cx, cy = x1+dx*t, y1+dy*t
        svg, _, _ = tex_place(tex, cx + (-uy)*off*side, cy + ux*off*side, EM, cls)
        p.append(svg)
    def label_wedge(a, b, tex, cls, below, x_left):
        """교차 간선: 왼쪽 끝 x_left에서 시작하는 수평 라벨을 선의 안쪽(below=True: 선 아래)에 붙임"""
        w, h, _, _ = tex_box(tex, EM)
        yl = line_y(a, b, x_left)
        cy = yl + (h/2 + CLR) if below else yl - (h/2 + CLR)
        svg, _, _ = tex_place(tex, x_left, cy, EM, cls, anchor="start")
        p.append(svg)

    (a1, a2), (b1, b2) = w_hidden
    c1, c2 = w_out
    edge(xs["x1"], zs["z1"], "z1"); edge(xs["x2"], zs["z1"], "z1")
    edge(xs["x1"], zs["z2"], "z2"); edge(xs["x2"], zs["z2"], "z2")
    edge(zs["z1"], ys["y"], "y");   edge(zs["z2"], ys["y"], "y")
    label_mid(xs["x1"], zs["z1"], wtex(1, a1), "fg-w-z1", side=-1)
    label_wedge(xs["x2"], zs["z1"], wtex(2, a2), "fg-w-z1", below=True,  x_left=30.5)   # 오르는 선 아래
    label_wedge(xs["x1"], zs["z2"], wtex(1, b1), "fg-w-z2", below=False, x_left=30.5)   # 내리는 선 위
    label_mid(xs["x2"], zs["z2"], wtex(2, b2), "fg-w-z2", side=+1)
    label_mid(zs["z1"], ys["y"], wtex(1, c1), "fg-w-y", side=-1, t=0.45)
    label_mid(zs["z2"], ys["y"], wtex(2, c2), "fg-w-y", side=+1, t=0.45)
    for name, (cx, cy) in {**xs, **zs, **ys}.items():
        cls = {"x1": "x", "x2": "x", "z1": "z1", "z2": "z2", "y": "y"}[name]
        p.append(f'<circle class="fg-node-{cls}" cx="{cx}" cy="{cy}" r="{r}"/>')
        tex = f"{name[0]}_{name[1:]}" if len(name) > 1 else name
        svg, _, _ = tex_place(tex, cx, cy, 4.4, "fg-node-text")
        p.append(svg)
    p.append('</svg>')
    return "\n".join(p)

figs = {
    "fig16_digits.svg": grid_svg([A16, B16, P16], ["이미지 A", "이미지 B", "이미지 P"], ["숫자 6", "숫자 9", "일부만 표시된 숫자"]),
    "fig23_images.svg": grid_svg([A23, B23, C23], ["이미지 A", "이미지 B", "이미지 C"], None, cell=5.2, gap=0.8, pad=1.6, group_gap=6),
    "fig24_images.svg": grid_svg([A24, B24, C24], ["이미지 A", "이미지 B", "이미지 C"], None, cell=5.2, gap=0.8, pad=1.6, group_gap=6),
    "fig20_mlp.svg": mlp_svg([(3, -2), (-1, 2)], (2, -3)),
    "fig21_mlp.svg": mlp_svg([(6, 5), (3, 2)], (5, "b")),
}
for name, svg in figs.items():
    (OUT / name).write_text(svg, encoding="utf-8")

print("16:", "H(P,A)=", hamming(P16, A16), "H(P,B)=", hamming(P16, B16))
print("23:", "|A|=", ones(A23), "|B|=", ones(B23), "C∩A=", overlap(C23, A23), "C∩B=", overlap(C23, B23), "H(C,A)=", hamming(C23, A23), "H(C,B)=", hamming(C23, B23))
print("24:", "|A|=", ones(A24), "|B|=", ones(B24), "C∩A=", overlap(C24, A24), "C∩B=", overlap(C24, B24), "H(C,A)=", hamming(C24, A24), "H(C,B)=", hamming(C24, B24))

body = ['<!DOCTYPE html><html lang="ko"><head><meta charset="utf-8"><title>시험지 그림 미리보기</title>',
        '<script>window.MathJax={tex:{inlineMath:[["$","$"],["\\(","\\)"]]}};</script>',
        '<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js" async></script>', STYLE_PREVIEW,
        '<style>body{font-family:Pretendard,"Malgun Gothic",sans-serif;background:#fff;color:#1A1A1A;margin:24px;} '
        'section{margin-bottom:26px;} h2{font-size:14px;margin:0 0 8px;} '
        f'.col{{width:{COL_MM}mm;border:1px dashed #bbb;padding:2mm 0;box-sizing:border-box;}} .col svg{{display:block;margin:0 auto;}} '
        'p{font-size:12px;color:#555;margin:6px 0 0;}</style></head><body>',
        f'<p style="font-size:12px">점선 상자 = 시험지 한 단의 실제 폭 {COL_MM}mm (A4, 여백 15mm, 단 간격 6mm 기준).</p>']
for title, name, note in [
    ("16번 — 전광판 6 · 9 · P (7×5)", "fig16_digits.svg", "H(P,A)=2, H(P,B)=6 → 6으로 분류"),
    ("20번 — 다층 퍼셉트론 (h=0)", "fig20_mlp.svg", "$z_1=\\sigma(3x_1-2x_2),\\; z_2=\\sigma(-x_1+2x_2),\\; y=\\sigma(2z_1-3z_2)$ — 시험지에서는 이 식이 발문에 MathJax로 들어갑니다."),
    ("21번 — 다층 퍼셉트론 (h=4)", "fig21_mlp.svg", "$z_1=\\sigma(6x_1+5x_2),\\; z_2=\\sigma(3x_1+2x_2),\\; y=\\sigma(5z_1+b\\,z_2)$"),
    ("23번 — A · B · C", "fig23_images.svg", "$\\mathrm{P_A}=\\tfrac35,\\ \\mathrm{P_B}=\\tfrac34$ → B"),
    ("24번 — A · B · C (해밍 vs 퍼셉트론)", "fig24_images.svg", "$H(C,A)=3 \\lt H(C,B)=5$ → A  /  $\\mathrm{P_A}=\\tfrac56 \\lt \\mathrm{P_B}=1$ → B"),
]:
    body.append(f'<section><h2>{title}</h2><div class="col">{figs[name]}</div><p>{note}</p></section>')
body.append('</body></html>')
(OUT / "preview.html").write_text("\n".join(body), encoding="utf-8")
