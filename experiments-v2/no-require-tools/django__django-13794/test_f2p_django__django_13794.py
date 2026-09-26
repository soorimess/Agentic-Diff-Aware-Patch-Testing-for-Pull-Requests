from django.template import Context, Template
from django.utils.functional import lazy
import unittest


def lazy_string():
    return "Hello"


class AddFilterLazyStringTest(unittest.TestCase):
    def test_add_filter_with_string_and_lazy_string(self):
        """Test that add filter works when string is first operand and lazy string is second."""
        # Create a lazy string
        lazy_str = lazy(lazy_string, str)()
        
        # This should not raise a TypeError and should return proper concatenation
        template = Template("{{ value|add:lazy_str }}")
        context = Context({'value': 'Hello', 'lazy_str': lazy_str})
        result = template.render(context)
        
        # The result should be "HelloHello", not an empty string
        self.assertEqual(result, "HelloHello")