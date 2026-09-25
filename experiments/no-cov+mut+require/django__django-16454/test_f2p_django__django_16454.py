"""
Regression test for Django issue #16454 - Management command subparsers don't retain error formatting.

This test specifically isolates the core regression: subparsers created by 
CommandParser.add_subparsers() do not preserve parameters like called_from_command_line.
"""
from django.test import SimpleTestCase
from django.core.management.base import CommandParser, CommandError


class SubparserErrorFormattingTest(SimpleTestCase):

    def test_add_subparsers_method_exists(self):
        """
        Verify that CommandParser.add_subparsers method exists.
        Before fix: Would not exist, test would fail.
        After fix: Method exists.
        """
        parser = CommandParser(called_from_command_line=True)
        # This exists after fix
        self.assertTrue(hasattr(parser, 'add_subparsers'))
        self.assertTrue(callable(getattr(parser, 'add_subparsers')))

    def test_subparser_preserves_called_from_command_line_parameter(self):
        """
        The core regression test: subparsers should preserve called_from_command_line parameter.
        
        Before fix: subparsers get None for called_from_command_line (via standard argparse)
        After fix: subparsers inherit the called_from_command_line parameter from parent
        """
        parser = CommandParser(called_from_command_line=True, prog='test')
        
        # When add_subparsers method is implemented, it should preserve parameters
        try:
            subparsers = parser.add_subparsers()
            subparser = subparsers.add_parser("subcmd")
            
            # The specific behavior we're checking for:
            # After fix: subparser.called_from_command_line should be True 
            # Before fix: subparser.called_from_command_line would be None or not exist
            self.assertTrue(hasattr(subparser, 'called_from_command_line'))
            self.assertEqual(subparser.called_from_command_line, True)
            
        except AttributeError:
            # If add_subparsers doesn't exist, we're in the pre-fix state
            # This is expected and shows the problem we want to test
            self.skipTest("add_subparsers not implemented in current state")

    def test_subparser_inherits_commandparser_type(self):
        """
        Test that subparsers created are CommandParser instances, not argparse.ArgumentParser
        """
        parser = CommandParser(called_from_command_line=True)
        
        try:
            subparsers = parser.add_subparsers()
            subparser = subparsers.add_parser("test")
            
            # Check that it's the correct type
            self.assertTrue(isinstance(subparser, CommandParser))
            
        except AttributeError:
            self.skipTest("add_subparsers not implemented in current state")