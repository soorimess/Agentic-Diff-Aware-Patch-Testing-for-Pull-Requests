import pytest
from flask import Blueprint


def test_blueprint_empty_name_raises_valueerror():
    """Test that creating a Blueprint with an empty name raises ValueError."""
    with pytest.raises(ValueError, match="'name' may not be empty."):
        Blueprint("", __name__)


def test_blueprint_empty_name_in_constructor():
    """Test that Blueprint constructor rejects empty names."""
    with pytest.raises(ValueError, match="'name' may not be empty."):
        Blueprint(name="", import_name=__name__)


def test_blueprint_with_valid_name_works():
    """Test that Blueprint with valid non-empty name works correctly."""
    bp = Blueprint("valid_name", __name__)
    assert bp.name == "valid_name"