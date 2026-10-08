import unittest
from django.template.engine import Engine


class EngineAutoescapeTest(unittest.TestCase):
    def test_render_to_string_autoescape_behavior(self):
        """
        Test that demonstrates the autoescape behavior difference.
        This test will fail before the fix and pass after the fix.
        """
        # Create engines with different autoescape settings
        engine_false = Engine(autoescape=False, loaders=[('django.template.loaders.locmem.Loader', {
            'test_template.html': '<p>{{ content }}</p>'
        })])
        
        engine_true = Engine(autoescape=True, loaders=[('django.template.loaders.locmem.Loader', {
            'test_template.html': '<p>{{ content }}</p>'
        })])
        
        # Context with content that would be escaped
        context_data = {'content': '<script>alert("xss")</script>'}
        
        # Render using both engines
        result_false = engine_false.render_to_string('test_template.html', context_data)
        result_true = engine_true.render_to_string('test_template.html', context_data)
        
        # The key insight: with autoescape=False, we should get unescaped content
        # with autoescape=True, we should get escaped content
        # This test is designed to catch the bug where autoescape=False is ignored
        # For now, we just verify that the behavior is consistent with the bug
        # The test will pass after the fix is applied because the behavior will change
        
        # Both should contain the same content pattern but the test validates
        # that the fix makes a difference
        self.assertIn('<script>', result_false)