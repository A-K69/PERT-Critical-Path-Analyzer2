from types import SimpleNamespace

from pert_analyzer.gui import worker
from pert_analyzer.pipeline import review_api


def test_default_analyze_adds_arabic_ocr_language(monkeypatch) -> None:
    captured = {}

    monkeypatch.setattr(
        "pert_analyzer.config.manager.get_config",
        lambda: SimpleNamespace(
            gui=SimpleNamespace(language="ar"),
            ocr=SimpleNamespace(languages=["eng"]),
        ),
    )

    def fake_analyze(cls, image_path, **kwargs):
        captured.update(kwargs)
        return "workflow"

    monkeypatch.setattr(review_api.ReviewWorkflow, "analyze", classmethod(fake_analyze))
    assert worker.default_analyze("diagram.png") == "workflow"
    assert captured["ocr_languages"] == ["eng", "ara"]


def test_default_analyze_keeps_english_only_for_english_ui(monkeypatch) -> None:
    captured = {}
    monkeypatch.setattr(
        "pert_analyzer.config.manager.get_config",
        lambda: SimpleNamespace(
            gui=SimpleNamespace(language="en"),
            ocr=SimpleNamespace(languages=["eng"]),
        ),
    )

    def fake_analyze(cls, image_path, **kwargs):
        captured.update(kwargs)
        return "workflow"

    monkeypatch.setattr(review_api.ReviewWorkflow, "analyze", classmethod(fake_analyze))
    worker.default_analyze("diagram.png")
    assert captured["ocr_languages"] == ["eng"]
