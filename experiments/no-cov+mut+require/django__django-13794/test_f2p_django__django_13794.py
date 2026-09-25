"""
Regression test for Django issue where the add template filter
fails to concatenate strings with lazy strings.
"""
from django.template import Context, Template
from django.utils.functional import lazy
from django.test import SimpleTestCase


def get_lazy_string():
    """A lazy function that returns a string."""
    return "lazy"


class AddFilterLazyStringTests(SimpleTestCase):
    
    def test_add_filter_with_lazy_string(self):
        """
        Test that the add filter can concatenate a regular string with a lazy string.
        Before the fix, this would raise a TypeError: can only concatenate str (not "__proxy__") to str
        """
        # Create a lazy string using the lazy function  
        lazy_str = lazy(get_lazy_string, str)()
        
        # This should not raise an exception and should concatenate properly  
        template = Template("{{ value|add:lazy_value }}")
        context = Context({'value': 'regular', 'lazy_value': lazy_str})
        result = template.render(context)
        
        # Should concatenate "regular" + "lazy" = "regularlazy"
        self.assertEqual(result, 'regularlazy')
    
    def test_radd_filter_with_lazy_string(self):
        """
        Test that the add filter works when lazy string is on the left side.
        """
        # Create a lazy string using the lazy function  
        lazy_str = lazy(get_lazy_string, str)()
        
        # This should not raise an exception and should concatenate properly
        template = Template("{{ lazy_value|add:value }}")
        context = Context({'value': 'regular', 'lazy_value': lazy_str})
        result = template.render(context)
        
        # Should concatenate "lazy" + "regular" = "lazyregular"
        self.assertEqual(result, 'lazyregular')