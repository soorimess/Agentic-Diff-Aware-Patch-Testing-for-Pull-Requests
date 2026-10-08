import base64
import unittest
from django.contrib.sessions.backends.base import SessionBase


class TestSessionHashingAlgorithm(unittest.TestCase):
    """
    Regression test for Django issue #13279.
    
    When DEFAULT_HASHING_ALGORITHM is set to 'sha1', session data should be
    encoded using the legacy format to maintain compatibility during the 
    transition to Django 3.1.
    """
    
    def test_legacy_encode_method_exists(self):
        """
        Test that _legacy_encode method exists in SessionBase.
        This method was added to fix the issue with DEFAULT_HASHING_ALGORITHM='sha1'.
        """
        session = SessionBase()
        
        # The fix adds _legacy_encode method to handle old format
        # This should exist in the fixed version but not in the broken version
        self.assertTrue(hasattr(session, '_legacy_encode'), 
                       "The _legacy_encode method should exist in the fixed version")
        
        # Test that it's callable
        self.assertTrue(callable(getattr(session, '_legacy_encode', None)),
                       "_legacy_encode should be callable")
        
    def test_legacy_encode_produces_valid_output(self):
        """
        Test that _legacy_encode produces valid base64 encoded output that can be decoded.
        This verifies the actual functionality of the legacy encoding.
        """
        session = SessionBase()
        session_data = {'user_id': 123, 'username': 'testuser'}
        
        # Test that _legacy_encode method works correctly
        try:
            # Call _legacy_encode directly to test it
            legacy_encoded = session._legacy_encode(session_data)
            
            # The result should be base64 encoded data
            self.assertIsInstance(legacy_encoded, str)
            
            # It should be valid base64 that can be decoded
            decoded_data = base64.b64decode(legacy_encoded.encode('ascii'))
            self.assertIsInstance(decoded_data, bytes)
            
            # Should contain a colon separator
            self.assertIn(b':', decoded_data)
            
        except AttributeError:
            # If _legacy_encode doesn't exist, this is the broken version
            self.fail("The _legacy_encode method should exist to handle sha1 format")
        except Exception as e:
            # If there's any other error, it indicates a broken implementation
            self.fail(f"Legacy encode failed with error: {e}")
            
    def test_encode_method_behavior(self):
        """
        Test that encode method behaves correctly.
        """
        session = SessionBase()
        session_data = {'user_id': 123, 'username': 'testuser'}
        
        # Test that encode method can be called without error
        # This should work in both versions
        encoded = session.encode(session_data)
        self.assertIsInstance(encoded, str)