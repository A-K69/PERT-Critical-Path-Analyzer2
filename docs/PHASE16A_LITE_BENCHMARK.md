# Generalization Benchmark

- **PERT Analyzer version:** 0.1.0
- **Generated at (UTC):** 2026-09-30T18:56:01.667039+00:00
- **Dataset root:** `/home/ubuntu/PERT-Critical-Path-Analyzer2/tests/test_data/Imag PERT`
- **Images discovered:** 8 · **Images analyzed:** 8

## Summary

- **Automatic success:** 0
- **Automatic review required:** 8
- **Fatal failures:** 0
- **With ground truth:** 0 · **Without ground truth:** 8
- **With accuracy annotation:** 8 · **Statuses:** {'COMPLETE': 8}
- **Largest activity-count inflation:** 37 (`4.jpeg`)

## Bottleneck summary (first abnormal stage per image)

| Failure class | Images |
| --- | --- |
| `GRAPH_BUILD` | 8 |

## Per-image results

### Summary table

| Image | Fmt | Size | Activities | Valid deps | OCR labels | Diagram | Outcome | Status | Bottleneck | Time |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `1.png` | PNG | 1361x752 | 22 | 11 | 204 | AON | AUTOMATIC_REVIEW_REQUIRED | REVIEW_REQUIRED | GRAPH_BUILD | 29.701 s |
| `11.jpeg` | JPEG | 1264x843 | 21 | 5 | 65 | AON | AUTOMATIC_REVIEW_REQUIRED | REVIEW_REQUIRED | GRAPH_BUILD | 19.118 s |
| `2.jpg` | JPEG | 2340x1080 | 29 | _unavail_ | 38 | AOA | AUTOMATIC_REVIEW_REQUIRED | REVIEW_REQUIRED | GRAPH_BUILD | 13.057 s |
| `3.jpeg` | JPEG | 1080x540 | 14 | _unavail_ | 30 | AOA | AUTOMATIC_REVIEW_REQUIRED | REVIEW_REQUIRED | GRAPH_BUILD | 13.402 s |
| `4.jpeg` | JPEG | 1080x720 | 37 | _unavail_ | 32 | AOA | AUTOMATIC_REVIEW_REQUIRED | REVIEW_REQUIRED | GRAPH_BUILD | 14.302 s |
| `5.jpeg` | JPEG | 1080x720 | 17 | 11 | 105 | AON | AUTOMATIC_REVIEW_REQUIRED | REVIEW_REQUIRED | GRAPH_BUILD | 24.138 s |
| `6.jpeg` | JPEG | 1080x540 | 17 | _unavail_ | 47 | AOA | AUTOMATIC_REVIEW_REQUIRED | REVIEW_REQUIRED | GRAPH_BUILD | 14.124 s |
| `7.jpeg` | JPEG | 1080x608 | 22 | 20 | 275 | AON | AUTOMATIC_REVIEW_REQUIRED | REVIEW_REQUIRED | GRAPH_BUILD | 23.287 s |

## Accuracy benchmark (v1.0 ground truth)

Reported per-image metrics are computed from v1.0 annotations in `tests/test_data/ground_truth/` (see the annotation schema there). Nodes are matched geometrically (bounding-box IoU / centre distance), never by array position or OCR label alone. Dependencies are compared as normalized directed pairs; direction accuracy is tracked separately from the undirected pair. Durations are never rounded. `-` = not computed (`N/A`) for that image.

| Image | Type | ExpActs | DetActs | ActP | ActR | ActF1 | ExpDeps | DetDeps | DepP | DepR | DepF1 | DirAcc | DurationAcc | GraphValid | Review |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `1.png` | AON | 22 | 22 | 1.0000 | 1.0000 | 1.0000 | 28 | 11 | 1.0000 | 0.3929 | 0.5641 | 1.0000 | 0.5909 (MAE 1.0909) | False | AUTOMATIC_REVIEW_REQUIRED |
| `11.jpeg` | AON | 21 | 21 | 1.0000 | 1.0000 | 1.0000 | 22 | 5 | 0.6000 | 0.1364 | 0.2222 | 0.7500 | 0.4762 (MAE 1.3333) | False | AUTOMATIC_REVIEW_REQUIRED |
| `2.jpg` | AOA | 6 | 9 | 0.6667 | 1.0000 | 0.8000 | 7 | - | - | - | - | - | - | False | AUTOMATIC_REVIEW_REQUIRED |
| `3.jpeg` | AOA | 13 | 13 | 1.0000 | 1.0000 | 1.0000 | - | - | - | - | - | - | - | False | AUTOMATIC_REVIEW_REQUIRED |
| `4.jpeg` | AOA | 12 | 15 | 0.7143 | 0.8333 | 0.7692 | 15 | - | - | - | - | - | - | False | AUTOMATIC_REVIEW_REQUIRED |
| `5.jpeg` | AON | 17 | 17 | 1.0000 | 1.0000 | 1.0000 | 14 | 11 | 0.9091 | 0.7143 | 0.8000 | 1.0000 | 0.5882 (MAE 1.7647) | False | AUTOMATIC_REVIEW_REQUIRED |
| `6.jpeg` | AOA | 12 | 12 | 1.0000 | 1.0000 | 1.0000 | - | - | - | - | - | - | - | False | AUTOMATIC_REVIEW_REQUIRED |
| `7.jpeg` | AON | 23 | 22 | 0.9545 | 0.9130 | 0.9333 | 36 | 14 | 0.3571 | 0.1389 | 0.2000 | 0.7143 | 0.9524 (MAE 0.0476) | False | AUTOMATIC_REVIEW_REQUIRED |

### Aggregates (simple per-image mean over comparable metrics)

| Diagram | Component | Metric | Images compared | Mean |
| --- | --- | --- | --- | --- |
| AON | activities | activity precision | 4 | 0.9886 |
| AON | activities | activity recall | 4 | 0.9783 |
| AON | dependencies | dependency precision | 4 | 0.7166 |
| AON | dependencies | dependency recall | 4 | 0.3456 |
| AON | dependencies | direction accuracy | 4 | 0.8661 |
| AON | durations | duration exact-match accuracy | 4 | 0.6519 |

| AOA | events | event precision | 4 | 0.8453 |
| AOA | events | event recall | 4 | 0.9583 |
| AOA | arrows | arrow precision | 4 | 0.6058 |
| AOA | arrows | arrow recall | 4 | 0.4595 |
| AOA | arrows | arrow direction accuracy | 4 | 0.7500 |

_Aggregation method: unweighted mean of the per-image metric over images where that metric is comparable (uncertain/N-A images excluded). Different components are never averaged together._

### Detail

### 1. `1.png`

- **Outcome:** `AUTOMATIC_REVIEW_REQUIRED` · **Final status:** `REVIEW_REQUIRED`
- **Format/Size:** PNG 1361x752 (48134 bytes) · **Elapsed:** 29.701 s
- **Diagram type:** AON (confidence 1.0)

**Measured pipeline progression:**

| Stage | Counts |
| --- | --- |
| Shape/candidate expansion (measured) | contours_analyzed=274 · raw_shapes=34 · final_candidate_nodes=31 · reconstructed_activities=22 |
| Arrow/dependency pipeline (measured) | raw_arrow_segments=600 · deduplicated_arrows=38 · validated_node_pairs=38 · validated_dependencies=11 · reconstructed_dependencies=11 |
| OCR text (measured) | ocr_regions=204 · ocr_labels=204 · ocr_id_candidates=0 · ocr_numeric_candidates=33 |
| Graph validation / CPM / PERT | graph_status=INVALID · graph_is_valid=False · cpm_gate=BLOCKED_REVIEW · cpm_project_duration=_unavail_ · critical_path_count=_unavail_ · pert_status=_unavail_ |

**First abnormal stage:** Building graph

**Failure classification:** `GRAPH_BUILD`
**Measured evidence:** graph_status=INVALID · cpm_gate=BLOCKED_REVIEW · reconstructed_activities=22

**Accuracy (v1.0 ground truth):**

- Diagram type: `AON` · Annotation status: `COMPLETE`
- Activities: expected `22`, detected `22`, precision `1.0000`, recall `1.0000`, F1 `1.0000`
- Dependencies/arrows: expected `28`, detected `11`, precision `1.0000`, recall `0.3929`, F1 `0.5641`
- Direction accuracy: `1.0000` (`11` correct · `0` reversed)
- Duration accuracy: `0.5909 (MAE 1.0909)`
- ID accuracy: `0.5455` over `22` compared nodes

### 2. `11.jpeg`

- **Outcome:** `AUTOMATIC_REVIEW_REQUIRED` · **Final status:** `REVIEW_REQUIRED`
- **Format/Size:** JPEG 1264x843 (145957 bytes) · **Elapsed:** 19.118 s
- **Diagram type:** AON (confidence 0.7946859903381643)

**Measured pipeline progression:**

| Stage | Counts |
| --- | --- |
| Shape/candidate expansion (measured) | contours_analyzed=11882 · raw_shapes=23 · final_candidate_nodes=23 · reconstructed_activities=21 |
| Arrow/dependency pipeline (measured) | raw_arrow_segments=557 · deduplicated_arrows=19 · validated_node_pairs=19 · validated_dependencies=5 · reconstructed_dependencies=5 |
| OCR text (measured) | ocr_regions=65 · ocr_labels=65 · ocr_id_candidates=0 · ocr_numeric_candidates=15 |
| Graph validation / CPM / PERT | graph_status=INVALID · graph_is_valid=False · cpm_gate=BLOCKED_REVIEW · cpm_project_duration=_unavail_ · critical_path_count=_unavail_ · pert_status=_unavail_ |

**First abnormal stage:** Building graph

**Failure classification:** `GRAPH_BUILD`
**Measured evidence:** graph_status=INVALID · cpm_gate=BLOCKED_REVIEW · reconstructed_activities=21

**Accuracy (v1.0 ground truth):**

- Diagram type: `AON` · Annotation status: `COMPLETE`
- Activities: expected `21`, detected `21`, precision `1.0000`, recall `1.0000`, F1 `1.0000`
- Dependencies/arrows: expected `22`, detected `5`, precision `0.6000`, recall `0.1364`, F1 `0.2222`
- Direction accuracy: `0.7500` (`3` correct · `1` reversed)
- Duration accuracy: `0.4762 (MAE 1.3333)`
- ID accuracy: `0.2381` over `21` compared nodes

### 3. `2.jpg`

- **Outcome:** `AUTOMATIC_REVIEW_REQUIRED` · **Final status:** `REVIEW_REQUIRED`
- **Format/Size:** JPEG 2340x1080 (213745 bytes) · **Elapsed:** 13.057 s
- **Diagram type:** AOA (confidence 1.0)

**Measured pipeline progression:**

| Stage | Counts |
| --- | --- |
| Shape/candidate expansion (measured) | contours_analyzed=3556 · raw_shapes=14 · final_candidate_nodes=14 · reconstructed_activities=29 |
| Arrow/dependency pipeline (measured) | raw_arrow_segments=405 · deduplicated_arrows=_unavail_ · validated_node_pairs=_unavail_ · validated_dependencies=_unavail_ · reconstructed_dependencies=33 |
| OCR text (measured) | ocr_regions=38 · ocr_labels=38 · ocr_id_candidates=0 · ocr_numeric_candidates=5 |
| Graph validation / CPM / PERT | graph_status=INVALID · graph_is_valid=False · cpm_gate=BLOCKED_REVIEW · cpm_project_duration=_unavail_ · critical_path_count=_unavail_ · pert_status=_unavail_ |

**First abnormal stage:** Building graph

**Failure classification:** `GRAPH_BUILD`
**Measured evidence:** graph_status=INVALID · cpm_gate=BLOCKED_REVIEW · reconstructed_activities=29

**Accuracy (v1.0 ground truth):**

- Diagram type: `AOA` · Annotation status: `COMPLETE`
- Events: expected `6`, detected `9`, precision `0.6667`, recall `1.0000`, F1 `0.8000`
- Dependencies/arrows: expected `7`, detected `None`, precision `-`, recall `-`, F1 `-`
- Direction accuracy: `-` (`-` correct · `-` reversed)
- Duration accuracy: `-`

### 4. `3.jpeg`

- **Outcome:** `AUTOMATIC_REVIEW_REQUIRED` · **Final status:** `REVIEW_REQUIRED`
- **Format/Size:** JPEG 1080x540 (39885 bytes) · **Elapsed:** 13.402 s
- **Diagram type:** AOA (confidence 1.0)

**Measured pipeline progression:**

| Stage | Counts |
| --- | --- |
| Shape/candidate expansion (measured) | contours_analyzed=747 · raw_shapes=16 · final_candidate_nodes=16 · reconstructed_activities=14 |
| Arrow/dependency pipeline (measured) | raw_arrow_segments=430 · deduplicated_arrows=_unavail_ · validated_node_pairs=_unavail_ · validated_dependencies=_unavail_ · reconstructed_dependencies=14 |
| OCR text (measured) | ocr_regions=30 · ocr_labels=30 · ocr_id_candidates=0 · ocr_numeric_candidates=7 |
| Graph validation / CPM / PERT | graph_status=INVALID · graph_is_valid=False · cpm_gate=BLOCKED_REVIEW · cpm_project_duration=_unavail_ · critical_path_count=_unavail_ · pert_status=_unavail_ |

**First abnormal stage:** Building graph

**Failure classification:** `GRAPH_BUILD`
**Measured evidence:** graph_status=INVALID · cpm_gate=BLOCKED_REVIEW · reconstructed_activities=14

**Accuracy (v1.0 ground truth):**

- Diagram type: `AOA` · Annotation status: `COMPLETE`
- Events: expected `13`, detected `13`, precision `1.0000`, recall `1.0000`, F1 `1.0000`
- Dependencies/arrows: expected `None`, detected `None`, precision `-`, recall `-`, F1 `-`
- Direction accuracy: `-` (`-` correct · `-` reversed)
- Duration accuracy: `-`

### 5. `4.jpeg`

- **Outcome:** `AUTOMATIC_REVIEW_REQUIRED` · **Final status:** `REVIEW_REQUIRED`
- **Format/Size:** JPEG 1080x720 (63497 bytes) · **Elapsed:** 14.302 s
- **Diagram type:** AOA (confidence 1.0)

**Measured pipeline progression:**

| Stage | Counts |
| --- | --- |
| Shape/candidate expansion (measured) | contours_analyzed=1262 · raw_shapes=15 · final_candidate_nodes=15 · reconstructed_activities=37 |
| Arrow/dependency pipeline (measured) | raw_arrow_segments=426 · deduplicated_arrows=_unavail_ · validated_node_pairs=_unavail_ · validated_dependencies=_unavail_ · reconstructed_dependencies=68 |
| OCR text (measured) | ocr_regions=32 · ocr_labels=32 · ocr_id_candidates=0 · ocr_numeric_candidates=5 |
| Graph validation / CPM / PERT | graph_status=INVALID · graph_is_valid=False · cpm_gate=BLOCKED_REVIEW · cpm_project_duration=_unavail_ · critical_path_count=_unavail_ · pert_status=_unavail_ |

**First abnormal stage:** Building graph

**Failure classification:** `GRAPH_BUILD`
**Measured evidence:** graph_status=INVALID · cpm_gate=BLOCKED_REVIEW · reconstructed_activities=37

**Accuracy (v1.0 ground truth):**

- Diagram type: `AOA` · Annotation status: `COMPLETE`
- Events: expected `12`, detected `15`, precision `0.7143`, recall `0.8333`, F1 `0.7692`
- Dependencies/arrows: expected `15`, detected `None`, precision `-`, recall `-`, F1 `-`
- Direction accuracy: `-` (`-` correct · `-` reversed)
- Duration accuracy: `-`

### 6. `5.jpeg`

- **Outcome:** `AUTOMATIC_REVIEW_REQUIRED` · **Final status:** `REVIEW_REQUIRED`
- **Format/Size:** JPEG 1080x720 (55833 bytes) · **Elapsed:** 24.138 s
- **Diagram type:** AON (confidence 0.6403940886699508)

**Measured pipeline progression:**

| Stage | Counts |
| --- | --- |
| Shape/candidate expansion (measured) | contours_analyzed=5168 · raw_shapes=29 · final_candidate_nodes=28 · reconstructed_activities=17 |
| Arrow/dependency pipeline (measured) | raw_arrow_segments=691 · deduplicated_arrows=51 · validated_node_pairs=51 · validated_dependencies=11 · reconstructed_dependencies=11 |
| OCR text (measured) | ocr_regions=105 · ocr_labels=105 · ocr_id_candidates=0 · ocr_numeric_candidates=20 |
| Graph validation / CPM / PERT | graph_status=INVALID · graph_is_valid=False · cpm_gate=BLOCKED_REVIEW · cpm_project_duration=_unavail_ · critical_path_count=_unavail_ · pert_status=_unavail_ |

**First abnormal stage:** Building graph

**Failure classification:** `GRAPH_BUILD`
**Measured evidence:** graph_status=INVALID · cpm_gate=BLOCKED_REVIEW · reconstructed_activities=17

**Accuracy (v1.0 ground truth):**

- Diagram type: `AON` · Annotation status: `COMPLETE`
- Activities: expected `17`, detected `17`, precision `1.0000`, recall `1.0000`, F1 `1.0000`
- Dependencies/arrows: expected `14`, detected `11`, precision `0.9091`, recall `0.7143`, F1 `0.8000`
- Direction accuracy: `1.0000` (`10` correct · `0` reversed)
- Duration accuracy: `0.5882 (MAE 1.7647)`
- ID accuracy: `0.9412` over `17` compared nodes

### 7. `6.jpeg`

- **Outcome:** `AUTOMATIC_REVIEW_REQUIRED` · **Final status:** `REVIEW_REQUIRED`
- **Format/Size:** JPEG 1080x540 (42452 bytes) · **Elapsed:** 14.124 s
- **Diagram type:** AOA (confidence 1.0)

**Measured pipeline progression:**

| Stage | Counts |
| --- | --- |
| Shape/candidate expansion (measured) | contours_analyzed=1328 · raw_shapes=15 · final_candidate_nodes=15 · reconstructed_activities=17 |
| Arrow/dependency pipeline (measured) | raw_arrow_segments=539 · deduplicated_arrows=_unavail_ · validated_node_pairs=_unavail_ · validated_dependencies=_unavail_ · reconstructed_dependencies=23 |
| OCR text (measured) | ocr_regions=47 · ocr_labels=47 · ocr_id_candidates=0 · ocr_numeric_candidates=17 |
| Graph validation / CPM / PERT | graph_status=INVALID · graph_is_valid=False · cpm_gate=BLOCKED_REVIEW · cpm_project_duration=_unavail_ · critical_path_count=_unavail_ · pert_status=_unavail_ |

**First abnormal stage:** Building graph

**Failure classification:** `GRAPH_BUILD`
**Measured evidence:** graph_status=INVALID · cpm_gate=BLOCKED_REVIEW · reconstructed_activities=17

**Accuracy (v1.0 ground truth):**

- Diagram type: `AOA` · Annotation status: `COMPLETE`
- Events: expected `12`, detected `12`, precision `1.0000`, recall `1.0000`, F1 `1.0000`
- Dependencies/arrows: expected `None`, detected `None`, precision `-`, recall `-`, F1 `-`
- Direction accuracy: `-` (`-` correct · `-` reversed)
- Duration accuracy: `-`

### 8. `7.jpeg`

- **Outcome:** `AUTOMATIC_REVIEW_REQUIRED` · **Final status:** `REVIEW_REQUIRED`
- **Format/Size:** JPEG 1080x608 (76454 bytes) · **Elapsed:** 23.287 s
- **Diagram type:** AON (confidence 1.0)

**Measured pipeline progression:**

| Stage | Counts |
| --- | --- |
| Shape/candidate expansion (measured) | contours_analyzed=950 · raw_shapes=22 · final_candidate_nodes=22 · reconstructed_activities=22 |
| Arrow/dependency pipeline (measured) | raw_arrow_segments=651 · deduplicated_arrows=63 · validated_node_pairs=63 · validated_dependencies=20 · reconstructed_dependencies=14 |
| OCR text (measured) | ocr_regions=275 · ocr_labels=275 · ocr_id_candidates=0 · ocr_numeric_candidates=52 |
| Graph validation / CPM / PERT | graph_status=INVALID · graph_is_valid=False · cpm_gate=BLOCKED_REVIEW · cpm_project_duration=_unavail_ · critical_path_count=_unavail_ · pert_status=_unavail_ |

**First abnormal stage:** Building graph

**Failure classification:** `GRAPH_BUILD`
**Measured evidence:** graph_status=INVALID · cpm_gate=BLOCKED_REVIEW · reconstructed_activities=22

**Accuracy (v1.0 ground truth):**

- Diagram type: `AON` · Annotation status: `COMPLETE`
- Activities: expected `23`, detected `22`, precision `0.9545`, recall `0.9130`, F1 `0.9333`
- Dependencies/arrows: expected `36`, detected `14`, precision `0.3571`, recall `0.1389`, F1 `0.2000`
- Direction accuracy: `0.7143` (`5` correct · `2` reversed)
- Duration accuracy: `0.9524 (MAE 0.0476)`
- ID accuracy: `0.0476` over `21` compared nodes
