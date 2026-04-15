# R01 리뷰 결과

카테고리: quality
발견된 이슈: 18개
완료 시각: 2026-03-24T08:34:55.918Z

## 발견된 이슈

### F001 [HIGH]
- file: `_shared/tools/pdf_math_renderer.py`
- line: 43
- severity: high
- category: quality
- message: 임시 파일 리소스 누수. latex_to_png()에서 NamedTemporaryFile(delete=False)로 생성한 파일을 호출자가 삭제해야 하지만, 함수 시그니처나 docstring에 이 책임이 명시되지 않음. pdf_renderer.py의 save()에서 정리하지만, 예외 발생 시 누수 가능.
- suggestion: contextmanager 패턴 또는 반환 시 cleanup 콜백 제공. 최소한 docstring에 "호출자가 삭제 책임" 명시.
- fixable: true

### F002 [MEDIUM]
- file: `_shared/tools/pdf_math_renderer.py`
- line: 53
- severity: medium
- category: quality
- message: strip_latex_delimiters()에서 $...$와 $$...$$ 구분 로직이 동일한 조건문으로 작성되어 있음. 두 if 문 모두 `text.startswith("$") and text.endswith("$")` 조건이 동일하여 $$...$$ 케이스에 도달 불가.
- suggestion: 첫 번째 조건을 `text.startswith("$$") and text.endswith("$$")`로 수정하고 슬라이싱을 `text[2:-2]`로 변경.
- fixable: true

### F003 [HIGH]
- file: `_shared/tools/pdf_renderer.py`
- line: 183
- severity: high
- category: quality
- message: _render_text_with_math()에서 `import re`를 함수 내부에서 반복 호출. 성능 문제는 미미하지만, 파일 상단에 import하는 것이 Python 컨벤션.
- suggestion: 파일 상단으로 `import re` 이동.
- fixable: true

### F004 [MEDIUM]
- file: `_shared/tools/pdf_renderer.py`
- line: 186
- severity: medium
- category: quality
- message: _render_text_with_math()의 정규식 `(\$[^$]+\$)`가 $$...$$ (display math)를 올바르게 처리하지 못함. `$$x^2$$` 입력 시 빈 문자열 파트가 생기거나 잘못된 분할 발생 가능.
- suggestion: display math와 inline math를 모두 처리하는 정규식 사용: `(\$\$[^$]+\$\$|\$[^$]+\$)`
- fixable: true

### F005 [MEDIUM]
- file: `_shared/tools/pdf_renderer.py`
- line: 1
- severity: medium
- category: quality
- message: pdf_renderer.py가 약 350줄로 적절하나, SchoolPdfRenderer 클래스가 StepPracticeMixin 포함 시 합산 800줄 이상. 클래스 책임이 헤더/문제/루브릭/정답지 등 과도하게 넓음.
- suggestion: 렌더링 로직을 문서 타입별(worksheet, assessment, answer_key)로 분리 검토.
- fixable: true

### F006 [MEDIUM]
- file: `_shared/tools/pdf_layout.py`
- line: 1
- severity: medium
- category: quality
- message: StepPracticeMixin이 self.pdf, self.margins, self._set_font() 등 SchoolPdfRenderer의 구체적 속성에 의존하지만 타입 힌트나 Protocol 정의 없음. 믹스인 사용자가 어떤 인터페이스를 제공해야 하는지 불명확.
- suggestion: typing.Protocol로 믹스인이 요구하는 인터페이스를 명시하거나, 최소한 docstring에 필수 메서드 목록 기재.
- fixable: true

### F007 [MEDIUM]
- file: `_shared/tools/deploy.py`
- line: 87
- severity: medium
- category: quality
- message: deploy_category()에서 파일 동일성 비교에 mtime + size만 사용. Google Drive 동기화 환경에서 mtime이 변경될 수 있어 의도치 않은 스킵 또는 불필요한 덮어쓰기 발생 가능.
- suggestion: 해시 기반 비교 옵션 추가 또는 현재 방식의 한계를 docstring에 명시.
- fixable: true

### F008 [MEDIUM]
- file: `_shared/tools/rename_output.py`
- line: 1
- severity: medium
- category: quality
- message: 모든 리네이밍 매핑이 하드코딩된 딕셔너리로 관리됨. 새 파일 추가 시 코드 수정 필요. 현재 ai-math만 지원하며 확장성 부족.
- suggestion: 네이밍 규칙을 JSON/YAML 설정 파일로 분리하거나, 패턴 기반 자동 변환 로직 도입 검토.
- fixable: true

### F009 [MEDIUM]
- file: `_shared/tools/html_to_pdf.py`
- line: 56
- severity: medium
- category: quality
- message: convert_html_to_pdf()에서 MathJax 렌더링 예외를 빈 except로 무시. MathJax가 있지만 렌더링 실패한 경우에도 불완전한 PDF가 생성됨.
- suggestion: except 블록에서 최소한 경고 로그 출력 (예: `print(f"[경고] MathJax 렌더링 대기 실패: {html_path.name}", file=sys.stderr)`).
- fixable: true

### F010 [HIGH]
- file: `_shared/templates/math_animation_lib.js`
- line: 24
- severity: high
- category: quality
- message: 전역 변수 window.mathAnimators를 여러 곳에서 조건 초기화. 생성자(line 24)와 파일 말미(line 375)에서 중복 초기화하여 로딩 순서에 따라 기존 등록이 덮어쓰기될 수 있음.
- suggestion: 파일 상단에서 한 번만 초기화: `window.mathAnimators = window.mathAnimators || {};` 후 생성자에서는 체크 없이 바로 등록.
- fixable: true

### F011 [LOW]
- file: `_shared/templates/math_animation_lib.js`
- line: 228
- severity: low
- category: quality
- message: _resetToStep()에서 reset() 호출 후 모든 단계를 순차 재생. reset()이 이미 currentStep을 -1로 설정하는데, 바로 다음 줄에서 다시 -1로 설정하는 중복 코드.
- suggestion: `this.currentStep = -1;` 중복 제거 (reset()이 이미 처리).
- fixable: true

### F012 [LOW]
- file: `_shared/templates/math_animation_lib.js`
- line: 229
- severity: low
- category: quality
- message: _resetToStep()에서 모든 단계를 동기적으로 재생하지만 _playStep() 내부에서 setTimeout/gsap.delayedCall 사용. 이전 단계 애니메이션 완료 전에 다음 단계가 시작되어 시각적 글리치 발생 가능.
- suggestion: 비동기 재생 체인 또는 즉시 상태 적용 모드(skipAnimation) 추가.
- fixable: true

### F013 [LOW]
- file: `_shared/templates/reveal_base.html`
- line: 23
- severity: low
- category: quality
- message: MathJax 설정에서 `startup.typeset: false`로 초기 타이프셋을 비활성화하고 Reveal 이벤트에서 수동 호출하지만, MathJax 로딩 완료 전에 Reveal ready 이벤트가 발생하면 safeTypeset()이 빈 Promise를 반환하여 수식이 렌더링되지 않을 수 있음.
- suggestion: safeTypeset()에서 mathJaxReady 플래그를 확인하고, 미준비 시 재시도 로직 추가.
- fixable: true

### F014 [LOW]
- file: `_shared/templates/reveal_base.html`
- line: 12
- severity: low
- category: quality
- message: 템플릿 변수 {{THEME}}, {{ACCENT_COLOR}} 등이 미치환 시 CSS가 깨짐. 기본값(fallback)이 없음.
- suggestion: CSS 변수에 기본값 설정: `--accent: var(--custom-accent, #f39c12);` 또는 템플릿 처리 시 유효성 검사.
- fixable: true

### F015 [LOW]
- file: `_shared/templates/worksheet_base.html`
- line: 100
- severity: low
- category: quality
- message: MathJax 설정의 inlineMath 구분자 배열이 `[['$', '$'], ['\\(', '\\)']]` 형태인데, HTML 내에서 코드 리뷰 텍스트와 혼합되어 구분자가 잘못 파싱됨. 실제 파일에서도 `$` 구분자가 일반 텍스트의 달러 기호와 충돌 가능.
- suggestion: 교육용 워크시트에서는 `\\(...\\)` 구분자만 사용하고 `$...$`는 제거 검토.
- fixable: true

### F016 [LOW]
- file: `_shared/templates/worksheet_base.html`
- line: 105
- severity: low
- category: quality
- message: MathJax를 CDN(cdn.jsdelivr.net)에서 로드하지만, reveal_base.html은 오프라인 로컬 파일 사용. 인쇄용 학습지라면 오프라인 환경에서도 동작해야 할 수 있음.
- suggestion: 오프라인 대응이 필요하면 reveal_base.html과 동일하게 로컬 MathJax 사용.
- fixable: true

### F017 [LOW]
- file: `_shared/tools/.pytest_cache/`
- severity: low
- category: quality
- message: .pytest_cache/ 디렉토리가 git에 추적되고 있음 (untracked 상태). 이 디렉토리는 테스트 캐시로 버전 관리 대상이 아님.
- suggestion: .gitignore에 `**/.pytest_cache/` 추가.
- fixable: true

### F018 [MEDIUM]
- file: `_shared/tools/pdf_renderer.py`
- line: 245
- severity: medium
- category: quality
- message: _render_page_numbers()에서 auto_page_break를 False로 설정 후 True로 복원하는 패턴. 예외 발생 시 auto_page_break가 False 상태로 남을 수 있음.
- suggestion: try/finally 블록으로 auto_page_break 상태 복원 보장.
- fixable: true

## 원본 출력

## Code Review Summary

**Files Reviewed:** 10 (실질 코드 파일, .pytest_cache 제외)
**Total Issues:** 18

### By Severity
- CRITICAL: 0
- HIGH: 3
- MEDIUM: 8
- LOW: 7

---

### Issues

```
[FINDING]
file: _shared/tools/pdf_math_renderer.py
line: 43
severity: high
category: quality
message: 임시 파일 리소스 누수. latex_to_png()에서 NamedTemporaryFile(delete=False)로 생성한 파일을 호출자가 삭제해야 하지만, 함수 시그니처나 docstring에 이 책임이 명시되지 않음. pdf_renderer.py의 save()에서 정리하지만, 예외 발생 시 누수 가능.
suggestion: contextmanager 패턴 또는 반환 시 cleanup 콜백 제공. 최소한 docstring에 "호출자가 삭제 책임" 명시.
fixable: true
```

```
[FINDING]
file: _shared/tools/pdf_math_renderer.py
line: 53
severity: medium
category: quality
message: strip_latex_delimiters()에서 $...$와 $$...$$ 구분 로직이 동일한 조건문으로 작성되어 있음. 두 if 문 모두 `text.startswith("$") and text.endswith("$")` 조건이 동일하여 $$...$$ 케이스에 도달 불가.
suggestion: 첫 번째 조건을 `text.startswith("$$") and text.endswith("$$")`로 수정하고 슬라이싱을 `text[2:-2]`로 변경.
fixable: true
```

```
[FINDING]
file: _shared/tools/pdf_renderer.py
line: 183
severity: high
category: quality
message: _render_text_with_math()에서 `import re`를 함수 내부에서 반복 호출. 성능 문제는 미미하지만, 파일 상단에 import하는 것이 Python 컨벤션.
suggestion: 파일 상단으로 `import re` 이동.
fixable: true
```

```
[FINDING]
file: _shared/tools/pdf_renderer.py
line: 186
severity: medium
category: quality
message: _render_text_with_math()의 정규식 `(\$[^$]+\$)`가 $$...$$ (display math)를 올바르게 처리하지 못함. `$$x^2$$` 입력 시 빈 문자열 파트가 생기거나 잘못된 분할 발생 가능.
suggestion: display math와 inline math를 모두 처리하는 정규식 사용: `(\$\$[^$]+\$\$|\$[^$]+\$)`
fixable: true
```

```
[FINDING]
file: _shared/tools/pdf_renderer.py
line: 1
severity: medium
category: quality
message: pdf_renderer.py가 약 350줄로 적절하나, SchoolPdfRenderer 클래스가 StepPracticeMixin 포함 시 합산 800줄 이상. 클래스 책임이 헤더/문제/루브릭/정답지 등 과도하게 넓음.
suggestion: 렌더링 로직을 문서 타입별(worksheet, assessment, answer_key)로 분리 검토.
fixable: true
```

```
[FINDING]
file: _shared/tools/pdf_layout.py
line: 1
severity: medium
category: quality
message: StepPracticeMixin이 self.pdf, self.margins, self._set_font() 등 SchoolPdfRenderer의 구체적 속성에 의존하지만 타입 힌트나 Protocol 정의 없음. 믹스인 사용자가 어떤 인터페이스를 제공해야 하는지 불명확.
suggestion: typing.Protocol로 믹스인이 요구하는 인터페이스를 명시하거나, 최소한 docstring에 필수 메서드 목록 기재.
fixable: true
```

```
[FINDING]
file: _shared/tools/deploy.py
line: 87
severity: medium
category: quality
message: deploy_category()에서 파일 동일성 비교에 mtime + size만 사용. Google Drive 동기화 환경에서 mtime이 변경될 수 있어 의도치 않은 스킵 또는 불필요한 덮어쓰기 발생 가능.
suggestion: 해시 기반 비교 옵션 추가 또는 현재 방식의 한계를 docstring에 명시.
fixable: true
```

```
[FINDING]
file: _shared/tools/rename_output.py
line: 1
severity: medium
category: quality
message: 모든 리네이밍 매핑이 하드코딩된 딕셔너리로 관리됨. 새 파일 추가 시 코드 수정 필요. 현재 ai-math만 지원하며 확장성 부족.
suggestion: 네이밍 규칙을 JSON/YAML 설정 파일로 분리하거나, 패턴 기반 자동 변환 로직 도입 검토.
fixable: true
```

```
[FINDING]
file: _shared/tools/html_to_pdf.py
line: 56
severity: medium
category: quality
message: convert_html_to_pdf()에서 MathJax 렌더링 예외를 빈 except로 무시. MathJax가 있지만 렌더링 실패한 경우에도 불완전한 PDF가 생성됨.
suggestion: except 블록에서 최소한 경고 로그 출력 (예: `print(f"[경고] MathJax 렌더링 대기 실패: {html_path.name}", file=sys.stderr)`).
fixable: true
```

```
[FINDING]
file: _shared/templates/math_animation_lib.js
line: 24
severity: high
category: quality
message: 전역 변수 window.mathAnimators를 여러 곳에서 조건 초기화. 생성자(line 24)와 파일 말미(line 375)에서 중복 초기화하여 로딩 순서에 따라 기존 등록이 덮어쓰기될 수 있음.
suggestion: 파일 상단에서 한 번만 초기화: `window.mathAnimators = window.mathAnimators || {};` 후 생성자에서는 체크 없이 바로 등록.
fixable: true
```

```
[FINDING]
file: _shared/templates/math_animation_lib.js
line: 228
severity: low
category: quality
message: _resetToStep()에서 reset() 호출 후 모든 단계를 순차 재생. reset()이 이미 currentStep을 -1로 설정하는데, 바로 다음 줄에서 다시 -1로 설정하는 중복 코드.
suggestion: `this.currentStep = -1;` 중복 제거 (reset()이 이미 처리).
fixable: true
```

```
[FINDING]
file: _shared/templates/math_animation_lib.js
line: 229
severity: low
category: quality
message: _resetToStep()에서 모든 단계를 동기적으로 재생하지만 _playStep() 내부에서 setTimeout/gsap.delayedCall 사용. 이전 단계 애니메이션 완료 전에 다음 단계가 시작되어 시각적 글리치 발생 가능.
suggestion: 비동기 재생 체인 또는 즉시 상태 적용 모드(skipAnimation) 추가.
fixable: true
```

```
[FINDING]
file: _shared/templates/reveal_base.html
line: 23
severity: low
category: quality
message: MathJax 설정에서 `startup.typeset: false`로 초기 타이프셋을 비활성화하고 Reveal 이벤트에서 수동 호출하지만, MathJax 로딩 완료 전에 Reveal ready 이벤트가 발생하면 safeTypeset()이 빈 Promise를 반환하여 수식이 렌더링되지 않을 수 있음.
suggestion: safeTypeset()에서 mathJaxReady 플래그를 확인하고, 미준비 시 재시도 로직 추가.
fixable: true
```

```
[FINDING]
file: _shared/templates/reveal_base.html
line: 12
severity: low
category: quality
message: 템플릿 변수 {{THEME}}, {{ACCENT_COLOR}} 등이 미치환 시 CSS가 깨짐. 기본값(fallback)이 없음.
suggestion: CSS 변수에 기본값 설정: `--accent: var(--custom-accent, #f39c12);` 또는 템플릿 처리 시 유효성 검사.
fixable: true
```

```
[FINDING]
file: _shared/templates/worksheet_base.html
line: 100
severity: low
category: quality
message: MathJax 설정의 inlineMath 구분자 배열이 `[['$', '$'], ['\\(', '\\)']]` 형태인데, HTML 내에서 코드 리뷰 텍스트와 혼합되어 구분자가 잘못 파싱됨. 실제 파일에서도 `$` 구분자가 일반 텍스트의 달러 기호와 충돌 가능.
suggestion: 교육용 워크시트에서는 `\\(...\\)` 구분자만 사용하고 `$...$`는 제거 검토.
fixable: true
```

```
[FINDING]
file: _shared/templates/worksheet_base.html
line: 105
severity: low
category: quality
message: MathJax를 CDN(cdn.jsdelivr.net)에서 로드하지만, reveal_base.html은 오프라인 로컬 파일 사용. 인쇄용 학습지라면 오프라인 환경에서도 동작해야 할 수 있음.
suggestion: 오프라인 대응이 필요하면 reveal_base.html과 동일하게 로컬 MathJax 사용.
fixable: true
```

```
[FINDING]
file: _shared/tools/.pytest_cache/
line: -
severity: low
category: quality
message: .pytest_cache/ 디렉토리가 git에 추적되고 있음 (untracked 상태). 이 디렉토리는 테스트 캐시로 버전 관리 대상이 아님.
suggestion: .gitignore에 `**/.pytest_cache/` 추가.
fixable: true
```

```
[FINDING]
file: _shared/tools/pdf_renderer.py
line: 245
severity: medium
category: quality
message: _render_page_numbers()에서 auto_page_break를 False로 설정 후 True로 복원하는 패턴. 예외 발생 시 auto_page_break가 False 상태로 남을 수 있음.
suggestion: try/finally 블록으로 auto_page_break 상태 복원 보장.
fixable: true
```

---

### Recommendation

**COMMENT** — CRITICAL 이슈는 없으나, HIGH 3건(전역 상태 관리, import 위치, 리소스 누수)과 MEDIUM 8건이 있어 점진적 개선을 권장합니다.

**우선 수정 권장:**
1. `pdf_math_renderer.py`의 `strip_latex_delimiters()` 버그 (기능 오류)
2. `math_animation_lib.js`의 전역 초기화 중복
3. `.pytest_cache/` gitignore 추가
