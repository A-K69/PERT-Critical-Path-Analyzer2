# Phase 18C — Network Interaction and Hover Preview

## Status

**Implemented and tested.** This phase strengthens the Network tab interaction layer without changing the authoritative graph or CPM data.

## Interaction improvements

The hover preview now measures itself before placement and is constrained to the Network tab bounds. Its preferred position is above and to the right of the node; it automatically moves below a node near the top edge, moves left when the right edge is crowded, and applies a final clamp for small viewports.

The implementation also tracks the currently hovered activity. A delayed or stale leave event from a previous node can no longer hide the preview belonging to the next node. Clicking a node clears the transient preview, pins the activity in the Inspector, and emits the existing `node_selected` signal for cross-tab navigation.

The preview presents one timing value per line—Early Start, Early Finish, Late Start, Late Finish—followed by float and critical membership. This avoids dense inline wrapping while keeping the compact technical visual style.

## Data-safety contract

All displayed values still come from the existing activity row and CPM/PERT snapshot. Phase 18C does not recompute timing values, infer relationships, or modify critical-path state.

## Verification

The focused Network suite now contains **27 passing tests**, including:

- Preview visibility and authoritative timing text.
- Preview geometry remaining inside the tab.
- Stale leave-event protection during rapid movement between nodes.
- Click-to-pin behavior and Inspector update.
- Extreme node positions that force boundary clamping.

The real application preview was captured in [`PHASE18C_NETWORK_HOVER_REAL_APP.png`](PHASE18C_NETWORK_HOVER_REAL_APP.png).
