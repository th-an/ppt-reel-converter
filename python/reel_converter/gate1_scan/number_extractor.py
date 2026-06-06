"""Extract unique numbers and statistics from text."""

from __future__ import annotations

import re


def extract_numbers(text: str) -> list[str]:
    patterns = [
        r'\$[\d,]+(?:\.\d+)?(?:\s*[MBKmbk])?',
        r'\d+(?:\.\d+)?(?:\s*%)',
        r'\d{1,3}(?:,\d{3})+(?:\.\d+)?',
        r'\d+(?:\.\d+)?',
    ]
    found = set()
    for pattern in patterns:
        matches = re.findall(pattern, text)
        for m in matches:
            m = m.strip()
            if m and len(m) > 0:
                found.add(m)
    return sorted(found)