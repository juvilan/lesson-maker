"""교과서 PDF 텍스트를 쪽 단위로 뽑는다.

교사용 교과서라 정답과 지도 유의사항이 본문에 함께 들어 있다.
덱을 쓰기 전에 반드시 원문을 읽을 것 — 값을 추정하면 틀린다.

    powershell.exe -NoProfile -Command "$env:PYTHONIOENCODING='utf-8'; python tools/read_book.py '<pdf>' 4 6 --full"

Git Bash 에서 python3 는 이 PC 에서 실패한다. PowerShell 로 실행할 것.

인자
    <pdf>        교과서 경로 (ai-math/book/, ai-math-2022/book/)
    [시작] [끝]   PDF 쪽 번호 (교과서 인쇄 쪽번호와 다르다 — 먼저 훑어서 대응을 잡을 것)
    --full       줄바꿈을 살려 전문 출력. 없으면 쪽당 400자 미리보기
"""
import io
import sys

import pypdf


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return
    path = sys.argv[1]
    args = [a for a in sys.argv[2:] if not a.startswith("--")]
    lo = int(args[0]) if len(args) > 0 else 1
    hi = int(args[1]) if len(args) > 1 else 10 ** 6
    full = "--full" in sys.argv

    reader = pypdf.PdfReader(path)
    print("총 %d쪽" % len(reader.pages))
    for i, page in enumerate(reader.pages):
        n = i + 1
        if n < lo or n > hi:
            continue
        text = (page.extract_text() or "").replace("\r", "")
        if not full:
            text = " ".join(text.split())[:400]
        print("\n===== PDF %d쪽 =====" % n)
        print(text)


if __name__ == "__main__":
    main()
