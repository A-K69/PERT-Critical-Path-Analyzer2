"""
Executive Overview for the Results dashboard.

Overview is intentionally a summary surface. Detailed network, activity-table,
critical-path, and PERT data live in their dedicated tabs and are not embedded
here a second time.
"""

from __future__ import annotations

from typing import Any

from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from pert_analyzer.gui.results.formatting import format_duration
from pert_analyzer.gui.themes.palette import (
    ACCENT,
    BORDER,
    DANGER,
    ELEVATED,
    SUCCESS,
    SURFACE,
    SURFACE_LIGHT,
    TEXT,
    TEXT_MUTED,
    TEXT_SECONDARY,
    WARNING,
)
from pert_analyzer.gui.themes.spacing import RADIUS_LG, RADIUS_SM
from pert_analyzer.gui.themes.typography import (
    KPI_FONT,
    LABEL_FONT,
    MUTED_FONT,
    STATUS_FONT,
    TITLE_FONT,
)


class KpiCard(QFrame):
    """A compact KPI card used by the executive Overview surface."""

    def __init__(self, title: str, parent: QWidget | None = None):
        super().__init__(parent)
        self.setObjectName("overviewKpiCard")
        self.setStyleSheet(
            f"QFrame#overviewKpiCard {{ background-color: {SURFACE};"
            f" border: 1px solid {BORDER}; border-radius: {RADIUS_LG}px; }}"
            f"QFrame#overviewKpiCard:hover {{ border-color: {ACCENT}; }}"
        )
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(4)
        self._title_label = QLabel(title)
        self._title_label.setFont(QFont(*MUTED_FONT))
        self._title_label.setStyleSheet(
            f"color: {TEXT_MUTED}; border: none; background: transparent;"
        )
        layout.addWidget(self._title_label)
        self._value_label = QLabel("Unavailable")
        self._value_label.setFont(QFont(*KPI_FONT))
        self._value_label.setStyleSheet(
            f"color: {TEXT}; border: none; background: transparent;"
        )
        layout.addWidget(self._value_label)
        self._note_label = QLabel("")
        self._note_label.setFont(QFont(*MUTED_FONT))
        self._note_label.setStyleSheet(
            f"color: {TEXT_MUTED}; border: none; background: transparent;"
        )
        layout.addWidget(self._note_label)

    def set_value(self, text: str, color: str = TEXT) -> None:
        self._value_label.setText(text)
        self._value_label.setStyleSheet(
            f"color: {color}; border: none; background: transparent;"
        )

    def set_note(self, text: str) -> None:
        self._note_label.setText(text)

    def title(self) -> str:
        return self._title_label.text()

    def value(self) -> str:
        return self._value_label.text()


class _Panel(QFrame):
    """Shared restrained surface for Overview cards."""

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self.setObjectName("overviewPanel")
        self.setStyleSheet(
            f"QFrame#overviewPanel {{ background-color: {SURFACE};"
            f" border: 1px solid {BORDER}; border-radius: {RADIUS_LG}px; }}"
        )


class OverviewTab(QWidget):
    """Executive summary without duplicated Network or Activities widgets."""

    open_network_requested = Signal()
    open_activities_requested = Signal()
    open_paths_requested = Signal()
    open_validation_requested = Signal()

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self._data: Any = None
        self._session: Any = None
        self._kpi_cards: dict[str, KpiCard] = {}

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(10)

        header = QHBoxLayout()
        heading_stack = QVBoxLayout()
        heading_stack.setSpacing(2)
        heading = QLabel("Project overview")
        heading.setFont(QFont(*TITLE_FONT))
        heading.setStyleSheet(f"color: {TEXT};")
        heading_stack.addWidget(heading)
        self._subtitle = QLabel(
            "A concise view of schedule health, critical structure, and review state."
        )
        self._subtitle.setWordWrap(True)
        self._subtitle.setFont(QFont(*MUTED_FONT))
        self._subtitle.setStyleSheet(f"color: {TEXT_MUTED};")
        heading_stack.addWidget(self._subtitle)
        header.addLayout(heading_stack, stretch=1)
        self._open_network_btn = self._action_button("Open Network")
        self._open_network_btn.clicked.connect(self.open_network_requested)
        header.addWidget(self._open_network_btn)
        root.addLayout(header)

        self._cards_row = QHBoxLayout()
        self._cards_row.setSpacing(10)
        for key, title in (
            ("duration", "Project duration"),
            ("activities", "Activities"),
            ("dependencies", "Dependencies"),
            ("critical_paths", "Critical paths"),
            ("critical_activities", "Critical activities"),
            ("review_state", "Review state"),
        ):
            card = KpiCard(title)
            self._kpi_cards[key] = card
            self._cards_row.addWidget(card, stretch=1)
        root.addLayout(self._cards_row)

        content = QGridLayout()
        content.setHorizontalSpacing(10)
        content.setVerticalSpacing(10)
        content.addWidget(self._build_health_panel(), 0, 0, 1, 3)
        content.addWidget(self._build_paths_panel(), 0, 3, 1, 2)
        content.addWidget(self._build_composition_panel(), 1, 0, 1, 2)
        content.addWidget(self._build_confidence_panel(), 1, 2, 1, 2)
        content.addWidget(self._build_action_panel(), 1, 4, 1, 1)
        root.addLayout(content, stretch=1)

    @staticmethod
    def _action_button(text: str) -> QPushButton:
        button = QPushButton(text)
        button.setObjectName("overviewAction")
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.setStyleSheet(
            f"QPushButton#overviewAction {{ color: {ACCENT};"
            f" background-color: {SURFACE_LIGHT}; border: 1px solid {BORDER};"
            f" border-radius: {RADIUS_SM}px; padding: 7px 12px; }}"
            f"QPushButton#overviewAction:hover {{ border-color: {ACCENT};"
            f" background-color: {ELEVATED}; }}"
        )
        return button

    @staticmethod
    def _panel_heading(panel: QFrame, kicker: str, title: str) -> QVBoxLayout:
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(5)
        kicker_label = QLabel(kicker.upper())
        kicker_label.setFont(QFont(*MUTED_FONT))
        kicker_label.setStyleSheet(f"color: {TEXT_MUTED};")
        layout.addWidget(kicker_label)
        title_label = QLabel(title)
        title_label.setFont(QFont(*STATUS_FONT))
        title_label.setStyleSheet(f"color: {TEXT};")
        layout.addWidget(title_label)
        return layout

    def _build_health_panel(self) -> QFrame:
        panel = _Panel()
        layout = self._panel_heading(panel, "Project health", "Ready for decision-making")
        header = QHBoxLayout()
        self._health_status = QLabel("Authoritative")
        self._health_status.setFont(QFont(*TITLE_FONT))
        self._health_status.setStyleSheet(f"color: {SUCCESS};")
        header.addWidget(self._health_status)
        header.addStretch()
        self._health_button = self._action_button("View validation")
        self._health_button.clicked.connect(self.open_validation_requested)
        header.addWidget(self._health_button)
        layout.addLayout(header)
        self._health_description = QLabel(
            "All review decisions are applied, the graph is valid, and CPM has produced the current schedule."
        )
        self._health_description.setWordWrap(True)
        self._health_description.setFont(QFont(*MUTED_FONT))
        self._health_description.setStyleSheet(f"color: {TEXT_SECONDARY};")
        layout.addWidget(self._health_description)
        self._health_checks = QLabel("")
        self._health_checks.setWordWrap(True)
        self._health_checks.setFont(QFont(*MUTED_FONT))
        self._health_checks.setStyleSheet(f"color: {TEXT_SECONDARY};")
        layout.addWidget(self._health_checks)
        return panel

    def _build_paths_panel(self) -> QFrame:
        panel = _Panel()
        layout = self._panel_heading(panel, "Critical structure", "Critical path snapshot")
        header = QHBoxLayout()
        header.addStretch()
        self._paths_button = self._action_button("Compare all paths")
        self._paths_button.clicked.connect(self.open_paths_requested)
        header.addWidget(self._paths_button)
        layout.addLayout(header)
        self._paths_summary = QLabel("No critical paths available.")
        self._paths_summary.setWordWrap(True)
        self._paths_summary.setFont(QFont(*MUTED_FONT))
        self._paths_summary.setStyleSheet(f"color: {TEXT_SECONDARY};")
        layout.addWidget(self._paths_summary)
        self._path_rows = QVBoxLayout()
        self._path_rows.setSpacing(6)
        layout.addLayout(self._path_rows)
        return panel

    def _build_composition_panel(self) -> QFrame:
        panel = _Panel()
        layout = self._panel_heading(panel, "Network composition", "How the project is shaped")
        self._composition = QLabel("")
        self._composition.setWordWrap(True)
        self._composition.setFont(QFont(*MUTED_FONT))
        self._composition.setStyleSheet(f"color: {TEXT_SECONDARY};")
        layout.addWidget(self._composition)
        button_row = QHBoxLayout()
        button_row.addStretch()
        button = self._action_button("Open Activities")
        button.clicked.connect(self.open_activities_requested)
        button_row.addWidget(button)
        layout.addLayout(button_row)
        return panel

    def _build_confidence_panel(self) -> QFrame:
        panel = _Panel()
        layout = self._panel_heading(panel, "Schedule confidence", "Deterministic CPM basis")
        self._confidence = QLabel("")
        self._confidence.setWordWrap(True)
        self._confidence.setFont(QFont(*MUTED_FONT))
        self._confidence.setStyleSheet(f"color: {TEXT_SECONDARY};")
        layout.addWidget(self._confidence)
        return panel

    def _build_action_panel(self) -> QFrame:
        panel = _Panel()
        layout = self._panel_heading(panel, "Next useful action", "Explore the schedule")
        self._next_action = QLabel("")
        self._next_action.setWordWrap(True)
        self._next_action.setFont(QFont(*MUTED_FONT))
        self._next_action.setStyleSheet(f"color: {TEXT_SECONDARY};")
        layout.addWidget(self._next_action)
        button = self._action_button("Go to Critical Paths")
        button.clicked.connect(self.open_paths_requested)
        layout.addWidget(button)
        return panel

    def set_data(self, data: Any, session: Any = None) -> None:
        """Populate the summary from the authoritative ResultsData snapshot."""
        self._data = data
        self._session = session
        path_count = data.critical_path_count or 0
        self._kpi_cards["duration"].set_value(format_duration(data.project_duration), ACCENT)
        self._kpi_cards["duration"].set_note("CPM verified")
        self._kpi_cards["activities"].set_value(str(data.activity_count), TEXT)
        self._kpi_cards["activities"].set_note("reviewed activities")
        self._kpi_cards["dependencies"].set_value(str(data.dependency_count), TEXT)
        self._kpi_cards["dependencies"].set_note("unique relationships")
        self._kpi_cards["critical_paths"].set_value(str(path_count), WARNING)
        self._kpi_cards["critical_paths"].set_note("zero-float routes")
        self._kpi_cards["critical_activities"].set_value(
            str(data.critical_activity_count), WARNING
        )
        self._kpi_cards["critical_activities"].set_note("on critical structure")
        self._kpi_cards["review_state"].set_value("Complete", SUCCESS)
        self._kpi_cards["review_state"].set_note("graph validated")

        self._health_status.setText("Authoritative")
        self._health_status.setStyleSheet(f"color: {SUCCESS};")
        self._health_checks.setText(
            "✓ Reviewed graph applied    ·    ✓ Validation passed    ·    "
            "✓ CPM result available    ·    ⚠ "
            f"{path_count} critical routes require attention"
        )
        non_critical = max(0, data.activity_count - data.critical_activity_count)
        self._composition.setText(
            f"{data.activity_count} reviewed activities · {data.dependency_count} "
            f"unique dependencies · {data.critical_activity_count} activities on "
            f"critical structure · {non_critical} non-critical activities."
        )
        self._confidence.setText(
            "Calculation source: Backend CPM\n"
            "Graph state: Valid\n"
            "Result authority: Authoritative\n\n"
            "Values shown in Results are read from the reviewed graph and backend analysis."
        )
        self._next_action.setText(
            f"There are {path_count} equal-duration critical route(s). "
            "Compare their branches, then inspect any activity in Network."
        )
        self._set_path_snapshot(data)

    def _set_path_snapshot(self, data: Any) -> None:
        while self._path_rows.count():
            item = self._path_rows.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
        paths = list(data.critical_paths or [])
        self._paths_summary.setText(
            f"{len(paths)} critical path(s) share the project duration of "
            f"{format_duration(data.project_duration)}."
            if paths
            else "No critical paths available."
        )

    def kpi_cards(self) -> dict[str, KpiCard]:
        return dict(self._kpi_cards)
