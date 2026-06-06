#!/usr/bin/env python3
"""Test the interactive content editor."""

import sys
sys.path.insert(0, "python")

from reel_converter.gate2_plan.content_editor import (
    edit_scene_text,
    edit_scene_body_item,
    remove_scene_body_item,
    add_scene_body_item,
)
from reel_converter.schemas.scene_plan import Scene

# Create a test scene
scene = Scene(
    layout="title_and_content",
    headline="Original Headline",
    body_items=["Item 1", "Item 2", "Item 3"],
    stat_number="$12M",
    stat_label="Revenue",
)

print("Original scene:")
print(f"  Headline: {scene.headline}")
print(f"  Body: {scene.body_items}")
print(f"  Stat: {scene.stat_number} - {scene.stat_label}")

# Edit headline
scene = edit_scene_text(scene, headline="Edited Headline")
print("\nAfter headline edit:")
print(f"  Headline: {scene.headline}")

# Edit body item
scene = edit_scene_body_item(scene, 1, "Edited Item 2")
print("\nAfter body item edit:")
print(f"  Body: {scene.body_items}")

# Remove body item
scene = remove_scene_body_item(scene, 2)
print("\nAfter removing item 3:")
print(f"  Body: {scene.body_items}")

# Add body item
scene = add_scene_body_item(scene, "New Item", index=1)
print("\nAfter adding new item at index 1:")
print(f"  Body: {scene.body_items}")

# Edit stat
scene = edit_scene_text(scene, stat_number="$15M", stat_label="Updated Revenue")
print("\nAfter stat edit:")
print(f"  Stat: {scene.stat_number} - {scene.stat_label}")

print("\n✅ Content editor test passed!")
