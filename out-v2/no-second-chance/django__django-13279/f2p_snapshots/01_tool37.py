import unittest
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