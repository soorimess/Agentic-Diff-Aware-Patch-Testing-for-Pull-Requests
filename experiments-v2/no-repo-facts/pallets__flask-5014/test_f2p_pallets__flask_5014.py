import pytest

import flask


def test_blueprint_empty_name_raises_value_error():
    """Test that Blueprint with empty name raises ValueError."""
    with pytest.raises(ValueError, match="'name' may not be empty."):
        flask.Blueprint("", __name__)


def test_blueprint_normal_name_works():
    """Test that normal Blueprint names still work."""
    bp = flask.Blueprint("valid_name", __name__)
    assert bp.name == "valid_name"