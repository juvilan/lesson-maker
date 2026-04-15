"""
pdf_math_renderer — LaTeX 수식 → PNG 이미지 렌더링 유틸리티

fpdf2 기반 PDF 생성 시 인라인 수식 임베드에 사용.
matplotlib.mathtext 기반으로 분수/첨자/그리스문자를 지원한다.
"""

import tempfile
from typing import Optional

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False


def latex_to_png(formula: str, fontsize: int = 14, dpi: int = 200) -> Optional[str]:
    """
    LaTeX 수식을 PNG 임시 파일로 렌더링한다.
    matplotlib.mathtext 사용 — 분수/첨자/그리스문자 지원.
    실패 시 None 반환.
    """
    if not HAS_MATPLOTLIB:
        return None
    try:
        from matplotlib.figure import Figure
        from matplotlib.backends.backend_agg import FigureCanvasAgg

        # 수식 전용 Figure (배경 투명, 여백 최소)
        fig = Figure(facecolor="none")
        canvas = FigureCanvasAgg(fig)
        ax = fig.add_axes([0, 0, 1, 1], facecolor="none")
        ax.axis("off")

        txt = ax.text(
            0.01, 0.5, f"${formula}$",
            fontsize=fontsize, va="center", ha="left",
            color="black", transform=ax.transAxes,
        )
        # 렌더링 후 텍스트 실제 크기 측정
        canvas.draw()
        renderer = canvas.get_renderer()
        bbox = txt.get_window_extent(renderer=renderer)

        # 픽셀 → 인치 변환으로 Figure 크기 재조정
        fig_w = max(bbox.width / dpi + 0.1, 0.3)
        fig_h = max(bbox.height / dpi + 0.06, 0.2)
        fig.set_size_inches(fig_w, fig_h)

        tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
        fig.savefig(tmp.name, bbox_inches="tight", dpi=dpi,
                    transparent=True, pad_inches=0.02)
        plt.close("all")
        return tmp.name
    except Exception:
        return None


def strip_latex_delimiters(text: str) -> str:
    """$...$, $$...$$ 구분자를 제거한다."""
    text = text.strip()
    if text.startswith("$$") and text.endswith("$$"):
        return text[2:-2]
    if text.startswith("$") and text.endswith("$"):
        return text[1:-1]
    return text
