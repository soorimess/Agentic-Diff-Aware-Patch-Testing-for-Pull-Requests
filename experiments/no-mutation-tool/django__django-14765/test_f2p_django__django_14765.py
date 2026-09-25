"""
Regression test for Django PR #14760 that changed ProjectState.__init__() 
to assume real_apps argument is a set.
"""

from django.db.migrations.state import ProjectState
from django.test import TestCase


class ProjectStateRealAppsTest(TestCase):
    """
    Test that ProjectState.__init__() correctly assumes real_apps is a set.
    """
    
    def test_project_state_real_apps_none(self):
        """Test that real_apps=None works correctly."""
        state = ProjectState(real_apps=None)
        self.assertEqual(state.real_apps, set())

    def test_project_state_real_apps_set(self):
        """Test that real_apps as a set works correctly."""
        state = ProjectState(real_apps=set(['app1', 'app2']))
        self.assertEqual(state.real_apps, {'app1', 'app2'})

    def test_project_state_real_apps_list_raises_assertion_error(self):
        """Test that real_apps as a list raises AssertionError."""
        # This should raise AssertionError in new code
        with self.assertRaises(AssertionError):
            ProjectState(real_apps=['app1', 'app2'])

    def test_project_state_real_apps_tuple_raises_assertion_error(self):
        """Test that real_apps as a tuple raises AssertionError."""
        # This should raise AssertionError in new code
        with self.assertRaises(AssertionError):
            ProjectState(real_apps=('app1', 'app2'))