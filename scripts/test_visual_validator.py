import sys
sys.path.insert(0, "python")

from reel_converter.gate4_verify.visual_validator import validate_pptx_visual

# Test on the generated reel
result = validate_pptx_visual("output_image3/combined_reel.pptx")

print(f"Visual Validation: {'✅ PASSED' if result['passed'] else '❌ FAILED'}")
print(f"Overflow detections: {result['overflow_count']}")

if result['overflows']:
    print("\nOverflow details:")
    for o in result['overflows']:
        print(f"  Slide {o['slide']} ({o['severity']}): {o['shape']}")
        print(f"    Text: {o['text_preview']}")
        print(f"    Estimated: {o['estimated_height']} vs Shape: {o['shape_height']} (ratio: {o['overflow_ratio']})")

print(f"\nRecommendations:")
for rec in result['recommendations']:
    print(f"  • {rec}")
