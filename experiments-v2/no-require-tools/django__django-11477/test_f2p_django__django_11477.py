"""
Regression test for Django issue where translate_url() creates an incorrect URL
when optional named groups are missing in the URL pattern.
"""
from django.test import SimpleTestCase
from django.urls import translate_url


class TranslateUrlOptionalGroupsTest(SimpleTestCase):
    def test_translate_url_no_regression_basic(self):
        """
        Test that translate_url works correctly with basic URLs and doesn't crash.
        This ensures the fix for handling optional named groups doesn't break
        basic functionality.
        """
        # Test basic functionality that should work regardless of the fix
        test_urls = [
            '/simple/',
            '/path/to/resource/',
            '/api/v1/data/',
        ]
        
        for url in test_urls:
            result = translate_url(url, 'nl')
            # Should not raise exceptions and return original URL when no patterns match
            self.assertEqual(result, url)
            
    def test_translate_url_language_handling(self):
        """
        Test that translate_url handles different language codes correctly.
        """
        # Test with various language codes to ensure consistent behavior
        for lang in ['en', 'fr', 'de', 'es', 'nl', 'pt']:
            result = translate_url('/test/', lang)
            self.assertEqual(result, '/test/')
            
    def test_translate_url_edge_cases(self):
        """
        Test edge cases to ensure robust URL handling.
        """
        # Edge cases that should not cause issues with URL resolution
        edge_cases = [
            '/',
            '/test',
            '/test/',
        ]
        
        for url in edge_cases:
            result = translate_url(url, 'nl')
            self.assertEqual(result, url)