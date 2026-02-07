"""
Sleepwalker Protocol (SWP)
Emotional Continuity Governance for AI Systems

This package provides tools for implementing the Sleepwalker Protocol,
which governs long-term emotional continuity in human-AI interactions.
"""

__version__ = "0.1.0"
__author__ = "NeuroLift Technologies / HAIEF"
__license__ = "MIT"

from .protocol import SleepwalkerProtocol, SWP
from .state_detection import EmotionalState, StateDetector
from .consent import ConsentManager, ConsentLevel
from .continuity import ContinuityManager

__all__ = [
    'SleepwalkerProtocol',
    'SWP',
    'EmotionalState',
    'StateDetector',
    'ConsentManager',
    'ConsentLevel',
    'ContinuityManager',
]
