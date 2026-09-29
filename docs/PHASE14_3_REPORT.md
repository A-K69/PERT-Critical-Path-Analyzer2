# Phase 14.3 — Missing-Arrowhead Direction Review Gate

**Status:** IMPLEMENTED and regression-verified.

## Behavior

AOA activities whose detected arrowhead is absent are now explicitly marked for human review. The reconstruction retains the geometric route and all evidence, but adds:

- `needs_review = true`;
- a warning that the arrowhead was not observed;
- an evidence trace explaining that direction is geometry/layout-derived;
- provenance indicating whether the route was recovered and which direction source was used.

This deliberately separates **route visibility** from **direction certainty**. A missing arrowhead can contribute a reviewable candidate, but it is not silently represented as a fully confirmed directed activity.

## Quality gate

The change does not alter the measured event-pair accuracy:

| Image | Precision | Recall | F1 | Direction accuracy |
|---|---:|---:|---:|---:|
| `3.jpeg` | 0.9231 | 0.8000 | 0.8571 | 1.0000 |
| `6.jpeg` | 1.0000 | 0.5714 | 0.7273 | 1.0000 |

The review item count increased as intended (`3.jpeg`: 17, `6.jpeg`: 19), making uncertain direction visible to the review workflow rather than hiding it.

## Verification

- 242 focused tests passed, including the explicit review contract.
- Full repository suite: **1456 passed**; two PDF export tests failed on the
  pre-existing environment mismatch where the installed legacy `fpdf` does not
  support the repository's `new_x`/`new_y` API. No Phase 14 test failed.
- Python compilation passed.
- The repository has a pre-existing unrelated Ruff `F821` warning for the forward annotation `ReconciliationResult`; no new syntax or focused-rule errors were introduced.

The final eight-image benchmark completed with **8 analyzed, 0 fatal failures,
and 5 complete accuracy annotations**. All eight images remain conservatively
review-required, as expected for this corpus.

## Next gate

Phase 14.4 should run the full no-regression gate: all focused and broad tests, full benchmark refresh, intermediate-event false-positive count, and AON regression measurements before publication.
