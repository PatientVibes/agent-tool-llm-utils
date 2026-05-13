"""Extract JSON from LLM text responses.

Canonical from card-extractor's `extract_json` in ai_client.py.
"""
from __future__ import annotations

import json
import re
from typing import Optional

_FENCED_JSON = re.compile(r"```(?:json)?\s*(\{.*?\}|\[.*?\])\s*```", re.DOTALL)
_BARE_JSON = re.compile(r"(\{.*?\}|\[.*?\])", re.DOTALL)


def extract_json(text: str) -> Optional[dict | list]:
    """Best-effort extraction of a JSON object or array from LLM text."""
    if not text:
        return None
    text = text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    m = _FENCED_JSON.search(text)
    if m:
        try:
            return json.loads(m.group(1))
        except json.JSONDecodeError:
            pass
    m = _BARE_JSON.search(text)
    if m:
        try:
            return json.loads(m.group(1))
        except json.JSONDecodeError:
            pass
    return None
