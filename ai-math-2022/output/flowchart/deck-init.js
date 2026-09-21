/* ============================================================
   deck-init.js — 슬라이드와 순서도 컨트롤러를 연결한다.
     · [data-fc-root] 하나당 컨트롤러 하나
     · 한 슬라이드에 여러 개면 Sequence(앞을 끝낸 뒤 다음)로 묶는다
     · →/Space/← 로 단계 이동, 단계가 끝나면 슬라이드 이동
   ============================================================ */
(function (global) {
  'use strict';

  function whenMathJaxReady(fn) {
    if (global.MathJax && global.MathJax.startup && global.MathJax.startup.promise) {
      global.MathJax.startup.promise.then(fn).catch(function (err) {
        console.warn('MathJax 준비 실패, 수식 없이 진행합니다.', err);
        fn();
      });
    } else {
      setTimeout(function () { whenMathJaxReady(fn); }, 60);
    }
  }

  /* 슬라이드 <section> → 컨트롤러(또는 Sequence) */
  var bySection = new Map();

  function buildRoot(root) {
    var name = root.dataset.fcSpec;
    var base = global.FCProblems[name];
    if (!base) throw new Error('순서도 정의를 찾을 수 없습니다: ' + name);

    /* 원본 spec은 건드리지 않고 복사본에 슬라이드별 설정을 얹는다 */
    var spec = Object.assign({}, base);
    if (root.dataset.fcScale) spec.scale = parseFloat(root.dataset.fcScale);

    var ctrl = new global.FlowChart.Controller(root, spec);

    root.querySelectorAll('[data-fc-act]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var act = btn.dataset.fcAct;
        if (act === 'next') ctrl.next();
        else if (act === 'prev') ctrl.prev();
        else if (act === 'reset') ctrl.reset();
        else if (act === 'end') ctrl.end();
      });
    });

    var chartHost = root.querySelector('[data-fc-chart]');
    if (chartHost) {
      chartHost.style.cursor = 'pointer';
      chartHost.addEventListener('click', function () { ctrl.next(); });
    }

    return ctrl;
  }

  function init() {
    document.querySelectorAll('section.fc-slide').forEach(function (sec) {
      var roots = [].slice.call(sec.querySelectorAll('[data-fc-root]'));
      if (!roots.length) return;
      var ctrls = roots.map(buildRoot);
      bySection.set(sec, ctrls.length > 1 ? new global.FlowChart.Sequence(ctrls) : ctrls[0]);
    });

    wireConclusion();
    wireKeyboard();
    global.safeTypeset();
  }

  /* 슬라이드 ③ : 두 순서도가 모두 끝나면 S − T 결론을 띄운다 */
  function wireConclusion() {
    var sec = document.getElementById('s13');
    if (!sec) return;
    var group = bySection.get(sec);
    if (!group || !group.list || group.list.length < 2) return;

    var left = group.list[0], right = group.list[1];
    var box = sec.querySelector('[data-fc-conclusion]');
    if (!box) return;

    var S = left.result.answer, T = right.result.answer;
    box.innerHTML = '같은 \\(2N\\)을 더하는데도 왼쪽은 다섯 번, 오른쪽은 네 번 더했습니다. ' +
                    '\\(\\;S - T = ' + S + ' - ' + T + ' = ' + (S - T) + '\\)';

    var update = function () {
      var done = !left.hasNext() && !right.hasNext();
      box.classList.toggle('visible', done);
    };
    left.spec.onStep = update;
    right.spec.onStep = update;
    update();
  }

  function currentController() {
    return bySection.get(global.Reveal.getCurrentSlide());
  }

  function advance(dir) {
    var c = currentController();
    if (c) {
      if (dir > 0 && c.hasNext()) { c.next(); return; }
      if (dir < 0 && c.hasPrev()) { c.prev(); return; }
    }
    if (dir > 0) global.Reveal.next(); else global.Reveal.prev();
  }

  function wireKeyboard() {
    global.Reveal.configure({
      keyboard: {
        39: function () { advance(1); },   /* → */
        32: function () { advance(1); },   /* Space */
        34: function () { advance(1); },   /* PageDown (프레젠터 리모컨) */
        78: function () { advance(1); },   /* N */
        37: function () { advance(-1); },  /* ← */
        33: function () { advance(-1); },  /* PageUp */
        80: function () { advance(-1); },  /* P */
        82: function () {                  /* R : 이 슬라이드 처음부터 */
          var c = currentController();
          if (c) c.reset();
        }
      }
    });
  }

  global.Reveal.on('ready', function () { whenMathJaxReady(init); });
})(window);
