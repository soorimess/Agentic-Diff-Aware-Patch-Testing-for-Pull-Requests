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


def test_blueprint_whitespace_name_still_works():
    """Test that whitespace-only names are still allowed (they're not empty)."""
    bp = flask.Blueprint("   ", __name__)
    assert bp.name == "   "


def test_blueprint_valid_name_works():
    """Test that valid blueprint names still work."""
    bp = flask.Blueprint("valid_name", __name__)
    assert bp.name == "valid_name"


def test_blueprint_dot_name_raises_value_error():
    """Test that creating a Blueprint with a name containing a dot raises ValueError."""
    with pytest.raises(ValueError, match="'name' may not contain a dot '.' character."):
        flask.Blueprint("name.with.dot", __name__)