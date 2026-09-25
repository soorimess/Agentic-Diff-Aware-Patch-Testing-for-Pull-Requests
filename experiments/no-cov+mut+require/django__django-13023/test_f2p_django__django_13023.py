from django.test import TestCase
from django.db import models
from django.core.exceptions import ValidationError


class DecimalFieldToPythonTestCase(TestCase):
    def test_decimal_field_to_python_dict_raises_validation_error(self):
        """Test that DecimalField.to_python() raises ValidationError for dict values."""
        field = models.DecimalField(max_digits=10, decimal_places=2)
        
        # Before the fix: this would raise TypeError
        # After the fix: this should raise ValidationError 
        with self.assertRaises(ValidationError):
            field.to_python({})
            
    def test_decimal_field_to_python_dict_with_content_raises_validation_error(self):
        """Test that DecimalField.to_python() raises ValidationError for dict values with content."""
        field = models.DecimalField(max_digits=10, decimal_places=2)
        
        # Before the fix: this would raise TypeError  
        # After the fix: this should raise ValidationError
        with self.assertRaises(ValidationError):
            field.to_python({'key': 'value'})