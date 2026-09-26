from django.template.defaultfilters import add
from django.utils.functional import lazy, lazystr
from django.test import SimpleTestCase


class AddFilterLazyStringTest(SimpleTestCase):
    """
    Test that the add filter can concatenate strings with lazy strings.
    This is a regression test for Django issue #13794.
    """

    def test_add_filter_with_lazy_string(self):
        """Test that adding a string to a lazy string works correctly."""
        # Create a lazy string using lazystr (the proper way)
        lazy_string = lazystr("hello")
        
        # This should work - concatenating a regular string with a lazy string
        result = add("world", lazy_string)
        self.assertEqual(result, "worldhello")

    def test_add_filter_with_lazy_string_reverse(self):
        """Test that adding a lazy string to a regular string works correctly."""
        # Create a lazy string using lazystr (the proper way)
        lazy_string = lazystr("world")
        
        # This should work - concatenating a lazy string with a regular string  
        result = add(lazy_string, "hello")
        self.assertEqual(result, "worldhello")