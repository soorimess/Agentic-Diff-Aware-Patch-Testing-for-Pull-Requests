import unittest
from django.core.management.base import CommandParser


class SubparserErrorFormattingTest(unittest.TestCase):
    """Test that management command subparsers retain error formatting."""

    def test_subparser_inherits_commandparser_properties(self):
        """
        Test that subparsers created from CommandParser inherit the parser class
        and called_from_command_line attribute.
        
        Before fix: subparsers were regular ArgumentParser instances
        After fix: subparsers are CommandParser instances with proper attributes
        """
        # Create a CommandParser with called_from_command_line=True
        parser = CommandParser(called_from_command_line=True)
        
        # Add subparsers like in the bug report
        subparsers = parser.add_subparsers(required=True)
        create = subparsers.add_parser("create")
        create.add_argument("name")
        
        # Test that the subparser properly inherits CommandParser properties
        # This is the core of the bug - subparsers should be CommandParser instances
        self.assertIsInstance(create, CommandParser)
        
        # Test that the subparser inherits the called_from_command_line attribute
        # This ensures proper error handling behavior
        self.assertEqual(create.called_from_command_line, True)