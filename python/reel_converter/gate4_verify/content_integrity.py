"""Check content integrity: title, bullets, images preserved in output."""

from __future__ import annotations

from ..schemas.fingerprint import SlideFingerprint
from ..schemas.scene_plan import ScenePlan
from ..schemas.render_result import RenderedScene


def check_content_integrity(
    fingerprint: SlideFingerprint,
    scene_plan: ScenePlan,
    rendered: list[RenderedScene],
) -> dict:
    all_output_text = " ".join(
        " ".join(s.placeholders_filled.values()) for s in rendered
    ).lower()

    title_match = False
    if fingerprint.title_text:
        title_words = fingerprint.title_text.lower().split()[:3]
        title_match = any(w in all_output_text for w in title_words)
    else:
        title_match = True

    missing_bullets = []
    for bullet in fingerprint.bullet_items:
        bullet_lower = bullet.lower()
        found = False
        for word in bullet_lower.split()[:3]:
            if word in all_output_text:
                found = True
                break
        if not found:
            missing_bullets.append(bullet)

    all_images_present = True
    missing_images = []
    for img in fingerprint.image_names:
        found = any(img in str(s.images_inserted) for s in rendered)
        if not found:
            all_images_present = False
            missing_images.append(img)

    all_output_words = all_output_text.split()
    original_words = " ".join(fingerprint.bullet_items).lower().split()
    missing_words = [w for w in set(original_words) if len(w) > 4 and w not in all_output_words]

    return {
        "title_match": title_match,
        "all_bullets_present": len(missing_bullets) == 0,
        "all_images_present": all_images_present,
        "missing_words": missing_words[:10],
        "missing_images": missing_images,
    }