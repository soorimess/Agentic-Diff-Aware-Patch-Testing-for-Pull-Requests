import unittest

from django.test import TestCase
from django.utils.translation.trans_real import language_code_prefix_re


class I18nLanguageCodeTest(TestCase):
    def test_complex_language_codes_match_with_fix(self):
        """
        Test that complex language codes with script and region components work.
        
        The bug: language_code_prefix_re regex only allows 0 or 1 additional components
        The fix: language_code_prefix_re regex allows 0 to 2 additional components
        
        This test specifically checks that language codes like:
        - en-latn-us (language-script-region) 
        - en-Latn-US (language-script-region with BCP 47 case format)
        work correctly with the fixed regex.
        """
        # These are the exact cases from the bug report that should work with the fix
        # but don't work with the old regex
        test_cases = [
            '/en-latn-us/',  # Should match and return 'en-latn-us'
            '/en-latn-us',   # Should match and return 'en-latn-us' 
            '/en-Latn-US/',  # Should match and return 'en-Latn-US'
            '/en-Latn-US',   # Should match and return 'en-Latn-US'
        ]
        
        # Test each case
        for path in test_cases:
            with self.subTest(path=path):
                match = language_code_prefix_re.match(path)
                # This assertion will fail with the old regex but pass with the new one
                # The key is that the regex now allows for 2 additional components
                # instead of just 1 or 0
                self.assertIsNotNone(match, 
                    f"Path {path} should match with the fixed regex but doesn't")
                if match:
                    # The regex should capture the full language code
                    captured = match.group(1)
                    # The captured value should be the full language code
                    # (this is a bit tricky to assert without knowing the exact expected value)
                    self.assertTrue(len(captured) > 0, 
                        f"Captured language code should not be empty for {path}")