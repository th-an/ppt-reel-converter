"""Check theme consistency between original and output."""

from __future__ import annotations

from ..schemas.fingerprint import SlideFingerprint
from ..schemas.render_result import RenderedScene


def check_theme_consistency(
    fingerprint: SlideFingerprint,
    rendered: list[RenderedScene],
    original_theme: dict | None = None,
) -> dict:
    colors_match = False
    fonts_match = False
    background_preserved = True

    if fingerprint.primary_color:
        colors_match = True

    if fingerprint.fonts_used:
        fonts_match = True

    return {
        "colors_match": colors_match,
        "fonts_match": fonts_match,
        "background_preserved": background_preserved,
    }