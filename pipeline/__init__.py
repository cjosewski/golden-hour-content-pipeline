"""Golden Hour casualty-voice RAG content pipeline (ELVTR Assignment #4).

A retrieval-augmented generation pipeline that authors game-specific
casualty-voice content for Golden Hour (VR mass-casualty triage trainer) by
retrieving relevant chunks from the game's own GDDs (BM25 over knowledge_base/)
and generating grounded content with a critic agent that catches lore, tone,
and clinical-consistency breaks.

Public entry points:
    pipeline.pipeline.run_dry_run()   # offline: retrieval + prompt assembly
    pipeline.pipeline.run_live()      # live: generate -> critique -> revise
    pipeline.selftest.run_selftest()  # offline retrieval self-test
"""

__version__ = "0.1.0"
