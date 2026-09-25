"""Small, explicit UI-locale layer for English and Arabic layouts."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QComboBox, QLabel, QPushButton, QWidget


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

UI_TEXT = {
    "Review Center": "مركز المراجعة",
    "Validation Center": "مركز التحقق",
    "Results Dashboard": "لوحة النتائج",
    "Network Builder": "منشئ الشبكة",
    "Analyze Diagram": "تحليل المخطط",
    "Understanding": "فهم النتائج",
    "Confirm or correct detected activities, dependencies, and durations.": "أكد أو صحح الأنشطة والعلاقات والمدد المكتشفة.",
    "Critical path analysis of the reviewed graph.": "تحليل المسار الحرج للرسم البياني الذي تمت مراجعته.",
    "Upload a PERT/CPM network diagram to begin": "ارفع مخطط شبكة PERT/CPM للبدء",
    "No image selected": "لم يتم اختيار صورة",
    "Select a review item from the list to begin.": "اختر عنصر مراجعة من القائمة للبدء.",
    "Confidence filter": "فلتر الثقة",
    "All items": "كل العناصر",
    "Low confidence": "ثقة منخفضة",
    "Medium confidence": "ثقة متوسطة",
    "High confidence": "ثقة عالية",
    "Focus evidence": "تركيز الأدلة",
    "Apply & Validate": "تطبيق والتحقق",
    "Leave Unresolved": "ترك دون حل",
    "Undo last decision": "التراجع عن آخر قرار",
    "Accept": "قبول",
    "Reject": "رفض",
    "Correct...": "تصحيح...",
    "Reverse": "عكس الاتجاه",
    "Export": "تصدير",
    "Report": "تقرير",
    "Calculate Results": "حساب النتائج",
    "Continue Review": "متابعة المراجعة",
    "Open Validation": "فتح التحقق",
    "FINAL RESULTS": "النتائج النهائية",
    "PRELIMINARY": "أولية",
    "RESULTS NOT READY": "النتائج غير جاهزة",
    "Ready": "جاهز",
    "Apply": "تطبيق",
    "Cancel": "إلغاء",
}


def translate_widget_tree(root: QWidget, value: str | UiLanguage | None) -> None:
    """Translate current visible widget text while preserving English for reversal."""
    language = normalize_language(value)
    for widget in [root, *root.findChildren(QWidget)]:
        if isinstance(widget, (QLabel, QPushButton)):
            source = widget.property("sourceText")
            if source is None:
                source = widget.text()
                widget.setProperty("sourceText", source)
            widget.setText(UI_TEXT.get(source, source) if language == UiLanguage.ARABIC else source)
        elif isinstance(widget, QComboBox):
            for index in range(widget.count()):
                source = widget.itemData(index, Qt.ItemDataRole.UserRole + 1)
                if source is None:
                    source = widget.itemText(index)
                    widget.setItemData(index, source, Qt.ItemDataRole.UserRole + 1)
                widget.setItemText(index, UI_TEXT.get(source, source) if language == UiLanguage.ARABIC else source)


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
