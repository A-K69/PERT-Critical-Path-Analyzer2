# Phase 19 — Activities Data and Component Design Audit

## Status

**Data review complete. Production UI code intentionally unchanged.** This audit defines what the Activities tab should display before the visual implementation begins.

## Authoritative data contract

The Activities tab receives `ResultsData.activities`, a list of immutable `ActivityRow` records. The extraction layer reads graph identity and relationships from the reviewed backend graph, and reads timing, float, and critical state from the backend CPM analysis. The UI must remain a read-only projection.

| Field | Authoritative source | Meaning | Recommended presentation |
|---|---|---|---|
| `activity_id` | Graph activity key / `ActivityRow` | Stable activity identity | Always visible in the table and detail header |
| `name` | Graph activity | Optional human-readable label | Visible in the table when available; fallback to ID |
| `duration` | Graph activity | Activity duration | Compact table metric and prominent detail metric |
| `early_start`, `early_finish` | CPM analysis | Earliest feasible timing window | Detail panel; optionally grouped as ES → EF |
| `late_start`, `late_finish` | CPM analysis | Latest feasible timing window | Detail panel; optionally grouped as LS → LF |
| `total_float` | CPM analysis | Schedule flexibility before affecting project duration | Table metric, filter/sort field, detail metric |
| `free_float` | CPM analysis | Flexibility before affecting an immediate successor | Detail panel and optional table column |
| `is_critical` | CPM analysis / `ActivityRow` | Critical-path membership | Gold status badge and filter |
| `predecessors` | Reviewed graph dependencies | Incoming relationships | Detail relationship section; compact count in table if needed |
| `successors` | Reviewed graph dependencies | Outgoing relationships | Detail relationship section; compact count in table if needed |

`ResultsData.project_duration`, `critical_activity_count`, and `critical_path_count` are dashboard-level values rather than activity fields. They may power the Activities header summary but must not be copied into every row. Complete critical-path sequences belong to the Critical Paths tab and Network highlighting, not to the Activities table.

## Findings in the current UI

The current table has 11 columns: ID, Duration, ES, EF, LS, LF, Total Float, Free Float, Critical, Predecessors, and Successors. This is complete from a data perspective but too wide for a high-quality interactive surface. Long predecessor/successor lists compete with timing values, and the same timing and relationship values are repeated in the lower detail panel. The available `ActivityRow.name` field is not currently shown in the table or detail panel.

The detail panel is the correct place for the complete timing window and full relationships, but it currently has no explicit actions to view the selected activity in Network or to open the relevant Critical Paths context. The existing `activity_selected` signal and ResultsPage routing already provide the safe foundation for those actions.

## Recommended component architecture

### 1. Activities context header

A compact header should establish scope without duplicating row data. Recommended summary cards:

| Card | Source |
|---|---|
| Total activities | `ResultsData.activity_count` |
| Critical activities | `ResultsData.critical_activity_count` |
| Non-critical activities | `activity_count - critical_activity_count` |
| Project duration | `ResultsData.project_duration` |

The fourth card is a project context value, not an activity value, and should be labeled clearly as such. No average duration or new aggregate should be introduced unless the product explicitly requires it; the backend currently exposes no authoritative average metric.

### 2. Filter and view toolbar

The toolbar should contain a search field for ID/name, a Critical / All filter, and compact sort controls for ID, Duration, Total Float, and Critical state. Filtering and sorting are presentation operations only. A small result count should communicate how many rows are visible without implying that the backend dataset changed.

### 3. Primary activity table

The table should prioritize scanning and selection. Recommended default columns are:

1. Activity (ID plus optional name)
2. Duration
3. Total Float
4. Free Float
5. Critical state
6. Predecessors / Successors as compact relationship counts, or a single Links column

Early/late values should not all be repeated in the default table. They remain available in the detail panel and can be exposed through a deliberate compact timing column later if user testing shows it is needed. Full relationship lists should not be rendered in every row because they make the table noisy and duplicate the detail panel.

Critical rows should use restrained gold accents, while the selected row should use the cyan selection treatment shared with Network. Missing numeric values must display `Unavailable`; no fallback or recalculation is allowed.

### 4. Selected Activity detail panel

The detail panel should be the authoritative inspection surface for the selected row:

- Activity ID and name.
- Duration and Critical / Non-critical status.
- Timing grid: Early Start, Early Finish, Late Start, Late Finish.
- Float grid: Total Float and Free Float.
- Relationship sections: Predecessors and Successors.
- Actions: **View in Network** and, when the activity belongs to one or more backend critical paths, **Show Critical Paths**.

The panel should use the same terminology and number formatting as Network Inspector. It should not calculate dates, infer missing relationships, or enumerate paths itself.

### 5. Empty and unavailable states

The tab needs separate messages for:

- No authoritative Results data.
- An authoritative dataset with zero activities.
- A valid row with missing timing values.
- A filter that returns no visible rows.

These states must not be conflated with review-required or non-authoritative states, which are controlled by ResultsPage readiness and provenance.

## Deliberate non-duplication rules

Activities is the activity-level inspection surface. Network owns topology and spatial relationships. Critical Paths owns complete path sequences and path-level selection. Overview owns project-level KPIs and the first few critical-path summaries. Therefore:

- Do not render a miniature Network inside Activities.
- Do not list complete critical-path chains in every activity row.
- Do not duplicate all timing fields in both the default table and the detail panel.
- Do not create a second CPM calculation or a UI-only relationship model.

## Implementation acceptance criteria

The Phase 19 implementation should preserve the existing `activity_selected` signal and ResultsPage synchronization. It should add explicit navigation actions only through presentation signals, keep sorting/filtering local to the tab, and continue to pass the existing authoritative-value tests. The first implementation should be evaluated against the 22-activity reference fixture as well as the two-activity smoke fixture.

## Recommended next step

Proceed to the visual implementation phase with the component order **context header → toolbar → compact table → detail panel actions → empty/filter states**. Capture a real Activities screenshot before adding further interaction polish.
