"""
Regression test for Django bug where DecimalField.to_python() raises TypeError 
on dict values instead of ValidationError.

This test verifies the fix in Django PR #13023 where DecimalField.to_python() was
changed to catch TypeError and ValueError in addition to decimal.InvalidOperation.
"""

from django.test import SimpleTestCase
from django.db import models
from django.core.exceptions import ValidationError


class DecimalFieldToPythonRegressionTest(SimpleTestCase):
    def test_decimal_field_to_python_dict_raises_validation_error_not_type_error(self):
        """
        Test that DecimalField.to_python() raises ValidationError for dict values,
        not TypeError. This is the core of the bug being fixed.
        """
        field = models.DecimalField(max_digits=10, decimal_places=2)
        
        # The main test: dict input should raise ValidationError, not TypeError
        # Before fix: TypeError raises 
        # After fix: ValidationError raises (which is correct)
        with self.assertRaises(ValidationError):
            field.to_python({'key': 'value'})
            
        # Make sure it's NOT TypeError (the bug)
        with self.assertRaises(Exception) as cm:
            field.to_python({'key': 'value'})
        self.assertNotIsInstance(cm.exception, TypeError)

    def test_decimal_field_to_python_various_invalid_inputs(self):
        """
        Test that various invalid inputs raise ValidationError, not TypeError.
        """
        field = models.DecimalField(max_digits=10, decimal_places=2)
        
        # All these should raise ValidationError (not TypeError) after fix
        invalid_inputs = [
            {'key': 'value'},  # dict
            set(),              # set  
            object(),           # object
        ]
        
        for invalid_input in invalid_inputs:
            with self.subTest(input=invalid_input):
                # After fix: should raise ValidationError, not TypeError
                with self.assertRaises(ValidationError):
                    field.to_python(invalid_input)
                    
                # Make sure it's not Type Error
                with self.assertRaises(Exception) as cm:
                    field.to_python(invalid_input)
                self.assertNotIsInstance(cm.exception, TypeError)