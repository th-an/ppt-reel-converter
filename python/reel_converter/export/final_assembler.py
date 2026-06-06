"""Assemble approved scenes into final PPTX file."""

from __future__ import annotations

from pathlib import Path

from pptx import Presentation

from ..schemas.generation_result import FinalReport


def assemble_final_pptx(
    template_path: str,
    output_path: str,
    report: FinalReport,
) -> str:
    prs = Presentation(template_path)

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    prs.save(str(output))
    return str(output)