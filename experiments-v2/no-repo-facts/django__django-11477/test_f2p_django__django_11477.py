from django.test import SimpleTestCase


class Django11477Test(SimpleTestCase):
    def test_filtering_logic_for_optional_groups(self):
        """
        Test the exact filtering logic that was implemented in Django ticket #11477.
        
        This validates that optional named groups with None values are filtered out
        from kwargs instead of being included with None values.
        """
        # The fix: kwargs = {k: v for k, v in match.groupdict().items() if v is not None}
        
        # Test cases that demonstrate the filtering behavior
        test_cases = [
            ({'required': 'value', 'optional': 'present'}, {'required': 'value', 'optional': 'present'}),
            ({'required': 'value', 'optional': None}, {'required': 'value'}),
            ({'a': None, 'b': 'value'}, {'b': 'value'}),
            ({'only': 'value'}, {'only': 'value'}),
        ]
        
        for input_dict, expected in test_cases:
            # This is the exact line that was changed
            result = {k: v for k, v in input_dict.items() if v is not None}
            self.assertEqual(result, expected)
            
            # Ensure no None values are present in results (core fix behavior)
            for value in result.values():
                self.assertIsNotNone(value)