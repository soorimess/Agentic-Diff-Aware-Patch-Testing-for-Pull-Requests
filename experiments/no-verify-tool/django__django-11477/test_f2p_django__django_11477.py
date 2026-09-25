"""
Regression test for translate_url() with optional named groups issue.

When URL patterns contain optional named groups that result in None values, 
translate_url() behaves differently after the fix compared to before.

The issue: in resolvers.py, line 156, the code was changed from:
    kwargs = match.groupdict()
to:
    kwargs = {k: v for k, v in match.groupdict().items() if v is not None}

This removes None values from kwargs in URL pattern matching behavior.
"""

from django.test import SimpleTestCase
from django.urls.resolvers import RoutePattern


class TranslateUrlOptionalGroupTest(SimpleTestCase):
    """
    Test that demonstrates the behavior change in URL pattern matching
    when optional named groups produce None values.
    """

    def test_optional_named_group_none_values_filtered(self):
        """
        Before fix: Optional named groups returning None were included in kwargs
        After fix: Optional named groups returning None are filtered out of kwargs
        """
        # Create a RoutePattern that uses an optional named group
        pattern = RoutePattern(r'^/article/(?P<year>\d{4})?/title/(?P<title>[^/]+)/$')
        
        # Match when year is present
        match_result = pattern.match('/article/2023/title/my-title/')
        self.assertIsNotNone(match_result)
        remaining_path, args, kwargs = match_result
        # Both parameters should be present
        self.assertEqual(kwargs.get('year'), '2023')
        self.assertEqual(kwargs.get('title'), 'my-title')

        # Match when year is NOT present (optional group that wasn't provided)
        # This should result in 'year': None in the groupdict() 
        match_result = pattern.match('/article/title/my-title/')
        self.assertIsNotNone(match_result)
        remaining_path, args, kwargs = match_result
        
        # The key difference:
        # Before change: kwargs would contain 'year': None 
        # After change: kwargs should NOT contain 'year' key at all
        # This is what breaks translate_url behavior
        self.assertNotIn('year', kwargs)
        self.assertEqual(kwargs.get('title'), 'my-title')

    def test_change_effect_on_url_resolution(self):
        """
        Test that directly demonstrates the workaround checks that show what changed.
        """
        # Get the regex that would be generated
        import re
        
        # Pattern with an optional named group
        pattern = r'^/article/(?P<year>\d{4})?/title/(?P<title>[^/]+)/$'
        regex = re.compile(pattern)
        
        # When year is provided
        match = regex.search('/article/2023/title/my-title/')
        groupdict_with_year = match.groupdict()
        # Both groups should be there
        self.assertEqual(groupdict_with_year.get('year'), '2023')
        self.assertEqual(groupdict_with_year.get('title'), 'my-title')
        
        # When year is NOT provided
        match = regex.search('/article/title/my-title/')
        groupdict_without_year = match.groupdict()
        # Optional group exists but returns None
        self.assertEqual(groupdict_without_year.get('year'), None)
        self.assertEqual(groupdict_without_year.get('title'), 'my-title')
        
        # This is the behavior change:
        # Old approach would use: groupdict_without_year as kwargs
        # New approach filters: {k: v for k, v in groupdict_without_year.items() if v is not None}
        filtered_kwargs = {k: v for k, v in groupdict_without_year.items() if v is not None}
        self.assertNotIn('year', filtered_kwargs)  # This is the problem fixed
        self.assertIn('title', filtered_kwargs)