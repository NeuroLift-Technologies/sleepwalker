"""TOI (Terms of Interaction) Loader Module.

Faithful Python port of ``src/toiLoader.ts`` from
``@neurolift-technologies/sleepwalker-protocol`` (the TypeScript reference is the
source of truth). ``js-yaml`` on the TS side maps to ``PyYAML``'s
``yaml.safe_load`` here.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Optional

import yaml


class TOILoader:
    """Loads a user's Terms of Interaction (TOI) document.

    Mirrors the TS ``TOILoader``: ``.json`` paths are parsed as JSON; everything
    else is parsed as YAML; a missing path, missing file, empty document, or any
    parse error falls back to the default TOI.
    """

    def __init__(self, toi_path: Optional[str] = None) -> None:
        self.toi_path: Optional[str] = toi_path

    def load(self) -> Any:
        """Mirror of TS ``load``."""
        if not self.toi_path or not Path(self.toi_path).exists():
            return self._get_default_toi()
        try:
            with open(self.toi_path, "r", encoding="utf-8") as f:
                content = f.read()
            if self.toi_path.endswith(".json"):
                return json.loads(content)
            parsed = yaml.safe_load(content)
            # Match the TS ``yaml.load(content) || this.getDefaultToi()``: JS ``||``
            # only falls back when the parse yields a *nullish* value (an empty or
            # whitespace-only document parses to ``None``/``undefined``). A valid
            # but empty document (``{}`` / ``[]``) is truthy in JS and must be
            # returned as-is, so we fall back ONLY on ``None`` (not Python's
            # broader falsiness, which would discard ``{}`` and ``[]``).
            return self._get_default_toi() if parsed is None else parsed
        # Narrowed to the failure modes the TS ``try`` block can actually hit and
        # that its bare ``catch`` swallows into the default TOI: file-access errors
        # from the read (``OSError`` — covers permission/IsADirectory/IO) and
        # parse errors (``json.JSONDecodeError`` for ``.json``, ``yaml.YAMLError``
        # for YAML). A blanket ``except Exception`` additionally hid unrelated
        # programming bugs; those now surface instead of silently degrading.
        except (OSError, json.JSONDecodeError, yaml.YAMLError):
            return self._get_default_toi()

    def _get_default_toi(self) -> Any:
        """Mirror of TS ``getDefaultToi``."""
        return {
            "swp": {
                "active": True,
                "intervention_threshold": "user_initiated_only",
                "processing_consent": False,
                "protected_topics": [],
            }
        }
