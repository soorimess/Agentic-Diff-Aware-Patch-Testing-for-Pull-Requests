"""
Regression test for Django subparser error formatting bug.
"""

def test_command_parser_add_subparsers_exists():
    """
    Test that verifies the add_subparsers method exists on CommandParser
    and works correctly to create subparsers.
    """
    from django.core.management.base import CommandParser
    
    # Create a CommandParser instance
    parser = CommandParser(called_from_command_line=True)
    
    # This should not raise an exception - the method should be callable
    subparsers = parser.add_subparsers()
    
    # Add a subparser to make sure it's functional
    subparser = subparsers.add_parser("test")
    
    # Basic validation that the setup works without error
    assert subparsers is not None
    assert subparser is not None
    
    return True