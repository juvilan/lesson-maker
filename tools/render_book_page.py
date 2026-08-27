"""교과서 PDF 지면을 PNG 이미지로 렌더링한다.

**행렬·격자·도표가 들어간 쪽은 텍스트 추출을 믿으면 안 된다.**
pypdf 는 행렬을 열 우선으로 뽑고, 그것 말고도 뒤섞이는 경우가 있다
(97쪽 S3·T3 가 서로 바뀐 채 나온 전례). 지면을 눈으로 봐야 한다.

Read 도구의 PDF 렌더링은 poppler(pdftoppm)를 요구하는데 이 PC 에는 없다.
그래서 pypdfium2 로 직접 뽑는다.

    powershell.exe -NoProfile -Command "python tools/render_book_page.py '<pdf>' 3 4"

그런 다음 Read 도구로 출력된 PNG 를 열면 지면이 보인다.

인자
    <pdf>       교과서 경로
    [시작] [끝]  PDF 쪽 번호 (교과서 인쇄 쪽번호와 다르다. tools/read_book.py 로 먼저 대응을 잡을 것)
    --scale N   배율 (기본 2.0 — 행렬 숫자가 작아 이보다 낮추면 읽기 어렵다)
    --out DIR   저장 폴더 (기본: 시스템 임시 폴더)
"""
import os
import sys
import tempfile

import pypdfium2 as pdfium


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return

    path = sys.argv[1]
    args = [a for a in sys.argv[2:] if not a.startswith("--")]
    lo = int(args[0]) if len(args) > 0 else 1
    hi = int(args[1]) if len(args) > 1 else lo

    scale = 2.0
    if "--scale" in sys.argv:
        scale = float(sys.argv[sys.argv.index("--scale") + 1])

    out_dir = tempfile.gettempdir()
    if "--out" in sys.argv:
        out_dir = sys.argv[sys.argv.index("--out") + 1]
    os.makedirs(out_dir, exist_ok=True)

    stem = os.path.splitext(os.path.basename(path))[0]
    pdf = pdfium.PdfDocument(path)
    n = len(pdf)
    print("총 %d쪽" % n)

    for num in range(lo, min(hi, n) + 1):
        page = pdf[num - 1]
        image = page.render(scale=scale).to_pil()
        dst = os.path.join(out_dir, "%s_p%02d.png" % (stem, num))
        image.save(dst)
        print("  %s  (%dx%d)" % (dst, image.width, image.height))


if __name__ == "__main__":
    main()
