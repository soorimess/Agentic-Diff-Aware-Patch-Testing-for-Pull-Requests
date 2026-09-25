# -*- coding: utf-8 -*-

"""
Regression test for psf/requests issue #6028 (proxy authentication bug).

This ensures that prepend_scheme_if_needed preserves authentication
information (user:pass@) in the netloc when a URL already contains a
scheme. Before the fix, calls such as:

    prepend_scheme_if_needed('http://user:pass@proxy:8080', 'http')

would drop the "user:pass@" part, which in turn prevented requests from
sending proxy authentication headers.

The correct behavior is to return the URL unchanged (i.e. preserving the
user:pass@ in the netloc).
"""

from requests.utils import prepend_scheme_if_needed


def test_prepend_scheme_preserves_auth_in_netloc():
    url = 'http://user:pass@proxy.example.com:8080'
    # The auth should be preserved in the netloc and the scheme should
    # remain http.
    assert prepend_scheme_if_needed(url, 'http') == url
