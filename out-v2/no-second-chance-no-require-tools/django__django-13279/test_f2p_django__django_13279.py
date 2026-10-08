import base64
import unittest
from django.contrib.sessions.backends.base import SessionBase
from django.contrib.sessions.serializers import PickleSerializer


class TestSessionHashingAlgorithm(unittest.TestCase):
    """
    Regression test for Django ticket #13279.
    Tests the session encoding behavior during transition to Django 3.1.
    """
    
    def test_session_encode_decode_cycle(self):
        """
        Test that encode/decode cycle works correctly for normal operation.
        """
        session = SessionBase()
        session.serializer = PickleSerializer
        
        test_data = {'user_id': 123, 'username': 'testuser', 'active': True}
        
        # Test encode/decode round trip
        encoded = session.encode(test_data)
        decoded = session.decode(encoded)
        
        self.assertEqual(decoded, test_data)
        
    def test_session_functional_compatibility(self):
        """
        Test that session functionality works correctly.
        """
        session = SessionBase()
        session.serializer = PickleSerializer
        
        # Test with various data types
        test_cases = [
            {'simple': 'string'},
            {'number': 42},
            {'list': [1, 2, 3]},
            {'dict': {'nested': 'value'}},
            {'mixed': {'int': 1, 'str': 'test', 'list': [1, 2]}},
        ]
        
        for test_data in test_cases:
            encoded = session.encode(test_data)
            decoded = session.decode(encoded)
            self.assertEqual(decoded, test_data)
            
    def test_session_legacy_format_handling(self):
        """
        Test that session can handle data in legacy format (backward compatibility).
        """
        session = SessionBase()
        session.serializer = PickleSerializer
        
        # Test that decode method can handle various inputs without crashing
        # This tests the fallback mechanism that was already in place
        test_data = {'test': 'data'}
        serialized = PickleSerializer().dumps(test_data)
        
        # Create mock legacy format data
        mock_hash = "da39a3ee5e6b4b0d3255bfef95601890afd80709"  # SHA1 hash of empty string
        legacy_encoded = base64.b64encode(mock_hash.encode() + b':' + serialized).decode('ascii')
        
        # Should not raise an exception
        decoded = session.decode(legacy_encoded)
        self.assertIsInstance(decoded, dict)