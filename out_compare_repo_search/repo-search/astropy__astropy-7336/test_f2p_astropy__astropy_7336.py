# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import pytest

from ... import units as u


def test_quantity_input_allows_init_with_none_return_annotation():
    """
    Regression test for astropy#7336 -- the quantity_input decorator should
    not try to apply a return-unit conversion when the annotated return type
    is ``None`` (as is common for constructors).
    """

    class PoC(object):
        @u.quantity_input
        def __init__(self, voltage: u.V) -> None:
            # store the passed-in quantity so we can inspect it after
            self.voltage = voltage

    # Instantiating should succeed (before the fix this raises AttributeError
    # because the decorator attempts to call ``.to(None)`` on the ``None``
    # returned by __init__).
    p = PoC(1.0 * u.V)

    # Verify that the value was accepted and stored as a Quantity with the
    # expected unit.
    assert isinstance(p.voltage, u.Quantity)
    assert p.voltage.unit is u.V
