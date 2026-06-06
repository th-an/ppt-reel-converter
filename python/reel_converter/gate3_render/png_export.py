"""PNG export using LibreOffice in headless mode."""

from __future__ import annotations

import subprocess
import os
import tempfile
from pathlib import Path


def export_pptx_to_pngs(
    pptx_path: str,
    output_dir: str,
    dpi: int = 150,
) -> list[str]:
    """Export PPTX slides to PNG images using LibreOffice.
    
    LibreOffice by default only exports the first slide with PNG.
    We use a workaround: convert to PDF first, then convert each PDF page to PNG.
    
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
    
    try:
        # Step 1: Convert PPTX to PDF first
        with tempfile.TemporaryDirectory() as tmp_dir:
            pdf_result = subprocess.run(
                [
                    "soffice",
                    "--headless",
                    "--convert-to", "pdf",
                    "--outdir", tmp_dir,
                    str(pptx_path),
                ],
                capture_output=True,
                text=True,
                timeout=60,
            )
            
            if pdf_result.returncode != 0:
                print(f"LibreOffice PDF export failed: {pdf_result.stderr}")
                return []
            
            # Find the generated PDF
            pdf_files = list(Path(tmp_dir).glob("*.pdf"))
            if not pdf_files:
                print("No PDF generated")
                return []
            
            pdf_path = pdf_files[0]
            
            # Step 2: Convert PDF to PNG using pdftoppm or ImageMagick
            # Try pdftoppm first (usually installed on macOS)
            try:
                result = subprocess.run(
                    [
                        "pdftoppm",
                        "-png",
                        "-r", str(dpi),
                        str(pdf_path),
                        str(output_dir / pptx_path.stem),
                    ],
                    capture_output=True,
                    text=True,
                    timeout=60,
                )
                
                if result.returncode == 0:
                    # pdftoppm naming: base-1.png, base-2.png, etc.
                    png_files = sorted(output_dir.glob(f"{pptx_path.stem}-*.png"))
                    return [str(p) for p in png_files]
            except FileNotFoundError:
                pass
            
            # Fallback: Try ImageMagick
            try:
                result = subprocess.run(
                    [
                        "convert",
                        "-density", str(dpi),
                        str(pdf_path),
                        str(output_dir / f"{pptx_path.stem}.png"),
                    ],
                    capture_output=True,
                    text=True,
                    timeout=60,
                )
                
                if result.returncode == 0:
                    # ImageMagick generates: base-0.png, base-1.png, etc.
                    png_files = sorted(output_dir.glob(f"{pptx_path.stem}-*.png"))
                    return [str(p) for p in png_files]
            except FileNotFoundError:
                pass
            
            # Last resort: try soffice with filter for PNG
            png_result = subprocess.run(
                [
                    "soffice",
                    "--headless",
                    "--convert-to", "png:impress_png_Export",
                    "--outdir", str(output_dir),
                    str(pptx_path),
                ],
                capture_output=True,
                text=True,
                timeout=60,
            )
            
            if png_result.returncode == 0:
                png_files = sorted(output_dir.glob(f"{pptx_path.stem}*.png"))
                return [str(p) for p in png_files]
            
            print("All PNG export methods failed")
            return []
    
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
