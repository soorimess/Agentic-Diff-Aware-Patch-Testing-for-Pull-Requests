"""
Test for Django DecimalField.to_python() dict handling fix
"""

def test_decimal_field_dict_invalid():
    """Test that dict values raise ValidationError instead of TypeError"""
    from django.db import models
    from django.core.exceptions import ValidationError
    
    field = models.DecimalField(max_digits=10, decimal_places=2)
    
    try:
        field.to_python({"a": "b"})
        assert False, "Should have raised an exception"
    except TypeError:
        # This is the bug - TypeError should be caught and re-raised as ValidationError
        raise AssertionError("This should not be reached with the fix applied")
    except ValidationError:
        # This is the desired behavior after the fix
        pass
    except Exception as e:
        raise AssertionError(f"Unexpected exception: {type(e).__name__}: {e}")


# This provides a specific function that's importable
def main_test():
    """Main test method for verification"""
    test_decimal_field_dict_invalid()
    
if __name__ == "__main__":
    main_test()
    print("Test passed!")