"""PNG export using LibreOffice in headless mode."""

from __future__ import annotations

import subprocess
import os
from pathlib import Path


def export_pptx_to_pngs(
    pptx_path: str,
    output_dir: str,
    dpi: int = 150,
) -> list[str]:
    """Export PPTX slides to PNG images using LibreOffice.
    
    Args:
        pptx_path: Path to the PPTX file
        output_dir: Directory to save PNG images
        dpi: DPI for the export (default 150)
    
    Returns:
        List of paths to the exported PNG files
    """
    pptx_path = Path(pptx_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # LibreOffice headless export
    # LibreOffice command: soffice --headless --convert-to png --outdir /path /input.pptx
    try:
        result = subprocess.run(
            [
                "soffice",
                "--headless",
                "--convert-to", "png",
                "--outdir", str(output_dir),
                str(pptx_path),
            ],
            capture_output=True,
            text=True,
            timeout=60,
        )
        
        if result.returncode != 0:
            print(f"LibreOffice export failed: {result.stderr}")
            return []
        
        # Find generated PNGs
        base_name = pptx_path.stem
        png_files = sorted(output_dir.glob(f"{base_name}*.png"))
        
        return [str(p) for p in png_files]
    
    except FileNotFoundError:
        print("LibreOffice not found. Install it with: brew install --cask libreoffice")
        return []
    except subprocess.TimeoutExpired:
        print("LibreOffice export timed out")
        return []


def export_slide_to_png(
    pptx_path: str,
    slide_index: int,
    output_path: str,
    dpi: int = 150,
) -> bool:
    """Export a single slide to PNG.
    
    Args:
        pptx_path: Path to the PPTX file
        slide_index: 0-based index of the slide to export
        output_path: Path to save the PNG
        dpi: DPI for the export
    
    Returns:
        True if successful
    """
    pptx_path = Path(pptx_path)
    output_dir = Path(output_path).parent
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Export all, then rename the specific one
    temp_dir = output_dir / "temp_export"
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    pngs = export_pptx_to_pngs(str(pptx_path), str(temp_dir), dpi)
    
    if slide_index < len(pngs):
        import shutil
        shutil.move(pngs[slide_index], output_path)
        # Clean up temp dir
        shutil.rmtree(temp_dir)
        return True
    
    return False
