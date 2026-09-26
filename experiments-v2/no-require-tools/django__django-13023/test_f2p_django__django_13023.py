import unittest
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.db import models


class DecimalFieldToPythonDictTest(unittest.TestCase):
    """
    Test that DecimalField.to_python() raises ValidationError instead of TypeError
    when passed a dictionary value.
    """
    
    def test_to_python_dict_raises_validation_error(self):
        """Test that passing a dict to DecimalField.to_python raises ValidationError."""
        field = models.DecimalField(max_digits=10, decimal_places=2)
        
        # This should raise ValidationError, not TypeError
        with self.assertRaises(ValidationError) as cm:
            field.to_python({'key': 'value'})
        
        # Verify it's the right kind of error
        self.assertIn('value must be a decimal number', str(cm.exception))
        
    def test_to_python_valueerror_raises_validation_error(self):
        """Test that passing invalid string to DecimalField.to_python raises ValidationError."""
        field = models.DecimalField(max_digits=10, decimal_places=2)
        
        # This should raise ValidationError, not ValueError
        with self.assertRaises(ValidationError) as cm:
            field.to_python('not_a_number')
        
        # Verify it's the right kind of error
        self.assertIn('value must be a decimal number', str(cm.exception))
        
    def test_to_python_none_works(self):
        """Test that None still works correctly."""
        field = models.DecimalField(max_digits=10, decimal_places=2)
        self.assertIsNone(field.to_python(None))
        
    def test_to_python_valid_values_still_work(self):
        """Test that valid values still work correctly."""
        field = models.DecimalField(max_digits=10, decimal_places=2)
        
        # Test with string
        self.assertEqual(field.to_python('12.34'), Decimal('12.34'))
        
        # Test with int
        self.assertEqual(field.to_python(42), Decimal('42'))
        
        # Test with float
        self.assertEqual(field.to_python(3.14), Decimal('3.14'))