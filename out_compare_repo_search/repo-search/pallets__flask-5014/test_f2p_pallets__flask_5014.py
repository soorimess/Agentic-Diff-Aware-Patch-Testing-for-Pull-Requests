import pytest
import flask


def test_blueprint_requires_non_empty_name():
    """Ensure creating a Blueprint with an empty name raises ValueError.

    Before the fix, this would silently succeed and lead to later errors.
    The correct behavior is to raise a ValueError at creation time.
    """
    with pytest.raises(ValueError):
        flask.Blueprint("", __name__)
