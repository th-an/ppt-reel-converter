from __future__ import annotations

from enum import Enum
from pydantic import BaseModel, Field


class ElementType(str, Enum):
    TITLE = "title"
    BODY = "body"
    BULLET = "bullet"
    IMAGE = "image"
    CHART = "chart"
    TABLE = "table"
    SMART_ART = "smart_art"
    SHAPE = "shape"
    GROUP = "group"
    CONNECTOR = "connector"
    UNKNOWN = "unknown"


class SlideFingerprint(BaseModel):
    slide_number: int
    title_text: str | None = None
    body_texts: list[str] = Field(default_factory=list)
    bullet_items: list[str] = Field(default_factory=list)
    table_count: int = 0
    table_data: list[list[str]] = Field(default_factory=list)
    image_count: int = 0
    image_names: list[str] = Field(default_factory=list)
    total_word_count: int = 0
    total_char_count: int = 0
    unique_numbers: list[str] = Field(default_factory=list)
    content_type: str = "unknown"
    element_count: int = 0
    primary_color: str | None = None
    fonts_used: list[str] = Field(default_factory=list)
    font_sizes: list[int] = Field(default_factory=list)
    has_smart_art: bool = False
    has_chart: bool = False
    has_grouped_shapes: bool = False
    has_connector: bool = False
    warnings: list[str] = Field(default_factory=list)