"""Environment, paths, and console setup for the Golden Hour content pipeline.

Importing this module is side-effect-light and key-free: it resolves paths and
reconfigures the Windows console to UTF-8, but it does NOT check for the API
key. The key is only required on the live-LLM path, so the check lives in
`require_api_key()` and is called from the generation layer — this is what lets
the retrieval self-test and the `--no-llm` dry run execute with no key set.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Windows consoles default to a legacy code page (cp1252) that cannot encode
# the box-drawing characters and arrows this pipeline prints in its dry-run
# and trace output. Force UTF-8 on the standard streams at import time so the
# offline output renders instead of raising UnicodeEncodeError. (Mirrors the
# same guard in Assignment #3's crew.py.)
# ---------------------------------------------------------------------------
if sys.platform == "win32":
    for _stream in (sys.stdout, sys.stderr):
        _reconfigure = getattr(_stream, "reconfigure", None)
        if _reconfigure is not None:
            try:
                _reconfigure(encoding="utf-8", errors="backslashreplace")
            except (ValueError, OSError):
                pass

# ---------------------------------------------------------------------------
# Paths. Everything is anchored to the repo root (this file's parent's parent)
# so the pipeline behaves identically regardless of the caller's cwd — the
# knowledge base and output directory resolve to the same place every time.
# ---------------------------------------------------------------------------
PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent
KNOWLEDGE_BASE_DIR = REPO_ROOT / "knowledge_base"
OUTPUT_DIR = REPO_ROOT / "output"

# The eight game design documents copied into this repo so it is self-contained
# and runnable after a clean `git clone`. Retrieval indexes exactly these.
KNOWLEDGE_BASE_DOCS = (
    "game-concept.md",
    "casualty-model.md",
    "casualty-facial-animation.md",
    "pulse-physiology-integration.md",
    "patient-assessment.md",
    "triage-system.md",
    "treatment-interventions.md",
    "voice-command-system.md",
)

# ---------------------------------------------------------------------------
# Model. Defaults to Sonnet 4.5 (same provider family as Assignment #3);
# override with the MODEL env var. The native Anthropic SDK takes the bare
# model id (no "anthropic/" LiteLLM prefix).
# ---------------------------------------------------------------------------
DEFAULT_MODEL = "claude-sonnet-4-5"


def get_model() -> str:
    """The model id to use, honoring the MODEL env override."""
    return os.environ.get("MODEL", DEFAULT_MODEL)


def require_api_key() -> str:
    """Return ANTHROPIC_API_KEY or exit with a plain PowerShell hint.

    Called only on the live-LLM path — never at import, and never by the
    offline retrieval self-test or the `--no-llm` dry run.
    """
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        sys.exit(
            "ANTHROPIC_API_KEY is not set.\n"
            'PowerShell:  $env:ANTHROPIC_API_KEY = "sk-ant-..."\n'
            "The key is read from the environment only; it is never stored in "
            "this repo (see .env.example and .gitignore). The offline paths "
            "(`uv run python -m pipeline.selftest` and "
            "`uv run python -m pipeline --no-llm`) do not need a key."
        )
    return key
