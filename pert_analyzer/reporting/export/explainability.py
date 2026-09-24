"""Human-readable explanation of an authoritative project report."""

from __future__ import annotations

from typing import Any, List


def interpretation_lines(report: Any) -> List[str]:
    """Return deterministic provenance and interpretation lines.

    This function only reads report fields. It never recomputes CPM, PERT,
    validation, or review values.
    """
    metadata = getattr(report, "metadata", None)
    summary = getattr(report, "summary", None)
    cpm = getattr(report, "cpm", None)
    validation = getattr(report, "validation", None)
    review = getattr(report, "review", None)

    project_name = getattr(metadata, "project_name", "Untitled Project")
    source_image = getattr(metadata, "source_image", "") or "Not recorded"
    validation_status = getattr(validation, "status", "NOT_VALIDATED")
    review_status = getattr(review, "graph_validation_status", "NOT_VALIDATED")
    review_available = bool(getattr(review, "available", False))
    duration = getattr(summary, "project_duration", None)
    path_count = getattr(summary, "critical_path_count", None)
    cpm_valid = getattr(cpm, "is_valid", None)
    decision_count = len(getattr(review, "decisions", None) or [])

    lines = [
        f"Authority: reviewed graph and backend CPM result for {project_name}.",
        f"Source image: {source_image}.",
        f"Graph validation: {validation_status}; review status: {review_status}.",
        f"Human review record: {'available' if review_available else 'not available'}; "
        f"recorded decisions: {decision_count}.",
        f"CPM validity: {cpm_valid if cpm_valid is not None else 'not recorded'}.",
        "Interpretation: project duration and critical paths are copied from the "
        "authoritative backend result; exporters do not recompute them.",
    ]
    if duration is not None or path_count is not None:
        lines.append(
            f"Headline result: duration={duration if duration is not None else 'unavailable'}, "
            f"critical paths={path_count if path_count is not None else 'unavailable'}."
        )
    return lines


__all__ = ["interpretation_lines"]

