"""The generation request set: which casualty states to author lines for.

Each content type has a fixed list of requests covering the POC injury space
(external hemorrhage, tension pneumothorax, open/sucking chest wound, airway
obstruction, minor injury) crossed with consciousness / respiratory /
hearing / mobility / affect states. Several requests deliberately sit on a
hard GDD rule — an unconscious casualty asked for a pain bark, a
respiratory-distress casualty, a conscious-but-deaf casualty given a
"walk to me" command — so the generate->critique->revise loop has a real
lore break to catch on a live run.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ContentType:
    """Metadata for one of the three content types."""

    key: str  # stable id, also the output filename stem
    title: str  # human label for traces/README
    model_name: str  # schema.CONTENT_MODELS key (same as `key`)
    output_filename: str
    # Anchor terms mixed into every retrieval query for this content type.
    # Kept deliberately SHORT: these are identical across every request in the
    # type, so long anchor lists dominate BM25 and flatten the per-request
    # signal. Terms that duplicate a request key (respiratory, consciousness,
    # SpO2, ...) are especially harmful here and are left to the keys.
    retrieval_terms: list[str]
    # One-line brief handed to the generator role.
    generator_brief: str


@dataclass(frozen=True)
class RequestSpec:
    """One casualty-state request within a content type."""

    content_type: str
    label: str  # short human label, appears in traces
    keys: dict[str, object]  # the state keys -> schema fields + prompt context
    # Extra retrieval terms beyond what `keys` contributes (optional).
    extra_terms: list[str] = field(default_factory=list)

    def query_terms(self) -> list[str]:
        """Key values + extra terms, as retrieval query tokens.

        Two subtleties, both load-bearing for retrieval quality:

        1. `bool` subclasses `int`, so a bare `isinstance(v, int)` would let
           `can_hear: True` leak the meaningless token "true" into the query.
           The explicit bool guard drops it.
        2. The per-request terms are emitted TWICE. BM25 scores by term
           frequency, and the content-type anchor terms are identical across
           every request in a type — without this weighting the shared
           boilerplate dominates the score and structurally different requests
           retrieve byte-identical chunk sets.
        """
        values = [
            str(v)
            for v in self.keys.values()
            if isinstance(v, str) or (isinstance(v, int) and not isinstance(v, bool))
        ]
        terms = [*values, *self.extra_terms]
        return [*terms, *terms]


CONTENT_TYPES: dict[str, ContentType] = {
    "pain_barks": ContentType(
        key="pain_barks",
        title="Pain / plea barks",
        model_name="pain_barks",
        output_filename="pain_barks.json",
        retrieval_terms=["casualty", "vocalization", "pain"],
        generator_brief=(
            "Author one short pain/plea bark a wounded casualty emits, keyed "
            "by injury_type x severity x consciousness x respiratory_status x "
            "affect."
        ),
    ),
    "command_responses": ContentType(
        key="command_responses",
        title="Command-response lines",
        model_name="command_responses",
        output_filename="command_responses.json",
        retrieval_terms=["voice command", "SALT global sort", "compliance"],
        generator_brief=(
            "Author what a casualty says and/or does when the trainee issues a "
            "voice command. Compliance gates on consciousness AND hearing AND "
            "mobility — never on leg function alone."
        ),
    ),
    "ambient_decline": ContentType(
        key="ambient_decline",
        title="Ambient decline vocalizations",
        model_name="ambient_decline",
        output_filename="ambient_decline.json",
        retrieval_terms=["casualty", "vocalization", "deterioration"],
        generator_brief=(
            "Author a non-command idle vocalization that tracks physiology "
            "decay over time. early = coherent complaint; mid = "
            "confusion/agitation; late = quiet moan/silence. Each line traces "
            "to a decaying physiology variable."
        ),
    ),
}


# ---------------------------------------------------------------------------
# Pain / plea barks
# ---------------------------------------------------------------------------
PAIN_BARK_REQUESTS: list[RequestSpec] = [
    RequestSpec(
        content_type="pain_barks",
        label="external hemorrhage / severe / conscious / fearful",
        keys={
            "injury_type": "external hemorrhage",
            "severity": "severe",
            "consciousness": "conscious",
            "respiratory_status": "normal",
            "affect": "fearful",
        },
    ),
    RequestSpec(
        content_type="pain_barks",
        label="tension pneumothorax / critical / conscious / respiratory distress",
        keys={
            "injury_type": "tension pneumothorax",
            "severity": "critical",
            "consciousness": "conscious",
            "respiratory_status": "distress",
            "affect": "panicked",
        },
        extra_terms=["needle decompression", "SpO2", "gasping"],
    ),
    RequestSpec(
        content_type="pain_barks",
        label="airway obstruction / severe / conscious / obstructed",
        keys={
            "injury_type": "airway obstruction",
            "severity": "severe",
            "consciousness": "conscious",
            "respiratory_status": "obstructed",
            "affect": "distressed",
        },
        extra_terms=["stridor", "gurgle", "airway"],
    ),
    RequestSpec(
        content_type="pain_barks",
        label="external hemorrhage / critical / UNCONSCIOUS",
        keys={
            "injury_type": "external hemorrhage",
            "severity": "critical",
            "consciousness": "unconscious",
            "respiratory_status": "normal",
            "affect": "unresponsive",
        },
        extra_terms=["level of consciousness", "moan"],
    ),
    RequestSpec(
        content_type="pain_barks",
        label="minor injury / minor / conscious / stoic (Green)",
        keys={
            "injury_type": "minor injury",
            "severity": "minor",
            "consciousness": "conscious",
            "respiratory_status": "normal",
            "affect": "stoic",
        },
        extra_terms=["minimal", "ambulatory", "walking wounded"],
    ),
]

# ---------------------------------------------------------------------------
# Command-response lines
# ---------------------------------------------------------------------------
COMMAND_RESPONSE_REQUESTS: list[RequestSpec] = [
    RequestSpec(
        content_type="command_responses",
        label='"walk to me" / minor injury / conscious / hearing / ambulatory',
        keys={
            "command": "If you can hear me and need help, walk to me",
            "injury_type": "minor injury",
            "consciousness": "conscious",
            "can_hear": True,
            "mobility": "ambulatory",
            "affect": "frightened but cooperative",
        },
        extra_terms=["walk to me", "assessed third"],
    ),
    RequestSpec(
        content_type="command_responses",
        label='"wave your arm" / external hemorrhage / conscious / hearing / still',
        keys={
            "command": "Wave your arm or make a purposeful movement",
            "injury_type": "external hemorrhage",
            "consciousness": "conscious",
            "can_hear": True,
            "mobility": "still",
            "affect": "weak, pleading",
        },
        extra_terms=["wave your arm", "purposeful movement", "assessed second"],
    ),
    RequestSpec(
        content_type="command_responses",
        label='"if you can hear me, wave" / tension pneumothorax / UNCONSCIOUS',
        keys={
            "command": "If you can hear me, wave your hand",
            "injury_type": "tension pneumothorax",
            "consciousness": "unconscious",
            "can_hear": False,
            "mobility": "still",
            "affect": "unresponsive",
        },
        extra_terms=["no response", "still", "assessed first"],
    ),
    RequestSpec(
        content_type="command_responses",
        label='"walk to the flag" / minor injury / conscious / DEAF / ambulatory',
        keys={
            "command": "Move to the flag if you can walk",
            "injury_type": "minor injury",
            "consciousness": "conscious",
            "can_hear": False,
            "mobility": "ambulatory",
            "affect": "confused, straining to understand",
        },
        extra_terms=["hearing", "cannot hear", "does not comply"],
    ),
    RequestSpec(
        content_type="command_responses",
        label='"squeeze my hand" / open chest wound / altered / hearing / purposeful',
        keys={
            "command": "Squeeze my hand if you can hear me",
            "injury_type": "open/sucking chest wound",
            "consciousness": "altered",
            "can_hear": True,
            "mobility": "purposeful-movement",
            "affect": "confused",
        },
        extra_terms=["obeys commands", "mental status", "chest seal"],
    ),
]

# ---------------------------------------------------------------------------
# Ambient decline vocalizations
# ---------------------------------------------------------------------------
AMBIENT_DECLINE_REQUESTS: list[RequestSpec] = [
    RequestSpec(
        content_type="ambient_decline",
        label="external hemorrhage / EARLY / conscious",
        keys={
            "injury_type": "external hemorrhage",
            "decline_stage": "early",
            "consciousness": "conscious",
            "respiratory_status": "normal",
            "affect": "anxious but lucid",
        },
        extra_terms=["perfusion", "blood loss", "coherent complaint"],
    ),
    RequestSpec(
        content_type="ambient_decline",
        label="external hemorrhage / MID / altered (confusion)",
        keys={
            "injury_type": "external hemorrhage",
            "decline_stage": "mid",
            "consciousness": "altered",
            "respiratory_status": "normal",
            "affect": "confused, agitated",
        },
        extra_terms=["perfusion index", "shock", "compensating", "agitation"],
    ),
    RequestSpec(
        content_type="ambient_decline",
        label="tension pneumothorax / MID / altered / distress",
        keys={
            "injury_type": "tension pneumothorax",
            "decline_stage": "mid",
            "consciousness": "altered",
            "respiratory_status": "distress",
            "affect": "air-hungry, frightened",
        },
        extra_terms=[
            "SpO2",
            "hypoxia",
            "respiration rate",
            "tension pneumothorax",
            "needle decompression",
            "compensating",
            "agitation",
        ],
    ),
    RequestSpec(
        content_type="ambient_decline",
        label="open/sucking chest wound / LATE / unconscious",
        keys={
            "injury_type": "open/sucking chest wound",
            "decline_stage": "late",
            "consciousness": "unconscious",
            "respiratory_status": "distress",
            "affect": "fading",
        },
        extra_terms=[
            "falling SpO2",
            "level of consciousness",
            "quiet moan",
            "open sucking chest wound",
            "chest seal",
            "unconscious vocalization suppressed",
        ],
    ),
    RequestSpec(
        content_type="ambient_decline",
        label="airway obstruction / LATE / unconscious / obstructed",
        keys={
            "injury_type": "airway obstruction",
            "decline_stage": "late",
            "consciousness": "unconscious",
            "respiratory_status": "obstructed",
            "affect": "agonal",
        },
        extra_terms=["hypoxia", "silence", "agonal", "SpO2"],
    ),
]

REQUESTS_BY_TYPE: dict[str, list[RequestSpec]] = {
    "pain_barks": PAIN_BARK_REQUESTS,
    "command_responses": COMMAND_RESPONSE_REQUESTS,
    "ambient_decline": AMBIENT_DECLINE_REQUESTS,
}
