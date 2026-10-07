# Results UI Architecture Audit

## Executive finding

The project does **not** contain two independent Results pages. It contains one `ResultsPage` with two materially different render states:

1. **Preliminary / blocked state** — normally reached by the image-analysis workflow while review items remain unresolved.
2. **Full analytical dashboard** — reached by the manual Network Builder, which creates an already-applied, valid, CPM-ready candidate.

This state split is technically intentional for safety, but the visual distinction is currently too large. From a user perspective it looks like two pages, and the image workflow appears unfinished compared with the Board/Network workflow.

## Evidence in the code

### Image-analysis route

`MainWindow._on_analysis_completed()` stores the workflow in `GuiSession` and sends image results through the review/validation flow. Until review decisions are applied, `ResultsPage.refresh()` receives a session for which `describe_ready()` returns `REVIEW_REQUIRED`.

The page then renders `_show_not_ready()` and only shows:

- a not-ready message;
- the preliminary detected-metrics card;
- review progress;
- navigation buttons to Review and Validation.

The full `Overview`, `Network`, `Activities`, `Critical Paths`, and `PERT` tabs are not shown in this state because `gui.results.data.extract()` deliberately returns no authoritative `ResultsData` until the readiness gate passes.

### Network Builder route

`MainWindow._on_manual_analyze()` calls `builder_model.create_candidate()`, assigns the candidate directly to the session, sets `RESULTS_AVAILABLE`, and navigates to Results. The manual candidate already carries:

- a graph;
- validation state;
- a runnable CPM gate;
- a CPM result.

Consequently, `describe_ready()` passes and the same `ResultsPage` renders the complete dashboard with KPI cards, network canvas, activity table, critical paths, and PERT.

## Why the current screenshot looks wrong

The current image-flow screenshot is not the analytical dashboard. It is the **safe pre-authoritative state**. It intentionally does not present detected data as final CPM data. However, the current preliminary state is too sparse and too visually different from the full dashboard:

- the visual hierarchy is centered around a large card rather than the dashboard shell;
- the rich tabs are absent;
- there is no visual network preview;
- there is no side-by-side evidence/review context;
- the user sees counts and text but not the diagram intelligence already recovered by CV/OCR;
- the image route therefore feels like a dead-end even though the safety gate is working correctly.

This is a UX architecture problem, not evidence that the review gate should be removed.

## Required design direction

Use **one Results shell with two explicit data modes**, rather than two unrelated visual pages:

### Mode A — Detected / Review Preview

For image-derived data before review/validation:

- keep a prominent `PRELIMINARY` and `REVIEW REQUIRED` status;
- show the recovered network preview using detected relationships, clearly marked as non-authoritative;
- show activity, dependency, and duration review queues;
- show confidence/priority indicators and evidence provenance;
- allow direct actions: `Continue Review`, `Open Validation`, `View Network`, `Compare after correction`;
- never show preliminary ES/EF/LS/LF, floats, critical paths, or project duration as authoritative CPM values;
- if a preview metric is detected but not computed by CPM, label it `Detected`, `Estimated`, or `Unavailable`, not `Final`.

### Mode B — Reviewed / Authoritative Dashboard

For both image and manual-builder workflows after the readiness gate passes:

- use the same KPI header and status banner;
- show authoritative CPM and PERT data;
- show the reviewed network, activities, critical paths, and exports;
- show provenance: source image or `Manual Network Builder`, diagram type, review state, and calculation source;
- preserve the current rich tabs as the baseline because this is the stronger existing design.

## Recommended visual architecture

```text
ResultsShell
├── Context header
│   ├── source / entry mode badge
│   ├── trust status badge
│   ├── review progress
│   └── primary next action
├── KPI / evidence strip
│   ├── activities
│   ├── dependencies
│   ├── review queue
│   ├── graph status
│   └── CPM readiness or authoritative duration
├── Main workspace
│   ├── Overview
│   ├── Network / Detected Preview
│   ├── Activities
│   ├── Critical Paths
│   └── PERT
└── Audit drawer / details
    ├── provenance
    ├── category review breakdown
    ├── calibration priority counts
    └── validation notes
```

The shell should remain stable between modes. Only the trust banner, available metrics, tab state, and action buttons should change.

## Important backend/UI contract

Do **not** make the UI recompute CPM. The current rule remains correct:

> Backend CPM/PERT results are authoritative. The UI may display them, but must never invent ES/EF/LS/LF, float, critical paths, or project duration.

To support a rich image preview safely, add a separate read-only preview snapshot from the existing workflow reconstruction. It must be visibly typed as preliminary and must not reuse `ResultsData` fields that imply authoritative CPM analysis.

Recommended separation:

- `ResultsData` — authoritative reviewed graph + CPM snapshot.
- `ResultsPreviewData` — detected/reconstructed graph and review evidence, with no CPM math fields.

## Proposed implementation phases

### Phase 17.3A — Unified Results shell

- create a stable header and mode/status contract shared by both routes;
- add an explicit `entry_mode`: `IMAGE_ANALYSIS` or `NETWORK_BUILDER`;
- normalize provenance labels;
- make the full dashboard and preliminary state visually consistent;
- preserve all readiness gates.

### Phase 17.3B — Safe image preview workspace

- render detected activities and relationships in a dedicated preview canvas;
- show confidence and review priority overlays;
- make uncertain relationships visually distinct;
- add direct navigation from a node/edge to the matching Review Center item;
- do not display authoritative CPM fields before readiness.

### Phase 17.3C — Dashboard information design

- improve KPI cards and iconography;
- turn long text summaries into structured cards;
- add responsive layouts for smaller windows;
- add legends, tooltips, hover states, and selection feedback;
- preserve Arabic/RTL behavior.

### Phase 17.3D — Final visual validation

- render screenshots for both entry paths;
- compare image-flow preview and Board Network dashboard side by side;
- add GUI acceptance tests for both modes;
- verify that no preliminary state is mislabeled as final.

## Decision

Do not continue with isolated cosmetic changes to the current preliminary card. The next implementation should be **Phase 17.3A: Unified Results Shell**, followed by a safe image preview workspace. This resolves the real problem: one consistent, modern Results experience with explicit trust modes, instead of a rich Board dashboard and a separate-looking image fallback screen.
