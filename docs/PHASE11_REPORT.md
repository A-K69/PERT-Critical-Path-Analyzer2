# Phase 11 — Third Complete AON Reference and Visual Route Safeguards

**Status:** COMPLETE — benchmark expanded and relationship validation improved without lowering confidence gates.

## Benchmark expansion

`tests/test_data/ground_truth/11.json` is now a manually verified `COMPLETE` AON annotation for the uploaded replacement image:

- 21 activity nodes;
- 22 explicit activity-to-activity dependencies;
- durations read from the visible node boxes;
- Start/End circles excluded as external terminals;
- both parallel branches `B→E→F→G→H` and `B→E1→F1→G1→H` included.

The complete AON reference set is now `1.png`, `5.jpeg`, and `11.jpeg`.

## Relationship improvement

`ValidatedDependencyBuilder` now records `visual_route_support`, combining:

- detector-derived shaft support;
- selected-pair boundary contact;
- geometric line continuity;
- arrowhead confidence.

A review candidate can only be promoted when all of the following are simultaneously true:

- confidence score ≥ `0.68`;
- route support ≥ `0.58`;
- arrowhead confidence ≥ `0.50`;
- both boundary contacts ≥ `0.40`;
- direction consistency ≥ `0.85`;
- angular consistency ≥ `0.80`;
- no intervening-node crossing.

The implementation does **not** lower the existing HIGH/MEDIUM thresholds. It adds a stricter evidence conjunction for ambiguous candidates.

Additionally, a shaft that crosses an unrelated detected node is routed to review rather than accepted as a direct dependency. This is a visual/topological contradiction safeguard.

## Measured effect on `11.jpeg`

The first unguarded run showed that promoting ambiguous candidates increased false positives. The policy was tightened and then re-measured. Final results:

| Metric | Before safeguard | After safeguard |
|---|---:|---:|
| Detected directed edges | 6 | 5 |
| Directed precision | 0.5000 | **0.6000** |
| Directed recall | 0.1364 | 0.1364 |
| Directed F1 | 0.2143 | **0.2222** |
| Undirected precision | 0.6667 | **0.8000** |
| Undirected recall | 0.1818 | 0.1818 |
| Undirected F1 | 0.2857 | **0.2963** |
| Direction accuracy | 0.7500 | 0.7500 |

The improvement is therefore a **quality improvement**: fewer visually contradicted false edges, higher precision, and no confidence-gate relaxation. Recall remains the next challenge because several visible connectors are fragmented or lack reliable arrowheads.

## Regression results

The prior complete references did not regress:

- `1.png`: directed precision `1.0000`, direction accuracy `1.0000`.
- `5.jpeg`: directed precision `0.9091`, recall `0.7143`, direction accuracy `1.0000`.

Verification:

- ground-truth validation: **8 annotations found, 0 errors, 0 warnings**;
- focused dependency, endpoint, and benchmark tests: **56 passed**;
- syntax and focused lint: passed.
- full refreshed benchmark: **8 images analyzed, 0 fatal failures, 8 review-required**;
  the benchmark now reflects the post-removal corpus and no longer reports the
  deleted `8.jpeg`, `10.jpeg`, or WhatsApp images.

## Next controlled step

Improve recall by reconstructing fragmented visual routes from connected line evidence, but keep the new crossing safeguard and the strict arrowhead/boundary/direction conjunction. No threshold reduction should be attempted until recall gains are demonstrated with precision stability across all three complete AON references.
