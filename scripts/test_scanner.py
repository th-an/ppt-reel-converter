import sys
sys.path.insert(0, "python")

from reel_converter.gate1_scan import scan_all_slides
from reel_converter.profile import profile_template
from reel_converter.schemas.template_config import TemplateConfig

# Test 1: Scan the test fixture
print("=== Test 1: Scanning test fixture ===")
results = scan_all_slides("tests/fixtures/simple_test.pptx")
print(f"Slides found: {len(results)}")
for fp in results:
    print(f"\nSlide {fp.slide_number}: {fp.content_type}")
    print(f"  Title: {fp.title_text}")
    print(f"  Bullets: {len(fp.bullet_items)}")
    print(f"  Images: {fp.image_count}")
    print(f"  Numbers: {fp.unique_numbers}")
    print(f"  Words: {fp.total_word_count}")
    print(f"  Warnings: {fp.warnings}")

# Test 2: Profile the template
print("\n=== Test 2: Profiling template ===")
config = profile_template("python/reel_converter/templates/reel_clean.pptx")
print(f"Template: {config.template_name}")
print(f"Dimensions: {config.dimensions.width_emu} x {config.dimensions.height_emu}")
print(f"Layouts: {list(config.layout_mappings.keys())}")
print(f"Routing: {config.content_type_routing}")

print("\n=== All tests passed ===")
