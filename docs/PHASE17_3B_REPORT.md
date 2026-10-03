# Phase 17.3B — Safe Image Preview Workspace

## Status

**Implemented and verified.**

## Objective

Make the image-analysis Results route visually useful before review completion without presenting preliminary detections as authoritative CPM results.

## Implementation

Added `DetectedPreviewTab`, a dedicated read-only canvas that consumes only:

```text
GuiSession.review_session.reconstruction
```

It does not consume `ResultsData`, CPM analyses, critical paths, float values, or project duration.

### Supported preview content

- AON reconstructed activity nodes.
- AON reconstructed dependency edges.
- AOA event nodes and activity arrows when event geometry is available.
- Detected duration labels only; no schedule calculations.
- Zoom in, zoom out, fit-to-view, and drag navigation.
- Node selection-ready visual objects and tooltips.
- Preliminary legend and trust labeling.

### Visual evidence states

- Blue: detected evidence.
- Amber: review required or low-confidence evidence.
- Green: resolved review evidence.
- Dashed amber edges: uncertain relationships.

The canvas is labeled:

```text
PRELIMINARY · NOT CPM
```

### Safety boundary

The preview does not:

- compute CPM or PERT;
- show ES, EF, LS, LF, float, critical paths, or project duration;
- alter review decisions;
- lower confidence thresholds;
- bypass validation or human review;
- replace the authoritative Results dashboard.

The authoritative dashboard remains gated by the existing `describe_ready()` contract.

## Tests

- Focused Results/Network/Recovery tests: **52 passed**.
- Full GUI suite: **319 passed**.
- Python compilation checks passed.
- `git diff --check` passed.

## Next phase

Phase 17.3C should improve the preview interaction layer by connecting selected nodes/edges to the matching Review Center item and adding richer confidence/evidence inspectors while retaining the same non-authoritative data boundary.
