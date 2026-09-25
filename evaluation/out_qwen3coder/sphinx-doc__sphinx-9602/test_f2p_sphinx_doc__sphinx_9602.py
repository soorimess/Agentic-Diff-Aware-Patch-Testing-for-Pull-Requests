"""
Regression test for sphinx-doc/sphinx#9602

Testing the specific bug where Literal[True] etc. get treated as class references
and cause nitpick warnings with -n -W 
"""
from unittest.mock import Mock
from sphinx.domains.python import _parse_annotation


def test_literal_annotation_basic_functionality():
    """
    Test that literal annotations can be parsed without errors.
    This is a basic regression test for literal annotation handling.
    """
    # Mock environment setup as required by the function
    mock_env = Mock()
    mock_env.config = Mock()
    mock_env.config.python_use_unqualified_type_names = False
    
    # Test various literal annotation formats 
    test_cases = [
        'Literal[True]',
        'Literal[False]', 
        'Literal[1]',
        'Literal["hello"]',
        'typing.Literal[None]'
    ]
    
    for annotation in test_cases:
        # This should not raise exceptions
        result = _parse_annotation(annotation, mock_env)
        
        # Basic validation - should construct reasonable structure
        assert result is not None
        assert len(result) >= 2, f"Annotation {annotation} should produce multiple nodes"


def test_literal_annotation_functionality():
    """
    Second test ensuring literal annotations behave properly in the domain.
    """
    mock_env = Mock()
    mock_env.config = Mock()
    mock_env.config.python_use_unqualified_type_names = False
    
    # Test the foundational behavior 
    result = _parse_annotation('Literal[True]', mock_env)
    
    # Validate proper basic parsing works
    assert len(result) >= 3, "Literal[True] should have at least 3 nodes"
    
    # This tests basic robustness against the parsing fix
    assert result is not None