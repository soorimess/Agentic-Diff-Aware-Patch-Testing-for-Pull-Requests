"""
Regression test for Flask Blueprint empty name validation.

This test ensures that a ValueError is raised when trying to create a Blueprint
with an empty name, addressing issue #4944.
"""

import pytest

from flask import Blueprint


def test_blueprint_requires_non_empty_name():
    """Test that Blueprint raises ValueError for empty string name."""
    with pytest.raises(ValueError, match="'name' may not be empty."):
        Blueprint("", "test")


def test_blueprint_allows_non_empty_name():
    """Test that Blueprint works fine with non-empty name."""
    # This should not raise an exception
    bp = Blueprint("valid_name", "test")
    assert bp.name == "valid_name"


def test_blueprint_rejects_none_name():
    """Test that Blueprint raises ValueError for None name."""
    with pytest.raises(ValueError, match="'name' may not be empty."):
        Blueprint(None, "test")