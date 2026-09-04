#!/usr/bin/env python3
"""2026-2학기 중간고사 인공지능 수학 시험지 HTML 생성 (lesson-maker exam_composer 규격)
- CSS: ../../../_shared/templates/{design-tokens,worksheet-system}.css
- 2단 ws-body, 발문 끝 [N점], OMR 전제(답란 없음), 그림은 인라인 SVG(fg-* 클래스 → --lm-* 토큰)
사용: python3 build_exam.py [--local]   (--local: 로컬 검증용 MathJax 경로)
"""
import sys, re
from pathlib import Path

HERE = Path(__file__).parent
FIG = HERE / "figures"
LOCAL = "--local" in sys.argv


_MATH_SPLIT = re.compile(r'(\$[^$]*\$)')
_LETTER = re.compile(r'(?<![A-Za-z0-9_\\{])([ABCDPQX])(?![A-Za-z0-9_])')
def it(text):
    """수식 밖에 홀로 쓰인 대상 이름(이미지 A, 텍스트 P, 학생 B …)을 교과서 관행대로 수학 이탤릭 $A$로 통일.
    $…$ 안은 건드리지 않음. AND/XOR/OMR 같은 단어는 뒤에 글자가 이어져 제외됨."""
    parts = _MATH_SPLIT.split(text)
    return "".join(p if p.startswith("$") else _LETTER.sub(r"$\1$", p) for p in parts)

def fig(name):
    """SVG 파일을 인라인으로. 폭은 mm 그대로, 문항 안에서 가운데 정렬."""
    svg = (FIG / name).read_text(encoding="utf-8")
    return f'<div class="ws-figure">{svg}</div>'

def choices(items):
    marks = "①②③④⑤"
    return '<ol class="ws-choices">' + "".join(f"<li>{m} {it(c)}</li>" for m, c in zip(marks, items)) + "</ol>"

def table(head, rows, first_col_left=False):
    th = "".join((f'<th class="left nw">{it(h)}</th>' if (first_col_left and i == 0) else f"<th>{it(h)}</th>") for i, h in enumerate(head))
    body = ""
    for r in rows:
        tds = "".join(f'<td class="left nw">{it(c)}</td>' if (first_col_left and i == 0) else f"<td>{it(c)}</td>" for i, c in enumerate(r))
        body += f"<tr>{tds}</tr>"
    return f'<table class="ws-table"><thead><tr>{th}</tr></thead><tbody>{body}</tbody></table>'

def bogi(*lines):
    return '<aside class="ws-info"><strong>&lt;보기&gt;</strong><br>' + "<br>".join(it(l) for l in lines) + "</aside>"

def problem(n, pts, stem, extra="", chs=None):
    body = f'<div class="ws-problem-body"><span class="ws-problem-number">{n}.</span>{it(stem)} <span class="ws-problem-points">[{pts}점]</span></div>'
    return f'<article class="ws-problem" id="q{n}">{body}{extra}{choices(chs) if chs else ""}</article>'

def setbox(label, text):
    return f'<aside class="ws-info ws-set"><strong>{label}</strong>{it(text)}</aside>'

# ───────────────────────────── 문항 ─────────────────────────────
P = {}

P[1] = problem(1, 3,
  "두 영화 감상평 P, Q에 나오는 단어 ‘감동’, ‘연기’, ‘음악’의 빈도수를 성분으로 하는 벡터가 각각 $\\vec{P}=(3,\\ 1,\\ 4)$, $\\vec{Q}=(1,\\ 4,\\ 2)$일 때, 두 감상평의 유클리드 유사도 $L(P, Q)$의 값은?",
  chs=["$3$", "$\\sqrt{13}$", "$4$", "$\\sqrt{17}$", "$17$"])

P[2] = problem(2, 3,
  "두 텍스트 P, Q를 구성하는 단어의 집합이 각각 $P=\\{$여행, 바다, 노을, 사진, 휴식$\\}$, $Q=\\{$바다, 사진, 휴식, 맛집$\\}$일 때, 두 텍스트의 자카드 유사도 $J(P, Q)$의 값은?",
  chs=["$\\dfrac{1}{3}$", "$\\dfrac{1}{2}$", "$\\dfrac{3}{5}$", "$\\dfrac{2}{3}$", "$\\dfrac{3}{4}$"])

P[3] = problem(3, 3,
  "다음은 두 명제 $x_1, x_2$에 대한 논리곱(AND)과 배타적 논리합(XOR)의 진리표이다. ㉠+㉡+㉢+㉣의 값은?",
  extra=table(["$x_1$", "$x_2$", "AND", "XOR"], [["0","0","0","0"],["0","1","㉠","㉡"],["1","0","0","1"],["1","1","㉢","㉣"]]),
  chs=["$0$", "$1$", "$2$", "$3$", "$4$"])

P[4] = problem(4, 3,
  "입력값 $x_1, x_2$에 대한 가중치가 $w_1=0.6$, $w_2=-0.4$이고, 활성화함수가 "
  "$\\sigma(x)=\\begin{cases}0 & (x \\lt 0)\\\\ 5 & (x\\ge 0)\\end{cases}$ 인 퍼셉트론이 있다. "
  "$x_1=2$, $x_2=1$을 입력할 때, 각각의 입력값과 가중치를 곱한 값들의 합 $x$와 출력값 $\\sigma(x)$에 대하여 $x+\\sigma(x)$의 값은?",
  chs=["$0.8$", "$1.6$", "$5$", "$5.8$", "$6.6$"])

P[5] = problem(5, 3,
  "성분이 0 또는 1인 $3\\times3$ 행렬로 나타낸 두 이미지 "
  "$P=\\begin{pmatrix}1&0&1\\\\0&1&0\\\\1&1&0\\end{pmatrix}$, $Q=\\begin{pmatrix}1&1&1\\\\0&0&0\\\\1&1&1\\end{pmatrix}$의 해밍 거리 $H(P, Q)$의 값은?",
  chs=["$3$", "$4$", "$5$", "$6$", "$9$"])

P[6] = problem(6, 3,
  "성분이 0 또는 1인 $3\\times3$ 행렬로 나타낸 이미지 A, B의 해밍 거리 $H(A, B)$에 대한 설명으로 옳은 것만을 &lt;보기&gt;에서 있는 대로 고른 것은?",
  extra=bogi("ㄱ. $H(A, A)=0$이다.", "ㄴ. $H(A, B)=H(B, A)$이다.", "ㄷ. $H(A, B)$의 값이 클수록 두 이미지 A, B는 더 유사하다."),
  chs=["ㄱ", "ㄴ", "ㄷ", "ㄱ, ㄴ", "ㄱ, ㄴ, ㄷ"])

P[7] = problem(7, 3,
  "성분이 0 또는 1인 행렬로 나타낸 이미지 A에 대하여, 입력되는 이미지가 A일 가능성을 계산하는 퍼셉트론 $\\mathrm{P_A}$의 가중치 행렬을 "
  "$W_A=\\dfrac{1}{(\\text{행렬 } A\\text{의 모든 성분의 합})}A$로 정하고, 활성화함수를 $\\sigma(x)=x$라 하자. "
  "이에 대한 설명으로 옳은 것만을 &lt;보기&gt;에서 있는 대로 고른 것은?",
  extra=bogi("ㄱ. 이미지 A 자신을 입력하면 출력값은 1이다.", "ㄴ. 어떤 이미지를 입력하더라도 출력값은 0 이상 1 이하이다.",
             "ㄷ. 두 이미지 A, B에 대한 퍼셉트론 $\\mathrm{P_A}$, $\\mathrm{P_B}$의 출력값 중 더 작은 쪽의 이미지로 분류한다."),
  chs=["ㄱ", "ㄴ", "ㄱ, ㄴ", "ㄱ, ㄷ", "ㄱ, ㄴ, ㄷ"])

P[8] = problem(8, 4,
  "두 텍스트 P, Q를 나타내는 벡터가 $\\vec{P}=(1,\\ 2,\\ 2)$, $\\vec{Q}=(2,\\ 3,\\ 6)$일 때, 두 텍스트의 코사인 유사도 $C(P, Q)$의 값은?",
  chs=["$\\dfrac{2}{3}$", "$\\dfrac{20}{21}$", "$1$", "$2$", "$20$"])

P[9] = problem(9, 4,
  "세 학생 A, B, C가 네 가지 동아리 활동 ‘밴드, 영화, 축구, 코딩’에 대한 선호도를 1위부터 4위까지 순위로 매긴 결과가 다음과 같다. "
  "각 학생의 선호도를 (밴드의 순위, 영화의 순위, 축구의 순위, 코딩의 순위)와 같은 벡터로 나타낼 때, "
  "코사인 유사도를 이용하여 판단한 선호도가 가장 유사한 두 학생의 코사인 유사도의 값은?",
  extra=table(["", "밴드", "영화", "축구", "코딩"], [["A","1","2","3","4"],["B","2","1","4","3"],["C","4","3","1","2"]]),
  chs=["$\\dfrac{7}{10}$", "$\\dfrac{4}{5}$", "$\\dfrac{13}{15}$", "$\\dfrac{9}{10}$", "$\\dfrac{14}{15}$"])

P[10] = problem(10, 4,
  "다음은 단어 사전 $U=\\{$금리, 주가, 공연, 수출, 전시$\\}$에 대하여 경제 기사, 문화 기사, 그리고 새로운 기사 A에 나오는 단어의 빈도수를 나타낸 것이다. "
  "유클리드 유사도를 이용하여 기사 A를 경제 기사 또는 문화 기사로 분류할 때, 분류 결과와 그때의 유클리드 유사도의 값을 순서대로 나열한 것은?",
  extra=table(["", "금리", "주가", "공연", "수출", "전시"], [["경제 기사","3","2","0","1","0"],["문화 기사","0","1","3","0","2"],["기사 A","2","2","1","0","1"]], first_col_left=True),
  chs=["경제 기사, $2$", "경제 기사, $\\sqrt{10}$", "경제 기사, $4$", "문화 기사, $2$", "문화 기사, $\\sqrt{10}$"])

P[11] = problem(11, 4,
  "입력값 $x_1, x_2$에 대한 가중치가 $w_1=0.3$, $w_2=-0.5$이고, 활성화함수가 "
  "$\\sigma(x)=\\begin{cases}0 & (x \\lt 0)\\\\ 2 & (x\\ge 0)\\end{cases}$ 인 퍼셉트론이 있다. "
  "다음은 주어진 입력값에 대하여 각각의 입력값과 가중치를 곱한 값들의 합 $x$와 출력값 $\\sigma(x)$를 나타낸 표이다. ㉠+㉡+㉢의 값은?",
  extra=table(["$x_1$", "$x_2$", "$x$", "$\\sigma(x)$"], [["0","0","0","㉡"],["0","1","㉠","0"],["1","0","0.3","2"],["1","1","㉢","0"]]),
  chs=["$-0.7$", "$1.3$", "$1.7$", "$2.3$", "$2.7$"])

P[12] = problem(12, 4,
  "입력값 $x_1, x_2$에 대한 가중치가 $w_1=4$, $w_2=3$이고, 활성화함수가 "
  "$\\sigma(x)=\\begin{cases}0 & (x \\lt h)\\\\ 1 & (x\\ge h)\\end{cases}$ 인 퍼셉트론이 논리합(OR) 연산을 수행하도록 하는 임곗값 $h$의 값의 범위는?",
  chs=["$0 \\lt h \\lt 3$", "$0\\le h\\le 3$", "$0 \\lt h\\le 4$", "$3 \\lt h\\le 7$", "$0 \\lt h\\le 3$"])

P[13] = problem(13, 4,
  "입력값 $x_1, x_2$에 대한 가중치가 $w_1=-4$, $w_2=-2$이고, 활성화함수가 "
  "$\\sigma(x)=\\begin{cases}0 & (x \\lt h)\\\\ 1 & (x\\ge h)\\end{cases}$ 인 퍼셉트론이 있다. "
  "이 퍼셉트론의 출력값이 다음 표와 같도록 하는 정수 $h$의 개수는?",
  extra=table(["$x_1$", "$x_2$", "$\\sigma(x)$"], [["0","0","1"],["0","1","0"],["1","0","0"],["1","1","0"]]),
  chs=["$1$", "$2$", "$3$", "$4$", "$5$"])

P[14] = problem(14, 4,
  "입력값 $x_1, x_2$에 대한 가중치가 $w_1, w_2$이고, 활성화함수가 "
  "$\\sigma(x)=\\begin{cases}0 & (x \\lt 1)\\\\ 1 & (x\\ge 1)\\end{cases}$ 인 퍼셉트론에 대한 설명으로 옳은 것만을 &lt;보기&gt;에서 있는 대로 고른 것은?",
  extra=bogi("ㄱ. $w_1=0.6$, $w_2=0.6$이면 이 퍼셉트론은 논리곱(AND) 연산을 수행한다.",
             "ㄴ. $w_1=1$, $w_2=1$이면 이 퍼셉트론은 논리곱(AND) 연산을 수행한다.",
             "ㄷ. $w_1, w_2$의 값을 어떻게 정하더라도 이 퍼셉트론은 배타적 논리합(XOR) 연산을 수행할 수 없다."),
  chs=["ㄱ", "ㄴ", "ㄱ, ㄷ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"])

P[15] = problem(15, 4,
  "성분이 0 또는 1인 $3\\times3$ 행렬로 나타낸 네 이미지가 다음과 같다. 해밍 거리를 이용하여 세 이미지 A, B, D 중에서 이미지 C와 가장 유사한 이미지를 찾을 때, "
  "그 이미지와 그때의 해밍 거리를 순서대로 나열한 것은?",
  extra='<p class="ws-math">$C=\\begin{pmatrix}0&1&0\\\\1&1&1\\\\0&1&0\\end{pmatrix},\\ A=\\begin{pmatrix}1&1&1\\\\1&0&1\\\\1&1&1\\end{pmatrix},$<br>'
        '$B=\\begin{pmatrix}0&1&0\\\\0&1&0\\\\0&1&0\\end{pmatrix},\\ D=\\begin{pmatrix}1&0&1\\\\0&1&0\\\\1&0&1\\end{pmatrix}$</p>',
  chs=["$A,\\ 2$", "$B,\\ 2$", "$B,\\ 3$", "$D,\\ 1$", "$D,\\ 8$"])

P[16] = problem(16, 4,
  "가로와 세로의 픽셀 수가 각각 5와 7인 전광판에 표시된 두 숫자 6과 9의 이미지 A, B와, 몇 개의 전구에 불이 들어오지 않아 일부만 표시된 어떤 숫자의 이미지 P가 다음 그림과 같다. "
  "불이 켜진 픽셀을 1, 꺼진 픽셀을 0으로 하여 세 이미지를 행렬로 나타낸 뒤 해밍 거리를 이용할 때, 이미지 P가 6과 9 중 어느 숫자로 분류되는지와 그때의 해밍 거리를 순서대로 나열한 것은?",
  extra=fig("fig16_digits.svg"),
  chs=["6, $2$", "6, $4$", "9, $2$", "9, $4$", "9, $6$"])

P[17] = problem(17, 4,
  "성분이 0 또는 1인 $2\\times3$ 행렬로 나타낸 이미지 $A=\\begin{pmatrix}1&1&0\\\\1&0&1\\end{pmatrix}$에 대하여, "
  "입력되는 이미지가 A일 가능성을 계산하는 퍼셉트론의 가중치 행렬을 $W=\\dfrac{1}{(\\text{행렬 } A\\text{의 모든 성분의 합})}A$로 정하고, 활성화함수를 $\\sigma(x)=x$라 하자. "
  "이 퍼셉트론에 이미지 $X=\\begin{pmatrix}1&1&1\\\\1&0&1\\end{pmatrix}$을 입력할 때, 출력값은?",
  chs=["$\\dfrac{1}{4}$", "$\\dfrac{1}{2}$", "$\\dfrac{3}{4}$", "$1$", "$4$"])

P[18] = problem(18, 4,
  "다음 표는 어느 지역의 연도별 전기차 등록 대수를 나타낸 것인데, 2022년의 자료가 누락되었다. 연도를 $x$년, 등록 대수를 $y$천 대라 하고 추세선의 식을 $f(x)=12(x-2019)+15$라 하자. "
  "누락된 2022년의 등록 대수의 예측값을 $p$, 2023년의 등록 대수의 측정값과 예측값 사이의 오차를 $q$라 할 때, $p$, $q$의 값을 순서대로 나열한 것은?",
  extra=table(["연도(년)", "등록 대수(천 대)"], [["2019","14"],["2020","28"],["2021","40"],["2022",""],["2023","60"],["2024","76"]]),
  chs=["$51,\\ -3$", "$51,\\ 3$", "$51,\\ 63$", "$63,\\ -3$", "$63,\\ 3$"])

P[19] = problem(19, 5,
  "입력값 $x_1, x_2$에 대한 가중치가 $w_1=2$, $w_2$이고, 활성화함수가 "
  "$\\sigma(x)=\\begin{cases}0 & (x \\lt 5)\\\\ 1 & (x\\ge 5)\\end{cases}$ 인 퍼셉트론이 논리곱(AND) 연산을 수행하도록 하는 모든 정수 $w_2$의 값의 합은?",
  chs=["$3$", "$4$", "$7$", "$9$", "$12$"])

P[20] = problem(20, 5,
  "활성화함수가 $\\sigma(x)=\\begin{cases}0 & (x \\lt 0)\\\\ 1 & (x\\ge 0)\\end{cases}$ 이고, 입력값 $x_1, x_2$로부터 은닉층의 값 $z_1, z_2$와 출력값 $y$가 "
  "그림과 같은 가중치로 정해지는 다층 퍼셉트론이 있다. 즉, $z_1=\\sigma(3x_1-2x_2)$, $z_2=\\sigma(-x_1+2x_2)$, $y=\\sigma(2z_1-3z_2)$이다. "
  "다음 네 쌍의 입력값 중 출력값 $y$가 1이 되는 것의 개수는?",
  extra=fig("fig20_mlp.svg") + table(["$x_1$", "2", "1", "$-1$", "$-1$"], [["$x_2$", "1", "$-1$", "2", "$-1$"]], first_col_left=True),
  chs=["$0$", "$1$", "$2$", "$3$", "$4$"])

P[21] = problem(21, 5,
  "활성화함수가 $\\sigma(x)=\\begin{cases}0 & (x \\lt 4)\\\\ 1 & (x\\ge 4)\\end{cases}$ 이고, 입력값 $x_1, x_2$로부터 은닉층의 값 $z_1, z_2$와 출력값 $y$가 "
  "그림과 같은 가중치로 정해지는 다층 퍼셉트론이 있다. 즉, $z_1=\\sigma(6x_1+5x_2)$, $z_2=\\sigma(3x_1+2x_2)$, $y=\\sigma(5z_1+b\\,z_2)$이다. "
  "이 다층 퍼셉트론이 배타적 논리합(XOR) 연산을 수행하도록 하는 정수 $b$의 최댓값은?",
  extra=fig("fig21_mlp.svg"),
  chs=["$-6$", "$-5$", "$-4$", "$-3$", "$-2$"])

P[22] = problem(22, 5,
  "성분이 0 또는 1인 $3\\times3$ 행렬로 나타낸 두 이미지 $P=\\begin{pmatrix}1&0&1\\\\0&1&0\\\\1&0&1\\end{pmatrix}$, $Q=\\begin{pmatrix}1&a&1\\\\0&1&b\\\\0&0&1\\end{pmatrix}$에 대하여 "
  "$H(P, Q)=3$일 때, $a, b$의 값은?",
  chs=["$a=0,\\ b=0$", "$a=0,\\ b=1$", "$a=1,\\ b=0$", "$a=1,\\ b=1$", "조건을 만족시키는 $a, b$는 존재하지 않는다."])

SET_23_24 = setbox("[23~24]",
  " 성분이 0 또는 1인 행렬로 나타낸 이미지 A에 대하여, 입력되는 이미지가 A일 가능성을 계산하는 퍼셉트론 $\\mathrm{P_A}$의 가중치 행렬은 "
  "$W_A=\\dfrac{1}{(\\text{행렬 } A\\text{의 모든 성분의 합})}A$이고, 활성화함수는 $\\sigma(x)=x$이다. 물음에 답하시오.")

P[23] = problem(23, 5,
  "성분이 0 또는 1인 $3\\times3$ 행렬로 나타낸 세 이미지 A, B, C가 그림과 같다. 이미지 C를 두 퍼셉트론 $\\mathrm{P_A}$, $\\mathrm{P_B}$에 입력할 때, "
  "인공지능이 C를 어느 이미지로 분류하는지와 그때의 출력값을 순서대로 나열한 것은?",
  extra=fig("fig23_images.svg"),
  chs=["$A,\\ \\dfrac{3}{5}$", "$A,\\ \\dfrac{3}{4}$", "$A,\\ 3$", "$B,\\ \\dfrac{3}{5}$", "$B,\\ \\dfrac{3}{4}$"])

P[24] = problem(24, 5,
  "성분이 0 또는 1인 $3\\times3$ 행렬로 나타낸 세 이미지 A, B, C가 그림과 같다. 이미지 C를 두 이미지 A, B 중 하나로 분류하려고 한다. "
  "옳은 것만을 &lt;보기&gt;에서 있는 대로 고른 것은?",
  extra=fig("fig24_images.svg") + bogi("ㄱ. $H(C, A)=3$이다.", "ㄴ. 퍼셉트론 $\\mathrm{P_B}$의 출력값은 1이다.",
             "ㄷ. 해밍 거리를 이용하면 C는 A로, 두 퍼셉트론 $\\mathrm{P_A}$, $\\mathrm{P_B}$를 이용하면 C는 B로 분류된다."),
  chs=["ㄱ", "ㄴ", "ㄱ, ㄴ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"])

P[25] = problem(25, 5,
  "다음 표는 어느 카페에서 낮 최고 기온에 따른 아이스 음료 판매량을 조사한 것이다. 기온을 $x\\,°\\mathrm{C}$, 판매량을 $y$잔이라 하고 추세선의 식을 $f(x)=5x+20$이라 하자. "
  "네 자료 중 오차의 크기가 가장 큰 자료의 기온과 그때의 오차를 순서대로 나열한 것은?",
  extra=table(["기온($°\\mathrm{C}$)", "20", "24", "28", "32"], [["판매량(잔)","118","144","155","183"]], first_col_left=True),
  chs=["$28,\\ -5$", "$24,\\ -4$", "$32,\\ 3$", "$24,\\ 4$", "$28,\\ 5$"])

# ───────────────────────────── 페이지 배치 ─────────────────────────────
PAGES = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
    [13, 14, 15, 16],
    [17, 18, 19, 20],
    [21, 22],
    [23, 24, 25],
]

HEAD_TITLE = "2026학년도 2학기 중간고사"
SUB = "인공지능 수학 · 3학년 · 50분 · 100점 만점"
MATHJAX = ("../../../../figures/node_modules/mathjax-full/es5/tex-chtml.js" if LOCAL
           else "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js")

EXTRA_CSS = """
/* 시험지 전용 보조 스타일 — 토큰만 사용 */
/* 2단 채움(column-fill:auto)이 동작하려면 페이지 높이가 고정되어야 함: 화면 297mm, 인쇄는 @page 여백(15/20mm) 제외 262mm */
.ws-page { height: 297mm; }
@media print { .ws-page { height: 262mm; } }
.ws-problem-points { color: var(--lm-page-ink-2); font-size: var(--lm-page-caption); white-space: nowrap; }
.ws-figure { margin: var(--lm-space-2) 0 var(--lm-space-1); text-align: center; break-inside: avoid; page-break-inside: avoid; }
.ws-figure > svg { display: inline-block; max-width: 100%; height: auto; }
.ws-figure svg svg { overflow: visible; }
.ws-table td.nw, .ws-table th.nw { white-space: nowrap; }
.ws-math { margin: var(--lm-space-2) 0; text-align: center; font-size: var(--lm-page-small); line-height: 1.9; }
.ws-set { margin-bottom: var(--lm-space-3); }
.ws-set strong { color: var(--lm-accent); }
/* 그림 클래스 → 디자인 토큰 */
.fg-board { fill: var(--lm-page-rule); }
.fg-off   { fill: var(--lm-page-ink); stroke: var(--lm-page); stroke-width: 0.35; }
.fg-on    { fill: var(--lm-page);     stroke: var(--lm-page-ink); stroke-width: 0.35; }
.fg-title { font-family: var(--lm-font-sans); font-weight: 700; fill: var(--lm-accent); text-anchor: middle; }
.fg-cap   { font-family: var(--lm-font-sans); fill: var(--lm-page-ink-2); text-anchor: middle; }
.fg-title-tex { color: var(--lm-accent); overflow: visible; }
.fg-node-x  { fill: var(--lm-paper-tint); }
.fg-node-z1 { fill: #D9D5E2; }   /* accent-math2 tint — 토큰 없음, 인쇄 무채색 */
.fg-node-z2 { fill: #D2E0D5; }   /* accent-statistics tint */
.fg-node-y  { fill: #F0DBD4; }   /* accent-calculus tint */
.fg-node-text { color: var(--lm-page-ink); overflow: visible; }
.fg-edge-z1 { stroke: var(--lm-accent-math2); stroke-width: 0.55; fill: none; stroke-linecap: round; }
.fg-edge-z2 { stroke: var(--lm-accent-statistics); stroke-width: 0.55; fill: none; stroke-linecap: round; }
.fg-edge-y  { stroke: var(--lm-page-ink-2); stroke-width: 0.55; fill: none; stroke-linecap: round; }
.fg-w-z1 { color: var(--lm-accent-math2); overflow: visible; }
.fg-w-z2 { color: var(--lm-accent-statistics); overflow: visible; }
.fg-w-y  { color: var(--lm-page-ink); overflow: visible; }
"""

def page(idx, nums, total):
    header = ""
    if idx == 0:
        header = f"""
    <header class="exam-head">
      <div class="exam-title">{HEAD_TITLE}</div>
      <div class="exam-sub">{SUB}</div>
      <div class="exam-metrics">
        <span>선택형 25문항</span>
        <span>시행 2026. 10.</span>
        <span>출제 교무부</span>
      </div>
    </header>
    <div class="ws-student">
      <span class="ws-student-field"><label>학년</label><span class="line"></span></span>
      <span class="ws-student-field"><label>반</label><span class="line"></span></span>
      <span class="ws-student-field"><label>번호</label><span class="line"></span></span>
      <span class="ws-student-field"><label>이름</label><span class="line"></span></span>
    </div>
    <aside class="ws-info">
      <strong>유의사항</strong> 답안은 모두 답안지(OMR)에 표시하시오. 계산 과정은 이 문제지의 여백을 활용할 수 있으며, 채점 대상에는 포함되지 않는다.
    </aside>"""
    items = ""
    for n in nums:
        items += P[n].replace('<article class="ws-problem" id="q23">', '<article class="ws-problem" id="q23">' + SET_23_24) if n == 23 else P[n]
    return f"""
  <div class="ws-page">{header}
    <div class="ws-body">
{items}
    </div>
    <div class="ws-pagenum">{idx+1} / {total}</div>
  </div>"""

html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <title>{HEAD_TITLE} 인공지능 수학</title>
  <link rel="stylesheet" href="../../../_shared/templates/design-tokens.css">
  <link rel="stylesheet" href="../../../_shared/templates/worksheet-system.css">
  <style>{EXTRA_CSS}</style>
  <script>
    window.MathJax = {{
      tex: {{ inlineMath: [['$', '$'], ['\\\\(', '\\\\)']], displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']] }},
      options: {{ skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'svg'] }},
      chtml: {{ scale: 0.95 }}
    }};
  </script>
  <script src="{MATHJAX}" async></script>
</head>
<body data-subject="ai_math">
{''.join(page(i, nums, len(PAGES)) for i, nums in enumerate(PAGES))}
</body>
</html>
"""
out = HERE / "lm" / "ai-math" / "output" / "exam" / ("시험지_2026-2학기_중간고사_인공지능수학" + ("_local" if LOCAL else "") + ".html")
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(html, encoding="utf-8")
print("written", out, len(html), "bytes")
