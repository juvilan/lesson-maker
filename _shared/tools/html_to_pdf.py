#!/usr/bin/env python3
"""
HTML → A4 PDF 변환 스크립트 (Playwright Chromium)

사용법:
  python html_to_pdf.py <파일 또는 디렉토리> [옵션]

예시:
  python html_to_pdf.py ai-math/output/exam/종합문제_대단원I_인공지능과수학.html
  python html_to_pdf.py ai-math/output/worksheet/ --pattern "학습지_*.html"
  python html_to_pdf.py ai-math/output/exam/ --pattern "종합문제_*.html"
  python html_to_pdf.py ai-math/output/ --all
"""

import argparse
import asyncio
import sys
from pathlib import Path

try:
    from playwright.async_api import async_playwright
except ImportError:
    print("설치 필요: pip install playwright && playwright install chromium")
    sys.exit(1)


# ─── 변환 핵심 로직 ────────────────────────────────────────────────────────────

# A4 @page margin: 상 15mm, 하 20mm → 인쇄 가능 높이 = 297 - 15 - 20 = 262mm
_A4_PRINTABLE_MM = 262.0
_PX_PER_MM = 96.0 / 25.4  # 96dpi 기준


async def validate_page_breaks(page) -> list[str]:
    """
    각 .ws-page 요소가 A4 인쇄 영역(262mm)을 초과하는지 검사.
    @media print 로 전환하여 인쇄 모드 CSS 적용 후 측정.
    반환: 경고 메시지 목록 (비어 있으면 이상 없음)
    """
    await page.emulate_media(media="print")
    max_px = _A4_PRINTABLE_MM * _PX_PER_MM

    issues: list[str] = await page.evaluate(
        """(maxPx) => {
            const pxPerMm = 96 / 25.4;
            const pages = document.querySelectorAll('.ws-page');
            const results = [];
            pages.forEach((el, i) => {
                const h = el.scrollHeight;
                if (h > maxPx) {
                    const totalMm = Math.round(h / pxPerMm);
                    const overMm  = Math.round((h - maxPx) / pxPerMm);
                    results.push(
                        `ws-page #${i + 1}: ${totalMm}mm — 인쇄 영역(262mm) 초과 +${overMm}mm`
                    );
                }
            });
            return results;
        }""",
        max_px,
    )

    await page.emulate_media(media=None)
    return issues


async def convert_html_to_pdf(
    page,
    html_path: Path,
    output_path: Path,
) -> list[str]:
    """단일 HTML 파일을 A4 PDF로 변환. 반환: 페이지 넘침 경고 목록"""
    url = html_path.resolve().as_uri()
    await page.goto(url, wait_until="networkidle")

    # MathJax 렌더링 대기
    try:
        await page.wait_for_function(
            "typeof MathJax !== 'undefined' && MathJax.typesetPromise !== undefined",
            timeout=10000,
        )
        await page.evaluate("MathJax.typesetPromise()")
        await page.wait_for_timeout(800)
    except Exception:
        # MathJax 없는 페이지는 그냥 진행
        print(f"[경고] MathJax 렌더링 대기 실패: {html_path.name}", file=sys.stderr)

    # 페이지 분할 사전 검증 (PDF 생성 전)
    issues = await validate_page_breaks(page)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    await page.pdf(
        path=str(output_path),
        format="A4",
        prefer_css_page_size=True,
        print_background=True,
    )

    return issues


async def run(args: argparse.Namespace) -> tuple[int, int]:
    """대상 파일 목록을 수집하고 변환 수행. 반환: (변환 수, 오류 수)"""
    target = Path(args.target).resolve()

    # 대상 파일 목록 수집
    html_files: list[Path] = []

    if target.is_file():
        if target.suffix.lower() != ".html":
            print(f"오류: HTML 파일이 아닙니다: {target}", file=sys.stderr)
            sys.exit(1)
        html_files = [target]
    elif target.is_dir():
        if args.all:
            html_files = sorted(target.rglob("*.html"))
        else:
            pattern = getattr(args, "pattern", "*.html") or "*.html"
            html_files = sorted(target.glob(pattern))
    else:
        print(f"오류: 경로가 존재하지 않습니다: {target}", file=sys.stderr)
        sys.exit(1)

    if not html_files:
        print("변환할 HTML 파일이 없습니다.")
        return 0, 0

    # --dry-run: 목록만 출력
    if args.dry_run:
        print(f"[dry-run] 변환 대상 {len(html_files)}개:")
        for f in html_files:
            pdf_path = _resolve_output(f, args.output_dir)
            print(f"  {f} → {pdf_path}")
        return len(html_files), 0

    # 실제 변환
    converted = 0
    errors = 0
    page_break_issues = 0

    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=True)
        page = await browser.new_page()

        for html_file in html_files:
            pdf_path = _resolve_output(html_file, args.output_dir)
            try:
                issues = await convert_html_to_pdf(page, html_file, pdf_path)
                if issues:
                    page_break_issues += len(issues)
                    for msg in issues:
                        print(f"  [⚠ 페이지 넘침] {msg}", file=sys.stderr)
                print(f"[변환] {html_file.name} → {pdf_path}")
                converted += 1
            except Exception as exc:
                print(f"[오류] {html_file.name}: {exc}", file=sys.stderr)
                errors += 1

        await browser.close()

    if args.strict and page_break_issues > 0:
        print(
            f"[오류] --strict 모드: 페이지 넘침 {page_break_issues}건 발견",
            file=sys.stderr,
        )
        sys.exit(1)

    return converted, errors


def _resolve_output(html_file: Path, output_dir: str | None) -> Path:
    """PDF 출력 경로 결정"""
    if output_dir:
        dst_dir = Path(output_dir).resolve()
        return dst_dir / html_file.with_suffix(".pdf").name
    return html_file.with_suffix(".pdf")


# ─── 진입점 ───────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="HTML 파일을 Playwright Chromium으로 A4 PDF로 변환합니다."
    )
    parser.add_argument(
        "target",
        help="변환할 HTML 파일 경로 또는 디렉토리 경로",
    )
    parser.add_argument(
        "--pattern",
        default="*.html",
        help="디렉토리 지정 시 glob 패턴 (기본: *.html)",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="디렉토리 내 모든 .html 파일 재귀 검색",
    )
    parser.add_argument(
        "--output-dir",
        dest="output_dir",
        default=None,
        help="PDF 저장 디렉토리 (기본: HTML과 같은 폴더)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="변환 없이 대상 파일 목록만 출력",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="페이지 넘침 감지 시 exit 1 반환 (CI/자동화 환경용)",
    )

    args = parser.parse_args()
    converted, errors = asyncio.run(run(args))

    suffix = " (dry-run)" if args.dry_run else ""
    print(f"\n완료{suffix}: 변환 {converted}개, 오류 {errors}개")

    if errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
