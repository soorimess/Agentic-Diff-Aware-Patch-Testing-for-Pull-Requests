"""
Regression test for Django issue #13023: 
DecimalField.to_python() raises TypeError on dict values.
"""
from django.test import SimpleTestCase
from django.db import models
from django.core.exceptions import ValidationError


class DecimalFieldToPythonTests(SimpleTestCase):
    
    def test_decimal_field_to_python_dict_raises_validation_error(self):
        """Test that DecimalField.to_python() raises ValidationError for dict values."""
        field = models.DecimalField()
        with self.assertRaises(ValidationError):
            field.to_python({'key': 'value'})
    
    def test_decimal_field_to_python_list_raises_validation_error(self):
        """Test that DecimalField.to_python() raises ValidationError for list values."""    
        field = models.DecimalField()
        with self.assertRaises(ValidationError):
            field.to_python(['a', 'b'])
    
    def test_decimal_field_to_python_invalid_string_raises_validation_error(self):
        """Test that DecimalField.to_python() raises ValidationError for invalid number strings."""
        field = models.DecimalField()
        with self.assertRaises(ValidationError):
            field.to_python("not_a_number")