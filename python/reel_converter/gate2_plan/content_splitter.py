"""Split landscape slide content into multiple reel scenes."""

from __future__ import annotations

from ..schemas.fingerprint import SlideFingerprint
from ..schemas.scene_plan import Scene

MAX_BULLETS_PER_SCENE = 3
MAX_WORDS_PER_SCENE = 15


def split_slide_content(fingerprint: SlideFingerprint) -> list[dict]:
    content_type = fingerprint.content_type
    splits = []

    if content_type == "bullets_with_image":
        splits.append({
            "type": "stat",
            "content": {
                "headline": fingerprint.title_text,
                "numbers": fingerprint.unique_numbers[:1],
            },
        })
        for chunk in _chunk(fingerprint.bullet_items, MAX_BULLETS_PER_SCENE):
            splits.append({
                "type": "bullets",
                "content": {"headline": fingerprint.title_text, "items": chunk},
            })
        for img in fingerprint.image_names:
            splits.append({"type": "image", "content": {"image_name": img}})

    elif content_type == "bullets":
        for chunk in _chunk(fingerprint.bullet_items, MAX_BULLETS_PER_SCENE):
            splits.append({
                "type": "bullets",
                "content": {"headline": fingerprint.title_text, "items": chunk},
            })

    elif content_type in ("chart_heavy", "stat_with_context"):
        for num in fingerprint.unique_numbers[:3]:
            splits.append({
                "type": "stat",
                "content": {
                    "stat_number": num,
                    "stat_label": fingerprint.title_text,
                },
            })

    elif content_type == "table":
        splits.append({
            "type": "stat",
            "content": {
                "stat_number": fingerprint.unique_numbers[0] if fingerprint.unique_numbers else "",
                "stat_label": fingerprint.title_text,
            },
        })
        flat_items = [
            cell.strip()
            for row in fingerprint.table_data
            for cell in row
            if cell.strip()
        ][:MAX_BULLETS_PER_SCENE]
        if flat_items:
            splits.append({
                "type": "bullets",
                "content": {"headline": fingerprint.title_text, "items": flat_items},
            })

    elif content_type == "image_only":
        for img in fingerprint.image_names:
            splits.append({
                "type": "image",
                "content": {"image_name": img, "caption": fingerprint.title_text},
            })

    else:
        splits.append({
            "type": "title",
            "content": {"headline": fingerprint.title_text or "Content"},
        })

    if not splits:
        splits.append({
            "type": "title",
            "content": {"headline": fingerprint.title_text or "Slide"},
        })

    return splits


def _chunk(items: list, size: int) -> list[list]:
    return [items[i : i + size] for i in range(0, len(items), size)]