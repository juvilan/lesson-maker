/* ============================================================
   problems-trace.js — 값 추적형 순서도
     · 슬라이드 13 : 두 순서도의 S와 T  →  S − T
     · 슬라이드 14 : (1) a ← 2a − 1     (2) a ← a + n
     · 슬라이드 15 : 부분분수 합 S
   모든 값은 trace() 안에서 실제로 계산한다. 하드코딩 없음.
   ============================================================ */
(function (global) {
  'use strict';

  var seq = global.FCUtil.seq;
  var Frac = global.FCUtil.Frac;
  var P = global.FCProblems = global.FCProblems || {};
  var YN = function (b) { return '<b>' + (b ? '예' : '아니요') + '</b>'; };

  /* ── 슬라이드 13 (왼쪽) : 판정이 N ← N+1 보다 앞에 있다 ───── */

  P.sumS = {
    width: 500,
    height: 580,
    intro: '왼쪽 순서도를 먼저 끝까지 돌려 \\(S\\)를 구합니다.',
    nodes: [
      { id: 'start', type: 'terminal', x: 165, y: 34,  w: 150, h: 50, label: '시작' },
      { id: 'init',  type: 'process',  x: 165, y: 122, w: 215, h: 92, label: '\\(N \\leftarrow 1\\)<br>\\(S \\leftarrow 1\\)' },
      { id: 'add',   type: 'process',  x: 165, y: 232, w: 195, h: 62, label: '\\(S \\leftarrow S + 2N\\)' },
      { id: 'cond',  type: 'decision', x: 165, y: 340, w: 215, h: 92, label: '\\(N = 5?\\)' },
      { id: 'incr',  type: 'process',  x: 390, y: 232, w: 175, h: 62, label: '\\(N \\leftarrow N+1\\)' },
      { id: 'out',   type: 'output',   x: 165, y: 446, w: 205, h: 66, label: '\\(S\\)를 인쇄' },
      { id: 'end',   type: 'terminal', x: 165, y: 532, w: 150, h: 50, label: '끝' }
    ],
    edges: seq(['start', 'init', 'add', 'cond']).concat([
      { from: 'cond', to: 'out', label: '예', labelAt: [191, 402] },
      { from: 'out', to: 'end' },
      { from: 'cond', to: 'incr', fromSide: 'right', toSide: 'bottom', via: [[390, 340]], label: '아니요', labelAt: [340, 318] },
      { from: 'incr', to: 'add', fromSide: 'top', toSide: 'top', via: [[390, 186], [165, 186]] }
    ]),
    trace: function () {
      var steps = [], N = 1, S = 1;
      steps.push({ node: 'start', desc: '왼쪽 순서도를 시작합니다.' });
      steps.push({
        node: 'init', desc: '\\(N \\leftarrow 1,\\ S \\leftarrow 1\\)',
        row: { 'N': 1, 'S': 1, '판정': '—' }
      });
      while (true) {
        var before = S;
        S = S + 2 * N;
        steps.push({
          node: 'add',
          desc: '\\(S \\leftarrow S + 2N\\) → \\(' + before + ' + ' + (2 * N) + ' = ' + S + '\\) &nbsp;(지금 \\(N = ' + N + '\\))'
        });
        var done = (N === 5);
        steps.push({
          node: 'cond',
          desc: '지금 \\(N = ' + N + '\\)이므로 \\(N = 5?\\) → ' + YN(done),
          row: { 'N': N, 'S': S, '판정': done ? '예' : '아니요' }
        });
        if (done) break;
        N = N + 1;
        steps.push({ node: 'incr', desc: '\\(N \\leftarrow N+1\\) → <b>\\(N = ' + N + '\\)</b>' });
      }
      steps.push({ node: 'out', tone: 'ok', desc: '\\(S\\)를 인쇄 → <b>\\(S = ' + S + '\\)</b>' });
      steps.push({
        node: 'end', tone: 'ok',
        desc: '왼쪽은 <b>\\(N=1\\)부터 \\(N=5\\)까지 다섯 번</b> 더했습니다. \\(S = ' + S + '\\)'
      });
      return { columns: ['N', 'S', '판정'], steps: steps, answer: S };
    }
  };

  /* ── 슬라이드 13 (오른쪽) : 판정이 N ← N+1 뒤에 있다 ──────── */

  P.sumT = {
    width: 440,
    height: 650,
    intro: '이제 오른쪽 순서도입니다. 상자 순서가 한 칸 다릅니다.',
    nodes: [
      { id: 'start', type: 'terminal', x: 180, y: 34,  w: 150, h: 50, label: '시작' },
      { id: 'init',  type: 'process',  x: 180, y: 122, w: 220, h: 92, label: '\\(N \\leftarrow 1\\)<br>\\(T \\leftarrow 1\\)' },
      { id: 'add',   type: 'process',  x: 180, y: 232, w: 220, h: 62, label: '\\(T \\leftarrow T + 2N\\)' },
      { id: 'incr',  type: 'process',  x: 180, y: 320, w: 220, h: 62, label: '\\(N \\leftarrow N+1\\)' },
      { id: 'cond',  type: 'decision', x: 180, y: 424, w: 230, h: 92, label: '\\(N = 5?\\)' },
      { id: 'out',   type: 'output',   x: 180, y: 530, w: 210, h: 66, label: '\\(T\\)를 인쇄' },
      { id: 'end',   type: 'terminal', x: 180, y: 616, w: 150, h: 50, label: '끝' }
    ],
    edges: seq(['start', 'init', 'add', 'incr', 'cond']).concat([
      { from: 'cond', to: 'out', label: '예', labelAt: [206, 486] },
      { from: 'out', to: 'end' },
      { from: 'cond', to: 'add', fromSide: 'right', toSide: 'top', via: [[390, 424], [390, 188], [180, 188]], label: '아니요', labelAt: [354, 400] }
    ]),
    trace: function () {
      var steps = [], N = 1, T = 1;
      steps.push({ node: 'start', desc: '오른쪽 순서도를 시작합니다.' });
      steps.push({
        node: 'init', desc: '\\(N \\leftarrow 1,\\ T \\leftarrow 1\\)',
        row: { 'N': 1, 'T': 1, '판정': '—' }
      });
      while (true) {
        var before = T;
        T = T + 2 * N;
        steps.push({
          node: 'add',
          desc: '\\(T \\leftarrow T + 2N\\) → \\(' + before + ' + ' + (2 * N) + ' = ' + T + '\\) &nbsp;(지금 \\(N = ' + N + '\\))'
        });
        N = N + 1;
        steps.push({
          node: 'incr',
          desc: '\\(N \\leftarrow N+1\\) → <b>\\(N = ' + N + '\\)</b> &nbsp;— <u>판정보다 먼저</u> \\(N\\)이 올라갑니다.',
          tone: 'warn'
        });
        var done = (N === 5);
        steps.push({
          node: 'cond',
          desc: '지금 \\(N = ' + N + '\\)이므로 \\(N = 5?\\) → ' + YN(done),
          row: { 'N': N, 'T': T, '판정': done ? '예' : '아니요' }
        });
        if (done) break;
      }
      steps.push({ node: 'out', tone: 'ok', desc: '\\(T\\)를 인쇄 → <b>\\(T = ' + T + '\\)</b>' });
      steps.push({
        node: 'end', tone: 'ok',
        desc: '오른쪽은 \\(N\\)이 먼저 5가 되어 버려 <b>\\(N=4\\)까지 네 번만</b> 더했습니다. \\(T = ' + T + '\\)'
      });
      return { columns: ['N', 'T', '판정'], steps: steps, answer: T };
    }
  };

  /* ── 슬라이드 14 (1) : a ← 2a − 1, n = 30에서 종료 ────────── */

  P.doubleA = {
    width: 480,
    height: 690,
    intro: '반복이 29번입니다. 몇 번만 돌려 보고 규칙을 찾읍시다.',
    nodes: [
      { id: 'start', type: 'terminal', x: 200, y: 40,  w: 150, h: 52, label: '시작' },
      { id: 'init',  type: 'process',  x: 200, y: 142, w: 250, h: 98, label: '\\(a \\leftarrow 3\\)<br>\\(n \\leftarrow 1\\)' },
      { id: 'step',  type: 'process',  x: 200, y: 278, w: 250, h: 98, label: '\\(a \\leftarrow 2a - 1\\)<br>\\(n \\leftarrow n + 1\\)' },
      { id: 'cond',  type: 'decision', x: 200, y: 404, w: 250, h: 96, label: '\\(n = 30?\\)' },
      { id: 'out',   type: 'output',   x: 200, y: 516, w: 200, h: 68, label: '\\(a\\)' },
      { id: 'end',   type: 'terminal', x: 200, y: 614, w: 150, h: 52, label: '끝' }
    ],
    edges: seq(['start', 'init', 'step', 'cond']).concat([
      { from: 'cond', to: 'out', label: '예', labelAt: [226, 470] },
      { from: 'out', to: 'end' },
      { from: 'cond', to: 'step', fromSide: 'right', toSide: 'top', via: [[430, 404], [430, 214], [200, 214]], label: '아니요', labelAt: [394, 380] }
    ]),
    trace: function () {
      var steps = [], a = 3, n = 1, it = 0, diffs = [];
      steps.push({ node: 'start', desc: '시작합니다.' });
      steps.push({ node: 'init', desc: '\\(a \\leftarrow 3,\\ n \\leftarrow 1\\)', row: { '반복': '초기', 'n': 1, 'a': 3, 'a−1': 2 } });
      while (true) {
        it++;
        var pa = a;
        a = 2 * a - 1;
        n = n + 1;
        if (it <= 4) diffs.push(a - 1);
        var detail = (it <= 4 || n === 30);
        if (detail) {
          steps.push({
            node: 'step',
            desc: '\\(a \\leftarrow 2a-1\\) → \\(2 \\times ' + pa + ' - 1 = ' + a + '\\),&nbsp; \\(n \\leftarrow n+1\\) → \\(n = ' + n + '\\)',
            row: { '반복': it, 'n': n, 'a': a, 'a−1': a - 1 }
          });
          steps.push({ node: 'cond', desc: '\\(n = ' + n + '\\) → \\(n = 30?\\) ' + YN(n === 30) });
        } else if (it === 5) {
          steps.push({
            node: 'step',
            desc: '이런 식으로 계속 반복됩니다. 29번을 다 돌리는 대신 <b>규칙</b>을 찾읍시다.',
            row: global.FlowChart.ELLIPSIS
          });
          steps.push({
            node: 'step', tone: 'info',
            desc: '표의 맨 오른쪽 \\(a-1\\) 열을 보세요: \\(' + diffs.join(',\\ ') + ',\\ \\ldots\\) — <b>매번 정확히 2배</b>입니다. ' +
                  '\\(a \\leftarrow 2a-1\\)은 \\(a-1 \\leftarrow 2(a-1)\\)과 같은 말이니까요. ' +
                  '처음 \\(a-1 = 2\\)였으므로 \\(k\\)번 반복하면 \\(a - 1 = 2^{k+1}\\).'
          });
        }
        if (n === 30) break;
      }
      var exp = it + 1;
      steps.push({
        node: 'out', tone: 'ok',
        desc: '\\(n\\)은 1에서 30까지 올라갔으니 반복은 모두 <b>' + it + '회</b>. ' +
              '따라서 \\(a - 1 = 2^{' + exp + '}\\), 즉 \\(a = 2^{' + exp + '} + 1\\).'
      });
      steps.push({
        node: 'end', tone: 'ok',
        desc: '인쇄되는 값은 <b>\\(a = 2^{' + exp + '} + 1 = ' + a + '\\)</b>'
      });
      return { columns: ['반복', 'n', 'a', 'a−1'], steps: steps, answer: a };
    }
  };

  /* ── 슬라이드 14 (2) : a ← a + n, n ← n + 2, n = 100에서 종료 ─ */

  P.sumEven = {
    width: 480,
    height: 730,
    intro: '이번에는 반복이 50번입니다. 더해지는 값의 규칙을 봅시다.',
    nodes: [
      { id: 'start', type: 'terminal', x: 200, y: 40,  w: 150, h: 52, label: '시작' },
      { id: 'init',  type: 'process',  x: 200, y: 142, w: 250, h: 98, label: '\\(a \\leftarrow 0\\)<br>\\(n \\leftarrow 0\\)' },
      { id: 'add',   type: 'process',  x: 200, y: 268, w: 250, h: 64, label: '\\(a \\leftarrow a + n\\)' },
      { id: 'inc',   type: 'process',  x: 200, y: 362, w: 250, h: 64, label: '\\(n \\leftarrow n + 2\\)' },
      { id: 'cond',  type: 'decision', x: 200, y: 474, w: 250, h: 96, label: '\\(n = 100?\\)' },
      { id: 'out',   type: 'output',   x: 200, y: 586, w: 200, h: 68, label: '\\(a\\)' },
      { id: 'end',   type: 'terminal', x: 200, y: 684, w: 150, h: 52, label: '끝' }
    ],
    edges: seq(['start', 'init', 'add', 'inc', 'cond']).concat([
      { from: 'cond', to: 'out', label: '예', labelAt: [226, 540] },
      { from: 'out', to: 'end' },
      { from: 'cond', to: 'add', fromSide: 'right', toSide: 'top', via: [[430, 474], [430, 220], [200, 220]], label: '아니요', labelAt: [394, 450] }
    ]),
    trace: function () {
      var steps = [], a = 0, n = 0, it = 0, lastAdded = 0;
      steps.push({ node: 'start', desc: '시작합니다.' });
      steps.push({ node: 'init', desc: '\\(a \\leftarrow 0,\\ n \\leftarrow 0\\)', row: { '반복': '초기', '더한 값': '—', 'n': 0, 'a': 0 } });
      while (true) {
        it++;
        var pa = a, pn = n;
        a = a + n;
        n = n + 2;
        lastAdded = pn;
        var detail = (it <= 4 || n === 100);
        if (detail) {
          steps.push({ node: 'add', desc: '\\(a \\leftarrow a + n\\) → \\(' + pa + ' + ' + pn + ' = ' + a + '\\)' });
          steps.push({
            node: 'inc', desc: '\\(n \\leftarrow n + 2\\) → \\(n = ' + n + '\\)',
            row: { '반복': it, '더한 값': pn, 'n': n, 'a': a }
          });
          steps.push({ node: 'cond', desc: '\\(n = ' + n + '\\) → \\(n = 100?\\) ' + YN(n === 100) });
        } else if (it === 5) {
          steps.push({
            node: 'add',
            desc: '같은 방식으로 계속 반복됩니다. <b>더한 값</b> 열의 규칙을 보세요.',
            row: global.FlowChart.ELLIPSIS
          });
          steps.push({
            node: 'add', tone: 'info',
            desc: '\\(a\\)에 더해지는 값은 \\(0,\\ 2,\\ 4,\\ 6,\\ \\ldots\\) — <b>짝수를 차례로</b> 더하고 있습니다. ' +
                  '주의: \\(a \\leftarrow a+n\\)이 \\(n \\leftarrow n+2\\)보다 <u>먼저</u>이므로, 마지막에 더해지는 값은 100이 아닙니다.'
          });
        }
        if (n === 100) break;
      }
      var half = lastAdded / 2;
      steps.push({
        node: 'out', tone: 'ok',
        desc: '반복은 <b>' + it + '회</b>이고, 마지막에 더한 값은 <b>' + lastAdded + '</b>입니다. ' +
              '따라서 \\(a = 0 + 2 + 4 + \\cdots + ' + lastAdded + ' = 2(1 + 2 + \\cdots + ' + half + ')\\).'
      });
      steps.push({
        node: 'end', tone: 'ok',
        desc: '<b>\\(a = 2 \\times \\dfrac{' + half + ' \\times ' + (half + 1) + '}{2} = ' + a + '\\)</b>'
      });
      return { columns: ['반복', '더한 값', 'n', 'a'], steps: steps, answer: a };
    }
  };

  /* ── 슬라이드 15 : 부분분수 합 ──────────────────────────── */

  P.partialFrac = {
    width: 560,
    height: 750,
    intro: '분수가 쌓입니다. 세 번만 직접 더해 보면 방법이 보입니다.',
    nodes: [
      { id: 'start', type: 'terminal', x: 240, y: 42,  w: 160, h: 54, label: '시작' },
      { id: 'init',  type: 'process',  x: 240, y: 146, w: 260, h: 98, label: '\\(n \\leftarrow 0\\)<br>\\(S \\leftarrow 0\\)' },
      { id: 'inc',   type: 'process',  x: 240, y: 272, w: 260, h: 64, label: '\\(n \\leftarrow n + 1\\)' },
      { id: 'add',   type: 'process',  x: 240, y: 386, w: 360, h: 104, label: '\\(S \\leftarrow S + \\dfrac{1}{(3n-1)(3n+2)}\\)' },
      { id: 'cond',  type: 'decision', x: 240, y: 508, w: 250, h: 96, label: '\\(n = 10?\\)' },
      { id: 'out',   type: 'output',   x: 240, y: 620, w: 230, h: 70, label: '\\(S\\)를 인쇄' },
      { id: 'end',   type: 'terminal', x: 240, y: 716, w: 160, h: 54, label: '끝' }
    ],
    edges: seq(['start', 'init', 'inc', 'add', 'cond']).concat([
      { from: 'cond', to: 'out', label: '예', labelAt: [266, 576] },
      { from: 'out', to: 'end' },
      { from: 'cond', to: 'inc', fromSide: 'right', toSide: 'top', via: [[500, 508], [500, 224], [240, 224]], label: '아니요', labelAt: [464, 484] }
    ]),
    trace: function () {
      var steps = [], S = new Frac(0, 1), n = 0;
      steps.push({ node: 'start', desc: '시작합니다.' });
      steps.push({ node: 'init', desc: '\\(n \\leftarrow 0,\\ S \\leftarrow 0\\)', row: { 'n': 0, '더한 항': '—', 'S': '\\(0\\)' } });
      while (true) {
        n = n + 1;
        var term = new Frac(1, (3 * n - 1) * (3 * n + 2));
        var prev = S;
        S = S.add(term);
        var detail = (n <= 3 || n === 10);
        if (detail) {
          steps.push({ node: 'inc', desc: '\\(n \\leftarrow n + 1\\) → \\(n = ' + n + '\\)' });
          steps.push({
            node: 'add',
            desc: '\\(S \\leftarrow S + \\dfrac{1}{(' + (3 * n - 1) + ')(' + (3 * n + 2) + ')} = ' +
                  prev.tex() + ' + ' + term.tex() + ' = ' + S.tex() + '\\)',
            row: { 'n': n, '더한 항': '\\(' + term.tex() + '\\)', 'S': '\\(' + S.tex() + '\\)' }
          });
          steps.push({ node: 'cond', desc: '\\(n = ' + n + '\\) → \\(n = 10?\\) ' + YN(n === 10) });
        } else if (n === 4) {
          steps.push({
            node: 'add',
            desc: '이대로 10번까지 분수를 더하면 계산이 번거롭습니다. 항을 <b>쪼개</b> 봅시다.',
            row: global.FlowChart.ELLIPSIS
          });
          steps.push({
            node: 'add', tone: 'info',
            desc: '부분분수: \\(\\dfrac{1}{(3n-1)(3n+2)} = \\dfrac{1}{3}\\left(\\dfrac{1}{3n-1} - \\dfrac{1}{3n+2}\\right)\\). ' +
                  '이렇게 쓰면 앞 항의 뒤쪽과 뒤 항의 앞쪽이 <b>서로 지워집니다.</b>'
          });
        }
        if (n === 10) break;
      }
      /* 망원합(telescoping)으로 독립 계산 → 누적합과 일치하는지 자체 검증 */
      var tele = new Frac(1, 3).mul(new Frac(1, 2).sub(new Frac(1, 3 * n + 2)));
      var agree = (tele.n === S.n && tele.d === S.d);
      steps.push({
        node: 'out', tone: 'ok',
        desc: '가운데가 모두 지워지고 <b>맨 앞</b>과 <b>맨 뒤</b>만 남습니다: ' +
              '\\(S = \\dfrac{1}{3}\\left(\\dfrac{1}{2} - \\dfrac{1}{' + (3 * n + 2) + '}\\right) = ' + tele.tex() + '\\)' +
              (agree ? '' : ' <b>(경고: 누적합 ' + S.tex() + '과 불일치)</b>')
      });
      steps.push({
        node: 'end', tone: 'ok',
        desc: '인쇄되는 값은 \\(S = ' + S.tex() + '\\) \\(( = ' + (S.n / S.d) + ')\\). ' +
              '한 항씩 더한 결과와 부분분수로 구한 결과가 ' + (agree ? '일치합니다.' : '다릅니다 — 확인 필요.')
      });
      return { columns: ['n', '더한 항', 'S'], steps: steps, answer: S.tex() };
    }
  };
})(window);
