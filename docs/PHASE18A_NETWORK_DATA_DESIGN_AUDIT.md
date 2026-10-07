# Phase 18A — Network Data Review and Design Audit

## Status

**Design review complete. Production code unchanged. Awaiting approval for Phase 18B implementation.**

## Reference data reviewed

The design uses the real reference Results fixture: **22 activities, 28 dependencies, 54 days, and 16 critical paths**. The backend snapshot already exposes the required Network data through `ResultsData` and its retained graph/CPM objects:

| Network requirement | Authoritative source | Available |
|---|---|---:|
| Activity ID | `ActivityRow.activity_id` / graph activity key | Yes |
| Activity name | `ActivityRow.name` / graph activity | Yes |
| Duration | `ActivityRow.duration` / graph activity | Yes |
| Early start / finish | `ActivityRow.early_start`, `early_finish` | Yes |
| Late start / finish | `ActivityRow.late_start`, `late_finish` | Yes |
| Total/free float | `ActivityRow.total_float`, `free_float` | Yes |
| Critical state | `ActivityRow.is_critical` / CPM analysis | Yes |
| Predecessors / successors | `ActivityRow.predecessors`, `successors` | Yes |
| Directed relationships | `DependencyRow.source`, `target` | Yes |
| Complete critical paths | `ResultsData.critical_paths` | Yes |
| Critical edges | `ResultsData.critical_edges` | Yes |
| PERT mode | Existing `set_pert_data()` and `PertData` | Yes |

## Current implementation findings

The current Network canvas is functionally safe and already has deterministic layout, node/edge items, critical-edge detection, zoom, fit, reset, path highlighting, metric mode switching, and node-selection signals. It correctly treats the GUI as a read-only projection of backend graph and CPM data.

The main presentation gaps are not missing backend data. They are visual and interaction gaps:

1. Activity nodes currently show only ID, one duration metric, float, and a critical marker. They do not provide a structured detail surface for early/late dates, names, or relationships.
2. The canvas has controls, but no clear visual grouping of network state, legend, selected activity, or current critical-path focus.
3. Selecting a node emits a signal, but the Network tab itself does not provide an Inspector surface that explains the selected node and its neighborhood.
4. Critical edges are technically highlighted, but the design needs a stronger distinction between ordinary graph context, critical structure, and the currently focused route.
5. The existing deterministic layout is safe but dense for a 22-activity graph. Phase 18B should improve presentation spacing and routing without changing graph topology or introducing a heuristic relationship algorithm.

## Proposed Phase 18B visual contract

The mockup introduces one coherent Network workspace:

- A compact header identifying the reviewed graph and authoritative CPM state.
- A toolbar with Fit to view, Reset zoom, zoom controls, Focus critical path, Clear highlight, and CPM/PERT metric selection.
- A small legend distinguishing critical path, standard graph, and selected state.
- A large graph canvas with a dark engineering grid, readable activity cards, semantic critical colors, directional arrows, and a focused route.
- A true left-to-right **layered DAG**, not a single-line river. Each parent is placed in a logical level and its siblings fan out locally: one child may sit slightly above the parent line, another near the parent line, and others below it. This preserves the actual dependency topology while making branching and merging read like a real network diagram.
- A right-side Selected Activity Inspector with duration, total float, early/late dates, predecessors, successors, critical-path membership, and explanatory text.
- A small glass-style hover preview for quick inspection. It shows Early Start, Early Finish, Late Start, Late Finish, float, and whether the activity belongs to the critical structure. Clicking pins the full Inspector.
- The upper branch level, primary logical level, and lower branch level have deliberate vertical separation and faint guide lines. This prevents sibling branches from visually collapsing into the parent level.
- A minimap/viewport cue and concise interaction hint for pan/zoom.

## Design rules

The Network surface must remain professional and data-first rather than decorative. Critical gold is reserved for zero-float/critical structure; cyan is reserved for the selected node and focused route; blue is used for ordinary interactive controls; green communicates authoritative/readiness state. The Inspector must never invent or recompute CPM values. It reads the selected `ActivityRow` and existing backend relationship collections.

For preliminary image-analysis sessions, the same visual shell may be reused, but the trust banner and labels must remain `PRELIMINARY` and must not show CPM values as authoritative until the existing readiness gate passes.

## Mockup scope

The PNG is a design proposal, not a production screenshot. It uses the actual reference metrics and actual critical route structure. The canvas illustrates the intended visual language and a representative visible portion of the graph; the production implementation will render all available nodes and edges through the existing deterministic layout and scrolling/fit behavior.

## Approval gate

Phase 18B should begin only after approval of the following decisions:

- The right-side Inspector is part of the Network design.
- The graph uses logical levels with local sibling fan-out and explicit merge points; it must not collapse a branching network into one straight line.
- The node card hierarchy is ID first, metrics second, critical state third.
- Hover previews show the four timing values: Early Start, Early Finish, Late Start, and Late Finish.
- Critical path focus uses gold for critical structure and cyan for the actively focused route.
- Network controls remain compact and grouped above the canvas.
- The Network tab may show all backend fields in the Inspector without duplicating the Activities table.

## Artifacts

- Design image v4: `docs/PHASE18A_NETWORK_DESIGN_MOCKUP_V4.png`
- Editable design source v4: `docs/PHASE18A_NETWORK_DESIGN_MOCKUP.html`
