from django.test import SimpleTestCase
from django.test.utils import ignore_warnings
import base64

from django.contrib.sessions.backends.base import SessionBase
from django.utils.deprecation import RemovedInDjango40Warning


class SessionsEncodeLegacyFormatTests(SimpleTestCase):

    def test_encode_uses_legacy_format_when_default_hashing_algorithm_is_sha1(self):
        with ignore_warnings(category=RemovedInDjango40Warning):
            with self.settings(DEFAULT_HASHING_ALGORITHM='sha1'):
                session = SessionBase()
                data = {'foo': 'bar', 'baz': 1}
                encoded = session.encode(data)

                # Legacy format: base64.b64encode(<hash>:<serialized>)
                serialized = session.serializer().dumps(data)
                expected_hash = session._hash(serialized)
                expected = base64.b64encode(expected_hash.encode() + b':' + serialized).decode('ascii')

                self.assertEqual(encoded, expected)
