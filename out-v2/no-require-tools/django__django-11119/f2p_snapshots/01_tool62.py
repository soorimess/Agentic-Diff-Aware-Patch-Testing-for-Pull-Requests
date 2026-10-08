import unittest
from django.template import Engine, Context


class RenderToStringAutoescapeTest(unittest.TestCase):
    """Test that Engine.render_to_string() honors the autoescape attribute."""

    def test_render_to_string_autoescape_false_dict_case(self):
        """
        Test that when a dict is passed to render_to_string with autoescape=False,
        the engine's autoescape setting is respected.
        """
        # Create an engine with autoescape=False
        engine = Engine(autoescape=False, loaders=[
            ('django.template.loaders.locmem.Loader', {
                'test_template.html': '{{ content }}'
            })
        ])
        
        # This is the problematic case - when we pass a dict, not a Context
        context = {'content': '<b>bold</b>'}
        
        # With the bug, this ignores engine.autoescape=False and always escapes
        # After the fix, it should respect engine.autoescape=False
        result = engine.render_to_string('test_template.html', context)
        
        # The key test: when autoescape=False, we should NOT see escaped HTML
        # This test will fail before the fix and pass after the fix
        self.assertIn('<b>', result)  # Should be present when autoescape=False

    def test_render_to_string_with_existing_context(self):
        """Test that render_to_string with existing Context object works correctly."""
        # Create an engine with autoescape=False
        engine = Engine(autoescape=False, loaders=[
            ('django.template.loaders.locmem.Loader', {
                'test_template.html': '{{ content }}'
            })
        ])
        
        # This works correctly - when we pass an explicit Context
        context = Context({'content': '<b>bold</b>'}, autoescape=False)
        
        # Render using render_to_string with existing Context
        result = engine.render_to_string('test_template.html', context)
        
        # With autoescape=False, the content should not be escaped
        self.assertIn('<b>', result)