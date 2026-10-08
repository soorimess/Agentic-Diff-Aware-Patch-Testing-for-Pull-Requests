import pytest

from flask import Blueprint


def test_blueprint_empty_name_raises_valueerror():
    """Test that creating a Blueprint with an empty name raises ValueError with exact message."""
    with pytest.raises(ValueError) as exc_info:
        Blueprint("", "test")
    assert str(exc_info.value) == "'name' may not be empty."


def test_blueprint_non_empty_name_works():
    """Test that creating a Blueprint with a non-empty name works normally."""
    bp = Blueprint("valid_name", "test")
    assert bp.name == "valid_name"