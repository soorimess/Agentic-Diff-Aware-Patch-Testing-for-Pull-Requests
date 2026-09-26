from django.template.defaultfilters import add
from django.test import SimpleTestCase
from django.utils.functional import lazy


class AddFilterLazyStringTest(SimpleTestCase):
    """
    Test that the add filter works correctly with lazy strings.
    Before the fix, concatenating a string with a lazy string would raise
    TypeError: can only concatenate str (not "__proxy__") to str or return empty string.
    """

    def test_add_string_with_lazy_string(self):
        """Test adding a regular string with a lazy string."""
        # Create a lazy string using django.utils.functional.lazy
        lazy_string = lazy(lambda: "world", str)
        
        # This should work after the fix - the lazy string should be properly concatenated
        result = add("hello ", lazy_string())
        self.assertEqual(result, "hello world")

    def test_add_lazy_string_with_string(self):
        """Test adding a lazy string with a regular string."""
        # Create a lazy string using django.utils.functional.lazy
        lazy_string = lazy(lambda: "hello", str)
        
        # This should work after the fix
        result = add(lazy_string(), " world")
        self.assertEqual(result, "hello world")

    def test_add_lazy_string_with_lazy_string(self):
        """Test adding a lazy string with another lazy string."""
        # Create two lazy strings
        lazy_string1 = lazy(lambda: "hello ", str)
        lazy_string2 = lazy(lambda: "world", str)
        
        # This should work after the fix
        result = add(lazy_string1(), lazy_string2())
        self.assertEqual(result, "hello world")