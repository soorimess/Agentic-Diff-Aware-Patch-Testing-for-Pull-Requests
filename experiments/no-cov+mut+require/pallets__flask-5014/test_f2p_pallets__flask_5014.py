import pytest
import flask


def test_blueprint_empty_name_raises_valueerror():
    """Test that creating a Blueprint with an empty name raises ValueError."""
    with pytest.raises(ValueError, match="'name' may not be empty."):
        flask.Blueprint("", __name__)


def test_blueprint_valid_name_works():
    """Test that creating a Blueprint with a valid name works correctly."""
    bp = flask.Blueprint("valid_name", __name__)
    assert bp.name == "valid_name"


def test_blueprint_name_with_dot_raises_valueerror():
    """Test that creating a Blueprint with a dot in the name raises ValueError."""
    with pytest.raises(ValueError, match="'name' may not contain a dot '.' character."):
        flask.Blueprint("invalid.name", __name__)