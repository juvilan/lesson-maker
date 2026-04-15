# R01 리뷰 결과

카테고리: security
발견된 이슈: 5개
완료 시각: 2026-03-24T21:43:10.573Z

## 발견된 이슈

### F001 [MEDIUM]
- file: `ai-math/output/_archive/demo_ai_math_perceptron.html`
- line: 8
- severity: medium
- category: security
- message: 외부 CDN(Reveal.js, MathJax, GSAP, Chart.js)을 integrity 속성 없이 로드합니다. CDN이 침해될 경우 악성 스크립트가 주입될 수 있습니다(Supply Chain Attack).
- suggestion: 각 CDN 리소스에 integrity="sha384-..." crossorigin="anonymous" 속성을 추가하거나, 라이브러리를 로컬에 번들링하세요. 예: <script src="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/reveal.js" integrity="sha384-xxxx" crossorigin="anonymous"></script>
- fixable: true

### F002 [MEDIUM]
- file: `ai-math/output/_archive/ai_math_perceptron.html`
- line: 6
- severity: medium
- category: security
- message: Google Fonts CDN을 integrity 없이 로드합니다. ai_math_perceptron_v2.html, matrix_lr_examples_slides.html, matrix_transform_slides.html도 동일합니다. 네트워크 MITM 환경(학교 공용 Wi-Fi 등)에서 리소스 변조 가능성이 있습니다.
- suggestion: HTTPS가 이미 사용 중이므로 실질적 위험은 낮으나, 오프라인 사용 시 로컬 폰트 파일로 교체하면 가용성과 보안 모두 개선됩니다.
- fixable: true

### F003 [LOW]
- file: `ai-math/output/_archive/ai_math_perceptron.html`
- severity: low
- category: security
- message: showAns(), updateNeuron(), updateAND() 등의 함수에서 innerHTML을 사용하여 DOM을 업데이트합니다. 현재 모든 입력이 하드코딩된 문자열이므로 XSS 위험은 없으나, 향후 사용자 입력을 받는 기능이 추가될 경우 위험해질 수 있습니다.
- suggestion: innerHTML 대신 textContent 또는 DOM API를 사용하는 것이 방어적 코딩 관행입니다. 단, 현재 코드에서는 실질적 XSS 벡터가 없으므로 우선순위는 낮습니다.
- fixable: true

### F004 [LOW]
- file: `ai-math/output/_archive/demo_ai_math_perceptron.html`
- severity: low
- category: security
- message: Reveal.js slidechanged 이벤트에서 MathJax.typesetPromise()를 typeof 체크 후 직접 호출합니다. 프로젝트 규칙(CLAUDE.md)에 따르면 window.safeTypeset()을 사용해야 합니다. safeTypeset이 없는 이 파일은 아카이브 파일이므로 실질적 보안 위험보다는 규칙 위반입니다.
- suggestion: 아카이브 파일이므로 수정 불필요. 신규 파일에서는 window.safeTypeset() 사용을 유지하세요.
- fixable: true

### F005 [INFO]
- file: `(전체 대상 파일)`
- severity: info
- category: security
- message: 모든 파일이 정적 HTML로, 서버 사이드 코드·인증·DB 접근·사용자 데이터 저장이 없습니다. OWASP Top 10 중 Injection, Broken Auth, Sensitive Data Exposure, Access Control, SSRF 등은 해당 사항이 없습니다. 하드코딩된 시크릿도 발견되지 않았습니다.
- suggestion: 없음
- fixable: false

## 원본 출력

Plan mode이므로 코드를 직접 수정하지 않고 보안 리뷰만 수행합니다.

이 파일들은 모두 **로컬 브라우저에서 실행되는 정적 교육용 HTML 슬라이드**입니다. 서버 사이드 코드, 인증, DB 접근, 사용자 입력 저장 등이 없으므로 공격 표면이 매우 제한적입니다.

---

# Security Review Report

**Scope:** ai-math/output/_archive/ 내 HTML 교안 파일 7개 + exam/slides 8개
**Risk Level:** LOW

## Summary
- Critical Issues: 0
- High Issues: 0
- Medium Issues: 2
- Low Issues: 2
- Info Issues: 1

---

```
[FINDING]
file: ai-math/output/_archive/demo_ai_math_perceptron.html
line: 8-9
severity: medium
category: security
message: 외부 CDN(Reveal.js, MathJax, GSAP, Chart.js)을 integrity 속성 없이 로드합니다. CDN이 침해될 경우 악성 스크립트가 주입될 수 있습니다(Supply Chain Attack).
suggestion: 각 CDN 리소스에 integrity="sha384-..." crossorigin="anonymous" 속성을 추가하거나, 라이브러리를 로컬에 번들링하세요. 예: <script src="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/reveal.js" integrity="sha384-xxxx" crossorigin="anonymous"></script>
fixable: true
```

```
[FINDING]
file: ai-math/output/_archive/ai_math_perceptron.html
line: 6
severity: medium
category: security
message: Google Fonts CDN을 integrity 없이 로드합니다. ai_math_perceptron_v2.html, matrix_lr_examples_slides.html, matrix_transform_slides.html도 동일합니다. 네트워크 MITM 환경(학교 공용 Wi-Fi 등)에서 리소스 변조 가능성이 있습니다.
suggestion: HTTPS가 이미 사용 중이므로 실질적 위험은 낮으나, 오프라인 사용 시 로컬 폰트 파일로 교체하면 가용성과 보안 모두 개선됩니다.
fixable: true
```

```
[FINDING]
file: ai-math/output/_archive/ai_math_perceptron.html
line: (showAns 함수, innerHTML 사용부)
severity: low
category: security
message: showAns(), updateNeuron(), updateAND() 등의 함수에서 innerHTML을 사용하여 DOM을 업데이트합니다. 현재 모든 입력이 하드코딩된 문자열이므로 XSS 위험은 없으나, 향후 사용자 입력을 받는 기능이 추가될 경우 위험해질 수 있습니다.
suggestion: innerHTML 대신 textContent 또는 DOM API를 사용하는 것이 방어적 코딩 관행입니다. 단, 현재 코드에서는 실질적 XSS 벡터가 없으므로 우선순위는 낮습니다.
fixable: true
```

```
[FINDING]
file: ai-math/output/_archive/demo_ai_math_perceptron.html
line: (MathJax.typesetPromise 호출부)
severity: low
category: security
message: Reveal.js slidechanged 이벤트에서 MathJax.typesetPromise()를 typeof 체크 후 직접 호출합니다. 프로젝트 규칙(CLAUDE.md)에 따르면 window.safeTypeset()을 사용해야 합니다. safeTypeset이 없는 이 파일은 아카이브 파일이므로 실질적 보안 위험보다는 규칙 위반입니다.
suggestion: 아카이브 파일이므로 수정 불필요. 신규 파일에서는 window.safeTypeset() 사용을 유지하세요.
fixable: true
```

```
[FINDING]
file: (전체 대상 파일)
severity: info
category: security
message: 모든 파일이 정적 HTML로, 서버 사이드 코드·인증·DB 접근·사용자 데이터 저장이 없습니다. OWASP Top 10 중 Injection, Broken Auth, Sensitive Data Exposure, Access Control, SSRF 등은 해당 사항이 없습니다. 하드코딩된 시크릿도 발견되지 않았습니다.
suggestion: 없음
fixable: false
```

---

## Security Checklist
- [x] No hardcoded secrets
- [x] No user input stored or transmitted
- [x] No SQL/command injection vectors
- [x] No authentication/authorization code
- [ ] SRI (Subresource Integrity) on external CDN resources — **미적용**
- [x] No sensitive data exposure

**결론:** 교육용 정적 HTML 파일로 공격 표면이 극히 제한적입니다. 유일한 실질적 개선점은 외부 CDN에 SRI(integrity) 속성을 추가하는 것이며, 이는 학교 네트워크 환경에서의 방어 깊이를 위한 권장사항입니다.

나머지 리뷰 대상 파일(exam/ 3개, slides/ 대본 4개)도 동일한 패턴의 정적 HTML이므로 위 findings가 동일하게 적용됩니다. 추가적인 보안 이슈는 발견되지 않았습니다.
