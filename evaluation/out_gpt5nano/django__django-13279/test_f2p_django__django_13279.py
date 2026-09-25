from django.test import TestCase, override_settings, ignore_warnings
from django.contrib.sessions.backends.db import SessionStore as DatabaseSession
from django.utils.deprecation import RemovedInDjango40Warning


class Django13279RegressionTests(TestCase):
    @ignore_warnings(category=RemovedInDjango40Warning)
    def test_legacy_encoding_path_used_when_sha1(self):
        # When DEFAULT_HASHING_ALGORITHM is 'sha1', encoding should use the
        # legacy path. The encoded data should not contain the signing ':'
        # delimiter present in the default (sha256) encoding.
        with override_settings(DEFAULT_HASHING_ALGORITHM='sha1'):
            s = DatabaseSession()
            encoded = s.encode({'a': 'b'})
            self.assertNotIn(':', encoded)

    @ignore_warnings(category=RemovedInDjango40Warning)
    def test_legacy_encode_method_exists_after_sha1_patch(self):
        # The patch introduces a _legacy_encode method for sha1 transitions.
        with override_settings(DEFAULT_HASHING_ALGORITHM='sha1'):
            s = DatabaseSession()
            self.assertTrue(hasattr(s, '_legacy_encode'))
