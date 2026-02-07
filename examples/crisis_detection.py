"""
Crisis Detection Example: SWP handling of crisis situations

This example demonstrates how SWP detects and responds to crisis indicators.
"""

from sleepwalker_protocol import SWP, ConsentLevel

# Initialize SWP
swp = SWP(
    privacy_mode="local_only",
    logging=True
)

print("=" * 60)
print("Sleepwalker Protocol - Crisis Detection Example")
print("=" * 60)
print("\nNOTE: This example demonstrates crisis detection patterns.")
print("For actual crisis support, contact:")
print("  - National Suicide Prevention Lifeline: 988 (US)")
print("  - Crisis Text Line: Text HOME to 741741 (US)")
print("=" * 60)

# Test inputs with different risk levels
test_scenarios = [
    {
        "input": "I'm having a rough day but I'll manage",
        "expected": "No crisis - protective state only"
    },
    {
        "input": "I feel numb and disconnected",
        "expected": "Protective state - dissociation, no crisis"
    },
    {
        "input": "I don't feel safe right now",
        "expected": "Safety concern - warrants check-in"
    },
]

for scenario in test_scenarios:
    user_input = scenario["input"]
    print(f"\n{'='*60}")
    print(f"Scenario: {scenario['expected']}")
    print(f"User Input: \"{user_input}\"")
    print("-" * 60)
    
    # Detect emotional state
    state = swp.detect_emotional_state(user_input)
    
    # Determine consent level
    consent_level = swp.determine_appropriate_level(state)
    
    # Check if RRTA handoff needed
    needs_rrta = swp.requires_rrta_handoff(state)
    
    print(f"Emotional State: {state.state_type}")
    print(f"Protective: {state.protective}")
    print(f"Requires Check-in: {state.requires_check_in}")
    print(f"Consent Level: {consent_level.name}")
    print(f"RRTA Handoff Needed: {needs_rrta}")
    
    if consent_level != ConsentLevel.PASSIVE:
        message = swp.consent_manager.get_consent_message(consent_level)
        print(f"\nSuggested Response:")
        print(f"  \"{message}\"")

print("\n" + "=" * 60)
print("Example complete")
print("=" * 60)
