from django.test import SimpleTestCase

from django.template.engine import Engine


class RenderToStringAutoescapeTests(SimpleTestCase):
    def test_render_to_string_honors_engine_autoescape(self):
        templates = {'hello.html': 'Hello, {{ name }}'}
        loaders = [
            ('django.template.loaders.cached.Loader', [
                ('django.template.loaders.locmem.Loader', templates),
            ]),
        ]
        engine = Engine(loaders=loaders, autoescape=False)
        # When autoescape is False on the engine, render_to_string should
        # not escape the variable output.
        output = engine.render_to_string('hello.html', {'name': 'Bob & Jim'})
        self.assertEqual(output, 'Hello, Bob & Jim')
