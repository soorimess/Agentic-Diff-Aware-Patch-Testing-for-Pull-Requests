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
            'test_template.html': '<p>{{ content }}</p>'
        })])
        
        # Context with HTML content that should be escaped if autoescape=True
        context_data = {'content': '<script>alert("xss")</script>'}
        
        # Render using the engine with autoescape=False
        result = engine.render_to_string('test_template.html', context_data)
        
        # The key insight: the bug is that autoescape=False is ignored
        # So both autoescape=False and autoescape=True produce same result
        # The result should contain escaped content (<script>)
        # But if the fix works, we should see different behavior
        self.assertIn('<script>', result)