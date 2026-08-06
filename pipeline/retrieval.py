"""BM25 lexical retrieval over the Golden Hour knowledge base.

This is the RAG core. Each knowledge-base markdown doc is chunked by section
(split on markdown headings), every chunk keeps its (source_doc, heading)
provenance, and a BM25Okapi index ranks chunks against a query built from the
content-type + the request's injury/state keys. Nothing here is hand-distilled:
the facts that ground each generation are retrieved from the GDDs at runtime.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

from rank_bm25 import BM25Okapi

from .config import KNOWLEDGE_BASE_DIR, KNOWLEDGE_BASE_DOCS

# A markdown ATX heading line: 1-6 '#', a space, then the heading text.
_HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
# Tokenizer: lowercase alphanumeric runs. Keeps digits so "30", "spo2",
# "march", "salt" survive as query/document terms.
_TOKEN_RE = re.compile(r"[a-z0-9]+")

# ---------------------------------------------------------------------------
# Retrieval tweak (2026-08-05), measured, not guessed: a dry run over all 15
# requests showed 35% of retrieved chunk slots were document-management
# metadata rather than game content. Every GDD here follows the same section
# template, and two of its sections carry no authorable content at all:
#   "Cross-References" — a doc-to-doc reference grid ("this doc references
#       that doc"), which scores highly because it is dense with system nouns.
#   "Build Agents"     — which agent/crew builds the system; project
#       management, not game lore.
# Both were crowding out the sections that actually describe how a casualty
# looks and sounds, so they are excluded at index time. Every other section —
# including "Dependencies", which does encode real cross-system rules — is
# retained. Excluding at chunk time (rather than filtering results) keeps BM25's
# corpus statistics honest: these sections never enter the index at all.
# ---------------------------------------------------------------------------
NON_CONTENT_HEADINGS: frozenset[str] = frozenset(
    {"cross-references", "build agents"}
)


def _tokenize(text: str) -> list[str]:
    return _TOKEN_RE.findall(text.lower())


@dataclass(frozen=True)
class Chunk:
    """One retrievable section of a knowledge-base document, with provenance."""

    source_doc: str
    heading: str
    text: str
    tokens: list[str] = field(compare=False, repr=False)

    def citation(self) -> str:
        return f"{self.source_doc} > {self.heading}"


@dataclass(frozen=True)
class RetrievedChunk:
    """A chunk plus its BM25 score for a specific query."""

    chunk: Chunk
    score: float


def chunk_markdown(source_doc: str, content: str) -> list[Chunk]:
    """Split one markdown document into section chunks on its headings.

    The text before the first heading (if any) becomes a "(preamble)" chunk so
    no content is dropped. Each subsequent heading starts a new chunk that runs
    until the next heading of any level. The heading line itself is folded into
    the chunk text so heading keywords count toward retrieval.
    """
    chunks: list[Chunk] = []
    current_heading = "(preamble)"
    current_lines: list[str] = []

    def flush() -> None:
        body = "\n".join(current_lines).strip()
        # Skip empty sections (e.g. a heading immediately followed by another).
        if not body:
            return
        # Skip document-management sections — see NON_CONTENT_HEADINGS.
        if current_heading.strip().lower() in NON_CONTENT_HEADINGS:
            return
        indexed_text = f"{current_heading}\n{body}"
        chunks.append(
            Chunk(
                source_doc=source_doc,
                heading=current_heading,
                text=body,
                tokens=_tokenize(indexed_text),
            )
        )

    for line in content.splitlines():
        match = _HEADING_RE.match(line)
        if match:
            flush()
            current_heading = match.group(2).strip()
            current_lines = []
        else:
            current_lines.append(line)
    flush()
    return chunks


class KnowledgeBase:
    """A BM25 index over all knowledge-base chunks, with query helpers."""

    def __init__(self, chunks: list[Chunk]):
        if not chunks:
            raise ValueError("KnowledgeBase built with zero chunks.")
        self.chunks = chunks
        self._bm25 = BM25Okapi([c.tokens for c in chunks])

    @classmethod
    def load(cls, base_dir: Path | None = None) -> "KnowledgeBase":
        """Build the index from the eight knowledge-base documents on disk."""
        base_dir = base_dir or KNOWLEDGE_BASE_DIR
        all_chunks: list[Chunk] = []
        missing: list[str] = []
        for doc in KNOWLEDGE_BASE_DOCS:
            path = base_dir / doc
            if not path.is_file():
                missing.append(doc)
                continue
            all_chunks.extend(chunk_markdown(doc, path.read_text(encoding="utf-8")))
        if missing:
            raise FileNotFoundError(
                "Knowledge base is incomplete — missing "
                f"{', '.join(missing)} under {base_dir}. The repo ships all "
                "eight GDD docs in knowledge_base/; re-clone or restore them."
            )
        return cls(all_chunks)

    def retrieve(self, query: str, top_k: int = 4) -> list[RetrievedChunk]:
        """Return the top_k chunks for a query, highest BM25 score first."""
        query_tokens = _tokenize(query)
        scores = self._bm25.get_scores(query_tokens)
        ranked = sorted(
            zip(self.chunks, scores), key=lambda pair: pair[1], reverse=True
        )
        return [
            RetrievedChunk(chunk=chunk, score=float(score))
            for chunk, score in ranked[:top_k]
        ]


def build_query(content_type_terms: list[str], key_terms: list[str]) -> str:
    """Assemble a retrieval query from content-type terms + request key terms.

    Kept deliberately simple and transparent — the query is just the terms
    joined with spaces, so it prints legibly in retrieval_trace.md and the
    dry-run output. Empty/blank terms are dropped.
    """
    terms = [t.strip() for t in (*content_type_terms, *key_terms) if t and t.strip()]
    return " ".join(terms)
