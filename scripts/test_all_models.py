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

results = {}
for model_name, model_info in MODEL_REGISTRY.items():
    print(f"Testing {model_name} ({model_info['format']})...", end=" ")
    try:
        result = asyncio.run(get_layout_decision(
            fingerprint=fp,
            template_config=template_config,
            catalog_markdown="",
            api_key=os.environ.get('OPENCODE_API_KEY'),
            model=model_name,
            preset="fast" if model_info['type'] == 'fast' else 'balanced',
            temperature=0.3,
        ))
        scenes = len(result.get('scenes', []))
        print(f"✅ {scenes} scenes")
        results[model_name] = {"status": "success", "scenes": scenes}
    except Exception as e:
        print(f"❌ {str(e)[:50]}")
        results[model_name] = {"status": "failed", "error": str(e)[:100]}

print(f"\n{'='*60}")
print(f"SUMMARY: {sum(1 for r in results.values() if r['status'] == 'success')}/{len(results)} models passed")
print(f"{'='*60}")
for model_name, result in results.items():
    status = "✅" if result['status'] == 'success' else "❌"
    print(f"{status} {model_name}: {result['status']}")
