/* ============================================================
   problems-blank.js — 빈칸 채우기형 순서도
     · 슬라이드 11 : 이차방정식의 서로 다른 실근의 개수 (가)(나)(다)
     · 슬라이드 12 : 1부터 10까지의 합, 판단 조건 빈칸
   ============================================================ */
(function (global) {
  'use strict';

  var seq = global.FCUtil.seq;
  var P = global.FCProblems = global.FCProblems || {};

  /* ── 슬라이드 11 : 판별식으로 실근의 개수 판정 ─────────────── */

  P.discriminant = {
    width: 820,
    height: 690,
    intro: '알고리즘 (i)~(iv)를 순서도의 어느 자리에 넣어야 할지 하나씩 맞춰 봅시다.',
    nodes: [
      { id: 'start', type: 'terminal', x: 380, y: 40,  w: 160, h: 52, label: '시작' },
      { id: 'calc',  type: 'process',  x: 380, y: 140, w: 280, h: 62, label: '\\(D = b^2 - 4ac\\)' },
      { id: 'd1',    type: 'decision', x: 250, y: 270, w: 260, h: 104, label: '<span class="fc-blank">(가)</span>' },
      { id: 'd2',    type: 'decision', x: 570, y: 395, w: 230, h: 96,  label: '\\(D = 0\\)' },
      { id: 'o2',    type: 'output',   x: 140, y: 520, w: 150, h: 68, label: '2' },
      { id: 'oNa',   type: 'output',   x: 420, y: 520, w: 150, h: 68, label: '<span class="fc-blank">(나)</span>' },
      { id: 'oDa',   type: 'output',   x: 740, y: 520, w: 150, h: 68, label: '<span class="fc-blank">(다)</span>' },
      { id: 'end',   type: 'terminal', x: 380, y: 635, w: 160, h: 52, label: '끝' }
    ],
    edges: [
      { from: 'start', to: 'calc' },
      { from: 'calc', to: 'd1', via: [[380, 194], [250, 194]] },
      { from: 'd1', to: 'o2',  fromSide: 'left',  via: [[140, 270]], label: '예',    labelAt: [186, 246] },
      { from: 'd1', to: 'd2',  fromSide: 'right', via: [[570, 270]], label: '아니요', labelAt: [462, 246] },
      { from: 'd2', to: 'oNa', fromSide: 'left',  via: [[420, 395]], label: '예',    labelAt: [466, 371] },
      { from: 'd2', to: 'oDa', fromSide: 'right', via: [[740, 395]], label: '아니요', labelAt: [742, 367] },
      { from: 'o2',  to: 'end', via: [[140, 598], [380, 598]] },
      { from: 'oNa', to: 'end', via: [[420, 598], [380, 598]] },
      { from: 'oDa', to: 'end', via: [[740, 598], [380, 598]] }
    ],
    trace: function () {
      var steps = [];
      steps.push({ node: 'start', desc: '순서도는 <b>시작</b>에서 출발합니다.' });
      steps.push({ node: 'calc',  desc: '먼저 판별식 \\(D = b^2 - 4ac\\)를 계산합니다. 실근의 개수는 오직 이 \\(D\\) 하나로 결정됩니다.' });
      steps.push({
        node: 'd1',
        desc: '첫 번째 판단입니다. 「예」로 가면 곧바로 <b>2</b>가 출력되지요. ' +
              '알고리즘 (ii)에서 실근이 2개인 경우는 \\(D>0\\)일 때입니다. ' +
              '따라서 <b>(가) = \\(D>0\\)</b>.',
        setLabel: { d1: '\\(D>0\\)' },
        tone: 'ok'
      });
      steps.push({ node: 'o2', desc: '\\(D>0\\)이면 서로 다른 실근의 개수는 <b>2</b>. 여기서 바로 끝납니다.' });
      steps.push({ node: 'd2', desc: '\\(D>0\\)이 아니면 남은 경우는 \\(D=0\\) 또는 \\(D&lt;0\\). 그래서 두 번째 판단 \\(D=0\\)으로 갑니다.' });
      steps.push({
        node: 'oNa',
        desc: '알고리즘 (iii): \\(D=0\\)이면 실근은 <b>1</b>개. 따라서 <b>(나) = 1</b>.',
        setLabel: { oNa: '1' },
        tone: 'ok'
      });
      steps.push({
        node: 'oDa',
        desc: '남은 경우는 \\(D&lt;0\\)뿐입니다. 알고리즘 (iv)에 따라 실근은 <b>0</b>개. 따라서 <b>(다) = 0</b>.',
        setLabel: { oDa: '0' },
        tone: 'ok'
      });
      steps.push({
        node: 'end',
        desc: '정리하면 <b>(가) \\(D>0\\), (나) 1, (다) 0</b>. ' +
              '판단을 하나 지날 때마다 경우가 하나씩 걸러지는 구조입니다.',
        tone: 'ok'
      });
      return { columns: [], steps: steps, answer: { 가: 'D>0', 나: 1, 다: 0 } };
    }
  };

  /* ── 슬라이드 12 : 1부터 10까지의 합, 판단 조건 빈칸 ───────── */

  P.sumTen = {
    width: 560,
    height: 770,
    intro: '빈칸을 비워 둔 채로 먼저 돌려 봅시다. 값이 어떻게 쌓이는지 보면 조건이 보입니다.',
    nodes: [
      { id: 'start', type: 'terminal', x: 280, y: 42,  w: 170, h: 56, label: '시작' },
      { id: 'init',  type: 'process',  x: 280, y: 152, w: 290, h: 96, label: '\\(S\\)에 1을 대입<br>\\(N\\)에 1을 대입' },
      { id: 'inc',   type: 'process',  x: 280, y: 278, w: 290, h: 64, label: '\\(N\\)에 \\(N+1\\)을 대입' },
      { id: 'add',   type: 'process',  x: 280, y: 382, w: 290, h: 64, label: '\\(S\\)에 \\(S+N\\)을 대입' },
      { id: 'cond',  type: 'decision', x: 280, y: 500, w: 320, h: 106, label: '<span class="fc-blank">?</span>' },
      { id: 'out',   type: 'output',   x: 280, y: 620, w: 260, h: 72, label: '\\(S\\)를 출력' },
      { id: 'end',   type: 'terminal', x: 280, y: 718, w: 170, h: 56, label: '끝' }
    ],
    edges: seq(['start', 'init', 'inc', 'add', 'cond']).concat([
      { from: 'cond', to: 'out', label: '예', labelAt: [304, 580] },
      { from: 'out', to: 'end' },
      {
        from: 'cond', to: 'inc', fromSide: 'left', toSide: 'left',
        via: [[40, 500], [40, 278]], label: '아니요', labelAt: [96, 478]
      }
    ]),
    trace: function () {
      var steps = [];
      var S = 1, N = 1, k = 0;

      steps.push({ node: 'start', desc: '시작합니다.' });
      steps.push({
        node: 'init',
        desc: '\\(S\\)에 1, \\(N\\)에 1을 대입합니다. 첫 항 1을 미리 넣어 둔 셈입니다.',
        row: { '회차': '초기', 'N': 1, 'S': 1 }
      });

      /* 조건을 비워 둔 채로 N=10까지 실제로 굴린다 */
      while (N < 10) {
        k++;
        var before = S;
        N = N + 1;
        S = S + N;
        var detail = (k <= 3 || N === 10);

        if (detail) {
          steps.push({ node: 'inc', desc: '\\(N\\)에 \\(N+1\\)을 대입 → <b>\\(N = ' + N + '\\)</b>' });
          steps.push({
            node: 'add',
            desc: '\\(S\\)에 \\(S+N\\)을 대입 → \\(' + before + ' + ' + N + ' = ' + S + '\\)',
            row: { '회차': k, 'N': N, 'S': S }
          });
          steps.push({
            node: 'cond',
            desc: '판단 자리입니다. 지금 \\(N=' + N + ',\\ S=' + S + '\\). ' +
                  (S === 55 ? '<b>드디어 \\(S=55\\)</b>입니다.' : '아직 55가 아니므로 더 돌아야 합니다.'),
            tone: S === 55 ? 'ok' : undefined
          });
        } else if (k === 4) {
          steps.push({
            node: 'add',
            desc: '같은 방식으로 \\(N\\)을 1씩 늘리며 \\(S\\)에 계속 더해 나갑니다.',
            row: global.FlowChart.ELLIPSIS
          });
        }
      }

      steps.push({
        node: 'cond',
        desc: '구하려는 값은 \\(1+2+\\cdots+10 = 55\\). 위 표에서 \\(S=55\\)가 되는 순간은 <b>\\(N=10\\)</b>일 때입니다. ' +
              '즉 빈칸은 <b>\\(N=10\\)에서 처음으로 참</b>이 되는 조건이어야 합니다.',
        tone: 'info'
      });

      /* 선택지 5개를 각각 실제로 실행해 본다 */
      var choices = [
        { tag: '①', tex: 'N &lt; 9',      f: function (n) { return n < 9; } },
        { tag: '②', tex: 'N > 9',      f: function (n) { return n > 9; } },
        { tag: '③', tex: 'N \\geq 9',  f: function (n) { return n >= 9; } },
        { tag: '④', tex: 'N > 10',     f: function (n) { return n > 10; } },
        { tag: '⑤', tex: 'N &lt; 10',     f: function (n) { return n < 10; } }
      ];

      var correct = null;
      choices.forEach(function (c) {
        var s2 = 1, n2 = 1, guard = 0;
        while (guard++ < 500) {
          n2 = n2 + 1;
          s2 = s2 + n2;
          if (c.f(n2)) break;
        }
        var good = (s2 === 55);
        if (good) correct = c;
        steps.push({
          node: 'cond',
          setLabel: { cond: '\\(' + c.tex + '\\)' },
          tone: good ? 'ok' : 'warn',
          desc: c.tag + ' \\(' + c.tex + '\\) → 처음 참이 되는 때는 \\(N=' + n2 + '\\), ' +
                '이때 출력값은 \\(S=' + s2 + '\\). ' +
                (good ? '<b>55와 일치 → 정답</b>' : '55가 아니므로 <b>오답</b>')
        });
      });

      steps.push({
        node: 'out',
        setLabel: { cond: '\\(' + correct.tex + '\\)' },
        tone: 'ok',
        desc: '정답은 <b>' + correct.tag + ' \\(' + correct.tex + '\\)</b>. ' +
              '③ \\(N \\geq 9\\)는 \\(N=9\\)에서 먼저 빠져나가 45가 되고, ' +
              '④ \\(N>10\\)은 한 번 더 돌아 66이 됩니다. <b>부등호 하나 차이로 답이 갈립니다.</b>'
      });

      return { columns: ['회차', 'N', 'S'], steps: steps, answer: correct.tag };
    }
  };
})(window);
