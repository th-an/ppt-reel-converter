"""Classify shapes into semantic element types."""

from __future__ import annotations


def classify_shape(element: dict, all_elements: list[dict] = None) -> str:
    if element.get("is_image"):
        return "image"
    if element.get("is_table"):
        return "table"
    if element.get("is_chart"):
        return "chart"
    if element.get("is_group"):
        return "group"

    text = element.get("text", "").strip()
    if not text:
        shape_type = element.get("shape_type", "")
        if "PICTURE" in shape_type:
            return "image"
        if "SMART_ART" in shape_type.upper():
            return "smart_art"
        return "shape"

    shape_type = element.get("shape_type", "").upper()
    name = element.get("name", "").upper()

    if "TITLE" in name or "TITLE" in shape_type:
        return "title"
    if _is_title_by_position(element, all_elements or []):
        return "title"
    if _is_body_text(element):
        return "body"

    return "shape"


def _is_title_by_position(element: dict, other_elements: list[dict]) -> bool:
    top = element.get("top", 0)
    height = element.get("height", 0)
    text = element.get("text", "").strip()
    if not top and not height:
        return False
    if not text:
        return False
    slide_height = element.get("slide_height", 9144000)
    if not slide_height:
        slide_height = 9144000
    if top is not None and height is not None and slide_height > 0:
        position_pct = top / slide_height
        # Title must be in top 25% of slide
        if position_pct < 0.25:
            font_size = element.get("font_size")
            # Title must be >= 24pt (304800 EMU)
            if font_size and int(font_size) >= 304800:
                # Check if it's the largest font size among text elements
                text_elements = [e for e in other_elements if e.get("text", "").strip()]
                if text_elements:
                    max_font = max(
                        (e.get("font_size", 0) or 0 for e in text_elements),
                        default=0
                    )
                    if font_size >= max_font * 0.9:  # Within 10% of max
                        return True
                return True
    return False


def _is_body_text(element: dict) -> bool:
    paragraphs = element.get("paragraphs", [])
    if len(paragraphs) > 1:
        return True
    text = element.get("text", "")
    if len(text) > 50:
        return True
    return False