"""
TOI Integration Example: Using SWP with Terms of Interaction

This example shows how to integrate SWP with a user's TOI configuration.
"""

from sleepwalker_protocol import SWP
import tempfile
import os

# Create a sample TOI configuration
toi_config = """
swp:
  active: true
  protective_state: "managing emotions, not ready to process"
  intervention_preference: "offer_support_without_pressure"
  protected_topics:
    - "family trauma"
    - "past relationships"
  processing_consent: false
"""

# Write TOI to a temporary file
with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
    f.write(toi_config)
    toi_path = f.name

try:
    # Initialize SWP with user's TOI
    swp = SWP(
        user_toi_path=toi_path,
        privacy_mode="local_only",
        logging=True
    )
    
    print("=" * 60)
    print("Sleepwalker Protocol - TOI Integration Example")
    print("=" * 60)
    print(f"\nUser's SWP Configuration:")
    print(f"  Active: {swp.user_toi['swp']['active']}")
    print(f"  Protected Topics: {swp.user_toi['swp']['protected_topics']}")
    print(f"  Processing Consent: {swp.user_toi['swp']['processing_consent']}")
    
    # Test with various inputs
    test_inputs = [
        "Can you help me write an email?",
        "I'm feeling pretty disconnected today",
        "Let's talk about my family",  # Protected topic
    ]
    
    for user_input in test_inputs:
        print(f"\n{'='*60}")
        print(f"User Input: \"{user_input}\"")
        print("-" * 60)
        
        # Assess interaction
        assessment = swp.assess_interaction(user_input)
        
        # Generate response
        response = swp.generate_response(
            user_input,
            detected_state=assessment['emotional_state']
        )
        
        print(f"State: {assessment['emotional_state'].state_type}")
        print(f"Protective: {assessment['protective_state_active']}")
        print(f"Consent Level: {assessment['consent_level'].name}")
        print(f"Response Type: {response['response_type']}")
        print(f"Intervention: {response['intervention']}")
    
    print("\n" + "=" * 60)
    print("Example complete")
    print("=" * 60)

finally:
    # Clean up temporary file
    os.unlink(toi_path)
