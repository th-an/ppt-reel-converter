"""OpenCode Go API client for AI layout decisions."""

from __future__ import annotations

import json

import httpx

from ..schemas.fingerprint import SlideFingerprint
from ..schemas.template_config import TemplateConfig

LAYOUT_SYSTEM_PROMPT = """You are a social media content designer specializing in 
Instagram Reels. You convert landscape presentation slides into vertical 9:16 reel 
scenes that are readable on a phone.

RULES:
1. ONE idea per scene. If a slide has 3+ distinct points, SPLIT it.
2. Maximum 15 words per scene. Condense aggressively.
3. All content MUST fit within safe zone (top 15% and bottom 20% are covered by Instagram UI).
4. Wide images -> center-crop to 9:16. Charts -> extract the single most important stat.
5. Tables -> convert to a list of key takeaways (max 3 items).
6. Every deck should start with a title_scene and end with cta_scene.
7. Preserve ALL numbers and key data from the original slide.
8. Preserve the original title or a condensed version of it.

Available layouts:
{catalog}

Respond ONLY with valid JSON:
{{
  "scenes": [
    {{
      "layout": "layout_name",
      "headline": "...",
      "body_items": ["item1", "item2"],
      "stat_number": "...",
      "stat_label": "...",
      "stat_sublabel": "...",
      "image_name": "...",
      "image_crop": "center|fit",
      "quote_text": "...",
      "quote_attribution": "...",
      "cta_headline": "...",
      "cta_subheadline": "..."
    }}
  ],
  "simplifications": [
    {{
      "original_content": "what was in the original",
      "simplified_to": "what it became",
      "reason": "why"
    }}
  ],
  "reasoning": "brief explanation"
}}"""


async def get_layout_decision(
    fingerprint: SlideFingerprint,
    template_config: TemplateConfig,
    catalog_markdown: str,
    api_key: str,
    model: str = "deepseek-v4-flash",
    base_url: str = "https://opencode.ai/zen/go/v1/chat/completions",
) -> dict:
    system_prompt = LAYOUT_SYSTEM_PROMPT.format(catalog=catalog_markdown)

    slide_description = json.dumps({
        "slide_number": fingerprint.slide_number,
        "title": fingerprint.title_text,
        "bullets": fingerprint.bullet_items,
        "numbers": fingerprint.unique_numbers,
        "images": fingerprint.image_names,
        "content_type": fingerprint.content_type,
        "total_words": fingerprint.total_word_count,
        "warnings": fingerprint.warnings,
    })

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            base_url,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": slide_description},
                ],
                "response_format": {"type": "json_object"},
                "temperature": 0.3,
            },
        )
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"]
        return json.loads(content)