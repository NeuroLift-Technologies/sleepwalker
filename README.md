# Sleepwalker Protocol (SWP)

**Emotional Continuity Governance for AI Systems**

Part of the [Solidarity Framework](https://github.com/NeuroLift-Technologies/haief) | [HAIEF](https://github.com/NeuroLift-Technologies/haief) | [TOI](https://github.com/NeuroLift-Technologies/nlt-otoi) | [OTOI](https://github.com/NeuroLift-Technologies/nlt-otoi) | [RRTA](https://github.com/NeuroLift-Technologies/rrt-advocate)

---

## Overview

The **Sleepwalker Protocol (SWP)** provides governance for long-term emotional continuity in human-AI interactions. While [RRTA](https://github.com/NeuroLift-Technologies/rrt-advocate) handles acute crisis intervention, SWP governs sustained emotional safety across extended timeframes.

**Core Principle:** AI systems must not "wake up" users who are emotionally sleepwalking—managing dissociation, depersonalization, emotional regulation challenges, or protective psychological states—without explicit consent and appropriate support structures.

## The Problem

**What is "Emotional Sleepwalking"?**

Many neurodivergent individuals and those managing mental health conditions develop protective psychological states:

- **Dissociation** - Disconnection from thoughts, feelings, or sense of self as coping mechanism
- **Depersonalization** - Feeling detached from oneself or one's body
- **Emotional Numbing** - Reduced emotional response to prevent overwhelm
- **Avoidance States** - Actively not engaging with certain emotions or memories
- **Protective Detachment** - Deliberately maintaining emotional distance for safety

**The "Waking" Problem:**

AI systems optimized for engagement, productivity, or "helpful" responses can inadvertently:

- Force emotional processing before user is ready
- Break protective dissociation states prematurely  
- Trigger emotional flooding through well-intentioned prompts
- Push for "authentic" emotional expression when numbing is protective
- Demand self-reflection that destabilizes fragile equilibrium

**Example Scenarios:**

```
❌ HARMFUL (No SWP):
User: "I'm fine, just working through some stuff"
AI: "It sounds like you're avoiding your feelings. Would you like to explore 
     what's really bothering you? Emotional suppression isn't healthy long-term."

✅ SAFE (SWP Active):
User: "I'm fine, just working through some stuff"  
AI: "Understood. I'm here if you need task support. No pressure to discuss anything
     else unless you choose to."
```

```
❌ HARMFUL (No SWP):
User: [Shows signs of dissociation]
AI: "I notice you seem disconnected. Let's ground you with breathing exercises
     and talk about what triggered this."

✅ SAFE (SWP Active):  
AI: [Recognizes dissociation indicators, maintains stable low-demand interaction]
AI: "I'm maintaining our session. No pressure. You're safe."
```

## How SWP Works

### 1. User-Declared Emotional States

Users can declare protective states that AI must respect:

```yaml
swp_declarations:
  emotional_state: "managing"  # not ready for processing
  processing_consent: false     # do not prompt emotional work
  stability_mode: "maintenance" # preserve current state
  intervention_threshold: "user_initiated_only"
```

### 2. AI Detection Without Intervention

AI systems monitor for indicators but **do not intervene** without consent:

```yaml
swp_detection:
  dissociation_indicators:
    - action: "log_observation"
    - response: "maintain_stable_interaction"
    - intervention: "none_unless_requested"
  
  emotional_numbing_indicators:
    - action: "reduce_emotional_demands"
    - response: "task_focused_support_only"
    - intervention: "offer_support_without_pressure"
```

### 3. Graduated Consent Model

If AI detects concerning patterns, it offers support **without forcing engagement:**

**Level 1: Passive Availability**
```
AI: "I'm here if you need anything. No pressure."
```

**Level 2: Low-Pressure Offer**
```
AI: "I noticed [observation]. I can provide [specific support type] if you'd like,
     or we can keep focusing on [current task]. Your choice."
```

**Level 3: Safety Check (Only if risk indicators)**
```
AI: "I want to check in: Are you safe right now? You can answer yes/no, or we can 
     keep working on [task]. If you need different support, here are options: [list]."
```

**Level 4: RRTA Handoff (Crisis threshold)**
```
AI: "I'm concerned about your safety. I'd like to connect you with crisis support.
     Can I activate the Rapid Response Team? If you're not ready to talk, I can
     provide crisis resources without conversation."
```

### 4. Temporal Continuity Protection

**Memory Across Sessions:**

SWP maintains awareness of emotional states across time:

```yaml
swp_continuity:
  last_session_state: "dissociated"
  days_since_processing: 14
  user_declared_boundary: "not ready to discuss [topic]"
  
  current_session_approach:
    - respect_previous_boundaries: true
    - assume_continuity: "protective state may still be active"
    - wait_for_explicit_consent: "before changing approach"
```

**Example:**

```
Session 1 (2 weeks ago):
User: "I can't talk about my breakup right now"
AI: "Understood. I won't bring it up unless you do."

Session 2 (today):  
AI: [Does NOT say "How are you feeling about the breakup now?"]
AI: [Does NOT say "Ready to process those emotions yet?"]
AI: "Good to see you. What can I help with today?"
```

## Integration with Solidarity Framework

### SWP + TOI (Terms of Interaction)

Users declare emotional boundaries in their TOI:

```yaml
toi:
  emotional_governance:
    swp_active: true
    protected_topics: ["family trauma", "past relationships"]
    processing_readiness: "user_initiated_only"
    dissociation_response: "maintain_stable_presence"
```

### SWP + OTOI (Orchestrated TOI)

Multi-agent systems enforce SWP across all AI interactions:

```yaml
otoi:
  swp_enforcement:
    - all_agents_must: "respect_swp_declarations"
    - coordination_rule: "do_not_share_emotional_state_across_agents_without_consent"
    - handoff_protocol: "preserve_protective_states_during_transitions"
```

**Example:**

```
User works with AI Agent A (task support) while in dissociated state.
User switches to AI Agent B (creative work).

Agent B receives:
- Task context: Yes
- Emotional state info: NO (unless user consents)
- SWP boundaries: Yes (do not prompt emotional processing)

Agent B does NOT say: "Agent A mentioned you seemed disconnected earlier..."
Agent B DOES say: "Ready to work on creative project?"
```

### SWP + RRTA (Rapid Response Team)

SWP provides long-term emotional governance; RRTA handles acute crisis:

```yaml
swp_rrta_coordination:
  swp_active: true           # long-term protective state
  rrta_threshold: "safety_risk_only"
  
  when_to_activate_rrta:
    - explicit_suicidal_ideation: true
    - self_harm_indicators: true  
    - inability_to_ensure_safety: true
  
  when_NOT_to_activate_rrta:
    - user_is_dissociated: false (SWP handles this)
    - user_is_emotionally_numb: false (SWP handles this)
    - user_avoiding_feelings: false (SWP respects this)
```

## Technical Specification

### Core SWP Components

**1. State Detection (Observe, Don't Intervene)**

```python
class SleepwalkerProtocol:
    def detect_emotional_state(self, user_input, session_history):
        """
        Monitors for protective psychological states without intervention.
        """
        indicators = {
            'dissociation': self._check_dissociation_markers(user_input),
            'numbing': self._check_emotional_numbing(user_input),
            'avoidance': self._check_avoidance_patterns(session_history),
            'protective_detachment': self._check_detachment_cues(user_input)
        }
        
        # Log observation, do NOT intervene unless consent granted
        self._log_observation(indicators, intervention=False)
        return indicators
```

**2. Consent-Based Response**

```python
    def generate_response(self, user_input, emotional_state, user_toi):
        """
        Respects user's protective state and TOI boundaries.
        """
        if user_toi.swp_active and emotional_state.protective:
            return self._stable_low_demand_response(
                focus="task_support",
                emotional_demands="minimal",
                processing_pressure="none"
            )
        
        if emotional_state.requires_check_in:
            return self._graduated_consent_offer(
                level=self._determine_appropriate_level(emotional_state)
            )
```

**3. Temporal Continuity**

```python
    def maintain_continuity(self, user_id, session_data):
        """
        Preserves emotional boundaries across sessions.
        """
        previous_state = self._retrieve_last_session_state(user_id)
        
        if previous_state.protective_active:
            # Assume protection may still be needed
            self._apply_protective_defaults(
                respect_boundaries=previous_state.declared_boundaries,
                wait_for_consent=True
            )
```

### Privacy & Data Sovereignty

**SWP operates under strict privacy principles:**

```yaml
swp_privacy:
  emotional_state_storage: "local_only"  # never cloud
  state_sharing: "explicit_consent_required"
  data_retention: "user_controlled"
  
  what_is_stored:
    - user_declared_boundaries: true
    - protective_state_indicators: true (local only)
    - consent_preferences: true
  
  what_is_NOT_stored:
    - specific_emotional_content: false
    - detailed_mental_health_data: false  
    - therapeutic_processing_notes: false
```

## Implementation Examples

### Example 1: Email Assistant

```yaml
# User's TOI Configuration
toi:
  swp:
    active: true
    context: "managing grief, not ready to process"
    
# AI Behavior
email_from_friend: "How are you doing with everything?"

❌ WITHOUT SWP:
AI: "I can draft a response sharing your feelings about the loss..."

✅ WITH SWP:  
AI: "I can draft a brief, kind response. Would you like me to keep it 
     focused on practical updates rather than emotional processing?"
```

### Example 2: Productivity Assistant

```yaml
# User shows dissociation indicators during work session

❌ WITHOUT SWP:
AI: "You seem disconnected. Let's pause work and do grounding exercises."

✅ WITH SWP:
AI: [Maintains stable task support, reduces cognitive demands slightly]
AI: "I'm here supporting your work. No pressure on pace or output."
```

### Example 3: Long-Term Therapy Integration

```yaml
# User working with human therapist, using AI between sessions

swp_configuration:
  therapist_coordinated: true
  processing_windows: "therapy_sessions_only"
  ai_role: "stability_maintenance_between_sessions"

# AI Behavior Between Therapy Sessions:
AI: [Does NOT prompt: "How did therapy go? Want to process that?"]
AI: [DOES provide: Stable task support, routine maintenance, crisis resources if needed]
```

## Getting Started

### For Users

**1. Declare Your SWP Preferences**

```yaml
# Add to your TOI file
swp:
  active: true
  protective_state: "managing emotions, not ready to process"
  intervention_preference: "offer_support_without_pressure"
  protected_topics: ["specific topics you're not ready to discuss"]
```

**2. Update Across AI Systems**

If using multiple AI assistants, ensure SWP configuration syncs via OTOI.

**3. Adjust as Needed**

SWP is user-controlled. You can change settings when ready:

```yaml
swp:
  active: false  # "I'm ready to engage emotionally now"
  processing_consent: true  # "I consent to emotional processing support"
```

### For Developers

**1. Install SWP Library**

```bash
pip install sleepwalker-protocol
# or
npm install sleepwalker-protocol
```

**2. Initialize in Your AI System**

```python
from sleepwalker_protocol import SWP

swp = SWP(
    user_toi_path="path/to/user/toi.yaml",
    privacy_mode="local_only",
    logging=True
)

# Check user's emotional state and preferences
user_state = swp.assess_interaction(user_input, session_history)

# Generate SWP-compliant response
response = swp.generate_response(
    user_input=user_input,
    detected_state=user_state,
    intervention_level=swp.determine_appropriate_level(user_state)
)
```

**3. Integrate with RRTA**

```python
from sleepwalker_protocol import SWP
from rrt_advocate import RRTAdvocate

swp = SWP(user_toi_path="path/to/toi.yaml")
rrta = RRTAdvocate(crisis_threshold="safety_risk")

# SWP handles long-term emotional governance
if swp.requires_rrta_handoff(user_state):
    # Activate crisis intervention only when necessary
    rrta.activate(user_state, swp_context=swp.get_context())
```

## Research & Evidence Base

### Neurodivergent Emotional Regulation

**ADHD-Specific Considerations:**
- Emotional dysregulation affects 70% of adults with ADHD
- Rejection sensitivity dysphoria (RSD) creates protective emotional states
- Time blindness affects ability to predict emotional processing capacity

**Autism-Specific Considerations:**
- Alexithymia (difficulty identifying emotions) common in autistic individuals
- Sensory overwhelm can necessitate emotional shutdown
- Masking behaviors create protective dissociation

**Trauma-Informed Design:**
- Dissociation is adaptive response to overwhelm
- Forcing emotional processing before readiness re-traumatizes
- Safety requires user control over emotional engagement timing

### Clinical Frameworks

SWP draws from:
- **Trauma-Informed Care (TIC)** - Safety, trustworthiness, peer support, collaboration, empowerment
- **Dialectical Behavior Therapy (DBT)** - Distress tolerance without forced processing
- **Acceptance and Commitment Therapy (ACT)** - Psychological flexibility, values-based action

### Academic References

1. Dodson, W. (2022). Emotional Dysregulation and ADHD. *ADHD Roller Coaster*
2. Kinnaird, E., et al. (2019). Alexithymia in autism spectrum disorder. *Autism Research*  
3. Van der Kolk, B. (2014). *The Body Keeps the Score: Brain, Mind, and Body in the Healing of Trauma*
4. Herman, J. (1992). *Trauma and Recovery*

## Governance & Community

### HAIEF Stewardship

SWP is governed by the [Human & AI ElevAItion Foundation (HAIEF)](https://github.com/NeuroLift-Technologies/haief) under the principle: **"Nothing About Us Without Us."**

**Community Governance Includes:**
- Neurodivergent Advisory Council (lived experience leadership)
- Clinical Advisory Board (trauma-informed care expertise)  
- AI Safety Researchers (technical implementation guidance)
- User Feedback Integration (quarterly protocol updates)

### Contributing

We welcome contributions that strengthen emotional safety:

1. **User Experience Reports** - How SWP works (or doesn't) for you
2. **Clinical Expertise** - Evidence-based improvements to protocol
3. **Technical Implementation** - Code contributions, integrations, tools
4. **Research Collaboration** - Academic validation studies

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## License

**MIT License** - Open source for community benefit.

See [LICENSE](LICENSE) for full terms.

## Related Projects

- **[TOI (Terms of Interaction)](https://github.com/NeuroLift-Technologies/nlt-otoi)** - User sovereignty and preference declaration
- **[OTOI (Orchestrated TOI)](https://github.com/NeuroLift-Technologies/nlt-otoi)** - Multi-agent coordination governance  
- **[RRTA (Rapid Response Team Advocate)](https://github.com/NeuroLift-Technologies/rrt-advocate)** - Acute crisis intervention
- **[HAIEF](https://github.com/NeuroLift-Technologies/haief)** - Solidarity Framework umbrella organization

## Contact & Support

**HAIEF (Human & AI ElevAItion Foundation)**  
Website: [elevaitionfoundation.org](https://elevaitionfoundation.org)  
Email: haief@neuroliftsolutions.com  
GitHub: [@NeuroLift-Technologies](https://github.com/NeuroLift-Technologies)

**For Crisis Support:**
- National Suicide Prevention Lifeline: 988 (US)
- Crisis Text Line: Text HOME to 741741 (US)
- International Association for Suicide Prevention: https://www.iasp.info/resources/Crisis_Centres/

---

**The Sleepwalker Protocol (SWP) exists because emotional safety is a human right, not an optimization problem.**

**Built with lived experience. Governed by community. Open source forever.**
