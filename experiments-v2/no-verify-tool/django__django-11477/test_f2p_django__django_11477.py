"""
Regression test for Django issue with optional named groups in URL patterns.

This test ensures that when URL patterns have optional named groups that are
missing from the URL, they are not included in the returned kwargs dictionary.
"""
import unittest

from django.urls.resolvers import RegexPattern


class OptionalNamedGroupsTest(unittest.TestCase):
    
    def test_optional_named_groups_are_excluded_when_none(self):
        """
        Test that optional named groups with None values are excluded from kwargs.
        
        When a URL pattern has optional named groups (using ? in regex) and those
        groups don't match (return None), they should not appear in the kwargs
        returned by match(), not even with a None value.
        """
        # Create a regex pattern with an optional named group
        # This pattern matches '/test/' followed by an optional named group 'param'
        pattern = RegexPattern(r'^/test/(?P<param>\w+)?/?$')
        
        # Test URL that matches but doesn't provide the optional param
        path_str = '/test/'
        
        # This should return kwargs without 'param' key when the optional group is missing
        result = pattern.match(path_str)
        
        # The result should be (remaining_path, args, kwargs)
        if result is not None:
            remaining_path, args, kwargs = result
            # The bug was that kwargs would contain {'param': None} instead of {}
            # After the fix, 'param' should not be in kwargs at all
            self.assertEqual(remaining_path, '')
            self.assertEqual(args, ())
            # This assertion will fail with old code but pass with new code
            self.assertNotIn('param', kwargs)
        else:
            self.fail("Pattern should match")
    
    def test_optional_named_groups_are_included_when_present(self):
        """
        Test that optional named groups with actual values are included in kwargs.
        """
        # Create a regex pattern with an optional named group
        pattern = RegexPattern(r'^/test/(?P<param>\w+)?/?$')
        
        # Test URL that provides the optional param
        path_str = '/test/value/'
        
        result = pattern.match(path_str)
        
        if result is not None:
            remaining_path, args, kwargs = result
            self.assertEqual(remaining_path, '')
            self.assertEqual(args, ())
            # The param should be present in kwargs with its value
            self.assertIn('param', kwargs)
            self.assertEqual(kwargs['param'], 'value')
        else:
            self.fail("Pattern should match")