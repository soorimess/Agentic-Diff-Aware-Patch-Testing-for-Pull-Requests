"""
Test for ProjectState.__init__ behavior change in PR #14760.
Before fix: real_apps can be iterables that are converted to sets
After fix: real_apps must be a set or None, AssertionError if not
"""

def test_project_state_accepts_list():
    """This test demonstrates the behavior before the fix - should pass with old code"""
    from django.db.migrations.state import ProjectState
    
    # This should work before the fix (list gets converted to set)
    # But should fail after the fix (AssertionError)
    state = ProjectState(real_apps=['app1', 'app2'])
    assert isinstance(state.real_apps, set)
    assert state.real_apps == {'app1', 'app2'}

def test_project_state_accepts_set():
    """This should work in both versions"""
    from django.db.migrations.state import ProjectState
    
    state = ProjectState(real_apps={'app1', 'app2'})
    assert isinstance(state.real_apps, set) 
    assert state.real_apps == {'app1', 'app2'}

def test_project_state_accepts_none():
    """This should work in both versions"""
    from django.db.migrations.state import ProjectState
    
    state = ProjectState(real_apps=None)
    assert state.real_apps == set()