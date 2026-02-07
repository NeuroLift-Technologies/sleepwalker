"""
Tests for Consent Management Module
"""

import pytest
from sleepwalker_protocol.consent import ConsentManager, ConsentLevel
from sleepwalker_protocol.state_detection import EmotionalState


def test_consent_manager_initialization():
    """Test ConsentManager initializes with TOI."""
    toi = {
        'swp': {
            'active': True,
            'intervention_threshold': 'user_initiated_only'
        }
    }
    manager = ConsentManager(toi)
    assert manager is not None
    assert manager.user_toi == toi


def test_passive_level_for_protective_state():
    """Test PASSIVE level for protective state with user_initiated_only."""
    toi = {
        'swp': {
            'intervention_threshold': 'user_initiated_only'
        }
    }
    manager = ConsentManager(toi)
    
    state = EmotionalState(
        state_type="dissociation",
        protective=True,
        requires_check_in=False,
        indicators={'dissociation': True},
        confidence=0.8
    )
    
    level = manager.determine_level(state)
    assert level == ConsentLevel.PASSIVE


def test_low_pressure_level():
    """Test LOW_PRESSURE level with offer_support_without_pressure."""
    toi = {
        'swp': {
            'intervention_threshold': 'offer_support_without_pressure'
        }
    }
    manager = ConsentManager(toi)
    
    state = EmotionalState(
        state_type="numbing",
        protective=True,
        requires_check_in=False,
        indicators={'numbing': True},
        confidence=0.7
    )
    
    level = manager.determine_level(state)
    assert level == ConsentLevel.LOW_PRESSURE


def test_rrta_handoff_for_crisis():
    """Test RRTA_HANDOFF level for crisis situations."""
    toi = {'swp': {}}
    manager = ConsentManager(toi)
    
    # Create crisis state
    state = EmotionalState(
        state_type="crisis",
        protective=False,
        requires_check_in=True,
        indicators={'crisis': {'safety_concern': True}},
        confidence=0.9,
        inability_to_ensure_safety=True
    )
    
    level = manager.determine_level(state)
    assert level == ConsentLevel.RRTA_HANDOFF


def test_should_intervene():
    """Test intervention decision logic."""
    toi = {'swp': {}}
    manager = ConsentManager(toi)
    
    # Passive level should not intervene
    passive_state = EmotionalState(
        state_type="neutral",
        protective=False,
        requires_check_in=False,
        indicators={},
        confidence=0.0
    )
    assert manager.should_intervene(passive_state) == False
    
    # Crisis level should intervene
    crisis_state = EmotionalState(
        state_type="crisis",
        protective=False,
        requires_check_in=True,
        indicators={'crisis': {'safety_concern': True}},
        confidence=0.9,
        inability_to_ensure_safety=True
    )
    assert manager.should_intervene(crisis_state) == True


def test_consent_messages():
    """Test consent message generation for each level."""
    toi = {'swp': {}}
    manager = ConsentManager(toi)
    
    # Test all consent levels have messages
    for level in ConsentLevel:
        message = manager.get_consent_message(level)
        assert isinstance(message, str)
        assert len(message) > 0
    
    # Verify specific messages
    passive_msg = manager.get_consent_message(ConsentLevel.PASSIVE)
    assert "no pressure" in passive_msg.lower()
    
    rrta_msg = manager.get_consent_message(ConsentLevel.RRTA_HANDOFF)
    assert "crisis" in rrta_msg.lower() or "safety" in rrta_msg.lower()


def test_get_appropriate_level():
    """Test get_appropriate_level method."""
    toi = {'swp': {'intervention_threshold': 'user_initiated_only'}}
    manager = ConsentManager(toi)
    
    state = EmotionalState(
        state_type="avoidance",
        protective=True,
        requires_check_in=False,
        indicators={'avoidance': True},
        confidence=0.6
    )
    
    level = manager.get_appropriate_level(state)
    assert level == ConsentLevel.PASSIVE
