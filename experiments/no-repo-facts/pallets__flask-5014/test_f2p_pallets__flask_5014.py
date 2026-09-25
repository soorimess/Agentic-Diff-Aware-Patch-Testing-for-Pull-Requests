import pytest
import flask


def test_blueprint_empty_name_raises_valueerror():
    """Test that creating a Blueprint with an empty name raises ValueError."""
    with pytest.raises(ValueError) as exc_info:
        flask.Blueprint("", __name__)
    
    # Check that the error message is correct
    assert "'name' may not be empty." in str(exc_info.value)


def test_blueprint_valid_name_works():
    """Test that creating a Blueprint with a valid name works correctly."""
    bp = flask.Blueprint("valid_name", __name__)
    assert bp.name == "valid_name"


def test_blueprint_name_with_dots_still_raises_valueerror():
    """Test that Blueprint with dots in name still raises ValueError (existing behavior)."""
    with pytest.raises(ValueError, match="'name' may not contain a dot '.' character."):
        flask.Blueprint("invalid.name", __name__)