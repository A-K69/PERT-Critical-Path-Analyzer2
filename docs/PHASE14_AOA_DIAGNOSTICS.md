# Phase 14.1 — AOA Route Diagnostics

Measurement-only inventory for diagonal and fragmented route stitching.
No candidate in this report is promoted to a production dependency.

## 3.jpeg

- Events: **13**
- Raw line segments: **430**
- Logical arrows: **14**
- Rejected arrows: **16**
- Unresolved logical arrows: **3**

| Source | Target | Segments | Coverage | Angular consistency | Intermediate events | Candidate | Near candidate |
|---|---:|---:|---:|---:|---|---|---|
| L | M | 8 | 1.000 | 0.965 | — | yes | yes |
| E | F | 3 | 1.000 | 0.664 | — | yes | yes |
| B | E | 2 | 1.000 | 0.947 | — | yes | yes |
| B | D | 3 | 1.000 | 0.840 | — | yes | yes |
| B | C | 3 | 1.000 | 0.828 | — | yes | yes |
| F | G | 2 | 1.000 | 1.000 | — | yes | yes |
| D | F | 3 | 1.000 | 0.916 | — | yes | yes |
| A | B | 2 | 1.000 | 0.943 | — | yes | yes |
| K | L | 10 | 1.000 | 0.859 | — | yes | yes |
| C | F | 2 | 1.000 | 0.705 | — | yes | yes |
| I | J | 2 | 1.000 | 0.800 | — | yes | yes |
| J | K | 7 | 1.000 | 0.846 | — | yes | yes |
| G | I | 3 | 1.000 | 0.573 | — | no | yes |
| F | H | 16 | 0.809 | 0.395 | cnode_f9cee25f | no | no |
| H | K | 17 | 0.781 | 0.286 | cnode_c4c633ac | no | no |
| C | G | 6 | 0.771 | 0.132 | — | no | no |
| I | K | 8 | 0.752 | 0.194 | cnode_c4c633ac | no | no |
| C | I | 10 | 0.735 | 0.234 | cnode_f9cee25f, cnode_1a389e5b | no | no |
| B | F | 17 | 0.730 | 0.891 | cnode_13fcdc0f | no | no |
| D | G | 15 | 0.729 | 0.898 | cnode_1a389e5b | no | no |
| A | D | 15 | 0.707 | 0.891 | cnode_a5704578 | no | no |
| B | G | 29 | 0.686 | 0.892 | cnode_1a389e5b, cnode_13fcdc0f | no | no |
| A | F | 29 | 0.682 | 0.896 | cnode_a5704578, cnode_13fcdc0f | no | no |
| A | G | 41 | 0.665 | 0.895 | cnode_a5704578, cnode_1a389e5b, cnode_13fcdc0f | no | no |
| J | L | 27 | 0.647 | 0.855 | cnode_41b9feee | no | no |
| K | M | 27 | 0.623 | 0.914 | cnode_41b0370a | no | no |
| J | M | 45 | 0.604 | 0.891 | cnode_41b0370a, cnode_41b9feee | no | no |
| H | J | 1 | 0.558 | 0.641 | — | no | no |
| E | H | 8 | 0.499 | 0.433 | cnode_f9cee25f | no | no |
| A | M | 101 | 0.497 | 0.904 | cnode_41b0370a, cnode_f9cee25f, cnode_a5704578, cnode_1a389e5b, cnode_13fcdc0f, cnode_41b9feee, cnode_c4c633ac | no | no |
| A | L | 84 | 0.491 | 0.895 | cnode_f9cee25f, cnode_a5704578, cnode_1a389e5b, cnode_13fcdc0f, cnode_41b9feee, cnode_c4c633ac | no | no |
| A | E | 2 | 0.490 | 0.072 | — | no | no |
| A | K | 68 | 0.481 | 0.900 | cnode_f9cee25f, cnode_a5704578, cnode_1a389e5b, cnode_13fcdc0f, cnode_c4c633ac | no | no |
| B | M | 89 | 0.480 | 0.904 | cnode_41b0370a, cnode_f9cee25f, cnode_1a389e5b, cnode_13fcdc0f, cnode_41b9feee, cnode_c4c633ac | no | no |
| A | J | 58 | 0.474 | 0.903 | cnode_f9cee25f, cnode_a5704578, cnode_1a389e5b, cnode_13fcdc0f | no | no |
| B | L | 72 | 0.470 | 0.894 | cnode_f9cee25f, cnode_1a389e5b, cnode_13fcdc0f, cnode_41b9feee, cnode_c4c633ac | no | no |
| E | G | 4 | 0.457 | 0.559 | — | no | yes |
| E | M | 55 | 0.456 | 0.640 | cnode_41b0370a, cnode_41b9feee, cnode_afa6be5d | no | no |
| B | K | 55 | 0.455 | 0.898 | cnode_f9cee25f, cnode_1a389e5b, cnode_13fcdc0f, cnode_c4c633ac | no | no |
| D | M | 74 | 0.455 | 0.906 | cnode_41b0370a, cnode_f9cee25f, cnode_1a389e5b, cnode_41b9feee, cnode_c4c633ac | no | no |
| H | L | 17 | 0.452 | 0.559 | cnode_41b9feee | no | no |
| I | L | 22 | 0.451 | 0.250 | cnode_41b9feee | no | no |
| B | J | 43 | 0.441 | 0.898 | cnode_f9cee25f, cnode_1a389e5b, cnode_13fcdc0f | no | no |
| I | M | 29 | 0.439 | 0.463 | cnode_41b0370a | no | no |
| D | L | 57 | 0.439 | 0.894 | cnode_f9cee25f, cnode_1a389e5b, cnode_41b9feee, cnode_c4c633ac | no | no |
| E | L | 56 | 0.435 | 0.576 | cnode_41b9feee, cnode_afa6be5d, cnode_c4c633ac | no | no |
| C | K | 46 | 0.428 | 0.476 | cnode_cd320434, cnode_c4c633ac | no | no |
| H | M | 18 | 0.422 | 0.627 | cnode_41b0370a, cnode_41b9feee | no | no |
| D | K | 39 | 0.414 | 0.897 | cnode_f9cee25f, cnode_1a389e5b, cnode_c4c633ac | no | no |
| A | H | 20 | 0.413 | 0.676 | cnode_a5704578, cnode_1a389e5b, cnode_13fcdc0f | no | no |
| F | M | 61 | 0.411 | 0.912 | cnode_41b0370a, cnode_f9cee25f, cnode_41b9feee, cnode_c4c633ac | no | no |
| G | H | 3 | 0.407 | 0.360 | — | no | no |
| C | J | 20 | 0.395 | 0.431 | cnode_cd320434 | no | no |
| D | H | 12 | 0.392 | 0.582 | cnode_f9cee25f, cnode_1a389e5b | no | no |
| B | H | 18 | 0.391 | 0.606 | cnode_1a389e5b, cnode_13fcdc0f | no | no |
| E | K | 42 | 0.390 | 0.526 | cnode_c4c633ac | no | no |
| A | I | 28 | 0.388 | 0.619 | cnode_a5704578, cnode_13fcdc0f | no | no |
| D | J | 28 | 0.385 | 0.898 | cnode_f9cee25f, cnode_1a389e5b | no | no |
| F | L | 44 | 0.381 | 0.899 | cnode_f9cee25f, cnode_41b9feee, cnode_c4c633ac | no | no |
| G | M | 49 | 0.368 | 0.907 | cnode_41b0370a, cnode_41b9feee, cnode_c4c633ac | no | no |
| B | I | 24 | 0.359 | 0.551 | cnode_13fcdc0f | no | no |
| D | I | 13 | 0.347 | 0.393 | cnode_1a389e5b | no | no |
| C | L | 42 | 0.346 | 0.571 | cnode_cd320434, cnode_41b9feee, cnode_c4c633ac | no | no |
| F | K | 26 | 0.332 | 0.909 | cnode_f9cee25f, cnode_c4c633ac | no | no |
| G | L | 32 | 0.317 | 0.886 | cnode_41b9feee, cnode_c4c633ac | no | no |
| F | J | 13 | 0.256 | 0.913 | cnode_f9cee25f | no | no |
| F | I | 3 | 0.229 | 0.224 | — | no | no |
| A | C | 2 | 0.228 | 0.382 | — | no | no |
| G | K | 14 | 0.218 | 0.893 | cnode_c4c633ac | no | no |
| C | M | 29 | 0.209 | 0.604 | cnode_cd320434, cnode_41b0370a, cnode_41b9feee | no | no |
| E | J | 2 | 0.059 | 0.592 | — | no | no |
| C | H | 2 | 0.048 | 0.832 | — | no | no |
| C | E | 0 | 0.000 | 0.000 | cnode_13fcdc0f | no | no |

## 6.jpeg

- Events: **12**
- Raw line segments: **539**
- Logical arrows: **17**
- Rejected arrows: **7**
- Unresolved logical arrows: **11**

| Source | Target | Segments | Coverage | Angular consistency | Intermediate events | Candidate | Near candidate |
|---|---:|---:|---:|---:|---|---|---|
| F | G | 2 | 1.000 | 0.955 | — | yes | yes |
| E | F | 5 | 1.000 | 0.735 | — | yes | yes |
| A | B | 2 | 1.000 | 0.998 | — | yes | yes |
| D | F | 5 | 1.000 | 0.855 | — | yes | yes |
| C | F | 4 | 1.000 | 0.808 | — | yes | yes |
| I | J | 2 | 1.000 | 0.708 | — | yes | yes |
| G | I | 3 | 1.000 | 0.682 | — | yes | yes |
| B | E | 3 | 1.000 | 0.894 | — | yes | yes |
| B | D | 6 | 1.000 | 0.936 | — | yes | yes |
| B | C | 3 | 1.000 | 0.922 | — | yes | yes |
| K | M | 1 | 1.000 | 0.778 | — | no | no |
| F | H | 23 | 1.000 | 0.587 | cnode_0d0d8e6b | no | no |
| A | F | 41 | 1.000 | 0.845 | cnode_e86b4b5a, cnode_16b2aa80 | no | no |
| A | D | 24 | 1.000 | 0.911 | cnode_16b2aa80 | no | no |
| A | G | 55 | 1.000 | 0.845 | cnode_1380f59b, cnode_e86b4b5a, cnode_16b2aa80 | no | no |
| A | H | 83 | 1.000 | 0.766 | cnode_1380f59b, cnode_e86b4b5a, cnode_0d0d8e6b, cnode_16b2aa80 | no | no |
| D | G | 20 | 1.000 | 0.851 | cnode_1380f59b | no | no |
| D | H | 44 | 1.000 | 0.682 | cnode_1380f59b, cnode_0d0d8e6b | no | no |
| J | M | 26 | 1.000 | 0.656 | cnode_fd4f7519 | no | no |
| G | H | 5 | 1.000 | 0.330 | — | no | no |
| B | F | 23 | 1.000 | 0.797 | cnode_e86b4b5a | no | no |
| B | G | 37 | 1.000 | 0.815 | cnode_1380f59b, cnode_e86b4b5a | no | no |
| B | H | 66 | 1.000 | 0.716 | cnode_1380f59b, cnode_e86b4b5a, cnode_0d0d8e6b | no | no |
| D | I | 15 | 0.966 | 0.294 | cnode_1380f59b | no | no |
| H | M | 40 | 0.916 | 0.727 | cnode_fd4f7519 | no | no |
| H | K | 28 | 0.887 | 0.634 | — | no | yes |
| A | M | 120 | 0.878 | 0.852 | cnode_fd4f7519, cnode_1380f59b, cnode_e86b4b5a, cnode_65e1ffeb, cnode_0d0d8e6b, cnode_16b2aa80 | no | no |
| B | M | 105 | 0.859 | 0.841 | cnode_fd4f7519, cnode_1380f59b, cnode_e86b4b5a, cnode_65e1ffeb, cnode_0d0d8e6b | no | no |
| A | K | 95 | 0.854 | 0.851 | cnode_1380f59b, cnode_e86b4b5a, cnode_65e1ffeb, cnode_0d0d8e6b, cnode_16b2aa80 | no | no |
| D | M | 89 | 0.828 | 0.852 | cnode_fd4f7519, cnode_1380f59b, cnode_65e1ffeb, cnode_0d0d8e6b | no | no |
| B | K | 81 | 0.824 | 0.844 | cnode_1380f59b, cnode_e86b4b5a, cnode_65e1ffeb, cnode_0d0d8e6b | no | no |
| D | K | 63 | 0.789 | 0.839 | cnode_1380f59b, cnode_65e1ffeb, cnode_0d0d8e6b | no | no |
| F | M | 71 | 0.786 | 0.857 | cnode_fd4f7519, cnode_65e1ffeb, cnode_0d0d8e6b | no | no |
| C | G | 15 | 0.779 | 0.213 | — | no | no |
| A | J | 48 | 0.763 | 0.841 | cnode_1380f59b, cnode_e86b4b5a, cnode_0d0d8e6b, cnode_16b2aa80 | no | no |
| C | I | 11 | 0.746 | 0.409 | cnode_1380f59b, cnode_0d0d8e6b | no | no |
| G | M | 53 | 0.725 | 0.836 | cnode_fd4f7519, cnode_65e1ffeb | no | no |
| F | K | 48 | 0.725 | 0.858 | cnode_65e1ffeb, cnode_0d0d8e6b | no | no |
| B | J | 37 | 0.697 | 0.802 | cnode_1380f59b, cnode_e86b4b5a, cnode_0d0d8e6b | no | no |
| I | K | 11 | 0.630 | 0.344 | cnode_65e1ffeb | no | no |
| G | K | 30 | 0.627 | 0.816 | cnode_65e1ffeb | no | no |
| E | M | 48 | 0.604 | 0.586 | cnode_fd4f7519, cnode_65e1ffeb | no | no |
| D | J | 30 | 0.596 | 0.780 | cnode_1380f59b, cnode_0d0d8e6b | no | no |
| C | K | 71 | 0.583 | 0.604 | cnode_0c822511 | no | no |
| I | M | 15 | 0.554 | 0.369 | cnode_fd4f7519 | no | no |
| J | K | 5 | 0.539 | 0.295 | — | no | no |
| C | M | 61 | 0.527 | 0.651 | cnode_fd4f7519, cnode_0c822511 | no | no |
| H | J | 2 | 0.509 | 0.393 | — | no | no |
| E | G | 6 | 0.505 | 0.041 | — | no | no |
| C | J | 25 | 0.503 | 0.566 | cnode_0c822511 | no | no |
| E | H | 13 | 0.466 | 0.094 | cnode_0d0d8e6b | no | no |
| E | K | 34 | 0.444 | 0.575 | cnode_65e1ffeb | no | no |
| A | E | 4 | 0.440 | 0.322 | — | no | no |
| F | J | 15 | 0.419 | 0.793 | cnode_0d0d8e6b | no | no |
| A | C | 4 | 0.412 | 0.064 | — | no | no |
| A | I | 27 | 0.398 | 0.477 | cnode_16b2aa80 | no | no |
| F | I | 3 | 0.370 | 0.445 | — | no | no |
| B | I | 19 | 0.305 | 0.373 | cnode_e86b4b5a | no | no |
| C | H | 24 | 0.259 | 0.678 | — | no | yes |
| G | J | 3 | 0.235 | 0.894 | — | no | no |
| E | I | 3 | 0.172 | 0.909 | — | no | no |
| E | J | 8 | 0.160 | 0.517 | — | no | no |
| C | E | 0 | 0.000 | 0.000 | cnode_e86b4b5a | no | no |
