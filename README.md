# Grant Proposal Drafter CLI

Local-first Python CLI that drafts grant proposal sections from project details
using a configurable OpenAI-compatible endpoint (default Ollama). No API keys
are required by default, nothing is sent to any third-party AI provider unless
you configure it to, and the generated Markdown is saved locally on your
machine.

Built by **Asdale Dynamics, LLC** (Indiana) - beginner-friendly AI education,
books and guides, and practical open-source tools. Credit: Asdale Dynamics, LLC.

## Education-only disclaimer

This tool and everything it generates are for educational purposes only. The
output is not legal, financial, medical, or professional grant-writing advice.
Review every draft with qualified professionals before submitting it to any
funder. Asdale Dynamics, LLC makes no warranties about the accuracy or
suitability of generated drafts.

## What it drafts

- Executive Summary
- Statement of Need
- Project Description
- Goals and Objectives
- Budget Narrative
- Evaluation Plan
- Sustainability Plan
- Conclusion

## Quick start

```bash
python -m grant_proposal_drafter \
  --input project.json \
  --output draft.md
```

Or pass details as flags:

```bash
python -m grant_proposal_drafter \
  --title "Community Literacy Program" \
  --organization "Asdale Dynamics, LLC" \
  --amount "$50,000" \
  --duration "12 months" \
  --output draft.md
```

Installed via pip, the command is also available as:

```bash
grant-draft --input project.json --output draft.md
```

## Configuration

The endpoint defaults to Ollama's OpenAI-compatible API at
`http://localhost:11434/v1` with model `llama3.2`. Override with flags or
environment variables:

- `--base-url` / `GRANT_DRAFTER_BASE_URL`
- `--model` / `GRANT_DRAFTER_MODEL`
- `--api-key` / `GRANT_DRAFTER_API_KEY` (optional; never saved to disk)
- `--timeout` (seconds, default 60)

`--input` takes a JSON file whose keys match the flag names (title,
organization, amount, duration, contact, target_population, problem_statement,
goals, activities, budget_items, evaluation_metrics, sustainability). Missing
details use sensible defaults.

## Tests

No external packages are required; tests use the standard library and a local
mock endpoint - no keys, no network:

```bash
python -m unittest discover -s tests -v
```

## License

MIT. Copyright (c) 2026 Asdale Dynamics, LLC. See LICENSE.
