from types import SimpleNamespace

from pert_analyzer.gui.reviews.confidence import (
    ConfidenceBand,
    confidence_band,
    confidence_reason,
    normalize_confidence,
)


def test_normalize_confidence_clamps_and_handles_invalid_values() -> None:
    assert normalize_confidence(1.4) == 1.0
    assert normalize_confidence(-0.2) == 0.0
    assert normalize_confidence("not-a-number") == 0.0
    assert normalize_confidence(float("nan")) == 0.0


def test_confidence_bands_use_shared_thresholds() -> None:
    assert confidence_band(0.9) is ConfidenceBand.HIGH
    assert confidence_band(0.5) is ConfidenceBand.MEDIUM
    assert confidence_band(0.2) is ConfidenceBand.LOW


def test_confidence_reason_preserves_explicit_reason() -> None:
    item = SimpleNamespace(confidence=0.2, reason="Arrowhead is ambiguous")
    assert confidence_reason(item) == "Arrowhead is ambiguous"


def test_confidence_reason_is_actionable_without_explicit_reason() -> None:
    item = SimpleNamespace(confidence=0.2, reason="")
    assert "highlighted image evidence" in confidence_reason(item)

