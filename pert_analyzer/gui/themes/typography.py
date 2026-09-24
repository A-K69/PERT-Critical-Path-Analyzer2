"""
Centralized typography system.

Font family, weights, and named (family, size, weight) tuples consumed by
QFont constructors throughout the GUI.
"""

from __future__ import annotations

from PySide6.QtGui import QFont

# ── Family ─────────────────────────────────────────────────────────
# Noto Sans Arabic is available on Linux and supports Arabic shaping as well
# as Latin text. Keeping one family here also makes QFont-based widgets and
# the application-wide QSS render consistently instead of falling back to
# Segoe UI (which is commonly unavailable outside Windows).
FONT_FAMILY = "Noto Sans Arabic"

# ── Named tuples: (family, size_px, weight) ────────────────────────
DISPLAY_FONT = (FONT_FAMILY, 28, QFont.Weight.Bold)
TITLE_FONT = (FONT_FAMILY, 16, QFont.Weight.DemiBold)
SUBTITLE_FONT = (FONT_FAMILY, 12, QFont.Weight.Normal)
LABEL_FONT = (FONT_FAMILY, 13, QFont.Weight.Normal)
BODY_FONT = (FONT_FAMILY, 13, QFont.Weight.Normal)
BODY_SMALL_FONT = (FONT_FAMILY, 11, QFont.Weight.Normal)
CAPTION_FONT = (FONT_FAMILY, 11, QFont.Weight.Normal)
MUTED_FONT = (FONT_FAMILY, 11, QFont.Weight.Normal)
STATUS_FONT = (FONT_FAMILY, 12, QFont.Weight.Normal)
TABLE_HEADER_FONT = (FONT_FAMILY, 11, QFont.Weight.DemiBold)
KPI_FONT = (FONT_FAMILY, 26, QFont.Weight.Bold)
BUTTON_FONT = (FONT_FAMILY, 12, QFont.Weight.Medium)
