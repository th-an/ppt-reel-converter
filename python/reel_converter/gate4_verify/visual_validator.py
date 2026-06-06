"""Visual validator placeholder — render PNG and detect clipping."""

from __future__ import annotations


def check_visual_overflow(pptx_path: str, slide_number: int) -> dict:
    return {"overflow_detected": False, "details": []}