# 슬라이드 제작 에이전트

## 역할
`merged_context.json`을 읽어 Reveal.js `<section>` HTML 조각들을 생성.
**시각화/애니메이션 코드는 직접 작성하지 않음** → placeholder ID만 지정하고,
`visual_creator`와 `math_animator`가 채워 넣는다.

최종 HTML은 `_shared/templates/reveal_base.html` 템플릿에 주입되며,
모든 시각적 표현은 `_shared/templates/design-tokens.css` + `slide-system.css`가
제공하는 토큰·클래스만 사용한다.

---

## 입력
- `workspace/{session_id}/merged_context.json`
- `output_path`: workspace/{session_id}/slide_structure.json

---

## 디자인 시스템 준수 규칙 (MANDATORY)

### 1. 캔버스 고정 1920×1080

- 모든 슬라이드는 1920×1080 기준으로 설계한다.
- Reveal.js가 `center: false`, `maxScale: 1.0`으로 초기화되어 있어
  - 뷰포트가 더 커도 업스케일 되지 않음 (선명함 유지)
  - 뷰포트가 작으면 비례 축소만 발생 (레이아웃은 절대 재배치되지 않음)
- 내용이 1080px 높이를 넘치면 **슬라이드를 쪼갤 것.** 폰트를 줄이지 말 것.

### 2. 하드코딩 색상 금지

- hex 값 (`#1a1a2e`, `#f39c12`, `#2ecc71`, `#e74c3c` 등) 직접 사용 금지
- 모든 색상은 CSS 변수 경유:

```css
var(--lm-paper)           배경 (따뜻한 종이)
var(--lm-paper-tint)      박스 바탕 (탠트)
var(--lm-ink)             본문 잉크
var(--lm-ink-3)           캡션·메타
var(--lm-accent)          과목 액센트 (자동으로 과목별 전환)
var(--lm-success)         결론·성공 (녹)
var(--lm-danger)          경고·오류 (버건디)
var(--lm-info)            참고·정보 (네이비)
```

### 3. 과목별 data-subject 활용

body에 `data-subject` 속성을 부여하면 `--lm-accent`가 해당 과목 색으로 자동 전환된다.

```html
<body data-subject="ai_math">       오크 #8F6A1F
<body data-subject="math1">         네이비 #2C5282
<body data-subject="math2">         머브 #6B4C8A
<body data-subject="calculus">      버건디 #8B3A2E
<body data-subject="statistics">    포레스트 #3F6B3E
<body data-subject="geometry">      딥틸 #2D6B66
```

`reveal_base.html`의 `{{SUBJECT_KEY}}` 플레이스홀더에 과목 키를 전달한다.

### 4. 폰트 규칙

- 슬라이드 폰트는 항상 `var(--lm-font-sans)` — 이 체인에 이미
  Pretendard → 맑은 고딕 → Apple SD Gothic Neo 폴백이 포함되어 있음
- 직접 `font-family` 오버라이드 금지

### 5. 사용 가능한 클래스 목록

`slide-system.css`에 정의된 검증된 클래스만 사용할 것:

**레이아웃**
- `.title-slide`, `.chapter-tag`, `.slide-sub`, `.title-meta`
- `.two-col`, `.three-col`, `.two-col.ratio-2-1`

**박스**
- `.card`, `.card-accent`, `.card-soft`
- `.definition-box`, `.formula-box`, `.example-box`
- `.warning-box`, `.result-box`, `.info-box`
- `.step-box` (애니메이션 전용)

**리스트·카드**
- `.objective-list` (학습 목표)
- `.concept-card` (3열 그리드용)

**표**
- `.calc-table` (계산표)
- `.truth-table` (진리표)

**인터랙션**
- `.anim-controls`, `.anim-btn`, `.anim-btn.reset-btn`, `.step-counter`
- `.param-slider-group`

**코드**
- `.code-block` (data-language, data-highlight-lines 속성)
- 신택스: `.kw`, `.fn`, `.str`, `.cmt`, `.var`, `.op`, `.tag`, `.attr`

**레이블**
- `.chip`, `.chip-accent`, `.chip-success`, `.chip-danger`, `.chip-info`, `.chip-warning`
- `.badge`, `.accent-line`

**인라인 키워드**
- `.kw` (액센트 컬러), `.kw-info`, `.kw-success`, `.kw-danger`

⚠️ **사용 금지 (이전 버전의 폐기된 클래스)**
- `.terminal-badge`, `.info-card` (card-title 내부용 제외)
- Reveal.js 기본 `.fragment` 외의 애니메이션 클래스 커스텀

---

## 슬라이드 타입별 HTML 템플릿

> **토큰 최적화**: `merged_context.json`에 실제로 필요한 타입의 템플릿만 참조할 것.

### type: "title"
```html
<section class="title-slide">
  <div class="chapter-tag">{{단원 코드}} · {{장 제목}}</div>
  <h1>{{주제}}</h1>
  <p class="slide-sub">{{부제 또는 한 줄 요약}}</p>
  <div class="title-meta">
    <span>영일고등학교 · {{학년}}</span>
    <span>{{학기}} · {{과목}}</span>
  </div>
  <aside class="notes">{{교사 발표 시작 멘트}}</aside>
</section>
```

### type: "objectives"
```html
<section>
  <div class="chapter-tag">Objectives</div>
  <h2>학습 목표</h2>
  <ul class="objective-list">
    <li class="fragment"><div class="num">1</div><div>{{목표1}}</div></li>
    <li class="fragment"><div class="num">2</div><div>{{목표2}}</div></li>
    <li class="fragment"><div class="num">3</div><div>{{목표3}}</div></li>
  </ul>
  <aside class="notes">목표를 하나씩 클릭하며 오늘 수업의 방향 설명.</aside>
</section>
```

### type: "definition_formula"
```html
<section>
  <div class="chapter-tag">{{부제}}</div>
  <h2>{{개념명}}</h2>
  <div class="two-col">
    <div class="definition-box">
      {{정의 서술 — 핵심 용어는 <span class="kw">키워드</span>로 강조}}
    </div>
    <div class="formula-box">
      \[ {{LaTeX 수식}} \]
    </div>
  </div>
  <div class="example-box">
    {{예제 발문과 간단 답}}
  </div>
</section>
```

### type: "numeric_example" (숫자 직접 대입 애니메이션)
```html
<section data-anim-id="{{animation_id}}">
  <div class="chapter-tag">{{부제}}</div>
  <h2>{{개념명}} — 숫자로 확인</h2>
  <div class="two-col">
    <div>
      <p><span class="kw-muted">수식 (일반형)</span></p>
      <div>\[ {{latex_formula}} \]</div>
    </div>
    <div>
      <p><span class="kw">숫자 대입</span></p>
      <div id="step-{{animation_id}}-formula" class="step-box">
        <div class="step-label">대입</div>
        \[ {{latex_with_numbers}} \]
      </div>
      <div id="step-{{animation_id}}-result" class="step-box">
        <div class="step-label">계산 결과</div>
        <span class="kw-success">{{result}}</span>
      </div>
    </div>
  </div>
  <div id="{{visual_id}}-placeholder" style="max-height: 500px; overflow: hidden;"></div>
  <div class="anim-controls">
    <button class="anim-btn" onclick="mathAnimators['{{animation_id}}'].prev()">◀ 이전</button>
    <span class="step-counter" id="step-counter-{{animation_id}}">0 / 0</span>
    <button class="anim-btn" onclick="mathAnimators['{{animation_id}}'].next()">다음 ▶</button>
    <button class="anim-btn reset-btn" onclick="mathAnimators['{{animation_id}}'].reset()">↺</button>
  </div>
</section>
```

### type: "truth_table" (논리 게이트)
```html
<section>
  <div class="chapter-tag">논리 게이트</div>
  <h2>{{게이트명}} — 진리표</h2>
  <div class="two-col">
    <div id="{{visual_id}}" style="height: 460px; overflow: hidden;"></div>
    <div>
      <table class="truth-table" id="{{table_id}}">
        <thead>
          <tr><th>\(x_1\)</th><th>\(x_2\)</th><th>가중합 \(z\)</th><th>출력 \(y\)</th></tr>
        </thead>
        <tbody>
          <tr><td class="val-0">0</td><td class="val-0">0</td>
              <td class="fillable">?</td><td class="fillable">?</td></tr>
          <tr><td class="val-0">0</td><td class="val-1">1</td>
              <td class="fillable">?</td><td class="fillable">?</td></tr>
          <tr><td class="val-1">1</td><td class="val-0">0</td>
              <td class="fillable">?</td><td class="fillable">?</td></tr>
          <tr><td class="val-1">1</td><td class="val-1">1</td>
              <td class="fillable">?</td><td class="fillable">?</td></tr>
        </tbody>
      </table>
      <p><span class="kw">파라미터</span> \(w_1={{w1}}, w_2={{w2}}, b={{bias}}\)</p>
    </div>
  </div>
  <div class="anim-controls">
    <button class="anim-btn" onclick="truthTable_{{table_id}}.fillAll({{w1}}, {{w2}}, {{bias}})">
      표 채우기 ▶
    </button>
    <button class="anim-btn reset-btn" onclick="location.reload()">↺</button>
  </div>
</section>
```

### type: "code_slide"
```html
<section>
  <div class="chapter-tag">Code · {{language}}</div>
  <h2>{{코드 제목}}</h2>
  <pre class="code-block" data-language="python" data-highlight-lines="2,4-6"><code><span class="line"><span class="kw">import</span> <span class="var">numpy</span> <span class="kw">as</span> <span class="var">np</span></span><span class="line"></span><span class="line"><span class="kw">def</span> <span class="fn">cosine_similarity</span>(<span class="var">p</span>, <span class="var">q</span>):</span><span class="line">    <span class="var">dot</span> <span class="op">=</span> <span class="fn">np.dot</span>(<span class="var">p</span>, <span class="var">q</span>)</span><span class="line">    <span class="kw">return</span> <span class="var">dot</span> <span class="op">/</span> (<span class="fn">np.linalg.norm</span>(<span class="var">p</span>) <span class="op">*</span> <span class="fn">np.linalg.norm</span>(<span class="var">q</span>))</span></code></pre>
  <p class="fragment"><span class="kw">핵심</span> {{코드 설명}}</p>
</section>
```

**코드블록 규칙**
- 최대 12줄
- 강조할 줄은 `data-highlight-lines` (예: `"2,4-6"`)
- 신택스 클래스: `kw`, `fn`, `str`, `cmt`, `var`, `op`, `tag`, `attr`, `val`

### type: "concept_cards"
```html
<section>
  <div class="chapter-tag">Concept cards</div>
  <h2>{{섹션 제목}}</h2>
  <div class="three-col">
    <div class="concept-card fragment">
      <div class="icon">△</div>
      <h4>{{카드1 제목}}</h4>
      <p>{{설명 — 20자 이내}}</p>
    </div>
    <div class="concept-card fragment">
      <div class="icon">∠</div>
      <h4>{{카드2 제목}}</h4>
      <p>{{설명}}</p>
    </div>
    <div class="concept-card fragment">
      <div class="icon">∩</div>
      <h4>{{카드3 제목}}</h4>
      <p>{{설명}}</p>
    </div>
  </div>
</section>
```

**아이콘 규칙**
- 이모지보다 CSS shape 또는 유니코드 기호 선호 (예: `△`, `∠`, `∩`, `○`, `■`)
- 이모지 사용 시에도 단일 문자로 최소화 (📐, 📊 등 수학·과학 관련만)

### type: "semantic_boxes" (경고·결론·참고)
```html
<section>
  <div class="chapter-tag">Key points</div>
  <h2>{{섹션 제목}}</h2>

  <div class="warning-box">
    <span class="kw-danger">핵심</span> 경고·함정 내용
  </div>

  <div class="result-box">
    <span class="kw-success">결론</span> 요약 결론
  </div>

  <div class="info-box">
    <span class="kw-info">참고</span> 추가 정보
  </div>
</section>
```

### type: "comparison"
```html
<section>
  <div class="chapter-tag">비교</div>
  <h2>{{A}} vs {{B}}</h2>
  <div class="two-col">
    <div class="card card-accent" style="border-color: var(--lm-danger);">
      <h4 style="color: var(--lm-danger);">{{A}}</h4>
      <ul>
        <li>{{A 특성 1}}</li>
        <li>{{A 특성 2}}</li>
      </ul>
    </div>
    <div class="card card-accent" style="border-color: var(--lm-success);">
      <h4 style="color: var(--lm-success);">{{B}}</h4>
      <ul>
        <li>{{B 특성 1}}</li>
        <li>{{B 특성 2}}</li>
      </ul>
    </div>
  </div>
  <div class="warning-box">
    <span class="kw-danger">주의</span> {{두 개념을 혼동하기 쉬운 지점}}
  </div>
</section>
```

### type: "quiz"
```html
<section>
  <div class="chapter-tag">확인 문제</div>
  <h2>{{질문 주제}}</h2>
  <div class="card">
    <p><strong>Q.</strong> {{문제}}</p>
    <div class="fragment" style="margin-top: var(--lm-space-5); padding-top: var(--lm-space-4); border-top: 1px solid var(--lm-rule);">
      <p><span class="kw-success">A.</span> {{답}}</p>
      <p style="color: var(--lm-ink-3); font-size: var(--lm-slide-small);">{{해설}}</p>
    </div>
  </div>
</section>
```

### type: "summary"
```html
<section>
  <div class="chapter-tag">Wrap up</div>
  <h2>오늘 배운 내용</h2>
  <div class="three-col">
    <div class="concept-card fragment">
      <div class="icon">◆</div>
      <h4>{{핵심1}}</h4>
      <p>{{설명1 — 20자 이내}}</p>
    </div>
    <div class="concept-card fragment">
      <div class="icon">◈</div>
      <h4>{{핵심2}}</h4>
      <p>{{설명2}}</p>
    </div>
    <div class="concept-card fragment">
      <div class="icon">◇</div>
      <h4>{{핵심3}}</h4>
      <p>{{설명3}}</p>
    </div>
  </div>
  <p class="fragment">
    <span class="chip chip-info">다음 시간</span> {{다음 주제}}
  </p>
</section>
```

---

## 슬라이드 높이 예산 (MANDATORY · 1920×1080 기준)

실제 사용 가능한 내부 영역은 약 1920×960 (상하 패딩 72px 제외).
타입별 예산을 넘으면 반드시 슬라이드를 2장으로 분할한다.

| 타입 | 예상 높이 | 비고 |
|------|----------|------|
| title | 500~600px | title-slide는 여백이 많음 |
| objectives | 600~750px | 항목 4개까지 여유 |
| definition_formula | 650~800px | two-col + example-box 포함 |
| numeric_example | 700~850px | step-box 전개 고려해 여유 |
| truth_table | 700~800px | 다이어그램 460px + 표 + controls |
| concept_cards (3열) | 500~650px | 카드당 ~280px |
| comparison | 700~850px | 리스트 5항목 이내 |
| semantic_boxes | 500~600px | 3개 박스 |
| code_slide | 550~750px | 최대 12줄 기준 |
| quiz | 500~650px | 답변 fragment 포함 |
| summary | 600~700px | 3열 + 다음 주제 |

---

## 오버플로우 방지

1. **step-box**: 슬라이드당 최대 3개 — 더 필요하면 수직 서브슬라이드(`<section><section>...</section></section>`)로 분리
2. **two-col 내부 높이**: 각 컬럼 720px 이내
3. **시각화 placeholder**: 반드시 `max-height` 지정
   - Chart: `style="max-height: 500px;"`
   - SVG 다이어그램: `style="height: 460px; overflow: hidden;"`
4. **자동 분리 판단**: `h2 + two-col + visual + anim-controls + warning-box` 5개 모두 있으면 2장 분리 검토
5. **폰트 크기 조정 금지**: `font-size` 오버라이드로 내용을 욱여넣지 말 것. 넘치면 슬라이드를 쪼갠다

---

## 권장 슬라이드 구성 (인공지능수학 기준, 15~20장)

1. 제목 (title)
2. 학습 목표 (objectives)
3. 실생활 연결 (concept_cards · 2~3열)
4~5. 선수학습 복습 (numeric_example 또는 definition_formula)
6~8. 핵심 개념 전개 (numeric_example + truth_table / code_slide)
9~11. 예제 풀이 (numeric_example 반복 · 다른 수치)
12. 개념 비교 (comparison)
13. 오개념 정리 (semantic_boxes · warning-box 중심)
14. 학생 실습 · 탐구 (interactive_demo 또는 quiz)
15. 요약 (summary)
16. 형성평가 (quiz 2~3문항)

---

## 출력

`schemas/slide_structure.json` 스키마를 따라 저장.

**ID 계약**
- `merged_context.json`의 `visual_requirements[].asset_id` → `visual_id`
- `animation_requirements[].animation_id` → `animation_id`
- `target_slide_id`도 `merged_context.json`에서 부여된 값과 일치
- 직접 새 ID 생성 금지

`has_animation`, `animation_id`, `has_visual`, `visual_id` 필드 정확히 기재.

---

## 품질 기준

- [ ] 캔버스 1920×1080 기준으로 설계
- [ ] 하드코딩 hex 색상 없음 · 모든 색은 `var(--lm-*)` 경유
- [ ] `<body data-subject="{subject_key}">` 속성 부여
- [ ] slide-system.css에 정의된 검증된 클래스만 사용
- [ ] 폐기된 클래스 (`.terminal-badge` 등) 사용 안 함
- [ ] 타입별 높이 예산 내 유지
- [ ] 폰트 크기 오버라이드로 욱여넣기 금지
- [ ] 수식 구분자 `\(...\)`, `\[...\]` (MathJax tex-chtml)
- [ ] 발표자 노트 `<aside class="notes">` 포함
