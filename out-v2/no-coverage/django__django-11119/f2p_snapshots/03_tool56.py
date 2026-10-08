import unittest
from django.template.engine import Engine


class EngineAutoescapeTest(unittest.TestCase):
    def test_render_to_string_honors_autoescape_false(self):
        """
        Test that Engine.render_to_string() honors autoescape=False setting.
        This test will fail before the fix and pass after the fix.
        """
        # Create an engine with autoescape disabled
        engine = Engine(autoescape=False, loaders=[('django.template.loaders.locmem.Loader', {
            'test_template.html': '{{ content }}'
        })])
        
        # Context with HTML content that should be escaped if autoescape=True
        context_data = {'content': '<script>alert("xss")</script>'}
        
        # Render using the engine with autoescape=False
        result = engine.render_to_string('test_template.html', context_data)
        
        # The test verifies that when autoescape=False, the content is not escaped
        # This test will pass once the fix is applied
        # Before the fix, it fails because autoescape=False is ignored
        # The result should contain unescaped HTML
        self.assertIn('<script>alert("xss")</script>', result)