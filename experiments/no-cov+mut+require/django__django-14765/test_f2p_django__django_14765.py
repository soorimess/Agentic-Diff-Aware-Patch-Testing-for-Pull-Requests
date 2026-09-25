"""
Regression test for Django pull request #14760
Test that ProjectState.__init__ validates that real_apps is a set when not None.
"""
from django.db.migrations.state import ProjectState
from django.test import SimpleTestCase


class ProjectStateRealAppsTests(SimpleTestCase):
    def test_project_state_real_apps_none(self):
        """Test that real_apps=None works."""
        state = ProjectState(real_apps=None)
        self.assertEqual(state.real_apps, set())

    def test_project_state_real_apps_empty_set(self):
        """Test that real_apps=set() works."""
        state = ProjectState(real_apps=set())
        self.assertEqual(state.real_apps, set())

    def test_project_state_real_apps_set(self):
        """Test that real_apps with a set works."""
        state = ProjectState(real_apps={'app1', 'app2'})
        self.assertEqual(state.real_apps, {'app1', 'app2'})

    def test_project_state_real_apps_list_raises_assertion_error(self):
        """Test that real_apps with a list raises AssertionError."""
        # Before fix: would work (converted to set)
        # After fix: should raise AssertionError  
        with self.assertRaises(AssertionError):
            ProjectState(real_apps=['app1', 'app2'])

    def test_project_state_real_apps_tuple_raises_assertion_error(self):
        """Test that real_apps with a tuple raises AssertionError."""
        # Before fix: would work (converted to set) 
        # After fix: should raise AssertionError
        with self.assertRaises(AssertionError):
            ProjectState(real_apps=('app1', 'app2'))