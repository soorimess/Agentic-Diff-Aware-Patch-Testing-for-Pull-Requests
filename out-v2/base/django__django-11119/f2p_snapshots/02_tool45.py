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
        
        # The key test: when autoescape=False engine is used, 
        # the content should NOT be escaped (i.e., we should see the raw HTML)
        # The result should contain the unescaped HTML, not the escaped version
        # The escaped version would be <b>bold text</b>
        # The unescaped version would be <b>bold text</b>
        
        # With the bug (before fix): Context(context) defaults to autoescape=True, so it's escaped
        # With the fix: Context(context, autoescape=self.autoescape) uses engine's setting
        self.assertIn('<b>bold text</b>', result)