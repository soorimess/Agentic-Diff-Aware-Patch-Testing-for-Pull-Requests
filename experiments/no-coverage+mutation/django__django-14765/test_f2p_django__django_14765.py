"""
Regression test for Django PR #14760 that made ProjectState.__init__() assume real_apps argument is a set.
"""

from django.test import TestCase
from django.db.migrations.state import ProjectState


class ProjectStateRealAppsTests(TestCase):
    def test_project_state_real_apps_list_raises_assertion_error(self):
        """
        Test that ProjectState.__init__ raises AssertionError when real_apps is a list
        instead of a set, as required after the PR.
        """
        # This should work in the old code but fail in the new code
        with self.assertRaises(AssertionError):
            ProjectState(models={}, real_apps=[1, 2, 3])

    def test_project_state_real_apps_tuple_raises_assertion_error(self):
        """
        Test that ProjectState.__init__ raises AssertionError when real_apps is a tuple
        instead of a set, as required after the PR.
        """
        # This should work in the old code but fail in the new code  
        with self.assertRaises(AssertionError):
            ProjectState(models={}, real_apps=(1, 2, 3))

    def test_project_state_real_apps_set_works(self):
        """
        Test that ProjectState.__init__ works correctly when real_apps is already a set.
        """
        # This should work in both old and new code
        project_state = ProjectState(models={}, real_apps={1, 2, 3})
        self.assertEqual(project_state.real_apps, {1, 2, 3})

    def test_project_state_real_apps_none_works(self):
        """
        Test that ProjectState.__init__ works correctly when real_apps is None.
        """
        # This should work in both old and new code
        project_state = ProjectState(models={}, real_apps=None)
        self.assertEqual(project_state.real_apps, set())