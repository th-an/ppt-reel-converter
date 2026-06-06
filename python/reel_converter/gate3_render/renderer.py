"""Orchestrate scene rendering: generate, fit, validate."""

from __future__ import annotations

from pathlib import Path

from pptx import Presentation

from ..schemas.fingerprint import SlideFingerprint
from ..schemas.scene_plan import ScenePlan
from ..schemas.template_config import TemplateConfig
from ..schemas.render_result import RenderedScene, PreQualityCheck
from .generator import generate_scenes
from .render_validator import validate_render


def render_scenes(
    scene_plan: ScenePlan,
    fingerprint: SlideFingerprint,
    template_config: TemplateConfig,
    output_path: str | None = None,
) -> tuple[list[RenderedScene], PreQualityCheck]:
    rendered = generate_scenes(scene_plan, template_config)

    if output_path:
        prs = Presentation(template_config.template_path or "templates/reel_clean.pptx")
        _ = _build_pptx(rendered, scene_plan, template_config, prs)
        temp_path = output_path
        if temp_path:
            prs.save(temp_path)

    quality = validate_render(rendered, scene_plan, template_config)

    return rendered, quality


def _build_pptx(
    rendered: list[RenderedScene],
    scene_plan: ScenePlan,
    template_config: TemplateConfig,
    prs: Presentation,
) -> Presentation:
    return prs