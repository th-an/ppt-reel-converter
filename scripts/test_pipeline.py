import sys
sys.path.insert(0, "python")

from reel_converter.pipeline.orchestrator import Orchestrator
from reel_converter.profile import profile_template
from reel_converter.schemas.template_config import TemplateConfig

# Test full pipeline
print("=== Full Pipeline Test ===")

# Profile template
config = profile_template("python/reel_converter/templates/reel_clean.pptx")
print(f"Template: {config.template_name}")
print(f"Dimensions: {config.dimensions.width_emu} x {config.dimensions.height_emu}")

# Create orchestrator
orchestrator = Orchestrator(config, api_key=None)

# Scan test fixture
fingerprints = orchestrator.scan_all("tests/fixtures/simple_test.pptx")
print(f"\nScanned {len(fingerprints)} slides")

# Process slide 1 (no AI)
print("\n=== Processing Slide 1 (title_only) ===")
result = orchestrator.process_slide(fingerprints[0], use_ai=False)
print(f"Scene plan: {len(result.scene_plan.scenes)} scenes")
for i, s in enumerate(result.scene_plan.scenes):
    print(f"  Scene {i+1}: {s.layout} - headline={s.headline}")
print(f"Coverage: title={result.scene_plan.coverage.title_preserved}, "
      f"bullets={result.scene_plan.coverage.all_bullets_addressed}")
print(f"Rendered: {len(result.rendered_scenes)} scenes")
print(f"Verification score: {result.verification.score}/100")
print(f"Passed: {result.verification.passed}")
print(f"Flags: {result.verification.flags}")

# Process slide 2 (bullets)
print("\n=== Processing Slide 2 (bullets) ===")
result = orchestrator.process_slide(fingerprints[1], use_ai=False)
print(f"Scene plan: {len(result.scene_plan.scenes)} scenes")
for i, s in enumerate(result.scene_plan.scenes):
    print(f"  Scene {i+1}: {s.layout} - headline={s.headline}, body={s.body_items}")
print(f"Coverage: title={result.scene_plan.coverage.title_preserved}, "
      f"bullets={result.scene_plan.coverage.all_bullets_addressed}")
print(f"Rendered: {len(result.rendered_scenes)} scenes")
print(f"Verification score: {result.verification.score}/100")
print(f"Passed: {result.verification.passed}")
print(f"Flags: {result.verification.flags}")

print("\n=== Pipeline Test Complete ===")
