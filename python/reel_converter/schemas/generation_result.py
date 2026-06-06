from __future__ import annotations

from pydantic import BaseModel, Field

from .fingerprint import SlideFingerprint
from .scene_plan import ScenePlan
from .render_result import RenderedScene, PreQualityCheck
from .verification_result import VerificationResult


class SlideResult(BaseModel):
    slide_number: int
    fingerprint: SlideFingerprint
    scene_plan: ScenePlan | None = None
    rendered_scenes: list[RenderedScene] = Field(default_factory=list)
    pre_quality: PreQualityCheck | None = None
    verification: VerificationResult | None = None
    approved: bool = False
    skipped: bool = False
    retry_count: int = 0


class FinalReport(BaseModel):
    input_file: str
    output_file: str | None = None
    template_used: str = "reel_clean"
    total_slides_input: int = 0
    total_scenes_output: int = 0
    slides_approved: int = 0
    slides_skipped: int = 0
    slides_flagged: int = 0
    average_score: float = 0.0
    per_slide_results: list[SlideResult] = Field(default_factory=list)
    per_slide_scores: dict[int, float] = Field(default_factory=dict)