"""Extract images from PPTX slides and return as base64 encoded blobs."""

from __future__ import annotations

import base64
from pathlib import Path

from pptx.slide import Slide


def extract_images(slide: Slide) -> dict[str, str]:
    images = {}
    idx = 0
    for shape in slide.shapes:
        try:
            if hasattr(shape, "image"):
                img = shape.image
                content_type = img.content_type
                blob = img.blob
                ext = _content_type_to_ext(content_type)
                name = f"image_{slide.slide_id}_{idx}.{ext}"
                images[name] = base64.b64encode(blob).decode("utf-8")
                idx += 1
        except Exception:
            continue
    return images


def extract_all_images_to_files(prs, output_dir: str) -> dict[str, str]:
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    image_paths = {}
    for slide_idx, slide in enumerate(prs.slides, start=1):
        for shape in slide.shapes:
            try:
                if hasattr(shape, "image"):
                    img = shape.image
                    content_type = img.content_type
                    blob = img.blob
                    ext = _content_type_to_ext(content_type)
                    name = f"slide{slide_idx}_image.{ext}"
                    filepath = output / name
                    filepath.write_bytes(blob)
                    image_paths[name] = str(filepath)
            except Exception:
                continue
    return image_paths


def _content_type_to_ext(content_type: str) -> str:
    mapping = {
        "image/png": "png",
        "image/jpeg": "jpg",
        "image/gif": "gif",
        "image/tiff": "tiff",
        "image/bmp": "bmp",
        "image/svg+xml": "svg",
    }
    return mapping.get(content_type, "png")