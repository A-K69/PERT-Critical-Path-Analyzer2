# Phase 17.3A — Unified Results Shell

## Status

**Implemented and verified.**

## Objective

Unify the visual entry context for the two Results workflows without weakening review or CPM safety gates:

- image analysis;
- manual Network Builder.

## Implementation

### Explicit entry mode

`GuiSession.entry_mode` now identifies the source workflow:

- `IMAGE_ANALYSIS` when an image is selected;
- `NETWORK_BUILDER` when a manual graph is sent from Network Builder;
- `NONE` before either workflow starts.

The Results page also retains a defensive fallback for older/fake sessions that do not provide this field.

### Shared Results context header

Both preliminary and authoritative Results states now render the same context surface with:

- entry mode;
- normalized source label;
- trust state;
- review progress.

Examples:

```text
ENTRY: IMAGE ANALYSIS   Source: diagram-7.jpeg   TRUST: PRELIMINARY   Review: 0/4 resolved
ENTRY: NETWORK BUILDER  Source: Manual Network Builder  TRUST: AUTHORITATIVE
```

### Safety contract preserved

The change is presentation and provenance only:

- preliminary image data remains visibly non-authoritative;
- CPM remains blocked while required review/validation is incomplete;
- the UI does not compute ES, EF, LS, LF, float, critical paths, or project duration;
- authoritative results continue to come only from the backend candidate/CPM result;
- no confidence thresholds or automatic acceptance behavior changed.

## Tests

- Focused Results/Recovery tests: **29 passed**.
- Full GUI suite: **318 passed**.
- Python compilation checks passed.
- `git diff --check` passed.

## Next phase

Phase 17.3B should add a safe detected-network preview workspace for image analysis. It must use a separate preliminary snapshot and distinguish uncertain nodes/edges visually without reusing authoritative CPM fields.
