from django.template.defaultfilters import add
from django.test import SimpleTestCase
from django.utils.functional import lazy


def lazy_string_func():
    return "world"


class AddLazyStringTests(SimpleTestCase):
    """
    Regression test for Django issue where add filter is unable to 
    concatenate strings with lazy strings.
    
    Before the fix: concatenating string + lazy string would result in empty string
    After the fix: concatenating string + lazy string should work correctly
    """

    def test_add_string_with_lazy_string(self):
        """Test that adding a string with a lazy string works correctly."""
        # Create a lazy string
        lazy_string = lazy(lazy_string_func, str)
        
        # Test with string + lazy string
        result = add("hello ", lazy_string())
        self.assertEqual(result, "hello world")
        
        # Test with lazy string + string  
        result = add(lazy_string(), " world")
        self.assertEqual(result, "world world")

    def test_add_filter_template_context(self):
        """Test that the add template filter works with lazy strings in templates."""
        from django.template import Context, Template
        
        # Create a lazy string
        lazy_string = lazy(lazy_string_func, str)
        
        # Test template with string + lazy string
        template = Template("{{ value|add:lazy_value }}")
        context = Context({'value': 'hello ', 'lazy_value': lazy_string()})
        result = template.render(context)
        self.assertEqual(result, 'hello world')
        
        # Test template with lazy string + string
        template = Template("{{ lazy_value|add:value }}")
        context = Context({'value': ' world', 'lazy_value': lazy_string()})
        result = template.render(context)
        self.assertEqual(result, 'world world')