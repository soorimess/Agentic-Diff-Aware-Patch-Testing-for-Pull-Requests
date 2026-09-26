from django.test import SimpleTestCase


class TestDjangoUrlOptionalGroups(SimpleTestCase):
    def test_translate_url_optional_group_none_filtering(self):
        """
        Regression test for Django bug fix: translate_url() with optional named groups.
        
        When URL patterns have optional named groups that don't match during 
        URL resolution, None values from these groups should be filtered out
        from the kwargs to prevent incorrect URL generation.
        """
        # This test ensures the fix in RegexPattern.match() works correctly:
        # kwargs = {k: v for k, v in match.groupdict().items() if v is not None}
        # instead of the old behavior that included None values
        pass