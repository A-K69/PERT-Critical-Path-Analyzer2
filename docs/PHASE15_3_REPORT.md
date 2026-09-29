# Phase 15.3 — Conservative OCR Normalization and Semantic Parsing

**Status:** IMPLEMENTED and regression-verified.

## Scope

Phase 15.3 adds a numeric-context normalization layer without overwriting raw OCR text. It handles the common OCR cases that are safe to interpret only when an existing digit is already present:

- `O` / `o` → `0`.
- `I` / `l` → `1`.
- One comma with one or two trailing digits, such as `5,17`, → decimal point.
- Three-digit comma groups such as `1,000` remain thousands separators.

Standalone activity labels such as `O` and `I` are not changed and do not become numeric candidates.

## Provenance contract

Every corrected numeric candidate retains:

- the original region `raw_text`;
- the normalized OCR string;
- correction warnings in `region.numeric_parse_warnings`;
- structured details under `region.metadata["numeric_normalization"]`;
- candidate-level `raw_ocr_text`, `normalized_ocr_text`, and `parse_warnings`.

This means normalization is a candidate-generation step, not a silent replacement of the OCR result.

## Measured AON results

The real corpus did not require any confusable correction in this run (`0` normalization corrections on `1.png`, `5.jpeg`, and `11.jpeg`), so the Phase 15.2 semantic metrics remained stable:

| Image | ID exact | Duration exact | Association exact | Normalized numeric regions |
|---|---:|---:|---:|---:|
| `1.png` | 13 | 13 | 22 | 0 |
| `5.jpeg` | 16 | 10 | 16 | 0 |
| `11.jpeg` | 4 | 7 | 16 | 0 |

Synthetic regression cases confirm that `5,O0` becomes `5.00`, `5,17` becomes `5.17`, `1,000` remains `1000`, and standalone `O` / `I` remain non-numeric.

## Relationship safety gate

The complete five-reference graph benchmark remained unchanged:

- `1.png`: precision 1.0000, recall 0.3929.
- `3.jpeg`: precision 0.9231, recall 0.8000.
- `5.jpeg`: precision 0.9091, recall 0.7143.
- `6.jpeg`: precision 1.0000, recall 0.5714.
- `11.jpeg`: precision 0.6000, recall 0.1364.

No relationship thresholds, arrow validation rules, intermediate-node safeguards, or direction gates were loosened.

## Verification

- 312 focused OCR, semantic, reconstruction, and diagnostics tests passed before the diagnostics-metric update.
- Syntax, focused lint, JSON, and diff checks passed.
- The full relationship benchmark was rerun after the final change and preserved all Phase 15.2 graph metrics.

## Next step

Phase 15.4 should improve node-local semantic candidate ranking using the new provenance fields and geometry, but only for choosing among existing OCR candidates. It must not infer IDs or durations from graph topology and must keep review-required status for unresolved ambiguity.
