"""
Test for Django issue #13794.

Bug: add filter is unable to concatenate strings with lazy string
Description: If you try to concatenate a string with a lazy string with the 
add template filter, the result is always the empty string because the add 
filter generates an exception (TypeError: can only concatenate str (not "__proxy__") to str).

This test verifies that lazy strings can be properly concatenated.
"""
from django.utils.functional import lazy
import unittest


def get_lazy_string():
    return "Hello World"


class TestLazyStringAdd(unittest.TestCase):
    
    def test_lazy_string_concatenation_left_side(self):
        """
        Test concatenation where a string is on the left of + operator.
        This exercises __radd__ method in __proxy__ class.
        """
        lazy_str = lazy(get_lazy_string, str)
        
        # This is when Python tries to call lazy_obj.__radd__("string")
        # which doesn't exist in the old version and causes the error described
        result = "Prefix: " + lazy_str()
        self.assertEqual(result, "Prefix: Hello World")
        
    def test_lazy_string_concatenation_right_side(self):
        """
        Test concatenation where a lazy string is on the left of + operator.
        This exercises __add__ method in __proxy__ class.
        """
        lazy_str = lazy(get_lazy_string, str)
        
        # This is when Python tries to call lazy_obj.__add__("string") 
        # which doesn't exist in the old version
        result = lazy_str() + " - Suffix"
        self.assertEqual(result, "Hello World - Suffix")
        
    def test_lazy_string_concatenation_both_sides(self):
        """
        Test concatenation of two lazy strings.
        """
        lazy_str1 = lazy(get_lazy_string, str)
        lazy_str2 = lazy(lambda: " from lazy", str)
        
        # This tests proxy.__add__ method directly  
        result = lazy_str1() + lazy_str2()
        self.assertEqual(result, "Hello World from lazy")