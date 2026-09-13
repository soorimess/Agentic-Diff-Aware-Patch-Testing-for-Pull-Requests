import requests


def test_not_send_content_length_for_get_and_head_but_send_for_others():
    """GET and HEAD should not include a Content-Length header when no body.

    Before the fix this library always set Content-Length to "0" which caused
    servers (e.g. some Amazon endpoints) to reject GET requests that included
    a Content-Length header. This test asserts that GET and HEAD requests do
    not contain the header, while other methods (POST) still include it as
    "0" when no body is provided.
    """
    get_req = requests.Request('GET', 'http://example.com').prepare()
    head_req = requests.Request('HEAD', 'http://example.com').prepare()
    post_req = requests.Request('POST', 'http://example.com').prepare()

    # GET and HEAD must not send Content-Length when there's no body.
    assert 'Content-Length' not in get_req.headers
    assert 'Content-Length' not in head_req.headers

    # POST (and other non-GET/HEAD methods) should include Content-Length == '0'.
    assert 'Content-Length' in post_req.headers
    assert post_req.headers['Content-Length'] == '0'
