import pytest

import flask


def test_blueprint_requires_non_empty_name():
    """Test that creating a Blueprint with an empty name raises ValueError."""
    with pytest.raises(ValueError, match="'name' may not be empty."):
        flask.Blueprint("", __name__)


def test_blueprint_with_valid_name():
    """Test that creating a Blueprint with a valid name works correctly."""
    bp = flask.Blueprint("valid_name", __name__)
    assert bp.name == "valid_name"


def test_blueprint_with_name_containing_dot():
    """Test that creating a Blueprint with a name containing dot raises ValueError."""
    with pytest.raises(ValueError, match="'name' may not contain a dot '.' character."):
        flask.Blueprint("name.with.dot", __name__)