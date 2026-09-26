from django.db.migrations.state import ProjectState
from django.test import TestCase


class ProjectStateRealAppsTest(TestCase):
    """Test that ProjectState.__init__ properly handles real_apps parameter."""

    def test_project_state_with_list_real_apps_raises_assertion_error(self):
        """
        Test that ProjectState.__init__ raises AssertionError when real_apps is a list
        instead of a set, as the fix enforces that real_apps must be a set.
        """
        # This should raise AssertionError after the fix is applied
        # but should work before the fix (when it converts list to set)
        with self.assertRaises(AssertionError):
            ProjectState(real_apps=['app1', 'app2'])

    def test_project_state_with_tuple_real_apps_raises_assertion_error(self):
        """
        Test that ProjectState.__init__ raises AssertionError when real_apps is a tuple
        instead of a set, as the fix enforces that real_apps must be a set.
        """
        # This should raise AssertionError after the fix is applied
        # but should work before the fix (when it converts tuple to set)
        with self.assertRaises(AssertionError):
            ProjectState(real_apps=('app1', 'app2'))

    def test_project_state_with_set_real_apps_works(self):
        """
        Test that ProjectState.__init__ works correctly when real_apps is a set.
        """
        # This should work both before and after the fix
        state = ProjectState(real_apps={'app1', 'app2'})
        self.assertEqual(state.real_apps, {'app1', 'app2'})

    def test_project_state_with_none_real_apps_works(self):
        """
        Test that ProjectState.__init__ works correctly when real_apps is None.
        """
        # This should work both before and after the fix
        state = ProjectState(real_apps=None)
        self.assertEqual(state.real_apps, set())