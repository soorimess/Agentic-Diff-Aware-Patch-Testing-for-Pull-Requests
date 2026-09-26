from django.template.defaultfilters import add
from django.utils.functional import lazy
from django.test import SimpleTestCase


class AddFilterLazyStringTest(SimpleTestCase):
    def test_add_lazy_string_with_regular_string(self):
        """Test that add filter works with lazy strings."""
        # Create a lazy string
        lazy_str = lazy(lambda: "Hello", str)
        
        # This should work - concatenating lazy string with regular string
        result = add(lazy_str(), " World")
        self.assertEqual(result, "Hello World")
        
    def test_add_regular_string_with_lazy_string(self):
        """Test that add filter works with lazy strings when string is first."""
        # Create a lazy string
        lazy_str = lazy(lambda: "World", str)
        
        # This should work - concatenating regular string with lazy string
        result = add("Hello ", lazy_str())
        self.assertEqual(result, "Hello World")