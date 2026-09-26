from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import models


class DecimalFieldToPythonDictTest(TestCase):
    def test_decimal_field_to_python_dict_raises_validation_error(self):
        """Test that DecimalField.to_python() raises ValidationError for dict values."""
        field = models.DecimalField(max_digits=10, decimal_places=2)
        
        # This should raise ValidationError, not TypeError
        with self.assertRaises(ValidationError):
            field.to_python({'key': 'value'})