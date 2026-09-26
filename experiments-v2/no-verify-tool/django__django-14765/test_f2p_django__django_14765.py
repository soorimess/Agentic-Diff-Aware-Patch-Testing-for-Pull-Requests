from django.db.migrations.state import ProjectState
from django.test import TestCase


class ProjectStateRealAppsTest(TestCase):
    """Test that ProjectState.__init__ works correctly with real_apps parameter."""
    
    def test_project_state_with_set_real_apps(self):
        """Test that ProjectState.__init__ works with real_apps as a set."""
        project_state = ProjectState(real_apps={'app1', 'app2'})
        self.assertEqual(project_state.real_apps, {'app1', 'app2'})
        
    def test_project_state_with_none_real_apps(self):
        """Test that ProjectState.__init__ works with real_apps as None."""
        project_state = ProjectState(real_apps=None)
        self.assertEqual(project_state.real_apps, set())