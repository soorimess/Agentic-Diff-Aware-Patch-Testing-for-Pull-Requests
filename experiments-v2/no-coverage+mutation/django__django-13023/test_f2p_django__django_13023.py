import unittest
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.db import models


class TestDecimalFieldDictValue(unittest.TestCase):
    """Test that DecimalField.to_python() raises ValidationError for dict values, not TypeError."""

    def test_decimal_field_to_python_dict_raises_validation_error(self):
        """Test that passing a dict to DecimalField.to_python() raises ValidationError."""
        field = models.DecimalField(max_digits=10, decimal_places=2)
        
        # This should raise ValidationError, not TypeError
        with self.assertRaises(ValidationError) as cm:
            field.to_python({'key': 'value'})
        
        # Verify it's the right type of exception
        self.assertEqual(cm.exception.code, 'invalid')
        
    def test_decimal_field_to_python_empty_dict_raises_validation_error(self):
        """Test that passing an empty dict to DecimalField.to_python() raises ValidationError."""
        field = models.DecimalField(max_digits=10, decimal_places=2)
        
        # Test with empty dict
        with self.assertRaises(ValidationError) as cm:
            field.to_python({})
        self.assertEqual(cm.exception.code, 'invalid')
        
    def test_decimal_field_to_python_nested_dict_raises_validation_error(self):
        """Test that passing nested dict to DecimalField.to_python() raises ValidationError."""
        field = models.DecimalField(max_digits=10, decimal_places=2)
        
        # Test with nested dict
        with self.assertRaises(ValidationError) as cm:
            field.to_python({'nested': {'key': 'value'}})
        self.assertEqual(cm.exception.code, 'invalid')