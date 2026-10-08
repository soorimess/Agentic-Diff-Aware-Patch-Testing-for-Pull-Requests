import unittest
from django.conf import settings
from django.test import TestCase


class I18nLanguageCodeTest(TestCase):
    def setUp(self):
        # Set up the test settings exactly as described in the bug report
        settings.LANGUAGE_CODE = 'en-us'
        settings.LANGUAGES = [
            ('en-us', "English"),
            ('en-latn-us', "Latin English"),
            ('en-Latn-US', "BCP 47 case format"),
        ]
        settings.USE_I18N = True

    def test_language_code_prefix_regex_limitation(self):
        """
        Regression test for Django issue #15098:
        Internationalisation didn't support language locale containing both script and region.
        
        The language_code_prefix_re regex pattern is too restrictive for language codes
        that contain both script and region components.
        """
        # Import the regex that causes the issue
        from django.utils.translation.trans_real import language_code_prefix_re
        
        # Test cases that currently fail due to the regex limitation
        # These are BCP 47 language tags with language + script + region (2 additional components needed)
        problematic_cases = [
            '/en-latn-us/',  # language-script-region - should work but currently fails
            '/en-Latn-US/',  # language-script-region - should work but currently fails
        ]
        
        # Test that these currently fail (demonstrating the bug)
        for case in problematic_cases:
            match = language_code_prefix_re.match(case)
            self.assertIsNone(match, 
                f"Current regex incorrectly fails to match {case} - this demonstrates the bug")
        
        # Test cases that work correctly with current regex (0 or 1 additional components)
        working_cases = [
            '/en-us/',       # language-region (1 additional component) 
            '/fr/',          # language only (0 additional components)
            '/de-de/',       # language-region (1 additional component)
        ]
        
        # Test that working cases still work
        for case in working_cases:
            match = language_code_prefix_re.match(case)
            self.assertIsNotNone(match, 
                f"Current regex should still allow {case}")