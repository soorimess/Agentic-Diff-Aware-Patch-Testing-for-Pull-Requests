from django.db import models
from django.core.exceptions import ValidationError
from django.test import TestCase


class DecimalFieldToPythonTest(TestCase):
    def test_dict_value_raises_validation_error_not_typeerror(self):
        """
        DecimalField.to_python() should raise ValidationError for dict values
        instead of the raw TypeError that is currently raised.
        """
        field = models.DecimalField()
        
        # This was raising TypeError before the fix, but should raise ValidationError
        with self.assertRaises(ValidationError) as cm:
            field.to_python({})
            
        # Verify it's the right type of ValidationError
        self.assertEqual(cm.exception.code, 'invalid')

    def test_invalid_string_still_raises_validation_error(self):
        """
        DecimalField.to_python() should continue to raise ValidationError for invalid strings.
        """
        field = models.DecimalField()
        
        # This should still raise ValidationError as before
        with self.assertRaises(ValidationError) as cm:
            field.to_python("not_a_number")
            
        # Verify it's the right type of ValidationError
        self.assertEqual(cm.exception.code, 'invalid')