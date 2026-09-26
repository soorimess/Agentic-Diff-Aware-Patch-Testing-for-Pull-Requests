from django.db import models
from django.core.exceptions import ValidationError
from django.test import TestCase
import decimal


class DecimalFieldToPythonTest(TestCase):
    def test_to_python_dict_raises_validation_error(self):
        """DecimalField.to_python() should raise ValidationError for dict values, not TypeError."""
        field = models.DecimalField()
        
        # This should raise ValidationError, not TypeError
        with self.assertRaises(ValidationError):
            field.to_python({})

    def test_to_python_list_raises_validation_error(self):
        """DecimalField.to_python() should raise ValidationError for list values, not ValueError."""
        field = models.DecimalField()
        
        # This should raise ValidationError, not ValueError
        with self.assertRaises(ValidationError):
            field.to_python([])

    def test_to_python_none_returns_none(self):
        """DecimalField.to_python() should return None for None values."""
        field = models.DecimalField()
        self.assertIsNone(field.to_python(None))

    def test_to_python_valid_string_returns_decimal(self):
        """DecimalField.to_python() should return Decimal for valid string values."""
        field = models.DecimalField()
        result = field.to_python("123.45")
        self.assertEqual(result, decimal.Decimal("123.45"))