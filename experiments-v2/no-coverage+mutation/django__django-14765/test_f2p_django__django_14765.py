from django.db.migrations.state import ProjectState
from django.test import TestCase


class ProjectStateRealAppsTest(TestCase):
    def test_project_state_rejects_non_set_real_apps(self):
        """
        Test that ProjectState.__init__ rejects non-set real_apps values.
        This behavior was introduced by the fix where real_apps is assumed to be a set.
        """
        # These should raise AssertionError because real_apps must be a set when not None
        # (This test verifies the NEW behavior)
        with self.assertRaises(AssertionError):
            ProjectState(real_apps=[1, 2, 3])  # list should not be accepted
            
        with self.assertRaises(AssertionError):
            ProjectState(real_apps=(1, 2, 3))  # tuple should not be accepted
    
    def test_project_state_accepts_set_real_apps(self):
        """
        Test that ProjectState.__init__ accepts set as real_apps argument.
        This should work in both old and new code.
        """
        # This should work in both old and new code
        state = ProjectState(real_apps={1, 2, 3})
        self.assertEqual(state.real_apps, {1, 2, 3})
    
    def test_project_state_accepts_none_real_apps(self):
        """
        Test that ProjectState.__init__ accepts None as real_apps argument.
        This should work in both old and new code.
        """
        # This should work in both old and new code
        state = ProjectState(real_apps=None)
        self.assertEqual(state.real_apps, set())