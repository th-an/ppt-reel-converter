"""Deterministic rule engine for mapping landscape slides to reel scenes."""

from __future__ import annotations

from ..schemas.fingerprint import SlideFingerprint
from ..schemas.scene_plan import Scene
from ..schemas.template_config import TemplateConfig

BULLETS_MAX_PER_SCENE = 3
TITLE_MAX_WORDS = 6


def apply_rules(
    fingerprint: SlideFingerprint,
    template_config: TemplateConfig,
) -> list[Scene]:
    content_type = fingerprint.content_type
    routing = template_config.content_type_routing
    layout_name = routing.get(content_type, template_config.fallback_layout_name)
    fingerprint.primary_color

    scenes = []

    if content_type == "title_only":
        scenes.append(Scene(
            layout=layout_name or "title_scene",
            headline=_truncate(fingerprint.title_text, TITLE_MAX_WORDS),
        ))

    elif content_type == "bullets_with_image":
        scenes.append(Scene(
            layout=_get_layout(routing, "stat_scene"),
            stat_number=fingerprint.unique_numbers[0] if fingerprint.unique_numbers else "",
            stat_label=_truncate(fingerprint.title_text, TITLE_MAX_WORDS),
        ))
        chunks = _chunk_list(fingerprint.bullet_items, BULLETS_MAX_PER_SCENE)
        for chunk in chunks:
            scenes.append(Scene(
                layout=_get_layout(routing, "bullet_scene"),
                headline=_truncate(fingerprint.title_text, TITLE_MAX_WORDS),
                body_items=chunk,
            ))
        for img_name in fingerprint.image_names:
            scenes.append(Scene(
                layout=_get_layout(routing, "image_scene"),
                image_name=img_name,
                image_crop="center",
            ))

    elif content_type == "bullets":
        chunks = _chunk_list(fingerprint.bullet_items, BULLETS_MAX_PER_SCENE)
        for i, chunk in enumerate(chunks):
            headline = fingerprint.title_text if i == 0 else f"{fingerprint.title_text} (cont'd)" if fingerprint.title_text else None
            scenes.append(Scene(
                layout=_get_layout(routing, "bullet_scene"),
                headline=_truncate(headline, TITLE_MAX_WORDS),
                body_items=chunk,
            ))

    elif content_type == "stat_with_context":
        for num in fingerprint.unique_numbers[:2]:
            scenes.append(Scene(
                layout=_get_layout(routing, "stat_scene"),
                stat_number=num,
                stat_label=_truncate(fingerprint.title_text, TITLE_MAX_WORDS),
            ))
        remaining = fingerprint.bullet_items[BULLETS_MAX_PER_SCENE:]
        if remaining:
            scenes.append(Scene(
                layout=_get_layout(routing, "bullet_scene"),
                headline=_truncate(fingerprint.title_text, TITLE_MAX_WORDS),
                body_items=remaining[:BULLETS_MAX_PER_SCENE],
            ))

    elif content_type == "image_only":
        for img_name in fingerprint.image_names:
            scenes.append(Scene(
                layout=_get_layout(routing, "image_scene"),
                image_name=img_name,
                image_crop="center",
                caption=_truncate(fingerprint.title_text, TITLE_MAX_WORDS),
            ))

    elif content_type == "table":
        scenes.append(Scene(
            layout=_get_layout(routing, "stat_scene"),
            stat_number=fingerprint.unique_numbers[0] if fingerprint.unique_numbers else "",
            stat_label=_truncate(fingerprint.title_text, TITLE_MAX_WORDS),
        ))
        for row in fingerprint.table_data[:2]:
            for cell in row:
                if cell.strip():
                    scenes.append(Scene(
                        layout=_get_layout(routing, "bullet_scene"),
                        headline=_truncate(fingerprint.title_text, TITLE_MAX_WORDS),
                        body_items=[cell.strip()],
                    ))
                    break

    elif content_type == "chart_heavy":
        for num in fingerprint.unique_numbers[:3]:
            scenes.append(Scene(
                layout=_get_layout(routing, "stat_scene"),
                stat_number=num,
                stat_label=_truncate(fingerprint.title_text, TITLE_MAX_WORDS),
            ))

    else:
        scenes.append(Scene(
            layout=template_config.fallback_layout_name,
            headline=_truncate(fingerprint.title_text, TITLE_MAX_WORDS) or "Content",
        ))

    if not scenes:
        scenes.append(Scene(
            layout=template_config.fallback_layout_name,
            headline=_truncate(fingerprint.title_text, TITLE_MAX_WORDS) or "Slide",
        ))

    return scenes


def _get_layout(routing: dict[str, str], content_type: str) -> str:
    return routing.get(content_type, content_type)


def _truncate(text: str | None, max_words: int) -> str | None:
    if not text:
        return None
    words = text.split()
    if len(words) <= max_words:
        return text
    return " ".join(words[:max_words]) + "..."


def _chunk_list(items: list, chunk_size: int) -> list[list]:
    return [items[i:i + chunk_size] for i in range(0, len(items), chunk_size)]