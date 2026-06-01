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


def test_user_id_path_traversal_is_contained(temp_storage):
    """A malicious user_id must not escape the storage directory."""
    manager = ContinuityManager(storage_path=temp_storage)

    malicious_id = "../../etc/passwd"
    manager.save_session(malicious_id, {'emotional_state': 'neutral'})

    storage_root = Path(temp_storage).resolve()

    # No file (or directory) was created outside the storage root.
    for created in storage_root.rglob('*'):
        assert storage_root in created.resolve().parents or created.resolve() == storage_root
    assert not (storage_root.parent / 'etc' / 'passwd').exists()

    # The sanitized id still round-trips: read uses the same sanitization.
    context = manager.get_context(malicious_id)
    assert context['has_history'] is True

    # Everything written stays directly inside the storage root.
    json_files = list(storage_root.glob('*.json'))
    assert len(json_files) == 1
    assert json_files[0].parent == storage_root


def test_distinct_user_ids_do_not_collide(temp_storage):
    """Ids that sanitize to the same slug must not share a storage file.

    Regression guard: keying on a stripped slug alone would map distinct users
    onto one file, letting one user's continuity overwrite or be returned for
    another. The storage key hashes the full id, so these stay separate.
    """
    manager = ContinuityManager(storage_path=temp_storage)

    # Same stripped characters, different real ids.
    manager.save_session("a/b", {'emotional_state': 'numbing'})
    manager.save_session("ab", {'emotional_state': 'neutral'})
    assert manager.get_context("a/b")['last_session_state'] == 'numbing'
    assert manager.get_context("ab")['last_session_state'] == 'neutral'

    # Two different emails that strip to identical characters stay separate.
    manager.save_session("alice@example.com", {'emotional_state': 'avoidance'})
    manager.save_session("aliceexample.com", {'emotional_state': 'dissociation'})
    assert manager.get_context("alice@example.com")['last_session_state'] == 'avoidance'
    assert manager.get_context("aliceexample.com")['last_session_state'] == 'dissociation'

    # Four ids -> four distinct files.
    assert len(list(Path(temp_storage).glob('*.json'))) == 4


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
