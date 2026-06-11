# _shared/tools · 렌더링 도구 안내

이 디렉토리의 스크립트들은 **HTML/PDF 변환 파이프라인**을 담당한다.

## 정책 요약

lesson-maker는 **HTML → PDF** 단일 경로를 표준으로 삼는다.

| 파이프라인 | 도구 | 상태 |
|---|---|---|
| HTML → A4 PDF | `html_to_pdf.py` (Playwright Chromium) | **표준 · 활성** |
| JSON → A4 PDF | `pdf_renderer.py` (fpdf2) | **DEPRECATED · 유지보수 중단** |

---

## 표준 경로: `html_to_pdf.py`

에이전트(`worksheet_generator`, `assessment_generator`, `exam_composer`)가
`_shared/templates/worksheet_base.html`을 기반으로 **HTML을 직접 생성**한다.
이 HTML은 `design-tokens.css` + `worksheet-system.css`를 참조하여 2단 레이아웃,
수능·모의고사 스타일 5지선다, 점수 표기 규칙, 답란 공백 원칙 등
모든 디자인 시스템 결정을 반영한다.

`html_to_pdf.py`가 Playwright로 해당 HTML을 A4 PDF로 변환하며,
페이지 넘침(262mm 초과) 자동 검증까지 포함한다.

### 사용법

```bash
# 단일 파일
python _shared/tools/html_to_pdf.py workspace/{session_id}/worksheet.html

# 디렉토리 전체 (패턴 매칭)
python _shared/tools/html_to_pdf.py ai-math/output/worksheet/ --pattern "학습지_*.html"

# 페이지 넘침 시 실패 (CI용)
python _shared/tools/html_to_pdf.py ai-math/output/exam/ --all --strict
```

---

## DEPRECATED 경로: `pdf_renderer.py`

이 스크립트는 fpdf2로 PDF를 직접 그리는 구식 경로로, **HTML/CSS 디자인 시스템을
전혀 참조하지 않는다.** 다음 이유로 유지보수가 중단되었다:

- 2단 레이아웃 구현 불가
- MathJax 수식 렌더링 불가 (LaTeX → PNG 변환 방식으로 한계)
- 답란에 밑줄·네모 박스가 하드코딩됨 (디자인 시스템 원칙 위배)
- 점수 메타 표기 (`[적용·중·10점]`)가 학생용 본문에 노출
- 새 토큰 시스템·과목 액센트·Pretendard 폰트 반영 불가

### 이전 버전 호환 목적

혹시 과거 세션에서 생성된 JSON을 PDF로 빠르게 뽑아야 하는 경우에만 한시적으로 사용 가능.
새 세션 생성 시에는 절대 이 경로를 선택하지 말 것.

### 스크립트를 직접 삭제하지 않는 이유

- 과거 산출물 재생성 필요 시를 위해 보존
- 혹시 다른 외부 스크립트가 참조하고 있을 가능성
- 삭제 대신 `DEPRECATED` 표시로 충분히 경고 전달

---

## 기타 도구

| 파일 | 역할 |
|---|---|
| `pdf_math_renderer.py` | LaTeX 수식을 PNG로 렌더링 (pdf_renderer.py 의존성) |
| `pdf_layout.py` | 단계별 연습 레이아웃 믹스인 (pdf_renderer.py 의존성) |
| `tex_renderer.py` | 텍스트 내 LaTeX 파싱 유틸 |
| `rename_output.py` | 산출물 파일명 일괄 변경 |
| `deploy.py` | 배포 스크립트 |
| `tests/` | pytest 테스트 |

---

## 에이전트 지침 참고

각 에이전트의 HTML 생성 규칙은 해당 `.md` 파일에 상세 기술되어 있다:

- `_shared/agents/worksheet_generator.md`
- `_shared/agents/assessment_generator.md`
- `_shared/agents/exam_composer.md`
- `_shared/agents/exam_bank_generator.md`
- `_shared/agents/slide_creator.md`
