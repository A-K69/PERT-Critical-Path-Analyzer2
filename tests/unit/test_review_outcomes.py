from pert_analyzer.benchmark.review_outcomes import measure_sessions, render_markdown


def _evidence(tier):
    return [{"metadata": {"review_calibration": {"tier": tier}}}]


def test_measure_sessions_aggregates_outcomes_by_tier_and_type():
    report = measure_sessions(
        [
            {
                "source_image_id": "sample.png",
                "decisions": [{"decision": "ACCEPT"}],
                "activities": [
                    {"status": "ACCEPTED", "confidence": 0.8, "evidence": _evidence("LOW_RISK_REVIEW")},
                    {"status": "CORRECTED", "confidence": 0.3, "evidence": _evidence("HIGH_PRIORITY_REVIEW")},
                ],
                "durations": [
                    {"status": "PENDING", "confidence": 0.0, "evidence": _evidence("BLOCKING_REVIEW")},
                ],
                "dependencies": [
                    {"status": "REJECTED", "confidence": 0.2, "evidence": _evidence("HIGH_RISK_REVIEW")},
                ],
            }
        ]
    )
    assert report["production_outcome_data_available"] is True
    assert report["items"] == 4
    assert report["sessions_with_decisions"] == 1
    assert report["by_tier"]["LOW_RISK_REVIEW"]["resolution_rate"] == 1.0
    assert report["by_tier"]["HIGH_PRIORITY_REVIEW"]["correction_rate"] == 1.0
    assert report["by_tier"]["BLOCKING_REVIEW"]["unresolved_blocker_rate"] == 1.0
    assert report["decision_counts"] == {
        "ACCEPTED": 1,
        "CORRECTED": 1,
        "PENDING": 1,
        "REJECTED": 1,
    }


def test_empty_measurement_is_explicitly_not_reviewer_evidence():
    report = measure_sessions([])
    assert report["production_outcome_data_available"] is False
    assert report["items"] == 0
    assert report["overall"]["resolution_rate"] is None
    markdown = render_markdown(report)
    assert "Production outcome data available: **False**" in markdown
    assert "Evaluation-only gold corrections" in markdown
