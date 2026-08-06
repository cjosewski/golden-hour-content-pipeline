"""Role prompts and the consistency rule list for the generator and critic.

The generator authors a candidate item from ONLY the retrieved GDD chunks plus
the request keys. The critic reviews that draft against the same chunks and an
explicit rule list, returns the violations, and emits a corrected item. The
rules are strict on purpose: several request states (unconscious, respiratory
distress, conscious-but-deaf) make a naive draft break a rule, so the critic
reliably has something to catch on a live run.

DELIBERATE: CONSISTENCY_RULES is injected into the CRITIC prompt only, never
into the generator prompt. Pre-briefing the generator on the whole checklist
made it self-censor, so the critic caught nothing and the consistency-checking
evidence in output/critic_log.md came back empty. The generator works from the
retrieved context alone; catching rule breaks is the critic's job. Do not
"helpfully" add format_rules() back into build_generator_prompt().
"""

from __future__ import annotations

import json

from .retrieval import RetrievedChunk

# ---------------------------------------------------------------------------
# The consistency rule list. This is the critic's checklist; every rule traces
# to the GDDs the pipeline retrieves from (cited in parentheses).
# ---------------------------------------------------------------------------
CONSISTENCY_RULES: list[str] = [
    "RESPIRATORY-DISTRESS SPEECH: a casualty in respiratory distress "
    "(respiratory_status = distress) CANNOT deliver calm, full, grammatical "
    "sentences. Their speech must be fragmented, clipped to a few words per "
    "breath, or gasping. (triage-system respiratory-distress trigger; "
    "casualty-facial-animation breathing/vocalization output.)",
    "UNCONSCIOUS = NO WORDS: an unconscious casualty (consciousness = "
    "unconscious) produces no intelligible speech at all — only a described "
    "non-verbal vocalization (moan) or silence. is_intelligible_speech MUST be "
    "false and vocalization MUST NOT contain quoted words. (casualty-facial-"
    "animation Unconscious hard-override: vocalization cue suppressed.)",
    "AIRWAY OBSTRUCTION = NO INTELLIGIBLE WORDS: with respiratory_status = "
    "obstructed (airway obstruction), the casualty cannot form intelligible "
    "words; render a described non-verbal airway sound (gurgle, stridor, "
    "gasping) instead. (treatment-interventions airway tier; patient-assessment "
    "airway check.)",
    "COMMAND COMPLIANCE GATES ON CONSCIOUSNESS *AND* HEARING *AND* MOBILITY, "
    "never on leg function alone: "
    "conscious + can_hear + ambulatory -> verbal compliance and moves; "
    "conscious + can_hear + immobile -> verbal acknowledgement WITHOUT movement; "
    "unconscious -> no response; "
    "conscious but NOT can_hear (deaf) -> no response (does not comply even "
    "though the legs work). The compliance field and the response text must "
    "match this gate exactly. (game-concept Pillar 5; triage-system global "
    "sort; casualty-model Pillar-5 gating constraint.)",
    "PHYSIOLOGY-TRACEABILITY: every line must trace to a named physiology "
    "variable, and physiology_trace must name a real one (e.g. SpO2, "
    "respiration rate, perfusion index, level of consciousness, hemorrhage "
    "rate) that actually explains this line. No scripted 'looks/sounds "
    "dramatic' content with no physiological cause. (Pillar 2 'the face is a "
    "vital sign'; casualty-facial-animation Determinism/traceability rule.)",
    "SCOPE: adults only; ballistic active-shooter scenario only (NO CBRN, no "
    "chemical/blast-agent content); injury_type must be one of the POC set "
    "(external hemorrhage, tension pneumothorax, open/sucking chest wound, "
    "airway obstruction, minor injury). (game-concept MVP scope; triage-system "
    "CBRN exclusion.)",
    "GROUNDED, NON-HEROIC TONE: clinical-documentary realism, not melodrama or "
    "theatre. No cinematic hero dialogue, no gratuitous gore for shock value; "
    "gore only at the minimum fidelity needed for clinical recognition. Lines "
    "read as a real person having the worst day of their life, not a movie. "
    "(game-concept Anti-Pillars 'NOT gratuitous'; casualty-facial-animation "
    "'NOT melodramatic or theatrical'.)",
    "AMBIENT DECLINE STAGE CONSISTENCY: the vocalization must match "
    "decline_stage — early = coherent complaint; mid = confusion / agitation; "
    "late = quiet moan or silence (trending toward non-verbal). A late-stage "
    "line cannot be a lucid full sentence. (casualty-facial-animation "
    "Stable->Compensating->Decompensating->Arrest; 'the voice is a vital "
    "sign'.)",
]


def format_rules() -> str:
    return "\n".join(f"  R{i}. {rule}" for i, rule in enumerate(CONSISTENCY_RULES, 1))


def format_chunks(retrieved: list[RetrievedChunk]) -> str:
    """Render retrieved chunks as grounded context, each with its citation."""
    blocks = []
    for i, rc in enumerate(retrieved, 1):
        blocks.append(
            f"[CHUNK {i}] source: {rc.chunk.source_doc} | section: "
            f"{rc.chunk.heading} | bm25={rc.score:.2f}\n{rc.chunk.text}"
        )
    return "\n\n".join(blocks)


GENERATOR_SYSTEM = (
    "You are the casualty-voice content author for Golden Hour, a single-"
    "player VR mass-casualty-incident triage trainer (Unreal Engine 5.8, PC "
    "VR). Every casualty is backed by the Pulse Physiology Engine, so a "
    "casualty's voice is a live clinical readout, never scripted drama. You "
    "write ONLY from the retrieved GDD context provided; you do not invent "
    "game facts. You output a single JSON object and nothing else."
)

CRITIC_SYSTEM = (
    "You are the consistency critic for Golden Hour casualty-voice content. "
    "You audit one generated item against the retrieved GDD context and an "
    "explicit rule list, list every violation precisely, and return a "
    "corrected item that fixes them while staying faithful to the request "
    "keys and the retrieved facts. You are strict: a line that a real "
    "clinician or the game's design lead would reject is a violation, not a "
    "style preference. You output a single JSON object and nothing else."
)


def build_generator_prompt(
    *,
    generator_brief: str,
    request_label: str,
    request_keys: dict,
    retrieved: list[RetrievedChunk],
    schema_json: dict,
) -> str:
    return (
        f"TASK: {generator_brief}\n\n"
        f"REQUEST ({request_label}) — author for exactly these keys:\n"
        f"{json.dumps(request_keys, indent=2)}\n\n"
        "RETRIEVED GDD CONTEXT (your only source of game facts — ground every "
        f"detail in this):\n{format_chunks(retrieved)}\n\n"
        "OUTPUT: a single JSON object matching this schema (no markdown, no "
        f"commentary):\n{json.dumps(schema_json, indent=2)}\n\n"
        "Fill the request keys into their matching fields verbatim, then "
        "author the vocalization/response, trigger, and physiology_trace "
        "grounded in the retrieved context."
    )


def build_critic_prompt(
    *,
    content_title: str,
    request_label: str,
    request_keys: dict,
    retrieved: list[RetrievedChunk],
    draft_json: str,
    verdict_schema_json: dict,
) -> str:
    return (
        f"CONTENT TYPE: {content_title}\n"
        f"REQUEST ({request_label}):\n{json.dumps(request_keys, indent=2)}\n\n"
        "RETRIEVED GDD CONTEXT (the ground truth to check against):\n"
        f"{format_chunks(retrieved)}\n\n"
        "RULE LIST — check the draft against every rule:\n"
        f"{format_rules()}\n\n"
        f"DRAFT ITEM TO AUDIT:\n{draft_json}\n\n"
        "Review the draft against each rule. If it breaks any rule, list each "
        "break in `violations` (name the rule number and what is wrong), set "
        "`passed` to false, and put a fixed version in `corrected_item` that "
        "satisfies every rule while keeping the request keys and staying "
        "grounded in the retrieved context. If the draft is already clean, set "
        "`passed` true, leave `violations` empty, and copy the draft unchanged "
        "into `corrected_item`.\n\n"
        "OUTPUT: a single JSON object matching this schema (no markdown, no "
        f"commentary):\n{json.dumps(verdict_schema_json, indent=2)}"
    )
