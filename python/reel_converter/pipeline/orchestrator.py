"""Orchestrate the 4-gate pipeline per slide, sequential with approval."""

from __future__ import annotations

from ..schemas.fingerprint import SlideFingerprint
from ..schemas.scene_plan import ScenePlan
from ..schemas.render_result import RenderedScene, PreQualityCheck
from ..schemas.verification_result import VerificationResult
from ..schemas.template_config import TemplateConfig
from ..schemas.generation_result import SlideResult
from ..gate1_scan import scan_all_slides
from ..gate2_plan import plan_slide, plan_slide_with_ai
from ..gate3_render import render_scenes
from ..gate4_verify import verify_slide


class Orchestrator:
    def __init__(self, template_config: TemplateConfig, api_key: str | None = None):
        self.template_config = template_config
        self.api_key = api_key
        self.results: list[SlideResult] = []
        self.max_gate2_retries = 3
        self.max_gate3_retries = 2
        self.max_gate4_retries = 2

    def scan_all(self, file_path: str) -> list[SlideFingerprint]:
        return scan_all_slides(file_path, self.template_config.template_name)

    def process_slide(
        self,
        fingerprint: SlideFingerprint,
        use_ai: bool = False,
    ) -> SlideResult:
        result = SlideResult(fingerprint=fingerprint, slide_number=fingerprint.slide_number)

        # Gate 2: Plan
        for attempt in range(self.max_gate2_retries + 1):
            try:
                if use_ai and self.api_key:
                    scene_plan = plan_slide_with_ai(
                        fingerprint=fingerprint,
                        template_config=self.template_config,
                        catalog_markdown="",
                        api_key=self.api_key,
                    )
                else:
                    scene_plan = plan_slide(fingerprint, self.template_config)

                coverage = scene_plan.coverage
                if coverage.title_preserved and (
                    coverage.all_bullets_addressed or not fingerprint.bullet_items
                ):
                    result.scene_plan = scene_plan
                    break
            except Exception:
                if attempt == self.max_gate2_retries:
                    scene_plan = plan_slide(fingerprint, self.template_config)
                    result.scene_plan = scene_plan
                    break

        # Gate 3: Render
        for attempt in range(self.max_gate3_retries + 1):
            try:
                rendered, pre_quality = render_scenes(
                    scene_plan=result.scene_plan,
                    fingerprint=fingerprint,
                    template_config=self.template_config,
                )
                result.rendered_scenes = rendered
                result.pre_quality = pre_quality
                if pre_quality.passed:
                    break
            except Exception:
                if attempt == self.max_gate3_retries:
                    break

        # Gate 4: Verify
        for attempt in range(self.max_gate4_retries + 1):
            verification = verify_slide(
                fingerprint=fingerprint,
                scene_plan=result.scene_plan,
                rendered=result.rendered_scenes,
            )
            result.verification = verification
            if verification.passed:
                break

        return result

    def approve_slide(self, slide_number: int) -> None:
        for r in self.results:
            if r.slide_number == slide_number:
                r.approved = True
                break

    def skip_slide(self, slide_number: int) -> None:
        for r in self.results:
            if r.slide_number == slide_number:
                r.skipped = True
                break