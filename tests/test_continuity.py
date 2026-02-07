"""
Tests for Temporal Continuity Module
"""

import pytest
import tempfile
import shutil
from pathlib import Path
from sleepwalker_protocol.continuity import ContinuityManager


@pytest.fixture
def temp_storage():
    """Create temporary storage directory for tests."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)


def test_continuity_manager_initialization(temp_storage):
    """Test ContinuityManager initialization."""
    manager = ContinuityManager(storage_path=temp_storage)
    assert manager is not None
    assert Path(temp_storage).exists()


def test_save_and_retrieve_session(temp_storage):
    """Test saving and retrieving session data."""
    manager = ContinuityManager(storage_path=temp_storage)
    
    user_id = "test_user_123"
    session_data = {
        'emotional_state': 'dissociation',
        'protective_state_active': True,
        'declared_boundaries': ['topic1', 'topic2']
    }
    
    # Save session
    manager.save_session(user_id, session_data)
    
    # Retrieve context
    context = manager.get_context(user_id)
    
    assert context['has_history'] == True
    assert context['last_session_state'] == 'dissociation'
    assert context['protective_state_active'] == True
    assert 'topic1' in context['declared_boundaries']


def test_multiple_sessions(temp_storage):
    """Test multiple sessions for same user."""
    manager = ContinuityManager(storage_path=temp_storage)
    
    user_id = "test_user_456"
    
    # First session
    manager.save_session(user_id, {'emotional_state': 'neutral'})
    
    # Second session
    manager.save_session(user_id, {'emotional_state': 'numbing'})
    
    # Third session
    manager.save_session(user_id, {'emotional_state': 'avoidance'})
    
    # Check session count
    context = manager.get_context(user_id)
    assert context['session_count'] == 3
    assert context['last_session_state'] == 'avoidance'


def test_new_user_context(temp_storage):
    """Test context for user with no history."""
    manager = ContinuityManager(storage_path=temp_storage)
    
    context = manager.get_context("new_user_789")
    
    assert context['has_history'] == False
    assert context['protective_state_active'] == False
    assert context['declared_boundaries'] == []


def test_update_boundary(temp_storage):
    """Test updating user boundaries."""
    manager = ContinuityManager(storage_path=temp_storage)
    
    user_id = "test_user_boundary"
    
    # Save initial session
    manager.save_session(user_id, {'emotional_state': 'neutral'})
    
    # Update boundary
    manager.update_boundary(user_id, 'protected_topics', ['trauma', 'relationships'])
    
    # Retrieve and verify
    context = manager.get_context(user_id)
    declared_boundaries = context['declared_boundaries']
    
    assert 'protected_topics' in declared_boundaries
    assert declared_boundaries['protected_topics'] == ['trauma', 'relationships']


def test_retrieve_last_session_state(temp_storage):
    """Test retrieving last session state."""
    manager = ContinuityManager(storage_path=temp_storage)
    
    user_id = "test_user_last_session"
    session_data = {
        'emotional_state': 'detachment',
        'task_context': 'email writing'
    }
    
    manager.save_session(user_id, session_data)
    
    last_state = manager.retrieve_last_session_state(user_id)
    
    assert last_state['emotional_state'] == 'detachment'
    assert last_state['task_context'] == 'email writing'
    assert 'timestamp' in last_state


def test_boundary_persistence(temp_storage):
    """Test that boundaries persist across sessions."""
    manager = ContinuityManager(storage_path=temp_storage)
    
    user_id = "test_user_persist"
    
    # First session with boundaries
    manager.save_session(user_id, {
        'emotional_state': 'neutral',
        'declared_boundaries': {'protected_topics': ['topic_a']}
    })
    
    # Second session without boundaries in session data
    manager.save_session(user_id, {
        'emotional_state': 'numbing'
    })
    
    # Boundaries should still be there
    context = manager.get_context(user_id)
    assert 'protected_topics' in context['declared_boundaries']
