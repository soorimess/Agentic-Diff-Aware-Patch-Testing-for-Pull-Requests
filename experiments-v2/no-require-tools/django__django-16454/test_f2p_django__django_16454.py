import unittest
from django.core.management.base import CommandParser


class TestSubparserErrorFormatting(unittest.TestCase):
    """Test that subparsers retain error formatting from CommandParser."""

    def test_subparser_inherits_called_from_command_line_parameter(self):
        """
        Test that subparsers inherit the called_from_command_line parameter
        from CommandParser, which is essential for proper error handling.
        
        This test specifically checks the core issue: before the fix, 
        subparsers don't inherit this parameter, causing inconsistent error handling.
        """
        # Create a CommandParser with called_from_command_line=True
        parent_parser = CommandParser(called_from_command_line=True)
        
        # Verify parent has the parameter correctly set
        self.assertTrue(hasattr(parent_parser, 'called_from_command_line'))
        self.assertTrue(parent_parser.called_from_command_line)
        
        # Add subparsers - this is where the bug occurs
        subparsers = parent_parser.add_subparsers(required=True)
        create = subparsers.add_parser("create")
        create.add_argument("name")
        
        # The fix ensures that subparsers inherit the called_from_command_line parameter
        # This assertion should pass after the fix is applied
        self.assertTrue(hasattr(create, 'called_from_command_line'))
        # This is the key assertion that should fail before the fix and pass after
        self.assertTrue(create.called_from_command_line, 
                       "Subparser should inherit called_from_command_line parameter")