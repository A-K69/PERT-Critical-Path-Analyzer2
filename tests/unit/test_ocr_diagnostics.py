from pert_analyzer.benchmark.ocr_diagnostics import _inside, render_markdown
from pert_analyzer.core.models import BoundingBox, Point
from pert_analyzer.cv.ocr_models import OCRTextRegion


def _region(text: str, x: float, y: float) -> OCRTextRegion:
    return OCRTextRegion(
        text=text,
        bounding_box=BoundingBox(x=x, y=y, width=10, height=10),
        center=Point(x + 5, y + 5),
    )


def test_inside_uses_text_center_and_optional_padding():
    region = _region("A", 45, 45)
    assert _inside(region, [40, 40, 20, 20]) is True
    assert _inside(_region("B", 65, 65), [40, 40, 20, 20]) is False
    assert _inside(_region("C", 65, 65), [40, 40, 20, 20], padding=10) is True


def test_render_markdown_exposes_error_taxonomy():
    markdown = render_markdown([
        {
            "image": "sample.png",
            "diagram_type": "AON",
            "expected_items": 1,
            "ocr_regions": 3,
            "ocr_numeric_candidates": 1,
            "ambiguous_associations": 1,
            "unmatched_regions": 0,
            "id_exact_matches": 1,
            "duration_exact_matches": 0,
            "association_exact_matches": 1,
            "item_error_counts": {"recognition_or_semantic_error": 1},
        }
    ])
    assert "recognition_or_semantic_error" in markdown
    assert "sample.png" in markdown
