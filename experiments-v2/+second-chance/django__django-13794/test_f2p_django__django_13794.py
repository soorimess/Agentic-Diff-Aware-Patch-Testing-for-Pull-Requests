from django.template.defaultfilters import add
from django.template import Context, Template
from django.utils.functional import lazy
from django.test import SimpleTestCase


def lazy_string_func():
    return "lazy_string"


class AddFilterLazyStringTest(SimpleTestCase):
    """
    Test that the add filter works correctly with lazy strings.
    Before the fix, this would raise TypeError: can only concatenate str 
    (not "__proxy__") to str
    """
    
    def test_add_filter_with_lazy_string(self):
        """Test that add filter works when adding a string to a lazy string"""
        # Create a lazy string
        lazy_string = lazy(lazy_string_func, str)()
        
        # This should not raise an exception
        result = add(lazy_string, " suffix")
        self.assertEqual(result, "lazy_string suffix")
        
    def test_add_filter_with_lazy_string_in_template(self):
        """Test that add filter works in template context with lazy string"""
        # Create a lazy string
        lazy_string = lazy(lazy_string_func, str)()
        
        # Create a template that uses the add filter
        template = Template("{{ value|add:postfix }}")
        context = Context({'value': lazy_string, 'postfix': " suffix"})
        
        # This should not raise an exception and should render correctly
        result = template.render(context)
        self.assertEqual(result.strip(), "lazy_string suffix")
        
    def test_add_filter_with_string_and_lazy_string(self):
        """Test that add filter works when adding a lazy string to a string"""
        # Create a lazy string
        lazy_string = lazy(lazy_string_func, str)()
        
        # This should not raise an exception
        result = add("prefix ", lazy_string)
        self.assertEqual(result, "prefix lazy_string")