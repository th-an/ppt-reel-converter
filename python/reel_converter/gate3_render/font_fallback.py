"""Font fallback chain for cross-platform compatibility."""

from __future__ import annotations

FONT_FALLBACK_CHAIN = {
    "Aptos": ["Aptos", "Calibri", "Arial", "sans-serif"],
    "Calibri": ["Calibri", "Arial", "Helvetica", "sans-serif"],
    "Arial": ["Arial", "Helvetica", "sans-serif"],
    "Helvetica": ["Helvetica", "Arial", "sans-serif"],
    "Segoe UI": ["Segoe UI", "Arial", "sans-serif"],
    "default": ["Aptos", "Calibri", "Arial", "sans-serif"],
}


def get_font_fallback(original_font: str | None) -> list[str]:
    if not original_font:
        return FONT_FALLBACK_CHAIN["default"]
    for key in FONT_FALLBACK_CHAIN:
        if key.lower() in original_font.lower():
            return FONT_FALLBACK_CHAIN[key]
    return [original_font] + FONT_FALLBACK_CHAIN["default"]


def get_safe_font(original_font: str | None) -> str:
    fallbacks = get_font_fallback(original_font)
    return fallbacks[0] if fallbacks else "sans-serif"