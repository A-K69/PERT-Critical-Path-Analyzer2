"""
Numeric extraction utilities for OCR post-processing.

Extracts numeric candidates from OCR text, supporting integers, decimals,
negative values, and Arabic-Indic numerals. Returns structured
NumericCandidate objects with bounding boxes and parse warnings.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import List, Optional, Tuple

from pert_analyzer.cv.ocr_models import NumericCandidate, OCRTextRegion
from pert_analyzer.core.models import BoundingBox


@dataclass
class NumericExtractionConfig:
    """Configuration for numeric extraction."""

    allow_negative: bool = True
    allow_decimals: bool = True
    decimal_separator: str = "."
    thousands_separator: str = ","
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    # Common decimal separators for international support
    alternate_decimal_separators: List[str] = field(default_factory=lambda: [",", " "])


# Regular expression for numeric patterns
# Matches: 5, -3.14, 1,000, 3.5, etc.
NUMERIC_PATTERN = re.compile(
    r"[-+]?(?:\d[\d,]*\.?\d*|\.\d+)"
)

# Stricter pattern for pure numeric text
PURE_NUMERIC_PATTERN = re.compile(
    r"^[-+]?(?:\d[\d,]*\.?\d*|\.\d+)$"
)

# Pattern for values like "3/6" or "3-6" (PERT-like)
PERT_LIKE_PATTERN = re.compile(
    r"(\d+(?:\.\d+)?)\s*[/\-]\s*(\d+(?:\.\d+)?)"
)


def normalize_numeric_ocr_text(text: str) -> Tuple[str, List[str]]:
    """Normalize only high-confidence numeric OCR confusions.

    The function is gated by an existing digit and a numeric-looking character
    set, so a standalone activity ID such as ``O`` or ``I`` is never changed.
    Raw OCR remains on the source region and corrections are returned as
    auditable warnings.
    """
    value = (text or "").strip()
    if not value or not re.search(r"\d", value):
        return value, []
    if not re.fullmatch(r"[0-9OoIlS.,\s+\-]+", value):
        return value, []
    warnings: List[str] = []
    normalized = value
    for old, new in {"O": "0", "o": "0", "I": "1", "l": "1"}.items():
        if old in normalized:
            normalized = normalized.replace(old, new)
            warnings.append(f"Mapped OCR '{old}' to '{new}' in numeric context")
    if "." not in normalized and normalized.count(",") == 1:
        left, right = normalized.split(",")
        if left.strip().lstrip("+-").isdigit() and 1 <= len(right.strip()) <= 2:
            normalized = normalized.replace(",", ".")
            warnings.append("Mapped comma decimal separator to '.'")
    return normalized, warnings


class NumericExtractor:
    """
    Extracts numeric candidates from OCR text regions.

    Supports integers, decimals, negative values, and Arabic-Indic numerals.
    """

    def __init__(self, config: Optional[NumericExtractionConfig] = None):
        """Initialize with optional configuration."""
        self.config = config or NumericExtractionConfig()

    def extract_from_region(
        self, region: OCRTextRegion
    ) -> List[NumericCandidate]:
        """
        Extract numeric candidates from a single OCR text region.

        Args:
            region: OCR text region to extract from.

        Returns:
            List of NumericCandidate objects found in the region.
        """
        candidates = []
        raw_text = region.normalized_text or region.text
        text, normalization_warnings = normalize_numeric_ocr_text(raw_text)
        if normalization_warnings:
            region.metadata.setdefault("numeric_normalization", {
                "raw_text": region.raw_text or region.text,
                "normalized_text": text,
                "warnings": [],
            })
            details = region.metadata["numeric_normalization"]
            details["warnings"].extend(
                warning for warning in normalization_warnings
                if warning not in details["warnings"]
            )
            region.numeric_parse_warnings.extend(
                warning for warning in normalization_warnings
                if warning not in region.numeric_parse_warnings
            )

        if not text or not text.strip():
            return candidates

        # Try pure numeric first
        pure_match = PURE_NUMERIC_PATTERN.match(text.strip())
        if pure_match:
            candidate = self._parse_numeric(
                text.strip(), region
            )
            if candidate:
                candidate.metadata["raw_ocr_text"] = region.raw_text or region.text
                candidate.metadata["normalized_ocr_text"] = text.strip()
                candidate.parse_warnings = normalization_warnings + candidate.parse_warnings
                candidates.append(candidate)
            return candidates

        # Find all numeric patterns in text
        for match in NUMERIC_PATTERN.finditer(text):
            num_text = match.group(0)
            candidate = self._parse_numeric(
                num_text, region
            )
            if candidate:
                candidate.metadata["raw_ocr_text"] = region.raw_text or region.text
                candidate.metadata["normalized_ocr_text"] = num_text
                candidate.parse_warnings = normalization_warnings + candidate.parse_warnings
                candidates.append(candidate)

        return candidates

    def extract_from_regions(
        self, regions: List[OCRTextRegion]
    ) -> List[NumericCandidate]:
        """
        Extract numeric candidates from multiple OCR text regions.

        Args:
            regions: List of OCR text regions.

        Returns:
            Combined list of NumericCandidate objects.
        """
        all_candidates = []
        for region in regions:
            candidates = self.extract_from_region(region)
            all_candidates.extend(candidates)
        return all_candidates

    def _parse_numeric(
        self, text: str, region: OCRTextRegion
    ) -> Optional[NumericCandidate]:
        """
        Parse a numeric string into a NumericCandidate.

        Args:
            text: Numeric text string.
            region: Source OCR text region.

        Returns:
            NumericCandidate if parsing succeeds, None otherwise.
        """
        warnings = []
        clean_text = text.strip()

        # Handle thousands separators
        if self.config.thousands_separator in clean_text:
            clean_text = clean_text.replace(self.config.thousands_separator, "")

        # Handle alternate decimal separators
        for sep in self.config.alternate_decimal_separators:
            if sep in clean_text and sep != self.config.decimal_separator:
                # Only replace if it looks like a decimal separator
                parts = clean_text.split(sep)
                if len(parts) == 2 and len(parts[1]) <= 3:
                    clean_text = clean_text.replace(sep, self.config.decimal_separator)
                    warnings.append(f"Replaced '{sep}' with decimal separator")

        # Handle negative sign
        is_negative = False
        if clean_text.startswith("-"):
            is_negative = True
            clean_text = clean_text[1:]
        elif clean_text.startswith("+"):
            clean_text = clean_text[1:]

        # Parse value
        try:
            value = float(clean_text)
            if is_negative:
                value = -value
        except ValueError:
            warnings.append(f"Could not parse '{text}' as numeric")
            return None

        # Validate range
        if self.config.min_value is not None and value < self.config.min_value:
            warnings.append(f"Value {value} below minimum {self.config.min_value}")
        if self.config.max_value is not None and value > self.config.max_value:
            warnings.append(f"Value {value} above maximum {self.config.max_value}")

        # Create candidate
        candidate = NumericCandidate(
            value=value,
            raw_text=text.strip(),
            confidence=region.confidence,
            bounding_box=region.bounding_box,
            source_region_id=region.region_id,
            parse_warnings=warnings,
            is_integer=value == int(value) if not warnings else False,
            is_negative=is_negative,
        )

        return candidate

    def is_numeric(self, text: str) -> bool:
        """
        Check if text is a valid numeric value.

        Args:
            text: Text to check.

        Returns:
            True if text is numeric.
        """
        if not text or not text.strip():
            return False
        return bool(PURE_NUMERIC_PATTERN.match(text.strip()))

    def extract_pert_like_values(
        self, text: str
    ) -> List[Tuple[float, float]]:
        """
        Extract PERT-like value pairs from text (e.g., "3/6", "3-6").

        Args:
            text: Text to search for PERT-like patterns.

        Returns:
            List of (value1, value2) tuples.
        """
        pairs = []
        for match in PERT_LIKE_PATTERN.finditer(text):
            try:
                v1 = float(match.group(1))
                v2 = float(match.group(2))
                pairs.append((v1, v2))
            except ValueError:
                continue
        return pairs
