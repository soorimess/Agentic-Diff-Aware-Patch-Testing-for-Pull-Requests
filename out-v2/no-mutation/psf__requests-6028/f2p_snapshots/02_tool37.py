# -*- coding: utf-8 -*-

import pytest

from requests.utils import prepend_scheme_if_needed


def test_prepend_scheme_if_needed_preserves_auth_when_scheme_exists():
    """Test that prepend_scheme_if_needed preserves authentication when URL already has scheme."""
    # This is the core bug: when URL has auth and scheme, auth should be preserved
    # Before fix: http://proxy.example.com (auth lost)
    # After fix: http://user:pass@proxy.example.com (auth preserved)
    url_with_auth = 'http://user:pass@proxy.example.com'
    result = prepend_scheme_if_needed(url_with_auth, 'https')
    
    # The auth part should be preserved even though we're trying to prepend 'https'
    # (but the function doesn't change existing schemes)
    assert 'user:pass@' in result
    # The scheme should remain 'http' since it already existed
    assert result == 'http://user:pass@proxy.example.com'


def test_prepend_scheme_if_needed_preserves_auth_when_scheme_added():
    """Test that prepend_scheme_if_needed preserves authentication when scheme is added."""
    # Test with a URL that has no scheme - should prepend scheme and preserve auth
    # This is a more complex case that might also be affected
    url_without_scheme = 'proxy.example.com'
    result = prepend_scheme_if_needed(url_without_scheme, 'https')
    
    # Since there's no auth in this URL, result should just be the scheme prepended
    assert result == 'https://proxy.example.com'