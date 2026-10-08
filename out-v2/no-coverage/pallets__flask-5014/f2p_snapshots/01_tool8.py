import pytest

import flask


def test_blueprint_empty_name_raises_valueerror():
    """Test that creating a Blueprint with an empty name raises ValueError."""
    with pytest.raises(ValueError, match="'name' may not be empty."):
        flask.Blueprint("", "test")


def test_blueprint_none_name_raises_valueerror():
    """Test that creating a Blueprint with a None name raises ValueError."""
    with pytest.raises(ValueError, match="'name' may not be empty."):
        flask.Blueprint(None, "test")


def test_blueprint_valid_name_works():
    """Test that creating a Blueprint with a valid name works correctly."""
    bp = flask.Blueprint("valid_name", "test")
    assert bp.name == "valid_name"