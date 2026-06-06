"""Classify shapes into semantic element types."""

from __future__ import annotations


def classify_shape(element: dict) -> str:
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
    if _is_title_by_position(element):
        return "title"
    if _is_body_text(element):
        return "body"

    return "shape"


def _is_title_by_position(element: dict) -> bool:
    top = element.get("top", 0)
    height = element.get("height", 0)
    if not top and not height:
        return False
    slide_height = 9144000
    if top is not None and height is not None and slide_height > 0:
        position_pct = top / slide_height
        if position_pct < 0.25:
            font_size = element.get("font_size")
            if font_size and int(font_size) >= 24000:
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