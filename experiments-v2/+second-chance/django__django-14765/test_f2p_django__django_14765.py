from django.db.migrations.state import ProjectState
from django.test import TestCase


class ProjectStateRealAppsTest(TestCase):
    """Test that ProjectState.__init__ properly handles real_apps parameter."""

    def test_project_state_with_list_real_apps_raises_assertion_error(self):
        """
        Test that ProjectState.__init__ raises AssertionError when real_apps is a list.
        
        This test verifies the fix in PR #14760 where ProjectState.__init__ now
        assumes real_apps is a set when non-None, rather than converting iterables.
        """
        # With the new code, lists should raise AssertionError
        real_apps = ['app1', 'app2', 'app3']
        
        # This should raise AssertionError with the new code
        with self.assertRaises(AssertionError):
            ProjectState(real_apps=real_apps)

    def test_project_state_with_set_real_apps_works(self):
        """
        Test that ProjectState.__init__ works correctly with set real_apps.
        """
        real_apps = {'app1', 'app2', 'app3'}
        state = ProjectState(real_apps=real_apps)
        self.assertEqual(state.real_apps, real_apps)

    def test_project_state_with_none_real_apps_works(self):
        """
        Test that ProjectState.__init__ works correctly with None real_apps.
        """
        state = ProjectState(real_apps=None)
        self.assertEqual(state.real_apps, set())

    def test_project_state_with_empty_list_real_apps_raises_assertion_error(self):
        """
        Test that ProjectState.__init__ raises AssertionError when real_apps is an empty list.
        """
        # With the new code, empty lists should also raise AssertionError
        real_apps = []
        
        # This should raise AssertionError with the new code
        with self.assertRaises(AssertionError):
            ProjectState(real_apps=real_apps)

    def test_project_state_with_tuple_real_apps_raises_assertion_error(self):
        """
        Test that ProjectState.__init__ raises AssertionError when real_apps is a tuple.
        
        This is another case that should raise AssertionError with the new code.
        """
        # With the new code, tuples should also raise AssertionError
        real_apps = ('app1', 'app2', 'app3')
        
        # This should raise AssertionError with the new code
        with self.assertRaises(AssertionError):
            ProjectState(real_apps=real_apps)