"""The live-LLM half: generator call, critic call, and the revise loop.

Uses the native `anthropic` SDK (same provider family as Assignment #3's
crewai[anthropic]). Importing this module needs no API key — the key is
required only when a call is actually made, via config.require_api_key(). This
is the half that CANNOT be verified offline: there is no API key in the build
environment, so this code is written and type-checked but not executed against
the live API.
"""

from __future__ import annotations

import json
from dataclasses import dataclass

import anthropic
from pydantic import BaseModel, ValidationError

from . import prompts
from .config import get_model, require_api_key
from .retrieval import RetrievedChunk
from .schema import CONTENT_MODELS, CriticVerdict

# Completions are a single small JSON object each; no streaming needed and a
# modest token ceiling is plenty. A bounded timeout keeps a wedged connection
# from hanging forever (the fail-fast-but-generous stance from A#3).
_MAX_TOKENS = 2048
_TIMEOUT_S = 120.0


@dataclass
class ItemResult:
    """The full generate->critique->revise record for one request, for logging."""

    content_type: str
    request_label: str
    request_keys: dict
    query: str
    retrieved: list[RetrievedChunk]
    draft: dict
    verdict: CriticVerdict
    final: dict


def extract_json(text: str) -> dict:
    """Pull the first balanced JSON object out of a model response.

    Tolerates markdown code fences and leading/trailing prose by scanning for
    the first '{' and matching braces (string-aware). Raises ValueError if no
    JSON object is found or it does not parse.
    """
    start = text.find("{")
    if start == -1:
        raise ValueError(f"No JSON object found in model response: {text[:200]!r}")
    depth = 0
    in_string = False
    escaped = False
    for i in range(start, len(text)):
        ch = text[i]
        if in_string:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                in_string = False
        else:
            if ch == '"':
                in_string = True
            elif ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    return json.loads(text[start : i + 1])
    raise ValueError("Unbalanced JSON braces in model response.")


def make_client() -> anthropic.Anthropic:
    """Build an Anthropic client, exiting with a plain hint if the key is unset."""
    return anthropic.Anthropic(api_key=require_api_key())


def _complete(client: anthropic.Anthropic, system: str, user: str) -> str:
    """One non-streaming completion; returns the concatenated text blocks."""
    message = client.messages.create(
        model=get_model(),
        max_tokens=_MAX_TOKENS,
        system=system,
        messages=[{"role": "user", "content": user}],
        timeout=_TIMEOUT_S,
    )
    return "".join(block.text for block in message.content if block.type == "text")


def _validate(content_type: str, item: dict) -> dict:
    """Validate an item dict against its content-type schema; return normalized."""
    model: type[BaseModel] = CONTENT_MODELS[content_type]
    try:
        return model.model_validate(item).model_dump()
    except ValidationError as exc:
        raise ValueError(
            f"Generated {content_type} item failed schema validation: {exc}"
        ) from exc


def generate_item(
    client: anthropic.Anthropic,
    *,
    content_type: str,
    generator_brief: str,
    request_label: str,
    request_keys: dict,
    retrieved: list[RetrievedChunk],
) -> dict:
    """Generate one candidate item from the retrieved context + request keys."""
    model: type[BaseModel] = CONTENT_MODELS[content_type]
    prompt = prompts.build_generator_prompt(
        generator_brief=generator_brief,
        request_label=request_label,
        request_keys=request_keys,
        retrieved=retrieved,
        schema_json=model.model_json_schema(),
    )
    raw = _complete(client, prompts.GENERATOR_SYSTEM, prompt)
    return _validate(content_type, extract_json(raw))


def critique_item(
    client: anthropic.Anthropic,
    *,
    content_type: str,
    content_title: str,
    request_label: str,
    request_keys: dict,
    retrieved: list[RetrievedChunk],
    draft: dict,
) -> CriticVerdict:
    """Run the critic over a draft; return its verdict (with corrected item)."""
    prompt = prompts.build_critic_prompt(
        content_title=content_title,
        request_label=request_label,
        request_keys=request_keys,
        retrieved=retrieved,
        draft_json=json.dumps(draft, indent=2),
        verdict_schema_json=CriticVerdict.model_json_schema(),
    )
    raw = _complete(client, prompts.CRITIC_SYSTEM, prompt)
    verdict = CriticVerdict.model_validate(extract_json(raw))
    # The corrected item must itself be schema-valid for the content type.
    verdict.corrected_item = _validate(content_type, verdict.corrected_item)
    return verdict
