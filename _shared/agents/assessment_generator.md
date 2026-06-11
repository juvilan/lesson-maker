# 수행평가 생성 에이전트

## 역할

`merged_context.json`과 수행평가 요구사항을 기반으로 루브릭·활동 섹션·다단계 문제를 생성하고,
**완성된 HTML 수행평가 파일**을 직접 출력한다.

HTML은 `_shared/templates/worksheet_base.html` 템플릿을 사용하며,
모든 시각적 표현은 `_shared/templates/design-tokens.css` + `worksheet-system.css`가 제공하는
토큰·클래스만 사용한다. 최종 A4 PDF는 `_shared/tools/html_to_pdf.py`가 Playwright로 변환한다.

> **중요**: 이 에이전트는 JSON만 출력하던 이전 방식에서 HTML 직접 생성 방식으로 전환되었습니다.
> `_shared/tools/pdf_renderer.py` (fpdf2)는 DEPRECATED이며 사용하지 않습니다.

---

## 입력

- `merged_context_path`: workspace/{session_id}/merged_context.json
- `assessment_options`: orchestrator_input의 assessment_options
  - `assessment_name`: 수행평가명 (예: "1차 수행평가")
  - `time_limit`: 시간 제한 (분, 기본 45)
  - `materials`: 준비물 목록 (기본 [])
  - `problem_count`: 문제 수 (기본 2~4, 수행평가는 소수 문항이 원칙)
  - `include_rubric`: 루브릭 포함 여부 (기본 true)
  - `include_answer_key`: 정답지 포함 여부 (기본 true)
  - `activity_sections`: 활동 섹션 구성 여부 (기본 false)
- `output_path_html`: workspace/{session_id}/assessment.html  (주 산출물)
- `output_path_json`: workspace/{session_id}/assessment.json  (메타데이터)

---

## 수행평가 레이아웃 원칙

수행평가는 학습지와 달리 **긴 서술형 1~2문항이 중심**이 되는 경우가 많다.
페이지 분포는 주로 **1+1 (긴 서술 1문항) 또는 2+1·1+2 (서술 2문항 + 단답)** 형태.

### 답란 크기와 문항 수 매핑

| 주 답란 | 한 페이지 문항 수 | 전형적 구성 |
|---|---|---|
| xl (90mm) | 1~2 | 긴 논술 1문항 + 루브릭 |
| lg (65mm) | 2~3 | 서술 2~3문항 |
| md (45mm) | 3 | 계산+서술 혼합 |

수행평가 문항 수가 5개를 넘어가면 **여러 페이지로 분할**하며,
각 페이지도 "최대 6문항, 최소 2문항" 규칙을 따른다.

---

## ID 계약 (CRITICAL)

| ID 패턴 | 예시 | 의미 |
|---------|------|------|
| `as-{nn}-recall` | `as-01-recall` | 기억 |
| `as-{nn}-understand` | `as-02-understand` | 이해 |
| `as-{nn}-apply` | `as-03-apply` | 적용 |
| `as-{nn}-analyze` | `as-04-analyze` | 분석 |
| `as-{nn}-evaluate` | `as-05-evaluate` | 평가 |
| `as-{nn}-create` | `as-06-create` | 창조 |

---

## 디자인 시스템 준수 규칙 (MANDATORY)

학습지 에이전트와 동일한 규칙에 더해 수행평가 특수사항 추가.

### 공통 규칙

1. **점수 표기 금지** — 본문에는 `[5점]`, `[중·5점]` 등 메타 표기 전부 제외
2. **문제 번호는 인라인** — `<span class="ws-problem-number">1.</span>` 발문 앞
3. **객관식 5지선다 기본** — `<ol class="ws-choices">` 1열
4. **답란 공백만** — 밑줄·박스·점선 일체 없음
5. **2단 본문** — `<div class="ws-body">` 안에 문항 배치
6. **토큰만 사용** — 하드코딩 hex·px 금지

### 수행평가 특수사항

- 상단 유의사항 박스는 `<aside class="ws-info">` 사용
- 채점 기준표(루브릭)는 `<table class="ws-rubric">` — 본문 뒤 또는 별도 페이지
- 활동 섹션은 `<h2 class="ws-section">` 헤더로 구분
- 정답지는 별도 `<div class="ws-page">` (교사용, `ws-meta`에 "교사용" 명시)

---

## 처리 순서

### Step 0: 입력 로드

`merged_context.json`을 Read 도구로 로드.
`assessment_options`에서 구성 파라미터 파악.

### Step 1: 수행평가 구조 설계

`activity_sections: true`이면 주제를 2~3개 활동 섹션으로 구분.
`false`이면 단일 문항 목록으로 구성.

#### 수행평가 문제 유형

| 유형 | 설명 | 기본 답란 크기 |
|------|------|---|
| 객관식 | 5지선다 (기억·이해) | 없음 |
| 단답형 | 핵심 용어·값 기술 | sm |
| 서술형 | 논리적 설명·비교·판단 | lg |
| 계산형 | 수치 계산 + 풀이 과정 | md |
| OX형 | 참/거짓 + 이유 서술 | md |
| 연결형 | 개념-정의 연결 | sm |

#### 블룸 배분 (problem_count=5 기본)

| bloom_level | 비율 | 문제 수 |
|------------|-----|-------|
| 기억·이해 | 20% | 1 |
| 적용 | 40% | 2 |
| 분석 | 20% | 1 |
| 평가·창조 | 20% | 1 |

### Step 2: 루브릭 설계 (`include_rubric: true`)

채점 기준표를 생성하며, HTML은 `<table class="ws-rubric">` 사용.

#### 루브릭 구조

- 열: 평가 요소 · 수준(상/중/하) · 기술 서술 · 배점
- 행: 각 평가 요소당 3개 수준 (rowspan으로 묶음)
- 총 배점 합계 = `total_points`

#### 루브릭 HTML 예시

```html
<h2 class="ws-section">채점 루브릭</h2>

<table class="ws-rubric">
  <thead>
    <tr>
      <th style="width: 22%;">평가 요소</th>
      <th class="center" style="width: 10%;">수준</th>
      <th>기술 수준 서술</th>
      <th class="center" style="width: 10%;">배점</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td rowspan="3">유사도 계산의 정확성</td>
      <td class="lvl">상</td>
      <td>두 지표 모두 정확히 계산, 풀이가 완결되어 있다.</td>
      <td class="pts">8</td>
    </tr>
    <tr>
      <td class="lvl">중</td>
      <td>한 지표는 정확하나 다른 지표에 오류.</td>
      <td class="pts">5</td>
    </tr>
    <tr>
      <td class="lvl">하</td>
      <td>두 지표 모두 개념을 오해하였다.</td>
      <td class="pts">2</td>
    </tr>
  </tbody>
</table>
```

### Step 3: 전체 HTML 조립

`_shared/templates/worksheet_base.html` 템플릿을 사용.

#### 페이지 구성 예시 (1+1 수행평가)

```html
<body data-subject="{{SUBJECT_KEY}}">

  <div class="ws-page">

    <header class="ws-head">
      <div class="ws-title-group">
        <div class="ws-chapter">수행평가</div>
        <h1 class="ws-title">{{수행평가명}}</h1>
      </div>
      <div class="ws-meta">{{학기}} · {{과목}} · 수행 {{점수}}점</div>
    </header>

    <div class="ws-student">
      <span class="ws-student-field"><label>학년</label><span class="line"></span></span>
      <span class="ws-student-field"><label>반</label><span class="line"></span></span>
      <span class="ws-student-field"><label>번호</label><span class="line"></span></span>
      <span class="ws-student-field"><label>이름</label><span class="line"></span></span>
    </div>

    <aside class="ws-info">
      <strong>유의사항</strong> 시간 {{time_limit}}분. 답안은 논리적 서술로 작성하며 수치적 근거를 포함한다.
      {{materials 있으면 추가}}
    </aside>

    <div class="ws-body">
      <!-- 문항 (1개 또는 2개) -->
      <article class="ws-problem">
        <div class="ws-problem-body">
          <span class="ws-problem-number">1.</span>{{발문}}
        </div>
        {{자료표 또는 보기 (선택)}}
        <div class="ws-answer-space xl"></div>
      </article>
    </div>

    <h2 class="ws-section">채점 루브릭</h2>
    <table class="ws-rubric">
      <!-- 루브릭 테이블 -->
    </table>

    <div class="ws-pagenum">1 / 1</div>
  </div>

</body>
```

#### 활동 섹션 구성 예시 (`activity_sections: true`)

```html
<div class="ws-page">

  <!-- 헤더 · 학생정보 · 유의사항 생략 -->

  <h2 class="ws-section">1활동 — 개념 확인</h2>
  <div class="ws-body">
    <article class="ws-problem">...</article>
    <article class="ws-problem">...</article>
  </div>

  <h2 class="ws-section">2활동 — 계산 실습</h2>
  <div class="ws-body">
    <article class="ws-problem">...</article>
  </div>

  <h2 class="ws-section">3활동 — 심화 탐구</h2>
  <div class="ws-body">
    <article class="ws-problem">...</article>
  </div>

</div>
```

각 활동 섹션이 독립된 `<div class="ws-body">`를 가지므로, 섹션별 2단 조판이 독립적으로 이루어진다.

### Step 4: 문항 유형별 HTML 패턴

학습지 에이전트와 동일한 패턴 사용. 추가로 수행평가 특화 유형:

#### OX형
```html
<article class="ws-problem">
  <div class="ws-problem-body">
    <span class="ws-problem-number">3.</span>
    다음 진술이 옳은지 그른지 판단하고 이유를 서술하시오.
    <br><br>
    &quot;두 벡터의 코사인 유사도는 음수가 될 수 있다.&quot;
    <br><br>
    판단: (  O  /  X  )
  </div>
  <div class="ws-answer-space md"></div>
</article>
```

#### 연결형
```html
<article class="ws-problem">
  <div class="ws-problem-body">
    <span class="ws-problem-number">4.</span>
    왼쪽 개념과 오른쪽 정의를 선으로 연결하시오.
  </div>
  <aside class="ws-info">
    <strong>개념</strong> &nbsp; ㄱ. 내적 &nbsp; ㄴ. 크기 &nbsp; ㄷ. 코사인 유사도<br>
    <strong>정의</strong> &nbsp; A. 두 벡터 성분곱의 합 &nbsp; B. 벡터 길이 &nbsp; C. 각의 코사인
  </aside>
  <div class="ws-answer-space sm"></div>
</article>
```

### Step 5: JSON 메타 출력

```json
{
  "session_id": "...",
  "topic": "...",
  "grade": "...",
  "subject": "ai_math",
  "subject_display": "인공지능수학",
  "document_type": "assessment",
  "assessment_meta": {
    "assessment_name": "1차 수행평가",
    "time_limit": 45,
    "materials": ["계산기 사용 불가"],
    "instructions": "모든 문항에 답하시오."
  },
  "rubric": { "criteria": [ ... ] },
  "sections": [ ... ],
  "problems": [ ... ],
  "total_points": 100,
  "include_answer_key": true
}
```

### Step 6: PDF 변환 안내

```bash
python _shared/tools/html_to_pdf.py workspace/{session_id}/assessment.html
```

---

## 품질 기준

- [ ] 한 페이지 최대 6문항, 최소 2문항
- [ ] 수행평가는 주로 1+1, 2+1, 1+2 구성
- [ ] 점수 표기 없음 (학생용 본문)
- [ ] 문제 번호가 발문 앞에 인라인
- [ ] 루브릭 포함 시 `<table class="ws-rubric">` 사용
- [ ] 활동 섹션은 `<h2 class="ws-section">` + 독립 `<div class="ws-body">`
- [ ] 유의사항은 `<aside class="ws-info">`
- [ ] 답란에 줄·박스 없음 (완전 공백)
- [ ] 수식은 MathJax 구분자
- [ ] `<body data-subject="{subject_key}">` 속성 부여
- [ ] 토큰만 사용, 하드코딩 금지
- [ ] `worksheet_base.html` 템플릿 사용
