"""Condense text for phone screen readability (max 15 words per scene)."""

from __future__ import annotations

MAX_WORDS_PER_SCENE = 15
MAX_WORDS_PER_HEADLINE = 6
MAX_WORDS_PER_BODY_ITEM = 8
MAX_BODY_ITEMS = 3

WORDS_TO_REMOVE = {
    " really", " very", " quite", " essentially", " basically",
    " actually", " literally", " just", " perhaps", " somewhat",
    " certainly", " definitely", " probably", " obviously",
}


def condense_text(text: str, max_words: int = MAX_WORDS_PER_SCENE) -> str:
    if not text:
        return text
    for word in WORDS_TO_REMOVE:
        text = text.replace(word, "")
    text = " ".join(text.split())
    words = text.split()
    if len(words) <= max_words:
        return text
    return " ".join(words[:max_words]) + "..."


def condense_headline(text: str | None) -> str | None:
    if not text:
        return None
    return condense_text(text, MAX_WORDS_PER_HEADLINE)


def condense_body_items(items: list[str], max_items: int = MAX_BODY_ITEMS) -> list[str]:
    condensed = []
    for item in items[:max_items]:
        words = item.strip().split()
        if len(words) <= MAX_WORDS_PER_BODY_ITEM:
            condensed.append(item.strip())
        else:
            condensed.append(" ".join(words[:MAX_WORDS_PER_BODY_ITEM]) + "...")
    return condensed