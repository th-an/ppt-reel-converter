"""OpenCode Go API client — Multi-model support with optimized prompts."""

from __future__ import annotations

import json
import os
from typing import Literal

import httpx

from ..schemas.fingerprint import SlideFingerprint
from ..schemas.template_config import TemplateConfig

# Model registry with all OpenCode Go models
MODEL_REGISTRY = {
    # OpenAI-compatible endpoint (v1/chat/completions)
    "deepseek-v4-flash": {
        "format": "openai",
        "endpoint": "https://opencode.ai/zen/go/v1/chat/completions",
        "model_id": "deepseek-v4-flash",
        "type": "fast",  # Fast, cheap, good for most cases
        "cost_per_1k": 0.00014,
        "context": 128000,
    },
    "deepseek-v4-pro": {
        "format": "openai",
        "endpoint": "https://opencode.ai/zen/go/v1/chat/completions",
        "model_id": "deepseek-v4-pro",
        "type": "capable",  # More capable, slower
        "cost_per_1k": 0.00174,
        "context": 128000,
    },
    "glm-5": {
        "format": "openai",
        "endpoint": "https://opencode.ai/zen/go/v1/chat/completions",
        "model_id": "glm-5",
        "type": "balanced",  # Balanced quality/speed
        "cost_per_1k": 0.00100,
        "context": 128000,
    },
    "glm-5.1": {
        "format": "openai",
        "endpoint": "https://opencode.ai/zen/go/v1/chat/completions",
        "model_id": "glm-5.1",
        "type": "balanced",
        "cost_per_1k": 0.00140,
        "context": 128000,
    },
    "kimi-k2.5": {
        "format": "openai",
        "endpoint": "https://opencode.ai/zen/go/v1/chat/completions",
        "model_id": "kimi-k2.5",
        "type": "balanced",
        "cost_per_1k": 0.00060,
        "context": 256000,
    },
    "kimi-k2.6": {
        "format": "openai",
        "endpoint": "https://opencode.ai/zen/go/v1/chat/completions",
        "model_id": "kimi-k2.6",
        "type": "balanced",
        "cost_per_1k": 0.00095,
        "context": 256000,
    },
    "mimo-v2.5": {
        "format": "openai",
        "endpoint": "https://opencode.ai/zen/go/v1/chat/completions",
        "model_id": "mimo-v2.5",
        "type": "fast",
        "cost_per_1k": 0.00014,
        "context": 128000,
    },
    "mimo-v2.5-pro": {
        "format": "openai",
        "endpoint": "https://opencode.ai/zen/go/v1/chat/completions",
        "model_id": "mimo-v2.5-pro",
        "type": "capable",
        "cost_per_1k": 0.00174,
        "context": 128000,
    },
    # Anthropic-compatible endpoint (v1/messages)
    "minimax-m3": {
        "format": "anthropic",
        "endpoint": "https://opencode.ai/zen/go/v1/messages",
        "model_id": "minimax-m3",
        "type": "balanced",
        "cost_per_1k": 0.00060,
        "context": 128000,
    },
    "minimax-m2.7": {
        "format": "anthropic",
        "endpoint": "https://opencode.ai/zen/go/v1/messages",
        "model_id": "minimax-m2.7",
        "type": "fast",
        "cost_per_1k": 0.00030,
        "context": 128000,
    },
    "minimax-m2.5": {
        "format": "anthropic",
        "endpoint": "https://opencode.ai/zen/go/v1/messages",
        "model_id": "minimax-m2.5",
        "type": "fast",
        "cost_per_1k": 0.00030,
        "context": 128000,
    },
    "qwen3.7-max": {
        "format": "anthropic",
        "endpoint": "https://opencode.ai/zen/go/v1/messages",
        "model_id": "qwen3.7-max",
        "type": "capable",
        "cost_per_1k": 0.00250,
        "context": 128000,
    },
    "qwen3.7-plus": {
        "format": "anthropic",
        "endpoint": "https://opencode.ai/zen/go/v1/messages",
        "model_id": "qwen3.7-plus",
        "type": "balanced",
        "cost_per_1k": 0.00040,
        "context": 256000,
    },
    "qwen3.6-plus": {
        "format": "anthropic",
        "endpoint": "https://opencode.ai/zen/go/v1/messages",
        "model_id": "qwen3.6-plus",
        "type": "balanced",
        "cost_per_1k": 0.00050,
        "context": 256000,
    },
}

# Model selection presets
PRESETS = {
    "fast": ["deepseek-v4-flash", "mimo-v2.5", "minimax-m2.5", "minimax-m2.7"],
    "balanced": ["glm-5", "kimi-k2.5", "minimax-m3", "qwen3.7-plus"],
    "capable": ["deepseek-v4-pro", "glm-5.1", "kimi-k2.6", "qwen3.7-max", "mimo-v2.5-pro"],
    "cheap": ["deepseek-v4-flash", "mimo-v2.5", "minimax-m2.5"],
    "all": list(MODEL_REGISTRY.keys()),
}

# Optimized prompts per model type
FAST_PROMPT = """You are a social media content designer. Convert landscape slides to 9:16 reel scenes.

RULES:
1. ONE idea per scene. Split if 3+ points.
2. Max 15 words per scene.
3. Content in safe zone (15% top, 20% bottom).
4. Charts → key stat. Tables → 3 takeaways.
5. Start with title_scene, end with cta_scene.
6. Preserve ALL numbers.

Available layouts:
{catalog}

Respond ONLY with JSON:
{{"scenes": [{{"layout": "name", "headline": "...", "body_items": ["..."], "stat_number": "...", "stat_label": "...", "image_name": "...", "quote_text": "...", "cta_headline": "..."}}], "reasoning": "..."}}"""

CAPABLE_PROMPT = """You are an expert social media content designer specializing in Instagram Reels.

Your task: Convert a landscape presentation slide into one or more vertical 9:16 (1080×1920) reel scenes.

## Design Principles
- **One idea per scene**: If a slide has multiple distinct points, split into multiple scenes
- **Phone readability**: Max 15 words per scene, minimum 28pt font equivalent
- **Safe zones**: Keep content between 15% from top and 20% from bottom (Instagram UI overlays)
- **Visual hierarchy**: Title > Stats > Body > Caption
- **Data preservation**: ALL numbers, percentages, and key metrics must appear in output

## Content Transformation Rules
- **Wide images** → Center-crop to 9:16 aspect ratio
- **Charts** → Extract the single most impactful statistic
- **Tables** → Convert to 2-3 key takeaways
- **Bullet lists** → Max 3 items per scene, condense each to ≤8 words
- **SmartArt** → Extract text + render as static image

## Scene Structure
Every deck should:
1. Open with a **title_scene** (big headline, optional subtitle)
2. Present key data with **stat_scene** (big number + label)
3. Detail with **bullet_scene** (headline + 2-3 points)
4. Close with **cta_scene** (call to action)

## Layout Catalog
{catalog}

## Output Format
Respond ONLY with valid JSON:
```json
{{
  "scenes": [
    {{
      "layout": "layout_name",
      "headline": "Max 6 words",
      "body_items": ["Max 8 words each", "Max 3 items"],
      "stat_number": "$12M",
      "stat_label": "Revenue",
      "stat_sublabel": "+15% YoY",
      "image_name": "image1.png",
      "image_crop": "center",
      "quote_text": "Quote text",
      "quote_attribution": "Author",
      "cta_headline": "Follow us",
      "cta_subheadline": "For more insights"
    }}
  ],
  "simplifications": [
    {{
      "original_content": "What was in the original",
      "simplified_to": "What it became",
      "reason": "Why this change was made"
    }}
  ],
  "reasoning": "Brief explanation of layout decisions and splits"
}}
```"""


def get_model_info(model_name: str) -> dict:
    """Get model configuration from registry."""
    if model_name not in MODEL_REGISTRY:
        raise ValueError(f"Unknown model: {model_name}. Available: {list(MODEL_REGISTRY.keys())}")
    return MODEL_REGISTRY[model_name]


def get_preset_models(preset: str) -> list[str]:
    """Get models for a preset category."""
    if preset not in PRESETS:
        raise ValueError(f"Unknown preset: {preset}. Available: {list(PRESETS.keys())}")
    return PRESETS[preset]


def select_best_model(
    preset: str = "balanced",
    preferred: str | None = None,
    fallback: bool = True,
) -> str:
    """Select the best available model based on preset and preferences."""
    candidates = PRESETS.get(preset, PRESETS["balanced"])
    
    if preferred and preferred in MODEL_REGISTRY:
        return preferred
    
    # Return first available model
    return candidates[0]


def get_system_prompt(model_name: str, catalog: str) -> str:
    """Get optimized system prompt for the model type."""
    model_info = get_model_info(model_name)
    model_type = model_info["type"]
    
    if model_type == "fast":
        prompt = FAST_PROMPT
    else:
        prompt = CAPABLE_PROMPT
    
    return prompt.format(catalog=catalog)


def build_openai_request(
    model_info: dict,
    system_prompt: str,
    user_content: str,
    temperature: float = 0.3,
) -> dict:
    """Build OpenAI-compatible request payload."""
    return {
        "model": model_info["model_id"],
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content},
        ],
        "response_format": {"type": "json_object"},
        "temperature": temperature,
        "max_tokens": 2000,
    }


def build_anthropic_request(
    model_info: dict,
    system_prompt: str,
    user_content: str,
    temperature: float = 0.3,
) -> dict:
    """Build Anthropic-compatible request payload."""
    return {
        "model": model_info["model_id"],
        "system": system_prompt,
        "messages": [
            {"role": "user", "content": user_content},
        ],
        "max_tokens": 2000,
        "temperature": temperature,
    }


def parse_openai_response(response_data: dict) -> dict:
    """Parse OpenAI-compatible response."""
    content = response_data["choices"][0]["message"]["content"]
    return json.loads(content)


def parse_anthropic_response(response_data: dict) -> dict:
    """Parse Anthropic-compatible response."""
    content = response_data["content"][0]["text"]
    return json.loads(content)


async def get_layout_decision(
    fingerprint: SlideFingerprint,
    template_config: TemplateConfig,
    catalog_markdown: str,
    api_key: str | None = None,
    model: str = "deepseek-v4-flash",
    preset: str = "balanced",
    temperature: float = 0.3,
    max_retries: int = 3,
    fallback_models: list[str] | None = None,
) -> dict:
    """Get AI layout decision with multi-model support and fallback.
    
    Args:
        fingerprint: The slide fingerprint to process
        template_config: Template configuration
        catalog_markdown: Available layouts catalog
        api_key: OpenCode Go API key (or from env var)
        model: Specific model to use (or first from preset)
        preset: Model preset (fast/balanced/capable/cheap/all)
        temperature: Sampling temperature
        max_retries: Number of retries on failure
        fallback_models: List of fallback models to try
    
    Returns:
        dict with scenes, simplifications, reasoning
    """
    # Get API key
    if not api_key:
        api_key = os.environ.get("OPENCODE_GO_API_KEY")
    if not api_key:
        raise ValueError(
            "OpenCode Go API key required. Set OPENCODE_GO_API_KEY env var or pass api_key parameter."
        )
    
    # Select model
    model_name = model
    if model_name not in MODEL_REGISTRY:
        model_name = select_best_model(preset=preset)
    
    model_info = get_model_info(model_name)
    system_prompt = get_system_prompt(model_name, catalog_markdown)
    
    # Build user content
    slide_description = json.dumps({
        "slide_number": fingerprint.slide_number,
        "title": fingerprint.title_text,
        "bullets": fingerprint.bullet_items,
        "numbers": fingerprint.unique_numbers,
        "images": fingerprint.image_names,
        "content_type": fingerprint.content_type,
        "total_words": fingerprint.total_word_count,
        "warnings": fingerprint.warnings,
    }, indent=2)
    
    # Build request based on API format
    if model_info["format"] == "openai":
        payload = build_openai_request(model_info, system_prompt, slide_description, temperature)
    else:
        payload = build_anthropic_request(model_info, system_prompt, slide_description, temperature)
    
    # Try primary model
    last_error = None
    for attempt in range(max_retries):
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    model_info["endpoint"],
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json",
                    },
                    json=payload,
                )
                response.raise_for_status()
                data = response.json()
                
                if model_info["format"] == "openai":
                    return parse_openai_response(data)
                else:
                    return parse_anthropic_response(data)
                    
        except Exception as e:
            last_error = e
            if attempt < max_retries - 1:
                continue
    
    # Try fallback models
    if fallback_models:
        for fallback_model in fallback_models:
            if fallback_model in MODEL_REGISTRY:
                try:
                    return await get_layout_decision(
                        fingerprint=fingerprint,
                        template_config=template_config,
                        catalog_markdown=catalog_markdown,
                        api_key=api_key,
                        model=fallback_model,
                        preset=preset,
                        temperature=temperature,
                        max_retries=1,
                        fallback_models=None,
                    )
                except Exception:
                    continue
    
    # All attempts failed
    raise RuntimeError(
        f"All model attempts failed. Last error: {last_error}. "
        f"Tried: {model_name} + {len(fallback_models or [])} fallbacks"
    )


def estimate_cost(
    slide_count: int,
    model: str = "deepseek-v4-flash",
    avg_input_tokens: int = 500,
    avg_output_tokens: int = 200,
) -> dict:
    """Estimate cost for processing N slides with a given model."""
    model_info = get_model_info(model)
    input_cost = (avg_input_tokens * slide_count / 1000) * model_info["cost_per_1k"]
    output_cost = (avg_output_tokens * slide_count / 1000) * model_info["cost_per_1k"]
    total = input_cost + output_cost
    
    return {
        "model": model,
        "slides": slide_count,
        "input_tokens": avg_input_tokens * slide_count,
        "output_tokens": avg_output_tokens * slide_count,
        "input_cost_usd": round(input_cost, 4),
        "output_cost_usd": round(output_cost, 4),
        "total_cost_usd": round(total, 4),
        "cost_per_slide": round(total / slide_count, 4),
    }


def get_model_recommendation(
    slide_count: int,
    budget_usd: float | None = None,
    priority: Literal["speed", "quality", "cost"] = "balanced",
) -> str:
    """Recommend the best model based on constraints."""
    if priority == "cost" or (budget_usd and slide_count > 50):
        # For large decks or tight budgets, use cheapest
        return "deepseek-v4-flash"
    elif priority == "speed":
        # Fast processing
        return "mimo-v2.5"
    elif priority == "quality":
        # Best quality
        return "deepseek-v4-pro"
    else:
        # Balanced
        if slide_count > 20:
            return "deepseek-v4-flash"  # Cheaper for large decks
        else:
            return "glm-5"  # Good quality for small decks