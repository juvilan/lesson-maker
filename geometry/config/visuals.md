# 기하 — 시각화 카탈로그 플러그인

visual_creator.md 에이전트가 이 파일을 로드하여
기하 특화 시각화(평면벡터, 공간벡터, 이차곡선, 공간도형)를 생성할 때 사용한다.

---

## 지원 시각화 타입 목록

| 타입명 | 설명 | 라이브러리 |
|--------|------|-----------|
| `vector_2d` | 2D 벡터 덧셈/뺄셈/스칼라 배, 슬라이더로 성분 조절 | p5.js |
| `dot_product_visual` | 내적 기하학적 의미 — 두 벡터 사이각과 정사영 표시 | p5.js |
| `vector_decomposition` | 벡터 분해 v = a·e₁ + b·e₂ 화살표 시각화 | SVG |
| `parabola_focus` | 포물선 위 점에서 초점·준선까지 거리 실시간 표시 | p5.js |
| `ellipse_foci` | 타원 위 점에서 두 초점까지 거리의 합 = 2a 표시 | p5.js |
| `hyperbola_def` | 쌍곡선 위 점에서 두 초점까지 거리 차 = 2a 표시 | p5.js |
| `conic_comparison` | 이차곡선 3종 비교 (포물선/타원/쌍곡선) 동일 좌표계 | Chart.js |
| `space_vector_3d` | 공간벡터 SVG 등각투영(isometric) 시각화 | SVG |
| `cross_product_visual` | 외적의 기하학적 의미 — 평행사변형 넓이 시각화 | SVG |

---

## 각 타입별 코드 패턴

### `vector_2d`
두 벡터 **a⃗**, **b⃗**를 화살표로 표시하고, 슬라이더로 각 성분을 조절하며
덧셈·뺄셈·스칼라 배를 실시간으로 확인.
컨테이너 너비를 읽어 반응형으로 동작한다.

```html
<div id="{{asset_id}}-wrap" style="width:100%; max-width:480px; margin:0 auto;">
  <div id="{{asset_id}}-canvas-holder"></div>
  <div style="font-size:0.8em; margin-top:0.6em;">
    <label>a⃗ x</label>
    <input type="range" min="-4" max="4" step="0.5" value="{{ax}}"
           id="{{asset_id}}-ax" oninput="updateVec2d_{{asset_id}}()">
    <span id="{{asset_id}}-axv">{{ax}}</span>
    &nbsp;
    <label>a⃗ y</label>
    <input type="range" min="-4" max="4" step="0.5" value="{{ay}}"
           id="{{asset_id}}-ay" oninput="updateVec2d_{{asset_id}}()">
    <span id="{{asset_id}}-ayv">{{ay}}</span>
  </div>
  <div style="font-size:0.8em; margin-top:0.3em;">
    <label>b⃗ x</label>
    <input type="range" min="-4" max="4" step="0.5" value="{{bx}}"
           id="{{asset_id}}-bx" oninput="updateVec2d_{{asset_id}}()">
    <span id="{{asset_id}}-bxv">{{bx}}</span>
    &nbsp;
    <label>b⃗ y</label>
    <input type="range" min="-4" max="4" step="0.5" value="{{by}}"
           id="{{asset_id}}-by" oninput="updateVec2d_{{asset_id}}()">
    <span id="{{asset_id}}-byv">{{by}}</span>
  </div>
  <div id="{{asset_id}}-result" style="font-size:0.78em; color:#f39c12; text-align:center; margin-top:0.4em;"></div>
</div>
```

```javascript
(function() {
  const wrap = document.getElementById('{{asset_id}}-wrap');
  const w = Math.min(wrap.clientWidth, 480);
  const h = Math.min(w * 0.625, 300);
  const holder = document.getElementById('{{asset_id}}-canvas-holder');

  const sketch = function(p) {
    const cx = w / 2, cy = h / 2;
    const scale = Math.min(w, h) / 10;

    function drawArrow(x1, y1, x2, y2, col) {
      p.stroke(col); p.strokeWeight(2.5); p.fill(col);
      p.line(x1, y1, x2, y2);
      const angle = p.atan2(y2 - y1, x2 - x1);
      p.push();
      p.translate(x2, y2);
      p.rotate(angle);
      p.triangle(0, 0, -10, -4, -10, 4);
      p.pop();
    }

    p.setup = function() {
      const cnv = p.createCanvas(w, h);
      cnv.parent('{{asset_id}}-canvas-holder');
      p.background(26, 26, 46);
    };

    p.draw = function() {
      p.background(26, 26, 46);
      // 격자
      p.stroke(60, 60, 80); p.strokeWeight(1);
      for (let i = -5; i <= 5; i++) {
        p.line(cx + i * scale, 0, cx + i * scale, h);
        p.line(0, cy + i * scale, w, cy + i * scale);
      }
      // 축
      p.stroke(100, 100, 120); p.strokeWeight(1.5);
      p.line(0, cy, w, cy); p.line(cx, 0, cx, h);
      p.fill(150); p.noStroke(); p.textSize(11); p.textAlign(p.CENTER);
      p.text('x', w - 10, cy - 4); p.text('y', cx + 8, 12);

      const ax = parseFloat(document.getElementById('{{asset_id}}-ax').value);
      const ay = parseFloat(document.getElementById('{{asset_id}}-ay').value);
      const bx = parseFloat(document.getElementById('{{asset_id}}-bx').value);
      const by = parseFloat(document.getElementById('{{asset_id}}-by').value);

      // a⃗
      drawArrow(cx, cy, cx + ax * scale, cy - ay * scale, p.color(52, 152, 219));
      p.fill(52, 152, 219); p.noStroke(); p.textSize(12);
      p.textAlign(p.LEFT);
      p.text('a⃗(' + ax + ',' + ay + ')', cx + ax * scale + 5, cy - ay * scale - 5);

      // b⃗
      drawArrow(cx, cy, cx + bx * scale, cy - by * scale, p.color(231, 76, 60));
      p.fill(231, 76, 60);
      p.text('b⃗(' + bx + ',' + by + ')', cx + bx * scale + 5, cy - by * scale - 5);

      // a⃗ + b⃗ (평행사변형 법칙)
      p.stroke(243, 156, 18); p.strokeWeight(1); p.noFill();
      p.line(cx + ax * scale, cy - ay * scale,
             cx + (ax + bx) * scale, cy - (ay + by) * scale);
      p.line(cx + bx * scale, cy - by * scale,
             cx + (ax + bx) * scale, cy - (ay + by) * scale);
      drawArrow(cx, cy,
                cx + (ax + bx) * scale, cy - (ay + by) * scale,
                p.color(243, 156, 18));
      p.fill(243, 156, 18); p.noStroke(); p.textSize(12);
      p.textAlign(p.LEFT);
      p.text('a⃗+b⃗(' + (ax+bx) + ',' + (ay+by) + ')',
             cx + (ax + bx) * scale + 5, cy - (ay + by) * scale - 5);
    };
  };

  window['updateVec2d_{{asset_id}}'] = function() {
    ['ax','ay','bx','by'].forEach(id => {
      const el = document.getElementById('{{asset_id}}-' + id);
      document.getElementById('{{asset_id}}-' + id + 'v').textContent = el.value;
    });
  };

  new p5(sketch);
})();
```

---

### `dot_product_visual`
두 벡터 **a⃗**, **b⃗**와 사이각 θ를 표시하고,
**a⃗** 위의 **b⃗** 정사영(projection)을 실시간으로 시각화.
각도 슬라이더로 θ를 조절하면 내적값 변화를 확인할 수 있다.

```html
<div id="{{asset_id}}-wrap" style="width:100%; max-width:480px; margin:0 auto;">
  <div id="{{asset_id}}-canvas-holder"></div>
  <div style="font-size:0.8em; margin-top:0.6em; text-align:center;">
    <label>사이각 θ (°)</label>
    <input type="range" min="0" max="180" step="5" value="{{theta_deg}}"
           id="{{asset_id}}-theta" oninput="updateDot_{{asset_id}}(this.value)">
    <span id="{{asset_id}}-thetav">{{theta_deg}}°</span>
  </div>
  <div id="{{asset_id}}-formula"
       style="font-size:0.82em; color:#f39c12; text-align:center; margin-top:0.4em;"></div>
</div>
```

```javascript
(function() {
  const wrap = document.getElementById('{{asset_id}}-wrap');
  const w = Math.min(wrap.clientWidth, 480);
  const h = Math.min(w * 0.625, 300);
  const cx = w * 0.35, cy = h * 0.65;
  const lenA = w * 0.28, lenB = w * 0.22;

  const sketch = function(p) {
    function drawArrow(x1, y1, x2, y2, col, label) {
      p.stroke(col); p.strokeWeight(2.5); p.fill(col);
      p.line(x1, y1, x2, y2);
      const angle = p.atan2(y2 - y1, x2 - x1);
      p.push(); p.translate(x2, y2); p.rotate(angle);
      p.triangle(0, 0, -10, -4, -10, 4); p.pop();
      if (label) {
        p.fill(col); p.noStroke(); p.textSize(13); p.textAlign(p.LEFT);
        p.text(label, x2 + 6, y2 - 4);
      }
    }

    p.setup = function() {
      const cnv = p.createCanvas(w, h);
      cnv.parent('{{asset_id}}-canvas-holder');
    };

    p.draw = function() {
      p.background(26, 26, 46);
      const theta = parseFloat(document.getElementById('{{asset_id}}-theta').value);
      const tRad = p.radians(theta);

      const ax = cx + lenA, ay = cy;
      const bx = cx + lenB * p.cos(-tRad), by = cy + lenB * p.sin(-tRad);

      // a⃗ 방향 정사영
      const projLen = lenB * p.cos(tRad);
      const projX = cx + projLen, projY = cy;

      // 정사영 점선
      p.stroke(150, 150, 150); p.strokeWeight(1); p.drawingContext.setLineDash([4, 4]);
      p.line(bx, by, projX, projY);
      p.drawingContext.setLineDash([]);

      // 정사영 구간 표시
      p.stroke(46, 204, 113); p.strokeWeight(3);
      p.line(cx, cy, projX, projY);
      p.fill(46, 204, 113); p.noStroke(); p.textSize(10);
      p.textAlign(p.CENTER);
      p.text('|b⃗|cosθ', cx + projLen / 2, cy + 14);

      // 각도 호
      p.noFill(); p.stroke(155, 89, 182); p.strokeWeight(1.5);
      p.arc(cx, cy, 50, 50, -tRad, 0);
      p.fill(155, 89, 182); p.noStroke(); p.textSize(11);
      p.textAlign(p.LEFT);
      p.text('θ', cx + 30, cy - 4);

      drawArrow(cx, cy, ax, ay, p.color(52, 152, 219), 'a⃗');
      drawArrow(cx, cy, bx, by, p.color(231, 76, 60), 'b⃗');

      // 수식 업데이트
      const dotVal = (lenA / w * 4) * (lenB / w * 4) * Math.cos(tRad);
      const formula = document.getElementById('{{asset_id}}-formula');
      if (formula) {
        formula.textContent =
          'a⃗·b⃗ = |a⃗||b⃗|cosθ = |a⃗||b⃗|cos' + theta + '° ≈ ' +
          dotVal.toFixed(2) +
          (Math.abs(theta - 90) < 3 ? '  → 수직! (내적=0)' :
           theta > 90 ? '  → 둔각 (내적<0)' : '  → 예각 (내적>0)');
      }
    };
  };

  window['updateDot_{{asset_id}}'] = function(val) {
    document.getElementById('{{asset_id}}-thetav').textContent = val + '°';
  };

  new p5(sketch);
})();
```

---

### `vector_decomposition`
벡터 **v** = a·**e₁** + b·**e₂** 분해를 SVG 화살표로 표시.
각 성분 화살표가 순서대로 나타나 분해 과정을 직관적으로 보여준다.

```html
<div id="{{asset_id}}-wrap" style="width:100%; max-width:420px; margin:0 auto; overflow:hidden;">
  <svg id="{{asset_id}}" viewBox="0 0 420 320"
       preserveAspectRatio="xMidYMid meet"
       style="width:100%; height:auto; overflow:hidden; display:block; background:#1a1a2e;">
    <defs>
      <marker id="{{asset_id}}-arr-blue" markerWidth="8" markerHeight="8"
              refX="6" refY="3" orient="auto">
        <path d="M0,0 L0,6 L8,3 z" fill="#3498db"/>
      </marker>
      <marker id="{{asset_id}}-arr-red" markerWidth="8" markerHeight="8"
              refX="6" refY="3" orient="auto">
        <path d="M0,0 L0,6 L8,3 z" fill="#e74c3c"/>
      </marker>
      <marker id="{{asset_id}}-arr-gold" markerWidth="8" markerHeight="8"
              refX="6" refY="3" orient="auto">
        <path d="M0,0 L0,6 L8,3 z" fill="#f39c12"/>
      </marker>
    </defs>

    <!-- 격자 -->
    <g stroke="#2c3e50" stroke-width="1">
      <line x1="60" y1="260" x2="360" y2="260"/>
      <line x1="210" y1="40" x2="210" y2="280"/>
    </g>
    <text x="355" y="255" fill="#7f8c8d" font-size="12">x</text>
    <text x="215" y="48" fill="#7f8c8d" font-size="12">y</text>

    <!-- 기저 벡터 e₁, e₂ -->
    <line x1="210" y1="260" x2="270" y2="260"
          stroke="#7f8c8d" stroke-width="1.5" stroke-dasharray="4,3"
          marker-end="url(#{{asset_id}}-arr-blue)"/>
    <text x="234" y="275" fill="#7f8c8d" font-size="11" text-anchor="middle">e₁</text>
    <line x1="210" y1="260" x2="210" y2="200"
          stroke="#7f8c8d" stroke-width="1.5" stroke-dasharray="4,3"
          marker-end="url(#{{asset_id}}-arr-red)"/>
    <text x="197" y="232" fill="#7f8c8d" font-size="11" text-anchor="middle">e₂</text>

    <!-- a·e₁ 성분 (애니메이션) -->
    <line id="{{asset_id}}-comp1"
          x1="210" y1="260" x2="{{ex}}" y2="260"
          stroke="#3498db" stroke-width="2.5"
          stroke-dasharray="200" stroke-dashoffset="200"
          marker-end="url(#{{asset_id}}-arr-blue)"/>
    <text id="{{asset_id}}-label1" x="{{ex_mid}}" y="275"
          fill="#3498db" font-size="12" text-anchor="middle" opacity="0">{{a}}·e₁</text>

    <!-- b·e₂ 성분 (애니메이션) -->
    <line id="{{asset_id}}-comp2"
          x1="{{ex}}" y1="260" x2="{{ex}}" y2="{{ey}}"
          stroke="#e74c3c" stroke-width="2.5"
          stroke-dasharray="200" stroke-dashoffset="200"
          marker-end="url(#{{asset_id}}-arr-red)"/>
    <text id="{{asset_id}}-label2" x="{{ex_mid2}}" y="{{ey_mid}}"
          fill="#e74c3c" font-size="12" text-anchor="middle" opacity="0">{{b}}·e₂</text>

    <!-- v 합벡터 (애니메이션) -->
    <line id="{{asset_id}}-vec"
          x1="210" y1="260" x2="{{ex}}" y2="{{ey}}"
          stroke="#f39c12" stroke-width="3"
          stroke-dasharray="300" stroke-dashoffset="300"
          marker-end="url(#{{asset_id}}-arr-gold)"/>
    <text id="{{asset_id}}-labelv" x="{{ex_label}}" y="{{ey_label}}"
          fill="#f39c12" font-size="13" font-weight="bold" opacity="0">v⃗</text>

    <!-- 수식 -->
    <text id="{{asset_id}}-eq" x="210" y="30" text-anchor="middle"
          fill="#95a5a6" font-size="13" opacity="0">
      v⃗ = {{a}}·e₁ + {{b}}·e₂
    </text>
  </svg>
  <div class="anim-ctrl" style="text-align:center; margin-top:0.5em;">
    <button class="abtn" onclick="playDecomp_{{asset_id}}()">분해 보기 ▶</button>
    <button class="abtn gray" onclick="resetDecomp_{{asset_id}}()">↺</button>
  </div>
</div>
```

```javascript
window['playDecomp_{{asset_id}}'] = function() {
  const id = '{{asset_id}}';
  gsap.to('#' + id + '-comp1',   { strokeDashoffset: 0, duration: 0.7, ease: 'power2.out' });
  gsap.to('#' + id + '-label1',  { opacity: 1, duration: 0.4, delay: 0.5 });
  gsap.to('#' + id + '-comp2',   { strokeDashoffset: 0, duration: 0.7, delay: 0.8, ease: 'power2.out' });
  gsap.to('#' + id + '-label2',  { opacity: 1, duration: 0.4, delay: 1.3 });
  gsap.to('#' + id + '-vec',     { strokeDashoffset: 0, duration: 0.8, delay: 1.7, ease: 'power2.out' });
  gsap.to('#' + id + '-labelv',  { opacity: 1, duration: 0.4, delay: 2.3 });
  gsap.to('#' + id + '-eq',      { opacity: 1, duration: 0.5, delay: 2.5 });
};

window['resetDecomp_{{asset_id}}'] = function() {
  const id = '{{asset_id}}';
  ['comp1','comp2','vec'].forEach(k => {
    gsap.set('#' + id + '-' + k, { strokeDashoffset: 200 });
  });
  ['label1','label2','labelv','eq'].forEach(k => {
    gsap.set('#' + id + '-' + k, { opacity: 0 });
  });
};
```

---

### `parabola_focus`
포물선 **y² = 4px** 위의 점 P에서 초점 F까지의 거리와 준선까지의 거리가
항상 같음을 실시간으로 표시. 슬라이더로 점 P의 y좌표를 이동한다.

```html
<div id="{{asset_id}}-wrap" style="width:100%; max-width:480px; margin:0 auto;">
  <div id="{{asset_id}}-canvas-holder"></div>
  <div style="font-size:0.8em; margin-top:0.5em; text-align:center;">
    <label>점 P의 y좌표</label>
    <input type="range" min="-{{range_y}}" max="{{range_y}}" step="0.5"
           value="{{init_y}}" id="{{asset_id}}-py"
           oninput="updateParabola_{{asset_id}}(this.value)">
    <span id="{{asset_id}}-pyv">{{init_y}}</span>
  </div>
  <div id="{{asset_id}}-dist"
       style="font-size:0.82em; color:#f39c12; text-align:center; margin-top:0.3em;"></div>
</div>
```

```javascript
(function() {
  const wrap = document.getElementById('{{asset_id}}-wrap');
  const w = Math.min(wrap.clientWidth, 480);
  const h = Math.min(w * 0.625, 300);
  const p_param = {{p_val}};

  const sketch = function(p) {
    const ox = w * 0.38, oy = h / 2;
    const scale = Math.min(w, h) / (p_param * 10);

    p.setup = function() {
      const cnv = p.createCanvas(w, h);
      cnv.parent('{{asset_id}}-canvas-holder');
    };

    p.draw = function() {
      p.background(26, 26, 46);
      // 축
      p.stroke(80, 80, 100); p.strokeWeight(1);
      p.line(0, oy, w, oy); p.line(ox, 0, ox, h);

      // 준선 x = -p
      const directrix_x = ox - p_param * scale;
      p.stroke(150, 80, 80); p.strokeWeight(1.5);
      p.drawingContext.setLineDash([6, 4]);
      p.line(directrix_x, 0, directrix_x, h);
      p.drawingContext.setLineDash([]);
      p.fill(200, 100, 100); p.noStroke(); p.textSize(11);
      p.text('준선 x=−' + p_param, directrix_x + 3, 18);

      // 초점 F(p, 0)
      const focus_x = ox + p_param * scale, focus_y = oy;
      p.fill(243, 156, 18); p.noStroke();
      p.circle(focus_x, focus_y, 10);
      p.textSize(12); p.textAlign(p.LEFT);
      p.text('F(' + p_param + ',0)', focus_x + 6, focus_y - 4);

      // 포물선 y² = 4px
      p.stroke(52, 152, 219); p.strokeWeight(2); p.noFill();
      p.beginShape();
      for (let py = -h / 2; py <= h / 2; py += 2) {
        const px_math = py * py / (4 * p_param);
        const sx = ox + px_math * scale;
        const sy = oy - py * scale;
        if (sx >= 0 && sx <= w) p.vertex(sx, sy);
      }
      p.endShape();

      // 점 P
      const py_val = parseFloat(document.getElementById('{{asset_id}}-py').value);
      const px_val = py_val * py_val / (4 * p_param);
      const Px = ox + px_val * scale, Py = oy - py_val * scale;

      p.fill(46, 204, 113); p.noStroke();
      p.circle(Px, Py, 12);
      p.textSize(12); p.textAlign(p.LEFT);
      p.text('P', Px + 6, Py - 4);

      // PF 거리
      p.stroke(243, 156, 18); p.strokeWeight(2);
      p.line(Px, Py, focus_x, focus_y);

      // 준선까지 거리
      p.stroke(231, 76, 60); p.strokeWeight(2);
      p.line(Px, Py, directrix_x, Py);

      const distPF = Math.sqrt((Px - focus_x) ** 2 + (Py - focus_y) ** 2);
      const distDir = Math.abs(Px - directrix_x);
      const el = document.getElementById('{{asset_id}}-dist');
      if (el) {
        el.innerHTML =
          'PF = <b>' + (distPF / scale).toFixed(2) + '</b>' +
          '&emsp;준선까지 = <b>' + (distDir / scale).toFixed(2) + '</b>' +
          '&emsp;→ ' +
          (Math.abs(distPF - distDir) < 2
            ? '<span style="color:#2ecc71">두 거리 일치 ✓</span>'
            : '<span style="color:#e74c3c">계산 중...</span>');
      }
    };
  };

  window['updateParabola_{{asset_id}}'] = function(val) {
    document.getElementById('{{asset_id}}-pyv').textContent = val;
  };

  new p5(sketch);
})();
```

---

### `ellipse_foci`
타원 **x²/a² + y²/b² = 1** 위의 점 P에서 두 초점까지의 거리 합 = 2a를
실시간으로 표시. 슬라이더로 점 P를 이동한다.

```html
<div id="{{asset_id}}-wrap" style="width:100%; max-width:480px; margin:0 auto;">
  <div id="{{asset_id}}-canvas-holder"></div>
  <div style="font-size:0.8em; margin-top:0.5em; text-align:center;">
    <label>점 P 위치 (각도 °)</label>
    <input type="range" min="0" max="360" step="3" value="{{init_angle}}"
           id="{{asset_id}}-angle"
           oninput="updateEllipse_{{asset_id}}(this.value)">
    <span id="{{asset_id}}-anglev">{{init_angle}}°</span>
  </div>
  <div id="{{asset_id}}-dist"
       style="font-size:0.82em; color:#f39c12; text-align:center; margin-top:0.3em;"></div>
</div>
```

```javascript
(function() {
  const wrap = document.getElementById('{{asset_id}}-wrap');
  const w = Math.min(wrap.clientWidth, 480);
  const h = Math.min(w * 0.625, 300);
  const a = {{ellipse_a}}, b = {{ellipse_b}};
  const c = Math.sqrt(a * a - b * b);
  const cx = w / 2, cy = h / 2;
  const scale = Math.min(w / (a * 2.8), h / (b * 2.8));

  const sketch = function(p) {
    p.setup = function() {
      const cnv = p.createCanvas(w, h);
      cnv.parent('{{asset_id}}-canvas-holder');
    };

    p.draw = function() {
      p.background(26, 26, 46);
      // 축
      p.stroke(80, 80, 100); p.strokeWeight(1);
      p.line(0, cy, w, cy); p.line(cx, 0, cx, h);

      // 타원
      p.stroke(52, 152, 219); p.strokeWeight(2); p.noFill();
      p.ellipse(cx, cy, a * 2 * scale, b * 2 * scale);

      // 초점 F₁, F₂
      const f1x = cx - c * scale, f2x = cx + c * scale;
      p.fill(243, 156, 18); p.noStroke();
      p.circle(f1x, cy, 10); p.circle(f2x, cy, 10);
      p.textSize(11); p.textAlign(p.CENTER);
      p.text('F₁(−' + c.toFixed(1) + ',0)', f1x, cy + 18);
      p.text('F₂(' + c.toFixed(1) + ',0)', f2x, cy + 18);

      // 점 P
      const angle = parseFloat(document.getElementById('{{asset_id}}-angle').value);
      const rad = angle * Math.PI / 180;
      const Px = cx + a * Math.cos(rad) * scale;
      const Py = cy - b * Math.sin(rad) * scale;

      p.fill(46, 204, 113); p.noStroke();
      p.circle(Px, Py, 12);
      p.textSize(12); p.textAlign(p.LEFT);
      p.text('P', Px + 6, Py - 4);

      // PF₁, PF₂ 선분
      p.stroke(231, 76, 60); p.strokeWeight(2);
      p.line(Px, Py, f1x, cy);
      p.stroke(46, 204, 113); p.strokeWeight(2);
      p.line(Px, Py, f2x, cy);

      const d1 = Math.sqrt((Px - f1x) ** 2 + (Py - cy) ** 2) / scale;
      const d2 = Math.sqrt((Px - f2x) ** 2 + (Py - cy) ** 2) / scale;
      const el = document.getElementById('{{asset_id}}-dist');
      if (el) {
        el.innerHTML =
          'PF₁ = <span style="color:#e74c3c"><b>' + d1.toFixed(2) + '</b></span>' +
          ' + PF₂ = <span style="color:#2ecc71"><b>' + d2.toFixed(2) + '</b></span>' +
          ' = <b>' + (d1 + d2).toFixed(2) + '</b>' +
          ' (2a = ' + (2 * a) + ')' +
          (Math.abs(d1 + d2 - 2 * a) < 0.05
            ? '  <span style="color:#2ecc71">✓</span>' : '');
      }
    };
  };

  window['updateEllipse_{{asset_id}}'] = function(val) {
    document.getElementById('{{asset_id}}-anglev').textContent = val + '°';
  };

  new p5(sketch);
})();
```

---

### `hyperbola_def`
쌍곡선 **x²/a² − y²/b² = 1** 위의 점 P에서 두 초점까지의 거리 차의 절댓값 = 2a를
슬라이더로 점을 이동하며 실시간으로 표시.

```html
<div id="{{asset_id}}-wrap" style="width:100%; max-width:480px; margin:0 auto;">
  <div id="{{asset_id}}-canvas-holder"></div>
  <div style="font-size:0.8em; margin-top:0.5em; text-align:center;">
    <label>점 P 위치 (t 파라미터)</label>
    <input type="range" min="-3" max="3" step="0.1" value="{{init_t}}"
           id="{{asset_id}}-t"
           oninput="updateHyperbola_{{asset_id}}(this.value)">
    <span id="{{asset_id}}-tv">{{init_t}}</span>
  </div>
  <div id="{{asset_id}}-dist"
       style="font-size:0.82em; color:#f39c12; text-align:center; margin-top:0.3em;"></div>
</div>
```

```javascript
(function() {
  const wrap = document.getElementById('{{asset_id}}-wrap');
  const w = Math.min(wrap.clientWidth, 480);
  const h = Math.min(w * 0.625, 300);
  const a = {{hyp_a}}, b = {{hyp_b}};
  const c = Math.sqrt(a * a + b * b);
  const cx = w / 2, cy = h / 2;
  const scale = Math.min(w / (c * 3.5), h / (b * 3.5));

  const sketch = function(p) {
    p.setup = function() {
      const cnv = p.createCanvas(w, h);
      cnv.parent('{{asset_id}}-canvas-holder');
    };

    p.draw = function() {
      p.background(26, 26, 46);
      p.stroke(80, 80, 100); p.strokeWeight(1);
      p.line(0, cy, w, cy); p.line(cx, 0, cx, h);

      // 점근선
      p.stroke(60, 60, 80); p.strokeWeight(1);
      p.drawingContext.setLineDash([4, 4]);
      const slope = b / a;
      p.line(cx - w / 2, cy + w / 2 * slope, cx + w / 2, cy - w / 2 * slope);
      p.line(cx - w / 2, cy - w / 2 * slope, cx + w / 2, cy + w / 2 * slope);
      p.drawingContext.setLineDash([]);

      // 쌍곡선
      p.stroke(52, 152, 219); p.strokeWeight(2); p.noFill();
      for (let branch = -1; branch <= 1; branch += 2) {
        p.beginShape();
        for (let t = -2.5; t <= 2.5; t += 0.05) {
          const hx = a * Math.cosh(t) * branch;
          const hy = b * Math.sinh(t);
          const sx = cx + hx * scale, sy = cy - hy * scale;
          if (sx >= 0 && sx <= w) p.vertex(sx, sy);
        }
        p.endShape();
      }

      // 초점
      const f1x = cx - c * scale, f2x = cx + c * scale;
      p.fill(243, 156, 18); p.noStroke();
      p.circle(f1x, cy, 10); p.circle(f2x, cy, 10);
      p.textSize(11); p.textAlign(p.CENTER);
      p.text('F₁', f1x, cy + 17); p.text('F₂', f2x, cy + 17);

      // 점 P (쌍곡선 오른쪽 가지)
      const t_val = parseFloat(document.getElementById('{{asset_id}}-t').value);
      const Px = cx + a * Math.cosh(t_val) * scale;
      const Py = cy - b * Math.sinh(t_val) * scale;

      p.fill(46, 204, 113); p.noStroke();
      p.circle(Px, Py, 12);

      p.stroke(231, 76, 60); p.strokeWeight(2);
      p.line(Px, Py, f1x, cy);
      p.stroke(46, 204, 113); p.strokeWeight(2);
      p.line(Px, Py, f2x, cy);

      const d1 = Math.sqrt((Px - f1x) ** 2 + (Py - cy) ** 2) / scale;
      const d2 = Math.sqrt((Px - f2x) ** 2 + (Py - cy) ** 2) / scale;
      const diff = Math.abs(d1 - d2);
      const el = document.getElementById('{{asset_id}}-dist');
      if (el) {
        el.innerHTML =
          '|PF₁ − PF₂| = |' + d1.toFixed(2) + ' − ' + d2.toFixed(2) + '|' +
          ' = <b>' + diff.toFixed(2) + '</b>' +
          ' (2a = ' + (2 * a) + ')' +
          (Math.abs(diff - 2 * a) < 0.1
            ? '  <span style="color:#2ecc71">✓</span>' : '');
      }
    };
  };

  window['updateHyperbola_{{asset_id}}'] = function(val) {
    document.getElementById('{{asset_id}}-tv').textContent = val;
  };

  new p5(sketch);
})();
```

---

### `conic_comparison`
포물선, 타원, 쌍곡선을 같은 좌표계에 나란히 표시해 특징을 비교.
Chart.js를 사용하며 반응형 비율을 유지한다.

```html
<div id="{{asset_id}}-wrap"
     style="width:100%; max-width:560px; margin:0 auto; max-height:280px;">
  <canvas id="{{asset_id}}"></canvas>
</div>
<div style="font-size:0.75em; text-align:center; margin-top:0.5em; color:#95a5a6;">
  <span style="color:#3498db;">●</span> 포물선 y²=4x &nbsp;
  <span style="color:#2ecc71;">●</span> 타원 x²/9+y²/4=1 &nbsp;
  <span style="color:#e74c3c;">●</span> 쌍곡선 x²/4−y²/2=1
</div>
```

```javascript
(function() {
  function makePoints(fn, xMin, xMax, step) {
    const pts = [];
    for (let x = xMin; x <= xMax; x += step) {
      const y = fn(x);
      if (y !== null) pts.push({ x: parseFloat(x.toFixed(3)), y: parseFloat(y.toFixed(3)) });
    }
    return pts;
  }

  // 포물선 y² = 4x → 위 가지 y = 2√x
  const parabolaUpper = makePoints(x => x >= 0 ? 2 * Math.sqrt(x) : null, 0, 4.5, 0.05);
  const parabolaLower = makePoints(x => x >= 0 ? -2 * Math.sqrt(x) : null, 0, 4.5, 0.05);

  // 타원 x²/9 + y²/4 = 1 → y = 2√(1-x²/9), x ∈ [-3,3]
  const ellipseUpper = makePoints(x => Math.abs(x) <= 3 ? 2 * Math.sqrt(1 - x*x/9) : null, -3, 3, 0.05);
  const ellipseLower = makePoints(x => Math.abs(x) <= 3 ? -2 * Math.sqrt(1 - x*x/9) : null, -3, 3, 0.05);

  // 쌍곡선 x²/4 - y²/2 = 1 → y = √(2(x²/4-1)), |x| >= 2
  const hyperRight = makePoints(x => x >= 2 ? Math.sqrt(2 * (x*x/4 - 1)) : null, 2, 4.5, 0.05);
  const hyperLeft  = makePoints(x => x <= -2 ? Math.sqrt(2 * (x*x/4 - 1)) : null, -4.5, -2, 0.05);
  const hyperRightL = makePoints(x => x >= 2 ? -Math.sqrt(2 * (x*x/4 - 1)) : null, 2, 4.5, 0.05);
  const hyperLeftL  = makePoints(x => x <= -2 ? -Math.sqrt(2 * (x*x/4 - 1)) : null, -4.5, -2, 0.05);

  new Chart(document.getElementById('{{asset_id}}'), {
    type: 'scatter',
    data: {
      datasets: [
        { label: '포물선(상)',    data: parabolaUpper, borderColor: '#3498db', showLine: true, pointRadius: 0, borderWidth: 2 },
        { label: '포물선(하)',    data: parabolaLower, borderColor: '#3498db', showLine: true, pointRadius: 0, borderWidth: 2 },
        { label: '타원(상)',      data: ellipseUpper,  borderColor: '#2ecc71', showLine: true, pointRadius: 0, borderWidth: 2 },
        { label: '타원(하)',      data: ellipseLower,  borderColor: '#2ecc71', showLine: true, pointRadius: 0, borderWidth: 2 },
        { label: '쌍곡선(우상)', data: hyperRight,    borderColor: '#e74c3c', showLine: true, pointRadius: 0, borderWidth: 2 },
        { label: '쌍곡선(우하)', data: hyperRightL,   borderColor: '#e74c3c', showLine: true, pointRadius: 0, borderWidth: 2 },
        { label: '쌍곡선(좌상)', data: hyperLeft,     borderColor: '#e74c3c', showLine: true, pointRadius: 0, borderWidth: 2 },
        { label: '쌍곡선(좌하)', data: hyperLeftL,    borderColor: '#e74c3c', showLine: true, pointRadius: 0, borderWidth: 2 },
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: true,
      aspectRatio: 1.6,
      plugins: {
        legend: { display: false },
        tooltip: { enabled: false }
      },
      scales: {
        x: {
          min: -5, max: 5,
          grid: { color: 'rgba(255,255,255,0.08)' },
          ticks: { color: '#7f8c8d', font: { size: 10 } }
        },
        y: {
          min: -4, max: 4,
          grid: { color: 'rgba(255,255,255,0.08)' },
          ticks: { color: '#7f8c8d', font: { size: 10 } }
        }
      }
    }
  });
})();
```

---

### `space_vector_3d`
공간벡터를 SVG 등각투영(isometric) 좌표계에서 시각화.
x, y, z 축을 120° 간격으로 배치하고 벡터 화살표를 그린다.

```html
<div id="{{asset_id}}-wrap"
     style="width:100%; max-width:420px; margin:0 auto; overflow:hidden;">
  <svg id="{{asset_id}}" viewBox="0 0 420 360"
       preserveAspectRatio="xMidYMid meet"
       style="width:100%; height:auto; overflow:hidden; display:block; background:#1a1a2e;">
    <defs>
      <marker id="{{asset_id}}-ax" markerWidth="8" markerHeight="8"
              refX="6" refY="3" orient="auto">
        <path d="M0,0 L0,6 L8,3 z" fill="#e74c3c"/>
      </marker>
      <marker id="{{asset_id}}-ay" markerWidth="8" markerHeight="8"
              refX="6" refY="3" orient="auto">
        <path d="M0,0 L0,6 L8,3 z" fill="#2ecc71"/>
      </marker>
      <marker id="{{asset_id}}-az" markerWidth="8" markerHeight="8"
              refX="6" refY="3" orient="auto">
        <path d="M0,0 L0,6 L8,3 z" fill="#3498db"/>
      </marker>
      <marker id="{{asset_id}}-av" markerWidth="8" markerHeight="8"
              refX="6" refY="3" orient="auto">
        <path d="M0,0 L0,6 L8,3 z" fill="#f39c12"/>
      </marker>
    </defs>

    <!-- 등각투영 축 -->
    <!-- x축: 오른쪽 아래 (30°) -->
    <line x1="210" y1="200" x2="330" y2="270"
          stroke="#e74c3c" stroke-width="1.5" marker-end="url(#{{asset_id}}-ax)"/>
    <text x="336" y="274" fill="#e74c3c" font-size="12">x</text>

    <!-- y축: 오른쪽 위 (−30°) -->
    <line x1="210" y1="200" x2="330" y2="130"
          stroke="#2ecc71" stroke-width="1.5" marker-end="url(#{{asset_id}}-ay)"/>
    <text x="336" y="128" fill="#2ecc71" font-size="12">y</text>

    <!-- z축: 위쪽 (90°) -->
    <line x1="210" y1="200" x2="210" y2="60"
          stroke="#3498db" stroke-width="1.5" marker-end="url(#{{asset_id}}-az)"/>
    <text x="215" y="55" fill="#3498db" font-size="12">z</text>

    <!-- 공간벡터 v = ({{vx}}, {{vy}}, {{vz}}) -->
    <!-- 등각투영 변환: screen_x = ox + vx*cos(30°)*s - vy*cos(30°)*s -->
    <!--               screen_y = oy - vz*s + vx*sin(30°)*s + vy*sin(30°)*s (단순화) -->
    <line id="{{asset_id}}-vec"
          x1="210" y1="200"
          x2="{{iso_ex}}" y2="{{iso_ey}}"
          stroke="#f39c12" stroke-width="3" opacity="0"
          marker-end="url(#{{asset_id}}-av)"/>

    <!-- 성분 화살표 (점선) -->
    <line id="{{asset_id}}-cx"
          x1="210" y1="200" x2="{{iso_cx}}" y2="{{iso_cy}}"
          stroke="#e74c3c" stroke-width="1.5" stroke-dasharray="5,4" opacity="0"/>
    <line id="{{asset_id}}-cy"
          x1="{{iso_cx}}" y1="{{iso_cy}}" x2="{{iso_cxy}}" y2="{{iso_cyy}}"
          stroke="#2ecc71" stroke-width="1.5" stroke-dasharray="5,4" opacity="0"/>
    <line id="{{asset_id}}-cz"
          x1="{{iso_cxy}}" y1="{{iso_cyy}}" x2="{{iso_ex}}" y2="{{iso_ey}}"
          stroke="#3498db" stroke-width="1.5" stroke-dasharray="5,4" opacity="0"/>

    <!-- 라벨 -->
    <text id="{{asset_id}}-label"
          x="{{iso_ex_label}}" y="{{iso_ey_label}}"
          fill="#f39c12" font-size="13" font-weight="bold" opacity="0">
      v⃗({{vx}},{{vy}},{{vz}})
    </text>
    <text x="210" y="30" text-anchor="middle"
          fill="#95a5a6" font-size="12">
      등각투영 — 공간벡터 v⃗ = ({{vx}}, {{vy}}, {{vz}})
    </text>
  </svg>
  <div class="anim-ctrl" style="text-align:center; margin-top:0.5em;">
    <button class="abtn" onclick="playVec3d_{{asset_id}}()">벡터 표시 ▶</button>
    <button class="abtn gray" onclick="resetVec3d_{{asset_id}}()">↺</button>
  </div>
</div>
```

```javascript
window['playVec3d_{{asset_id}}'] = function() {
  const id = '{{asset_id}}';
  gsap.to('#' + id + '-cx',    { opacity: 1, duration: 0.5 });
  gsap.to('#' + id + '-cy',    { opacity: 1, duration: 0.5, delay: 0.5 });
  gsap.to('#' + id + '-cz',    { opacity: 1, duration: 0.5, delay: 1.0 });
  gsap.to('#' + id + '-vec',   { opacity: 1, duration: 0.6, delay: 1.5 });
  gsap.to('#' + id + '-label', { opacity: 1, duration: 0.4, delay: 2.0 });
};

window['resetVec3d_{{asset_id}}'] = function() {
  const id = '{{asset_id}}';
  ['cx','cy','cz','vec','label'].forEach(k => {
    gsap.set('#' + id + '-' + k, { opacity: 0 });
  });
};
```

---

### `cross_product_visual`
두 벡터 **a⃗**, **b⃗**가 이루는 평행사변형을 SVG로 시각화하고,
외적의 크기 |**a⃗** × **b⃗**| = |**a⃗**||**b⃗**|sinθ = 평행사변형 넓이임을 표시.

```html
<div id="{{asset_id}}-wrap"
     style="width:100%; max-width:420px; margin:0 auto; overflow:hidden;">
  <svg id="{{asset_id}}" viewBox="0 0 420 300"
       preserveAspectRatio="xMidYMid meet"
       style="width:100%; height:auto; overflow:hidden; display:block; background:#1a1a2e;">
    <defs>
      <marker id="{{asset_id}}-ma" markerWidth="8" markerHeight="8"
              refX="6" refY="3" orient="auto">
        <path d="M0,0 L0,6 L8,3 z" fill="#3498db"/>
      </marker>
      <marker id="{{asset_id}}-mb" markerWidth="8" markerHeight="8"
              refX="6" refY="3" orient="auto">
        <path d="M0,0 L0,6 L8,3 z" fill="#e74c3c"/>
      </marker>
    </defs>

    <!-- 평행사변형 채우기 -->
    <polygon id="{{asset_id}}-para"
             points="{{ox}},{{oy}} {{ax_tip}},{{ay_tip}} {{ab_tip}},{{ab_tipy}} {{bx_tip}},{{by_tip}}"
             fill="rgba(243,156,18,0.18)" stroke="#f39c12" stroke-width="1.5" opacity="0"/>

    <!-- a⃗ -->
    <line id="{{asset_id}}-va"
          x1="{{ox}}" y1="{{oy}}" x2="{{ax_tip}}" y2="{{ay_tip}}"
          stroke="#3498db" stroke-width="2.5" opacity="0"
          marker-end="url(#{{asset_id}}-ma)"/>
    <text id="{{asset_id}}-la"
          x="{{ax_label}}" y="{{ay_label}}"
          fill="#3498db" font-size="13" font-weight="bold" opacity="0">a⃗</text>

    <!-- b⃗ -->
    <line id="{{asset_id}}-vb"
          x1="{{ox}}" y1="{{oy}}" x2="{{bx_tip}}" y2="{{by_tip}}"
          stroke="#e74c3c" stroke-width="2.5" opacity="0"
          marker-end="url(#{{asset_id}}-mb)"/>
    <text id="{{asset_id}}-lb"
          x="{{bx_label}}" y="{{by_label}}"
          fill="#e74c3c" font-size="13" font-weight="bold" opacity="0">b⃗</text>

    <!-- 높이 점선 -->
    <line id="{{asset_id}}-height"
          x1="{{ax_tip}}" y1="{{ay_tip}}" x2="{{ax_tip}}" y2="{{oy}}"
          stroke="#2ecc71" stroke-width="1.5" stroke-dasharray="5,4" opacity="0"/>
    <text id="{{asset_id}}-lh"
          x="{{hx_label}}" y="{{hy_label}}"
          fill="#2ecc71" font-size="11" opacity="0">|a⃗|sinθ</text>

    <!-- 각도 호 -->
    <text id="{{asset_id}}-theta-label"
          x="{{theta_lx}}" y="{{theta_ly}}"
          fill="#9b59b6" font-size="12" opacity="0">θ</text>

    <!-- 수식 -->
    <text id="{{asset_id}}-formula"
          x="210" y="28" text-anchor="middle"
          fill="#f39c12" font-size="13" opacity="0">
      |a⃗×b⃗| = |a⃗||b⃗|sinθ = 평행사변형 넓이
    </text>
    <text id="{{asset_id}}-area"
          x="210" y="48" text-anchor="middle"
          fill="#f39c12" font-size="12" opacity="0">
      넓이 = {{area_val}}
    </text>
  </svg>
  <div class="anim-ctrl" style="text-align:center; margin-top:0.5em;">
    <button class="abtn" onclick="playCross_{{asset_id}}()">외적 시각화 ▶</button>
    <button class="abtn gray" onclick="resetCross_{{asset_id}}()">↺</button>
  </div>
</div>
```

```javascript
window['playCross_{{asset_id}}'] = function() {
  const id = '{{asset_id}}';
  gsap.to('#' + id + '-va',           { opacity: 1, duration: 0.5 });
  gsap.to('#' + id + '-la',           { opacity: 1, duration: 0.4, delay: 0.3 });
  gsap.to('#' + id + '-vb',           { opacity: 1, duration: 0.5, delay: 0.6 });
  gsap.to('#' + id + '-lb',           { opacity: 1, duration: 0.4, delay: 0.9 });
  gsap.to('#' + id + '-para',         { opacity: 1, duration: 0.6, delay: 1.2 });
  gsap.to('#' + id + '-height',       { opacity: 1, duration: 0.4, delay: 1.8 });
  gsap.to('#' + id + '-lh',           { opacity: 1, duration: 0.3, delay: 2.1 });
  gsap.to('#' + id + '-theta-label',  { opacity: 1, duration: 0.3, delay: 2.3 });
  gsap.to('#' + id + '-formula',      { opacity: 1, duration: 0.5, delay: 2.6 });
  gsap.to('#' + id + '-area',         { opacity: 1, duration: 0.5, delay: 3.0 });
};

window['resetCross_{{asset_id}}'] = function() {
  const id = '{{asset_id}}';
  ['va','la','vb','lb','para','height','lh','theta-label','formula','area'].forEach(k => {
    gsap.set('#' + id + '-' + k, { opacity: 0 });
  });
};
```

---

## 기하 주요 수치 파라미터 (권장값)

```yaml
# 평면벡터 예시
vector_2d:
  ax: 2, ay: 1   # a⃗ = (2, 1)
  bx: -1, by: 2  # b⃗ = (-1, 2)
  합벡터: (1, 3)

dot_product_visual:
  a_len: 3, b_len: 2
  theta_deg: 60
  내적: 3×2×cos60° = 3

vector_decomposition:
  a: 3, b: 2       # v⃗ = 3e₁ + 2e₂
  기저: e₁=(1,0), e₂=(0,1)

# 이차곡선 예시
parabola_focus:
  p_val: 1         # y² = 4x, 초점 F(1,0), 준선 x=-1
  range_y: 4
  init_y: 2

ellipse_foci:
  ellipse_a: 5, ellipse_b: 4   # c = 3, F(±3, 0)
  init_angle: 60
  2a = 10 검증: PF₁+PF₂=10

hyperbola_def:
  hyp_a: 2, hyp_b: 2   # c = 2√2, F(±2√2, 0)
  init_t: 0.8
  2a = 4 검증: |PF₁-PF₂|=4

conic_comparison:
  포물선: y²=4x (p=1)
  타원: x²/9+y²/4=1 (a=3,b=2,c=√5)
  쌍곡선: x²/4-y²/2=1 (a=2,b=√2,c=√6)

# 공간벡터 예시
space_vector_3d:
  vx: 2, vy: 1, vz: 3
  등각투영 스케일: 60px per unit
  # iso 변환 (단순화):
  # screen_x = ox + vx*cos30°*s + vy*cos150°*s
  # screen_y = oy - vz*s - vx*sin30°*s + vy*sin30°*s

cross_product_visual:
  a⃗: (3, 0, 0)   # 화면에서 (3,0) 방향
  b⃗: (1, 2, 0)   # 화면에서 (1,2) 방향
  |a⃗×b⃗|: |3×2×sin(arctan(2/1))| = 6 (넓이=6)
  사이각 θ: arctan(2/3) ≈ 33.7°
```
