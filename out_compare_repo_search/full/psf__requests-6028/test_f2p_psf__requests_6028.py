# -*- coding: utf-8 -*-

from requests.utils import prepend_scheme_if_needed


def test_prepend_scheme_if_needed_preserves_auth_in_netloc():
    """Ensure auth in a schemeless URL is preserved when a scheme is prepended.

    This caught a regression where URLs like "//user:pass@proxy:3128" would
    lose the user:pass portion after calling prepend_scheme_if_needed(..., 'http'),
    which in turn caused proxy authentication to be omitted.
    """
    url = "//user:pass@proxy.example.com:3128"
    result = prepend_scheme_if_needed(url, 'http')
    assert result == "http://user:pass@proxy.example.com:3128"
