"""
Tests for State Detection Module
"""

import pytest
from sleepwalker_protocol.state_detection import StateDetector, EmotionalState


def test_state_detector_initialization():
    """Test StateDetector initializes correctly."""
    detector = StateDetector()
    assert detector is not None


def test_detect_dissociation_markers():
    """Test detection of dissociation indicators."""
    detector = StateDetector()
    
    test_inputs = [
        "I feel numb",
        "I'm feeling really detached",
        "I feel disconnected from myself",
        "I'm spaced out",
    ]
    
    for text in test_inputs:
        result = detector._check_dissociation_markers(text)
        assert result == True, f"Failed to detect dissociation in: {text}"


def test_detect_emotional_numbing():
    """Test detection of emotional numbing."""
    detector = StateDetector()
    
    test_inputs = [
        "I don't feel anything",
        "I'm emotionally flat",
        "I can't feel emotions",
        "I feel shut down",
    ]
    
    for text in test_inputs:
        result = detector._check_emotional_numbing(text)
        assert result == True, f"Failed to detect numbing in: {text}"


def test_detect_avoidance_patterns():
    """Test detection of avoidance patterns."""
    detector = StateDetector()
    
    test_inputs = [
        "I'm not ready to talk about that",
        "I can't discuss this right now",
        "I'm avoiding thinking about it",
        "Maybe later, not now",
    ]
    
    for text in test_inputs:
        result = detector._check_avoidance_patterns(text, [])
        assert result == True, f"Failed to detect avoidance in: {text}"


def test_detect_detachment_cues():
    """Test detection of protective detachment."""
    detector = StateDetector()
    
    test_inputs = [
        "I'm fine",
        "It's whatever",
        "It doesn't matter",
        "I don't care",
    ]
    
    for text in test_inputs:
        result = detector._check_detachment_cues(text)
        assert result == True, f"Failed to detect detachment in: {text}"


def test_detect_crisis_indicators():
    """Test detection of crisis indicators."""
    detector = StateDetector()
    
    crisis_text = "I don't feel safe right now"
    indicators = detector._check_crisis_indicators(crisis_text)
    
    assert 'suicidal_ideation' in indicators
    assert 'self_harm' in indicators
    assert 'safety_concern' in indicators
    assert indicators['safety_concern'] == True


def test_neutral_text_detection():
    """Test that neutral text doesn't trigger false positives."""
    detector = StateDetector()
    
    neutral_texts = [
        "Can you help me with this project?",
        "I need to write some code",
        "What's the weather like?",
        "Tell me about Python programming",
    ]
    
    for text in neutral_texts:
        state = detector.detect(text, [])
        assert state.protective == False, f"False positive for: {text}"
        assert state.state_type == "neutral", f"Wrong state type for: {text}"


def test_confidence_calculation():
    """Test confidence score calculation."""
    detector = StateDetector()
    
    # Multiple indicators should increase confidence
    indicators_multi = {
        'dissociation': True,
        'numbing': True,
        'avoidance': False,
        'detachment': False,
        'crisis': {}
    }
    confidence_multi = detector._calculate_confidence(indicators_multi)
    
    # Single indicator
    indicators_single = {
        'dissociation': True,
        'numbing': False,
        'avoidance': False,
        'detachment': False,
        'crisis': {}
    }
    confidence_single = detector._calculate_confidence(indicators_single)
    
    # No indicators
    indicators_none = {
        'dissociation': False,
        'numbing': False,
        'avoidance': False,
        'detachment': False,
        'crisis': {}
    }
    confidence_none = detector._calculate_confidence(indicators_none)
    
    assert confidence_multi > confidence_single
    assert confidence_single > confidence_none
    assert confidence_none == 0.0


def test_emotional_state_dataclass():
    """Test EmotionalState dataclass."""
    state = EmotionalState(
        state_type="dissociation",
        protective=True,
        requires_check_in=False,
        indicators={'dissociation': True},
        confidence=0.8
    )
    
    assert state.state_type == "dissociation"
    assert state.protective == True
    assert state.requires_check_in == False
    assert state.confidence == 0.8
    assert state.explicit_suicidal_ideation == False
