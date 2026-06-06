"""Analyze whitespace balance and content density."""

from __future__ import annotations

from ..schemas.render_result import RenderedScene


def analyze_whitespace(rendered: list[RenderedScene]) -> dict:
    if not rendered:
        return {
            "top_margin_ratio": 0.15,
            "bottom_margin_ratio": 0.20,
            "content_area_usage": 0.5,
            "horizontal_balance": 0.5,
        }

    total_area_usage = 0.0
    for scene in rendered:
        if scene.placeholders_filled:
            content_words = sum(
                len(v.split()) for v in scene.placeholders_filled.values()
            )
            estimated_usage = min(content_words / 15.0, 1.0)
            total_area_usage += estimated_usage

    avg_usage = total_area_usage / len(rendered)

    return {
        "top_margin_ratio": 0.15,
        "bottom_margin_ratio": 0.20,
        "content_area_usage": round(avg_usage, 2),
        "horizontal_balance": 0.5,
    }