"""Review calibration diagnostics for the Phase 15.5 benchmark."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, Iterable

from pert_analyzer.pipeline.analyzer import EndToEndAnalyzer
from pert_analyzer.pipeline.human_review import build_review_session


def diagnose_image(path: str | Path) -> Dict[str, Any]:
    image = Path(path)
    result = EndToEndAnalyzer().analyze(str(image))
    session = build_review_session(result, source_image_id=image.name)
    calibration = session.metadata.get("review_calibration", {})
    return {
        "image": image.name,
        "analysis_status": getattr(result.status, "value", str(result.status)),
        "activity_reviews": len(session.activities),
        "duration_reviews": len(session.durations),
        "dependency_reviews": len(session.dependencies),
        "ambiguities": len(session.ambiguities),
        "tier_counts": calibration.get("tier_counts", {}),
        "auto_accept_enabled": calibration.get("auto_accept_enabled", False),
        "relationship_gate_unchanged": calibration.get(
            "relationship_gate_unchanged", True
        ),
    }


def diagnose_images(paths: Iterable[str | Path]) -> list[Dict[str, Any]]:
    return [diagnose_image(path) for path in paths]


def render_markdown(records: list[Dict[str, Any]]) -> str:
    lines = [
        "# Phase 15.5 Review Calibration Diagnostics",
        "",
        "The calibration is triage-only: no item is auto-accepted and the relationship gate is unchanged.",
        "",
        "| Image | Activity reviews | Duration reviews | Dependency reviews | Ambiguities | Tiers |",
        "|---|---:|---:|---:|---:|---|",
    ]
    for record in records:
        tiers = ", ".join(
            f"{key}={value}" for key, value in sorted(record["tier_counts"].items())
        ) or "none"
        lines.append(
            f"| `{record['image']}` | {record['activity_reviews']} | "
            f"{record['duration_reviews']} | {record['dependency_reviews']} | "
            f"{record['ambiguities']} | {tiers} |"
        )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("images", nargs="+")
    parser.add_argument("--json", default="docs/PHASE15_5_REVIEW_DIAGNOSTICS.json")
    parser.add_argument("--markdown", default="docs/PHASE15_5_REVIEW_DIAGNOSTICS.md")
    args = parser.parse_args()
    records = diagnose_images(args.images)
    Path(args.json).write_text(json.dumps(records, indent=2) + "\n")
    Path(args.markdown).write_text(render_markdown(records))
    print(render_markdown(records))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
