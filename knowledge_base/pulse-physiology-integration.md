# Pulse Physiology Integration

> **Status**: Draft
> **Author**: game-designer
> **Last Updated**: 2026-07-15
> **Last Verified**: 2026-07-15
> **Implements Pillar**: Pillar 1 (Clinical truth under pressure)

## Summary

This system adopts the official **Pulse Unreal Plugin** (Kitware + Lumeto,
Apache 2.0) as the whole-body human physiology simulation backend for every
casualty. One engine instance simulates one patient on one CPU core at
~5–10x real time; because that does not scale to 10–30 concurrent casualties
on any platform (least of all Quest), this system also owns the
**physiology-LOD strategy**: a small budgeted pool of live engines for
near/actively-treated casualties, and pre-baked serialized physiology
trajectories for distant/untriaged ones. The official Pulse Unreal Plugin IS
the buy-over-build path for physiology under the project's third-party
acceleration strategy (see `game-concept.md` Technical Considerations); the
Week-1 UE 5.8 recompile spike below is what ratifies it via the Phase-3 ADR
referenced in Open Questions.

> **Quick reference** — Layer: `Foundation` · Priority: `MVP` · Key deps: `None`

## Overview

Every clinical claim this game makes — that a tourniquet actually stops a
bleed, that an untreated tension pneumothorax actually kills, that a
casualty's face actually reflects their real state — depends on this system
being trustworthy. It exists to give every other system a source of ground
truth that behaves like real physiology instead of scripted numbers.

Key facts driving this design:
- Apache 2.0 licensed; the Unreal plugin was co-developed by Kitware and Lumeto and funded by an Epic MegaGrant, exposing the engine via a **Blueprint Actor Component** — a strong fit for this project's Blueprint-only codebase.
- Models the exact insults and interventions this scenario needs: hemorrhage, tension pneumothorax, airway obstruction, plus tourniquet, wound packing, needle decompression, chest seal, NPA/OPA, and supplemental oxygen.
- Engine state serializes to JSON/binary and reloads instantly — this is what makes pre-baked casualty trajectories viable for instant spawn and for the Quest platform split.
- **HARD CONSTRAINT (active POC risk)**: the official plugin targets UE 4.26/5.0 only (this project is on 5.8 — a recompile is required and unverified, PC VR). Kitware also ships Win64-only libraries (no supported Android/Quest build path for live simulation) — this is a real constraint but is **deferred to the Alpha milestone** (Quest is not in the POC; see `game-concept.md` Platform).

## Player Fantasy

The trainee never interacts with this system directly — they experience it
only as a casualty whose chest genuinely rises and falls, whose pulse
genuinely responds to a tourniquet. This system exists to make Pillar 1 and
Pillar 2's promises literally true rather than aesthetic claims.

## Detailed Design

### Core Rules

- Each "live" casualty owns one Pulse physiology component instance, running within a budgeted pool of concurrent live engines. For the POC this budget is a PC VR-only concern (Quest is deferred to the Alpha milestone, feasibility-gated — see `systems-index.md` High-Risk Systems).
- Casualties outside that pool run from a pre-baked, serialized state trajectory (with authored treated/untreated branch points per archetype) instead of a live engine, and are promoted to a live engine when the trainee approaches or begins treating them.
- This live/pre-baked LOD split is an established, feasible pattern for scaling simulation fidelity across many concurrent actors (only the actor(s) under direct attention get full-fidelity live simulation, everything else runs a cheaper approximation) — a known-shape engineering approach for this project to apply, not a speculative gamble. The open work is tuning its specific triggers and budgets (below), not proving the pattern itself.
- [To be designed] — exact promotion/demotion triggers (distance threshold vs. explicit "begin assessment" action), tick rate, and how many live engines the POC budgets on each platform.

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
| Casualty Model | Casualty Model depends on this | Every casualty actor owns a physiology component sourced from this system |
| Treatment & Interventions | Treatment & Interventions depends on this | Every intervention verb maps 1:1 to a Pulse action call |
| Casualty Facial Animation | Casualty Facial Animation depends on this | Provides raw physiology (HR, pressures, SpO2, respiration rate, level of consciousness, hemorrhage, injuries, arrest); that system derives pain, features, and expression from these — pain and affect are NOT outputs of this system |
| Scenario Authoring & Data | Scenario Authoring & Data depends on this | Casualty archetypes are authored as Pulse patient files/conditions and pre-baked state trajectories |

## Tuning Knobs

| Parameter | Current Value | Safe Range | Effect of Increase | Effect of Decrease |
|-----------|--------------|------------|-------------------|-------------------|
| Engine tick rate | 20 ms (Pulse default) | [To be designed] | Higher fidelity, higher CPU cost | Lower CPU cost, coarser physiology response |
| Max concurrent live engines (PC VR — POC target platform; Quest budget deferred to the Alpha milestone, feasibility-gated) | [To be designed] | [To be designed] | More casualties get full-fidelity live physiology | More casualties run pre-baked-only, less responsive to unexpected trainee actions |
| LOD promotion distance/trigger | [To be designed] | [To be designed] | | |

## Visual/Audio Requirements

[To be designed] — this system has no direct visual/audio output of its own; see `casualty-facial-animation.md` for the presentation layer this system drives

## Game Feel

### Feel Reference

[To be designed]

### Input Responsiveness

[To be designed]

### Animation Feel Targets

[To be designed]

### Impact Moments

[To be designed]

### Weight and Responsiveness Profile

[To be designed]

### Feel Acceptance Criteria

- [ ] [To be designed]

## UI Requirements

[To be designed] — this is a backend system with no direct UI

## Cross-References

| This Document References | Target GDD | Specific Element Referenced | Nature |
|--------------------------|-----------|----------------------------|--------|
| "Casualty archetypes authored as Pulse patient files + baked trajectories" | `design/gdd/scenario-authoring-data.md` | Casualty archetype authoring format | Data dependency |
| "Facial expression is derived by that system from this system's output" | `design/gdd/casualty-facial-animation.md` | Raw physiology outputs (vitals, LOC, hemorrhage, injuries, arrest) consumed by the facial pipeline's Stage 1 | Ownership handoff |
| "The Pulse integration contract is the portable simulation core of a future external-platform deliverable" | `design/gdd/addendum-physiology-response-plugin.md` | Actions-in/vitals-out interface contract (Full Vision addendum, out of POC scope) | Ownership handoff |

## Acceptance Criteria

- [ ] GIVEN a casualty archetype has a pre-baked state trajectory, WHEN that casualty spawns, THEN it loads instantly without a runtime stabilization cost
- [ ] GIVEN the trainee approaches or begins treating a pre-baked casualty, WHEN the promotion trigger fires, THEN the casualty switches to a live engine at the correct point in its trajectory
- [ ] Performance: Vitals-update latency and frame budget are maintained at 90Hz PC VR (POC target) with the target casualty count — [To be designed] (pending the Week-1 PC VR spike). A 72Hz Quest target is deferred to the Alpha milestone, feasibility-gated — not a POC acceptance criterion.
- [ ] No hardcoded values in implementation — tick rate, live-engine budget, and promotion distance are data-driven

## Open Questions

| Question | Owner | Deadline | Resolution |
|----------|-------|----------|-----------|
| Will the official Pulse Unreal Plugin recompile against UE 5.8, or does this require wrapping the Pulse C API directly? | unreal-specialist | Week-1 technical spike | → ADR (Phase 3) — not a GDD-time decision |
| What is the actual per-engine memory footprint (not published by Kitware)? | unreal-specialist | Week-1 technical spike | [To be designed] |
| Does the current plugin build surface every needed intervention (needle decompression, chest seal, wound packing, NPA/OPA) at the Blueprint layer, or only in the C++ core? | unreal-specialist | Week-1 technical spike | [To be designed] |
| What is the Quest-viable live-engine budget once rendering and voice recognition are also running? | unreal-specialist | Alpha-milestone feasibility spike — deferred, not POC-blocking | [To be designed] |

## Build Agents

- Research crew pulls plugin and SDK documentation ahead of the Week-1 recompile spike.
- Engineering pair runs the Week-1 recompile spike and produces the GO/NO-GO evidence, then wires the live casualty in Week 2.
- Adversarial QA agent attacks the packaged Tier-1 loop in Weeks 5-6 (bonus scope).

Mapped in the compiled GDD's build-time agent plan (§12.1).
