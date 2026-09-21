/* ============================================================
   build-standalone.js
   덱의 로컬 CSS·JS를 본문에 인라인해 단일 HTML로 만든다.
   구글 드라이브처럼 상대경로 자산을 함께 둘 수 없는 곳에 올릴 때 사용.
   (reveal.js·MathJax는 CDN 그대로 — 저장소본과 동일)

   실행: node build-standalone.js <입력.html> <출력.html>
   ============================================================ */
const fs = require('fs');
const path = require('path');

const [, , inPath, outPath] = process.argv;
if (!inPath || !outPath) {
  console.error('사용법: node build-standalone.js <입력.html> <출력.html>');
  process.exit(1);
}

const baseDir = path.dirname(path.resolve(inPath));
let html = fs.readFileSync(inPath, 'utf8');
const inlined = [];

/* 로컬 <link rel="stylesheet" href="...">  →  <style> */
html = html.replace(
  /[ \t]*<link[^>]*rel="stylesheet"[^>]*href="(\.[^"]+)"[^>]*>\n?/g,
  (m, href) => {
    const file = path.resolve(baseDir, href);
    const css = fs.readFileSync(file, 'utf8');
    inlined.push(href);
    return `  <style>\n/* ===== ${path.basename(href)} ===== */\n${css}\n  </style>\n`;
  }
);

/* 로컬 <script src="...">  →  <script> */
html = html.replace(
  /[ \t]*<script src="(\.[^"]+)"><\/script>\n?/g,
  (m, src) => {
    const file = path.resolve(baseDir, src);
    const js = fs.readFileSync(file, 'utf8');
    inlined.push(src);
    // 본문에 </script>가 들어가면 파싱이 끊긴다
    const safe = js.replace(/<\/script>/gi, '<\\/script>');
    return `<script>\n/* ===== ${path.basename(src)} ===== */\n${safe}\n</script>\n`;
  }
);

/* @font-face의 로컬 폰트 경로 → CDN
   (저장소본은 _shared/fonts를 쓰지만 단일 파일에서는 상대경로가 깨진다.
    jsdelivr 파일이 _shared/fonts/PretendardVariable.woff2와 바이트 단위로 동일함을 확인했다.) */
const FONT_CDN = 'https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/' +
                 'packages/pretendard/dist/web/variable/woff2/PretendardVariable.woff2';
html = html.replace(/url\(['"]\.\.\/fonts\/PretendardVariable\.woff2['"]\)/g, `url('${FONT_CDN}')`);

/* 남은 로컬 참조가 있으면 실패로 본다 */
const leftover = [...html.matchAll(/(?:href|src)="(\.[^"]+)"/g)].map(m => m[1]);
if (leftover.length) {
  console.error('남은 로컬 참조:', leftover);
  process.exit(1);
}

fs.writeFileSync(outPath, html);
console.log(`인라인 ${inlined.length}개:`);
inlined.forEach(f => console.log('  ' + f));
console.log(`→ ${outPath} (${(fs.statSync(outPath).size / 1024).toFixed(0)} KB)`);
