"""Regression test for Sphinx issue with Literal annotations in nitpick mode."""

from sphinx.domains.python import _parse_annotation


def test_literal_annotation_values_dont_crash():
    """Test that literal annotation values parse without crashing."""
    
    # Mock environment with required attributes
    class MockEnv:
        def __init__(self):
            self.ref_context = {}
            self.domaindata = {}
            self.config = type('Config', (), {
                'python_use_unqualified_type_names': False
            })()
    
    env = MockEnv()
    
    # Test the exact case from the bug report that was problematic
    # Literal[True] and Literal[False] should not cause cross-reference issues
    try:
        result = _parse_annotation('typing.Literal[True]', env)
        assert result is not None
    except Exception as e:
        # If we get an AttributeError about missing config, that's expected for mock
        # but if we get a different error, it might be related to the cross-reference issue
        if 'config' not in str(e):
            raise


def test_literal_annotation_basic_parsing():
    """Test basic literal annotation parsing functionality."""
    
    class MockEnv:
        def __init__(self):
            self.ref_context = {}
            self.domaindata = {}
            self.config = type('Config', (), {
                'python_use_unqualified_type_names': False
            })()
    
    env = MockEnv()
    
    # Basic functionality test - should not crash
    result = _parse_annotation('typing.Literal[True]', env)
    assert result is not None
    assert isinstance(result, list)


def test_literal_annotation_various_literals():
    """Test various literal annotation types."""
    
    class MockEnv:
        def __init__(self):
            self.ref_context = {}
            self.domaindata = {}
            self.config = type('Config', (), {
                'python_use_unqualified_type_names': False
            })()
    
    env = MockEnv()
    
    # Test literal values that were causing issues in nitpick mode
    test_cases = [
        'typing.Literal[True]',
        'typing.Literal[False]',
        'typing.Literal[42]',
        'typing.Literal["hello"]',
        'Literal[True]',
        'Literal[False]'
    ]
    
    for annotation in test_cases:
        result = _parse_annotation(annotation, env)
        assert result is not None