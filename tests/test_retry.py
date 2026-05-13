"""Tests for llm_utils.retry."""
import asyncio
import pytest

from llm_utils import retry_async, is_transient


def test_is_transient_429():
    assert is_transient(RuntimeError("429 too many requests"))


def test_is_transient_500():
    assert is_transient(RuntimeError("HTTP 500 server error"))


def test_is_transient_timeout():
    assert is_transient(RuntimeError("connection timeout"))


def test_is_transient_non_transient():
    assert not is_transient(ValueError("bad input"))


@pytest.mark.asyncio
async def test_retry_async_succeeds_first_try():
    async def factory():
        return 42
    result = await retry_async(factory, max_retries=2)
    assert result == 42


@pytest.mark.asyncio
async def test_retry_async_retries_on_transient():
    attempts = {"count": 0}

    async def factory():
        attempts["count"] += 1
        if attempts["count"] < 2:
            raise RuntimeError("429 throttled")
        return "ok"

    result = await retry_async(factory, max_retries=2, backoff=0.01)
    assert result == "ok"
    assert attempts["count"] == 2


@pytest.mark.asyncio
async def test_retry_async_raises_on_non_transient():
    async def factory():
        raise ValueError("permanent")

    with pytest.raises(ValueError, match="permanent"):
        await retry_async(factory, max_retries=2)
