import pytest
from _pytest.reports import TestReport
from _pytest._code.code import ExceptionChainRepr


def test_chained_exception_serialization_preserves_chain():
    """Test that chained exceptions are properly serialized and deserialized."""
    
    # Create the components needed for ExceptionChainRepr
    from _pytest._code.code import ReprTraceback, ReprFileLocation
    
    # Create minimal reprtraceback objects 
    reprtraceback1 = ReprTraceback([], None, "long")
    reprcrash1 = ReprFileLocation("test_file.py", 5, "ValueError: 21")
    
    reprtraceback2 = ReprTraceback([], None, "long") 
    reprcrash2 = ReprFileLocation("test_file.py", 7, "ValueError: 22")
    
    reprtraceback3 = ReprTraceback([], None, "long")
    reprcrash3 = ReprFileLocation("test_file.py", 9, "ValueError: 23")
    
    # Create the chain in the right order (oldest to newest)
    chain = [
        (reprtraceback1, reprcrash1, None),  # Innermost
        (reprtraceback2, reprcrash2, "During handling of the above exception, another exception occurred:"),  # Middle
        (reprtraceback3, reprcrash3, "During handling of the above exception, another exception occurred:"),  # Outermost
    ]
    
    # Create ExceptionChainRepr
    exception_chain_repr = ExceptionChainRepr(chain)
    
    # Create a TestReport with this exception chain
    report = TestReport(
        nodeid="test_chained_exception",
        location=("test_file.py", 10, "test_function"),
        keywords={},
        outcome="failed",
        longrepr=exception_chain_repr,
        when="call",
        sections=[],
    )
    
    # Test serialization
    serialized = report._to_json()
    
    # Test deserialization
    deserialized = TestReport._from_json(serialized)
    
    # The key assertion: the deserialized report should have the same chain information
    # This is what would fail in the old code - the chain should be preserved
    assert hasattr(deserialized.longrepr, 'chain')
    assert deserialized.longrepr.chain is not None
    assert len(deserialized.longrepr.chain) == 3
    
    # Verify that we get an ExceptionChainRepr back, not a ReprExceptionInfo
    assert isinstance(deserialized.longrepr, ExceptionChainRepr)
    
    # Verify that the chain structure is preserved (not just the count)
    assert deserialized.longrepr.chain[0][2] is None  # First should have no description
    assert deserialized.longrepr.chain[1][2] is not None  # Middle should have description
    assert deserialized.longrepr.chain[2][2] is not None  # Last should have description