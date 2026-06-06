"""Orchestrate all Gate 4 checks and compute final score."""

from __future__ import annotations

from ..schemas.fingerprint import SlideFingerprint
from ..schemas.scene_plan import ScenePlan
from ..schemas.render_result import RenderedScene
from ..schemas.verification_result import VerificationResult, ThemeConsistency, TypographyCheck, WhitespaceCheck
from .content_integrity import check_content_integrity
from .number_checker import check_numbers
from .theme_consistency import check_theme_consistency
from .typography_checker import check_typography
from .whitespace_analyzer import analyze_whitespace
from .scoring import compute_score


def verify_slide(
    fingerprint: SlideFingerprint,
    scene_plan: ScenePlan,
    rendered: list[RenderedScene],
    original_theme: dict | None = None,
) -> VerificationResult:
    integrity = check_content_integrity(fingerprint, scene_plan, rendered)
    numbers = check_numbers(fingerprint, scene_plan, rendered)
    theme = check_theme_consistency(fingerprint, rendered, original_theme)
    typography = check_typography(rendered)
    whitespace = analyze_whitespace(rendered)

    score = compute_score(
        content_integrity=integrity,
        numbers=numbers,
        theme=theme,
        typography=typography,
        whitespace=whitespace,
    )

    flags = []
    if not integrity["title_match"]:
        flags.append("Title not found in output")
    if not integrity["all_bullets_present"]:
        flags.append("Some bullets missing from output")
    if not numbers["all_present"]:
        flags.append(f"Missing numbers: {numbers['missing']}")
    if not theme["colors_match"]:
        flags.append("Theme colors do not match original")
    if whitespace["content_area_usage"] < 0.3:
        flags.append("Content density below 30% — scene may appear sparse")
    if whitespace["content_area_usage"] > 0.8:
        flags.append("Content density above 80% — scene may appear cramped")

    return VerificationResult(
        slide_number=fingerprint.slide_number,
        title_match=integrity["title_match"],
        all_bullets_present=integrity["all_bullets_present"],
        all_numbers_present=numbers["all_present"],
        all_images_present=integrity["all_images_present"],
        missing_words=integrity["missing_words"],
        missing_numbers=numbers["missing"],
        missing_images=integrity["missing_images"],
        text_overflow_scenes=[s.scene_number for s in rendered if s.has_text_overflow],
        font_size_ok=all(
            s.min_font_size_pt is None or s.min_font_size_pt >= 14.0
            for s in rendered
        ),
        safe_zone_ok=True,
        theme_consistency=ThemeConsistency(**theme),
        typography_hierarchy=TypographyCheck(**typography),
        whitespace_balance=WhitespaceCheck(**whitespace),
        score=score,
        passed=score >= 80,
        flags=flags,
    )