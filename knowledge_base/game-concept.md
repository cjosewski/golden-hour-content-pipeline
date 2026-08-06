# Game Concept: Golden Hour

*Created: 2026-07-15*
*Status: Draft*

> **Working title note**: "Golden Hour" refers to the EMS principle that trauma
> outcomes hinge on the first hour of care. Placeholder — confirm or replace
> before this document is approved.

---

## Core Identity

| Aspect | Detail |
| ---- | ---- |
| **Genre** | VR Serious Game / Clinical Training Simulator (first-person simulation) |
| **Platform** | PC VR (Windows build, OpenXR) — POC target; reference headset Meta Quest 3 via wireless PC streaming, joined by Samsung Galaxy XR as a second first-class streamed headset for development and delivery — Quest 3 remains the primary reference headset (per product-owner direction (2026-07-19)); flagship peripheral: Virtuix Omni One Enterprise motion treadmill (per product-owner direction (2026-07-16)). Meta Quest standalone on-device build — Alpha+ investigation, feasibility-gated; NOT in the POC. |
| **Target Audience** | EMS/paramedic trainees, fire-EMS departments, EMS training academies |
| **Player Count** | Single-player (POC). Architected so a live multiplayer instructor/team-training mode can be added later — not built for POC. |
| **Session Length** | ~15–20 min in-scenario + prebrief and debrief (~30–40 min total training block); Virtuix Omni treadmill sessions are additionally capped at ≤30 min continuous with mandatory hydration breaks per manufacturer safety guidance (per product-owner direction (2026-07-16)) — the existing scenario length already sits comfortably under this cap |
| **Monetization** | Not a design-time decision — presumed per-seat/per-department training license, business-side |
| **Estimated Scope** | Large (9+ months) — this document scopes the POC vertical slice first |
| **Comparable Titles** | SimX (Triage Mass Casualty scenario), Health Scholars (voice-driven clinical VR), MedCognition PerSim (AR patient encounters), DHS S&T EDGE (multi-role active-shooter trainer) |

---

## Core Fantasy

You are the calm, competent clinician who walks into chaos and makes the calls
that decide who lives. Not a hero with a weapon — a professional whose only
tools are trained hands, clear judgment, and a stethoscope. The fantasy is
mastery under pressure: reading a scene in seconds, sorting the salvageable
from the lost, and doing exactly what doctrine says — no more, no less — while
the environment keeps trying to make you panic. As the paramedic, you never
fight and are never armed — your victory condition is never "eliminate the
threat" — it is "everyone who could be saved, was."

---

## Unique Hook

It's like SimX's Triage Mass Casualty scenario, AND ALSO the casualty's own
face is a physiological readout driven by a validated whole-body human
physiology simulation, not scripted animation — live and real-time for
casualties under active assessment or nearby the trainee, and
physiology-derived, pre-computed trajectories (branching at authored decision
points as the trainee acts) for casualties further away — so learning to read
distress, pallor, respiratory effort, and consciousness on a human face IS the
assessment skill being trained, everywhere in the scene. AND ALSO the scene itself is not a
static stage: it began in a zone that is merely *cleared*, not *secure*, and
can re-escalate mid-treatment, forcing the trainee to interrupt care and
adapt exactly the way a real Rescue Task Force response does. AND ALSO the scene answers the trainee's voice: the global sort, triage
calls, and casualty interaction are spoken, and a casualty's compliance
always traces to their actual physiological state — one who cannot hear,
understand, or move does not respond, and that non-response IS the clinical
finding (per product-owner direction (2026-07-16); see Pillar 5 — whose
long-term vision adds trainee vocal-tone/stress monitoring, with casualties
and AI teammates responding to *how* a command is delivered).

---

## Player Experience Analysis (MDA Framework)

### Target Aesthetics (What the player FEELS)

| Aesthetic | Priority | How We Deliver It |
| ---- | ---- | ---- |
| **Sensation** (sensory pleasure) | 3 | Clinical-documentary visual/audio realism (harsh emergency lighting, radio traffic, dust) — grounded, not spectacular |
| **Fantasy** (make-believe, role-playing) | 2 | Full embodiment of the competent-paramedic identity; hands do the work, voice does the communication |
| **Narrative** (drama, story arc) | 4 | The incident itself has a shape — arrival, escalating chaos, extraction — but is systemic, not scripted cutscenes |
| **Challenge** (obstacle course, mastery) | 1 | Doctrine-correct decisions under time and threat pressure, scored against real EMS benchmarks |
| **Fellowship** (social connection) | N/A | Not targeted in POC (single-player); roadmap item for multiplayer team training |
| **Discovery** (exploration, secrets) | 3 | Diagnostic discovery — reading vitals and expression to uncover what's actually wrong with a casualty |
| **Expression** (self-expression, creativity) | N/A | Not a design goal — doctrine constrains "correct" play deliberately |
| **Submission** (relaxation, comfort zone) | N/A | Explicitly not targeted — this is a high-stakes training simulation |

### Key Dynamics (Emergent player behaviors)

- Players develop a scanning heuristic: global voice-driven sort before individual assessment, mirroring real SALT triage cognition.
- Under time pressure, doctrine steps (MARCH order) start to feel like internalized reflex rather than a checklist.
- Players feel genuine anxiety at the shelter-in-place re-escalation event and must consciously re-prioritize mid-treatment — this is the intended stress-inoculation moment. **This intentional stress-inoculation moment requires the distress-support pathway (see `duty-of-care-flow.md` Open Questions) to be explicitly resolved BEFORE this feature is built — a must-resolve-before-build gate, not an open-ended design question.**
- Players begin narrating actions out loud even when not strictly required by voice-command grammar (closed-loop communication habit transfer — the desired real-world skill carryover).

### Core Mechanics (Systems we build)

1. Voice- and hand-driven SALT global sort and individual patient assessment
2. MARCH-ordered life-threat treatment interventions mapped 1:1 to a live physiology simulation's actions
3. A dynamic hot/warm/cold zone and threat system that gates permitted actions and can re-escalate mid-scenario
4. Casualty facial and vocal expression as a clinical instrument driven by the physiology simulation — live and real-time for casualties under active assessment or nearby the trainee, physiology-derived pre-computed trajectories (branching at authored decision points) for casualties elsewhere (see `casualty-model.md`)
5. Scored extraction to a Casualty Collection Point with full action logging feeding an end-of-scenario summary

---

## Player Motivation Profile

### Primary Psychological Needs Served

| Need | How This Game Satisfies It | Strength |
| ---- | ---- | ---- |
| **Autonomy** (freedom, meaningful choice) | Trainee chooses assessment order, treatment sequence, and pacing within doctrine bounds; multiple valid paths through the incident | Core |
| **Competence** (mastery, skill growth) | Explicit scoring against real EMS benchmarks; immediate physiological/facial feedback to every action; mastery of doctrine visibly changes casualty outcomes | Core |
| **Relatedness** (connection, belonging) | AI Rescue Task Force escort and casualties provide relational stakes in the POC; full relatedness (live team training) is a roadmap multiplayer feature | Supporting |

### Player Type Appeal (Bartle Taxonomy)

- [x] **Achievers** (goal completion, collection, progression) — How: explicit scoring rubric, named EMS benchmarks (under-triage <5%, tourniquet ≤120s) to chase
- [x] **Explorers** (discovery, understanding systems, finding secrets) — How: reading physiology through vitals and expression is itself a diagnostic-discovery loop
- [ ] **Socializers** (relationships, cooperation, community) — Not targeted in POC (see roadmap)
- [ ] **Killers/Competitors** (domination, PvP, leaderboards) — Violence-as-fun and domination/PvP explicitly excluded; see anti-pillars

### Flow State Design

- **Onboarding curve**: a mandatory prebrief scene teaches VR controls (point/grab/teleport/voice — see `vr-interaction-locomotion.md`'s First-Run Onboarding sub-scope) plus SALT global-sort and MARCH treatment order *before* the scenario begins — the first 10 minutes are explanation, controls practice, and psychological-safety framing, not gameplay.
- **Difficulty scaling**: casualty count, injury severity mix, and threat re-escalation timing are scenario tuning knobs (see `scenario-authoring-data.md`), not hardcoded.
- **Feedback clarity**: every intervention produces an immediate, physiologically-grounded change in vitals and facial expression; the end-of-scenario score screen makes overall performance legible.
- **Recovery from failure**: a missed triage call or doctrine violation is never a "game over" — it surfaces as a specific, actionable item in the post-scenario debrief. Failure teaches; it does not punish or shame (see Pillar 4).

---

## Core Loop

### Moment-to-Moment (30 seconds)

Approach a casualty. Read their face, vitals, and movement state. Call their
triage category out loud. If a MARCH-order life threat is present and within
warm-zone scope, treat it immediately.

### Short-Term (5–15 minutes)

Work through a casualty cluster under RTF escort: locate → sort (SALT global
sort by voice) → individually assess → treat MARCH-order life threats → tag →
extract to the Casualty Collection Point — while the zone/threat state can
shift underneath you (e.g., a shelter-in-place order interrupts active
treatment).

### Session-Level (15–20 minutes)

The full incident, from arrival at the scene to CCP handoff of every located
casualty, ending in the score and summary screen. (Structured METHANE radio
reporting is a Vertical Slice feature — see `incident-command-comms.md` — not
required for the POC's session loop to close.)

### Long-Term Progression (Platform vision — beyond POC)

Trainees progress across a growing scenario library (different incident
types, increasing casualty count and chaos), with competency tracked over
time and instructor-assigned remediation scenarios. Not present in the POC.

### Retention Hooks

- **Curiosity**: "What happens if I make a different call on this casualty?"
- **Investment**: personal score history — a streak of scenarios under the 5% under-triage benchmark.
- **Mastery**: chasing the tourniquet ≤120s and under-triage <5% / over-triage <50% benchmarks.
- **Social**: roadmap — cohort leaderboards / instructor review, not in POC.

---

## Game Pillars

### Pillar 1: Clinical truth under pressure

The physiology, the doctrine, and the consequences must be real — nothing is
faked for spectacle.

*Design test*: If a scripted dramatic beat (e.g., a casualty screaming for
effect) conflicts with what the physiology simulation would actually produce
given that casualty's state, the physiology simulation wins.

### Pillar 2: The face is a vital sign

Casualty faces are a clinical instrument the trainee is trained to read, not
decoration. Casualties under active assessment or nearby the trainee run a
live physiology engine driving their face in real time; casualties elsewhere
run physiology-derived, pre-computed trajectories that branch at authored
decision points as the trainee acts (see `casualty-model.md`'s LOD system) —
but every expression, live or pre-computed, still traces back to a real
physiology variable, never a scripted "looks dramatic" choice.

*Design test*: If an animation or narrative request calls for an expression
that cannot be traced back to a physiology variable (pain, consciousness,
respiratory distress, pallor), it does not ship.

### Pillar 3: Doctrine, not heroics

Every permitted trainee action is bounded by real EMS scope-of-practice and
zone rules; there is no "do everything" button.

*Design test*: If a feature would let the trainee perform a full workup or an
out-of-scope intervention in the warm zone without it being flagged as a
scored doctrine violation, the feature is redesigned.

### Pillar 4: Safe to fail, hard to master

Failure teaches — it never punishes or shames. Mastery is real, measurable,
and earned.

*Design test*: Every failure state routes to a specific debrief insight. None
of them produce a hard game-over, a jump-scare, or a scare-tactic penalty.

### Pillar 5: The scene listens — communication is a mechanic

*(Added per product-owner direction (2026-07-16).)* Talking is not an input
convenience; it is a core skill being trained. Casualties respond to the
trainee's voice according to their actual physiological state: a casualty
who can hear and walk complies with "walk to me"; one who cannot, doesn't —
and that difference IS the triage signal. The long-term vision extends this
in two ways: the system will monitor the trainee's own vocal tone and stress
level, and casualties and AI teammates will respond to *how* the trainee
communicates — a calm, clear command earning compliance that a panicked one
would not (post-MVP; see Scope Tiers, Full Vision).

*Design test*: If a casualty's response to the trainee's voice cannot be
traced to that casualty's physiological state (consciousness, hearing,
mobility), it does not ship.

### Anti-Pillars (What This Game Is NOT)

- **NOT a shooter**: violence is never the objective, the win condition, or
  the fun — and no scenario ever frames killing as success. This is NOT an
  absolute weapon ban (per product-owner direction, 2026-07-16): the
  platform vision includes armed trainee roles (e.g., law-enforcement
  officers in police-training scenarios) where weapon handling is a
  role-gated capability governed by that role's own real-world duty and
  use-of-force doctrine — scored and debriefed like every other action,
  never celebrated. Adding weapon capability is the platform's last
  resort: built only where a role's doctrine genuinely requires it, never
  as a default. The POC's paramedic trainee is
  unarmed for the entire experience, which is doctrinally accurate for EMS
  in a Rescue Task Force.
- **NOT a haptic skills trainer**: VR without force feedback does not
  reliably teach fine motor technique (tourniquet windlass tension, needle
  angle, packing depth). This is explicitly out of scope — the sim trains
  decisions, sequence, and communication, and states this boundary honestly
  rather than overclaiming what it teaches.
- **NOT gratuitous**: casualty injuries and gore render at the minimum
  fidelity needed for clinical recognition, never for shock value. This
  protects both the training legitimacy and the wellbeing of trainees who are
  themselves working professionals, not an audience seeking spectacle.
- **NOT an unguided trauma exposure**: psychological-safety scaffolding
  (prebrief, always-available opt-out, structured debrief) is mandatory
  infrastructure, not a UI afterthought — see `duty-of-care-flow.md`.

---

## Inspiration and References

| Reference | What We Take From It | What We Do Differently | Why It Matters |
| ---- | ---- | ---- | ---- |
| **SimX — Triage Mass Casualty** | The moderator-controlled MCI scenario structure and its objective checklist (scene safety, PPE, life-threat recognition) | Physiology-driven *dynamic* re-triage instead of scripted vitals; casualty expression is a live clinical instrument, not canned animation | Direct commercial precedent that VR MCI triage training is a real, funded training category |
| **Health Scholars** | Voice-as-communication-training framing; closed-loop communication as an explicit learning objective | A closed command grammar plus an optional free-dialogue tier, rather than voice-only code-leading; treatment is physical/hand-driven, not purely verbal; casualty compliance with a voice command always traces to that casualty's own physiological state (consciousness, hearing, mobility) rather than a recognized-command trigger alone (Pillar 5 — per product-owner direction, 2026-07-16) | Proves voice-driven clinical VR is CE-relevant and already accepted by the EMS training market |
| **DHS S&T EDGE** | Any-participant-POV replay as the after-action-review gold standard | POC ships single-player with score+summary only; full timeline-replay AAR is specified in the GDDs but scheduled for a later milestone, not the POC | Establishes that active-shooter multi-role VR training is an established, government-backed category, and sets the debrief bar we're deliberately deferring |

**Non-game inspirations**: real MCI after-action reports; the Hartford
Consensus "Stop the Bleed" campaign materials; the calm, procedural tone of
professional EMS training video, deliberately avoided from any cinematic
action-film framing.

---

## Target Player Profile

| Attribute | Detail |
| ---- | ---- |
| **Age range** | 19–55 (working EMT/paramedic professional range) |
| **Gaming experience** | Casual to none — do not assume gamer literacy; onboarding must teach VR controls, not just doctrine |
| **Time availability** | Department-scheduled training blocks, ~30–45 minutes including prebrief/debrief |
| **Platform preference** | Whatever their department or academy owns — a PC VR rig in a training lab, or a Quest headset for distributed/remote training |
| **Current games they play** | Typically none — the nearest analog is CE course software, moulage drills, or tabletop MCI exercises, not entertainment games |
| **What they're looking for** | Repeatable, safe, honest practice for a high-stakes scenario most will face rarely — or once — in a career |
| **What would turn them away** | Anything that reads as entertainment/spectacle rather than training; inaccurate doctrine; motion sickness; being asked to act outside real scope of practice |

---

## Technical Considerations

| Consideration | Assessment |
| ---- | ---- |
| **Recommended Engine** | Unreal Engine 5.8 (already pinned for this project) — MetaHuman pipeline for clinically expressive faces, OpenXR for cross-platform VR, current codebase is Blueprint-only |
| **Locomotion & Input Platform** | Per product-owner direction (2026-07-16): motion controllers only — hand tracking is explicitly rejected for the product (simplicity of development and use), not merely deferred; voice commands are unaffected. Four first-class locomotion modes are supported: controller-based free-form/smooth movement, teleportation, large room-scale physical walking, and the Virtuix Omni One Enterprise motion treadmill (flagship target) — a single abstract movement-intent interface with per-mode backends, so any site trains with whatever locomotion hardware it has. Reference headset is Meta Quest 3, driven by a site PC via wireless streaming (Virtual Desktop primary / Steam Link fallback) over a dedicated Wi-Fi 6E router per station — wired Link is ruled out because a cable wraps on a 360° treadmill. Joined by Samsung Galaxy XR as a second first-class streamed headset — Virtual Desktop primary (day-one Samsung-partnered support) / Samsung Game Link or Google PC Connect fallback (Steam Link availability on Android XR is unconfirmed), same dedicated-router pattern; Quest 3 remains primary reference; Galaxy XR's own motion controllers (in hand) are the input path, its native hand/eye tracking is not used; Omni treadmill stations stay Quest 3 until Virtuix confirms Galaxy XR pairing (per product-owner direction (2026-07-19)). See `vr-interaction-locomotion.md` for the full locomotion-mode design. Controllers only for POC/MVP; camera-based hand tracking remains rejected; per product-owner direction (2026-07-16), UDCAP VR Gloves (UDEXREAL) are a post-MVP, customer-gated controller-free input option for customers who insist on no controllers — the existing device-agnostic action binding avoids restructuring gameplay logic (no POC-time work), though glove-specific bindings (push-to-talk, button-free UI selection) are new design work deferred to activation time |
| **Key Technical Challenges** | Pulse Physiology Engine recompile for UE 5.8 (official builds target 4.26/5.0 only — HIGH risk, active POC risk); the physiology→facial-expression mapping remains a genuine market differentiator — no existing product demonstrates physiology-driven affect at this fidelity — built on an established, deterministic layered affect-modeling pattern (see `casualty-facial-animation.md`), so the remaining work is implementation, tuning, and SME clinical-plausibility validation, not an unsolved research problem. Deferred to the Alpha milestone (Quest feasibility-gated, NOT POC blockers): no supported Android/Quest path for live Pulse simulation (Win64-only libs); MetaHuman fidelity vs. Quest mobile performance budget; on-device offline voice-recognition latency on Quest |
| **Art Style** | 3D photorealistic — MetaHuman-grade casualties; clinical-documentary environment realism, not gratuitous |
| **Art Pipeline Complexity** | High — MetaHuman authoring plus a custom facial-pose blending layer per casualty archetype |
| **Audio Needs** | Moderate–High — ambient MCI soundscape (sirens, crowd, radio traffic), closed-loop voice-command recognition, casualty vocalizations (pain/distress), instructor/radio VO |
| **Networking** | None for POC (single-player). Client-server multiplayer instructor/team-training mode is roadmap only — architect for it, do not build it now |
| **Content Volume** | POC = one authored active-shooter MCI level, 5–15 casualty archetypes. Full Vision = a scenario library spanning multiple incident types |
| **Procedural Systems** | None at runtime for POC. `scenario-authoring-data.md` specifies a minimal data-driven casualty/injury authoring layer for the POC's single authored scenario (a flat data table for archetypes and tuning knobs); a general-purpose, reusable, scenario-library authoring pipeline is Full Vision scope |
| **Third-Party Acceleration (buy-over-build)** | Per product-owner direction (2026-07-16): prefer proven marketplace/Fab plugins over custom builds wherever they cover a needed capability, to fast-track development. Named candidates: **Pulse Unreal Plugin** (physiology backend, Kitware/Lumeto, Apache 2.0); **Georgy Dev suite** — Runtime Speech Recognizer + Runtime Audio Importer (on-device Whisper voice recognition + VAD mic capture), Runtime MetaHuman Lip Sync (casualty vocalization lipsync), optional Runtime Local LLM / AI Chatbot Integrator (Tier-2 free-form dialogue path), and Runtime Text To Speech (candidate for AI dispatch/radio voice lines if `incident-command-comms.md` is built). Each named candidate is ratified by a Phase-3 ADR after its own feasibility spike — this strategy accelerates implementation, it does not skip the ADR step |

---

## Risks and Open Questions

### Design Risks
- Balancing realism against approachability for non-gamer trainees unfamiliar with VR locomotion could produce a frustrating first-run experience if onboarding is under-designed.
- The dynamic re-escalation (shelter-in-place) event could feel arbitrary or punishing rather than instructive if its pacing isn't grounded in stress-inoculation-training principles (graduated exposure, not a jump-scare).

### Technical Risks
- Pulse Physiology Engine's UE 5.8 recompile is unproven — official support stops at UE 5.0; this is the single highest technical risk in the project, and it is an active POC risk (the POC is PC VR only, so this recompile must succeed on PC VR regardless of Quest).
- **Deferred to the Alpha milestone (Quest feasibility-gated — NOT a POC blocker)**: there is no supported Quest/Android path for live physiology simulation as of this research pass.
- **Deferred to the Alpha milestone (Quest feasibility-gated — NOT a POC blocker)**: MetaHuman-on-Quest performance and fidelity at the casualty counts this scenario needs is uncharted territory.
- **Single-maintainer vendor exposure**: the voice + lipsync stack named under Third-Party Acceleration above (Runtime Speech Recognizer, Runtime Audio Importer, Runtime MetaHuman Lip Sync) is supplied by one developer (Georgy Dev) — a single point of failure supplying core capabilities to two separate POC systems. Mitigation: pin plugin versions, validate the stack during the Week-1 spike, and document exit paths in the ratifying Phase-3 ADR.
- **NEW top interaction risk, per product-owner direction (2026-07-16)**: kneel-and-treat ergonomics on the Virtuix Omni One Enterprise treadmill — sustained, multi-minute two-handed floor-level casualty treatment is unverified on hardware (the dish is hard, concave, and deliberately low-friction; one-knee kneeling is reviewer-confirmed, but nothing documents minutes-long floor work). This is now the project's FIRST hardware spike, ahead of the Pulse recompile in trainee-facing risk terms. Mitigation channel: the user's company is a Virtuix hardware partner, so hardware-side accommodation (e.g., kneeling ergonomics) is a real resolution path — owner: product owner via Virtuix partnership. See `vr-interaction-locomotion.md` Open Questions.
- Wireless PC-to-Quest-3 streaming stability at the training site — target ~35–45ms motion-to-photon is acceptable for training but must be validated against treadmill locomotion comfort; mitigated by a dedicated Wi-Fi 6E router per treadmill station (PC on Ethernet).
- Physical exertion and trainee intake screening: Omni treadmill play is vigorous exercise (~77% HRmax, 7.3 METs) capped at ≤30 min sessions with hydration breaks; requires trainee intake screening against the manufacturer's user envelope (age 13+, height 4'4"–6'4", weight ≤250 lb, and medical contraindications) — some trainees will be excluded and routed to one of the other three locomotion modes, which is why the four-mode locomotion requirement (per product-owner direction (2026-07-16)) is a hard requirement, not a nice-to-have. See `duty-of-care-flow.md`.

### Market Risks
- SimX and Health Scholars are established, CE-relevant incumbents already distributed into EMS training programs.
- CE/CAPCE accreditation is a business-side dependency (partnering with an accredited sponsor organization) that the product alone cannot secure through design or engineering.

### Scope Risks
- Full timeline-replay AAR — the genre's expected bar per DHS EDGE — is deferred past the POC; evaluators expecting SimX/EDGE-level debrief may read the POC's score+summary screen as incomplete unless this deferral is clearly communicated.
- Clinical/SME validation cycles for triage-threshold and physiology-to-expression content new to this product are not yet scheduled and could gate any public-facing release of this content; thresholds carried over from the assigned SME's prior approved work do not require re-validation.

### Open Questions
- When is the acting-SME collaboration session scheduled to confirm triage thresholds and warm-zone scope-of-practice rules that are new to this product? (The project's assigned clinical SME's approval of clinical content of the same kind on two prior efforts — a completed internal proof of concept and a related platform already in active deployment with customers — carries over; the project lead serves as acting SME through the MVP.) → Should resolve before Phase 2 (Systems Design) closes.
- What is the actual sustainable casualty count on Quest 2/3 once MetaHuman rendering, physiology LOD, and on-device voice recognition are all running together? → **Deferred to the Alpha milestone**: resolve via a feasibility spike/prototype before committing to a Quest casualty-count target or beginning the Quest parity pass; not a POC-blocking question.

---

## MVP Definition

**Core hypothesis**: A single-player VR scenario where a trainee triages,
treats, and extracts casualties from a re-escalating warm-zone mass-casualty
incident — scored against real EMS benchmarks — produces a coherent,
repeatable training experience worth building further.

**Required for MVP (= the POC)**:
1. One authored active-shooter MCI level with 5–15 casualty archetypes, running live and/or pre-baked Pulse physiology
2. SALT-primary triage (global sort + individual assessment) with dynamic re-triage driven by live physiology
3. MARCH-ordered treatment interventions (tourniquet, wound packing, chest seal, needle decompression, NPA/OPA, recovery position) mapped to Pulse physiology actions
4. Hot/warm/cold zone system with a dynamic re-escalation event (shelter-in-place)
5. Voice command system (closed grammar) with a mandatory hand-menu fallback for every voice-driven action
6. Casualty facial animation driven by physiology (pain, consciousness, respiratory distress, pallor) — live in real time for casualties under active assessment or nearby the trainee; physiology-derived, pre-computed trajectories that branch at authored decision points for casualties elsewhere (see `casualty-model.md`'s LOD system)
7. Score + summary screen (triage accuracy, time-to-first-tourniquet, per-casualty outcomes, doctrine violations)
8. Duty-of-care flow: mandatory prebrief, always-available stop-scenario exit, post-scenario decompression
9. VR locomotion: four first-class modes — controller-based free-form/smooth movement, teleportation, room-scale physical walking, and the Virtuix Omni One Enterprise treadmill — with motion controllers as the only input method (hand tracking rejected) (per product-owner direction (2026-07-16))

**Explicitly NOT in MVP** (defer to later):
- Full timeline-replay after-action review (specified in the GDDs, scheduled for a later milestone)
- Multiplayer / live instructor station (architected for, not built)
- Multiple scenario types / a scenario library (one MCI level only)
- START-protocol as a selectable config option (SALT primary only for POC)
- CE/CAPCE accreditation infrastructure (record-keeping, identity verification)
- Trainee vocal-tone and stress monitoring with adaptive casualty/AI-teammate response (Pillar 5's long-term vision — per product-owner direction (2026-07-16))

### Scope Tiers (if budget/time shrinks)

| Tier | Content | Features | Timeline |
| ---- | ---- | ---- | ---- |
| **MVP / POC** | One active-shooter MCI level, single-player | Core loop only: SALT triage, MARCH treatment, zone re-escalation, score+summary | [To be scoped by producer] |
| **Vertical Slice** | POC scope polished to full visual/audio bar | Read-only instructor spectate station added; full timeline-replay AAR implemented; structured METHANE radio-report scoring (Incident Command & Comms) implemented | [To be scoped] |
| **Alpha** | 2–3 scenario types (different incident archetypes) | START config option added; pediatric casualty support; Quest standalone parity pass (feasibility-gated — see Technical Risks) | [To be scoped] |
| **Full Vision** | Multi-scenario training platform | Live multiplayer instructor + team training; CE/CAPCE-ready reporting and record-keeping; scenario-authoring tools for training departments; armed-role scenario support (e.g., law-enforcement training) with role-gated weapon handling governed by each role's own duty/use-of-force doctrine — weapon capability added only where a role's doctrine requires it (per product-owner direction, 2026-07-16); the physiology-driven casualty response stack packaged as a separate plug-in deliverable for external simulation platforms, first named target the OneARC VBS simulator platform (per product-owner direction, 2026-07-16 — see `addendum-physiology-response-plugin.md`); UDCAP VR Gloves (UDEXREAL) controller-free input option for customers who insist on no controllers (customer-gated; may pull earlier if a customer commitment lands) — per product-owner direction (2026-07-16); **trainee vocal-tone and stress monitoring with adaptive casualty/AI-teammate response** (Pillar 5's long-term vision — per product-owner direction, 2026-07-16) | [To be scoped] |

---

## Visual Identity Anchor

The single reference image that anchors this project's visual target: a
MetaHuman casualty's face, pale and glassy-eyed, breathing shallow and fast,
seen through the trainee's own gloved hands as they pack a wound — lit by
harsh, practical emergency lighting, dust hanging in the air, radio chatter
half-audible in the background. The visual grade is **clinical-documentary
realism** — closer to body-cam and EMS training-video color grading than to
cinematic action grading: desaturated, practical-light-motivated, no
stylized blood spray, no slow motion, no hero lighting. Casualties are
rendered and directed to read as real people having the worst day of their
life, never as damage models or set-dressing. Environment art prioritizes
wayfinding and zone legibility (clear exit paths, a visibly present RTF
escort, readable zone boundaries) over spectacle — every visual choice should
answer "does this help the trainee do their job," not "does this look
cinematic."

---

## Next Steps

- [x] Skeleton-stage approval received from the product owner (2026-07-16): "The GDDs look good." This is an informal green light on the concept + skeleton set as the working foundation — formal per-GDD `/design-review` still applies as each system's design is completed, and this document's Status stays Draft until then.
- [ ] Confirm this document's technical assumptions still match `.claude/docs/technical-preferences.md` (re-verified 2026-07-16 after the platform-direction pass: UE 5.8, PC VR Windows build with Quest 3 as streamed reference headset; Virtuix Omni One Enterprise flagship peripheral; four locomotion modes; motion controllers only, hand tracking rejected; Quest standalone deferred to Alpha, feasibility-gated; Chaos physics; re-verified again 2026-07-19 after the Galaxy XR addition: Samsung Galaxy XR added as a second first-class streamed dev + delivery headset, Quest 3 remains primary reference, Omni treadmill stays Quest 3-only pending Virtuix confirmation)
- [x] Working method for look-and-feel content, per product-owner direction (2026-07-16): the Game Feel and Visual/Audio Requirements content still marked [To be designed] in many of the system GDDs (some already carry partial content) is deliberately filled iteratively DURING MVP build, not before it. This is compatible with the project's review gates — those sections are not among the 8 required blocking sections (Overview, Player Fantasy, Detailed Rules/Design, Formulas, Edge Cases, Dependencies, Tuning Knobs, Acceptance Criteria), which are still designed and reviewed up front. One qualifier: the authoring pipeline (`/design-system`) marks the Visual/Audio Requirements table mandatory at authoring time for visual/character/UI/level-category systems — those systems get their baseline visual/audio requirement rows during design as the pipeline requires; it is the deeper feel-tuning content (frame budgets, haptics, impact moments, exact values) that defers to MVP build.
- [ ] Decide whether a companion `game-pillars.md` (full per-department pillar breakdown) is wanted, or whether this document's Game Pillars section is sufficient for the POC
- [ ] Decompose concept into systems — see the companion `systems-index.md`
- [ ] Design each system — see the 14 companion GDDs, starting with Foundation-layer systems
- [ ] Schedule a Week-1 technical spike: kneel-and-treat ergonomics on Virtuix Omni One Enterprise hardware (per product-owner direction (2026-07-16)) — the project's FIRST hardware task, ahead of the Pulse recompile spike; mitigation channel is the Virtuix hardware partnership
- [ ] Schedule a Week-1 technical spike: Pulse Physiology Engine recompile feasibility on UE 5.8 (PC VR)
- [ ] Schedule the acting-SME collaboration session to confirm any triage or treatment thresholds new to this product before they are locked — thresholds carried over from the SME-approved knowledge base already have sign-off
- [ ] Before the Quest parity pass begins (Alpha milestone): run the deferred Quest feasibility spike (MetaHuman/voice/physiology performance ceiling on-device)

---

## Build Agents

- **Authoring crew** handles every revision of this document.
- **Design-review agent crew** re-reviews this document whenever a design decision changes.
- **Style guide agent** enforces the visual identity anchor over demo assets.

Mapped in the compiled GDD's build-time agent plan (§12.1).
