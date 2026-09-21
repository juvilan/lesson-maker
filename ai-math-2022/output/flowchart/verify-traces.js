/* verify-traces.js — node로 trace()를 실행해 정답을 독립 확인한다.
   실행: node verify-traces.js  */
const fs = require('fs');
const path = require('path');

const sandbox = { FlowChart: { ELLIPSIS: { __ellipsis: true } } };
global.window = sandbox;

['fc-util.js', 'problems-blank.js', 'problems-trace.js'].forEach(f => {
  const code = fs.readFileSync(path.join(__dirname, f), 'utf8');
  new Function('window', code)(sandbox);
});

const P = sandbox.FCProblems;
const expected = {
  discriminant: { 가: 'D>0', 나: 1, 다: 0 },
  sumTen: '②',
  sumS: 31,
  sumT: 21,
  doubleA: Math.pow(2, 30) + 1,
  sumEven: 2450,
  partialFrac: '\\dfrac{5}{32}'
};

let fail = 0;
Object.keys(expected).forEach(key => {
  const r = P[key].trace();
  const got = r.answer;
  const exp = expected[key];
  const ok = JSON.stringify(got) === JSON.stringify(exp);
  if (!ok) fail++;
  console.log(
    `${ok ? 'PASS' : 'FAIL'}  ${key.padEnd(13)} 단계 ${String(r.steps.length).padStart(3)}개 | ` +
    `기댓값 ${JSON.stringify(exp)} / 실제 ${JSON.stringify(got)}`
  );
});

/* 모든 단계가 실제 노드를 가리키는지도 확인 */
Object.keys(P).forEach(key => {
  const ids = new Set(P[key].nodes.map(n => n.id));
  P[key].trace().steps.forEach((s, i) => {
    if (s.node && !ids.has(s.node)) { fail++; console.log(`FAIL  ${key} 단계 ${i}: 없는 노드 '${s.node}'`); }
    Object.keys(s.setLabel || {}).forEach(id => {
      if (!ids.has(id)) { fail++; console.log(`FAIL  ${key} 단계 ${i}: setLabel 대상 없음 '${id}'`); }
    });
  });
  P[key].edges.forEach(e => {
    if (!ids.has(e.from) || !ids.has(e.to)) { fail++; console.log(`FAIL  ${key} 간선 ${e.from}→${e.to}: 없는 노드`); }
  });
});

/* 수식 \( ... \) 안에 HTML 태그가 들어가면 MathJax가 통째로 건너뛴다.
   화면에 원시 TeX가 그대로 남으므로 여기서 막는다. */
Object.keys(P).forEach(key => {
  const check = (where, html) => {
    if (typeof html !== 'string') return;
    const re = /\\\(([\s\S]*?)\\\)/g;
    let m;
    while ((m = re.exec(html))) {
      if (/<[a-zA-Z/]/.test(m[1])) {
        fail++;
        console.log(`FAIL  ${key} ${where}: 수식 안에 HTML 태그 → \\(${m[1].slice(0, 50)}\\)`);
      }
    }
  };
  P[key].trace().steps.forEach((s, i) => {
    check(`단계 ${i} desc`, s.desc);
    Object.values(s.setLabel || {}).forEach(v => check(`단계 ${i} setLabel`, v));
  });
  P[key].nodes.forEach(n => check(`노드 ${n.id}`, n.label));
});

console.log(fail === 0 ? '\n모두 통과' : `\n실패 ${fail}건`);
process.exit(fail === 0 ? 0 : 1);
