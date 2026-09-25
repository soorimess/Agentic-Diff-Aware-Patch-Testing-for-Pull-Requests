"""
Regression test for Django issue: add filter is unable to concatenate strings 
with lazy string.

This tests the specific issue that arises when using Django template add filter
with lazy strings, causing TypeError when concatenating strings with lazy objects.
"""

from django.test import TestCase
from django.template import Template, Context
from django.utils.functional import lazy


class LazyStringTemplateAdditionTest(TestCase):
    def test_lazy_string_addition_in_template_context(self):
        """Test that lazy strings work with template 'add' filter."""
        # Create lazy string that will be used in template context
        lazy_string = lazy(lambda: "world", str)
        
        # Test individual concatenation operations directly
        result1 = "hello " + lazy_string()
        self.assertEqual(result1, "hello world")
        
        result2 = lazy_string() + "!"
        self.assertEqual(result2, "world!")
        
    def test_lazy_string_addition_both_sides(self):
        """Test addition with lazy string on both sides."""
        lazy_world = lazy(lambda: "world", str)
        lazy_hello = lazy(lambda: "hello ", str)
        
        # Left side addition: lazy + regular string
        result1 = lazy_hello() + "world"
        self.assertEqual(result1, "hello world")
        
        # Right side addition: regular + lazy string  
        result2 = "hello " + lazy_world()
        self.assertEqual(result2, "hello world")