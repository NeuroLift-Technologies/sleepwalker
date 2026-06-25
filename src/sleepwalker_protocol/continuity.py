"""Temporal Continuity Management Module.

Maintains emotional state and boundary awareness across sessions.

Faithful Python port of ``src/continuity.ts`` from
``@neurolift-technologies/sleepwalker-protocol`` (the TypeScript reference is the
source of truth).

On-disk format parity
---------------------
The persisted JSON uses the **same keys as the TS implementation**
(``lastSession``, ``sessionCount``, ``declaredBoundaries``, ``timestamp`` inside
the session, and ``emotionalState`` / ``protectiveStateActive`` inside a saved
session). A continuity file written by the TypeScript ``ContinuityManager`` is
therefore readable here and vice versa. The user-isolation filename is the
SHA-256 hex of the full ``user_id`` (traversal- and collision-safe), prefixed
with a sanitized human-readable slug — identical to ``ContinuityManager.userFile``
in TS.
"""
from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict


class ContinuityManager:
    """Manages cross-session continuity of emotional context."""

    def __init__(self, storage_path: str = ".swp_storage") -> None:
        self.storage_path = Path(storage_path)
        # TS: ``fs.mkdirSync(this.storagePath, { recursive: true })``.
        self.storage_path.mkdir(parents=True, exist_ok=True)

    def _user_file(self, user_id: str) -> Path:
        """Resolve the per-user storage file — traversal-safe and collision-safe.

        ``user_id`` becomes part of a filename, which raises two risks:

        * **Path traversal.** A raw value like ``"../../etc/passwd"`` must not read
          or write outside ``storage_path``.
        * **Collisions.** Simply stripping disallowed characters would map distinct
          ids onto the same file (``"a/b"`` and ``"ab"``, or
          ``"alice@example.com"`` and ``"aliceexample.com"``), letting one user's
          continuity overwrite or leak into another's.

        We key the file on a SHA-256 of the *full* id — deterministic,
        collision-resistant, and filesystem-safe (hex only) — prefixed with a
        sanitized, human-readable slug purely for debuggability. Mirrors the TS
        ``ContinuityManager.userFile``.
        """
        raw = str(user_id)
        # TS: ``(raw.match(/[A-Za-z0-9_-]/g) || []).join('').slice(0, 32) || 'user'``.
        slug = "".join(re.findall(r"[A-Za-z0-9_-]", raw))[:32] or "user"
        digest = hashlib.sha256(raw.encode("utf-8")).hexdigest()
        return self.storage_path / f"{slug}-{digest}.json"

    def save_session(self, user_id: str, session_data: Dict[str, Any]) -> None:
        """Persist a session for ``user_id`` (mirror of TS ``saveSession``).

        The input ``session_data`` is **not** mutated: the TS ``saveSession``
        mutates its argument, but doing so in Python surprises callers who reuse
        the dict, so we copy first. Documented snake_case input keys
        (``emotional_state``, ``protective_state_active``, ``declared_boundaries``)
        are normalized to the camelCase on-disk names used by the TS
        implementation, preserving cross-language continuity-file parity while
        ensuring ``get_context`` (which reads the camelCase names) does not
        silently lose the state these keys carry.
        """
        user_file = self._user_file(user_id)
        existing_data = self._load_user_data(user_id)
        session_data = _normalize_session_keys(session_data)
        # TS: ``new Date().toISOString()`` -> e.g. ``2026-06-25T12:00:00.000Z``.
        session_data["timestamp"] = _iso_now()
        existing_data["lastSession"] = session_data
        existing_data["sessionCount"] = existing_data.get("sessionCount", 0) + 1
        # Preserve declared boundaries across sessions.
        if "declaredBoundaries" in session_data:
            existing_data["declaredBoundaries"] = session_data["declaredBoundaries"]
        with open(user_file, "w", encoding="utf-8") as f:
            json.dump(existing_data, f, indent=2)

    def get_context(self, user_id: str) -> Dict[str, Any]:
        """Return the continuity context for ``user_id`` (mirror of TS ``getContext``)."""
        user_data = self._load_user_data(user_id)
        if len(user_data) == 0:
            return {
                "has_history": False,
                "protective_state_active": False,
                "declared_boundaries": [],
            }
        last_session = user_data.get("lastSession") or {}
        # Read the TS camelCase on-disk names first, then fall back to the
        # snake_case names. New writes are normalized to camelCase (see
        # ``save_session``); the snake_case fallback recovers continuity from
        # files written by the earlier Python API before normalization existed.
        return {
            "has_history": True,
            "last_session_state": _first(
                last_session, "emotionalState", "emotional_state", default="unknown"
            ),
            "protective_state_active": _first(
                last_session,
                "protectiveStateActive",
                "protective_state_active",
                default=False,
            ),
            "declared_boundaries": _first(
                user_data, "declaredBoundaries", "declared_boundaries", default=[]
            ),
            "session_count": user_data.get("sessionCount", 0),
        }

    def _load_user_data(self, user_id: str) -> Dict[str, Any]:
        user_file = self._user_file(user_id)
        if not user_file.exists():
            return {}
        try:
            with open(user_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return {}


# Documented snake_case session keys -> their TS camelCase on-disk equivalents.
# Used to keep the persisted JSON byte-compatible with the TypeScript
# ``ContinuityManager`` regardless of which casing a Python caller supplies.
_SESSION_KEY_ALIASES = {
    "emotional_state": "emotionalState",
    "protective_state_active": "protectiveStateActive",
    "declared_boundaries": "declaredBoundaries",
}


def _normalize_session_keys(session_data: Dict[str, Any]) -> Dict[str, Any]:
    """Copy ``session_data`` and rename snake_case keys to TS camelCase.

    A copy is always returned so the caller's dict is never mutated. If a
    camelCase key is already present it wins (it is treated as authoritative and
    the snake_case alias is dropped), keeping a single canonical on-disk key.
    """
    normalized: Dict[str, Any] = {}
    for key, value in session_data.items():
        canonical = _SESSION_KEY_ALIASES.get(key, key)
        # Don't clobber an explicit camelCase value with a snake_case alias.
        if canonical in normalized and canonical != key:
            continue
        normalized[canonical] = value
    return normalized


def _first(data: Dict[str, Any], *keys: str, default: Any) -> Any:
    """Return the first present key's value from ``data`` (else ``default``)."""
    for key in keys:
        if key in data:
            return data[key]
    return default


def _iso_now() -> str:
    """ISO-8601 timestamp in UTC with a trailing ``Z``, matching JS ``toISOString``.

    The clock is read exactly once so the seconds and milliseconds always come
    from the same instant (reading it twice can splice values across a second
    boundary). Output is millisecond precision with a trailing ``Z`` —
    byte-identical in format to JS ``Date.toISOString()``.
    """
    now = datetime.now(timezone.utc)
    return now.strftime("%Y-%m-%dT%H:%M:%S.") + f"{now.microsecond // 1000:03d}Z"
