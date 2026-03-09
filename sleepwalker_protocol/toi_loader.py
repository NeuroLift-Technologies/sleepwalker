"""
TOI (Terms of Interaction) Loader Module

Loads and parses user's Terms of Interaction configuration.
"""

from typing import Dict, Any, Optional
import yaml
import json
from pathlib import Path


class TOILoader:
    """
    Loads user's Terms of Interaction (TOI) configuration.
    
    Supports YAML and JSON formats for TOI files.
    """
    
    def __init__(self, toi_path: Optional[str] = None):
        """
        Initialize TOI loader with path to TOI file.
        
        Args:
            toi_path: Path to user's TOI file (YAML or JSON)
        """
        self.toi_path = Path(toi_path) if toi_path else None
    
    def load(self) -> Dict[str, Any]:
        """
        Load and parse TOI file.
        
        Returns:
            Dictionary containing TOI configuration
        """
        if not self.toi_path or not self.toi_path.exists():
            return self._get_default_toi()
        
        # Determine format from extension
        if self.toi_path.suffix in ['.yaml', '.yml']:
            return self._load_yaml()
        elif self.toi_path.suffix == '.json':
            return self._load_json()
        else:
            # Try YAML first, then JSON
            try:
                return self._load_yaml()
            except:
                try:
                    return self._load_json()
                except:
                    return self._get_default_toi()
    
    def _load_yaml(self) -> Dict[str, Any]:
        """Load TOI from YAML file."""
        try:
            with open(self.toi_path, 'r') as f:
                return yaml.safe_load(f) or {}
        except (yaml.YAMLError, IOError):
            return self._get_default_toi()
    
    def _load_json(self) -> Dict[str, Any]:
        """Load TOI from JSON file."""
        try:
            with open(self.toi_path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return self._get_default_toi()
    
    def _get_default_toi(self) -> Dict[str, Any]:
        """
        Get default TOI configuration.
        
        Returns:
            Default TOI with SWP active and conservative settings
        """
        return {
            'swp': {
                'active': True,
                'intervention_threshold': 'user_initiated_only',
                'processing_consent': False,
                'protected_topics': []
            }
        }
