# 인공지능 수학(2022) — 애니메이션 카탈로그 플러그인

math_animator.md 에이전트가 이 파일을 로드하여
인공지능 수학(2022 개정) 특화 단계별 애니메이션을 생성할 때 사용한다.

---

## 지원 애니메이션 목록

| 애니메이션 ID | 주제 | 단계 수 | 특징 |
|-------------|------|---------|------|
| `perceptron_forward` | 퍼셉트론 순전파 | 3~4단계 | 노드 활성화 + 계산표 |
| `truth_table_build` | 진리표 완성 | 행 수만큼 | 행별 계산 후 채우기 |
| `boundary_line_derive` | 경계선 수식 유도 | 4단계 | θ→y절편 연결 |
| `xor_set_explain` | XOR 집합으로 설명 | 4단계 | 대칭차집합 직관 |
| `xor_problem` | XOR 선형 분리 시도 | 3단계 | 실패 과정 시각화 |
| `xor_mlp_solve` | XOR = OR AND NAND | 4단계 | 층 쌓기 이유 설명 |
| `activation_role` | 활성화 함수 역할 변화 | 4단계 | 계단→sigmoid→ReLU |
| `mlp_forward` | 다층 퍼셉트론 순전파 | 4~6단계 | 레이어별 계산표 |
| `sigmoid_compute` | 시그모이드 계산 | 3단계 | e^-z 계산 과정 |
| `mse_compute` | MSE 손실 계산 | 3단계 | (y-ŷ)² 계산 |
| `gradient_step` | 경사하강법 1스텝 | 4단계 | dL/dw → w 업데이트 |
| `weight_update` | 역전파 가중치 업데이트 | 4단계 | 계산표 동반 |
| `data_classify_demo` | 데이터 분류 단계별 데모 | 4단계 | 정형/비정형 분류 ★ 신규 |
| `ml_training_loop` | 지도학습 훈련 루프 | 4단계 | 데이터→모델→예측→개선 ★ 신규 |
| `ai_era_transition` | AI 시대 전환 타임라인 | 5단계 | 시대별 등장 ★ 신규 |
| `bigdata_pipeline_step` | 빅데이터 파이프라인 단계 | 5단계 | 수집→평가 순차 ★ 신규 |

---

## 각 애니메이션 상세 패턴

### `perceptron_forward` — 퍼셉트론 순전파

**계산 단계**:
```
Step 1: 입력값 설정 (x₁=?, x₂=? 선택)
Step 2: 가중합 계산
  z = w₁x₁ + w₂x₂ + b
  → 숫자 대입: z = 0.5×1 + 0.5×1 + (-0.7) = 0.3
Step 3: 활성화 함수 적용
  z ≥ 0 → y = 1  또는  z < 0 → y = 0
(Step 4: 계산표의 해당 행 채우기)
```

**GSAP 요소 전환**:
- 노드 색: `#2c3e50` → `#f39c12` (활성화)
- 엣지 `stroke-dashoffset`: 110 → 0 (신호 흐름)
- 결과 노드: `#2c3e50` → `#2ecc71` (출력 1) / `#e74c3c` (출력 0)

---

### `truth_table_build` — 진리표 완성

각 행을 클릭으로 하나씩 완성.

**단계 구성**:
```
[클릭 1] (0,0) 행: z = -0.7 → y=0
[클릭 2] (0,1) 행: z = -0.2 → y=0
[클릭 3] (1,0) 행: z = -0.2 → y=0
[클릭 4] (1,1) 행: z =  0.3 → y=1
```

---

### `boundary_line_derive` — 경계선 수식 유도

**단계 구성**:
```
Step 1: 퍼셉트론 판단 조건
  w₁x₁ + w₂x₂ = θ (경계선)

Step 2: x₂에 대해 정리
  x₂ = -(w₁/w₂)·x₁ + θ/w₂
  기울기: -w₁/w₂  /  y절편: θ/w₂

Step 3: AND 게이트 예시 대입
  w₁=0.5, w₂=0.5, θ=0.7
  → x₂ = -x₁ + 1.4

Step 4: θ 변화 효과
  θ↑ → 경계선 위로 → 1 영역 좁아짐 (AND)
  θ↓ → 경계선 아래로 → 1 영역 넓어짐 (OR)
```

---

### `xor_set_explain` — XOR 집합으로 설명

**단계 구성**:
```
Step 1: OR = A ∪ B, AND = A ∩ B 제시
Step 2: XOR = A △ B = (A∪B) − (A∩B)
Step 3: 산점도 연결 — 1인 점이 두 덩어리
Step 4: 해결 방향 → 층 쌓기
```

---

### `xor_problem` — XOR 선형 분리 시도

**단계 구성**:
```
Step 1: XOR 진리표 & 산점도 표시
Step 2: 직선 분리 시도 → 모두 실패
Step 3: "선형 분리 불가" 결론 + 다층 퍼셉트론 필요성
```

---

### `xor_mlp_solve` — XOR = OR AND NAND

**단계 구성**:
```
Step 1: h₁ = OR(x₁, x₂), h₂ = NAND(x₁, x₂)
Step 2: NAND 설명 — NOT AND, 둘 다 1이면 0
Step 3: 진리표로 확인 — AND(OR, NAND) = XOR
Step 4: "복잡한 판단 = 단순한 판단들의 조합"
```

---

### `activation_role` — 활성화 함수 역할 변화

**단계 구성**:
```
Step 1: 계단함수 — 발화 여부만 판단, 미분 불가
Step 2: 비선형성의 필요 — 층을 쌓는 의미 부여
Step 3: sigmoid — 미분 가능, 기울기 소실 문제
Step 4: ReLU → Leaky ReLU — 현재 표준
```

---

### `data_classify_demo` — 데이터 분류 단계별 데모 ★ 신규

**교수법 포인트**: 학생들이 실제 데이터를 보고 분류하는 과정을 단계별로 경험.

**단계 구성**:
```
Step 1: 다양한 데이터 예시 제시
  나이(28), 성별(남), 혈액형(A), 사진, 이메일 내용, 동영상

Step 2: "표로 정리할 수 있나?" 질문
  → 나이, 성별, 혈액형 → 정형 데이터 강조
  → 사진, 이메일, 동영상 → 비정형 데이터 강조

Step 3: 정형 데이터 세분화
  → 나이, 점수 = 수치형 (평균 계산 의미 있음)
  → 성별, 혈액형 = 범주형 (평균 계산 의미 없음)

Step 4: 결론 — 데이터 분류 트리 완성
  (data_type_taxonomy 시각화 점등)
```

**계산 추적 표**:
```
| 데이터 | 정형/비정형 | 수치형/범주형 |
|--------|------------|--------------|
| 나이   | 정형       | 수치형       |
| 성별   | 정형       | 범주형       |
| 혈액형 | 정형       | 범주형       |
| 사진   | 비정형     | —            |
| 이메일 | 비정형     | —            |
```

**강의 원고 키포인트**:
```
Step 2 narration:
  "나이 28을 표의 한 칸에 넣을 수 있죠? 이게 정형 데이터예요.
  사진은요? 한 칸에 못 넣죠. 이게 비정형 데이터입니다."

Step 3 narration:
  "나이의 평균을 구하면 의미가 있죠.
  그런데 혈액형의 평균? A+B/2=? 의미가 없습니다.
  숫자로 연산할 수 있느냐, 없느냐가 수치형과 범주형의 차이예요."
```

---

### `ml_training_loop` — 지도학습 훈련 루프 ★ 신규

**교수법 포인트**: 기존 프로그래밍 vs 머신러닝의 패러다임 차이.

**단계 구성**:
```
Step 1: 기존 프로그래밍 패러다임
  데이터 + 규칙(프로그램) → 결과
  예) 스팸 필터: 특정 단어 있으면 스팸 (규칙 직접 작성)

Step 2: 머신러닝 패러다임 (역전)
  데이터 + 정답(레이블) → 규칙(모델)
  예) 스팸 데이터 수만 건 → AI가 규칙 스스로 학습

Step 3: 훈련 루프
  입력 → 예측 → 오차 계산 → 가중치 조정 → 반복
  (화살표 순환 다이어그램)

Step 4: 결론
  → "AI는 데이터에서 패턴을 스스로 찾는다"
  → 규칙을 프로그래머가 아닌 데이터가 결정
```

**강의 원고 키포인트**:
```
Step 2 narration:
  "기존 프로그래밍은 규칙을 우리가 직접 써요.
  '이런 단어가 있으면 스팸' 이런 식으로요.
  머신러닝은 반대입니다.
  스팸 메일 100만 건을 주면, AI가 규칙을 스스로 찾아요."

Step 3 narration:
  "이 루프가 학습의 본질입니다.
  예측하고, 틀리면, 가중치를 조금 고치고, 다시 예측하고.
  이걸 수만 번 반복하면 점점 정확해지는 거예요."
```

---

### `ai_era_transition` — AI 시대 전환 타임라인 ★ 신규

**교수법 포인트**: AI의 역사는 기대와 좌절의 반복 — 현재 제3차 붐.

**단계 구성**:
```
Step 1: 1950년대 — 태동
  튜링 테스트 (1950), 퍼셉트론 (1957)
  "기계가 생각할 수 있다!" → 과잉 기대

Step 2: 1970~80년대 — 제1차 AI 겨울
  XOR 문제 미해결, 계산 능력 한계
  "기대만큼 안 된다" → 연구비 삭감

Step 3: 1986년 — 역전파
  Rumelhart & Hinton의 역전파 발표
  다층 퍼셉트론 학습 가능 → 제2차 붐

Step 4: 2012년 — 딥러닝 혁신
  AlexNet (GPU + 빅데이터)
  2016 AlphaGo → 전 세계 충격

Step 5: 2020년대 — 생성형 AI
  GPT-4, DALL-E, ChatGPT
  2024 노벨 물리학상 → AI 연구의 과학적 인정
```

**강의 원고 키포인트**:
```
Step 2 narration:
  "첫 번째 AI 겨울이 왜 왔냐면,
  퍼셉트론 하나로는 XOR을 못 풀거든요.
  이걸 Minsky가 수학적으로 증명해버리니까
  연구비가 다 끊겼어요."

Step 5 narration:
  "2024년 노벨 물리학상이 AI 연구자들에게 갔어요.
  이게 무슨 의미냐면, AI가 이제 물리학만큼
  세상을 바꾸는 도구로 인정받았다는 거예요."
```

---

### `bigdata_pipeline_step` — 빅데이터 파이프라인 단계 ★ 신규

**교수법 포인트**: AI 활용의 실제 흐름 — 데이터가 어떻게 의사결정으로 이어지는가.

**단계 구성**:
```
Step 1: 수집 단계
  다양한 소스에서 데이터 수집
  예) 병원 진료 기록 수십만 건, IoT 센서 데이터

Step 2: 가공 단계
  결측값 처리, 이상치 제거, 정규화
  "쓸 수 있는 형태로 정제"
  중요성: 전체 AI 프로젝트의 80% 시간이 여기

Step 3: 분석/모델링 단계
  패턴 탐색, 모델 선택, 학습
  지도/비지도 학습 적용

Step 4: 예측 단계
  새 데이터에 모델 적용
  예) 신약 후보 물질 효과 예측

Step 5: 평가/의사결정 단계
  정확도 검증, 윤리적 검토
  전문가 최종 판단 (AI는 도구)
```

**강의 원고 키포인트**:
```
Step 2 narration:
  "데이터 가공이 전체의 80%를 차지한다고 합니다.
  AI 개발자의 대부분의 시간이 여기에 써요.
  좋은 AI는 좋은 데이터에서 나오거든요."

Step 5 narration:
  "AI가 예측을 해도 최종 결정은 사람이 해야 해요.
  특히 의료나 법률 같은 분야에서는요.
  AI는 의사결정 도구이지, 의사결정자가 아닙니다."
```

---

## 공통 GSAP 효과 코드 조각

### 노드 활성화
```javascript
function activateNode(nodeId, color = '#f39c12') {
  gsap.to('#' + nodeId, {
    attr: { fill: color, stroke: color },
    filter: `drop-shadow(0 0 8px ${color})`,
    duration: 0.5
  });
}
```

### 엣지 신호 흐름
```javascript
function flowEdge(edgeId, delay = 0) {
  gsap.to('#' + edgeId, {
    strokeDashoffset: 0,
    duration: 0.6,
    delay,
    ease: 'none',
    onStart: function() {
      gsap.to('#' + edgeId, { stroke: '#f39c12', duration: 0.3 });
    }
  });
}
```

### 계산 셀 채우기
```javascript
function fillCell(id, val, color = '#fff') {
  const el = document.getElementById(id);
  if (!el) return;
  gsap.to(el, {
    backgroundColor: 'rgba(243,156,18,0.3)', duration: 0.3,
    onComplete: () => {
      el.textContent = val;
      el.style.color = color;
      el.classList.add('filled');
      gsap.to(el, { backgroundColor: 'transparent', duration: 0.5 });
    }
  });
}
```

### 단계별 step-box 표시
```javascript
// .visible 클래스로만 표시 (인라인 스타일 직접 수정 금지)
function showStep(stepId) {
  document.getElementById(stepId).classList.add('visible');
}
```

---

## 강의 원고 키포인트 (2022 개정 특화)

```yaml
data_classify_demo:
  step2_narration: >
    "나이 28을 표의 한 칸에 넣을 수 있죠? 이게 정형 데이터예요.
    사진은요? 한 칸에 못 넣죠. 비정형 데이터입니다."
  step3_narration: >
    "혈액형의 평균 구하면 의미가 있나요? A+B/2=?
    의미가 없습니다. 이게 범주형 데이터의 특징입니다."

ml_training_loop:
  step2_narration: >
    "기존 프로그래밍은 규칙을 우리가 직접 써요.
    머신러닝은 반대입니다. 데이터를 주면 AI가 규칙을 스스로 찾아요."
  step3_narration: >
    "이 루프가 학습의 본질입니다.
    예측하고, 틀리면, 가중치를 조금 고치고, 반복.
    이걸 수만 번 반복하면 점점 정확해지는 거예요."

ai_era_transition:
  step2_narration: >
    "첫 번째 AI 겨울이 왜 왔냐면,
    XOR을 못 풀거든요. Minsky가 이걸 수학적으로 증명해버리니까
    연구비가 다 끊겼어요."
  step5_narration: >
    "2024년 노벨 물리학상이 AI 연구자들에게 갔어요.
    AI가 이제 물리학만큼 세상을 바꾸는 도구로 인정받은 거예요."

bigdata_pipeline_step:
  step2_narration: >
    "데이터 가공이 전체의 80%를 차지합니다.
    좋은 AI는 좋은 데이터에서 나오거든요."
  step5_narration: >
    "AI가 예측을 해도 최종 결정은 사람이 해야 해요.
    AI는 의사결정 도구이지, 의사결정자가 아닙니다."
```
