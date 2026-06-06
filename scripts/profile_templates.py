import sys
sys.path.insert(0, "python")

import json
from pathlib import Path

from reel_converter.profile import profile_template

# Profile each template
template_names = ["modern", "bold", "minimal", "corporate"]

for name in template_names:
    template_path = f"python/reel_converter/templates/reel_{name}.pptx"
    print(f"\nProfiling {name}...")
    
    # Create config using profiler
    config = profile_template(template_path)
    
    # Save config
    config_path = f"python/reel_converter/templates/reel_{name}_config.json"
    with open(config_path, 'w') as f:
        json.dump(config.model_dump(), f, indent=2)
    
    print(f"  Config saved to {config_path}")
    print(f"  Dimensions: {config.dimensions.width_emu} x {config.dimensions.height_emu}")
    print(f"  Layouts: {len(config.layout_mappings)}")
    for layout_name, mapping in config.layout_mappings.items():
        print(f"    - {layout_name}: index={mapping.layout_index}")

print("\nAll configs created!")
