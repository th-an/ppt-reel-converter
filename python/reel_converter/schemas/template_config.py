from __future__ import annotations

from pydantic import BaseModel, Field


class BrandConfig(BaseModel):
    primary_color: str = "0196FF"
    secondary_color: str = "000000"
    accent_color: str = "595959"
    header_font: str = "Aptos"
    body_font: str = "Aptos"


class LayoutMapping(BaseModel):
    layout_index: int
    layout_name: str
    use_case: str | None = None


class SafeZone(BaseModel):
    top_pct: float = 0.15
    bottom_pct: float = 0.20


class Dimensions(BaseModel):
    width_emu: int = 5143500
    height_emu: int = 9144000


class TemplateConfig(BaseModel):
    template_name: str
    template_path: str | None = None
    dimensions: Dimensions = Field(default_factory=Dimensions)
    safe_zone: SafeZone = Field(default_factory=SafeZone)
    brand: BrandConfig = Field(default_factory=BrandConfig)
    layout_mappings: dict[str, LayoutMapping] = Field(default_factory=dict)
    content_type_routing: dict[str, str] = Field(default_factory=dict)
    requires_branding_slide: bool = True
    branding_layout_index: int | None = None
    fallback_layout_index: int = 2
    fallback_layout_name: str = "bullet_scene"