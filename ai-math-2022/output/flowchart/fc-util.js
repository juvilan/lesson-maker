/* ============================================================
   fc-util.js — 순서도 문제 정의에 쓰는 작은 도우미들
   ============================================================ */
(function (global) {
  'use strict';

  /* 위에서 아래로 이어지는 기본 간선을 한 번에 만든다 */
  function seq(ids) {
    return ids.slice(0, -1).map(function (id, i) {
      return { from: id, to: ids[i + 1] };
    });
  }

  /* 기약분수 (슬라이드 15의 부분분수 합에 사용) */
  function gcd(a, b) {
    a = Math.abs(a); b = Math.abs(b);
    while (b) { var t = a % b; a = b; b = t; }
    return a;
  }

  function Frac(n, d) {
    if (d === undefined) d = 1;
    if (d < 0) { n = -n; d = -d; }
    var g = gcd(n, d) || 1;
    this.n = n / g;
    this.d = d / g;
  }

  Frac.prototype.add = function (o) {
    return new Frac(this.n * o.d + o.n * this.d, this.d * o.d);
  };

  Frac.prototype.sub = function (o) {
    return new Frac(this.n * o.d - o.n * this.d, this.d * o.d);
  };

  Frac.prototype.mul = function (o) {
    return new Frac(this.n * o.n, this.d * o.d);
  };

  Frac.prototype.tex = function () {
    return this.d === 1 ? String(this.n) : '\\dfrac{' + this.n + '}{' + this.d + '}';
  };

  global.FCUtil = { seq: seq, Frac: Frac };
})(window);
