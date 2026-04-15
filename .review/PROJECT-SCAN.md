# Project Scan

**프로젝트**: lesson-maker
**경로**: /Users/jeongsanghwa/Projects/lesson-maker
**기술 스택**: Python
**총 파일 수**: 84
**Git**: 있음

## 파일 타입별 분포

- .html: 68개
- .py: 10개
- (no ext): 3개
- .js: 1개
- .tag: 1개
- .md: 1개

## 사용 가능한 스크립트


## 요약

## lesson-maker 프로젝트 요약

**수학 교사를 위한 Reveal.js 기반 강의 교안 자동 생성 시스템**으로, 오케스트레이터(`orchestrator.md`)가 11개 전문 에이전트(슬라이드 생성, 시각화, 애니메이션, 학습지, 시험지 등)를 파이프라인으로 조율하는 **에이전트 오케스트레이션 아키텍처**를 사용한다. 과목별 플러그인 구조(`ai-math/`, `geometry/`, `calculus/` 등의 `config/visuals.md`, `animations.md`)로 6개 수학 과목을 지원하며, 공통 템플릿과 도구는 `_shared/`에 집중되어 있다. 출력물의 대부분(68개)이 HTML 파일로, 슬라이드·학습지·시험지·수행평가 등 다양한 교육 자료를 단일 HTML로 생성하고 Google Drive로 배포하는 구조다.

**리뷰 시 중점 영역**: (1) `_shared/tools/`의 Python 도구들(deploy, html_to_pdf, pdf_renderer 등 7개) — 외부 서비스 연동과 파일 처리 로직, (2) `_shared/templates/`의 공통 템플릿과 `math_animation_lib.js` — 모든 출력물의 렌더링 품질에 직결, (3) 각 과목별 `config/` 플러그인 파일의 코드 패턴 일관성.

*스캔 시각: 2026-03-24T08:28:42.253Z*