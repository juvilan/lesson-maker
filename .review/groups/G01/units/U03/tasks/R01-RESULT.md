# R01 리뷰 결과

카테고리: quality
발견된 이슈: 18개
완료 시각: 2026-03-24T08:38:05.418Z

## 발견된 이슈

### F001 [HIGH]
- file: `ai-math/output/_archive/ai_math_perceptron.html`
- line: 1
- severity: high
- category: quality
- message: 파일이 약 2000줄 이상으로 800줄 상한을 크게 초과함. CSS/JS/HTML이 단일 파일에 모두 포함되어 유지보수 불가능.
- suggestion: 아카이브 파일이므로 수정 불필요. 향후 교안 제작 시 reveal_base.html 템플릿 기반으로 분리 생성.
- fixable: false

### F002 [HIGH]
- file: `ai-math/output/_archive/ai_math_perceptron_v2.html`
- line: 1
- severity: high
- category: quality
- message: v1과 거의 동일한 CSS 코드(약 400줄)가 중복 복사됨. v1 대비 font-size를 CSS 변수로 개선했으나 파일 자체가 여전히 2000줄+ 초과.
- suggestion: 공통 CSS를 _shared/templates 또는 별도 CSS 파일로 추출. 아카이브이므로 현재 수정 불필요.
- fixable: false

### F003 [CRITICAL]
- file: `ai-math/output/_archive/demo_ai_math_perceptron.html`
- line: 3
- severity: critical
- category: quality
- message: MathJax.typesetPromise()를 직접 호출(line ~Reveal.on 이벤트). 프로젝트 규칙상 window.safeTypeset() 사용 필수. safeTypeset 미정의 시 MathJax 로딩 전 호출되면 에러 발생 가능.
- suggestion: `MathJax.typesetPromise()` → `if(window.safeTypeset) window.safeTypeset(); else if(typeof MathJax!=='undefined') MathJax.typesetPromise();`
- fixable: true

### F004 [MEDIUM]
- file: `ai-math/output/_archive/demo_ai_math_perceptron.html`
- line: 87
- severity: medium
- category: quality
- message: Reveal.js, MathJax, GSAP, Chart.js를 모두 외부 CDN에 의존. 오프라인 교실 환경에서 작동 불가. 주석에 "오프라인 시 libs/ 교체" 언급은 있으나 실제 fallback 없음.
- suggestion: 교실 프로젝터 사용 시 오프라인 가능성 높음. 로컬 libs/ 폴더 또는 인라인 번들 방식 적용 필요.
- fixable: true

### F005 [MEDIUM]
- file: `ai-math/output/_archive/demo_ai_math_perceptron.html`
- line: 280
- severity: medium
- category: quality
- message: StepAnim.prev() 메서드가 구현 미완성. 인자를 받지만 사용하지 않고, reset() 후 재생 로직이 없어 "이전" 버튼이 실질적으로 동작하지 않음.
- suggestion: prev()에서 cur-1까지 스텝을 순차 재생하도록 구현하거나, 각 스텝의 역방향 애니메이션 추가.
- fixable: true

### F006 [MEDIUM]
- file: `ai-math/output/_archive/demo_ai_math_perceptron.html`
- line: 230
- severity: medium
- category: quality
- message: innerHTML을 사용한 DOM 조작 (`document.getElementById('act-readout').innerHTML = ...`). 이 파일은 사용자 입력을 받지 않아 XSS 위험은 없으나, textContent 또는 DOM API 사용이 더 안전.
- suggestion: innerHTML 대신 textContent 또는 createElement 사용.
- fixable: true

### F007 [MEDIUM]
- file: `ai-math/output/_archive/ai_math_perceptron.html`
- severity: medium
- category: quality
- message: JavaScript에서 DOM 직접 변이 패턴 다수 사용 (el.textContent = ..., el.style.color = ..., el.classList.add(...)). Immutability 원칙 위반이나, DOM 조작에서는 불가피한 측면 있음.
- suggestion: 아카이브 파일이므로 수정 불필요. 향후 교안에서는 상태 객체를 기반으로 렌더링하는 패턴 권장.
- fixable: false

### F008 [LOW]
- file: `ai-math/output/_archive/ai_math_perceptron_v2.html`
- severity: low
- category: quality
- message: 인라인 스타일이 약 100곳 이상 사용됨 (style="font-size:...", style="color:var(--green)" 등). CSS 클래스로 추출 가능한 반복 패턴 다수.
- suggestion: 반복되는 인라인 스타일을 CSS 유틸리티 클래스로 추출 (.text-green, .text-sm 등).
- fixable: true

### F009 [LOW]
- file: `ai-math/output/_archive/matrix_transform_slides.html`
- severity: low
- category: quality
- message: 슬라이드 내 이미지/행렬 시각화가 모두 하드코딩된 HTML. 슬라이드 7개에 대해 유사한 pixel-grid/matrix-wrap 구조가 반복됨. 데이터 기반 렌더링으로 전환 시 코드량 70% 감소 가능.
- suggestion: 행렬 데이터를 JS 배열로 정의하고 템플릿 함수로 DOM 생성.
- fixable: true

### F010 [LOW]
- file: `ai-math/output/_archive/matrix_lr_examples_slides.html`
- severity: low
- category: quality
- message: matrix_transform_slides.html과 동일한 CSS 코드가 약 200줄 중복 복사됨. 두 파일이 같은 디자인 시스템을 공유하지만 독립 파일로 유지됨.
- suggestion: 공통 CSS를 별도 파일로 추출하거나, 하나의 슬라이드 덱으로 통합.
- fixable: true

### F011 [MEDIUM]
- file: `ai-math/output/_archive/ai_math_perceptron.html`
- severity: medium
- category: quality
- message: heroCanvas에 대한 JavaScript 렌더링 코드가 파일 잘림으로 확인 불가하나, canvas 요소만 선언되고 실제 그리기 코드가 분리되어 있을 가능성. canvas가 빈 상태로 표시될 수 있음.
- suggestion: canvas 렌더링 코드가 존재하는지 확인 필요. 없으면 canvas 요소 제거 또는 placeholder 표시.
- fixable: true

### F012 [MEDIUM]
- file: `ai-math/output/_archive/demo_ai_math_perceptron.html`
- severity: medium
- category: quality
- message: SVG 내 stroke-dasharray/dashoffset 애니메이션 설정이 있으나 (e-w1, e-w2 등), 실제 애니메이션을 트리거하는 JavaScript 코드가 없음. 엣지 라인이 보이지 않는 상태로 남음.
- suggestion: GSAP 또는 CSS 애니메이션으로 dashoffset을 0으로 전환하는 코드 추가, 또는 초기값을 dashoffset="0"으로 변경.
- fixable: true

### F013 [HIGH]
- file: `ai-math/output/_archive/ai_math_perceptron.html`
- severity: high
- category: quality
- message: 연도 표기 불일치 — sidebar에 "2025"로 표기되어 있으나 v2에서는 "2026"으로 수정됨. 아카이브 파일이지만 혼동 가능.
- suggestion: v1은 아카이브이므로 그대로 두되, 실제 사용 시 v2 기준으로 통일.
- fixable: true

### F014 [MEDIUM]
- file: `ai-math/output/_archive/ai_math_perceptron_v2.html`
- severity: medium
- category: quality
- message: 함수 선언부가 파일 잘림으로 확인 불가하나, HTML에서 onclick="toggleTL(this)", onclick="revealTruth(...)" 등 인라인 이벤트 핸들러를 다수 사용. addEventListener 패턴 대비 유지보수성 떨어짐.
- suggestion: 인라인 onclick 대신 이벤트 위임(event delegation) 패턴 사용.
- fixable: true

### F015 [HIGH]
- file: `ai-math/output/_archive/matrix_lr_examples_slides.html`
- severity: high
- category: quality
- message: 파일이 약 1500줄+ 이상이며, 슬라이드 12개분의 HTML이 모두 하드코딩. 행렬 곱 예제마다 거의 동일한 구조(P행렬 → × → A행렬 → = → 결과)가 반복되어 DRY 원칙 위반.
- suggestion: 슬라이드 데이터를 JSON 배열로 정의하고, JS 템플릿 함수로 동적 생성.
- fixable: true

### F016 [LOW]
- file: `전체 (6개 파일)`
- severity: low
- category: quality
- message: 전체 6개 파일 중 어떤 파일도 에러 핸들링이 없음. document.getElementById() 결과가 null일 때의 방어 코드 부재. 특히 demo 파일의 StepAnim에서 el이 null이면 gsap.to(null, ...)이 호출됨.
- suggestion: null 체크 추가: `const el = document.getElementById(id); if (!el) return;`
- fixable: true

### F017 [INFO]
- file: `전체 (6개 파일)`
- severity: info
- category: quality
- message: 모든 파일이 _archive/ 폴더에 위치하며 현재 활발하게 사용되지 않는 레거시 코드. 새 교안은 reveal_base.html 템플릿 + 에이전트 파이프라인으로 생성됨.
- suggestion: 아카이브 파일의 유용한 시각화/인터랙티브 컴포넌트를 _shared/templates/에 재사용 가능한 형태로 추출하는 것을 고려.
- fixable: false

### F018 [INFO]
- file: `전체 (6개 파일)`
- severity: info
- category: quality
- message: 접근성(a11y) 미흡 — ARIA 레이블 없음, 키보드 네비게이션 불완전, 색상 대비 미검증, SVG에 title/desc 없음. 교육용 자료로서 다양한 학습자 접근성 고려 필요.
- suggestion: 향후 교안 템플릿에 기본 ARIA 속성 포함.
- fixable: true

## 원본 출력

아카이브 파일들의 quality 리뷰 결과를 보고합니다. 이 파일들은 `_archive/`에 위치한 레거시 교안이므로 심각도를 한 단계 낮추어 평가합니다.

---

## Code Review Summary

**Files Reviewed:** 6 (제공된 파일 기준, 나머지는 잘림/미포함)
**Total Issues:** 18

### By Severity
- CRITICAL: 1 (must fix)
- HIGH: 4 (should fix)
- MEDIUM: 7 (consider fixing)
- LOW: 4 (optional)
- INFO: 2

---

### Issues

```
[FINDING]
file: ai-math/output/_archive/ai_math_perceptron.html
line: 1
severity: high
category: quality
message: 파일이 약 2000줄 이상으로 800줄 상한을 크게 초과함. CSS/JS/HTML이 단일 파일에 모두 포함되어 유지보수 불가능.
suggestion: 아카이브 파일이므로 수정 불필요. 향후 교안 제작 시 reveal_base.html 템플릿 기반으로 분리 생성.
fixable: false
```

```
[FINDING]
file: ai-math/output/_archive/ai_math_perceptron_v2.html
line: 1
severity: high
category: quality
message: v1과 거의 동일한 CSS 코드(약 400줄)가 중복 복사됨. v1 대비 font-size를 CSS 변수로 개선했으나 파일 자체가 여전히 2000줄+ 초과.
suggestion: 공통 CSS를 _shared/templates 또는 별도 CSS 파일로 추출. 아카이브이므로 현재 수정 불필요.
fixable: false
```

```
[FINDING]
file: ai-math/output/_archive/demo_ai_math_perceptron.html
line: 3
severity: critical
category: quality
message: MathJax.typesetPromise()를 직접 호출(line ~Reveal.on 이벤트). 프로젝트 규칙상 window.safeTypeset() 사용 필수. safeTypeset 미정의 시 MathJax 로딩 전 호출되면 에러 발생 가능.
suggestion: `MathJax.typesetPromise()` → `if(window.safeTypeset) window.safeTypeset(); else if(typeof MathJax!=='undefined') MathJax.typesetPromise();`
fixable: true
```

```
[FINDING]
file: ai-math/output/_archive/demo_ai_math_perceptron.html
line: 87
severity: medium
category: quality
message: Reveal.js, MathJax, GSAP, Chart.js를 모두 외부 CDN에 의존. 오프라인 교실 환경에서 작동 불가. 주석에 "오프라인 시 libs/ 교체" 언급은 있으나 실제 fallback 없음.
suggestion: 교실 프로젝터 사용 시 오프라인 가능성 높음. 로컬 libs/ 폴더 또는 인라인 번들 방식 적용 필요.
fixable: true
```

```
[FINDING]
file: ai-math/output/_archive/demo_ai_math_perceptron.html
line: 280
severity: medium
category: quality
message: StepAnim.prev() 메서드가 구현 미완성. 인자를 받지만 사용하지 않고, reset() 후 재생 로직이 없어 "이전" 버튼이 실질적으로 동작하지 않음.
suggestion: prev()에서 cur-1까지 스텝을 순차 재생하도록 구현하거나, 각 스텝의 역방향 애니메이션 추가.
fixable: true
```

```
[FINDING]
file: ai-math/output/_archive/demo_ai_math_perceptron.html
line: 230
severity: medium
category: quality
message: innerHTML을 사용한 DOM 조작 (`document.getElementById('act-readout').innerHTML = ...`). 이 파일은 사용자 입력을 받지 않아 XSS 위험은 없으나, textContent 또는 DOM API 사용이 더 안전.
suggestion: innerHTML 대신 textContent 또는 createElement 사용.
fixable: true
```

```
[FINDING]
file: ai-math/output/_archive/ai_math_perceptron.html
line: 다수
severity: medium
category: quality
message: JavaScript에서 DOM 직접 변이 패턴 다수 사용 (el.textContent = ..., el.style.color = ..., el.classList.add(...)). Immutability 원칙 위반이나, DOM 조작에서는 불가피한 측면 있음.
suggestion: 아카이브 파일이므로 수정 불필요. 향후 교안에서는 상태 객체를 기반으로 렌더링하는 패턴 권장.
fixable: false
```

```
[FINDING]
file: ai-math/output/_archive/ai_math_perceptron_v2.html
line: 다수 (example-box, callout 등)
severity: low
category: quality
message: 인라인 스타일이 약 100곳 이상 사용됨 (style="font-size:...", style="color:var(--green)" 등). CSS 클래스로 추출 가능한 반복 패턴 다수.
suggestion: 반복되는 인라인 스타일을 CSS 유틸리티 클래스로 추출 (.text-green, .text-sm 등).
fixable: true
```

```
[FINDING]
file: ai-math/output/_archive/matrix_transform_slides.html
line: 전체
severity: low
category: quality
message: 슬라이드 내 이미지/행렬 시각화가 모두 하드코딩된 HTML. 슬라이드 7개에 대해 유사한 pixel-grid/matrix-wrap 구조가 반복됨. 데이터 기반 렌더링으로 전환 시 코드량 70% 감소 가능.
suggestion: 행렬 데이터를 JS 배열로 정의하고 템플릿 함수로 DOM 생성.
fixable: true
```

```
[FINDING]
file: ai-math/output/_archive/matrix_lr_examples_slides.html
line: 전체
severity: low
category: quality
message: matrix_transform_slides.html과 동일한 CSS 코드가 약 200줄 중복 복사됨. 두 파일이 같은 디자인 시스템을 공유하지만 독립 파일로 유지됨.
suggestion: 공통 CSS를 별도 파일로 추출하거나, 하나의 슬라이드 덱으로 통합.
fixable: true
```

```
[FINDING]
file: ai-math/output/_archive/ai_math_perceptron.html
line: 히어로 캔버스 JS 영역
severity: medium
category: quality
message: heroCanvas에 대한 JavaScript 렌더링 코드가 파일 잘림으로 확인 불가하나, canvas 요소만 선언되고 실제 그리기 코드가 분리되어 있을 가능성. canvas가 빈 상태로 표시될 수 있음.
suggestion: canvas 렌더링 코드가 존재하는지 확인 필요. 없으면 canvas 요소 제거 또는 placeholder 표시.
fixable: true
```

```
[FINDING]
file: ai-math/output/_archive/demo_ai_math_perceptron.html
line: SVG 영역 (perceptron-svg)
severity: medium
category: quality
message: SVG 내 stroke-dasharray/dashoffset 애니메이션 설정이 있으나 (e-w1, e-w2 등), 실제 애니메이션을 트리거하는 JavaScript 코드가 없음. 엣지 라인이 보이지 않는 상태로 남음.
suggestion: GSAP 또는 CSS 애니메이션으로 dashoffset을 0으로 전환하는 코드 추가, 또는 초기값을 dashoffset="0"으로 변경.
fixable: true
```

```
[FINDING]
file: ai-math/output/_archive/ai_math_perceptron.html
line: sidebar 영역
severity: high
category: quality
message: 연도 표기 불일치 — sidebar에 "2025"로 표기되어 있으나 v2에서는 "2026"으로 수정됨. 아카이브 파일이지만 혼동 가능.
suggestion: v1은 아카이브이므로 그대로 두되, 실제 사용 시 v2 기준으로 통일.
fixable: true
```

```
[FINDING]
file: ai-math/output/_archive/ai_math_perceptron_v2.html
line: 전체 JS
severity: medium
category: quality
message: 함수 선언부가 파일 잘림으로 확인 불가하나, HTML에서 onclick="toggleTL(this)", onclick="revealTruth(...)" 등 인라인 이벤트 핸들러를 다수 사용. addEventListener 패턴 대비 유지보수성 떨어짐.
suggestion: 인라인 onclick 대신 이벤트 위임(event delegation) 패턴 사용.
fixable: true
```

```
[FINDING]
file: ai-math/output/_archive/matrix_lr_examples_slides.html
line: 전체
severity: high
category: quality
message: 파일이 약 1500줄+ 이상이며, 슬라이드 12개분의 HTML이 모두 하드코딩. 행렬 곱 예제마다 거의 동일한 구조(P행렬 → × → A행렬 → = → 결과)가 반복되어 DRY 원칙 위반.
suggestion: 슬라이드 데이터를 JSON 배열로 정의하고, JS 템플릿 함수로 동적 생성.
fixable: true
```

```
[FINDING]
file: 전체 (6개 파일)
line: N/A
severity: low
category: quality
message: 전체 6개 파일 중 어떤 파일도 에러 핸들링이 없음. document.getElementById() 결과가 null일 때의 방어 코드 부재. 특히 demo 파일의 StepAnim에서 el이 null이면 gsap.to(null, ...)이 호출됨.
suggestion: null 체크 추가: `const el = document.getElementById(id); if (!el) return;`
fixable: true
```

```
[FINDING]
file: 전체 (6개 파일)
line: N/A
severity: info
category: quality
message: 모든 파일이 _archive/ 폴더에 위치하며 현재 활발하게 사용되지 않는 레거시 코드. 새 교안은 reveal_base.html 템플릿 + 에이전트 파이프라인으로 생성됨.
suggestion: 아카이브 파일의 유용한 시각화/인터랙티브 컴포넌트를 _shared/templates/에 재사용 가능한 형태로 추출하는 것을 고려.
fixable: false
```

```
[FINDING]
file: 전체 (6개 파일)
line: N/A
severity: info
category: quality
message: 접근성(a11y) 미흡 — ARIA 레이블 없음, 키보드 네비게이션 불완전, 색상 대비 미검증, SVG에 title/desc 없음. 교육용 자료로서 다양한 학습자 접근성 고려 필요.
suggestion: 향후 교안 템플릿에 기본 ARIA 속성 포함.
fixable: true
```

---

### Recommendation

**COMMENT** — 아카이브 파일이므로 즉시 수정 불필요하나, 다음 사항을 향후 교안 제작에 반영할 것을 권장:

1. **CRITICAL**: `safeTypeset()` 규칙 준수 (demo 파일)
2. **HIGH**: 파일 크기 제한 (800줄) 준수 — 새 교안은 reveal_base.html 기반으로 이미 해결됨
3. **MEDIUM**: CDN 의존성 → 오프라인 환경 대비 로컬 번들링 고려
4. **재사용**: matrix_transform/matrix_lr_examples의 행렬 시각화 컴포넌트를 `_shared/templates/`로 추출하면 향후 기하/선형대수 교안에서 활용 가능
