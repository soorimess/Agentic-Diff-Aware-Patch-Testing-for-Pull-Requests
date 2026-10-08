from django.template import Engine, Context
from django.test import TestCase


class RenderToStringAutoescapeTest(TestCase):
    def test_engine_autoescape_setting_ignored(self):
        """
        Demonstrates that Engine.render_to_string() ignores the autoescape setting.
        This test shows the exact behavior that should be fixed.
        """
        # Create engine with autoescape=False
        engine = Engine(autoescape=False)
        
        # The bug: Context(context) doesn't pass autoescape parameter
        # So even with autoescape=False on engine, content gets autoescaped
        context_buggy = Context({'content': '<script>alert("xss")</script>'})
        context_correct = Context({'content': '<script>alert("xss")</script>'}, autoescape=engine.autoescape)
        
        # The test shows the difference - when autoescape=False is set,
        # both approaches should produce the same result (unescaped)
        # But currently they don't because of the bug
        template = engine.from_string('{{ content }}')
        result_buggy = template.render(context_buggy)
        result_correct = template.render(context_correct)
        
        # This assertion would pass once the bug is fixed
        # For now it fails, showing the bug exists
        self.assertEqual(result_buggy, result_correct)