# Generalization Benchmark

- **PERT Analyzer version:** 0.1.0
- **Generated at (UTC):** 2026-09-28T21:18:57.632949+00:00
- **Dataset root:** `/home/ubuntu/PERT-Critical-Path-Analyzer2/tests/test_data/Imag PERT`
- **Images discovered:** 8 · **Images analyzed:** 8

## Summary

- **Automatic success:** 0
- **Automatic review required:** 8
- **Fatal failures:** 0
- **With ground truth:** 0 · **Without ground truth:** 8
- **With accuracy annotation:** 5 · **Statuses:** {'COMPLETE': 5}
- **Largest activity-count inflation:** 36 (`4.jpeg`)

## Bottleneck summary (first abnormal stage per image)

| Failure class | Images |
| --- | --- |
| `GRAPH_BUILD` | 8 |

## Per-image results

### Summary table

| Image | Fmt | Size | Activities | Valid deps | OCR labels | Diagram | Outcome | Status | Bottleneck | Time |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `1.png` | PNG | 1361x752 | 22 | 11 | 395 | AON | AUTOMATIC_REVIEW_REQUIRED | REVIEW_REQUIRED | GRAPH_BUILD | 29.123 s |
| `11.jpeg` | JPEG | 1264x843 | 21 | 5 | 86 | AON | AUTOMATIC_REVIEW_REQUIRED | REVIEW_REQUIRED | GRAPH_BUILD | 20.394 s |
| `2.jpg` | JPEG | 2340x1080 | 29 | _unavail_ | 77 | AOA | AUTOMATIC_REVIEW_REQUIRED | REVIEW_REQUIRED | GRAPH_BUILD | 13.735 s |
| `3.jpeg` | JPEG | 1080x540 | 13 | _unavail_ | 59 | AOA | AUTOMATIC_REVIEW_REQUIRED | REVIEW_REQUIRED | GRAPH_BUILD | 13.4 s |
| `4.jpeg` | JPEG | 1080x720 | 36 | _unavail_ | 62 | AOA | AUTOMATIC_REVIEW_REQUIRED | REVIEW_REQUIRED | GRAPH_BUILD | 12.41 s |
| `5.jpeg` | JPEG | 1080x720 | 17 | 11 | 146 | AON | AUTOMATIC_REVIEW_REQUIRED | REVIEW_REQUIRED | GRAPH_BUILD | 22.549 s |
| `6.jpeg` | JPEG | 1080x540 | 15 | _unavail_ | 85 | AOA | AUTOMATIC_REVIEW_REQUIRED | REVIEW_REQUIRED | GRAPH_BUILD | 13.031 s |
| `7.jpeg` | JPEG | 1080x608 | 22 | 20 | 602 | AON | AUTOMATIC_REVIEW_REQUIRED | REVIEW_REQUIRED | GRAPH_BUILD | 22.576 s |

## Accuracy benchmark (v1.0 ground truth)

Reported per-image metrics are computed from v1.0 annotations in `tests/test_data/ground_truth/` (see the annotation schema there). Nodes are matched geometrically (bounding-box IoU / centre distance), never by array position or OCR label alone. Dependencies are compared as normalized directed pairs; direction accuracy is tracked separately from the undirected pair. Durations are never rounded. `-` = not computed (`N/A`) for that image.

| Image | Type | ExpActs | DetActs | ActP | ActR | ActF1 | ExpDeps | DetDeps | DepP | DepR | DepF1 | DirAcc | DurationAcc | GraphValid | Review |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `1.png` | AON | 22 | 22 | 1.0000 | 1.0000 | 1.0000 | 28 | 11 | 1.0000 | 0.3929 | 0.5641 | 1.0000 | 0.5909 (MAE 1.0909) | False | AUTOMATIC_REVIEW_REQUIRED |
| `11.jpeg` | AON | 21 | 21 | 1.0000 | 1.0000 | 1.0000 | 22 | 5 | 0.6000 | 0.1364 | 0.2222 | 0.7500 | 0.5238 (MAE 1.2381) | False | AUTOMATIC_REVIEW_REQUIRED |
| `3.jpeg` | AOA | 13 | 13 | 1.0000 | 1.0000 | 1.0000 | - | - | - | - | - | - | - | False | AUTOMATIC_REVIEW_REQUIRED |
| `5.jpeg` | AON | 17 | 17 | 1.0000 | 1.0000 | 1.0000 | 14 | 11 | 0.9091 | 0.7143 | 0.8000 | 1.0000 | 0.5882 (MAE 1.7647) | False | AUTOMATIC_REVIEW_REQUIRED |
| `6.jpeg` | AOA | 12 | 12 | 1.0000 | 1.0000 | 1.0000 | - | - | - | - | - | - | - | False | AUTOMATIC_REVIEW_REQUIRED |

### Aggregates (simple per-image mean over comparable metrics)

| Diagram | Component | Metric | Images compared | Mean |
| --- | --- | --- | --- | --- |
| AON | activities | activity precision | 3 | 1.0000 |
| AON | activities | activity recall | 3 | 1.0000 |
| AON | dependencies | dependency precision | 3 | 0.8364 |
| AON | dependencies | dependency recall | 3 | 0.4145 |
| AON | dependencies | direction accuracy | 3 | 0.9167 |
| AON | durations | duration exact-match accuracy | 3 | 0.5676 |

| AOA | events | event precision | 2 | 1.0000 |
| AOA | events | event recall | 2 | 1.0000 |
| AOA | arrows | arrow precision | 2 | 0.9584 |
| AOA | arrows | arrow recall | 2 | 0.5809 |
| AOA | arrows | arrow direction accuracy | 2 | 1.0000 |

_Aggregation method: unweighted mean of the per-image metric over images where that metric is comparable (uncertain/N-A images excluded). Different components are never averaged together._

### Detail

### 1. `1.png`

- **Outcome:** `AUTOMATIC_REVIEW_REQUIRED` · **Final status:** `REVIEW_REQUIRED`
- **Format/Size:** PNG 1361x752 (48134 bytes) · **Elapsed:** 29.123 s
- **Diagram type:** AON (confidence 1.0)

**Measured pipeline progression:**

| Stage | Counts |
| --- | --- |
| Shape/candidate expansion (measured) | contours_analyzed=274 · raw_shapes=34 · final_candidate_nodes=31 · reconstructed_activities=22 |
| Arrow/dependency pipeline (measured) | raw_arrow_segments=600 · deduplicated_arrows=38 · validated_node_pairs=38 · validated_dependencies=11 · reconstructed_dependencies=11 |
| OCR text (measured) | ocr_regions=395 · ocr_labels=395 · ocr_id_candidates=2 · ocr_numeric_candidates=26 |
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
- **Format/Size:** JPEG 1264x843 (145957 bytes) · **Elapsed:** 20.394 s
- **Diagram type:** AON (confidence 0.7946859903381643)

**Measured pipeline progression:**

| Stage | Counts |
| --- | --- |
| Shape/candidate expansion (measured) | contours_analyzed=11882 · raw_shapes=23 · final_candidate_nodes=23 · reconstructed_activities=21 |
| Arrow/dependency pipeline (measured) | raw_arrow_segments=557 · deduplicated_arrows=19 · validated_node_pairs=19 · validated_dependencies=5 · reconstructed_dependencies=5 |
| OCR text (measured) | ocr_regions=86 · ocr_labels=86 · ocr_id_candidates=0 · ocr_numeric_candidates=14 |
| Graph validation / CPM / PERT | graph_status=INVALID · graph_is_valid=False · cpm_gate=BLOCKED_REVIEW · cpm_project_duration=_unavail_ · critical_path_count=_unavail_ · pert_status=_unavail_ |

**First abnormal stage:** Building graph

**Failure classification:** `GRAPH_BUILD`
**Measured evidence:** graph_status=INVALID · cpm_gate=BLOCKED_REVIEW · reconstructed_activities=21

**Accuracy (v1.0 ground truth):**

- Diagram type: `AON` · Annotation status: `COMPLETE`
- Activities: expected `21`, detected `21`, precision `1.0000`, recall `1.0000`, F1 `1.0000`
- Dependencies/arrows: expected `22`, detected `5`, precision `0.6000`, recall `0.1364`, F1 `0.2222`
- Direction accuracy: `0.7500` (`3` correct · `1` reversed)
- Duration accuracy: `0.5238 (MAE 1.2381)`
- ID accuracy: `0.2381` over `21` compared nodes

### 3. `2.jpg`

- **Outcome:** `AUTOMATIC_REVIEW_REQUIRED` · **Final status:** `REVIEW_REQUIRED`
- **Format/Size:** JPEG 2340x1080 (213745 bytes) · **Elapsed:** 13.735 s
- **Diagram type:** AOA (confidence 1.0)

**Measured pipeline progression:**

| Stage | Counts |
| --- | --- |
| Shape/candidate expansion (measured) | contours_analyzed=3556 · raw_shapes=14 · final_candidate_nodes=14 · reconstructed_activities=29 |
| Arrow/dependency pipeline (measured) | raw_arrow_segments=405 · deduplicated_arrows=_unavail_ · validated_node_pairs=_unavail_ · validated_dependencies=_unavail_ · reconstructed_dependencies=33 |
| OCR text (measured) | ocr_regions=77 · ocr_labels=77 · ocr_id_candidates=1 · ocr_numeric_candidates=5 |
| Graph validation / CPM / PERT | graph_status=INVALID · graph_is_valid=False · cpm_gate=BLOCKED_REVIEW · cpm_project_duration=_unavail_ · critical_path_count=_unavail_ · pert_status=_unavail_ |

**First abnormal stage:** Building graph

**Failure classification:** `GRAPH_BUILD`
**Measured evidence:** graph_status=INVALID · cpm_gate=BLOCKED_REVIEW · reconstructed_activities=29

### 4. `3.jpeg`

- **Outcome:** `AUTOMATIC_REVIEW_REQUIRED` · **Final status:** `REVIEW_REQUIRED`
- **Format/Size:** JPEG 1080x540 (39885 bytes) · **Elapsed:** 13.4 s
- **Diagram type:** AOA (confidence 1.0)

**Measured pipeline progression:**

| Stage | Counts |
| --- | --- |
| Shape/candidate expansion (measured) | contours_analyzed=747 · raw_shapes=16 · final_candidate_nodes=16 · reconstructed_activities=13 |
| Arrow/dependency pipeline (measured) | raw_arrow_segments=430 · deduplicated_arrows=_unavail_ · validated_node_pairs=_unavail_ · validated_dependencies=_unavail_ · reconstructed_dependencies=13 |
| OCR text (measured) | ocr_regions=59 · ocr_labels=59 · ocr_id_candidates=0 · ocr_numeric_candidates=1 |
| Graph validation / CPM / PERT | graph_status=INVALID · graph_is_valid=False · cpm_gate=BLOCKED_REVIEW · cpm_project_duration=_unavail_ · critical_path_count=_unavail_ · pert_status=_unavail_ |

**First abnormal stage:** Building graph

**Failure classification:** `GRAPH_BUILD`
**Measured evidence:** graph_status=INVALID · cpm_gate=BLOCKED_REVIEW · reconstructed_activities=13

**Accuracy (v1.0 ground truth):**

- Diagram type: `AOA` · Annotation status: `COMPLETE`
- Events: expected `13`, detected `13`, precision `1.0000`, recall `1.0000`, F1 `1.0000`
- Dependencies/arrows: expected `None`, detected `None`, precision `-`, recall `-`, F1 `-`
- Direction accuracy: `-` (`-` correct · `-` reversed)
- Duration accuracy: `-`

### 5. `4.jpeg`

- **Outcome:** `AUTOMATIC_REVIEW_REQUIRED` · **Final status:** `REVIEW_REQUIRED`
- **Format/Size:** JPEG 1080x720 (63497 bytes) · **Elapsed:** 12.41 s
- **Diagram type:** AOA (confidence 1.0)

**Measured pipeline progression:**

| Stage | Counts |
| --- | --- |
| Shape/candidate expansion (measured) | contours_analyzed=1262 · raw_shapes=15 · final_candidate_nodes=15 · reconstructed_activities=36 |
| Arrow/dependency pipeline (measured) | raw_arrow_segments=426 · deduplicated_arrows=_unavail_ · validated_node_pairs=_unavail_ · validated_dependencies=_unavail_ · reconstructed_dependencies=62 |
| OCR text (measured) | ocr_regions=62 · ocr_labels=62 · ocr_id_candidates=1 · ocr_numeric_candidates=4 |
| Graph validation / CPM / PERT | graph_status=INVALID · graph_is_valid=False · cpm_gate=BLOCKED_REVIEW · cpm_project_duration=_unavail_ · critical_path_count=_unavail_ · pert_status=_unavail_ |

**First abnormal stage:** Building graph

**Failure classification:** `GRAPH_BUILD`
**Measured evidence:** graph_status=INVALID · cpm_gate=BLOCKED_REVIEW · reconstructed_activities=36

### 6. `5.jpeg`

- **Outcome:** `AUTOMATIC_REVIEW_REQUIRED` · **Final status:** `REVIEW_REQUIRED`
- **Format/Size:** JPEG 1080x720 (55833 bytes) · **Elapsed:** 22.549 s
- **Diagram type:** AON (confidence 0.6403940886699508)

**Measured pipeline progression:**

| Stage | Counts |
| --- | --- |
| Shape/candidate expansion (measured) | contours_analyzed=5168 · raw_shapes=29 · final_candidate_nodes=28 · reconstructed_activities=17 |
| Arrow/dependency pipeline (measured) | raw_arrow_segments=691 · deduplicated_arrows=51 · validated_node_pairs=51 · validated_dependencies=11 · reconstructed_dependencies=11 |
| OCR text (measured) | ocr_regions=146 · ocr_labels=146 · ocr_id_candidates=1 · ocr_numeric_candidates=21 |
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
- **Format/Size:** JPEG 1080x540 (42452 bytes) · **Elapsed:** 13.031 s
- **Diagram type:** AOA (confidence 1.0)

**Measured pipeline progression:**

| Stage | Counts |
| --- | --- |
| Shape/candidate expansion (measured) | contours_analyzed=1328 · raw_shapes=15 · final_candidate_nodes=15 · reconstructed_activities=15 |
| Arrow/dependency pipeline (measured) | raw_arrow_segments=539 · deduplicated_arrows=_unavail_ · validated_node_pairs=_unavail_ · validated_dependencies=_unavail_ · reconstructed_dependencies=16 |
| OCR text (measured) | ocr_regions=85 · ocr_labels=85 · ocr_id_candidates=0 · ocr_numeric_candidates=1 |
| Graph validation / CPM / PERT | graph_status=INVALID · graph_is_valid=False · cpm_gate=BLOCKED_REVIEW · cpm_project_duration=_unavail_ · critical_path_count=_unavail_ · pert_status=_unavail_ |

**First abnormal stage:** Building graph

**Failure classification:** `GRAPH_BUILD`
**Measured evidence:** graph_status=INVALID · cpm_gate=BLOCKED_REVIEW · reconstructed_activities=15

**Accuracy (v1.0 ground truth):**

- Diagram type: `AOA` · Annotation status: `COMPLETE`
- Events: expected `12`, detected `12`, precision `1.0000`, recall `1.0000`, F1 `1.0000`
- Dependencies/arrows: expected `None`, detected `None`, precision `-`, recall `-`, F1 `-`
- Direction accuracy: `-` (`-` correct · `-` reversed)
- Duration accuracy: `-`

### 8. `7.jpeg`

- **Outcome:** `AUTOMATIC_REVIEW_REQUIRED` · **Final status:** `REVIEW_REQUIRED`
- **Format/Size:** JPEG 1080x608 (76454 bytes) · **Elapsed:** 22.576 s
- **Diagram type:** AON (confidence 1.0)

**Measured pipeline progression:**

| Stage | Counts |
| --- | --- |
| Shape/candidate expansion (measured) | contours_analyzed=950 · raw_shapes=22 · final_candidate_nodes=22 · reconstructed_activities=22 |
| Arrow/dependency pipeline (measured) | raw_arrow_segments=651 · deduplicated_arrows=63 · validated_node_pairs=63 · validated_dependencies=20 · reconstructed_dependencies=14 |
| OCR text (measured) | ocr_regions=602 · ocr_labels=602 · ocr_id_candidates=18 · ocr_numeric_candidates=53 |
| Graph validation / CPM / PERT | graph_status=INVALID · graph_is_valid=False · cpm_gate=BLOCKED_REVIEW · cpm_project_duration=_unavail_ · critical_path_count=_unavail_ · pert_status=_unavail_ |

**First abnormal stage:** Building graph

**Failure classification:** `GRAPH_BUILD`
**Measured evidence:** graph_status=INVALID · cpm_gate=BLOCKED_REVIEW · reconstructed_activities=22
