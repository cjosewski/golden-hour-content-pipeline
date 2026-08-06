# Critic Log

Each item's pre-critic draft, the violations the critic flagged, and the corrected post-critic version. A visible before/after here is the consistency-checking evidence.
> 4 of 15 items were revised by the critic.


## Pain / plea barks (`pain_barks`)

### external hemorrhage / severe / conscious / fearful

**Critic verdict:** REVISED

**Violations flagged:**

- R7. GROUNDED, NON-HEROIC TONE: The vocalization 'Oh God—I'm bleeding out—please help me!' crosses into melodramatic territory with 'bleeding out' (a cinematic phrase rather than grounded reality). A real person in severe hemorrhage would more likely reference what they see/feel directly ('I'm bleeding', 'There's so much blood') rather than using the theatrical shorthand 'bleeding out'. The tone reads as scripted drama rather than documentary realism.
- R5. PHYSIOLOGY-TRACEABILITY: The physiology_trace value 'hemorrhage' is too vague. Per the GDD chunks, the system provides 'hemorrhage rate' as the named variable (Chunk 2: 'hemorrhage' listed among raw physiology outputs; Chunk 4: 'hemorrhage_controlled' and 'uncontrolled hemorrhage' as specific states). The trace must name the specific variable that crossed the threshold mentioned in the trigger, which would be 'hemorrhage rate' not the general category 'hemorrhage'.

**Pre-critic draft:**

```json
{
  "injury_type": "external hemorrhage",
  "severity": "severe",
  "consciousness": "conscious",
  "respiratory_status": "normal",
  "affect": "fearful",
  "is_intelligible_speech": true,
  "vocalization": "Oh God—I'm bleeding out—please help me!",
  "trigger": "Hemorrhage rate crosses severe threshold while casualty remains conscious with normal respiratory function; fear appraisal active",
  "physiology_trace": "hemorrhage"
}
```

**Post-critic corrected:**

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

**Critic verdict:** PASS (clean)

**Pre-critic draft:**

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

**Post-critic corrected:**

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

**Critic verdict:** PASS (clean)

**Pre-critic draft:**

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

**Post-critic corrected:**

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

**Critic verdict:** PASS (clean)

**Pre-critic draft:**

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

**Post-critic corrected:**

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

**Critic verdict:** REVISED

**Violations flagged:**

- R7 GROUNDED, NON-HEROIC TONE: The line 'I'm fine. Help the others first.' reads as cinematic hero dialogue—a stoic sacrifice trope common in movies. A real person with a minor injury in an active-shooter scenario would more likely express their state plainly ('It's just my arm' or 'I can walk') or comply with triage protocol, not nobly redirect the medic. This crosses into theatrical framing rather than clinical-documentary realism.

**Pre-critic draft:**

```json
{
  "injury_type": "minor injury",
  "severity": "minor",
  "consciousness": "conscious",
  "respiratory_status": "normal",
  "affect": "stoic",
  "is_intelligible_speech": true,
  "vocalization": "I'm fine. Help the others first.",
  "trigger": "Trainee approaches during global sort or begins individual assessment on a Green-category casualty with stoic appraisal/coping policy",
  "physiology_trace": "pain_total (low magnitude, 0.0–0.3 range, driven primarily by minor injury severity with minimal pain_acute spike) and consciousness/LOC (fully conscious, obeys_commands_or_purposeful_movement = true)"
}
```

**Post-critic corrected:**

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

**Critic verdict:** PASS (clean)

**Pre-critic draft:**

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

**Post-critic corrected:**

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

**Critic verdict:** PASS (clean)

**Pre-critic draft:**

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

**Post-critic corrected:**

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

**Critic verdict:** PASS (clean)

**Pre-critic draft:**

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

**Post-critic corrected:**

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

**Critic verdict:** PASS (clean)

**Pre-critic draft:**

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

**Post-critic corrected:**

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

**Critic verdict:** PASS (clean)

**Pre-critic draft:**

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

**Post-critic corrected:**

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

**Critic verdict:** PASS (clean)

**Pre-critic draft:**

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

**Post-critic corrected:**

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

**Critic verdict:** REVISED

**Violations flagged:**

- R8. AMBIENT DECLINE STAGE CONSISTENCY: The vocalization is too coherent and lucid for mid-stage decline with altered consciousness. The draft delivers a full, grammatically complete sentence with clear subordinate clauses ('I was just... where am I? I need to—wait, what was I...?'). While it shows confusion, the sentence structure is too organized. Mid-stage altered consciousness with confusion/agitation should produce more fragmented, repetitive, or disjointed speech—genuine confusion, not articulate puzzlement. The line reads more like someone momentarily disoriented (early stage) than someone whose consciousness level is actively declining into the altered range due to shock compensation failure.

**Pre-critic draft:**

```json
{
  "injury_type": "external hemorrhage",
  "decline_stage": "mid",
  "consciousness": "altered",
  "respiratory_status": "normal",
  "affect": "confused, agitated",
  "is_intelligible_speech": true,
  "vocalization": "\"Why's it so cold? I was just... where am I? I need to—wait, what was I...?\"",
  "trigger": "Homeostasis state = Compensating; consciousness level declining into altered range; no trainee interaction for >15 seconds",
  "physiology_trace": "Mean arterial pressure (MAP) trend slope falling while body compensates; perfusion index dropping below baseline; consciousness level (LOC) declining from conscious threshold toward altered range; shock probability crossing Compensating threshold"
}
```

**Post-critic corrected:**

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

**Critic verdict:** REVISED

**Violations flagged:**

- R1 RESPIRATORY-DISTRESS SPEECH: The vocalization contains fragmentary words "Can't... can't..." which technically complies with fragmentation, but the lengthy descriptive phrase 'Labored gasping with fragmentary words' followed by 'followed by urgent grunting on each exhale, speech breaking apart into air-hungry whimpers' reads as over-elaborate narration rather than the tight, clipped rendering the rule demands. The draft blurs the line between describing the physiology and rendering the actual vocalization a trainee would hear.
- R8 AMBIENT DECLINE STAGE CONSISTENCY: While the draft attempts to show mid-stage confusion/agitation, the vocalization leans too heavily on described sounds ('urgent grunting', 'air-hungry whimpers') rather than showing the confusion/agitation characteristic of mid-stage decline. Mid-stage for tension pneumothorax should show disorientation or agitated fragmentary attempts at communication, not purely non-verbal sounds—that progression is reserved for late-stage.

**Pre-critic draft:**

```json
{
  "injury_type": "tension pneumothorax",
  "decline_stage": "mid",
  "consciousness": "altered",
  "respiratory_status": "distress",
  "affect": "air-hungry, frightened",
  "is_intelligible_speech": false,
  "vocalization": "Labored gasping with fragmentary words: \"Can't... can't...\" followed by urgent grunting on each exhale, speech breaking apart into air-hungry whimpers",
  "trigger": "Altered consciousness onset with persistent respiratory distress; casualty no longer tracking trainee movement or environment coherently",
  "physiology_trace": "SpO2 declining below 85% as untreated tension pneumothorax collapses lung volume and impairs oxygenation; altered mental status reflects cerebral hypoxia from falling arterial oxygen saturation"
}
```

**Post-critic corrected:**

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

**Critic verdict:** PASS (clean)

**Pre-critic draft:**

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

**Post-critic corrected:**

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

**Critic verdict:** PASS (clean)

**Pre-critic draft:**

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

**Post-critic corrected:**

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
