"""Pydantic schemas for the three casualty-voice content types.

Every generated item is structured data, not prose: the line text (or a
described non-verbal vocalization), the gating/trigger condition, the
injury/consciousness/hearing/mobility/affect keys, and a `physiology_trace`
that names the physiology variable the line derives from. The critic returns a
verdict of the same shape so a corrected item is itself schema-valid.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

# ---------------------------------------------------------------------------
# Shared enums — the POC injury space and casualty-state axes, straight from
# the GDDs (game-concept MVP §, triage-system, casualty-facial-animation).
# ---------------------------------------------------------------------------
InjuryType = Literal[
    "external hemorrhage",
    "tension pneumothorax",
    "open/sucking chest wound",
    "airway obstruction",
    "minor injury",
]
Consciousness = Literal["conscious", "altered", "unconscious"]
# "obstructed" = airway obstruction present; "distress" = breathing but
# labored (the RR>30 / respiratory-distress trigger); "normal" otherwise.
RespiratoryStatus = Literal["normal", "distress", "obstructed"]
Severity = Literal["minor", "moderate", "severe", "critical"]
DeclineStage = Literal["early", "mid", "late"]
Mobility = Literal["ambulatory", "purposeful-movement", "still"]
# How a casualty answers a spoken command — the SALT global-sort behavior,
# gated on consciousness AND hearing AND mobility (Pillar 5).
ComplianceType = Literal[
    "verbal-and-moves",  # conscious + hearing + ambulatory: complies and moves
    "verbal-acknowledgement-no-move",  # conscious + hearing, immobile: answers, cannot move
    "non-verbal-movement",  # waves / purposeful movement without intelligible words
    "no-response",  # unconscious, or conscious-but-deaf: nothing
]


class PainBark(BaseModel):
    """A short pain/plea vocalization keyed by injury x state x affect."""

    injury_type: InjuryType
    severity: Severity
    consciousness: Consciousness
    respiratory_status: RespiratoryStatus
    affect: str = Field(
        description="Appraisal/coping read, e.g. fearful, stoic, dissociated, "
        "pleading — traces to the facial pipeline's Stage 4/6 output"
    )
    is_intelligible_speech: bool = Field(
        description="False when the casualty produces only a described "
        "non-verbal vocalization (moan/gurgle/gasp/stridor) rather than words"
    )
    vocalization: str = Field(
        description="The spoken line in quotes, OR a described non-verbal "
        "vocalization in brackets, e.g. [wet gurgling on each breath]"
    )
    trigger: str = Field(
        description="When this bark fires — the gating condition in words"
    )
    physiology_trace: str = Field(
        description="The physiology variable this line derives from "
        "(e.g. SpO2, respiration rate, level of consciousness, hemorrhage rate)"
    )


class CommandResponse(BaseModel):
    """A casualty's response to a trainee voice command (SALT global sort)."""

    command: str = Field(
        description='The voice command issued, e.g. "If you can hear me, wave" '
        'or "Move to the flag if you can walk"'
    )
    injury_type: InjuryType
    consciousness: Consciousness
    can_hear: bool = Field(
        description="Hearing capability — compliance gates on this, not on "
        "leg function (Pillar 5)"
    )
    mobility: Mobility
    affect: str
    compliance: ComplianceType
    response: str = Field(
        description="The casualty's reply in quotes and/or a described action "
        "or explicit non-response, e.g. [no response — remains still]"
    )
    trigger: str = Field(description="The command + state that gates this response")
    physiology_trace: str = Field(
        description="The physiology/state variable the response traces to "
        "(level of consciousness, hearing capability, mobility state)"
    )


class AmbientDecline(BaseModel):
    """An idle vocalization that tracks physiology decay over time."""

    injury_type: InjuryType
    decline_stage: DeclineStage = Field(
        description="early = coherent complaint; mid = confusion/agitation; "
        "late = quiet moan/silence"
    )
    consciousness: Consciousness
    respiratory_status: RespiratoryStatus
    affect: str
    is_intelligible_speech: bool
    vocalization: str = Field(
        description="Spoken line in quotes OR a described non-verbal "
        "vocalization; late-stage decline trends toward moan/silence"
    )
    trigger: str = Field(
        description="The decay state that fires this idle line (no command, "
        "no trainee contact)"
    )
    physiology_trace: str = Field(
        description="The decaying physiology variable driving this stage "
        "(e.g. falling SpO2, dropping perfusion index, declining LOC)"
    )


# Discriminated by content type at the call site; each maps to one output file.
CONTENT_MODELS: dict[str, type[BaseModel]] = {
    "pain_barks": PainBark,
    "command_responses": CommandResponse,
    "ambient_decline": AmbientDecline,
}


class CriticVerdict(BaseModel):
    """The critic's ruling on one generated item."""

    passed: bool = Field(
        description="True only if the draft violates none of the rule list"
    )
    violations: list[str] = Field(
        default_factory=list,
        description="One entry per rule broken; empty when passed is true",
    )
    corrected_item: dict = Field(
        description="The revised item as a JSON object matching the content "
        "type's schema. Equals the draft unchanged when passed is true."
    )


class ContentFile(BaseModel):
    """The on-disk shape of each output/*.json content file."""

    schema_version: str = "0.1.0"
    game: str = "Golden Hour"
    content_type: str
    items: list[dict]
