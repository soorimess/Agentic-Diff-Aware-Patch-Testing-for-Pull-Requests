from django.test import SimpleTestCase
from django.template import Engine


class RenderToStringAutoescapeTests(SimpleTestCase):
    def test_render_to_string_honors_engine_autoescape(self):
        """Engine.render_to_string() should use Engine.autoescape for Context.

        Before the fix, Engine.render_to_string() created a Context without
        passing the engine's autoescape setting, causing output to be
        auto-escaped even when the engine was configured with autoescape=False.
        """
        engine = Engine(
            loaders=[('django.template.loaders.locmem.Loader', {
                'test_template.html': '{{ value }}',
            })],
            autoescape=False,
        )
        output = engine.render_to_string('test_template.html', {'value': '<b>bold</b>'})
        # Expect unescaped output when engine.autoescape is False
        self.assertEqual(output, '<b>bold</b>')
