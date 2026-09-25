def test_subparser_called_from_command_line():
    """Test that subparsers inherit called_from_command_line from parent."""
    from django.core.management.base import CommandParser
    
    # Check the basic scenario from the bug report
    base_parser = CommandParser(called_from_command_line=True, prog='test_command')
    subparsers = base_parser.add_subparsers(required=True)
    create = subparsers.add_parser("create")
    create.add_argument("name") 
    
    # The key assumption: after the fix, this should not be None
    assert create.called_from_command_line is True
    return True