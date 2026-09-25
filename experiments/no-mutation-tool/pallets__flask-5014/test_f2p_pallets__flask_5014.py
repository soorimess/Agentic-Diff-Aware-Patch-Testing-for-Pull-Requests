import pytest
from flask import Blueprint


def test_blueprint_empty_name_raises_valueerror():
    """Test that creating a Blueprint with an empty name raises ValueError."""
    with pytest.raises(ValueError, match="'name' may not be empty."):
        Blueprint("", "test")


def test_blueprint_normal_name_works():
    """Test that creating a Blueprint with a normal name works correctly."""
    bp = Blueprint("test_name", "test")
    assert bp.name == "test_name"


def test_blueprint_name_with_dot_raises_valueerror():
    """Test that creating a Blueprint with a name containing a dot raises ValueError."""
    with pytest.raises(ValueError, match="'name' may not contain a dot '.' character."):
        Blueprint("test.name", "test")