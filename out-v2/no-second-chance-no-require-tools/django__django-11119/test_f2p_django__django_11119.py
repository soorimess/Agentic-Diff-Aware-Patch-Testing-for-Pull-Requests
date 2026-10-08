import unittest
from django.template import Context
from django.template.engine import Engine


class AutoescapeRenderToStringTest(unittest.TestCase):
    """Test that Engine.render_to_string() honors the autoescape attribute."""

    def test_render_to_string_honors_autoescape_false(self):
        """
        When an Engine is created with autoescape=False, 
        render_to_string should not autoescape content.
        """
        # Create an engine with autoescape disabled
        engine = Engine(autoescape=False, dirs=['tests/template_tests/templates'])
        
        # Test content that would be escaped if autoescape was True
        content = '<script>alert("xss")</script>'
        
        # This should not escape the HTML when autoescape=False
        result = engine.render_to_string('test_autoescape_content.html', {'content': content})
        
        # With autoescape=False, the content should not be escaped
        # So we should see raw HTML tags in the output
        self.assertIn('<script>', result)
        self.assertIn('alert("xss")', result)
        self.assertIn('</script>', result)

    def test_render_to_string_honors_autoescape_true(self):
        """
        When an Engine is created with autoescape=True (default),
        render_to_string should autoescape content.
        """
        # Create an engine with autoescape enabled (default)
        engine = Engine(autoescape=True, dirs=['tests/template_tests/templates'])
        
        # Test content that would be escaped if autoescape was True
        content = '<script>alert("xss")</script>'
        
        # This should escape the HTML when autoescape=True
        result = engine.render_to_string('test_autoescape_content.html', {'content': content})
        
        # With autoescape=True, the content should be escaped
        # So we should see escaped HTML in the output
        self.assertIn('<script>', result)
        self.assertIn('"xss"', result)
        self.assertIn('</script>', result)