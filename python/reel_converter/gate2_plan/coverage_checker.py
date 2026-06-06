"""Verify that a scene plan covers all content from the original slide."""

from __future__ import annotations

from ..schemas.fingerprint import SlideFingerprint
from ..schemas.scene_plan import Scene, CoverageDeclaration


def check_coverage(
    fingerprint: SlideFingerprint,
    scenes: list[Scene],
) -> CoverageDeclaration:
    title_preserved = False
    title_text = None
    all_bullets_addressed = True
    all_images_addressed = True
    all_numbers_preserved = True
    numbers_found = set()

    if fingerprint.title_text:
        for scene in scenes:
            scene_text = " ".join([
                scene.headline or "",
                scene.stat_label or "",
                scene.cta_headline or "",
                scene.quote_text or "",
            ]).lower()
            title_words = fingerprint.title_text.lower().split()[:3]
            if any(w in scene_text for w in title_words):
                title_preserved = True
                title_text = fingerprint.title_text
                break
    else:
        title_preserved = True

    if fingerprint.bullet_items:
        for bullet in fingerprint.bullet_items:
            found = False
            bullet_l = bullet.lower()
            for scene in scenes:
                for item in (scene.body_items or []):
                    if any(w in item.lower() for w in bullet_l.split()[:3]):
                        found = True
                        break
                if found:
                    break
            if not found:
                all_bullets_addressed = False

    if fingerprint.image_names:
        scene_image_names = set()
        for scene in scenes:
            if scene.image_name:
                scene_image_names.add(scene.image_name)
        for img_name in fingerprint.image_names:
            if img_name not in scene_image_names:
                all_images_addressed = False

    if fingerprint.unique_numbers:
        all_scene_text = ""
        for scene in scenes:
            all_scene_text += " ".join([
                scene.headline or "",
                " ".join(scene.body_items or []),
                scene.stat_number or "",
                scene.stat_label or "",
                scene.stat_sublabel or "",
                scene.quote_text or "",
                scene.cta_headline or "",
                scene.cta_subheadline or "",
                scene.image_caption or "",
            ])
        for num in fingerprint.unique_numbers:
            if num in all_scene_text:
                numbers_found.add(num)
        all_numbers_preserved = len(numbers_found) >= len(fingerprint.unique_numbers)

    estimated_words = sum(
        len((s.headline or "").split()) + len(" ".join(s.body_items or []).split())
        + len((s.stat_number or "").split()) + len((s.stat_label or "").split())
        for s in scenes
    )

    return CoverageDeclaration(
        title_preserved=title_preserved,
        title_text=title_text,
        all_bullets_addressed=all_bullets_addressed,
        all_images_addressed=all_images_addressed,
        all_numbers_preserved=all_numbers_preserved,
        numbers_list=sorted(numbers_found),
        total_scenes=len(scenes),
        estimated_total_words=estimated_words,
    )