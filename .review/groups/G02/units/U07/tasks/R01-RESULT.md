# R01 리뷰 결과

카테고리: security
발견된 이슈: 1개
완료 시각: 2026-03-24T21:46:23.493Z

## 발견된 이슈

### F001 [INFO]
- file: `ai-math-2022/output/slides/슬라이드_1-1_인공지능의의미.html (및 슬라이드 1-2, 1-3 동일)`
- severity: info
- category: security
- message: 외부 라이브러리(Reveal.js, MathJax, Chart.js, GSAP, p5.js)를 로컬 상대경로(../../libs/)로 로드하고 있으며 Subresource Integrity(SRI) 해시가 없습니다. 현재 로컬 전용이므로 실질적 위험은 없으나, 웹 서버 배포 시 공급망 변조 위험이 존재합니다.
- suggestion: 웹 서버 배포 시 CDN + SRI 해시 적용 또는 로컬 파일 무결성 검증 절차 추가 검토
- fixable: true

## 원본 출력

이 파일들은 모두 **정적 HTML 교육 자료**(Reveal.js 슬라이드, 강의 대본, 학습지)로, 서버 사이드 코드, 사용자 입력 처리, API 호출, 인증/인가, 데이터베이스 연동이 전혀 없습니다.

## Security Review 결과

**Risk Level: LOW**

- Critical Issues: 0
- High Issues: 0
- Medium Issues: 0
- Low Issues: 0
- Info Issues: 1

### 검토 항목별 결과

| OWASP 카테고리 | 해당 여부 | 결과 |
|---|---|---|
| Injection (SQLi, Command) | 해당 없음 | DB/서버 연동 없음 |
| Authentication | 해당 없음 | 인증 없음 |
| Sensitive Data Exposure | 해당 없음 | 민감 데이터 없음 |
| XSS | 해당 없음 | 사용자 입력 없음 |
| CSRF | 해당 없음 | 폼/API 없음 |
| Hardcoded Secrets | 확인 완료 | 발견 없음 |

```
[FINDING]
file: ai-math-2022/output/slides/슬라이드_1-1_인공지능의의미.html (및 슬라이드 1-2, 1-3 동일)
line: N/A
severity: info
category: security
message: 외부 라이브러리(Reveal.js, MathJax, Chart.js, GSAP, p5.js)를 로컬 상대경로(../../libs/)로 로드하고 있으며 Subresource Integrity(SRI) 해시가 없습니다. 현재 로컬 전용이므로 실질적 위험은 없으나, 웹 서버 배포 시 공급망 변조 위험이 존재합니다.
suggestion: 웹 서버 배포 시 CDN + SRI 해시 적용 또는 로컬 파일 무결성 검증 절차 추가 검토
fixable: true
```

### Security Checklist

- [x] No hardcoded secrets (API keys, passwords, tokens)
- [x] No user input handling (XSS/injection 불가)
- [x] No SQL/command injection vectors
- [x] No sensitive data in HTML
- [x] No external API calls or fetch requests
- [x] No authentication/authorization code
- [x] Dependencies: 로컬 오프라인 로드 (CDN 미사용)

**결론**: 9개 파일 모두 정적 교육 콘텐츠로, 보안 공격 표면(attack surface)이 사실상 없습니다. 실질적 보안 이슈 없음.
