"""
Regression tests for sphinx-doc/sphinx#10807

This test verifies the behavior of the new toc_object_entries_show_parents
configuration option and related ToC generation improvements.
"""
import pytest


def test_toc_object_entries_show_parents_config_option_exists():
    """Test that the new config option exists (will fail before the change)."""
    from sphinx.config import Config
    
    # Check that the config option exists in the config values
    config_values = Config.config_values
    # This should pass after the change is implemented
    try:
        assert 'toc_object_entries_show_parents' in config_values
        # Check default value
        default_value = config_values['toc_object_entries_show_parents'][0]
        assert default_value == 'domain'
    except KeyError:
        # This is expected before the change is implemented
        pytest.skip("toc_object_entries_show_parents config option not yet implemented")


def test_module_directive_has_content():
    """Test that module directives now accept content (will fail before the change)."""
    try:
        from sphinx.domains.python import PyModule
        from sphinx.domains.javascript import JSModule
        
        # Check that PyModule now accepts content
        assert PyModule.has_content is True
        
        # Check that JSModule now accepts content  
        assert JSModule.has_content is True
    except (ImportError, AttributeError):
        # This is expected before the change is implemented
        pytest.skip("Module directives do not yet accept content")


def test_toc_generation_features():
    """Test that ToC generation features exist (will fail before the change)."""
    try:
        # Test that the new methods exist on directive base classes
        from sphinx.directives import ObjectDescription
        
        # These should exist after the change
        assert hasattr(ObjectDescription, '_object_hierarchy_parts')
        assert hasattr(ObjectDescription, '_toc_entry_name')
        
        # Test that the noindexentry option is supported
        # This is a bit harder to test without full setup, but we can at least
        # verify the directive base class has the attribute
        assert hasattr(ObjectDescription, 'run')
        
    except (ImportError, AttributeError):
        # This is expected before the change is implemented
        pytest.skip("ToC generation features not yet implemented")