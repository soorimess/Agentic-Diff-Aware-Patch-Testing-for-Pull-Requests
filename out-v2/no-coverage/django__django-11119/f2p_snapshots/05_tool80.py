import unittest
from django.template.engine import Engine


class EngineAutoescapeTest(unittest.TestCase):
    def test_render_to_string_honors_autoescape_false(self):
        """
        Test that Engine.render_to_string() honors autoescape=False setting.
        This test fails before the fix and passes after the fix.
        """
        # Create engine with autoescape disabled
        engine = Engine(autoescape=False, loaders=[('django.template.loaders.locmem.Loader', {
            'test_template.html': '{{ content }}'
        })])
        
        # Context with HTML content that would be escaped
        context_data = {'content': '<script>alert("xss")</script>'}
        
        # Render using the engine
        result = engine.render_to_string('test_template.html', context_data)
        
        # The key test: when autoescape=False, the HTML should NOT be escaped
        # This test will fail before the fix because autoescape=False is ignored
        # and the content is always escaped
        # After the fix, it should pass because autoescape=False is honored
        self.assertIn('<script>alert("xss")</script>', result)