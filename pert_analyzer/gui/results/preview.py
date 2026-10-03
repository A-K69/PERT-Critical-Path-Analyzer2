"""Safe, non-authoritative preview of image reconstruction evidence.

This widget deliberately consumes ``ReviewSession.reconstruction`` rather than
``ResultsData``. It renders detected geometry and evidence state only; it never
renders CPM metrics, critical paths, float, or project duration.
"""

from __future__ import annotations

import math
from typing import Any

from PySide6.QtCore import QPointF, QRectF, Qt, Signal
from PySide6.QtGui import QBrush, QColor, QFont, QPainter, QPen, QPolygonF
from PySide6.QtWidgets import (
    QComboBox,
    QGraphicsEllipseItem,
    QGraphicsLineItem,
    QGraphicsScene,
    QGraphicsSimpleTextItem,
    QGraphicsView,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from pert_analyzer.gui.themes.palette import ACCENT, BORDER, SURFACE_LIGHT, TEXT, TEXT_MUTED, WARNING


_PENDING = QColor(WARNING)
_RESOLVED = QColor("#35c48a")
_NEUTRAL = QColor(ACCENT)
_CANVAS = QColor("#0d0f15")
_TEXT = QColor("#f1f3f5")
_MUTED = QColor("#a6adb8")


def _confidence(value: Any) -> float:
    try:
        return max(0.0, min(1.0, float(value)))
    except (TypeError, ValueError):
        return 0.0


def _position(item: Any, index: int, total: int) -> tuple[float, float]:
    raw = getattr(item, "position", None)
    if raw is not None and len(raw) >= 2:
        try:
            return float(raw[0]), float(raw[1])
        except (TypeError, ValueError):
            pass
    columns = max(1, int(math.ceil(math.sqrt(max(1, total)))))
    return 120.0 + (index % columns) * 190.0, 90.0 + (index // columns) * 120.0


def _arrow(painter: QPainter, start: QPointF, end: QPointF, color: QColor) -> None:
    dx, dy = end.x() - start.x(), end.y() - start.y()
    length = math.hypot(dx, dy)
    if length < 1e-6:
        return
    ux, uy = dx / length, dy / length
    px, py = -uy, ux
    tip = end
    base = QPointF(end.x() - ux * 10.0, end.y() - uy * 10.0)
    left = QPointF(base.x() + px * 5.0, base.y() + py * 5.0)
    right = QPointF(base.x() - px * 5.0, base.y() - py * 5.0)
    painter.setBrush(QBrush(color))
    painter.setPen(QPen(color, 1))
    painter.drawPolygon(QPolygonF([tip, left, right]))


class _PreviewNode(QGraphicsEllipseItem):
    def __init__(self, label: str, detail: str, center: tuple[float, float], color: QColor):
        x, y = center
        super().__init__(QRectF(x - 48, y - 32, 96, 64))
        self.activity_id = label
        self.setBrush(QBrush(QColor("#1a202b")))
        self.setPen(QPen(color, 2.5))
        self.setToolTip(f"{label}\n{detail}")
        self.setFlag(QGraphicsEllipseItem.GraphicsItemFlag.ItemIsSelectable, True)
        text = QGraphicsSimpleTextItem(f"{label}\n{detail}", self)
        text.setBrush(QBrush(_TEXT))
        text.setFont(QFont("Segoe UI", 8))
        rect = text.boundingRect()
        text.setPos(x - rect.width() / 2, y - rect.height() / 2)


class DetectedPreviewTab(QWidget):
    """Interactive preliminary canvas with confidence/review visual cues."""

    node_selected = Signal(str)

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self._review_session: Any = None
        self._scene = QGraphicsScene(self)
        self._view = QGraphicsView(self._scene)
        self._view.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        self._view.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self._view.setBackgroundBrush(_CANVAS)
        self._view.setMinimumHeight(280)
        self._view.setStyleSheet(f"QGraphicsView {{ border: 1px solid {BORDER}; border-radius: 8px; }}")
        self._nodes: dict[str, _PreviewNode] = {}

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(6)
        toolbar = QHBoxLayout()
        title = QLabel("Detected network preview")
        title.setStyleSheet(f"color: {TEXT}; font-weight: 600;")
        toolbar.addWidget(title)
        badge = QLabel("PRELIMINARY · NOT CPM")
        badge.setStyleSheet(f"color: {WARNING}; font-weight: 600;")
        toolbar.addWidget(badge)
        toolbar.addStretch()
        self._fit = QPushButton("Fit")
        self._fit.clicked.connect(self.fit_to_view)
        self._zoom_in = QPushButton("+")
        self._zoom_in.clicked.connect(lambda: self._view.scale(1.2, 1.2))
        self._zoom_out = QPushButton("−")
        self._zoom_out.clicked.connect(lambda: self._view.scale(1 / 1.2, 1 / 1.2))
        for button in (self._fit, self._zoom_in, self._zoom_out):
            toolbar.addWidget(button)
        root.addLayout(toolbar)
        root.addWidget(self._view, stretch=1)
        legend = QLabel(
            "Legend: blue = detected evidence · amber = review required · green = resolved evidence"
        )
        legend.setWordWrap(True)
        legend.setStyleSheet(f"color: {TEXT_MUTED}; padding: 3px;")
        root.addWidget(legend)
        self._empty = QLabel("No reconstruction preview is available yet.")
        self._empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._empty.setStyleSheet(f"color: {TEXT_MUTED};")
        root.addWidget(self._empty)
        self.hide()

    def set_review_session(self, review_session: Any) -> None:
        self._review_session = review_session
        self._render()

    def clear_preview(self) -> None:
        self._review_session = None
        self._scene.clear()
        self._nodes.clear()
        self.hide()

    def fit_to_view(self) -> None:
        rect = self._scene.itemsBoundingRect()
        if not rect.isNull():
            self._view.fitInView(rect.adjusted(-30, -30, 30, 30), Qt.AspectRatioMode.KeepAspectRatio)

    def node_items(self) -> dict[str, _PreviewNode]:
        return dict(self._nodes)

    def _status_color(self, item_id: str, category: str, item: Any = None) -> QColor:
        items = getattr(self._review_session, category, []) or []
        for review in items:
            key = getattr(review, "geometric_node_id", None) or getattr(review, "arrow_id", None)
            if key == item_id:
                status = getattr(getattr(review, "status", None), "value", "PENDING")
                return _RESOLVED if status != "PENDING" else _PENDING
        confidence = _confidence(getattr(item, "confidence", 0.0))
        return _NEUTRAL if confidence >= 0.5 else _PENDING

    def _render(self) -> None:
        self._scene.clear()
        self._nodes.clear()
        reconstruction = getattr(self._review_session, "reconstruction", None)
        if reconstruction is None:
            self._empty.setText("No reconstruction preview is available yet.")
            self._empty.show()
            self.show()
            return

        activities = list(getattr(reconstruction, "activities", []) or [])
        events = list(getattr(reconstruction, "events", []) or [])
        diagram_type = str(getattr(reconstruction, "diagram_type", "AON"))
        if diagram_type == "AOA" and events:
            self._render_aoa(events, activities)
        else:
            self._render_aon(activities)
        self._empty.setVisible(not self._nodes)
        self.show()
        self.fit_to_view()

    def _render_aon(self, activities: list[Any]) -> None:
        positions: dict[str, tuple[float, float]] = {}
        for index, activity in enumerate(activities):
            key = getattr(activity, "geometric_node_id", None) or getattr(activity, "activity_id", None) or f"node-{index + 1}"
            positions[key] = _position(activity, index, len(activities))
            label = getattr(activity, "activity_id", None) or "unreadable ID"
            duration = getattr(activity, "duration", None)
            detail = f"Detected duration: {duration:g}" if isinstance(duration, (int, float)) and duration > 0 else "Duration: unavailable"
            color = self._status_color(key, "activities", activity)
            node = _PreviewNode(label, detail, positions[key], color)
            node.setFlag(QGraphicsEllipseItem.GraphicsItemFlag.ItemIsSelectable, True)
            self._scene.addItem(node)
            self._nodes[key] = node

        for dep in getattr(getattr(self._review_session, "reconstruction", None), "dependencies", []) or []:
            src, tgt = getattr(dep, "source_id", None), getattr(dep, "target_id", None)
            if src not in positions or tgt not in positions:
                continue
            self._draw_edge(positions[src], positions[tgt], self._status_color(getattr(dep, "source_arrow_id", None) or f"{src}->{tgt}", "dependencies", dep))

    def _render_aoa(self, events: list[Any], activities: list[Any]) -> None:
        positions: dict[str, tuple[float, float]] = {}
        for index, event in enumerate(events):
            key = getattr(event, "event_id", None) or f"event-{index + 1}"
            positions[key] = _position(event, index, len(events))
            node = _PreviewNode(getattr(event, "label", None) or key, "Detected event", positions[key], _NEUTRAL)
            self._scene.addItem(node)
            self._nodes[key] = node
        for index, activity in enumerate(activities):
            src, tgt = getattr(activity, "source_node", None), getattr(activity, "target_node", None)
            if src not in positions or tgt not in positions:
                continue
            color = self._status_color(getattr(activity, "source_arrow_id", None) or getattr(activity, "activity_id", None), "activities", activity)
            self._draw_edge(positions[src], positions[tgt], color)
            label = getattr(activity, "activity_id", None) or "unreadable activity"
            text = QGraphicsSimpleTextItem(f"{label} · detected")
            text.setBrush(QBrush(_MUTED))
            text.setPos((positions[src][0] + positions[tgt][0]) / 2, (positions[src][1] + positions[tgt][1]) / 2)
            self._scene.addItem(text)

    def _draw_edge(self, start: tuple[float, float], end: tuple[float, float], color: QColor) -> None:
        x1, y1 = start
        x2, y2 = end
        line = QGraphicsLineItem(x1, y1, x2, y2)
        line.setPen(QPen(color, 2.0, Qt.PenStyle.DashLine if color == _PENDING else Qt.PenStyle.SolidLine))
        self._scene.addItem(line)
        painter_path = QGraphicsSimpleTextItem("›")
        painter_path.setBrush(QBrush(color))
        painter_path.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        painter_path.setPos(x2 - 7, y2 - 15)
        self._scene.addItem(painter_path)
