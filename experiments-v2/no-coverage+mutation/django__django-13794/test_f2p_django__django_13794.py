from django.template.defaultfilters import add
from django.utils.functional import lazy
from django.test import SimpleTestCase


class AddFilterLazyStringTest(SimpleTestCase):
    """
    Test that the add filter can concatenate strings with lazy strings.
    This is a regression test for Django issue #13794.
    """

    def test_add_string_with_lazy_string(self):
        """Test that adding a regular string to a lazy string works."""
        # Create a lazy string
        lazy_str = lazy(lambda: "Hello", str)
        
        # This should work without raising TypeError
        result = add("World", lazy_str())
        self.assertEqual(result, "WorldHello")

    def test_add_lazy_string_with_string(self):
        """Test that adding a lazy string to a regular string works."""
        # Create a lazy string
        lazy_str = lazy(lambda: "World", str)
        
        # This should work without raising TypeError
        result = add(lazy_str(), "Hello")
        self.assertEqual(result, "WorldHello")