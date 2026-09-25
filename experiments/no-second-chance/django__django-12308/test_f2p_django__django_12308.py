"""
Regression test for Django issue: JSONField are not properly displayed in admin when they are readonly
This test verifies the correct behavior after the fix is applied.
"""
from django.test import SimpleTestCase
from django.db import models
from django.contrib.admin.utils import display_for_field


class MockJSONField(models.JSONField):
    """Mock JSONField for tests"""
    pass


class TestJSONFieldDisplay(SimpleTestCase):
    """Test JSONField admin display behavior"""
    
    def test_jsonfield_shows_valid_json_after_fix(self):
        """Test that JSONFields show as valid JSON after the fix is applied"""
        # Create a JSONField mock
        field = MockJSONField()
        
        # Test data 
        test_value = {'foo': 'bar'} 
        empty_value_display = '-'
        
        # After fix, this should be processed by field.get_prep_value() 
        # which calls json.dumps() and should return valid JSON with double quotes
        result = display_for_field(test_value, field, empty_value_display)
        
        # With the fix, should show as valid JSON with double quotes  
        self.assertEqual(result, '{"foo": "bar"}')
        
    def test_jsonfield_complex_data_after_fix(self):
        """Test with more complex JSON structure - valid JSON after fix"""
        field = MockJSONField()
        test_value = {'nested': {'a': 1, 'b': [1, 2, 3]}}
        empty_value_display = '-'
        
        result = display_for_field(test_value, field, empty_value_display)
        
        # Should be valid JSON with double quotes 
        self.assertEqual(result, '{"nested": {"a": 1, "b": [1, 2, 3]}}')
        
    def test_jsonfield_empty_dict_after_fix(self):
        """Test with empty dict"""
        field = MockJSONField()
        test_value = {}
        empty_value_display = '-'
        
        result = display_for_field(test_value, field, empty_value_display)
        
        self.assertEqual(result, '{}')
        
    def test_jsonfield_none_value(self):
        """Test that None values are handled correctly"""
        field = MockJSONField()
        test_value = None
        empty_value_display = '-'
        
        result = display_for_field(test_value, field, empty_value_display)
        
        # Should return the empty_value_display for None values
        self.assertEqual(result, '-')
        
    def test_jsonfield_typeerror_handling_after_fix(self):
        """Test the TypeError case - when get_prep_value raises TypeError"""
        # We need to mock a field where get_prep_value raises TypeError
        # Let's create a special field that overrides get_prep_value to raise TypeError
        class TestJSONFieldWithError(models.JSONField):
            def get_prep_value(self, value):
                raise TypeError("Test TypeError for JSONField")
        
        field = TestJSONFieldWithError()
        test_value = {'foo': 'bar'}
        empty_value_display = '-'
        
        # When get_prep_value raises TypeError, should fall back to display_for_value
        result = display_for_field(test_value, field, empty_value_display)
        
        # Should fall back to regular display_for_value behavior 
        # This expects the same behavior as Python representation
        self.assertEqual(result, "{'foo': 'bar'}")
        
    def test_regular_field_unaffected(self):
        """Test that regular fields are not affected"""
        field = models.CharField(max_length=100)
        test_value = "test string"
        empty_value_display = '-'
        
        result = display_for_field(test_value, field, empty_value_display)
        
        self.assertEqual(result, "test string")