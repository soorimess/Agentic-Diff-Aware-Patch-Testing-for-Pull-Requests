import unittest
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models


class DecimalFieldToPythonDictTest(unittest.TestCase):
    
    def test_to_python_dict_raises_validation_error(self):
        """DecimalField.to_python() should raise ValidationError for dict values, not TypeError."""
        field = models.DecimalField(max_digits=10, decimal_places=2)
        
        # Test with a dictionary - this should raise ValidationError, not TypeError
        with self.assertRaises(ValidationError):
            field.to_python({1: 2})
            
    def test_to_python_dict_raises_validation_error_with_string(self):
        """DecimalField.to_python() should raise ValidationError for dict values, not TypeError."""
        field = models.DecimalField(max_digits=10, decimal_places=2)
        
        # Test with a dict with string key/value
        with self.assertRaises(ValidationError):
            field.to_python({'a': 'b'})
            
    def test_to_python_dict_raises_validation_error_empty_dict(self):
        """DecimalField.to_python() should raise ValidationError for empty dict values."""
        field = models.DecimalField(max_digits=10, decimal_places=2)
        
        # Test with an empty dictionary
        with self.assertRaises(ValidationError):
            field.to_python({})