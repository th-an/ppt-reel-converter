"""Orchestrate scene rendering: generate, fit, validate."""

from __future__ import annotations

from pathlib import Path

from pptx import Presentation

from ..schemas.fingerprint import SlideFingerprint
from ..schemas.scene_plan import ScenePlan
from ..schemas.template_config import TemplateConfig
from ..schemas.render_result import RenderedScene, PreQualityCheck
from .generator import generate_scenes
from .pptx_writer import write_scenes_to_pptx
from .render_validator import validate_render


def render_scenes(
    scene_plan: ScenePlan,
    fingerprint: SlideFingerprint,
    template_config: TemplateConfig,
    output_path: str | None = None,
    original_images: dict[str, str] | None = None,
) -> tuple[list[RenderedScene], PreQualityCheck]:
    # Generate metadata
    rendered = generate_scenes(scene_plan, template_config)

    # Write actual PPTX if output path provided
    if output_path:
        write_scenes_to_pptx(
            scene_plan=scene_plan,
            template_config=template_config,
            output_path=output_path,
            original_images=original_images,
        )

    quality = validate_render(rendered, scene_plan, template_config)

    return rendered, quality