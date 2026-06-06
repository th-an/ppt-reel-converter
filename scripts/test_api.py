import os
import sys
sys.path.insert(0, "python")

import asyncio
from reel_converter.gate2_plan.ai_agent import get_layout_decision, MODEL_REGISTRY
from reel_converter.gate1_scan import scan_all_slides
from reel_converter.schemas.template_config import TemplateConfig
import json

# Load template config
template_config = TemplateConfig(**json.load(open("python/reel_converter/templates/reel_clean_config.json")))

# Scan a simple test
fingerprints = scan_all_slides("tests/fixtures/simple_test.pptx", "reel_clean")
fp = fingerprints[0]

print(f"Testing with slide: {fp.title_text}")
print(f"API Key: {os.environ.get('OPENCODE_API_KEY', 'not set')[:15]}...")
print()

# Test with a fast model
model_name = "deepseek-v4-flash"
print(f"Testing model: {model_name}")
print(f"Endpoint: {MODEL_REGISTRY[model_name]['endpoint']}")
print()

try:
    result = asyncio.run(get_layout_decision(
        fingerprint=fp,
        template_config=template_config,
        catalog_markdown="",
        api_key=os.environ.get('OPENCODE_API_KEY'),
        model=model_name,
        preset="fast",
        temperature=0.3,
    ))
    print(f"✅ SUCCESS")
    print(f"Scenes: {len(result.get('scenes', []))}")
    for scene in result.get('scenes', []):
        print(f"  - {scene}")
    print(f"Reasoning: {result.get('reasoning', 'N/A')}")
except Exception as e:
    print(f"❌ FAILED: {e}")
    import traceback
    traceback.print_exc()
