# Phase 15.4 — Provenance-Aware Semantic Candidate Ranking

**Status:** IMPLEMENTED and regression-verified.

## Interruption recovery

The repository was clean after resuming. Phase 15.3 was already merged into `main` through PR #10, no PRs were open, and the post-resume smoke suite passed 220 tests. Phase 15.4 was started from the verified `origin/main` checkpoint.

## Changes

### Activity-ID alternatives

Alternative OCR IDs are now normalized with `strip().upper()` before validation and resolution. The raw OCR ID and original alternatives remain unchanged in the resolution result. This handles harmless casing/whitespace variation without inventing a new label or using graph topology.

### Duration candidates

Duration ranking now uses existing OCR provenance when it is available:

- a normalized numeric string is used for format validation;
- a corrected reading receives a bounded `-0.04` confidence adjustment;
- the evidence explicitly records `numeric_ocr_normalized(-0.04)`;
- the parsed value and raw OCR remain available;
- the existing duration-sub-crop bonus and range checks remain unchanged.

The ranking only chooses among candidates already produced by OCR. It never creates a duration or infers one from relationships.

## Measured results

Phase 15.4 preserved the Phase 15.3 OCR metrics:

| Image | ID exact | Duration exact | Association exact | Ambiguous associations |
|---|---:|---:|---:|---:|
| `1.png` | 13 | 13 | 22 | 111 |
| `5.jpeg` | 16 | 10 | 16 | 58 |
| `11.jpeg` | 4 | 7 | 16 | 19 |

The complete relationship benchmark was also unchanged:

| Image | Precision | Recall | F1 |
|---|---:|---:|---:|
| `1.png` | 1.0000 | 0.3929 | 0.5641 |
| `3.jpeg` | 0.9231 | 0.8000 | 0.8571 |
| `5.jpeg` | 0.9091 | 0.7143 | 0.8000 |
| `6.jpeg` | 1.0000 | 0.5714 | 0.7273 |
| `11.jpeg` | 0.6000 | 0.1364 | 0.2222 |

## Verification

- 314 focused semantic, OCR, region, reconstruction, and diagnostics tests passed.
- Syntax, focused lint, and diff checks passed.
- The five-reference relationship benchmark was rerun after the change.
- No interruption-related repository corruption, uncommitted changes, or open PRs were found during resume.

The complete headless suite finished with **1464 passed and 2 failed**. Both failures are the same pre-existing environment dependency mismatch in PDF export: the installed legacy `fpdf` implementation does not accept the `new_x` / `new_y` keyword arguments used by the repository's PDF renderer. No Phase 15.4 OCR or semantic test failed, and the PDF renderer was intentionally left outside this phase.

## Next step

The next logical stage is a full-corpus OCR/graph refresh followed by Phase 15.5 review calibration: measure when a semantic candidate should remain `REVIEW_REQUIRED` instead of being auto-selected, using only OCR confidence, provenance, and spatial evidence.
