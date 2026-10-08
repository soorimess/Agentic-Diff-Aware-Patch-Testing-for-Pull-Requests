import base64
import unittest
from django.contrib.sessions.backends.base import SessionBase
from django.contrib.sessions.serializers import JSONSerializer
from django.test import TestCase


class TestSessionHashingAlgorithm(TestCase):
    """
    Regression test for Django issue #13279.
    Tests that session data can be properly encoded/decoded when
    DEFAULT_HASHING_ALGORITHM is set to 'sha1' for backward compatibility.
    """

    def test_legacy_encode_method_exists_and_works(self):
        """Test that the _legacy_encode method exists and works correctly."""
        # Create a session backend instance
        session = SessionBase()
        session.serializer = JSONSerializer
        
        # Test data
        test_data = {'user_id': 123, 'username': 'testuser', 'is_active': True}
        
        # This test should fail in the pre-fix version because _legacy_encode doesn't exist
        # but should pass in the post-fix version
        try:
            legacy_encoded = session._legacy_encode(test_data)
            self.assertIsInstance(legacy_encoded, str)
            
            # Verify it can be decoded back
            decoded = session._legacy_decode(legacy_encoded)
            self.assertEqual(decoded, test_data)
            
        except AttributeError:
            # This is expected in the pre-fix code
            self.fail("_legacy_encode method should exist after the fix is applied")

    def test_legacy_decode_compatibility(self):
        """Test that legacy encoded data can be decoded properly."""
        # Create a session backend instance
        session = SessionBase()
        session.serializer = JSONSerializer
        
        # Test data
        test_data = {'user_id': 123, 'username': 'testuser', 'is_active': True}
        
        # Manually create legacy format data to test decoding
        # This simulates what would be in the database before the fix
        serialized = JSONSerializer().dumps(test_data)
        hash_value = session._hash(serialized)
        legacy_data = base64.b64encode(hash_value.encode() + b':' + serialized).decode('ascii')
        
        # This should work with legacy decode
        decoded = session.decode(legacy_data)
        self.assertEqual(decoded, test_data)

    def test_encode_decode_basic_functionality(self):
        """
        Test that basic encode/decode functionality works.
        """
        session = SessionBase()
        session.serializer = JSONSerializer
        
        test_data = {'session_key': 'test_value', 'count': 123}
        
        try:
            # Test encoding
            encoded = session.encode(test_data)
            self.assertIsInstance(encoded, str)
            
            # Test decoding
            decoded = session.decode(encoded)
            self.assertEqual(decoded, test_data)
            
        except AttributeError as e:
            # This would happen if _legacy_encode is missing (pre-fix)
            if "_legacy_encode" in str(e):
                self.fail("_legacy_encode method should exist after the fix is applied")
            else:
                raise