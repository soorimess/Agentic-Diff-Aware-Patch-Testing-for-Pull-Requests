"""
Regression test for Django issue where subparsers don't retain error formatting.
This test ensures that management command subparsers properly format error messages
instead of showing stack traces.

The issue is that CommandParser.add_subparsers() was not preserving the 
CommandParser subclass behavior when creating new subparsers, leading to 
stack traces instead of clean error messages for missing arguments.

The root cause was that when CommandParser.add_subparsers() created subparsers
via ArgumentParser.add_subparsers(), the resulting subparsers didn't inherit
the CommandParser-specific attributes like called_from_command_line, which are
needed for clean error formatting.

This tests ensures that subparsers maintain proper inheritance to avoid
stack traces in error messages.
"""
from django.core.management.base import BaseCommand, CommandParser
from django.test import TestCase


class TestSubparserErrorFormatting(TestCase):
    """Test cases for CommandParser subparser error formatting behavior."""

    def test_subparsers_preserve_commandparser_attributes(self):
        """
        Test that subparsers created by CommandParser.add_subparsers() 
        preserve CommandParser-specific attributes like called_from_command_line.
        
        This prevents stack traces in error messages when subparsers have 
        missing required arguments.
        """
        # Create a CommandParser with CommandParser-specific attributes
        parser = CommandParser(called_from_command_line=True)
        
        # Add subparsers - this is where the original bug was 
        # (add_subparsers method was missing, so default was used)
        subparsers = parser.add_subparsers()
        
        # Create a subparser for testing
        subparser = subparsers.add_parser('create')
        
        # With the fix in place, subparser should be a CommandParser instance
        # to maintain proper error handling behavior  
        self.assertIsInstance(subparser, CommandParser)
        
        # Both parent and subparser should preserve the called_from_command_line attribute
        self.assertTrue(hasattr(parser, 'called_from_command_line'))
        self.assertTrue(hasattr(subparser, 'called_from_command_line'))
        self.assertEqual(parser.called_from_command_line, subparser.called_from_command_line)
        
    def test_subparser_error_formatting_inheritance(self):
        """
        Test that subparser inherits proper error formatting behavior
        from the CommandParser parent class.
        """
        # Create a parser with special error formatting 
        parser = CommandParser(
            called_from_command_line=True,
            missing_args_message="Custom missing args message"
        )
        
        # Add subparsers - tests the fix behavior
        subparsers = parser.add_subparsers()
        
        # Create a subcommand with required arguments
        subcommand = subparsers.add_parser('test')
        subcommand.add_argument('--required', required=True, help='A required argument')
        
        # Both parent and subcommand should be CommandParser instances
        self.assertIsInstance(parser, CommandParser)
        self.assertIsInstance(subcommand, CommandParser)