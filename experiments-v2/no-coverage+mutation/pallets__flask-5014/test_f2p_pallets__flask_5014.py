import pytest

from flask import Blueprint


def test_blueprint_empty_name_raises_value_error():
    """Test that creating a Blueprint with an empty name raises ValueError."""
    with pytest.raises(ValueError, match="'name' may not be empty."):
        Blueprint("", "test")


def test_blueprint_none_name_raises_value_error():
    """Test that creating a Blueprint with None name raises ValueError."""
    with pytest.raises(ValueError, match="'name' may not be empty."):
        Blueprint(None, "test")


def test_blueprint_valid_name_works():
    """Test that creating a Blueprint with a valid name works correctly."""
    bp = Blueprint("valid_name", "test")
    assert bp.name == "valid_name"