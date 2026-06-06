"""CLI entry point for the PPT Reel Converter."""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from pathlib import Path

from reel_converter.pipeline.orchestrator import Orchestrator
from reel_converter.pipeline.approval_manager import ApprovalManager
from reel_converter.pipeline.report_generator import generate_report, save_report
from reel_converter.profile import profile_template, generate_config
from reel_converter.schemas.template_config import TemplateConfig


def main():
    parser = argparse.ArgumentParser(description="PPT Reel Converter — Landscape to 9:16 Portrait")
    parser.add_argument("input", help="Path to landscape PPTX file")
    parser.add_argument("--template", default="reel_clean", help="Template style (default: reel_clean)")
    parser.add_argument("--output-dir", default="./output", help="Output directory")
    parser.add_argument("--api-key", default=None, help="OpenCode Go API key (optional)")
    parser.add_argument("--model", default="deepseek-v4-flash", help="OpenCode Go model")
    parser.add_argument("--use-ai", action="store_true", help="Use AI for layout decisions")
    parser.add_argument("--auto-approve", action="store_true", help="Auto-approve slides scoring >= 80")
    args = parser.parse_args()

    template_dir = Path(__file__).parent / "templates"
    template_path = str(template_dir / f"{args.template}.pptx")
    config_path = str(template_dir / f"{args.template}_config.json")

    if Path(config_path).exists():
        with open(config_path) as f:
            config_data = json.load(f)
        template_config = TemplateConfig(**config_data)
    else:
        print(f"Profiling template: {template_path}")
        template_config = profile_template(template_path)
        generate_config(template_config, str(template_dir))

    print(f"Scanning: {args.input}")
    orchestrator = Orchestrator(template_config, api_key=args.api_key)
    fingerprints = orchestrator.scan_all(args.input)

    print(f"Found {len(fingerprints)} slides")
    print(f"Template: {args.template}")
    print(f"AI: {'enabled' if args.use_ai else 'disabled'}")
    print()

    approval = ApprovalManager()

    for fp in fingerprints:
        print(f"Processing slide {fp.slide_number}/{len(fingerprints)}: {fp.content_type}")
        print(f"  Title: {fp.title_text or '(none)'}")
        print(f"  Elements: {fp.element_count}, Bullets: {len(fp.bullet_items)}, "
              f"Images: {fp.image_count}, Numbers: {len(fp.unique_numbers)}")
        if fp.warnings:
            for w in fp.warnings:
                print(f"  Warning: {w}")

        result = orchestrator.process_slide(fp, use_ai=args.use_ai)

        if result.verification:
            v = result.verification
            print(f"  Gate 4 Score: {v.score}/100 {'PASS' if v.passed else 'FLAG'}")
            if v.flags:
                for flag in v.flags:
                    print(f"    Flag: {flag}")

        if args.auto_approve and result.verification and result.verification.passed:
            orchestrator.approve_slide(fp.slide_number)
            print(f"  Auto-approved (score >= 80)")
        else:
            print(f"  Awaiting approval...")
            if result.verification and result.verification.score < 80:
                print(f"  ⚠ Score below 80. Manual review recommended.")
            answer = input(f"  Approve slide {fp.slide_number}? [y/s(skip)/r(retry)]: ").strip().lower()
            if answer in ("y", "yes", ""):
                orchestrator.approve_slide(fp.slide_number)
            elif answer in ("s", "skip"):
                orchestrator.skip_slide(fp.slide_number)
            else:
                result = orchestrator.process_slide(fp, use_ai=args.use_ai)

        orchestrator.results.append(result)
        print()

    report = generate_report(
        results=orchestrator.results,
        input_file=args.input,
        template_used=args.template,
    )

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    report_path = save_report(report, str(output_dir / "validation_report.json"))
    print(f"\nReport saved: {report_path}")
    print(f"Total slides: {report.total_slides_input}")
    print(f"Total scenes: {report.total_scenes_output}")
    print(f"Approved: {report.slides_approved}")
    print(f"Skipped: {report.slides_skipped}")
    print(f"Flagged: {report.slides_flagged}")
    print(f"Average score: {report.average_score}/100")


if __name__ == "__main__":
    main()