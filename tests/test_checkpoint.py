"""Tests for llm_utils.checkpoint."""
import json
from pathlib import Path

from llm_utils import save_checkpoint, load_checkpoint


def test_save_and_load_roundtrip(tmp_path: Path):
    p = tmp_path / "ckpt.json"
    save_checkpoint(p, {"forms": {"A": "done"}})
    loaded = load_checkpoint(p)
    assert loaded["forms"] == {"A": "done"}
    assert "timestamp" in loaded


def test_load_missing_returns_empty(tmp_path: Path):
    p = tmp_path / "missing.json"
    assert load_checkpoint(p) == {}


def test_load_invalid_returns_empty(tmp_path: Path):
    p = tmp_path / "bad.json"
    p.write_text("not valid json")
    assert load_checkpoint(p) == {}


def test_save_none_path_noop():
    # Should not raise
    save_checkpoint(None, {"x": 1})


def test_load_none_path_empty():
    assert load_checkpoint(None) == {}
