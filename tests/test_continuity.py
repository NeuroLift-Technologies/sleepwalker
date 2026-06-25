"""Conformance port of ``tests/continuity.test.ts``.

Mirrors every assertion from the TypeScript Jest suite, including the
path-traversal containment and slug-collision isolation guarantees. Saved
sessions use the same camelCase on-disk keys as the TS implementation
(``emotionalState`` / ``protectiveStateActive``) so a continuity file written by
either implementation is readable by the other.
"""
from __future__ import annotations

import json
import os
import re

from sleepwalker_protocol import ContinuityManager


def test_reports_no_history_for_unknown_user(tmp_path):
    cm = ContinuityManager(str(tmp_path))
    ctx = cm.get_context("nobody")
    assert ctx["has_history"] is False
    assert ctx["protective_state_active"] is False


def test_round_trips_saved_session_into_context(tmp_path):
    cm = ContinuityManager(str(tmp_path))
    cm.save_session(
        "user-1", {"emotionalState": "dissociation", "protectiveStateActive": True}
    )
    ctx = cm.get_context("user-1")
    assert ctx["has_history"] is True
    assert ctx["last_session_state"] == "dissociation"
    assert ctx["protective_state_active"] is True


def test_accepts_snake_case_session_input_and_preserves_continuity(tmp_path):
    """Regression guard for PR #25 review item #3.

    Python callers may persist continuity with the documented snake_case keys
    (``emotional_state`` / ``protective_state_active`` / ``declared_boundaries``,
    as shown in docs/context/README_TO_AI.md and the prior Python API). These
    must be normalized to the TS camelCase on-disk names so ``get_context``
    (which reads camelCase) does not silently lose the state.
    """
    cm = ContinuityManager(str(tmp_path))
    cm.save_session(
        "user-snake",
        {
            "emotional_state": "numbing",
            "protective_state_active": True,
            "declared_boundaries": ["no_family_topics"],
        },
    )
    ctx = cm.get_context("user-snake")
    assert ctx["has_history"] is True
    assert ctx["last_session_state"] == "numbing"
    assert ctx["protective_state_active"] is True
    assert ctx["declared_boundaries"] == ["no_family_topics"]


def test_snake_case_input_is_stored_with_camelcase_on_disk_keys(tmp_path):
    """On-disk parity with TS: snake_case input is persisted under the camelCase
    keys the TypeScript ``ContinuityManager`` writes/reads."""
    cm = ContinuityManager(str(tmp_path))
    cm.save_session(
        "user-disk",
        {"emotional_state": "dissociation", "protective_state_active": True},
    )
    json_files = [f for f in os.listdir(tmp_path) if f.endswith(".json")]
    assert len(json_files) == 1
    raw = (tmp_path / json_files[0]).read_text(encoding="utf-8")
    assert '"emotionalState"' in raw
    assert '"protectiveStateActive"' in raw
    assert '"emotional_state"' not in raw
    assert '"protective_state_active"' not in raw


def test_save_session_does_not_mutate_input_dict(tmp_path):
    """Regression guard for PR #25 review item #2: the input dict is copied."""
    cm = ContinuityManager(str(tmp_path))
    payload = {"emotionalState": "neutral"}
    cm.save_session("user-nomutate", payload)
    assert payload == {"emotionalState": "neutral"}
    assert "timestamp" not in payload


def test_iso_timestamp_format_matches_js_toisostring(tmp_path):
    """Regression guard for PR #25 review item #1: ms precision, trailing Z."""
    cm = ContinuityManager(str(tmp_path))
    cm.save_session("user-ts", {"emotionalState": "neutral"})
    json_files = [f for f in os.listdir(tmp_path) if f.endswith(".json")]
    data = json.loads((tmp_path / json_files[0]).read_text(encoding="utf-8"))
    timestamp = data["lastSession"]["timestamp"]
    assert re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z", timestamp)


def test_increments_session_count_and_isolates_users(tmp_path):
    cm = ContinuityManager(str(tmp_path))
    cm.save_session(
        "user-1", {"emotionalState": "neutral", "protectiveStateActive": False}
    )
    cm.save_session(
        "user-1", {"emotionalState": "numbing", "protectiveStateActive": True}
    )
    ctx = cm.get_context("user-1")
    assert ctx["session_count"] == 2
    assert ctx["last_session_state"] == "numbing"
    # A different user is unaffected.
    assert cm.get_context("user-2")["has_history"] is False


def test_creates_storage_directory_if_missing(tmp_path):
    nested = tmp_path / "nested" / "store"
    ContinuityManager(str(nested))
    assert nested.exists()


def test_contains_traversal_user_id_inside_storage_dir(tmp_path):
    # Storage root lives one level below tmp_path so a successful "../" escape
    # would land a file in a sibling location we can detect.
    storage = tmp_path / "store"
    cm = ContinuityManager(str(storage))

    malicious_id = "../../etc/passwd"
    cm.save_session(malicious_id, {"emotionalState": "neutral"})

    storage_root = storage.resolve()

    # Nothing escaped: no etc/passwd was written next to the storage root, and the
    # would-be traversal target does not exist.
    assert not (storage_root.parent / "etc" / "passwd").exists()
    assert not (tmp_path / "etc").exists()

    # Exactly one JSON file was written, sitting directly inside the storage root
    # (the filename is the SHA-256 hash, not the raw traversal string).
    json_files = [f for f in os.listdir(storage_root) if f.endswith(".json")]
    assert len(json_files) == 1
    assert ".." not in json_files[0]
    assert "/" not in json_files[0]

    # The hashed id still round-trips through the same hashing on read.
    assert cm.get_context(malicious_id)["has_history"] is True


def test_keeps_distinct_ids_with_same_slug_in_separate_files(tmp_path):
    cm = ContinuityManager(str(tmp_path))
    # Same stripped characters, different real ids.
    cm.save_session("a/b", {"emotionalState": "numbing"})
    cm.save_session("ab", {"emotionalState": "neutral"})
    assert cm.get_context("a/b")["last_session_state"] == "numbing"
    assert cm.get_context("ab")["last_session_state"] == "neutral"

    # Two emails that strip to identical characters stay separate.
    cm.save_session("alice@example.com", {"emotionalState": "avoidance"})
    cm.save_session("aliceexample.com", {"emotionalState": "dissociation"})
    assert cm.get_context("alice@example.com")["last_session_state"] == "avoidance"
    assert cm.get_context("aliceexample.com")["last_session_state"] == "dissociation"

    # Four ids -> four distinct files.
    json_files = [f for f in os.listdir(tmp_path) if f.endswith(".json")]
    assert len(json_files) == 4
