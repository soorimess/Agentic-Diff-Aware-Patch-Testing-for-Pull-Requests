import unittest
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models


class TestDecimalFieldDictValue(unittest.TestCase):
    """
    Test that DecimalField.to_python() raises ValidationError instead of TypeError
    when a dictionary is passed as the value.
    """
    
    def test_to_python_dict_raises_validation_error(self):
        """Test that passing a dict to DecimalField.to_python() raises ValidationError."""
        field = models.DecimalField(max_digits=10, decimal_places=2)
        
        # This should raise ValidationError, not TypeError
        with self.assertRaises(ValidationError):
            field.to_python({})
    
    def test_to_python_dict_with_data_raises_validation_error(self):
        """Test that passing a dict with data to DecimalField.to_python() raises ValidationError."""
        field = models.DecimalField(max_digits=10, decimal_places=2)
        
        # This should raise ValidationError, not TypeError
        with self.assertRaises(ValidationError):
            field.to_python({'key': 'value'})
    
    def test_to_python_valid_values_still_work(self):
        """Test that valid values still work correctly."""
        field = models.DecimalField(max_digits=10, decimal_places=2)
        
        # Valid values should work as before
        self.assertEqual(field.to_python('12.34'), Decimal('12.34'))
        self.assertEqual(field.to_python(12.34), Decimal('12.34'))
        self.assertEqual(field.to_python(12), Decimal('12.00'))
        self.assertIsNone(field.to_python(None))
        
    def test_to_python_invalid_string_still_raises_validation_error(self):
        """Test that invalid strings still properly raise ValidationError."""
        field = models.DecimalField(max_digits=10, decimal_places=2)
        
        # Invalid strings should still raise ValidationError
        with self.assertRaises(ValidationError):
            field.to_python('not_a_number')