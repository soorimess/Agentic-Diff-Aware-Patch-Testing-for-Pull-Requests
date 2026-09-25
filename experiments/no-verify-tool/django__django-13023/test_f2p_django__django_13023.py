"""
Regression test for Django bug where DecimalField.to_python() raises
TypeError on dict values instead of ValidationError.
"""
import unittest
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.db import models


class DecimalFieldDictTest(unittest.TestCase):
    def test_decimalfield_dict_value_raises_validationerror(self):
        """
        Test that calling DecimalField.to_python() with a dictionary raises
        ValidationError instead of TypeError.
        """
        field = models.DecimalField(max_digits=10, decimal_places=2)
        
        # This should raise ValidationError, not TypeError
        with self.assertRaises(ValidationError):
            field.to_python({})
            
    def test_decimalfield_list_value_raises_validationerror(self):
        """
        Test that calling DecimalField.to_python() with a list raises
        ValidationError instead of TypeError.
        """
        field = models.DecimalField(max_digits=10, decimal_places=2)
        
        # This should raise ValidationError, not TypeError
        with self.assertRaises(ValidationError):
            field.to_python([])
            
    def test_decimalfield_set_value_raises_validationerror(self):
        """
        Test that calling DecimalField.to_python() with a set raises
        ValidationError instead of TypeError.
        """
        field = models.DecimalField(max_digits=10, decimal_places=2)
        
        # This should raise ValidationError, not TypeError
        with self.assertRaises(ValidationError):
            field.to_python(set())
            
    def test_decimalfield_object_value_raises_validationerror(self):
        """
        Test that calling DecimalField.to_python() with an object raises
        ValidationError instead of TypeError.
        """
        field = models.DecimalField(max_digits=10, decimal_places=2)
        
        # This should raise ValidationError, not TypeError
        with self.assertRaises(ValidationError):
            field.to_python(object())