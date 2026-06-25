"""Conformance port of ``tests/consent.test.ts``.

Mirrors every assertion from the TypeScript Jest suite.
"""
from __future__ import annotations

from typing import Any, Dict

from sleepwalker_protocol import ConsentLevel, ConsentManager
from sleepwalker_protocol.state_detection import EmotionalState


def state(**overrides: Any) -> EmotionalState:
    """Build an EmotionalState with sensible defaults for targeted assertions.

    Mirror of the TS test helper ``state(overrides)``.
    """
    base: Dict[str, Any] = {
        "state_type": "neutral",
        "protective": False,
        "requires_check_in": False,
        "indicators": {
            "dissociation": False,
            "numbing": False,
            "avoidance": False,
            "detachment": False,
            "crisis": {
                "suicidal_ideation": False,
                "self_harm": False,
                "safety_concern": False,
            },
        },
        "confidence": 0,
        "explicit_suicidal_ideation": False,
        "self_harm_indicators": False,
        "inability_to_ensure_safety": False,
    }
    base.update(overrides)
    return EmotionalState(**base)


def test_escalates_any_crisis_flag_to_rrta_handoff():
    cm = ConsentManager()
    assert (
        cm.determine_level(state(explicit_suicidal_ideation=True))
        == ConsentLevel.RRTA_HANDOFF
    )
    assert (
        cm.determine_level(state(self_harm_indicators=True))
        == ConsentLevel.RRTA_HANDOFF
    )
    assert (
        cm.determine_level(state(inability_to_ensure_safety=True))
        == ConsentLevel.RRTA_HANDOFF
    )


def test_safety_check_when_check_in_required_without_crisis():
    cm = ConsentManager()
    assert (
        cm.determine_level(state(requires_check_in=True)) == ConsentLevel.SAFETY_CHECK
    )


def test_defaults_protective_state_to_passive():
    cm = ConsentManager()
    assert cm.determine_level(state(protective=True)) == ConsentLevel.PASSIVE


def test_low_pressure_when_toi_opts_into_offering_support():
    cm = ConsentManager(
        {"swp": {"intervention_threshold": "offer_support_without_pressure"}}
    )
    assert cm.determine_level(state(protective=True)) == ConsentLevel.LOW_PRESSURE


def test_passive_for_neutral_state():
    assert ConsentManager().determine_level(state()) == ConsentLevel.PASSIVE


def test_provides_message_for_every_consent_level():
    cm = ConsentManager()
    for level in ConsentLevel:
        msg = cm.get_consent_message(level)
        assert isinstance(msg, str)
        assert len(msg) > 0
