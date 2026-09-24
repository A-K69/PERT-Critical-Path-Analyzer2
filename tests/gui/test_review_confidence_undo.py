from types import SimpleNamespace

from pert_analyzer.gui.pages.review_page import ReviewPage
from pert_analyzer.gui.reviews.categories import ReviewCategory
from pert_analyzer.gui.reviews.confidence import confidence_band
from pert_analyzer.gui.reviews.detail_panels import ReviewActionRequest
from tests.gui.fakes import reviewed_session


def test_confidence_summary_counts_pending_items(qapp) -> None:
    page = ReviewPage()
    session = reviewed_session()
    page.refresh(session)
    text = page._confidence_summary.text()
    assert "Confidence:" in text
    assert "low" in text and "medium" in text and "high" in text


def test_filtered_list_emits_visible_item(qapp) -> None:
    page = ReviewPage()
    session = reviewed_session()
    page.refresh(session)
    items = page.current_items()
    assert len(items) == 2
    target_band = confidence_band(getattr(items[1], "confidence", 0.0)).value
    page._item_list.set_confidence_filter(target_band)
    assert page._item_list.count() >= 1
    visible = page._item_list._visible_items[0]
    page._item_list.setCurrentRow(0)
    assert page._activity_panel._item is visible


def test_undo_restores_last_activity_decision(qapp) -> None:
    page = ReviewPage()
    session = reviewed_session()
    page.refresh(session)
    item = page._activity_panel._item
    page._on_detail_decision(
        ReviewActionRequest(ReviewCategory.ACTIVITIES, item, "ACCEPT")
    )
    assert item.status.value == "ACCEPTED"
    assert session.review_session.pending_activity_count == 1
    page._undo_last_decision()
    assert item.status.value == "PENDING"
    assert session.review_session.pending_activity_count == 2
    assert not session.review_session.decisions
    assert page._last_undo is None

