from django.template import Engine
from django.test import SimpleTestCase


class RenderToStringAutoescapeTests(SimpleTestCase):
    def test_render_to_string_honors_engine_autoescape(self):
        """Engine.render_to_string() should use the engine.autoescape setting

        When a plain dict is passed as the context, render_to_string() must
        create a Context that inherits the engine's autoescape setting. Before
        the bugfix this used the Context default (autoescape=True) which meant
        Engine(autoescape=False).render_to_string(...) incorrectly produced
        escaped output.
        """
        templates = {'test.html': '{{ var }}'}

        engine = Engine(
            loaders=[('django.template.loaders.locmem.Loader', templates)],
            autoescape=False,
        )
        output = engine.render_to_string('test.html', {'var': '<b>hello</b>'})
        # With autoescape disabled on the engine, the variable should NOT be escaped.
        self.assertEqual(output, '<b>hello</b>')

        # Sanity-check the opposite behaviour still holds.
        engine2 = Engine(
            loaders=[('django.template.loaders.locmem.Loader', templates)],
            autoescape=True,
        )
        output2 = engine2.render_to_string('test.html', {'var': '<b>hello</b>'})
        self.assertEqual(output2, '&lt;b&gt;hello&lt;/b&gt;')
