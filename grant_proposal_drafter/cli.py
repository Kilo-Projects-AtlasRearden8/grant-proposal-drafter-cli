import argparse
import json
import os
import sys

from .client import LLMClient, LLMError
from .drafter import DEFAULT_DETAILS, GrantDrafter, SECTION_ORDER

DEFAULT_BASE_URL = "http://localhost:11434/v1"
DEFAULT_MODEL = "llama3.2"

DETAILS_FLAGS = [
    "title",
    "organization",
    "amount",
    "duration",
    "contact",
    "target_population",
    "problem_statement",
    "goals",
    "activities",
    "budget_items",
    "evaluation_metrics",
    "sustainability",
]


def build_parser():
    parser = argparse.ArgumentParser(
        prog="grant-draft",
        description="Draft grant proposal sections using a local OpenAI-compatible endpoint (default Ollama). Education only.",
    )
    parser.add_argument("--input", help="JSON file with project details")
    parser.add_argument("--output", default="grant_proposal_draft.md",
                        help="Output Markdown file (default: grant_proposal_draft.md)")
    parser.add_argument("--base-url", default=os.environ.get("GRANT_DRAFTER_BASE_URL", DEFAULT_BASE_URL),
                        help="OpenAI-compatible endpoint base URL")
    parser.add_argument("--model", default=os.environ.get("GRANT_DRAFTER_MODEL", DEFAULT_MODEL),
                        help="Model name")
    parser.add_argument("--api-key", default=os.environ.get("GRANT_DRAFTER_API_KEY"),
                        help="Optional API key (never saved to disk)")
    parser.add_argument("--timeout", type=int, default=60, help="Request timeout in seconds")
    for flag in DETAILS_FLAGS:
        parser.add_argument(f"--{flag}", default=None, help=f"Project detail: {flag}")
    return parser


def load_details(args):
    details = {}
    if args.input:
        with open(args.input, "r", encoding="utf-8") as handle:
            details = json.load(handle)
    for flag in DETAILS_FLAGS:
        value = getattr(args, flag)
        if value:
            details[flag] = value
    merged = dict(DEFAULT_DETAILS)
    merged.update(details)
    return merged


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    details = load_details(args)
    client = LLMClient(
        base_url=args.base_url,
        model=args.model,
        api_key=args.api_key,
        timeout=args.timeout,
    )
    drafter = GrantDrafter(client)
    try:
        sections = drafter.draft_all(details)
    except LLMError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        print("Tip: start Ollama (default http://localhost:11434/v1) or use --base-url/--model.", file=sys.stderr)
        return 1
    markdown = drafter.render_markdown(details, sections)
    with open(args.output, "w", encoding="utf-8") as handle:
        handle.write(markdown)
    print(f"Draft saved to {args.output}")
    print("REMINDER: education-only draft - review with qualified professionals before submission.")
    return 0
