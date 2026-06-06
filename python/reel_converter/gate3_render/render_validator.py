"""Validate rendered scenes before Gate 4."""

from __future__ import annotations

from ..schemas.scene_plan import ScenePlan
from ..schemas.template_config import TemplateConfig
from ..schemas.render_result import RenderedScene, PreQualityCheck, FontSizeViolation

MIN_HEADLINE_PT = 28.0
MIN_BODY_PT = 14.0


def validate_render(
    rendered: list[RenderedScene],
    scene_plan: ScenePlan,
    template_config: TemplateConfig,
) -> PreQualityCheck:
    empty_scenes = []
    placeholder_text_found = []
    text_overflow_count = 0
    font_size_violations = []
    safe_zone_violations = []
    image_count_mismatch = []

    for scene in rendered:
        if not scene.placeholders_filled and not scene.images_inserted:
            empty_scenes.append(scene.scene_number)

        for key, value in scene.placeholders_filled.items():
            if any(p in value.lower() for p in ["click to add", "[image:", "todo", "lorem ipsum"]):
                placeholder_text_found.append(f"{scene.scene_number}:{key}={value}")

        if scene.has_text_overflow:
            text_overflow_count += 1

        if scene.min_font_size_pt is not None:
            if scene.min_font_size_pt < MIN_BODY_PT:
                font_size_violations.append(
                    FontSizeViolation(
                        scene=scene.scene_number,
                        placeholder="body",
                        size_pt=scene.min_font_size_pt,
                        minimum_pt=MIN_BODY_PT,
                    )
                )

        expected_images = sum(
            1 for idx, s in enumerate(scene_plan.scenes, start=1)
            if s.image_name and idx == scene.scene_number
        )
        if len(scene.images_inserted) < expected_images:
            image_count_mismatch.append(scene.scene_number)

    passed = (
        len(empty_scenes) == 0
        and len(placeholder_text_found) == 0
        and text_overflow_count == 0
        and len(font_size_violations) == 0
        and len(safe_zone_violations) == 0
        and len(image_count_mismatch) == 0
    )

    return PreQualityCheck(
        empty_scenes=empty_scenes,
        placeholder_text_found=placeholder_text_found,
        text_overflow_count=text_overflow_count,
        font_size_violations=font_size_violations,
        safe_zone_violations=safe_zone_violations,
        image_count_mismatch=image_count_mismatch,
        passed=passed,
    )