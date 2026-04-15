# workspace/ — 중간 JSON 파일 저장소

오케스트레이터가 Wave 1→2→3 파이프라인 실행 중 생성하는 **중간 JSON 파일**들이 저장된다.

## 구조

```
workspace/
├── {YYYYMMDD_HHMMSS}/        ← 세션별 자동 생성 디렉토리
│   ├── textbook_analysis.json
│   ├── web_research.json
│   ├── visual_assets.json
│   ├── math_animations.json
│   ├── slide_structure.json
│   ├── worksheet.json
│   └── lecture_script.json
├── {subject}_{topic}/        ← 주제별 디렉토리 (선택)
└── *.json                    ← 개별 JSON (레거시)
```

## 정리 정책

| 보존 | 삭제 가능 |
|------|-----------|
| 최종 출력 참조에 사용된 JSON | 완성된 슬라이드에 대응하는 오래된 세션 |
| 문제은행 JSON (`exam_bank_*.json`) | 3개월 이상 된 세션 디렉토리 |

## Git 제외

workspace/ 하위 파일은 모두 `.gitignore`로 제외된다.
결과물은 `{subject}/output/` 에 HTML로 저장되므로 중간 파일은 복구 불필요.
