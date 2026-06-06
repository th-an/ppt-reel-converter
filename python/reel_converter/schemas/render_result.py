from __future__ import annotations

from pydantic import BaseModel, Field


class RenderedScene(BaseModel):
    scene_number: int
    layout_used: str
    placeholders_filled: dict[str, str] = Field(default_factory=dict)
    images_inserted: list[str] = Field(default_factory=list)
    has_text_overflow: bool = False
    min_font_size_pt: float | None = None


class FontSizeViolation(BaseModel):
    scene: int
    placeholder: str
    size_pt: float
    minimum_pt: float


class PreQualityCheck(BaseModel):
    empty_scenes: list[int] = Field(default_factory=list)
    placeholder_text_found: list[str] = Field(default_factory=list)
    text_overflow_count: int = 0
    font_size_violations: list[FontSizeViolation] = Field(default_factory=list)
    safe_zone_violations: list[int] = Field(default_factory=list)
    image_count_mismatch: list[int] = Field(default_factory=list)
    passed: bool = False