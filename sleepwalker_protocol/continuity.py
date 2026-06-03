"""
Temporal Continuity Management Module

Maintains emotional state and boundary awareness across sessions.
"""

from typing import Dict, Any, Optional
import json
import os
import hashlib
from pathlib import Path
from datetime import datetime


class ContinuityManager:
    """
    Manages temporal continuity of emotional states across sessions.
    
    This manager preserves user boundaries and protective states across
    time, ensuring AI doesn't "forget" important emotional context.
    """
    
    def __init__(self, storage_path: str = ".swp_storage"):
        """
        Initialize continuity manager with storage location.

        Args:
            storage_path: Path for storing session continuity data
        """
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(exist_ok=True)

    def _user_file(self, user_id: str) -> Path:
        """
        Resolve the storage file for a user — traversal-safe and collision-safe.

        ``user_id`` becomes part of a filename, which raises two risks:

        * **Path traversal.** A raw value like ``"../../etc/passwd"`` must not
          read or write outside ``storage_path``.
        * **Collisions.** Simply stripping disallowed characters would map
          distinct ids onto the same file (``"a/b"`` and ``"ab"``, or
          ``"alice@example.com"`` and ``"aliceexample.com"``), letting one
          user's continuity overwrite or leak into another's.

        We therefore key the file on a SHA-256 of the *full* id — deterministic,
        collision-resistant, and filesystem-safe (hex only) — prefixed with a
        sanitized, human-readable slug purely for debuggability.

        Args:
            user_id: User identifier

        Returns:
            Path to the user's JSON file, always inside ``storage_path``
        """
        raw = str(user_id)
        slug = "".join(c for c in raw if c.isalnum() or c in "_-")[:32] or "user"
        # Full SHA-256 hex (the filename is the user-isolation boundary; the
        # extra length is free and maximizes separation between users).
        digest = hashlib.sha256(raw.encode("utf-8")).hexdigest()
        return self.storage_path / f"{slug}-{digest}.json"
    
    def save_session(
        self,
        user_id: str,
        session_data: Dict[str, Any]
    ) -> None:
        """
        Save session data for temporal continuity.
        
        Args:
            user_id: User identifier
            session_data: Session data to preserve
        """
        user_file = self._user_file(user_id)

        # Add timestamp
        session_data['timestamp'] = datetime.now().isoformat()
        
        # Load existing data
        existing_data = self._load_user_data(user_id)
        
        # Update with new session data
        existing_data['last_session'] = session_data
        existing_data['session_count'] = existing_data.get('session_count', 0) + 1
        
        # Preserve declared boundaries across sessions
        if 'declared_boundaries' in session_data:
            existing_data['declared_boundaries'] = session_data['declared_boundaries']
        
        # Save updated data
        with open(user_file, 'w') as f:
            json.dump(existing_data, f, indent=2)
    
    def get_context(self, user_id: str) -> Dict[str, Any]:
        """
        Retrieve continuity context for user.
        
        Args:
            user_id: User identifier
            
        Returns:
            Dictionary containing continuity context
        """
        user_data = self._load_user_data(user_id)
        
        if not user_data:
            return {
                'has_history': False,
                'protective_state_active': False,
                'declared_boundaries': []
            }
        
        last_session = user_data.get('last_session', {})
        
        return {
            'has_history': True,
            'last_session_state': last_session.get('emotional_state', 'unknown'),
            'protective_state_active': last_session.get('protective_state_active', False),
            'declared_boundaries': user_data.get('declared_boundaries', []),
            'days_since_last_session': self._calculate_days_since(
                last_session.get('timestamp')
            ),
            'session_count': user_data.get('session_count', 0)
        }
    
    def retrieve_last_session_state(self, user_id: str) -> Dict[str, Any]:
        """
        Retrieve last session state for user.
        
        Args:
            user_id: User identifier
            
        Returns:
            Last session state data
        """
        user_data = self._load_user_data(user_id)
        return user_data.get('last_session', {})
    
    def update_boundary(
        self,
        user_id: str,
        boundary_type: str,
        boundary_value: Any
    ) -> None:
        """
        Update user's declared boundaries.
        
        Args:
            user_id: User identifier
            boundary_type: Type of boundary (e.g., 'protected_topics')
            boundary_value: Value for the boundary
        """
        user_data = self._load_user_data(user_id)
        
        if 'declared_boundaries' not in user_data:
            user_data['declared_boundaries'] = {}
        
        user_data['declared_boundaries'][boundary_type] = boundary_value
        user_data['boundary_updated'] = datetime.now().isoformat()

        # Save updated data
        user_file = self._user_file(user_id)
        with open(user_file, 'w') as f:
            json.dump(user_data, f, indent=2)
    
    def _load_user_data(self, user_id: str) -> Dict[str, Any]:
        """
        Load user data from storage.
        
        Args:
            user_id: User identifier
            
        Returns:
            User data dictionary
        """
        user_file = self._user_file(user_id)

        if not user_file.exists():
            return {}
        
        try:
            with open(user_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    
    def _calculate_days_since(self, timestamp_str: Optional[str]) -> Optional[int]:
        """
        Calculate days since given timestamp.
        
        Args:
            timestamp_str: ISO format timestamp string
            
        Returns:
            Number of days since timestamp, or None if invalid
        """
        if not timestamp_str:
            return None
        
        try:
            timestamp = datetime.fromisoformat(timestamp_str)
            delta = datetime.now() - timestamp
            return delta.days
        except ValueError:
            return None
