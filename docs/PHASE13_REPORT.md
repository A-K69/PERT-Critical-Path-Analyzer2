# Phase 13 — Conservative AOA Fragmented-Route Recovery

**Status:** COMPLETE — high-confidence pixel-supported fragmented routes are recovered without relaxing the intermediate-event safeguard or lowering existing precision.

## Implementation

The AOA detector now performs a second, narrow recovery pass after ordinary arrow validation:

1. Enumerate direct pairs of detected event circles.
2. Reject any candidate whose centerline crosses an unrelated event circle.
3. Sample the grayscale image only between the two event boundaries.
4. Require both high dark-pixel support and high sample coverage.
5. Skip pairs already represented by an accepted route.
6. Recover the route only in the observed left-to-right event layout, with explicit provenance that the arrowhead was not observed.

The recovered arrow is not treated as an unconstrained confidence promotion. It carries `recovered_route`, route support, route coverage, and a recovery reason in its evidence payload.

## Measured AOA results

| Image | Metric | Phase 12 | Phase 13 |
|---|---|---:|---:|
| `3.jpeg` | Directed precision | 0.9167 | **0.9231** |
| `3.jpeg` | Directed recall | 0.7333 | **0.8000** |
| `3.jpeg` | Directed F1 | 0.8148 | **0.8571** |
| `3.jpeg` | Direction accuracy | 1.0000 | 1.0000 |
| `6.jpeg` | Directed precision | 1.0000 | **1.0000** |
| `6.jpeg` | Directed recall | 0.4286 | **0.5714** |
| `6.jpeg` | Directed F1 | 0.6000 | **0.7273** |
| `6.jpeg` | Direction accuracy | 1.0000 | 1.0000 |

The precision guard held: `3.jpeg` improved from 0.9167 to 0.9231 and `6.jpeg` remained at 1.0000. The intermediate-event crossing safeguard remains active for both ordinary and recovered routes.

## AON regression check

The recovery is enabled only when the detector is in AOA context. The complete AON references were re-measured and the existing AON path remained unchanged:

- `1.png`: dependency precision 1.0000, recall 0.3929.
- `5.jpeg`: dependency precision 0.9091, recall 0.7143.
- `11.jpeg`: dependency precision 0.6000, recall 0.1364.

## Verification

- Focused detector/reconstruction/benchmark tests: **202 passed**.
- Broader Phase 11/12 regression suite: **269 passed**.
- Static syntax, lint, and diff checks: passed.
- Ground-truth validation: **8 annotations, 0 errors, 0 warnings**.
- Full benchmark refresh: **8 images analyzed, 0 fatal failures, 5 complete
  accuracy annotations**; all eight remain conservatively review-required.

## Remaining limitation

Some diagonal and visually interrupted routes remain unresolved because their pixel support is below the strict route threshold. The next improvement should address multi-segment diagonal stitching and local arrowhead orientation, not lower the current recovery threshold.
