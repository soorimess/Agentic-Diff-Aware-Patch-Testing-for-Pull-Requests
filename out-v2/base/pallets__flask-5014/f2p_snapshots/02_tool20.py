import pytest

import flask


def test_blueprint_empty_name_raises_value_error():
    """Test that creating a Blueprint with an empty name raises ValueError."""
    with pytest.raises(ValueError, match="'name' may not be empty."):
        flask.Blueprint("", __name__)


def test_blueprint_none_name_raises_value_error():
    """Test that creating a Blueprint with None name raises ValueError."""
    with pytest.raises(ValueError, match="'name' may not be empty."):
        flask.Blueprint(None, __name__)


def test_blueprint_name_with_dot_raises_value_error():
    """Test that creating a Blueprint with a name containing dot raises ValueError."""
    with pytest.raises(ValueError, match="'name' may not contain a dot"):
        flask.Blueprint("name.with.dot", __name__)


def test_blueprint_valid_name_works():
    """Test that creating a Blueprint with a valid name works correctly."""
    bp = flask.Blueprint("valid_name", __name__)
    assert bp.name == "valid_name"