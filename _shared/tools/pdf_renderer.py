"""
SchoolPdfRenderer — A4 PDF 직접 생성기
JSON 입력 → fpdf2 기반 A4 PDF 출력 (한글 폰트 지원)

사용법:
  python pdf_renderer.py worksheet.json output.pdf
  python pdf_renderer.py assessment.json output.pdf --template school_template.json
"""

import json
import sys
import os
import re
import argparse
from pathlib import Path
from typing import Optional


# ─────────────────────────────────────────────
# 의존성 체크
# ─────────────────────────────────────────────
try:
    from fpdf import FPDF
    from fpdf.enums import XPos, YPos
except ImportError:
    print("ERROR: fpdf2가 설치되지 않았습니다. 다음 명령으로 설치하세요:")
    print("  pip install fpdf2")
    sys.exit(1)

from pdf_math_renderer import latex_to_png, strip_latex_delimiters, HAS_MATPLOTLIB
from pdf_layout import StepPracticeMixin


# ─────────────────────────────────────────────
# 상수
# ─────────────────────────────────────────────
A4_W = 210  # mm
A4_H = 297  # mm

# 문제 유형별 높이 추정 (mm)
HEIGHT_MULTICHOICE_BASE = 30
HEIGHT_MULTICHOICE_PER_CHOICE = 7
HEIGHT_SHORT_ANSWER = 30
HEIGHT_ESSAY_BASE = 30
HEIGHT_ESSAY_ANSWER_BOX = 35
HEIGHT_CALC_BASE = 30
HEIGHT_CALC_PER_LINE = 10
HEIGHT_CALC_ANSWER_LINES = 4

# 폰트 후보 (macOS 기준)
FONT_CANDIDATES = [
    "/System/Library/Fonts/AppleSDGothicNeo.ttc",
    "/Library/Fonts/AppleGothic.ttf",
    "/System/Library/Fonts/Supplemental/AppleGothic.ttf",
    "/usr/share/fonts/truetype/nanum/NanumGothic.ttf",  # Linux
]


# ─────────────────────────────────────────────
# 폰트 탐색
# ─────────────────────────────────────────────
def find_korean_font() -> Optional[str]:
    """시스템에서 한글 폰트 경로를 탐색한다."""
    for path in FONT_CANDIDATES:
        if os.path.exists(path):
            return path
    return None



# ─────────────────────────────────────────────
# 문제 높이 사전 계산
# ─────────────────────────────────────────────
def estimate_problem_height(problem: dict) -> float:
    """문제 하나의 인쇄 높이(mm)를 추정한다."""
    ptype = problem.get("type", "서술형")
    if ptype == "객관식":
        choices = problem.get("choices", [])
        return HEIGHT_MULTICHOICE_BASE + len(choices) * HEIGHT_MULTICHOICE_PER_CHOICE
    if ptype == "단답형":
        return HEIGHT_SHORT_ANSWER
    if ptype == "계산형":
        lines = HEIGHT_CALC_ANSWER_LINES
        return HEIGHT_CALC_BASE + lines * HEIGHT_CALC_PER_LINE
    # 서술형
    return HEIGHT_ESSAY_BASE + HEIGHT_ESSAY_ANSWER_BOX


# ─────────────────────────────────────────────
# SchoolPdfRenderer
# ─────────────────────────────────────────────
class SchoolPdfRenderer(StepPracticeMixin):
    """
    JSON 워크시트/수행평가 데이터를 A4 PDF로 렌더링한다.

    config: school_template.json 내용 (dict)
    """

    def __init__(self, config: dict):
        self.config = config
        self.margins = config.get("margins", {"top": 15, "right": 15, "bottom": 20, "left": 15})
        self.font_path = self._resolve_font(config.get("fonts", {}))
        self.pdf = FPDF(orientation="P", unit="mm", format="A4")
        self.pdf.set_auto_page_break(auto=True, margin=self.margins["bottom"])
        self._register_fonts()
        self._page_number = 0
        self._math_tmp_files: list[str] = []

    # ── 폰트 ──────────────────────────────────

    def _resolve_font(self, fonts_config: dict) -> Optional[str]:
        for key in ("primary", "fallback"):
            name = fonts_config.get(key)
            if name:
                for candidate in FONT_CANDIDATES:
                    if name.lower() in candidate.lower() and os.path.exists(candidate):
                        return candidate
        return find_korean_font()

    def _register_fonts(self):
        if self.font_path:
            self.pdf.add_font("Korean", "", self.font_path)
            self.pdf.add_font("Korean", "B", self.font_path)
        else:
            raise RuntimeError(
                "한글 폰트를 찾을 수 없습니다. AppleSDGothicNeo 또는 NanumGothic을 설치하세요."
            )

    def _set_font(self, size: int = 10, bold: bool = False):
        style = "B" if bold else ""
        self.pdf.set_font("Korean", style=style, size=size)

    # ── 페이지 관리 ───────────────────────────

    def _new_page(self):
        self.pdf.add_page()
        self._page_number += 1
        self.pdf.set_margins(
            left=self.margins["left"],
            top=self.margins["top"],
            right=self.margins["right"],
        )

    def _usable_width(self) -> float:
        return A4_W - self.margins["left"] - self.margins["right"]

    def _remaining_height(self) -> float:
        return A4_H - self.margins["bottom"] - self.pdf.get_y()

    def _ensure_space(self, needed_mm: float):
        """필요한 공간이 부족하면 새 페이지를 시작한다."""
        if self._remaining_height() < needed_mm:
            self._new_page()
            self._render_continuation_header()

    # ── 헤더 ──────────────────────────────────

    def render_header(self, data: dict):
        """
        첫 페이지 헤더: 교표 + 제목 + 점수란 + 학생정보란
        data 키: title, subject, grade, semester, total_points, date,
                 document_type ("worksheet"|"assessment"),
                 assessment_meta (수행평가 전용)
        """
        self._new_page()
        logo_path = self.config.get("logo_path")

        # 로고
        if logo_path and os.path.exists(logo_path):
            self.pdf.image(logo_path, x=self.margins["left"], y=self.margins["top"],
                           w=15, h=15)
            self.pdf.set_y(self.margins["top"])
            self.pdf.set_x(self.margins["left"] + 18)
        else:
            self.pdf.set_y(self.margins["top"])
            self.pdf.set_x(self.margins["left"])

        # 제목 행
        grade = data.get("grade", "")
        semester = data.get("semester", "")
        subject = data.get("subject_display", data.get("subject", ""))
        title = data.get("title", data.get("topic", "학습지"))
        header_fmt = self.config.get(
            "header_format", "{grade} {semester} {subject}"
        ).format(grade=grade, semester=semester, subject=subject)

        self._set_font(size=9)
        self.pdf.cell(0, 5, header_fmt, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        self._set_font(size=14, bold=True)
        self.pdf.cell(0, 8, title, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        # 수행평가 메타 (선택)
        assessment_meta = data.get("assessment_meta")
        if assessment_meta:
            self._set_font(size=9)
            meta_parts = []
            if assessment_meta.get("time_limit"):
                meta_parts.append(f"시간: {assessment_meta['time_limit']}분")
            if assessment_meta.get("materials"):
                meta_parts.append(f"준비물: {', '.join(assessment_meta['materials'])}")
            if meta_parts:
                self.pdf.cell(0, 5, "  |  ".join(meta_parts),
                              new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        self.pdf.ln(2)

        # 학생정보 + 점수란
        self._render_student_info_bar(data)
        self.pdf.ln(4)

    def _render_student_info_bar(self, data: dict):
        """학년·반·번·이름 칸 + 점수 박스를 한 행으로 렌더링한다."""
        fields = self.config.get("student_info_fields", ["학년", "반", "번", "이름"])
        total_points = data.get("total_points", 100)
        w = self._usable_width()

        # 점수 박스 폭
        score_w = 28
        fields_w = w - score_w - 2

        field_w = fields_w / len(fields)
        x_start = self.margins["left"]
        y = self.pdf.get_y()

        self.pdf.set_draw_color(0, 0, 0)
        self.pdf.set_line_width(0.3)

        for i, field in enumerate(fields):
            x = x_start + i * field_w
            self.pdf.set_xy(x, y)
            self._set_font(size=8, bold=True)
            self.pdf.cell(18, 8, field, border=1)
            self.pdf.cell(field_w - 18, 8, "", border=1)

        # 점수 박스
        x = x_start + fields_w + 2
        self.pdf.set_xy(x, y)
        self._set_font(size=8, bold=True)
        self.pdf.cell(score_w, 4, f"/ {total_points}점", border="LRT", align="C",
                      new_x=XPos.LEFT, new_y=YPos.NEXT)
        self.pdf.set_x(x)
        self.pdf.cell(score_w, 4, "점수", border="LRB", align="C")

        self.pdf.set_xy(self.margins["left"], y + 8)

    def _render_continuation_header(self):
        """2페이지 이후 상단 연속 헤더 (소형)."""
        self._set_font(size=8)
        self.pdf.set_text_color(120, 120, 120)
        self.pdf.cell(0, 5, f"(계속) — {self._page_number}페이지",
                      new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.pdf.set_text_color(0, 0, 0)
        self.pdf.ln(2)

    # ── 문제 렌더링 ───────────────────────────

    def render_problem(self, problem: dict, number: int):
        """문제 하나를 렌더링한다. 필요 시 자동 페이지 분할."""
        height = estimate_problem_height(problem)
        self._ensure_space(height)

        ptype = problem.get("type", "서술형")
        bloom = problem.get("bloom_level", "")
        difficulty = problem.get("difficulty", "")
        points = problem.get("points", 10)

        # 문제 번호 + 메타
        self._set_font(size=10, bold=True)
        meta = f"[{bloom}·{difficulty}·{points}점]"
        self.pdf.cell(10, 6, f"{number}.", new_x=XPos.RIGHT, new_y=YPos.LAST)
        self._set_font(size=8)
        self.pdf.cell(0, 6, meta, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        # 문제 본문
        question = problem.get("question", "")
        self._render_text_with_math(question, size=10)
        self.pdf.ln(1)

        # 유형별 렌더링
        if ptype == "객관식":
            self._render_choices(problem.get("choices", []))
            self._render_answer_blank(label="답: ___________")
        elif ptype == "단답형":
            self._render_answer_blank(label="답: _______________________________")
        elif ptype == "계산형":
            self._render_calculation_box()
        else:  # 서술형
            self._render_essay_box()

        self.pdf.ln(3)

    def _render_text_with_math(self, text: str, size: int = 10):
        """
        $...$ LaTeX 수식을 PNG 이미지로 임베드하며 텍스트를 렌더링한다.
        수식이 없으면 일반 multi_cell로 렌더링한다.
        """
        if "$" not in text:
            self._set_font(size=size)
            self.pdf.multi_cell(self._usable_width(), 5, text)
            return

        # 텍스트를 $$...$$ 또는 $...$ 기준으로 분할 (display math 우선)
        parts = re.split(r"(\$\$[^$]+\$\$|\$[^$]+\$)", text)
        self._set_font(size=size)

        for part in parts:
            if part.startswith("$") and part.endswith("$") and len(part) > 2:
                formula = strip_latex_delimiters(part)
                img_path = latex_to_png(formula, fontsize=size)
                if img_path:
                    self._math_tmp_files.append(img_path)
                    # 인라인 이미지 삽입 — 현재 줄 높이와 맞춤
                    line_h_mm = size * 0.5
                    self.pdf.image(img_path, h=line_h_mm)
                else:
                    # 폴백: 텍스트로 표시
                    self.pdf.write(5, part)
            else:
                self.pdf.write(5, part)
        self.pdf.ln(5)

    def _render_choices(self, choices: list[str]):
        self._set_font(size=10)
        labels = ["①", "②", "③", "④", "⑤"]
        for i, choice in enumerate(choices[:5]):
            label = labels[i] if i < len(labels) else f"{i+1}."
            self.pdf.cell(8, 6, label)
            self.pdf.multi_cell(self._usable_width() - 8, 6, choice)

    def _render_answer_blank(self, label: str = "답: ___________"):
        self._set_font(size=10)
        self.pdf.cell(0, 6, label, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    def _render_calculation_box(self):
        """계산형 — 풀이 칸 (3줄)."""
        self._set_font(size=9)
        self.pdf.cell(0, 5, "풀이 과정:", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.pdf.set_draw_color(180, 180, 180)
        for _ in range(HEIGHT_CALC_ANSWER_LINES):
            self.pdf.cell(self._usable_width(), HEIGHT_CALC_PER_LINE, "",
                          border="B", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.pdf.set_draw_color(0, 0, 0)

    def _render_essay_box(self):
        """서술형 — 답안 박스."""
        self._set_font(size=9)
        self.pdf.cell(0, 5, "답:", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.pdf.set_draw_color(0, 0, 0)
        self.pdf.rect(
            self.margins["left"],
            self.pdf.get_y(),
            self._usable_width(),
            HEIGHT_ESSAY_ANSWER_BOX,
        )
        self.pdf.set_y(self.pdf.get_y() + HEIGHT_ESSAY_ANSWER_BOX)

    # ── 수행평가 전용 요소 ────────────────────

    def render_rubric(self, rubric: dict):
        """채점 기준표(루브릭) 렌더링."""
        criteria = rubric.get("criteria", [])
        if not criteria:
            return

        self._ensure_space(len(criteria) * 12 + 20)
        self._set_font(size=10, bold=True)
        self.pdf.cell(0, 7, "채점 기준표", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        # 헤더
        w = self._usable_width()
        col_widths = [w * 0.45, w * 0.15, w * 0.15, w * 0.25]
        headers = ["평가 기준", "배점", "득점", "비고"]

        self._set_font(size=9, bold=True)
        self.pdf.set_fill_color(220, 220, 220)
        for i, (header, col_w) in enumerate(zip(headers, col_widths)):
            self.pdf.cell(col_w, 7, header, border=1, fill=True, align="C")
        self.pdf.ln()

        # 행
        self._set_font(size=9)
        self.pdf.set_fill_color(255, 255, 255)
        for criterion in criteria:
            desc = criterion.get("description", "")
            points = str(criterion.get("points", ""))
            note = criterion.get("note", "")
            row = [desc, points, "", note]
            for i, (cell_text, col_w) in enumerate(zip(row, col_widths)):
                self.pdf.cell(col_w, 7, cell_text, border=1)
            self.pdf.ln()

        self.pdf.ln(3)

    def render_activity_section(self, section: dict):
        """활동 섹션 (수행평가 내 활동형 문제 묶음)."""
        self._ensure_space(20)
        title = section.get("title", "")
        instructions = section.get("instructions", "")

        self._set_font(size=11, bold=True)
        self.pdf.set_fill_color(240, 240, 240)
        self.pdf.cell(0, 7, f"▶ {title}", border="B", fill=True,
                      new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.pdf.ln(1)

        if instructions:
            self._set_font(size=9)
            self.pdf.multi_cell(self._usable_width(), 5, f"[지시사항] {instructions}")
            self.pdf.ln(2)

        for i, problem in enumerate(section.get("problems", []), 1):
            self.render_problem(problem, i)

    # ── 정답지 ────────────────────────────────

    def render_answer_key(self, problems: list[dict]):
        """모범답안 페이지를 새 페이지에 렌더링한다."""
        self._new_page()
        self._set_font(size=13, bold=True)
        self.pdf.cell(0, 8, "정답 및 풀이", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.pdf.set_draw_color(0, 0, 0)
        self.pdf.line(
            self.margins["left"], self.pdf.get_y(),
            A4_W - self.margins["right"], self.pdf.get_y()
        )
        self.pdf.ln(3)

        for i, problem in enumerate(problems, 1):
            self._ensure_space(30)
            number = problem.get("number", i)
            answer = problem.get("answer", "")
            steps = problem.get("solution_steps", [])

            # 문제 번호 + 정답 (LaTeX 수식 지원)
            self._set_font(size=10, bold=True)
            self.pdf.cell(12, 6, f"{number}번.")
            self._set_font(size=10)
            self.pdf.write(6, "정답: ")
            self._render_text_with_math(answer, size=10)

            # 풀이 단계 (LaTeX 수식 지원)
            if steps:
                for step in steps:
                    self._ensure_space(12)
                    label = step.get("step_label", "")
                    explanation = step.get("explanation", "")
                    self._set_font(size=9)
                    self.pdf.set_x(self.margins["left"] + 6)
                    self.pdf.write(5, f"{label}  ")
                    self._render_text_with_math(explanation, size=9)
            self.pdf.ln(3)

    # ── 페이지 번호 ───────────────────────────

    def _render_page_numbers(self):
        """모든 페이지 하단 중앙에 페이지 번호를 삽입한다."""
        fmt = self.config.get("page_number_format", "- {n} -")
        total = len(self.pdf.pages)
        # auto_page_break를 끄지 않으면 set_y 후 cell()이 다음 페이지를 생성함
        self.pdf.set_auto_page_break(False)
        try:
            for i in range(1, total + 1):
                self.pdf.page = i
                self.pdf.set_y(A4_H - self.margins["bottom"] + 3)
                self._set_font(size=8)
                self.pdf.cell(0, 5, fmt.format(n=i, total=total), align="C")
        finally:
            self.pdf.set_auto_page_break(True, margin=self.margins["bottom"])

    # ── 저장 ──────────────────────────────────

    def save(self, output_path: str):
        """PDF 파일로 저장한다. 임시 수식 이미지 파일도 정리한다."""
        self._render_page_numbers()
        self.pdf.output(output_path)

        for tmp_file in self._math_tmp_files:
            try:
                os.unlink(tmp_file)
            except OSError:
                pass

        return output_path


# ─────────────────────────────────────────────
# 진입점 — JSON → PDF
# ─────────────────────────────────────────────

def load_template(template_path: Optional[str]) -> dict:
    """school_template.json을 로드한다. 없으면 기본값 반환."""
    default = {
        "logo_path": None,
        "header_format": "{grade}학년 {semester}학기 {subject}",
        "student_info_fields": ["학년", "반", "번", "이름"],
        "page_number_format": "- {n} -",
        "margins": {"top": 15, "right": 15, "bottom": 20, "left": 15},
        "fonts": {"primary": "AppleSDGothicNeo", "fallback": "AppleGothic"},
    }
    if not template_path:
        # 기본 경로 탐색
        default_path = Path(__file__).parent.parent / "config" / "school_template.json"
        if default_path.exists():
            template_path = str(default_path)

    if template_path and os.path.exists(template_path):
        with open(template_path, encoding="utf-8") as f:
            loaded = json.load(f)
            return {**default, **loaded}

    return default


def render_worksheet(data: dict, renderer: SchoolPdfRenderer):
    """worksheet 타입 JSON을 렌더링한다."""
    renderer.render_header(data)
    problems = data.get("problems", [])
    for i, problem in enumerate(problems, 1):
        renderer.render_problem(problem, i)

    if data.get("include_answer_key", True):
        renderer.render_answer_key(problems)


def render_assessment(data: dict, renderer: SchoolPdfRenderer):
    """assessment 타입 JSON을 렌더링한다."""
    renderer.render_header(data)

    # 루브릭 (있을 때만)
    rubric = data.get("rubric")
    if rubric:
        renderer.render_rubric(rubric)

    # 활동 섹션 or 일반 문제 목록
    sections = data.get("sections")
    if sections:
        for section in sections:
            renderer.render_activity_section(section)
    else:
        problems = data.get("problems", [])
        for i, problem in enumerate(problems, 1):
            renderer.render_problem(problem, i)

    if data.get("include_answer_key", True):
        all_problems = data.get("problems", [])
        if not all_problems and sections:
            all_problems = [p for s in sections for p in s.get("problems", [])]
        renderer.render_answer_key(all_problems)


def main():
    parser = argparse.ArgumentParser(
        description="JSON → A4 PDF 렌더러 (학습지/수행평가)"
    )
    parser.add_argument("input", help="입력 JSON 파일 경로")
    parser.add_argument("output", help="출력 PDF 파일 경로")
    parser.add_argument(
        "--template",
        help="school_template.json 경로 (기본: _shared/config/school_template.json)",
        default=None,
    )
    args = parser.parse_args()

    # 입력 로드
    with open(args.input, encoding="utf-8") as f:
        data = json.load(f)

    # 출력 디렉토리 생성
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # 템플릿 로드
    config = load_template(args.template)

    # 렌더러 초기화
    renderer = SchoolPdfRenderer(config)

    # 문서 타입 / 스타일에 따라 렌더링
    doc_type = data.get("document_type", "worksheet")
    worksheet_style = data.get("worksheet_style", "")

    if worksheet_style == "step_practice":
        renderer.render_step_practice(data)
    elif doc_type == "assessment":
        render_assessment(data, renderer)
    else:
        render_worksheet(data, renderer)

    # 저장
    saved = renderer.save(str(output_path))
    print(f"PDF 생성 완료: {saved}")


if __name__ == "__main__":
    main()
