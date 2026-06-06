"""Gate 1: SCAN — Inventory and validate input landscape PPTX."""

from .scanner import scan_slide, scan_all_slides
from .pptx_parser import parse_slide
from .shape_classifier import classify_shape
from .number_extractor import extract_numbers
from .theme_extractor import extract_theme
from .image_extractor import extract_images_from_pptx, extract_slide_images

__all__ = [
    "scan_slide",
    "scan_all_slides",
    "parse_slide",
    "classify_shape",
    "extract_numbers",
    "extract_theme",
    "extract_images_from_pptx",
    "extract_slide_images",
]