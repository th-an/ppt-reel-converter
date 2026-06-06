"""Scan all slides in a PPTX file, creating fingerprints for each."""

from __future__ import annotations

from pathlib import Path

from pptx import Presentation

from ..schemas.fingerprint import SlideFingerprint
from .pptx_parser import parse_slide
from .shape_classifier import classify_shape
from .number_extractor import extract_numbers
from .theme_extractor import extract_theme


def scan_all_slides(file_path: str, template_style: str = "reel_clean") -> list[SlideFingerprint]:
    prs = Presentation(file_path)
    theme = extract_theme(prs)
    fingerprints = []
    for idx, slide in enumerate(prs.slides, start=1):
        fp = scan_slide(slide, idx, theme)
        fingerprints.append(fp)
    return fingerprints


def scan_slide(slide, slide_number: int, theme) -> SlideFingerprint:
    elements = parse_slide(slide)
    title_text = None
    body_texts = []
    bullet_items = []
    image_count = 0
    image_names = []
    table_count = 0
    table_data = []
    has_smart_art = False
    has_chart = False
    has_grouped_shapes = False
    has_connector = False
    fonts_used = []
    font_sizes = []
    all_text = []

    for el in elements:
        el_type = classify_shape(el)
        if el_type == "title" and el.get("text"):
            title_text = el["text"].strip()
            all_text.append(title_text)
        elif el_type == "body" and el.get("text"):
            body_texts.append(el["text"].strip())
            all_text.append(el["text"].strip())
            for para in el.get("paragraphs", []):
                text = para.get("text", "").strip()
                if text:
                    bullet_items.append(text)
        elif el_type == "image":
            image_count += 1
            name = el.get("name", f"image_{image_count}")
            image_names.append(name)
        elif el_type == "table":
            table_count += 1
            if el.get("rows"):
                table_data.append(el["rows"])
        elif el_type == "smart_art":
            has_smart_art = True
        elif el_type == "chart":
            has_chart = True
        elif el_type == "group":
            has_grouped_shapes = True
        elif el_type == "connector":
            has_connector = True

        if el.get("font_name"):
            fonts_used.append(el["font_name"])
        if el.get("font_size"):
            font_sizes.append(int(el["font_size"]))

    all_text_joined = " ".join(all_text)
    total_words = len(all_text_joined.split())
    total_chars = len(all_text_joined)
    unique_numbers = extract_numbers(all_text_joined)

    warnings = []
    if has_smart_art:
        warnings.append("SmartArt detected — will extract as image + text")
    if has_chart:
        warnings.append("Chart detected — will extract key statistics")
    if has_grouped_shapes:
        warnings.append("Grouped shapes detected — will process individually")

    from ..schemas.fingerprint import ElementType
    element_types = [classify_shape(el) for el in elements]

    content_type = _infer_content_type(
        title_text=title_text,
        bullet_items=bullet_items,
        image_count=image_count,
        table_count=table_count,
        has_chart=has_chart,
    )

    return SlideFingerprint(
        slide_number=slide_number,
        title_text=title_text,
        body_texts=body_texts,
        bullet_items=bullet_items,
        table_count=table_count,
        table_data=table_data,
        image_count=image_count,
        image_names=image_names,
        total_word_count=total_words,
        total_char_count=total_chars,
        unique_numbers=unique_numbers,
        content_type=content_type,
        element_count=len(elements),
        primary_color=theme.primary_color if theme else None,
        fonts_used=list(set(fonts_used)),
        font_sizes=sorted(set(font_sizes)),
        has_smart_art=has_smart_art,
        has_chart=has_chart,
        has_grouped_shapes=has_grouped_shapes,
        has_connector=has_connector,
        warnings=warnings,
    )


def _infer_content_type(
    title_text: str | None,
    bullet_items: list[str],
    image_count: int,
    table_count: int,
    has_chart: bool,
) -> str:
    if title_text and not bullet_items and image_count == 0:
        return "title_only"
    if bullet_items and image_count > 0:
        return "bullets_with_image"
    if bullet_items and len(bullet_items) <= 3:
        return "stat_with_context"
    if bullet_items:
        return "bullets"
    if image_count > 0 and not bullet_items:
        return "image_only"
    if table_count > 0:
        return "table"
    if has_chart:
        return "chart_heavy"
    if title_text:
        return "title_only"
    return "unknown"