"""
Consent Management Module

Manages graduated consent model for AI interventions.
"""

from enum import Enum
from typing import Dict, Any, Optional
from .state_detection import EmotionalState


class ConsentLevel(Enum):
    """
    Graduated consent levels for AI intervention.
    
    Levels progress from minimal to crisis intervention:
    - PASSIVE: Passive availability, no prompting
    - LOW_PRESSURE: Low-pressure offer of support
    - SAFETY_CHECK: Direct safety check (only when risk indicators present)
    - RRTA_HANDOFF: Crisis intervention handoff to Rapid Response Team
    """
    PASSIVE = 1
    LOW_PRESSURE = 2
    SAFETY_CHECK = 3
    RRTA_HANDOFF = 4


class ConsentManager:
    """
    Manages consent-based interactions and graduated intervention model.
    
    This manager determines appropriate intervention levels based on
    user preferences (TOI) and detected emotional states.
    """
    
    def __init__(self, user_toi: Dict[str, Any]):
        """
        Initialize consent manager with user's TOI preferences.
        
        Args:
            user_toi: User's Terms of Interaction configuration
        """
        self.user_toi = user_toi
        self.swp_config = user_toi.get('swp', {})
    
    def get_appropriate_level(
        self,
        emotional_state: EmotionalState
    ) -> ConsentLevel:
        """
        Determine appropriate consent level for current situation.
        
        Args:
            emotional_state: Detected emotional state
            
        Returns:
            Appropriate ConsentLevel
        """
        return self.determine_level(emotional_state)
    
    def determine_level(
        self,
        emotional_state: EmotionalState
    ) -> ConsentLevel:
        """
        Determine appropriate intervention level based on state and user preferences.
        
        Args:
            emotional_state: Current emotional state
            
        Returns:
            Appropriate ConsentLevel for this situation
        """
        # Check user's intervention threshold preference
        intervention_threshold = self.swp_config.get(
            'intervention_threshold',
            'user_initiated_only'
        )
        
        # Crisis situations warrant RRTA handoff
        if emotional_state.explicit_suicidal_ideation or \
           emotional_state.self_harm_indicators or \
           emotional_state.inability_to_ensure_safety:
            return ConsentLevel.RRTA_HANDOFF
        
        # If state requires check-in but no crisis (shouldn't happen with current logic)
        if emotional_state.requires_check_in:
            return ConsentLevel.SAFETY_CHECK
        
        # For protective states, respect user's intervention preference
        if emotional_state.protective:
            if intervention_threshold == 'user_initiated_only':
                # Minimal intervention - just be available
                return ConsentLevel.PASSIVE
            elif intervention_threshold == 'offer_support_without_pressure':
                # Can offer support gently
                return ConsentLevel.LOW_PRESSURE
            else:
                # Default to passive for protective states
                return ConsentLevel.PASSIVE
        
        # No intervention needed for neutral states
        return ConsentLevel.PASSIVE
    
    def should_intervene(
        self,
        emotional_state: EmotionalState,
        consent_level: Optional[ConsentLevel] = None
    ) -> bool:
        """
        Determine if AI should intervene at all.
        
        Args:
            emotional_state: Current emotional state
            consent_level: Consent level (determined if not provided)
            
        Returns:
            True if intervention is appropriate, False otherwise
        """
        if consent_level is None:
            consent_level = self.determine_level(emotional_state)
        
        # Only intervene for safety checks and RRTA handoffs
        return consent_level in [ConsentLevel.SAFETY_CHECK, ConsentLevel.RRTA_HANDOFF]
    
    def get_consent_message(self, level: ConsentLevel) -> str:
        """
        Get appropriate consent message for given level.
        
        Args:
            level: Consent level
            
        Returns:
            Appropriate message for this consent level
        """
        messages = {
            ConsentLevel.PASSIVE: "I'm here if you need anything. No pressure.",
            ConsentLevel.LOW_PRESSURE: "I can provide support if you'd like, or we can keep focusing on [current task]. Your choice.",
            ConsentLevel.SAFETY_CHECK: "I want to check in: Are you safe right now? You can answer yes/no, or we can keep working. If you need different support, let me know.",
            ConsentLevel.RRTA_HANDOFF: "I'm concerned about your safety. I'd like to connect you with crisis support. Can I provide crisis resources?"
        }
        
        return messages.get(level, messages[ConsentLevel.PASSIVE])
