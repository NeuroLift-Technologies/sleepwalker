"""``sleepwalker_protocol`` — Python port of
``@neurolift-technologies/sleepwalker-protocol``.

Emotional Continuity Governance for AI Systems. The TypeScript package is the
source of truth; this port mirrors its public API in snake_case and reproduces
the same detection patterns, consent model, continuity store format, and TOI
loading behavior.

.. warning::

   PROTOTYPE — NOT A SAFETY SYSTEM. This is experimental crisis-detection code
   with stubbed intervention layers. It is NOT medical advice, NOT a crisis
   service, and performs no real-time monitoring; it can miss real crisis
   signals. Do not rely on it as a safety net. In the US call or text 988; in an
   emergency call 911.

Public API (mirror of ``src/index.ts``)::

    from sleepwalker_protocol import (
        SleepwalkerProtocol, SWP,
        EmotionalState, StateDetector,
        ConsentLevel, ConsentManager,
        ContinuityManager,
        TOILoader,
    )
"""
from __future__ import annotations

from .consent import ConsentLevel, ConsentManager
from .continuity import ContinuityManager
from .protocol import SWP, SleepwalkerProtocol
from .state_detection import EmotionalState, StateDetector
from .toi_loader import TOILoader

__version__ = "1.0.1"
__author__ = "NeuroLift Technologies / HAIEF"
__license__ = "Apache-2.0"

__all__ = [
    # protocol
    "SleepwalkerProtocol",
    "SWP",
    # state detection
    "EmotionalState",
    "StateDetector",
    # consent
    "ConsentLevel",
    "ConsentManager",
    # continuity
    "ContinuityManager",
    # toi loading
    "TOILoader",
    "__version__",
]
