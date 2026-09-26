import pytest

import flask


def test_blueprint_empty_name_raises_valueerror():
    """Test that creating a Blueprint with an empty name raises ValueError."""
    with pytest.raises(ValueError, match="'name' may not be empty."):
        flask.Blueprint("", __name__)


def test_blueprint_none_name_raises_valueerror():
    """Test that creating a Blueprint with a None name raises ValueError."""
    with pytest.raises(ValueError, match="'name' may not be empty."):
        flask.Blueprint(None, __name__)


def test_blueprint_dot_in_name_raises_valueerror():
    """Test that creating a Blueprint with a dot in name raises ValueError."""
    with pytest.raises(ValueError, match="'name' may not contain a dot '.' character."):
        flask.Blueprint("my.blueprint", __name__)


def test_blueprint_valid_name_works():
    """Test that creating a Blueprint with a valid name works correctly."""
    bp = flask.Blueprint("valid_name", __name__)
    assert bp.name == "valid_name"