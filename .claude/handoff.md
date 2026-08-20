# 인수인계 노트

**작성**: 2026-08-19 (수) 09:32 KST · 맥(M4, `jeongsanghwa`) → 윈도우 업무용 노트북

---

## 1. 브랜치 지도

윈도우에서 clone하면 **worktree 구조가 아니라 브랜치들**을 받습니다.
맥의 `.claude/worktrees/` 레이아웃은 gitignore라 넘어오지 않습니다. 재현하지 마시고 `git checkout`으로 오가시면 됩니다.

**2026-08-19 병합 완료.** `main`만 보시면 됩니다.

| 브랜치 | 내용 | 상태 |
|---|---|---|
| `main` | 아래 둘이 모두 들어 있음 | ✅ 여기서 작업 |
| `lesson/ai-math-2022-1-1` | 인공지능수학(2022) 1-1 1~2차시 수업자료 (`3b40f30`) | main에 병합됨 |
| `claude/reverent-moser-21ec5b` | Pretendard 폰트 로컬 번들링 + 이 노트 | main에 병합됨 |
| `claude/strange-villani-e75dbb` | **내용 없음** — main과 동일한 빈 브랜치 | 원격에 없음. 무시 |

두 브랜치는 건드리는 파일이 겹치지 않아 충돌 없이 병합됐습니다.
병합된 브랜치들은 삭제하셔도 됩니다.

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

### ⚠️ 슬라이드 작성 시 함정 — 수식 안의 `<`

MathJax 수식 안에서 **`<` 바로 뒤에 알파벳이 오면 브라우저가 HTML 태그 시작으로 파싱해
그 줄의 나머지를 통째로 삼킵니다.** 콘솔 에러도, MathJax 에러도 나지 않아 눈으로만 발견됩니다.

```
\(x<h\)        → <h ... 가 태그로 먹힘 (깨짐)
\(0<h\le 2\)  → 깨짐
\(x &lt; h\)   → 정상
\(x < 1\)      → 정상 (뒤가 숫자·공백이면 태그가 아님)
```

**규칙: 수식 안의 `<`는 항상 `&lt;`로 쓴다.** 2026-08-20 1-2-3차시 덱에서 실제로 겪었습니다.
검출: `grep -nE '<[a-zA-Z]' 파일 | grep -v '</\?\(div\|span\|b\|td\|tr\)'`

## 4. 기기 전환 시 주의

- **저장소 안에 없는 것은 넘어오지 않습니다.** 계획 파일은 맥의 `~/.claude/plans/`에 있어 윈도우에 없습니다. 대화 내용도 마찬가지입니다. 남길 게 있으면 이 파일에 적으세요.
- **계획서는 `docs/plans/`에 남깁니다.** `~/.claude/plans/`는 기기를 넘지 못하므로, 계획이 확정되면 `docs/plans/YYYY-MM-DD-<주제>.md`로 저장소에 복사해 커밋합니다. 결과물(코드)만 넘어오고 판단 근거가 사라지는 걸 막기 위해서입니다. 실례: `docs/plans/2026-08-19-pretendard-bundling.md` — 커밋 `bcb12e4`의 근거 문서로, 폰트 조사 실측치(폴백 1070.91px vs Pretendard 1130.57px 등)가 들어 있습니다.
- **새 기기 설정의 정본은 `README.md`의 "다른 기기에서 작업하기"입니다.** 전체 clone + `pip install -r requirements.txt` + `playwright install chromium`. 교과서 PDF는 수업 설계에 쓰이므로 저장소에 **일부러 포함**돼 있고, 지도서(52MB)만 제외돼 Google Drive에서 따로 복사합니다.
- (선택) 학교 노트북 용량이 부담되면 교과서 PDF를 빼고 받을 수도 있습니다. clone 약 283MB 중 대부분이 `*/book/*.pdf`(316MB)입니다. 다만 PDF 없이는 교안 설계 시 교과서 참조가 안 되니, **기본은 README대로 전체 clone**을 권합니다.
  ```
  git clone --filter=blob:none --no-checkout https://github.com/juvilan/lesson-maker.git
  cd lesson-maker && git sparse-checkout set --no-cone '/*' '!/*/book/' && git checkout main
  ```
  ⚠️ **이 명령은 쓰지 마세요 — 검증 결과 실패입니다.** 2026-08-19 윈도우에서 실제로 실행한 결과 `You are in a sparse checkout with 0% of tracked files present.` 로, 파일이 하나도 체크아웃되지 않은 빈 저장소가 만들어졌습니다. `--no-cone`의 포함 패턴 `'/*'`와 배제 패턴 `'!/*/book/'`이 충돌한 것으로 보입니다. 용량을 줄여야 한다면 cone 모드로 다시 작성해 **실제 clone으로 검증한 뒤** 이 자리에 적어주세요. (잘못 실행했다면 되돌리기: `git sparse-checkout disable` 또는 저장소를 지우고 README대로 전체 clone.)
- **습관**: 작업 시작 `/sync`, 작업 끝 `/commit-push-pr`. 이번에 `3b40f30`이 push 없이 맥에만 20일 남아 있던 게 이 습관이 빠져서였습니다.

## 5. 윈도우 노트북 환경 — 남은 작업 3건 (2026-08-19)

저장소가 아니라 **기기 설정** 쪽 잔여 작업입니다. 저장소 작업(3절)과 별개입니다.

1. **빈 껍데기 폴더 삭제** — `C:\Users\user\lesson-maker`. 4절의 sparse-checkout 명령이 만든 0% 체크아웃 저장소 자리로, 내용물(중복 clone 604MB + 깨진 `.git`)은 이미 지웠고 **빈 디렉터리만 남았습니다.** 그 폴더를 작업 디렉터리로 잡은 Claude Code 세션이 있으면 삭제가 막히니, `Projects\lesson-maker`에서 세션을 연 뒤 실행하세요.
   ```
   Remove-Item -Force C:\Users\user\lesson-maker
   ```
   ※ 이 저장소의 정본 위치는 `C:\Users\user\Projects\lesson-maker`입니다 (맥의 `~/Projects/lesson-maker`와 같은 배치).

2. **Python Store 별칭 정리** (GUI라 직접 해야 함) — 설정 → 앱 → 고급 앱 설정 → 앱 실행 별칭에서 **`python3` (3.13) 항목 끄기**.
   **Python은 설치돼 있습니다 — 3.14.7** (`AppData\Local\Python\pythoncore-3.14-64`, pip 26.2.1). PowerShell에서는 `python`·`python3`·`py` 모두 정상입니다.
   그런데 **Git Bash에서만 `python3`이 항상 실패합니다**(`0x80070002`). 사라진 3.13 Store 패키지를 가리키는 확장자 없는 별칭 stub을 MSYS가 실행하지 못하는 것으로, **Bash에서 안 된다고 "Python 미설치"로 오진하기 쉽습니다**(실제로 2026-08-19에 그렇게 오진했습니다). 판단 전에 PowerShell로 교차 확인하세요.
   별칭을 정리하면 Git Bash에서도 `python3`이 살아나고, `~/.claude/skills/continuous-learning-v2/hooks/observe.sh`의 간헐적 blocking 에러도 사라집니다. (그 훅은 현재 `~/.claude/homunculus/disabled` 파일로 꺼둔 상태 — 파일을 지우면 다시 켜집니다.)
   PDF 파이프라인 의존성은 **설치·검증 완료**입니다: playwright 1.62.0 + pypdf 6.16.1 + Chrome Headless Shell 151. `html_to_pdf.py`로 kitchen-sink 8페이지 변환 확인.

3. **`~/.claude/rules/agents-v2.md`의 `~/qjc-office/` 경로** — 이 기기에 그 경로가 없어 참조 6개가 전부 끊깁니다. 같은 내용이 `C:\Users\user\Projects\claude-forge\`에 있고, `reference/`에 3개(`agents-config-ref.md`, `agents-teams-ref.md`, `server-inventory.md`)가 존재합니다.
   나머지 3개(`agent-catalog.md`, `agent-pipeline.md`, `parallel-agents-guide.md`)는 **claude-forge 저장소 어디에도 없습니다**(0/0 동기화 상태 확인). 맥에서 `ls ~/qjc-office/dotclaude/reference/`로 실재 여부를 먼저 확인하고, 있으면 claude-forge에 커밋·push, 없으면 rules에서 참조를 제거하세요.
   경로 통일 방식은 미결정입니다 — (A) 맥에 `~/Projects/claude-forge` symlink 후 rules를 그 경로로 통일 / (B) rules를 `claude-forge/reference/` 상대 표기로 / (C) 윈도우 경로로 바꾸고 맥은 나중에.
   ⚠️ **`~/.claude/rules/*.md`와 `~/.claude/settings.json`은 `claude-forge/`와 바이트 동일한 install 산출물입니다.** 직접 고치면 `/forge-update`·`install.ps1`이 되돌립니다. 수정은 반드시 claude-forge 저장소에서 하세요.
