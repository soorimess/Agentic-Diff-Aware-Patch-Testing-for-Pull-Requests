import unittest

from django.test import TestCase
from django.utils.translation.trans_real import language_code_prefix_re


class I18nLanguageCodeTest(TestCase):
    def test_complex_language_codes_now_work(self):
        """
        Test that language codes with script and region components work correctly.
        
        The bug: language_code_prefix_re regex only allowed 0 or 1 additional components,
        but RFC 5646 language tags can have up to 2 additional components 
        (language-script-region).
        
        This test verifies that complex language codes like:
        - en-latn-us (language-script-region) 
        - en-Latn-US (language-script-region with BCP 47 case format)
        now work with the fixed regex.
        """
        # These are the specific cases from the bug report that should now work
        complex_cases = [
            '/en-latn-us/',  # Should match with the fixed regex
            '/en-latn-us',   # Should match with the fixed regex 
            '/en-Latn-US/',  # Should match with the fixed regex
            '/en-Latn-US',   # Should match with the fixed regex
        ]
        
        # Test that these cases now match (they would fail with the old regex)
        for path in complex_cases:
            with self.subTest(path=path):
                match = language_code_prefix_re.match(path)
                # This assertion will pass with the fixed regex but fail with the old one
                self.assertIsNotNone(match, 
                    f"Path {path} should match with the fixed regex but doesn't")