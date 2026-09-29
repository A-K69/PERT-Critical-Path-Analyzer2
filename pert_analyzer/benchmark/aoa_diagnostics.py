"""Diagnostics for AOA diagonal and fragmented route recovery.

This module is measurement-only. It does not modify the production detector or
promote any candidate route. It inventories raw line support for manually
annotated event pairs so Phase 14 stitching thresholds can be chosen from
observed evidence rather than guesses.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

from pert_analyzer.pipeline.analyzer import EndToEndAnalyzer

Point2 = Tuple[float, float]
Circle = Tuple[str, float, float, float]


def _distance(a: Point2, b: Point2) -> float:
    return math.hypot(a[0] - b[0], a[1] - b[1])


def _angle_delta(a: float, b: float) -> float:
    """Smallest difference between two unoriented line angles."""
    delta = abs((a - b) % 180.0)
    return min(delta, 180.0 - delta)


def _segment_angle(start: Point2, end: Point2) -> float:
    return math.degrees(math.atan2(end[1] - start[1], end[0] - start[0])) % 180.0


def _union_coverage(intervals: Sequence[Tuple[float, float]]) -> float:
    if not intervals:
        return 0.0
    ordered = sorted((min(a, b), max(a, b)) for a, b in intervals)
    merged: List[Tuple[float, float]] = [ordered[0]]
    for start, end in ordered[1:]:
        previous_start, previous_end = merged[-1]
        if start <= previous_end:
            merged[-1] = (previous_start, max(previous_end, end))
        else:
            merged.append((start, end))
    return sum(end - start for start, end in merged)


def _route_segment_support(
    source: Circle,
    target: Circle,
    segments: Iterable[Any],
    max_lateral_distance: float = 14.0,
    max_angle_delta: float = 22.0,
) -> Dict[str, Any]:
    """Measure raw Hough support along the interior source-target corridor."""
    _, sx, sy, sr = source
    _, tx, ty, tr = target
    dx, dy = tx - sx, ty - sy
    distance = math.hypot(dx, dy)
    if distance <= sr + tr + 8.0:
        return {"supporting_segments": 0, "coverage": 0.0, "angular_consistency": 0.0}
    ux, uy = dx / distance, dy / distance
    start_t = (sr + 4.0) / distance
    end_t = 1.0 - (tr + 4.0) / distance
    intervals: List[Tuple[float, float]] = []
    angles: List[float] = []
    for segment in segments:
        a = (float(segment.start.x), float(segment.start.y))
        b = (float(segment.end.x), float(segment.end.y))
        midpoint = ((a[0] + b[0]) / 2.0, (a[1] + b[1]) / 2.0)
        projection = ((midpoint[0] - sx) * ux + (midpoint[1] - sy) * uy) / distance
        if projection <= start_t or projection >= end_t:
            continue
        lateral = abs((midpoint[0] - sx) * uy - (midpoint[1] - sy) * ux)
        angle = _angle_delta(_segment_angle(a, b), _segment_angle((sx, sy), (tx, ty)))
        if lateral > max_lateral_distance or angle > max_angle_delta:
            continue
        projections = [
            (point[0] - sx) * ux + (point[1] - sy) * uy
            for point in (a, b)
        ]
        intervals.append((
            max(start_t, min(projections) / distance),
            min(end_t, max(projections) / distance),
        ))
        angles.append(angle)
    route_length = max(1e-9, end_t - start_t)
    coverage = _union_coverage(intervals) / route_length
    return {
        "supporting_segments": len(intervals),
        "coverage": round(min(1.0, coverage), 4),
        "angular_consistency": round(
            max(0.0, 1.0 - (sum(angles) / len(angles)) / max_angle_delta)
            if angles else 0.0,
            4,
        ),
        "max_lateral_distance": max_lateral_distance,
        "max_angle_delta": max_angle_delta,
    }


def _event_circles(result: Any) -> List[Circle]:
    circles: List[Circle] = []
    shape_result = getattr(result, "_shape_result", None)
    for node in getattr(shape_result, "candidate_nodes", []) or []:
        position = getattr(node, "position", None)
        bbox = getattr(node, "bounding_box", None)
        if position is None or bbox is None:
            continue
        shape_name = str(getattr(node, "shape_type", "")).upper()
        if "CIRCLE" not in shape_name:
            continue
        radius = max(8.0, (float(bbox.width) + float(bbox.height)) / 4.0)
        circles.append((node.node_id, float(position.x), float(position.y), radius))
    return circles


def _intervening(source: Circle, target: Circle, circles: Sequence[Circle]) -> List[str]:
    _, sx, sy, sr = source
    _, tx, ty, tr = target
    dx, dy = tx - sx, ty - sy
    length_sq = dx * dx + dy * dy
    if length_sq <= 1e-9:
        return []
    crossed: List[str] = []
    endpoint_ids = {source[0], target[0]}
    for cid, cx, cy, radius in circles:
        if cid in endpoint_ids:
            continue
        projection = ((cx - sx) * dx + (cy - sy) * dy) / length_sq
        if projection <= 0.08 or projection >= 0.92:
            continue
        px, py = sx + projection * dx, sy + projection * dy
        if math.hypot(cx - px, cy - py) <= radius * 1.05:
            crossed.append(cid)
    return crossed


def diagnose_image(
    image_path: str | Path,
    annotation_path: str | Path | None = None,
) -> Dict[str, Any]:
    """Return a serializable diagnostic inventory for one AOA image."""
    path = Path(image_path)
    result = EndToEndAnalyzer().analyze(str(path))
    circles = _event_circles(result)
    labels: Dict[str, str] = {}
    if annotation_path is not None:
        annotation = json.loads(Path(annotation_path).read_text(encoding="utf-8"))
        expected = {
            item["id"]: tuple(item["position"][:2])
            for item in annotation.get("events", [])
            if item.get("id") and item.get("position")
        }
        for circle in circles:
            labels[circle[0]] = min(
                expected,
                key=lambda label: _distance((circle[1], circle[2]), expected[label]),
            )
    arrow_result = getattr(result, "_arrow_result", None)
    raw_segments = list(getattr(arrow_result, "raw_line_segments", []) or [])
    arrows = list(getattr(arrow_result, "arrows", []) or [])
    rejected = list(getattr(arrow_result, "rejected_arrows", []) or [])
    route_inventory: List[Dict[str, Any]] = []
    for source in circles:
        for target in circles:
            if source[0] == target[0] or target[1] <= source[1]:
                continue
            support = _route_segment_support(source, target, raw_segments)
            crossed = _intervening(source, target, circles)
            if support["supporting_segments"] or crossed:
                route_inventory.append({
                    "source": source[0],
                    "target": target[0],
                    "source_label": labels.get(source[0]),
                    "target_label": labels.get(target[0]),
                    **support,
                    "intervening_events": crossed,
                    "candidate": bool(
                        support["supporting_segments"] >= 2
                        and support["coverage"] >= 0.35
                        and support["angular_consistency"] >= 0.65
                        and not crossed
                    ),
                    "near_candidate": bool(
                        support["supporting_segments"] >= 2
                        and support["coverage"] >= 0.25
                        and support["angular_consistency"] >= 0.45
                        and not crossed
                    ),
                })
    unresolved = []
    for arrow in arrows:
        validation = arrow.evidence.get("aoa_validation", {})
        if validation.get("event_contact_count", 0) < 2:
            unresolved.append({
                "arrow_id": arrow.arrow_id,
                "length": round(float(arrow.length), 2),
                "arrowhead_confidence": round(float(arrow.arrowhead_confidence), 3),
                "event_contact_count": validation.get("event_contact_count", 0),
                "start": [round(float(arrow.start.x), 2), round(float(arrow.start.y), 2)],
                "end": [round(float(arrow.end.x), 2), round(float(arrow.end.y), 2)],
            })
    return {
        "image": path.name,
        "diagram_type": getattr(result, "diagram_type", None),
        "event_count": len(circles),
        "raw_line_segments": len(raw_segments),
        "logical_arrows": len(arrows),
        "rejected_arrows": len(rejected),
        "unresolved_logical_arrows": unresolved,
        "route_inventory": sorted(
            route_inventory,
            key=lambda item: (item["candidate"], item["coverage"]),
            reverse=True,
        ),
    }


def render_markdown(records: Sequence[Dict[str, Any]]) -> str:
    lines = [
        "# Phase 14.1 — AOA Route Diagnostics",
        "",
        "Measurement-only inventory for diagonal and fragmented route stitching.",
        "No candidate in this report is promoted to a production dependency.",
        "",
    ]
    for record in records:
        lines.extend([
            f"## {record['image']}",
            "",
            f"- Events: **{record['event_count']}**",
            f"- Raw line segments: **{record['raw_line_segments']}**",
            f"- Logical arrows: **{record['logical_arrows']}**",
            f"- Rejected arrows: **{record['rejected_arrows']}**",
            f"- Unresolved logical arrows: **{len(record['unresolved_logical_arrows'])}**",
            "",
            "| Source | Target | Segments | Coverage | Angular consistency | Intermediate events | Candidate | Near candidate |",
            "|---|---:|---:|---:|---:|---|---|---|",
        ])
        for route in record["route_inventory"]:
            source = route.get("source_label") or route["source"]
            target = route.get("target_label") or route["target"]
            lines.append(
                f"| {source} | {target} | "
                f"{route['supporting_segments']} | {route['coverage']:.3f} | "
                f"{route['angular_consistency']:.3f} | "
                f"{', '.join(route['intervening_events']) or '—'} | "
                f"{'yes' if route['candidate'] else 'no'} | "
                f"{'yes' if route['near_candidate'] else 'no'} |"
            )
        lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("images", nargs="+", help="AOA image paths")
    parser.add_argument("--ground-truth-dir", type=Path)
    parser.add_argument("--json", dest="json_path", type=Path)
    parser.add_argument("--markdown", dest="markdown_path", type=Path)
    args = parser.parse_args()
    records = []
    for image in args.images:
        annotation = None
        if args.ground_truth_dir:
            annotation = args.ground_truth_dir / f"{Path(image).stem}.json"
        records.append(diagnose_image(image, annotation if annotation and annotation.exists() else None))
    if args.json_path:
        args.json_path.write_text(json.dumps(records, indent=2), encoding="utf-8")
    if args.markdown_path:
        args.markdown_path.write_text(render_markdown(records), encoding="utf-8")
    if not args.json_path and not args.markdown_path:
        print(json.dumps(records, indent=2))


if __name__ == "__main__":
    main()
