# Changelog

## 0.1.0 — 2026-05-12

Initial release. Extracted from `agent-harness-chorus-csd-analyzer` + `agent-harness-card-extractor` as part of the 2026-05-12 agent-toolbox extraction (see `D:/ai-agents/docs/superpowers/specs/2026-05-12-agent-toolbox-extraction-design.md`).

- `retry_async(coro_factory, max_retries=1, backoff=2.0)` — async retry-with-backoff for transient LLM call failures.
- `is_transient(exc) -> bool` — exception classifier (HTTP 429/5xx + timeout/connection/rate-limit keywords).
- `sanitize_field_text(text, max_len=200) -> str` — prompt-injection filter for untrusted strings flowing into LLM context.
- `extract_json(text) -> dict | list | None` — best-effort JSON extraction from LLM responses (direct, fenced, embedded).
- `save_checkpoint(path, data)` / `load_checkpoint(path) -> dict` — JSON checkpoint helpers with timestamp injection.
