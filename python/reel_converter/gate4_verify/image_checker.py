"""Image checker placeholder — verify images present in output."""

from __future__ import annotations


def check_images(
    original_images: list[str],
    output_images: list[str],
) -> dict:
    missing = [img for img in original_images if img not in output_images]
    return {
        "all_present": len(missing) == 0,
        "missing": missing,
    }