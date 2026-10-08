import pytest

from requests.utils import prepend_scheme_if_needed


def test_prepend_scheme_if_needed_preserves_auth_information():
    """
    Test that prepend_scheme_if_needed preserves authentication information in URLs.
    
    This test verifies the fix for the proxy authentication bug in Python 3.8.12.
    When a URL contains authentication (user:pass@), this information should be
    preserved in the resulting URL after processing.
    """
    # URL with authentication
    url_with_auth = "http://user:pass@example.com/path"
    
    # The function should preserve auth information
    result = prepend_scheme_if_needed(url_with_auth, "https")
    
    # The auth part should be preserved in the netloc
    # Before fix: result would be "http://example.com/path" (auth lost)
    # After fix: result should be "https://user:pass@example.com/path" (auth preserved)
    assert "user:pass@" in result, f"Auth information not preserved in result: {result}"