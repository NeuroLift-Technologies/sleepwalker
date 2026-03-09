"""
Temporal Continuity Management Module

Maintains emotional state and boundary awareness across sessions.
"""

from typing import Dict, Any, Optional
import json
import os
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
        user_file = self.storage_path / f"{user_id}.json"
        
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
        user_file = self.storage_path / f"{user_id}.json"
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
        user_file = self.storage_path / f"{user_id}.json"
        
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
