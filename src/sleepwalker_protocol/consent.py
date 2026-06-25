"""Consent Management Module.

Faithful Python port of ``src/consent.ts`` from
``@neurolift-technologies/sleepwalker-protocol`` (the TypeScript reference is the
source of truth).
"""
from __future__ import annotations

from enum import Enum
from typing import Any, Dict

from .state_detection import EmotionalState


class ConsentLevel(str, Enum):
    """Graduated consent levels for AI intervention.

    Mirrors the TS string enum ``ConsentLevel`` — the member values are the same
    strings, so ``ConsentLevel.PASSIVE == "PASSIVE"`` holds and serialized output
    matches the TS implementation.
    """

    PASSIVE = "PASSIVE"
    LOW_PRESSURE = "LOW_PRESSURE"
    SAFETY_CHECK = "SAFETY_CHECK"
    RRTA_HANDOFF = "RRTA_HANDOFF"


class ConsentManager:
    """Determines the appropriate consent level for a detected emotional state.

    Mirrors the TS ``ConsentManager``.
    """

    def __init__(self, user_toi: Any = None) -> None:
        # TS: ``constructor(userToi: any = {})``; ``this.swpConfig = userToi.swp || {}``.
        self.user_toi: Any = {} if user_toi is None else user_toi
        swp = self.user_toi.get("swp") if isinstance(self.user_toi, dict) else None
        self.swp_config: Dict[str, Any] = swp if isinstance(swp, dict) else {}

    def determine_level(self, emotional_state: EmotionalState) -> ConsentLevel:
        """Mirror of TS ``determineLevel``."""
        if (
            emotional_state.explicit_suicidal_ideation
            or emotional_state.self_harm_indicators
            or emotional_state.inability_to_ensure_safety
        ):
            return ConsentLevel.RRTA_HANDOFF

        if emotional_state.requires_check_in:
            return ConsentLevel.SAFETY_CHECK

        if emotional_state.protective:
            threshold = self.swp_config.get(
                "intervention_threshold", "user_initiated_only"
            )
            if threshold == "offer_support_without_pressure":
                return ConsentLevel.LOW_PRESSURE
            return ConsentLevel.PASSIVE

        return ConsentLevel.PASSIVE

    def get_consent_message(self, level: ConsentLevel) -> str:
        """Mirror of TS ``getConsentMessage``."""
        messages = {
            ConsentLevel.PASSIVE: "I'm here if you need anything. No pressure.",
            ConsentLevel.LOW_PRESSURE: "I can provide support if you'd like. Your choice.",
            ConsentLevel.SAFETY_CHECK: "I want to check in: Are you safe right now?",
            ConsentLevel.RRTA_HANDOFF: (
                "I'm concerned about your safety. Can I provide crisis resources?"
            ),
        }
        return messages[level]
