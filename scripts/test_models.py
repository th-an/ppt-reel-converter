import sys
sys.path.insert(0, "python")

from reel_converter.gate2_plan.ai_agent import (
    MODEL_REGISTRY,
    PRESETS,
    select_best_model,
    get_model_info,
    get_model_recommendation,
    estimate_cost,
)

print("=== OpenCode Go Multi-Model Support Test ===\n")

# Test 1: List all models
print("Test 1: All models registered")
print(f"Total models: {len(MODEL_REGISTRY)}")
for name, info in MODEL_REGISTRY.items():
    print(f"  ✓ {name:20s} {info['type']:8s} ${info['cost_per_1k']:.5f}/1K  {info['format']}")

# Test 2: Presets
print("\nTest 2: Model presets")
for preset, models in PRESETS.items():
    print(f"  {preset:10s}: {len(models)} models")

# Test 3: Model selection
print("\nTest 3: Model selection")
print(f"  Fast preset: {select_best_model('fast')}")
print(f"  Balanced preset: {select_best_model('balanced')}")
print(f"  Capable preset: {select_best_model('capable')}")
print(f"  Cheap preset: {select_best_model('cheap')}")
print(f"  With preferred: {select_best_model('balanced', 'glm-5')}")

# Test 4: Model info
print("\nTest 4: Model info")
info = get_model_info("deepseek-v4-flash")
print(f"  deepseek-v4-flash: {info}")

# Test 5: Cost estimation
print("\nTest 5: Cost estimation")
for model in ["deepseek-v4-flash", "glm-5", "deepseek-v4-pro"]:
    cost = estimate_cost(20, model)
    print(f"  {model:20s} 20 slides: ${cost['total_cost_usd']:.4f} (${cost['cost_per_slide']:.4f}/slide)")

# Test 6: Recommendations
print("\nTest 6: Model recommendations")
print(f"  Small deck (5 slides): {get_model_recommendation(5)}")
print(f"  Medium deck (20 slides): {get_model_recommendation(20)}")
print(f"  Large deck (50 slides): {get_model_recommendation(50)}")
print(f"  Budget priority: {get_model_recommendation(20, priority='cost')}")
print(f"  Quality priority: {get_model_recommendation(20, priority='quality')}")
print(f"  Speed priority: {get_model_recommendation(20, priority='speed')}")

print("\n=== All tests passed ===")
