import pytest
from flask import Blueprint


def test_blueprint_empty_name_raises_valueerror():
    """Test that creating a Blueprint with an empty name raises ValueError."""
    with pytest.raises(ValueError, match="'name' may not be empty."):
        Blueprint("", "test")


def test_blueprint_name_cannot_contain_dot():
    """Test that creating a Blueprint with a name containing a dot raises ValueError."""
    with pytest.raises(ValueError, match="'name' may not contain a dot '.' character."):
        Blueprint("test.name", "test")


def test_blueprint_valid_name_works():
    """Test that creating a Blueprint with a valid name works correctly."""
    bp = Blueprint("valid_name", "test")
    assert bp.name == "valid_name"