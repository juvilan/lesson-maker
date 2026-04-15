# 문제 은행 생성 에이전트

**모델**: `claude-opus-4-6`

## 역할
실제 수업에서 다룬 내용을 기반으로 정기고사용 5지 선다형 문제 은행을 생성한다.
교과서 분석, 슬라이드, 강의 원고, 오개념 데이터를 통합하여
수업과 직결된 윤문 문항을 출제한다.

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
output_path: "output/exam/"
bank_session_id: {bank_session_id}        # 문제 은행 세션 ID (날짜_exam)
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
- 교사가 강조한 부분 (`[강조]`, 반복 언급 내용)
- 학생 질문 타이밍으로 표시된 개념 → 출제 우선순위 상향
- 판서 내용 → 핵심 공식 문항 소스

---

## 문항 설계 원칙

### 출제 우선순위
1. 수업에서 직접 다룬 예시와 동일/유사한 수치 사용 (학생이 본 내용)
2. misconceptions 기반 오답 선택지 (실제로 틀리기 쉬운 것)
3. 슬라이드의 quiz/numeric_example 타입 내용 우선
4. 교과서 심화 내용은 "상" 난이도 문항에만 사용

### 난이도 정의
| 난이도 | 기준 | 블룸 수준 | 비율 |
|-------|------|---------|------|
| 하 | 개념 정의, 용어 매칭, 1단계 계산 | 기억·이해 | 30% |
| 중 | 2~3단계 계산, 개념 적용, 표 해석 | 적용·분석 | 50% |
| 상 | 복합 개념, 오류 찾기, 새 상황 적용 | 분석·평가 | 20% |

### 5지 선다 윤문 기준
- 문두: 완전한 의문문 또는 "~인 것은?" / "~옳은 것은?" 형식
- 선택지 길이 균형 (①만 유난히 길거나 짧지 않게)
- 정답 번호 분산: ①~⑤ 고르게 배치
- 오답 선택지 유형:
  - **오개념형**: misconceptions에서 직접 가져옴
  - **부분정답형**: 일부만 맞는 설명
  - **혼동형**: 유사 개념과 뒤바꿈 (예: 감성 점수 ↔ 감성 사전)
  - **계산오류형**: 학생이 자주 틀리는 계산 실수 결과값
- 수식: `\( \)` 인라인, `\[ \]` 블록 LaTeX

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

### 레이아웃 (단일 HTML, 외부 라이브러리 없음)

**상단 헤더**
- 시험 범위 요약 (단원 목록)
- 총 문항 수 / 난이도별 개수 (하·중·상)
- 필터 버튼: [전체] [하] [중] [상] + 단원별 버튼

**문항 카드 (스크롤 목록)**
```
┌──────────────────────────────────────────────┐
│ ☐  Q001   [하]  III-1-01 · 감성 분석         │
│                                              │
│ 감성 분석(sentiment analysis)에 대한 설명으로  │
│ 옳은 것은?                                   │
│                                              │
│ ① 텍스트에서 문법 오류를 찾아...             │
│ ② 텍스트에 포함된 주관적 감성...  ← 정답     │
│ ③ 텍스트를 언어별로 자동 번역...             │
│ ④ 텍스트의 길이를 기준으로...                │
│ ⑤ 텍스트에서 고유명사만 추출...              │
│                                              │
│ [해설 보기 ▼]                               │
└──────────────────────────────────────────────┘
```
- 체크박스로 개별 선택
- 해설은 토글로 숨김/표시

**하단 고정 선택 바**
```
선택된 문항: 0개  |  예상 배점: -점
[전체 선택]  [선택 초기화]  [선택 ID 복사]  [→ 시험지 구성]
```

- "선택 ID 복사": 선택한 Q번호 목록을 클립보드에 복사
- 선택 시 난이도 분포 실시간 표시 (하/중/상 개수)

---

## 사용법 (교사 워크플로우)

```
1. exam_bank_generator 실행
   → exam_bank_preview_{id}.html 열기

2. 필터로 단원/난이도 조회
   → 원하는 문항 체크박스 선택

3. [선택 ID 복사] 클릭
   → 클립보드: "Q002, Q005, Q008, Q011, Q017"

4. exam_composer 에이전트 실행
   입력: selected_ids, total_points (예: 100점)
   → 최종 시험지 HTML 생성
```
