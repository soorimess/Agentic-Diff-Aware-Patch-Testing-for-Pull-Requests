from django.db.migrations.state import ProjectState
from django.test import TestCase


class ProjectStateRealAppsTest(TestCase):
    """Test that ProjectState.__init__ properly handles real_apps parameter."""

    def test_project_state_init_requires_set_for_real_apps(self):
        """
        Test that ProjectState.__init__ raises AssertionError when real_apps is not a set.
        
        This test verifies the behavior change in PR #14760 where ProjectState.__init__()
        now assumes real_apps is a set when non-None, rather than checking and converting.
        """
        # This should work (real_apps is None)
        state1 = ProjectState(real_apps=None)
        self.assertEqual(state1.real_apps, set())
        
        # This should work (real_apps is a set)
        state2 = ProjectState(real_apps={'app1', 'app2'})
        self.assertEqual(state2.real_apps, {'app1', 'app2'})
        
        # This should fail with AssertionError after the fix
        # (real_apps is a list, not a set)
        with self.assertRaises(AssertionError):
            ProjectState(real_apps=['app1', 'app2'])