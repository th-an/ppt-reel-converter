from __future__ import annotations

from pydantic import BaseModel, Field


class ThemeConsistency(BaseModel):
    colors_match: bool = False
    fonts_match: bool = False
    background_preserved: bool = False


class TypographyCheck(BaseModel):
    headlines_larger_than_body: bool = False
    consistent_body_size: bool = False
    no_all_caps_body: bool = True


class WhitespaceCheck(BaseModel):
    top_margin_ratio: float = 0.0
    bottom_margin_ratio: float = 0.0
    content_area_usage: float = 0.0
    horizontal_balance: float = 0.0


class VerificationResult(BaseModel):
    slide_number: int
    title_match: bool = False
    all_bullets_present: bool = False
    all_numbers_present: bool = False
    all_images_present: bool = False
    missing_words: list[str] = Field(default_factory=list)
    missing_numbers: list[str] = Field(default_factory=list)
    missing_images: list[str] = Field(default_factory=list)
    text_overflow_scenes: list[int] = Field(default_factory=list)
    font_size_ok: bool = False
    safe_zone_ok: bool = False
    theme_consistency: ThemeConsistency = Field(default_factory=ThemeConsistency)
    typography_hierarchy: TypographyCheck = Field(default_factory=TypographyCheck)
    whitespace_balance: WhitespaceCheck = Field(default_factory=WhitespaceCheck)
    score: float = 0.0
    passed: bool = False
    flags: list[str] = Field(default_factory=list)