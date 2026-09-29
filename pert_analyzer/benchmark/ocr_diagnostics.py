"""Measurement-only OCR baseline diagnostics for Phase 15.1."""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from pert_analyzer.pipeline.analyzer import EndToEndAnalyzer


def _inside(region: Any, bbox: List[float], padding: float = 0.0) -> bool:
    x, y, w, h = bbox
    cx, cy = float(region.center.x), float(region.center.y)
    return x - padding <= cx <= x + w + padding and y - padding <= cy <= y + h + padding


def _distance(region: Any, position: List[float]) -> float:
    return math.hypot(float(region.center.x) - position[0], float(region.center.y) - position[1])


def _text_key(region: Any) -> str:
    return (getattr(region, "normalized_text", None) or getattr(region, "text", "") or "").strip()


def _expected_items(annotation: Dict[str, Any]) -> List[Dict[str, Any]]:
    return list(annotation.get("activities", []) or [])


def _nearest_expected_node(node: Any, expected: List[Dict[str, Any]]) -> Optional[str]:
    position = getattr(node, "position", None)
    if position is None or not expected:
        return None
    return min(
        expected,
        key=lambda item: math.hypot(
            float(position.x) - float(item["position"][0]),
            float(position.y) - float(item["position"][1]),
        ),
    ).get("id")


def diagnose_image(image_path: str | Path, annotation_path: str | Path | None = None) -> Dict[str, Any]:
    path = Path(image_path)
    result = EndToEndAnalyzer().analyze(str(path))
    ocr = getattr(result, "_ocr_result", None)
    regions = list(getattr(ocr, "regions", []) or [])
    associations = {
        item.text_region_id: item
        for item in (getattr(result, "_association_results", None) or [])
    }
    annotation = json.loads(Path(annotation_path).read_text(encoding="utf-8")) if annotation_path else {}
    expected = _expected_items(annotation)
    expected_by_id = {item.get("id"): item for item in expected}
    shape_result = getattr(result, "_shape_result", None)
    nodes = list(getattr(shape_result, "candidate_nodes", []) or [])
    node_to_expected = {
        node.node_id: _nearest_expected_node(node, expected)
        for node in nodes
    }
    region_rows: List[Dict[str, Any]] = []
    for region in regions:
        association = associations.get(region.region_id)
        best = getattr(association, "best_association", None) if association else None
        region_rows.append({
            "region_id": region.region_id,
            "text": _text_key(region),
            "raw_text": getattr(region, "raw_text", ""),
            "confidence": round(float(getattr(region, "confidence", 0.0)), 3),
            "text_type": getattr(getattr(region, "text_type", None), "value", str(getattr(region, "text_type", ""))),
            "is_numeric": bool(getattr(region, "is_numeric", False)),
            "parsed_value": getattr(region, "parsed_value", None),
            "center": [round(float(region.center.x), 1), round(float(region.center.y), 1)],
            "association_ambiguous": bool(getattr(association, "is_ambiguous", False)),
            "association_score": round(float(getattr(best, "association_score", 0.0)), 3) if best else 0.0,
            "associated_expected_id": node_to_expected.get(getattr(best, "candidate_target_id", "")) if best else None,
        })
    item_rows: List[Dict[str, Any]] = []
    for item in expected:
        item_id = item.get("id", "")
        bbox = item.get("bbox", [0, 0, 0, 0])
        inside = [region for region in regions if _inside(region, bbox)]
        expanded = [region for region in regions if _inside(region, bbox, padding=max(bbox[2], bbox[3]) * 0.35)]
        id_matches = [region for region in inside if _text_key(region).upper() == str(item_id).upper()]
        duration = item.get("duration")
        duration_matches = [
            region for region in inside
            if getattr(region, "parsed_value", None) is not None
            and duration is not None
            and abs(float(region.parsed_value) - float(duration)) <= 0.01
        ]
        association_hits = [
            region for region in inside
            if node_to_expected.get(
                getattr(getattr(associations.get(region.region_id), "best_association", None), "candidate_target_id", "")
            ) == item_id
        ]
        if not inside and expanded:
            error_class = "localization_error"
        elif not id_matches and not duration_matches:
            error_class = "recognition_or_semantic_error"
        elif inside and not association_hits:
            error_class = "association_error"
        elif len(inside) > 3:
            error_class = "duplicate_detections"
        else:
            error_class = "matched"
        item_rows.append({
            "id": item_id,
            "expected_duration": duration,
            "regions_inside": len(inside),
            "regions_nearby": len(expanded),
            "id_match": bool(id_matches),
            "duration_match": bool(duration_matches),
            "association_match": bool(association_hits),
            "error_class": error_class,
            "observed_text": [_text_key(region) for region in inside],
        })
    counts: Dict[str, int] = {}
    for row in item_rows:
        counts[row["error_class"]] = counts.get(row["error_class"], 0) + 1
    ambiguous = sum(1 for row in region_rows if row["association_ambiguous"])
    unmatched = sum(1 for row in region_rows if not row["associated_expected_id"])
    return {
        "image": path.name,
        "diagram_type": getattr(result, "diagram_type", None),
        "expected_items": len(expected),
        "ocr_regions": len(regions),
        "ocr_numeric_candidates": len(getattr(ocr, "numeric_candidates", []) or []),
        "association_results": len(associations),
        "ambiguous_associations": ambiguous,
        "unmatched_regions": unmatched,
        "item_error_counts": counts,
        "id_exact_matches": sum(1 for row in item_rows if row["id_match"]),
        "duration_exact_matches": sum(1 for row in item_rows if row["duration_match"]),
        "association_exact_matches": sum(1 for row in item_rows if row["association_match"]),
        "items": item_rows,
        "regions": region_rows,
    }


def render_markdown(records: List[Dict[str, Any]]) -> str:
    lines = [
        "# Phase 15.1 — OCR Baseline Diagnostics",
        "",
        "Measurement-only report. No OCR behavior is changed by this artifact.",
        "",
        "| Image | Type | Expected items | OCR regions | Numeric candidates | Ambiguous associations | Unmatched regions | ID exact | Duration exact | Association exact |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for record in records:
        lines.append(
            f"| {record['image']} | {record['diagram_type']} | {record['expected_items']} | "
            f"{record['ocr_regions']} | {record['ocr_numeric_candidates']} | "
            f"{record['ambiguous_associations']} | {record['unmatched_regions']} | "
            f"{record['id_exact_matches']} | {record['duration_exact_matches']} | "
            f"{record['association_exact_matches']} |"
        )
        lines.append("")
        lines.append(f"### {record['image']} error classes")
        lines.append("")
        for key, value in sorted(record["item_error_counts"].items()):
            lines.append(f"- `{key}`: **{value}**")
        lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("images", nargs="+")
    parser.add_argument("--ground-truth-dir", type=Path)
    parser.add_argument("--json", dest="json_path", type=Path)
    parser.add_argument("--markdown", dest="markdown_path", type=Path)
    args = parser.parse_args()
    records = []
    for image in args.images:
        annotation = None
        if args.ground_truth_dir:
            candidate = args.ground_truth_dir / f"{Path(image).stem}.json"
            annotation = candidate if candidate.exists() else None
        records.append(diagnose_image(image, annotation))
    if args.json_path:
        args.json_path.write_text(json.dumps(records, indent=2), encoding="utf-8")
    if args.markdown_path:
        args.markdown_path.write_text(render_markdown(records), encoding="utf-8")
    if not args.json_path and not args.markdown_path:
        print(json.dumps(records, indent=2))


if __name__ == "__main__":
    main()
