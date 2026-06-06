"""Compute weighted composite score for Gate 4 verification."""

from __future__ import annotations

WEIGHTS = {
    "content_integrity": 0.40,
    "numbers": 0.10,
    "theme": 0.15,
    "typography": 0.15,
    "whitespace": 0.20,
}


def compute_score(
    content_integrity: dict,
    numbers: dict,
    theme: dict,
    typography: dict,
    whitespace: dict,
) -> float:
    integrity_score = 0.0
    integrity_max = 4.0
    if content_integrity.get("title_match"):
        integrity_score += 1.0
    if content_integrity.get("all_bullets_present"):
        integrity_score += 1.5
    if content_integrity.get("all_images_present"):
        integrity_score += 1.5
    integrity_pct = integrity_score / integrity_max

    numbers_pct = 1.0 if numbers.get("all_present", True) else 0.5

    theme_score = 0.0
    if theme.get("colors_match"):
        theme_score += 0.5
    if theme.get("fonts_match"):
        theme_score += 0.5
    if theme.get("background_preserved", True):
        theme_score += 0.5
    theme_pct = theme_score / 1.5

    typo_score = 0.0
    if typography.get("headlines_larger_than_body", True):
        typo_score += 0.4
    if typography.get("consistent_body_size", True):
        typo_score += 0.3
    if typography.get("no_all_caps_body", True):
        typo_score += 0.3
    typo_pct = typo_score / 1.0

    ws_usage = whitespace.get("content_area_usage", 0.5)
    if 0.4 <= ws_usage <= 0.7:
        ws_pct = 1.0
    elif 0.3 <= ws_usage <= 0.8:
        ws_pct = 0.7
    else:
        ws_pct = 0.4

    total = (
        integrity_pct * WEIGHTS["content_integrity"]
        + numbers_pct * WEIGHTS["numbers"]
        + theme_pct * WEIGHTS["theme"]
        + typo_pct * WEIGHTS["typography"]
        + ws_pct * WEIGHTS["whitespace"]
    )
    return round(total * 100, 1)