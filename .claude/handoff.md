# 인수인계 노트

**작성**: 2026-08-19 (수) 09:32 KST · 맥(M4, `jeongsanghwa`) → 윈도우 업무용 노트북

---

## 1. 브랜치 지도

윈도우에서 clone하면 **worktree 구조가 아니라 브랜치들**을 받습니다.
맥의 `.claude/worktrees/` 레이아웃은 gitignore라 넘어오지 않습니다. 재현하지 마시고 `git checkout`으로 오가시면 됩니다.

| 브랜치 | 내용 | 상태 |
|---|---|---|
| `main` | 공통 베이스 (`d8a22b6`) | 원격과 동일 |
| `lesson/ai-math-2022-1-1` | 인공지능수학(2022) 1-1 1~2차시 수업자료 (`3b40f30`) | main에 미병합 |
| `claude/reverent-moser-21ec5b` | Pretendard 폰트 로컬 번들링 + 이 노트 | main에 미병합 |
| ~~`claude/strange-villani-e75dbb`~~ | **내용 없음** — main과 동일한 빈 브랜치. 무시하거나 삭제 | — |

**세 브랜치는 아직 합치지 않았습니다.** 기기 이동을 머지 결정에 묶지 않으려고 그대로 뒀습니다.
윈도우에서 순서를 정해 정리하시면 됩니다.

## 2. 직전 작업 — Pretendard 폰트 번들링 (완료·검증됨)

`_shared/templates/design-tokens.css`가 폰트 공급원 두 개를 선언하는데 **둘 다 404**였습니다.

- CDN `@import`의 `pretendard@2.3.0` — 존재하지 않는 태그 (최신은 1.3.9)
- 로컬 `@font-face`의 `../fonts/PretendardVariable.woff2` — `_shared/fonts/` 자체가 없었음

결과적으로 Pretendard는 그동안 **전혀 적용되지 않고** 맑은 고딕으로 렌더링되고 있었습니다.

**조치**: `_shared/fonts/PretendardVariable.woff2`(1.96MB, SIL OFL 1.1, LICENSE 동봉)를 저장소에 번들링하고 깨진 CDN `@import`를 제거. 이제 외부 의존 0.

**검증 완료** (재확인 필요 없음):
- 서버 로그 404 = `/favicon.ico` 2건뿐, 폰트·CSS는 전부 200/304
- `document.fonts`에 `Pretendard Variable|45 920|loaded`
- 폭 실측: Pretendard 1130.57px vs 폴백 1070.91px → 실제 적용됨
- `design-tokens.css` 내 외부 URL **0개**

재검증이 필요하면 (포트 8765는 다른 프로세스가 점유 중이니 피할 것):

```
python3 -m http.server 8791
```

띄운 뒤 `_shared/templates/reference/worksheet-kitchen-sink.html` 을 엽니다.
⚠️ `output/` 산출물 HTML로는 검증이 안 됩니다 — 아래 3번 참조.

## 3. 다음에 할 일 (범위 밖으로 남긴 실재 문제 3건)

우선순위 순.

1. **산출물 90개가 디자인 시스템과 단절** — `output/` 하위 HTML 중 `design-tokens.css`를 참조하는 파일이 **0개**입니다. 전부 Google Fonts(Noto Sans KR)를 직접 링크합니다. 즉 이번 폰트 수정의 혜택이 실제 수업자료에는 닿지 않습니다. 가장 큰 건.
2. **템플릿 상대경로 깊이 불일치** — `reveal_base.html:48`·`worksheet_base.html:11`이 `../../_shared/`를 쓰는데 산출물 89/90개는 `<과목>/output/<하위폴더>/` 3단계라 `../../../_shared/`가 필요합니다. 템플릿을 그대로 복사하면 CSS가 404 납니다. 1번을 하려면 이것부터.
3. `--lm-font-mono: 'JetBrains Mono'`에 대응하는 `@font-face`가 저장소 어디에도 없습니다.

## 4. 기기 전환 시 주의

- **저장소 안에 없는 것은 넘어오지 않습니다.** 계획 파일은 맥의 `~/.claude/plans/`에 있어 윈도우에 없습니다. 대화 내용도 마찬가지입니다. 남길 게 있으면 이 파일에 적으세요.
- **clone 용량**: 약 283MB이고 그 대부분이 `*/book/*.pdf`(316MB, 미래엔 교과서)입니다. 교안 작업에 매번 필요하진 않으니 학교 노트북에서는 제외하고 받는 것을 권합니다.
  ```
  git clone --filter=blob:none --no-checkout https://github.com/juvilan/lesson-maker.git
  ```
  ```
  cd lesson-maker && git sparse-checkout set --no-cone '/*' '!/*/book/' && git checkout main
  ```
  (이 두 명령은 아직 실제로 실행해 검증하지 않았습니다. `du -sh .`로 결과를 확인하세요. PDF가 필요해지면 `git sparse-checkout disable`.)
- **습관**: 작업 시작 `/sync`, 작업 끝 `/commit-push-pr`. 이번에 `3b40f30`이 push 없이 맥에만 20일 남아 있던 게 이 습관이 빠져서였습니다.
