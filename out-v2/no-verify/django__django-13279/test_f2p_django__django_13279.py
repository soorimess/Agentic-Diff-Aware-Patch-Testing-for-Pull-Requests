from django.conf import settings
from django.contrib.sessions.backends.base import SessionBase
from django.test import SimpleTestCase
from django.utils.deprecation import RemovedInDjango40Warning
from django.test.utils import ignore_warnings


class TestSessionEncoding(SimpleTestCase):
    """
    Regression test for Django issue #13279.
    Session data cannot be decoded during the transition to Django 3.1.
    This test ensures that session data can be properly encoded and decoded
    during the transition period when DEFAULT_HASHING_ALGORITHM is set to 'sha1'.
    """
    
    def test_encode_decode_session_data(self):
        """
        Test that session data can be encoded and decoded properly.
        This test verifies the core functionality that was broken in the transition.
        """
        # Create a session base instance
        session = SessionBase()
        
        # Test with various data types that might cause issues
        test_data = {
            'user_id': 123,
            'username': 'testuser',
            'is_active': True,
            'permissions': ['read', 'write'],
            'metadata': {'created': '2021-01-01', 'version': 1}
        }
        
        # Encode and decode the session data
        encoded_data = session.encode(test_data)
        decoded_data = session.decode(encoded_data)
        
        # The roundtrip should work correctly
        self.assertEqual(decoded_data, test_data)
        
        # Test with empty data
        empty_data = {}
        encoded_empty = session.encode(empty_data)
        decoded_empty = session.decode(encoded_empty)
        self.assertEqual(decoded_empty, empty_data)