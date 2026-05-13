"""Generic JSON checkpoint save/load helpers."""
from __future__ import annotations

import json
import logging
import time
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


def save_checkpoint(path: Path | None, data: dict[str, Any]) -> None:
    """Write `data` as JSON to `path`, adding a `timestamp` key."""
    if path is None:
        return
    try:
        out = {**data, "timestamp": time.time()}
        path.write_text(json.dumps(out, indent=2), encoding="utf-8")
    except Exception as e:
        logger.warning("Failed to save checkpoint to %s: %s", path, e)


def load_checkpoint(path: Path | None) -> dict[str, Any]:
    """Load a JSON checkpoint, returning {} if absent or invalid."""
    if path is None or not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        logger.warning("Failed to load checkpoint from %s: %s", path, e)
        return {}
