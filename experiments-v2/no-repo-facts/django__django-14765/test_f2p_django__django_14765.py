from django.test import SimpleTestCase
from django.db.migrations.state import ProjectState


class ProjectStateRealAppsTypeTests(SimpleTestCase):
    """Tests for ProjectState real_apps parameter type handling."""

    def test_projectstate_real_apps_none(self):
        """Test that real_apps=None creates empty set."""
        project_state = ProjectState(real_apps=None)
        self.assertEqual(project_state.real_apps, set())

    def test_projectstate_real_apps_set(self):
        """Test that real_apps as a set works correctly."""
        project_state = ProjectState(real_apps={'app1', 'app2'})
        self.assertEqual(project_state.real_apps, {'app1', 'app2'})

    def test_projectstate_real_apps_list_raises_assertion_error(self):
        """Test that real_apps as a list raises AssertionError (the bug)."""
        # This should raise AssertionError with the new code but worked with old code
        with self.assertRaises(AssertionError):
            ProjectState(real_apps=['app1', 'app2'])