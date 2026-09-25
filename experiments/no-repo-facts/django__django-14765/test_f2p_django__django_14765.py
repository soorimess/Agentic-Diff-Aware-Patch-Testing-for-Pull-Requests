from django.db.migrations.state import ProjectState
from django.test import SimpleTestCase


class ProjectStateRealAppsTest(SimpleTestCase):
    """Test that ProjectState.__init__ correctly handles real_apps parameter."""

    def test_project_state_with_none_real_apps(self):
        """Test that ProjectState works when real_apps is None."""
        state = ProjectState(models={}, real_apps=None)
        self.assertEqual(state.real_apps, set())

    def test_project_state_with_set_real_apps(self):
        """Test that ProjectState works when real_apps is a set."""
        state = ProjectState(models={}, real_apps={'app1', 'app2'})
        self.assertEqual(state.real_apps, {'app1', 'app2'})

    def test_project_state_with_list_real_apps_raises_assertion_error(self):
        """Test that ProjectState raises AssertionError when real_apps is a list."""
        # This will fail with AssertionError in the new code because it's not a set
        # This is the specific bug - passing a list should have been prevented
        # from the beginning since ProjectState.__init__() is an internal API
        with self.assertRaises(AssertionError):
            ProjectState(models={}, real_apps=['app1', 'app2'])