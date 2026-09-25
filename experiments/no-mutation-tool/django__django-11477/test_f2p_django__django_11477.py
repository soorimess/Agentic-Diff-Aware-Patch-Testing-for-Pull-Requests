"""
Regression test for Django issue with translate_url() and optional named groups.

This test specifically verifies the behavior change in django/urls/resolvers.py:
    kwargs = match.groupdict()  # Old code (wrong behavior)
    kwargs = {k: v for k, v in match.groupdict().items() if v is not None}  # New code (correct behavior)

The issue: When URL patterns have optional named groups that don't match, 
the old code would include None values in kwargs, causing incorrect behavior 
in URL reversal logic.
"""
from django.test import SimpleTestCase
from django.urls.resolvers import RegexPattern


class TranslateUrlOptionalGroupsTest(SimpleTestCase):
    def test_match_filters_none_values_from_optional_groups(self):
        """ 
        Test that RegexPattern.match() filters out None values from optional named groups.
        
        This directly tests the core issue addressed by the fix:
        - Before fix: Optional named groups with None values were included in kwargs
        - After fix: Optional named groups with None values are excluded from kwargs
        
        The fix ensures that kwargs passed to reverse() don't contain None values,
        which could cause URL reversing to behave incorrectly.
        """
        # Pattern with an optional named group that would match with None value
        pattern = RegexPattern(r'^(?:/(?P<lang>[a-z]{2}))?/users/(?P<id>\d+)/$')
        
        # Match path that doesn't match the optional language group  
        path = '/users/123/'  # No language prefix, so lang group won't match and will be None
        
        result = pattern.match(path) 
        self.assertIsNotNone(result)
        
        # Extract components 
        remaining_path, args, kwargs = result
        
        # The critical check: None values should not be in kwargs
        # This is what was wrong in the previous code
        none_keys = [k for k, v in kwargs.items() if v is None]
        self.assertEqual(len(none_keys), 0, 
            f"Found None values in kwargs for keys: {none_keys}. "
            "These should have been filtered out by the fix.")
        
        # Real-world validation - the kwargs should contain only valid values
        self.assertIn('id', kwargs)
        self.assertEqual(kwargs['id'], '123')
        # 'lang' key should NOT be present at all (filtered out by fix)
        self.assertNotIn('lang', kwargs)
        
        # Also validate that args is properly set when no kwargs
        self.assertEqual(args, ())


    def test_pattern_with_multiple_optional_groups(self):
        """Test that patterns with multiple optional groups work correctly.""" 
        # Pattern with multiple optional named groups - some that will match, some won't
        pattern = RegexPattern(r'^(?:/(?P<lang>[a-z]{2}))?(?:/(?P<category>[a-zA-Z]+))?(?:/(?P<id>\d+))?/$')
        
        # Match path with only the last part - others will be None
        path = '/123/'  # Only ID, no language or category
        
        result = pattern.match(path)
        self.assertIsNotNone(result)
        
        remaining_path, args, kwargs = result
        
        # No None values should be present
        none_keys = [k for k, v in kwargs.items() if v is None]
        self.assertEqual(len(none_keys), 0,
            f"Found None values in kwargs for keys: {none_keys}. "
            "These should have been filtered out by the fix.")
        
        # Should only have 'id' present since that was matched
        self.assertIn('id', kwargs)
        self.assertEqual(kwargs['id'], '123')
        self.assertNotIn('lang', kwargs)  # Should be filtered out completely  
        self.assertNotIn('category', kwargs)  # Should be filtered out completely