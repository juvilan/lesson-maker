// TeX 문자열 → MathJax SVG (경로 인라인, 폰트 독립). stdin: JSON 배열, stdout: JSON {tex: svg}
import { mathjax } from 'mathjax-full/js/mathjax.js';
import { TeX } from 'mathjax-full/js/input/tex.js';
import { SVG } from 'mathjax-full/js/output/svg.js';
import { liteAdaptor } from 'mathjax-full/js/adaptors/liteAdaptor.js';
import { RegisterHTMLHandler } from 'mathjax-full/js/handlers/html.js';
import { AllPackages } from 'mathjax-full/js/input/tex/AllPackages.js';
const adaptor = liteAdaptor(); RegisterHTMLHandler(adaptor);
const tex = new TeX({ packages: AllPackages });
const svg = new SVG({ fontCache: 'none' });
const html = mathjax.document('', { InputJax: tex, OutputJax: svg });
let input = ''; process.stdin.on('data', d => input += d);
process.stdin.on('end', () => {
  const list = JSON.parse(input); const out = {};
  for (const t of list) {
    const node = html.convert(t, { display: false });
    out[t] = adaptor.outerHTML(node);   // <mjx-container><svg ...>...</svg></mjx-container>
  }
  process.stdout.write(JSON.stringify(out));
});
