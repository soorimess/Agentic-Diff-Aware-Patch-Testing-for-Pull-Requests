import pytest

import flask


def test_require_non_empty_blueprint_name():
    """BluePrints must not be created with an empty name.

    Before the fix, creating a Blueprint with an empty name was allowed and
    led to confusing behavior later. The correct behavior is to raise a
    ValueError when an empty name is provided.
    """
    with pytest.raises(ValueError):
        flask.Blueprint("", __name__)
