# 인공지능 수학 — 시각화 카탈로그 플러그인

visual_creator.md 에이전트가 이 파일을 로드하여
인공지능 수학 특화 시각화를 생성할 때 사용한다.

---

## 지원 시각화 타입 목록

| 타입명 | 설명 | 라이브러리 |
|--------|------|----------|
| `perceptron_diagram` | 퍼셉트론 노드/엣지/가중치 다이어그램 | SVG + GSAP |
| `neural_network` | 다층 신경망 구조 다이어그램 | SVG |
| `truth_table` | 논리 게이트 진리표 (클릭으로 행 채우기) | HTML 표 |
| `xor_scatter` | XOR 산점도 (선형 분리 불가 시각화) | p5.js |
| `xor_set_diagram` | XOR를 집합(벤다이어그램)으로 시각화 | SVG |
| `decision_boundary` | 결정 경계 2D 시각화 + 경계선 수식 연결 | p5.js |
| `activation_function` | 활성화 함수 비교 그래프 (역할 3단계 설명 포함) | Chart.js |
| `loss_curve` | 에폭별 손실 감소 곡선 | Chart.js |
| `gradient_descent_2d` | 2D 손실 곡선 위 경사하강법 | p5.js |
| `weight_update_table` | 가중치 업데이트 계산 추적 표 | HTML 표 |
| `matrix_multiply` | 행렬 곱셈 시각화 | SVG + GSAP |
| `daily_example_box` | 일상 예시 강조 박스 (논리 게이트 단원 필수) | HTML |

---

## 각 타입별 코드 패턴

### `perceptron_diagram`
입력 노드, 가중치 엣지, 합산 노드, 활성화 함수, 출력 노드를
SVG로 그리고 각 노드에 실제 숫자를 표시.

```html
<svg id="{{asset_id}}" width="420" height="240" viewBox="0 0 420 240" style="overflow:visible;">
  <!-- 입력 노드 2개 -->
  <circle id="{{asset_id}}-x1" cx="55" cy="80" r="30" fill="#2c3e50" stroke="#7f8c8d" stroke-width="2"/>
  <text x="55" y="76" text-anchor="middle" fill="#ecf0f1" font-size="12">x₁</text>
  <text id="{{asset_id}}-vx1" x="55" y="90" text-anchor="middle" fill="#f39c12" font-size="11">=0</text>

  <circle id="{{asset_id}}-x2" cx="55" cy="170" r="30" fill="#2c3e50" stroke="#7f8c8d" stroke-width="2"/>
  <text x="55" y="166" text-anchor="middle" fill="#ecf0f1" font-size="12">x₂</text>
  <text id="{{asset_id}}-vx2" x="55" y="180" text-anchor="middle" fill="#f39c12" font-size="11">=0</text>

  <!-- 가중치 엣지 -->
  <line id="{{asset_id}}-e1" x1="85" y1="90" x2="185" y2="118"
        stroke="#7f8c8d" stroke-width="1.8"
        stroke-dasharray="120" stroke-dashoffset="120"/>
  <line id="{{asset_id}}-e2" x1="85" y1="162" x2="185" y2="132"
        stroke="#7f8c8d" stroke-width="1.8"
        stroke-dasharray="120" stroke-dashoffset="120"/>

  <!-- 가중치 라벨 (애니메이션 단계에서 등장) -->
  <text id="{{asset_id}}-lw1" x="125" y="98" fill="#95a5a6" font-size="11" opacity="0">w₁={{w1}}</text>
  <text id="{{asset_id}}-lw2" x="125" y="156" fill="#95a5a6" font-size="11" opacity="0">w₂={{w2}}</text>
  <text id="{{asset_id}}-lb"  x="200" y="175" fill="#95a5a6" font-size="11" opacity="0">b={{bias}}</text>

  <!-- Σ 노드 -->
  <circle id="{{asset_id}}-sum" cx="210" cy="125" r="34" fill="#2c3e50" stroke="#7f8c8d" stroke-width="2"/>
  <text x="210" y="119" text-anchor="middle" fill="#ecf0f1" font-size="16">Σ</text>
  <text id="{{asset_id}}-vsum" x="210" y="136" text-anchor="middle" fill="#f39c12" font-size="11" opacity="0">z=?</text>

  <!-- Σ → f(z) 엣지 -->
  <line id="{{asset_id}}-esf" x1="244" y1="125" x2="282" y2="125"
        stroke="#7f8c8d" stroke-width="1.8"
        stroke-dasharray="40" stroke-dashoffset="40"/>

  <!-- 활성화 함수 박스 -->
  <rect id="{{asset_id}}-act" x="282" y="105" width="50" height="40" rx="8"
        fill="#2c3e50" stroke="#7f8c8d" stroke-width="2"/>
  <text x="307" y="122" text-anchor="middle" fill="#95a5a6" font-size="10">f(z)</text>
  <text id="{{asset_id}}-vact" x="307" y="136" text-anchor="middle" fill="#2ecc71" font-size="10" opacity="0">?</text>

  <!-- f → y 엣지 -->
  <line id="{{asset_id}}-efo" x1="332" y1="125" x2="370" y2="125"
        stroke="#7f8c8d" stroke-width="1.8"
        stroke-dasharray="40" stroke-dashoffset="40"/>

  <!-- 출력 노드 -->
  <circle id="{{asset_id}}-out" cx="385" cy="125" r="28" fill="#2c3e50" stroke="#7f8c8d" stroke-width="2"/>
  <text id="{{asset_id}}-vout" x="385" y="130" text-anchor="middle" fill="#fff" font-size="13" font-weight="bold">y=?</text>
</svg>

<!-- 인터랙티브 입력 선택 -->
<div style="font-size:0.8em; margin-top:0.5em; text-align:center;">
  입력 선택:
  <button class="abtn" onclick="setInputs_{{asset_id}}(0,0)">00</button>
  <button class="abtn" onclick="setInputs_{{asset_id}}(0,1)">01</button>
  <button class="abtn" onclick="setInputs_{{asset_id}}(1,0)">10</button>
  <button class="abtn" onclick="setInputs_{{asset_id}}(1,1)">11</button>
</div>
```

```javascript
function setInputs_{{asset_id}}(x1, x2) {
  const w1 = {{w1}}, w2 = {{w2}}, b = {{bias}};
  const z = w1*x1 + w2*x2 + b;
  const y = z >= 0 ? 1 : 0;

  document.getElementById('{{asset_id}}-vx1').textContent = '='+x1;
  document.getElementById('{{asset_id}}-vx2').textContent = '='+x2;

  gsap.to('#{{asset_id}}-lw1', { opacity:1, duration:0.4 });
  gsap.to('#{{asset_id}}-lw2', { opacity:1, duration:0.4, delay:0.1 });
  gsap.to('#{{asset_id}}-lb',  { opacity:1, duration:0.4, delay:0.2 });
  gsap.to('#{{asset_id}}-e1',  { strokeDashoffset:0, duration:0.6, ease:'none' });
  gsap.to('#{{asset_id}}-e2',  { strokeDashoffset:0, duration:0.6, ease:'none', delay:0.1 });

  setTimeout(() => {
    document.getElementById('{{asset_id}}-vsum').textContent = 'z='+z.toFixed(2);
    gsap.to('#{{asset_id}}-vsum', { opacity:1, duration:0.4 });
    gsap.to('#{{asset_id}}-sum', { stroke:'#f39c12', duration:0.4 });

    gsap.to('#{{asset_id}}-esf', { strokeDashoffset:0, duration:0.4, ease:'none', delay:0.3 });
    setTimeout(() => {
      document.getElementById('{{asset_id}}-vact').textContent = z>=0?'≥0':'<0';
      gsap.to('#{{asset_id}}-vact', { opacity:1, duration:0.3 });
    }, 600);

    gsap.to('#{{asset_id}}-efo', { strokeDashoffset:0, duration:0.4, ease:'none', delay:0.8 });
    setTimeout(() => {
      const vout = document.getElementById('{{asset_id}}-vout');
      vout.textContent = 'y='+y;
      vout.style.color = y===1 ? '#2ecc71' : '#e74c3c';
      gsap.to('#{{asset_id}}-out', { stroke: y===1?'#2ecc71':'#e74c3c', duration:0.4 });
    }, 1000);
  }, 700);
}
```

---

### `neural_network`
다층 신경망 구조를 레이어별로 표시.
NeuralNetDiagram 클래스(`templates/math_animation_lib.js`) 사용.

```html
<div id="{{asset_id}}-container" style="width:{{width}}px; height:{{height}}px; margin:0 auto;"></div>
<script>
const {{asset_id}}_net = new NeuralNetDiagram('{{asset_id}}-container', {{layers}}, {
  width: {{width}}, height: {{height}},
  nodeRadius: 28,
  showWeights: false
});
</script>
```

---

### `truth_table`
논리 게이트 진리표.
`PerceptronTruthTable` 클래스 사용 또는 순수 HTML.

```html
<table class="truth-table" id="{{asset_id}}">
  <thead>
    <tr><th>x₁</th><th>x₂</th><th>z (가중합)</th><th>y (출력)</th></tr>
  </thead>
  <tbody>
    <tr><td class="v0">0</td><td class="v0">0</td><td class="fillable">?</td><td class="fillable">?</td></tr>
    <tr><td class="v0">0</td><td class="v1">1</td><td class="fillable">?</td><td class="fillable">?</td></tr>
    <tr><td class="v1">1</td><td class="v0">0</td><td class="fillable">?</td><td class="fillable">?</td></tr>
    <tr><td class="v1">1</td><td class="v1">1</td><td class="fillable">?</td><td class="fillable">?</td></tr>
  </tbody>
</table>
<div class="anim-ctrl">
  <button class="abtn" onclick="fillTruth_{{asset_id}}()">전체 채우기 ▶</button>
</div>
```

---

### `xor_scatter`
XOR 데이터 포인트 시각화 (선형 분리 불가 강조).

```html
<canvas id="{{asset_id}}" width="280" height="280" style="border-radius:8px;"></canvas>
<script>
(function() {
  const c = document.getElementById('{{asset_id}}');
  const ctx = c.getContext('2d');
  const W=280, H=280, m=40, s=180;
  ctx.fillStyle='#1a1a2e'; ctx.fillRect(0,0,W,H);
  ctx.strokeStyle='#555'; ctx.lineWidth=1;
  ctx.strokeRect(m,m,s,s);
  ctx.fillStyle='#bdc3c7'; ctx.font='12px sans-serif'; ctx.textAlign='center';
  ctx.fillText('0',m,H-10); ctx.fillText('1',m+s,H-10);
  ctx.textAlign='right';
  ctx.fillText('0',m-5,H-m+4); ctx.fillText('1',m-5,m+4);
  [[0,0,0],[0,1,1],[1,0,1],[1,1,0]].forEach(([x1,x2,lbl]) => {
    const px=m+x1*s, py=H-m-x2*s;
    ctx.beginPath(); ctx.arc(px,py,14,0,Math.PI*2);
    ctx.fillStyle=lbl?'#2ecc71':'#e74c3c'; ctx.fill();
    ctx.strokeStyle='#fff'; ctx.lineWidth=2; ctx.stroke();
    ctx.fillStyle='#fff'; ctx.font='bold 13px sans-serif';
    ctx.textAlign='center'; ctx.fillText(lbl,px,py+5);
  });
  ctx.fillStyle='#e74c3c'; ctx.font='bold 11px sans-serif';
  ctx.textAlign='center'; ctx.fillText('직선으로 분리 불가!',W/2,18);
})();
</script>
```

---

### `xor_set_diagram` ★ 신규
XOR를 집합(벤다이어그램)으로 시각화.
**수업 핵심**: OR(합집합), AND(교집합), XOR(대칭차집합)을 나란히 놓고 비교.

**교수법 포인트**:
- OR = A ∪ B (합집합) → 직선 하나로 분리 가능
- AND = A ∩ B (교집합) → 직선 하나로 분리 가능
- XOR = A △ B (대칭차집합) = (A∪B) - (A∩B) → **1인 영역이 두 덩어리**라 직선 하나로 불가능

```html
<div style="display:flex; gap:1.5em; justify-content:center; align-items:flex-start;">
  <!-- OR: 합집합 -->
  <div style="text-align:center;">
    <svg width="140" height="100" viewBox="0 0 140 100">
      <circle cx="50" cy="50" r="35" fill="rgba(46,204,113,0.25)" stroke="#2ecc71" stroke-width="2"/>
      <circle cx="90" cy="50" r="35" fill="rgba(46,204,113,0.25)" stroke="#2ecc71" stroke-width="2"/>
      <text x="35" y="54" text-anchor="middle" fill="#2ecc71" font-size="13" font-weight="bold">1</text>
      <text x="70" y="54" text-anchor="middle" fill="#2ecc71" font-size="13" font-weight="bold">1</text>
      <text x="105" y="54" text-anchor="middle" fill="#2ecc71" font-size="13" font-weight="bold">1</text>
    </svg>
    <div style="font-size:0.75em; color:#2ecc71;">OR = A ∪ B</div>
    <div style="font-size:0.7em; color:#95a5a6;">직선 분리 ✓</div>
  </div>
  <!-- AND: 교집합 -->
  <div style="text-align:center;">
    <svg width="140" height="100" viewBox="0 0 140 100">
      <circle cx="50" cy="50" r="35" fill="rgba(149,165,166,0.1)" stroke="#7f8c8d" stroke-width="2"/>
      <circle cx="90" cy="50" r="35" fill="rgba(149,165,166,0.1)" stroke="#7f8c8d" stroke-width="2"/>
      <!-- 교집합 영역만 초록 -->
      <path d="M70,20 Q90,35 90,50 Q90,65 70,80 Q50,65 50,50 Q50,35 70,20Z"
            fill="rgba(46,204,113,0.4)" stroke="none"/>
      <text x="70" y="54" text-anchor="middle" fill="#2ecc71" font-size="13" font-weight="bold">1</text>
    </svg>
    <div style="font-size:0.75em; color:#f39c12;">AND = A ∩ B</div>
    <div style="font-size:0.7em; color:#95a5a6;">직선 분리 ✓</div>
  </div>
  <!-- XOR: 대칭차집합 -->
  <div style="text-align:center;">
    <svg width="140" height="100" viewBox="0 0 140 100">
      <circle cx="50" cy="50" r="35" fill="rgba(231,76,60,0.25)" stroke="#e74c3c" stroke-width="2"/>
      <circle cx="90" cy="50" r="35" fill="rgba(231,76,60,0.25)" stroke="#e74c3c" stroke-width="2"/>
      <!-- 교집합 영역 덮어서 지우기 -->
      <path d="M70,20 Q90,35 90,50 Q90,65 70,80 Q50,65 50,50 Q50,35 70,20Z"
            fill="#1a1a2e" stroke="none"/>
      <text x="28" y="54" text-anchor="middle" fill="#e74c3c" font-size="13" font-weight="bold">1</text>
      <text x="112" y="54" text-anchor="middle" fill="#e74c3c" font-size="13" font-weight="bold">1</text>
    </svg>
    <div style="font-size:0.75em; color:#e74c3c;">XOR = A △ B</div>
    <div style="font-size:0.7em; color:#e74c3c; font-weight:bold;">직선 분리 ✗</div>
  </div>
</div>
<div style="margin-top:0.8em; font-size:0.78em; color:#95a5a6; text-align:center;">
  XOR의 1인 영역이 <span style="color:#e74c3c; font-weight:bold;">두 덩어리</span>로 분리되어 있어 직선 하나로 동시에 잡을 수 없다
</div>
```

---

### `decision_boundary` ★ 경계선-수식 연결 강화
결정 경계 2D 시각화.

**교수법 포인트 — 임계값 θ와 경계선의 관계**:
```
w₁x₁ + w₂x₂ = θ  →  x₂ = -(w₁/w₂)·x₁ + θ/w₂
기울기: -w₁/w₂
y절편: θ/w₂

→ 임계값을 올릴수록 경계선이 위로 이동 → 1인 영역이 좁아짐
→ θ=0.3 이하면 OR처럼 작동, θ=0.7 이상이면 AND처럼 작동
→ 교과서가 w₁=w₂로 맞춘 이유: 기울기를 -1로 고정하여 θ 효과만 깔끔하게 보여주기 위한 교육적 단순화
```

```html
<canvas id="{{asset_id}}" width="320" height="300" style="border-radius:8px;"></canvas>
<div class="param-slider-group">
  <label>임계값 θ</label>
  <input type="range" min="0.1" max="1.0" step="0.05" value="{{theta}}"
         id="{{asset_id}}-sl" oninput="updateBoundary_{{asset_id}}(this.value)">
  <span id="{{asset_id}}-sv">{{theta}}</span>
</div>
<!-- 경계선 수식 실시간 표시 -->
<div id="{{asset_id}}-formula" style="font-size:0.78em; color:#f39c12; text-align:center; margin-top:0.3em;">
  x₂ = -x₁ + θ  (w₁=w₂=0.5일 때 기울기=-1)
</div>
<div id="{{asset_id}}-gate-label" style="font-size:0.8em; color:#95a5a6; text-align:center;">
  현재: AND/OR 중간
</div>
<script>
(function() {
  const canvas = document.getElementById('{{asset_id}}');
  const ctx = canvas.getContext('2d');
  const W=320, H=300, m=50, s=200;
  const w1={{w1}}, w2={{w2}};

  function draw(theta) {
    ctx.clearRect(0,0,W,H);
    ctx.fillStyle='#1a1a2e'; ctx.fillRect(0,0,W,H);

    // 축
    ctx.strokeStyle='#444'; ctx.lineWidth=1;
    ctx.beginPath(); ctx.moveTo(m,m); ctx.lineTo(m,m+s); ctx.lineTo(m+s,m+s); ctx.stroke();
    ctx.fillStyle='#bdc3c7'; ctx.font='12px sans-serif';
    ctx.textAlign='center';
    ctx.fillText('x₁',m+s/2,m+s+20);
    ctx.save(); ctx.translate(m-25,m+s/2); ctx.rotate(-Math.PI/2);
    ctx.fillText('x₂',0,0); ctx.restore();
    ctx.fillText('0',m,m+s+15); ctx.fillText('1',m+s,m+s+15);

    // 결정 경계선: w1*x1 + w2*x2 = theta
    // x2 = (theta - w1*x1) / w2
    const x1_0 = 0, x2_0 = (theta - w1*x1_0) / w2;
    const x1_1 = 1, x2_1 = (theta - w1*x1_1) / w2;
    const px0 = m + x1_0*s, py0 = m+s - x2_0*s;
    const px1 = m + x1_1*s, py1 = m+s - x2_1*s;
    ctx.strokeStyle='#f39c12'; ctx.lineWidth=2.5;
    ctx.setLineDash([6,3]);
    ctx.beginPath(); ctx.moveTo(px0,py0); ctx.lineTo(px1,py1); ctx.stroke();
    ctx.setLineDash([]);

    // 데이터 포인트
    const andPoints = [[0,0,0],[0,1,0],[1,0,0],[1,1,1]];
    andPoints.forEach(([x1v,x2v,lbl]) => {
      const px = m+x1v*s, py = m+s-x2v*s;
      ctx.beginPath(); ctx.arc(px,py,12,0,Math.PI*2);
      ctx.fillStyle = lbl?'#2ecc71':'#e74c3c'; ctx.fill();
      ctx.strokeStyle='#fff'; ctx.lineWidth=2; ctx.stroke();
      ctx.fillStyle='#fff'; ctx.font='bold 12px sans-serif';
      ctx.textAlign='center'; ctx.fillText(lbl,px,py+4);
    });

    // y절편 표시
    const yIntercept = theta / w2;
    const label = document.getElementById('{{asset_id}}-formula');
    if (label) {
      label.textContent = `x₂ = -x₁ + ${theta.toFixed(2)}/0.5  →  기울기=-1, y절편=${yIntercept.toFixed(2)}`;
    }
    const gateLabel = document.getElementById('{{asset_id}}-gate-label');
    if (gateLabel) {
      if (theta <= 0.3) gateLabel.textContent = '현재 설정: OR처럼 동작 (넓게 1)';
      else if (theta >= 0.7) gateLabel.textContent = '현재 설정: AND처럼 동작 (좁게 1)';
      else gateLabel.textContent = '현재 설정: AND/OR 중간';
      gateLabel.style.color = theta >= 0.7 ? '#2ecc71' : (theta <= 0.3 ? '#3498db' : '#95a5a6');
    }
  }

  window['updateBoundary_{{asset_id}}'] = function(val) {
    document.getElementById('{{asset_id}}-sv').textContent = parseFloat(val).toFixed(2);
    draw(parseFloat(val));
  };
  draw({{theta}});
})();
</script>
```

---

### `activation_function` ★ 역할 3단계 설명 강화
시그모이드, ReLU, Leaky ReLU, 계단 함수 비교.
슬라이더로 z 입력값 조정 가능.

**교수법 포인트 — 활성화 함수의 역할이 바뀐 이유**:
```
원래 목적 (계단함수): 뉴런처럼 "발화하느냐 마느냐" 결정
문제: 계단함수는 미분 불가 → 역전파 학습 불가

역할이 3가지로 확장된 이유:
1. 비선형성 추가: 층을 쌓는 의미를 만들어줌
   (활성화 함수 없이 층만 쌓으면 선형 변환 반복 = 선형 변환 하나와 같음)
2. 미분 가능: 역전파로 학습 가능하게
3. 정보 보존: 0.3이면 0.3대로 다음 층에 전달 (계단함수처럼 0/1로 자르지 않음)

ReLU의 "죽은 뉴런" 문제:
- 음수를 다 0으로 자르다 보니 일부 뉴런이 영원히 0만 출력
Leaky ReLU:
- x ≤ 0일 때 0.01x → "완전히 죽이지 말고 여지를 주자"는 발상
```

```html
<canvas id="{{asset_id}}" width="480" height="280"></canvas>
<div class="param-slider-group">
  <label>입력 z</label>
  <input type="range" min="-5" max="5" step="0.1" value="0"
         oninput="updateAct_{{asset_id}}(this.value)">
  <span id="{{asset_id}}-sv">0.0</span>
</div>
<div id="{{asset_id}}-readout" style="font-size:0.8em; color:#f39c12; margin-top:0.3em; text-align:center;"></div>
<!-- 역할 설명 3단계 박스 -->
<div style="display:flex; gap:0.8em; margin-top:0.7em; font-size:0.75em;">
  <div style="flex:1; background:rgba(243,156,18,0.1); border-left:3px solid #f39c12; padding:0.5em;">
    <strong style="color:#f39c12;">① 비선형성</strong><br>층을 쌓는 의미 부여
  </div>
  <div style="flex:1; background:rgba(52,152,219,0.1); border-left:3px solid #3498db; padding:0.5em;">
    <strong style="color:#3498db;">② 미분 가능</strong><br>역전파 학습 허용
  </div>
  <div style="flex:1; background:rgba(46,204,113,0.1); border-left:3px solid #2ecc71; padding:0.5em;">
    <strong style="color:#2ecc71;">③ 정보 보존</strong><br>중간값 그대로 전달
  </div>
</div>
```

---

### `loss_curve`
에폭별 MSE 손실 감소. 학습률 비교 가능.

```html
<canvas id="{{asset_id}}" width="480" height="280"></canvas>
```

---

### `gradient_descent_2d`
포물선 위의 공이 최솟값으로 굴러가는 시각화.
버튼으로 1스텝씩 진행, 계산 표 동반.

```html
<canvas id="{{asset_id}}" width="480" height="280"></canvas>
<table class="calc-table" id="{{asset_id}}-tbl">
  <thead>
    <tr><th>단계</th><th>w</th><th>L(w)</th><th>∇L</th><th>w_new</th></tr>
  </thead>
  <tbody></tbody>
</table>
<div class="anim-ctrl">
  <button class="abtn" onclick="gdStep_{{asset_id}}()">1 스텝 ▶</button>
  <button class="abtn gray" onclick="gdReset_{{asset_id}}()">↺</button>
</div>
```

---

### `daily_example_box` ★ 신규
논리 게이트 단원에서 **반드시** 삽입하는 일상 예시 박스.
수식 설명 전에 직관을 먼저 잡아주는 역할.

**사용 시점**: 각 게이트(AND/OR/XOR) 설명 슬라이드에 수식보다 먼저 배치.

```html
<div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:0.8em; margin:0.8em 0; font-size:0.78em;">
  <!-- AND 예시 -->
  <div style="background:rgba(243,156,18,0.1); border:1px solid #f39c1266; border-radius:8px; padding:0.8em;">
    <div style="font-size:1.2em; margin-bottom:0.3em;">🔐</div>
    <strong style="color:#f39c12;">AND — 카드 잠금</strong>
    <p style="margin:0.4em 0 0; color:#bdc3c7;">
      카드 인식 <strong>AND</strong> 비밀번호 맞음<br>
      → 문 열림
    </p>
    <p style="margin:0.3em 0 0; color:#95a5a6; font-size:0.9em;">둘 다 1이어야 1</p>
  </div>
  <!-- OR 예시 -->
  <div style="background:rgba(52,152,219,0.1); border:1px solid #3498db66; border-radius:8px; padding:0.8em;">
    <div style="font-size:1.2em; margin-bottom:0.3em;">🚨</div>
    <strong style="color:#3498db;">OR — 화재 경보</strong>
    <p style="margin:0.4em 0 0; color:#bdc3c7;">
      화재감지 <strong>OR</strong> 연기감지<br>
      → 경보 울림
    </p>
    <p style="margin:0.3em 0 0; color:#95a5a6; font-size:0.9em;">하나라도 1이면 1</p>
  </div>
  <!-- XOR 예시 -->
  <div style="background:rgba(231,76,60,0.1); border:1px solid #e74c3c66; border-radius:8px; padding:0.8em;">
    <div style="font-size:1.2em; margin-bottom:0.3em;">💡</div>
    <strong style="color:#e74c3c;">XOR — 계단 스위치</strong>
    <p style="margin:0.4em 0 0; color:#bdc3c7;">
      위 스위치 <strong>XOR</strong> 아래 스위치<br>
      → 하나만 올려야 불 켜짐
    </p>
    <p style="margin:0.3em 0 0; color:#95a5a6; font-size:0.9em;">다르면 1, 같으면 0</p>
  </div>
</div>
<!-- 출결 체크 예시 (XOR 심화) -->
<div style="background:rgba(155,89,182,0.1); border-left:3px solid #9b59b6; padding:0.6em 1em; margin-top:0.3em; font-size:0.78em; border-radius:0 6px 6px 0;">
  <strong style="color:#9b59b6;">출결 체크도 XOR입니다</strong>
  <span style="color:#bdc3c7; margin-left:0.5em;">명부(1) AND 결석(0) → 이상 감지 / 명부(0) AND 출석(1) → 이상 감지</span>
</div>
```

---

## 인공지능 수학 주요 숫자 파라미터 (권장값)

```yaml
AND 게이트:
  w1: 0.5, w2: 0.5, bias: -0.7
  theta: 0.7
  경계선: x₂ = -x₁ + 1.4  (기울기=-1, y절편=1.4)
  설명: z(1,1)=0.3>0→1, z(1,0)=-0.2<0→0

OR 게이트:
  w1: 0.5, w2: 0.5, bias: -0.2
  theta: 0.2
  경계선: x₂ = -x₁ + 0.4  (기울기=-1, y절편=0.4)
  설명: z(0,0)=-0.2<0→0, z(1,0)=0.3>0→1

교과서가 w₁=w₂로 맞춘 이유:
  기울기를 항상 -1로 고정 → 임계값 θ의 효과(y절편)만 깔끔하게 보여주기 위한 교육적 단순화
  w₁≠w₂이면 기울기도 같이 바뀌어서 학생이 혼란스러워짐

XOR (2층):
  은닉층 w: [[1,1],[1,1]], b: [-0.5,-1.5]
  출력층 w: [1,-2], b: -0.5
  구조: OR AND NAND = XOR
    - OR: "최소 하나는 켜졌다"
    - NAND: "전부 다 켜진 건 아니다"
    - AND(OR, NAND): "정확히 하나만 켜졌다" = XOR

시그모이드 숫자:
  σ(0)=0.5, σ(1)=0.731, σ(2)=0.880, σ(-1)=0.269

MSE 예시:
  y=1, ŷ=0.7 → L=0.09
  y=1, ŷ=0.3 → L=0.49

경사하강법:
  학습률: 0.1 (안정), 0.5 (빠름/불안정 비교)
  초기 w=-2, 목표 w=1인 L(w)=(w-1)²
```
