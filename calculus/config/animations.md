# 미적분 — 애니메이션 카탈로그

lecture_script.md 에이전트가 이 파일을 로드하여
미적분 특화 단계별 애니메이션을 생성할 때 사용한다.
극한, 미분, 적분, 미적분 기본 정리 단원에 특화.

---

## 지원 애니메이션 타입 목록

| 타입명 | 설명 | 단계 수 |
|--------|------|--------|
| `limit_squeeze` | 샌드위치 정리 — g(x)≤f(x)≤h(x) 수렴 단계별 표시 | 4 |
| `epsilon_delta` | 엡실론-델타 극한 정의 시각화 | 3 |
| `derivative_limit_def` | lim_{h→0} (f(x+h)-f(x))/h 계산 전개 | 5 |
| `chain_rule_compute` | 합성함수 미분 단계 — 치환→계산→곱 | 4 |
| `product_rule_compute` | 곱의 미분법 (fg)' = f'g + fg' 단계 계산 | 4 |
| `integration_by_parts` | 부분 적분 ∫u dv = uv - ∫v du 단계 전개 | 5 |
| `ftc_connection` | 미적분 기본 정리 — d/dx ∫_a^x f(t)dt = f(x) | 4 |
| `riemann_limit` | 구분구적법 → 정적분 수렴 — n 증가 단계 | 4 |

---

## 각 애니메이션 상세

### `limit_squeeze`
**샌드위치 정리**: g(x) ≤ f(x) ≤ h(x)이고 lim g(x) = lim h(x) = L이면 lim f(x) = L.

#### 단계 구성

| Step | 제목 | 내용 |
|------|------|------|
| 1 | 세 함수 등장 | g(x), f(x), h(x) 곡선을 하나씩 그린다. 아직 극한은 언급 안 함 |
| 2 | 부등식 확인 | 구간 내 g(x) ≤ f(x) ≤ h(x) 관계를 색 구역으로 강조 |
| 3 | 경계 두 함수가 수렴 | x→a에서 g(x)→L, h(x)→L 화살표와 수평선 L 등장 |
| 4 | f(x)도 수렴 확정 | f(x)가 L 사이에 끼어 있으므로 lim f(x)=L 확정. 결론 박스 |

#### 강의 원고 키포인트 (한국어 나레이션)

```
[Step 1]
"세 함수를 같은 좌표계에 그려볼게요.
 파란 곡선 g(x), 노란 곡선 f(x), 빨간 곡선 h(x)입니다."

[Step 2]
"이 구간에서 항상 g(x)가 제일 아래, h(x)가 제일 위에 있고,
 f(x)는 그 사이에 끼어 있습니다.
 마치 샌드위치처럼요."

[Step 3]
"x가 a에 가까워질 때 아래 빵 g(x)와 위 빵 h(x)가
 모두 같은 값 L에 수렴합니다."

[Step 4]
"샌드위치 속 f(x)는 위아래로 탈출할 수 없습니다.
 따라서 f(x)도 반드시 L로 수렴합니다.
 이것이 샌드위치(조임) 정리입니다."
```

#### GSAP 애니메이션 코드

```javascript
// Step 1: 세 곡선 순차 등장
gsap.timeline()
  .from('#{{asset_id}}-gcurve', { opacity: 0, duration: 0.6 })
  .from('#{{asset_id}}-fcurve', { opacity: 0, duration: 0.6 }, '+=0.3')
  .from('#{{asset_id}}-hcurve', { opacity: 0, duration: 0.6 }, '+=0.3');

// Step 2: 샌드위치 구역 강조
gsap.to('#{{asset_id}}-band', { opacity: 1, duration: 0.8 });

// Step 3: L 수평선 등장
gsap.timeline()
  .from('#{{asset_id}}-limit-line', { scaleX: 0, transformOrigin: 'left', duration: 0.6 })
  .from('#{{asset_id}}-limit-label', { opacity: 0, duration: 0.4 });

// Step 4: 결론 박스
gsap.from('#{{asset_id}}-conclusion', { opacity: 0, y: 10, duration: 0.5 });
```

---

### `epsilon_delta`
**엡실론-델타 극한 정의**: 모든 ε>0에 대해 δ>0가 존재하여 0<|x-a|<δ이면 |f(x)-L|<ε.

#### 단계 구성

| Step | 제목 | 내용 |
|------|------|------|
| 1 | 극한 정의 텍스트 | "lim_{x→a} f(x) = L"의 엡실론-델타 정식 정의 표시 |
| 2 | δ 상자 설정 | x축 방향 (a-δ, a+δ) 구간을 파란 박스로 표시 |
| 3 | ε 범위 확인 | y축 방향 (L-ε, L+ε) 구간을 초록 밴드로 표시. δ 구간 내 f(x)가 ε 밴드 안에 있음 확인 |

#### 단계별 강의 원고 키포인트

```
[Step 1]
"극한의 직관은 '가까이 가면 가까워진다'입니다.
 이것을 수학적으로 엄밀하게 정의한 것이 엡실론-델타입니다."

[Step 2]
"먼저 목표를 정합니다. f(x)와 L의 차이를 ε 이내로 만들고 싶다고 해요.
 그러면 x와 a를 얼마나 가깝게 해야 할까요?
 그 거리가 바로 δ입니다."

[Step 3]
"x가 a로부터 δ 이내에 있을 때,
 f(x)가 L로부터 ε 이내에 반드시 들어오면
 우리는 극한이 L이라고 말할 수 있습니다.
 ε을 아무리 작게 잡아도 그에 맞는 δ를 항상 찾을 수 있을 때
 극한이 존재합니다."
```

#### 계산 추적 표 구조

| | 조건 | 의미 |
|-|------|------|
| 입력 범위 | 0 < \|x - a\| < δ | x가 a에서 δ보다 가까이 (단, x≠a) |
| 출력 범위 | \|f(x) - L\| < ε | f(x)가 L에서 ε보다 가까이 |
| 극한 존재 | ∀ε>0, ∃δ>0 | 모든 ε에 대응하는 δ가 존재 |

#### GSAP 애니메이션 코드

```javascript
// Step 1: 정의 텍스트 타이핑 효과
gsap.from('#{{asset_id}}-def-text', { opacity: 0, y: -8, duration: 0.6 });

// Step 2: δ 박스 확장
gsap.timeline({ delay: 0.5 })
  .from('#{{asset_id}}-delta-box', {
    scaleX: 0,
    transformOrigin: 'center',
    duration: 0.7,
    ease: 'back.out(1.5)'
  })
  .from('#{{asset_id}}-delta-label', { opacity: 0, duration: 0.4 });

// Step 3: ε 밴드 등장 + 검증
gsap.timeline({ delay: 1.2 })
  .from('#{{asset_id}}-epsilon-band', {
    scaleY: 0,
    transformOrigin: 'center',
    duration: 0.7,
    ease: 'back.out(1.5)'
  })
  .from('#{{asset_id}}-epsilon-label', { opacity: 0, duration: 0.4 })
  .from('#{{asset_id}}-check-mark', { opacity: 0, scale: 0, transformOrigin: 'center', duration: 0.5, ease: 'back.out(2)' });
```

---

### `derivative_limit_def`
**미분의 정의**: f'(x) = lim_{h→0} [f(x+h) - f(x)] / h
f(x) = x²의 x = 2에서의 미분계수를 실제 숫자로 대입하여 계산.

#### 단계 구성

| Step | 제목 | 내용 |
|------|------|------|
| 1 | 정의 공식 표시 | f'(x) = lim_{h→0} [f(x+h)-f(x)]/h |
| 2 | f(x)=x², x=2 대입 | f'(2) = lim_{h→0} [(2+h)²-4]/h |
| 3 | 분자 전개 | (2+h)² - 4 = 4+4h+h²-4 = 4h+h² |
| 4 | 약분 | (4h+h²)/h = 4+h |
| 5 | h→0 극한 | lim_{h→0}(4+h) = 4 → f'(2) = 4 |

#### 계산 추적 표 구조

| 단계 | 식 | 결과 |
|------|-----|------|
| 정의 대입 | [(2+h)²-4] / h | — |
| 분자 전개 | [4+4h+h²-4] / h | — |
| 정리 | (4h+h²) / h | — |
| 인수분해 | h(4+h) / h | — |
| 약분 | 4+h | (h≠0) |
| 극한 | lim_{h→0}(4+h) | **4** |

#### 강의 원고 키포인트

```
[Step 1]
"미분계수의 정의입니다.
 f'(x)는 극한 기호 안에 숨어 있었습니다.
 h는 x에서의 작은 변화량이에요."

[Step 2]
"f(x)=x²를 x=2에서 계산해 봅시다.
 2+h 위치의 함수값에서 x=2에서의 값을 빼고, h로 나눕니다.
 이것이 '평균 변화율'이고, h를 0에 보내면 '순간 변화율'이 됩니다."

[Step 3-4]
"분자를 전개하고 정리하면 h가 공통인수로 나타납니다.
 약분하면 h 값이 0이 아닌 경우 깔끔하게 4+h가 됩니다."

[Step 5]
"이제 h를 0으로 보내면 4입니다.
 x=2에서 f(x)=x²의 접선 기울기는 4.
 이것이 미분계수 f'(2)=4입니다."
```

#### GSAP 애니메이션 코드

```javascript
const steps = [
  '#{{asset_id}}-step1',
  '#{{asset_id}}-step2',
  '#{{asset_id}}-step3',
  '#{{asset_id}}-step4',
  '#{{asset_id}}-step5'
];

function showStep_{{asset_id}}(idx) {
  steps.forEach((sel, i) => {
    gsap.to(sel, {
      opacity: i <= idx ? 1 : 0.2,
      y: i <= idx ? 0 : 8,
      duration: 0.4
    });
  });
  if (idx === steps.length - 1) {
    gsap.to('#{{asset_id}}-result-box', {
      opacity: 1, scale: 1.05, duration: 0.4, ease: 'back.out(1.5)',
      onComplete: () => gsap.to('#{{asset_id}}-result-box', { scale: 1, duration: 0.2 })
    });
  }
}
```

---

### `chain_rule_compute`
**합성함수 미분** y = f(g(x))의 단계별 계산.
예: y = sin(x²)

#### 단계 구성

| Step | 제목 | 내용 |
|------|------|------|
| 1 | 치환 설정 | u = g(x) = x² 설정. y = f(u) = sin(u) |
| 2 | du/dx 계산 | d/dx(x²) = 2x |
| 3 | dy/du 계산 | d/du(sin u) = cos u = cos(x²) |
| 4 | 체인 룰 적용 | dy/dx = dy/du · du/dx = cos(x²) · 2x |

#### 계산 추적 표 구조

| | 표현식 | 값 |
|-|--------|-----|
| 외함수 y | f(u) = sin(u) | — |
| 내함수 u | g(x) = x² | — |
| 내함수 미분 | du/dx | 2x |
| 외함수 미분 | dy/du | cos(u) = cos(x²) |
| 결합 (체인 룰) | dy/dx = dy/du · du/dx | **2x·cos(x²)** |

#### 강의 원고 키포인트

```
[Step 1]
"합성함수 미분의 핵심은 '분리'입니다.
 y = sin(x²)를 u = x², y = sin(u)로 분리해서 생각합니다."

[Step 2]
"내함수 x²를 x에 대해 미분합니다. 결과는 2x입니다."

[Step 3]
"외함수 sin(u)를 u에 대해 미분합니다. 결과는 cos(u)이고,
 u를 다시 x²로 되돌리면 cos(x²)입니다."

[Step 4]
"체인 룰은 두 미분값의 곱입니다.
 dy/dx = cos(x²) · 2x. 순서를 바꿔 2x·cos(x²)라고 씁니다.
 기어를 두 개 연결한 것처럼 변화율이 곱해집니다."
```

#### GSAP 애니메이션 코드

```javascript
gsap.timeline()
  .from('#{{asset_id}}-sub-u',    { opacity: 0, x: -12, duration: 0.5 })
  .from('#{{asset_id}}-sub-y',    { opacity: 0, x: -12, duration: 0.5 }, '+=0.2')
  .from('#{{asset_id}}-du-dx',    { opacity: 0, scale: 0.8, duration: 0.5 }, '+=0.3')
  .from('#{{asset_id}}-dy-du',    { opacity: 0, scale: 0.8, duration: 0.5 }, '+=0.3')
  .from('#{{asset_id}}-chain-res',{ opacity: 0, y: 10, duration: 0.6, ease: 'back.out(1.5)' }, '+=0.3');
```

---

### `product_rule_compute`
**곱의 미분법**: (fg)' = f'g + fg'
예: y = x²·sin(x)

#### 단계 구성

| Step | 제목 | 내용 |
|------|------|------|
| 1 | f, g 분리 | f(x) = x², g(x) = sin(x) 구분 |
| 2 | f', g' 계산 | f'(x) = 2x, g'(x) = cos(x) |
| 3 | 공식 적용 | (fg)' = f'g + fg' = 2x·sin(x) + x²·cos(x) |
| 4 | 결과 정리 | y' = 2x·sin(x) + x²·cos(x) (단순화 불가) |

#### 계산 추적 표 구조

| | f | g |
|-|---|---|
| 원함수 | x² | sin(x) |
| 도함수 | 2x | cos(x) |
| 곱의 미분 1항 | f'g = 2x·sin(x) | — |
| 곱의 미분 2항 | fg' = x²·cos(x) | — |
| **합계** | **y' = 2x·sin(x) + x²·cos(x)** | — |

#### 강의 원고 키포인트

```
[Step 1]
"두 함수의 곱을 미분할 때는 하나씩 차례로 미분합니다.
 첫 번째 함수 f=x², 두 번째 함수 g=sin(x)로 구분합니다."

[Step 2]
"각 함수의 도함수를 별도로 구합니다.
 f'(x)=2x, g'(x)=cos(x)입니다."

[Step 3]
"곱의 미분 공식: (fg)' = (미분한 첫 번째)×(원래 두 번째) + (원래 첫 번째)×(미분한 두 번째).
 마치 두 명이 교대로 미분을 담당하는 구조입니다."

[Step 4]
"결과를 정리하면 2x·sin(x) + x²·cos(x)입니다.
 더 이상 단순화되지 않으므로 이것이 최종 답입니다."
```

#### GSAP 애니메이션 코드

```javascript
gsap.timeline()
  .from('#{{asset_id}}-f-box',    { opacity: 0, y: -10, duration: 0.5 })
  .from('#{{asset_id}}-g-box',    { opacity: 0, y: -10, duration: 0.5 }, '-=0.3')
  .from('#{{asset_id}}-df-box',   { opacity: 0, x: 10,  duration: 0.5 }, '+=0.3')
  .from('#{{asset_id}}-dg-box',   { opacity: 0, x: 10,  duration: 0.5 }, '-=0.3')
  .from('#{{asset_id}}-term1',    { opacity: 0, scale: 0.9, duration: 0.5 }, '+=0.3')
  .from('#{{asset_id}}-plus',     { opacity: 0, duration: 0.3 }, '-=0.1')
  .from('#{{asset_id}}-term2',    { opacity: 0, scale: 0.9, duration: 0.5 }, '-=0.1')
  .from('#{{asset_id}}-result',   { opacity: 0, y: 10, duration: 0.5, ease: 'back.out(1.5)' }, '+=0.3');
```

---

### `integration_by_parts`
**부분 적분**: ∫u dv = uv - ∫v du
예: ∫x·eˣ dx

#### 단계 구성

| Step | 제목 | 내용 |
|------|------|------|
| 1 | 공식 제시 | ∫u dv = uv - ∫v du 공식 표시 |
| 2 | u, dv 선택 | u = x (LIATE 규칙: 대수 우선), dv = eˣ dx |
| 3 | du, v 계산 | du = dx, v = eˣ |
| 4 | 공식 대입 | ∫x·eˣ dx = x·eˣ - ∫eˣ dx |
| 5 | 나머지 적분 및 최종 | = x·eˣ - eˣ + C = eˣ(x-1) + C |

#### 계산 추적 표 구조

| 선택 | 미분 / 적분 방향 | 결과 |
|------|-----------------|------|
| u = x | 미분 → | du = dx |
| dv = eˣ dx | 적분 → | v = eˣ |
| uv 항 | u × v | x·eˣ |
| ∫v du 항 | ∫eˣ dx | eˣ |
| **최종** | uv - ∫v du | **eˣ(x-1) + C** |

#### 강의 원고 키포인트

```
[Step 1]
"부분 적분은 곱의 미분법을 거꾸로 이용한 것입니다.
 (uv)' = u'v + uv'를 적분하면 ∫u dv = uv - ∫v du가 됩니다."

[Step 2]
"u와 dv를 어떻게 고를지가 핵심입니다.
 LIATE 규칙: 로그 → 역삼각 → 대수(다항) → 삼각 → 지수 순으로 u를 선택합니다.
 x가 다항, eˣ가 지수이므로 u=x, dv=eˣ dx로 고릅니다."

[Step 3]
"u를 미분해서 du를, dv를 적분해서 v를 구합니다."

[Step 4]
"공식에 대입하면 x·eˣ - ∫eˣ dx가 됩니다.
 남은 적분 ∫eˣ dx는 eˣ이므로 바로 계산됩니다."

[Step 5]
"최종 답은 eˣ(x-1)+C입니다.
 eˣ를 공통인수로 묶으면 더 깔끔합니다."
```

#### GSAP 애니메이션 코드

```javascript
const ibpSteps = ['formula','uv-select','du-v-calc','substitute','final'];
let ibpIdx_{{asset_id}} = -1;

window['ibpNext_{{asset_id}}'] = function() {
  ibpIdx_{{asset_id}}++;
  if (ibpIdx_{{asset_id}} >= ibpSteps.length) return;
  const sel = '#{{asset_id}}-' + ibpSteps[ibpIdx_{{asset_id}}];
  gsap.fromTo(sel,
    { opacity: 0, y: 12 },
    { opacity: 1, y: 0, duration: 0.55, ease: 'power2.out' }
  );
  if (ibpIdx_{{asset_id}} === ibpSteps.length - 1) {
    gsap.to('#{{asset_id}}-final-box', {
      backgroundColor: 'rgba(46,204,113,0.15)',
      borderColor: '#2ecc71',
      duration: 0.4
    });
  }
};
```

---

### `ftc_connection`
**미적분 기본 정리 2부**: d/dx ∫_a^x f(t)dt = f(x)
누적넓이 함수 A(x) = ∫_a^x f(t)dt를 미분하면 피적분함수 f(x)가 나온다.

#### 단계 구성

| Step | 제목 | 내용 |
|------|------|------|
| 1 | 누적넓이 함수 정의 | A(x) = ∫_a^x f(t)dt — x를 오른쪽 끝으로 바꾸면서 넓이 누적 |
| 2 | 작은 증분 추가 | A(x+h) - A(x) = ∫_x^{x+h} f(t)dt ≈ f(x)·h (얇은 직사각형) |
| 3 | 비율로 나누기 | [A(x+h)-A(x)] / h ≈ f(x) |
| 4 | h→0 극한 | A'(x) = lim_{h→0} [A(x+h)-A(x)]/h = f(x) |

#### 강의 원고 키포인트

```
[Step 1]
"오른쪽 끝 x를 오른쪽으로 조금씩 밀면서 넓이를 누적합니다.
 이 누적넓이를 A(x)라고 정의합니다."

[Step 2]
"x를 h만큼 늘리면 넓이가 얼마나 늘까요?
 f(x)·h인 얇은 직사각형 하나가 추가됩니다.
 h가 작을수록 이 근사는 정확해집니다."

[Step 3]
"넓이 변화량을 h로 나누면 평균 변화율이 됩니다.
 이것은 f(x)에 가까워집니다."

[Step 4]
"h→0 극한을 취하면 A'(x) = f(x)가 정확히 성립합니다.
 '쌓인 넓이 함수를 미분하면 원래 함수가 나온다' — 이것이 미적분의 핵심 연결고리입니다."
```

#### GSAP 애니메이션 코드

```javascript
gsap.timeline({ delay: 0.3 })
  .from('#{{asset_id}}-Ax-def',    { opacity: 0, x: -16, duration: 0.5 })
  .from('#{{asset_id}}-area-fill', { scaleX: 0, transformOrigin: 'left', duration: 0.8 }, '+=0.3')
  .from('#{{asset_id}}-Axh-diff',  { opacity: 0, x: -16, duration: 0.5 }, '+=0.4')
  .from('#{{asset_id}}-thin-rect', { scaleY: 0, transformOrigin: 'bottom', duration: 0.6, ease: 'back.out(1.5)' }, '-=0.2')
  .from('#{{asset_id}}-ratio',     { opacity: 0, duration: 0.5 }, '+=0.4')
  .from('#{{asset_id}}-ftc2-conclusion', {
    opacity: 0, y: 10, scale: 0.95,
    duration: 0.6, ease: 'back.out(1.5)'
  }, '+=0.5');
```

---

### `riemann_limit`
**구분구적법 → 정적분 수렴**: n을 늘려가며 리만 합이 정적분 값으로 수렴하는 과정.

#### 단계 구성

| Step | 제목 | 내용 |
|------|------|------|
| 1 | n=4 분할 | 구간 [a,b]를 4개 직사각형으로 분할. 합 S₄ 수치 표시 |
| 2 | n=10 분할 | 10개 직사각형. 오차 줄어드는 것 강조. S₁₀ 수치 갱신 |
| 3 | n=50 분할 | 50개 직사각형. 곡선에 거의 딱 붙음. S₅₀ 수치 갱신 |
| 4 | n→∞ 수렴 | "직사각형 무한히 얇아지면" → 정적분 정의. 정확값 표시 |

#### 계산 추적 표 구조 (f(x)=x², [0,1] 좌끝 합)

| n | Δx | Σ (리만 합) | 오차 |
|---|-----|------------|------|
| 4 | 0.25 | 0.2188 | 0.1146 |
| 10 | 0.1 | 0.2850 | 0.0483 |
| 50 | 0.02 | 0.3234 | 0.0099 |
| 100 | 0.01 | 0.3284 | 0.0050 |
| ∞ | → 0 | **1/3 ≈ 0.3333** | **0** |

#### 강의 원고 키포인트

```
[Step 1]
"구간을 4개로 나누면 직사각형 4개로 넓이를 근사합니다.
 계단처럼 울퉁불퉁해서 오차가 꽤 큽니다."

[Step 2]
"10개로 늘리면 더 잘 맞습니다.
 오차가 절반 이하로 줄었습니다."

[Step 3]
"50개가 되면 육안으로는 곡선과 거의 구분이 안 됩니다."

[Step 4]
"n을 무한히 보내면 직사각형이 무한히 얇아지고,
 합은 정확한 넓이 1/3에 수렴합니다.
 정적분은 이 극한값을 기호 ∫로 쓴 것입니다.
 Σ(시그마)가 ∫(인테그랄)이 된 이유입니다."
```

#### GSAP 애니메이션 코드

```javascript
const riemannN_{{asset_id}} = [4, 10, 50, null];
let riemannIdx_{{asset_id}} = 0;

window['riemannNext_{{asset_id}}'] = function() {
  const idx = riemannIdx_{{asset_id}};
  if (idx >= riemannN_{{asset_id}}.length) return;
  riemannIdx_{{asset_id}}++;

  const n = riemannN_{{asset_id}}[idx];
  if (n !== null) {
    // p5 캔버스 갱신은 외부 updateRiemann 함수 호출
    if (window['updateRiemann_{{canvas_id}}']) {
      window['updateRiemann_{{canvas_id}}'](n);
    }
    gsap.from('#{{asset_id}}-step' + (idx+1), { opacity: 0, y: 8, duration: 0.5 });
    gsap.to('#{{asset_id}}-nval', { textContent: n, duration: 0.3, snap: { textContent: 1 } });
  } else {
    // n→∞ 결론
    gsap.timeline()
      .to('#{{asset_id}}-rects', { opacity: 0, duration: 0.4 })
      .from('#{{asset_id}}-exact-conclusion', {
        opacity: 0, scale: 0.9, duration: 0.6, ease: 'back.out(1.5)'
      });
  }
};
```

---

## 공통 GSAP 효과 코드 조각

아래 코드 조각은 모든 미적분 애니메이션에서 재사용 가능한 공통 패턴이다.

### 수식 단계별 페이드인

```javascript
/**
 * 수식 요소 배열을 순차 페이드인
 * @param {string} prefix - 요소 ID 접두사 (예: 'my-asset')
 * @param {number} count  - 단계 수
 * @param {number} delay  - 단계 간 딜레이 (초)
 */
function fadeInSteps(prefix, count, delay = 0.4) {
  gsap.timeline().set('[id^="' + prefix + '-step"]', { opacity: 0 });
  for (let i = 1; i <= count; i++) {
    gsap.to('#' + prefix + '-step' + i, {
      opacity: 1, y: 0, duration: 0.5,
      delay: (i - 1) * delay
    });
  }
}
```

### 결론 박스 강조 펄스

```javascript
/**
 * 결론 박스 등장 + 펄스 효과
 * @param {string} id - 결론 박스 요소 ID
 */
function pulseConclusion(id) {
  gsap.timeline()
    .fromTo('#' + id,
      { opacity: 0, scale: 0.88 },
      { opacity: 1, scale: 1.06, duration: 0.4, ease: 'back.out(1.7)' }
    )
    .to('#' + id, { scale: 1, duration: 0.25 });
}
```

### 계산 테이블 행 순차 등장

```javascript
/**
 * 테이블 tbody 행을 위에서 아래로 순차 등장
 * @param {string} tableId - 테이블 요소 ID
 * @param {number} rowDelay - 행 간 딜레이 (초)
 */
function animateTableRows(tableId, rowDelay = 0.3) {
  const rows = document.querySelectorAll('#' + tableId + ' tbody tr');
  gsap.set(rows, { opacity: 0, x: -12 });
  rows.forEach(function(row, i) {
    gsap.to(row, { opacity: 1, x: 0, duration: 0.4, delay: i * rowDelay });
  });
}
```

### 화살표 선 그리기 효과

```javascript
/**
 * SVG line/path 요소를 strokeDashoffset 애니메이션으로 그리기
 * @param {string} id       - SVG 요소 ID
 * @param {number} length   - stroke-dasharray 값 (경로 길이)
 * @param {number} duration - 지속 시간 (초)
 * @param {number} delay    - 시작 딜레이 (초)
 */
function drawLine(id, length, duration, delay) {
  gsap.set('#' + id, { strokeDasharray: length, strokeDashoffset: length });
  gsap.to('#' + id, {
    strokeDashoffset: 0,
    duration: duration,
    delay: delay || 0,
    ease: 'none'
  });
}
```

### 슬라이더 값 변경 시 캔버스 재드로우 디바운스

```javascript
/**
 * 슬라이더 입력 디바운스 — 빠른 드래그 시 성능 보호
 * @param {Function} drawFn  - 재드로우 함수
 * @param {number}   waitMs  - 대기 시간 ms (기본 30)
 */
function debounceSlider(drawFn, waitMs = 30) {
  let timer;
  return function(val) {
    clearTimeout(timer);
    timer = setTimeout(function() { drawFn(val); }, waitMs);
  };
}
```

### 수치 카운터 애니메이션

```javascript
/**
 * 숫자를 from에서 to로 애니메이션
 * @param {string} id      - 표시 요소 ID
 * @param {number} from    - 시작값
 * @param {number} to      - 목표값
 * @param {number} decimals - 소수점 자리
 */
function countTo(id, from, to, decimals) {
  gsap.to({ val: from }, {
    val: to,
    duration: 0.8,
    ease: 'power2.out',
    onUpdate: function() {
      const el = document.getElementById(id);
      if (el) el.textContent = this.targets()[0].val.toFixed(decimals);
    }
  });
}
```
