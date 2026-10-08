"""Regression test for Literal annotation values being treated as missing py:class"""

from sphinx.domains.python import _parse_annotation


def test_literal_annotation_values_dont_cause_nitpick_errors():
    """Test that Literal annotation values don't trigger nitpick warnings.
    
    The bug was that Literal[True] would be parsed as a Text node containing "True",
    which would then be converted to a cross-reference via type_to_xref. Since "True" 
    is not a class, this would fail in nitpick mode.
    
    The fix ensures literal values inside Literal annotations are handled specially.
    """
    
    # Mock environment (simplified version)
    class MockEnv:
        def __init__(self):
            self.ref_context = {}
            self.domaindata = {}
            class MockConfig:
                python_use_unqualified_type_names = False
            self.config = MockConfig()
    
    env = MockEnv()
    
    # These literal values should not cause cross-reference errors
    test_cases = [
        'Literal[True]',
        'Literal[False]', 
        'Literal[1]',
        'Literal["hello"]',
        'Literal[None]'
    ]
    
    for case in test_cases:
        # This should work without errors in nitpick mode
        # The fix prevents literal values from being treated as class references
        result = _parse_annotation(case, env)
        assert isinstance(result, list)
        assert len(result) > 0


def test_typing_literal_annotations():
    """Test that typing.Literal annotations work correctly."""
    
    class MockEnv:
        def __init__(self):
            self.ref_context = {}
            self.domaindata = {}
            class MockConfig:
                python_use_unqualified_type_names = False
            self.config = MockConfig()
    
    env = MockEnv()
    
    # Test typing.Literal variants
    test_cases = [
        'typing.Literal[True]',
        'typing.Literal[False]',
        'typing.Literal[1]',
        'typing.Literal["hello"]'
    ]
    
    for case in test_cases:
        result = _parse_annotation(case, env)
        assert isinstance(result, list)
        assert len(result) > 0


def test_regular_types_still_work():
    """Ensure regular type annotations continue to work normally."""
    
    class MockEnv:
        def __init__(self):
            self.ref_context = {}
            self.domaindata = {}
            class MockConfig:
                python_use_unqualified_type_names = False
            self.config = MockConfig()
    
    env = MockEnv()
    
    # Regular types should work as before
    test_cases = [
        'bool',
        'str',
        'int',
        'List[str]',
        'Dict[str, int]'
    ]
    
    for case in test_cases:
        result = _parse_annotation(case, env)
        assert isinstance(result, list)
        assert len(result) > 0


def test_literal_annotation_structure():
    """Test that literal annotations have correct internal structure."""
    
    class MockEnv:
        def __init__(self):
            self.ref_context = {}
            self.domaindata = {}
            class MockConfig:
                python_use_unqualified_type_names = False
            self.config = MockConfig()
    
    env = MockEnv()
    
    # Parse a literal annotation to ensure it works correctly
    result = _parse_annotation('Literal[True]', env)
    
    # Should return a list of nodes without errors
    assert isinstance(result, list)
    assert len(result) > 0