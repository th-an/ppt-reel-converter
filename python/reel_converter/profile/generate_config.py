"""Generate config JSON and catalog markdown from a profiled template."""

from __future__ import annotations

import json
from pathlib import Path

from ..schemas.template_config import TemplateConfig


def generate_config(config: TemplateConfig, output_dir: str) -> tuple[str, str]:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    config_path = out / f"{config.template_name}_config.json"
    catalog_path = out / f"{config.template_name}_catalog.md"

    with open(config_path, "w") as f:
        json.dump(config.model_dump(), f, indent=2)

    catalog_md = _generate_catalog_markdown(config)
    catalog_path.write_text(catalog_md)

    return str(config_path), str(catalog_path)


def _generate_catalog_markdown(config: TemplateConfig) -> str:
    lines = [
        f"# {config.template_name} Layout Catalog",
        "",
        f"Dimensions: {config.dimensions.width_emu} × {config.dimensions.height_emu} EMU",
        f"Safe zone: top {config.safe_zone.top_pct:.0%}, bottom {config.safe_zone.bottom_pct:.0%}",
        "",
    ]

    for name, mapping in config.layout_mappings.items():
        lines.append(f"## Layout {mapping.layout_index}: {mapping.layout_name}")
        lines.append(f"- **Use when:** {_get_use_case(name)}")
        lines.append(f"- **Index:** {mapping.layout_index}")
        lines.append("")

    lines.append("## Content Type Routing")
    lines.append("")
    lines.append("| Content Type | Layout |")
    lines.append("|---|---|")
    for ct, layout_name in config.content_type_routing.items():
        lines.append(f"| {ct} | {layout_name} |")

    return "\n".join(lines)


def _get_use_case(layout_name: str) -> str:
    use_cases = {
        "title_scene": "Opening a reel, big statement, section divider",
        "stat_scene": "Highlighting a single number/metric",
        "bullet_scene": "Key points, 2-3 bullets maximum",
        "quote_scene": "Quote highlight with attribution",
        "image_scene": "Full-bleed image with optional caption",
        "cta_scene": "Call to action, closing slide",
        "list_scene": "Numbered items, 4 items maximum",
        "section_scene": "Section divider with number",
    }
    for key, desc in use_cases.items():
        if key in layout_name:
            return desc
    return "General purpose slide"