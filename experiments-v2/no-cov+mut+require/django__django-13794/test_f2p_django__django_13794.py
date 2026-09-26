from django.template.defaultfilters import add
from django.utils.functional import lazy
from django.test import SimpleTestCase


def lazy_string_func():
    return "Hello"


class AddFilterLazyStringTest(SimpleTestCase):
    """
    Test that the add filter can concatenate strings with lazy strings.
    This is a regression test for Django issue #13794.
    """

    def test_add_filter_concatenates_lazy_string_with_regular_string(self):
        """Test that add filter works when lazy string is on the right side."""
        # Create a lazy string
        lazy_string = lazy(lazy_string_func, str)
        
        # Test concatenating regular string with lazy string  
        result = add("Hello ", lazy_string())
        self.assertEqual(result, "Hello Hello")