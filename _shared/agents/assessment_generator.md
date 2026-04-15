# 수행평가 생성 에이전트

## 역할
`merged_context.json`과 수행평가 요구사항을 기반으로 루브릭·활동 섹션·다단계 문제를 생성하고,
`worksheet.json` 스키마(`document_type: "assessment"`)로 출력한다.
PDF 렌더링은 `_shared/tools/pdf_renderer.py`가 담당한다.

---

## 입력

- `merged_context_path`: workspace/{session_id}/merged_context.json
- `assessment_options`: orchestrator_input의 assessment_options
  - `assessment_name`: 수행평가명 (예: "1차 수행평가")
  - `time_limit`: 시간 제한 (분, 기본 45)
  - `materials`: 준비물 목록 (기본 [])
  - `problem_count`: 문제 수 (기본 5)
  - `include_rubric`: 루브릭 포함 여부 (기본 true)
  - `include_answer_key`: 정답지 포함 여부 (기본 true)
  - `activity_sections`: 활동 섹션 구성 여부 (기본 false)
- `output_path`: workspace/{session_id}/worksheet.json

---

## ID 계약 (CRITICAL)

`worksheet_requirements`의 `problem_id` 패턴을 수행평가용으로 조정한다.

| ID 패턴 | 예시 | 의미 |
|---------|------|------|
| `as-{nn}-recall` | `as-01-recall` | 기억 수준 |
| `as-{nn}-understand` | `as-02-understand` | 이해 수준 |
| `as-{nn}-apply` | `as-03-apply` | 적용 수준 |
| `as-{nn}-analyze` | `as-04-analyze` | 분석 수준 |
| `as-{nn}-evaluate` | `as-05-evaluate` | 평가 수준 |
| `as-{nn}-create` | `as-06-create` | 창조 수준 |

---

## 처리 순서

### Step 0: 입력 로드

`merged_context.json`을 Read 도구로 로드.
- `topic`, `grade`, `subject`, `learning_objectives`, `key_concepts` 파악
- `assessment_options`에서 구성 파라미터 파악

### Step 1: 수행평가 구조 설계

`activity_sections: true`이면 주제를 2~3개 활동 섹션으로 구분한다.
`activity_sections: false`이면 단일 문제 목록으로 구성한다.

#### 수행평가 문제 유형 (학습지 대비 확장)

| 유형 | 설명 |
|------|------|
| 객관식 | 5지선다 (기억·이해) |
| 단답형 | 핵심 용어/값 기술 |
| 서술형 | 논리적 설명·비교·판단 |
| 계산형 | 수치 계산 + 풀이 과정 |
| OX형 | 참/거짓 판별 + 이유 서술 |
| 진위표 | 조건별 참/거짓 표 완성 |
| 연결형 | 개념-정의 연결 |

#### 블룸 배분 (problem_count=5 기본)

| bloom_level | 비율 | 문제 수 |
|------------|-----|-------|
| 기억·이해 | 20% | 1 |
| 적용 | 40% | 2 |
| 분석 | 20% | 1 |
| 평가·창조 | 20% | 1 |

### Step 2: 루브릭 생성 (include_rubric: true)

채점 기준표를 `rubric.criteria` 배열로 생성:
- 각 기준: 평가 내용, 배점, 비고
- 총 배점 합계 = `total_points`

#### 루브릭 예시 (퍼셉트론 수행평가)
```json
{
  "criteria": [
    { "description": "퍼셉트론 개념 정확히 서술", "points": 20, "note": "입력·가중치·임계값 포함 시" },
    { "description": "AND 게이트 계산 과정 기술", "points": 30, "note": "3단계 이상" },
    { "description": "XOR 불가능 이유 논리적 설명", "points": 30, "note": "선형 분리 언급 필수" },
    { "description": "다층 퍼셉트론 해결 방안 제시", "points": 20, "note": "독창적 설명 가산점" }
  ]
}
```

### Step 3: 문제 생성

각 문제에 대해:
1. `source_concept`으로 `key_concepts`에서 관련 개념 탐색
2. `bloom_level`, `type`, `difficulty`에 맞는 문제 작성
3. `key_concepts`의 `numeric_example` 활용

#### 문제 생성 원칙
- **계산형**: 반드시 3단계 이상 `solution_steps` 포함
- **OX형**: 진술문 + `"answer": "O"` 또는 `"answer": "X"` + 이유 서술 칸
- **진위표**: 조건 목록 + 표 구조 → question에 표 Markdown으로 포함
- **연결형**: 좌열(개념)·우열(정의) → question에 두 목록 포함
- **LaTeX 수식**: 인라인 수식 `$...$` 형식

#### 인공지능수학 특화
- 퍼셉트론: w1=0.5, w2=0.5, bias=-0.7 사용
- 진리표: AND, OR, NAND, XOR 게이트 활용
- 계산 단계: 가중합 → 임계값 비교 → 출력 순서

### Step 4: sections 구성 (activity_sections: true)

활동 섹션은 주제를 논리 흐름으로 묶는다:
- Section 1 — 개념 확인 (기억·이해 문제)
- Section 2 — 계산 실습 (적용·분석 문제)
- Section 3 — 심화 탐구 (평가·창조 문제)

```json
{
  "sections": [
    {
      "title": "1활동 — 개념 확인",
      "instructions": "다음 물음에 답하시오.",
      "problems": [ ... ]
    }
  ]
}
```

### Step 5: JSON 출력

`_shared/schemas/worksheet.json` 스키마에 맞춰 출력:

```json
{
  "session_id": "...",
  "topic": "...",
  "grade": "...",
  "semester": "1학기",
  "subject": "ai_math",
  "subject_display": "인공지능수학",
  "output_format": "pdf",
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

`sections`를 사용할 경우 `problems`는 빈 배열 `[]`로 두어도 된다.
`pdf_renderer.py`는 `sections`가 있으면 sections를, 없으면 problems를 렌더링한다.

---

## 품질 기준
- `problem_id` 패턴: `as-NN-bloom_abbr`
- 계산형: `solution_steps` 3단계 이상
- 총 배점 합계 = 100점 (루브릭 기준)
- 모든 수식 `$...$` LaTeX 적용
- OX형/진위표/연결형: question 필드에 구조 명확히 기술
