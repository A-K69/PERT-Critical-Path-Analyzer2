# Phase 14.2 — Multi-Segment AOA Stitching

**Status:** IMPLEMENTED and regression-verified. The real-image baseline is unchanged because the current `3.jpeg` and `6.jpeg` cases are already handled by Phase 13's direct pixel-supported recovery; the new chain path is exercised by synthetic coverage and remains available for more fragmented diagonal cases.

## Implementation

The AOA recovery pass now accepts filtered Hough segments and can search for a bounded chain of up to four segments when direct corridor support is insufficient. A chain is eligible only when:

- it begins near the source event boundary and ends near the target boundary;
- adjacent segments are within a small endpoint gap;
- neighboring segment angles differ by at most 22 degrees;
- every segment has minimum length and line confidence;
- the total chain length is not excessively longer than the direct route;
- no segment crosses an unrelated event circle;
- the recovered route remains explicit in provenance as a multi-segment stitch.

The chain path does not lower the arrowhead threshold and does not promote a route whose intermediate-event check fails.

## Real-image gate

The Phase 13 precision baseline was preserved:

| Image | Precision | Recall | F1 |
|---|---:|---:|---:|
| `3.jpeg` | 0.9231 | 0.8000 | 0.8571 |
| `6.jpeg` | 1.0000 | 0.5714 | 0.7273 |

No new false positive appeared, and no precision regression occurred. The unchanged metrics are expected: the current corpus exposes strong direct corridors, while the new chain branch is intended for future diagonal/gap cases that are not yet represented as a production miss in these two images.

## Verification

- **206 tests passed** across arrow detection, reconstruction, diagnostics, and benchmark annotation coverage.
- Syntax, focused lint, and diff checks passed.
- Phase 14.1 diagnostics remain available as the route-selection evidence source.

## Next gate

Phase 14.3 should add direction recovery for chains with missing arrowheads. It must keep a route in review unless direction is supported by an observed neighboring arrow, a consistent layout/topology orientation, or another independent visual signal.
