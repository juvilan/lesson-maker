"""
pdf_layout — Step Practice 워크시트 레이아웃 믹스인

SchoolPdfRenderer가 이 믹스인을 상속하여 step_practice 렌더링 기능을 얻는다.
믹스인 메서드는 self.pdf, self.margins, self._set_font(), self._ensure_space(),
self._usable_width(), self._new_page() 등 SchoolPdfRenderer 기반 메서드에 의존한다.
"""

from fpdf.enums import XPos, YPos

A4_W = 210  # mm — pdf_renderer 와 동일한 값


class StepPracticeMixin:
    """
    step_practice 형식 워크시트 렌더링 메서드 묶음.
    SchoolPdfRenderer 에 mixin으로 포함되어 사용한다.
    """

    # ── Step 기반 워크시트 (step_practice) ────────────────────────────

    def render_step_practice(self, data: dict):
        """
        step_practice 형식의 워크시트를 렌더링한다.
        구조: 헤더 → context_box → steps[] → checklist → (답안지)
        """
        self._render_step_header_page(data)
        context = data.get("context_box")
        if context:
            self._render_context_box(context)

        for step in data.get("steps", []):
            self._render_step_section(step, for_answer=False)

        checklist = data.get("checklist", [])
        if checklist:
            self._render_checklist(checklist)

        if data.get("include_answer_key", True):
            self._render_step_answer_key(data)

    def _render_step_header_page(self, data: dict):
        """Step 워크시트 전용 헤더 (점수란 없음, 학번·이름만)."""
        self._new_page()
        subject = data.get("subject_display", data.get("subject", ""))
        topic = data.get("topic", "")
        subtitle = data.get("subtitle", "")

        # 소제목 태그
        self._set_font(size=8)
        self.pdf.set_text_color(150, 150, 150)
        tag = f"Practice Worksheet  ·  {subject}"
        self.pdf.cell(0, 5, tag, align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.pdf.set_text_color(0, 0, 0)

        # 제목
        self._set_font(size=15, bold=True)
        self.pdf.cell(0, 9, topic, align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        # 부제목
        if subtitle:
            self._set_font(size=10)
            self.pdf.set_text_color(100, 100, 100)
            self.pdf.cell(0, 6, subtitle, align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            self.pdf.set_text_color(0, 0, 0)

        # 구분선
        self.pdf.set_draw_color(30, 30, 30)
        self.pdf.set_line_width(0.5)
        y = self.pdf.get_y() + 2
        self.pdf.line(self.margins["left"], y, A4_W - self.margins["right"], y)
        self.pdf.set_line_width(0.3)
        self.pdf.set_draw_color(0, 0, 0)
        self.pdf.set_y(y + 4)

        # 학번 · 이름
        self._set_font(size=10)
        self.pdf.cell(12, 7, "학번")
        self.pdf.cell(55, 7, "", border="B")
        self.pdf.cell(6, 7, "")
        self.pdf.cell(12, 7, "이름")
        self.pdf.cell(40, 7, "", border="B")
        self.pdf.ln(10)

    def _render_context_box(self, context: dict):
        """문제 상황 박스 (테두리 있는 박스)."""
        self._ensure_space(35)
        self._render_step_badge(context.get("label", "상황"), context.get("title", ""))
        self.pdf.ln(1)

        y_start = self.pdf.get_y()
        w = self._usable_width()
        self._set_font(size=10)

        lines = [context.get("intro", "")]
        for item in context.get("items", []):
            lines.append(f"  {item}")

        # 높이 계산 (각 줄 6mm)
        box_h = len(lines) * 6 + 6
        self.pdf.rect(self.margins["left"], y_start, w, box_h)
        self.pdf.set_xy(self.margins["left"] + 3, y_start + 3)

        for line in lines:
            self._set_font(size=10)
            self.pdf.cell(w - 6, 6, line, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            self.pdf.set_x(self.margins["left"] + 3)

        self.pdf.set_y(y_start + box_h + 3)

    def _render_step_badge(self, badge: str, title: str, subtitle: str = ""):
        """STEP N 배지 + 제목 행."""
        self._set_font(size=8, bold=True)
        self.pdf.set_fill_color(60, 60, 60)
        self.pdf.set_text_color(255, 255, 255)
        badge_w = max(len(badge) * 3.5 + 8, 18)
        self.pdf.cell(badge_w, 6, badge, fill=True, align="C")
        self.pdf.set_text_color(0, 0, 0)
        self.pdf.cell(3, 6, "")
        self._set_font(size=10, bold=True)
        self.pdf.cell(80, 6, title)
        if subtitle:
            self._set_font(size=9)
            self.pdf.set_text_color(120, 120, 120)
            self.pdf.cell(0, 6, f"  {subtitle}")
            self.pdf.set_text_color(0, 0, 0)
        self.pdf.ln(7)

    def _render_note_box(self, text: str):
        """회색 배경 안내 박스."""
        self._ensure_space(15)
        lines = text.split("\n")
        box_h = len(lines) * 5 + 6
        y = self.pdf.get_y()
        w = self._usable_width()

        self.pdf.set_fill_color(247, 247, 247)
        self.pdf.set_draw_color(180, 180, 180)
        self.pdf.set_line_width(0.8)
        # 좌측 굵은 선
        self.pdf.line(self.margins["left"], y, self.margins["left"], y + box_h)
        self.pdf.set_line_width(0.2)
        self.pdf.rect(self.margins["left"], y, w, box_h, style="F")
        self.pdf.set_draw_color(0, 0, 0)
        self.pdf.set_line_width(0.3)

        self.pdf.set_xy(self.margins["left"] + 4, y + 2)
        for line in lines:
            self._set_font(size=9)
            self.pdf.set_text_color(60, 60, 60)
            self.pdf.cell(w - 8, 5, line, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            self.pdf.set_x(self.margins["left"] + 4)
        self.pdf.set_text_color(0, 0, 0)
        self.pdf.set_y(y + box_h + 3)

    def _render_fill_lines(self, fill_lines: list, for_answer: bool = False):
        """빈칸 채우기 줄 목록."""
        self._ensure_space(len(fill_lines) * 9 + 5)
        w = self._usable_width()

        self.pdf.set_draw_color(0, 0, 0)
        self.pdf.set_fill_color(245, 245, 245)

        box_y = self.pdf.get_y()
        box_h = len(fill_lines) * 8 + 6
        self.pdf.set_draw_color(180, 180, 180)
        self.pdf.rect(self.margins["left"], box_y, w, box_h)
        self.pdf.set_draw_color(0, 0, 0)

        self.pdf.set_xy(self.margins["left"] + 3, box_y + 3)

        for item in fill_lines:
            label = item.get("label", "")
            given = item.get("given")
            note = item.get("note", "")
            answer = item.get("answer", "")

            self._set_font(size=9)
            label_text = f"{label} : "
            label_w = min(len(label_text) * 2.5 + 5, 55)

            self.pdf.cell(label_w, 7, label_text)

            if given:
                self.pdf.set_fill_color(240, 240, 240)
                self._set_font(size=9)
                self.pdf.cell(w - label_w - 6, 7, given, fill=True)
            elif for_answer and answer:
                self.pdf.set_fill_color(230, 245, 230)
                self._set_font(size=9)
                self.pdf.cell(w - label_w - 6, 7, answer, fill=True)
            else:
                self.pdf.set_fill_color(255, 255, 255)
                self.pdf.cell(w - label_w - 6, 7, "", border="B")

            if note:
                self.pdf.set_xy(self.pdf.get_x() - 20, self.pdf.get_y())

            self.pdf.ln(8)
            self.pdf.set_x(self.margins["left"] + 3)
            self.pdf.set_fill_color(255, 255, 255)

        self.pdf.set_y(box_y + box_h + 3)

    def _render_step_table(self, table_data: dict, for_answer: bool = False):
        """STEP 테이블 렌더링 (blank/given/sub 셀 타입)."""
        headers = table_data.get("headers", [])
        rows = table_data.get("rows", [])
        if not headers or not rows:
            return

        self._ensure_space(len(rows) * 9 + 14)

        w = self._usable_width()
        n_data_cols = len(headers) - 1  # 첫 열은 행 레이블
        label_col_w = 20
        data_col_w = (w - label_col_w) / max(n_data_cols, 1)

        # 헤더
        self.pdf.set_fill_color(60, 60, 60)
        self.pdf.set_text_color(255, 255, 255)
        self._set_font(size=9, bold=True)
        self.pdf.cell(label_col_w, 7, headers[0], border=1, fill=True, align="C")
        for h in headers[1:]:
            self.pdf.cell(data_col_w, 7, h, border=1, fill=True, align="C")
        self.pdf.ln()
        self.pdf.set_text_color(0, 0, 0)

        # 데이터 행
        for row in rows:
            label = row.get("label", "")
            cells = row.get("cells", [])

            self.pdf.set_fill_color(240, 240, 240)
            self._set_font(size=9, bold=True)
            self.pdf.cell(label_col_w, 8, label, border=1, fill=True, align="C")

            for cell in cells:
                ctype = cell.get("type", "blank")
                val = cell.get("v", "")
                answer = cell.get("answer", "")

                if ctype == "given":
                    self.pdf.set_fill_color(245, 245, 245)
                    self._set_font(size=9)
                    self.pdf.cell(data_col_w, 8, val, border=1, fill=True, align="C")
                elif ctype == "sub":
                    self.pdf.set_fill_color(250, 250, 250)
                    self._set_font(size=7)
                    self.pdf.set_text_color(160, 160, 160)
                    self.pdf.cell(data_col_w, 8, val, border=1, fill=True, align="C")
                    self.pdf.set_text_color(0, 0, 0)
                elif for_answer and answer:
                    self.pdf.set_fill_color(230, 245, 230)
                    self._set_font(size=9)
                    self.pdf.cell(data_col_w, 8, answer, border=1, fill=True, align="C")
                else:
                    self.pdf.set_fill_color(255, 255, 255)
                    self._set_font(size=9)
                    self.pdf.cell(data_col_w, 8, "", border=1, fill=True, align="C")

            self.pdf.ln()

        self.pdf.set_fill_color(255, 255, 255)
        self.pdf.ln(1)

    def _render_follow_up(self, text: str, answer: str = "", for_answer: bool = False):
        """테이블 아래 추가 빈칸 문장."""
        self._ensure_space(10)
        self._set_font(size=9)
        self.pdf.set_text_color(80, 80, 80)
        prefix = "*  "
        if for_answer and answer:
            self.pdf.multi_cell(self._usable_width(), 5,
                                f"{prefix}{text}\n    → 정답: {answer}")
        else:
            self.pdf.multi_cell(self._usable_width(), 5, f"{prefix}{text}")
        self.pdf.set_text_color(0, 0, 0)
        self.pdf.ln(2)

    def _render_essay_section(self, questions: list, for_answer: bool = False):
        """서술형 질문 목록."""
        for q in questions:
            question = q.get("question", "")
            answer = q.get("answer", "")
            self._ensure_space(40)

            self._set_font(size=10, bold=True)
            self.pdf.multi_cell(self._usable_width(), 5, question)
            self.pdf.ln(1)

            if for_answer and answer:
                self.pdf.set_fill_color(245, 250, 245)
                self._set_font(size=9)
                self.pdf.multi_cell(self._usable_width(), 5, answer, fill=True)
            else:
                box_h = 28
                y = self.pdf.get_y()
                self.pdf.set_fill_color(255, 255, 255)
                self.pdf.set_draw_color(200, 200, 200)
                self.pdf.rect(self.margins["left"], y, self._usable_width(), box_h)
                for line_i in range(1, 4):
                    ly = y + line_i * 7
                    self.pdf.line(self.margins["left"], ly,
                                  self.margins["left"] + self._usable_width(), ly)
                self.pdf.set_draw_color(0, 0, 0)
                self.pdf.set_y(y + box_h)
            self.pdf.ln(4)

    def _render_checklist(self, items: list):
        """자기 확인 체크리스트."""
        self._ensure_space(len(items) * 7 + 14)
        w = self._usable_width()
        y = self.pdf.get_y()
        box_h = len(items) * 6 + 10

        self.pdf.set_draw_color(200, 200, 200)
        self.pdf.rect(self.margins["left"], y, w, box_h)
        self.pdf.set_draw_color(0, 0, 0)

        self.pdf.set_xy(self.margins["left"] + 3, y + 3)
        self._set_font(size=9, bold=True)
        self.pdf.cell(0, 5, "확인 체크리스트", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.pdf.set_x(self.margins["left"] + 3)

        for item in items:
            self._set_font(size=9)
            self.pdf.set_text_color(80, 80, 80)
            self.pdf.cell(0, 6, f"□  {item}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            self.pdf.set_x(self.margins["left"] + 3)

        self.pdf.set_text_color(0, 0, 0)
        self.pdf.set_y(y + box_h + 4)

    def _render_step_section(self, step: dict, for_answer: bool = False):
        """단일 STEP 섹션을 렌더링한다."""
        stype = step.get("type", "")
        # 헤더만 달랑 남는 고아 방지: 타입별 최소 필요 공간
        if stype == "essay":
            min_space = 55
        elif stype == "table":
            rows = len(step.get("table", {}).get("rows", []))
            min_space = 14 + rows * 9 + 15
        elif stype == "fill_lines":
            lines = len(step.get("fill_lines", []))
            min_space = lines * 8 + 20
        else:
            min_space = 30
        self._ensure_space(min_space)

        badge = step.get("badge", "")
        title = step.get("title", "")
        subtitle = step.get("subtitle", "")
        note = step.get("note")
        stype = step.get("type", "")

        self._render_step_badge(badge, title, subtitle)

        if note:
            self._render_note_box(note)

        if stype == "fill_lines":
            self._render_fill_lines(step.get("fill_lines", []), for_answer=for_answer)

        elif stype == "table":
            self._render_step_table(step.get("table", {}), for_answer=for_answer)
            follow_up = step.get("follow_up", "")
            if follow_up:
                self._render_follow_up(
                    follow_up,
                    answer=step.get("follow_up_answer", ""),
                    for_answer=for_answer,
                )

        elif stype == "essay":
            self._render_essay_section(step.get("questions", []), for_answer=for_answer)

        self.pdf.ln(2)

    def _render_step_answer_key(self, data: dict):
        """Step 워크시트 정답지 페이지."""
        self._new_page()
        self._set_font(size=13, bold=True)
        self.pdf.cell(0, 8, "정답 및 풀이", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.pdf.set_draw_color(0, 0, 0)
        self.pdf.line(
            self.margins["left"], self.pdf.get_y(),
            A4_W - self.margins["right"], self.pdf.get_y(),
        )
        self.pdf.ln(4)

        for step in data.get("steps", []):
            self._render_step_section(step, for_answer=True)
