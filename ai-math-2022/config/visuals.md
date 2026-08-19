# 인공지능 수학(2022) — 시각화 카탈로그 플러그인

visual_creator.md 에이전트가 이 파일을 로드하여
인공지능 수학(2022 개정) 특화 시각화를 생성할 때 사용한다.

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
| `daily_example_box` | 일상 예시 강조 박스 (논리 게이트 단원 필수) | HTML |
| `loss_curve` | 에폭별 손실 감소 곡선 | Chart.js |
| `gradient_descent_2d` | 2D 손실 곡선 위 경사하강법 | p5.js |
| `weight_update_table` | 가중치 업데이트 계산 추적 표 | HTML 표 |
| `matrix_multiply` | 행렬 곱셈 시각화 | SVG + GSAP |
| `data_type_taxonomy` | 데이터 분류 트리 (정형/비정형, 수치/범주, 텍스트/이미지) | SVG |
| `ml_type_comparison` | 지도/비지도/강화학습 3열 비교 카드 | HTML |
| `ai_timeline` | 1950s~2020s AI 역사 인터랙티브 타임라인 | HTML + CSS |
| `bigdata_5v_model` | 3V/5V 빅데이터 모델 다이어그램 | SVG |
| `ai_pipeline_flow` | AI 파이프라인 5단계 플로우차트 | SVG |
| `ai_bias_case` | AI 공정성/편향 케이스 카드 | HTML |

---

## 각 타입별 코드 패턴

### `perceptron_diagram`
입력 노드, 가중치 엣지, 합산 노드, 활성화 함수, 출력 노드를
SVG로 그리고 각 노드에 실제 숫자를 표시.

```html
<svg id="{{asset_id}}" width="420" height="240" viewBox="0 0 420 240" style="overflow:hidden;">
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

  <!-- 가중치 라벨 -->
  <text id="{{asset_id}}-lw1" x="125" y="98" fill="#95a5a6" font-size="11" opacity="0">w₁={{w1}}</text>
  <text id="{{asset_id}}-lw2" x="125" y="156" fill="#95a5a6" font-size="11" opacity="0">w₂={{w2}}</text>
  <text id="{{asset_id}}-lb"  x="200" y="175" fill="#95a5a6" font-size="11" opacity="0">b={{bias}}</text>

  <!-- Σ 노드 -->
  <circle id="{{asset_id}}-sum" cx="210" cy="125" r="34" fill="#2c3e50" stroke="#7f8c8d" stroke-width="2"/>
  <text x="210" y="119" text-anchor="middle" fill="#ecf0f1" font-size="16">Σ</text>
  <text id="{{asset_id}}-vsum" x="210" y="136" text-anchor="middle" fill="#f39c12" font-size="11" opacity="0">z=?</text>

  <!-- 활성화 함수 박스 -->
  <rect id="{{asset_id}}-act" x="282" y="105" width="50" height="40" rx="8"
        fill="#2c3e50" stroke="#7f8c8d" stroke-width="2"/>
  <text x="307" y="122" text-anchor="middle" fill="#95a5a6" font-size="10">f(z)</text>
  <text id="{{asset_id}}-vact" x="307" y="136" text-anchor="middle" fill="#2ecc71" font-size="10" opacity="0">?</text>

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

---

### `neural_network`
다층 신경망 구조를 레이어별로 표시.

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
<canvas id="{{asset_id}}" width="420" height="420" style="border-radius:8px; max-height:420px;"></canvas>
<script>
(function() {
  const c = document.getElementById('{{asset_id}}');
  const ctx = c.getContext('2d');
  const W=420, H=420, m=60, s=270;
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

### `xor_set_diagram`
XOR를 집합(벤다이어그램)으로 시각화.

```html
<div style="display:flex; gap:1.5em; justify-content:center; align-items:flex-start;">
  <!-- OR: 합집합 -->
  <div style="text-align:center;">
    <svg width="140" height="100" viewBox="0 0 140 100" style="overflow:hidden;">
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
    <svg width="140" height="100" viewBox="0 0 140 100" style="overflow:hidden;">
      <circle cx="50" cy="50" r="35" fill="rgba(149,165,166,0.1)" stroke="#7f8c8d" stroke-width="2"/>
      <circle cx="90" cy="50" r="35" fill="rgba(149,165,166,0.1)" stroke="#7f8c8d" stroke-width="2"/>
      <path d="M70,20 Q90,35 90,50 Q90,65 70,80 Q50,65 50,50 Q50,35 70,20Z"
            fill="rgba(46,204,113,0.4)" stroke="none"/>
      <text x="70" y="54" text-anchor="middle" fill="#2ecc71" font-size="13" font-weight="bold">1</text>
    </svg>
    <div style="font-size:0.75em; color:#f39c12;">AND = A ∩ B</div>
    <div style="font-size:0.7em; color:#95a5a6;">직선 분리 ✓</div>
  </div>
  <!-- XOR: 대칭차집합 -->
  <div style="text-align:center;">
    <svg width="140" height="100" viewBox="0 0 140 100" style="overflow:hidden;">
      <circle cx="50" cy="50" r="35" fill="rgba(231,76,60,0.25)" stroke="#e74c3c" stroke-width="2"/>
      <circle cx="90" cy="50" r="35" fill="rgba(231,76,60,0.25)" stroke="#e74c3c" stroke-width="2"/>
      <path d="M70,20 Q90,35 90,50 Q90,65 70,80 Q50,65 50,50 Q50,35 70,20Z"
            fill="#1a1a2e" stroke="none"/>
      <text x="28" y="54" text-anchor="middle" fill="#e74c3c" font-size="13" font-weight="bold">1</text>
      <text x="112" y="54" text-anchor="middle" fill="#e74c3c" font-size="13" font-weight="bold">1</text>
    </svg>
    <div style="font-size:0.75em; color:#e74c3c;">XOR = A △ B</div>
    <div style="font-size:0.7em; color:#e74c3c; font-weight:bold;">직선 분리 ✗</div>
  </div>
</div>
```

---

### `decision_boundary`
결정 경계 2D 시각화 + 경계선 수식 연결.

```html
<canvas id="{{asset_id}}" width="480" height="420" style="border-radius:8px; max-height:420px;"></canvas>
<div class="param-slider-group">
  <label>임계값 θ</label>
  <input type="range" min="0.1" max="1.0" step="0.05" value="{{theta}}"
         id="{{asset_id}}-sl" oninput="updateBoundary_{{asset_id}}(this.value)">
  <span id="{{asset_id}}-sv">{{theta}}</span>
</div>
<div id="{{asset_id}}-formula" style="font-size:0.78em; color:#f39c12; text-align:center; margin-top:0.3em;"></div>
```

---

### `activation_function`
시그모이드, ReLU, Leaky ReLU, 계단 함수 비교.
Chart.js 사용. **반드시** `responsive:true, maintainAspectRatio:true, aspectRatio:1.6` 적용.

```html
<div style="position:relative; max-height:420px;">
  <canvas id="{{asset_id}}"></canvas>
</div>
<script>
new Chart(document.getElementById('{{asset_id}}'), {
  type: 'line',
  data: { /* sigmoid, ReLU, step 데이터 */ },
  options: {
    responsive: true,
    maintainAspectRatio: true,
    aspectRatio: 1.6,
    /* 기타 옵션 */
  }
});
</script>
```

---

### `daily_example_box`
논리 게이트 단원에서 반드시 삽입하는 일상 예시 박스.

```html
<div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:0.8em; margin:0.8em 0; font-size:0.78em;">
  <!-- AND 예시 -->
  <div style="background:rgba(243,156,18,0.1); border:1px solid #f39c1266; border-radius:8px; padding:0.8em;">
    <div style="font-size:1.2em; margin-bottom:0.3em;">🔐</div>
    <strong style="color:#f39c12;">AND — 카드 잠금</strong>
    <p style="margin:0.4em 0 0; color:#bdc3c7;">
      카드 인식 <strong>AND</strong> 비밀번호 맞음<br>→ 문 열림
    </p>
    <p style="margin:0.3em 0 0; color:#95a5a6; font-size:0.9em;">둘 다 1이어야 1</p>
  </div>
  <!-- OR 예시 -->
  <div style="background:rgba(52,152,219,0.1); border:1px solid #3498db66; border-radius:8px; padding:0.8em;">
    <div style="font-size:1.2em; margin-bottom:0.3em;">🚨</div>
    <strong style="color:#3498db;">OR — 화재 경보</strong>
    <p style="margin:0.4em 0 0; color:#bdc3c7;">
      화재감지 <strong>OR</strong> 연기감지<br>→ 경보 울림
    </p>
    <p style="margin:0.3em 0 0; color:#95a5a6; font-size:0.9em;">하나라도 1이면 1</p>
  </div>
  <!-- XOR 예시 -->
  <div style="background:rgba(231,76,60,0.1); border:1px solid #e74c3c66; border-radius:8px; padding:0.8em;">
    <div style="font-size:1.2em; margin-bottom:0.3em;">💡</div>
    <strong style="color:#e74c3c;">XOR — 계단 스위치</strong>
    <p style="margin:0.4em 0 0; color:#bdc3c7;">
      위 스위치 <strong>XOR</strong> 아래 스위치<br>→ 하나만 올려야 불 켜짐
    </p>
    <p style="margin:0.3em 0 0; color:#95a5a6; font-size:0.9em;">다르면 1, 같으면 0</p>
  </div>
</div>
```

---

### `data_type_taxonomy` ★ 신규 (2022 개정)
데이터 분류 트리 — 정형/비정형, 수치형/범주형, 텍스트/이미지/영상.

**교수법 포인트**: 정형 데이터는 표로 정리 가능, 비정형은 그렇지 않음.
수치형 = 연산 가능(평균 계산 의미 있음), 범주형 = 연산 불가(성별, 혈액형).

```html
<div style="font-size:0.78em; text-align:center;">
  <!-- 루트 -->
  <div style="display:inline-block; background:#2c3e50; border:2px solid #f39c12; border-radius:8px; padding:0.5em 1.5em; color:#f39c12; font-weight:bold;">데이터</div>

  <!-- 1단계 분기 -->
  <div style="display:flex; justify-content:center; gap:4em; margin-top:0.8em; position:relative;">
    <!-- 정형 -->
    <div>
      <div style="background:rgba(52,152,219,0.2); border:1px solid #3498db; border-radius:6px; padding:0.4em 1.2em; color:#3498db; font-weight:bold;">정형 데이터</div>
      <div style="font-size:0.85em; color:#95a5a6; margin-top:0.2em;">표로 정리 가능</div>
      <!-- 2단계 -->
      <div style="display:flex; gap:1.5em; margin-top:0.6em; justify-content:center;">
        <div>
          <div style="background:rgba(52,152,219,0.1); border:1px solid #3498db55; border-radius:5px; padding:0.3em 0.8em; color:#3498db; font-size:0.9em;">수치형</div>
          <div style="font-size:0.8em; color:#95a5a6; margin-top:0.2em;">키, 나이, 점수</div>
        </div>
        <div>
          <div style="background:rgba(52,152,219,0.1); border:1px solid #3498db55; border-radius:5px; padding:0.3em 0.8em; color:#3498db; font-size:0.9em;">범주형</div>
          <div style="font-size:0.8em; color:#95a5a6; margin-top:0.2em;">성별, 혈액형</div>
        </div>
      </div>
    </div>
    <!-- 비정형 -->
    <div>
      <div style="background:rgba(231,76,60,0.2); border:1px solid #e74c3c; border-radius:6px; padding:0.4em 1.2em; color:#e74c3c; font-weight:bold;">비정형 데이터</div>
      <div style="font-size:0.85em; color:#95a5a6; margin-top:0.2em;">표로 정리 불가</div>
      <!-- 2단계 -->
      <div style="display:flex; gap:0.8em; margin-top:0.6em; justify-content:center;">
        <div>
          <div style="background:rgba(231,76,60,0.1); border:1px solid #e74c3c55; border-radius:5px; padding:0.3em 0.6em; color:#e74c3c; font-size:0.85em;">텍스트</div>
        </div>
        <div>
          <div style="background:rgba(231,76,60,0.1); border:1px solid #e74c3c55; border-radius:5px; padding:0.3em 0.6em; color:#e74c3c; font-size:0.85em;">이미지</div>
        </div>
        <div>
          <div style="background:rgba(231,76,60,0.1); border:1px solid #e74c3c55; border-radius:5px; padding:0.3em 0.6em; color:#e74c3c; font-size:0.85em;">영상/음성</div>
        </div>
      </div>
    </div>
  </div>
</div>
```

---

### `ml_type_comparison` ★ 신규 (2022 개정)
지도/비지도/강화학습 3열 비교 카드.

**교수법 포인트**:
- 지도학습 = 정답지 있음 (스팸 분류, 가격 예측)
- 비지도학습 = 정답지 없음 (고객 군집화, 이상 탐지)
- 강화학습 = 보상으로 학습 (게임, 로봇)

```html
<div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:1em; font-size:0.78em;">
  <!-- 지도학습 -->
  <div style="background:rgba(46,204,113,0.1); border:1px solid #2ecc7166; border-radius:10px; padding:0.9em; text-align:center;">
    <div style="font-size:1.5em; margin-bottom:0.3em;">📚</div>
    <div style="color:#2ecc71; font-weight:bold; font-size:1.05em; margin-bottom:0.4em;">지도학습</div>
    <div style="color:#95a5a6; font-size:0.9em; margin-bottom:0.5em;">정답 레이블 있음</div>
    <hr style="border-color:#2ecc7133; margin:0.4em 0;">
    <div style="color:#bdc3c7; font-size:0.9em; line-height:1.6;">
      스팸 메일 분류<br>집값 예측<br>이미지 분류
    </div>
  </div>
  <!-- 비지도학습 -->
  <div style="background:rgba(52,152,219,0.1); border:1px solid #3498db66; border-radius:10px; padding:0.9em; text-align:center;">
    <div style="font-size:1.5em; margin-bottom:0.3em;">🔍</div>
    <div style="color:#3498db; font-weight:bold; font-size:1.05em; margin-bottom:0.4em;">비지도학습</div>
    <div style="color:#95a5a6; font-size:0.9em; margin-bottom:0.5em;">정답 레이블 없음</div>
    <hr style="border-color:#3498db33; margin:0.4em 0;">
    <div style="color:#bdc3c7; font-size:0.9em; line-height:1.6;">
      고객 군집화<br>이상 탐지<br>추천 시스템
    </div>
  </div>
  <!-- 강화학습 -->
  <div style="background:rgba(243,156,18,0.1); border:1px solid #f39c1266; border-radius:10px; padding:0.9em; text-align:center;">
    <div style="font-size:1.5em; margin-bottom:0.3em;">🎮</div>
    <div style="color:#f39c12; font-weight:bold; font-size:1.05em; margin-bottom:0.4em;">강화학습</div>
    <div style="color:#95a5a6; font-size:0.9em; margin-bottom:0.5em;">보상으로 학습</div>
    <hr style="border-color:#f39c1233; margin:0.4em 0;">
    <div style="color:#bdc3c7; font-size:0.9em; line-height:1.6;">
      AlphaGo<br>자율주행<br>게임 플레이
    </div>
  </div>
</div>
```

---

### `ai_timeline` ★ 신규 (2022 개정)
1950s~2020s AI 역사 인터랙티브 타임라인.
클릭으로 시대별 상세 정보 표시.

**교수법 포인트**:
- 1950s: 튜링 테스트, 퍼셉트론 제안
- 1970~80s: AI 겨울 (기대 과잉 → 실망)
- 1980s: 역전파 알고리즘
- 2010s: 딥러닝 르네상스 (AlexNet, AlphaGo)
- 2020s: 생성형 AI, 2024 노벨 물리학상

```html
<div id="{{asset_id}}" style="font-size:0.75em; overflow:hidden;">
  <!-- 타임라인 바 -->
  <div style="display:flex; align-items:center; gap:0; margin-bottom:0.6em; position:relative;">
    <div style="flex:1; height:3px; background:linear-gradient(to right, #3498db, #f39c12, #e74c3c, #2ecc71, #9b59b6);"></div>
  </div>
  <!-- 시대별 마커 -->
  <div style="display:flex; justify-content:space-between; text-align:center;">
    <div class="era-marker" onclick="showEra_{{asset_id}}('1950')" style="cursor:pointer; flex:1;">
      <div style="width:12px; height:12px; background:#3498db; border-radius:50%; margin:0 auto 0.3em;"></div>
      <div style="color:#3498db; font-weight:bold;">1950s</div>
      <div style="color:#95a5a6; font-size:0.9em;">태동기</div>
    </div>
    <div class="era-marker" onclick="showEra_{{asset_id}}('1970')" style="cursor:pointer; flex:1;">
      <div style="width:12px; height:12px; background:#e74c3c; border-radius:50%; margin:0 auto 0.3em;"></div>
      <div style="color:#e74c3c; font-weight:bold;">1970~80s</div>
      <div style="color:#95a5a6; font-size:0.9em;">AI 겨울</div>
    </div>
    <div class="era-marker" onclick="showEra_{{asset_id}}('1986')" style="cursor:pointer; flex:1;">
      <div style="width:12px; height:12px; background:#f39c12; border-radius:50%; margin:0 auto 0.3em;"></div>
      <div style="color:#f39c12; font-weight:bold;">1986</div>
      <div style="color:#95a5a6; font-size:0.9em;">역전파</div>
    </div>
    <div class="era-marker" onclick="showEra_{{asset_id}}('2012')" style="cursor:pointer; flex:1;">
      <div style="width:12px; height:12px; background:#2ecc71; border-radius:50%; margin:0 auto 0.3em;"></div>
      <div style="color:#2ecc71; font-weight:bold;">2012~16</div>
      <div style="color:#95a5a6; font-size:0.9em;">딥러닝</div>
    </div>
    <div class="era-marker" onclick="showEra_{{asset_id}}('2020')" style="cursor:pointer; flex:1;">
      <div style="width:12px; height:12px; background:#9b59b6; border-radius:50%; margin:0 auto 0.3em;"></div>
      <div style="color:#9b59b6; font-weight:bold;">2020s</div>
      <div style="color:#95a5a6; font-size:0.9em;">생성형 AI</div>
    </div>
  </div>
  <!-- 상세 정보 박스 -->
  <div id="{{asset_id}}-detail" style="margin-top:0.6em; min-height:3em; background:rgba(255,255,255,0.05); border-radius:6px; padding:0.6em; color:#bdc3c7; font-size:0.95em; display:none;">
    클릭하여 시대별 내용을 확인하세요.
  </div>
</div>
<script>
(function() {
  const eraData = {
    '1950': { color:'#3498db', title:'1950년대 — AI의 태동', text:'1950 튜링 테스트 제안 ("기계가 생각할 수 있는가?") / 1957 퍼셉트론 고안 (Rosenblatt) / 1956 다트머스 회의 — AI라는 용어 탄생' },
    '1970': { color:'#e74c3c', title:'AI 겨울 (1970~1980s)', text:'XOR 문제 → 단층 퍼셉트론 한계 드러남 / 과잉 기대 → 예산 삭감 / 전문가 시스템의 한계 노출 / 연구 침체기' },
    '1986': { color:'#f39c12', title:'1986 — 역전파 알고리즘', text:'Rumelhart & Hinton — 역전파(backpropagation) 발표 / 다층 퍼셉트론 학습 가능해짐 / 제2차 AI 붐의 씨앗' },
    '2012': { color:'#2ecc71', title:'2012~2016 — 딥러닝 르네상스', text:'2012 AlexNet — ImageNet 오류율 26%→16% 혁신 / GPU 병렬 학습으로 대규모 신경망 가능 / 2016 AlphaGo — 이세돌 9단 4:1 승' },
    '2020': { color:'#9b59b6', title:'2020s — 생성형 AI 시대', text:'GPT-3/4, DALL-E, ChatGPT 등장 / 2024 노벨 물리학상: Hopfield & Hinton (신경망 연구) / AI가 일상 도구로 전환' }
  };
  window['showEra_{{asset_id}}'] = function(era) {
    const d = eraData[era];
    const box = document.getElementById('{{asset_id}}-detail');
    box.style.display = 'block';
    box.style.borderLeft = '3px solid ' + d.color;
    box.innerHTML = '<strong style="color:' + d.color + '">' + d.title + '</strong><br><span style="font-size:0.9em;">' + d.text + '</span>';
  };
})();
</script>
```

---

### `bigdata_5v_model` ★ 신규 (2022 개정)
빅데이터의 3V → 5V 모델 다이어그램.

**교수법 포인트**:
- 3V (기본): Volume(규모), Velocity(속도), Variety(다양성)
- 5V (확장): + Value(가치), Veracity(정확성)
- 규모만 크다고 빅데이터가 아님 — 가치와 정확성이 핵심

```html
<div style="display:flex; justify-content:center; align-items:center; gap:0.5em; flex-wrap:wrap; font-size:0.78em;">
  <!-- 3V 원형 -->
  <div style="display:flex; gap:0.5em;">
    <div style="background:rgba(52,152,219,0.15); border:2px solid #3498db; border-radius:50%; width:90px; height:90px; display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center;">
      <div style="font-size:1.1em;">📦</div>
      <div style="color:#3498db; font-weight:bold; font-size:0.95em;">Volume</div>
      <div style="color:#95a5a6; font-size:0.8em;">규모</div>
    </div>
    <div style="background:rgba(52,152,219,0.15); border:2px solid #3498db; border-radius:50%; width:90px; height:90px; display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center;">
      <div style="font-size:1.1em;">⚡</div>
      <div style="color:#3498db; font-weight:bold; font-size:0.95em;">Velocity</div>
      <div style="color:#95a5a6; font-size:0.8em;">속도</div>
    </div>
    <div style="background:rgba(52,152,219,0.15); border:2px solid #3498db; border-radius:50%; width:90px; height:90px; display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center;">
      <div style="font-size:1.1em;">🎨</div>
      <div style="color:#3498db; font-weight:bold; font-size:0.95em;">Variety</div>
      <div style="color:#95a5a6; font-size:0.8em;">다양성</div>
    </div>
  </div>
  <!-- 화살표 -->
  <div style="color:#f39c12; font-size:1.5em; font-weight:bold;">+</div>
  <!-- 2V 추가 -->
  <div style="display:flex; gap:0.5em;">
    <div style="background:rgba(243,156,18,0.15); border:2px solid #f39c12; border-radius:50%; width:90px; height:90px; display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center;">
      <div style="font-size:1.1em;">💎</div>
      <div style="color:#f39c12; font-weight:bold; font-size:0.95em;">Value</div>
      <div style="color:#95a5a6; font-size:0.8em;">가치</div>
    </div>
    <div style="background:rgba(243,156,18,0.15); border:2px solid #f39c12; border-radius:50%; width:90px; height:90px; display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center;">
      <div style="font-size:1.1em;">✅</div>
      <div style="color:#f39c12; font-weight:bold; font-size:0.95em;">Veracity</div>
      <div style="color:#95a5a6; font-size:0.8em;">정확성</div>
    </div>
  </div>
  <!-- 결론 -->
  <div style="width:100%; text-align:center; margin-top:0.5em; color:#95a5a6; font-size:0.9em;">
    3V(기본) → <span style="color:#f39c12; font-weight:bold;">5V(확장)</span> — 규모만 크다고 빅데이터가 아님
  </div>
</div>
```

---

### `ai_pipeline_flow` ★ 신규 (2022 개정)
AI 파이프라인 5단계 플로우차트.

**단계**: 수집 → 가공 → 분석/모델링 → 예측 → 평가/의사결정

```html
<div style="display:flex; align-items:center; justify-content:center; gap:0.3em; font-size:0.75em; flex-wrap:nowrap; overflow:hidden;">
  <!-- 1단계 -->
  <div style="text-align:center; min-width:80px;">
    <div style="background:rgba(52,152,219,0.2); border:1px solid #3498db; border-radius:8px; padding:0.5em 0.3em;">
      <div style="font-size:1.3em;">📥</div>
      <div style="color:#3498db; font-weight:bold; font-size:0.95em;">수집</div>
      <div style="color:#95a5a6; font-size:0.8em; line-height:1.3;">센서<br>인터넷</div>
    </div>
  </div>
  <div style="color:#f39c12; font-size:1.2em; font-weight:bold;">→</div>
  <!-- 2단계 -->
  <div style="text-align:center; min-width:80px;">
    <div style="background:rgba(243,156,18,0.2); border:1px solid #f39c12; border-radius:8px; padding:0.5em 0.3em;">
      <div style="font-size:1.3em;">🔧</div>
      <div style="color:#f39c12; font-weight:bold; font-size:0.95em;">가공</div>
      <div style="color:#95a5a6; font-size:0.8em; line-height:1.3;">정제<br>변환</div>
    </div>
  </div>
  <div style="color:#f39c12; font-size:1.2em; font-weight:bold;">→</div>
  <!-- 3단계 -->
  <div style="text-align:center; min-width:80px;">
    <div style="background:rgba(46,204,113,0.2); border:1px solid #2ecc71; border-radius:8px; padding:0.5em 0.3em;">
      <div style="font-size:1.3em;">🧠</div>
      <div style="color:#2ecc71; font-weight:bold; font-size:0.95em;">분석</div>
      <div style="color:#95a5a6; font-size:0.8em; line-height:1.3;">모델<br>학습</div>
    </div>
  </div>
  <div style="color:#f39c12; font-size:1.2em; font-weight:bold;">→</div>
  <!-- 4단계 -->
  <div style="text-align:center; min-width:80px;">
    <div style="background:rgba(155,89,182,0.2); border:1px solid #9b59b6; border-radius:8px; padding:0.5em 0.3em;">
      <div style="font-size:1.3em;">🔮</div>
      <div style="color:#9b59b6; font-weight:bold; font-size:0.95em;">예측</div>
      <div style="color:#95a5a6; font-size:0.8em; line-height:1.3;">추론<br>분류</div>
    </div>
  </div>
  <div style="color:#f39c12; font-size:1.2em; font-weight:bold;">→</div>
  <!-- 5단계 -->
  <div style="text-align:center; min-width:80px;">
    <div style="background:rgba(231,76,60,0.2); border:1px solid #e74c3c; border-radius:8px; padding:0.5em 0.3em;">
      <div style="font-size:1.3em;">📊</div>
      <div style="color:#e74c3c; font-weight:bold; font-size:0.95em;">평가</div>
      <div style="color:#95a5a6; font-size:0.8em; line-height:1.3;">검증<br>결정</div>
    </div>
  </div>
</div>
```

---

### `ai_bias_case` ★ 신규 (2022 개정)
AI 공정성/편향 케이스 카드.

**교수법 포인트**:
- 편향된 데이터 → 편향된 AI
- 편향의 종류: 학습 데이터 편향, 알고리즘 편향, 사용자 피드백 편향

```html
<div style="font-size:0.78em;">
  <div style="display:grid; grid-template-columns:1fr 1fr; gap:0.8em;">
    <!-- 케이스 1 -->
    <div style="background:rgba(231,76,60,0.1); border-left:3px solid #e74c3c; border-radius:0 8px 8px 0; padding:0.7em;">
      <div style="color:#e74c3c; font-weight:bold; margin-bottom:0.3em;">채용 AI 성차별</div>
      <div style="color:#bdc3c7; font-size:0.9em; line-height:1.5;">
        과거 남성 채용 데이터로 학습<br>
        → 여성 지원자 점수 자동 감점<br>
        <span style="color:#95a5a6;">학습 데이터의 역사적 편향 반영</span>
      </div>
    </div>
    <!-- 케이스 2 -->
    <div style="background:rgba(231,76,60,0.1); border-left:3px solid #f39c12; border-radius:0 8px 8px 0; padding:0.7em;">
      <div style="color:#f39c12; font-weight:bold; margin-bottom:0.3em;">얼굴 인식 오류</div>
      <div style="color:#bdc3c7; font-size:0.9em; line-height:1.5;">
        밝은 피부 사진 위주 학습<br>
        → 어두운 피부 인식률 낮음<br>
        <span style="color:#95a5a6;">학습 데이터 다양성 부족</span>
      </div>
    </div>
    <!-- 케이스 3 -->
    <div style="background:rgba(52,152,219,0.1); border-left:3px solid #3498db; border-radius:0 8px 8px 0; padding:0.7em;">
      <div style="color:#3498db; font-weight:bold; margin-bottom:0.3em;">의료 진단 AI</div>
      <div style="color:#bdc3c7; font-size:0.9em; line-height:1.5;">
        특정 인종 의료 데이터 부족<br>
        → 해당 그룹 진단 정확도 ↓<br>
        <span style="color:#95a5a6;">데이터 대표성 문제</span>
      </div>
    </div>
    <!-- 해결 방향 -->
    <div style="background:rgba(46,204,113,0.1); border-left:3px solid #2ecc71; border-radius:0 8px 8px 0; padding:0.7em;">
      <div style="color:#2ecc71; font-weight:bold; margin-bottom:0.3em;">해결 방향</div>
      <div style="color:#bdc3c7; font-size:0.9em; line-height:1.5;">
        ✓ 다양한 데이터 수집<br>
        ✓ 편향 탐지 알고리즘<br>
        ✓ 인간 검토 프로세스
      </div>
    </div>
  </div>
</div>
```

---

## 인공지능 수학(2022) 주요 파라미터 (권장값)

```yaml
강조색: '#f39c12'  # 기존 ai-math와 동일

AND 게이트:
  w1: 0.5, w2: 0.5, bias: -0.7
  theta: 0.7

OR 게이트:
  w1: 0.5, w2: 0.5, bias: -0.2
  theta: 0.2

XOR (2층):
  은닉층 w: [[1,1],[1,1]], b: [-0.5,-1.5]
  출력층 w: [1,-2], b: -0.5
  구조: OR AND NAND = XOR

시그모이드: σ(0)=0.5, σ(1)=0.731, σ(2)=0.880, σ(-1)=0.269
```
