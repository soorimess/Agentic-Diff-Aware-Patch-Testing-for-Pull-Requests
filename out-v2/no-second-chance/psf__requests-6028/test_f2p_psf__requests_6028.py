# -*- coding: utf-8 -*-
"""
Regression test for proxy authentication bug in Python 3.8.12.

This test ensures that prepend_scheme_if_needed properly handles URLs
with authentication components, which is critical for proxy authentication
to work correctly.
"""

import pytest
from requests.utils import prepend_scheme_if_needed


def test_prepend_scheme_if_needed_with_auth():
    """Test that prepend_scheme_if_needed preserves authentication in netloc."""
    # This is the case that was broken - URLs with auth should keep auth in netloc
    url_with_auth = 'http://user:pass@example.com/path'
    result = prepend_scheme_if_needed(url_with_auth, 'http')
    # The auth part should be preserved in the netloc
    assert result == 'http://user:pass@example.com/path'


def test_prepend_scheme_if_needed_with_auth_and_port():
    """Test that prepend_scheme_if_needed preserves authentication with port."""
    url_with_auth_and_port = 'http://user:pass@example.com:8080/path'
    result = prepend_scheme_if_needed(url_with_auth_and_port, 'http')
    # The auth part should be preserved in the netloc with port
    assert result == 'http://user:pass@example.com:8080/path'


def test_prepend_scheme_if_needed_without_auth():
    """Test that prepend_scheme_if_needed still works for URLs without auth."""
    url_without_auth = 'http://example.com/path'
    result = prepend_scheme_if_needed(url_without_auth, 'http')
    assert result == 'http://example.com/path'


def test_prepend_scheme_if_needed_already_has_scheme():
    """Test that prepend_scheme_if_needed doesn't double-scheme URLs."""
    url_with_scheme = 'http://user:pass@example.com/path'
    result = prepend_scheme_if_needed(url_with_scheme, 'https')
    assert result == 'http://user:pass@example.com/path'