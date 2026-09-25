"""
Regression test for Django 11477: translate_url() creates an incorrect URL when 
optional named groups are missing in the URL pattern.

This ensures the fix in django/urls/resolvers.py properly filters out None 
values from kwargs when dealing with optional named groups in URL patterns.
"""

from django.test import SimpleTestCase
from django.urls.resolvers import RegexPattern


class TestOptionalGroupsFiltering(SimpleTestCase):
    
    def test_optional_named_groups_none_values_filtered(self):
        """
        Verify that optional named groups result in filtered kwargs.
        
        Before fix: kwargs = {'year': '2023', 'month': None}
        After fix:  kwargs = {'year': '2023'}
        
        The key difference is that 'month' should not be a key in kwargs
        when it has a None value, because that None value should be filtered out.
        """
        # Pattern with required year and optional month group
        pattern = RegexPattern(r'(?P<year>\d{4})/(?P<month>\d{2})?/?$')
        path = '/2023/'
        
        result = pattern.match(path)
        self.assertIsNotNone(result)
        remaining_path, args, kwargs = result
        
        # For clearly observable behavior difference:
        # - If the fix is NOT applied, 'month' key will exist with None value
        # - If the fix IS applied, 'month' key will NOT exist at all
        self.assertIn('year', kwargs)
        self.assertEqual(kwargs['year'], '2023')
        
        # Key test - after the fix, the None values should be filtered out 
        # from kwargs dictionary
        if 'month' in kwargs:
            # Bug still present: None values are kept rather than filtered
            self.assertIsNone(kwargs['month'])
            # This assertion fails when fixed version is active
            self.fail("BUG: None values from optional named groups should be filtered out")
        
        # If we happen to reach here, the fix is in effect - 'month' key not present
        # This is the desired behavior after the change


class TestSpecificBugCondition(SimpleTestCase):
    """
    Test the precise condition that demonstrates the bug.
    
    Based on Django ticket 11477: the issue was with translate_url() using 
    incorrect URLs when optional named groups were missing.
    """
    
    def test_no_none_in_filtered_kwargs(self):
        """
        Simply verify that after fix, no None values appear in filtered kwargs.
        """
        pattern = RegexPattern(r'(?P<year>\d{4})/(?P<month>\d{2})?/?$')
        path = '/2023/'
        
        result = pattern.match(path)
        self.assertIsNotNone(result)
        remaining_path, args, kwargs = result
        
        # Critical: ensure no keys in kwargs have None as values
        # This enforces the core invariant of the fix
        for key, value in kwargs.items():
            self.assertIsNotNone(value, 
                f"Optional named group '{key}' resulted in None value - should be filtered out")