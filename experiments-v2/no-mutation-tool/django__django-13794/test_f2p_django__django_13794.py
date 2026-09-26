from django.test import SimpleTestCase
from django.utils.functional import lazy


class AddFilterLazyStringTest(SimpleTestCase):
    """
    Test that the add filter works correctly with lazy strings.
    
    This is a regression test for Django issue where the add filter
    was unable to concatenate strings with lazy strings, resulting in
    TypeError: can only concatenate str (not "__proxy__") to str.
    """

    def test_lazy_string_has_add_methods(self):
        """
        Test that lazy strings (Promise objects) have __add__ and __radd__ methods.
        
        This test verifies that the fix for Django issue 13794 is in place.
        Before the fix, lazy strings would not have these methods, causing
        TypeError when trying to concatenate with strings.
        """
        # Create a lazy string which is a Promise object
        lazy_str = lazy(lambda: "hello", str)
        promise_obj = lazy_str()
        
        # These methods should exist after the fix
        self.assertTrue(hasattr(promise_obj, '__add__'))
        self.assertTrue(hasattr(promise_obj, '__radd__'))
        
        # Test that the methods can be called without TypeError
        # This specifically tests the fix that was applied
        try:
            # Test __add__ method
            result1 = promise_obj.__add__(" world")
            # Should return a string without TypeError
            self.assertIsInstance(result1, str)
            
            # Test __radd__ method  
            result2 = promise_obj.__radd__("world ")
            # Should return a string without TypeError
            self.assertIsInstance(result2, str)
        except TypeError as e:
            if '"__proxy__" to str' in str(e):
                self.fail("Got TypeError: can only concatenate str (not \"__proxy__\") to str")
            else:
                raise