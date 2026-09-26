import pytest

import flask


def test_blueprint_requires_non_empty_name():
    """Test that creating a Blueprint with an empty name raises ValueError."""
    with pytest.raises(ValueError, match="'name' may not be empty."):
        flask.Blueprint("", "test")


def test_blueprint_allows_non_empty_name():
    """Test that creating a Blueprint with a non-empty name works correctly."""
    bp = flask.Blueprint("valid_name", "test")
    assert bp.name == "valid_name"