"""Shared confidence policy for the human review experience."""

from __future__ import annotations

from enum import Enum


class ConfidenceBand(str, Enum):
    """User-facing confidence bands derived from a normalized score."""

    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


HIGH_THRESHOLD = 0.75
MEDIUM_THRESHOLD = 0.45


def normalize_confidence(value: object) -> float:
    """Return a safe confidence score in the inclusive range [0, 1]."""
    try:
        score = float(value or 0.0)
    except (TypeError, ValueError):
        return 0.0
    if score != score:  # NaN
        return 0.0
    return max(0.0, min(1.0, score))


def confidence_band(value: object) -> ConfidenceBand:
    """Classify a score using thresholds shared by list and detail views."""
    score = normalize_confidence(value)
    if score >= HIGH_THRESHOLD:
        return ConfidenceBand.HIGH
    if score >= MEDIUM_THRESHOLD:
        return ConfidenceBand.MEDIUM
    return ConfidenceBand.LOW


def confidence_reason(item: object) -> str:
    """Explain why an item may need attention, without inventing evidence."""
    explicit = str(getattr(item, "reason", "") or "").strip()
    if explicit:
        return explicit
    band = confidence_band(getattr(item, "confidence", 0.0))
    if band is ConfidenceBand.LOW:
        return "Low-confidence detection; verify the value against the highlighted image evidence."
    if band is ConfidenceBand.MEDIUM:
        return "Moderate-confidence detection; compare the alternatives before accepting."
    return "High-confidence detection; accept only if the highlighted evidence agrees."


__all__ = [
    "ConfidenceBand",
    "HIGH_THRESHOLD",
    "MEDIUM_THRESHOLD",
    "confidence_band",
    "confidence_reason",
    "normalize_confidence",
]

