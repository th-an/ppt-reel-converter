import os
import sys
sys.path.insert(0, "python")

import asyncio
from reel_converter.gate2_plan.ai_agent import get_layout_decision, MODEL_REGISTRY
from reel_converter.gate1_scan import scan_all_slides
from reel_converter.schemas.template_config import TemplateConfig
import json
import traceback

# Load template config
template_config = TemplateConfig(**json.load(open("python/reel_converter/templates/reel_clean_config.json")))

# Scan a simple test
fingerprints = scan_all_slides("tests/fixtures/simple_test.pptx", "reel_clean")
fp = fingerprints[0]

print(f"Testing with slide: {fp.title_text}")
print()

# Test models with verbose error output
models_to_test = [
    "deepseek-v4-pro",    # OpenAI format, capable
    "glm-5",              # OpenAI format, balanced
    "minimax-m3",         # Anthropic format, capable
]

for model_name in models_to_test:
    model_info = MODEL_REGISTRY[model_name]
    print(f"\nTesting {model_name} ({model_info['format']})...")
    print(f"  Endpoint: {model_info['endpoint']}")
    try:
        result = asyncio.run(
            asyncio.wait_for(
                get_layout_decision(
                    fingerprint=fp,
                    template_config=template_config,
                    catalog_markdown="",
                    api_key=os.environ.get('OPENCODE_API_KEY'),
                    model=model_name,
                    preset="balanced",
                    temperature=0.3,
                ),
                timeout=30
            )
        )
        scenes = len(result.get('scenes', []))
        print(f"  ✅ SUCCESS: {scenes} scenes")
    except Exception as e:
        print(f"  ❌ FAILED: {e}")
        traceback.print_exc()
