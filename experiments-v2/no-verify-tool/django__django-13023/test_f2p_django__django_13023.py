import unittest
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.db import models


class DecimalFieldToPythonDictTest(unittest.TestCase):
    """
    Test that DecimalField.to_python() raises ValidationError for dict values
    instead of TypeError.
    """
    
    def test_to_python_dict_raises_validation_error(self):
        """Test that passing a dict to DecimalField.to_python raises ValidationError."""
        field = models.DecimalField(max_digits=10, decimal_places=2)
        
        # This should raise ValidationError, not TypeError
        with self.assertRaises(ValidationError) as cm:
            field.to_python({})
        
        # Verify it's the right kind of error
        self.assertIn('value must be a decimal number', str(cm.exception))
        
    def test_to_python_dict_raises_validation_error_with_non_empty_dict(self):
        """Test that passing a non-empty dict to DecimalField.to_python raises ValidationError."""
        field = models.DecimalField(max_digits=10, decimal_places=2)
        
        # This should raise ValidationError, not TypeError
        with self.assertRaises(ValidationError) as cm:
            field.to_python({'key': 'value'})
        
        # Verify it's the right kind of error
        self.assertIn('value must be a decimal number', str(cm.exception))
        
    def test_to_python_other_types_still_work(self):
        """Test that other valid types still work as expected."""
        field = models.DecimalField(max_digits=10, decimal_places=2)
        
        # These should work normally
        self.assertEqual(field.to_python('3.14'), Decimal('3.14'))
        self.assertEqual(field.to_python(3), Decimal('3'))
        self.assertEqual(field.to_python(3.14), Decimal('3.14'))
        self.assertIsNone(field.to_python(None))