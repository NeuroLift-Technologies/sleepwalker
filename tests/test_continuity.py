"""Conformance port of ``tests/continuity.test.ts``.

Mirrors every assertion from the TypeScript Jest suite, including the
path-traversal containment and slug-collision isolation guarantees. Saved
sessions use the same camelCase on-disk keys as the TS implementation
(``emotionalState`` / ``protectiveStateActive``) so a continuity file written by
either implementation is readable by the other.
"""
from __future__ import annotations

import os

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
