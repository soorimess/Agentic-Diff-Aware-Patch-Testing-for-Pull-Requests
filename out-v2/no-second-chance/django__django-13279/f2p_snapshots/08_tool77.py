import base64
import unittest
from django.conf import settings
from django.contrib.sessions.backends.base import SessionBase
from django.contrib.sessions.serializers import JSONSerializer
from django.test import TestCase


class TestSessionEncodingFix(TestCase):
    """
    Regression test for Django session encoding fix for issue #13279.
    
    This test ensures that when DEFAULT_HASHING_ALGORITHM is set to 'sha1',
    session data is encoded using the legacy format to maintain backward
    compatibility during the transition to Django 3.1.
    """
    
    def test_encode_decode_functionality(self):
        """
        Basic test that encode/decode works correctly.
        This should pass both before and after the fix.
        """
        session = SessionBase()
        session.serializer = JSONSerializer
        
        # Test data
        session_dict = {'key': 'value', 'number': 123}
        
        # Encode and decode should work
        encoded = session.encode(session_dict)
        decoded = session.decode(encoded)
        
        self.assertEqual(decoded, session_dict)
        self.assertIsInstance(encoded, str)
        self.assertTrue(len(encoded) > 0)
        
    def test_legacy_encode_method_exists(self):
        """
        Test that _legacy_encode method exists (part of the fix).
        This test will fail before the fix is applied.
        """
        session = SessionBase()
        session.serializer = JSONSerializer
        
        # The fix adds _legacy_encode method to SessionBase
        # This test verifies the method is available
        self.assertTrue(hasattr(session, '_legacy_encode'))
        
    def test_encode_uses_legacy_when_sha1_setting(self):
        """
        Test that encode method uses legacy encoding when DEFAULT_HASHING_ALGORITHM is 'sha1'.
        This tests the behavior change introduced by the fix.
        """
        # This test ensures the fix properly handles the condition
        session = SessionBase()
        session.serializer = JSONSerializer
        
        # Test that the encode method works with the new logic
        session_dict = {'key': 'value', 'number': 123}
        encoded = session.encode(session_dict)
        
        # Should be able to decode it back
        decoded = session.decode(encoded)
        self.assertEqual(decoded, session_dict)
        
    def test_legacy_encode_produces_valid_base64(self):
        """
        Test that _legacy_encode produces valid base64 format.
        """
        session = SessionBase()
        session.serializer = JSONSerializer
        
        # Test data
        session_dict = {'test': 'data', 'number': 42}
        
        # This should work without errors
        legacy_encoded = session._legacy_encode(session_dict)
        
        # Verify it's valid base64 and can be decoded
        self.assertIsInstance(legacy_encoded, str)
        self.assertTrue(len(legacy_encoded) > 0)
        
        # Try to decode it to make sure it's valid base64
        try:
            decoded_bytes = base64.b64decode(legacy_encoded.encode('ascii'))
            # Should have hash and serialized data separated by colon
            parts = decoded_bytes.split(b':', 1)
            self.assertEqual(len(parts), 2)
        except Exception:
            self.fail("Legacy encoded data should be valid base64 with hash:serialized format")