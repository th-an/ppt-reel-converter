import sys
sys.path.insert(0, "python")

from pathlib import Path

from reel_converter.pipeline.orchestrator import Orchestrator
from reel_converter.profile import profile_template
from reel_converter.schemas.template_config import TemplateConfig
from reel_converter.gate3_render import render_scenes

# Test full pipeline with actual PPTX output
print("=== End-to-End PPTX Generation Test ===\n")

# Profile template
config = profile_template("python/reel_converter/templates/reel_clean.pptx")
print(f"Template: {config.template_name}")
print(f"Dimensions: {config.dimensions.width_emu} x {config.dimensions.height_emu}")

# Create orchestrator
orchestrator = Orchestrator(config, api_key=None)

# Scan test fixture
fingerprints = orchestrator.scan_all("tests/fixtures/simple_test.pptx")
print(f"\nScanned {len(fingerprints)} slides")

# Process each slide and generate PPTX
output_dir = "output"
Path(output_dir).mkdir(parents=True, exist_ok=True)

for fp in fingerprints:
    print(f"\n--- Slide {fp.slide_number} ({fp.content_type}) ---")
    
    # Process through pipeline
    result = orchestrator.process_slide(fp, use_ai=False)
    
    # Generate actual PPTX
    output_path = f"{output_dir}/slide_{fp.slide_number}_scenes.pptx"
    
    if result.scene_plan:
        rendered, quality = render_scenes(
            scene_plan=result.scene_plan,
            fingerprint=fp,
            template_config=config,
            output_path=output_path,
        )
        
        print(f"  Scenes: {len(rendered)}")
        for r in rendered:
            print(f"    Scene {r.scene_number}: {r.layout_used}")
            print(f"      Filled: {list(r.placeholders_filled.keys())}")
        
        print(f"  Output: {output_path}")
        print(f"  Score: {result.verification.score}/100")
        print(f"  Passed: {result.verification.passed}")
        
        # Verify file exists
        if Path(output_path).exists():
            size = Path(output_path).stat().st_size
            print(f"  File size: {size} bytes")
        else:
            print(f"  ERROR: File not created!")

print("\n=== Test Complete ===")
print(f"Check output directory: {output_dir}/")

# List output files
from glob import glob
files = glob(f"{output_dir}/*.pptx")
print(f"\nGenerated files:")
for f in files:
    size = Path(f).stat().st_size
    print(f"  {f} ({size} bytes)")
