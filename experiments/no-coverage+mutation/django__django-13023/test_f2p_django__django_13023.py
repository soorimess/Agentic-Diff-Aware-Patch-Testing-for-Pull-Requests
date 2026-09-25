import unittest
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.db import models

class TestDecimalFieldToPython(unittest.TestCase):
    
    def test_decimal_field_to_python_dict_raises_validation_error(self):
        """
        Test that DecimalField.to_python() raises ValidationError for dict values,
        not TypeError as was the case before the fix.
        """
        field = models.DecimalField()
        
        # This should raise ValidationError, not TypeError 
        with self.assertRaises(ValidationError) as cm:
            field.to_python({'key': 'value'})
            
        # Verify it's the right type of validation error
        self.assertIn('invalid', cm.exception.code)
        
    def test_decimal_field_to_python_string_works(self):
        """Test that string values still work correctly."""
        field = models.DecimalField()
        
        # This should work fine
        result = field.to_python('123.45')
        self.assertIsInstance(result, Decimal)
        self.assertEqual(str(result), '123.45')
        
    def test_decimal_field_to_python_float_works(self):
        """Test that float values still work correctly."""
        field = models.DecimalField()
        
        # This should work fine
        result = field.to_python(123.45)
        self.assertIsInstance(result, Decimal)