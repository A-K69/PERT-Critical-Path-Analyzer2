"""Measure reviewer outcomes against Phase 15.5 calibration tiers.

This module consumes exported ``ReviewSession.to_dict()`` JSON files. It never
changes review decisions, thresholds, graph gates, or production behavior.
When no exported sessions are supplied, the report explicitly records that
there is no production reviewer-outcome sample rather than treating fixtures
or calibration baselines as reviewer evidence.
"""
from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable

ITEM_TYPES = ("activities", "durations", "dependencies")


def _status(item: dict[str, Any]) -> str:
    return str(item.get("status", "PENDING")).upper()


def _tier(item: dict[str, Any]) -> str:
    for evidence in item.get("evidence", []) or []:
        tier = (
            evidence.get("metadata", {})
            .get("review_calibration", {})
            .get("tier")
        )
        if tier:
            return str(tier)
    # Exported sessions created before Phase 15.5 remain measurable, but are
    # separated instead of being retroactively assigned a tier.
    return "UNCLASSIFIED_PRE_15_5"


def _confidence(item: dict[str, Any]) -> float | None:
    value = item.get("confidence")
    try:
        return float(value) if value is not None else None
    except (TypeError, ValueError):
        return None


def _outcome(item: dict[str, Any]) -> str:
    status = _status(item)
    if status == "CORRECTED":
        return "CORRECTED"
    if status == "ACCEPTED":
        return "ACCEPTED"
    if status == "REJECTED":
        return "REJECTED"
    return "PENDING"


def _iter_items(session: dict[str, Any]):
    for item_type in ITEM_TYPES:
        for item in session.get(item_type, []) or []:
            yield item_type[:-1], item


def _empty_bucket() -> dict[str, Any]:
    return {
        "total": 0,
        "resolved": 0,
        "pending": 0,
        "accepted": 0,
        "corrected": 0,
        "rejected": 0,
        "resolution_rate": None,
        "correction_rate": None,
        "unresolved_blocker_rate": None,
        "mean_confidence": None,
    }


def _finalize(bucket: dict[str, Any]) -> dict[str, Any]:
    total = bucket["total"]
    resolved = bucket["resolved"]
    confidence_sum = bucket.pop("_confidence_sum", 0.0)
    confidence_count = bucket.pop("_confidence_count", 0)
    bucket["resolution_rate"] = round(resolved / total, 4) if total else None
    bucket["correction_rate"] = (
        round(bucket["corrected"] / total, 4) if total else None
    )
    bucket["unresolved_blocker_rate"] = (
        round(bucket.pop("_unresolved_blockers", 0) / total, 4)
        if total
        else None
    )
    bucket["mean_confidence"] = (
        round(confidence_sum / confidence_count, 4)
        if confidence_count
        else None
    )
    return bucket


def measure_sessions(sessions: Iterable[dict[str, Any]]) -> dict[str, Any]:
    records = list(sessions)
    by_tier: dict[str, dict[str, Any]] = defaultdict(_empty_bucket)
    by_type: dict[str, dict[str, Any]] = defaultdict(_empty_bucket)
    decision_counts: Counter[str] = Counter()
    total_items = 0
    total_sessions = len(records)
    sessions_with_decisions = 0

    for session in records:
        if session.get("decisions"):
            sessions_with_decisions += 1
        for item_type, item in _iter_items(session):
            tier = _tier(item)
            outcome = _outcome(item)
            buckets = (by_tier[tier], by_type[item_type])
            total_items += 1
            decision_counts[outcome] += 1
            for bucket in buckets:
                bucket["total"] += 1
                bucket["resolved"] += outcome != "PENDING"
                bucket["pending"] += outcome == "PENDING"
                bucket["accepted"] += outcome == "ACCEPTED"
                bucket["corrected"] += outcome == "CORRECTED"
                bucket["rejected"] += outcome == "REJECTED"
                if outcome == "PENDING" and tier == "BLOCKING_REVIEW":
                    bucket.setdefault("_unresolved_blockers", 0)
                    bucket["_unresolved_blockers"] += 1
                confidence = _confidence(item)
                if confidence is not None:
                    bucket.setdefault("_confidence_sum", 0.0)
                    bucket.setdefault("_confidence_count", 0)
                    bucket["_confidence_sum"] += confidence
                    bucket["_confidence_count"] += 1

    finalized_tiers = {k: _finalize(v) for k, v in sorted(by_tier.items())}
    finalized_types = {k: _finalize(v) for k, v in sorted(by_type.items())}
    overall = _finalize(
        {
            key: sum(bucket[key] for bucket in by_tier.values())
            for key in ("total", "resolved", "pending", "accepted", "corrected", "rejected")
        }
        | {
            "_unresolved_blockers": sum(
                bucket.get("_unresolved_blockers", 0) for bucket in by_tier.values()
            ),
            "_confidence_sum": sum(
                bucket.get("_confidence_sum", 0.0) for bucket in by_tier.values()
            ),
            "_confidence_count": sum(
                bucket.get("_confidence_count", 0) for bucket in by_tier.values()
            ),
        }
    )
    return {
        "schema_version": "1.0",
        "phase": "15.6",
        "measurement_only": True,
        "production_outcome_data_available": total_sessions > 0 and total_items > 0,
        "sessions": total_sessions,
        "sessions_with_decisions": sessions_with_decisions,
        "items": total_items,
        "decision_counts": dict(sorted(decision_counts.items())),
        "overall": overall,
        "by_tier": finalized_tiers,
        "by_type": finalized_types,
        "limitations": [
            "No persisted production reviewer sessions were found in this repository at measurement time.",
            "Evaluation-only gold corrections are not counted as reviewer outcomes.",
            "False-review rate requires an explicit reviewer outcome label or adjudicated ground truth.",
        ],
    }


def load_sessions(paths: Iterable[str | Path]) -> list[dict[str, Any]]:
    sessions = []
    for path in paths:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        if isinstance(data, list):
            sessions.extend(data)
        else:
            sessions.append(data)
    return sessions


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Phase 15.6 — Reviewer Outcome Measurement",
        "",
        "Measurement-only report. No review decision, confidence threshold, CPM gate, or relationship gate is changed.",
        "",
        f"- Production outcome data available: **{report['production_outcome_data_available']}**",
        f"- Sessions: **{report['sessions']}**; sessions with decisions: **{report['sessions_with_decisions']}**",
        f"- Review items: **{report['items']}**",
        "",
        "## Overall metrics",
        "",
        "| Metric | Value |",
        "|---|---:|",
    ]
    for key in ("total", "resolved", "pending", "accepted", "corrected", "rejected", "resolution_rate", "correction_rate", "unresolved_blocker_rate", "mean_confidence"):
        lines.append(f"| {key} | {report['overall'].get(key)} |")
    lines.extend(["", "## Metrics by calibration tier", "", "| Tier | Total | Resolved | Pending | Accepted | Corrected | Rejected | Resolution rate | Correction rate |", "|---|---:|---:|---:|---:|---:|---:|---:|---:|"])
    for tier, values in report["by_tier"].items():
        lines.append(
            f"| {tier} | {values['total']} | {values['resolved']} | {values['pending']} | "
            f"{values['accepted']} | {values['corrected']} | {values['rejected']} | "
            f"{values['resolution_rate']} | {values['correction_rate']} |"
        )
    lines.extend(["", "## Limitations", ""])
    lines.extend(f"- {text}" for text in report["limitations"])
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("sessions", nargs="*", help="ReviewSession.to_dict() JSON files")
    parser.add_argument("--json", default="docs/PHASE15_6_REVIEW_OUTCOMES.json")
    parser.add_argument("--markdown", default="docs/PHASE15_6_REVIEW_OUTCOMES.md")
    args = parser.parse_args()
    report = measure_sessions(load_sessions(args.sessions))
    Path(args.json).write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    Path(args.markdown).write_text(render_markdown(report), encoding="utf-8")
    print(render_markdown(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
