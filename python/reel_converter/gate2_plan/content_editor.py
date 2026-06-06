"""Inline content editor for editing text before rendering."""

from __future__ import annotations

from ..schemas.scene_plan import Scene


def edit_scene_text(
    scene: Scene,
    headline: str | None = None,
    body_items: list[str] | None = None,
    stat_number: str | None = None,
    stat_label: str | None = None,
    stat_sublabel: str | None = None,
    quote_text: str | None = None,
    quote_attribution: str | None = None,
    cta_headline: str | None = None,
    cta_subheadline: str | None = None,
) -> Scene:
    """Edit a scene's text content.
    
    Args:
        scene: The scene to edit
        headline: New headline text
        body_items: New body items list
        stat_number: New stat number
        stat_label: New stat label
        stat_sublabel: New stat sublabel
        quote_text: New quote text
        quote_attribution: New quote attribution
        cta_headline: New CTA headline
        cta_subheadline: New CTA subheadline
    
    Returns:
        Modified scene (new instance)
    """
    return Scene(
        layout=scene.layout,
        headline=headline if headline is not None else scene.headline,
        body_items=body_items if body_items is not None else scene.body_items,
        stat_number=stat_number if stat_number is not None else scene.stat_number,
        stat_label=stat_label if stat_label is not None else scene.stat_label,
        stat_sublabel=stat_sublabel if stat_sublabel is not None else scene.stat_sublabel,
        image_name=scene.image_name,
        image_crop=scene.image_crop,
        image_caption=scene.image_caption,
        quote_text=quote_text if quote_text is not None else scene.quote_text,
        quote_attribution=quote_attribution if quote_attribution is not None else scene.quote_attribution,
        cta_headline=cta_headline if cta_headline is not None else scene.cta_headline,
        cta_subheadline=cta_subheadline if cta_subheadline is not None else scene.cta_subheadline,
    )


def edit_scene_body_item(scene: Scene, index: int, new_text: str) -> Scene:
    """Edit a single body item in a scene.
    
    Args:
        scene: The scene to edit
        index: Index of the body item to edit
        new_text: New text for the body item
    
    Returns:
        Modified scene (new instance)
    """
    new_body_items = list(scene.body_items)
    if 0 <= index < len(new_body_items):
        new_body_items[index] = new_text
    return Scene(
        layout=scene.layout,
        headline=scene.headline,
        body_items=new_body_items,
        stat_number=scene.stat_number,
        stat_label=scene.stat_label,
        stat_sublabel=scene.stat_sublabel,
        image_name=scene.image_name,
        image_crop=scene.image_crop,
        image_caption=scene.image_caption,
        quote_text=scene.quote_text,
        quote_attribution=scene.quote_attribution,
        cta_headline=scene.cta_headline,
        cta_subheadline=scene.cta_subheadline,
    )


def remove_scene_body_item(scene: Scene, index: int) -> Scene:
    """Remove a body item from a scene.
    
    Args:
        scene: The scene to edit
        index: Index of the body item to remove
    
    Returns:
        Modified scene (new instance)
    """
    new_body_items = [item for i, item in enumerate(scene.body_items) if i != index]
    return Scene(
        layout=scene.layout,
        headline=scene.headline,
        body_items=new_body_items,
        stat_number=scene.stat_number,
        stat_label=scene.stat_label,
        stat_sublabel=scene.stat_sublabel,
        image_name=scene.image_name,
        image_crop=scene.image_crop,
        image_caption=scene.image_caption,
        quote_text=scene.quote_text,
        quote_attribution=scene.quote_attribution,
        cta_headline=scene.cta_headline,
        cta_subheadline=scene.cta_subheadline,
    )


def add_scene_body_item(scene: Scene, text: str, index: int | None = None) -> Scene:
    """Add a body item to a scene.
    
    Args:
        scene: The scene to edit
        text: Text to add
        index: Position to insert (default: append)
    
    Returns:
        Modified scene (new instance)
    """
    new_body_items = list(scene.body_items)
    if index is not None:
        new_body_items.insert(index, text)
    else:
        new_body_items.append(text)
    return Scene(
        layout=scene.layout,
        headline=scene.headline,
        body_items=new_body_items,
        stat_number=scene.stat_number,
        stat_label=scene.stat_label,
        stat_sublabel=scene.stat_sublabel,
        image_name=scene.image_name,
        image_crop=scene.image_crop,
        image_caption=scene.image_caption,
        quote_text=scene.quote_text,
        quote_attribution=scene.quote_attribution,
        cta_headline=scene.cta_headline,
        cta_subheadline=scene.cta_subheadline,
    )
