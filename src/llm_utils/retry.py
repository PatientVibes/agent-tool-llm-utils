"""Async retry-with-backoff for transient LLM call failures.

Canonical from chorus-csd-analyzer's `_retry_async` and `_is_transient`,
unified with card-extractor's `retry_async`. Union of both transient
status code sets and keyword checks.
"""
from __future__ import annotations

import asyncio
import logging
from typing import Awaitable, Callable, TypeVar

logger = logging.getLogger(__name__)

T = TypeVar("T")

_TRANSIENT_STATUS_CODES = {429, 500, 502, 503, 504}
_TRANSIENT_KEYWORDS = ("timeout", "connection", "temporarily", "rate limit")


def is_transient(exc: Exception) -> bool:
    """Classify whether an exception is worth retrying."""
    msg = str(exc).lower()
    if any(str(code) in msg for code in _TRANSIENT_STATUS_CODES):
        return True
    if any(kw in msg for kw in _TRANSIENT_KEYWORDS):
        return True
    return False


async def retry_async(
    coro_factory: Callable[[], Awaitable[T]],
    max_retries: int = 1,
    backoff: float = 2.0,
) -> T:
    """Retry an async callable on transient errors with exponential backoff.

    Args:
        coro_factory: a zero-arg callable that returns a fresh coroutine
            each call (NOT the coroutine itself).
        max_retries: number of retries after the first attempt (default 1).
        backoff: base seconds between attempts; doubles each retry.
    """
    last_exc: Exception | None = None
    for attempt in range(max_retries + 1):
        try:
            return await coro_factory()
        except Exception as e:
            last_exc = e
            if attempt < max_retries and is_transient(e):
                wait = backoff * (2**attempt)
                logger.warning(
                    "Transient error (attempt %d/%d), retrying in %.1fs: %s",
                    attempt + 1, max_retries + 1, wait, e,
                )
                await asyncio.sleep(wait)
            else:
                raise
    assert last_exc is not None
    raise last_exc
