"""
Core Sleepwalker Protocol Implementation

Provides the main SWP class for integrating emotional continuity governance
into AI systems.
"""

from typing import Dict, Optional, Any
import logging
from pathlib import Path

from .state_detection import StateDetector, EmotionalState
from .consent import ConsentManager, ConsentLevel
from .continuity import ContinuityManager
from .toi_loader import TOILoader


logger = logging.getLogger(__name__)


class SleepwalkerProtocol:
    """
    Main Sleepwalker Protocol implementation.
    
    This class provides the core functionality for detecting emotional states,
    managing consent, and maintaining temporal continuity in AI interactions.
    
    Example:
        >>> swp = SWP(
        ...     user_toi_path="path/to/user/toi.yaml",
        ...     privacy_mode="local_only",
        ...     logging=True
        ... )
        >>> user_state = swp.assess_interaction(user_input, session_history)
        >>> response = swp.generate_response(user_input, user_state)
    """
    
    def __init__(
        self,
        user_toi_path: Optional[str] = None,
        privacy_mode: str = "local_only",
        logging: bool = True,
        storage_path: Optional[str] = None
    ):
        """
        Initialize the Sleepwalker Protocol.
        
        Args:
            user_toi_path: Path to user's Terms of Interaction (TOI) file
            privacy_mode: Privacy mode for state storage ("local_only", "encrypted")
            logging: Whether to enable logging
            storage_path: Path for storing session continuity data
        """
        self.privacy_mode = privacy_mode
        self.storage_path = storage_path or ".swp_storage"
        
        if logging:
            logging.basicConfig(level=logging.INFO)
        
        # Load user's TOI configuration
        self.toi_loader = TOILoader(user_toi_path)
        self.user_toi = self.toi_loader.load() if user_toi_path else {}
        
        # Initialize components
        self.state_detector = StateDetector()
        self.consent_manager = ConsentManager(self.user_toi)
        self.continuity_manager = ContinuityManager(self.storage_path)
        
        logger.info("Sleepwalker Protocol initialized")
    
    def detect_emotional_state(
        self,
        user_input: str,
        session_history: Optional[list] = None
    ) -> EmotionalState:
        """
        Monitors for protective psychological states without intervention.
        
        Args:
            user_input: Current user input text
            session_history: List of previous interactions in this session
            
        Returns:
            EmotionalState object with detected indicators
        """
        session_history = session_history or []
        
        # Detect emotional state indicators
        state = self.state_detector.detect(user_input, session_history)
        
        # Log observation without intervening
        self._log_observation(state, intervention=False)
        
        return state
    
    def assess_interaction(
        self,
        user_input: str,
        session_history: Optional[list] = None
    ) -> Dict[str, Any]:
        """
        Assess current interaction context including emotional state and user preferences.
        
        Args:
            user_input: Current user input text
            session_history: List of previous interactions in this session
            
        Returns:
            Dictionary containing state assessment and recommendations
        """
        # Detect emotional state
        emotional_state = self.detect_emotional_state(user_input, session_history)
        
        # Check user's consent preferences
        consent_level = self.consent_manager.get_appropriate_level(emotional_state)
        
        # Get continuity context
        continuity_context = self.continuity_manager.get_context(user_input)
        
        return {
            'emotional_state': emotional_state,
            'consent_level': consent_level,
            'continuity_context': continuity_context,
            'swp_active': self._is_swp_active(),
            'protective_state_active': emotional_state.protective
        }
    
    def generate_response(
        self,
        user_input: str,
        detected_state: Optional[EmotionalState] = None,
        intervention_level: Optional[ConsentLevel] = None
    ) -> Dict[str, Any]:
        """
        Respects user's protective state and TOI boundaries.
        
        Args:
            user_input: Current user input text
            detected_state: Previously detected emotional state (optional)
            intervention_level: Appropriate consent level (optional)
            
        Returns:
            Dictionary containing response guidance and metadata
        """
        # Detect state if not provided
        if detected_state is None:
            detected_state = self.detect_emotional_state(user_input)
        
        # Determine appropriate intervention level if not provided
        if intervention_level is None:
            intervention_level = self.determine_appropriate_level(detected_state)
        
        # Check if SWP is active and user is in protective state
        if self._is_swp_active() and detected_state.protective:
            return self._stable_low_demand_response(
                focus="task_support",
                emotional_demands="minimal",
                processing_pressure="none"
            )
        
        # Check if state requires graduated consent offer
        if detected_state.requires_check_in:
            return self._graduated_consent_offer(level=intervention_level)
        
        # Default: neutral, supportive response
        return {
            'response_type': 'neutral',
            'guidance': 'Provide task-focused support without emotional demands',
            'intervention': 'none'
        }
    
    def determine_appropriate_level(
        self,
        emotional_state: EmotionalState
    ) -> ConsentLevel:
        """
        Determine appropriate consent/intervention level based on emotional state.
        
        Args:
            emotional_state: Detected emotional state
            
        Returns:
            Appropriate ConsentLevel for this situation
        """
        return self.consent_manager.determine_level(emotional_state)
    
    def requires_rrta_handoff(self, user_state: EmotionalState) -> bool:
        """
        Determine if situation requires RRTA (Rapid Response Team) handoff.
        
        Args:
            user_state: Current emotional state
            
        Returns:
            True if RRTA handoff is needed (crisis threshold reached)
        """
        # Check for explicit safety risk indicators
        crisis_indicators = [
            'explicit_suicidal_ideation',
            'self_harm_indicators',
            'inability_to_ensure_safety'
        ]
        
        return any(
            getattr(user_state, indicator, False)
            for indicator in crisis_indicators
        )
    
    def get_context(self) -> Dict[str, Any]:
        """
        Get current SWP context for sharing with other systems (e.g., RRTA).
        
        Returns:
            Dictionary containing SWP context
        """
        return {
            'swp_active': self._is_swp_active(),
            'user_boundaries': self.user_toi.get('swp', {}).get('protected_topics', []),
            'consent_preferences': self.user_toi.get('swp', {}).get('intervention_preference', 'offer_support_without_pressure')
        }
    
    def maintain_continuity(self, user_id: str, session_data: Dict[str, Any]) -> None:
        """
        Preserves emotional boundaries across sessions.
        
        Args:
            user_id: User identifier
            session_data: Current session data to store
        """
        self.continuity_manager.save_session(user_id, session_data)
    
    def _is_swp_active(self) -> bool:
        """Check if SWP is active in user's TOI."""
        return self.user_toi.get('swp', {}).get('active', True)
    
    def _stable_low_demand_response(
        self,
        focus: str,
        emotional_demands: str,
        processing_pressure: str
    ) -> Dict[str, Any]:
        """Generate guidance for stable, low-demand response."""
        return {
            'response_type': 'stable_low_demand',
            'focus': focus,
            'emotional_demands': emotional_demands,
            'processing_pressure': processing_pressure,
            'guidance': 'Maintain stable, task-focused interaction without emotional prompts',
            'intervention': 'none'
        }
    
    def _graduated_consent_offer(self, level: ConsentLevel) -> Dict[str, Any]:
        """Generate graduated consent offer based on level."""
        level_guidance = {
            ConsentLevel.PASSIVE: "I'm here if you need anything. No pressure.",
            ConsentLevel.LOW_PRESSURE: "I noticed you might need support. I can help if you'd like, or we can continue with [current task]. Your choice.",
            ConsentLevel.SAFETY_CHECK: "I want to check in: Are you safe right now? You can answer yes/no, or we can keep working. If you need different support, let me know.",
            ConsentLevel.RRTA_HANDOFF: "I'm concerned about your safety. I'd like to connect you with crisis support. Can I provide crisis resources?"
        }
        
        return {
            'response_type': 'consent_offer',
            'level': level.name,
            'guidance': level_guidance.get(level, level_guidance[ConsentLevel.PASSIVE]),
            'intervention': 'consent_required'
        }
    
    def _log_observation(self, state: EmotionalState, intervention: bool = False) -> None:
        """Log state observation for monitoring purposes."""
        logger.info(f"SWP Observation - State: {state.state_type}, Protective: {state.protective}, Intervention: {intervention}")


# Alias for convenience
SWP = SleepwalkerProtocol
