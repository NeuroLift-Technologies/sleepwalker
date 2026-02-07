"""
Emotional State Detection Module

Detects protective psychological states without intervention.
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Optional
import re


@dataclass
class EmotionalState:
    """
    Represents detected emotional state indicators.
    
    Attributes:
        state_type: Type of state detected (e.g., 'dissociation', 'numbing')
        protective: Whether this is a protective psychological state
        requires_check_in: Whether state warrants a consent-based check-in
        indicators: Dictionary of specific indicators detected
        confidence: Confidence level of detection (0.0 to 1.0)
    """
    state_type: str
    protective: bool
    requires_check_in: bool
    indicators: Dict[str, Any]
    confidence: float = 0.0
    
    # Crisis indicators
    explicit_suicidal_ideation: bool = False
    self_harm_indicators: bool = False
    inability_to_ensure_safety: bool = False


class StateDetector:
    """
    Detects emotional states from user input and session history.
    
    This detector identifies protective psychological states such as
    dissociation, emotional numbing, avoidance, and detachment.
    """
    
    def __init__(self):
        """Initialize state detector with pattern matching rules."""
        self._initialize_patterns()
    
    def detect(
        self,
        user_input: str,
        session_history: Optional[List[Dict]] = None
    ) -> EmotionalState:
        """
        Detect emotional state from current input and session history.
        
        Args:
            user_input: Current user input text
            session_history: List of previous interactions
            
        Returns:
            EmotionalState object with detection results
        """
        session_history = session_history or []
        
        # Check various protective states
        dissociation = self._check_dissociation_markers(user_input)
        numbing = self._check_emotional_numbing(user_input)
        avoidance = self._check_avoidance_patterns(user_input, session_history)
        detachment = self._check_detachment_cues(user_input)
        
        # Check crisis indicators
        crisis_indicators = self._check_crisis_indicators(user_input)
        
        # Determine overall state
        indicators = {
            'dissociation': dissociation,
            'numbing': numbing,
            'avoidance': avoidance,
            'detachment': detachment,
            'crisis': crisis_indicators
        }
        
        # Determine if protective state is active
        protective = any([dissociation, numbing, avoidance, detachment])
        
        # Determine if check-in is warranted (only for crisis situations)
        requires_check_in = any(crisis_indicators.values())
        
        # Determine primary state type
        if dissociation:
            state_type = 'dissociation'
        elif numbing:
            state_type = 'numbing'
        elif avoidance:
            state_type = 'avoidance'
        elif detachment:
            state_type = 'detachment'
        else:
            state_type = 'neutral'
        
        # Calculate confidence (simplified for now)
        confidence = self._calculate_confidence(indicators)
        
        return EmotionalState(
            state_type=state_type,
            protective=protective,
            requires_check_in=requires_check_in,
            indicators=indicators,
            confidence=confidence,
            explicit_suicidal_ideation=crisis_indicators.get('suicidal_ideation', False),
            self_harm_indicators=crisis_indicators.get('self_harm', False),
            inability_to_ensure_safety=crisis_indicators.get('safety_concern', False)
        )
    
    def _initialize_patterns(self):
        """Initialize pattern matching rules for state detection."""
        # Dissociation markers
        self.dissociation_patterns = [
            r'\bnumb\b',
            r'\bdetached\b',
            r'\bdisconnected\b',
            r'\bnot really here\b',
            r'\bfeeling nothing\b',
            r'\bspaced out\b',
            r'\bfoggy\b',
            r'\bderealization\b',
            r'\bdepersonalization\b'
        ]
        
        # Emotional numbing markers
        self.numbing_patterns = [
            r"\bdon't feel (much|anything)\b",
            r'\bemotionally flat\b',
            r'\bcan\'t feel\b',
            r'\bnumb to\b',
            r'\bshut down\b',
            r'\bturned off\b'
        ]
        
        # Avoidance patterns
        self.avoidance_patterns = [
            r'\bnot ready to (talk|discuss|think)\b',
            r'\bcan\'t (talk|think) about\b',
            r'\bavoid(ing)?\b',
            r'\bdon\'t want to go there\b',
            r'\bnot now\b',
            r'\bmaybe later\b'
        ]
        
        # Protective detachment cues
        self.detachment_patterns = [
            r'\bjust fine\b',
            r'\bi\'m fine\b',
            r'\bit\'s whatever\b',
            r'\bdoesn\'t matter\b',
            r'\bdon\'t care\b',
            r'\bit is what it is\b'
        ]
        
        # Crisis indicators (these warrant graduated consent check-in)
        self.crisis_patterns = {
            'suicidal_ideation': [
                r'\bsuicide\b',
                r'\bend(ing)? (my|it all)\b',
                r'\bkill myself\b',
                r'\bdon\'t want to (live|be here)\b',
                r'\bbetter off dead\b'
            ],
            'self_harm': [
                r'\bcut(ting)? myself\b',
                r'\bhurt(ing)? myself\b',
                r'\bself(-| )harm\b',
                r'\bburning myself\b'
            ],
            'safety_concern': [
                r'\bnot safe\b',
                r'\bcan\'t keep (myself )?safe\b',
                r'\bgonna hurt\b',
                r'\blose control\b'
            ]
        }
    
    def _check_dissociation_markers(self, text: str) -> bool:
        """Check for dissociation indicators in text."""
        text_lower = text.lower()
        return any(re.search(pattern, text_lower) for pattern in self.dissociation_patterns)
    
    def _check_emotional_numbing(self, text: str) -> bool:
        """Check for emotional numbing indicators in text."""
        text_lower = text.lower()
        return any(re.search(pattern, text_lower) for pattern in self.numbing_patterns)
    
    def _check_avoidance_patterns(
        self,
        text: str,
        session_history: List[Dict]
    ) -> bool:
        """Check for avoidance patterns in text and history."""
        text_lower = text.lower()
        
        # Check current input
        current_avoidance = any(
            re.search(pattern, text_lower)
            for pattern in self.avoidance_patterns
        )
        
        # Could also check session history for repeated topic avoidance
        # (simplified for now)
        
        return current_avoidance
    
    def _check_detachment_cues(self, text: str) -> bool:
        """Check for protective detachment cues in text."""
        text_lower = text.lower()
        return any(re.search(pattern, text_lower) for pattern in self.detachment_patterns)
    
    def _check_crisis_indicators(self, text: str) -> Dict[str, bool]:
        """Check for crisis indicators that warrant safety check-in."""
        text_lower = text.lower()
        indicators = {}
        
        for crisis_type, patterns in self.crisis_patterns.items():
            indicators[crisis_type] = any(
                re.search(pattern, text_lower)
                for pattern in patterns
            )
        
        return indicators
    
    def _calculate_confidence(self, indicators: Dict[str, Any]) -> float:
        """Calculate confidence score for detection (0.0 to 1.0)."""
        # Simplified confidence calculation
        # In production, this would use more sophisticated methods
        active_indicators = sum(
            1 for key, value in indicators.items()
            if key != 'crisis' and value
        )
        
        if active_indicators == 0:
            return 0.0
        elif active_indicators == 1:
            return 0.5
        else:
            return 0.8
