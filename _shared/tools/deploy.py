#!/usr/bin/env python3
"""
lesson-maker 자료 → Google Drive 자동 배포 스크립트

사용법:
  python3 lesson-maker/_shared/tools/deploy.py ai-math slides
  python3 lesson-maker/_shared/tools/deploy.py ai-math 수행평가
  python3 lesson-maker/_shared/tools/deploy.py ai-math exam
  python3 lesson-maker/_shared/tools/deploy.py ai-math worksheet
  python3 lesson-maker/_shared/tools/deploy.py ai-math all
  python3 lesson-maker/_shared/tools/deploy.py geometry slides
  python3 lesson-maker/_shared/tools/deploy.py ai-math all --dry-run

수행평가 자동 감지:
  output/ 아래 '수행평가'로 시작하는 폴더를 모두 자동 스캔합니다.
  - output/수행평가/           → 드라이브: 2026_수행평가/ (flat)
  - output/수행평가3_경향성과예측/ → 드라이브: 2026_수행평가/수행평가3_경향성과예측/
"""

import argparse
import shutil
import sys
from pathlib import Path

# ─── 경로 설정 ─────────────────────────────────────────────────────────────────

PROJECT_ROOT = Path(__file__).resolve().parents[2]  # lesson-maker/
DRIVE_ROOT = (
    Path.home()
    / "내 드라이브(juvilan0429@gmail.com)"
    / "001_영일고"
    / "1_학교업무"
)
YEAR = "2026"

# ─── 매핑 테이블 ───────────────────────────────────────────────────────────────

SUBJECT_MAP: dict[str, str] = {
    "ai-math": "인공지능수학",
    "ai-math-2022": "인공지능수학(2022)",
    "geometry": "기하",
}

# category → (소스 상대경로, 드라이브 대상 경로)
# slides의 대상은 subject_kr이 포함되므로 런타임에 포맷 처리
CATEGORY_CONFIG: dict[str, tuple[str, str]] = {
    "slides":    ("output/slides",   "02_수업/1_정규수업/{year}/{subject_kr}/슬라이드"),
    "수행평가":   ("output/수행평가",  "03_평가/1_수행평가/{year}_수행평가"),
    "exam":      ("output/exam",     "03_평가/0_정기고사/{year}_정기고사"),
    "worksheet": ("output/worksheet",  "02_수업/1_정규수업/{year}/{subject_kr}/학습지"),
}

CATEGORY_GLOBS: dict[str, list[str]] = {
    "slides":    ["*.html"],
    "수행평가":   ["*.html", "*.pdf", "*.jpg", "*.png"],
    "exam":      ["*.html", "*.pdf"],
    "worksheet": ["*.html", "*.pdf"],
}

EXCLUDE_NAMES: set[str] = {".DS_Store"}
EXCLUDE_DIRS: set[str] = {".playwright-mcp", ".claude", "__pycache__"}

# ─── 헬퍼 함수 ────────────────────────────────────────────────────────────────

def should_exclude(path: Path) -> bool:
    """숨김 폴더, DS_Store, json 중간파일 등 제외 여부 판단"""
    if path.name in EXCLUDE_NAMES:
        return True
    for part in path.parts:
        if part in EXCLUDE_DIRS:
            return True
    return False


def collect_files(src_dir: Path, globs: list[str]) -> list[Path]:
    """소스 폴더에서 glob 패턴에 맞는 파일 수집 (재귀, 제외 필터 적용)"""
    result: list[Path] = []
    for pattern in globs:
        for file in src_dir.rglob(pattern):
            if file.is_file() and not should_exclude(file):
                result.append(file)
    # 중복 제거 (여러 glob이 같은 파일을 잡을 경우)
    seen: set[Path] = set()
    unique: list[Path] = []
    for f in result:
        if f not in seen:
            seen.add(f)
            unique.append(f)
    return unique


def resolve_dst_dir(category: str, subject_kr: str) -> Path:
    """대상 Google Drive 경로 결정"""
    _, dst_template = CATEGORY_CONFIG[category]
    dst_rel = dst_template.format(year=YEAR, subject_kr=subject_kr)
    return DRIVE_ROOT / dst_rel


def deploy_category(
    subject: str,
    subject_kr: str,
    category: str,
    dry_run: bool,
) -> tuple[int, int, int]:
    """
    단일 카테고리 배포 수행.
    반환: (copied, skipped, errors)
    """
    src_rel, _ = CATEGORY_CONFIG[category]
    src_dir = PROJECT_ROOT / subject / src_rel
    dst_dir = resolve_dst_dir(category, subject_kr)
    globs = CATEGORY_GLOBS[category]

    print(f"\n[{category}]")
    print(f"  src : {src_dir}")
    print(f"  dst : {dst_dir}")

    if not src_dir.exists():
        print(f"  ⚠️  소스 폴더 없음, 건너뜀")
        return 0, 0, 0

    files = collect_files(src_dir, globs)
    if not files:
        print(f"  ℹ️  복사할 파일 없음")
        return 0, 0, 0

    copied = skipped = errors = 0

    for src_file in sorted(files):
        # 소스 폴더 기준 상대경로 유지
        rel = src_file.relative_to(src_dir)
        dst_file = dst_dir / rel

        try:
            # 동일 파일 비교 (mtime + size)
            if dst_file.exists():
                src_stat = src_file.stat()
                dst_stat = dst_file.stat()
                if (
                    abs(src_stat.st_mtime - dst_stat.st_mtime) < 1.0
                    and src_stat.st_size == dst_stat.st_size
                ):
                    print(f"  ⏭  SKIP  {rel}")
                    skipped += 1
                    continue
                else:
                    print(f"  🔄  OVERWRITE  {rel}")
            else:
                print(f"  ✅  COPY  {rel}")

            if not dry_run:
                dst_file.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src_file, dst_file)
            copied += 1

        except Exception as exc:
            print(f"  ❌  ERROR  {rel}: {exc}", file=sys.stderr)
            errors += 1

    return copied, skipped, errors


def deploy_수행평가_auto(
    subject: str,
    dry_run: bool,
) -> tuple[int, int, int]:
    """
    output/ 아래 '수행평가'로 시작하는 모든 폴더를 자동 감지하여 배포.

    - output/수행평가/           → 드라이브: {year}_수행평가/ (flat)
    - output/수행평가3_xxx/      → 드라이브: {year}_수행평가/수행평가3_xxx/
    """
    output_dir = PROJECT_ROOT / subject / "output"
    dst_root = DRIVE_ROOT / f"03_평가/1_수행평가/{YEAR}_수행평가"
    globs = CATEGORY_GLOBS["수행평가"]

    total_c = total_s = total_e = 0

    if not output_dir.exists():
        print(f"  ⚠️  output 폴더 없음: {output_dir}")
        return 0, 0, 0

    # '수행평가'로 시작하는 하위 폴더 전체 스캔
    subdirs = sorted(
        d for d in output_dir.iterdir()
        if d.is_dir() and d.name.startswith("수행평가")
    )

    if not subdirs:
        print("  ℹ️  수행평가* 폴더 없음")
        return 0, 0, 0

    for src_dir in subdirs:
        # 기존 'output/수행평가/' → 드라이브 루트에 flat 복사
        # 그 외 'output/수행평가N_xxx/' → 드라이브에 하위 폴더로 복사
        if src_dir.name == "수행평가":
            dst_dir = dst_root
        else:
            dst_dir = dst_root / src_dir.name

        print(f"\n  [수행평가/{src_dir.name}]")
        print(f"    src : {src_dir}")
        print(f"    dst : {dst_dir}")

        files = collect_files(src_dir, globs)
        if not files:
            print(f"    ℹ️  복사할 파일 없음")
            continue

        for src_file in sorted(files):
            rel = src_file.relative_to(src_dir)
            dst_file = dst_dir / rel

            try:
                if dst_file.exists():
                    src_stat = src_file.stat()
                    dst_stat = dst_file.stat()
                    if (
                        abs(src_stat.st_mtime - dst_stat.st_mtime) < 1.0
                        and src_stat.st_size == dst_stat.st_size
                    ):
                        print(f"    ⏭  SKIP  {rel}")
                        total_s += 1
                        continue
                    else:
                        print(f"    🔄  OVERWRITE  {rel}")
                else:
                    print(f"    ✅  COPY  {rel}")

                if not dry_run:
                    dst_file.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(src_file, dst_file)
                total_c += 1

            except Exception as exc:
                print(f"    ❌  ERROR  {rel}: {exc}", file=sys.stderr)
                total_e += 1

    return total_c, total_s, total_e


def run_deploy(subject: str, category: str, dry_run: bool) -> None:
    if subject not in SUBJECT_MAP:
        print(
            f"오류: 알 수 없는 subject '{subject}'. "
            f"지원: {', '.join(SUBJECT_MAP.keys())}",
            file=sys.stderr,
        )
        sys.exit(1)

    subject_kr = SUBJECT_MAP[subject]

    if dry_run:
        print("=== DRY-RUN 모드 (실제 파일 복사 없음) ===")

    categories = list(CATEGORY_CONFIG.keys()) if category == "all" else [category]

    if category != "all" and category not in CATEGORY_CONFIG:
        print(
            f"오류: 알 수 없는 category '{category}'. "
            f"지원: {', '.join(CATEGORY_CONFIG.keys())}, all",
            file=sys.stderr,
        )
        sys.exit(1)

    total_copied = total_skipped = total_errors = 0

    for cat in categories:
        if cat == "수행평가":
            # 수행평가* 폴더 자동 감지 모드
            print(f"\n[수행평가] (output/ 내 수행평가* 폴더 자동 스캔)")
            c, s, e = deploy_수행평가_auto(subject, dry_run)
        else:
            c, s, e = deploy_category(subject, subject_kr, cat, dry_run)
        total_copied += c
        total_skipped += s
        total_errors += e

    print("\n─" * 40)
    suffix = " (dry-run)" if dry_run else ""
    print(
        f"완료{suffix}: "
        f"복사 {total_copied}개, 스킵 {total_skipped}개, 오류 {total_errors}개"
    )

    if total_errors:
        sys.exit(1)


# ─── 진입점 ───────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="lesson-maker 자료를 Google Drive로 배포합니다."
    )
    parser.add_argument(
        "subject",
        choices=list(SUBJECT_MAP.keys()),
        help=f"과목 키 ({', '.join(SUBJECT_MAP.keys())})",
    )
    parser.add_argument(
        "category",
        help=(
            "배포 카테고리: "
            f"{', '.join(CATEGORY_CONFIG.keys())}, all"
        ),
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="실제 복사 없이 어떤 파일이 복사될지 미리 확인",
    )
    args = parser.parse_args()
    run_deploy(args.subject, args.category, args.dry_run)


if __name__ == "__main__":
    main()
