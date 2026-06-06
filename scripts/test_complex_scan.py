import sys
sys.path.insert(0, "python")

from reel_converter.gate1_scan import scan_all_slides

fingerprints = scan_all_slides("tests/fixtures/complex_test.pptx", "reel_clean")

print(f"Scanned {len(fingerprints)} slides:\n")
for fp in fingerprints:
    print(f"Slide {fp.slide_number}: {fp.content_type}")
    print(f"  Title: {fp.title_text}")
    print(f"  Bullets: {len(fp.bullet_items)} items")
    if fp.bullet_items:
        for item in fp.bullet_items:
            print(f"    • {item}")
    print(f"  Numbers: {fp.unique_numbers}")
    print(f"  Images: {fp.image_names}")
    print(f"  Table rows: {len(fp.table_data)}")
    if fp.table_data:
        for row in fp.table_data:
            print(f"    {row}")
    print(f"  Theme: primary={fp.primary_color}, fonts={fp.fonts_used}")
    print(f"  Warnings: {fp.warnings}")
    print()
