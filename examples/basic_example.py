"""
Basic Example: Using Sleepwalker Protocol

This example demonstrates basic usage of the SWP library.
"""

from sleepwalker_protocol import SWP

# Initialize SWP
swp = SWP(
    privacy_mode="local_only",
    logging=True
)

# Example user inputs demonstrating different emotional states
test_inputs = [
    "I'm fine, just working through some stuff",
    "I feel really disconnected right now",
    "Can you help me with this project?",
    "I don't want to talk about my feelings",
]

print("=" * 60)
print("Sleepwalker Protocol - Basic Example")
print("=" * 60)

for user_input in test_inputs:
    print(f"\nUser Input: \"{user_input}\"")
    print("-" * 60)
    
    # Assess the interaction
    assessment = swp.assess_interaction(user_input, session_history=[])
    
    # Get response guidance
    response = swp.generate_response(user_input)
    
    print(f"Emotional State: {assessment['emotional_state'].state_type}")
    print(f"Protective State: {assessment['protective_state_active']}")
    print(f"Response Type: {response['response_type']}")
    print(f"Guidance: {response['guidance']}")

print("\n" + "=" * 60)
print("Example complete")
print("=" * 60)
