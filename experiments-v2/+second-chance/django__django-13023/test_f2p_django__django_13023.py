from django.db import models
from django.test import TestCase
from django.core.exceptions import ValidationError


class DecimalFieldToPythonDictTest(TestCase):
    def test_decimal_field_to_python_dict_raises_validation_error(self):
        """DecimalField.to_python() should raise ValidationError for dict values, not TypeError."""
        field = models.DecimalField()
        
        # This should raise ValidationError, not TypeError
        with self.assertRaises(ValidationError):
            field.to_python({})

    def test_decimal_field_to_python_dict_raises_validation_error_with_nested_dict(self):
        """DecimalField.to_python() should raise ValidationError for nested dict values."""
        field = models.DecimalField()
        
        # This should raise ValidationError, not TypeError  
        with self.assertRaises(ValidationError):
            field.to_python({'key': 'value'})