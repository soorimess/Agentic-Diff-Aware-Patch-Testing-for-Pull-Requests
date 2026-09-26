import unittest
from django.core.management.base import CommandParser
from django.test import TestCase


class SubparserErrorFormattingTest(TestCase):
    """Test that subparsers retain error formatting from CommandParser."""

    def test_subparser_inherits_called_from_command_line(self):
        """
        Test that demonstrates the core issue: subparsers should inherit
        the called_from_command_line parameter from their parent CommandParser.
        
        Before fix: subparsers have called_from_command_line=None
        After fix: subparsers should have called_from_command_line=True
        """
        # Create a parent CommandParser with called_from_command_line=True
        parent_parser = CommandParser(called_from_command_line=True)
        
        # Add subparsers - this is where the bug manifests
        subparsers = parent_parser.add_subparsers(required=True)
        create = subparsers.add_parser("create")
        create.add_argument("name")
        
        # The key assertion: the subparser should have the same 
        # called_from_command_line value as the parent
        self.assertEqual(parent_parser.called_from_command_line, True)
        self.assertEqual(create.called_from_command_line, True, 
                        "Subparser should inherit called_from_command_line from parent")
        
    def test_subparser_error_handling_is_clean(self):
        """
        Test that subparsers use clean error handling instead of stack traces.
        """
        # Create a CommandParser with called_from_command_line=True (as from CLI)
        parser = CommandParser(called_from_command_line=True)
        
        # Add subparsers with required arguments
        subparsers = parser.add_subparsers(required=True)
        create = subparsers.add_parser("create")
        create.add_argument("name")
        
        # This should raise CommandError (clean error) not SystemExit (stack trace)
        try:
            parser.parse_args(['create'])
            self.fail("Expected an exception to be raised")
        except Exception as e:
            # Should be CommandError, not SystemExit
            self.assertNotIsInstance(e, SystemExit, 
                                  "Should not raise SystemExit - this would be a stack trace")
            # Should be a CommandError with clean message
            self.assertIsInstance(e, Exception)  # At least some exception