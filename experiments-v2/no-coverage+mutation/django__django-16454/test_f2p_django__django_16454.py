import unittest
from django.core.management.base import CommandParser


class TestSubparserErrorFormatting(unittest.TestCase):
    
    def test_subparser_inherits_called_from_command_line_parameter(self):
        """Test that subparsers inherit the called_from_command_line parameter from parent parser"""
        
        # Create a parent parser with called_from_command_line=True
        parent_parser = CommandParser(called_from_command_line=True)
        
        # Create subparsers - this is where the bug occurs
        subparsers = parent_parser.add_subparsers(required=True)
        subparser = subparsers.add_parser("create")
        subparser.add_argument("name")
        
        # The fix should ensure that subparser inherits the called_from_command_line parameter
        # Before the fix: subparser.called_from_command_line would be None
        # After the fix: subparser.called_from_command_line should be True
        self.assertIsNotNone(subparser.called_from_command_line)
        self.assertEqual(subparser.called_from_command_line, True)
    
    def test_subparser_inherits_called_from_command_line_false(self):
        """Test that subparsers inherit called_from_command_line=False correctly"""
        
        # Create a parent parser with called_from_command_line=False
        parent_parser = CommandParser(called_from_command_line=False)
        
        # Create subparsers 
        subparsers = parent_parser.add_subparsers(required=True)
        subparser = subparsers.add_parser("create")
        subparser.add_argument("name")
        
        # Subparser should inherit the called_from_command_line parameter
        self.assertIsNotNone(subparser.called_from_command_line)
        self.assertEqual(subparser.called_from_command_line, False)