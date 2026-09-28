# Phase 10 — Labeled AON Expansion and Visual Shaft Evidence

**Status:** COMPLETE — first conservative AON evidence improvement implemented and measured.

## Scope

1. Promoted `tests/test_data/ground_truth/5.json` from detector-seeded `UNCERTAIN` draft to manually verified `COMPLETE` ground truth.
2. Kept the benchmark honest: node labels, durations, and 14 visible activity-to-activity arrows were read from the image; external `Start`/`End` terminals were not fabricated as activities.
3. Added a bounded `shaft_visual_support` evidence factor to `ValidatedDependencyBuilder`.

## Production change

`pert_analyzer/cv/validated_dependency.py` now consumes the arrow detector's pixel-derived:

- `line_confidence`;
- `shaft_continuity.length`;
- the number of merged source segments.

These are combined into a value in `[0, 1]` and added as a maximum `0.08 * support` bonus to the existing geometry score. Boundary contact, direction consistency, pairing, and the existing HIGH/MEDIUM/LOW gates remain authoritative. No confidence threshold was lowered, and no weak candidate bypasses review.

The value is preserved in `DependencyEvidence`, raw provenance (`raw_evidence.visual`), and debug output for explainability.

## Real-image measurement: `5.jpeg`

Run with OpenCV, Tesseract English/Arabic OCR, and the production benchmark runner:

| Metric | Result |
|---|---:|
| Annotation | COMPLETE |
| Activities | 17 expected / 17 detected |
| Activity precision / recall | 1.0000 / 1.0000 |
| ID accuracy | 0.9412 |
| Duration exact-match accuracy | 0.5882 |
| Duration MAE | 1.7647 |
| Dependencies | 14 expected / 11 detected |
| Dependency precision / recall / F1 | 0.9091 / 0.7143 / 0.8000 |
| Direction accuracy | 1.0000 |
| Final pipeline status | REVIEW_REQUIRED |
| CPM gate | BLOCKED_REVIEW |

The result is intentionally still review-gated. The benchmark shows measurable relationship recovery without converting uncertain edges into authoritative CPM input.

## Verification

- Ground-truth validator: **0 errors**, one pre-existing warning for missing duration in `10.jpeg`.
- Targeted dependency, endpoint-invariance, and ground-truth benchmark tests: **55 passed**.
- Full suite: **1,449 passed, 2 failed**. The two failures are unrelated PDF-environment failures: the sandbox imports system `fpdf 1.7.2` ahead of declared `fpdf2 2.8.7`, so `FPDF.cell(new_x=...)` is unavailable. The source change does not touch PDF code.
- OCR-enabled real-image run completed without warnings.

## Next controlled step

Repeat the same measurement on the two complete AON references (`1.png`, `5.jpeg`) after any subsequent scoring change. Add another complete AON label only after manual pixel verification. Do not generalize to AOA or lower gates until dependency precision and direction accuracy remain stable across the expanded AON set.
