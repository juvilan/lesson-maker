"""
test_pdf_renderer — pdf_renderer.py 핵심 함수 유닛 테스트

fpdf2 미설치 환경에서도 독립적으로 실행 가능한 테스트만 포함.
(SchoolPdfRenderer 인스턴스화는 한글 폰트가 필요하므로 제외)
"""

import sys
import os
import importlib.util
import pytest

# _shared/tools 를 경로에 추가
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# fpdf2 미설치 시 pdf_renderer 관련 테스트 전체 스킵
fpdf2_available = importlib.util.find_spec("fpdf") is not None
skip_if_no_fpdf2 = pytest.mark.skipif(
    not fpdf2_available,
    reason="fpdf2 미설치 — pip install fpdf2"
)


# ──────────────────────────────────────────────────────
# estimate_problem_height 테스트
# ──────────────────────────────────────────────────────

@skip_if_no_fpdf2
def test_estimate_problem_height_import():
    """estimate_problem_height 함수가 임포트 가능한지 확인."""
    from pdf_renderer import estimate_problem_height  # noqa: F401


@skip_if_no_fpdf2
def test_estimate_multichoice_height():
    """객관식: 기본 높이 + 선택지 수 × 단위 높이."""
    from pdf_renderer import (
        estimate_problem_height,
        HEIGHT_MULTICHOICE_BASE,
        HEIGHT_MULTICHOICE_PER_CHOICE,
    )
    problem = {"type": "객관식", "choices": ["①", "②", "③", "④", "⑤"]}
    expected = HEIGHT_MULTICHOICE_BASE + 5 * HEIGHT_MULTICHOICE_PER_CHOICE
    assert estimate_problem_height(problem) == expected


@skip_if_no_fpdf2
def test_estimate_short_answer_height():
    """단답형: 고정 높이."""
    from pdf_renderer import estimate_problem_height, HEIGHT_SHORT_ANSWER
    problem = {"type": "단답형"}
    assert estimate_problem_height(problem) == HEIGHT_SHORT_ANSWER


@skip_if_no_fpdf2
def test_estimate_essay_height():
    """서술형: 기본 높이 + 답안 박스 높이."""
    from pdf_renderer import (
        estimate_problem_height,
        HEIGHT_ESSAY_BASE,
        HEIGHT_ESSAY_ANSWER_BOX,
    )
    problem = {"type": "서술형"}
    assert estimate_problem_height(problem) == HEIGHT_ESSAY_BASE + HEIGHT_ESSAY_ANSWER_BOX


@skip_if_no_fpdf2
def test_estimate_default_to_essay():
    """타입 미지정 시 서술형으로 처리."""
    from pdf_renderer import (
        estimate_problem_height,
        HEIGHT_ESSAY_BASE,
        HEIGHT_ESSAY_ANSWER_BOX,
    )
    problem = {}
    assert estimate_problem_height(problem) == HEIGHT_ESSAY_BASE + HEIGHT_ESSAY_ANSWER_BOX


@skip_if_no_fpdf2
def test_estimate_calc_height():
    """계산형: 기본 높이 + 줄 수 × 단위 높이."""
    from pdf_renderer import (
        estimate_problem_height,
        HEIGHT_CALC_BASE,
        HEIGHT_CALC_PER_LINE,
        HEIGHT_CALC_ANSWER_LINES,
    )
    problem = {"type": "계산형"}
    expected = HEIGHT_CALC_BASE + HEIGHT_CALC_ANSWER_LINES * HEIGHT_CALC_PER_LINE
    assert estimate_problem_height(problem) == expected


# ──────────────────────────────────────────────────────
# load_template 테스트
# ──────────────────────────────────────────────────────

@skip_if_no_fpdf2
def test_load_template_returns_defaults_when_no_file():
    """경로가 없으면 기본 템플릿을 반환한다."""
    from pdf_renderer import load_template
    config = load_template("/nonexistent/path/template.json")
    assert "margins" in config
    assert "header_format" in config
    assert "student_info_fields" in config


@skip_if_no_fpdf2
def test_load_template_margins_structure():
    """기본 margins에 필수 키 4개가 있다."""
    from pdf_renderer import load_template
    config = load_template(None)
    margins = config["margins"]
    for key in ("top", "right", "bottom", "left"):
        assert key in margins, f"margins에 '{key}' 키 없음"


@skip_if_no_fpdf2
def test_load_template_custom_json(tmp_path):
    """유효한 JSON 파일이 있으면 기본값을 오버라이드한다."""
    import json
    from pdf_renderer import load_template

    custom = {"page_number_format": "[ {n} ]"}
    p = tmp_path / "template.json"
    p.write_text(json.dumps(custom), encoding="utf-8")

    config = load_template(str(p))
    assert config["page_number_format"] == "[ {n} ]"
    # 기본값은 유지
    assert "margins" in config


# ──────────────────────────────────────────────────────
# find_korean_font 테스트
# ──────────────────────────────────────────────────────

@skip_if_no_fpdf2
def test_find_korean_font_returns_string_or_none():
    """반환값이 str이거나 None이어야 한다."""
    from pdf_renderer import find_korean_font
    result = find_korean_font()
    assert result is None or isinstance(result, str)


@skip_if_no_fpdf2
def test_find_korean_font_path_exists_if_found():
    """폰트 경로가 반환되면 실제로 존재해야 한다."""
    import os
    from pdf_renderer import find_korean_font
    result = find_korean_font()
    if result is not None:
        assert os.path.exists(result), f"폰트 경로가 존재하지 않음: {result}"
