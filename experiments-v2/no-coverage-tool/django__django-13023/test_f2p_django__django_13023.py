from decimal import Decimal
from django.db import models
from django.core.exceptions import ValidationError
from django.test import TestCase


class DecimalFieldToPythonTest(TestCase):
    def test_to_python_dict_raises_validation_error(self):
        """DecimalField.to_python() should raise ValidationError for dict values, not TypeError."""
        field = models.DecimalField()
        
        # This should raise ValidationError, not TypeError
        with self.assertRaises(ValidationError):
            field.to_python({'key': 'value'})
            
    def test_to_python_list_raises_validation_error(self):
        """DecimalField.to_python() should raise ValidationError for list values, not TypeError."""
        field = models.DecimalField()
        
        # This should raise ValidationError, not TypeError
        with self.assertRaises(ValidationError):
            field.to_python(['a', 'b'])
            
    def test_to_python_invalid_string_raises_validation_error(self):
        """Ensure invalid strings still raise ValidationError."""
        field = models.DecimalField()
        
        with self.assertRaises(ValidationError):
            field.to_python('not_a_number')