"""Check that all unique numbers from the original appear in the output."""

from __future__ import annotations

from ..schemas.fingerprint import SlideFingerprint
from ..schemas.scene_plan import ScenePlan
from ..schemas.render_result import RenderedScene


def check_numbers(
    fingerprint: SlideFingerprint,
    scene_plan: ScenePlan,
    rendered: list[RenderedScene],
) -> dict:
    if not fingerprint.unique_numbers:
        return {"all_present": True, "missing": [], "found": []}

    all_output_text = " ".join(
        " ".join(s.placeholders_filled.values()) for s in rendered
    )

    found = []
    missing = []
    for num in fingerprint.unique_numbers:
        if num in all_output_text:
            found.append(num)
        else:
            missing.append(num)

    return {
        "all_present": len(missing) == 0,
        "missing": missing,
        "found": found,
    }