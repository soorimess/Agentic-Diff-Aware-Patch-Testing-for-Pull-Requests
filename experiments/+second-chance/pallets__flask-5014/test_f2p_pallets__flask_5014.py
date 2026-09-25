"""
Regression test for Flask Blueprint empty name validation.

This test ensures that Blueprint raises a ValueError when created with an empty name,
as per the pull request that adds this validation.
"""
import pytest
from flask import Blueprint


def test_blueprint_empty_name_raises_valueerror():
    """Test that creating a Blueprint with an empty name raises ValueError."""
    with pytest.raises(ValueError, match="'name' may not be empty."):
        Blueprint("", __name__)


def test_blueprint_none_name_raises_valueerror():
    """Test that creating a Blueprint with None name raises ValueError."""
    with pytest.raises(ValueError, match="'name' may not be empty."):
        Blueprint(None, __name__)


def test_blueprint_valid_name_works():
    """Test that creating a Blueprint with a valid name works fine."""
    bp = Blueprint("valid_name", __name__)
    assert bp.name == "valid_name"


def test_blueprint_name_with_dot_raises_valueerror():
    """Test that creating a Blueprint with a name containing a dot raises ValueError."""
    with pytest.raises(ValueError, match="'name' may not contain a dot \'.\' character."):
        Blueprint("invalid.name", __name__)


def test_blueprint_whitespace_name_works():
    """Test that creating a Blueprint with whitespace-only name works (not empty)."""
    bp = Blueprint("   ", __name__)  # whitespace is not empty
    assert bp.name == "   "