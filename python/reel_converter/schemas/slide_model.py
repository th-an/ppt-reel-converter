from __future__ import annotations

from pydantic import BaseModel, Field


class Theme(BaseModel):
    primary_color: str | None = None
    secondary_color: str | None = None
    accent_color: str | None = None
    header_font: str | None = None
    body_font: str | None = None
    background_type: str = "solid"
    background_color: str = "FFFFFF"


class Element(BaseModel):
    element_type: str
    text: str | None = None
    font_size_pt: float | None = None
    font_name: str | None = None
    font_bold: bool = False
    font_italic: bool = False
    font_color: str | None = None
    position_pct: dict[str, float] | None = None
    width_pct: float | None = None
    height_pct: float | None = None
    image_name: str | None = None
    image_data: str | None = None
    bullet_items: list[str] = Field(default_factory=list)
    table_rows: list[list[str]] = Field(default_factory=list)


class SlideModel(BaseModel):
    slide_number: int
    content_type: str = "unknown"
    background: dict = Field(default_factory=dict)
    theme: Theme = Field(default_factory=Theme)
    elements: list[Element] = Field(default_factory=list)
    images: dict[str, str] = Field(default_factory=dict)