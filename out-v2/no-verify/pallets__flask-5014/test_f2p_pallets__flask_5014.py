import pytest

import flask


def test_blueprint_empty_name_raises_valueerror():
    """Test that creating a Blueprint with an empty name raises ValueError."""
    with pytest.raises(ValueError, match="'name' may not be empty."):
        flask.Blueprint("", __name__)


def test_blueprint_name_cannot_contain_dot():
    """Test that creating a Blueprint with a name containing a dot raises ValueError."""
    with pytest.raises(ValueError, match="'name' may not contain a dot '.' character."):
        flask.Blueprint("invalid.name", __name__)