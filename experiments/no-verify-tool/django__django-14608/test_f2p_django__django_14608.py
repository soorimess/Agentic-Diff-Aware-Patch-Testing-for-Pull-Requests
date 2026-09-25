"""
Regression test for Django issue #14608: Add `nonform` CSS class for non form errors in FormSets
"""

def run_regression_test():
    """
    Run test to verify formsets use 'nonform' CSS class for non-form errors.
    
    This regression test checks that:
    - Before fix: formset._non_form_errors.error_class = 'errorlist' 
    - After fix: formset._non_form_errors.error_class = 'errorlist nonform'
    
    This matches the behavior in forms where non-field errors use 'nonfield' class.
    """
    from django.forms import BaseFormSet, ValidationError
    
    class NonFormErrorFormSet(BaseFormSet):
        def clean(self):
            raise ValidationError('Non-form error message')
    
    # Create formset and trigger validation
    formset = NonFormErrorFormSet()
    formset.full_clean()
    
    # Check CSS class on non-form errors
    expected_css_class = 'errorlist nonform'
    actual_css_class = formset._non_form_errors.error_class
    
    if actual_css_class == expected_css_class:
        print("SUCCESS: Formset correctly uses 'nonform' CSS class")
        return True
    else:
        print(f"EXPECTED: '{expected_css_class}'")
        print(f"ACTUAL:   '{actual_css_class}'")
        print("FAIL: Formset does not use 'nonform' CSS class (bug present)")
        return False

if __name__ == '__main__':
    # Configure Django for testing 
    import os
    import sys
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tests.test_sqlite')
    sys.path.insert(0, '.')
    
    import django
    django.setup()
    
    # Run the test
    success = run_regression_test()
    if success:
        print("\n✅ Test PASSED - Bug is fixed")
        sys.exit(0) 
    else:
        print("\n❌ Test FAILED - Bug is present (expected in unfixed code)")
        sys.exit(1)