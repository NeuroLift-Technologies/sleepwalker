"""
Tests for TOI Loader Module
"""

import pytest
import tempfile
import os
from sleepwalker_protocol.toi_loader import TOILoader


def test_toi_loader_with_no_file():
    """Test TOI loader returns default when no file provided."""
    loader = TOILoader()
    toi = loader.load()
    
    assert 'swp' in toi
    assert toi['swp']['active'] == True
    assert toi['swp']['intervention_threshold'] == 'user_initiated_only'


def test_load_yaml_toi():
    """Test loading TOI from YAML file."""
    yaml_content = """
swp:
  active: true
  protective_state: "managing"
  intervention_preference: "offer_support_without_pressure"
  protected_topics:
    - "trauma"
    - "relationships"
"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write(yaml_content)
        temp_path = f.name
    
    try:
        loader = TOILoader(temp_path)
        toi = loader.load()
        
        assert toi['swp']['active'] == True
        assert toi['swp']['protective_state'] == 'managing'
        assert 'trauma' in toi['swp']['protected_topics']
        assert 'relationships' in toi['swp']['protected_topics']
    finally:
        os.unlink(temp_path)


def test_load_json_toi():
    """Test loading TOI from JSON file."""
    json_content = """{
  "swp": {
    "active": true,
    "protective_state": "processing",
    "protected_topics": ["work", "family"]
  }
}"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        f.write(json_content)
        temp_path = f.name
    
    try:
        loader = TOILoader(temp_path)
        toi = loader.load()
        
        assert toi['swp']['active'] == True
        assert toi['swp']['protective_state'] == 'processing'
        assert 'work' in toi['swp']['protected_topics']
    finally:
        os.unlink(temp_path)


def test_invalid_file_returns_default():
    """Test that invalid file returns default TOI."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write("invalid: yaml: content::: [[[")
        temp_path = f.name
    
    try:
        loader = TOILoader(temp_path)
        toi = loader.load()
        
        # Should return default TOI
        assert 'swp' in toi
        assert toi['swp']['active'] == True
    finally:
        os.unlink(temp_path)


def test_nonexistent_file_returns_default():
    """Test that nonexistent file returns default TOI."""
    loader = TOILoader("/nonexistent/path/to/toi.yaml")
    toi = loader.load()
    
    assert 'swp' in toi
    assert toi['swp']['active'] == True


def test_default_toi_structure():
    """Test structure of default TOI."""
    loader = TOILoader()
    toi = loader._get_default_toi()
    
    assert 'swp' in toi
    assert 'active' in toi['swp']
    assert 'intervention_threshold' in toi['swp']
    assert 'processing_consent' in toi['swp']
    assert 'protected_topics' in toi['swp']
    assert isinstance(toi['swp']['protected_topics'], list)
