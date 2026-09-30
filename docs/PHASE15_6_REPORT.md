# Phase 15.6 — Reviewer Outcome Measurement

**Status:** IMPLEMENTED; awaiting production reviewer-session data.

## Objective

Measure whether the Phase 15.5 calibration tiers improve review triage using actual reviewer outcomes. This phase is measurement-only: it does not change review decisions, confidence thresholds, CPM blocking, relationship gates, or graph construction.

## Data audit result

No persisted production reviewer-session JSON files were found in the repository or the active workspace. The repository contains:

- `ReviewSession` serialization and audit decisions in `human_review.py`.
- Evaluation-only gold-correction helpers used by reference tests.
- Phase 15.5 calibration baseline diagnostics.
- No exported sessions containing real reviewer decisions.

Accordingly, the report intentionally records:

- `production_outcome_data_available: false`
- `sessions: 0`
- `items: 0`
- all rates as `null`, not zero

A null rate means **there is no sample**, not that reviewers achieved zero performance.

## Implemented metrics

`pert_analyzer.benchmark.review_outcomes` consumes one or more JSON files exported through `ReviewSession.to_dict()` and reports:

- number of sessions and sessions containing decisions;
- total, resolved, pending, accepted, corrected, and rejected items;
- resolution rate by calibration tier;
- correction rate by calibration tier;
- unresolved blocking-review rate;
- mean confidence by tier and review item type;
- activity, duration, and dependency breakdowns;
- explicit limitations when no data or no tier metadata is available.

The analyzer recognizes the Phase 15.5 tier from review evidence metadata. Pre-15.5 sessions are grouped under `UNCLASSIFIED_PRE_15_5` instead of being assigned a tier retroactively.

## Why evaluation fixtures are excluded

The gold helper in `tests/helpers/reference_gold.py` creates **evaluation-only** corrections from canonical ground truth. Those actions are not human reviewer behavior and would inflate correction and resolution rates if counted as real outcomes. Phase 15.6 therefore accepts only explicitly supplied session exports and does not scan or reinterpret test fixtures.

## How to measure actual sessions

Export a session using the existing serialization contract:

```python
from pathlib import Path
import json

Path("review_session.json").write_text(
    json.dumps(session.to_dict(), indent=2) + "\n",
    encoding="utf-8",
)
```

Then run:

```bash
PYTHONPATH=. python -m pert_analyzer.benchmark.review_outcomes \
  review_session.json \
  --json docs/PHASE15_6_REVIEW_OUTCOMES.json \
  --markdown docs/PHASE15_6_REVIEW_OUTCOMES.md
```

Multiple session files may be passed in one command. The tool is read-only with respect to the sessions and only writes the requested report artifacts.

## Quality gate

- 41 focused tests passed, including outcome aggregation, tier grouping, no-data behavior, review-session contracts, and reference-review integration.
- Syntax, focused lint, JSON, and diff checks passed.
- No production behavior was changed.
- No auto-accept path was introduced.
- No threshold or graph gate was weakened.

The complete headless suite finished with **1468 passed and 2 failed**. Both failures are the existing unrelated PDF compatibility issue: the installed legacy `fpdf` package rejects the `new_x` / `new_y` arguments used by the repository PDF renderer. No Phase 15.6 test or review-flow test failed.

## Current conclusion

Phase 15.5 has produced a measurable triage structure, but **calibration quality cannot yet be judged empirically** because there are no actual reviewer outcomes. The correct next operational step is to collect/export real sessions, preserving the tier metadata and decision audit trail. Once a meaningful sample exists, Phase 15.6 can calculate acceptance, correction, rejection, unresolved-blocker, and false-review rates.

## Next step

Collect a representative batch of real review sessions across AON and AOA images. The first analysis should remain measurement-only and report sample sizes and confidence intervals before considering any calibration threshold change.
