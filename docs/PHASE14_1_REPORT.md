# Phase 14.1 — AOA Diagnostics

**Status:** COMPLETE. Measurement only; no production route-stitching behavior was changed in this subphase.

## Purpose

Before implementing multi-segment stitching, the detector now produces a repeatable inventory of raw Hough support between manually annotated AOA events. The diagnostics measure:

- raw line-segment count;
- logical and unresolved arrows;
- number of raw segments supporting each direct event corridor;
- corridor coverage;
- angular consistency;
- intermediate-event crossings;
- strict candidates and near-candidates for the next stitching phase.

Every reported candidate remains diagnostic only. It is not promoted into the production graph.

## Baseline inventory

| Image | Events | Raw segments | Logical arrows | Rejected arrows | Unresolved logical arrows |
|---|---:|---:|---:|---:|---:|
| `3.jpeg` | 13 | 430 | 14 | 16 | 3 |
| `6.jpeg` | 12 | 539 | 17 | 7 | 11 |

## Findings

### `3.jpeg`

- Several true direct routes have complete raw support but were not represented as a single accepted arrow, including `B→D`, `D→F`, and `G→I`.
- `G→H` has partial support and lower angular consistency, making it a near-candidate rather than a safe first-pass stitch.
- Many false direct corridors have high pixel/segment coverage only because they cross one or more event circles. The intermediate-event guard correctly marks these as unsafe.
- This confirms that the next implementation should stitch **segments**, not lower the arrow confidence gate.

### `6.jpeg`

- `B→D`, `D→F`, `F→G`, `J→K`, and `K→M` have strong direct corridor support in the raw segments.
- Several other high-coverage corridors are unsafe because they cross intermediate events; they must not be recovered as direct links.
- The diagnostic inventory exposes a substantial unresolved-arrow population, so direction recovery must remain separate from geometric route stitching.

## Evidence gates for Phase 14.2

The next subphase will start with strict gates derived from this inventory:

```text
supporting_segments >= 2
coverage >= 0.35
angular_consistency >= 0.65
intermediate_event_crossing == false
```

Near-candidates with coverage/angle just below these values will be retained for review diagnostics, not automatically accepted. The exact threshold may be tightened if any precision regression appears.

## Design decision

Phase 14 will remain staged:

1. **14.1 Diagnostics** — completed here.
2. **14.2 Multi-segment stitching** — combine only coherent raw segments into visual route candidates.
3. **14.3 Direction recovery** — infer missing-arrowhead direction only when independent layout/topology evidence exists; otherwise route to review.
4. **14.4 Quality gate** — require no precision decline and no new intermediate-crossing false positives.

## Artifacts

- `docs/PHASE14_AOA_DIAGNOSTICS.md`
- `docs/PHASE14_AOA_DIAGNOSTICS.json`
- `pert_analyzer/benchmark/aoa_diagnostics.py`

The next code change will be limited to Phase 14.2 and will be measured against the Phase 13 precision baseline before any merge.
