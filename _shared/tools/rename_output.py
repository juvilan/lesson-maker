"""
rename_output.py — ai-math output/ 폴더 파일 네이밍 규칙 일괄 적용 도구

사용법:
  python rename_output.py --subject ai-math --dry-run   # 변경 내용 미리보기
  python rename_output.py --subject ai-math              # 실제 실행
"""

import argparse
import shutil
from pathlib import Path

# ------------------------------------------------------------------
# 경로 설정
# ------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]  # lesson-maker/

# ------------------------------------------------------------------
# 매핑 테이블
# ------------------------------------------------------------------

# slides/ 내에서 이름만 변경 (접두사 추가)
SLIDES_RENAME = {
    "I-01_인공지능의역사.html":          "슬라이드_I-01_인공지능의역사.html",
    "I-02_인공지능과수학.html":          "슬라이드_I-02_인공지능과수학.html",
    "II-1-01_텍스트자료의표현.html":     "슬라이드_II-1-01_텍스트자료의표현.html",
    "II-1-02_텍스트자료의처리.html":     "슬라이드_II-1-02_텍스트자료의처리.html",
    "II-1-03_텍스트자료의시각화.html":   "슬라이드_II-1-03_텍스트자료의시각화.html",
    "II-2-01_이미지자료의표현.html":     "슬라이드_II-2-01_이미지자료의표현.html",
    "II-2-02_이미지자료의처리.html":     "슬라이드_II-2-02_이미지자료의처리.html",
    "III-1-01_텍스트분류_감성분석.html": "슬라이드_III-1-01_텍스트분류_감성분석.html",
    "III-1-02_이미지분류.html":          "슬라이드_III-1-02_이미지분류.html",
    "III-1-03_유사도분석.html":          "슬라이드_III-1-03_유사도분석.html",
    "III-2-01_자료분석과예측.html":      "슬라이드_III-2-01_자료분석과예측.html",
    "III-2-02_경향성과예측.html":        "슬라이드_III-2-02_경향성과예측.html",
    "III-1-01_텍스트분류_대본.html":     "대본_III-1-01_텍스트분류.html",
    "III-1-02_이미지분류_대본.html":     "대본_III-1-02_이미지분류.html",
}

# slides/ → _archive/ 이동 (원본 이름 유지)
SLIDES_TO_ARCHIVE = [
    "matrix_lr_examples_slides.html",
    "matrix_transform_script.json",
    "matrix_transform_slides.html",
    "matrix_viz.html",
    "matrix_why_slides.html",
]

# output/ 루트 → worksheet/ 이동 + 리네이밍
ROOT_TO_WORKSHEET = {
    "II-2-01_이미지자료의표현_학습지.html":  "학습지_II-2-01_이미지자료의표현.html",
    "II-2-02_이미지자료의처리_학습지.html":  "학습지_II-2-02_이미지자료의처리.html",
    "III-1-02_이미지분류_학습지.html":        "학습지_III-1-02_이미지분류.html",
    "III-1-03_유사도분석_학습지.html":         "학습지_III-1-03_유사도분석.html",
    "III-2-01_자료분석과예측_학습지.html":    "학습지_III-2-01_자료분석과예측.html",
    "worksheet_20260317_152844.html":          "학습지_III-1-01_감성분석.html",
    "worksheet_20260317_160047.html":          "학습지_III-2-02_경향성과예측.html",
}

# output/ 루트 → _archive/ 이동
ROOT_TO_ARCHIVE = [
    "ai_math_perceptron.html",
    "ai_math_perceptron_v2.html",
    "demo_ai_math_perceptron.html",
]

# exam/ 내 리네이밍
EXAM_RENAME = {
    "대단원I_종합문제.html":  "종합문제_대단원I_인공지능과수학.html",
    "대단원II_종합문제.html": "종합문제_대단원II_자료의표현.html",
}

# 수행평가/ 내 리네이밍
PERFORMANCE_RENAME = {
    "수행평가1_AI발전의논리적흐름.html":         "수행평가_1_AI발전의논리적흐름.html",
    "수행평가1_AI발전의논리적흐름_모범답안.html": "수행평가_1_AI발전의논리적흐름_모범답안.html",
    "수행평가1_안내지.html":                       "수행평가_1_안내지.html",
    "수행평가2-1_텍스트벡터화.html":               "수행평가_2-1_텍스트벡터화.html",
    "수행평가2-2_이미지행렬화.html":               "수행평가_2-2_이미지행렬화.html",
    "모범답안_텍스트벡터화.html":                   "수행평가_2-1_텍스트벡터화_모범답안.html",
    "연습_텍스트벡터화.html":                       "수행평가연습_2-1_텍스트벡터화.html",
}

# ------------------------------------------------------------------
# 지원 과목
# ------------------------------------------------------------------
SUPPORTED_SUBJECTS = {"ai-math"}


# ------------------------------------------------------------------
# 핵심 함수
# ------------------------------------------------------------------

def ensure_dir(path: Path, dry_run: bool) -> None:
    """디렉토리가 없으면 생성(또는 dry-run 안내)."""
    if not path.exists():
        if dry_run:
            print(f"  CREATE_DIR  {path}")
        else:
            path.mkdir(parents=True, exist_ok=True)
            print(f"  CREATE_DIR  {path}")


def do_rename(src: Path, dst: Path, dry_run: bool, counters: dict) -> None:
    """같은 디렉토리 내 이름 변경."""
    if not src.exists():
        print(f"  SKIP  {src.name}  (없음)")
        counters["skip"] += 1
        return
    label = "RENAME"
    print(f"  {label}  {src.name} → {dst.name}")
    if not dry_run:
        src.rename(dst)
    counters["rename"] += 1


def do_move(src: Path, dst: Path, dry_run: bool, counters: dict) -> None:
    """파일을 다른 폴더로 이동(이름 변경 포함)."""
    if not src.exists():
        print(f"  SKIP  {src.name}  (없음)")
        counters["skip"] += 1
        return
    rel_src = src.relative_to(src.parent.parent)  # output/ 기준 상대경로
    rel_dst = dst.relative_to(dst.parent.parent)
    print(f"  MOVE  {rel_src} → {rel_dst}")
    if not dry_run:
        shutil.move(str(src), str(dst))
    counters["move"] += 1


# ------------------------------------------------------------------
# 섹션별 처리 함수
# ------------------------------------------------------------------

def process_slides_rename(slides_dir: Path, archive_dir: Path, dry_run: bool, counters: dict) -> None:
    prefix = "[DRY-RUN] " if dry_run else ""
    print(f"\n{prefix}slides/ 리네이밍:")
    for old_name, new_name in SLIDES_RENAME.items():
        src = slides_dir / old_name
        dst = slides_dir / new_name
        do_rename(src, dst, dry_run, counters)

    print(f"\n{prefix}slides/ → _archive/ 이동:")
    ensure_dir(archive_dir, dry_run)
    for name in SLIDES_TO_ARCHIVE:
        src = slides_dir / name
        dst = archive_dir / name
        do_move(src, dst, dry_run, counters)


def process_root_files(output_dir: Path, worksheet_dir: Path, archive_dir: Path, dry_run: bool, counters: dict) -> None:
    prefix = "[DRY-RUN] " if dry_run else ""
    print(f"\n{prefix}output/ 루트 → worksheet/ 이동:")
    ensure_dir(worksheet_dir, dry_run)
    for old_name, new_name in ROOT_TO_WORKSHEET.items():
        src = output_dir / old_name
        dst = worksheet_dir / new_name
        do_move(src, dst, dry_run, counters)

    print(f"\n{prefix}output/ 루트 → _archive/ 이동:")
    ensure_dir(archive_dir, dry_run)
    for name in ROOT_TO_ARCHIVE:
        src = output_dir / name
        dst = archive_dir / name
        do_move(src, dst, dry_run, counters)


def process_exam_rename(exam_dir: Path, dry_run: bool, counters: dict) -> None:
    prefix = "[DRY-RUN] " if dry_run else ""
    print(f"\n{prefix}exam/ 리네이밍:")
    for old_name, new_name in EXAM_RENAME.items():
        src = exam_dir / old_name
        dst = exam_dir / new_name
        do_rename(src, dst, dry_run, counters)


def process_performance_rename(perf_dir: Path, dry_run: bool, counters: dict) -> None:
    prefix = "[DRY-RUN] " if dry_run else ""
    print(f"\n{prefix}수행평가/ 리네이밍:")
    for old_name, new_name in PERFORMANCE_RENAME.items():
        src = perf_dir / old_name
        dst = perf_dir / new_name
        do_rename(src, dst, dry_run, counters)


# ------------------------------------------------------------------
# 메인
# ------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="output/ 폴더 파일을 새 네이밍 규칙으로 이동/리네이밍합니다."
    )
    parser.add_argument(
        "--subject",
        required=True,
        choices=sorted(SUPPORTED_SUBJECTS),
        help="처리할 과목 (현재: ai-math)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="실제 변경 없이 무엇을 할지 출력합니다",
    )
    args = parser.parse_args()

    subject_dir = PROJECT_ROOT / args.subject
    output_dir  = subject_dir / "output"

    if not output_dir.exists():
        raise SystemExit(f"오류: output 폴더를 찾을 수 없습니다 — {output_dir}")

    slides_dir    = output_dir / "slides"
    exam_dir      = output_dir / "exam"
    worksheet_dir = output_dir / "worksheet"
    perf_dir      = output_dir / "수행평가"
    archive_dir   = output_dir / "_archive"

    counters: dict[str, int] = {"rename": 0, "move": 0, "skip": 0}

    mode_label = "dry-run" if args.dry_run else "실행"
    print(f"=== rename_output ({args.subject}, {mode_label}) ===")
    print(f"대상 경로: {output_dir}")

    process_slides_rename(slides_dir, archive_dir, args.dry_run, counters)
    process_root_files(output_dir, worksheet_dir, archive_dir, args.dry_run, counters)
    process_exam_rename(exam_dir, args.dry_run, counters)
    process_performance_rename(perf_dir, args.dry_run, counters)

    suffix = " (dry-run)" if args.dry_run else ""
    print(
        f"\n완료{suffix}: "
        f"이동 {counters['move']}개, "
        f"리네이밍 {counters['rename']}개, "
        f"없음(SKIP) {counters['skip']}개"
    )


if __name__ == "__main__":
    main()
