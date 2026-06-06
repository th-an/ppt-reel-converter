"""Orchestrate scene planning using rule engine and optional AI."""

from __future__ import annotations

from ..schemas.fingerprint import SlideFingerprint
from ..schemas.scene_plan import ScenePlan, Scene, CoverageDeclaration, Simplification
from ..schemas.template_config import TemplateConfig
from .rule_engine import apply_rules
from .coverage_checker import check_coverage


def plan_slide(
    fingerprint: SlideFingerprint,
    template_config: TemplateConfig,
) -> ScenePlan:
    scenes = apply_rules(fingerprint, template_config)
    coverage = check_coverage(fingerprint, scenes)
    return ScenePlan(
        slide_number=fingerprint.slide_number,
        original_fingerprint=fingerprint,
        scenes=scenes,
        coverage=coverage,
        reasoning="Rule engine applied",
        simplifications=[],
    )


async def plan_slide_with_ai(
    fingerprint: SlideFingerprint,
    template_config: TemplateConfig,
    catalog_markdown: str,
    api_key: str,
    model: str = "deepseek-v4-flash",
) -> ScenePlan:
    try:
        from .ai_agent import get_layout_decision
        ai_result = await get_layout_decision(
            fingerprint=fingerprint,
            template_config=template_config,
            catalog_markdown=catalog_markdown,
            api_key=api_key,
            model=model,
        )
        scenes = ai_result.get("scenes", [])
        parsed = []
        for s in scenes:
            parsed.append(Scene(**s))
        coverage = check_coverage(fingerprint, parsed)
        return ScenePlan(
            slide_number=fingerprint.slide_number,
            original_fingerprint=fingerprint,
            scenes=parsed,
            coverage=coverage,
            reasoning=ai_result.get("reasoning", "AI agent decision"),
            simplifications=[
                Simplification(**s) for s in ai_result.get("simplifications", [])
            ],
        )
    except Exception:
        return plan_slide(fingerprint, template_config)