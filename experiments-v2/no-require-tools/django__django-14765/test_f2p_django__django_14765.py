from django.db.migrations.state import ProjectState
from django.test import TestCase


class ProjectStateRealAppsTest(TestCase):
    """Test that ProjectState.__init__ properly handles real_apps argument."""

    def test_project_state_with_set_real_apps_works(self):
        """Test that ProjectState.__init__ works with set real_apps."""
        # This should work with both old and new code
        state = ProjectState(real_apps={'app1', 'app2'})
        self.assertEqual(state.real_apps, {'app1', 'app2'})

    def test_project_state_with_none_real_apps_works(self):
        """Test that ProjectState.__init__ works with None real_apps."""
        state = ProjectState(real_apps=None)
        self.assertEqual(state.real_apps, set())

    def test_project_state_with_string_real_apps_raises_assertion_error(self):
        """
        Test that ProjectState.__init__ raises AssertionError when real_apps is a string.
        
        This verifies the new behavior: real_apps must be a set or None.
        """
        # This should raise AssertionError with the new code (which assumes real_apps is a set)
        with self.assertRaises(AssertionError):
            ProjectState(real_apps="invalid_string")

    def test_project_state_with_list_real_apps_raises_assertion_error(self):
        """
        Test that ProjectState.__init__ raises AssertionError when real_apps is a list.
        
        This verifies the new behavior: real_apps must be a set or None.
        """
        # This should raise AssertionError with the new code (which assumes real_apps is a set)
        with self.assertRaises(AssertionError):
            ProjectState(real_apps=['app1', 'app2'])

    def test_project_state_with_tuple_real_apps_raises_assertion_error(self):
        """
        Test that ProjectState.__init__ raises AssertionError when real_apps is a tuple.
        
        This verifies the new behavior: real_apps must be a set or None.
        """
        # This should raise AssertionError with the new code (which assumes real_apps is a set)
        with self.assertRaises(AssertionError):
            ProjectState(real_apps=('app1', 'app2'))