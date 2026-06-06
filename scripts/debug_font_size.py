import sys
sys.path.insert(0, "python")

from pptx import Presentation
from reel_converter.gate1_scan.pptx_parser import parse_slide

prs = Presentation("tests/fixtures/complex_test.pptx")
for idx, slide in enumerate(prs.slides, 1):
    print(f"\nSlide {idx}:")
    elements = parse_slide(slide, prs.slide_height)
    for el in elements:
        if el.get("text"):
            print(f"  '{el['text'][:50]}' → font_size={el.get('font_size')}, top={el.get('top')}, slide_height={el.get('slide_height')}")
