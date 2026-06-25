"""Emotional State Detection Module.

Detects protective psychological states without intervention.

Faithful Python port of ``src/stateDetection.ts`` from
``@neurolift-technologies/sleepwalker-protocol`` — the TypeScript reference is the
source of truth. Pattern set, ``state_type`` precedence, the fixed ``0.7``
confidence for protective states, and the crisis flag mapping all mirror the TS
``StateDetector`` exactly.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Pattern


@dataclass
class EmotionalState:
    """Detected emotional state indicators (mirror of the TS ``EmotionalState``).

    Field names are the snake_case equivalents of the TS interface:

    ===========================  ================================
    TypeScript                   Python
    ===========================  ================================
    ``stateType``                ``state_type``
    ``protective``               ``protective``
    ``requiresCheckIn``          ``requires_check_in``
    ``indicators``               ``indicators``
    ``confidence``               ``confidence``
    ``explicitSuicidalIdeation`` ``explicit_suicidal_ideation``
    ``selfHarmIndicators``       ``self_harm_indicators``
    ``inabilityToEnsureSafety``  ``inability_to_ensure_safety``
    ===========================  ================================

    ``indicators`` mirrors the nested TS object::

        {
            "dissociation": bool,
            "numbing": bool,
            "avoidance": bool,
            "detachment": bool,
            "crisis": {
                "suicidal_ideation": bool,
                "self_harm": bool,
                "safety_concern": bool,
            },
        }
    """

    state_type: str
    protective: bool
    requires_check_in: bool
    indicators: Dict[str, Any]
    confidence: float
    explicit_suicidal_ideation: bool
    self_harm_indicators: bool
    inability_to_ensure_safety: bool


class StateDetector:
    """Detects emotional states from user input.

    Mirrors the TS ``StateDetector``: the same regular expressions, evaluated
    case-insensitively (the TS patterns carry the ``/i`` flag), with the same
    precedence when choosing the primary ``state_type``.
    """

    def __init__(self) -> None:
        self.dissociation_patterns: List[Pattern[str]] = []
        self.numbing_patterns: List[Pattern[str]] = []
        self.avoidance_patterns: List[Pattern[str]] = []
        self.detachment_patterns: List[Pattern[str]] = []
        self.crisis_patterns: Dict[str, List[Pattern[str]]] = {
            "suicidal_ideation": [],
            "self_harm": [],
            "safety_concern": [],
        }
        self._initialize_patterns()

    def _initialize_patterns(self) -> None:
        # Each pattern mirrors a TS RegExp literal with the /i flag.
        self.dissociation_patterns = [
            re.compile(r"\bnumb\b", re.IGNORECASE),
            re.compile(r"\bdetached\b", re.IGNORECASE),
            re.compile(r"\bdisconnected\b", re.IGNORECASE),
            re.compile(r"\bnot really here\b", re.IGNORECASE),
            re.compile(r"\bfeeling nothing\b", re.IGNORECASE),
            re.compile(r"\bspaced out\b", re.IGNORECASE),
        ]

        self.numbing_patterns = [
            re.compile(r"\bdon't feel (much|anything)\b", re.IGNORECASE),
            re.compile(r"\bemotionally flat\b", re.IGNORECASE),
            re.compile(r"\bcan't feel\b", re.IGNORECASE),
        ]

        self.avoidance_patterns = [
            re.compile(r"\bnot ready to (talk|discuss|think)\b", re.IGNORECASE),
            re.compile(r"\bcan't (talk|think|discuss) (about|this)\b", re.IGNORECASE),
            re.compile(r"\bavoid(ing)?\b", re.IGNORECASE),
        ]

        self.detachment_patterns = [
            re.compile(r"\bjust fine\b", re.IGNORECASE),
            re.compile(r"\bi'm fine\b", re.IGNORECASE),
            re.compile(r"\bit's whatever\b", re.IGNORECASE),
            re.compile(r"\bdoesn't matter\b", re.IGNORECASE),
        ]

        self.crisis_patterns = {
            "suicidal_ideation": [
                re.compile(r"\bsuicide\b", re.IGNORECASE),
                re.compile(r"\bkill myself\b", re.IGNORECASE),
            ],
            "self_harm": [
                re.compile(r"\bhurt(ing)? myself\b", re.IGNORECASE),
                re.compile(r"\bself(-| )harm\b", re.IGNORECASE),
            ],
            "safety_concern": [
                re.compile(r"\bnot safe\b", re.IGNORECASE),
                re.compile(r"\bdon't feel safe\b", re.IGNORECASE),
            ],
        }

    def detect(
        self, user_input: str, session_history: Optional[List[Any]] = None
    ) -> EmotionalState:
        """Detect the emotional state of ``user_input``.

        ``session_history`` mirrors the TS parameter (defaulting to ``[]``); it is
        accepted for API parity but not consulted, exactly as in the TS source.
        """
        if session_history is None:
            session_history = []

        dissociation = self._check_patterns(user_input, self.dissociation_patterns)
        numbing = self._check_patterns(user_input, self.numbing_patterns)
        avoidance = self._check_patterns(user_input, self.avoidance_patterns)
        detachment = self._check_patterns(user_input, self.detachment_patterns)

        crisis = {
            "suicidal_ideation": self._check_patterns(
                user_input, self.crisis_patterns["suicidal_ideation"]
            ),
            "self_harm": self._check_patterns(
                user_input, self.crisis_patterns["self_harm"]
            ),
            "safety_concern": self._check_patterns(
                user_input, self.crisis_patterns["safety_concern"]
            ),
        }

        protective = dissociation or numbing or avoidance or detachment
        requires_check_in = (
            crisis["suicidal_ideation"]
            or crisis["self_harm"]
            or crisis["safety_concern"]
        )

        state_type = "neutral"
        if dissociation:
            state_type = "dissociation"
        elif numbing:
            state_type = "numbing"
        elif avoidance:
            state_type = "avoidance"
        elif detachment:
            state_type = "detachment"

        confidence = 0.7 if protective else 0.0

        return EmotionalState(
            state_type=state_type,
            protective=protective,
            requires_check_in=requires_check_in,
            indicators={
                "dissociation": dissociation,
                "numbing": numbing,
                "avoidance": avoidance,
                "detachment": detachment,
                "crisis": crisis,
            },
            confidence=confidence,
            explicit_suicidal_ideation=crisis["suicidal_ideation"],
            self_harm_indicators=crisis["self_harm"],
            inability_to_ensure_safety=crisis["safety_concern"],
        )

    @staticmethod
    def _check_patterns(text: str, patterns: List[Pattern[str]]) -> bool:
        return any(pattern.search(text) for pattern in patterns)
