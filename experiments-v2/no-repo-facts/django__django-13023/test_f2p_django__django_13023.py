import unittest
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.db import models


class TestDecimalFieldToPythonDict(unittest.TestCase):
    def test_decimal_field_to_python_dict_raises_validation_error(self):
        """
        Test that DecimalField.to_python() raises ValidationError when passed a dict,
        not TypeError as it did before the fix.
        """
        field = models.DecimalField(max_digits=4, decimal_places=2)
        
        # This should raise ValidationError, not TypeError
        with self.assertRaises(ValidationError) as cm:
            field.to_python({'key': 'value'})
        
        # Verify it's the right kind of error
        self.assertIn('invalid', cm.exception.code)
        
    def test_decimal_field_to_python_dict_raises_validation_error_with_different_values(self):
        """
        Test that DecimalField.to_python() raises ValidationError for various dict inputs.
        """
        field = models.DecimalField(max_digits=4, decimal_places=2)
        
        # Test with different dict values
        test_values = [
            {'a': 1, 'b': 2},
            {'key': 'value', 'number': 42},
            {},
        ]
        
        for value in test_values:
            with self.subTest(value=value):
                with self.assertRaises(ValidationError) as cm:
                    field.to_python(value)
                self.assertIn('invalid', cm.exception.code)
                
    def test_decimal_field_to_python_none_raises_validation_error(self):
        """
        Test that DecimalField.to_python() properly handles None values.
        None should be returned as-is, not raise an exception.
        """
        field = models.DecimalField(max_digits=4, decimal_places=2)
        
        # None should be returned as-is
        result = field.to_python(None)
        self.assertIsNone(result)
        
    def test_decimal_field_to_python_invalid_string_raises_validation_error(self):
        """
        Test that DecimalField.to_python() raises ValidationError for invalid strings,
        which should raise decimal.InvalidOperation.
        """
        field = models.DecimalField(max_digits=4, decimal_places=2)
        
        # Invalid strings should raise ValidationError
        with self.assertRaises(ValidationError) as cm:
            field.to_python('invalid')
        
        self.assertIn('invalid', cm.exception.code)