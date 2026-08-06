# Voice Command System

> **Status**: Draft
> **Author**: game-designer
> **Last Updated**: 2026-07-15
> **Last Verified**: 2026-07-15
> **Implements Pillar**: Pillar 5 (The scene listens — communication is a mechanic; primary — per product-owner direction (2026-07-16)), Pillar 3 (Doctrine, not heroics — closed-loop communication is itself real doctrine)

## Summary

A two-tier voice architecture: **Tier 1** (always available, both
platforms) runs on-device, fully offline speech recognition (Whisper via the
Runtime Speech Recognizer plugin) through a **closed command grammar /
intent matcher** — not open conversation — for medical actions and triage
calls; **Tier 2** (optional, config-gated) adds LLM-based free-form dialogue
for connected/PC VR sites only. Every voice-driven action has a **mandatory
non-voice hand-menu fallback**, both for accessibility and because a real
MCI soundscape is a genuinely hard environment for speech recognition. Per
product-owner direction (2026-07-16), Runtime Speech Recognizer + Runtime
Audio Importer are the fast-track implementation candidate for Tier 1
(third-party acceleration strategy — see `game-concept.md` Technical
Considerations), to be ratified by a Phase-3 ADR after the voice spike (see
Open Questions). Per product-owner direction (2026-07-16), voice interaction with
physiologically-accurate casualty response is elevated to design Pillar 5
(`game-concept.md`) — this system is its primary implementation, with the
casualty-response side owned by `casualty-model.md`/`triage-system.md`. The
pillar's long-term vision — monitoring the trainee's own vocal tone and
stress level so casualties and AI teammates respond to *how* a command is
delivered — is post-MVP (Full Vision tier), out of POC scope; the Tier-1
offline mic pipeline is the foundation it would build on.

> **Quick reference** — Layer: `Core` · Priority: `MVP` · Key deps: `VR Interaction & Locomotion`

## Overview

Voice is how the trainee sorts a crowd of casualties and calls for help —
mirroring exactly how a real MCI responder works — not a magic command
console. This system exists to make that channel reliable, offline-capable,
and honest about its own limits.

Key facts driving this design:
- On-device Whisper (Runtime Speech Recognizer, Fab — supports UE 4.27–5.8 including Quest/Android) plus Runtime Audio Importer for mic capture/VAD feeds a closed command grammar/intent matcher — fully offline, audio never leaves the headset.
- On Quest specifically, design for **VAD-chunked batch decode with tiny/base quantized models**, not continuous streaming — community benchmarks report Android live-streaming recognition running ~5x slower than real time, while batch mode stays fast.
- Every voice action needs a non-voice hand-menu fallback — this is both an accessibility requirement and a resilience requirement against recognition failure in a loud, chaotic scene.
- Framed explicitly as a **communication-training mechanic** (METHANE reports, closed-loop communication), not merely an input-replacement convenience — published evidence shows voice commands don't measurably improve raw task performance, but closed-loop communication training itself shows sustained real skill gains, and that is the actual training objective here.
- Per product-owner direction (2026-07-16), this system is the primary implementation of Pillar 5 (the scene listens — communication is a mechanic): a casualty's response to a voice command always traces to that casualty's physiological state (consciousness, hearing, mobility). The pillar's long-term vision — trainee vocal-tone/stress monitoring with adaptive casualty/AI-teammate response — is Full Vision tier, not POC.

## Player Fantasy

Your voice is how you sort a crowd and call for help — just like a real MCI
responder — never a magic command console that does more than doctrine
allows.

## Detailed Design

### Core Rules

- **Tier 1 (always on, both platforms — PC VR is the POC target platform; Quest is Alpha-milestone, feasibility-gated)**: mic audio → VAD gating → on-device Whisper transcription → closed grammar/intent matcher (synonym table + fuzzy matching) → resolved game action. No network call.
- **Tier 2 (optional, config-gated)**: free-form dialogue via LLM intent parsing — cloud-based on connected training sites, or Runtime Local LLM on PC VR only; disabled entirely on offline Quest deployments.
- Every command resolvable via voice must also be resolvable via a world-space hand-menu action — no voice-exclusive verbs.
- [To be designed] — push-to-talk vs. VAD-gated open-mic decision; confirmation/echo-back loop behavior on low-confidence recognition ("Say again?").

### States and Transitions

[To be designed]

### Interactions with Other Systems

[To be designed]

## Formulas

[To be designed]

## Edge Cases

| Scenario | Expected Behavior | Rationale |
|----------|------------------|-----------|
| [To be designed] | | |

## Dependencies

| System | Direction | Nature of Dependency |
|--------|-----------|---------------------|
| VR Interaction & Locomotion | This depends on VR Interaction & Locomotion | Push-to-talk input coexistence; world-space feedback UI attach point |
| Patient Assessment | Patient Assessment depends on this | Examine-verb voice commands resolve through this system's grammar |
| Triage System | Triage System depends on this | Global-sort commands and spoken category calls resolve through this system |
| Incident Command & Comms | Incident Command & Comms depends on this | METHANE report delivery is voice-driven |
| HUD & World-Space UI | HUD & World-Space UI depends on this | Voice command visual feedback surfaces through world-space UI |

## Tuning Knobs

| Parameter | Current Value | Safe Range | Effect of Increase | Effect of Decrease |
|-----------|--------------|------------|-------------------|-------------------|
| Whisper model size (per platform) | [To be designed] — larger tiers on PC VR (POC target); tiny/base on Quest deferred to the Alpha milestone, feasibility-gated | [To be designed] | Higher accuracy, higher latency/CPU cost | Lower latency/cost, lower accuracy |
| VAD energy/silence threshold | [To be designed] | [To be designed] | | |
| Per-command confidence threshold | [To be designed] | [To be designed] | Fewer false positives, more "say again" prompts | More false positives accepted |
| Max command latency budget (PC VR — POC target) | ≤0.8s (candidate target) | [To be designed] | | |
| Max command latency budget (Quest — Alpha milestone, feasibility-gated, deferred) | ≤1.5s (candidate target) | [To be designed] | | |

## Visual/Audio Requirements

| Event | Visual Feedback | Audio Feedback | Priority |
|-------|----------------|---------------|----------|
| Command recognized | World-space confirmation indicator | Short confirmation tone | High |
| Low-confidence / unrecognized command | World-space "say again?" prompt | [To be designed] | High |

## Game Feel

### Feel Reference

[To be designed]

### Input Responsiveness

| Action | Max Input-to-Response Latency (ms) | Frame Budget (at 90fps PC VR — POC target) | Notes |
|--------|-----------------------------------|------------------------|-------|
| Utterance-end to game-action | ≤800ms PC VR (candidate, POC target) | [To be designed] | Candidate target from research, not yet validated on-device. A ≤1500ms Quest candidate target is deferred to the Alpha milestone, feasibility-gated. |

### Animation Feel Targets

[To be designed]

### Impact Moments

[To be designed]

### Weight and Responsiveness Profile

[To be designed]

### Feel Acceptance Criteria

- [ ] ≥95% recognition of the command grammar at conversational volume with MCI ambient audio playing, on PC VR (POC target — candidate, needs validation)
- [ ] Zero network calls in offline mode (verifiable)
- [ ] Mic audio is never persisted or transmitted (privacy acceptance criterion)
- [ ] Deferred to the Alpha milestone (feasibility-gated, not a POC target): ≥95% recognition of the command grammar on Quest 2 with the full MCI scene rendering

## UI Requirements

| Information | Display Location | Update Frequency | Condition |
|-------------|-----------------|-----------------|-----------|
| Recognized command feedback | World-space indicator near trainee's view or on a wrist-worn element | On each recognition event | Always active while mic is engaged |

## Cross-References

| This Document References | Target GDD | Specific Element Referenced | Nature |
|--------------------------|-----------|----------------------------|--------|
| "Push-to-talk coexists with hand interaction" | `design/gdd/vr-interaction-locomotion.md` | Input binding coexistence | Rule dependency |
| "Global-sort commands and category calls resolve through this grammar" | `design/gdd/triage-system.md` | SALT command grammar meaning | Rule dependency |
| "METHANE report delivery is voice-driven" | `design/gdd/incident-command-comms.md` | METHANE report structure | Data dependency |

## Acceptance Criteria

- [ ] GIVEN a trainee is offline (PC VR, no network — POC target), WHEN they issue any Tier 1 command, THEN it resolves entirely on-device with zero network calls. (The same offline rule applies to Quest once the Alpha-milestone Quest pass is built — Quest support itself is deferred, not this offline design rule.)
- [ ] GIVEN a voice command fails to recognize, WHEN the trainee retries or opens the hand-menu, THEN the same action is achievable without voice
- [ ] Performance: Utterance-end to resolved game-action completes within the platform's latency budget — [To be designed] (pending the Week-1 PC VR latency spike; the Quest latency budget is deferred to the Alpha milestone, feasibility-gated)
- [ ] No hardcoded values in implementation — grammar/synonym table, confidence thresholds, and model tier selection are data-driven

## Open Questions

| Question | Owner | Deadline | Resolution |
|----------|-------|----------|-----------|
| Actual Quest 2 recognition latency with the full MCI scene rendering alongside it | unreal-specialist | Alpha-milestone feasibility spike — deferred, not POC-blocking | [To be designed] |
| Push-to-talk vs. always-on VAD-gated mic as the default interaction model | game-designer | Before Detailed Design is finalized | [To be designed] |
| Whether Tier 2 (LLM dialogue) is in scope for the POC at all, or purely a later-milestone note | producer / game-designer | Before this GDD is approved | Currently scoped as: noted here, not built in POC per `game-concept.md` |
| Which Tier 1 speech-recognition/mic-capture plugin implements this system (Runtime Speech Recognizer + Runtime Audio Importer is the fast-track candidate, locked by product-owner direction 2026-07-16) | unreal-specialist | Week-1 technical spike | → ADR (Phase 3) — ratifies the candidate and records the exit path (e.g., whisper.cpp direct integration) if the spike fails |
| Whether streamed Meta Quest 3 mic audio (per product-owner direction (2026-07-16): reference headset via wireless PC streaming) routes correctly into the PC-side Whisper recognizer through the streaming stack (Virtual Desktop/SteamVR audio routing) — and, per product-owner direction (2026-07-19), the equivalent Galaxy XR mic path (Virtual Desktop on Android XR, or the Samsung Game Link / Google PC Connect fallback) routing into the same PC-side recognizer | unreal-specialist | Before the Week-1 voice spike closes | [To be designed] — validated for both headsets whenever the voice Tier-3 item is pulled; if not validated by then, voice demos run on Quest 3 only |
| Glove-mode dependency: this system's mandatory hand-menu fallback for every voice action currently assumes controller-button operation; in the post-MVP UDCAP glove option (see `vr-interaction-locomotion.md`), button-free menu interaction (gesture or dwell) is unresolved, so the fallback mechanism must be redefined for glove mode before that option ships | game-designer + unreal-specialist | When the glove option is activated by a customer commitment | [To be designed] |
| How the Pillar-5 long-term vision senses trainee vocal tone/stress (on-device vocal-feature analysis over the existing Tier-1 mic pipeline vs. a third-party affect plugin), and how casualty/AI-teammate response adapts to it | game-designer + unreal-specialist | Post-MVP — when the Full Vision feature is scheduled; not POC-blocking | [To be designed] |

## Build Agents

This system is a Tier-3 demo extra: build work is pulled by the Engineering pair on a pull-based basis per the ranked extras list, and it is never scored in the POC. Mapped in the compiled GDD's build-time agent plan (§12.1).
