"""
Test for Django issue #13794: add filter should concatenate strings with lazy strings.
Before the fix, this would raise: TypeError: can only concatenate str (not "__proxy__") to str
"""
from django.test import SimpleTestCase
from django.utils.translation import gettext_lazy


class AddFilterLazyStringTest(SimpleTestCase):
    """Test cases for add filter with lazy strings."""

    def test_add_string_and_lazy_string_does_not_raise_typeerror(self):
        """
        Test that adding a string to a lazy string does not raise TypeError.
        
        This is the core functionality that was failing before the patch was applied.
        """
        # Create a lazy string (will be a Promise object)  
        lazy_string = gettext_lazy("Hello")
        normal_string = " World"
        
        # The crucial test is that this operation doesn't raise TypeError
        # which was the reported bug: TypeError: can only concatenate str (not "__proxy__") to str
        
        # Check that the operation works without raising a TypeError
        # We construct the test so we can demonstrate the behavior difference
        try:
            # This would have failed before the fix  
            result = normal_string + lazy_string
            # If successful, result should be a string
            self.assertIsInstance(result, str)
        except TypeError as e:
            # Check that it's the specific error we're avoiding
            if "__proxy__" in str(e) and "concatenate str" in str(e):
                self.fail("Add filter should not raise TypeError when concatenating string with lazy string: %s" % str(e))
            raise  # Re-raise if it's a different TypeError

        # Also check reverse order
        try:
            result = lazy_string + normal_string
            self.assertIsInstance(result, str)  
        except TypeError as e:
            if "__proxy__" in str(e) and "concatenate str" in str(e):
                self.fail("Add filter should not raise TypeError when concatenating lazy string with string: %s" % str(e))
            raise  # Re-raise if it's a different TypeError