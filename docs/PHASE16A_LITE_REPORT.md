# Phase 16A-Lite — Benchmark Completion and UI Transition Gate

**Status:** COMPLETE; benchmark gate passed for transition to the results/review UX phase.

## Objective

Close the minimum evidence gap before UI work without opening an unbounded computer-vision rewrite. This phase adds human-verified ground truth for the three remaining corpus images, runs the unchanged production pipeline over all eight images, and identifies only the highest-value follow-up problems.

## Annotation work

Completed and validated these previously draft annotations:

- `2.jpg` — AOA, 6 events and 7 directed event edges.
- `4.jpeg` — AOA, 12 events and 15 directed event edges; repeated visible labels were disambiguated as `F1/F2`, `H1/H2`, and `E1`.
- `7.jpeg` — AON, 23 labeled activities (`A`–`W`), visible durations, and 36 directed dependencies.

Validation result:

```text
Annotations found: 8 | errors: 0 | warnings: 0
```

The source images were not changed. The annotations are hand-authored from the pixels; detector drafts were used only as geometry hints and were replaced rather than treated as truth.

## Full-corpus benchmark result

The production pipeline was run without changing thresholds or relationship gates.

| Image | Type | Node/event precision | Node/event recall | Relationship precision | Relationship recall | Relationship F1 |
|---|---|---:|---:|---:|---:|---:|
| `1.png` | AON | 1.0000 | 1.0000 | 1.0000 | 0.3929 | 0.5641 |
| `11.jpeg` | AON | 1.0000 | 1.0000 | 0.6000 | 0.1364 | 0.2222 |
| `2.jpg` | AOA | 0.6667 | 1.0000 | 0.0000 | 0.0000 | N/A |
| `3.jpeg` | AOA | 1.0000 | 1.0000 | 0.9231 | 0.8000 | 0.8571 |
| `4.jpeg` | AOA | 0.7143 | 0.8333 | 0.5000 | 0.4667 | 0.4828 |
| `5.jpeg` | AON | 1.0000 | 1.0000 | 0.9091 | 0.7143 | 0.8000 |
| `6.jpeg` | AOA | 1.0000 | 1.0000 | 1.0000 | 0.5714 | 0.7273 |
| `7.jpeg` | AON | 0.9545 | 0.9130 | 0.3571 | 0.1389 | 0.2000 |

Corpus execution completed with:

- 8 images discovered and analyzed.
- 0 fatal failures.
- 0 automatic successes.
- 8 `REVIEW_REQUIRED` outcomes.
- All 8 images now have `COMPLETE` accuracy annotations.

## Findings

### What is stable enough for UI work

- AON activity detection is strong on the existing references: `1.png`, `5.jpeg`, and `11.jpeg` all have activity precision and recall of `1.0`; the new Arabic AON image `7.jpeg` is close, with precision `0.9545` and recall `0.9130`.
- AOA event detection is strong on `3.jpeg` and `6.jpeg` and measurable on the new images. `4.jpeg` has enough signal to expose useful review states, although its event detector still produces extra/missed events.
- The pipeline safety behavior remains intact: every image stays in `REVIEW_REQUIRED`; no uncertain graph is promoted to authoritative CPM data.
- The benchmark now has sufficient diversity to design UI states around real evidence instead of synthetic examples.

### What should not be changed before the UI phase

- Do not lower confidence thresholds.
- Do not auto-accept the new `7.jpeg` result despite its good duration agreement; its relationship F1 is only `0.20`.
- Do not generalize the AOA strategy from `3.jpeg`/`6.jpeg` to `2.jpg` or `4.jpeg` without a targeted experiment. Their relationship F1 values are `N/A` and `0.4828`, respectively.
- Do not treat the zero mapped-arrow score on `2.jpg` as a reason to bypass review; it is a clear diagnostic target for a later AOA experiment.

## Decision: transition to Phase 17

The Phase 16A-Lite gate is passed. The project should now begin **Phase 17 — Results and Review UX**, starting with a data-backed quality summary and review-priority presentation.

The CV backlog remains explicit and bounded:

1. `2.jpg`: AOA event/arrow association and screenshot/layout masking.
2. `4.jpeg`: AOA event deduplication and extra arrow rejection.
3. `7.jpeg`: AON Arabic OCR identity association and relationship recovery.
4. `11.jpeg`: AON relationship recall without reducing precision.

These are follow-up experiments, not prerequisites for the first UI iteration.

## UI contract for the next phase

The first UI increment should consume existing result/review data and expose:

- overall status and `REVIEW_REQUIRED` reason;
- blocking, high-priority, standard, and lower-risk review counts;
- activity/event detection quality;
- OCR identity and duration quality where available;
- relationship precision/recall/F1 when benchmark data is present;
- graph validity and CPM/PERT gate state;
- explainable evidence for a selected relationship;
- a clear action to open the review center or network builder.

This contract keeps the conservative gates unchanged while making partial results useful and auditable.
