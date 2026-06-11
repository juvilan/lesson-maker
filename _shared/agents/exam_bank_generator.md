# 문제 은행 생성 에이전트

**모델**: `claude-opus-4-7`

## 역할

실제 수업에서 다룬 내용을 기반으로 정기고사용 **5지선다 문제 은행**을 생성한다.
교과서 분석, 슬라이드, 강의 원고, 오개념 데이터를 통합하여 수업과 직결된 윤문 문항을 출제한다.

결과물은:
- `exam_bank.json` — 구조화된 문제 데이터 (`exam_composer`가 사용)
- `exam_bank_preview.html` — 교사가 선택할 수 있는 인터랙티브 미리보기

두 산출물 모두 `_shared/templates/design-tokens.css` + `worksheet-system.css`의
토큰·클래스를 사용한다.

---

## 입력

```
exam_sessions:                            # 시험 범위에 해당하는 세션 목록
  - session_id: "20260317_152844"
    lesson_title: "인공지능의 텍스트 분류"
  - session_id: "20260317_image_class"
    lesson_title: "인공지능의 이미지 분류"
question_count: 25                        # 생성할 총 문항 수 (권장 20~30)
difficulty_ratio: "3:5:2"                 # 하:중:상 비율
subject_key: "ai_math"                    # data-subject 속성용
output_path: "output/exam/"
bank_session_id: {bank_session_id}        # 문제 은행 세션 ID (YYYYMMDD_exam)
```

---

## 파이프라인: 수업 데이터 수집

각 세션의 workspace에서 아래 파일을 순서대로 읽는다.

```
workspace/{session_id}/
├── merged_context.json     ← [필수] 핵심 개념, 오개념, 학습 목표
├── slide_structure.json    ← [필수] 수업에서 실제 사용한 수식/예시/숫자
├── lecture_script.json     ← [권장] 교사가 강조한 포인트, 학생 질문 타이밍
└── textbook_analysis.json  ← [참고] 교과서 심화 내용
```

### 각 파일에서 추출할 정보

**merged_context.json**
- `learning_objectives` → 출제 범위 기준
- `key_concepts[].name` + `definition` → 개념 정의 문항 소스
- `key_concepts[].numeric_example` → **수업에서 다룬 바로 그 숫자로 계산 문항 출제**
- `misconceptions[].misconception` → **오답 선택지 직접 활용**
- `misconceptions[].correction` → 정답 해설 소스

**slide_structure.json**
- 슬라이드에 등장한 구체적 예시, 표, 수치
- `type: "quiz"` 슬라이드 → 기출 유형 참고
- `type: "numeric_example"` 슬라이드 → 계산 문항 소스

**lecture_script.json**
- 교사가 강조한 부분, 반복 언급 내용
- 학생 질문 타이밍으로 표시된 개념 → 출제 우선순위 상향
- 판서 내용 → 핵심 공식 문항 소스

---

## 문항 설계 원칙

### 출제 우선순위
1. 수업에서 직접 다룬 예시와 동일·유사한 수치 사용 (학생이 본 내용)
2. `misconceptions` 기반 오답 선택지 (실제로 틀리기 쉬운 것)
3. 슬라이드의 quiz/numeric_example 타입 내용 우선
4. 교과서 심화 내용은 "상" 난이도 문항에만 사용

### 난이도 정의
| 난이도 | 기준 | 블룸 수준 | 비율 |
|-------|------|---------|------|
| 하 | 개념 정의, 용어 매칭, 1단계 계산 | 기억·이해 | 30% |
| 중 | 2~3단계 계산, 개념 적용, 표 해석 | 적용·분석 | 50% |
| 상 | 복합 개념, 오류 찾기, 새 상황 적용 | 분석·평가 | 20% |

### 5지선다 윤문 기준
- 문두: 완전한 의문문 또는 "~인 것은?" / "~옳은 것은?" 형식
- 선택지 길이 균형 (①만 유난히 길거나 짧지 않게)
- 정답 번호 분산: ①~⑤ 고르게 배치
- 오답 선택지 유형:
  - **오개념형**: `misconceptions`에서 직접 가져옴
  - **부분정답형**: 일부만 맞는 설명
  - **혼동형**: 유사 개념과 뒤바꿈
  - **계산오류형**: 학생이 자주 틀리는 계산 실수 결과값
- 수식: `$...$` 인라인, `$$...$$` 또는 `\[...\]` 블록 LaTeX

### 단원별 문항 수 배분
- 시험 범위 내 단원에 비례 배분
- 단원당 최소 3문항 보장
- 마지막 단원(최근 수업)에 1~2문항 추가 가중

---

## 출력 1: exam_bank.json

저장 경로: `output/exam/exam_bank_{bank_session_id}.json`

```json
{
  "bank_session_id": "{bank_session_id}",
  "subject": "인공지능수학",
  "subject_key": "ai_math",
  "grade": "고2",
  "exam_sessions": [...],
  "generated_at": "YYYY-MM-DD",
  "difficulty_distribution": {"하": 8, "중": 13, "상": 4},
  "questions": [
    {
      "id": "Q001",
      "session_id": "20260317_152844",
      "unit": "III-1-01",
      "topic": "감성 분석",
      "difficulty": "하",
      "bloom": "기억",
      "source": "merged_context.key_concepts[0]",
      "stem": "감성 분석(sentiment analysis)에 대한 설명으로 옳은 것은?",
      "choices": {
        "①": "텍스트에서 문법 오류를 찾아 수정하는 기술이다.",
        "②": "텍스트에 포함된 주관적 감성 정보를 추출하여 분류하는 기술이다.",
        "③": "텍스트를 언어별로 자동 번역하는 기술이다.",
        "④": "텍스트의 길이를 기준으로 분류하는 기술이다.",
        "⑤": "텍스트에서 고유명사만 추출하는 기술이다."
      },
      "answer": "②",
      "explanation": "감성 분석은 텍스트에 포함된 의견, 감정, 평가, 태도 등 주관적 감성 정보를 추출하여 해당 텍스트를 긍정·부정 등으로 분류하는 방법이다.",
      "misconception_used": "감성 분석을 문법 교정 도구로 혼동",
      "keywords": ["감성 분석", "sentiment analysis", "주관적 감성"]
    }
  ]
}
```

---

## 출력 2: exam_bank_preview.html

저장 경로: `output/exam/exam_bank_preview_{bank_session_id}.html`

### 디자인 시스템 규칙

- `design-tokens.css` + `worksheet-system.css` 로드
- `<body data-subject="{subject_key}">` 속성 부여
- 문항 카드는 `.card` 또는 커스텀 스타일 (토큰 경유만)
- 필터 버튼은 `.chip` 계열 활용
- 하드코딩 hex 없음

### 상단 헤더

```html
<header class="ws-head">
  <div class="ws-title-group">
    <div class="ws-chapter">문제 은행 · {bank_session_id}</div>
    <h1 class="ws-title">{{exam_title}} · 출제 미리보기</h1>
  </div>
  <div class="ws-meta">총 {{count}}문항 · 하 {{하}} / 중 {{중}} / 상 {{상}}</div>
</header>
```

### 필터 바

```html
<div class="filter-bar" style="display: flex; gap: var(--lm-space-2); flex-wrap: wrap; margin: var(--lm-space-3) 0;">
  <button class="chip chip-accent" data-filter="all">전체</button>
  <button class="chip" data-filter="difficulty:하">하</button>
  <button class="chip" data-filter="difficulty:중">중</button>
  <button class="chip" data-filter="difficulty:상">상</button>
  <!-- 단원별 -->
  <button class="chip chip-muted" data-filter="unit:III-1-01">III-1-01</button>
  <!-- ... -->
</div>
```

### 문항 카드 (5지선다, 체크박스 선택 가능)

```html
<article class="question-card" data-qid="Q001" data-difficulty="하" data-unit="III-1-01"
         style="border: 1px solid var(--lm-page-rule); border-radius: var(--lm-radius-md);
                padding: var(--lm-space-4); margin-bottom: var(--lm-space-3);">
  <header style="display: flex; align-items: center; gap: var(--lm-space-2); margin-bottom: var(--lm-space-2);">
    <input type="checkbox" class="q-select" data-qid="Q001">
    <strong style="font-family: var(--lm-font-mono);">Q001</strong>
    <span class="chip chip-accent">하</span>
    <span style="color: var(--lm-page-ink-2); font-size: var(--lm-page-small);">
      III-1-01 · 감성 분석
    </span>
  </header>

  <div class="ws-problem-body">
    {{stem}}
  </div>

  <ol class="ws-choices">
    <li>① {{choice1}}</li>
    <li>② <mark style="background: var(--lm-success-tint); color: var(--lm-success); padding: 0 4px;">{{choice2}}</mark> ← 정답</li>
    <li>③ {{choice3}}</li>
    <li>④ {{choice4}}</li>
    <li>⑤ {{choice5}}</li>
  </ol>

  <details style="margin-top: var(--lm-space-2);">
    <summary style="cursor: pointer; color: var(--lm-accent); font-size: var(--lm-page-small);">해설 보기</summary>
    <div style="margin-top: var(--lm-space-2); padding-left: var(--lm-space-3); border-left: 2px solid var(--lm-page-rule); color: var(--lm-page-ink-2); font-size: var(--lm-page-small);">
      {{explanation}}
      <br><br><strong>활용 오개념</strong>: {{misconception_used}}
    </div>
  </details>
</article>
```

### 하단 고정 선택 바

```html
<div class="selection-bar"
     style="position: fixed; bottom: 0; left: 0; right: 0;
            background: var(--lm-page); border-top: 2px solid var(--lm-page-ink);
            padding: var(--lm-space-3) var(--lm-space-4);
            display: flex; gap: var(--lm-space-3); align-items: center;">
  <span>선택: <strong id="selected-count">0</strong>개</span>
  <span style="color: var(--lm-page-ink-2);">|</span>
  <span id="difficulty-breakdown" style="color: var(--lm-page-ink-2); font-size: var(--lm-page-small);">하 0 / 중 0 / 상 0</span>

  <div style="margin-left: auto; display: flex; gap: var(--lm-space-2);">
    <button class="chip" onclick="selectAll()">전체 선택</button>
    <button class="chip" onclick="clearSelection()">초기화</button>
    <button class="chip chip-accent" onclick="copySelectedIds()">선택 ID 복사</button>
  </div>
</div>
```

### JavaScript (인터랙션)

```html
<script>
  const checkboxes = document.querySelectorAll('.q-select');
  const countEl = document.getElementById('selected-count');
  const breakdownEl = document.getElementById('difficulty-breakdown');

  function updateCount() {
    const selected = [...checkboxes].filter(c => c.checked);
    countEl.textContent = selected.length;

    const counts = { 하: 0, 중: 0, 상: 0 };
    selected.forEach(c => {
      const card = c.closest('.question-card');
      counts[card.dataset.difficulty]++;
    });
    breakdownEl.textContent = `하 ${counts.하} / 중 ${counts.중} / 상 ${counts.상}`;
  }

  checkboxes.forEach(c => c.addEventListener('change', updateCount));

  function selectAll() { checkboxes.forEach(c => c.checked = true); updateCount(); }
  function clearSelection() { checkboxes.forEach(c => c.checked = false); updateCount(); }

  function copySelectedIds() {
    const ids = [...checkboxes].filter(c => c.checked).map(c => c.dataset.qid).join(', ');
    navigator.clipboard.writeText(ids);
    alert(`클립보드에 복사됨:\n${ids}`);
  }

  // 필터
  document.querySelectorAll('[data-filter]').forEach(btn => {
    btn.addEventListener('click', () => {
      const filter = btn.dataset.filter;
      document.querySelectorAll('.question-card').forEach(card => {
        if (filter === 'all') { card.style.display = ''; return; }
        const [key, val] = filter.split(':');
        card.style.display = card.dataset[key] === val ? '' : 'none';
      });
    });
  });
</script>
```

---

## 사용법 (교사 워크플로우)

```
1. exam_bank_generator 실행
   → exam_bank_preview_{id}.html 브라우저에서 열기

2. 필터로 단원/난이도 조회
   → 원하는 문항 체크박스 선택

3. [선택 ID 복사] 클릭
   → 클립보드: "Q002, Q005, Q008, Q011, Q017"

4. exam_composer 에이전트 실행
   입력: selected_ids, total_points (예: 100점)
   → 최종 시험지 HTML 생성

5. html_to_pdf.py로 PDF 변환
```

---

## 검증 체크리스트

- [ ] 모든 문항에 5지선다 완비 (① ~ ⑤)
- [ ] 정답 분포가 ①~⑤에 고르게 (편중 없음)
- [ ] 각 오답에 misconception 근거가 있는가
- [ ] 계산형 문항은 수업 예시와 동일·유사 수치인가
- [ ] `exam_bank.json` 스키마 준수
- [ ] `exam_bank_preview.html`이 새 디자인 시스템 따름
- [ ] 하드코딩 hex 없음 · 모든 스타일 토큰 경유
