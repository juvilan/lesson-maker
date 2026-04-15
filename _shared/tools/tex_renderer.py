"""
tex_renderer.py — JSON → LaTeX → xelatex → PDF
한글(kotex) + 수식(amsmath) 완전 지원

사용법:
  python tex_renderer.py worksheet.json output.pdf
  python tex_renderer.py assessment.json output.pdf --template school_template.json
"""

import json
import os
import sys
import argparse
import subprocess
import tempfile
import shutil
import re
from pathlib import Path
from typing import Optional


# ─────────────────────────────────────────────
# xelatex 경로
# ─────────────────────────────────────────────
XELATEX_CANDIDATES = [
    "/opt/homebrew/bin/xelatex",
    "/usr/local/bin/xelatex",
    "/Library/TeX/texbin/xelatex",
    shutil.which("xelatex") or "",
]

def find_xelatex() -> str:
    for p in XELATEX_CANDIDATES:
        if p and os.path.exists(p):
            return p
    raise RuntimeError(
        "xelatex를 찾을 수 없습니다. 'brew install texlive' 로 설치하세요."
    )


# ─────────────────────────────────────────────
# LaTeX 특수문자 이스케이프
# ─────────────────────────────────────────────
# str.translate 단일 패스 — 순차 replace는 이미 이스케이프된 문자를 재처리하는 버그가 있음
_ESCAPE_TABLE = str.maketrans({
    "\\": r"\textbackslash{}",
    "&":  r"\&",
    "%":  r"\%",
    "#":  r"\#",
    "_":  r"\_",
    "{":  r"\{",
    "}":  r"\}",
    "~":  r"\textasciitilde{}",
    "^":  r"\textasciicircum{}",
})

def tex_escape(text: str) -> str:
    """
    일반 텍스트(수식 밖)의 LaTeX 특수문자를 이스케이프한다.
    $...$ 구간은 그대로 유지한다.
    str.translate로 단일 패스 처리 — 이미 삽입된 이스케이프 시퀀스 재처리 없음.
    """
    parts = re.split(r"(\$[^$]+\$|\$\$[^$]+\$\$)", text)
    result = []
    for part in parts:
        if part.startswith("$"):
            result.append(part)   # 수식 그대로
        else:
            # 연속 밑줄(3개 이상)을 빈칸 표시로 변환
            # translate 이후 삽입해야 이스케이프가 덮어쓰지 않음
            subparts = re.split(r"(_{3,})", part)
            escaped = []
            for sp in subparts:
                if re.match(r"_{3,}$", sp):
                    escaped.append(r"\hspace{25mm}")
                else:
                    escaped.append(sp.translate(_ESCAPE_TABLE))
            result.append("".join(escaped))
    return "".join(result)


# ─────────────────────────────────────────────
# 학교 템플릿 로드
# ─────────────────────────────────────────────
def load_template(template_path: Optional[str]) -> dict:
    default = {
        "logo_path": None,
        "header_format": "{grade}학년 {semester}학기 {subject}",
        "student_info_fields": ["학년", "반", "번", "이름"],
        "page_number_format": "-- {n} --",
        "margins": {"top": 18, "right": 18, "bottom": 18, "left": 18},
        "fonts": {"main": "Apple SD Gothic Neo", "math": "Latin Modern Math"},
    }
    if not template_path:
        default_path = Path(__file__).parent.parent / "config" / "school_template.json"
        if default_path.exists():
            template_path = str(default_path)
    if template_path and os.path.exists(template_path):
        with open(template_path, encoding="utf-8") as f:
            loaded = json.load(f)
            return {**default, **loaded}
    return default


# ─────────────────────────────────────────────
# LaTeX 문서 생성기
# ─────────────────────────────────────────────
class TexDocBuilder:
    """
    JSON 워크시트 데이터를 LaTeX 소스로 변환한다.
    xelatex + kotex + amsmath 기반.
    """

    def __init__(self, config: dict):
        self.config = config
        self.lines: list[str] = []

    # ── 헬퍼 ──────────────────────────────────

    def L(self, line: str = ""):
        self.lines.append(line)

    def build(self) -> str:
        return "\n".join(self.lines)

    # ── 문서 프리앰블 ─────────────────────────

    def preamble(self, data: dict):
        m = self.config.get("margins", {})
        top    = m.get("top", 18)
        bottom = m.get("bottom", 18)
        left   = m.get("left", 18)
        right  = m.get("right", 18)

        main_font = self.config.get("fonts", {}).get("main", "Apple SD Gothic Neo")
        math_font = self.config.get("fonts", {}).get("math", "Latin Modern Math")

        self.L(r"\documentclass[a4paper,11pt]{article}")
        self.L(r"\usepackage{kotex}")           # 한글
        self.L(r"\usepackage{fontspec}")        # 폰트 지정
        self.L(r"\usepackage{unicode-math}")    # 유니코드 수식
        self.L(r"\usepackage{amsmath,amssymb,amsthm}")
        self.L(r"\usepackage{array,booktabs,multirow,tabularx,colortbl}")
        self.L(r"\usepackage{enumitem}")
        self.L(r"\usepackage{geometry}")
        self.L(r"\usepackage{graphicx}")
        self.L(r"\usepackage{xcolor}")
        self.L(r"\usepackage{mdframed}")
        self.L(r"\usepackage{fancyhdr}")
        self.L(r"\usepackage{lastpage}")
        self.L(r"\usepackage{setspace}")
        self.L(r"\usepackage{tcolorbox}")
        self.L(r"\tcbuselibrary{skins,breakable}")
        self.L(r"\usepackage{needspace}")
        self.L()

        # 폰트 설정
        self.L(rf"\setmainfont{{{main_font}}}")
        self.L(rf"\setmathfont{{{math_font}}}")
        self.L()

        # 여백
        self.L(rf"\geometry{{a4paper, top={top}mm, bottom={bottom}mm, "
               rf"left={left}mm, right={right}mm}}")
        self.L()

        # 줄간격
        self.L(r"\setstretch{1.3}")
        self.L()

        # 페이지 스타일
        self.L(r"\pagestyle{fancy}")
        self.L(r"\fancyhf{}")
        self.L(r"\renewcommand{\headrulewidth}{0pt}")
        self.L(r"\fancyfoot[C]{\small --- \thepage\ ---}")
        self.L()

        # 문제 번호 카운터
        self.L(r"\newcounter{problemno}")
        self.L()

        # 풀이 칸 명령
        self.L(r"\newcommand{\calcbox}[1][40mm]{%")
        self.L(r"  \vspace{2mm}")
        self.L(r"  \noindent\textbf{\small 풀이 과정}\\[-1mm]")
        self.L(r"  \noindent\rule{\linewidth}{0.3pt}\\[-2.5mm]")
        self.L(r"  \rule{\linewidth}{0.3pt}\\[-2.5mm]")
        self.L(r"  \rule{\linewidth}{0.3pt}\\[-2.5mm]")
        self.L(r"  \rule{\linewidth}{0.3pt}\\[-2.5mm]")
        self.L(r"  \rule{\linewidth}{0.3pt}")
        self.L(r"  \vspace{1mm}}")
        self.L()

        # 서술형 답안 칸 (빈 공간)
        self.L(r"\newcommand{\essaybox}[1][5]{%")
        self.L(r"  \vspace{18mm}}")
        self.L()

        # 난이도 배지 색상
        self.L(r"\definecolor{badgegray}{RGB}{60,60,60}")
        self.L(r"\definecolor{stepbg}{RGB}{245,245,245}")
        self.L(r"\definecolor{answerbg}{RGB}{235,248,235}")
        self.L()

    # ── 문서 시작/끝 ──────────────────────────

    def begin_doc(self):
        self.L(r"\begin{document}")

    def end_doc(self):
        self.L(r"\end{document}")

    # ── 학습지 헤더 ───────────────────────────

    def worksheet_header(self, data: dict):
        grade   = tex_escape(data.get("grade", ""))
        sem     = tex_escape(data.get("semester", ""))
        subject = tex_escape(data.get("subject_display", data.get("subject", "")))
        topic   = tex_escape(data.get("topic", "학습지"))
        subtitle = tex_escape(data.get("subtitle", ""))
        total_pts = data.get("total_points")
        fields  = self.config.get("student_info_fields", ["학년", "반", "번", "이름"])

        header_fmt = self.config.get(
            "header_format", "{grade}학년 {semester}학기 {subject}"
        ).format(grade=grade, semester=sem, subject=subject)

        self.L(r"\begin{center}")
        self.L(rf"{{\small\color{{gray}} {tex_escape(header_fmt)}}}")
        self.L(r"\\[2mm]")
        self.L(rf"{{\LARGE\bfseries {topic}}}")
        if subtitle:
            self.L(r"\\[1mm]")
            self.L(rf"{{\normalsize\color{{gray}} {subtitle}}}")
        self.L(r"\end{center}")
        self.L(r"\vspace{-2mm}")
        self.L(r"\noindent\rule{\linewidth}{0.8pt}")
        self.L(r"\vspace{1mm}")

        # 학생 정보 + 점수란
        field_cols = " & ".join(
            rf"\textbf{{{tex_escape(f)}}}"
            for f in fields
        )
        if total_pts:
            score_col = rf" & \textbf{{점수}} / {total_pts}점"
        else:
            score_col = ""

        n_cols = len(fields) + (1 if total_pts else 0)
        col_spec = "l" * n_cols
        self.L(r"\begin{tabular}{" + col_spec + r"}")
        self.L(field_cols + score_col + r" \\")
        self.L(r"\end{tabular}")
        self.L(r"\par\vspace{2mm}")

    # ── 일반 학습지 문제 ──────────────────────

    def render_problems(self, problems: list[dict]):
        for i, problem in enumerate(problems, 1):
            self._render_problem(problem, i)

    def _render_problem(self, problem: dict, number: int):
        ptype      = problem.get("type", "서술형")
        bloom      = problem.get("bloom_level", "")
        difficulty = problem.get("difficulty", "")
        points     = problem.get("points", 10)
        question   = problem.get("question", "")

        # 문제 번호 + 메타 배지
        self.L(r"\noindent")
        self.L(rf"\textbf{{{number}.}}"
               rf"\quad {{\small [{tex_escape(bloom)} · {tex_escape(difficulty)} · {points}점]}}")
        self.L(r"\\[1mm]")

        # 문제 본문
        self.L(rf"\noindent {tex_escape(question)}")
        self.L()

        # 유형별 답안 칸
        if ptype == "객관식":
            choices = problem.get("choices", [])
            labels = ["①", "②", "③", "④", "⑤"]
            self.L(r"\begin{enumerate}[label=\protect\textcircled{\arabic*},leftmargin=*,itemsep=1pt]")
            for choice in choices[:5]:
                self.L(rf"  \item {tex_escape(choice)}")
            self.L(r"\end{enumerate}")
            self.L(r"\noindent 답:")
        elif ptype == "단답형":
            self.L(r"\noindent 답:")
        elif ptype == "계산형":
            self.L(r"\calcbox")
        else:
            self.L(r"\essaybox")

        self.L(r"\vspace{4mm}")

    # ── 정답지 ────────────────────────────────

    def render_answer_key(self, problems: list[dict]):
        self.L(r"\newpage")
        self.L(r"\begin{center}")
        self.L(r"{\Large\bfseries 정답 및 풀이}")
        self.L(r"\end{center}")
        self.L(r"\noindent\rule{\linewidth}{0.8pt}")
        self.L(r"\vspace{3mm}")

        for i, problem in enumerate(problems, 1):
            number  = problem.get("number", i)
            answer  = problem.get("answer", "")
            steps   = problem.get("solution_steps", [])

            self.L(r"\noindent")
            self.L(rf"\textbf{{{number}번.}} \quad 정답: {tex_escape(answer)}")
            self.L()

            if steps:
                for step in steps:
                    label = tex_escape(step.get("step_label", ""))
                    explanation = tex_escape(step.get("explanation", ""))
                    self.L(rf"\noindent\textbf{{{label}}} \enspace {explanation}\\")

            self.L(r"\vspace{3mm}")

    # ── Step 기반 워크시트 ────────────────────

    def render_context_box(self, context: dict):
        label = tex_escape(context.get("label", "상황"))
        title = tex_escape(context.get("title", ""))
        intro = tex_escape(context.get("intro", ""))
        items = context.get("items", [])

        self.L(r"\noindent")
        self.L(rf"\colorbox{{badgegray}}{{\textcolor{{white}}{{\small\bfseries {label}}}}}"
               rf"\enspace\textbf{{{title}}}")
        self.L(r"\vspace{1mm}")
        self.L(r"\begin{tcolorbox}[colback=white,colframe=black!70,boxrule=0.5pt,"
               r"left=6pt,right=6pt,top=4pt,bottom=4pt]")
        if intro:
            self.L(rf"{intro}\\[1mm]")
        for item in items:
            self.L(rf"\noindent {tex_escape(item)}\\")
        self.L(r"\end{tcolorbox}")
        self.L(r"\vspace{2mm}")

    def render_step_section(self, step: dict, for_answer: bool = False):
        badge    = tex_escape(step.get("badge", ""))
        title    = tex_escape(step.get("title", ""))
        subtitle = tex_escape(step.get("subtitle", ""))
        note     = step.get("note")
        stype    = step.get("type", "")

        # 배지 + 제목 — 스텝 헤더가 페이지 하단에 고립되지 않도록 보호
        self.L(r"\needspace{6\baselineskip}")
        self.L(r"\noindent")
        self.L(rf"\colorbox{{badgegray}}{{\textcolor{{white}}{{\small\bfseries {badge}}}}}"
               rf"\enspace\textbf{{{title}}}"
               + (rf"\enspace{{\small\color{{gray}} {subtitle}}}" if subtitle else ""))
        self.L(r"\par\vspace{1mm}")

        # 안내 박스
        if note:
            self.L(r"\begin{tcolorbox}[colback=stepbg,colframe=gray!50,boxrule=0.3pt,"
                   r"left=5pt,right=5pt,top=2pt,bottom=2pt]")
            for nline in note.split("\n"):
                self.L(rf"\noindent\small {tex_escape(nline)}\\")
            self.L(r"\end{tcolorbox}")
            self.L(r"\vspace{1mm}")

        if stype == "fill_lines":
            self._render_fill_lines(step.get("fill_lines", []), for_answer)
        elif stype == "table":
            self._render_step_table(step.get("table", {}), for_answer)
            follow_up = step.get("follow_up", "")
            if follow_up:
                answer_text = step.get("follow_up_answer", "")
                if for_answer and answer_text:
                    self.L(rf"\noindent\small $\Rightarrow$ {tex_escape(follow_up)}")
                    self.L()
                    self.L(rf"\noindent\small\color{{gray}} {tex_escape(answer_text)}")
                else:
                    self.L(rf"\noindent\small $\Rightarrow$ {tex_escape(follow_up)}")
                    self.L(r"\par")
        elif stype == "essay":
            self._render_essay_questions(step.get("questions", []), for_answer)

        self.L(r"\par\vspace{3mm}")

    def _render_fill_lines(self, fill_lines: list, for_answer: bool):
        for item in fill_lines:
            label  = tex_escape(item.get("label", ""))
            given  = item.get("given")
            note   = tex_escape(item.get("note", ""))
            answer = item.get("answer", "")

            self.L(rf"\noindent\textbf{{{label}}} : \enspace")
            if given:
                self.L(rf"\colorbox{{stepbg}}{{{tex_escape(given)}}}")
            elif for_answer and answer:
                self.L(rf"\colorbox{{answerbg}}{{{tex_escape(answer)}}}")
            else:
                self.L(r"\hspace{0pt}")
            if note:
                self.L(rf"\quad\small\color{{gray}}{note}")
            self.L(r"\\[3pt]")

    def _render_step_table(self, table_data: dict, for_answer: bool):
        headers = table_data.get("headers", [])
        rows    = table_data.get("rows", [])
        if not headers or not rows:
            return

        n = len(headers)
        # 첫 열 넓이 고정, 나머지 균등
        col_spec = r">{\\centering\\arraybackslash}p{18mm}" + \
                   (r"|>{\\centering\\arraybackslash}X" * (n - 1))
        col_spec = "|c|" + "|".join(["c"] * (n - 1)) + "|"

        self.L(r"\begin{center}")
        self.L(r"\renewcommand{\arraystretch}{1.4}")
        self.L(rf"\begin{{tabular}}{{{col_spec}}}")
        self.L(r"\hline")

        # 헤더 행
        header_row = " & ".join(
            rf"\cellcolor{{badgegray}}\textcolor{{white}}{{\small\bfseries {tex_escape(h)}}}"
            for h in headers
        )
        self.L(header_row + r" \\ \hline")

        # 데이터 행
        for row in rows:
            label = tex_escape(row.get("label", ""))
            cells = row.get("cells", [])
            row_parts = [rf"\cellcolor{{stepbg}}\bfseries {label}"]
            for cell in cells:
                ctype  = cell.get("type", "blank")
                val    = cell.get("v", "")
                answer = cell.get("answer", "")
                if ctype == "given":
                    row_parts.append(rf"\cellcolor{{stepbg}} {tex_escape(val)}")
                elif ctype == "sub":
                    row_parts.append(rf"\cellcolor{{stepbg}}{{\tiny\color{{gray}} {tex_escape(val)}}}")
                elif for_answer and answer:
                    row_parts.append(rf"\cellcolor{{answerbg}} {tex_escape(answer)}")
                else:
                    row_parts.append("")
            self.L(" & ".join(row_parts) + r" \\ \hline")

        self.L(r"\end{tabular}")
        self.L(r"\end{center}")

    def _render_essay_questions(self, questions: list, for_answer: bool):
        for q in questions:
            question = tex_escape(q.get("question", ""))
            answer   = tex_escape(q.get("answer", ""))
            self.L(rf"\noindent\textbf{{{question}}}")
            self.L()
            if for_answer and answer:
                self.L(rf"\noindent\small\color{{gray}} {answer}")
            else:
                self.L(r"\essaybox")
            self.L(r"\vspace{2mm}")

    def render_checklist(self, items: list):
        self.L(r"\begin{tcolorbox}[colback=white,colframe=black!30,boxrule=0.4pt,"
               r"left=5pt,right=5pt,top=3pt,bottom=3pt,title={\small 확인 체크리스트},"
               r"coltitle=black,fonttitle=\bfseries\small]")
        for item in items:
            self.L(rf"\noindent $\square$ \small {tex_escape(item)}\\")
        self.L(r"\end{tcolorbox}")

    # ── Step 정답지 ───────────────────────────

    def render_step_answer_key(self, data: dict):
        self.L(r"\newpage")
        self.L(r"\begin{center}")
        self.L(r"{\Large\bfseries 정답 및 풀이}")
        self.L(r"\end{center}")
        self.L(r"\noindent\rule{\linewidth}{0.8pt}")
        self.L(r"\vspace{3mm}")
        for step in data.get("steps", []):
            self.render_step_section(step, for_answer=True)


# ─────────────────────────────────────────────
# 문서 조립
# ─────────────────────────────────────────────

def build_worksheet_tex(data: dict, config: dict) -> str:
    b = TexDocBuilder(config)
    b.preamble(data)
    b.begin_doc()
    b.worksheet_header(data)
    b.render_problems(data.get("problems", []))
    if data.get("include_answer_key", True):
        b.render_answer_key(data.get("problems", []))
    b.end_doc()
    return b.build()


def build_step_practice_tex(data: dict, config: dict) -> str:
    b = TexDocBuilder(config)
    b.preamble(data)
    b.begin_doc()
    b.worksheet_header(data)

    context = data.get("context_box")
    if context:
        b.render_context_box(context)

    for step in data.get("steps", []):
        b.render_step_section(step, for_answer=False)

    checklist = data.get("checklist", [])
    if checklist:
        b.render_checklist(checklist)

    if data.get("include_answer_key", True):
        b.render_step_answer_key(data)

    b.end_doc()
    return b.build()


def build_assessment_tex(data: dict, config: dict) -> str:
    b = TexDocBuilder(config)
    b.preamble(data)
    b.begin_doc()
    b.worksheet_header(data)

    meta = data.get("assessment_meta", {})
    if meta:
        parts = []
        if meta.get("time_limit"):
            parts.append(f"시간: {meta['time_limit']}분")
        if meta.get("materials"):
            parts.append("준비물: " + ", ".join(meta["materials"]))
        if parts:
            b.L(r"\noindent\small " + tex_escape("  |  ".join(parts)))
            b.L(r"\vspace{2mm}")

    rubric = data.get("rubric")
    if rubric:
        _build_rubric(b, rubric)

    sections = data.get("sections")
    if sections:
        for section in sections:
            b.L(rf"\noindent\textbf{{\large {tex_escape(section.get('title',''))}}}")
            inst = section.get("instructions", "")
            if inst:
                b.L(rf"\\\small {tex_escape(inst)}")
            b.L(r"\vspace{1mm}")
            for i, prob in enumerate(section.get("problems", []), 1):
                b._render_problem(prob, i)
    else:
        b.render_problems(data.get("problems", []))

    if data.get("include_answer_key", True):
        all_problems = data.get("problems", [])
        if not all_problems and sections:
            all_problems = [p for s in sections for p in s.get("problems", [])]
        b.render_answer_key(all_problems)

    b.end_doc()
    return b.build()


def _build_rubric(b: TexDocBuilder, rubric: dict):
    criteria = rubric.get("criteria", [])
    if not criteria:
        return
    b.L(r"\noindent\textbf{채점 기준표}\\[2mm]")
    b.L(r"\begin{tabular}{|p{80mm}|c|c|p{30mm}|}")
    b.L(r"\hline")
    b.L(r"\cellcolor{badgegray}\textcolor{white}{\bfseries 평가 기준} & "
        r"\cellcolor{badgegray}\textcolor{white}{\bfseries 배점} & "
        r"\cellcolor{badgegray}\textcolor{white}{\bfseries 득점} & "
        r"\cellcolor{badgegray}\textcolor{white}{\bfseries 비고} \\ \hline")
    for c in criteria:
        desc   = tex_escape(c.get("description", ""))
        pts    = str(c.get("points", ""))
        note   = tex_escape(c.get("note", ""))
        b.L(rf"{desc} & {pts} & & {note} \\ \hline")
    b.L(r"\end{tabular}")
    b.L(r"\vspace{4mm}")


# ─────────────────────────────────────────────
# xelatex 컴파일
# ─────────────────────────────────────────────

def compile_tex(tex_source: str, output_pdf: str) -> str:
    """
    tex_source 문자열을 임시 디렉토리에서 xelatex로 컴파일하여
    output_pdf 경로에 저장한다.
    """
    xelatex = find_xelatex()
    with tempfile.TemporaryDirectory() as tmpdir:
        tex_path = os.path.join(tmpdir, "doc.tex")
        with open(tex_path, "w", encoding="utf-8") as f:
            f.write(tex_source)

        # 2회 컴파일 (lastpage 등 크로스 레퍼런스 반영)
        cmd = [
            xelatex,
            "-interaction=nonstopmode",
            "-no-shell-escape",
            "-output-directory", tmpdir,
            tex_path,
        ]
        for _ in range(2):
            result = subprocess.run(
                cmd, capture_output=True, text=True, cwd=tmpdir
            )

        pdf_tmp = os.path.join(tmpdir, "doc.pdf")
        if not os.path.exists(pdf_tmp):
            raise RuntimeError("xelatex 컴파일 실패: PDF 생성에 실패했습니다. TeX 소스를 확인하세요.")

        Path(output_pdf).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(pdf_tmp, output_pdf)

    return output_pdf


# ─────────────────────────────────────────────
# 진입점
# ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="JSON → LaTeX(xelatex) → A4 PDF (한글 + 수식 완전 지원)"
    )
    parser.add_argument("input",    help="입력 JSON 파일")
    parser.add_argument("output",   help="출력 PDF 파일")
    parser.add_argument("--template", default=None,
                        help="school_template.json 경로")
    parser.add_argument("--tex",    action="store_true",
                        help=".tex 소스도 같은 폴더에 저장")
    args = parser.parse_args()

    with open(args.input, encoding="utf-8") as f:
        data = json.load(f)

    config = load_template(args.template)

    doc_type       = data.get("document_type", "worksheet")
    worksheet_style = data.get("worksheet_style", "")

    if worksheet_style == "step_practice":
        tex_source = build_step_practice_tex(data, config)
    elif doc_type == "assessment":
        tex_source = build_assessment_tex(data, config)
    else:
        tex_source = build_worksheet_tex(data, config)

    if args.tex:
        tex_out = str(Path(args.output).with_suffix(".tex"))
        with open(tex_out, "w", encoding="utf-8") as f:
            f.write(tex_source)
        print(f"TeX 소스 저장: {tex_out}")

    saved = compile_tex(tex_source, args.output)
    print(f"PDF 생성 완료: {saved}")


if __name__ == "__main__":
    main()
