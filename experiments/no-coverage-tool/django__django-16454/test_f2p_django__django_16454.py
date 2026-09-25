"""
Regression test for subparser error formatting in Django management commands.

This test focuses on the specific behavior where CommandParser.add_subparsers() 
does not properly inherit parser class and properties for subparsers.

The fix ensures that when CommandParser creates subparsers, they maintain 
the same CommandParser class and properties (missing_args_message, called_from_command_line) 
to provide consistent error formatting.
"""

def test_subparser_parser_class_inheritance():
    """
    Test that subparsers created by CommandParser inherit the CommandParser class.
    
    This behavior change was introduced in the fix to ensure consistent 
    error formatting for subparsers.
    """
    # Note: This test must be run against both before/after the fix
    # It verifies that subparsers are CommandParser instances, not ArgumentParser instances
    
    from django.core.management.base import CommandParser
    from argparse import ArgumentParser
    
    # Test with a CommandParser instance
    parent_parser = CommandParser(
        missing_args_message="Custom missing args error",
        called_from_command_line=True
    )
    
    # Create subparsers
    subparsers = parent_parser.add_subparsers()
    
    # This is the critical point - create a subparser 
    subparser = subparsers.add_parser("test_subcommand")
    
    # The fix ensures this subparser maintains the CommandParser class
    # Before the fix, this would just be ArgumentParser because add_subparsers
    # defaults to creating ArgumentParser instances for subparsers
    assert isinstance(subparser, CommandParser), \
        "Subparser should be CommandParser instance for proper error formatting"
        
    # Subparser should also have the CommandParser's special properties
    assert hasattr(subparser, 'called_from_command_line'), \
        "Subparser should inherit called_from_command_line"
    assert hasattr(subparser, 'missing_args_message'), \
        "Subparser should inherit missing_args_message"
        
    # Verify properties are properly inherited
    assert subparser.called_from_command_line is True
    assert subparser.missing_args_message == "Custom missing args error"