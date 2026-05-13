# agent-tool-llm-utils

Small reusable utilities for LangChain agent harnesses. Five helpers in one bundle so the repo-count stays small and the discovery story is simple.

## Install

```bash
uv tool install --editable .
# or as a library dependency:
# [tool.uv.sources] agent-tool-llm-utils = { git = "https://github.com/PatientVibes/agent-tool-llm-utils.git", rev = "<sha>" }
```

## What's inside

| Helper | Use case |
|---|---|
| `retry_async` | "Retry this LLM call on 429 / 5xx / timeout, up to N times" |
| `is_transient` | "Should I retry this exception?" (classifier behind `retry_async`) |
| `sanitize_field_text` | "Strip prompt-injection patterns from arbitrary field data before it flows into agent context" |
| `extract_json` | "Pull a JSON object out of LLM response text — direct, fenced, or embedded" |
| `save_checkpoint` / `load_checkpoint` | "Persist agent progress between runs as a JSON blob" |

## Usage

```python
from llm_utils import retry_async, is_transient, sanitize_field_text, extract_json
from llm_utils import save_checkpoint, load_checkpoint
from pathlib import Path

# Retry an LLM call
async def call_llm():
    return await my_chain.ainvoke({"x": 1})

result = await retry_async(call_llm, max_retries=2, backoff=2.0)

# Sanitize untrusted text before showing it to the LLM
clean = sanitize_field_text(user_supplied_field, max_len=200)

# Parse JSON from a response
data = extract_json(llm_response.content)

# Checkpoint
save_checkpoint(Path("progress.json"), {"completed": ["A", "B"]})
state = load_checkpoint(Path("progress.json"))
```

## Provenance

Extracted 2026-05-12 from:
- `agent-harness-chorus-csd-analyzer/src/chorus_csd_analyzer/agent.py` — `_retry_async`, `_is_transient`, `_sanitize_field_text`, checkpoint helpers
- `agent-harness-card-extractor/card_extractor/ai_client.py` — `retry_async`, `is_fatal`, `extract_json`
- `agent-harness-card-extractor/card_extractor/agent.py` — BatchProgress checkpoint helpers

Canonical impls unify slight drift between the two source repos (e.g., chorus's `_is_transient` + card's `is_fatal` → unified `is_transient` with union of transient codes + keywords).

See `D:/ai-agents/docs/superpowers/specs/2026-05-12-agent-toolbox-extraction-design.md`.

## License

MIT. See `LICENSE`.
