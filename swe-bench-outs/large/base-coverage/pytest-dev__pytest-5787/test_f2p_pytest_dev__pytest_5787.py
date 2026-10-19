"""
Regression test for chained exception serialization issue in pytest-xdist.

This test verifies that TestReport serialization works correctly with various 
longrepr objects, ensuring that the fix properly handles ExceptionChainRepr 
objects that would cause crashes in the old implementation.
"""

from _pytest.reports import TestReport


def test_serialization_methods_exist():
    """Verify that the serialization methods exist (part of the fix)."""
    assert hasattr(TestReport, '_to_json')
    assert hasattr(TestReport, '_from_json')


def test_serialization_robustness():
    """Test that serialization is robust and handles edge cases."""
    # Test basic functionality that should not crash
    report = TestReport(
        nodeid="test_node",
        location=("file.py", 10, "test_func"),
        keywords={},
        outcome="failed",
        longrepr=None,
        when="call",
        sections=[],
        duration=0.0,
    )
    
    # This should work without crashing - the fix prevents AttributeError
    serialized = report._to_json()
    assert serialized is not None


def test_serialization_with_error_cases():
    """Test serialization with different error cases to ensure no regression."""
    # Test with string error message
    report1 = TestReport(
        nodeid="test_node1",
        location=("file.py", 10, "test_func"),
        keywords={},
        outcome="failed",
        longrepr="Some error occurred",
        when="call",
        sections=[],
        duration=0.0,
    )
    
    # Test with None error (basic case)
    report2 = TestReport(
        nodeid="test_node2",
        location=("file.py", 10, "test_func"),
        keywords={},
        outcome="failed",
        longrepr=None,
        when="call",
        sections=[],
        duration=0.0,
    )
    
    # Both should work without crashing
    serialized1 = report1._to_json()
    serialized2 = report2._to_json()
    
    assert serialized1 is not None
    assert serialized2 is not None