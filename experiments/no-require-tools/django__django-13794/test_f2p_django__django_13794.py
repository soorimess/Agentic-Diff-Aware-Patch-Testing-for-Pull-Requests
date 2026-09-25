"""
Regression test for Django issue where add filter fails to concatenate
strings with lazy strings.
"""

import unittest
from django.utils.functional import lazy


class TestLazyStringAddition(unittest.TestCase):
    def test_lazy_string_concatenation(self):
        """
        Test string concatenation with lazy strings works after fix.
        Before fix: TypeError with "must be str, not __proxy__"
        After fix: Works correctly
        """
        # Create a lazy string 
        lazy_string = lazy(lambda: "world", str)()
        
        # This should work after the fix
        result1 = "hello " + lazy_string
        self.assertEqual(result1, "hello world")
        
        result2 = lazy_string + "!"
        self.assertEqual(result2, "world!")