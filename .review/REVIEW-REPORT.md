# lesson-maker 코드 리뷰 리포트

생성 시각: 2026-03-24T21:51:19.205Z

## 요약

총 이슈: **53개**

| 심각도 | 건수 |
|--------|------|
| critical | 1 |
| high | 8 |
| medium | 23 |
| low | 17 |
| info | 4 |

## 카테고리별

- quality: 36개
- security: 17개

## CRITICAL (1개)

### F003: ai-math/output/_archive/demo_ai_math_perceptron.html:3
- **카테고리**: quality
- **메시지**: MathJax.typesetPromise()를 직접 호출(line ~Reveal.on 이벤트). 프로젝트 규칙상 window.safeTypeset() 사용 필수. safeTypeset 미정의 시 MathJax 로딩 전 호출되면 에러 발생 가능.
- **제안**: `MathJax.typesetPromise()` → `if(window.safeTypeset) window.safeTypeset(); else if(typeof MathJax!=='undefined') MathJax.typesetPromise();`
- **수정 가능**: 예

## HIGH (8개)

### F001: _shared/tools/pdf_math_renderer.py:43
- **카테고리**: quality
- **메시지**: 임시 파일 리소스 누수. latex_to_png()에서 NamedTemporaryFile(delete=False)로 생성한 파일을 호출자가 삭제해야 하지만, 함수 시그니처나 docstring에 이 책임이 명시되지 않음. pdf_renderer.py의 save()에서 정리하지만, 예외 발생 시 누수 가능.
- **제안**: contextmanager 패턴 또는 반환 시 cleanup 콜백 제공. 최소한 docstring에 "호출자가 삭제 책임" 명시.
- **수정 가능**: 예

### F003: _shared/tools/pdf_renderer.py:183
- **카테고리**: quality
- **메시지**: _render_text_with_math()에서 `import re`를 함수 내부에서 반복 호출. 성능 문제는 미미하지만, 파일 상단에 import하는 것이 Python 컨벤션.
- **제안**: 파일 상단으로 `import re` 이동.
- **수정 가능**: 예

### F010: _shared/templates/math_animation_lib.js:24
- **카테고리**: quality
- **메시지**: 전역 변수 window.mathAnimators를 여러 곳에서 조건 초기화. 생성자(line 24)와 파일 말미(line 375)에서 중복 초기화하여 로딩 순서에 따라 기존 등록이 덮어쓰기될 수 있음.
- **제안**: 파일 상단에서 한 번만 초기화: `window.mathAnimators = window.mathAnimators || {};` 후 생성자에서는 체크 없이 바로 등록.
- **수정 가능**: 예

### F001: ai-math/output/_archive/ai_math_perceptron.html:1
- **카테고리**: quality
- **메시지**: 파일이 약 2000줄 이상으로 800줄 상한을 크게 초과함. CSS/JS/HTML이 단일 파일에 모두 포함되어 유지보수 불가능.
- **제안**: 아카이브 파일이므로 수정 불필요. 향후 교안 제작 시 reveal_base.html 템플릿 기반으로 분리 생성.
- **수정 가능**: 아니오

### F002: ai-math/output/_archive/ai_math_perceptron_v2.html:1
- **카테고리**: quality
- **메시지**: v1과 거의 동일한 CSS 코드(약 400줄)가 중복 복사됨. v1 대비 font-size를 CSS 변수로 개선했으나 파일 자체가 여전히 2000줄+ 초과.
- **제안**: 공통 CSS를 _shared/templates 또는 별도 CSS 파일로 추출. 아카이브이므로 현재 수정 불필요.
- **수정 가능**: 아니오

### F013: ai-math/output/_archive/ai_math_perceptron.html
- **카테고리**: quality
- **메시지**: 연도 표기 불일치 — sidebar에 "2025"로 표기되어 있으나 v2에서는 "2026"으로 수정됨. 아카이브 파일이지만 혼동 가능.
- **제안**: v1은 아카이브이므로 그대로 두되, 실제 사용 시 v2 기준으로 통일.
- **수정 가능**: 예

### F015: ai-math/output/_archive/matrix_lr_examples_slides.html
- **카테고리**: quality
- **메시지**: 파일이 약 1500줄+ 이상이며, 슬라이드 12개분의 HTML이 모두 하드코딩. 행렬 곱 예제마다 거의 동일한 구조(P행렬 → × → A행렬 → = → 결과)가 반복되어 DRY 원칙 위반.
- **제안**: 슬라이드 데이터를 JSON 배열로 정의하고, JS 템플릿 함수로 동적 생성.
- **수정 가능**: 예

### F001: _shared/tools/tex_renderer.py:339
- **카테고리**: security
- **메시지**: subprocess.run으로 xelatex 실행 시 입력 JSON 데이터가 LaTeX 소스에 삽입된다. tex_escape가 일반 텍스트 특수문자는 처리하지만, LaTeX 명령어 인젝션(\input, \write18 등)을 완전히 차단하지 못한다. 악의적 JSON 입력에 \input{/etc/passwd}나 \immediate\write18{cmd} 같은 페이로드가 포함되면 파일 읽기 또는 (shell-escape 활성 시) 임의 명령 실행이 가능하다.
- **제안**: (1) xelatex 실행 시 -no-shell-escape 플래그를 명시적으로 추가하여 \write18 계열 명령 실행을 차단. (2) tex_escape에서 백슬래시를 \textbackslash{}로 변환하고 있으나, $...$ 수식 구간 내부는 이스케이프하지 않으므로 수식 내 \input 등의 명령이 통과할 수 있음. 수식 구간에서도 위험 명령어(\input, \include, \write, \openout, \catcode)를 필터링하는 deny-list 검증 추가 필요.
- **수정 가능**: 예

## MEDIUM (23개)

### F002: _shared/tools/pdf_math_renderer.py:53
- **카테고리**: quality
- **메시지**: strip_latex_delimiters()에서 $...$와 $$...$$ 구분 로직이 동일한 조건문으로 작성되어 있음. 두 if 문 모두 `text.startswith("$") and text.endswith("$")` 조건이 동일하여 $$...$$ 케이스에 도달 불가.
- **제안**: 첫 번째 조건을 `text.startswith("$$") and text.endswith("$$")`로 수정하고 슬라이싱을 `text[2:-2]`로 변경.
- **수정 가능**: 예

### F004: _shared/tools/pdf_renderer.py:186
- **카테고리**: quality
- **메시지**: _render_text_with_math()의 정규식 `(\$[^$]+\$)`가 $$...$$ (display math)를 올바르게 처리하지 못함. `$$x^2$$` 입력 시 빈 문자열 파트가 생기거나 잘못된 분할 발생 가능.
- **제안**: display math와 inline math를 모두 처리하는 정규식 사용: `(\$\$[^$]+\$\$|\$[^$]+\$)`
- **수정 가능**: 예

### F005: _shared/tools/pdf_renderer.py:1
- **카테고리**: quality
- **메시지**: pdf_renderer.py가 약 350줄로 적절하나, SchoolPdfRenderer 클래스가 StepPracticeMixin 포함 시 합산 800줄 이상. 클래스 책임이 헤더/문제/루브릭/정답지 등 과도하게 넓음.
- **제안**: 렌더링 로직을 문서 타입별(worksheet, assessment, answer_key)로 분리 검토.
- **수정 가능**: 예

### F006: _shared/tools/pdf_layout.py:1
- **카테고리**: quality
- **메시지**: StepPracticeMixin이 self.pdf, self.margins, self._set_font() 등 SchoolPdfRenderer의 구체적 속성에 의존하지만 타입 힌트나 Protocol 정의 없음. 믹스인 사용자가 어떤 인터페이스를 제공해야 하는지 불명확.
- **제안**: typing.Protocol로 믹스인이 요구하는 인터페이스를 명시하거나, 최소한 docstring에 필수 메서드 목록 기재.
- **수정 가능**: 예

### F007: _shared/tools/deploy.py:87
- **카테고리**: quality
- **메시지**: deploy_category()에서 파일 동일성 비교에 mtime + size만 사용. Google Drive 동기화 환경에서 mtime이 변경될 수 있어 의도치 않은 스킵 또는 불필요한 덮어쓰기 발생 가능.
- **제안**: 해시 기반 비교 옵션 추가 또는 현재 방식의 한계를 docstring에 명시.
- **수정 가능**: 예

### F008: _shared/tools/rename_output.py:1
- **카테고리**: quality
- **메시지**: 모든 리네이밍 매핑이 하드코딩된 딕셔너리로 관리됨. 새 파일 추가 시 코드 수정 필요. 현재 ai-math만 지원하며 확장성 부족.
- **제안**: 네이밍 규칙을 JSON/YAML 설정 파일로 분리하거나, 패턴 기반 자동 변환 로직 도입 검토.
- **수정 가능**: 예

### F009: _shared/tools/html_to_pdf.py:56
- **카테고리**: quality
- **메시지**: convert_html_to_pdf()에서 MathJax 렌더링 예외를 빈 except로 무시. MathJax가 있지만 렌더링 실패한 경우에도 불완전한 PDF가 생성됨.
- **제안**: except 블록에서 최소한 경고 로그 출력 (예: `print(f"[경고] MathJax 렌더링 대기 실패: {html_path.name}", file=sys.stderr)`).
- **수정 가능**: 예

### F018: _shared/tools/pdf_renderer.py:245
- **카테고리**: quality
- **메시지**: _render_page_numbers()에서 auto_page_break를 False로 설정 후 True로 복원하는 패턴. 예외 발생 시 auto_page_break가 False 상태로 남을 수 있음.
- **제안**: try/finally 블록으로 auto_page_break 상태 복원 보장.
- **수정 가능**: 예

### F004: ai-math/output/_archive/demo_ai_math_perceptron.html:87
- **카테고리**: quality
- **메시지**: Reveal.js, MathJax, GSAP, Chart.js를 모두 외부 CDN에 의존. 오프라인 교실 환경에서 작동 불가. 주석에 "오프라인 시 libs/ 교체" 언급은 있으나 실제 fallback 없음.
- **제안**: 교실 프로젝터 사용 시 오프라인 가능성 높음. 로컬 libs/ 폴더 또는 인라인 번들 방식 적용 필요.
- **수정 가능**: 예

### F005: ai-math/output/_archive/demo_ai_math_perceptron.html:280
- **카테고리**: quality
- **메시지**: StepAnim.prev() 메서드가 구현 미완성. 인자를 받지만 사용하지 않고, reset() 후 재생 로직이 없어 "이전" 버튼이 실질적으로 동작하지 않음.
- **제안**: prev()에서 cur-1까지 스텝을 순차 재생하도록 구현하거나, 각 스텝의 역방향 애니메이션 추가.
- **수정 가능**: 예

### F006: ai-math/output/_archive/demo_ai_math_perceptron.html:230
- **카테고리**: quality
- **메시지**: innerHTML을 사용한 DOM 조작 (`document.getElementById('act-readout').innerHTML = ...`). 이 파일은 사용자 입력을 받지 않아 XSS 위험은 없으나, textContent 또는 DOM API 사용이 더 안전.
- **제안**: innerHTML 대신 textContent 또는 createElement 사용.
- **수정 가능**: 예

### F007: ai-math/output/_archive/ai_math_perceptron.html
- **카테고리**: quality
- **메시지**: JavaScript에서 DOM 직접 변이 패턴 다수 사용 (el.textContent = ..., el.style.color = ..., el.classList.add(...)). Immutability 원칙 위반이나, DOM 조작에서는 불가피한 측면 있음.
- **제안**: 아카이브 파일이므로 수정 불필요. 향후 교안에서는 상태 객체를 기반으로 렌더링하는 패턴 권장.
- **수정 가능**: 아니오

### F011: ai-math/output/_archive/ai_math_perceptron.html
- **카테고리**: quality
- **메시지**: heroCanvas에 대한 JavaScript 렌더링 코드가 파일 잘림으로 확인 불가하나, canvas 요소만 선언되고 실제 그리기 코드가 분리되어 있을 가능성. canvas가 빈 상태로 표시될 수 있음.
- **제안**: canvas 렌더링 코드가 존재하는지 확인 필요. 없으면 canvas 요소 제거 또는 placeholder 표시.
- **수정 가능**: 예

### F012: ai-math/output/_archive/demo_ai_math_perceptron.html
- **카테고리**: quality
- **메시지**: SVG 내 stroke-dasharray/dashoffset 애니메이션 설정이 있으나 (e-w1, e-w2 등), 실제 애니메이션을 트리거하는 JavaScript 코드가 없음. 엣지 라인이 보이지 않는 상태로 남음.
- **제안**: GSAP 또는 CSS 애니메이션으로 dashoffset을 0으로 전환하는 코드 추가, 또는 초기값을 dashoffset="0"으로 변경.
- **수정 가능**: 예

### F014: ai-math/output/_archive/ai_math_perceptron_v2.html
- **카테고리**: quality
- **메시지**: 함수 선언부가 파일 잘림으로 확인 불가하나, HTML에서 onclick="toggleTL(this)", onclick="revealTruth(...)" 등 인라인 이벤트 핸들러를 다수 사용. addEventListener 패턴 대비 유지보수성 떨어짐.
- **제안**: 인라인 onclick 대신 이벤트 위임(event delegation) 패턴 사용.
- **수정 가능**: 예

### F002: _shared/tools/tex_renderer.py:335
- **카테고리**: security
- **메시지**: xelatex 컴파일 실패 시 로그 파일 마지막 3000자를 에러 메시지에 포함하여 raise한다. 로그에는 서버 파일 경로, 시스템 정보, 임시 디렉토리 구조 등 민감 정보가 포함될 수 있으며, 이 에러가 상위 호출자를 통해 사용자에게 노출되면 정보 유출로 이어진다.
- **제안**: 에러 메시지에 로그 전체를 포함하지 말고, "LaTeX 컴파일 실패" 같은 일반 메시지만 반환. 상세 로그는 파일로 저장하거나 로깅 프레임워크로 기록.
- **수정 가능**: 예

### F003: _shared/tools/tex_renderer.py:119
- **카테고리**: security
- **메시지**: load_template에서 사용자가 --template 인자로 지정한 임의 경로의 JSON 파일을 읽는다. 경로 검증 없이 os.path.exists + open을 수행하므로, 경로 순회(path traversal)를 통해 시스템 내 임의 JSON 파일을 읽을 수 있다. CLI 도구 특성상 위험도는 제한적이나, 웹 서비스로 래핑될 경우 심각해진다.
- **제안**: 허용 디렉토리 기준으로 realpath를 검증하거나, 템플릿 경로를 특정 디렉토리 내로 제한.
- **수정 가능**: 예

### F001: ai-math/output/_archive/demo_ai_math_perceptron.html:8
- **카테고리**: security
- **메시지**: 외부 CDN(Reveal.js, MathJax, GSAP, Chart.js)을 integrity 속성 없이 로드합니다. CDN이 침해될 경우 악성 스크립트가 주입될 수 있습니다(Supply Chain Attack).
- **제안**: 각 CDN 리소스에 integrity="sha384-..." crossorigin="anonymous" 속성을 추가하거나, 라이브러리를 로컬에 번들링하세요. 예: <script src="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/reveal.js" integrity="sha384-xxxx" crossorigin="anonymous"></script>
- **수정 가능**: 예

### F002: ai-math/output/_archive/ai_math_perceptron.html:6
- **카테고리**: security
- **메시지**: Google Fonts CDN을 integrity 없이 로드합니다. ai_math_perceptron_v2.html, matrix_lr_examples_slides.html, matrix_transform_slides.html도 동일합니다. 네트워크 MITM 환경(학교 공용 Wi-Fi 등)에서 리소스 변조 가능성이 있습니다.
- **제안**: HTTPS가 이미 사용 중이므로 실질적 위험은 낮으나, 오프라인 사용 시 로컬 폰트 파일로 교체하면 가용성과 보안 모두 개선됩니다.
- **수정 가능**: 예

### F001: ai-math/output/slides/슬라이드_I-01_인공지능의역사.html:7
- **카테고리**: security
- **메시지**: CDN에서 Reveal.js를 로드할 때 Subresource Integrity(SRI) 해시가 없음. CDN이 침해되면 악성 스크립트가 주입될 수 있음.
- **제안**: <link> 및 <script> 태그에 integrity="sha384-..." crossorigin="anonymous" 속성 추가. 모든 슬라이드 파일에 동일하게 적용.
- **수정 가능**: 예

### F002: ai-math/output/slides/슬라이드_I-02_인공지능과수학.html:11
- **카테고리**: security
- **메시지**: MathJax CDN 로드 시 SRI 해시 없음. GSAP CDN(cdnjs.cloudflare.com)도 동일.
- **제안**: integrity 속성 추가. 예: <script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js" integrity="sha384-..." crossorigin="anonymous"></script>
- **수정 가능**: 예

### F003: ai-math/output/slides/슬라이드_II-1-01_텍스트자료의표현.html:12
- **카테고리**: security
- **메시지**: MathJax, Google Fonts 등 모든 외부 CDN 리소스에 SRI 해시 없음. 이 파일 포함 리뷰 대상 전체 15개 파일에 동일하게 해당.
- **제안**: 공통 베이스 템플릿(reveal_base.html)에서 SRI를 일괄 적용하는 것을 권장.
- **수정 가능**: 예

### F001: unknown
- **카테고리**: security
- **메시지**: - **Critical/High/ 0건**
- **수정 가능**: 아니오

## LOW (17개)

### F011: _shared/templates/math_animation_lib.js:228
- **카테고리**: quality
- **메시지**: _resetToStep()에서 reset() 호출 후 모든 단계를 순차 재생. reset()이 이미 currentStep을 -1로 설정하는데, 바로 다음 줄에서 다시 -1로 설정하는 중복 코드.
- **제안**: `this.currentStep = -1;` 중복 제거 (reset()이 이미 처리).
- **수정 가능**: 예

### F012: _shared/templates/math_animation_lib.js:229
- **카테고리**: quality
- **메시지**: _resetToStep()에서 모든 단계를 동기적으로 재생하지만 _playStep() 내부에서 setTimeout/gsap.delayedCall 사용. 이전 단계 애니메이션 완료 전에 다음 단계가 시작되어 시각적 글리치 발생 가능.
- **제안**: 비동기 재생 체인 또는 즉시 상태 적용 모드(skipAnimation) 추가.
- **수정 가능**: 예

### F013: _shared/templates/reveal_base.html:23
- **카테고리**: quality
- **메시지**: MathJax 설정에서 `startup.typeset: false`로 초기 타이프셋을 비활성화하고 Reveal 이벤트에서 수동 호출하지만, MathJax 로딩 완료 전에 Reveal ready 이벤트가 발생하면 safeTypeset()이 빈 Promise를 반환하여 수식이 렌더링되지 않을 수 있음.
- **제안**: safeTypeset()에서 mathJaxReady 플래그를 확인하고, 미준비 시 재시도 로직 추가.
- **수정 가능**: 예

### F014: _shared/templates/reveal_base.html:12
- **카테고리**: quality
- **메시지**: 템플릿 변수 {{THEME}}, {{ACCENT_COLOR}} 등이 미치환 시 CSS가 깨짐. 기본값(fallback)이 없음.
- **제안**: CSS 변수에 기본값 설정: `--accent: var(--custom-accent, #f39c12);` 또는 템플릿 처리 시 유효성 검사.
- **수정 가능**: 예

### F015: _shared/templates/worksheet_base.html:100
- **카테고리**: quality
- **메시지**: MathJax 설정의 inlineMath 구분자 배열이 `[['$', '$'], ['\\(', '\\)']]` 형태인데, HTML 내에서 코드 리뷰 텍스트와 혼합되어 구분자가 잘못 파싱됨. 실제 파일에서도 `$` 구분자가 일반 텍스트의 달러 기호와 충돌 가능.
- **제안**: 교육용 워크시트에서는 `\\(...\\)` 구분자만 사용하고 `$...$`는 제거 검토.
- **수정 가능**: 예

### F016: _shared/templates/worksheet_base.html:105
- **카테고리**: quality
- **메시지**: MathJax를 CDN(cdn.jsdelivr.net)에서 로드하지만, reveal_base.html은 오프라인 로컬 파일 사용. 인쇄용 학습지라면 오프라인 환경에서도 동작해야 할 수 있음.
- **제안**: 오프라인 대응이 필요하면 reveal_base.html과 동일하게 로컬 MathJax 사용.
- **수정 가능**: 예

### F017: _shared/tools/.pytest_cache/
- **카테고리**: quality
- **메시지**: .pytest_cache/ 디렉토리가 git에 추적되고 있음 (untracked 상태). 이 디렉토리는 테스트 캐시로 버전 관리 대상이 아님.
- **제안**: .gitignore에 `**/.pytest_cache/` 추가.
- **수정 가능**: 예

### F008: ai-math/output/_archive/ai_math_perceptron_v2.html
- **카테고리**: quality
- **메시지**: 인라인 스타일이 약 100곳 이상 사용됨 (style="font-size:...", style="color:var(--green)" 등). CSS 클래스로 추출 가능한 반복 패턴 다수.
- **제안**: 반복되는 인라인 스타일을 CSS 유틸리티 클래스로 추출 (.text-green, .text-sm 등).
- **수정 가능**: 예

### F009: ai-math/output/_archive/matrix_transform_slides.html
- **카테고리**: quality
- **메시지**: 슬라이드 내 이미지/행렬 시각화가 모두 하드코딩된 HTML. 슬라이드 7개에 대해 유사한 pixel-grid/matrix-wrap 구조가 반복됨. 데이터 기반 렌더링으로 전환 시 코드량 70% 감소 가능.
- **제안**: 행렬 데이터를 JS 배열로 정의하고 템플릿 함수로 DOM 생성.
- **수정 가능**: 예

### F010: ai-math/output/_archive/matrix_lr_examples_slides.html
- **카테고리**: quality
- **메시지**: matrix_transform_slides.html과 동일한 CSS 코드가 약 200줄 중복 복사됨. 두 파일이 같은 디자인 시스템을 공유하지만 독립 파일로 유지됨.
- **제안**: 공통 CSS를 별도 파일로 추출하거나, 하나의 슬라이드 덱으로 통합.
- **수정 가능**: 예

### F016: 전체 (6개 파일)
- **카테고리**: quality
- **메시지**: 전체 6개 파일 중 어떤 파일도 에러 핸들링이 없음. document.getElementById() 결과가 null일 때의 방어 코드 부재. 특히 demo 파일의 StepAnim에서 el이 null이면 gsap.to(null, ...)이 호출됨.
- **제안**: null 체크 추가: `const el = document.getElementById(id); if (!el) return;`
- **수정 가능**: 예

### F004: _shared/tools/tests/test_pdf_renderer.py:10
- **카테고리**: security
- **메시지**: sys.path.insert(0, ...)로 상위 디렉토리를 모듈 검색 경로에 추가한다. 테스트 코드이므로 실질적 위험은 낮으나, 해당 경로에 악성 모듈이 존재하면 의도치 않은 코드가 임포트될 수 있다(dependency confusion 유사 패턴).
- **제안**: 테스트 실행 시 conftest.py나 pyproject.toml의 [tool.pytest.ini_options] pythonpath 설정으로 관리하는 것이 더 안전.
- **수정 가능**: 예

### F005: _shared/tools/tex_renderer.py:328
- **카테고리**: security
- **메시지**: compile_tex에서 subprocess.run 호출 시 cmd가 리스트 형태라 shell injection은 불가하나, capture_output=True로 stdout/stderr를 메모리에 저장한다. 극단적으로 큰 LaTeX 로그가 생성되면 메모리 소모 가능성이 있다(DoS 벡터).
- **제안**: subprocess.run에 timeout 파라미터를 추가하여 무한 컴파일 방지 (예: timeout=120).
- **수정 가능**: 예

### F003: ai-math/output/_archive/ai_math_perceptron.html
- **카테고리**: security
- **메시지**: showAns(), updateNeuron(), updateAND() 등의 함수에서 innerHTML을 사용하여 DOM을 업데이트합니다. 현재 모든 입력이 하드코딩된 문자열이므로 XSS 위험은 없으나, 향후 사용자 입력을 받는 기능이 추가될 경우 위험해질 수 있습니다.
- **제안**: innerHTML 대신 textContent 또는 DOM API를 사용하는 것이 방어적 코딩 관행입니다. 단, 현재 코드에서는 실질적 XSS 벡터가 없으므로 우선순위는 낮습니다.
- **수정 가능**: 예

### F004: ai-math/output/_archive/demo_ai_math_perceptron.html
- **카테고리**: security
- **메시지**: Reveal.js slidechanged 이벤트에서 MathJax.typesetPromise()를 typeof 체크 후 직접 호출합니다. 프로젝트 규칙(CLAUDE.md)에 따르면 window.safeTypeset()을 사용해야 합니다. safeTypeset이 없는 이 파일은 아카이브 파일이므로 실질적 보안 위험보다는 규칙 위반입니다.
- **제안**: 아카이브 파일이므로 수정 불필요. 신규 파일에서는 window.safeTypeset() 사용을 유지하세요.
- **수정 가능**: 예

### F004: ai-math/output/slides/슬라이드_II-1-02_텍스트자료의처리.html:14
- **카테고리**: security
- **메시지**: MathJax 설정에서 startup.ready()를 오버라이드하여 defaultReady()를 호출하는 패턴이 있음. 현재는 안전하지만, 이 패턴은 MathJax 초기화 흐름에 커스텀 코드를 삽입할 수 있는 진입점이 됨.
- **제안**: 커스텀 로직이 없다면 startup 오버라이드 제거. 기본 초기화만 사용.
- **수정 가능**: 예

### F005: ai-math/output/slides/슬라이드_I-02_인공지능과수학.html
- **카테고리**: security
- **메시지**: 키보드 이벤트 리스너에서 'f' 키 입력 시 requestFullscreen()을 호출. 프레젠테이션 파일 용도로는 안전하나, 이 파일이 웹에 호스팅될 경우 사용자가 예상하지 못한 전체화면 전환이 발생할 수 있음(minor UX security).
- **제안**: 교실 로컬 사용 전용이면 무시 가능. 웹 호스팅 시에는 명시적 버튼 UI로 대체 권장.
- **수정 가능**: 예

## INFO (4개)

### F017: 전체 (6개 파일)
- **카테고리**: quality
- **메시지**: 모든 파일이 _archive/ 폴더에 위치하며 현재 활발하게 사용되지 않는 레거시 코드. 새 교안은 reveal_base.html 템플릿 + 에이전트 파이프라인으로 생성됨.
- **제안**: 아카이브 파일의 유용한 시각화/인터랙티브 컴포넌트를 _shared/templates/에 재사용 가능한 형태로 추출하는 것을 고려.
- **수정 가능**: 아니오

### F018: 전체 (6개 파일)
- **카테고리**: quality
- **메시지**: 접근성(a11y) 미흡 — ARIA 레이블 없음, 키보드 네비게이션 불완전, 색상 대비 미검증, SVG에 title/desc 없음. 교육용 자료로서 다양한 학습자 접근성 고려 필요.
- **제안**: 향후 교안 템플릿에 기본 ARIA 속성 포함.
- **수정 가능**: 예

### F005: (전체 대상 파일)
- **카테고리**: security
- **메시지**: 모든 파일이 정적 HTML로, 서버 사이드 코드·인증·DB 접근·사용자 데이터 저장이 없습니다. OWASP Top 10 중 Injection, Broken Auth, Sensitive Data Exposure, Access Control, SSRF 등은 해당 사항이 없습니다. 하드코딩된 시크릿도 발견되지 않았습니다.
- **제안**: 없음
- **수정 가능**: 아니오

### F001: ai-math-2022/output/slides/슬라이드_1-1_인공지능의의미.html (및 슬라이드 1-2, 1-3 동일)
- **카테고리**: security
- **메시지**: 외부 라이브러리(Reveal.js, MathJax, Chart.js, GSAP, p5.js)를 로컬 상대경로(../../libs/)로 로드하고 있으며 Subresource Integrity(SRI) 해시가 없습니다. 현재 로컬 전용이므로 실질적 위험은 없으나, 웹 서버 배포 시 공급망 변조 위험이 존재합니다.
- **제안**: 웹 서버 배포 시 CDN + SRI 해시 적용 또는 로컬 파일 무결성 검증 절차 추가 검토
- **수정 가능**: 예
