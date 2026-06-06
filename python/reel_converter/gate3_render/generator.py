"""Generate 9:16 PPTX slides from a scene plan using template placeholders."""

from __future__ import annotations

from ..schemas.scene_plan import ScenePlan, Scene
from ..schemas.template_config import TemplateConfig
from ..schemas.render_result import RenderedScene
from .placeholder_filler import fill_placeholder
from .content_fitter import calculate_fit_font_size, shrink_text_to_fit


def generate_scenes(
    scene_plan: ScenePlan,
    template_config: TemplateConfig,
) -> list[RenderedScene]:
    rendered = []
    for idx, scene in enumerate(scene_plan.scenes, start=1):
        rendered_scene = _generate_scene(scene, idx, template_config)
        rendered.append(rendered_scene)
    return rendered


def _generate_scene(
    scene: Scene,
    scene_number: int,
    template_config: TemplateConfig,
) -> RenderedScene:
    layout_name = scene.layout
    layout_mapping = template_config.layout_mappings.get(
        layout_name,
        template_config.layout_mappings.get(template_config.fallback_layout_name),
    )
    placeholders_filled = {}
    images_inserted = []

    if scene.headline:
        placeholders_filled["title"] = scene.headline
    if scene.body_items:
        placeholders_filled["body"] = "\n".join(f"• {item}" for item in scene.body_items)
    if scene.stat_number:
        placeholders_filled["title"] = scene.stat_number
    if scene.stat_label:
        placeholders_filled["body"] = scene.stat_label
    if scene.stat_sublabel:
        placeholders_filled["subtitle"] = scene.stat_sublabel
    if scene.image_name:
        images_inserted.append(scene.image_name)
    if scene.quote_text:
        placeholders_filled["title"] = f'"{scene.quote_text}"'
    if scene.quote_attribution:
        placeholders_filled["subtitle"] = f"— {scene.quote_attribution}"
    if scene.cta_headline:
        placeholders_filled["title"] = scene.cta_headline
    if scene.cta_subheadline:
        placeholders_filled["subtitle"] = scene.cta_subheadline

    has_overflow = False
    min_font = None

    return RenderedScene(
        scene_number=scene_number,
        layout_used=layout_name,
        placeholders_filled=placeholders_filled,
        images_inserted=images_inserted,
        has_text_overflow=has_overflow,
        min_font_size_pt=min_font,
    )