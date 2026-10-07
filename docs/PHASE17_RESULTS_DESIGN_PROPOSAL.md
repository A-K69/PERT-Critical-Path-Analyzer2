# Results Page Design Proposal — Image 1

## Design phase boundary

This is a **visual proposal only**. The application UI has not been changed as part of this design review. The proposal uses the verified AON ground truth for `tests/test_data/Imag PERT/1.png` and its documented CPM anchor:

- 22 activities.
- 28 unique dependencies.
- Project duration: 54 days.
- 16 zero-float critical paths.

## Design objective

Make the Results page feel like one product regardless of entry route:

- image analysis;
- Network Builder.

The final authoritative Results view should expose the same information architecture in both routes. Only the trust/provenance badge changes.

## Proposed screen regions

### 1. Product header

- Product identity: `PERT // CONTROL CENTER`.
- Current route: `RESULTS`.
- Source: `Image analysis / 1.png` or `Manual Network Builder`.
- Trust badge: `AUTHORITATIVE RESULT` only after backend validation and review gates pass.

### 2. Executive KPI strip

Cards map to authoritative backend values:

| Card | Data source | Example for image 1 |
|---|---|---:|
| Project duration | backend CPM result | 54 d |
| Activities | reviewed GraphModel | 22 |
| Dependencies | reviewed GraphModel, unique edges | 28 |
| Critical paths | backend CPM result | 16 |
| Critical activities | backend CPM zero-float analysis | 22 |
| Data confidence | aggregated evidence/review contract | 96% example presentation value; exact production formula must be approved before implementation |

### 3. Network Explorer

- Large, spacious graph canvas.
- Geometry based on the reviewed graph, not a decorative redraw.
- Edge arrows remain directional and selectable.
- Critical path is emphasized in amber.
- Non-selected valid relationships remain visible but quieter.
- Fit, zoom, and view-mode controls.
- Selection should update the inspector without leaving Results.

### 4. Activity Inspector

Selecting a node opens a structured card:

- activity ID;
- activity name/label;
- duration;
- early start/finish;
- late start/finish;
- total float;
- critical state;
- predecessors and successors;
- evidence/provenance link.

All schedule values must be displayed from backend CPM analysis. The UI must not recompute them.

### 5. Data Integrity panel

A compact audit surface should answer:

- Was the graph validated?
- Are the CPM values backend-produced?
- How many unique relationships were accepted?
- Is the current result authoritative or preliminary?
- Can the user open the evidence trace?

## Visual direction

- Dark technical control-center theme.
- Cyan for validated structure and interaction.
- Amber for critical paths and attention.
- Green for authoritative/validated state.
- Muted blue-gray for supporting information.
- Rounded panels with restrained borders and strong spacing.
- No dense overlapping labels inside the graph.
- Node cards must be readable at default zoom; tooltips and inspector provide details.

## Important correction from Phase 17.3B

The preliminary image preview is intentionally not the final authoritative network design. It was a safety prototype. The approved Results design should reuse the **authoritative Network Builder visual language** for the image route after review is complete, rather than presenting two unrelated network renderers.

## Approval checkpoints

Before implementation, approve or revise:

1. Overall dark control-center direction.
2. KPI strip content and ordering.
3. Network canvas size and node-card density.
4. Amber critical-path emphasis.
5. Right-side activity inspector.
6. Data Integrity panel.
7. Whether the final production UI should use English labels, Arabic labels, or bilingual labels.

## Proposed implementation order after approval

1. Refactor the authoritative Network canvas visual layer.
2. Add node/edge selection and inspector binding.
3. Apply the same Results shell to image and manual routes.
4. Add evidence/provenance actions.
5. Build image-route authoritative state using the reviewed graph.
6. Add responsive screenshots and regression tests.

No code should be merged from the design proposal until the visual direction is accepted.
