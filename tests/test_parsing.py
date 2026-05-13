"""Tests for llm_utils.parsing."""
from llm_utils import extract_json


def test_direct_json_object():
    assert extract_json('{"a": 1}') == {"a": 1}


def test_direct_json_array():
    assert extract_json('[1, 2, 3]') == [1, 2, 3]


def test_fenced_json_with_label():
    text = '```json\n{"a": 1}\n```'
    assert extract_json(text) == {"a": 1}


def test_fenced_json_no_label():
    text = '```\n{"a": 1}\n```'
    assert extract_json(text) == {"a": 1}


def test_embedded_in_prose():
    text = 'Here is the result: {"a": 1, "b": 2} as requested.'
    assert extract_json(text) == {"a": 1, "b": 2}


def test_invalid_returns_none():
    assert extract_json("not json at all") is None


def test_empty_returns_none():
    assert extract_json("") is None


def test_multi_span_returns_first():
    """Bare-JSON regex must be non-greedy to handle multiple JSON spans."""
    text = 'Some preamble {"meta": true} then payload {"result": 42} done.'
    # Should match the first object, not span both
    result = extract_json(text)
    assert result == {"meta": True}
