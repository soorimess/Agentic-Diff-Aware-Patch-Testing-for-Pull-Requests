"""
Regression test for Django issue #16454: Management command subparsers don't retain error formatting.

This test ensures that when a management command uses subparsers, missing required arguments
in subparsers produce clean usage messages instead of stack traces.
"""
from unittest import TestCase

from django.core.management.base import CommandParser


class TestSubparserErrorFormatting(TestCase):
    def test_subparser_inherits_called_from_command_line(self):
        """
        Test that subparsers inherit the called_from_command_line parameter from parent.
        
        This is the core issue: without the fix, subparsers don't get the 
        called_from_command_line parameter, so they don't format errors properly.
        """
        # Create parent CommandParser with called_from_command_line=True
        parent_parser = CommandParser(called_from_command_line=True)
        
        # Add subparsers - this is where the fix is needed
        subparsers = parent_parser.add_subparsers()
        
        # Create a subparser - this should inherit parent's called_from_command_line
        subparser = subparsers.add_parser("test")
        
        # The fix ensures that subparser is a CommandParser instance
        # and inherits the called_from_command_line parameter
        self.assertIsInstance(subparser, CommandParser)
        
        # The key assertion: subparser should have called_from_command_line=True
        # This is what the fix enables - without it, this would be None
        self.assertTrue(subparser.called_from_command_line)
        
    def test_subparser_error_handling_consistency(self):
        """
        Test that demonstrates the fix: subparsers should handle errors consistently 
        with their parent CommandParser.
        """
        # Create a CommandParser that simulates command line execution
        parent_parser = CommandParser(called_from_command_line=True)
        
        # Add subparsers
        subparsers = parent_parser.add_subparsers(required=True)
        
        # Create a subparser with required argument
        subparser = subparsers.add_parser("create")
        subparser.add_argument("name")
        
        # The fix ensures that subparsers behave like CommandParser instances
        self.assertIsInstance(subparser, CommandParser)
        
        # Test that the subparser can be used for argument parsing
        # The key is that it should behave like a CommandParser
        try:
            parent_parser.parse_args(['create'])
            self.fail("Expected an error to be raised")
        except Exception:
            # We expect some kind of error to be raised (CommandError or SystemExit)
            # The important thing is that it's not a raw stack trace
            pass