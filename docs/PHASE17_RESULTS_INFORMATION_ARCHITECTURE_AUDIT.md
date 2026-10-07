# Phase 17 — Results Information Architecture Audit

## Purpose

This audit pauses implementation and maps the complete Results experience before redesigning it. The goal is not to style one screenshot; it is to define one coherent analytical product across:

- Image Analysis entry.
- Network Builder entry.
- Overview.
- Network.
- Activities.
- Critical Paths.
- PERT.
- Review, Validation, and shared navigation.

## Executive finding

The project already contains a strong amount of analytical data. The current problem is primarily **information architecture and presentation**, not absence of data.

The Results page currently exposes five analytical tabs, but the user must mentally assemble the project story across them:

1. **Overview** — executive KPIs, embedded network, critical paths, embedded activities.
2. **Network** — graph canvas, CPM/PERT metric switch, zoom, path focus, node selection.
3. **Activities** — full schedule table and activity detail panel.
4. **Critical Paths** — path list and selected path sequence.
5. **PERT** — three-point estimates, expected duration, variance, standard deviation, probability target, and PERT paths.

The redesign should therefore create a single **Results Control Center** with shared context, a clear hierarchy, cross-tab selection, and one consistent visual language.

## Verified data for image 1

The approved image-1 design reference is `tests/test_data/Imag PERT/1.png`.

Its verified ground truth contains:

- 22 activities.
- 28 unique dependencies.
- Project duration: 54 days.
- 16 zero-float critical paths.
- AON topology with the exact node positions and relationships from the image.

The design mockup uses this data because it is clear and representative, rather than the uncertain preliminary output from image 7.

## Complete Results data inventory

### Shared Results context

Visible in both entry routes:

- Entry mode: Image Analysis or Network Builder.
- Source image or manual builder provenance.
- Trust state: Preliminary, Not Authoritative, Reviewed/CPM Pending, or Authoritative.
- Review resolution progress.
- Diagram type.
- Backend/validation provenance.

This context must remain visible when switching tabs.

### Overview tab

Current data:

- Activities count.
- Dependencies count.
- Project duration.
- Critical path count.
- Critical activity count.
- Narrative network summary.
- Embedded interactive network.
- Critical path list.
- Embedded activities table.

Design role:

> Executive answer to “What is the state of this project?”

Recommended future layout:

- KPI strip first.
- Trust/validation banner second.
- One primary network visualization.
- Critical-path summary beside or below the network.
- Activity risk/attention summary.
- Avoid duplicating a second full network and a second full table unless the user explicitly expands them.

### Network tab

Current data and interaction:

- Activity ID in each node.
- Duration or PERT expected time.
- Total float.
- Critical status.
- Directional dependency arrows.
- Critical-edge styling.
- Path highlight.
- Node selection.
- Fit to view.
- Reset zoom.
- Zoom in/out.
- Clear highlight.
- Focus critical path.
- CPM/PERT metric mode.
- Tooltips with activity ID, metric, and float.

Design role:

> Spatial explanation of how work flows and where the critical structure is.

Recommended future layout:

- Preserve graph geometry from the reviewed graph/image where meaningful.
- Use a larger canvas with intentional spacing and orthogonal or clean routed edges.
- Use node cards with clear hierarchy: ID, name, duration/expected time, float, status.
- Use a persistent inspector panel for the selected node/edge.
- Keep CPM/PERT mode visible as a metric lens, not as a different graph.
- Add a graph legend and “backend values” indicator.

### Activities tab

Current table columns:

- ID.
- Duration.
- ES — Early Start.
- EF — Early Finish.
- LS — Late Start.
- LF — Late Finish.
- Total Float.
- Free Float.
- Critical.
- Predecessors.
- Successors.

Current interaction:

- Numeric sorting.
- Single-row selection.
- Read-only table.
- Activity detail panel.
- Cross-selection with Network.

Design role:

> Exact schedule inspection and auditability.

Recommended future layout:

- Replace the dense first impression with a filterable, sortable data grid.
- Add column groups: Identity, Timing, Slack, Relationships.
- Pin critical rows or add a critical-only filter.
- Keep the detail inspector synchronized with Network selection.
- Show “Unavailable” rather than inventing missing values.

### Critical Paths tab

Current data and interaction:

- Number of critical paths.
- Project duration shared by paths.
- Master list of paths.
- Selected path number.
- Selected path duration.
- Activity sequence.
- Activity count.
- Selection propagated to the Network canvas.

Design role:

> Explain alternative zero-float routes, not merely list them.

Recommended future layout:

- Show path cards with path number, duration, activity count, and distinguishing branch.
- Provide a compact path comparison view.
- Make selected path highlight the same path in Network.
- Add branch-point explanation for projects such as image 1, where multiple equal-duration routes exist.

### PERT tab

Current input data:

- Activity ID.
- Optimistic estimate O.
- Most-likely estimate M.
- Pessimistic estimate P.

Current result data:

- Expected project duration.
- Project variance.
- Project standard deviation.
- Completion probability for a target.
- Per-activity expected time.
- Per-activity variance.
- Per-activity standard deviation.
- Per-activity critical status.
- PERT critical paths.

Current safety behavior:

- Backend PertEngine determines status.
- Missing/invalid estimates block PERT.
- UI never computes expected time, variance, or standard deviation.
- Previous PERT results are cleared when estimates change.

Design role:

> Show uncertainty and confidence around the deterministic CPM schedule.

Recommended future layout:

- Separate “Estimate input” from “PERT result”.
- Make status state prominent: missing, invalid, ready, or calculated.
- Use a probability card with target and result together.
- Add visual comparison between deterministic duration and expected PERT duration.
- Keep estimates editable only in the intended PERT workspace.

## Authoritative data boundaries

The Results redesign must retain these rules:

| Data | Authoritative source | UI behavior |
|---|---|---|
| Activity duration | Reviewed GraphModel | Display verbatim |
| ES/EF/LS/LF | Backend CPM ActivityAnalysis | Display verbatim |
| Total/free float | Backend CPM ActivityAnalysis | Display verbatim |
| Critical status | Backend CPM result | Display verbatim |
| Critical paths | Backend CPM result | Display verbatim |
| Project duration | Backend CPM result | Display verbatim |
| O/M/P estimates | Session/GraphModel estimate fields | Edit only in PERT workspace |
| Expected time/variance/std dev | Backend PertResult | Display verbatim |
| Review status | ReviewSession | Display and link to review |
| Graph validation | Validation result | Display as gate/status |
| Preliminary reconstruction | ReviewSession.reconstruction | Never label authoritative |

The UI must not calculate or silently normalize schedule values.

## Current cross-tab interaction contract

Already present and worth preserving:

- Critical path selection highlights the Network canvas.
- Network node selection opens/selects the Activities tab.
- Overview network selection navigates to Network.
- Overview activity selection synchronizes Network selection.
- Results and Review/Validation navigation are connected through explicit signals.

The redesign should expand this into a unified selection model rather than replace it with isolated tabs.

## Cross-page design system requirements

The user’s wider goal includes redesigning all pages, so Results must not introduce a visual language that conflicts with them.

### Header and navigation

Current shared shell:

- Header bar.
- Sidebar navigation.
- Workflow indicator: Analyze → Understand → Review → Validate → Results.
- Language toggle.
- Version/status information.

Future direction:

- Replace text glyph icons with a consistent icon set.
- Keep navigation labels and status indicators aligned across all pages.
- Use the same selected, hover, disabled, warning, and error states.
- Support RTL layout without icon or order confusion.

### Scroll behavior

Current behavior is distributed:

- Overview has an internal scroll area.
- Validation has a detail scroll area.
- Network Builder has scrollable activity content and split panels.
- Results contains nested scroll areas, tabs, tables, and graph canvases.

Future direction:

- Define one scroll policy per page: page scroll, section scroll, or canvas pan.
- Avoid nested vertical scrollbars when possible.
- Keep the primary page header and trust state visible.
- Make graph scrolling/panning distinct from page scrolling.
- Style scrollbar width, hover, and contrast consistently.

### Components

Shared reusable components should include:

- Page header with title/subtitle/context.
- Trust/status banner.
- KPI card.
- Inspector panel.
- Data table with grouped headers and filters.
- Empty/loading/error state.
- Evidence/provenance card.
- Graph toolbar and legend.
- Step/progress indicator.
- Primary/secondary/destructive button variants.

### Icons

Current navigation uses Unicode glyphs. The redesign should move to a consistent icon source with:

- fixed visual weight;
- semantic mapping;
- accessible tooltips;
- RTL-safe placement;
- no dependence on font-specific glyph rendering.

## Proposed design sequence

### Stage A — Information architecture approval

Approve the complete Results structure before implementation:

1. Shared context/trust header.
2. Overview as executive dashboard.
3. Network as primary visual analysis workspace.
4. Activities as exact schedule audit.
5. Critical Paths as route comparison.
6. PERT as uncertainty workspace.
7. Inspector/evidence surface shared across tabs.

### Stage B — Static visual concepts

Produce separate visual mockups for:

- Results Overview.
- Results Network with selected activity.
- Activities table with selected critical row.
- Critical Paths master-detail view.
- PERT input/result states.
- Shared navigation/sidebar and scroll behavior.

Use image 1 as the main data source for authoritative Results mockups.

### Stage C — Visual review and approval

The user reviews each mockup and specifies:

- keep/change;
- density;
- language;
- colors;
- node-card detail;
- sidebar icon style;
- interaction expectations.

No production code is changed during this stage unless explicitly requested.

### Stage D — Implementation

Implement page by page, preserving backend contracts and adding visual regression tests.

### Stage E — Cross-page integration

Apply the approved design system to Analyze, Understand, Review, Validate, Results, and Network Builder, then verify RTL, scroll, keyboard, and state transitions.

## Design decision at this point

The image-1 network mockup is a good **visual direction**, but it is not yet the complete Results design. It must be extended to include the full tab data described above and a consistent shell for all other pages.

The next visual deliverable should therefore be a **Results design board** containing one mockup per Results section, rather than immediately coding the Network canvas.
