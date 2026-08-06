"""Offline retrieval self-test.

Runs three known queries against the real knowledge base and asserts the
expected source document appears in the top results. Proves the RAG retrieval
half works end to end with no API key. Exit code 0 = pass, 1 = fail.

Run standalone:  uv run python -m pipeline.selftest
"""

from __future__ import annotations

import sys
from dataclasses import dataclass

from .retrieval import KnowledgeBase

_TOP_K = 3


@dataclass(frozen=True)
class RetrievalCase:
    name: str
    query: str
    expected_doc: str  # must appear among the top-_TOP_K retrieved chunks


# Each query uses vocabulary that most distinctively belongs to one GDD doc.
CASES: list[RetrievalCase] = [
    RetrievalCase(
        name="facial affect pipeline",
        query="facial expression pain appraisal coping unconscious arrest "
        "vocalization suppressed homeostasis",
        expected_doc="casualty-facial-animation.md",
    ),
    RetrievalCase(
        name="offline voice recognition",
        query="closed command grammar whisper offline speech recognition "
        "microphone VAD push to talk",
        expected_doc="voice-command-system.md",
    ),
    RetrievalCase(
        name="MARCH treatment verbs",
        query="tourniquet wound packing needle decompression chest seal MARCH "
        "massive hemorrhage intervention",
        expected_doc="treatment-interventions.md",
    ),
]


def run_selftest(top_k: int = _TOP_K) -> bool:
    """Run all retrieval cases; return True iff every case passes."""
    kb = KnowledgeBase.load()
    print(f"Retrieval self-test: {len(kb.chunks)} chunks indexed, "
          f"top_k={top_k}\n")
    all_passed = True
    for case in CASES:
        retrieved = kb.retrieve(case.query, top_k=top_k)
        docs = [rc.chunk.source_doc for rc in retrieved]
        passed = case.expected_doc in docs
        all_passed = all_passed and passed
        mark = "PASS" if passed else "FAIL"
        print(f"[{mark}] {case.name}")
        print(f"       query: {case.query}")
        print(f"       expected doc in top {top_k}: {case.expected_doc}")
        for i, rc in enumerate(retrieved, 1):
            hit = " <-- expected" if rc.chunk.source_doc == case.expected_doc else ""
            print(f"         {i}. [{rc.score:6.2f}] {rc.chunk.source_doc} > "
                  f"{rc.chunk.heading}{hit}")
        print()
    print("RESULT:", "ALL PASSED" if all_passed else "FAILURES PRESENT")
    return all_passed


def main() -> int:
    return 0 if run_selftest() else 1


if __name__ == "__main__":
    sys.exit(main())
