import pytest
from flask import Blueprint


def test_blueprint_requires_non_empty_name():
    """Test that Blueprint raises ValueError when name is empty string."""
    with pytest.raises(ValueError, match="'name' may not be empty."):
        Blueprint("", __name__)


def test_blueprint_allows_non_empty_name():
    """Test that Blueprint works normally with non-empty names."""
    # This should work without raising an exception
    bp = Blueprint("valid_name", __name__)
    assert bp.name == "valid_name"