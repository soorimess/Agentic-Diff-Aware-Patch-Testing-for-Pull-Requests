from django.contrib.sessions.backends.base import SessionBase
from django.test import SimpleTestCase
from django.test.utils import ignore_warnings
from django.utils.deprecation import RemovedInDjango40Warning


class SessionEncodeLegacyHashingAlgorithmTests(SimpleTestCase):
    @ignore_warnings(category=RemovedInDjango40Warning)
    def test_encode_uses_legacy_format_when_default_hashing_algorithm_is_sha1(self):
        session = SessionBase()
        data = {'a test key': 'a test value'}

        with self.settings(
            DEFAULT_HASHING_ALGORITHM='sha1',
            SECRET_KEY='django_tests_secret_key',
        ):
            encoded = session.encode(data)
            self.assertEqual(session._legacy_decode(encoded), data)
