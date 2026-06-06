#!/usr/bin/env python3
"""CLI for converting PPTX to Instagram Reel format.

Usage:
    python scripts/convert_pptx.py <input.pptx> --output <output_dir>
    python scripts/convert_pptx.py <input.pptx> --output <output_dir> --model gpt-4o
    python scripts/convert_pptx.py <input.pptx> --output <output_dir> --preset fast
    python scripts/convert_pptx.py <input.pptx> --output <output_dir> --export-png
"""

import sys
import argparse
import json
from pathlib import Path

sys.path.insert(0, "python")

from reel_converter.pipeline.orchestrator import Orchestrator
from reel_converter.profile import profile_template
from reel_converter.gate3_render.png_export import export_pptx_to_pngs
from reel_converter.schemas.template_config import TemplateConfig


def main():
    parser = argparse.ArgumentParser(description="Convert PPTX to Instagram Reel format")
    parser.add_argument("input", help="Input PPTX file")
    parser.add_argument("--output", "-o", default="output", help="Output directory")
    parser.add_argument("--template", default="reel_clean", help="Template name")
    parser.add_argument("--model", default="auto", help="AI model to use")
    parser.add_argument("--preset", default="balanced", help="Model preset")
    parser.add_argument("--temperature", type=float, default=0.7, help="Temperature")
    parser.add_argument("--export-png", action="store_true", help="Also export PNG images")
    parser.add_argument("--api-key", help="API key (or set OPENCODE_API_KEY env var)")
    parser.add_argument("--api-base", help="API base URL")
    parser.add_argument("--auto-approve", action="store_true", help="Auto-approve slides with score >= 80")
    parser.add_argument("--auto-approve-threshold", type=float, default=80.0, help="Auto-approve threshold (default: 80)")
    
    args = parser.parse_args()
    
    # Validate input
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file not found: {args.input}")
        sys.exit(1)
    
    # Create output directory
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Load template
    template_config = _load_template(args.template)
    
    print(f"🎯 Converting {args.input} to Reel format")
    print(f"📐 Template: {args.template} ({template_config.dimensions.width_emu} x {template_config.dimensions.height_emu} EMU)")
    print(f"🤖 Model: {args.model} (preset: {args.preset})")
    if args.auto_approve:
        print(f"⚡ Auto-approve: enabled (threshold: {args.auto_approve_threshold})")
    print()
    
    # Initialize orchestrator
    orchestrator = Orchestrator(
        template_config=template_config,
        model=args.model,
        preset=args.preset,
        temperature=args.temperature,
        api_key=args.api_key,
        auto_approve_threshold=args.auto_approve_threshold if args.auto_approve else 999.0,
    )
    
    # Process each slide
    all_scenes = []
    slide_results = []
    
    # Scan all slides
    fingerprints = orchestrator.scan_all(str(input_path))
    
    print(f"📄 Found {len(fingerprints)} slides")
    print()
    
    # Process each slide
    for slide_idx, fingerprint in enumerate(fingerprints):
        slide_num = slide_idx + 1
        print(f"--- Slide {slide_num}/{len(fingerprints)} ({fingerprint.content_type}) ---")
        
        # Process slide through all 4 gates
        result = orchestrator.process_slide(fingerprint, use_ai=False)
        
        plan = result.scene_plan
        print(f"  📋 Plan: {len(plan.scenes)} scene(s)")
        for scene in plan.scenes:
            print(f"    - {scene.layout}: {scene.headline or scene.stat_number or scene.body_items or 'image'}")
        
        # Render individual slide scenes
        output_pptx = str(output_dir / f"slide_{slide_num}_scenes.pptx")
        from reel_converter.gate3_render import render_scenes
        rendered, pre_quality = render_scenes(
            scene_plan=plan,
            fingerprint=fingerprint,
            template_config=template_config,
            output_path=output_pptx,
        )
        
        print(f"  ✅ Passed: {pre_quality.passed}")
        print(f"  💾 Output: {output_pptx}")
        
        slide_results.append({
            "slide": slide_num,
            "scenes": len(plan.scenes),
            "passed": pre_quality.passed,
            "output": output_pptx,
        })
        
        all_scenes.extend(plan.scenes)
        print()
    
    # Combine all scenes into a single PPTX
    combined_pptx = str(output_dir / "combined_reel.pptx")
    _combine_scenes(all_scenes, template_config, combined_pptx)
    print(f"🎬 Combined reel: {combined_pptx}")
    
    # Export PNGs if requested
    if args.export_png:
        print(f"\n🖼️  Exporting PNGs...")
        pngs = export_pptx_to_pngs(combined_pptx, str(output_dir / "pngs"))
        if pngs:
            print(f"  Exported {len(pngs)} PNGs to {output_dir / 'pngs'}")
        else:
            print("  ⚠️ PNG export failed (LibreOffice not installed?)")
    
    # Save summary
    summary = {
        "input": str(input_path),
        "template": args.template,
        "model": args.model,
        "preset": args.preset,
        "total_slides": len(fingerprints),
        "total_scenes": len(all_scenes),
        "slide_results": slide_results,
        "combined_output": combined_pptx,
    }
    
    summary_path = output_dir / "summary.json"
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2)
    
    print(f"\n📊 Summary saved to {summary_path}")
    print(f"\n✅ Conversion complete! {len(all_scenes)} reel scenes from {len(fingerprints)} slides")


def _load_template(template_name: str) -> TemplateConfig:
    """Load template configuration."""
    template_dir = Path("python/reel_converter/templates")
    config_path = template_dir / f"{template_name}_config.json"
    
    if not config_path.exists():
        config_path = template_dir / "reel_clean_config.json"
    
    import json
    with open(config_path) as f:
        data = json.load(f)
    
    return TemplateConfig(**data)


def _combine_scenes(scenes, template_config, output_path):
    """Combine all scenes into a single PPTX file."""
    from reel_converter.gate3_render.pptx_writer import write_scenes_to_pptx
    from reel_converter.schemas.scene_plan import ScenePlan, Scene, CoverageDeclaration
    from reel_converter.schemas.fingerprint import SlideFingerprint
    
    # Create a dummy ScenePlan with required fields
    scene_plan = ScenePlan(
        slide_number=1,
        original_fingerprint=SlideFingerprint(
            slide_number=1,
            content_type="combined",
        ),
        scenes=scenes,
        coverage=CoverageDeclaration(total_scenes=len(scenes)),
    )
    
    write_scenes_to_pptx(
        scene_plan=scene_plan,
        template_config=template_config,
        output_path=output_path,
    )


if __name__ == "__main__":
    main()
