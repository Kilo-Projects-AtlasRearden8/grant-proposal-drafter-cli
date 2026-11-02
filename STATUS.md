# STATUS

## What was built

**grant-proposal-drafter-cli** v0.1.0 - a local-first Python CLI that drafts grant
proposal sections from project details using a configurable OpenAI-compatible
endpoint (default Ollama at `http://localhost:11434/v1`, model `llama3.2`).
Generated Markdown is saved locally; no API keys are required by default and
none are stored to disk.

Package `grant_proposal_drafter`:
- `client.py` - `LLMClient` posts to `{base_url}/chat/completions` via stdlib
  `urllib`, parses the OpenAI-compatible response, raises `LLMError` on connection
  or shape failures.
- `drafter.py` - `GrantDrafter` drafts 8 sections (executive summary, statement
  of need, project description, goals and objectives, budget narrative,
  evaluation plan, sustainability plan, conclusion) with templates filled from
  project details; `render_markdown` wraps them with the education-only
  disclaimer and project metadata.
- `cli.py` - argparse CLI (`grant-draft` / `python -m grant_proposal_drafter`)
  with `--input` JSON, `--output`, `--base-url`, `--model`, `--api-key`,
  `--timeout`, and per-detail flags; env var overrides
  (`GRANT_DRAFTER_BASE_URL`, `GRANT_DRAFTER_MODEL`, `GRANT_DRAFTER_API_KEY`).

Tests: `tests/test_mock_endpoint.py` - 6 unittest tests against a local mock
HTTP server (no network, no keys).

Also included: `pyproject.toml` (entry point `grant-draft`), `README.md`,
`LICENSE` (MIT, Copyright (c) 2026 Asdale Dynamics, LLC), `.gitignore`.

Credit: Asdale Dynamics, LLC (Indiana) - beginner-friendly AI education, books,
and practical open-source tools (dylanasdale.github.io).

## How to run

```bash
python3 -m grant_proposal_drafter --input project.json --output draft.md
```

Or with flags:

```bash
python3 -m grant_proposal_drafter \
  --title "Community Literacy Program" \
  --organization "Asdale Dynamics, LLC" \
  --amount "$50,000" \
  --duration "12 months" \
  --output draft.md
```

Or install and use the entry point:

```bash
pip install .
grant-draft --input project.json --output draft.md
```

Override the endpoint:

```bash
grant-draft --base-url http://localhost:11434/v1 --model llama3.2 \
  --input project.json --output draft.md
```

## Verification results

```
python3 -m unittest discover -s tests -v
Ran 6 tests - OK
```

Tests cover: client round-trip against a mock HTTP server, payload shape
(stream off, model forwarded), connection-failure `LLMError`, all 8 sections
produced, markdown structure (title, disclaimer, section headings), CLI writing
the output file through the mock endpoint, and CLI exiting nonzero without
creating a file when the endpoint is unreachable.

CLI help (`python3 -m grant_proposal_drafter --help`) prints correctly.

## Known gaps

- Requires a running LLM endpoint (Ollama default); the tool does not bundle or
  start a model. No built-in provider fallback.
- Outputs are AI-generated drafts for education only; they must be reviewed by
  qualified professionals before submission to any funder.
- No API-key storage by design; keys passed via `--api-key` live only in the
  process.
- No web UI, no interactive prompts, no saved-project library.
- Default model `llama3.2` must be available on the configured Ollama instance.
