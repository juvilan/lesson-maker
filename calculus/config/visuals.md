# 미적분 — 시각화 카탈로그 플러그인

visual_creator.md 에이전트가 이 파일을 로드하여
미적분 특화 시각화를 생성할 때 사용한다.
극한(엡실론-델타), 미분, 도함수, 적분, 리만 합, 미적분 기본 정리 단원에 특화.

---

## 지원 시각화 타입 목록

| 타입명 | 설명 | 라이브러리 |
|--------|------|----------|
| `limit_two_sided` | 좌극한/우극한 시각화. x→a± 접근 경로를 두 색 화살표로 표시 | p5.js |
| `derivative_slope_tracer` | f(x)와 f'(x)를 위아래 두 패널로 동시 표시. 슬라이더로 접선 추적 | p5.js |
| `riemann_sum` | 리만 합 시각화. 슬라이더로 직사각형 수 n 조절 + 합 수치 표시 | p5.js |
| `integral_area` | 정적분 넓이. a~b 구간 fill 색칠 | Chart.js |
| `ftc_visual` | 미적분 기본 정리. F(b)-F(a)=∫f(x)dx 관계를 두 그래프로 표현 | SVG |
| `chain_rule_diagram` | 합성함수 미분 구조도. u=g(x), y=f(u) 단계 화살표 | SVG |
| `related_rates_diagram` | 관련 변화율 상황 다이어그램. 슬라이더 애니메이션 | p5.js |

---

## 각 타입별 코드 패턴

### `limit_two_sided`
좌극한(x→a⁻)과 우극한(x→a⁺)의 접근 경로를 각각 다른 색 화살표로 표시.
좌극한 값과 우극한 값이 일치하면 극한이 존재함을 시각적으로 확인.
컨테이너 너비를 읽어 반응형으로 동작.

```html
<div id="{{asset_id}}-wrap" style="width:100%; max-width:480px; margin:0 auto;"></div>
<div style="font-size:0.8em; text-align:center; margin-top:0.4em;">
  <span style="color:#3498db;">■ 좌극한 x→{{a}}⁻</span>
  &nbsp;&nbsp;
  <span style="color:#e74c3c;">■ 우극한 x→{{a}}⁺</span>
</div>
<div id="{{asset_id}}-result" style="font-size:0.82em; color:#2ecc71; text-align:center; margin-top:0.3em;"></div>
<script>
(function() {
  const wrap = document.getElementById('{{asset_id}}-wrap');
  const w = Math.min(wrap.clientWidth, 480);
  const h = Math.min(w * 0.625, 300);
  const a = {{a}};
  const leftLimit = {{left_limit}};
  const rightLimit = {{right_limit}};
  const steps = 8;

  const sk = new p5(function(p) {
    const m = { l: 50, r: 20, t: 20, b: 40 };
    const xMin = {{x_min}}, xMax = {{x_max}};
    const yMin = {{y_min}}, yMax = {{y_max}};

    function toCanvasX(x) { return m.l + (x - xMin) / (xMax - xMin) * (w - m.l - m.r); }
    function toCanvasY(y) { return h - m.b - (y - yMin) / (yMax - yMin) * (h - m.t - m.b); }
    function evalF(x) { return {{함수식}}; }

    p.setup = function() {
      const cnv = p.createCanvas(w, h);
      cnv.parent('{{asset_id}}-wrap');
      p.noLoop();
      p.draw();
    };

    p.draw = function() {
      p.background(26, 26, 46);

      // 축
      p.stroke(80); p.strokeWeight(1);
      p.line(m.l, h - m.b, w - m.r, h - m.b);
      p.line(m.l, m.t, m.l, h - m.b);
      p.fill(180); p.noStroke(); p.textSize(11); p.textAlign(p.CENTER);
      p.text('x', w/2, h - 5);
      p.text(xMin, m.l, h - m.b + 14);
      p.text(xMax, w - m.r, h - m.b + 14);

      // 함수 곡선
      p.noFill(); p.stroke(149, 165, 166); p.strokeWeight(1.5);
      p.beginShape();
      for (let px = m.l; px <= w - m.r; px++) {
        const x = xMin + (px - m.l) / (w - m.l - m.r) * (xMax - xMin);
        if (Math.abs(x - a) < 0.02) continue;
        const y = evalF(x);
        if (y < yMin || y > yMax) continue;
        p.vertex(px, toCanvasY(y));
      }
      p.endShape();

      // 좌극한 화살표 (파란색)
      p.stroke(52, 152, 219); p.strokeWeight(2);
      for (let i = 1; i <= steps; i++) {
        const x = a - i * 0.12;
        const y = evalF(x);
        const px = toCanvasX(x);
        const py = toCanvasY(y);
        const nx = toCanvasX(x + 0.06);
        const ny = toCanvasY(evalF(x + 0.06));
        p.line(px, py, nx, ny);
        // 화살촉
        if (i === 1) {
          const angle = Math.atan2(ny - py, nx - px);
          p.fill(52, 152, 219); p.noStroke();
          p.triangle(nx, ny,
            nx - 8*Math.cos(angle-0.4), ny - 8*Math.sin(angle-0.4),
            nx - 8*Math.cos(angle+0.4), ny - 8*Math.sin(angle+0.4));
        }
      }

      // 우극한 화살표 (빨간색)
      p.stroke(231, 76, 60); p.strokeWeight(2);
      for (let i = 1; i <= steps; i++) {
        const x = a + i * 0.12;
        const y = evalF(x);
        const px = toCanvasX(x);
        const py = toCanvasY(y);
        const nx = toCanvasX(x - 0.06);
        const ny = toCanvasY(evalF(x - 0.06));
        p.line(px, py, nx, ny);
        if (i === 1) {
          const angle = Math.atan2(ny - py, nx - px);
          p.fill(231, 76, 60); p.noStroke();
          p.triangle(nx, ny,
            nx - 8*Math.cos(angle-0.4), ny - 8*Math.sin(angle-0.4),
            nx - 8*Math.cos(angle+0.4), ny - 8*Math.sin(angle+0.4));
        }
      }

      // a에서 열린 원 (극한점)
      const ax = toCanvasX(a);
      const lx = toCanvasY(leftLimit);
      p.noFill(); p.stroke(255, 255, 255); p.strokeWeight(2);
      p.ellipse(ax, lx, 10, 10);

      // x=a 수직선
      p.stroke(120); p.strokeWeight(1); p.drawingContext.setLineDash([4, 3]);
      p.line(ax, m.t, ax, h - m.b);
      p.drawingContext.setLineDash([]);
      p.fill(200); p.noStroke(); p.textSize(11); p.textAlign(p.CENTER);
      p.text('a=' + a, ax, h - m.b + 14);
    };
  });

  // 결과 레이블
  const resultEl = document.getElementById('{{asset_id}}-result');
  if (resultEl) {
    if (Math.abs(leftLimit - rightLimit) < 1e-9) {
      resultEl.textContent = '좌극한 = 우극한 = ' + leftLimit + '  →  극한 존재 ✓';
      resultEl.style.color = '#2ecc71';
    } else {
      resultEl.textContent = '좌극한(' + leftLimit + ') ≠ 우극한(' + rightLimit + ')  →  극한 없음 ✗';
      resultEl.style.color = '#e74c3c';
    }
  }
})();
</script>
```

---

### `derivative_slope_tracer`
위 패널: f(x) 곡선 + x₀에서의 접선.
아래 패널: f'(x) 곡선 + 현재 x₀에서의 점.
슬라이더로 x₀를 이동하면 두 패널이 동기화.

```html
<div id="{{asset_id}}-wrap" style="width:100%; max-width:480px; margin:0 auto;"></div>
<div class="param-slider-group" style="margin-top:0.5em;">
  <label>x₀</label>
  <input type="range" min="{{x_min}}" max="{{x_max}}" step="0.05" value="{{x0}}"
         id="{{asset_id}}-sl" oninput="updateSlope_{{asset_id}}(this.value)">
  <span id="{{asset_id}}-sv">{{x0}}</span>
</div>
<div id="{{asset_id}}-info" style="font-size:0.8em; color:#f39c12; text-align:center; margin-top:0.3em;"></div>
<script>
(function() {
  const wrap = document.getElementById('{{asset_id}}-wrap');
  const w = Math.min(wrap.clientWidth, 480);
  const h = Math.min(w * 0.625, 300);
  const panelH = Math.floor(h / 2) - 4;
  const xMin = {{x_min}}, xMax = {{x_max}};
  const yMin = {{y_min}}, yMax = {{y_max}};
  const dyMin = {{dy_min}}, dyMax = {{dy_max}};
  const m = { l: 44, r: 12, t: 14, b: 28 };

  function evalF(x)  { return {{함수식}}; }
  function evalDF(x) { return {{도함수식}}; }

  function toX(x, pW) { return m.l + (x - xMin) / (xMax - xMin) * (pW - m.l - m.r); }
  function toY(y, pH, yMn, yMx) { return pH - m.b - (y - yMn) / (yMx - yMn) * (pH - m.t - m.b); }

  let currentX0 = {{x0}};
  let sk;

  function redraw() {
    if (sk) sk.remove();
    sk = new p5(function(p) {
      p.setup = function() {
        const cnv = p.createCanvas(w, panelH * 2 + 8);
        cnv.parent('{{asset_id}}-wrap');
        p.noLoop();
        drawPanels(p);
      };
    });
  }

  function drawPanels(p) {
    p.background(26, 26, 46);
    const x0 = currentX0;
    const fx0 = evalF(x0);
    const dfx0 = evalDF(x0);

    // --- 상단 패널: f(x) ---
    p.stroke(80); p.strokeWeight(1);
    p.line(m.l, panelH - m.b, w - m.r, panelH - m.b);
    p.line(m.l, m.t, m.l, panelH - m.b);
    p.fill(150); p.noStroke(); p.textSize(10); p.textAlign(p.LEFT);
    p.text('f(x)', m.l + 4, m.t + 10);

    p.noFill(); p.stroke(149, 165, 166); p.strokeWeight(1.5);
    p.beginShape();
    for (let px = m.l; px <= w - m.r; px++) {
      const x = xMin + (px - m.l) / (w - m.l - m.r) * (xMax - xMin);
      const y = evalF(x);
      if (y < yMin - 0.5 || y > yMax + 0.5) continue;
      p.vertex(px, toY(y, panelH, yMin, yMax));
    }
    p.endShape();

    // 접선
    p.stroke(243, 156, 18); p.strokeWeight(2);
    const tLen = (xMax - xMin) * 0.25;
    const tx0 = x0 - tLen, ty0 = fx0 + dfx0 * (tx0 - x0);
    const tx1 = x0 + tLen, ty1 = fx0 + dfx0 * (tx1 - x0);
    p.line(toX(tx0, w), toY(ty0, panelH, yMin, yMax),
           toX(tx1, w), toY(ty1, panelH, yMin, yMax));

    // x₀ 점
    p.fill(243, 156, 18); p.noStroke();
    p.ellipse(toX(x0, w), toY(fx0, panelH, yMin, yMax), 8, 8);

    // x₀ 수직선
    p.stroke(120); p.strokeWeight(1); p.drawingContext.setLineDash([3, 3]);
    p.line(toX(x0, w), m.t, toX(x0, w), panelH - m.b);
    p.drawingContext.setLineDash([]);

    // --- 하단 패널: f'(x) ---
    const offY = panelH + 8;
    p.stroke(80); p.strokeWeight(1);
    p.line(m.l, offY + panelH - m.b, w - m.r, offY + panelH - m.b);
    p.line(m.l, offY + m.t, m.l, offY + panelH - m.b);
    p.fill(150); p.noStroke(); p.textSize(10); p.textAlign(p.LEFT);
    p.text("f'(x)", m.l + 4, offY + m.t + 10);

    p.noFill(); p.stroke(52, 152, 219); p.strokeWeight(1.5);
    p.beginShape();
    for (let px = m.l; px <= w - m.r; px++) {
      const x = xMin + (px - m.l) / (w - m.l - m.r) * (xMax - xMin);
      const dy = evalDF(x);
      if (dy < dyMin - 0.5 || dy > dyMax + 0.5) continue;
      p.vertex(px, offY + toY(dy, panelH, dyMin, dyMax));
    }
    p.endShape();

    // x₀에서 f'(x₀) 점
    p.fill(231, 76, 60); p.noStroke();
    p.ellipse(toX(x0, w), offY + toY(dfx0, panelH, dyMin, dyMax), 9, 9);

    // 수직선
    p.stroke(120); p.strokeWeight(1); p.drawingContext.setLineDash([3, 3]);
    p.line(toX(x0, w), offY + m.t, toX(x0, w), offY + panelH - m.b);
    p.drawingContext.setLineDash([]);

    // 정보 레이블
    const infoEl = document.getElementById('{{asset_id}}-info');
    if (infoEl) {
      infoEl.textContent =
        `x₀ = ${x0.toFixed(2)},  f(x₀) = ${fx0.toFixed(3)},  f'(x₀) = ${dfx0.toFixed(3)}  (기울기)`;
    }
  }

  window['updateSlope_{{asset_id}}'] = function(val) {
    currentX0 = parseFloat(val);
    document.getElementById('{{asset_id}}-sv').textContent = currentX0.toFixed(2);
    redraw();
  };

  redraw();
})();
</script>
```

---

### `riemann_sum`
슬라이더로 직사각형 수 n을 조절하면 분할 직사각형이 실시간으로 갱신되고
리만 합 근삿값이 수치로 표시됨. n → ∞ 수렴 과정을 직관적으로 확인.

```html
<div id="{{asset_id}}-wrap" style="width:100%; max-width:480px; margin:0 auto;"></div>
<div class="param-slider-group" style="margin-top:0.5em;">
  <label>n (직사각형 수)</label>
  <input type="range" min="1" max="50" step="1" value="{{n}}"
         id="{{asset_id}}-sl" oninput="updateRiemann_{{asset_id}}(this.value)">
  <span id="{{asset_id}}-sv">{{n}}</span>
</div>
<div id="{{asset_id}}-sum" style="font-size:0.85em; color:#2ecc71; text-align:center; margin-top:0.3em;"></div>
<script>
(function() {
  const wrap = document.getElementById('{{asset_id}}-wrap');
  const w = Math.min(wrap.clientWidth, 480);
  const h = Math.min(w * 0.625, 300);
  const a = {{a}}, b = {{b}};
  const xMin = {{x_min}}, xMax = {{x_max}};
  const yMin = 0, yMax = {{y_max}};
  const m = { l: 44, r: 12, t: 16, b: 32 };
  const exactVal = {{exact_integral}};

  function evalF(x) { return {{함수식}}; }
  function toX(x) { return m.l + (x - xMin) / (xMax - xMin) * (w - m.l - m.r); }
  function toY(y) { return h - m.b - (y - yMin) / (yMax - yMin) * (h - m.t - m.b); }

  let currentN = {{n}};
  let sk;

  function redraw() {
    if (sk) sk.remove();
    sk = new p5(function(p) {
      p.setup = function() {
        const cnv = p.createCanvas(w, h);
        cnv.parent('{{asset_id}}-wrap');
        p.noLoop();

        p.background(26, 26, 46);

        // 직사각형 (좌끝 리만 합)
        const dx = (b - a) / currentN;
        let rSum = 0;
        for (let i = 0; i < currentN; i++) {
          const xi = a + i * dx;
          const yi = evalF(xi);
          rSum += yi * dx;
          const px = toX(xi);
          const pw = toX(xi + dx) - px;
          const py = toY(yi);
          const baseY = toY(0);
          p.fill(52, 152, 219, 120);
          p.stroke(52, 152, 219);
          p.strokeWeight(0.8);
          p.rect(px, py, pw, baseY - py);
        }

        // 함수 곡선 (위에 덮기)
        p.noFill(); p.stroke(243, 156, 18); p.strokeWeight(2);
        p.beginShape();
        for (let px = m.l; px <= w - m.r; px++) {
          const x = xMin + (px - m.l) / (w - m.l - m.r) * (xMax - xMin);
          const y = evalF(x);
          if (y < yMin - 0.2 || y > yMax + 0.2) continue;
          p.vertex(px, toY(y));
        }
        p.endShape();

        // 축
        p.stroke(80); p.strokeWeight(1);
        p.line(m.l, h - m.b, w - m.r, h - m.b);
        p.line(m.l, m.t, m.l, h - m.b);
        p.fill(180); p.noStroke(); p.textSize(11); p.textAlign(p.CENTER);
        p.text('a=' + a, toX(a), h - m.b + 14);
        p.text('b=' + b, toX(b), h - m.b + 14);

        // 구간 마킹
        p.stroke(150); p.strokeWeight(1); p.drawingContext.setLineDash([3, 3]);
        p.line(toX(a), m.t, toX(a), h - m.b);
        p.line(toX(b), m.t, toX(b), h - m.b);
        p.drawingContext.setLineDash([]);

        // 합 표시
        const sumEl = document.getElementById('{{asset_id}}-sum');
        if (sumEl) {
          const err = Math.abs(rSum - exactVal);
          sumEl.textContent =
            `Σ (n=${currentN}) ≈ ${rSum.toFixed(4)}  |  실제값 ${exactVal.toFixed(4)}  |  오차 ${err.toFixed(4)}`;
        }
      };
    });
  }

  window['updateRiemann_{{asset_id}}'] = function(val) {
    currentN = parseInt(val);
    document.getElementById('{{asset_id}}-sv').textContent = currentN;
    redraw();
  };

  redraw();
})();
</script>
```

---

### `integral_area`
정적분 ∫_a^b f(x)dx의 넓이를 Chart.js로 색칠.
구간 [a, b]만 fill 색으로 강조, 나머지는 투명.

```html
<div style="max-height:280px; position:relative;">
  <canvas id="{{asset_id}}"></canvas>
</div>
<div style="font-size:0.82em; color:#95a5a6; text-align:center; margin-top:0.4em;">
  ∫<sub>{{a}}</sub><sup>{{b}}</sup> {{함수_레이블}} dx ≈ <span style="color:#2ecc71;">{{exact_integral}}</span>
</div>
<script>
(function() {
  const a = {{a}}, b = {{b}};
  const step = 0.05;
  const labels = [], fData = [], fillData = [];

  for (let x = {{x_min}}; x <= {{x_max}} + 0.01; x += step) {
    const xr = Math.round(x * 1000) / 1000;
    labels.push(xr.toFixed(2));
    const y = {{함수식}};
    fData.push({ x: xr, y: y });
    if (xr >= a - 0.001 && xr <= b + 0.001) {
      fillData.push({ x: xr, y: y });
    } else {
      fillData.push({ x: xr, y: null });
    }
  }

  new Chart(document.getElementById('{{asset_id}}'), {
    type: 'line',
    data: {
      datasets: [
        {
          label: '{{함수_레이블}}',
          data: fData,
          borderColor: '#f39c12',
          borderWidth: 2,
          pointRadius: 0,
          fill: false,
          tension: 0.4,
          parsing: false
        },
        {
          label: '넓이',
          data: fillData,
          borderColor: 'transparent',
          backgroundColor: 'rgba(46,204,113,0.3)',
          borderWidth: 0,
          pointRadius: 0,
          fill: 'origin',
          tension: 0.4,
          parsing: false,
          spanGaps: false
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: true,
      aspectRatio: 1.6,
      plugins: {
        legend: { labels: { color: '#bdc3c7', boxWidth: 12 } }
      },
      scales: {
        x: {
          type: 'linear',
          ticks: { color: '#95a5a6', maxTicksLimit: 8 },
          grid: { color: 'rgba(255,255,255,0.05)' }
        },
        y: {
          ticks: { color: '#95a5a6' },
          grid: { color: 'rgba(255,255,255,0.05)' }
        }
      }
    }
  });
})();
</script>
```

---

### `ftc_visual`
미적분 기본 정리: F(b) - F(a) = ∫_a^b f(x)dx 관계.
왼쪽 SVG: f(x) 그래프 + 넓이 강조.
오른쪽 SVG: F(x) 그래프 + F(b), F(a) 높이 차 강조.

```html
<svg id="{{asset_id}}" viewBox="0 0 560 240"
     style="width:100%; max-width:560px; overflow:hidden; display:block; margin:0 auto;"
     preserveAspectRatio="xMidYMid meet">

  <!-- 왼쪽: f(x) 패널 -->
  <rect x="0" y="0" width="260" height="240" fill="#1a1a2e"/>
  <text x="130" y="18" text-anchor="middle" fill="#bdc3c7" font-size="12">f(x) — 피적분함수</text>

  <!-- 축 -->
  <line x1="30" y1="200" x2="250" y2="200" stroke="#555" stroke-width="1"/>
  <line x1="30" y1="30"  x2="30"  y2="200" stroke="#555" stroke-width="1"/>

  <!-- f(x) = {{f_label}} 곡선 경로 (SVG path) -->
  <path id="{{asset_id}}-fcurve" d="{{f_path}}"
        fill="none" stroke="#f39c12" stroke-width="2"/>

  <!-- a~b 넓이 채우기 -->
  <path id="{{asset_id}}-area" d="{{area_path}}"
        fill="rgba(46,204,113,0.3)" stroke="none"/>

  <!-- a, b 수직선 -->
  <line x1="{{ax_px}}" y1="30"  x2="{{ax_px}}" y2="200" stroke="#3498db" stroke-width="1.5" stroke-dasharray="4 3"/>
  <line x1="{{bx_px}}" y1="30"  x2="{{bx_px}}" y2="200" stroke="#e74c3c" stroke-width="1.5" stroke-dasharray="4 3"/>
  <text x="{{ax_px}}" y="215" text-anchor="middle" fill="#3498db" font-size="11">a={{a}}</text>
  <text x="{{bx_px}}" y="215" text-anchor="middle" fill="#e74c3c" font-size="11">b={{b}}</text>

  <!-- 넓이 레이블 -->
  <text x="130" y="230" text-anchor="middle" fill="#2ecc71" font-size="11">
    ∫f(x)dx = {{exact_integral}}
  </text>

  <!-- 오른쪽: F(x) 패널 -->
  <rect x="300" y="0" width="260" height="240" fill="#1a1a2e"/>
  <text x="430" y="18" text-anchor="middle" fill="#bdc3c7" font-size="12">F(x) — 원시함수</text>

  <!-- 축 -->
  <line x1="330" y1="200" x2="550" y2="200" stroke="#555" stroke-width="1"/>
  <line x1="330" y1="30"  x2="330" y2="200" stroke="#555" stroke-width="1"/>

  <!-- F(x) 곡선 -->
  <path id="{{asset_id}}-Fcurve" d="{{F_path}}"
        fill="none" stroke="#9b59b6" stroke-width="2"/>

  <!-- F(a), F(b) 수평선 -->
  <line x1="{{ax_Fpx}}" y1="{{Fa_py}}" x2="330" y2="{{Fa_py}}"
        stroke="#3498db" stroke-width="1.5" stroke-dasharray="4 3"/>
  <line x1="{{bx_Fpx}}" y1="{{Fb_py}}" x2="330" y2="{{Fb_py}}"
        stroke="#e74c3c" stroke-width="1.5" stroke-dasharray="4 3"/>

  <!-- F(a), F(b) 점 -->
  <circle cx="{{ax_Fpx}}" cy="{{Fa_py}}" r="4" fill="#3498db"/>
  <circle cx="{{bx_Fpx}}" cy="{{Fb_py}}" r="4" fill="#e74c3c"/>

  <!-- 높이 차 브라켓 -->
  <line x1="335" y1="{{Fa_py}}" x2="335" y2="{{Fb_py}}"
        stroke="#2ecc71" stroke-width="2"/>
  <text x="345" y="{{ftc_mid_py}}" fill="#2ecc71" font-size="11">F(b)-F(a)</text>
  <text x="430" y="230" text-anchor="middle" fill="#2ecc71" font-size="11">
    F({{b}})-F({{a}}) = {{exact_integral}}
  </text>

  <!-- 등호 연결 -->
  <text x="280" y="122" text-anchor="middle" fill="#f39c12" font-size="20" font-weight="bold">=</text>
</svg>
<div style="font-size:0.78em; color:#95a5a6; text-align:center; margin-top:0.4em;">
  미적분 기본 정리: F(b) - F(a) = ∫<sub>a</sub><sup>b</sup> f(x)dx
</div>
```

---

### `chain_rule_diagram`
합성함수 y = f(g(x))의 미분 연쇄 구조.
x → u=g(x) → y=f(u) 단계를 화살표로 연결.
각 단계에 du/dx, dy/du, dy/dx 레이블 표시.

```html
<svg id="{{asset_id}}" viewBox="0 0 500 160"
     style="width:100%; max-width:500px; overflow:hidden; display:block; margin:0 auto;"
     preserveAspectRatio="xMidYMid meet">

  <!-- 배경 -->
  <rect width="500" height="160" fill="#1a1a2e"/>

  <!-- 노드: x -->
  <circle cx="60" cy="80" r="36" fill="#2c3e50" stroke="#7f8c8d" stroke-width="2"/>
  <text x="60" y="76" text-anchor="middle" fill="#ecf0f1" font-size="14">x</text>
  <text x="60" y="92" text-anchor="middle" fill="#95a5a6" font-size="10">입력</text>

  <!-- 화살표: x → u -->
  <line x1="96" y1="80" x2="184" y2="80" stroke="#3498db" stroke-width="2"/>
  <polygon points="184,74 196,80 184,86" fill="#3498db"/>
  <text x="144" y="68" text-anchor="middle" fill="#3498db" font-size="11">u = {{g_expr}}</text>
  <text x="144" y="100" text-anchor="middle" fill="#3498db" font-size="10">du/dx = {{dg_expr}}</text>

  <!-- 노드: u = g(x) -->
  <circle cx="230" cy="80" r="40" fill="#2c3e50" stroke="#3498db" stroke-width="2"/>
  <text x="230" y="76" text-anchor="middle" fill="#3498db" font-size="13">u</text>
  <text x="230" y="91" text-anchor="middle" fill="#95a5a6" font-size="10">=g(x)</text>

  <!-- 화살표: u → y -->
  <line x1="270" y1="80" x2="358" y2="80" stroke="#e74c3c" stroke-width="2"/>
  <polygon points="358,74 370,80 358,86" fill="#e74c3c"/>
  <text x="314" y="68" text-anchor="middle" fill="#e74c3c" font-size="11">y = {{f_expr}}</text>
  <text x="314" y="100" text-anchor="middle" fill="#e74c3c" font-size="10">dy/du = {{df_expr}}</text>

  <!-- 노드: y = f(u) -->
  <circle cx="415" cy="80" r="40" fill="#2c3e50" stroke="#e74c3c" stroke-width="2"/>
  <text x="415" y="76" text-anchor="middle" fill="#e74c3c" font-size="13">y</text>
  <text x="415" y="91" text-anchor="middle" fill="#95a5a6" font-size="10">=f(u)</text>

  <!-- 체인 룰 결과 -->
  <rect x="60" y="128" width="380" height="24" rx="6" fill="rgba(243,156,18,0.12)" stroke="#f39c12" stroke-width="1"/>
  <text x="250" y="144" text-anchor="middle" fill="#f39c12" font-size="12">
    dy/dx = (dy/du) · (du/dx) = {{df_expr}} · {{dg_expr}} = {{chain_result}}
  </text>
</svg>
```

---

### `related_rates_diagram`
관련 변화율 상황(물탱크, 사다리 등)을 p5.js로 애니메이션.
슬라이더로 시간 t를 조절하면 상황이 갱신되고
관련 변화율 수치가 표시됨.

```html
<div id="{{asset_id}}-wrap" style="width:100%; max-width:480px; margin:0 auto;"></div>
<div class="param-slider-group" style="margin-top:0.5em;">
  <label>t (시간)</label>
  <input type="range" min="{{t_min}}" max="{{t_max}}" step="0.1" value="{{t0}}"
         id="{{asset_id}}-sl" oninput="updateRates_{{asset_id}}(this.value)">
  <span id="{{asset_id}}-sv">{{t0}}</span>
</div>
<div id="{{asset_id}}-rates" style="font-size:0.82em; color:#f39c12; text-align:center; margin-top:0.4em;"></div>
<script>
(function() {
  const wrap = document.getElementById('{{asset_id}}-wrap');
  const w = Math.min(wrap.clientWidth, 480);
  const h = Math.min(w * 0.625, 300);
  let currentT = {{t0}};
  let sk;

  // 상황: 사다리 (길이 L=5)가 벽에 기댄 채 미끄러짐
  // x(t) = {{x_expr}},  y(t) = sqrt(L²-x(t)²)
  const L = {{ladder_length}};

  function getXY(t) {
    const x = {{x_expr}};
    const y = Math.sqrt(Math.max(0, L*L - x*x));
    const dxdt = {{dx_dt_expr}};
    const dydt = -x / y * dxdt;
    return { x, y, dxdt, dydt };
  }

  function redraw() {
    if (sk) sk.remove();
    sk = new p5(function(p) {
      p.setup = function() {
        const cnv = p.createCanvas(w, h);
        cnv.parent('{{asset_id}}-wrap');
        p.noLoop();

        p.background(26, 26, 46);
        const { x, y, dxdt, dydt } = getXY(currentT);

        // 스케일 (단위 → 픽셀)
        const sc = Math.min((w - 60) / (L + 1), (h - 60) / (L + 1));
        const ox = 50, oy = h - 40;

        // 바닥, 벽
        p.stroke(100); p.strokeWeight(2);
        p.line(ox - 10, oy, ox + (L + 1) * sc, oy);  // 바닥
        p.line(ox, oy + 10, ox, oy - (L + 1) * sc);  // 벽

        // 사다리
        const px1 = ox + x * sc, py1 = oy;
        const px2 = ox,          py2 = oy - y * sc;
        p.stroke(243, 156, 18); p.strokeWeight(3);
        p.line(px1, py1, px2, py2);

        // 끝점
        p.fill(231, 76, 60); p.noStroke();
        p.ellipse(px1, py1, 10, 10);
        p.fill(52, 152, 219);
        p.ellipse(px2, py2, 10, 10);

        // x, y 치수선
        p.stroke(149, 165, 166); p.strokeWeight(1);
        p.drawingContext.setLineDash([3, 3]);
        p.line(px2, py2, px2, oy);
        p.line(ox, py1, px1, py1);
        p.drawingContext.setLineDash([]);
        p.fill(180); p.noStroke(); p.textSize(11); p.textAlign(p.CENTER);
        p.text('x=' + x.toFixed(2), (ox + px1) / 2, oy + 16);
        p.text('y=' + y.toFixed(2), ox - 20, (py2 + oy) / 2);

        // 변화율 표시
        const ratesEl = document.getElementById('{{asset_id}}-rates');
        if (ratesEl) {
          ratesEl.innerHTML =
            `t = ${currentT.toFixed(1)}&nbsp;&nbsp;|&nbsp;&nbsp;` +
            `x = ${x.toFixed(3)},&nbsp; dx/dt = ${dxdt.toFixed(3)}&nbsp;&nbsp;|&nbsp;&nbsp;` +
            `y = ${y.toFixed(3)},&nbsp; <span style="color:#3498db;">dy/dt = ${dydt.toFixed(3)}</span>`;
        }
      };
    });
  }

  window['updateRates_{{asset_id}}'] = function(val) {
    currentT = parseFloat(val);
    document.getElementById('{{asset_id}}-sv').textContent = currentT.toFixed(1);
    redraw();
  };

  redraw();
})();
</script>
```

---

## 미적분 권장 수치 파라미터

```yaml
# 대표 함수 및 도함수값

f(x) = x²:
  f'(x): 2x
  f''(x): 2
  대표 접선 기울기:
    x=1: 2
    x=2: 4
    x=3: 6
  정적분 ∫₀² x² dx: 8/3 ≈ 2.667

f(x) = x³:
  f'(x): 3x²
  f''(x): 6x
  대표 접선 기울기:
    x=1: 3
    x=2: 12
    x=-1: 3 (양수, 기울기 대칭)
  정적분 ∫₀¹ x³ dx: 1/4 = 0.25

f(x) = sin(x):
  f'(x): cos(x)
  f''(x): -sin(x)
  대표 접선 기울기:
    x=0: 1 (cos 0 = 1)
    x=π/2: 0 (cos π/2 = 0, 극댓값)
    x=π: -1 (cos π = -1)
  정적분 ∫₀^π sin(x) dx: 2

f(x) = cos(x):
  f'(x): -sin(x)
  정적분 ∫₀^(π/2) cos(x) dx: 1

f(x) = eˣ:
  f'(x): eˣ  (자기 자신 — 유일한 성질)
  대표값:
    e⁰=1, e¹≈2.718, e²≈7.389, e⁻¹≈0.368
  정적분 ∫₀¹ eˣ dx: e-1 ≈ 1.718

f(x) = ln(x):
  f'(x): 1/x  (x>0)
  대표 접선 기울기:
    x=1: 1
    x=2: 0.5
    x=e: 1/e ≈ 0.368
  정적분 ∫₁^e ln(x) dx: 1

# 체인 룰 예시값
합성함수 sin(x²):
  u = x²,  du/dx = 2x
  y = sin(u),  dy/du = cos(u) = cos(x²)
  dy/dx = 2x·cos(x²)

합성함수 (x²+1)³:
  u = x²+1,  du/dx = 2x
  y = u³,  dy/du = 3u²
  dy/dx = 3(x²+1)² · 2x = 6x(x²+1)²

# 리만 합 수렴 예시 (f(x)=x², [0,1], 좌끝 합)
n=1:  Σ = 0.000
n=4:  Σ = 0.219
n=10: Σ = 0.285
n=50: Σ = 0.323
n=∞:  exact = 1/3 ≈ 0.333

# 미적분 기본 정리 대표 예
F(x) = x³/3  →  F'(x) = x²  →  ∫₀² x² dx = F(2)-F(0) = 8/3-0 = 8/3
F(x) = -cos(x)  →  F'(x) = sin(x)  →  ∫₀^π sin(x) dx = -cos(π)-(-cos(0)) = 1+1 = 2

# 관련 변화율 사다리 예시
사다리 길이 L=5, x(t)=t+1 (1≤t≤4)
  dx/dt = 1 (일정)
  y = √(25-x²)
  dy/dt = -x/y · dx/dt = -x / √(25-x²)
  t=2: x=3, y=4, dy/dt = -3/4 = -0.75
  t=3: x=4, y=3, dy/dt = -4/3 ≈ -1.333  (속도 가속)
```
