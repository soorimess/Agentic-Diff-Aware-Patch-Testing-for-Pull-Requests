from django.db.migrations.state import ProjectState
from django.test import SimpleTestCase


class ProjectStateRealAppsTest(SimpleTestCase):
    """
    Tests for ProjectState.__init__() real_apps parameter behavior.
    
    Before PR #14760, ProjectState.__init__() would accept any iterable and 
    convert it to a set. After the PR, it only accepts a set directly.
    """
    
    def test_project_state_accepts_set(self):
        """Test that ProjectState.__init__() accepts sets (should work in both versions)"""
        # This should work in both old and new versions
        state = ProjectState(real_apps={"app1", "app2"})
        self.assertEqual(state.real_apps, {"app1", "app2"})

    def test_project_state_rejects_non_set_iterable_after_fix(self):
        """Test that ProjectState.__init__() rejects non-set iterables after the fix"""
        # This should fail in the fixed version with AssertionError
        with self.assertRaises(AssertionError):
            ProjectState(real_apps=["app1", "app2"])

    def test_project_state_rejects_none(self):
        """Test that ProjectState.__init__() handles None correctly"""
        # This should work in both old and new versions
        state = ProjectState(real_apps=None)
        self.assertEqual(state.real_apps, set())
        
    def test_project_state_rejects_tuple(self):
        """Test that ProjectState.__init__() rejects tuples with assertion error"""
        # This should raise AssertionError in the fixed version
        with self.assertRaises(AssertionError):
            ProjectState(real_apps=("app1", "app2"))
            
    def test_project_state_rejects_other_iterables(self):
        """Test that ProjectState.__init__() rejects other iterables with assertion error"""
        # This should raise AssertionError in the fixed version
        with self.assertRaises(AssertionError):
            ProjectState(real_apps=iter(["app1", "app2"]))