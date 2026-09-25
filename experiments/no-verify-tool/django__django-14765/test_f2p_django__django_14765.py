"""
Regression test for Django issue #14765.

Ensures ProjectState.__init__() strictly requires real_apps to be a set or None 
after the change in PR #14760.
"""

from django.db.migrations.state import ProjectState
from django.test import SimpleTestCase


class TestProjectStateRealApps(SimpleTestCase):
    """Test that ProjectState only accepts sets or None for real_apps parameter."""
    
    def test_empty_list_raises_assertion_error(self):
        """Test that passing an empty list to real_apps raises AssertionError."""
        # Before fix: would work (convert list to set)  
        # After fix: raises AssertionError (strict validation)
        with self.assertRaises(AssertionError):
            ProjectState(models={}, real_apps=[])
            
    def test_empty_set_works(self):
        """Test that passing an empty set to real_apps works."""
        state = ProjectState(models={}, real_apps=set())
        self.assertEqual(state.real_apps, set())
        
    def test_none_works(self):
        """Test that passing None to real_apps works."""
        state = ProjectState(models={}, real_apps=None)
        self.assertEqual(state.real_apps, set())
        
    def test_non_empty_set_works(self):
        """Test that passing a non-empty set to real_apps works."""
        state = ProjectState(models={}, real_apps={'app1', 'app2'})
        self.assertEqual(state.real_apps, {'app1', 'app2'})