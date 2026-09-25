from django.db.migrations.state import ProjectState


def test_project_state_set_real_apps():
    """Test that ProjectState accepts sets as real_apps."""
    project_state = ProjectState(real_apps={'app1', 'app2'})
    assert isinstance(project_state.real_apps, set)
    assert project_state.real_apps == {'app1', 'app2'}


def test_project_state_none_real_apps():
    """Test that ProjectState accepts None as real_apps."""
    project_state = ProjectState(real_apps=None)
    assert isinstance(project_state.real_apps, set)
    assert project_state.real_apps == set()


def test_project_state_empty_set_real_apps():
    """Test that ProjectState accepts empty sets as real_apps."""
    project_state = ProjectState(real_apps=set())
    assert isinstance(project_state.real_apps, set)
    assert project_state.real_apps == set()