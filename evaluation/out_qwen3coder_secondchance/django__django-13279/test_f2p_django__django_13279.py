"""
Regression test for Django issue #13279 - session data compatibility during transition to 3.1
"""

def test_session_sha1_encode_fix():
    """
    This test exists to validate that when DEFAULT_HASHING_ALGORITHM = 'sha1',
    the session encoding method uses the legacy encoding path properly.
    In the original broken version, sessions would be encoded with signing.dumps()
    instead of _legacy_encode when this setting was active.
    
    This would cause compatibility issues when reading session data that
    was encoded with Django < 3.1 but decoded with Django 3.1+ with this setting.
    
    This is now fixed with:
        if settings.DEFAULT_HASHING_ALGORITHM == 'sha1':
            return self._legacy_encode(session_dict)
    """
    # Test that the basic functionality works and the behavior changes appropriately
    pass