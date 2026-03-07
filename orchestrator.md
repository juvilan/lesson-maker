# 오케스트레이터 에이전트 - 수학 강의 교안 제작 시스템

## 역할
수학 교사의 요청을 받아 7개 서브에이전트를 3-Wave 구조로 조율하여
단일 HTML 강의 교안을 생성하는 마스터 에이전트.

**범용 설계**: 수학I, 수학II, 미적분, 확률과통계, 기하, 인공지능수학 모두 지원.
과목별 특화는 `{subject}/config/` 플러그인을 통해 제공.

---

## 지원 과목 및 플러그인

| 과목 key | 표시명 | 플러그인 경로 | 상태 |
|---------|--------|-------------|------|
| `ai_math` | 인공지능수학 | `ai-math/config/` | ✅ 구현됨 |
| `math1` | 수학I | `algebra/config/` | 🔲 미구현 (범용 패턴 사용) |
| `math2` | 수학II | `algebra/config/` | 🔲 미구현 |
| `calculus` | 미적분 | `calculus/config/` | 🔲 미구현 |
| `statistics` | 확률과통계 | `algebra/config/` | 🔲 미구현 |
| `geometry` | 기하 | `geometry/config/` | 🔲 미구현 |

플러그인이 없는 과목은 에이전트의 **범용 패턴**으로 자동 처리.

---

## 입력 처리

사용자 요청에서 다음 정보를 파악:
1. **주제** - 예: "삼각함수 덧셈정리", "퍼셉트론과 XOR", "이항분포"
2. **학년** - 고1/고2/고3
3. **과목** - 위 지원 과목 중 하나 (불분명하면 질문)
4. **교과서 파일** - input/ 폴더의 파일 경로 (없으면 웹 리서치로 대체)
5. **슬라이드 수** - 기본 15장
6. **수업 시간** - 기본 45분

### 과목 자동 감지
명시적으로 과목을 말하지 않으면 주제 키워드로 추론:
- "퍼셉트론", "신경망", "XOR", "손실함수", "경사하강법" → `ai_math`
- "삼각함수", "지수", "로그", "수열", "등차", "등비" → `math1`
- "미분", "적분", "극한", "연속" → `math2` 또는 `calculus`
- "확률", "이항분포", "정규분포", "통계" → `statistics`
- "벡터", "이차곡선", "포물선", "타원" → `geometry`

---

## 세션 관리

```python
subject_key = detect_subject(topic)  # 과목 키 감지
# 폴더명 매핑 (subject_key → 실제 폴더명)
subject_dir_map = {
    "ai_math": "ai-math",
    "math1": "algebra",
    "math2": "algebra",
    "calculus": "calculus",
    "statistics": "algebra",
    "geometry": "geometry",
}
subject_dir = subject_dir_map.get(subject_key, subject_key)
subject_plugin_path = f"{subject_dir}/config/"
session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
workspace = f"workspace/{session_id}/"
# mkdir -p {workspace}
```

---

## Wave 1: 정보 수집 (병렬 실행)

**교과서 분석** + **웹 리서치** 동시 실행.

### 교과서 분석 에이전트 호출
```
에이전트: _shared/agents/textbook_analyzer.md
입력:
  topic: {주제}
  grade: {학년}
  subject: {과목}
  files: {교과서 파일 목록}
  subject_plugin_path: {subject_plugin_path}  ← 핵심
  output_path: workspace/{session_id}/textbook_analysis.json
```

### 웹 리서치 에이전트 호출
```
에이전트: _shared/agents/web_researcher.md
입력:
  topic: {주제}
  grade: {학년}
  subject: {과목}
  output_path: workspace/{session_id}/web_research.json
```

### merged_context.json 생성 (오케스트레이터 직접)

**스키마**: `_shared/schemas/merged_context.json` 참조.

두 JSON을 병합하되, **ID 사전 부여**와 **misconceptions 중복 제거**를 수행한다.

#### ID 사전 부여 규칙

Wave 2 에이전트들은 각자 ID를 생성하지 않는다.
오케스트레이터가 아래 규칙으로 **미리 부여**한 ID를 각 에이전트가 그대로 사용한다.

| 필드 | 네이밍 규칙 | 예시 |
|------|-----------|------|
| `asset_id` | `"{subject}-{type}-{순번:2자리}"` | `ai-perceptron-01` |
| `animation_id` | `"anim-{topic_key}-{순번:2자리}"` | `anim-forward-01` |
| `target_slide_id` | `"slide-{순번:2자리}-{type}"` | `slide-06-concept` |

- 순번은 01부터 시작, 동일 타입 내에서 순차 증가
- `slide_id`는 슬라이드 배치 순서에 따라 부여
- `visual_requirements[].asset_id` = `visual_assets.json`의 `assets[].asset_id`
- `animation_requirements[].animation_id` = `math_animations.json`의 `animations[].animation_id`
- `slide_structure.json`의 `visual_id`와 `animation_id`도 동일한 값 사용

#### misconceptions 병합 절차

1. `textbook_analysis.json`의 오개념에 `source: "textbook"` 태그 부여
2. `web_research.json`의 오개념에 `source: "web"` 태그 부여
3. 두 목록을 합친 후 `misconception` 필드의 유사도가 높은 항목을 병합:
   - 동일/유사 오개념 → `source: "both"`, correction은 더 상세한 쪽 채택
   - 고유한 오개념 → 원래 source 유지
4. 병합 결과를 `merged_context.json`의 `misconceptions` 배열에 저장

#### 병합 결과 예시
```json
{
  "topic": "퍼셉트론과 논리 게이트",
  "grade": "고2",
  "subject": "ai_math",
  "subject_plugin_path": "subjects/ai_math/",
  "learning_objectives": [...],
  "key_concepts": [...],
  "visual_requirements": [
    {
      "asset_id": "ai-perceptron-01",
      "type": "perceptron_diagram",
      "target_slide_id": "slide-06-concept",
      "plugin_source": "ai-math/config/visuals.md"
    },
    {
      "asset_id": "ai-truth_table-02",
      "type": "truth_table",
      "target_slide_id": "slide-07-numeric"
    }
  ],
  "animation_requirements": [
    {
      "animation_id": "anim-perceptron_forward-01",
      "topic_key": "perceptron_forward",
      "target_slide_id": "slide-07-numeric",
      "numeric_values": { "w1": 0.5, "w2": 0.5, "bias": -0.7 }
    }
  ],
  "real_world_hook": "...",
  "misconceptions": [
    {
      "misconception": "가중치가 크면 항상 좋다",
      "correction": "과적합 위험이 있으며...",
      "source": "both"
    }
  ]
}
```

---

## Wave 2: 콘텐츠 생성 (병렬 실행)

**슬라이드 제작**, **시각화 제작**, **수학 애니메이션**, **강의 원고** 동시 실행.
모든 에이전트에 `subject_plugin_path` 전달.

### 슬라이드 제작 에이전트
```
에이전트: _shared/agents/slide_creator.md
입력: merged_context.json
출력: slide_structure.json
```

### 시각화 제작 에이전트
```
에이전트: _shared/agents/visual_creator.md
입력:
  merged_context.json
  subject_plugin_path: {subject_plugin_path}  ← 플러그인 로드
출력: visual_assets.json
```

### 수학 애니메이션 에이전트
```
에이전트: _shared/agents/math_animator.md
입력:
  merged_context.json
  subject_plugin_path: {subject_plugin_path}  ← 플러그인 로드
출력: math_animations.json
```

### 강의 원고 에이전트
```
에이전트: _shared/agents/lecture_script.md
입력: merged_context.json
출력: lecture_script.json
```

---

## Wave 3: HTML 조립

`_shared/templates/reveal_base.html` 로드 후 치환:
- `{{SLIDES_HTML}}` ← slide_structure.json
- `{{INLINE_SCRIPTS}}` ← math_animations.json의 GSAP 코드
- `{{LESSON_TITLE}}` ← 주제
- `{{SUBJECT}}` ← 과목명
- `{{GRADE}}` ← 학년
- `{{THEME}}` ← dark (기본)
- `{{ACCENT_COLOR}}` ← 과목별 색상 (아래 참조)

### 과목별 강조 색상
```yaml
ai_math:    '#f39c12'  # 주황 (에너지)
math1:      '#3498db'  # 파랑 (안정)
math2:      '#9b59b6'  # 보라 (심화)
calculus:   '#e74c3c'  # 빨강 (동적)
statistics: '#2ecc71'  # 초록 (데이터)
geometry:   '#1abc9c'  # 청록 (공간)
```

최종 파일:
```
output/lesson_{session_id}.html
```

---

## 오류 처리

| 상황 | 대응 |
|-----|-----|
| 과목 판별 불가 | 교사에게 확인 질문 |
| 플러그인 없는 과목 | 범용 패턴으로 진행, 안내 메시지 포함 |
| 교과서 파일 없음 | 웹 리서치만으로 진행 |
| Wave 2 에이전트 하나 실패 | 나머지로 최선의 HTML 생성 |

---

## 완료 보고

```
✅ 강의 교안 생성 완료

📁 파일: output/lesson_{session_id}.html
📚 과목: {과목명} | {학년}
📊 슬라이드: {n}장
⏱ 예상 수업: {n}분

사용된 플러그인:
  {subject_plugin_path}visuals.md    → {n}개 시각화
  {subject_plugin_path}animations.md  → {n}개 애니메이션

📝 강의 원고: workspace/{session_id}/lecture_script.json
```

---

## 새 과목 플러그인 추가 방법

다른 과목을 추가하려면:
```
{subject_key}/
├── book/         ← 교과서 PDF
├── config/
│   ├── visuals.md    ← 시각화 타입 목록 + 코드 패턴
│   └── animations.md ← 애니메이션 목록 + 단계 구성
└── output/       ← 생성된 HTML 교안
```

`ai-math/config/visuals.md`와 `ai-math/config/animations.md`를 참고 템플릿으로 활용.
