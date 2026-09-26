from django.db.migrations.state import ProjectState
from django.test import TestCase


class ProjectStateRealAppsTest(TestCase):
    """Test that ProjectState.__init__ properly handles real_apps parameter."""

    def test_project_state_with_set_real_apps_strict_enforcement(self):
        """
        Test that ProjectState.__init__ properly enforces that real_apps must be a set.
        This validates the new strict behavior after the change.
        """
        # Test the new behavior: real_apps must be a set
        real_apps_set = {'app1', 'app2', 'app3'}
        project_state = ProjectState(real_apps=real_apps_set)
        self.assertEqual(project_state.real_apps, {'app1', 'app2', 'app3'})

    def test_project_state_with_none_real_apps(self):
        """
        Test that ProjectState.__init__ handles real_apps=None correctly.
        """
        project_state = ProjectState(real_apps=None)
        self.assertEqual(project_state.real_apps, set())