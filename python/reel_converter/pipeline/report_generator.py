"""Generate final validation report."""

from __future__ import annotations

import json
from pathlib import Path

from ..schemas.generation_result import FinalReport, SlideResult


def generate_report(
    results: list[SlideResult],
    input_file: str,
    template_used: str = "reel_clean",
) -> FinalReport:
    total_scenes = sum(len(r.rendered_scenes) for r in results)
    approved = sum(1 for r in results if r.approved)
    skipped = sum(1 for r in results if r.skipped)
    flagged = sum(1 for r in results if r.verification and not r.verification.passed)

    scores = {}
    for r in results:
        if r.verification:
            scores[r.slide_number] = r.verification.score

    avg_score = sum(scores.values()) / len(scores) if scores else 0.0

    return FinalReport(
        input_file=input_file,
        template_used=template_used,
        total_slides_input=len(results),
        total_scenes_output=total_scenes,
        slides_approved=approved,
        slides_skipped=skipped,
        slides_flagged=flagged,
        average_score=round(avg_score, 1),
        per_slide_results=results,
        per_slide_scores=scores,
    )


def save_report(report: FinalReport, output_path: str) -> str:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(report.model_dump(), f, indent=2, default=str)
    return str(path)