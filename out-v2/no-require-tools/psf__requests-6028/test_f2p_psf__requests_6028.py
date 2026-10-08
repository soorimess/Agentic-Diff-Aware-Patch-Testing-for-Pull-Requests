# -*- coding: utf-8 -*-
"""
Regression test for proxy authentication bug in Python 3.8.12.

This test ensures that when a URL contains authentication information,
the prepend_scheme_if_needed function properly includes the authentication
in the netloc when reconstructing the URL.
"""

import pytest
from requests.utils import prepend_scheme_if_needed


def test_prepend_scheme_if_needed_with_auth():
    """Test that authentication information is preserved in netloc."""
    # Test case with authentication in URL with scheme
    url_with_auth = "http://user:pass@example.com:8080/path"
    result = prepend_scheme_if_needed(url_with_auth, "http")
    # The auth should be preserved in the netloc part
    expected = "http://user:pass@example.com:8080/path"
    assert result == expected


def test_prepend_scheme_if_needed_without_auth():
    """Test that URLs without authentication work as before."""
    # Test case without authentication
    url_without_auth = "http://example.com:8080/path"
    result = prepend_scheme_if_needed(url_without_auth, "http")
    expected = "http://example.com:8080/path"
    assert result == expected


def test_prepend_scheme_if_needed_simple_url():
    """Test that simple URLs work as before."""
    url = "example.com/path"
    result = prepend_scheme_if_needed(url, "http")
    expected = "http://example.com/path"
    assert result == expected