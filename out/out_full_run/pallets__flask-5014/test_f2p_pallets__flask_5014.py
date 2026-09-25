import pytest

from flask import Blueprint


def test_blueprint_requires_non_empty_name():
    """A Blueprint must not be created with an empty name.

    Previously, creating a Blueprint with an empty name succeeded and led to
    incorrect behavior later. The fix raises a ValueError when the name is
    empty. This test asserts that behavior.
    """
    with pytest.raises(ValueError):
        Blueprint("", __name__)
