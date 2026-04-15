# R01 리뷰 결과

카테고리: security
발견된 이슈: 1개
완료 시각: 2026-03-24T21:47:56.432Z

## 발견된 이슈

### F001 [MEDIUM]
- file: `unknown`
- severity: medium
- category: security
- message: - **Critical/High/ 0건**
- fixable: false

## 원본 출력

Security 리뷰 결과 요약:

- **전체 위험도: LOW** — 실질적 보안 위험 없음
- **Critical/High/Medium: 0건**
- **Low 2건**: `슬라이드_1-1_이차곡선.html`에서 `innerHTML` 사용 (계산된 숫자값만 삽입하므로 XSS 벡터 없음)
- **Info 2건**: inline onclick/style로 인한 CSP 비호환 (로컬 전용이므로 해당 없음)

로컬 교실 프로젝터용 정적 HTML 파일이라 서버 통신·인증·사용자 데이터 처리가 전혀 없어 **코드 수정 불필요**합니다.
