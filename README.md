# lesson-maker

수학 교사가 Reveal.js 기반 HTML 슬라이드/학습지/시험지를 생성·배포하는 시스템입니다.

## 진입점

- `lesson-maker/orchestrator.md`

## 출력 경로

- `lesson-maker/{subject}/output/slides/`
- `lesson-maker/{subject}/output/worksheet/`
- `lesson-maker/{subject}/output/exam/`
- `lesson-maker/{subject}/output/수행평가/`
- 중간 산출물: `lesson-maker/workspace/`

## 과목 플러그인

각 과목은 `{subject}/config/` 아래에 시각화/애니메이션 템플릿을 둡니다.

- `visuals.md`: 시각화 타입 목록 + 코드 패턴
- `animations.md`: 애니메이션 단계 구성 패턴

## 배포/도구

공통 도구는 `lesson-maker/_shared/tools/`에 있습니다.

- `deploy.py`: Google Drive 자동 배포
- `rename_output.py`: 출력 파일 네이밍 정돈
- `html_to_pdf.py`: Playwright 기반 PDF 변환

