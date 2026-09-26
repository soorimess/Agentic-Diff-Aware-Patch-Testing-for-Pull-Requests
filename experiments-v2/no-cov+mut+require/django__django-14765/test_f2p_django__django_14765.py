from django.db.migrations.state import ProjectState
from django.test import TestCase


class ProjectStateRealAppsTest(TestCase):
    """Test that ProjectState.__init__() properly handles real_apps argument."""

    def test_project_state_with_list_real_apps_raises_assertion_error(self):
        """
        Test that ProjectState.__init__() raises AssertionError when real_apps
        is passed as a list (non-set) after the fix.
        """
        # This should raise AssertionError in the new code
        # but work in the old code (converts list to set)
        with self.assertRaises(AssertionError):
            ProjectState(real_apps=['app1', 'app2'])

    def test_project_state_with_set_real_apps_works(self):
        """
        Test that ProjectState.__init__() works correctly when real_apps
        is passed as a set.
        """
        # This should work in both old and new code
        state = ProjectState(real_apps={'app1', 'app2'})
        self.assertEqual(state.real_apps, {'app1', 'app2'})

    def test_project_state_with_none_real_apps_works(self):
        """
        Test that ProjectState.__init__() works correctly when real_apps
        is passed as None.
        """
        # This should work in both old and new code
        state = ProjectState(real_apps=None)
        self.assertEqual(state.real_apps, set())