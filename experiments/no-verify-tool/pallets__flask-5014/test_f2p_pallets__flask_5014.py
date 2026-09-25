import pytest


def test_blueprint_empty_name_raises_valueerror():
    """Test that creating a Blueprint with an empty name raises ValueError.
    
    This is a regression test for the bug where Blueprints could be created
    with empty names, which caused issues (see #4944).
    """
    from flask import Blueprint
    
    # Creating a blueprint with an empty string name should raise ValueError
    with pytest.raises(ValueError, match="'name' may not be empty."):
        Blueprint("", __name__)


def test_blueprint_name_with_dot_still_raises_valueerror():
    """Test that the existing validation for dots in blueprint names still works."""
    from flask import Blueprint
    
    # Creating a blueprint with a dot in name should still raise ValueError
    with pytest.raises(ValueError, match="'name' may not contain a dot '.' character."):
        Blueprint("name.with.dot", __name__)


def test_blueprint_normal_name_works():
    """Test that creating a Blueprint with a normal name works fine."""
    from flask import Blueprint
    
    # This should work fine without any errors
    bp = Blueprint("normal_name", __name__)
    assert bp.name == "normal_name"