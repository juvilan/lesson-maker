"""
test_rename_output — rename_output.py 핵심 함수 유닛 테스트

실제 파일 시스템 변경 없이 dry_run=True 로직과 매핑 테이블을 검증한다.
"""

import sys
import os
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


# ──────────────────────────────────────────────────────
# 매핑 테이블 구조 테스트
# ──────────────────────────────────────────────────────

def test_slides_rename_mapping_is_dict():
    """SLIDES_RENAME이 dict 타입이다."""
    from rename_output import SLIDES_RENAME
    assert isinstance(SLIDES_RENAME, dict)


def test_slides_rename_values_have_prefix():
    """SLIDES_RENAME의 모든 대상 파일명은 '슬라이드_' 또는 '대본_'으로 시작한다."""
    from rename_output import SLIDES_RENAME
    for dst in SLIDES_RENAME.values():
        assert dst.startswith("슬라이드_") or dst.startswith("대본_"), \
            f"접두사 누락: {dst}"


def test_slides_rename_no_duplicate_destinations():
    """SLIDES_RENAME의 대상 파일명에 중복이 없다."""
    from rename_output import SLIDES_RENAME
    dsts = list(SLIDES_RENAME.values())
    assert len(dsts) == len(set(dsts)), "대상 파일명에 중복 있음"


def test_root_to_worksheet_values_have_prefix():
    """ROOT_TO_WORKSHEET의 모든 대상 파일명은 '학습지_'로 시작한다."""
    from rename_output import ROOT_TO_WORKSHEET
    for dst in ROOT_TO_WORKSHEET.values():
        assert dst.startswith("학습지_"), f"학습지_ 접두사 누락: {dst}"


def test_exam_rename_values_have_prefix():
    """EXAM_RENAME의 모든 대상 파일명은 '종합문제_'로 시작한다."""
    from rename_output import EXAM_RENAME
    for dst in EXAM_RENAME.values():
        assert dst.startswith("종합문제_"), f"종합문제_ 접두사 누락: {dst}"


# ──────────────────────────────────────────────────────
# do_rename / do_move 함수 테스트 (임시 파일 사용)
# ──────────────────────────────────────────────────────

def test_do_rename_skips_missing_file(capsys):
    """소스 파일이 없으면 SKIP을 출력하고 counters['skip']을 증가시킨다."""
    from rename_output import do_rename
    counters = {"rename": 0, "skip": 0, "move": 0}
    src = Path("/nonexistent/source.html")
    dst = Path("/nonexistent/dest.html")
    do_rename(src, dst, dry_run=True, counters=counters)
    assert counters["skip"] == 1
    assert counters["rename"] == 0


def test_do_rename_dry_run_does_not_move(tmp_path):
    """dry_run=True 이면 실제 파일 이동 없이 counters['rename']만 증가한다."""
    from rename_output import do_rename
    src = tmp_path / "old.html"
    dst = tmp_path / "new.html"
    src.write_text("<html/>")

    counters = {"rename": 0, "skip": 0, "move": 0}
    do_rename(src, dst, dry_run=True, counters=counters)

    assert src.exists(), "dry_run인데 원본 파일이 삭제됨"
    assert not dst.exists(), "dry_run인데 대상 파일이 생성됨"
    assert counters["rename"] == 1


def test_do_rename_actual(tmp_path):
    """dry_run=False 이면 파일이 실제로 이름 변경된다."""
    from rename_output import do_rename
    src = tmp_path / "old.html"
    dst = tmp_path / "new.html"
    src.write_text("<html/>")

    counters = {"rename": 0, "skip": 0, "move": 0}
    do_rename(src, dst, dry_run=False, counters=counters)

    assert not src.exists(), "원본 파일이 남아 있음"
    assert dst.exists(), "대상 파일이 생성되지 않음"
    assert counters["rename"] == 1


def test_do_move_skips_missing_file():
    """소스 파일이 없으면 skip 카운터를 증가시킨다."""
    from rename_output import do_move
    counters = {"rename": 0, "skip": 0, "move": 0}
    src = Path("/nonexistent/slides/file.html")
    dst = Path("/nonexistent/_archive/file.html")
    do_move(src, dst, dry_run=True, counters=counters)
    assert counters["skip"] == 1


def test_ensure_dir_dry_run_does_not_create(tmp_path):
    """dry_run=True 이면 디렉토리를 생성하지 않는다."""
    from rename_output import ensure_dir
    target = tmp_path / "new_subdir"
    ensure_dir(target, dry_run=True)
    assert not target.exists(), "dry_run인데 디렉토리가 생성됨"


def test_ensure_dir_actual_creates(tmp_path):
    """dry_run=False 이면 디렉토리를 실제로 생성한다."""
    from rename_output import ensure_dir
    target = tmp_path / "new_subdir"
    ensure_dir(target, dry_run=False)
    assert target.exists(), "디렉토리가 생성되지 않음"
