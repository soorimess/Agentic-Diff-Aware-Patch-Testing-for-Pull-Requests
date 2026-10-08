import os
import unittest

from django.template import Context
from django.template.engine import Engine


class TestEngineAutoescape(unittest.TestCase):
    def test_render_to_string_ignores_autoescape_false(self):
        """
        Engine.render_to_string() should honor the autoescape attribute.
        When an engine is created with autoescape=False, render_to_string
        should not autoescape content.
        """
        # Create an engine with autoescape=False
        engine = Engine(autoescape=False, dirs=['tests/template_tests/templates'])
        
        # Test content that would normally be escaped
        test_content = '<script>alert("xss")</script>'
        
        # Render using render_to_string with existing template
        result = engine.render_to_string('test_context.html', {'obj': test_content})
        
        # With autoescape=False, the content should NOT be escaped
        # But currently it is (the bug)
        # This test will fail with the bug, and pass after the fix
        self.assertIn('<script>alert("xss")</script>', result)
        
    def test_render_to_string_with_context_autoescape_false(self):
        """
        Engine.render_to_string() correctly handles autoescape when Context is passed.
        """
        # Create an engine with autoescape=False
        engine = Engine(autoescape=False, dirs=['tests/template_tests/templates'])
        
        # Test content that would normally be escaped
        test_content = '<script>alert("xss")</script>'
        
        # Create a Context with autoescape=False
        context = Context({'obj': test_content}, autoescape=False)
        
        # Render using render_to_string with a Context
        result = engine.render_to_string('test_context.html', context)
        
        # When Context is passed directly with autoescape=False, it works correctly
        # We should see the raw HTML (not escaped)
        self.assertIn('<script>alert("xss")</script>', result)