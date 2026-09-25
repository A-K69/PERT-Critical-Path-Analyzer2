"""Small, explicit UI-locale layer for English and Arabic layouts."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QWidget


class UiLanguage(StrEnum):
    ENGLISH = "en"
    ARABIC = "ar"


@dataclass(frozen=True)
class UiLocale:
    language: UiLanguage
    direction: Qt.LayoutDirection

    @property
    def is_rtl(self) -> bool:
        return self.direction == Qt.LayoutDirection.RightToLeft


LOCALES = {
    UiLanguage.ENGLISH: UiLocale(UiLanguage.ENGLISH, Qt.LayoutDirection.LeftToRight),
    UiLanguage.ARABIC: UiLocale(UiLanguage.ARABIC, Qt.LayoutDirection.RightToLeft),
}


def normalize_language(value: str | UiLanguage | None) -> UiLanguage:
    try:
        return UiLanguage(value or UiLanguage.ENGLISH)
    except ValueError:
        return UiLanguage.ENGLISH


def locale_for(value: str | UiLanguage | None) -> UiLocale:
    return LOCALES[normalize_language(value)]


def apply_ui_locale(widget: QWidget, value: str | UiLanguage | None) -> UiLocale:
    """Apply direction to the application and widget without touching analysis data."""
    locale = locale_for(value)
    app = QApplication.instance()
    if app is not None:
        app.setLayoutDirection(locale.direction)
    widget.setLayoutDirection(locale.direction)
    widget.setProperty("uiLanguage", locale.language.value)
    widget.setProperty("uiDirection", "rtl" if locale.is_rtl else "ltr")
    widget.style().unpolish(widget)
    widget.style().polish(widget)
    return locale


NAV_LABELS = {
    UiLanguage.ENGLISH: {
        "analyze": "Analyze",
        "understanding": "Understand",
        "review": "Review",
        "validate": "Validate",
        "results": "Results",
        "network_builder": "Build Network",
    },
    UiLanguage.ARABIC: {
        "analyze": "تحليل",
        "understanding": "فهم النتائج",
        "review": "المراجعة",
        "validate": "التحقق",
        "results": "النتائج",
        "network_builder": "بناء الشبكة",
    },
}


def nav_label(key: str, value: str | UiLanguage | None) -> str:
    language = normalize_language(value)
    return NAV_LABELS[language].get(key, key)


__all__ = [
    "UiLanguage",
    "UiLocale",
    "apply_ui_locale",
    "locale_for",
    "nav_label",
    "normalize_language",
]
