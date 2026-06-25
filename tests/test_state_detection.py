"""Conformance port of ``tests/stateDetection.test.ts``.

Mirrors every assertion from the TypeScript Jest suite so the Python port matches
the reference behavior of ``@neurolift-technologies/sleepwalker-protocol``.
"""
from __future__ import annotations

from sleepwalker_protocol import StateDetector

detector = StateDetector()


def test_neutral_non_protective_for_ordinary_input():
    s = detector.detect("I finished the report and it went well")
    assert s.state_type == "neutral"
    assert s.protective is False
    assert s.requires_check_in is False
    assert s.confidence == 0.0


def test_detects_dissociation_with_07_confidence():
    s = detector.detect("I just feel numb today")
    assert s.state_type == "dissociation"
    assert s.protective is True
    assert s.indicators["dissociation"] is True
    assert s.confidence == 0.7


def test_detects_detachment_from_flat_im_fine():
    s = detector.detect("honestly i'm fine, whatever")
    assert s.protective is True
    assert s.state_type == "detachment"


def test_flags_explicit_suicidal_ideation_requires_check_in():
    s = detector.detect("sometimes I want to kill myself")
    assert s.explicit_suicidal_ideation is True
    assert s.requires_check_in is True
    assert s.indicators["crisis"]["suicidal_ideation"] is True


def test_flags_self_harm_and_safety_concern():
    assert detector.detect("I keep hurting myself").self_harm_indicators is True
    assert (
        detector.detect("I don't feel safe right now").inability_to_ensure_safety
        is True
    )
