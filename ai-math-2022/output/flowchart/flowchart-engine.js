/* ============================================================
   flowchart-engine.js
   순서도(flow chart)를 데이터로 받아 SVG로 그리고,
   실제 알고리즘 실행 결과를 단계별로 추적 표시하는 엔진.

   핵심 원칙: 추적표에 들어가는 모든 값은 trace() 안에서
   실제 연산으로 계산된다. 어떤 값도 하드코딩하지 않는다.
   ============================================================ */
(function (global) {
  'use strict';

  var SVGNS = 'http://www.w3.org/2000/svg';

  function svgEl(tag, attrs) {
    var e = document.createElementNS(SVGNS, tag);
    Object.keys(attrs || {}).forEach(function (k) { e.setAttribute(k, attrs[k]); });
    return e;
  }

  function div(cls, style) {
    var e = document.createElement('div');
    if (cls) e.className = cls;
    if (style) Object.keys(style).forEach(function (k) { e.style[k] = style[k]; });
    return e;
  }

  /* ── 노드 기하 ─────────────────────────────────────────── */

  function anchor(n, side) {
    switch (side) {
      case 'top':    return { x: n.x, y: n.y - n.h / 2 };
      case 'bottom': return { x: n.x, y: n.y + n.h / 2 };
      case 'left':   return { x: n.x - n.w / 2, y: n.y };
      case 'right':  return { x: n.x + n.w / 2, y: n.y };
      default:       return { x: n.x, y: n.y };
    }
  }

  function shapeFor(n) {
    var l = n.x - n.w / 2, r = n.x + n.w / 2,
        t = n.y - n.h / 2, b = n.y + n.h / 2;

    if (n.type === 'terminal') {
      return svgEl('rect', { x: l, y: t, width: n.w, height: n.h, rx: n.h / 2, ry: n.h / 2 });
    }
    if (n.type === 'decision') {
      return svgEl('polygon', {
        points: [n.x + ',' + t, r + ',' + n.y, n.x + ',' + b, l + ',' + n.y].join(' ')
      });
    }
    if (n.type === 'output') {
      // 인쇄/출력: 아래쪽이 물결인 문서 모양
      var wave = n.h * 0.16;
      var d = 'M ' + l + ' ' + t + ' H ' + r + ' V ' + (b - wave) +
              ' C ' + (r - n.w * 0.28) + ' ' + (b + wave) + ', ' +
                      (l + n.w * 0.28) + ' ' + (b - wave * 2.2) + ', ' +
                      l + ' ' + (b - wave) + ' Z';
      return svgEl('path', { d: d });
    }
    return svgEl('rect', { x: l, y: t, width: n.w, height: n.h, rx: 3, ry: 3 });
  }

  /* ── 간선 ──────────────────────────────────────────────── */

  function edgePoints(e, byId) {
    var a = byId[e.from], b = byId[e.to];
    if (!a || !b) throw new Error('간선의 노드를 찾을 수 없습니다: ' + e.from + '→' + e.to);
    var p0 = anchor(a, e.fromSide || 'bottom');
    var p1 = anchor(b, e.toSide || 'top');
    var mid = (e.via || []).map(function (p) { return { x: p[0], y: p[1] }; });
    return [p0].concat(mid, [p1]);
  }

  function drawEdge(svg, e, byId, markerId) {
    var pts = edgePoints(e, byId);
    var d = pts.map(function (p, i) { return (i ? 'L ' : 'M ') + p.x + ' ' + p.y; }).join(' ');
    var path = svgEl('path', {
      d: d, class: 'fc-edge', fill: 'none', 'marker-end': 'url(#' + markerId + ')'
    });
    svg.appendChild(path);
    return { path: path, points: pts };
  }

  /* ── 렌더링 ────────────────────────────────────────────── */

  function renderChart(host, spec) {
    var W = spec.width, H = spec.height;
    var byId = {};
    spec.nodes.forEach(function (n) { byId[n.id] = n; });

    /* scale: 한 슬라이드에 순서도를 둘 이상 놓을 때 비례 축소 */
    var s = spec.scale || 1;
    var wrap = div('fc-chart');
    wrap.style.width = (W * s) + 'px';
    wrap.style.height = (H * s) + 'px';

    var inner = div('fc-chart-inner');
    inner.style.width = W + 'px';
    inner.style.height = H + 'px';
    if (s !== 1) {
      inner.style.transform = 'scale(' + s + ')';
      inner.style.transformOrigin = '0 0';
    }

    var svg = svgEl('svg', {
      viewBox: '0 0 ' + W + ' ' + H,
      preserveAspectRatio: 'xMidYMid meet',
      width: '100%', height: '100%'
    });
    svg.style.overflow = 'hidden';

    var markerId = 'fc-arrow-' + Math.random().toString(36).slice(2, 8);
    var defs = svgEl('defs');
    var marker = svgEl('marker', {
      id: markerId, viewBox: '0 0 10 10', refX: '9', refY: '5',
      markerWidth: '6', markerHeight: '6', orient: 'auto-start-reverse'
    });
    marker.appendChild(svgEl('path', { d: 'M 0 0 L 10 5 L 0 10 z', class: 'fc-arrowhead' }));
    defs.appendChild(marker);
    svg.appendChild(defs);

    (spec.edges || []).forEach(function (e) { drawEdge(svg, e, byId, markerId); });

    var shapes = {};
    spec.nodes.forEach(function (n) {
      var s = shapeFor(n);
      s.setAttribute('class', 'fc-shape fc-shape--' + n.type);
      svg.appendChild(s);
      shapes[n.id] = s;
    });

    inner.appendChild(svg);

    /* 라벨은 HTML 레이어로 얹는다 (MathJax·한글 조판 품질 확보) */
    var labels = {};
    spec.nodes.forEach(function (n) {
      var lb = div('fc-label', {
        left: n.x + 'px', top: n.y + 'px', width: (n.w - 10) + 'px'
      });
      lb.innerHTML = n.label || '';
      inner.appendChild(lb);
      labels[n.id] = lb;
    });

    (spec.edges || []).forEach(function (e) {
      if (!e.label) return;
      var pts = edgePoints(e, byId);
      var at = e.labelAt || [(pts[0].x + pts[1].x) / 2, (pts[0].y + pts[1].y) / 2];
      var lb = div('fc-edge-label', { left: at[0] + 'px', top: at[1] + 'px' });
      lb.textContent = e.label;
      inner.appendChild(lb);
    });

    wrap.appendChild(inner);
    host.appendChild(wrap);
    return { wrap: wrap, shapes: shapes, labels: labels };
  }

  /* ── 추적표 ────────────────────────────────────────────── */

  function renderTable(host, columns) {
    var table = document.createElement('table');
    table.className = 'fc-table';
    var thead = document.createElement('thead');
    var tr = document.createElement('tr');
    columns.forEach(function (c) {
      var th = document.createElement('th');
      th.innerHTML = c;
      tr.appendChild(th);
    });
    thead.appendChild(tr);
    table.appendChild(thead);
    var tbody = document.createElement('tbody');
    table.appendChild(tbody);
    host.appendChild(table);
    return tbody;
  }

  /* ── 컨트롤러 ──────────────────────────────────────────── */

  function Controller(root, spec) {
    this.spec = spec;
    this.root = root;
    this.result = spec.trace();
    this.steps = this.result.steps;
    this.i = -1;

    var chartHost = root.querySelector('[data-fc-chart]');
    var tableHost = root.querySelector('[data-fc-table]');
    var descHost  = root.querySelector('[data-fc-desc]');

    this.view = renderChart(chartHost, spec);
    this.tbody = tableHost ? renderTable(tableHost, this.result.columns) : null;
    this.descHost = descHost;

    this.baseLabels = {};
    var self = this;
    Object.keys(this.view.labels).forEach(function (id) {
      self.baseLabels[id] = self.view.labels[id].innerHTML;
    });

    this.render();
  }

  Controller.prototype.hasNext = function () { return this.i < this.steps.length - 1; };
  Controller.prototype.hasPrev = function () { return this.i > -1; };
  Controller.prototype.next = function () { if (this.hasNext()) { this.i++; this.render(); } };
  Controller.prototype.prev = function () { if (this.hasPrev()) { this.i--; this.render(); } };
  Controller.prototype.reset = function () { this.i = -1; this.render(); };
  Controller.prototype.end = function () { this.i = this.steps.length - 1; this.render(); };

  Controller.prototype.render = function () {
    var self = this;
    var step = this.i >= 0 ? this.steps[this.i] : null;

    /* 노드 강조 */
    Object.keys(this.view.shapes).forEach(function (id) {
      self.view.shapes[id].classList.remove('is-active');
      self.view.labels[id].classList.remove('is-active');
    });
    if (step && step.node && this.view.shapes[step.node]) {
      this.view.shapes[step.node].classList.add('is-active');
      this.view.labels[step.node].classList.add('is-active');
    }

    /* 라벨 치환 (빈칸 공개형 문제) */
    Object.keys(this.baseLabels).forEach(function (id) {
      self.view.labels[id].innerHTML = self.baseLabels[id];
      self.view.labels[id].classList.remove('is-revealed');
    });
    for (var k = 0; k <= this.i; k++) {
      var s = this.steps[k];
      if (!s.setLabel) continue;
      Object.keys(s.setLabel).forEach(function (id) {
        if (!self.view.labels[id]) return;
        self.view.labels[id].innerHTML = s.setLabel[id];
        self.view.labels[id].classList.add('is-revealed');
      });
    }

    /* 추적표 */
    if (this.tbody) {
      this.tbody.innerHTML = '';
      /* row: 한 줄 추가 · rows: 여러 줄 추가 · rowsReset: 지금까지의 줄을 버리고 다시 시작
         (같은 순서도를 다른 조건으로 돌려 보여 줄 때 표를 갈아 끼운다) */
      var rows = [];
      for (var j = 0; j <= this.i; j++) {
        var st = this.steps[j];
        if (st.rowsReset) rows = [];
        if (st.row) rows.push(st.row);
        if (st.rows) rows = rows.concat(st.rows);
      }
      rows.forEach(function (r, idx) {
        var tr = document.createElement('tr');
        if (idx === rows.length - 1) tr.className = 'is-current';
        if (r.__ellipsis) tr.className = 'is-ellipsis';
        self.result.columns.forEach(function (c, ci) {
          var td = document.createElement('td');
          td.innerHTML = r.__ellipsis ? (ci === 0 ? '⋮' : '⋮') : (r[c] === undefined ? '' : r[c]);
          tr.appendChild(td);
        });
        self.tbody.appendChild(tr);
      });
    }

    /* 설명 */
    if (this.descHost) {
      this.descHost.innerHTML = step ? (step.desc || '') : (this.spec.intro || '시작하려면 [다음]을 누르세요.');
      this.descHost.className = 'fc-desc' + (step && step.tone ? ' fc-desc--' + step.tone : '');
    }

    var counter = this.root.querySelector('[data-fc-counter]');
    if (counter) counter.textContent = (this.i + 1) + ' / ' + this.steps.length;

    if (global.safeTypeset) global.safeTypeset([this.root]);
    if (this.spec.onStep) this.spec.onStep(this, step);
  };

  /* ── 여러 순서도를 한 슬라이드에서 차례로 ──────────────────
     앞 순서도를 끝까지 돌린 뒤 다음 순서도로 넘어간다.
     (두 순서도를 비교하는 문제에서 사용) */

  function Sequence(controllers) { this.list = controllers; }

  Sequence.prototype.hasNext = function () {
    return this.list.some(function (c) { return c.hasNext(); });
  };
  Sequence.prototype.hasPrev = function () {
    return this.list.some(function (c) { return c.hasPrev(); });
  };
  Sequence.prototype.next = function () {
    for (var i = 0; i < this.list.length; i++) {
      if (this.list[i].hasNext()) { this.list[i].next(); return; }
    }
  };
  Sequence.prototype.prev = function () {
    for (var i = this.list.length - 1; i >= 0; i--) {
      if (this.list[i].hasPrev()) { this.list[i].prev(); return; }
    }
  };
  Sequence.prototype.reset = function () { this.list.forEach(function (c) { c.reset(); }); };
  Sequence.prototype.end   = function () { this.list.forEach(function (c) { c.end(); }); };

  global.FlowChart = {
    Controller: Controller,
    Sequence: Sequence,
    ELLIPSIS: { __ellipsis: true }
  };
})(window);
