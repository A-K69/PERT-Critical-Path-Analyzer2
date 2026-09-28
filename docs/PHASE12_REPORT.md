# Phase 12 — AOA Ground Truth and Visual Event-Route Safeguards

**Status:** COMPLETE — two readable AOA references were annotated and the detector now rejects visually contradicted event routes.

## Benchmark expansion

Two draft annotations were manually verified and promoted to `COMPLETE`:

- `3.jpeg`: 13 events and 15 visible directed event-to-event arrows.
- `6.jpeg`: 12 events and 14 visible directed event-to-event arrows.

These are intentionally modeled as **AOA** references: circles are event nodes and visible arrows are event-to-event activity routes. In `6.jpeg`, the visible `K→M` arrow is labeled `L(3)`; `L` is an activity label, not a separate event circle.

## Visual improvement

The AOA arrow validator now uses two geometry-based safeguards:

1. **Same-event self-loop rejection:** a shaft whose two ends contact the same event circle is treated as a visual artifact, even if a false arrowhead was detected.
2. **Intervening-event crossing rejection:** a shaft that crosses the interior of an unrelated event circle is treated as a merged Hough route or routed artifact, not a direct event-to-event activity.

This is based on actual event-circle geometry and does not lower a confidence threshold. Existing no-arrowhead and short legitimate-arrow behavior remains covered by regression tests.

## Measured results

| Image | Metric | Before | After |
|---|---|---:|---:|
| `3.jpeg` | Event F1 | 1.0000 | 1.0000 |
| `3.jpeg` | Directed arrow precision | 0.5238 | **0.9167** |
| `3.jpeg` | Directed arrow recall | 0.7333 | 0.7333 |
| `3.jpeg` | Directed arrow F1 | 0.6111 | **0.8148** |
| `3.jpeg` | Direction accuracy | 1.0000 | 1.0000 |
| `6.jpeg` | Event F1 | 1.0000 | 1.0000 |
| `6.jpeg` | Directed arrow precision | 0.5455 | **1.0000** |
| `6.jpeg` | Directed arrow recall | 0.4286 | 0.4286 |
| `6.jpeg` | Directed arrow F1 | 0.4800 | **0.6000** |
| `6.jpeg` | Direction accuracy | 1.0000 | 1.0000 |

Recall is unchanged because the remaining misses are primarily fragmented or unresolved arrow endpoints; recovering those should be the next AOA-specific task, not a threshold relaxation.

## Verification

- AOA, reconstruction, and ground-truth tests: **201 passed**.
- Static syntax and focused lint: passed.
- Annotation validation: **8 annotations found, 0 errors, 0 warnings**.
- Refreshed full benchmark: **8 images analyzed, 0 fatal failures, 5 complete
  accuracy annotations**; all eight remain review-required by the conservative
  production review gate.
- No changes were made to the AON safeguards from Phase 11.
