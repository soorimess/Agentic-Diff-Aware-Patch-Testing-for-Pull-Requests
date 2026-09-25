import pytest

from flask import Blueprint


def test_blueprint_requires_non_empty_name():
    """Test that Blueprint raises ValueError for empty name."""
    with pytest.raises(ValueError, match="'name' may not be empty."):
        Blueprint("", __name__)


def test_blueprint_allows_non_empty_name():
    """Test that Blueprint works fine with non-empty name."""
    bp = Blueprint("test", __name__)
    assert bp.name == "test"