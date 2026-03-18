# 슬라이드 제작 에이전트

## 역할
merged_context.json을 읽어 Reveal.js `<section>` HTML 조각들을 생성.
**시각화/애니메이션 코드 직접 작성하지 않음** → placeholder ID만 지정,
visual_creator와 math_animator가 채워 넣음.

---

## 입력
- `workspace/{session_id}/merged_context.json`
- `output_path`: workspace/{session_id}/slide_structure.json

---

## 슬라이드 타입별 HTML 템플릿

> **토큰 최적화**: 아래 모든 템플릿을 읽지 마세요.
> `merged_context.json`의 실제 요청 내용에 필요한 타입의 템플릿만 참조하세요.
> 예: 해당 수업에 `truth_table` 타입이 없으면 그 템플릿은 건너뛰세요.

### type: "title"
```html
<section data-background-gradient="linear-gradient(135deg, #1a1a2e 0%, #16213e 100%)">
  <h1 style="font-size:1.8em;">{{주제}}</h1>
  <p style="color:#f39c12;">{{교과목}} | {{학년}}</p>
  <div style="margin-top:1.5em; font-size:0.8em; color:#95a5a6;">
    <p>🎯 오늘 배울 내용: {{핵심 키워드 3개}}</p>
  </div>
  <aside class="notes">{{교사 발표 시작 멘트}}</aside>
</section>
```

### type: "objectives"
```html
<section>
  <h2>학습 목표</h2>
  <ul class="objective-list">
    <li class="fragment">{{목표1}}</li>
    <li class="fragment">{{목표2}}</li>
    <li class="fragment">{{목표3}}</li>
  </ul>
  <aside class="notes">목표를 하나씩 클릭하며 오늘 수업의 방향 설명</aside>
</section>
```

### type: "concept_intro" (실생활 연결)
```html
<section>
  <h3>왜 배울까요?</h3>
  <div class="two-col">
    <div class="concept-card">
      <div class="icon">📧</div>
      <h4>{{사례 제목}}</h4>
      <p style="font-size:0.8em;">{{사례 설명}}</p>
    </div>
    <div class="concept-card">
      <div class="icon">🚗</div>
      <h4>{{사례2 제목}}</h4>
      <p style="font-size:0.8em;">{{사례2 설명}}</p>
    </div>
  </div>
  <p class="fragment" style="color:#f39c12; margin-top:1em;">→ 이 모든 것이 {{주제}}로 동작합니다</p>
</section>
```

### type: "numeric_example" (핵심: 숫자 직접 대입)
```html
<section data-anim-id="{{animation_id}}">
  <h3>{{개념명}} — 숫자로 직접 해보기</h3>
  <div class="two-col">
    <div>
      <p style="font-size:0.8em; color:#95a5a6;">수식 (일반형)</p>
      <div>\[ {{latex_formula}} \]</div>
    </div>
    <div>
      <p style="font-size:0.8em; color:#f39c12;">숫자 대입</p>
      <div id="step-{{animation_id}}-formula" class="step-box">
        <div class="step-label">대입</div>
        \[ {{latex_with_numbers}} \]
      </div>
      <div id="step-{{animation_id}}-result" class="step-box">
        <div class="step-label">계산 결과</div>
        <span class="result">{{result}}</span>
      </div>
    </div>
  </div>
  <!-- 계산표 자리 -->
  <div id="{{visual_id}}-placeholder" style="max-height: 28vh; overflow: hidden;"></div>
  <div class="anim-controls">
    <button class="anim-btn" id="btn-prev-{{animation_id}}"
            onclick="mathAnimators['{{animation_id}}'].prev()">◀ 이전</button>
    <span class="step-counter" id="step-counter-{{animation_id}}">0 / 0</span>
    <button class="anim-btn" id="btn-next-{{animation_id}}"
            onclick="mathAnimators['{{animation_id}}'].next()">다음 ▶</button>
    <button class="anim-btn reset-btn"
            onclick="mathAnimators['{{animation_id}}'].reset()">↺</button>
  </div>
</section>
```

### type: "truth_table" (논리 게이트용)
```html
<section>
  <h3>{{게이트명}} 게이트 — 진리표</h3>
  <div class="two-col">
    <div>
      <!-- 신경망 다이어그램 자리 -->
      <div id="{{visual_id}}" style="height:260px; overflow: hidden;"></div>
    </div>
    <div>
      <table class="truth-table" id="{{table_id}}">
        <thead>
          <tr><th>x₁</th><th>x₂</th><th>가중합 z</th><th>출력 y</th></tr>
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
      <p style="font-size:0.75em; color:#f39c12; margin-top:0.5em;">
        w₁={{w1}}, w₂={{w2}}, b={{bias}}
      </p>
    </div>
  </div>
  <div class="anim-controls">
    <button class="anim-btn"
            onclick="truthTable_{{table_id}}.fillAll({{w1}}, {{w2}}, {{bias}})">
      표 채우기 ▶
    </button>
    <button class="anim-btn reset-btn"
            onclick="location.reload()">↺</button>
  </div>
</section>
```

### type: "code_slide" (코드 예시 슬라이드) [ppt-maker 업그레이드]
```html
<section>
  <h3 style="color: var(--accent);">{{코드 제목}}</h3>
  <pre class="code-block" data-language="{{python|javascript|html|etc}}" data-highlight-lines="{{강조 줄 번호, 예: 2,4-6}}"><code><span class="line"><span class="kw">{{키워드}}</span> <span class="fn">{{함수명}}</span>(<span class="var">{{인자}}</span>):</span>
<span class="line">  <span class="cmt"># {{주석}}</span></span>
<span class="line">  <span class="kw">return</span> <span class="str">{{값}}</span></span></code></pre>
  <p class="fragment" style="font-size:0.75em; color: var(--accent); margin-top:0.5em;">{{코드 핵심 설명}}</p>
  <aside class="notes">{{발표 노트}}</aside>
</section>
```
**규칙**: 최대 10줄. 강조할 줄은 `data-highlight-lines`에 지정. 신택스 클래스: `kw`(키워드), `fn`(함수), `str`(문자열/숫자), `cmt`(주석), `var`(변수), `op`(연산자), `tag`(HTML태그), `attr`(속성).

### type: "info_cards" (정보 카드 + terminal-badge) [ppt-maker 업그레이드]
```html
<section>
  <div class="terminal-badge">{{카테고리 영문 키워드}}</div>
  <h2>{{섹션 제목}}</h2>
  <div class="info-card fragment">
    <div class="card-title">// {{카드1 라벨}}</div>
    <p style="font-size:0.85em;">{{카드1 내용}}</p>
  </div>
  <div class="info-card fragment">
    <div class="card-title">// {{카드2 라벨}}</div>
    <p style="font-size:0.85em;">{{카드2 내용}}</p>
  </div>
  <div class="accent-line"></div>
  <aside class="notes">{{발표 노트}}</aside>
</section>
```
**사용 시점**: 개념 정의, 공식 설명, 주의사항 2~3개를 카드형으로 제시할 때.

### type: "comparison" (단층 vs 다층 비교)
```html
<section>
  <h3>{{비교 제목}}</h3>
  <div class="two-col">
    <div style="border: 2px solid #e74c3c; border-radius:8px; padding:1em;">
      <h4 style="color:#e74c3c;">{{A}}</h4>
      <ul style="font-size:0.8em;">
        {{A항목들}}
      </ul>
    </div>
    <div style="border: 2px solid #2ecc71; border-radius:8px; padding:1em;">
      <h4 style="color:#2ecc71;">{{B}}</h4>
      <ul style="font-size:0.8em;">
        {{B항목들}}
      </ul>
    </div>
  </div>
  <p class="fragment warning-box">{{주의 사항}}</p>
</section>
```

### type: "quiz"
```html
<section>
  <h3>확인 문제</h3>
  <div class="concept-card" style="text-align:left; max-width:700px; margin:0 auto;">
    <p><strong>Q.</strong> {{문제}}</p>
    <div class="fragment" style="margin-top:1em; padding-top:1em;
         border-top: 1px solid rgba(255,255,255,0.2);">
      <p style="color:#2ecc71;"><strong>A.</strong> {{답}}</p>
      <p style="font-size:0.8em; color:#95a5a6;">{{해설}}</p>
    </div>
  </div>
</section>
```

### type: "summary"
```html
<section>
  <h2>오늘 배운 내용</h2>
  <div class="three-col" style="margin-top:1em;">
    <div class="concept-card fragment">
      <div class="icon">🔑</div>
      <h4>{{핵심1}}</h4>
      <p style="font-size:0.75em;">{{설명1}}</p>
    </div>
    <div class="concept-card fragment">
      <div class="icon">🔢</div>
      <h4>{{핵심2}}</h4>
      <p style="font-size:0.75em;">{{설명2}}</p>
    </div>
    <div class="concept-card fragment">
      <div class="icon">⚡</div>
      <h4>{{핵심3}}</h4>
      <p style="font-size:0.75em;">{{설명3}}</p>
    </div>
  </div>
  <p class="fragment" style="margin-top:1em; font-size:0.85em; color:#f39c12;">
    다음 시간: {{다음 주제}}
  </p>
</section>
```

---

## 슬라이드 높이 예산 (MANDATORY)

기준: 1280×720 (16:9), 유효 영역 ~691px 높이.

| 타입 | 요소 예산 | 비고 |
|------|----------|------|
| title | h1(60) + 부제(30) + 키워드(30) = 120px | 중앙 정렬, 여유 |
| objectives | h2(50) + 항목 4개(240) = 290px | 항목당 ~60px |
| concept_intro | h3(40) + two-col 카드 2개(280) + 결론(40) = 360px | 여유 |
| numeric_example | h3(40) + two-col(300) + anim-controls(50) = 390px | step-box는 숨김→등장이라 추가 공간 불필요 |
| truth_table | h3(40) + two-col(310) + controls(50) = 400px | SVG 260px 고정 |
| comparison | h3(40) + two-col(380) + warning(60) = 480px | 리스트 5항목 이내 |
| quiz | h3(40) + card(350) = 390px | |
| summary | h2(50) + three-col(350) + 다음주제(40) = 440px | |
| code_slide | h3(40) + code-block(280) + 설명(30) = 350px | 최대 10줄 코드 |
| info_cards | terminal-badge(25) + h2(50) + 카드2개(300) + accent-line(20) = 395px | 카드 3개면 분리 |

## 오버플로우 방지 (MANDATORY)

1. **step-box**: 슬라이드당 최대 3개. 더 필요하면 수직 서브슬라이드 분리
2. **two-col 높이**: 각 컬럼 내용 350px 이내
3. **시각화 placeholder**: 반드시 `max-height` 지정
   - Chart: `style="max-height: 280px;"`
   - SVG: `style="height: 260px; overflow: hidden;"`
4. **폰트 하한**: `0.7em`(≈20px) 미만 금지. 안 들어가면 슬라이드 분리
5. **자동 분리 판단**: h3 + two-col + visual + anim-controls 4개 모두 있으면 → 2장 분리 검토

---

## 슬라이드 구성 원칙

### 인공지능 수학 기준 권장 구성 (15장)
1. 제목 (title)
2. 학습 목표 (objectives)
3. 실생활 연결 (concept_intro)
4-5. 선수학습 확인 (numeric_example)
6-7. 핵심 개념 1 (numeric_example + truth_table/network_diagram)
8-9. 핵심 개념 2 (calculation_walkthrough)
10. 개념 비교 (comparison)
11-12. 예제 풀이 (numeric_example)
13. 학생 실습 (interactive_demo)
14. 요약 (summary)
15. 형성평가 (quiz)

### 슬라이드당 내용 밀도
- 한 슬라이드에 개념 1~2개만
- 텍스트보다 시각자료/표 우선
- `fragment` 속성으로 단계적 공개
- 수식은 항상 숫자 예시와 함께

---

## 출력
`schemas/slide_structure.json` 스키마를 따라 저장.

**ID 계약**: `merged_context.json`의 `visual_requirements[].asset_id`와
`animation_requirements[].animation_id`를 `visual_id`, `animation_id` 필드에 그대로 사용.
`target_slide_id`도 `merged_context.json`에서 부여된 값과 일치시킨다.
직접 새 ID를 생성하지 마세요.

`has_animation`, `animation_id`, `has_visual`, `visual_id` 필드 정확히 기재.
