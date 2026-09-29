# Phase 15.2 — OCR Deduplication and Duration Propagation

**Status:** IMPLEMENTED — focused verification complete.

## Changes

1. Replaced exact-text-only merge behavior with conservative overlap-aware deduplication.
2. Prefer node-region OCR over full-image OCR for overlapping readings.
3. Preserve discarded readings in `region.metadata["ocr_dedup"]` as alternate readings with confidence and source provenance.
4. Keep ID and numeric-duration readings separate even when OCR boxes overlap.
5. Re-run numeric extraction after merged node OCR so parsed durations are available to semantic reconstruction.

The deduplication guard intentionally does not use center proximity alone: activity IDs and durations are close by design but represent different semantic fields.

## Measured effect

| Image | Baseline regions | Phase 15.2 regions | ID exact baseline → Phase 15.2 | Duration exact baseline → Phase 15.2 | Association exact baseline → Phase 15.2 |
|---|---:|---:|---:|---:|---:|
| `1.png` | 395 | **204** | 13 → **13** | 0 → **13** | 22 → **22** |
| `5.jpeg` | 146 | **105** | 16 → **16** | 0 → **10** | 16 → **16** |
| `11.jpeg` | 86 | **65** | 4 → **4** | 4 → **7** | 16 → **16** |

Ambiguous association counts also fell from 228 to 111 on `1.png`, 70 to 58 on `5.jpeg`, and 29 to 19 on `11.jpeg`.

## Quality gate

- No measured ID exact-match regression.
- No measured association exact-match regression.
- Duration exact matches increased on all three AON references.
- Direct execution of the Phase 14 implementation in an isolated worktree
  produced the same relationship metrics on `5.jpeg` (`precision=0.9091`,
  `recall=0.7143`) and `11.jpeg` (`precision=0.6000`, `recall=0.1364`).
- The AOA relationship metrics remained unchanged: `3.jpeg` precision
  `0.9231` / recall `0.8000`; `6.jpeg` precision `1.0000` / recall `0.5714`.
- The graph/topology gates remain unchanged; OCR still cannot invent a relationship without geometric evidence.

## Verification

- 364 focused OCR, semantic, pipeline, reconstruction, and graph tests passed;
  one PDF export test failed on the pre-existing `fpdf` API mismatch
  (`new_x` unsupported).
- Added overlap-conflict regression coverage for alternate-reading provenance.
- Syntax and focused lint checks passed for the changed OCR and test modules.

## Next step

Phase 15.3 should add safe normalization for IDs and durations, using alternate readings as candidates rather than overwriting raw OCR text. It must preserve the current precision and association gains.
