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
            # ``yaml.load(content) || getDefaultToi()`` — an empty/``None`` parse
            # falls back to the default, matching the TS ``|| this.getDefaultToi()``.
            return yaml.safe_load(content) or self._get_default_toi()
        except Exception:
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
