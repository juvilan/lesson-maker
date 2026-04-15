# 수학I/II/확률과통계 — 시각화 카탈로그 플러그인

visual_creator.md 에이전트가 이 파일을 로드하여
수학I (지수·로그·삼각함수·수열), 수학II (극한·미분·적분기초),
확률과통계 (이산확률·이항분포·정규분포) 공통 시각화를 생성할 때 사용한다.

---

## 지원 시각화 타입 목록

| 타입명 | 설명 | 라이브러리 |
|--------|------|-----------|
| `log_exp_graph` | 지수/로그 함수 비교 그래프 (y=aˣ, y=logₐx 동시 표시) | Chart.js |
| `trig_graph` | 삼각함수 그래프 (sin/cos/tan 선택, 특수각 마커 포함) | Chart.js |
| `sequence_table` | 수열 계산 추적 표 (등차/등비, fillable 셀) | HTML 표 |
| `limit_approach` | 좌극한/우극한 시각화 (x→a 접근) | Chart.js |
| `derivative_tangent` | 접선과 함수 그래프 (슬라이더로 x값 조정, 접선 실시간) | p5.js |
| `area_under_curve` | 적분 영역 시각화 (리만 합 + 구분구적법 슬라이더) | p5.js |
| `normal_distribution` | 정규분포 곡선 (μ/σ 슬라이더로 실시간 변형) | Chart.js |
| `binomial_distribution` | 이항분포 막대그래프 (n/p 슬라이더) | Chart.js |
| `probability_tree` | 조건부 확률 트리 (두 단계 이벤트 분기) | SVG |

---

## 각 타입별 코드 패턴

### `log_exp_graph`

y=aˣ(지수함수)와 y=logₐ(x)(로그함수)를 다른 색으로 동시 표시.
두 함수가 y=x에 대해 대칭임을 직관적으로 확인.

```html
<div style="max-height:280px; position:relative;">
  <canvas id="{{asset_id}}"></canvas>
</div>
<div class="param-slider-group" style="font-size:0.8em; margin-top:0.4em;">
  <label>밑수 a</label>
  <input type="range" min="1.5" max="4" step="0.1" value="{{base}}"
         id="{{asset_id}}-sl" oninput="updateLogExp_{{asset_id}}(this.value)">
  <span id="{{asset_id}}-sv">{{base}}</span>
</div>
```

```javascript
(function() {
  const ctx = document.getElementById('{{asset_id}}').getContext('2d');
  let chart;

  function buildData(base) {
    const expX = [], expY = [], logX = [], logY = [], symX = [], symY = [];
    for (let x = -3; x <= 3; x += 0.05) {
      expX.push(x);
      expY.push(Math.pow(base, x));
    }
    for (let x = 0.05; x <= 3; x += 0.05) {
      logX.push(x);
      logY.push(Math.log(x) / Math.log(base));
    }
    for (let x = -3; x <= 3; x += 0.1) {
      symX.push(x);
      symY.push(x);
    }
    return { expX, expY, logX, logY, symX, symY };
  }

  function render(base) {
    const d = buildData(base);
    const datasets = [
      {
        label: `y = ${base}ˣ`,
        data: d.expX.map((x, i) => ({ x, y: d.expY[i] })),
        borderColor: '#e74c3c',
        backgroundColor: 'transparent',
        borderWidth: 2,
        pointRadius: 0,
        tension: 0.4
      },
      {
        label: `y = log₍${base}₎(x)`,
        data: d.logX.map((x, i) => ({ x, y: d.logY[i] })),
        borderColor: '#3498db',
        backgroundColor: 'transparent',
        borderWidth: 2,
        pointRadius: 0,
        tension: 0.4
      },
      {
        label: 'y = x',
        data: d.symX.map((x, i) => ({ x, y: d.symY[i] })),
        borderColor: '#555',
        backgroundColor: 'transparent',
        borderWidth: 1,
        borderDash: [4, 4],
        pointRadius: 0
      }
    ];
    if (chart) {
      chart.data.datasets = datasets;
      chart.options.plugins.title.text = `밑수 a = ${base}`;
      chart.update();
    } else {
      chart = new Chart(ctx, {
        type: 'line',
        data: { datasets },
        options: {
          responsive: true,
          maintainAspectRatio: true,
          aspectRatio: 1.6,
          parsing: false,
          scales: {
            x: { type: 'linear', min: -3, max: 3, grid: { color: '#333' }, ticks: { color: '#bdc3c7' } },
            y: { min: -3, max: 5, grid: { color: '#333' }, ticks: { color: '#bdc3c7' } }
          },
          plugins: {
            legend: { labels: { color: '#bdc3c7', font: { size: 11 } } },
            title: { display: true, text: `밑수 a = ${base}`, color: '#f39c12' }
          }
        }
      });
    }
  }

  window['updateLogExp_{{asset_id}}'] = function(val) {
    const base = parseFloat(val);
    document.getElementById('{{asset_id}}-sv').textContent = base.toFixed(1);
    render(base);
  };
  render({{base}});
})();
```

---

### `trig_graph`

sin/cos/tan 중 선택 표시.
특수각(0, π/6, π/4, π/3, π/2, π 등) 마커 포인트 포함.

```html
<div style="max-height:280px; position:relative;">
  <canvas id="{{asset_id}}"></canvas>
</div>
<div style="text-align:center; margin-top:0.4em; font-size:0.8em;">
  <button class="abtn" onclick="showTrig_{{asset_id}}('sin')">sin</button>
  <button class="abtn" onclick="showTrig_{{asset_id}}('cos')">cos</button>
  <button class="abtn" onclick="showTrig_{{asset_id}}('tan')">tan</button>
</div>
```

```javascript
(function() {
  const ctx = document.getElementById('{{asset_id}}').getContext('2d');
  let chart;

  const specialAngles = [0, Math.PI/6, Math.PI/4, Math.PI/3, Math.PI/2,
                         2*Math.PI/3, 3*Math.PI/4, 5*Math.PI/6, Math.PI,
                         7*Math.PI/6, 5*Math.PI/4, 4*Math.PI/3, 3*Math.PI/2,
                         5*Math.PI/3, 7*Math.PI/4, 11*Math.PI/6, 2*Math.PI];
  const specialLabels = ['0', 'π/6', 'π/4', 'π/3', 'π/2',
                          '2π/3', '3π/4', '5π/6', 'π',
                          '7π/6', '5π/4', '4π/3', '3π/2',
                          '5π/3', '7π/4', '11π/6', '2π'];

  const fnMap = {
    sin: { fn: Math.sin, color: '#e74c3c', yMin: -1.5, yMax: 1.5 },
    cos: { fn: Math.cos, color: '#3498db', yMin: -1.5, yMax: 1.5 },
    tan: { fn: x => {
      const v = Math.tan(x);
      return Math.abs(v) > 10 ? null : v;
    }, color: '#2ecc71', yMin: -4, yMax: 4 }
  };

  function render(type) {
    const { fn, color, yMin, yMax } = fnMap[type];
    const lineData = [], markerData = [];

    for (let x = 0; x <= 2 * Math.PI; x += 0.02) {
      const y = fn(x);
      lineData.push({ x, y: y === null ? null : y });
    }
    specialAngles.forEach((angle, i) => {
      const y = fn(angle);
      if (y !== null && isFinite(y) && Math.abs(y) <= Math.abs(yMax)) {
        markerData.push({ x: angle, y, label: specialLabels[i] });
      }
    });

    const datasets = [
      {
        label: `y = ${type}(x)`,
        data: lineData,
        borderColor: color,
        backgroundColor: 'transparent',
        borderWidth: 2,
        pointRadius: 0,
        spanGaps: false,
        tension: 0
      },
      {
        label: '특수각',
        data: markerData,
        borderColor: color,
        backgroundColor: color,
        borderWidth: 0,
        pointRadius: 5,
        showLine: false
      }
    ];

    if (chart) {
      chart.data.datasets = datasets;
      chart.options.scales.y.min = yMin;
      chart.options.scales.y.max = yMax;
      chart.update();
    } else {
      chart = new Chart(ctx, {
        type: 'line',
        data: { datasets },
        options: {
          responsive: true,
          maintainAspectRatio: true,
          aspectRatio: 1.6,
          parsing: false,
          scales: {
            x: {
              type: 'linear', min: 0, max: 2 * Math.PI,
              grid: { color: '#333' }, ticks: { color: '#bdc3c7', stepSize: Math.PI / 2 }
            },
            y: { min: yMin, max: yMax, grid: { color: '#333' }, ticks: { color: '#bdc3c7' } }
          },
          plugins: {
            legend: { labels: { color: '#bdc3c7', font: { size: 11 } } }
          }
        }
      });
    }
  }

  window['showTrig_{{asset_id}}'] = render;
  render('{{trig_type}}');
})();
```

---

### `sequence_table`

등차 또는 등비수열의 n=1~6 행 값을 단계별로 채우는 표.
`fillable` 셀 클릭으로 학생이 확인하는 방식.

```html
<table class="calc-table" id="{{asset_id}}">
  <thead>
    <tr>
      <th>n</th>
      <th>a_n (수식)</th>
      <th>계산 과정</th>
      <th>값</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>1</td><td class="formula">{{formula_n1}}</td><td class="fillable" id="{{asset_id}}-proc-1">?</td><td class="fillable" id="{{asset_id}}-val-1">?</td></tr>
    <tr><td>2</td><td class="formula">{{formula_n2}}</td><td class="fillable" id="{{asset_id}}-proc-2">?</td><td class="fillable" id="{{asset_id}}-val-2">?</td></tr>
    <tr><td>3</td><td class="formula">{{formula_n3}}</td><td class="fillable" id="{{asset_id}}-proc-3">?</td><td class="fillable" id="{{asset_id}}-val-3">?</td></tr>
    <tr><td>4</td><td class="formula">{{formula_n4}}</td><td class="fillable" id="{{asset_id}}-proc-4">?</td><td class="fillable" id="{{asset_id}}-val-4">?</td></tr>
    <tr><td>5</td><td class="formula">{{formula_n5}}</td><td class="fillable" id="{{asset_id}}-proc-5">?</td><td class="fillable" id="{{asset_id}}-val-5">?</td></tr>
    <tr><td>6</td><td class="formula">{{formula_n6}}</td><td class="fillable" id="{{asset_id}}-proc-6">?</td><td class="fillable" id="{{asset_id}}-val-6">?</td></tr>
  </tbody>
</table>
<div class="anim-ctrl">
  <button class="abtn" onclick="fillSeq_{{asset_id}}()">다음 행 채우기 ▶</button>
  <button class="abtn gray" onclick="resetSeq_{{asset_id}}()">↺</button>
</div>
```

```javascript
(function() {
  // type: 'arithmetic' | 'geometric'
  // a1: 첫째항, d: 공차(등차) 또는 r: 공비(등비)
  const type = '{{seq_type}}';
  const a1 = {{a1}};
  const d = {{d}};   // 등차수열용 공차 (등비수열이면 무시)
  const r = {{r}};   // 등비수열용 공비 (등차수열이면 무시)

  function computeVal(n) {
    if (type === 'arithmetic') return a1 + (n - 1) * d;
    return a1 * Math.pow(r, n - 1);
  }

  function computeProc(n) {
    if (type === 'arithmetic') {
      return n === 1
        ? `${a1}`
        : `${a1} + (${n}-1)×${d} = ${a1} + ${(n-1)*d}`;
    }
    return n === 1
      ? `${a1}`
      : `${a1} × ${r}^${n-1} = ${a1} × ${Math.pow(r, n-1).toFixed(3)}`;
  }

  let step = 0;

  window['fillSeq_{{asset_id}}'] = function() {
    if (step >= 6) return;
    step++;
    const proc = document.getElementById('{{asset_id}}-proc-' + step);
    const val  = document.getElementById('{{asset_id}}-val-'  + step);
    if (proc) {
      gsap.to(proc, {
        backgroundColor: 'rgba(243,156,18,0.3)', duration: 0.3,
        onComplete: () => {
          proc.textContent = computeProc(step);
          proc.classList.add('filled');
          gsap.to(proc, { backgroundColor: 'transparent', duration: 0.5 });
        }
      });
    }
    if (val) {
      setTimeout(() => {
        gsap.to(val, {
          backgroundColor: 'rgba(46,204,113,0.3)', duration: 0.3,
          onComplete: () => {
            val.textContent = computeVal(step).toFixed(2).replace(/\.00$/, '');
            val.style.color = '#2ecc71';
            val.classList.add('filled');
            gsap.to(val, { backgroundColor: 'transparent', duration: 0.5 });
          }
        });
      }, 400);
    }
  };

  window['resetSeq_{{asset_id}}'] = function() {
    step = 0;
    for (let n = 1; n <= 6; n++) {
      const proc = document.getElementById('{{asset_id}}-proc-' + n);
      const val  = document.getElementById('{{asset_id}}-val-'  + n);
      if (proc) { proc.textContent = '?'; proc.classList.remove('filled'); }
      if (val)  { val.textContent  = '?'; val.style.color = ''; val.classList.remove('filled'); }
    }
  };
})();
```

---

### `limit_approach`

x→a 접근 시 좌극한(왼쪽에서 접근)과 우극한(오른쪽에서 접근)을 두 색의 선으로 표시.

```html
<div style="max-height:280px; position:relative;">
  <canvas id="{{asset_id}}"></canvas>
</div>
<div style="text-align:center; font-size:0.78em; margin-top:0.3em; color:#95a5a6;">
  <span style="color:#e74c3c;">■</span> 좌극한 (x→{{a}}⁻) &nbsp;
  <span style="color:#3498db;">■</span> 우극한 (x→{{a}}⁺)
</div>
```

```javascript
(function() {
  const ctx = document.getElementById('{{asset_id}}').getContext('2d');
  const a = {{a}};
  const eps = 0.002;

  // 함수 f(x) 정의: 플레이스홀더로 실제 함수 대입
  function f(x) { return {{fn_expr}}; }

  const leftData = [], rightData = [];
  for (let x = a - 2; x < a - eps; x += 0.02) {
    leftData.push({ x, y: f(x) });
  }
  for (let x = a + eps; x <= a + 2; x += 0.02) {
    rightData.push({ x, y: f(x) });
  }

  new Chart(ctx, {
    type: 'line',
    data: {
      datasets: [
        {
          label: `x→${a}⁻ (좌극한)`,
          data: leftData,
          borderColor: '#e74c3c',
          backgroundColor: 'transparent',
          borderWidth: 2.5,
          pointRadius: 0,
          tension: 0
        },
        {
          label: `x→${a}⁺ (우극한)`,
          data: rightData,
          borderColor: '#3498db',
          backgroundColor: 'transparent',
          borderWidth: 2.5,
          pointRadius: 0,
          tension: 0
        },
        {
          label: 'x = a 경계',
          data: [{ x: a, y: -5 }, { x: a, y: 5 }],
          borderColor: '#f39c1266',
          backgroundColor: 'transparent',
          borderWidth: 1,
          borderDash: [4, 4],
          pointRadius: 0,
          showLine: true
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: true,
      aspectRatio: 1.6,
      parsing: false,
      scales: {
        x: { type: 'linear', min: a - 2.2, max: a + 2.2, grid: { color: '#333' }, ticks: { color: '#bdc3c7' } },
        y: { min: {{y_min}}, max: {{y_max}}, grid: { color: '#333' }, ticks: { color: '#bdc3c7' } }
      },
      plugins: {
        legend: { labels: { color: '#bdc3c7', font: { size: 11 } } },
        title: { display: true, text: 'x → {{a}} 에서의 극한', color: '#f39c12' }
      }
    }
  });
})();
```

---

### `derivative_tangent`

슬라이더로 x값을 조정하면 해당 점에서의 접선이 실시간으로 그려진다.
p5.js 캔버스, 컨테이너 width를 읽어 반응형으로 동작.

```html
<div id="{{asset_id}}-container" style="width:100%; position:relative;"></div>
<div class="param-slider-group" style="font-size:0.8em; margin-top:0.4em;">
  <label>x 값</label>
  <input type="range" min="{{x_min}}" max="{{x_max}}" step="0.05" value="{{x_init}}"
         id="{{asset_id}}-sl" oninput="updateTangent_{{asset_id}}(this.value)">
  <span id="{{asset_id}}-sv">{{x_init}}</span>
</div>
<div id="{{asset_id}}-info" style="font-size:0.78em; color:#f39c12; text-align:center; margin-top:0.2em;"></div>
```

```javascript
(function() {
  const container = document.getElementById('{{asset_id}}-container');
  const W = container.clientWidth || 480;
  const H = Math.round(W / 1.6);
  let currentX = {{x_init}};

  // f(x) 및 f'(x) 실제 함수 대입
  function f(x)  { return {{fn_expr}}; }
  function df(x) { return {{dfn_expr}}; }

  const sketch = function(p) {
    const margin = 50;
    const domainMin = {{x_min}} - 0.5, domainMax = {{x_max}} + 0.5;
    const rangeMin = {{y_min}}, rangeMax = {{y_max}};

    function toCanvas(x, y) {
      const px = margin + (x - domainMin) / (domainMax - domainMin) * (W - 2 * margin);
      const py = (H - margin) - (y - rangeMin) / (rangeMax - rangeMin) * (H - 2 * margin);
      return [px, py];
    }

    p.setup = function() {
      const cnv = p.createCanvas(W, H);
      cnv.parent('{{asset_id}}-container');
      p.textFont('sans-serif');
    };

    p.draw = function() {
      p.background('#1a1a2e');

      // 축
      p.stroke('#444'); p.strokeWeight(1);
      const [x0, y0] = toCanvas(domainMin, 0);
      const [x1, y1] = toCanvas(domainMax, 0);
      const [ax0, ay0] = toCanvas(0, rangeMin);
      const [ax1, ay1] = toCanvas(0, rangeMax);
      p.line(x0, y0, x1, y1);
      p.line(ax0, ay0, ax1, ay1);

      // 함수 곡선
      p.stroke('#3498db'); p.strokeWeight(2); p.noFill();
      p.beginShape();
      for (let x = domainMin; x <= domainMax; x += 0.02) {
        const y = f(x);
        if (isFinite(y) && y >= rangeMin && y <= rangeMax) {
          const [px, py] = toCanvas(x, y);
          p.vertex(px, py);
        }
      }
      p.endShape();

      // 접선
      const slope = df(currentX);
      const yc = f(currentX);
      const tangentFn = x => slope * (x - currentX) + yc;
      p.stroke('#e74c3c'); p.strokeWeight(2); p.noFill();
      p.beginShape();
      for (let x = domainMin; x <= domainMax; x += 0.05) {
        const y = tangentFn(x);
        if (isFinite(y) && y >= rangeMin - 1 && y <= rangeMax + 1) {
          const [px, py] = toCanvas(x, y);
          p.vertex(px, py);
        }
      }
      p.endShape();

      // 접점
      const [cpx, cpy] = toCanvas(currentX, yc);
      p.fill('#f39c12'); p.noStroke();
      p.ellipse(cpx, cpy, 10, 10);

      // 정보 표시
      const info = document.getElementById('{{asset_id}}-info');
      if (info) {
        info.textContent = `x = ${currentX.toFixed(2)}, f(x) = ${yc.toFixed(3)}, f'(x) = ${slope.toFixed(3)}`;
      }

      p.noLoop();
    };
  };

  new p5(sketch);

  window['updateTangent_{{asset_id}}'] = function(val) {
    currentX = parseFloat(val);
    document.getElementById('{{asset_id}}-sv').textContent = currentX.toFixed(2);
    // p5 인스턴스 재draw
    const cnv = document.querySelector('#{{asset_id}}-container canvas');
    if (cnv && cnv._pInst) cnv._pInst.redraw();
  };
})();
```

---

### `area_under_curve`

리만 합 n개 직사각형 + 구분구적법 슬라이더.
컨테이너 clientWidth를 읽어 반응형으로 동작.

```html
<div id="{{asset_id}}-container" style="width:100%; position:relative;"></div>
<div class="param-slider-group" style="font-size:0.8em; margin-top:0.4em;">
  <label>분할 수 n</label>
  <input type="range" min="2" max="50" step="1" value="{{n_init}}"
         id="{{asset_id}}-sl" oninput="updateArea_{{asset_id}}(this.value)">
  <span id="{{asset_id}}-sv">{{n_init}}</span>
</div>
<div id="{{asset_id}}-info" style="font-size:0.78em; color:#f39c12; text-align:center; margin-top:0.2em;"></div>
```

```javascript
(function() {
  const container = document.getElementById('{{asset_id}}-container');
  const W = container.clientWidth || 480;
  const H = Math.round(W / 1.6);
  let nDiv = {{n_init}};

  const a = {{integral_a}}, b = {{integral_b}};
  function f(x) { return {{fn_expr}}; }

  const sketch = function(p) {
    const margin = 50;
    const xMin = a - 0.3, xMax = b + 0.3;
    const yMin = 0, yMax = {{y_max}};

    function toCanvas(x, y) {
      const px = margin + (x - xMin) / (xMax - xMin) * (W - 2 * margin);
      const py = (H - margin) - (y - yMin) / (yMax - yMin) * (H - 2 * margin);
      return [px, py];
    }

    function riemannSum(n) {
      const dx = (b - a) / n;
      let sum = 0;
      for (let i = 0; i < n; i++) {
        sum += f(a + i * dx) * dx;
      }
      return sum;
    }

    p.setup = function() {
      const cnv = p.createCanvas(W, H);
      cnv.parent('{{asset_id}}-container');
    };

    p.draw = function() {
      p.background('#1a1a2e');

      // 리만 직사각형
      const dx = (b - a) / nDiv;
      p.fill('rgba(52,152,219,0.4)'); p.stroke('#3498db'); p.strokeWeight(0.5);
      for (let i = 0; i < nDiv; i++) {
        const xi = a + i * dx;
        const yi = f(xi);
        const [px0, py0] = toCanvas(xi, 0);
        const [px1, py1] = toCanvas(xi + dx, yi);
        p.rect(px0, py1, px1 - px0, py0 - py1);
      }

      // 축
      p.stroke('#555'); p.strokeWeight(1);
      const [x0, y0] = toCanvas(xMin, 0);
      const [x1, y1] = toCanvas(xMax, 0);
      p.line(x0, y0, x1, y1);

      // 함수 곡선
      p.stroke('#e74c3c'); p.strokeWeight(2.5); p.noFill();
      p.beginShape();
      for (let x = xMin; x <= xMax; x += 0.02) {
        const y = f(x);
        if (isFinite(y) && y >= yMin && y <= yMax) {
          const [px, py] = toCanvas(x, y);
          p.vertex(px, py);
        }
      }
      p.endShape();

      // 구간 표시
      p.fill('#f39c12'); p.noStroke(); p.textSize(12);
      const [paX] = toCanvas(a, 0);
      const [pbX] = toCanvas(b, 0);
      p.text(`a=${a}`, paX - 10, H - 10);
      p.text(`b=${b}`, pbX - 10, H - 10);

      // 리만 합 표시
      const sum = riemannSum(nDiv);
      const info = document.getElementById('{{asset_id}}-info');
      if (info) {
        info.textContent = `n = ${nDiv},  리만 합 ≈ ${sum.toFixed(4)}`;
      }

      p.noLoop();
    };
  };

  new p5(sketch);

  window['updateArea_{{asset_id}}'] = function(val) {
    nDiv = parseInt(val);
    document.getElementById('{{asset_id}}-sv').textContent = nDiv;
    const cnv = document.querySelector('#{{asset_id}}-container canvas');
    if (cnv && cnv._pInst) cnv._pInst.redraw();
  };
})();
```

---

### `normal_distribution`

μ/σ 슬라이더로 정규분포 곡선을 실시간 변형.

```html
<div style="max-height:280px; position:relative;">
  <canvas id="{{asset_id}}"></canvas>
</div>
<div style="font-size:0.8em; margin-top:0.4em; display:flex; gap:1.5em; justify-content:center;">
  <div class="param-slider-group">
    <label>μ</label>
    <input type="range" min="-3" max="3" step="0.1" value="{{mu}}"
           id="{{asset_id}}-mu" oninput="updateNorm_{{asset_id}}()">
    <span id="{{asset_id}}-mu-sv">{{mu}}</span>
  </div>
  <div class="param-slider-group">
    <label>σ</label>
    <input type="range" min="0.3" max="3" step="0.1" value="{{sigma}}"
           id="{{asset_id}}-sigma" oninput="updateNorm_{{asset_id}}()">
    <span id="{{asset_id}}-sigma-sv">{{sigma}}</span>
  </div>
</div>
```

```javascript
(function() {
  const ctx = document.getElementById('{{asset_id}}').getContext('2d');
  let chart;

  function normalPDF(x, mu, sigma) {
    return (1 / (sigma * Math.sqrt(2 * Math.PI))) *
           Math.exp(-0.5 * Math.pow((x - mu) / sigma, 2));
  }

  function render(mu, sigma) {
    const data = [];
    for (let x = -6; x <= 6; x += 0.05) {
      data.push({ x, y: normalPDF(x, mu, sigma) });
    }
    if (chart) {
      chart.data.datasets[0].data = data;
      chart.data.datasets[0].label = `N(${mu}, ${sigma}²)`;
      chart.update();
    } else {
      chart = new Chart(ctx, {
        type: 'line',
        data: {
          datasets: [{
            label: `N(${mu}, ${sigma}²)`,
            data,
            borderColor: '#e74c3c',
            backgroundColor: 'rgba(231,76,60,0.1)',
            fill: true,
            borderWidth: 2,
            pointRadius: 0,
            tension: 0.4
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: true,
          aspectRatio: 1.6,
          parsing: false,
          scales: {
            x: { type: 'linear', min: -6, max: 6, grid: { color: '#333' }, ticks: { color: '#bdc3c7' } },
            y: { min: 0, grid: { color: '#333' }, ticks: { color: '#bdc3c7' } }
          },
          plugins: {
            legend: { labels: { color: '#bdc3c7', font: { size: 11 } } }
          }
        }
      });
    }
  }

  window['updateNorm_{{asset_id}}'] = function() {
    const mu    = parseFloat(document.getElementById('{{asset_id}}-mu').value);
    const sigma = parseFloat(document.getElementById('{{asset_id}}-sigma').value);
    document.getElementById('{{asset_id}}-mu-sv').textContent    = mu.toFixed(1);
    document.getElementById('{{asset_id}}-sigma-sv').textContent = sigma.toFixed(1);
    render(mu, sigma);
  };
  render({{mu}}, {{sigma}});
})();
```

---

### `binomial_distribution`

n/p 슬라이더로 이항분포 막대그래프 실시간 갱신.

```html
<div style="max-height:280px; position:relative;">
  <canvas id="{{asset_id}}"></canvas>
</div>
<div style="font-size:0.8em; margin-top:0.4em; display:flex; gap:1.5em; justify-content:center;">
  <div class="param-slider-group">
    <label>n</label>
    <input type="range" min="2" max="20" step="1" value="{{n}}"
           id="{{asset_id}}-n" oninput="updateBinom_{{asset_id}}()">
    <span id="{{asset_id}}-n-sv">{{n}}</span>
  </div>
  <div class="param-slider-group">
    <label>p</label>
    <input type="range" min="0.1" max="0.9" step="0.05" value="{{p}}"
           id="{{asset_id}}-p" oninput="updateBinom_{{asset_id}}()">
    <span id="{{asset_id}}-p-sv">{{p}}</span>
  </div>
</div>
```

```javascript
(function() {
  const ctx = document.getElementById('{{asset_id}}').getContext('2d');
  let chart;

  function combination(n, k) {
    if (k < 0 || k > n) return 0;
    if (k === 0 || k === n) return 1;
    let result = 1;
    for (let i = 0; i < Math.min(k, n - k); i++) {
      result = result * (n - i) / (i + 1);
    }
    return Math.round(result);
  }

  function binomialPMF(n, k, p) {
    return combination(n, k) * Math.pow(p, k) * Math.pow(1 - p, n - k);
  }

  function render(n, p) {
    const labels = Array.from({ length: n + 1 }, (_, k) => `k=${k}`);
    const data   = Array.from({ length: n + 1 }, (_, k) => binomialPMF(n, k, p));
    const mean   = (n * p).toFixed(2);
    const vari   = (n * p * (1 - p)).toFixed(2);

    if (chart) {
      chart.data.labels = labels;
      chart.data.datasets[0].data = data;
      chart.data.datasets[0].label = `B(${n}, ${p}) — E(X)=${mean}, V(X)=${vari}`;
      chart.update();
    } else {
      chart = new Chart(ctx, {
        type: 'bar',
        data: {
          labels,
          datasets: [{
            label: `B(${n}, ${p}) — E(X)=${mean}, V(X)=${vari}`,
            data,
            backgroundColor: 'rgba(52,152,219,0.7)',
            borderColor: '#3498db',
            borderWidth: 1
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: true,
          aspectRatio: 1.6,
          scales: {
            x: { grid: { color: '#333' }, ticks: { color: '#bdc3c7', font: { size: 10 } } },
            y: { min: 0, grid: { color: '#333' }, ticks: { color: '#bdc3c7' } }
          },
          plugins: {
            legend: { labels: { color: '#bdc3c7', font: { size: 11 } } }
          }
        }
      });
    }
  }

  window['updateBinom_{{asset_id}}'] = function() {
    const n = parseInt(document.getElementById('{{asset_id}}-n').value);
    const p = parseFloat(document.getElementById('{{asset_id}}-p').value);
    document.getElementById('{{asset_id}}-n-sv').textContent = n;
    document.getElementById('{{asset_id}}-p-sv').textContent = p.toFixed(2);
    render(n, p);
  };
  render({{n}}, {{p}});
})();
```

---

### `probability_tree`

두 단계 이벤트 분기 구조의 조건부 확률 트리.
SVG, preserveAspectRatio="xMidYMid meet", overflow:hidden.

```html
<div style="width:100%; overflow:hidden;">
  <svg id="{{asset_id}}" viewBox="0 0 500 320"
       preserveAspectRatio="xMidYMid meet"
       style="width:100%; max-height:320px; display:block;">

    <!-- 루트 노드 -->
    <circle cx="60" cy="160" r="22" fill="#2c3e50" stroke="#7f8c8d" stroke-width="2"/>
    <text x="60" y="165" text-anchor="middle" fill="#ecf0f1" font-size="11">S</text>

    <!-- 1단계: A, A' -->
    <line x1="82" y1="150" x2="178" y2="90" stroke="#7f8c8d" stroke-width="1.5"/>
    <text x="125" y="108" text-anchor="middle" fill="#f39c12" font-size="11">P(A)={{p_A}}</text>
    <circle cx="200" cy="80" r="22" fill="#2c3e50" stroke="#e74c3c" stroke-width="2"/>
    <text x="200" y="85" text-anchor="middle" fill="#e74c3c" font-size="11">A</text>

    <line x1="82" y1="170" x2="178" y2="230" stroke="#7f8c8d" stroke-width="1.5"/>
    <text x="125" y="215" text-anchor="middle" fill="#f39c12" font-size="11">P(A')={{p_Ac}}</text>
    <circle cx="200" cy="240" r="22" fill="#2c3e50" stroke="#3498db" stroke-width="2"/>
    <text x="200" y="245" text-anchor="middle" fill="#3498db" font-size="11">A'</text>

    <!-- 2단계 A 분기: B|A, B'|A -->
    <line x1="222" y1="72" x2="318" y2="40" stroke="#7f8c8d" stroke-width="1.5"/>
    <text x="268" y="48" text-anchor="middle" fill="#95a5a6" font-size="10">P(B|A)={{p_B_given_A}}</text>
    <circle cx="340" cy="32" r="20" fill="#2c3e50" stroke="#2ecc71" stroke-width="2"/>
    <text x="340" y="37" text-anchor="middle" fill="#2ecc71" font-size="10">A∩B</text>

    <line x1="222" y1="88" x2="318" y2="118" stroke="#7f8c8d" stroke-width="1.5"/>
    <text x="268" y="116" text-anchor="middle" fill="#95a5a6" font-size="10">P(B'|A)={{p_Bc_given_A}}</text>
    <circle cx="340" cy="128" r="20" fill="#2c3e50" stroke="#e67e22" stroke-width="2"/>
    <text x="340" y="133" text-anchor="middle" fill="#e67e22" font-size="10">A∩B'</text>

    <!-- 2단계 A' 분기: B|A', B'|A' -->
    <line x1="222" y1="232" x2="318" y2="200" stroke="#7f8c8d" stroke-width="1.5"/>
    <text x="268" y="208" text-anchor="middle" fill="#95a5a6" font-size="10">P(B|A')={{p_B_given_Ac}}</text>
    <circle cx="340" cy="192" r="20" fill="#2c3e50" stroke="#9b59b6" stroke-width="2"/>
    <text x="340" y="197" text-anchor="middle" fill="#9b59b6" font-size="10">A'∩B</text>

    <line x1="222" y1="248" x2="318" y2="278" stroke="#7f8c8d" stroke-width="1.5"/>
    <text x="268" y="274" text-anchor="middle" fill="#95a5a6" font-size="10">P(B'|A')={{p_Bc_given_Ac}}</text>
    <circle cx="340" cy="288" r="20" fill="#2c3e50" stroke="#1abc9c" stroke-width="2"/>
    <text x="340" y="293" text-anchor="middle" fill="#1abc9c" font-size="10">A'∩B'</text>

    <!-- 결합확률 -->
    <text x="495" y="37"  text-anchor="end" fill="#2ecc71"  font-size="10" id="{{asset_id}}-p1">P={{p_A}}×{{p_B_given_A}}</text>
    <text x="495" y="133" text-anchor="end" fill="#e67e22"  font-size="10" id="{{asset_id}}-p2">P={{p_A}}×{{p_Bc_given_A}}</text>
    <text x="495" y="197" text-anchor="end" fill="#9b59b6"  font-size="10" id="{{asset_id}}-p3">P={{p_Ac}}×{{p_B_given_Ac}}</text>
    <text x="495" y="293" text-anchor="end" fill="#1abc9c"  font-size="10" id="{{asset_id}}-p4">P={{p_Ac}}×{{p_Bc_given_Ac}}</text>
  </svg>
</div>
```

---

## 수학I/II/통계 권장 수치 파라미터

```yaml
# --- 지수·로그 함수 ---
log_exp_graph:
  base_default: 2
  base_range: [1.5, 4]
  주요값:
    2^0: 1, 2^1: 2, 2^2: 4, 2^(1/2): 1.414
    log2(1): 0, log2(2): 1, log2(4): 2, log2(8): 3

# --- 삼각함수 특수각 ---
trig_special_values:
  단위원_기준:
    0도(0):      sin=0,       cos=1,       tan=0
    30도(π/6):   sin=1/2,     cos=√3/2,    tan=1/√3 ≈ 0.577
    45도(π/4):   sin=√2/2,    cos=√2/2,    tan=1
    60도(π/3):   sin=√3/2,    cos=1/2,     tan=√3 ≈ 1.732
    90도(π/2):   sin=1,       cos=0,       tan=정의없음
    120도(2π/3): sin=√3/2,    cos=-1/2,    tan=-√3
    180도(π):    sin=0,       cos=-1,      tan=0
    270도(3π/2): sin=-1,      cos=0,       tan=정의없음
    360도(2π):   sin=0,       cos=1,       tan=0

# --- 수열 ---
sequence:
  등차수열_예시:
    a1: 2, d: 3   # 2, 5, 8, 11, 14, 17
    a1: 1, d: 2   # 1, 3, 5, 7, 9, 11 (홀수)
  등비수열_예시:
    a1: 1, r: 2   # 1, 2, 4, 8, 16, 32
    a1: 3, r: 3   # 3, 9, 27, 81, 243, 729
  등차수열_합:
    S_n: n/2 × (2a₁ + (n-1)d)  또는  n/2 × (a₁ + aₙ)
  등비수열_합:
    r≠1: S_n = a₁(rⁿ - 1) / (r - 1)
    r=1: S_n = n × a₁

# --- 극한 ---
limit_approach:
  fn_expr_예시: "(x*x - 1) / (x - 1)"   # x→1, 극한값=2
  fn_expr_예시2: "(x*x - 4) / (x - 2)"  # x→2, 극한값=4
  a_default: 1
  y_min: -1, y_max: 5

# --- 미분 ---
derivative_tangent:
  fn_expr_예시: "x*x"          # f(x)=x², f'(x)=2x
  dfn_expr_예시: "2*x"
  fn_expr_예시2: "x*x*x - x"   # f(x)=x³-x, f'(x)=3x²-1
  dfn_expr_예시2: "3*x*x - 1"
  x_init: 1, x_min: -2, x_max: 2
  y_min: -2, y_max: 4

# --- 적분 ---
area_under_curve:
  fn_expr_예시: "x*x"           # ∫₀²x²dx = 8/3 ≈ 2.667
  integral_a: 0, integral_b: 2
  n_init: 10
  y_max: 5

# --- 이항분포 ---
binomial_distribution:
  예시1: n=10, p=0.3  # E=3, σ²=2.1
  예시2: n=5,  p=0.5  # 동전 5회
  예시3: n=8,  p=0.4
  공식:
    P(X=k): nCk × p^k × (1-p)^(n-k)
    E(X): np
    V(X): np(1-p)

# --- 정규분포 ---
normal_distribution:
  표준정규: mu=0, sigma=1
  예시2:    mu=70, sigma=10  # 시험 점수 예시
  주요값(표준정규):
    P(Z≤0): 0.5000
    P(Z≤1): 0.8413
    P(Z≤2): 0.9772
    P(Z≤3): 0.9987
    P(-1≤Z≤1): 0.6826
    P(-2≤Z≤2): 0.9544
    P(-3≤Z≤3): 0.9974
  표준화: Z = (X - μ) / σ

# --- 확률 트리 ---
probability_tree:
  예시_동전_주사위:
    p_A: 0.5, p_Ac: 0.5
    p_B_given_A: 0.6, p_Bc_given_A: 0.4
    p_B_given_Ac: 0.3, p_Bc_given_Ac: 0.7
  베이즈정리_연결:
    P(A|B) = P(A)×P(B|A) / P(B)
    P(B) = P(A)×P(B|A) + P(A')×P(B|A')
```
