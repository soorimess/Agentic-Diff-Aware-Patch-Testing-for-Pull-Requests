"""
Regression test for Django issue #16454: Management command subparsers don't
retain error formatting.

This test verifies that CommandParser properly passes the correct constructor
arguments to subparsers when add_subparsers() is called, ensuring error
messages are user-friendly rather than stack traces.

Issue: Subparsers created via CommandParser.add_subparsers() didn't inherit
the 'called_from_command_line' parameter, causing stack traces instead of
user-friendly usage messages when required arguments are missing.
"""
from unittest import TestCase
from django.core.management.base import CommandParser
from functools import partial


class TestSubparserErrorHandling(TestCase):
    """
    Test the specific behavior changed by the fix to CommandParser.add_subparsers().
    """
    
    def test_add_subparsers_passthrough_attributes(self):
        """
        Test that CommandParser.add_subparsers() passes through required 
        constructor arguments to subparsers.
        """
        # Create a parser instance with specific attributes that should 
        # be passed through to subparsers
        parent_parser = CommandParser(
            called_from_command_line=True,
            missing_args_message="Custom missing args message"
        )
        
        # The fix: when we call add_subparsers, it modifies how subparsers are created
        subparsers = parent_parser.add_subparsers()
        
        # Create a subparser - this is where the test catches the change in behavior
        subparser = subparsers.add_parser('test_command')
        
        # The fix ensures that subparser is properly configured as a CommandParser 
        # with the same attributes as the parent
        
        # Test the core verification that it's a CommandParser instance
        self.assertIsInstance(subparser, CommandParser)
        
        # Test that key attributes are properly passed through (main fix)
        self.assertTrue(hasattr(subparser, 'called_from_command_line'))
        # The primary test - was called_from_command_line copied properly?
        # Without the fix, this would be None or False (because subparser would be 
        # an argparse.ArgumentParser, not a CommandParser)
        self.assertTrue(subparser.called_from_command_line)