# Pretendard 폰트 로컬 번들링 (오프라인 대응)

> **보관 노트** (2026-08-19 추가)
> 이 문서는 커밋 `bcb12e4`의 계획서다. 원래 맥의 `~/.claude/plans/`에 있어 기기 전환 시
> 넘어오지 않았기에, 판단 근거를 코드와 같은 곳에 남기려고 저장소로 옮겼다. **본문은 원문 그대로다.**
>
> 아래 "검증" 절의 명령은 **맥 기준**이다. 그대로 실행되지 않는다:
> - 서버 경로가 맥 worktree(`/Users/jeongsanghwa/...`)이며, 그 worktree는 이미 main에 병합되어 존재하지 않는다.
> - 윈도우 업무용 노트북에는 Python이 설치돼 있지 않아 `python3 -m http.server` 자체가 안 돈다.
> - 포트 8765는 다른 프로세스가 점유 중이라 재검증 시 8791 등으로 피해야 한다 (`.claude/handoff.md` 2절).
>
> 작업 자체는 **완료·검증됨**이며 재검증이 필요하지 않다. 결과 확인만 하려면
> `_shared/fonts/PretendardVariable.woff2`(2,057,688 bytes, 시그니처 `wOF2`) 존재와
> `design-tokens.css` 내 외부 URL 0개를 보면 된다.

---

## Context

`_shared/templates/design-tokens.css`의 폰트 블록(19~29줄)이 **두 개의 폰트 공급원을 선언하는데 둘 다 404**다. 실측으로 확인한 내용:

| 줄 | 선언 | 실제 상태 |
|---|---|---|
| 21 | `@import .../pretendard@2.3.0/dist/web/variable/pretendardvariable.min.css` | **404** — `2.3.0` 태그가 존재하지 않음 (최신 = `1.3.9`) |
| 23~29 | `@font-face { src: url('../fonts/PretendardVariable.woff2') }` | **404** — `_shared/fonts/` 디렉토리 자체가 없음 (저장소 내 폰트 파일 0개) |

결과: Pretendard는 **지금도 전혀 로딩되지 않고** `--lm-font-sans`(96줄) 폴백 체인의 맑은 고딕/Apple SD Gothic Neo로 렌더링되고 있다. 최초 진단의 "CDN이 실제 폰트를 공급 중이라 렌더링은 정상"이라는 전제는 실측으로 반증됐다.

**이번 작업의 목적**: 로컬 woff2를 저장소에 번들링해 오프라인·CDN 차단 환경에서도 Pretendard가 실제로 적용되게 만들고, 깨진 CDN 의존을 제거한다.

### 함께 확인된 사실 (계획 수립 근거)

- **영향 범위는 좁다.** `design-tokens.css`를 실제로 `<link>`하는 파일은 4개뿐이다: `_shared/templates/reveal_base.html:48`, `worksheet_base.html:11`, `reference/slide-kitchen-sink.html:21`, `reference/worksheet-kitchen-sink.html:8`. **`output/` 하위 산출물 HTML 90개 중 참조하는 파일은 0개**다. 따라서 "모든 산출물 HTML에서 404" 역시 사실이 아니며, 검증도 산출물이 아닌 kitchen-sink로 해야 한다.
- **CSS 폰트 매칭 동작(브라우저 실측).** 같은 `font-family` + 같은 descriptor의 `@font-face`가 여러 개일 때, 로드에 실패한 face는 건너뛰고 같은 family의 다른 유효 face가 사용된다. 선언 순서 양방향 모두 확인. → 19줄 주석의 "CDN 1순위 · 로컬 2순위"는 실제 동작(마지막 선언 우선)과 반대다.
- **라이선스.** Pretendard는 SIL Open Font License 1.1. OFL 1.1은 폰트 소프트웨어 사본에 저작권·라이선스 고지를 동봉할 것을 요구하므로 `_shared/fonts/LICENSE`를 함께 커밋한다.

### 범위 밖 (사용자 결정: 이번엔 손대지 않음)

아래 2건은 실재하는 문제지만 별도 작업으로 남긴다.

1. **산출물이 디자인 시스템과 단절** — `output/` HTML 90개 전부 `design-tokens.css` 대신 Google Fonts(Noto Sans KR)를 직접 링크한다. 이번 폰트 수정의 혜택이 산출물에는 닿지 않는다.
2. **템플릿 상대경로 깊이 불일치** — `reveal_base.html` / `worksheet_base.html`이 `../../_shared/`를 쓰는데 산출물 89/90개가 `<과목>/output/<하위폴더>/` 3단계에 있어 `../../../_shared/`가 필요하다.

(참고로 `--lm-font-mono: 'JetBrains Mono'`도 대응하는 `@font-face`가 저장소 어디에도 없다. 기록만 남긴다.)

---

## 변경 사항

### 1. `_shared/fonts/PretendardVariable.woff2` 추가 (신규)

- 출처: `https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/packages/pretendard/dist/web/variable/woff2/PretendardVariable.woff2`
- 크기: 1.96 MB (2,057,688 bytes), `content-type: font/woff2` — 실측 확인됨
- `.gitignore`에 폰트 제외 규칙이 없으므로 그대로 추적된다.
- 다운로드 후 파일 크기와 woff2 시그니처(`wOF2`)를 확인해 정상 파일인지 검사한다.

### 2. `_shared/fonts/LICENSE` 추가 (신규)

- 출처: `https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/LICENSE` (SIL OFL 1.1)
- OFL 1.1의 고지 동봉 요건 충족.

### 3. `_shared/templates/design-tokens.css` 18~29줄 수정

깨진 `@import`(21줄)를 삭제하고, `@font-face` 블록은 그대로 두되 주석을 실제 동작에 맞게 고친다. `src` 경로 `../fonts/PretendardVariable.woff2`는 `_shared/templates/` 기준으로 `_shared/fonts/`를 정확히 가리키므로 **변경하지 않는다**.

```css
/* ────────────────────────────────────────────────────────────────────────────
 * Pretendard 폰트 — 저장소 번들 woff2 (오프라인 동작, CDN 의존 없음)
 * 파일: _shared/fonts/PretendardVariable.woff2 (SIL OFL 1.1, LICENSE 동봉)
 * 로드 실패 시 --lm-font-sans 폴백 체인(맑은 고딕 등)으로 자동 대체됨.
 * ────────────────────────────────────────────────────────────────────────── */
@font-face {
  font-family: 'Pretendard Variable';
  font-weight: 45 920;
  font-style: normal;
  font-display: swap;
  src: url('../fonts/PretendardVariable.woff2') format('woff2-variations');
}
```

96줄 `--lm-font-sans` 폴백 체인은 손대지 않는다 — 로드 실패 시 안전망으로 계속 유효하다.

---

## 검증

최초 진단이 제안한 검증 방법은 그대로 쓰면 아무것도 증명하지 못한다. 두 가지를 바로잡아 진행한다:

- **서버 루트**: 편집은 worktree에서 이뤄지므로 `--directory`를 worktree로 지정해야 한다. 원본 경로(`~/Projects/lesson-maker`)를 서빙하면 수정 전 파일을 보게 된다.
- **대상 파일**: 산출물 HTML은 `design-tokens.css`를 참조하지 않으므로 변경 전후 모두 404가 없다. 실제 소비자인 **kitchen-sink**를 열어야 한다.

### 1) 서버 기동

```bash
python3 -m http.server 8765 --directory /Users/jeongsanghwa/Projects/lesson-maker/.claude/worktrees/reverent-moser-21ec5b
```

### 2) 404 부재 확인 (음성 테스트)

브라우저로 `http://localhost:8765/_shared/templates/reference/worksheet-kitchen-sink.html` 을 열고 `read_network_requests`로 폰트/CSS 요청에 404가 없는지, `jsdelivr` 폰트 요청이 사라졌는지 확인한다. (`slide-kitchen-sink.html`도 동일하게 확인 — 단 이쪽은 reveal.js CDN을 별도로 쓴다.)

### 3) 폰트가 실제 적용됐는지 확인 (양성 테스트) — 핵심

"404가 없다"는 오프라인 대응이 됐다는 증거가 아니다. 계획 수립 중 사용한 폭 측정 방식을 그대로 재사용해, Pretendard가 실제로 그려지는지 확인한다. 기준값은 이미 실측돼 있다: **폴백(맑은 고딕) 1070.91px vs Pretendard 적용 1130.57px** (100px, `가나다라마바사ABCabc123`).

```js
(async () => {
  await document.fonts.ready;
  const m = f => { const d=document.createElement('span');
    d.style.cssText=`font-family:${f};font-size:100px;position:absolute;visibility:hidden;white-space:nowrap;`;
    d.textContent='가나다라마바사ABCabc123'; document.body.appendChild(d);
    const w=d.getBoundingClientRect().width; d.remove(); return Math.round(w*100)/100; };
  return JSON.stringify({
    faces: [...document.fonts].map(f=>`${f.family}|${f.status}`),
    withPretendard: m("'Pretendard Variable','Malgun Gothic',sans-serif"),
    fallbackOnly:   m("'Malgun Gothic',sans-serif")
  });
})()
```

**합격 기준**: `faces`에 `Pretendard Variable|loaded`가 있고, `withPretendard !== fallbackOnly`.

### 4) 오프라인 회귀 테스트

브라우저 네트워크를 오프라인으로 전환하거나 `cdn.jsdelivr.net`을 차단한 상태에서 (2)(3)을 재실행해 결과가 동일한지 확인한다. 이 단계가 통과해야 이번 작업의 목적이 달성된 것이다.

### 5) 서버 정리

`preview_stop`으로 서버를 종료한다.
