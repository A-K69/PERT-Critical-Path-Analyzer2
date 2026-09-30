from pert_analyzer.benchmark.review_diagnostics import render_markdown


def test_render_markdown_exposes_triage_only_policy_and_tiers():
    output = render_markdown(
        [
            {
                "image": "example.png",
                "activity_reviews": 1,
                "duration_reviews": 2,
                "dependency_reviews": 3,
                "ambiguities": 4,
                "tier_counts": {"BLOCKING_REVIEW": 2},
                "auto_accept_enabled": False,
                "relationship_gate_unchanged": True,
            }
        ]
    )
    assert "triage-only" in output
    assert "BLOCKING_REVIEW=2" in output
    assert "example.png" in output
