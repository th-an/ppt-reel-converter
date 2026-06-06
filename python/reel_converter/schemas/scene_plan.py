from __future__ import annotations

from pydantic import BaseModel, Field

from .fingerprint import SlideFingerprint


class Scene(BaseModel):
    layout: str
    content: dict = Field(default_factory=dict)
    headline: str | None = None
    body_items: list[str] = Field(default_factory=list)
    stat_number: str | None = None
    stat_label: str | None = None
    stat_sublabel: str | None = None
    image_name: str | None = None
    image_crop: str = "center"
    image_caption: str | None = None
    quote_text: str | None = None
    quote_attribution: str | None = None
    cta_headline: str | None = None
    cta_subheadline: str | None = None


class CoverageDeclaration(BaseModel):
    title_preserved: bool = False
    title_text: str | None = None
    all_bullets_addressed: bool = False
    all_images_addressed: bool = False
    all_numbers_preserved: bool = False
    numbers_list: list[str] = Field(default_factory=list)
    total_scenes: int = 0
    estimated_total_words: int = 0


class Simplification(BaseModel):
    original_content: str
    simplified_to: str
    reason: str


class ScenePlan(BaseModel):
    slide_number: int
    original_fingerprint: SlideFingerprint
    scenes: list[Scene] = Field(default_factory=list)
    coverage: CoverageDeclaration = Field(default_factory=CoverageDeclaration)
    reasoning: str = ""
    simplifications: list[Simplification] = Field(default_factory=list)