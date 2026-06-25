"""Core Sleepwalker Protocol Implementation.

Faithful Python port of ``src/protocol.ts`` from
``@neurolift-technologies/sleepwalker-protocol`` (the TypeScript reference is the
source of truth). The TS constructor takes an ``SWPOptions`` object; the Python
mirror exposes the same options as snake_case keyword arguments.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

from .consent import ConsentManager
from .continuity import ContinuityManager
from .state_detection import EmotionalState, StateDetector
from .toi_loader import TOILoader

logger = logging.getLogger(__name__)


class SleepwalkerProtocol:
    """Main Sleepwalker Protocol implementation (mirror of TS ``SleepwalkerProtocol``).

    Args mirror the TS ``SWPOptions`` interface:

    * ``user_toi_path`` — path to the user's TOI document (loaded only when set).
    * ``privacy_mode`` — accepted for API parity (the TS field exists but is unused).
    * ``logging_enabled`` — emit init / state log lines (default ``True``).
    * ``storage_path`` — continuity store directory (default ``".swp_storage"``).
    * ``user_id`` — stable continuity identity for this instance. Never derived from
      input text; falls back to a TOI-declared id, then ``"default_user"``.
    """

    def __init__(
        self,
        user_toi_path: Optional[str] = None,
        privacy_mode: Optional[str] = None,
        logging_enabled: bool = True,
        storage_path: Optional[str] = None,
        user_id: Optional[str] = None,
    ) -> None:
        # TS: ``options.loggingEnabled !== false`` -> default-on unless explicitly False.
        self.logging_enabled = logging_enabled is not False
        self.privacy_mode = privacy_mode

        toi_loader = TOILoader(user_toi_path)
        loaded_toi = toi_loader.load() if user_toi_path else {}
        # A malformed TOI can parse to a non-dict; coerce so downstream ``.swp``
        # lookups are always safe (mirror of the TS ``typeof ... === 'object'`` guard).
        self.user_toi: Dict[str, Any] = (
            loaded_toi if isinstance(loaded_toi, dict) else {}
        )

        # Stable continuity identity for this instance. Never derive this from the
        # user's input text — doing so makes every interaction look like a brand new
        # user and continuity can never be retrieved. Accept an explicit id, then a
        # top-level or swp-nested TOI id. The id is hashed where it becomes a
        # filename (see ContinuityManager._user_file), so traversal is contained.
        swp_toi = self.user_toi.get("swp")
        swp_toi = swp_toi if isinstance(swp_toi, dict) else {}
        self.user_id = (
            user_id
            or self.user_toi.get("user_id")
            or swp_toi.get("user_id")
            or "default_user"
        )

        self.state_detector = StateDetector()
        self.consent_manager = ConsentManager(self.user_toi)
        self.continuity_manager = ContinuityManager(storage_path or ".swp_storage")
        if self.logging_enabled:
            logger.info("Sleepwalker Protocol initialized")

    def detect_emotional_state(
        self, user_input: str, session_history: Optional[List[Any]] = None
    ) -> EmotionalState:
        """Mirror of TS ``detectEmotionalState``."""
        if session_history is None:
            session_history = []
        state = self.state_detector.detect(user_input, session_history)
        if self.logging_enabled:
            logger.info(
                "SWP: State=%s, Protective=%s", state.state_type, state.protective
            )
        return state

    def assess_interaction(
        self,
        user_input: str,
        session_history: Optional[List[Any]] = None,
        user_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Mirror of TS ``assessInteraction``.

        Continuity is keyed by ``user_id`` (defaulting to this instance's
        ``user_id``) — never by the message text.
        """
        if session_history is None:
            session_history = []
        emotional_state = self.detect_emotional_state(user_input, session_history)
        consent_level = self.consent_manager.determine_level(emotional_state)
        continuity_context = self.continuity_manager.get_context(
            user_id or self.user_id
        )
        return {
            "emotional_state": emotional_state,
            "consent_level": consent_level,
            "continuity_context": continuity_context,
            "swp_active": self._swp_active(),
            "protective_state_active": emotional_state.protective,
        }

    def maintain_continuity(self, user_id: str, session_data: Dict[str, Any]) -> None:
        """Preserve emotional boundaries across sessions (mirror of TS ``maintainContinuity``).

        The read (``assess_interaction``) and the write (``maintain_continuity``)
        stay separate so that assessment never implicitly writes to disk.
        """
        self.continuity_manager.save_session(user_id, session_data)

    def generate_response(
        self,
        user_input: str,
        detected_state: Optional[EmotionalState] = None,
    ) -> Dict[str, Any]:
        """Mirror of TS ``generateResponse``."""
        state = detected_state or self.detect_emotional_state(user_input)
        if self._swp_active() and state.protective:
            return {
                "response_type": "stable_low_demand",
                "guidance": "Maintain stable, task-focused interaction",
                "intervention": "none",
            }
        if state.requires_check_in:
            level = self.consent_manager.determine_level(state)
            return {
                "response_type": "consent_offer",
                "level": level,
                "guidance": self.consent_manager.get_consent_message(level),
                "intervention": "consent_required",
            }
        return {
            "response_type": "neutral",
            "guidance": "Provide task-focused support",
            "intervention": "none",
        }

    def requires_rrta_handoff(self, user_state: EmotionalState) -> bool:
        """Mirror of TS ``requiresRrtaHandoff``."""
        return (
            user_state.explicit_suicidal_ideation
            or user_state.self_harm_indicators
            or user_state.inability_to_ensure_safety
        )

    def _swp_active(self) -> bool:
        """Mirror of the TS ``this.userToi.swp?.active !== false`` guard."""
        swp = self.user_toi.get("swp")
        if not isinstance(swp, dict):
            return True
        return swp.get("active") is not False


# Alias for convenience — mirror of TS ``export const SWP = SleepwalkerProtocol``.
SWP = SleepwalkerProtocol
