"""CLI entry point for the Golden Hour content pipeline.

    uv run python -m pipeline              # live run (needs ANTHROPIC_API_KEY)
    uv run python -m pipeline --no-llm     # offline: retrieval + prompt assembly
    uv run python -m pipeline --selftest   # offline retrieval self-test
    uv run python -m pipeline --top-k 6    # override retrieved-chunk count

The top-level guard turns a framework traceback into one plain, actionable
line naming the likely cause — mirroring Assignment #3's error handling.
"""

from __future__ import annotations

import argparse
import sys

from .config import get_model
from .pipeline import TOP_K, run_dry_run, run_live
from .selftest import run_selftest


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pipeline",
        description="RAG casualty-voice content pipeline for Golden Hour.",
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--no-llm",
        action="store_true",
        help="Offline dry run: print queries, retrieved chunks, and assembled "
        "prompts without calling Anthropic (no API key needed).",
    )
    mode.add_argument(
        "--selftest",
        action="store_true",
        help="Run the offline retrieval self-test and exit (no API key needed).",
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=TOP_K,
        help=f"Number of chunks to retrieve per request (default {TOP_K}).",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)

    if args.selftest:
        return 0 if run_selftest() else 1

    if args.no_llm:
        run_dry_run(top_k=args.top_k)
        return 0

    # Live run.
    try:
        run_live(top_k=args.top_k)
    except SystemExit:
        raise  # the fail-fast key check already printed a clean hint
    except Exception as exc:  # top-level guard -> one plain, actionable line
        detail = str(exc)
        lowered = detail.lower()
        if "authentication" in lowered or "invalid x-api-key" in lowered or "401" in detail:
            hint = (
                "Anthropic rejected the API key. Set ANTHROPIC_API_KEY to a "
                "current, active key with available credit."
            )
        elif "not_found" in lowered or "404" in detail:
            hint = (
                f"Anthropic did not accept the model {get_model()!r}. Confirm "
                "your account can call it, or override it with the MODEL env var."
            )
        elif (
            "overloaded" in lowered
            or "rate limit" in lowered
            or "rate_limit" in lowered
            or "429" in detail
            or "529" in detail
        ):
            hint = "Anthropic was rate-limited or overloaded — wait a moment and re-run."
        elif "connection" in lowered or "timeout" in lowered:
            hint = (
                "The connection to Anthropic dropped or stalled. Check your "
                "network/VPN/proxy and re-run."
            )
        else:
            hint = "See the error detail below, address the cause, and re-run."
        sys.exit(f"\nPipeline run failed: {hint}\n\nError detail: {detail}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
