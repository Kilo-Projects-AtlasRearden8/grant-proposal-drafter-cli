# Grant Proposal Drafter CLI

A friendly, local-first Python CLI that drafts grant proposal sections from your
project details using an OpenAI-compatible endpoint (Ollama by default). It
saves a Markdown draft to your computer — nothing leaves your machine unless you
choose to point it elsewhere.

Built by **Asdale Dynamics, LLC** (Indiana) — beginner-friendly AI education,
books and guides, and practical open-source tools you can publish or sell.
Credit: Asdale Dynamics, LLC.

> Heads-up: this is an **education-only** tool. What it produces is a starting
> point, not legal, financial, or professional grant-writing advice. Please
> review any draft with qualified professionals before you submit it to a
> funder. Asdale Dynamics, LLC makes no promises about accuracy or outcomes.

## What it does

It takes your project details (title, organization, amount, duration, goals,
activities, and more) and turns them into a complete Markdown grant proposal
draft with eight sections:

- Executive Summary
- Statement of Need
- Project Description
- Goals and Objectives
- Budget Narrative
- Evaluation Plan
- Sustainability Plan
- Conclusion

Each section gets its own heading, and the whole thing is wrapped with an
education-only disclaimer and your project metadata at the top.

## Quick start

### Option 1: Run straight from the folder (no install needed)

```bash
python3 -m grant_proposal_drafter \
  --input project.json \
  --output draft.md
```

### Option 2: Pass details as flags

```bash
python3 -m grant_proposal_drafter \
  --title "Community Literacy Program" \
  --organization "Asdale Dynamics, LLC" \
  --amount "$50,000" \
  --duration "12 months" \
  --target_population "adult learners in Marion County" \
  --problem_statement "Local adults lack access to free literacy classes." \
  --goals "Improve adult literacy in Marion County." \
  --activities "Weekly classes and tutoring." \
  --output draft.md
```

### Option 3: Install it

```bash
pip install .
grant-draft --input project.json --output draft.md
```

## What goes in `--input`?

A JSON file whose keys match the flag names. Leave anything out — sensible
defaults fill the gaps:

```json
{
  "title": "Community Literacy Program",
  "organization": "Asdale Dynamics, LLC",
  "amount": "$50,000",
  "duration": "12 months",
  "contact": "hello@example.org",
  "target_population": "adult learners in Marion County",
  "problem_statement": "Local adults lack access to free literacy classes.",
  "goals": "Improve adult literacy in Marion County.",
  "activities": "Weekly classes and tutoring.",
  "budget_items": "Instructor wages, materials, space rental.",
  "evaluation_metrics": "Reading assessments and attendance.",
  "sustainability": "Local grants and donations."
}
```

## Point it at your endpoint

By default it talks to Ollama's OpenAI-compatible API at
`http://localhost:11434/v1` using the `llama3.2` model. Change it with flags or
environment variables:

| Flag | Environment variable | Default |
|------|---------------------|---------|
| `--base-url` | `GRANT_DRAFTER_BASE_URL` | `http://localhost:11434/v1` |
| `--model` | `GRANT_DRAFTER_MODEL` | `llama3.2` |
| `--api-key` | `GRANT_DRAFTER_API_KEY` | (none) |
| `--timeout` | — | `60` seconds |

The `--api-key` value lives only in that command's memory — it is never written
to disk.

No API key is required by default. Nothing is sent to any third-party AI
provider unless you configure the endpoint to do so. Local-first by design.

## Tests

No extra packages needed — tests use the Python standard library and a local
mock endpoint. No keys, no network:

```bash
python3 -m unittest discover -s tests -v
```

Six tests cover: hitting the mock endpoint, connection failure, all eight
sections being produced, Markdown structure, the CLI writing a file, and the
CLI refusing to write when the endpoint is down.

## License

MIT. Copyright (c) 2026 Asdale Dynamics, LLC. See LICENSE.

## About Asdale Dynamics, LLC

Dylan Asdale is a registered nurse turned AI author and founder of Asdale
Dynamics, LLC (Indiana, formed October 2026). His book *The Massive AI Manual*
and hub site dylanasdale.github.io explain AI "like a friend would": plain
English, step by step, never condescending. This tool is part of that mission —
beginner-friendly AI education and practical open-source apps.
