"""
Regression test for Django issue #16454:
Management command subparsers don't retain error formatting

This test verifies that CommandParser properly preserves error formatting
behavior in subparsers by ensuring called_from_command_line is inherited.
"""

from unittest import TestCase
from django.core.management.base import CommandParser


class TestCommandParserSubparsers(TestCase):
    """
    Test for Django issue #16454 where subparsers don't retain error formatting.
    This catches the regression where subparsers don't inherit called_from_command_line.
    """
    
    def test_subparsers_inherit_called_from_command_line_true(self):
        """
        Test that subparsers inherit called_from_command_line=True from parent.
        
        Before fix: subparsers would have called_from_command_line=None
        After fix: subparsers should have called_from_command_line=True
        """
        # Create a CommandParser with called_from_command_line=True
        main_parser = CommandParser(called_from_command_line=True)
        
        # Create subparsers (this is where the bug manifests in the old code)  
        subparsers = main_parser.add_subparsers()
        subparser = subparsers.add_parser('test_sub')
        
        # This assertion will fail if bug exists (subparser has None instead of True)
        self.assertEqual(
            subparser.called_from_command_line, 
            True,
            "Subparser should inherit called_from_command_line=True from parent parser"
        )

    def test_subparsers_inherit_called_from_command_line_false(self):
        """
        Test that subparsers inherit called_from_command_line=False from parent.
        """
        # Create a CommandParser with called_from_command_line=False
        main_parser = CommandParser(called_from_command_line=False)
        
        # Create subparsers 
        subparsers = main_parser.add_subparsers()
        subparser = subparsers.add_parser('test_sub')
        
        # This assertion will fail if bug exists (subparser has None instead of False)  
        self.assertEqual(
            subparser.called_from_command_line, 
            False,
            "Subparser should inherit called_from_command_line=False from parent parser"
        )

    def test_subparsers_inherit_all_error_formatting_attrs(self):
        """
        Test that subparsers inherit all error formatting parameters properly.
        """
        # Create with both relevant parameters
        main_parser = CommandParser(
            called_from_command_line=True,
            missing_args_message="Custom missing args message"
        )
        
        # Create subparsers 
        subparsers = main_parser.add_subparsers()
        subparser = subparsers.add_parser('test_sub')
        
        # Check that the key parameter is preserved
        self.assertEqual(
            subparser.called_from_command_line,
            True,
            "called_from_command_line should be inherited"
        )
        
        # Verify that the main parser's construction attributes are correct
        self.assertEqual(main_parser.called_from_command_line, True)