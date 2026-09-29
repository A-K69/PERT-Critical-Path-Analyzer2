from pert_analyzer.core.models import Point
from pert_analyzer.cv.models import DetectedLineSegment
from pert_analyzer.benchmark.aoa_diagnostics import (
    _intervening,
    _route_segment_support,
)


def _segment(x1, y1, x2, y2):
    return DetectedLineSegment(
        start=Point(x1, y1),
        end=Point(x2, y2),
        length=((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5,
    )


def test_route_support_measures_fragmented_collinear_segments():
    source = ("A", 100.0, 150.0, 30.0)
    target = ("B", 300.0, 150.0, 30.0)
    segments = [_segment(130, 150, 180, 150), _segment(181, 150, 270, 150)]
    support = _route_segment_support(source, target, segments)
    assert support["supporting_segments"] == 2
    assert support["coverage"] > 0.9
    assert support["angular_consistency"] == 1.0


def test_route_support_penalizes_diagonal_angle_mismatch():
    source = ("A", 100.0, 100.0, 25.0)
    target = ("B", 300.0, 300.0, 25.0)
    segments = [_segment(120, 280, 280, 120), _segment(150, 250, 250, 150)]
    support = _route_segment_support(source, target, segments)
    assert support["supporting_segments"] == 0
    assert support["angular_consistency"] == 0.0


def test_intervening_event_is_detected():
    circles = [
        ("A", 100.0, 150.0, 30.0),
        ("B", 200.0, 150.0, 30.0),
        ("C", 300.0, 150.0, 30.0),
    ]
    assert _intervening(circles[0], circles[2], circles) == ["B"]
    assert _intervening(circles[0], circles[1], circles) == []
