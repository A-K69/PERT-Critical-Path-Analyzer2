# Phase 15.1 — OCR Baseline and Error Diagnostics

**Status:** COMPLETE — measurement only. No production OCR behavior was changed.

## Scope

The diagnostic runner executes the existing end-to-end pipeline and classifies OCR failures into:

- **Recognition / semantic error:** text is inside an annotated activity region, but the expected ID and duration are not recovered.
- **Localization error:** text appears only in an expanded neighborhood rather than inside the expected node box.
- **Association error:** text is inside the correct node region, but the best geometric association maps to another detected node.
- **Duplicate detections:** multiple OCR regions are produced for one node, typically from full-image OCR plus region OCR.
- **Matched:** at least one expected semantic field and the association are recovered.

The report intentionally measures the current system; it does not tune thresholds or alter graph reconstruction.

## Baseline results

| Image | Type | Expected items | OCR regions | Numeric candidates | Ambiguous associations | Unmatched regions | ID exact | Duration exact | Association exact |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `1.png` | AON | 22 | 395 | 43 | 228 | 64 | 13 | 0 | 22 |
| `3.jpeg` | AOA | 0 | 59 | 8 | 13 | 59 | — | — | — |
| `5.jpeg` | AON | 17 | 146 | 27 | 70 | 67 | 16 | 0 | 16 |
| `6.jpeg` | AOA | 0 | 85 | 31 | 15 | 85 | — | — | — |
| `11.jpeg` | AON | 21 | 86 | 19 | 29 | 10 | 4 | 4 | 16 |

### Findings

1. **Duplicate OCR regions are the largest structural problem.** `1.png` produces 395 regions for 22 nodes and `5.jpeg` produces 146 for 17 nodes. This is consistent with merging full-image OCR and node-region OCR without a strong deduplication key.
2. **AON geometry association is stronger than semantic extraction.** Association exact matches are 22/22 on `1.png`, 16/17 on `5.jpeg`, and 16/21 on `11.jpeg`; therefore the first production improvement should not loosen spatial association thresholds.
3. **Duration parsing/propagation is a measurable bottleneck.** Exact duration matches are 0 on `1.png` and `5.jpeg`, even where visible OCR strings include values such as `2.00`, `5.17`, and `28.00`. This indicates a parsing or region-to-duration propagation gap, not only character recognition noise.
4. **`11.jpeg` is primarily a recognition/localization case.** It has 11 recognition/semantic errors and 3 localization errors; only 4/21 IDs and 4/21 durations are exact. The parallel branch labels are particularly difficult for the current OCR configuration.
5. **AOA requires a separate text association benchmark.** The current AOA ground truth describes event-to-event arrows, not activity text regions. Accordingly, the baseline records OCR volume and unmatched/ambiguous rates for `3.jpeg` and `6.jpeg` but does not pretend that event annotations are activity-label truth.
6. **Ambiguity is inflated by candidate pooling.** The current combined associator evaluates node and arrow candidates together; this is useful for review visibility but should not be treated as a semantic error by itself.

## Recommended Phase 15.2 priorities

1. Deduplicate full-image and node-region OCR using normalized text, spatial overlap, source representation, and confidence.
2. Preserve the highest-quality region while retaining alternate readings as provenance instead of counting them as independent labels.
3. Add a region-local duration parser that records the source OCR string, parsed value, parse warnings, and expected numeric context.
4. Keep the current association geometry and precision gates unchanged while measuring the effect of deduplication.
5. Add AOA arrow-crop OCR separately from AON node-crop OCR; do not compare AOA text metrics to AON activity-ID metrics.

## Verification

- Phase 15.1 diagnostic JSON and Markdown artifacts were generated for five complete annotated/reference images.
- The new diagnostic helper tests cover center-based localization, padding behavior, and taxonomy rendering.
- The next implementation stage must be accepted only if ID/duration precision and graph precision do not decrease.
