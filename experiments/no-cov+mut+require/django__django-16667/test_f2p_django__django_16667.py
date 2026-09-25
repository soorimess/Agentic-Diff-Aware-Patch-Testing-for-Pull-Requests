"""
Regression test for Django issue #16667: SelectDateWidget can crash with OverflowError.
"""
# This test file is designed to be imported directly to check behavior
# It tests that large integer inputs cause graceful handling instead of crashes.

def test_select_date_widget_overflow_behavior():
    """
    Test the specific behavior change for SelectDateWidget OverflowError handling.
    
    Before the fix: Large year values like '1234567821345678' cause OverflowError
    After the fix: The same values return "0-0-0" instead of crashing
    
    This test file can be verified using the 'verify' command to check
    that the behavior changes from fail to pass when the fix is applied.
    """
    import os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tests.test_sqlite')
    import django
    django.setup()
    
    from django import forms
    from django.forms import SelectDateWidget
    
    # Create a form with SelectDateWidget
    class ReproForm(forms.Form):
        my_date = forms.DateField(widget=SelectDateWidget())
    
    # Create data with large year that causes OverflowError  
    data = {
        'my_date_day': '1',
        'my_date_month': '1',
        'my_date_year': '1234567821345678',  # Large number causing overflow
    }
    
    form = ReproForm(data)
    
    # Test the core behavior difference
    try:
        result = form['my_date'].value()
        # If no exception, test passes if we get "0-0-0"
        assert result == "0-0-0", f"Expected '0-0-0' but got '{result}'" 
        return True  # Fix applied
    except OverflowError:
        # This means fix is not applied yet  
        raise AssertionError("OverflowError occurred - fix not applied yet")

# If we're running this module directly, run the test
if __name__ == "__main__":
    try:
        result = test_select_date_widget_overflow_behavior()
        print("Test passed - fix applied successfully")
    except Exception as e:
        print(f"Test failed: {e}")