# Phase 15.5 — Review Calibration

**Status:** IMPLEMENTED and regression-verified.

## Objective

Calibrate review triage so human reviewers can distinguish blocking defects, high-priority uncertainty, standard review, and strong visual evidence. This phase deliberately does **not** auto-accept any item, alter `REVIEW_REQUIRED` semantics, lower confidence gates, or bypass CPM validation.

## Baseline finding

The existing review session mixed materially different cases under the same generic review label. For example, some confirmed semantic IDs with strong OCR confidence were placed beside missing durations, inferred IDs, and uncertain arrows. The baseline therefore produced a large review queue without exposing its relative urgency.

Representative baseline counts:

| Image | Activity reviews | Duration reviews | Dependency reviews | Ambiguities |
|---|---:|---:|---:|---:|
| `1.png` | 2 | 4 | 23 | 47 |
| `3.jpeg` | 4 | 7 | 0 | 2 |
| `5.jpeg` | 3 | 3 | 30 | 56 |
| `6.jpeg` | 3 | 3 | 0 | 1 |
| `11.jpeg` | 7 | 4 | 14 | 39 |

## Calibration policy

### Activity identity

- `BLOCKING_REVIEW`: inferred IDs or semantic status already marked `REVIEW_REQUIRED`.
- `HIGH_PRIORITY_REVIEW`: confidence below `0.50`.
- `STANDARD_REVIEW`: confidence from `0.50` through below `0.70`.
- `LOW_RISK_REVIEW`: confirmed-looking evidence at or above `0.70`, still requiring review when the existing pipeline requested it.

### Duration

- `BLOCKING_REVIEW`: missing or invalid duration (`<= 0`); CPM remains blocked.
- `HIGH_PRIORITY_REVIEW`: valid-looking duration evidence below `0.40` confidence.
- `STANDARD_REVIEW`: remaining duration review cases.

### Dependencies

- `HIGH_RISK_REVIEW`: confidence below `0.40`.
- `STANDARD_REVIEW`: confidence from `0.40` through below `0.75`.
- `STRONG_EVIDENCE_REVIEW`: confidence at or above `0.75`, retained in review because direction and topology must still be human-confirmed.

All review evidence now carries a `review_calibration` metadata object with the tier, confidence, reason codes, and non-bypass guarantees. The session also exposes aggregate tier counts for UI and audit consumers. Empty-evidence items are included in the aggregate summary without fabricating OCR provenance.

## Measured calibration output

| Image | Blocking | High priority | Standard | Low risk | Strong evidence | High risk |
|---|---:|---:|---:|---:|---:|---:|
| `1.png` | 2 | 2 | 19 | 2 | 2 | 2 |
| `3.jpeg` | 10 | 1 | 0 | 0 | 0 | 0 |
| `5.jpeg` | 3 | 1 | 22 | 2 | 0 | 8 |
| `6.jpeg` | 5 | 1 | 0 | 0 | 0 | 0 |
| `11.jpeg` | 8 | 1 | 13 | 1 | 1 | 1 |

## Relationship quality gate

The complete five-reference directed relationship metrics are unchanged:

| Image | Precision | Recall | F1 |
|---|---:|---:|---:|
| `1.png` | 1.0000 | 0.3929 | 0.5641 |
| `3.jpeg` | 0.9231 | 0.8000 | 0.8571 |
| `5.jpeg` | 0.9091 | 0.7143 | 0.8000 |
| `6.jpeg` | 1.0000 | 0.5714 | 0.7273 |
| `11.jpeg` | 0.6000 | 0.1364 | 0.2222 |

## Verification

- 60 focused review, human-review, semantic, integration, and diagnostics tests passed after the empty-evidence summary fix.
- Diagnostic renderer test added and passed.
- Syntax, focused lint, and diff checks passed.
- Real-image calibration diagnostics generated for all five complete references.
- No automatic acceptance was introduced.
- CPM and relationship gates remain unchanged.

The complete headless suite finished with **1466 passed and 2 failed**. The two failures are the same unrelated PDF compatibility issue documented in the previous phase: the installed legacy `fpdf` package rejects the `new_x` / `new_y` arguments used by the repository renderer.

## Known environment issue

The repository-wide suite previously recorded 1464 passed and 2 unrelated PDF failures caused by the installed legacy `fpdf` package rejecting `new_x` / `new_y`. Phase 15.5 does not modify PDF export.

## Next step

Phase 15.6 should use reviewer outcomes, when available, to evaluate calibration quality: acceptance rate by tier, correction rate, false-review rate, and unresolved-blocker rate. It should remain measurement-first before any threshold changes.
