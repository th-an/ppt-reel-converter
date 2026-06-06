"""Binary search for optimal font size that fits content within placeholder bounds."""

from __future__ import annotations


def calculate_fit_font_size(
    text: str,
    max_width_pt: float,
    max_height_pt: float,
    initial_size_pt: float = 18.0,
    min_size_pt: float = 14.0,
    font_name: str = "Aptos",
    step: float = 1.0,
) -> float:
    low = min_size_pt
    high = initial_size_pt
    best_size = min_size_pt

    while low <= high:
        mid = (low + high) / 2
        if _text_fits(text, mid, max_width_pt, max_height_pt, font_name):
            best_size = mid
            low = mid + step
        else:
            high = mid - step

    return best_size


def _text_fits(
    text: str,
    font_size_pt: float,
    max_width_pt: float,
    max_height_pt: float,
    font_name: str,
) -> bool:
    lines = text.split("\n")
    char_width_pt = font_size_pt * 0.6
    line_height_pt = font_size_pt * 1.2
    total_height = len(lines) * line_height_pt

    if total_height > max_height_pt:
        return False

    for line in lines:
        line_width = len(line) * char_width_pt
        if line_width > max_width_pt:
            return False

    return True


def shrink_text_to_fit(
    text: str,
    max_width_pt: float,
    max_height_pt: float,
    initial_size_pt: float = 18.0,
    min_size_pt: float = 14.0,
) -> tuple[str, float]:
    font_size = calculate_fit_font_size(
        text, max_width_pt, max_height_pt, initial_size_pt, min_size_pt,
    )
    if font_size >= min_size_pt:
        return text, font_size
    words = text.split()
    truncated = " ".join(words[:len(words) * 2 // 3]) + "..."
    font_size = calculate_fit_font_size(
        truncated, max_width_pt, max_height_pt, initial_size_pt, min_size_pt,
    )
    return truncated, font_size