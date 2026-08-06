# Casualty Facial Animation

> **Status**: Draft
> **Author**: game-designer
> **Last Updated**: 2026-07-15
> **Last Verified**: 2026-07-15
> **Implements Pillar**: Pillar 2 (The face is a vital sign)

## Summary

MetaHuman casualties carry a **Facial Expression Layer** in their Face
AnimBP that blends Facial Pose Library poses, weighted by the output drivers
this system computes from raw Pulse physiology (heart rate, pressures, SpO2,
respiration rate, level of consciousness, hemorrhage, injuries, arrest) —
never wired directly from a single raw vital. This system implements a **deterministic,
layered physiology→affect→expression pipeline** — an established
affect-modeling design pattern (physiology → derived features →
pain/appraisal → coping policy → expression output; see Detailed Design →
Core Rules) adopted here as this project's own design decision. Expression
is COMPUTED from physiology at every stage, not hand-scripted, so it is
reproducible and traceable back to a named variable at a specific time. It
still requires SME validation for clinical plausibility before it can be
trusted as a training tool, but the pipeline's shape is a known
implementation-and-tuning problem, not a research unknown — only its
specific tuned weights and thresholds remain open (see Tuning Knobs and
Open Questions). Per product-owner direction (2026-07-16), Runtime MetaHuman
Lip Sync (mood-enabled model) is the fast-track candidate for the
casualty-vocalization lipsync layer that composes with — and does not
replace — this pipeline's output stage (third-party acceleration strategy —
see `game-concept.md` Technical Considerations), to be ratified by a Phase-3
ADR after the lipsync spike (see Open Questions). Per product-owner direction
(2026-07-16), this
mapping layer's existing data-driven requirement gains an engine-agnostic
corollary (mapping data free of engine-specific types; the engine binding
isolated behind the mapping interface) and serves a second purpose: this
mapping layer is the portable core of a possible future plug-in deliverable of the
physiology→casualty-response stack for external simulation platforms (first
named target: OneARC VBS) — out of POC scope; see
`addendum-physiology-response-plugin.md`.

> **Quick reference** — Layer: `Feature` · Priority: `MVP` · Key deps: `Pulse Physiology Integration, Casualty Model`

## Overview

A casualty's face is not decoration in this game — it is one of the primary
instruments the trainee is trained to read during assessment and triage.
This system exists to make that instrument honest: every expression must
trace back to a real physiology variable, never to a scripted "looks
dramatic" choice.

**Pipeline principle**: physiology is the single source of truth. Raw
vitals are NEVER wired directly to face poses — every physiology input
passes through feature extraction, then pain/appraisal, then a
coping-policy stage before it ever reaches an expression output (see
Detailed Design → Core Rules). This exists for three reasons: (a) it
prevents twitchy, noise-driven animation — a single noisy vitals sample
never has a direct line to the face; (b) it gives the system
explainability — "why did this casualty present that way?" is always
answerable by tracing the expression back to a named physiology or
appraisal variable at a specific time, which is directly valuable for the
scoring/debrief after-action review; (c) it produces realistic cognitive
latency — the face doesn't twitch the instant a vital changes, because a
real casualty's expression follows their brain's appraisal of their state,
not their raw vitals in real time.

Key facts driving this design:
- The Face AnimBP blends **Facial Pose Library** poses (premade Control Rig poses shipped with every MetaHuman project, supporting partial-face poses and weighted multi-pose blending) — the right substrate for pain/consciousness blends.
- The Pulse-output → pose-weight mapping is computed by this project's own deterministic physiology→affect→expression pipeline (see Detailed Design → Core Rules), rather than authored per-casualty by hand; the pipeline's specific tuned weights and thresholds still require their own SME review cycle before the output can be trusted as clinically plausible (see Tuning Knobs and Open Questions).
- **Platform**: PC VR is the POC target — it runs LOD0/1 for close-up assessment fidelity with grooms allowed, with fidelity concentrated on whichever casualty is currently being assessed. **Deferred to the Alpha milestone (Quest feasibility-gated, NOT a POC requirement)**: a Quest platform split requiring a Min-LOD clamp, mandatory hair cards (strand-based grooms don't render on Android), the 75-bone mobile skinning limit, and texture LOD clamps.
- Lipsync uses Runtime MetaHuman Lip Sync (mood-enabled model) for casualty vocalizations on PC VR (POC target). **Deferred to the Alpha milestone**: whether the cheaper standard model is needed and validated on-device for Quest.
- MetaHuman Collections (UE 5.8, Experimental) is a stretch/upgrade path for scaling casualty/bystander counts later; the POC baseline is a hand-managed pool of ~5–15 full-fidelity casualties.

## Player Fantasy

Reading a face tells you what a monitor can't yet — this system exists so
that instinct is genuinely trainable and honest, not a director's trick.

## Detailed Design

### Core Rules

- Facial Expression Layer blends Facial Pose Library poses (and any custom-authored pain/agonal/unconscious poses), weighted by the **Stage 7 output drivers** computed by this system's physiology→affect→expression pipeline (see the pipeline stages below) — pose weights plus vocalization cue, breathing intensity, gaze probability, and body-motion gain. Raw vitals never drive a pose directly (see the Overview pipeline principle).
- Expression fidelity is dynamically concentrated on the casualty currently being assessed; other casualties in view run at a lower facial LOD.
- The pipeline below is specified at the design/interface level; which UE construct implements each stage (Blueprint function library, Animation Blueprint state, custom component, etc.) is deferred to → ADR (Phase 3).
- **Stage 1 — Physiological inputs** (read from `pulse-physiology-integration.md`, live or baked): heart rate (HR), arterial/mean arterial pressure (MAP), SpO2, respiration rate, level of consciousness, hemorrhage rate, active injuries, and the arrest flag. Read-only tap into ground truth — this stage owns no logic of its own.
- **Stage 2 — Derived features**, computed from Stage 1: trend slopes for HR and MAP (rate of change, not instantaneous value), a perfusion index, a homeostasis-state enum (Stable → Compensating → Decompensating → Arrest — see States and Transitions), and a shock probability.
- **Stage 3 — Pain model**: an acute component (event-driven from injuries/interventions, fast decay) combined perceptually with a lingering component (driven by injury severity, slow decay) — see Formulas for the combine function.
- **Stage 4 — Appraisal**: deterministic threat, distress, fear, and control-loss scalars, PLUS a primary-emotion vector — a set of discrete primary emotions, each a 0..1 intensity, grounded generically in discrete-emotion theory (e.g. Plutchik's primary emotions) as this project's public academic basis. Computed entirely from Stages 1–3 — see Formulas. The four named scalars (threat, distress, fear, control-loss) are the projections the coping policy reads most directly; each is a member of, or a projection from, the same primary-emotion space — `fear` in particular is a single shared value, not two independent computations.
- **Stage 5 — Subjective/belief state**: the casualty's perceived state may lag or diverge from physiological ground truth, which is what makes denial, bravado, and dissociation legible behaviors rather than the casualty always "knowing" their true severity.
- **Stage 6 — Coping policy**: selects a coping mode (e.g. seek-help / endure / dissociate / resignation) from the appraisal + belief-state inputs, with hysteresis so the mode does not flicker between adjacent stage ticks near a decision boundary. (Here "resignation" denotes acute resignation / calm compliance within the minutes-long scenario window — not the long-arc grief-stage sense of "acceptance"; the exact mode set is SME-reviewed, see Open Questions.)
- **Stage 7 — Output drivers**: coping mode + appraisal drive the existing MetaHuman Face AnimBP pose weights, plus a vocalization cue, breathing intensity, eye-contact/gaze probability, and body-motion gain — feeding the lipsync layer (Runtime MetaHuman Lip Sync) and world-space cues.
- **Hard-override rule**: two Stage 1 ground-truth conditions bypass the Stage 4–6 appraisal/coping path entirely and drive Stage 7 directly — (a) the arrest flag forces the Arrest output state (vocalization stops, fixed pose), and (b) level of consciousness below the unconsciousness threshold forces the Unconscious output state (gaze and vocalization suppressed). Ground truth outranks appraisal; a casualty can never "cope" its way out of arrest or unconsciousness.
- **Persona-as-weights rule**: casualty temperament (e.g. stoic, anxious, bravado, fatalism) is expressed entirely as WEIGHT SETS that bias Stage 5 (belief) and Stage 6 (coping) — the equations and the seven-stage structure never change per casualty. This is how casualty-to-casualty personality variety is achieved without new per-casualty logic.
- **Determinism rule**: the same physiology input sequence yields the same expression output sequence, every time; every expression output must trace to a named variable, at a specific stage, at a specific time — required for reproducible training content and for the scoring/debrief after-action trace.
- **Decoupled update rates rule**: Stage 1 samples at Pulse's own tick rate (see `pulse-physiology-integration.md` Tuning Knobs); Stages 2–6 (the affect/appraisal layer) run at a lower, fixed cognitive cadence (~10 Hz — see Tuning Knobs); Stage 7 (output) drives at frame rate. This decoupling is deliberate, not merely a performance optimization — it produces realistic cognitive latency, since a real casualty's face follows their brain's appraisal of their state, not their raw vitals in real time.
- **Deterministic-before-learned rule** *(note only, deferred)*: Stage 6 is designed as a replaceable surface so a future learned/ML coping policy could substitute for the deterministic one, but only after shadow-mode validation against this deterministic baseline — a → ADR / later-milestone decision, not POC scope.

### States and Transitions

**Homeostasis states** (computed by this pipeline's Stage 2 from Stage 1
physiology. The raw ground truth — vitals and the arrest flag — is owned by
Pulse Physiology Integration / Casualty Model; the homeostasis-state enum and
shock probability are DERIVED here, not raw Pulse outputs. If another system
(e.g. Triage System) needs a shared homeostasis/shock signal, a single owned
definition should be established at the Phase-3 architecture pass to avoid
divergent computations — see Open Questions):

| State | Entry Condition | Exit / Next State |
|-------|-----------------|-------------------|
| Stable | Default state while shock probability and MAP/HR trend slopes stay within normal bounds | → Compensating when shock probability crosses [To be designed] |
| Compensating | Shock probability crosses its threshold while MAP remains within a defended range (the body is compensating) | → Decompensating when MAP trend slope falls below [To be designed] despite compensation; → Stable if the underlying insult is treated and trends normalize |
| Decompensating | MAP falls outside the defended range; perfusion index drops below [To be designed] | → Arrest when the arrest flag becomes true; → Compensating/Stable if treatment reverses the trend before arrest |
| Arrest | Stage 1 arrest flag = true (ground truth, owned by Pulse Physiology Integration / Casualty Model) | Terminal for this system — this system never causes or reverses arrest; it only reads the flag and updates output drivers accordingly |

**Readable expression/output states** (Stage 7 output, driven by coping
mode + appraisal):

| Expression State | Entry Condition (traces to pipeline) | Notes |
|-------------------|----------------------------------------|-------|
| Neutral | Homeostasis Stable; all Stage 4 appraisal scalars below their [To be designed] "notable" thresholds | Default / baseline resting expression |
| Distress | Homeostasis Compensating or worse; Stage 4 distress scalar crosses [To be designed]; coping mode = seek-help or endure | Primary "something is wrong" readable state |
| Fear | Stage 4 fear scalar crosses [To be designed] (see Formulas, fear-style example) | Can co-occur with Distress; persona weights (Stages 5–6) bias how visibly it presents |
| Dissociated | Coping mode = dissociate (Stage 6), selected when belief-state divergence from ground truth (Stage 5) is high and persona weights favor dissociation over seeking help | Casualty may present calmer than ground-truth severity would suggest — an intentional assessment challenge, not a bug |
| Weak | Homeostasis Decompensating; ConsciousnessLevel below an "altered" threshold [To be designed] but above the Unconscious threshold | Reduced body-motion gain and vocalization intensity (Stage 7 output drivers) |
| Unconscious | ConsciousnessLevel (Stage 1) crosses below its unconsciousness threshold [To be designed] | Face AnimBP holds a fixed unconscious pose; vocalization cue suppressed; eye-contact/gaze probability forced to 0 |
| Arrest | Stage 1 arrest flag = true | Face AnimBP holds a fixed arrest pose; vocalization stops entirely; overrides all other coping-policy hysteresis (arrest is ground truth, not an appraisal outcome) |

[To be designed] — exact numeric thresholds for every transition above
(shock probability, MAP slope, perfusion index, appraisal-scalar "notable"
cutoffs, consciousness thresholds) require SME input; see Tuning Knobs and
Open Questions.

### Interactions with Other Systems

- **Pulse Physiology Integration / Casualty Model**: provide the raw physiology (Stage 1) and own the live/baked LOD state. This pipeline reads, never writes, physiology; it runs on whatever fidelity a casualty is at — a baked casualty gets affect from its baked physiology trajectory, and promotion to a live engine sharpens it.
- **Treatment & Interventions**: intervention events (e.g. a tourniquet application) are inputs to Stage 3 acute pain; a successful intervention that changes physiology also flows back through the whole pipeline via Pulse.
- **Patient Assessment**: consumes this system's Stage 7 output (the visible face and behavior) as a required assessment input — the trainee reads the face, and the face is this pipeline's product.
- **Triage System**: the trainee's in-fiction PERCEPTION of mental status and respiratory distress is face-mediated (this system's output), but Triage's SCORED ground-truth category reads Pulse physiology directly, by design. This separation is intentional: a casualty's coping/dissociation (Stage 5 divergence) can change what the trainee perceives without changing the scored truth — which is what makes "the dissociated casualty who looks calmer than they are" a real assessment challenge rather than a scoring exploit.
- **Scoring & Debrief**: every expression output traces to a named variable at a specific time (Determinism rule); the POC logs this trace, and the later-milestone after-action review surfaces it ("why did this casualty present as stable when they were decompensating?").

## Formulas

### Perceptual pain combine (Stage 3)

```
pain_total = 1 - (1 - pain_acute) * (1 - pain_lingering)
```

| Variable | Type | Range | Source | Description |
|----------|------|-------|--------|-------------|
| `pain_acute` | float | 0..1 | Stage 3, event-driven from injuries/interventions; fast decay | Momentary pain spike from a fresh injury or an intervention (e.g. tourniquet application); decays quickly once the triggering event passes |
| `pain_lingering` | float | 0..1 | Stage 3, driven by injury severity; slow decay | Baseline pain from the casualty's standing injury severity; decays slowly, reflecting a wound that keeps hurting |
| `pain_total` | float | 0..1 | Output of this formula | Combined perceived pain, fed into Stage 4 appraisal only — it reaches expression through the appraisal → coping-policy path, never wired directly to Stage 7 output |

**Output range**: 0..1.

**Worked example**: `pain_acute = 0.6` (fresh tourniquet-application spike), `pain_lingering = 0.3` (moderate standing leg injury) →
`pain_total = 1 - (1 - 0.6) * (1 - 0.3) = 1 - (0.4 * 0.7) = 1 - 0.28 = 0.72`.

**Why probabilistic-OR, not addition**: this combine form always stays in
0..1 regardless of input magnitude (a plain sum could exceed 1 and would
need a separate clamp), and it matches the intuition that "two pains feel
slightly worse than one" without simple additive stacking — pain compounds,
it doesn't stack linearly. Specific decay-rate values are
[To be designed] — SME-tuned; see Tuning Knobs.

### Primary-emotion computation (Stage 4)

General form, one instance per discrete primary emotion `x`:

```
emotion_x = clamp01( sum_i( w_i * feature_i ) )
```

where `feature_i` are normalized physiology/derived-feature inputs from
Stages 1–2, and `w_i` are per-emotion, per-input weights.

**Worked example form — fear**:

```
fear = clamp01( w1 * shock_probability + w2 * max(0, hr_slope_norm) + w3 * (1 - spo2) )
```

| Variable | Type | Range | Source | Description |
|----------|------|-------|--------|-------------|
| `shock_probability` | float | 0..1 | Stage 2 derived feature | Likelihood the casualty is in or entering shock |
| `hr_slope_norm` | float | -1..1 (only the positive/rising direction contributes here, via `max(0, ·)`) | Stage 2 derived feature, normalized HR trend slope | Rate of change of heart rate, normalized |
| `spo2` | float | 0..1 (normalized from 0–100%) | Stage 1 physiological input | Blood oxygen saturation; falling SpO2 raises fear via the `(1 - spo2)` term |
| `w1`, `w2`, `w3` | float | 0..1, [To be designed] — SME-tuned | Tuning Knobs | Per-input weights controlling how strongly each feature drives fear |
| `fear` | float | 0..1 | Output of this formula | One entry in the primary-emotion vector, consumed by Stage 6 coping-policy selection |

**Output range**: 0..1 per emotion; the full primary-emotion vector is one
0..1 value per discrete primary emotion.

**Worked example**: `shock_probability = 0.5`, `hr_slope_norm = 0.4`
(HR rising), `spo2 = 0.9` (90%), with illustrative placeholder weights
`w1 = 0.5`, `w2 = 0.3`, `w3 = 0.4` (not tuned values) →
`fear = clamp01(0.5*0.5 + 0.3*0.4 + 0.4*0.1) = clamp01(0.25 + 0.12 + 0.04) = clamp01(0.41) = 0.41`.

The resulting primary-emotion vector is written for Stage 6 (coping policy)
to consume, and is fully reproducible from physiology — it satisfies the
Determinism rule in Core Rules. The discrete-emotion basis (e.g. Plutchik's
primary emotions) is a public academic framework used here as general
grounding for this project's own emotion-vector design; specific per-emotion
weights are [To be designed] — SME-tuned; see Tuning Knobs and Open
Questions.

## Edge Cases

| Scenario | Expected Behavior | Rationale |
|----------|------------------|-----------|
| [To be designed] | | |

## Dependencies

| System | Direction | Nature of Dependency |
|--------|-----------|---------------------|
| Pulse Physiology Integration | This depends on Pulse Physiology Integration | Reads raw physiology (HR, pressures, SpO2, respiration rate, level of consciousness, hemorrhage, injuries, arrest) as Stage 1 inputs; pain and all affect are derived downstream by this pipeline, NOT read from Pulse |
| Casualty Model | This depends on Casualty Model | The Facial Expression Layer is attached to this system's casualty actor |
| Treatment & Interventions | This depends on Treatment & Interventions | Intervention events feed Stage 3 acute-pain spikes (see Interactions) |
| Patient Assessment | Patient Assessment depends on this | Facial state (Stage 7 output) is a required assessment input |
| Triage System | Triage System depends on this | The trainee's face-mediated PERCEPTION of mental-status / respiratory-distress comes from this system's output; Triage's SCORED ground truth reads Pulse directly (see Interactions) |
| Scoring & Debrief | Scoring & Debrief depends on this | The expression-decision trace (Determinism rule) feeds the later-milestone after-action review; the POC logs the trace |

## Tuning Knobs

| Parameter | Current Value | Safe Range | Effect of Increase | Effect of Decrease |
|-----------|--------------|------------|-------------------|-------------------|
| Pain → pose-weight curve | [To be designed] — SME review required | [To be designed] | | |
| Consciousness → eye/brow/jaw slack mapping | [To be designed] — SME review required | [To be designed] | | |
| Facial LOD distance thresholds (PC VR — POC target) | [To be designed] | [To be designed] | | |
| Max simultaneous full-fidelity faces (PC VR — POC target) | [To be designed] | [To be designed] | | |
| Lipsync model tier (PC VR — POC target) | [To be designed] | [To be designed] | | |
| Facial LOD distance thresholds, max simultaneous full-fidelity faces, lipsync model tier (Quest) | Deferred to the Alpha milestone, feasibility-gated — not POC scope | — | | |
| Persona weight sets (per temperament: stoic, anxious, bravado, fatalism — Stage 5/6 bias) | [To be designed] — SME-tuned | [To be designed] | Higher bias toward that temperament's signature response (e.g. higher bravado weight suppresses visible distress) | Lower bias produces a more generic, less personality-distinct appraisal-driven response |
| Per-emotion input weights (`w1`, `w2`, `w3`... per primary emotion — see Formulas) | [To be designed] — SME-tuned | 0..1 per weight | Emotion more strongly driven by that input | Emotion less sensitive to that input |
| Pain acute-decay rate (Stage 3) | [To be designed] | [To be designed] — fast enough to read as a spike, slow enough not to flicker frame-to-frame | Sharper, shorter-lived pain spikes on injury/intervention events | Pain lingers longer after the triggering event; risks a duller "always in pain" read |
| Cognitive-stage tick rate (Stages 2–6) | ~10 Hz (candidate) | [To be designed] | Higher-fidelity, more responsive appraisal at higher CPU cost | Coarser appraisal updates; more pronounced cognitive latency |
| Coping-policy hysteresis threshold (Stage 6) | [To be designed] | [To be designed] | Fewer, more stable coping-mode switches; risks feeling "stuck" in a mode too long | More frequent coping-mode switches; risks visible flicker between modes |
| Expression-update latency target (Stage 7) | 500ms (candidate — matches the Visual/Audio Requirements target below) | [To be designed] | Faster perceived responsiveness; risks feeling twitchy if pushed too low | Slower perceived responsiveness; risks reading as unresponsive if pushed too high |

## Visual/Audio Requirements

| Event | Visual Feedback | Audio Feedback | Priority |
|-------|----------------|---------------|----------|
| Pulse physiology crosses a threshold (e.g., pain spike, consciousness drop) | Facial expression updates within 500ms (candidate target) | Casualty vocalization intensity updates in step | High — this is the primary clinical readout channel |

## Game Feel

### Feel Reference

Should feel like observing a real distressed person's face — subtle,
continuous, and readable, not like a cartoon emotion-icon system. NOT
melodramatic or theatrical.

### Input Responsiveness

[To be designed] — this is a simulation-driven presentation system, not a direct-input system

### Animation Feel Targets

[To be designed]

### Impact Moments

[To be designed]

### Weight and Responsiveness Profile

[To be designed]

### Feel Acceptance Criteria

- [ ] Clinical reviewers can identify consciousness level from the face alone at assessment distance (candidate target — needs SME validation)
- [ ] [To be designed]

## UI Requirements

[To be designed] — facial expression is diegetic, not a UI element

## Cross-References

| This Document References | Target GDD | Specific Element Referenced | Nature |
|--------------------------|-----------|----------------------------|--------|
| "Stage 1 reads raw physiology from Pulse" | `design/gdd/pulse-physiology-integration.md` | Raw physiology outputs (HR, pressures, SpO2, respiration rate, level of consciousness, hemorrhage, injuries, arrest) — pain/affect derived downstream here | Data dependency |
| "Attached to the casualty actor" | `design/gdd/casualty-model.md` | Casualty actor composition | Rule dependency |
| "Facial state is a required assessment input" | `design/gdd/patient-assessment.md` | Assessment findings input | Data dependency |
| "The data-driven mapping layer is the portable presentation core of a future external-platform deliverable; the engine binding stays isolated behind the mapping interface" | `design/gdd/addendum-physiology-response-plugin.md` | Physiology→pose-weight mapping portability constraint (Full Vision addendum, out of POC scope) | Rule dependency |

## Acceptance Criteria

- [ ] GIVEN a casualty's physiology crosses a threshold that the pipeline maps to a changed pain/appraisal output, WHEN the next facial-animation tick runs, THEN the expression visibly updates within 500ms (candidate target — pending validation by the acting SME)
- [ ] **Determinism**: GIVEN the same physiology input sequence is replayed through the pipeline, WHEN the pipeline runs to completion, THEN the resulting expression output sequence is identical every time
- [ ] **Traceability**: GIVEN any expression output at runtime, WHEN a designer or reviewer inspects it via debug/logging, THEN it maps to a named physiology or appraisal variable at a specific pipeline stage and a specific time
- [ ] **Latency**: GIVEN a physiology value crosses a defined threshold, WHEN the next cognitive-stage tick runs, THEN the expression visibly updates within the expression-update latency target (candidate: 500ms — pending validation by the acting SME)
- [ ] **Clinical plausibility**: GIVEN a clinical SME reviews recorded expression/behavior sequences against physiology ground truth, WHEN the review is complete, THEN the SME signs off that the expression/behavior matches what a real casualty in that state would present
- [ ] Performance: 90fps sustained on PC VR (POC target) with N casualties in view — N to be set pending the rendering spike. A 72fps-on-Quest-2 target is deferred to the Alpha milestone, feasibility-gated.
- [ ] No hardcoded values in implementation — the physiology→pose-weight mapping (pipeline weights and thresholds) is data-driven, not hardcoded logic

## Open Questions

| Question | Owner | Deadline | Resolution |
|----------|-------|----------|-----------|
| The pipeline's exact tuned weights and thresholds (pain-model decay rates, per-emotion input weights, appraisal-scalar and homeostasis-transition thresholds, coping-policy hysteresis) — the pipeline's FORM is now specified (see Detailed Design and Formulas); only the specific values are open | acting SME (project lead) + game-designer | Before Phase 2 (Systems Design) closes | [To be designed] |
| Persona weight sets per temperament (stoic, anxious, bravado, fatalism) — the specific weight values that bias Stage 5/6 belief and coping per persona | acting SME (project lead) + game-designer | Before Phase 2 (Systems Design) closes | [To be designed] |
| SME validation of the affect→expression mapping for overall clinical plausibility — once tuned, does the pipeline's output actually read as a real casualty in that state? | acting SME (project lead) | Before Phase 2 (Systems Design) closes | [To be designed] |
| Should the homeostasis-state enum and shock probability (derived here in Stage 2) be a single shared owned signal if Triage System needs them too, to avoid divergent computations of the same clinical signal? | technical-director + game-designer | Phase 3 (Technical Setup) architecture pass | → ADR (Phase 3) — not a GDD-time decision |
| Whether a future learned/ML coping policy could replace the deterministic Stage 6 policy, and what shadow-mode validation against the deterministic baseline would require | unreal-specialist + game-designer | Deferred — later milestone, not POC scope | → ADR (Phase 3) / later milestone — not POC scope |
| Whether Runtime MetaHuman Lip Sync's standard (cheaper) model runs within budget on Quest | unreal-specialist | Alpha-milestone feasibility spike — deferred, not POC-blocking | [To be designed] |
| Which lipsync plugin implements casualty vocalization on PC VR (Runtime MetaHuman Lip Sync mood-enabled model is the fast-track candidate, locked by product-owner direction 2026-07-16) | unreal-specialist | Lipsync feasibility spike (PC VR, POC) | → ADR (Phase 3) — ratifies the candidate and records the exit path (e.g., pose-library-only expression, no audio-driven lipsync) if the spike fails |
| MetaHuman material/renderer compatibility with this project's Quest mobile rendering path (Substrate/Forward+MSAA stack, baked-only GI) | unreal-specialist | Alpha-milestone feasibility spike — deferred, not POC-blocking | [To be designed] |

## Build Agents

The Goal-oriented coding agent builds the four-state affect slice (W3-W4), with the Engineering pair wiring it to live physiology output; the lead judges readability at the W4 checkpoint. Mapped in the compiled GDD's build-time agent plan (§12.1).
