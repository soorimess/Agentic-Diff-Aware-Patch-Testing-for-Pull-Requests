import unittest
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.db import models


class DecimalFieldToPythonDictTest(unittest.TestCase):
    """
    Test that DecimalField.to_python() raises ValidationError instead of TypeError
    when passed a dictionary value.
    """

    def test_decimal_field_to_python_dict_raises_validation_error(self):
        """Test that passing a dict to DecimalField.to_python raises ValidationError."""
        field = models.DecimalField(max_digits=10, decimal_places=2)
        
        # This should raise ValidationError, not TypeError
        with self.assertRaises(ValidationError) as cm:
            field.to_python({'key': 'value'})
        
        # Verify it's the right type of error
        self.assertIn('invalid', cm.exception.code)
        
    def test_decimal_field_to_python_other_types_still_work(self):
        """Test that other valid types still work correctly."""
        field = models.DecimalField(max_digits=10, decimal_places=2)
        
        # These should work normally
        self.assertEqual(field.to_python(None), None)
        self.assertEqual(field.to_python('12.34'), Decimal('12.34'))
        self.assertEqual(field.to_python(12.34), Decimal('12.34'))
        self.assertEqual(field.to_python(12), Decimal('12.00'))
        
        # Invalid strings should raise ValidationError
        with self.assertRaises(ValidationError):
            field.to_python('invalid')