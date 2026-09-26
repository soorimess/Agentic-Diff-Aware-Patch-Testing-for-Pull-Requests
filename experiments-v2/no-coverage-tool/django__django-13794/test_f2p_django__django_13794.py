from django.template.defaultfilters import add
from django.utils.functional import lazy
from django.test import SimpleTestCase


class AddFilterLazyStringTest(SimpleTestCase):
    def test_add_string_with_lazy_string(self):
        """Test that add filter works with lazy strings - reproduces the bug report."""
        # Create a lazy string
        lazy_string = lazy(lambda: "hello", str)
        
        # This should not raise TypeError and should return "hellohello"
        result = add("hello", lazy_string())
        self.assertEqual(result, "hellohello")
        
        # Test with lazy string as first argument
        result2 = add(lazy_string(), " world")
        self.assertEqual(result2, "hello world")

    def test_add_string_with_lazy_string_in_template_context(self):
        """Test that add filter works with lazy strings in template context."""
        from django.template import Context, Template
        
        # Create a lazy string
        lazy_string = lazy(lambda: "lazy", str)
        
        # Test in template context - this is the exact scenario from the bug report
        template = Template("{{ value|add:lazy_value }}")
        context = Context({'value': 'hello ', 'lazy_value': lazy_string()})
        
        # This should render without error and produce the expected result
        result = template.render(context)
        self.assertEqual(result, 'hello lazy')