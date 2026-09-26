from django.test import TestCase
from django.urls.resolvers import RegexPattern


class TranslateUrlOptionalGroupsTest(TestCase):
    def test_optional_named_groups_in_url_pattern(self):
        """
        Test that translate_url() handles optional named groups correctly.
        When optional named groups are missing, they should not be included in kwargs.
        """
        # Create a regex pattern with an optional named group
        pattern = r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<optional>\w+)?$'
        regex_pattern = RegexPattern(pattern)
        
        # Test URL without the optional part
        path = '2023/12/01/'
        
        # This should match and return the correct components
        result = regex_pattern.match(path)
        
        # Before the fix, this would include 'optional': None in kwargs
        # After the fix, this should not include 'optional' at all in kwargs
        if result is not None:
            remaining_path, args, kwargs = result
            # The kwargs should NOT contain the optional group when it's not matched
            self.assertNotIn('optional', kwargs, 
                          "Optional named group should not be in kwargs when not matched")
            self.assertIn('year', kwargs)
            self.assertIn('month', kwargs)
            self.assertIn('day', kwargs)
            self.assertEqual(kwargs['year'], '2023')
            self.assertEqual(kwargs['month'], '12')
            self.assertEqual(kwargs['day'], '01')
        else:
            self.fail("Pattern should match the path")
    
    def test_optional_named_groups_with_value(self):
        """
        Test that optional named groups with values are still included correctly.
        """
        # Create a regex pattern with an optional named group
        pattern = r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<optional>\w+)?$'
        regex_pattern = RegexPattern(pattern)
        
        # Test URL with the optional part
        path = '2023/12/01/somevalue'
        
        # This should match and return the correct components
        result = regex_pattern.match(path)
        
        if result is not None:
            remaining_path, args, kwargs = result
            # The kwargs should contain the optional group when it's matched
            self.assertIn('optional', kwargs, 
                         "Optional named group should be in kwargs when matched")
            self.assertEqual(kwargs['optional'], 'somevalue')
        else:
            self.fail("Pattern should match the path")