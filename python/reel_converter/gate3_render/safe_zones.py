"""Enforce Instagram Reels safe zones (15% top, 20% bottom)."""

from __future__ import annotations

from ..schemas.template_config import SafeZone

REEL_SAFE_ZONE = SafeZone(top_pct=0.15, bottom_pct=0.20)


def get_safe_area(
    slide_width_emu: int,
    slide_height_emu: int,
    safe_zone: SafeZone | None = None,
) -> dict[str, int]:
    sz = safe_zone or REEL_SAFE_ZONE
    top_margin = int(slide_height_emu * sz.top_pct)
    bottom_margin = int(slide_height_emu * sz.bottom_pct)
    content_top = top_margin
    content_bottom = slide_height_emu - bottom_margin
    content_height = content_bottom - content_top

    return {
        "top_margin": top_margin,
        "bottom_margin": bottom_margin,
        "content_top": content_top,
        "content_bottom": content_bottom,
        "content_height": content_height,
        "slide_width": slide_width_emu,
        "slide_height": slide_height_emu,
    }


def is_within_safe_zone(
    left: int,
    top: int,
    width: int,
    height: int,
    slide_width_emu: int,
    slide_height_emu: int,
    safe_zone: SafeZone | None = None,
) -> bool:
    area = get_safe_area(slide_width_emu, slide_height_emu, safe_zone)
    return (
        top >= area["content_top"]
        and (top + height) <= area["content_bottom"]
        and left >= 0
        and (left + width) <= slide_width_emu
    )