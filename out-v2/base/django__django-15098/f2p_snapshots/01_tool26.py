import re
from django.test import SimpleTestCase
from django.utils.translation.trans_real import language_code_prefix_re


class LanguageCodePrefixRegexTest(SimpleTestCase):
    """
    Test the language_code_prefix_re regex to ensure it handles locale codes 
    with both script and region components correctly.
    """
    
    def test_regex_behavior_before_and_after_fix(self):
        """
        Test that demonstrates the difference between the old and new regex behavior.
        """
        # The current (broken) regex pattern
        current_pattern = r'^/(\w+([@-]\w+)?)(/|$)'
        # The fixed regex pattern  
        fixed_pattern = r'^/(\w+([@-]\w+){0,2})(/|$)'
        
        current_regex = re.compile(current_pattern)
        fixed_regex = re.compile(fixed_pattern)
        
        # Test cases that should work with both versions
        basic_cases = [
            '/en-us/',
            '/fr-fr/',
        ]
        
        # Test cases that should work with the fixed version but not the current version
        advanced_cases = [
            '/en-latn-us/',      # language-script-region
            '/en-Latn-US/',      # BCP 47 case format
            '/zh-hans-cn/',      # language-script-region
        ]
        
        # Test basic cases with both versions
        for case in basic_cases:
            current_match = current_regex.match(case)
            fixed_match = fixed_regex.match(case)
            self.assertIsNotNone(current_match, f"Basic case {case} should match with current regex")
            self.assertIsNotNone(fixed_match, f"Basic case {case} should match with fixed regex")
            
        # Test advanced cases - these should fail with current but pass with fixed
        for case in advanced_cases:
            current_match = current_regex.match(case)
            fixed_match = fixed_regex.match(case)
            
            # Current regex should NOT match these
            self.assertIsNone(current_match, 
                            f"Advanced case {case} should NOT match with current regex")
            
            # Fixed regex SHOULD match these
            self.assertIsNotNone(fixed_match, 
                               f"Advanced case {case} should match with fixed regex")
            
            # Both should capture the full language code
            if fixed_match:
                self.assertEqual(fixed_match.group(1), case[1:-1], 
                               f"Fixed regex should capture full language code for {case}")
    
    def test_language_code_prefix_re_current_behavior(self):
        """
        Test the current behavior of language_code_prefix_re to show the bug.
        """
        # These should work but currently don't due to the regex limitation
        problematic_cases = [
            '/en-latn-us/',
            '/en-Latn-US/',
        ]
        
        for case in problematic_cases:
            match = language_code_prefix_re.match(case)
            # This will fail with current code, and should pass after fix
            self.assertIsNotNone(match, 
                               f"language_code_prefix_re should match {case} (this will fail before fix)")
            
            # Verify it captures the full language code
            if match:
                captured = match.group(1)
                expected = case[1:-1]  # Remove leading / and trailing /
                self.assertEqual(captured, expected,
                               f"Captured language code should be {expected}, got {captured}")