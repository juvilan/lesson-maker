# R01 리뷰 결과

카테고리: security
발견된 이슈: 5개
완료 시각: 2026-03-24T21:43:53.803Z

## 발견된 이슈

### F001 [MEDIUM]
- file: `ai-math/output/slides/슬라이드_I-01_인공지능의역사.html`
- line: 7
- severity: medium
- category: security
- message: CDN에서 Reveal.js를 로드할 때 Subresource Integrity(SRI) 해시가 없음. CDN이 침해되면 악성 스크립트가 주입될 수 있음.
- suggestion: <link> 및 <script> 태그에 integrity="sha384-..." crossorigin="anonymous" 속성 추가. 모든 슬라이드 파일에 동일하게 적용.
- fixable: true

### F002 [MEDIUM]
- file: `ai-math/output/slides/슬라이드_I-02_인공지능과수학.html`
- line: 11
- severity: medium
- category: security
- message: MathJax CDN 로드 시 SRI 해시 없음. GSAP CDN(cdnjs.cloudflare.com)도 동일.
- suggestion: integrity 속성 추가. 예: <script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js" integrity="sha384-..." crossorigin="anonymous"></script>
- fixable: true

### F003 [MEDIUM]
- file: `ai-math/output/slides/슬라이드_II-1-01_텍스트자료의표현.html`
- line: 12
- severity: medium
- category: security
- message: MathJax, Google Fonts 등 모든 외부 CDN 리소스에 SRI 해시 없음. 이 파일 포함 리뷰 대상 전체 15개 파일에 동일하게 해당.
- suggestion: 공통 베이스 템플릿(reveal_base.html)에서 SRI를 일괄 적용하는 것을 권장.
- fixable: true

### F004 [LOW]
- file: `ai-math/output/slides/슬라이드_II-1-02_텍스트자료의처리.html`
- line: 14
- severity: low
- category: security
- message: MathJax 설정에서 startup.ready()를 오버라이드하여 defaultReady()를 호출하는 패턴이 있음. 현재는 안전하지만, 이 패턴은 MathJax 초기화 흐름에 커스텀 코드를 삽입할 수 있는 진입점이 됨.
- suggestion: 커스텀 로직이 없다면 startup 오버라이드 제거. 기본 초기화만 사용.
- fixable: true

### F005 [LOW]
- file: `ai-math/output/slides/슬라이드_I-02_인공지능과수학.html`
- severity: low
- category: security
- message: 키보드 이벤트 리스너에서 'f' 키 입력 시 requestFullscreen()을 호출. 프레젠테이션 파일 용도로는 안전하나, 이 파일이 웹에 호스팅될 경우 사용자가 예상하지 못한 전체화면 전환이 발생할 수 있음(minor UX security).
- suggestion: 교실 로컬 사용 전용이면 무시 가능. 웹 호스팅 시에는 명시적 버튼 UI로 대체 권장.
- fixable: true

## 원본 출력

이 파일들은 로컬에서 사용하는 정적 HTML 프레젠테이션 파일로, 사용자 입력/인증/API/DB가 없어 공격 표면이 매우 제한적입니다. 실질적인 보안 이슈만 보고합니다.

```
[FINDING]
file: ai-math/output/slides/슬라이드_I-01_인공지능의역사.html
line: 7-9
severity: medium
category: security
message: CDN에서 Reveal.js를 로드할 때 Subresource Integrity(SRI) 해시가 없음. CDN이 침해되면 악성 스크립트가 주입될 수 있음.
suggestion: <link> 및 <script> 태그에 integrity="sha384-..." crossorigin="anonymous" 속성 추가. 모든 슬라이드 파일에 동일하게 적용.
fixable: true
```

```
[FINDING]
file: ai-math/output/slides/슬라이드_I-02_인공지능과수학.html
line: 11
severity: medium
category: security
message: MathJax CDN 로드 시 SRI 해시 없음. GSAP CDN(cdnjs.cloudflare.com)도 동일.
suggestion: integrity 속성 추가. 예: <script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js" integrity="sha384-..." crossorigin="anonymous"></script>
fixable: true
```

```
[FINDING]
file: ai-math/output/slides/슬라이드_II-1-01_텍스트자료의표현.html
line: 12-18
severity: medium
category: security
message: MathJax, Google Fonts 등 모든 외부 CDN 리소스에 SRI 해시 없음. 이 파일 포함 리뷰 대상 전체 15개 파일에 동일하게 해당.
suggestion: 공통 베이스 템플릿(reveal_base.html)에서 SRI를 일괄 적용하는 것을 권장.
fixable: true
```

```
[FINDING]
file: ai-math/output/slides/슬라이드_II-1-02_텍스트자료의처리.html
line: 14-19
severity: low
category: security
message: MathJax 설정에서 startup.ready()를 오버라이드하여 defaultReady()를 호출하는 패턴이 있음. 현재는 안전하지만, 이 패턴은 MathJax 초기화 흐름에 커스텀 코드를 삽입할 수 있는 진입점이 됨.
suggestion: 커스텀 로직이 없다면 startup 오버라이드 제거. 기본 초기화만 사용.
fixable: true
```

```
[FINDING]
file: ai-math/output/slides/슬라이드_I-02_인공지능과수학.html
line: 하단 script
severity: low
category: security
message: 키보드 이벤트 리스너에서 'f' 키 입력 시 requestFullscreen()을 호출. 프레젠테이션 파일 용도로는 안전하나, 이 파일이 웹에 호스팅될 경우 사용자가 예상하지 못한 전체화면 전환이 발생할 수 있음(minor UX security).
suggestion: 교실 로컬 사용 전용이면 무시 가능. 웹 호스팅 시에는 명시적 버튼 UI로 대체 권장.
fixable: true
```

---

**요약**: 리뷰 대상 15개 파일 모두 정적 프레젠테이션으로, 사용자 입력 처리·인증·DB·API 호출이 없어 OWASP Top 10의 대부분(Injection, Broken Auth, SSRF 등)은 해당 없음. 유일한 실질적 이슈는 **외부 CDN 리소스의 SRI 미적용**(medium)이며, 이는 `_shared/templates/reveal_base.html` 베이스 템플릿에서 일괄 수정하는 것이 효율적입니다.

**Risk Level: LOW**
