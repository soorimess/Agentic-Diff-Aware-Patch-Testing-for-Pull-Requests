from django.template import Context, Template
from django.test import SimpleTestCase
from django.utils.functional import lazy
from django.utils.translation import gettext_lazy


class AddFilterLazyStringTest(SimpleTestCase):
    """
    Test for Django issue where add filter fails with lazy strings.
    Before the fix: TypeError: can only concatenate str (not "__proxy__") to str
    After the fix: Should properly concatenate strings with lazy strings
    """
    
    def test_add_string_with_lazy_string(self):
        """Test adding a regular string with a lazy string using add filter."""
        # Create a lazy string
        lazy_str = gettext_lazy('hello')
        
        # This should work - concatenate string with lazy string
        template = Template('{{ var|add:lazy_var }}')
        context = Context({'var': 'world', 'lazy_var': lazy_str})
        result = template.render(context)
        
        # Should properly concatenate to 'worldhello'
        self.assertEqual(result, 'worldhello')
    
    def test_add_lazy_string_with_string(self):
        """Test adding a lazy string with a regular string using add filter."""
        # Create a lazy string  
        lazy_str = gettext_lazy('hello')
        
        # This should also work - concatenate lazy string with string
        template = Template('{{ lazy_var|add:var }}')
        context = Context({'var': 'world', 'lazy_var': lazy_str})
        result = template.render(context)
        
        # Should properly concatenate to 'helloworld'
        self.assertEqual(result, 'helloworld')
        
    def test_add_lazy_string_with_lazy_string(self):
        """Test adding lazy string with another lazy string."""
        # Create two lazy strings
        lazy_str1 = gettext_lazy('hello')
        lazy_str2 = gettext_lazy('world')
        
        # This should work - concatenate two lazy strings
        template = Template('{{ lazy_var1|add:lazy_var2 }}')
        context = Context({'lazy_var1': lazy_str1, 'lazy_var2': lazy_str2})
        result = template.render(context)
        
        # Should properly concatenate to 'helloworld'
        self.assertEqual(result, 'helloworld')
    
    def test_add_number_with_lazy_string(self):
        """Test adding a number with a lazy string."""
        # Create a lazy string
        lazy_str = gettext_lazy('test')
        
        # This should work - when the lazy string gets converted to string, it should concatenate
        template = Template('{{ var|add:lazy_var }}')
        context = Context({'var': 123, 'lazy_var': lazy_str})
        result = template.render(context)
        
        # Should properly concatenate to '123test'
        self.assertEqual(result, '123test')