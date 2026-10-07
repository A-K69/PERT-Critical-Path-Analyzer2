"""
Deterministic AON layout layer for the network canvas.

Computes presentation-only coordinates from the backend graph. Never
modifies GraphModel data; the layout is a view-level concern.

Uses a topological (Kahn) ordering, groups activities by their longest
logical level, and exposes both the legacy compact layout and the newer
layered layout used by the Network Results view.
"""

from __future__ import annotations

from collections import defaultdict, deque
from typing import Any, Dict, List, Tuple


NODE_WIDTH = 132
NODE_HEIGHT = 68
H_SPACING = 72
V_SPACING = 28
MARGIN = 40
LAYER_H_SPACING = 112
LAYER_V_SPACING = 74


def build_layout(
    activity_ids: List[str],
    dependencies: List[Any],
    node_width: int = NODE_WIDTH,
    node_height: int = NODE_HEIGHT,
    h_spacing: int = H_SPACING,
    v_spacing: int = V_SPACING,
    margin: int = MARGIN,
) -> Dict[str, Tuple[float, float, float, float]]:
    """Return activity_id -> (x, y, width, height) presentation rects.

    ``dependencies`` accepts objects with ``source``/``target`` attributes
    or (source, target) tuples.
    """
    id_set = set(activity_ids)
    successors: Dict[str, List[str]] = defaultdict(list)
    predecessors: Dict[str, List[str]] = defaultdict(list)
    edge_pairs: List[Tuple[str, str]] = []
    for dep in dependencies:
        if isinstance(dep, tuple):
            src, tgt = dep
        else:
            src = getattr(dep, "source", None)
            tgt = getattr(dep, "target", None)
        if src is None or tgt is None:
            continue
        if src in id_set and tgt in id_set:
            successors[src].append(tgt)
            predecessors[tgt].append(src)
            edge_pairs.append((src, tgt))

    indegree = {aid: len(predecessors.get(aid, [])) for aid in activity_ids}
    ready = deque(sorted(aid for aid in activity_ids if indegree[aid] == 0))
    topo_order: List[str] = []
    while ready:
        aid = ready.popleft()
        topo_order.append(aid)
        for nxt in sorted(successors.get(aid, [])):
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                ready.append(nxt)
    # Any unvisited (disconnected) nodes keep a stable appendix.
    for aid in sorted(activity_ids):
        if aid not in set(topo_order):
            topo_order.append(aid)

    level: Dict[str, int] = {aid: 0 for aid in activity_ids}
    for aid in topo_order:
        for nxt in successors.get(aid, []):
            level[nxt] = max(level[nxt], level[aid] + 1)

    by_level: Dict[int, List[str]] = defaultdict(list)
    for aid in topo_order:
        by_level[level[aid]].append(aid)

    col_step = node_width + h_spacing
    row_step = node_height + v_spacing
    positions: Dict[str, Tuple[float, float, float, float]] = {}
    for lvl in sorted(by_level):
        ids_in_level = sorted(by_level[lvl])
        for row, aid in enumerate(ids_in_level):
            x = margin + lvl * col_step
            y = margin + row * row_step
            positions[aid] = (float(x), float(y), float(node_width), float(node_height))

    return positions


def build_layered_layout(
    activity_ids: List[str],
    dependencies: List[Any],
    node_width: int = NODE_WIDTH,
    node_height: int = NODE_HEIGHT,
    h_spacing: int = LAYER_H_SPACING,
    v_spacing: int = LAYER_V_SPACING,
    margin: int = MARGIN,
) -> Dict[str, Tuple[float, float, float, float]]:
    """Return a readable left-to-right layered DAG layout.

    Nodes are grouped by their longest logical level. Within each level,
    siblings are placed around the median y-position of their predecessors,
    producing local fan-out and merge patterns instead of a single straight
    line or an arbitrary global grid. Only presentation coordinates change;
    the backend graph and dependency relationships remain untouched.
    """
    id_set = set(activity_ids)
    successors: Dict[str, List[str]] = defaultdict(list)
    predecessors: Dict[str, List[str]] = defaultdict(list)
    for dep in dependencies:
        if isinstance(dep, tuple):
            src, tgt = dep
        else:
            src = getattr(dep, "source", None)
            tgt = getattr(dep, "target", None)
        if src in id_set and tgt in id_set:
            successors[src].append(tgt)
            predecessors[tgt].append(src)

    indegree = {aid: len(predecessors.get(aid, [])) for aid in activity_ids}
    ready = deque(sorted(aid for aid in activity_ids if indegree[aid] == 0))
    topo_order: List[str] = []
    while ready:
        aid = ready.popleft()
        topo_order.append(aid)
        for nxt in sorted(successors.get(aid, [])):
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                ready.append(nxt)
    for aid in sorted(activity_ids):
        if aid not in topo_order:
            topo_order.append(aid)

    level = {aid: 0 for aid in activity_ids}
    for aid in topo_order:
        for nxt in sorted(successors.get(aid, [])):
            level[nxt] = max(level[nxt], level[aid] + 1)

    by_level: Dict[int, List[str]] = defaultdict(list)
    for aid in topo_order:
        by_level[level[aid]].append(aid)

    row_step = node_height + v_spacing
    center_y = margin + 4 * row_step
    y_by_id: Dict[str, float] = {}
    for lvl in sorted(by_level):
        ids_in_level = sorted(by_level[lvl])
        anchors: List[Tuple[str, float]] = []
        for aid in ids_in_level:
            parent_ys = [y_by_id[p] for p in predecessors.get(aid, []) if p in y_by_id]
            anchors.append((aid, sum(parent_ys) / len(parent_ys) if parent_ys else center_y))
        anchors.sort(key=lambda item: (item[1], item[0]))
        placed: Dict[str, float] = {}
        for aid, anchor in anchors:
            placed[aid] = max(anchor, (max(placed.values()) + row_step) if placed else anchor)
        if placed:
            offset = center_y - (min(placed.values()) + max(placed.values())) / 2
            for aid, y in placed.items():
                y_by_id[aid] = y + offset

    col_step = node_width + h_spacing
    return {
        aid: (
            float(margin + level[aid] * col_step),
            float(y_by_id.get(aid, center_y)),
            float(node_width),
            float(node_height),
        )
        for aid in activity_ids
    }


def edge_points(
    positions: Dict[str, Tuple[float, float, float, float]],
    source: str,
    target: str,
) -> Tuple[Tuple[float, float], Tuple[float, float]]:
    """Return (start, end) points for a source->target dependency arrow."""
    sx, sy, sw, sh = positions[source]
    tx, ty, tw, th = positions[target]
    start = (sx + sw, sy + sh / 2)
    end = (tx, ty + th / 2)
    return start, end
