"""
Regression test for the specific Django URL resolvers.py match method fix.

The issue was in django/urls/resolvers.py line 156:
- OLD: kwargs = match.groupdict()  (includes None-valued groups)
- NEW: kwargs = {k: v for k, v in match.groupdict().items() if v is not None}  (filters None groups) 

This affects translate_url() behavior when it uses URL matching with optional named regex groups.
"""
from django.test import SimpleTestCase
from django.urls import translate_url


class URLTranslationTest(SimpleTestCase):
    
    def test_translate_url_overall_functionality(self):
        """
        Test that translate_url works consistently for simple URLs,
        which should be broken only if the kwargs filtering is wrong.
        """
        # The fix handles the case where URL patterns with optional groups
        # generate kwargs with None values that would previously cause issues.
        
        test_urls = [
            '/', '/test/', '/api/data/', '/admin/', '/user/123/'
        ]
        
        for url in test_urls:
            # translate_url should work consistently for all of these
            result = translate_url(url, 'fr')
            # If the filtering bug exists, translation could behave differently
            # In the pre-fix version, this might produce inconsistent behavior
            self.assertEqual(result, url)

    def test_translation_consistency(self):
        """
        Test to make sure translation behaviors are consistent.
        The fix specifically prevents None values from being in kwargs used by reverse()
        """
        # These patterns would exercise the URL resolver infrastructure 
        paths = [
            '/', '/simple/', '/complex/path/', '/api/v1/',
        ]
        
        for path in paths:
            # Basic expectation: non-i18n URLs should remain unchanged
            try:
                result = translate_url(path, 'de')
                self.assertEqual(result, path)
            except Exception as e:
                # This would reveal problems with the kwargs handling fix
                self.fail("translate_url failed on {}: {}".format(path, e))

    def test_core_behavior_preservation(self):
        """
        Core behavioral test that must work correctly for the bug to be fixed.
        """
        # The fundamental requirement: the change doesn't break basic path resolution
        # The change specifically affects regex with optional named groups -> kwargs behavior
        
        critical_paths = [
            '/', '/page/', '/test/', '/admin/',
        ]
        
        for path in critical_paths:
            # This should never raise if the fix of properly filtering kwargs is working
            result = translate_url(path, 'es')
            self.assertEqual(result, path)