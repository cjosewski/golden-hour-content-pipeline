# Retrieval Trace

For each content type and request: the exact retrieval query, the top retrieved GDD chunk(s) with source doc + section, and the final generated output — side by side. This is the RAG audit trail.

## Pain / plea barks (`pain_barks`)

### external hemorrhage / severe / conscious / fearful

**Query:** `casualty vocalization pain external hemorrhage severe conscious normal fearful external hemorrhage severe conscious normal fearful`

**Top retrieved chunks:**

1. `casualty-facial-animation.md` > *Summary* (bm25=9.97)
   > MetaHuman casualties carry a **Facial Expression Layer** in their Face AnimBP that blends Facial Pose Library poses, weighted by the output drivers this system computes from raw Pulse physiology (heart rate, pressures, SpO2, respiration rate, level of consciousness, hemorrhage, injuries, arrest) — never wired directly from a single raw vital. This system implements a **deterministic, layered physiology→affect→expression pipeline** — an established affect-modeling design pattern (physiology → derived features → pain/appraisal → coping policy → expression output; see Detailed Design → Core Rules) adopted here as this project's own design decision. Expression is COMPUTED from physiology at every stage, not hand-scripted, so it is reproducible and traceable back to a named variable at a specific time. It still requires SME validation for clinical plausibility before it can be trusted as a tr ...
2. `pulse-physiology-integration.md` > *Dependencies* (bm25=8.21)
   > | System | Direction | Nature of Dependency | |--------|-----------|---------------------| | Casualty Model | Casualty Model depends on this | Every casualty actor owns a physiology component sourced from this system | | Treatment & Interventions | Treatment & Interventions depends on this | Every intervention verb maps 1:1 to a Pulse action call | | Casualty Facial Animation | Casualty Facial Animation depends on this | Provides raw physiology (HR, pressures, SpO2, respiration rate, level of consciousness, hemorrhage, injuries, arrest); that system derives pain, features, and expression from these — pain and affect are NOT outputs of this system | | Scenario Authoring & Data | Scenario Authoring & Data depends on this | Casualty archetypes are authored as Pulse patient files/conditions and pre-baked state trajectories |
3. `casualty-facial-animation.md` > *Visual/Audio Requirements* (bm25=7.85)
   > | Event | Visual Feedback | Audio Feedback | Priority | |-------|----------------|---------------|----------| | Pulse physiology crosses a threshold (e.g., pain spike, consciousness drop) | Facial expression updates within 500ms (candidate target) | Casualty vocalization intensity updates in step | High — this is the primary clinical readout channel |
4. `treatment-interventions.md` > *Acceptance Criteria* (bm25=7.58)
   > - [ ] GIVEN a casualty has an active uncontrolled hemorrhage, WHEN the trainee successfully applies a tourniquet, THEN the casualty's physiology reflects hemorrhage cessation and `hemorrhage_controlled` becomes true for the SALT decision tree - [ ] GIVEN a tension pneumothorax casualty, WHEN the trainee successfully performs needle decompression, THEN respiratory distress physiology improves within a defined time window — [To be designed] - [ ] GIVEN the trainee is in the warm zone, WHEN they attempt an intervention outside warm-zone scope, THEN the action is logged as a scored doctrine violation - [ ] Performance: System update completes within [X]ms — [To be designed] - [ ] No hardcoded values in implementation — pass windows and success conditions are data-driven per the Tuning Knobs table

**Generated output (post-critic):**

```json
{
  "injury_type": "external hemorrhage",
  "severity": "severe",
  "consciousness": "conscious",
  "respiratory_status": "normal",
  "affect": "fearful",
  "is_intelligible_speech": true,
  "vocalization": "Oh God—there's so much blood—please, I need help!",
  "trigger": "Hemorrhage rate crosses severe threshold while casualty remains conscious with normal respiratory function; fear appraisal active",
  "physiology_trace": "hemorrhage rate"
}
```

### tension pneumothorax / critical / conscious / respiratory distress

**Query:** `casualty vocalization pain tension pneumothorax critical conscious distress panicked needle decompression SpO2 gasping tension pneumothorax critical conscious distress panicked needle decompression SpO2 gasping`

**Top retrieved chunks:**

1. `treatment-interventions.md` > *Acceptance Criteria* (bm25=28.58)
   > - [ ] GIVEN a casualty has an active uncontrolled hemorrhage, WHEN the trainee successfully applies a tourniquet, THEN the casualty's physiology reflects hemorrhage cessation and `hemorrhage_controlled` becomes true for the SALT decision tree - [ ] GIVEN a tension pneumothorax casualty, WHEN the trainee successfully performs needle decompression, THEN respiratory distress physiology improves within a defined time window — [To be designed] - [ ] GIVEN the trainee is in the warm zone, WHEN they attempt an intervention outside warm-zone scope, THEN the action is logged as a scored doctrine violation - [ ] Performance: System update completes within [X]ms — [To be designed] - [ ] No hardcoded values in implementation — pass windows and success conditions are data-driven per the Tuning Knobs table
2. `treatment-interventions.md` > *Overview* (bm25=23.20)
   > This is where the trainee's hands do the actual life-saving work — but only the work that real warm-zone doctrine permits. Every intervention here is scoped to life threats, ordered by MARCH, and produces a real physiological response because it drives an actual Pulse action, not a scripted animation. Key facts driving this design: - **Verb set (warm-zone, life-threats-only scope)**: tourniquet application; wound packing (hemostatic or plain gauze) plus pressure dressing; chest seal (vented preferred) for open/sucking chest wounds; needle decompression (2nd intercostal space) for tension pneumothorax; NPA/OPA airway adjuncts; supplemental oxygen; recovery position; drag/carry extraction to the Casualty Collection Point. - Full head-to-toe workups, spinal immobilization rituals, and IV fluid resuscitation wait for the cold zone / evacuation phase — performing them in the warm zone is a sc ...
3. `pulse-physiology-integration.md` > *Overview* (bm25=21.95)
   > Every clinical claim this game makes — that a tourniquet actually stops a bleed, that an untreated tension pneumothorax actually kills, that a casualty's face actually reflects their real state — depends on this system being trustworthy. It exists to give every other system a source of ground truth that behaves like real physiology instead of scripted numbers. Key facts driving this design: - Apache 2.0 licensed; the Unreal plugin was co-developed by Kitware and Lumeto and funded by an Epic MegaGrant, exposing the engine via a **Blueprint Actor Component** — a strong fit for this project's Blueprint-only codebase. - Models the exact insults and interventions this scenario needs: hemorrhage, tension pneumothorax, airway obstruction, plus tourniquet, wound packing, needle decompression, chest seal, NPA/OPA, and supplemental oxygen. - Engine state serializes to JSON/binary and reloads insta ...
4. `treatment-interventions.md` > *Core Rules* (bm25=21.49)
   > - Verb set (see Summary/Overview above) is exhaustive for the POC's warm-zone scope; no additional interventions are modeled. - Each intervention verb has a defined MARCH-order relevance: tourniquet application and wound packing (hemostatic or plain gauze) + pressure dressing are **M — Massive hemorrhage** tier; chest seal and needle decompression are **R — Respiration** tier (they treat the two respiratory life threats — open/sucking chest wound and tension pneumothorax — not hemorrhage); NPA/OPA airway adjuncts are **A — Airway** tier; recovery position is **A — Airway** tier for unconscious casualties. These four MARCH tiers are kept distinct — M and R are never blurred under one combined label. - [To be designed] — exact interaction mechanic per verb, success/failure conditions, and how partial/incorrect application (e.g., a tourniquet applied too loosely) is represented, if at all,  ...

**Generated output (post-critic):**

```json
{
  "injury_type": "tension pneumothorax",
  "severity": "critical",
  "consciousness": "conscious",
  "respiratory_status": "distress",
  "affect": "panicked",
  "is_intelligible_speech": true,
  "vocalization": "I can't—I can't breathe!",
  "trigger": "Repeating bark during critical tension pneumothorax with respiratory distress, before needle decompression intervention",
  "physiology_trace": "Respiration rate, SpO2, intrathoracic pressure (tension pneumothorax pathology modeled by Pulse)"
}
```

### airway obstruction / severe / conscious / obstructed

**Query:** `casualty vocalization pain airway obstruction severe conscious obstructed distressed stridor gurgle airway airway obstruction severe conscious obstructed distressed stridor gurgle airway`

**Top retrieved chunks:**

1. `treatment-interventions.md` > *Core Rules* (bm25=17.82)
   > - Verb set (see Summary/Overview above) is exhaustive for the POC's warm-zone scope; no additional interventions are modeled. - Each intervention verb has a defined MARCH-order relevance: tourniquet application and wound packing (hemostatic or plain gauze) + pressure dressing are **M — Massive hemorrhage** tier; chest seal and needle decompression are **R — Respiration** tier (they treat the two respiratory life threats — open/sucking chest wound and tension pneumothorax — not hemorrhage); NPA/OPA airway adjuncts are **A — Airway** tier; recovery position is **A — Airway** tier for unconscious casualties. These four MARCH tiers are kept distinct — M and R are never blurred under one combined label. - [To be designed] — exact interaction mechanic per verb, success/failure conditions, and how partial/incorrect application (e.g., a tourniquet applied too loosely) is represented, if at all,  ...
2. `patient-assessment.md` > *Overview* (bm25=15.99)
   > Assessment is the diagnostic half of the core loop — before the trainee can sort or treat anyone, they have to find out what's actually wrong. This system defines the vocabulary of clinical questions the trainee can ask a casualty, by hand or by voice, and what they learn from each one. Key facts driving this design: - Assessment sequence follows **MARCH** (Massive hemorrhage → Airway → Respiration → Circulation → Head injury/Hypothermia) — the TECC/TCCC standard that supersedes ABC for penetrating trauma because exsanguination kills faster than airway compromise. - Examine verb set: check breathing, check radial pulse / capillary refill, check mental status ("squeeze my hand" / follows commands), check for major hemorrhage, expose the chest for respiratory-distress signs. - Casualty facial expression (pain, consciousness, respiratory distress, pallor) is itself a required, readable-at-d ...
3. `casualty-facial-animation.md` > *Feel Reference* (bm25=14.42)
   > Should feel like observing a real distressed person's face — subtle, continuous, and readable, not like a cartoon emotion-icon system. NOT melodramatic or theatrical.
4. `pulse-physiology-integration.md` > *Overview* (bm25=14.37)
   > Every clinical claim this game makes — that a tourniquet actually stops a bleed, that an untreated tension pneumothorax actually kills, that a casualty's face actually reflects their real state — depends on this system being trustworthy. It exists to give every other system a source of ground truth that behaves like real physiology instead of scripted numbers. Key facts driving this design: - Apache 2.0 licensed; the Unreal plugin was co-developed by Kitware and Lumeto and funded by an Epic MegaGrant, exposing the engine via a **Blueprint Actor Component** — a strong fit for this project's Blueprint-only codebase. - Models the exact insults and interventions this scenario needs: hemorrhage, tension pneumothorax, airway obstruction, plus tourniquet, wound packing, needle decompression, chest seal, NPA/OPA, and supplemental oxygen. - Engine state serializes to JSON/binary and reloads insta ...

**Generated output (post-critic):**

```json
{
  "injury_type": "airway obstruction",
  "severity": "severe",
  "consciousness": "conscious",
  "respiratory_status": "obstructed",
  "affect": "distressed",
  "is_intelligible_speech": false,
  "vocalization": "[harsh inspiratory stridor with panicked catch on each breath]",
  "trigger": "Idle/ambient bark during severe airway obstruction while conscious and distressed, before any airway adjunct intervention",
  "physiology_trace": "Airway resistance/obstruction level; respiration rate; level of consciousness"
}
```

### external hemorrhage / critical / UNCONSCIOUS

**Query:** `casualty vocalization pain external hemorrhage critical unconscious normal unresponsive level of consciousness moan external hemorrhage critical unconscious normal unresponsive level of consciousness moan`

**Top retrieved chunks:**

1. `pulse-physiology-integration.md` > *Dependencies* (bm25=19.38)
   > | System | Direction | Nature of Dependency | |--------|-----------|---------------------| | Casualty Model | Casualty Model depends on this | Every casualty actor owns a physiology component sourced from this system | | Treatment & Interventions | Treatment & Interventions depends on this | Every intervention verb maps 1:1 to a Pulse action call | | Casualty Facial Animation | Casualty Facial Animation depends on this | Provides raw physiology (HR, pressures, SpO2, respiration rate, level of consciousness, hemorrhage, injuries, arrest); that system derives pain, features, and expression from these — pain and affect are NOT outputs of this system | | Scenario Authoring & Data | Scenario Authoring & Data depends on this | Casualty archetypes are authored as Pulse patient files/conditions and pre-baked state trajectories |
2. `casualty-facial-animation.md` > *Summary* (bm25=16.51)
   > MetaHuman casualties carry a **Facial Expression Layer** in their Face AnimBP that blends Facial Pose Library poses, weighted by the output drivers this system computes from raw Pulse physiology (heart rate, pressures, SpO2, respiration rate, level of consciousness, hemorrhage, injuries, arrest) — never wired directly from a single raw vital. This system implements a **deterministic, layered physiology→affect→expression pipeline** — an established affect-modeling design pattern (physiology → derived features → pain/appraisal → coping policy → expression output; see Detailed Design → Core Rules) adopted here as this project's own design decision. Expression is COMPUTED from physiology at every stage, not hand-scripted, so it is reproducible and traceable back to a named variable at a specific time. It still requires SME validation for clinical plausibility before it can be trusted as a tr ...
3. `casualty-facial-animation.md` > *Dependencies* (bm25=16.09)
   > | System | Direction | Nature of Dependency | |--------|-----------|---------------------| | Pulse Physiology Integration | This depends on Pulse Physiology Integration | Reads raw physiology (HR, pressures, SpO2, respiration rate, level of consciousness, hemorrhage, injuries, arrest) as Stage 1 inputs; pain and all affect are derived downstream by this pipeline, NOT read from Pulse | | Casualty Model | This depends on Casualty Model | The Facial Expression Layer is attached to this system's casualty actor | | Treatment & Interventions | This depends on Treatment & Interventions | Intervention events feed Stage 3 acute-pain spikes (see Interactions) | | Patient Assessment | Patient Assessment depends on this | Facial state (Stage 7 output) is a required assessment input | | Triage System | Triage System depends on this | The trainee's face-mediated PERCEPTION of mental-status / respirato ...
4. `casualty-facial-animation.md` > *Core Rules* (bm25=14.97)
   > - Facial Expression Layer blends Facial Pose Library poses (and any custom-authored pain/agonal/unconscious poses), weighted by the **Stage 7 output drivers** computed by this system's physiology→affect→expression pipeline (see the pipeline stages below) — pose weights plus vocalization cue, breathing intensity, gaze probability, and body-motion gain. Raw vitals never drive a pose directly (see the Overview pipeline principle). - Expression fidelity is dynamically concentrated on the casualty currently being assessed; other casualties in view run at a lower facial LOD. - The pipeline below is specified at the design/interface level; which UE construct implements each stage (Blueprint function library, Animation Blueprint state, custom component, etc.) is deferred to → ADR (Phase 3). - **Stage 1 — Physiological inputs** (read from `pulse-physiology-integration.md`, live or baked): heart r ...

**Generated output (post-critic):**

```json
{
  "injury_type": "external hemorrhage",
  "severity": "critical",
  "consciousness": "unconscious",
  "respiratory_status": "normal",
  "affect": "unresponsive",
  "is_intelligible_speech": false,
  "vocalization": "[no vocalization — silent except for shallow breathing]",
  "trigger": "Hard-override rule: level of consciousness below unconsciousness threshold forces Unconscious output state, suppressing vocalization entirely regardless of injury or hemorrhage severity",
  "physiology_trace": "level of consciousness (Stage 1 physiological input, read from Pulse Physiology Integration); bypasses Stage 4–6 appraisal/coping path per hard-override rule and drives Stage 7 output directly to suppress vocalization cue"
}
```

### minor injury / minor / conscious / stoic (Green)

**Query:** `casualty vocalization pain minor injury minor conscious normal stoic minimal ambulatory walking wounded minor injury minor conscious normal stoic minimal ambulatory walking wounded`

**Top retrieved chunks:**

1. `triage-system.md` > *States and Transitions* (bm25=22.20)
   > | State | Entry Condition | Exit Condition | Behavior | |-------|----------------|----------------|----------| | Untriaged | Casualty spawns / trainee has not yet reached them | Trainee begins global sort or individual assessment | No tag applied; casualty AI runs ambient behavior (per `casualty-model.md`) — may call out, move, or lie still per ground-truth state | | Sorted (queue position assigned) | Global sort command issued and casualty responds (walks/waves/still) | Trainee begins individual assessment on this casualty | Casualty has an assessment-order position but no category yet | | Green / Minimal | Individual assessment resolves all-4-true + minor injuries only | Re-triage recomputation changes underlying physiology past a Green threshold | Ambulatory; self-directs to CCP if instructed; low animation/audio priority | | Yellow / Delayed | Individual assessment resolves all-4-tru ...
2. `triage-system.md` > *Ground-Truth Category Derivation* (bm25=21.76)
   > ``` category = derive_salt_category(breathing, obeys_commands_or_purposeful_movement, peripheral_pulse_present, respiratory_distress, hemorrhage_controlled, survivable_with_resources, minor_injuries_only) ``` | Variable | Type | Range | Source | Description | |----------|------|-------|--------|-------------| | breathing | bool | true/false | Pulse Physiology Engine (respiration rate > 0 after airway-opened check) | Whether the casualty is breathing after one airway-reposition attempt | | obeys_commands_or_purposeful_movement | bool | true/false | Pulse Physiology Engine (consciousness/LOC output) | SALT question (a) | | peripheral_pulse_present | bool | true/false | Pulse Physiology Engine (perfusion output) | SALT question (b) | | respiratory_distress | bool | true/false | Pulse Physiology Engine (respiratory rate, effort output) | SALT question (c) — inverted in the formula (question  ...
3. `casualty-model.md` > *Summary* (bm25=13.61)
   > The Casualty Model is the casualty actor itself: its injury loadout, its ground-truth state derived live from Pulse physiology, its mobility/behavior state (ambulatory / purposeful-movement / still), and — critically — the **physiology-LOD arbiter** that decides which casualties run a live physiology engine versus a pre-baked trajectory. Every other gameplay system targets a casualty; this system defines what a casualty *is*. > **Quick reference** — Layer: `Foundation` · Priority: `MVP` · Key deps: `Pulse Physiology Integration`
4. `casualty-facial-animation.md` > *Perceptual pain combine (Stage 3)* (bm25=12.31)
   > ``` pain_total = 1 - (1 - pain_acute) * (1 - pain_lingering) ``` | Variable | Type | Range | Source | Description | |----------|------|-------|--------|-------------| | `pain_acute` | float | 0..1 | Stage 3, event-driven from injuries/interventions; fast decay | Momentary pain spike from a fresh injury or an intervention (e.g. tourniquet application); decays quickly once the triggering event passes | | `pain_lingering` | float | 0..1 | Stage 3, driven by injury severity; slow decay | Baseline pain from the casualty's standing injury severity; decays slowly, reflecting a wound that keeps hurting | | `pain_total` | float | 0..1 | Output of this formula | Combined perceived pain, fed into Stage 4 appraisal only — it reaches expression through the appraisal → coping-policy path, never wired directly to Stage 7 output | **Output range**: 0..1. **Worked example**: `pain_acute = 0.6` (fresh tou ...

**Generated output (post-critic):**

```json
{
  "injury_type": "minor injury",
  "severity": "minor",
  "consciousness": "conscious",
  "respiratory_status": "normal",
  "affect": "stoic",
  "is_intelligible_speech": true,
  "vocalization": "I can walk. It's not bad.",
  "trigger": "Trainee approaches during global sort or begins individual assessment on a Green-category casualty with stoic appraisal/coping policy",
  "physiology_trace": "pain_total (low magnitude, 0.0–0.3 range, driven primarily by minor injury severity with minimal pain_acute spike) and consciousness/LOC (fully conscious, obeys_commands_or_purposeful_movement = true)"
}
```

## Command-response lines (`command_responses`)

### "walk to me" / minor injury / conscious / hearing / ambulatory

**Query:** `voice command SALT global sort compliance If you can hear me and need help, walk to me minor injury conscious ambulatory frightened but cooperative walk to me assessed third If you can hear me and need help, walk to me minor injury conscious ambulatory frightened but cooperative walk to me assessed third`

**Top retrieved chunks:**

1. `triage-system.md` > *Core Rules* (bm25=65.01)
   > 1. **Global sort (SALT Step 1) is voice-command-driven and happens once per casualty cluster**, before individual assessment begins: - Trainee issues (or the RTF/incident command issues on the trainee's behalf) the command "If you can hear me and need help, walk to me" — casualties whose ground-truth physiology supports ambulation (see `casualty-model.md` mobility state) walk toward the trainee's marked position. These are assessed **third**. - Trainee issues "Wave your arm" / "Make a purposeful movement" — casualties capable of purposeful movement but not walking respond. These are assessed **second**. - Casualties who do neither (still, or an obvious uncontrolled life threat visible at a distance, e.g., arterial bleeding) are assessed **first**. - This sort produces an **assessment order**, not a final category — it is a queue, not a tag. 2. **Individual assessment (SALT Step 2) follow ...
2. `game-concept.md` > *Pillar 5: The scene listens — communication is a mechanic* (bm25=64.15)
   > *(Added per product-owner direction (2026-07-16).)* Talking is not an input convenience; it is a core skill being trained. Casualties respond to the trainee's voice according to their actual physiological state: a casualty who can hear and walk complies with "walk to me"; one who cannot, doesn't — and that difference IS the triage signal. The long-term vision extends this in two ways: the system will monitor the trainee's own vocal tone and stress level, and casualties and AI teammates will respond to *how* the trainee communicates — a calm, clear command earning compliance that a panicked one would not (post-MVP; see Scope Tiers, Full Vision). *Design test*: If a casualty's response to the trainee's voice cannot be traced to that casualty's physiological state (consciousness, hearing, mobility), it does not ship.
3. `triage-system.md` > *Interactions with Other Systems* (bm25=46.19)
   > - **Patient Assessment** provides the examine verbs (check breathing, check pulse, check mental status, check hemorrhage) that the individual assessment decision tree in Core Rules Rule 2 consumes as input. Triage System does not implement its own sensing — it reads Patient Assessment's output. - **Casualty Model** owns the casualty's ground-truth physiology state and the mobility/behavior state (ambulatory / purposeful-movement / still) that the global sort in Core Rules Rule 1 reads. - **Voice Command System** resolves the global-sort commands ("walk to me", "wave your arm") and the trainee's spoken category call into game actions; Triage System defines the grammar's *meaning*, Voice Command System defines how the utterance is recognized and dispatched. - **Treatment & Interventions** consumes the triage category and assessment findings to gate which MARCH-order interventions are conte ...
4. `triage-system.md` > *Overview* (bm25=45.20)
   > Triage is the act of sorting many casualties by urgency when resources cannot treat everyone immediately — it is the first and most decision-dense task the trainee performs at every casualty cluster. In this game, triage happens in two passes matching real SALT doctrine: a **global sort** across the whole visible casualty group, driven by voice commands ("walk to me" / "wave your arm"), which sorts casualties into rough response tiers before any hands-on contact; and an **individual assessment** at each casualty, where the trainee checks breathing, pulse/perfusion, mental status, and hemorrhage control to arrive at one of five categories. The category is not fixed once called — SALT explicitly allows and expects re-triage, and this game treats that as core gameplay, not an edge case: a casualty's true state is always live, computed by the physiology simulation, so time pressure and treat ...

**Generated output (post-critic):**

```json
{
  "command": "If you can hear me and need help, walk to me",
  "injury_type": "minor injury",
  "consciousness": "conscious",
  "can_hear": true,
  "mobility": "ambulatory",
  "affect": "frightened but cooperative",
  "compliance": "verbal-and-moves",
  "response": "\"Okay—I'm coming!\" [begins walking quickly toward the trainee's position, favoring one side but maintaining balance]",
  "trigger": "walk-to-me command + conscious + can_hear=true + ambulatory",
  "physiology_trace": "Consciousness=conscious (can process command), hearing capability=true (receives audio input), mobility state=ambulatory (ground-truth physiology supports ambulation per Casualty Model)"
}
```

### "wave your arm" / external hemorrhage / conscious / hearing / still

**Query:** `voice command SALT global sort compliance Wave your arm or make a purposeful movement external hemorrhage conscious still weak, pleading wave your arm purposeful movement assessed second Wave your arm or make a purposeful movement external hemorrhage conscious still weak, pleading wave your arm purposeful movement assessed second`

**Top retrieved chunks:**

1. `triage-system.md` > *Interactions with Other Systems* (bm25=60.15)
   > - **Patient Assessment** provides the examine verbs (check breathing, check pulse, check mental status, check hemorrhage) that the individual assessment decision tree in Core Rules Rule 2 consumes as input. Triage System does not implement its own sensing — it reads Patient Assessment's output. - **Casualty Model** owns the casualty's ground-truth physiology state and the mobility/behavior state (ambulatory / purposeful-movement / still) that the global sort in Core Rules Rule 1 reads. - **Voice Command System** resolves the global-sort commands ("walk to me", "wave your arm") and the trainee's spoken category call into game actions; Triage System defines the grammar's *meaning*, Voice Command System defines how the utterance is recognized and dispatched. - **Treatment & Interventions** consumes the triage category and assessment findings to gate which MARCH-order interventions are conte ...
2. `triage-system.md` > *Core Rules* (bm25=58.99)
   > 1. **Global sort (SALT Step 1) is voice-command-driven and happens once per casualty cluster**, before individual assessment begins: - Trainee issues (or the RTF/incident command issues on the trainee's behalf) the command "If you can hear me and need help, walk to me" — casualties whose ground-truth physiology supports ambulation (see `casualty-model.md` mobility state) walk toward the trainee's marked position. These are assessed **third**. - Trainee issues "Wave your arm" / "Make a purposeful movement" — casualties capable of purposeful movement but not walking respond. These are assessed **second**. - Casualties who do neither (still, or an obvious uncontrolled life threat visible at a distance, e.g., arterial bleeding) are assessed **first**. - This sort produces an **assessment order**, not a final category — it is a queue, not a tag. 2. **Individual assessment (SALT Step 2) follow ...
3. `triage-system.md` > *Overview* (bm25=44.83)
   > Triage is the act of sorting many casualties by urgency when resources cannot treat everyone immediately — it is the first and most decision-dense task the trainee performs at every casualty cluster. In this game, triage happens in two passes matching real SALT doctrine: a **global sort** across the whole visible casualty group, driven by voice commands ("walk to me" / "wave your arm"), which sorts casualties into rough response tiers before any hands-on contact; and an **individual assessment** at each casualty, where the trainee checks breathing, pulse/perfusion, mental status, and hemorrhage control to arrive at one of five categories. The category is not fixed once called — SALT explicitly allows and expects re-triage, and this game treats that as core gameplay, not an edge case: a casualty's true state is always live, computed by the physiology simulation, so time pressure and treat ...
4. `casualty-model.md` > *Overview* (bm25=42.70)
   > A casualty in this game is not a health bar with a skin on it — it is a specific person with an authored injury loadout, a real physiology simulation underneath, and a face and body that reflect that simulation truthfully. This system is where those pieces come together into one actor the rest of the game can query and act on. Key facts driving this design: - Each casualty actor owns a Pulse physiology component (see `pulse-physiology-integration.md`) plus an authored injury loadout (see `scenario-authoring-data.md`). - This system owns the LOD/promotion decision referenced in `systems-index.md`'s Circular Dependencies note — it is the single point that decides whether a casualty is "live" (full physiology engine) or "baked" (pre-serialized trajectory), consuming trainee proximity/assessment-state as input. - Mobility/behavior state (ambulatory, purposeful-movement, still) is what `triag ...

**Generated output (post-critic):**

```json
{
  "command": "Wave your arm or make a purposeful movement",
  "injury_type": "external hemorrhage",
  "consciousness": "conscious",
  "can_hear": true,
  "mobility": "still",
  "affect": "weak, pleading",
  "compliance": "verbal-acknowledgement-no-move",
  "response": "\"I— I can't… please, I'm hurt…\" [remains still, does not attempt movement]",
  "trigger": "SALT Step 1 global-sort command (wave/purposeful-movement) + conscious + can_hear=true + mobility=still",
  "physiology_trace": "Consciousness=conscious gates awareness of command; can_hear=true gates auditory reception; mobility=still (ground-truth physiology state from Pulse) prevents compliance with movement request despite hearing and understanding it — this casualty is assessed FIRST per SALT global-sort rule (still = tier-1 assessment priority)"
}
```

### "if you can hear me, wave" / tension pneumothorax / UNCONSCIOUS

**Query:** `voice command SALT global sort compliance If you can hear me, wave your hand tension pneumothorax unconscious still unresponsive no response still assessed first If you can hear me, wave your hand tension pneumothorax unconscious still unresponsive no response still assessed first`

**Top retrieved chunks:**

1. `triage-system.md` > *Overview* (bm25=41.10)
   > Triage is the act of sorting many casualties by urgency when resources cannot treat everyone immediately — it is the first and most decision-dense task the trainee performs at every casualty cluster. In this game, triage happens in two passes matching real SALT doctrine: a **global sort** across the whole visible casualty group, driven by voice commands ("walk to me" / "wave your arm"), which sorts casualties into rough response tiers before any hands-on contact; and an **individual assessment** at each casualty, where the trainee checks breathing, pulse/perfusion, mental status, and hemorrhage control to arrive at one of five categories. The category is not fixed once called — SALT explicitly allows and expects re-triage, and this game treats that as core gameplay, not an edge case: a casualty's true state is always live, computed by the physiology simulation, so time pressure and treat ...
2. `triage-system.md` > *Player Fantasy* (bm25=40.96)
   > You are the person who can look at a crowd of hurt strangers and, in seconds, know who needs you *first*. It is not about saving everyone — it is about making the hardest, fastest, most consequential judgment call in medicine, correctly, again and again, while the scene refuses to hold still for you. The tension is entirely diagnostic and moral, never combative: the enemy is uncertainty and time, not a person. Getting it right feels like competence under real pressure; getting it wrong is felt immediately (a casualty you under-triaged visibly deteriorates) but never punished with shame — it becomes the sharpest, most memorable line in your debrief.
3. `triage-system.md` > *Core Rules* (bm25=40.52)
   > 1. **Global sort (SALT Step 1) is voice-command-driven and happens once per casualty cluster**, before individual assessment begins: - Trainee issues (or the RTF/incident command issues on the trainee's behalf) the command "If you can hear me and need help, walk to me" — casualties whose ground-truth physiology supports ambulation (see `casualty-model.md` mobility state) walk toward the trainee's marked position. These are assessed **third**. - Trainee issues "Wave your arm" / "Make a purposeful movement" — casualties capable of purposeful movement but not walking respond. These are assessed **second**. - Casualties who do neither (still, or an obvious uncontrolled life threat visible at a distance, e.g., arterial bleeding) are assessed **first**. - This sort produces an **assessment order**, not a final category — it is a queue, not a tag. 2. **Individual assessment (SALT Step 2) follow ...
4. `triage-system.md` > *Interactions with Other Systems* (bm25=30.99)
   > - **Patient Assessment** provides the examine verbs (check breathing, check pulse, check mental status, check hemorrhage) that the individual assessment decision tree in Core Rules Rule 2 consumes as input. Triage System does not implement its own sensing — it reads Patient Assessment's output. - **Casualty Model** owns the casualty's ground-truth physiology state and the mobility/behavior state (ambulatory / purposeful-movement / still) that the global sort in Core Rules Rule 1 reads. - **Voice Command System** resolves the global-sort commands ("walk to me", "wave your arm") and the trainee's spoken category call into game actions; Triage System defines the grammar's *meaning*, Voice Command System defines how the utterance is recognized and dispatched. - **Treatment & Interventions** consumes the triage category and assessment findings to gate which MARCH-order interventions are conte ...

**Generated output (post-critic):**

```json
{
  "command": "If you can hear me, wave your hand",
  "injury_type": "tension pneumothorax",
  "consciousness": "unconscious",
  "can_hear": false,
  "mobility": "still",
  "affect": "unresponsive",
  "compliance": "no-response",
  "response": "[no response — remains still]",
  "trigger": "wave/purposeful-movement command + unconscious + cannot hear",
  "physiology_trace": "Level of consciousness (unconscious) and hearing capability (false) gate all compliance; mobility state (still) reflects inability to perform purposeful movement. Per SALT global sort (Core Rules Rule 1), casualties who do not respond to voice commands are assessed first."
}
```

### "walk to the flag" / minor injury / conscious / DEAF / ambulatory

**Query:** `voice command SALT global sort compliance Move to the flag if you can walk minor injury conscious ambulatory confused, straining to understand hearing cannot hear does not comply Move to the flag if you can walk minor injury conscious ambulatory confused, straining to understand hearing cannot hear does not comply`

**Top retrieved chunks:**

1. `game-concept.md` > *Pillar 5: The scene listens — communication is a mechanic* (bm25=58.16)
   > *(Added per product-owner direction (2026-07-16).)* Talking is not an input convenience; it is a core skill being trained. Casualties respond to the trainee's voice according to their actual physiological state: a casualty who can hear and walk complies with "walk to me"; one who cannot, doesn't — and that difference IS the triage signal. The long-term vision extends this in two ways: the system will monitor the trainee's own vocal tone and stress level, and casualties and AI teammates will respond to *how* the trainee communicates — a calm, clear command earning compliance that a panicked one would not (post-MVP; see Scope Tiers, Full Vision). *Design test*: If a casualty's response to the trainee's voice cannot be traced to that casualty's physiological state (consciousness, hearing, mobility), it does not ship.
2. `game-concept.md` > *Unique Hook* (bm25=46.90)
   > It's like SimX's Triage Mass Casualty scenario, AND ALSO the casualty's own face is a physiological readout driven by a validated whole-body human physiology simulation, not scripted animation — live and real-time for casualties under active assessment or nearby the trainee, and physiology-derived, pre-computed trajectories (branching at authored decision points as the trainee acts) for casualties further away — so learning to read distress, pallor, respiratory effort, and consciousness on a human face IS the assessment skill being trained, everywhere in the scene. AND ALSO the scene itself is not a static stage: it began in a zone that is merely *cleared*, not *secure*, and can re-escalate mid-treatment, forcing the trainee to interrupt care and adapt exactly the way a real Rescue Task Force response does. AND ALSO the scene answers the trainee's voice: the global sort, triage calls, an ...
3. `triage-system.md` > *Core Rules* (bm25=37.69)
   > 1. **Global sort (SALT Step 1) is voice-command-driven and happens once per casualty cluster**, before individual assessment begins: - Trainee issues (or the RTF/incident command issues on the trainee's behalf) the command "If you can hear me and need help, walk to me" — casualties whose ground-truth physiology supports ambulation (see `casualty-model.md` mobility state) walk toward the trainee's marked position. These are assessed **third**. - Trainee issues "Wave your arm" / "Make a purposeful movement" — casualties capable of purposeful movement but not walking respond. These are assessed **second**. - Casualties who do neither (still, or an obvious uncontrolled life threat visible at a distance, e.g., arterial bleeding) are assessed **first**. - This sort produces an **assessment order**, not a final category — it is a queue, not a tag. 2. **Individual assessment (SALT Step 2) follow ...
4. `casualty-model.md` > *Open Questions* (bm25=36.07)
   > | Question | Owner | Deadline | Resolution | |----------|-------|----------|-----------| | Exact LOD promotion/demotion trigger (distance threshold vs. explicit action) | game-designer | Before Detailed Design is finalized | [To be designed] | | Which UE construct implements the casualty actor (Blueprint class hierarchy, data asset composition)? | ue-blueprint-specialist | Phase 3 (Technical Setup) | → ADR (Phase 3) — not a GDD-time decision | | Pillar-5 gating constraint (per product-owner direction (2026-07-16)): the ambulatory / purposeful-movement / still behavior-state derivation must gate on consciousness and hearing capability, not physical ambulation alone — a deaf or unconscious casualty must not auto-comply with a spoken global-sort command just because their legs work (see `game-concept.md` Pillar 5 design test; `triage-system.md` Core Rules) | game-designer | Before the mobil ...

**Generated output (post-critic):**

```json
{
  "command": "Move to the flag if you can walk",
  "injury_type": "minor injury",
  "consciousness": "conscious",
  "can_hear": false,
  "mobility": "ambulatory",
  "affect": "confused, straining to understand",
  "compliance": "no-response",
  "response": "[no response — remains still, eyes scanning the trainee's face and lips with visible confusion; head tilted slightly as if straining to parse meaning from visual cues alone]",
  "trigger": "ambulatory-walk command + conscious + deaf",
  "physiology_trace": "hearing capability = false (gates compliance per Pillar 5 design test; consciousness and mobility are present but insufficient without hearing to process spoken command)"
}
```

### "squeeze my hand" / open chest wound / altered / hearing / purposeful

**Query:** `voice command SALT global sort compliance Squeeze my hand if you can hear me open/sucking chest wound altered purposeful-movement confused obeys commands mental status chest seal Squeeze my hand if you can hear me open/sucking chest wound altered purposeful-movement confused obeys commands mental status chest seal`

**Top retrieved chunks:**

1. `patient-assessment.md` > *Overview* (bm25=49.39)
   > Assessment is the diagnostic half of the core loop — before the trainee can sort or treat anyone, they have to find out what's actually wrong. This system defines the vocabulary of clinical questions the trainee can ask a casualty, by hand or by voice, and what they learn from each one. Key facts driving this design: - Assessment sequence follows **MARCH** (Massive hemorrhage → Airway → Respiration → Circulation → Head injury/Hypothermia) — the TECC/TCCC standard that supersedes ABC for penetrating trauma because exsanguination kills faster than airway compromise. - Examine verb set: check breathing, check radial pulse / capillary refill, check mental status ("squeeze my hand" / follows commands), check for major hemorrhage, expose the chest for respiratory-distress signs. - Casualty facial expression (pain, consciousness, respiratory distress, pallor) is itself a required, readable-at-d ...
2. `treatment-interventions.md` > *Core Rules* (bm25=40.00)
   > - Verb set (see Summary/Overview above) is exhaustive for the POC's warm-zone scope; no additional interventions are modeled. - Each intervention verb has a defined MARCH-order relevance: tourniquet application and wound packing (hemostatic or plain gauze) + pressure dressing are **M — Massive hemorrhage** tier; chest seal and needle decompression are **R — Respiration** tier (they treat the two respiratory life threats — open/sucking chest wound and tension pneumothorax — not hemorrhage); NPA/OPA airway adjuncts are **A — Airway** tier; recovery position is **A — Airway** tier for unconscious casualties. These four MARCH tiers are kept distinct — M and R are never blurred under one combined label. - [To be designed] — exact interaction mechanic per verb, success/failure conditions, and how partial/incorrect application (e.g., a tourniquet applied too loosely) is represented, if at all,  ...
3. `triage-system.md` > *Core Rules* (bm25=39.15)
   > 1. **Global sort (SALT Step 1) is voice-command-driven and happens once per casualty cluster**, before individual assessment begins: - Trainee issues (or the RTF/incident command issues on the trainee's behalf) the command "If you can hear me and need help, walk to me" — casualties whose ground-truth physiology supports ambulation (see `casualty-model.md` mobility state) walk toward the trainee's marked position. These are assessed **third**. - Trainee issues "Wave your arm" / "Make a purposeful movement" — casualties capable of purposeful movement but not walking respond. These are assessed **second**. - Casualties who do neither (still, or an obvious uncontrolled life threat visible at a distance, e.g., arterial bleeding) are assessed **first**. - This sort produces an **assessment order**, not a final category — it is a queue, not a tag. 2. **Individual assessment (SALT Step 2) follow ...
4. `triage-system.md` > *Ground-Truth Category Derivation* (bm25=38.63)
   > ``` category = derive_salt_category(breathing, obeys_commands_or_purposeful_movement, peripheral_pulse_present, respiratory_distress, hemorrhage_controlled, survivable_with_resources, minor_injuries_only) ``` | Variable | Type | Range | Source | Description | |----------|------|-------|--------|-------------| | breathing | bool | true/false | Pulse Physiology Engine (respiration rate > 0 after airway-opened check) | Whether the casualty is breathing after one airway-reposition attempt | | obeys_commands_or_purposeful_movement | bool | true/false | Pulse Physiology Engine (consciousness/LOC output) | SALT question (a) | | peripheral_pulse_present | bool | true/false | Pulse Physiology Engine (perfusion output) | SALT question (b) | | respiratory_distress | bool | true/false | Pulse Physiology Engine (respiratory rate, effort output) | SALT question (c) — inverted in the formula (question  ...

**Generated output (post-critic):**

```json
{
  "command": "Squeeze my hand if you can hear me",
  "injury_type": "open/sucking chest wound",
  "consciousness": "altered",
  "can_hear": true,
  "mobility": "purposeful-movement",
  "affect": "confused",
  "compliance": "non-verbal-movement",
  "response": "[Squeezes weakly, then releases — hand drops back to chest. Eyes are open but unfocused; does not track the trainee's face.]",
  "trigger": "squeeze-my-hand command + altered consciousness + hearing intact + purposeful-movement capable",
  "physiology_trace": "Pulse Physiology Engine consciousness/LOC output (altered, capable of purposeful movement per obeys_commands_or_purposeful_movement SALT question a); hearing capability true; open/sucking chest wound drives respiratory effort but does not block motor compliance"
}
```

## Ambient decline vocalizations (`ambient_decline`)

### external hemorrhage / EARLY / conscious

**Query:** `casualty vocalization deterioration external hemorrhage early conscious normal anxious but lucid perfusion blood loss coherent complaint external hemorrhage early conscious normal anxious but lucid perfusion blood loss coherent complaint`

**Top retrieved chunks:**

1. `casualty-facial-animation.md` > *Core Rules* (bm25=13.39)
   > - Facial Expression Layer blends Facial Pose Library poses (and any custom-authored pain/agonal/unconscious poses), weighted by the **Stage 7 output drivers** computed by this system's physiology→affect→expression pipeline (see the pipeline stages below) — pose weights plus vocalization cue, breathing intensity, gaze probability, and body-motion gain. Raw vitals never drive a pose directly (see the Overview pipeline principle). - Expression fidelity is dynamically concentrated on the casualty currently being assessed; other casualties in view run at a lower facial LOD. - The pipeline below is specified at the design/interface level; which UE construct implements each stage (Blueprint function library, Animation Blueprint state, custom component, etc.) is deferred to → ADR (Phase 3). - **Stage 1 — Physiological inputs** (read from `pulse-physiology-integration.md`, live or baked): heart r ...
2. `casualty-facial-animation.md` > *States and Transitions* (bm25=12.82)
   > **Homeostasis states** (computed by this pipeline's Stage 2 from Stage 1 physiology. The raw ground truth — vitals and the arrest flag — is owned by Pulse Physiology Integration / Casualty Model; the homeostasis-state enum and shock probability are DERIVED here, not raw Pulse outputs. If another system (e.g. Triage System) needs a shared homeostasis/shock signal, a single owned definition should be established at the Phase-3 architecture pass to avoid divergent computations — see Open Questions): | State | Entry Condition | Exit / Next State | |-------|-----------------|-------------------| | Stable | Default state while shock probability and MAP/HR trend slopes stay within normal bounds | → Compensating when shock probability crosses [To be designed] | | Compensating | Shock probability crosses its threshold while MAP remains within a defended range (the body is compensating) | → Decomp ...
3. `triage-system.md` > *Tuning Knobs* (bm25=11.31)
   > | Parameter | Current Value | Safe Range | Effect of Increase | Effect of Decrease | |-----------|--------------|------------|-------------------|-------------------| | Respiratory rate "Red" threshold (RR) | 30 breaths/min | 25–35 | Fewer casualties trigger automatic Red via RR alone (more rely on the full 4-question check) | More casualties trigger automatic Red via RR alone, may over-triage | | Capillary refill "poor perfusion" threshold | 2 seconds | 1.5–3.0 s | Stricter — more casualties flagged as poor perfusion (pushes toward Red) | Looser — fewer casualties flagged, may under-triage a shock casualty | | Per-patient triage time target | 30–60 s | 20–90 s | More generous — trainee has more time before pacing pressure/scoring penalty | Tighter — closer to real field conditions but risks frustrating novice trainees | | Tourniquet application pass window | ≤120 s | 60–180 s | More for ...
4. `casualty-facial-animation.md` > *Summary* (bm25=11.02)
   > MetaHuman casualties carry a **Facial Expression Layer** in their Face AnimBP that blends Facial Pose Library poses, weighted by the output drivers this system computes from raw Pulse physiology (heart rate, pressures, SpO2, respiration rate, level of consciousness, hemorrhage, injuries, arrest) — never wired directly from a single raw vital. This system implements a **deterministic, layered physiology→affect→expression pipeline** — an established affect-modeling design pattern (physiology → derived features → pain/appraisal → coping policy → expression output; see Detailed Design → Core Rules) adopted here as this project's own design decision. Expression is COMPUTED from physiology at every stage, not hand-scripted, so it is reproducible and traceable back to a named variable at a specific time. It still requires SME validation for clinical plausibility before it can be trusted as a tr ...

**Generated output (post-critic):**

```json
{
  "injury_type": "external hemorrhage",
  "decline_stage": "early",
  "consciousness": "conscious",
  "respiratory_status": "normal",
  "affect": "anxious but lucid",
  "is_intelligible_speech": true,
  "vocalization": "I'm bleeding... it won't stop. Am I going to be okay?",
  "trigger": "Homeostasis state transitions to Compensating; hemorrhage rate remains elevated while MAP stays within defended range; Stage 4 distress scalar crosses notable threshold",
  "physiology_trace": "Shock probability crossing threshold (Stage 2 derived feature) driven by active hemorrhage rate and rising heart rate (Stage 1); MAP trend slope beginning negative deflection but MAP absolute value still within compensated range; perfusion index declining but above Decompensating threshold"
}
```

### external hemorrhage / MID / altered (confusion)

**Query:** `casualty vocalization deterioration external hemorrhage mid altered normal confused, agitated perfusion index shock compensating agitation external hemorrhage mid altered normal confused, agitated perfusion index shock compensating agitation`

**Top retrieved chunks:**

1. `casualty-facial-animation.md` > *States and Transitions* (bm25=38.45)
   > **Homeostasis states** (computed by this pipeline's Stage 2 from Stage 1 physiology. The raw ground truth — vitals and the arrest flag — is owned by Pulse Physiology Integration / Casualty Model; the homeostasis-state enum and shock probability are DERIVED here, not raw Pulse outputs. If another system (e.g. Triage System) needs a shared homeostasis/shock signal, a single owned definition should be established at the Phase-3 architecture pass to avoid divergent computations — see Open Questions): | State | Entry Condition | Exit / Next State | |-------|-----------------|-------------------| | Stable | Default state while shock probability and MAP/HR trend slopes stay within normal bounds | → Compensating when shock probability crosses [To be designed] | | Compensating | Shock probability crosses its threshold while MAP remains within a defended range (the body is compensating) | → Decomp ...
2. `casualty-facial-animation.md` > *Core Rules* (bm25=11.35)
   > - Facial Expression Layer blends Facial Pose Library poses (and any custom-authored pain/agonal/unconscious poses), weighted by the **Stage 7 output drivers** computed by this system's physiology→affect→expression pipeline (see the pipeline stages below) — pose weights plus vocalization cue, breathing intensity, gaze probability, and body-motion gain. Raw vitals never drive a pose directly (see the Overview pipeline principle). - Expression fidelity is dynamically concentrated on the casualty currently being assessed; other casualties in view run at a lower facial LOD. - The pipeline below is specified at the design/interface level; which UE construct implements each stage (Blueprint function library, Animation Blueprint state, custom component, etc.) is deferred to → ADR (Phase 3). - **Stage 1 — Physiological inputs** (read from `pulse-physiology-integration.md`, live or baked): heart r ...
3. `triage-system.md` > *Tuning Knobs* (bm25=11.06)
   > | Parameter | Current Value | Safe Range | Effect of Increase | Effect of Decrease | |-----------|--------------|------------|-------------------|-------------------| | Respiratory rate "Red" threshold (RR) | 30 breaths/min | 25–35 | Fewer casualties trigger automatic Red via RR alone (more rely on the full 4-question check) | More casualties trigger automatic Red via RR alone, may over-triage | | Capillary refill "poor perfusion" threshold | 2 seconds | 1.5–3.0 s | Stricter — more casualties flagged as poor perfusion (pushes toward Red) | Looser — fewer casualties flagged, may under-triage a shock casualty | | Per-patient triage time target | 30–60 s | 20–90 s | More generous — trainee has more time before pacing pressure/scoring penalty | Tighter — closer to real field conditions but risks frustrating novice trainees | | Tourniquet application pass window | ≤120 s | 60–180 s | More for ...
4. `triage-system.md` > *Ground-Truth Category Derivation* (bm25=10.01)
   > ``` category = derive_salt_category(breathing, obeys_commands_or_purposeful_movement, peripheral_pulse_present, respiratory_distress, hemorrhage_controlled, survivable_with_resources, minor_injuries_only) ``` | Variable | Type | Range | Source | Description | |----------|------|-------|--------|-------------| | breathing | bool | true/false | Pulse Physiology Engine (respiration rate > 0 after airway-opened check) | Whether the casualty is breathing after one airway-reposition attempt | | obeys_commands_or_purposeful_movement | bool | true/false | Pulse Physiology Engine (consciousness/LOC output) | SALT question (a) | | peripheral_pulse_present | bool | true/false | Pulse Physiology Engine (perfusion output) | SALT question (b) | | respiratory_distress | bool | true/false | Pulse Physiology Engine (respiratory rate, effort output) | SALT question (c) — inverted in the formula (question  ...

**Generated output (post-critic):**

```json
{
  "injury_type": "external hemorrhage",
  "decline_stage": "mid",
  "consciousness": "altered",
  "respiratory_status": "normal",
  "affect": "confused, agitated",
  "is_intelligible_speech": true,
  "vocalization": "\"Cold... why's it... I need— where... what's...?\"",
  "trigger": "Homeostasis state = Compensating; consciousness level declining into altered range; no trainee interaction for >15 seconds",
  "physiology_trace": "Mean arterial pressure (MAP) trend slope falling while body compensates; perfusion index dropping below baseline; consciousness level (LOC) declining from conscious threshold toward altered range; shock probability crossing Compensating threshold"
}
```

### tension pneumothorax / MID / altered / distress

**Query:** `casualty vocalization deterioration tension pneumothorax mid altered distress air-hungry, frightened SpO2 hypoxia respiration rate tension pneumothorax needle decompression compensating agitation tension pneumothorax mid altered distress air-hungry, frightened SpO2 hypoxia respiration rate tension pneumothorax needle decompression compensating agitation`

**Top retrieved chunks:**

1. `treatment-interventions.md` > *Acceptance Criteria* (bm25=41.47)
   > - [ ] GIVEN a casualty has an active uncontrolled hemorrhage, WHEN the trainee successfully applies a tourniquet, THEN the casualty's physiology reflects hemorrhage cessation and `hemorrhage_controlled` becomes true for the SALT decision tree - [ ] GIVEN a tension pneumothorax casualty, WHEN the trainee successfully performs needle decompression, THEN respiratory distress physiology improves within a defined time window — [To be designed] - [ ] GIVEN the trainee is in the warm zone, WHEN they attempt an intervention outside warm-zone scope, THEN the action is logged as a scored doctrine violation - [ ] Performance: System update completes within [X]ms — [To be designed] - [ ] No hardcoded values in implementation — pass windows and success conditions are data-driven per the Tuning Knobs table
2. `treatment-interventions.md` > *Core Rules* (bm25=38.57)
   > - Verb set (see Summary/Overview above) is exhaustive for the POC's warm-zone scope; no additional interventions are modeled. - Each intervention verb has a defined MARCH-order relevance: tourniquet application and wound packing (hemostatic or plain gauze) + pressure dressing are **M — Massive hemorrhage** tier; chest seal and needle decompression are **R — Respiration** tier (they treat the two respiratory life threats — open/sucking chest wound and tension pneumothorax — not hemorrhage); NPA/OPA airway adjuncts are **A — Airway** tier; recovery position is **A — Airway** tier for unconscious casualties. These four MARCH tiers are kept distinct — M and R are never blurred under one combined label. - [To be designed] — exact interaction mechanic per verb, success/failure conditions, and how partial/incorrect application (e.g., a tourniquet applied too loosely) is represented, if at all,  ...
3. `pulse-physiology-integration.md` > *Overview* (bm25=36.10)
   > Every clinical claim this game makes — that a tourniquet actually stops a bleed, that an untreated tension pneumothorax actually kills, that a casualty's face actually reflects their real state — depends on this system being trustworthy. It exists to give every other system a source of ground truth that behaves like real physiology instead of scripted numbers. Key facts driving this design: - Apache 2.0 licensed; the Unreal plugin was co-developed by Kitware and Lumeto and funded by an Epic MegaGrant, exposing the engine via a **Blueprint Actor Component** — a strong fit for this project's Blueprint-only codebase. - Models the exact insults and interventions this scenario needs: hemorrhage, tension pneumothorax, airway obstruction, plus tourniquet, wound packing, needle decompression, chest seal, NPA/OPA, and supplemental oxygen. - Engine state serializes to JSON/binary and reloads insta ...
4. `treatment-interventions.md` > *Overview* (bm25=34.62)
   > This is where the trainee's hands do the actual life-saving work — but only the work that real warm-zone doctrine permits. Every intervention here is scoped to life threats, ordered by MARCH, and produces a real physiological response because it drives an actual Pulse action, not a scripted animation. Key facts driving this design: - **Verb set (warm-zone, life-threats-only scope)**: tourniquet application; wound packing (hemostatic or plain gauze) plus pressure dressing; chest seal (vented preferred) for open/sucking chest wounds; needle decompression (2nd intercostal space) for tension pneumothorax; NPA/OPA airway adjuncts; supplemental oxygen; recovery position; drag/carry extraction to the Casualty Collection Point. - Full head-to-toe workups, spinal immobilization rituals, and IV fluid resuscitation wait for the cold zone / evacuation phase — performing them in the warm zone is a sc ...

**Generated output (post-critic):**

```json
{
  "injury_type": "tension pneumothorax",
  "decline_stage": "mid",
  "consciousness": "altered",
  "respiratory_status": "distress",
  "affect": "air-hungry, frightened",
  "is_intelligible_speech": false,
  "vocalization": "Gasping breaths punctuated by fragmentary confused speech: \"Can't... where... I can't...\" — words clipped short by air hunger, each phrase breaking into a grunt or whimper mid-attempt",
  "trigger": "Altered consciousness onset with persistent respiratory distress; casualty no longer tracking trainee movement or environment coherently",
  "physiology_trace": "SpO2 declining below 85% as untreated tension pneumothorax collapses lung volume and impairs oxygenation; altered mental status reflects cerebral hypoxia from falling arterial oxygen saturation"
}
```

### open/sucking chest wound / LATE / unconscious

**Query:** `casualty vocalization deterioration open/sucking chest wound late unconscious distress fading falling SpO2 level of consciousness quiet moan open sucking chest wound chest seal unconscious vocalization suppressed open/sucking chest wound late unconscious distress fading falling SpO2 level of consciousness quiet moan open sucking chest wound chest seal unconscious vocalization suppressed`

**Top retrieved chunks:**

1. `treatment-interventions.md` > *Core Rules* (bm25=72.46)
   > - Verb set (see Summary/Overview above) is exhaustive for the POC's warm-zone scope; no additional interventions are modeled. - Each intervention verb has a defined MARCH-order relevance: tourniquet application and wound packing (hemostatic or plain gauze) + pressure dressing are **M — Massive hemorrhage** tier; chest seal and needle decompression are **R — Respiration** tier (they treat the two respiratory life threats — open/sucking chest wound and tension pneumothorax — not hemorrhage); NPA/OPA airway adjuncts are **A — Airway** tier; recovery position is **A — Airway** tier for unconscious casualties. These four MARCH tiers are kept distinct — M and R are never blurred under one combined label. - [To be designed] — exact interaction mechanic per verb, success/failure conditions, and how partial/incorrect application (e.g., a tourniquet applied too loosely) is represented, if at all,  ...
2. `treatment-interventions.md` > *Tuning Knobs* (bm25=46.96)
   > | Parameter | Current Value | Safe Range | Effect of Increase | Effect of Decrease | |-----------|--------------|------------|-------------------|-------------------| | Tourniquet application pass window | ≤120s | 60–180s | More forgiving | Stricter, closer to expert benchmarks | | [To be designed] — per-intervention success windows for wound packing, chest seal, needle decompression, NPA/OPA | | | | |
3. `treatment-interventions.md` > *Overview* (bm25=42.84)
   > This is where the trainee's hands do the actual life-saving work — but only the work that real warm-zone doctrine permits. Every intervention here is scoped to life threats, ordered by MARCH, and produces a real physiological response because it drives an actual Pulse action, not a scripted animation. Key facts driving this design: - **Verb set (warm-zone, life-threats-only scope)**: tourniquet application; wound packing (hemostatic or plain gauze) plus pressure dressing; chest seal (vented preferred) for open/sucking chest wounds; needle decompression (2nd intercostal space) for tension pneumothorax; NPA/OPA airway adjuncts; supplemental oxygen; recovery position; drag/carry extraction to the Casualty Collection Point. - Full head-to-toe workups, spinal immobilization rituals, and IV fluid resuscitation wait for the cold zone / evacuation phase — performing them in the warm zone is a sc ...
4. `treatment-interventions.md` > *Summary* (bm25=36.56)
   > The trainee's warm-zone life-threat intervention verb set — **tourniquet application, wound packing + pressure dressing, chest seal, needle decompression, NPA/OPA airway adjuncts, supplemental O2, recovery position, and drag/carry extraction** — each mapped 1:1 to a Pulse Physiology Engine action call. Full workups, spinal immobilization rituals, and IV fluids are explicitly out of scope for this system (they belong to a later cold-zone phase, not modeled in the POC). > **Quick reference** — Layer: `Core` · Priority: `MVP` · Key deps: `Casualty Model, Patient Assessment, VR Interaction & Locomotion, Pulse Physiology Integration`

**Generated output (post-critic):**

```json
{
  "injury_type": "open/sucking chest wound",
  "decline_stage": "late",
  "consciousness": "unconscious",
  "respiratory_status": "distress",
  "affect": "fading",
  "is_intelligible_speech": false,
  "vocalization": "Shallow, wet gurgling breaths becoming increasingly irregular, separated by lengthening pauses; faint respiratory effort with diminishing air movement",
  "trigger": "Unconscious casualty with untreated open/sucking chest wound continuing to deteriorate; no chest seal applied, progressive respiratory failure",
  "physiology_trace": "SpO2 critically low (<70%), respiratory rate falling toward agonal pattern, perfusion index dropping as hypoxia-driven cardiovascular collapse progresses"
}
```

### airway obstruction / LATE / unconscious / obstructed

**Query:** `casualty vocalization deterioration airway obstruction late unconscious obstructed agonal hypoxia silence agonal SpO2 airway obstruction late unconscious obstructed agonal hypoxia silence agonal SpO2`

**Top retrieved chunks:**

1. `treatment-interventions.md` > *Core Rules* (bm25=14.93)
   > - Verb set (see Summary/Overview above) is exhaustive for the POC's warm-zone scope; no additional interventions are modeled. - Each intervention verb has a defined MARCH-order relevance: tourniquet application and wound packing (hemostatic or plain gauze) + pressure dressing are **M — Massive hemorrhage** tier; chest seal and needle decompression are **R — Respiration** tier (they treat the two respiratory life threats — open/sucking chest wound and tension pneumothorax — not hemorrhage); NPA/OPA airway adjuncts are **A — Airway** tier; recovery position is **A — Airway** tier for unconscious casualties. These four MARCH tiers are kept distinct — M and R are never blurred under one combined label. - [To be designed] — exact interaction mechanic per verb, success/failure conditions, and how partial/incorrect application (e.g., a tourniquet applied too loosely) is represented, if at all,  ...
2. `casualty-facial-animation.md` > *Core Rules* (bm25=12.78)
   > - Facial Expression Layer blends Facial Pose Library poses (and any custom-authored pain/agonal/unconscious poses), weighted by the **Stage 7 output drivers** computed by this system's physiology→affect→expression pipeline (see the pipeline stages below) — pose weights plus vocalization cue, breathing intensity, gaze probability, and body-motion gain. Raw vitals never drive a pose directly (see the Overview pipeline principle). - Expression fidelity is dynamically concentrated on the casualty currently being assessed; other casualties in view run at a lower facial LOD. - The pipeline below is specified at the design/interface level; which UE construct implements each stage (Blueprint function library, Animation Blueprint state, custom component, etc.) is deferred to → ADR (Phase 3). - **Stage 1 — Physiological inputs** (read from `pulse-physiology-integration.md`, live or baked): heart r ...
3. `pulse-physiology-integration.md` > *Overview* (bm25=10.48)
   > Every clinical claim this game makes — that a tourniquet actually stops a bleed, that an untreated tension pneumothorax actually kills, that a casualty's face actually reflects their real state — depends on this system being trustworthy. It exists to give every other system a source of ground truth that behaves like real physiology instead of scripted numbers. Key facts driving this design: - Apache 2.0 licensed; the Unreal plugin was co-developed by Kitware and Lumeto and funded by an Epic MegaGrant, exposing the engine via a **Blueprint Actor Component** — a strong fit for this project's Blueprint-only codebase. - Models the exact insults and interventions this scenario needs: hemorrhage, tension pneumothorax, airway obstruction, plus tourniquet, wound packing, needle decompression, chest seal, NPA/OPA, and supplemental oxygen. - Engine state serializes to JSON/binary and reloads insta ...
4. `casualty-facial-animation.md` > *Primary-emotion computation (Stage 4)* (bm25=9.79)
   > General form, one instance per discrete primary emotion `x`: ``` emotion_x = clamp01( sum_i( w_i * feature_i ) ) ``` where `feature_i` are normalized physiology/derived-feature inputs from Stages 1–2, and `w_i` are per-emotion, per-input weights. **Worked example form — fear**: ``` fear = clamp01( w1 * shock_probability + w2 * max(0, hr_slope_norm) + w3 * (1 - spo2) ) ``` | Variable | Type | Range | Source | Description | |----------|------|-------|--------|-------------| | `shock_probability` | float | 0..1 | Stage 2 derived feature | Likelihood the casualty is in or entering shock | | `hr_slope_norm` | float | -1..1 (only the positive/rising direction contributes here, via `max(0, ·)`) | Stage 2 derived feature, normalized HR trend slope | Rate of change of heart rate, normalized | | `spo2` | float | 0..1 (normalized from 0–100%) | Stage 1 physiological input | Blood oxygen saturation; ...

**Generated output (post-critic):**

```json
{
  "injury_type": "airway obstruction",
  "decline_stage": "late",
  "consciousness": "unconscious",
  "respiratory_status": "obstructed",
  "affect": "agonal",
  "is_intelligible_speech": false,
  "vocalization": "Faint stridor—barely audible breath sounds against full obstruction—then silence",
  "trigger": "Level of consciousness drops below unconsciousness threshold (Stage 1 physiological input) while airway remains obstructed; arrest flag not yet set but perfusion index critically low",
  "physiology_trace": "Level of consciousness (LOC) below unconsciousness threshold + SpO2 critically low (approaching arrest) + perfusion index critically degraded. Per the Hard-override rule (casualty-facial-animation.md Core Rules), LOC below unconsciousness threshold forces the Unconscious output state, suppressing vocalization and gaze. The obstruction prevents gas exchange; falling SpO2 drives shock probability and fear (Stage 4 appraisal) before consciousness is lost, but once unconscious the appraisal/coping path is bypassed entirely. The faint stridor represents the final involuntary respiratory effort against complete obstruction before the system enters arrest."
}
```
