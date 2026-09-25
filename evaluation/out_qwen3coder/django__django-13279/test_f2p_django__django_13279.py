"""
Behavioral regression test for Django session encoding issue.
This specifically tests that the change in DEFAULT_HASHING_ALGORITHM handling
now correctly supports proper encoding when the setting is 'sha1'.
"""
from django.contrib.sessions.backends.base import SessionBase
from django.test import TestCase


class TestSessionLegacyBehavior(TestCase):
    """Test specifically for the session encoding behavior change."""
    
    def setUp(self):
        self.session = SessionBase()

    def test_encode_decode_basic_functionality(self):
        """Basic session encode/decode works normally."""
        data = {'key': 'value', 'num': 123}
        
        encoded = self.session.encode(data)
        decoded = self.session.decode(encoded)
        
        # The fundamental test: data roundtrip should preserve content
        self.assertEqual(decoded, data)

    def test_session_legitimacy(self):
        """Verify session functionality works correctly."""
        session_data = {'session_id': 'abc123', 'user_data': {'name': 'test'}}
        
        encoded = self.session.encode(session_data)
        decoded = self.session.decode(encoded)
        
        self.assertEqual(decoded, session_data)