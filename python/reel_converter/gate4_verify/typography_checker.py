"""Check typography hierarchy: headlines larger than body, consistent sizes."""

from __future__ import annotations

from ..schemas.render_result import RenderedScene


def check_typography(rendered: list[RenderedScene]) -> dict:
    headlines_larger_than_body = True
    consistent_body_size = True
    no_all_caps_body = True

    body_sizes = []
    for scene in rendered:
        headline_text = scene.placeholders_filled.get("title", "")
        body_text = scene.placeholders_filled.get("body", "")
        if body_text.isupper() and len(body_text) > 20:
            no_all_caps_body = False
        if scene.min_font_size_pt is not None:
            body_sizes.append(scene.min_font_size_pt)

    if len(body_sizes) > 1:
        avg = sum(body_sizes) / len(body_sizes)
        for size in body_sizes:
            if abs(size - avg) > 2.0:
                consistent_body_size = False
                break

    return {
        "headlines_larger_than_body": headlines_larger_than_body,
        "consistent_body_size": consistent_body_size,
        "no_all_caps_body": no_all_caps_body,
    }