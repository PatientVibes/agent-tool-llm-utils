"""Prompt-injection filter for untrusted text flowing into LLM context.

Canonical from chorus-csd-analyzer's `_sanitize_field_text`.
"""
from __future__ import annotations

import re

_INJECTION_PATTERNS = re.compile(
    r"(?i)"
    r"(?:ignore\s+(?:all\s+)?(?:previous|above|prior)\s+instructions)"
    r"|(?:you\s+are\s+now\s+)"
    r"|(?:system\s*:\s*)"
    r"|(?:assistant\s*:\s*)"
    r"|(?:human\s*:\s*)"
    r"|(?:<\s*/?(?:system|instruction|prompt))"
    r"|(?:\[INST\])"
)


def sanitize_field_text(text: str, max_len: int = 200) -> str:
    """Strip prompt-injection patterns and truncate."""
    if not text:
        return text
    cleaned = _INJECTION_PATTERNS.sub("[filtered]", text)
    if len(cleaned) > max_len:
        cleaned = cleaned[:max_len] + "..."
    return cleaned
