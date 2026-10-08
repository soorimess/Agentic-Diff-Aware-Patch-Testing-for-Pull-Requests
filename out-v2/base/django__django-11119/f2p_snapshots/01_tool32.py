import unittest
from django.template import Context
from django.template.engine import Engine


class AutoescapeTest(unittest.TestCase):
    def test_render_to_string_honors_engine_autoescape_false(self):
        """
        Engine.render_to_string() should honor the autoescape attribute.
        When an engine is created with autoescape=False, render_to_string
        should not autoescape content.
        """
        # Create an engine with autoescape=False
        engine = Engine(autoescape=False, dirs=['tests/template_tests/templates'])
        
        # Test with a context containing HTML content
        context = {'content': '<b>bold text</b>'}
        
        # Render using the engine's render_to_string method with a template name
        result = engine.render_to_string('test_bug/autoescape_test.html', context)
        
        # With autoescape=False engine, the content should NOT be escaped
        # The result should contain the raw HTML tags, not escaped ones
        # This test should pass after the fix is applied
        self.assertIn('<b>bold text</b>', result)