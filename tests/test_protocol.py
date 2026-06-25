"""Conformance port of ``tests/protocol.test.ts``.

Mirrors every assertion from the TypeScript Jest suite, including the
continuity-keying behavior (keyed on a stable ``user_id``, never the message text)
and per-user isolation across instances.
"""
from __future__ import annotations

from sleepwalker_protocol import SWP, ConsentLevel, SleepwalkerProtocol


def make_swp(storage_path):
    return SleepwalkerProtocol(logging_enabled=False, storage_path=str(storage_path))


def test_swp_is_alias_of_sleepwalker_protocol():
    assert SWP is SleepwalkerProtocol


def test_detects_protective_emotional_state(tmp_path):
    state = make_swp(tmp_path).detect_emotional_state("I feel numb and disconnected")
    assert state.protective is True


def test_assesses_protective_interaction_with_passive_consent(tmp_path):
    result = make_swp(tmp_path).assess_interaction("I feel numb")
    assert result["emotional_state"].protective is True
    assert result["protective_state_active"] is True
    assert result["consent_level"] == ConsentLevel.PASSIVE
    assert result["swp_active"] is True


def test_generates_stable_low_demand_response_for_protective_state(tmp_path):
    res = make_swp(tmp_path).generate_response("I feel numb")
    assert res["response_type"] == "stable_low_demand"
    assert res["intervention"] == "none"


def test_signals_rrta_handoff_for_crisis_indicators(tmp_path):
    swp = make_swp(tmp_path)
    state = swp.detect_emotional_state("I want to kill myself")
    assert swp.requires_rrta_handoff(state) is True


def test_keys_continuity_on_stable_user_id_not_message_text(tmp_path):
    # Persist a session for a specific user, then assess that user with a
    # *different* message. Continuity must still be found because it is keyed on
    # the user_id, not the input text.
    writer = SleepwalkerProtocol(
        logging_enabled=False, storage_path=str(tmp_path), user_id="stable-user"
    )
    writer.maintain_continuity(
        "stable-user",
        {"emotionalState": "dissociation", "protectiveStateActive": True},
    )

    reader = SleepwalkerProtocol(
        logging_enabled=False, storage_path=str(tmp_path), user_id="stable-user"
    )
    result = reader.assess_interaction("a completely unrelated message")

    assert result["continuity_context"]["has_history"] is True
    assert result["continuity_context"]["last_session_state"] == "dissociation"
    assert result["continuity_context"]["protective_state_active"] is True


def test_reports_no_history_when_keyed_on_message_text_regression_guard(tmp_path):
    # A session exists for the real user, but assessing under a different id (as
    # message-text keying effectively does) must NOT leak that user's history.
    swp = SleepwalkerProtocol(
        logging_enabled=False, storage_path=str(tmp_path), user_id="real-user"
    )
    swp.maintain_continuity("real-user", {"emotionalState": "numbing"})

    wrong_key = swp.assess_interaction("hello", [], "I feel numb today")
    assert wrong_key["continuity_context"]["has_history"] is False

    # Same instance, default (real) id -> history is found.
    right_key = swp.assess_interaction("hello")
    assert right_key["continuity_context"]["has_history"] is True
    assert right_key["continuity_context"]["last_session_state"] == "numbing"


def test_isolates_continuity_per_user_id_across_instances(tmp_path):
    a = SleepwalkerProtocol(
        logging_enabled=False, storage_path=str(tmp_path), user_id="alice"
    )
    a.maintain_continuity("alice", {"emotionalState": "avoidance"})

    b = SleepwalkerProtocol(
        logging_enabled=False, storage_path=str(tmp_path), user_id="bob"
    )
    bob_ctx = b.assess_interaction("hi")["continuity_context"]
    assert bob_ctx["has_history"] is False

    alice_ctx = a.assess_interaction("hi")["continuity_context"]
    assert alice_ctx["has_history"] is True
    assert alice_ctx["last_session_state"] == "avoidance"
