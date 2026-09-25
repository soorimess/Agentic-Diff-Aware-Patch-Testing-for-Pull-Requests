"""
Regression test for Django bug: DecimalField.to_python() raises TypeError on dict values.

This test specifically targets the fix in https://github.com/django/django/pull/13023
"""
import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from decimal import Decimal
from django.core.exceptions import ValidationError
from django.db import models


def test_decimal_field_dict_input():
    """Test that dict input raises ValidationError instead of TypeError"""
    field = models.DecimalField(max_digits=10, decimal_places=2)
    
    # These should raise ValidationError not TypeError
    # Status: Before fix = TypeError, After fix = ValidationError
    try:
        field.to_python({})
        assert False, "Should have raised an exception"
    except TypeError:
        # This is old buggy behavior that we want to prevent
        raise AssertionError("TypeError raised - bug still exists!")
    except ValidationError:
        # This is the desired behavior after fix
        pass  # OK - test passes
    
    try:
        field.to_python({'key': 'value'})
        assert False, "Should have raised an exception"
    except TypeError:
        # This is old buggy behavior that we want to prevent  
        raise AssertionError("TypeError raised - bug still exists!")
    except ValidationError:
        # This is the desired behavior after fix
        pass  # OK - test passes


def test_decimal_field_normal_inputs():
    """Ensure normal inputs work correctly (regression test)"""
    field = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Valid functionality should still work
    assert field.to_python('12.34') == Decimal('12.34')
    assert field.to_python(None) is None