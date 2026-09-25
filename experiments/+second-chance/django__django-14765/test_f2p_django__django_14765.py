"""
Regression test for Django issue #14765.
ProjectState.__init__() should assert that real_apps is a set when provided.
"""
from django.db.migrations.state import ProjectState


def test_project_state_requires_set():
    """Test strict enforcement of real_apps being set type."""
    
    # Real_apps=None should work (unchanged behavior)
    state = ProjectState(real_apps=None)
    assert state.real_apps == set()
    
    # Real_apps=set should work (unchanged behavior) 
    state = ProjectState(real_apps={1, 2, 3})
    assert state.real_apps == {1, 2, 3}
    
    # Real_apps=list should fail with AssertionError (new strict behavior)
    try:
        ProjectState(real_apps=[1, 2, 3])
        assert False, "AssertionError expected for list input"
    except AssertionError:
        pass
    
    # Real_apps=tuple should fail with AssertionError (new strict behavior)
    try:
        ProjectState(real_apps=(1, 2, 3))
        assert False, "AssertionError expected for tuple input"  
    except AssertionError:
        pass
    
    # Real_apps=str should fail with AssertionError (new strict behavior)
    try:
        ProjectState(real_apps="abc")
        assert False, "AssertionError expected for string input"
    except AssertionError:
        pass