"""Export PPTX slides to PNG images using LibreOffice headless."""

from __future__ import annotations

import subprocess
from pathlib import Path


def export_pngs(pptx_path: str, output_dir: str, dpi: int = 150) -> list[str]:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    try:
        result = subprocess.run(
            [
                "soffice",
                "--headless",
                "--convert-to", "png",
                "--outdir", str(out),
                pptx_path,
            ],
            capture_output=True,
            text=True,
            timeout=60,
        )
        if result.returncode != 0:
            return _fallback_export(pptx_path, output_dir)
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return _fallback_export(pptx_path, output_dir)

    pngs = sorted(out.glob("*.png"))
    scene_pngs = []
    for i, png in enumerate(pngs, start=1):
        new_name = out / f"scene_{i:02d}.png"
        png.rename(new_name)
        scene_pngs.append(str(new_name))

    return scene_pngs


def _fallback_export(pptx_path: str, output_dir: str) -> list[str]:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    return []