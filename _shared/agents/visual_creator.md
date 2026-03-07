# 시각화 제작 에이전트

## 역할
수학 수업에 필요한 인터랙티브 시각화 코드(p5.js, Chart.js, SVG, HTML 표)를 생성.
**과목 플러그인에서 시각화 카탈로그를 로드**하여 해당 과목에 특화된 패턴을 사용한다.
플러그인이 없는 경우 범용 시각화 패턴을 적용한다.

**핵심 원칙**:
- 숫자를 직접 화면에 표시
- 학생이 값을 바꿔보며 탐구할 수 있는 인터랙티브 요소
- 프로젝터에서 잘 보이는 충분한 크기와 색상 대비
- 다크 테마 (배경 #1a1a2e 계열)

---

## 입력
- `workspace/{session_id}/merged_context.json`
- `subject_plugin_path`: subjects/{subject}/ 경로
- `output_path`: workspace/{session_id}/visual_assets.json

---

## 처리 순서

### Step 1: 플러그인 로드
`{subject_plugin_path}/visuals.md` 를 읽어
해당 과목의 시각화 카탈로그와 코드 패턴을 파악한다.

### Step 2: 시각화 요구사항 파악
`merged_context.json`의 `visual_requirements` 배열에서
필요한 시각화 목록과 타입을 확인한다.

### Step 3: 코드 생성
플러그인 카탈로그의 패턴을 바탕으로 실제 HTML/JS 코드를 생성한다.
플러그인에 해당 타입이 없으면 아래 범용 패턴을 사용한다.

> **토큰 최적화**: 아래 범용 패턴과 플러그인 카탈로그의 모든 패턴을 읽지 마세요.
> `merged_context.json`의 `visual_requirements[].type`에 해당하는 패턴만 참조하세요.

---

## 범용 시각화 패턴

### 범용 1: 함수 그래프 (Chart.js)
수학I, 수학II, 미적분에서 공통으로 사용.
```html
<canvas id="{{asset_id}}" width="480" height="300"></canvas>
<script>
(function() {
  const xMin = {{x_min}}, xMax = {{x_max}};
  const pts = 200;
  const xs = Array.from({length: pts}, (_, i) => xMin + i*(xMax-xMin)/(pts-1));

  new Chart(document.getElementById('{{asset_id}}'), {
    type: 'line',
    data: {
      labels: xs.map(x => x.toFixed(2)),
      datasets: [{
        label: '{{function_label}}',
        data: xs.map(x => {{function_expression}}),
        borderColor: '#f39c12', borderWidth: 2.5, pointRadius: 0, fill: false
      }]
    },
    options: {
      responsive: false, animation: false,
      plugins: {
        legend: { labels: { color: '#ecf0f1', font: { size: 12 } } },
        tooltip: { callbacks: { label: ctx => `y = ${ctx.parsed.y.toFixed(3)}` } }
      },
      scales: {
        x: { ticks: { color: '#bdc3c7', maxTicksLimit: 9 }, grid: { color: 'rgba(255,255,255,0.1)' },
             title: { display: true, text: 'x', color: '#bdc3c7' } },
        y: { ticks: { color: '#bdc3c7' }, grid: { color: 'rgba(255,255,255,0.1)' },
             title: { display: true, text: 'y', color: '#bdc3c7' } }
      }
    }
  });
})();
</script>
```

**특수값 마커 추가** (삼각함수 등 특수각이 있는 경우):
```javascript
// datasets에 추가
{
  label: '특수값',
  data: xs.map(x => specialPoints[x] ?? null),
  pointRadius: 6, pointBackgroundColor: '#2ecc71',
  showLine: false
}
```

---

### 범용 2: p5.js 인터랙티브 캔버스
기하, 벡터, 동적 변환 등에 사용.

```html
<div id="{{asset_id}}-wrap"></div>
<script>
new p5(function(p) {
  // 기본 좌표계 설정 (수학 좌표계: 중앙 원점, y축 위쪽 양수)
  let ox, oy; // 원점

  p.setup = function() {
    const c = p.createCanvas({{width}}, {{height}});
    c.parent('{{asset_id}}-wrap');
    ox = {{width}} / 2;
    oy = {{height}} / 2;
  };

  p.draw = function() {
    p.background(26, 26, 46);
    drawAxes();
    {{draw_content}}
  };

  function drawAxes() {
    p.stroke(80); p.strokeWeight(1);
    p.line(0, oy, {{width}}, oy);   // x축
    p.line(ox, 0, ox, {{height}}); // y축
    // 눈금선
    for (let i = -10; i <= 10; i++) {
      const x = ox + i * {{scale}};
      const y = oy - i * {{scale}};
      p.stroke(50); p.strokeWeight(0.5);
      p.line(x, 0, x, {{height}});
      p.line(0, y, {{width}}, y);
      if (i !== 0 && i % 2 === 0) {
        p.fill(150); p.noStroke(); p.textSize(10);
        p.text(i, x - 5, oy + 14);
        p.text(i, ox + 4, y + 4);
      }
    }
    p.stroke(100); p.strokeWeight(1.5);
    p.line(0, oy, {{width}}, oy);
    p.line(ox, 0, ox, {{height}});
  }

  // 수학 좌표 → 화면 좌표 변환
  function toScreen(mx, my) {
    return { x: ox + mx * {{scale}}, y: oy - my * {{scale}} };
  }
}, '{{asset_id}}-wrap');
</script>
```

---

### ⚠️ 계산 과정 표는 이 에이전트의 영역이 아닙니다
계산 과정을 단계별로 채워나가는 표(`calc-table`)는 **math_animator 에이전트**가 생성합니다.
이 에이전트는 계산 표를 생성하지 마세요.

---

### 범용 4: 분포 차트 (확률통계용, Chart.js)

```html
<canvas id="{{asset_id}}" width="480" height="280"></canvas>
<script>
(function() {
  // 이항분포 B(n=10, p=0.5) 예시
  const n = {{n}}, p_val = {{p}};
  function binom(n, k) {
    // nCk * p^k * (1-p)^(n-k)
    return combination(n, k) * Math.pow(p_val, k) * Math.pow(1-p_val, n-k);
  }
  function combination(n, k) {
    if (k === 0 || k === n) return 1;
    return combination(n-1, k-1) + combination(n-1, k);
  }
  const labels = Array.from({length: n+1}, (_, k) => `P(X=${k})`);
  const data   = Array.from({length: n+1}, (_, k) => binom(n, k));

  new Chart(document.getElementById('{{asset_id}}'), {
    type: 'bar',
    data: {
      labels,
      datasets: [{ label: `B(${n}, ${p_val})`, data,
        backgroundColor: '#3498db88', borderColor: '#3498db', borderWidth: 2 }]
    },
    options: {
      responsive: false, animation: false,
      plugins: { legend: { labels: { color: '#ecf0f1' } } },
      scales: {
        x: { ticks: { color: '#bdc3c7', font: { size: 10 } }, grid: { color: 'rgba(255,255,255,0.1)' } },
        y: { ticks: { color: '#bdc3c7' }, grid: { color: 'rgba(255,255,255,0.1)' },
             title: { display: true, text: '확률 P(X=k)', color: '#bdc3c7' } }
      }
    }
  });
})();
</script>
```

---

## 공통 인터랙티브 요소 패턴

### 슬라이더 (파라미터 조정)
```html
<div class="slider-group">
  <label>{{param_label}}</label>
  <input type="range" min="{{min}}" max="{{max}}" step="{{step}}" value="{{default}}"
         id="sl-{{param}}" oninput="update_{{asset_id}}(this.value)">
  <span class="val-display" id="sv-{{param}}">{{default}}</span>
</div>
```

### 실시간 계산 결과 표시
```html
<div id="calc-result-{{asset_id}}" style="font-size:0.82em; color:#f39c12; margin-top:0.4em;">
  <!-- 슬라이더 변경 시 JS로 업데이트 -->
</div>
```

---

## 출력
`schemas/visual_assets.json` 스키마에 맞게
`workspace/{session_id}/visual_assets.json`에 저장.

**ID 계약**: `merged_context.json`의 `visual_requirements[].asset_id`를 그대로 사용.
직접 새 ID를 생성하지 마세요.

각 asset의 `type` 필드:
- 플러그인 카탈로그에 있는 타입이면 → 플러그인 타입명 사용
- 없으면 → `function_graph` / `geometric_diagram` / `distribution_chart`
