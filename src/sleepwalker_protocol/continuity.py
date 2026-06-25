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
        """Persist a session for ``user_id`` (mirror of TS ``saveSession``)."""
        user_file = self._user_file(user_id)
        existing_data = self._load_user_data(user_id)
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
        return {
            "has_history": True,
            "last_session_state": last_session.get("emotionalState", "unknown"),
            "protective_state_active": last_session.get("protectiveStateActive", False),
            "declared_boundaries": user_data.get("declaredBoundaries", []),
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


def _iso_now() -> str:
    """ISO-8601 timestamp in UTC with a trailing ``Z``, matching JS ``toISOString``."""
    return (
        datetime.now(timezone.utc)
        .strftime("%Y-%m-%dT%H:%M:%S.")
        + f"{datetime.now(timezone.utc).microsecond // 1000:03d}Z"
    )
